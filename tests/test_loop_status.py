#!/usr/bin/env python3
"""
Tests for skills/loopify/scripts/loop_status.py (a release gate; runs in CI with the other suites).

The status report is what a tired person reads instead of three files, so three things are pinned:
the verdict is the first line, at most three things to do follow it, and each verdict is reached
for its own reason. Every case builds a real state directory in a temp folder.

Standard library only. Run: python3 tests/test_loop_status.py   (exit 0 = all pass)
"""
import datetime
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "skills", "loopify", "scripts")
sys.path.insert(0, SCRIPTS)
from loop_status import build_report, parse_interval, parse_stamp, read_queue  # noqa: E402

failures = []
_total = 0


def check(name, ok, detail=""):
    global _total
    _total += 1
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        failures.append(name)


LINE = ("/loop 20m Run one cycle of /Users/you/acme/.loop/job.md · read it first, "
        "obey its stop rule (30 ticks or the PR merges), log the tick.")
TICKS = """tick: 3/30

## tick 1 · 2026-09-01T09:00 · changed
- fixed the lint failure, committed 4f2a1c9

## tick 2 · 2026-09-01T09:20 · noop

## tick 3 · 2026-09-01T09:40 · changed
- answered one review thread
"""
QUEUE = """# QUEUE

- [tick 2] Post the drafted reply on PR 412
  reason: posting is above the autonomy level
  unblock: post the reply, then delete this item
- [tick 3] The e2e check fails on a real assertion
  reason: a logic bug, not a lint fix
  unblock: fix the rounding in total.ts
- [tick 3] A third thing
  reason: unclear
  unblock: unknown, needs a human to look
"""
NOW = datetime.datetime(2026, 9, 1, 9, 50)


def state(tmp, ticks=TICKS, queue=None, line=LINE, stopped=False, lock=False, slug="job"):
    d = os.path.join(tmp, slug)
    os.makedirs(d, exist_ok=True)
    for name, body in (("TICKS.md", ticks), ("QUEUE.md", queue)):
        if body is not None:
            with open(os.path.join(d, name), "w", encoding="utf-8") as f:
                f.write(body)
    if line:
        with open(os.path.join(tmp, f"LINE-{slug}.txt"), "w", encoding="utf-8") as f:
            f.write(line + "\n")
    for name, on in (("STOPPED", stopped), ("LOCK", lock)):
        if on:
            open(os.path.join(d, name), "w").close()
    return d


def todo_lines(text):
    lines = text.splitlines()
    a, b = lines.index("Do next:"), lines.index("Detail:")
    return [l for l in lines[a + 1:b] if l[:1].isdigit()]


with tempfile.TemporaryDirectory() as tmp:
    verdict, text = build_report(state(tmp), now=NOW)
    check("a recent log with an empty queue is OK", verdict == "OK", text)
    check("the verdict is the first line", text.splitlines()[0].startswith("STATUS: OK"), text)
    check("the first line carries the counter and the last tick",
          "tick 3/30" in text.splitlines()[0] and "2026-09-01T09:40" in text.splitlines()[0], text)
    check("the first line says how long ago the last tick ran", "10 min ago" in text.splitlines()[0], text)
    check("'Do next:' is the second line", text.splitlines()[1] == "Do next:", text)
    check("OK lists between one and three things to do", 1 <= len(todo_lines(text)) <= 3, text)
    check("the interval is read from the saved line", "20m (from the saved line)" in text, text)
    check("the detail counts each status", "3 (2 changed, 1 noop, 0 stopped)" in text, text)
    check("the cap headroom is stated", "27 tick(s) left" in text, text)

with tempfile.TemporaryDirectory() as tmp:
    verdict, text = build_report(state(tmp, queue=QUEUE), now=NOW)
    todo = todo_lines(text)
    check("open queue items make the verdict NEEDS YOU", verdict == "NEEDS YOU", text)
    check("NEEDS YOU lists exactly three things to do", len(todo) == 3, text)
    check("the first thing to do is the oldest queued item", "tick 2: Post the drafted reply" in todo[0], text)
    check("the unblock line of an item is printed under it",
          "   unblock: post the reply, then delete this item" in text, text)
    check("more than two items: the third step points at the rest", "other 1 item(s)" in todo[2], text)
    check("the queue size is on the first line", "3 queued" in text.splitlines()[0], text)

