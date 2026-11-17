#!/usr/bin/env python3
"""A /loop fact dated to an older Claude Code version must say so wherever it is stated.

docs/limits.md ends with a per-fact table ("Which version each fact was checked on"). The newest
version in that table is the current one. A row with an older version was not re-checked there.
For every such row, each place in SKILL.md, docs/faq.md and docs/limits.md that states the fact
(found by a short list of key phrases) must name that older version within WINDOW characters.

Run: python3 tests/test_dated_facts.py   (exit 0 = pass, 1 = fail). Standard library only.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIMITS = ROOT / "docs" / "limits.md"
FILES = [ROOT / "skills" / "loopify" / "SKILL.md", ROOT / "docs" / "faq.md", LIMITS]
WINDOW = 250  # characters on either side of the phrase

# Table row (the "Fact" cell, as written) -> regular expressions that state the fact in running
# text, matched case-insensitively. Keep a row here even once it is current: if it is
# ever dated back, the test starts guarding it again with no edit.
KEY_PHRASES = {
    "`/clear` wipes the schedule": [r"/clear\W{0,8}(which )?wipe"],
    "First fire at once in fixed mode": [
        r"runs the first cycle at once",
        r"prompt runs \*\*at once\*\*",
        r"runs the prompt immediately",
    ],
    "The cloud-schedule question and its seven conditions": [
        "seven runtime conditions",
        "seven runtime checks",
        "cloud schedule or this session only",
    ],
    "`acceptEdits` scope under `claude -p`": [
        r"acceptedits` auto-accepts",
        r"acceptedits` covers",
    ],
}

ROW_RE = re.compile(r"^\| (?P<fact>.+?) \| (?P<ver>\d+\.\d+\.\d+), (?P<date>\d{4}-\d{2}-\d{2}) \|", re.M)


def vkey(v):
    return tuple(int(x) for x in v.split("."))


def table_rows(text):
    start = text.find("## Which version each fact was checked on")
    if start < 0:
        raise SystemExit("FAIL: docs/limits.md has no 'Which version each fact was checked on' section")
    return start, [(m.group("fact"), m.group("ver"), m.group("date")) for m in ROW_RE.finditer(text, start)]


def main():
    failures = []
    limits_text = LIMITS.read_text(encoding="utf-8")
    table_start, rows = table_rows(limits_text)
    if not rows:
        print("FAIL: the per-fact table in docs/limits.md has no rows")
        return 1
    current = max((r[1] for r in rows), key=vkey)
    dated = [r for r in rows if vkey(r[1]) < vkey(current)]
    checked = 0
    for fact, ver, date in dated:
        phrases = KEY_PHRASES.get(fact)
        if not phrases:
            failures.append(f"row '{fact}' is dated {ver} but has no key phrases in this test: add some")
            continue
        for path in FILES:
            text = path.read_text(encoding="utf-8")
            if path == LIMITS:
                text = text[:table_start]  # the table itself carries the version by construction
            low = text.lower()
            for phrase in phrases:
                for m in re.finditer(phrase, low):
                    checked += 1
                    lo, hi = max(0, m.start() - WINDOW), m.end() + WINDOW
                    if ver not in text[lo:hi]:
                        line = text.count("\n", 0, m.start()) + 1
                        rel = path.relative_to(ROOT)
                        failures.append(f"{rel}:{line}: states '{fact}' ('{phrase}') without its version {ver} nearby")
    for f in failures:
        print(f"FAIL: {f}")
    status = "PASS" if not failures else "FAIL"
    print(f"{status}: dated facts: {len(dated)} row(s) older than {current}, "
          f"{checked} mention(s) checked, {len(failures)} failure(s)")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
