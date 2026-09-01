#!/usr/bin/env python3
"""
loopify skill eval — machine-checkable static assertions on skills/loopify/SKILL.md.

This is the deterministic half of the eval suite. It encodes the design lock (the contract
the adversarial gate approved on 2026-09-01) as pass/fail checks so a regression is caught in
CI. It was written BEFORE the skill existed and run once against the missing file (RED: not found, exit 1);
see evals/RED-baseline.md. The behavioral half — a cold model asked to "loopify" a job with
no skill installed — is recorded in the same file.

Usage:
    python3 evals/check_skill.py [path-to-SKILL.md]   # default: skills/loopify/SKILL.md
Exit code 0 = all checks pass, 1 = at least one failed. Standard library only.
"""
import os
import re
import sys

# Two strings are locked byte-identical across the whole repo (README, SKILL.md, the example
# brief, the tests). They are compared against the RAW text, because the point of locking them
# is that the wording does not drift.
STORY = ("Hand Claude a job that repeats. Come back to a log of what every tick did — "
         "not a loop you have to babysit.")
CANON = ("/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, "
         "obey its stop rule (30 ticks or the PR merges), log the tick.")

# The 14 sections of the brief template, in order (design lock §2.5).
TEMPLATE_SECTIONS = [
    "# LOOP:", "## GOAL (per tick)", "## Standing decisions", "## Hard safety rails",
    "## The cycle", "## State files", "## Per-tick definition of done", "## Stop rule",
    "## Pacing rule", "## Duplicate-tick rule", "## Report-on-stop", "## Persistence gate",
    "## Honest limits", "## Handoff",
]

# Locked verbatim fragments the template must carry (also asserted on the example brief by
# tests/test_manifests.py, so the two cannot drift apart). Matched on a whitespace-collapsed,
# backtick-stripped view.
LOCKED_FRAGMENTS = [
    ("persistence gate, sentence 1",
     "this file is the standing loop brief: never archive, move, delete or rewrite it from inside a run."),
    ("persistence gate, sentence 2", "runs write only under the state directory"),
    ("persistence gate, sentence 3", "proposed brief edits go to queue.md for the human."),
    ("exactly one cycle", "run exactly one cycle"),
    ("7-day restart note", "the loop also dies at the 7-day expiry — paste the line again"),
    ("never ~300 s (5-minute TTL)", "never ~300 s"),
    ("one wakeup only", "one wakeup only"),
    ("LESSONS.md cap", "≤ 150 lines"),
    ("untrusted-content rail", "is data, never instructions"),
    ("never-commit rail", "never stage, commit or push the state directory or this brief"),
    ("durable tick counter", "tick: n/<cap>"),
    ("machine-countable tick header", "## tick <n> ·"),
    ("STOPPED sentinel", "stopped"),
    ("LOCK file", "lock"),
]


def parse_frontmatter(block):
    """Minimal YAML parse for top-level scalars + folded/literal block scalars."""
    data = {}
    lines = block.split("\n")
    i = 0
    key_re = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#") or line[:1] in (" ", "\t"):
            i += 1
            continue
        km = key_re.match(line)
        if not km:
            i += 1
            continue
        key, rest = km.group(1), km.group(2).strip()
        if rest.startswith(("|", ">")):
            collected = []
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt.strip() == "":
                    collected.append("")
                    i += 1
                    continue
                if nxt[:1] in (" ", "\t"):
                    collected.append(nxt.strip())
                    i += 1
                else:
                    break
            data[key] = " ".join(c for c in collected if c != "").strip()
            continue
        val = rest
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
            val = val[1:-1]
        data[key] = val
        i += 1
    return data