with tempfile.TemporaryDirectory() as tmp:
    d = state(tmp, queue=QUEUE)
    late = datetime.datetime(2026, 9, 1, 10, 30)
    verdict, text = build_report(d, now=late)
    check("no tick for more than two intervals is STALE", verdict == "STALE", text)
    check("STALE tells the user to paste the saved line again", LINE in text, text)
    check("STALE outranks NEEDS YOU, and still names a queued item", "QUEUE.md, tick 2" in text, text)
    verdict, _ = build_report(d, now=datetime.datetime(2026, 9, 1, 10, 20))
    check("exactly two intervals is not yet STALE", verdict == "NEEDS YOU")
    verdict, _ = build_report(d, now=late, interval="1h")
    check("--interval overrides the saved line", verdict == "NEEDS YOU")

with tempfile.TemporaryDirectory() as tmp:
    verdict, text = build_report(state(tmp, line=None), now=datetime.datetime(2026, 9, 3, 9, 0))
    check("with no interval an old log is not called STALE", verdict == "OK", text)
    check("with no interval the report says it cannot tell a live loop from a dead one",
          "cannot tell a live loop from a dead one" in text and "--interval" in text, text)

with tempfile.TemporaryDirectory() as tmp:
    verdict, text = build_report(state(tmp, stopped=True, queue=QUEUE), now=NOW)
    check("a STOPPED file makes the verdict STOPPED", verdict == "STOPPED", text)
    check("STOPPED says how to run the loop again", "delete" in text and "STOPPED" in text and LINE in text, text)
    check("STOPPED outranks STALE", build_report(state(tmp, stopped=True), now=datetime.datetime(2026, 9, 5))[0] == "STOPPED")

with tempfile.TemporaryDirectory() as tmp:
    ended = TICKS.replace("## tick 3 · 2026-09-01T09:40 · changed", "## tick 3 · 2026-09-01T09:40 · stopped")
    check("a last tick marked stopped is STOPPED without the file", build_report(state(tmp, ticks=ended), now=NOW)[0] == "STOPPED")

with tempfile.TemporaryDirectory() as tmp:
    verdict, text = build_report(state(tmp, ticks="tick: 0/30\n"), now=NOW)
    check("a seeded log with no entry is NOT STARTED", verdict == "NOT STARTED", text)
    check("NOT STARTED prints the line to paste", LINE in text, text)
    verdict, text = build_report(state(tmp, ticks=None, slug="empty", line=None), now=NOW)
    check("a state directory with no TICKS.md is NOT STARTED", verdict == "NOT STARTED", text)

with tempfile.TemporaryDirectory() as tmp:
    broken = TICKS.replace("## tick 2 · 2026-09-01T09:20 · noop", "## tick 2 · yesterday · fine")
    verdict, text = build_report(state(tmp, ticks=broken), now=NOW)
    check("a log that fails ticks_lint is BROKEN LOG", verdict == "BROKEN LOG", text)
    check("BROKEN LOG names the lint to run", "ticks_lint.py" in text, text)

with tempfile.TemporaryDirectory() as tmp:
    _, text = build_report(state(tmp, lock=True), now=NOW)
    check("a LOCK file is reported in the detail", "lock          present" in text, text)

with tempfile.TemporaryDirectory() as tmp:
    d = state(tmp, queue=QUEUE)
    before = sorted(os.listdir(d))
    build_report(d, now=NOW)
    check("the report is read-only: the state directory is unchanged", sorted(os.listdir(d)) == before)

check("parse_interval reads 20m, 1h, 90s and 2d",
      [parse_interval(t) for t in ("20m", "1h", "90s", "2d")] == [1200, 3600, 90, 172800])
