#!/usr/bin/env python3
"""
The loop status report: one screen that says how a loopify loop is doing and what to do next.

A loop writes its proof to a state directory (TICKS.md, QUEUE.md, LESSONS.md, plus the LOCK and
STOPPED marker files). Reading three files to learn "is it alive, and does it need me?" is work,
so this prints the answer first:

    python3 scripts/loop_status.py <STATE DIR>
    python3 scripts/loop_status.py <STATE DIR> --interval 20m
    python3 scripts/loop_status.py <STATE DIR> --now 2026-09-01T09:50   (a fixed clock, for tests)

Line 1 is the verdict. Then at most three things to do. Then the detail.

Verdicts:
  OK           ticks are logged, nothing is queued, the last tick is recent
  NEEDS YOU    the loop queued items it would not do alone (QUEUE.md)
  STALE        no tick for more than two intervals: the loop is probably dead
  STOPPED      the loop met its stop rule (a STOPPED file, or a last tick marked stopped)
  NOT STARTED  no tick is logged yet
  BROKEN LOG   TICKS.md does not follow the pinned format (run ticks_lint.py for the lines)

The interval comes from --interval, or from LINE-<slug>.txt beside the state directory, which
loopify writes with the brief. Without an interval the report cannot tell a live loop from a dead
one, and it says so.

Exit 0 = OK, STOPPED or NOT STARTED. Exit 1 = NEEDS YOU, STALE or BROKEN LOG. Exit 2 = usage, or
the state directory does not exist. Read-only: it never writes to the state directory.
No third-party deps; standard library only.
"""
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ticks_lint import COUNTER_RE, HEADER_RE, FENCE_RE, lint_ticks  # noqa: E402

INTERVAL_RE = re.compile(r"^(\d+)([smhd])$")
ITEM_RE = re.compile(r"^\s*[-*]\s+\[tick\s+(\d+)\]\s*(.+?)\s*$")
FIELD_RE = re.compile(r"^\s+(reason|unblock):\s*(.*?)\s*$")
UNIT_SECONDS = {"s": 1, "m": 60, "h": 3600, "d": 86400}
EXIT_CODE = {"OK": 0, "STOPPED": 0, "NOT STARTED": 0, "NEEDS YOU": 1, "STALE": 1, "BROKEN LOG": 1}


def _read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def parse_interval(token):
    """'20m' -> 1200 seconds, or None."""
    m = INTERVAL_RE.match((token or "").strip())
    return int(m.group(1)) * UNIT_SECONDS[m.group(2)] if m else None


def parse_stamp(stamp):
    """An ISO-8601 stamp as a naive local datetime, or None when it carries no time."""
    s = stamp.strip().replace(" ", "T")
    if "T" not in s:
        return None
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    s = re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", s)
    try:
        dt = datetime.datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is not None:
        dt = dt.astimezone().replace(tzinfo=None)
    return dt


def human(seconds):
    seconds = int(max(0, seconds))
    if seconds < 90:
        return f"{seconds} s"
    if seconds < 5400:
        return f"{round(seconds / 60)} min"
    if seconds < 172800:
        return f"{seconds / 3600:.1f} h"
    return f"{seconds / 86400:.1f} days"


def read_ticks(text):
    """Return (counter, cap, entries). An entry is (number, stamp, status)."""
    lines = text.splitlines()
    first = next((l for l in lines if l.strip()), "")
    m = COUNTER_RE.match(first.strip())
    counter, cap = (int(m.group(1)), m.group(2)) if m else (None, None)
    entries, fence = [], None
    for line in lines:
        fm = FENCE_RE.match(line)
        if fm:
            fence = None if fence else fm.group(1)[0]
            continue
        if fence is None:
            hm = HEADER_RE.match(line.rstrip())
            if hm:
                entries.append((int(hm.group(1)), hm.group(2).strip(), hm.group(3).lower()))
    return counter, cap, entries