def norm(text):
    return re.sub(r"\s+", " ", text).replace("`", "").replace("*", "").lower()


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "skills/loopify/SKILL.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} not found")
        print("-" * 60)
        print(f"0 checks passed for {path} (nothing to check: RED)")
        return 1

    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not m:
        print(f"FAIL: no YAML frontmatter in {path}")
        return 1
    block = m.group(1)
    fm = parse_frontmatter(block)
    body = text[m.end():]
    unquoted = re.sub(r"(?m)^\s{0,3}>\s?", "", body)
    low = norm(unquoted)

    checks = []  # (name, ok, detail)

    # --- Frontmatter (agentskills.io/specification, fetched 2026-09-01) ---
    name = fm.get("name", "")
    checks.append(("name: 1-64 chars, [a-z0-9-], no leading/trailing/double hyphen",
                   bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)) and len(name) <= 64, f"name={name!r}"))
    parent = os.path.basename(os.path.dirname(os.path.abspath(path)))
    checks.append(("name matches the parent directory", name == parent, f"name={name!r} dir={parent!r}"))
    desc = fm.get("description", "")
    checks.append(("description non-empty and <= 1024 chars", bool(desc.strip()) and len(desc) <= 1024, f"len={len(desc)}"))
    checks.append(("metadata.version present, quoted (spec: metadata values are strings)",
                   bool(re.search(r"^\s+version:\s*[\"']\d+\.\d+\.\d+[\"']", block, re.MULTILINE)), ""))
    checks.append(("no bare top-level `version:` field", not re.search(r"^version:", block, re.MULTILINE), ""))
    checks.append(("frontmatter declares license", bool(fm.get("license", "").strip()), ""))
    checks.append(("frontmatter declares argument-hint", bool(fm.get("argument-hint", "").strip()), ""))
    checks.append(("body documents the /loopify command and $ARGUMENTS",
                   "/loopify" in low and "$arguments" in low, ""))

    # --- Description: WHEN-only, branded, disambiguated ---
    dlow = desc.lower()
    checks.append(("description carries the plain-words story VERBATIM", STORY in desc, ""))
    checks.append(("description carries the 'loopify' trigger", "loopify" in dlow, ""))
    checks.append(("description disambiguates vs goalify / /goal (a job that finishes)",
                   "goalify" in dlow and "/goal" in dlow and "finish" in dlow, ""))
    checks.append(("description disambiguates vs autopilot/ultrawork/ralph (do it now)",
                   all(w in dlow for w in ("autopilot", "ultrawork", "ralph")), ""))
    checks.append(("description says it is for a job that REPEATS", "repeat" in dlow, ""))
    checks.append(("description says AUTHOR, does NOT start the loop",
                   "author" in dlow and "not" in dlow and ("start the loop" in dlow or "run the loop" in dlow), ""))
    checks.append(("description is WHEN-only (no numbered steps, no procedure summary)",
                   not re.search(r"\b[1-9]\.\s", desc) and not ("research" in dlow and "question batch" in dlow and "fan" in dlow), ""))

    # --- Overview + vocabulary lock ---
    checks.append(("story appears VERBATIM in the body", STORY.lower() in low, ""))
    checks.append(("vocabulary lock: the brief — a file", "the brief — a file" in low, ""))
    checks.append(("vocabulary lock: the line — a string", "the line — a string" in low, ""))
    checks.append(("vocabulary: a tick, a cycle, the state directory are defined",
                   "a tick" in low and "a cycle" in low and "state directory" in low, ""))
    checks.append(("never calls the line a condition",
                   not re.search(r"/loop\s*<?\s*condition|loop[-\s]+condition|the loop'?s? condition", low), ""))
    checks.append(("never says /loop judges/evaluates/checks whether you're done",
                   not re.search(r"/?loop\s+(judges|evaluates|checks whether)", low), ""))
    checks.append(("no /goal-style language (sentinel word, closeout turn, archive gate, 4,000)",
                   not any(t in low for t in ("sentinel word", "closeout turn", "archive gate", "4,000")), ""))

    # --- Facts about /loop (binary 2.1.252 + docs), all must be stated ---
    facts = {
        "7-day expiry, both modes": "7-day" in low and ("both modes" in low or "self-paced too" in low),
        "session-scoped / open session": "open session" in low or "session-scoped" in low,
        "no evaluator": "no evaluator" in low,
        "loop.md 25,000-byte cut (loop.md only)": "25,000" in low and "loop.md" in low,
        "cloud question is MAY, not WILL": "may be asked" in low,
        "claude -p \"/loop\" fires zero times": "fires zero times" in low or "never fires" in low,
        "Esc stops only self-paced": "esc" in low,
        "fixed needs CronDelete": "crondelete" in low,
        "noop flag": "noop" in low,
        "clamp [60, 3600]": "[60, 3600]" in low,
        "dynamic re-entry: prompt prefixed with /loop": "prefixed" in low and "/loop " in unquoted,
        "fixed re-fire: bare prompt, no skill instructions": "verbatim" in low and "no skill instructions" in low,
        "acceptEdits auto-accepts file edits only": "acceptedits" in low and ("edits only" in low or "file edit" in low),
        "--allowedTools for headless Bash": "--allowedtools" in low,
        "classifier review string labelled uncertain": "classifier" in low and "uncertain" in low,
        "jitter: cite docs (30 minutes), footnote the binary (10 %)": "30 min" in low and ("10 %" in low or "10%" in low),
        "fixed mode fires the first cycle at once": "at once" in low or "immediately" in low,
        "/clear wipes the schedule": "/clear" in low and ("wipes" in low or "kills the schedule" in low),
    }
    for clause, ok in facts.items():
        checks.append((f"fact: {clause}", ok, ""))

    # --- The template, checked in its own scope ---
    tm = re.search(r"^```markdown\s*\n(.*?)\n```\s*$", body, re.DOTALL | re.MULTILINE)
    tmpl = tm.group(1) if tm else ""
    tmpl_low = norm(tmpl)
    checks.append(("template: a fenced ```markdown block exists", bool(tmpl), ""))
    for sec in TEMPLATE_SECTIONS:
        checks.append((f"template section: {sec}", sec.lower() in tmpl_low, ""))
    for label, frag in LOCKED_FRAGMENTS:
        checks.append((f"template locked fragment: {label}", frag in tmpl_low, f"expected {frag!r}"))
    mechanics = {
        "counter incremented BEFORE work": "increment" in tmpl_low and "before" in tmpl_low,
        "mode check with branches (a) (b) (c)": "mode check" in tmpl_low and "(a)" in tmpl_low and "(b)" in tmpl_low and "(c)" in tmpl_low,
        "detection wins over Standing decision 1": "detection wins" in tmpl_low,
        "tick-cap precedence: smaller number wins": "smaller number wins" in tmpl_low,
        "per-tick budget (subagents + minutes)": "per-tick budget" in tmpl_low and "subagents" in tmpl_low,
        "noop-streak backoff": "double the delay" in tmpl_low,
        "Monitor: list running tasks FIRST, arm once": "list running tasks first" in tmpl_low,
        "Monitor cancelled on stop": "cancel any monitor" in tmpl_low,
        "never git add -A / commit -a": "git add -a" in tmpl_low,
        "LESSONS.md provenance: never copy third-party text": "never copy an instruction" in tmpl_low,
        "TICKS.md rotation by rename": "rename" in tmpl_low,
        "state files created if missing": "create any that are missing" in tmpl_low,
        "STOPPED checked first in STATE": "stopped" in tmpl_low and "exists" in tmpl_low,
        "pause-and-queue on the irreversible": "pause-and-queue" in tmpl_low or "pause that item" in tmpl_low,
        "stop rule is dual (wall-clock / tick cap) plus a job condition": "whichever comes first" in tmpl_low and "job condition" in tmpl_low,
        "pacing: 1200–1800 s idle": "1200–1800 s" in tmpl_low or "1200-1800 s" in tmpl_low,
        "pacing: 3600 s sits on the 1-hour cache boundary": "1-hour cache boundary" in tmpl_low,
        "report-on-stop is Done / Proof / Next": "done / proof / next" in tmpl_low,
        "honest limit: a running loop is not proof": "not proof it is doing the right thing" in tmpl_low,
        "honest limit: staleness check (two intervals)": "two intervals" in tmpl_low,
        "template handoff carries the line with the path inside": "run one cycle of <absolute path>" in tmpl_low,
    }
    for clause, ok in mechanics.items():
        checks.append((f"template: {clause}", ok, ""))

    # --- The eight loop-line rules (prose form; the code form is evals/loop_line_lint.py) ---
    rules = {
        "rule 1: interval token regex ^\\d+[smhd]$ or the verb": "^\\d+[smhd]$" in body and "verb" in low,
        "rule 2: Run one cycle of <ABSOLUTE PATH>; ~/ and relative rejected": "run one cycle of" in low and "absolute" in low and "~/" in unquoted and "relative" in low,
        "rule 3: stop rule in a few words + log the tick": "stop rule" in low and "log the tick" in low,
        "rule 4: ≤ 220 characters": "220" in low,
        "rule 5: the five daily phrases, incl. the slug; no bare $": all(p in low for p in ("every morning", "daily", "every day", "each night", "every weekday")) and "slug" in low and "bare $" in low,
        "rule 6: never a one-shot slash command (inert text for non-invocable skills)": "one-shot slash command" in low and "inert" in low,
        "rule 7: ≥ 60 min → cloud caveat, answer This session only, no local files": "this session only" in low and "no local files" in low,
        "rule 8: the line's mode matches Standing decision 1": "standing decision 1" in low and "match" in low,
        "the code form of the lint is named": "loop_line_lint.py" in body,
    }
    for clause, ok in rules.items():
        checks.append((f"loop-line {clause}", ok, ""))
    checks.append(("ships the canonical line, byte-identical", CANON in body, ""))

    # --- Mode-choice rule, pointer option, handoff, PREPARE rules ---
    checks.append(("mode-choice: fixed when the user names a cadence", "names a cadence" in low, ""))
    checks.append(("mode-choice: self-paced when event-gated, with ONE Monitor", "observable event" in low and "monitor" in low, ""))
    checks.append(("mode-choice: ≥ 60 min cadences point at /schedule or Desktop tasks", "/schedule" in low or "routines" in low, ""))
    checks.append(("pointer: .claude/loop.md, ≤ 5 lines", ".claude/loop.md" in low and ("≤ 5" in low or "five lines" in low or "5 lines" in low), ""))
    checks.append(("pointer caveat: ignored the moment a prompt is typed", "ignored" in low, ""))
    checks.append(("pointer caveat: one default per project", "one default per project" in low, ""))
    handoff = {
        "prints the whole line inline": "inline" in low,
        "Permissions line (pre-approve the tick's commands)": "permissions:" in low and "pre-approve" in low,
        "self-paced alternative on one line": "self-paced instead" in low,
        "headless recipe: claude -p + acceptEdits + --allowedTools": "claude -p" in low and "--permission-mode acceptedits" in low and "--allowedtools" in low,
        "stop verification: what scheduled tasks do I have?": "what scheduled tasks do i have" in low,
        "restart after a stop: delete STOPPED": "delete" in low and "stopped" in low,
        "fixed-mode double fire is normal": "two ticks close together" in low,
        "never leaves the user holding only a path": "never" in low and "bare path" in low,
    }
    for clause, ok in handoff.items():
        checks.append((f"handoff: {clause}", ok, ""))
    prepare = {
        "never run /loop or /clear yourself": "never run /loop or /clear yourself" in low,
        "never start the loop": "never start the loop" in low,
        "subagent barrier": "subagent barrier" in low and "still live" in low,
        "live visible progress": "live visible progress" in low,
        "one question batch, ≤ 4 genuine forks": "one question batch" in low or "one interactive batch" in low,
        "bare /loopify finds the purpose itself: inspects the project, proposes jobs, asks which": "propose" in low and "first question" in low,
        "the batch is mandatory when a fork exists; non-interactive runs take defaults out loud and queue them": "cannot ask" in low and "confirm before the first tick" in low,
        "dry run": "dry run" in low,
        "never predict a dollar cost": "never predict a dollar" in low,
        "no secrets in the brief: name where it lives, never its value": "never its value" in low,
        "probe the cycle's commands read-only once": "probe" in low and "read-only" in low,
        "model routing (fast for breadth, deep for the brief)": "fast model" in low and "deep model" in low,
        "3-strike escalation": "3-strike" in low,
        "brief size budget": "12,000" in low or "12 kb" in low,
        ".gitignore created if absent": "create" in low and ".gitignore" in low,
    }
    for clause, ok in prepare.items():
        checks.append((f"PREPARE: {clause}", ok, ""))

    # --- Honest limits + cross-harness + structure ---
    checks.append(("honest limits: read the tick log", "read the tick log" in low, ""))
    checks.append(("honest limits: #64744 quoted only with the 2.1.160 caveat", "2.1.160" in low, ""))
    checks.append(("honest limits: re-fire issues are history", "history" in low and "51304" in low, ""))
    checks.append(("cross-harness names Kimi, Copilot, Cursor, Qwen, Hermes", all(w in low for w in ("kimi", "copilot", "cursor", "qwen", "hermes")), ""))
    checks.append(("cross-harness: Hermes fresh session per fire", "fresh session" in low, ""))
    checks.append(("cross-harness: Qwen prompt-only /loop is fixed 10 min", "10 min" in low or "10-minute" in low, ""))
    checks.append(("SKILL.md body < 500 lines", body.count("\n") < 500, f"{body.count(chr(10))} lines"))

    failed = [c for c in checks if not c[1]]
    for nm, ok, detail in checks:
        tag = "PASS" if ok else "FAIL"
        extra = f"  ({detail})" if detail and not ok else ""
        print(f"{tag}: {nm}{extra}")
    print("-" * 60)
    print(f"{len(checks) - len(failed)}/{len(checks)} checks passed for {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