check("parse_interval rejects words", parse_interval("soon") is None and parse_interval("") is None)
check("parse_stamp reads a naive stamp", parse_stamp("2026-09-01T09:40") == datetime.datetime(2026, 9, 1, 9, 40))
check("parse_stamp returns None for a date with no time", parse_stamp("2026-09-01") is None)
check("parse_stamp reads a Z stamp without raising", parse_stamp("2026-09-01T09:40:00Z") is not None)
items = read_queue(QUEUE)
check("read_queue finds three items with their fields",
      len(items) == 3 and items[0]["tick"] == 2 and items[1]["reason"].startswith("a logic bug")
      and items[2]["unblock"].startswith("unknown"))
check("read_queue ignores a heading and an empty file", read_queue("# QUEUE\n") == [] and read_queue(None) == [])

# --- the command line, as a user runs it ---
SCRIPT = os.path.join(SCRIPTS, "loop_status.py")
EXAMPLE = os.path.join("examples", "loop-state", "pr-babysitter")
run = subprocess.run([sys.executable, SCRIPT, EXAMPLE, "--now", "2026-09-01T09:50"],
                     capture_output=True, text=True, cwd=ROOT)
check("CLI on the shipped example exits 1 (NEEDS YOU)", run.returncode == 1, run.stdout + run.stderr)
check("CLI on the shipped example opens with the verdict",
      run.stdout.startswith("STATUS: NEEDS YOU · tick 7/30 · last tick 2026-09-01T09:40 (changed, 10 min ago) · 2 queued"),
      run.stdout[:200])
readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
check("README.md shows the real output of the shipped example, byte for byte", run.stdout.strip() in readme)
run = subprocess.run([sys.executable, SCRIPT, os.path.join(ROOT, "no-such-dir")], capture_output=True, text=True)
check("CLI on a missing directory exits 2 and says what to pass",
      run.returncode == 2 and "state directory" in run.stdout, run.stdout)
run = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True)
check("CLI with no argument exits 2 with a usage line", run.returncode == 2 and "Usage" in run.stdout, run.stdout)
run = subprocess.run([sys.executable, SCRIPT, EXAMPLE, "--interval", "soon"], capture_output=True, text=True, cwd=ROOT)
check("CLI rejects a bad --interval with an example", run.returncode == 2 and "20m" in run.stdout, run.stdout)

# --- the two lints print their verdict first ---
lint = os.path.join(SCRIPTS, "loop_line_lint.py")
run = subprocess.run([sys.executable, lint, "/loop every morning keep the PR healthy"], capture_output=True, text=True)
out = run.stdout.splitlines()
check("loop-line lint: a bad line exits 1 with the verdict on line 1",
      run.returncode == 1 and out[0].startswith("FAIL: loop-line lint"), run.stdout)
check("loop-line lint: a bad line ends with the shape to copy", out[-1].startswith("Shape to copy: /loop 20m Run one cycle of"), run.stdout)
run = subprocess.run([sys.executable, lint, LINE], capture_output=True, text=True)
check("loop-line lint: a good line prints one PASS line", run.returncode == 0 and run.stdout.strip() == f"PASS: loop-line lint ({len(LINE)} chars)", run.stdout)
tl = os.path.join(SCRIPTS, "ticks_lint.py")
run = subprocess.run([sys.executable, tl, os.path.join(ROOT, "no-such-TICKS.md")], capture_output=True, text=True)
check("ticks lint: a missing file exits 1 and says where the log lives",
      run.returncode == 1 and ".loop/<slug>/TICKS.md" in run.stdout, run.stdout)
run = subprocess.run([sys.executable, tl, os.path.join(ROOT, EXAMPLE, "TICKS.md")], capture_output=True, text=True)
check("ticks lint: the shipped example log passes", run.returncode == 0 and run.stdout.startswith("PASS: ticks lint"), run.stdout)

print("-" * 60)
print(f"{_total - len(failures)}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