def read_queue(text):
    """Return the open items of QUEUE.md: dicts with tick, item, reason, unblock."""
    items, cur = [], None
    for line in (text or "").splitlines():
        im = ITEM_RE.match(line)
        if im:
            cur = {"tick": int(im.group(1)), "item": im.group(2), "reason": "", "unblock": ""}
            items.append(cur)
            continue
        fm = FIELD_RE.match(line)
        if fm and cur is not None:
            cur[fm.group(1)] = fm.group(2)
        elif line.strip() and not line.startswith((" ", "\t")):
            cur = None
    return items


def find_line(state_dir):
    """The line loopify saved beside the state directory, or None."""
    state_dir = os.path.abspath(state_dir)
    slug = os.path.basename(state_dir.rstrip(os.sep))
    text = _read(os.path.join(os.path.dirname(state_dir), f"LINE-{slug}.txt"))
    if not text:
        return None
    return next((l.strip() for l in text.splitlines() if l.strip().startswith("/loop ")), None)


def build_report(state_dir, now=None, interval=None):
    """Return (verdict, text). `interval` is a token such as '20m'; `now` is a datetime."""
    now = now or datetime.datetime.now()
    ticks_path = os.path.join(state_dir, "TICKS.md")
    ticks = _read(ticks_path)
    queue = read_queue(_read(os.path.join(state_dir, "QUEUE.md")))
    lessons = _read(os.path.join(state_dir, "LESSONS.md"))
    stopped_file = os.path.exists(os.path.join(state_dir, "STOPPED"))
    lock = os.path.exists(os.path.join(state_dir, "LOCK"))
    line = find_line(state_dir)

    interval_source = "--interval"
    if interval is None and line:
        token = line.split()[1] if len(line.split()) > 1 else ""
        if parse_interval(token):
            interval, interval_source = token, "the saved line"
    step = parse_interval(interval)

    counter, cap, entries = read_ticks(ticks) if ticks is not None else (None, None, [])
    lint_ok, lint_failures = lint_ticks(ticks) if ticks is not None else (True, [])
    last = entries[-1] if entries else None
    last_at = parse_stamp(last[1]) if last else None
    age = (now - last_at).total_seconds() if last_at else None
    stale = bool(step and age is not None and age > 2 * step)
    n_queue = len(queue)
    restart = "paste the line into /loop again" if not line else f"paste this again: {line}"

    if ticks is None or (not entries and not counter):
        verdict = "NOT STARTED"
    elif not lint_ok:
        verdict = "BROKEN LOG"
    elif stopped_file or (last and last[2] == "stopped"):
        verdict = "STOPPED"
    elif stale:
        verdict = "STALE"
    elif n_queue:
        verdict = "NEEDS YOU"
    else:
        verdict = "OK"

    head = [f"STATUS: {verdict}"]
    if counter is not None:
        head.append(f"tick {counter}/{cap}")
    if last:
        when = f", {human(age)} ago" if age is not None else ""
        head.append(f"last tick {last[1]} ({last[2]}{when})")
    head.append(f"{n_queue} queued")

    todo = []
    queue_steps = [
        f"QUEUE.md, tick {q['tick']}: {q['item']}"
        + (f"\n   unblock: {q['unblock']}" if q["unblock"] else "")
        for q in queue
    ]
    if verdict == "NOT STARTED":
        todo.append(f"Start the loop: {restart}" if line else
                    "Start the loop: paste the line loopify printed into /loop.")
        todo.append("Pre-approve the commands the handoff listed, so no tick waits on a prompt.")
        todo.append("Run this report again after the first interval.")
    elif verdict == "BROKEN LOG":
        todo.append(f"See the bad lines: python3 {os.path.join(os.path.dirname(__file__), 'ticks_lint.py')} {ticks_path}")
        todo.append("Do not trust the tick count until the log passes.")
        todo.append("Fix the header shape in the brief, not in the log: TICKS.md is append-only.")
    elif verdict == "STOPPED":
        todo.append(f"Read the Report-on-stop block at the top of {ticks_path}.")
        todo.extend(queue_steps[:1])
        todo.append(f"To run it again: delete {os.path.join(state_dir, 'STOPPED')}, then {restart}")
    elif verdict == "STALE":
        todo.append('Check the session is still open: ask "what scheduled tasks do I have?".')
        todo.append(f"If the list is empty, {restart}")
        todo.extend(queue_steps[:1] or [f"Read tick {last[0]} in {ticks_path} for the last thing it did."])
    elif verdict == "NEEDS YOU":
        todo.extend(queue_steps[:2])
        if n_queue > 2:
            todo.append(f"Then the other {n_queue - 2} item(s) in {os.path.join(state_dir, 'QUEUE.md')}.")
        else:
            todo.append(f"Read tick {last[0]} in {ticks_path} and check its evidence.")
    else:
        todo.append(f"Read tick {last[0]} in {ticks_path} and check its evidence.")
        if cap and cap.isdigit() and counter is not None:
            todo.append(f"{int(cap) - counter} tick(s) left before the cap: raise it in the brief if the job needs more.")
        if not step:
            todo.append("Pass --interval (for example 20m) so this report can tell a live loop from a dead one.")
        else:
            todo.append("Nothing is queued: no action needed from you right now.")

    counts = {s: sum(1 for e in entries if e[2] == s) for s in ("changed", "noop", "stopped")}
    detail = [
        ("ticks logged", f"{len(entries)} ({counts['changed']} changed, {counts['noop']} noop, {counts['stopped']} stopped)"),
        ("queue", f"{n_queue} open item(s)"),
        ("lessons", f"{len([l for l in (lessons or '').splitlines() if l.strip()])} line(s)" if lessons is not None else "no LESSONS.md"),
        ("lock", "present: a tick is mid-cycle, or one crashed" if lock else "none"),
        ("interval", f"{interval} (from {interval_source})" if step else "unknown: cannot tell a live loop from a dead one"),
        ("log format", "passes ticks_lint" if lint_ok else f"{len(lint_failures)} failure(s) in ticks_lint"),
        ("state dir", state_dir),
    ]
    out = [" · ".join(head), "Do next:"]
    out += [f"{i}. {t}" for i, t in enumerate(todo[:3], 1)]
    out.append("Detail:")
    out += [f"  {k:<13} {v}" for k, v in detail]
    return verdict, "\n".join(out)


def main(argv):
    args = argv[1:]
    now, interval, state_dir = None, None, None
    while args:
        a = args.pop(0)
        if a in ("-h", "--help"):
            print(__doc__)
            return 0
        if a in ("--now", "--interval") and args:
            value = args.pop(0)
            if a == "--now":
                now = parse_stamp(value)
                if now is None:
                    print(f"FAIL: --now needs an ISO-8601 date and time, such as 2026-09-01T09:50 (got {value!r})")
                    return 2
            else:
                interval = value
                if parse_interval(interval) is None:
                    print(f"FAIL: --interval needs a number and a unit, such as 20m or 1h (got {value!r})")
                    return 2
        elif state_dir is None and not a.startswith("--"):
            state_dir = a
        else:
            print(f"FAIL: unknown argument {a!r}. Usage: loop_status.py <STATE DIR> [--interval 20m] [--now <ISO>]")
            return 2
    if state_dir is None:
        print("Usage: python3 loop_status.py <STATE DIR> [--interval 20m] [--now <ISO>]")
        print("The state directory is the folder beside the brief, such as <project>/.loop/<slug>/.")
        return 2
    if not os.path.isdir(state_dir):
        print(f"FAIL: {state_dir} is not a directory.")
        print("Pass the state directory loopify printed in its handoff, such as <project>/.loop/<slug>/.")
        return 2
    verdict, text = build_report(state_dir, now=now, interval=interval)
    print(text)
    return EXIT_CODE[verdict]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
