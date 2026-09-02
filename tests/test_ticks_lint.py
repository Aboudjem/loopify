#!/usr/bin/env python3
"""
Tests for skills/loopify/scripts/ticks_lint.py (a release gate; runs in CI next to
tests/test_manifests.py).

A good fixture must pass; each bad fixture must fail for its own reason. The point of the lint is
that a tick log stays machine-readable, so a later tick and a human read the same numbers: the
counter, the entry count, the order, the timestamps and the statuses.

Standard library only. Run: python3 tests/test_ticks_lint.py   (exit 0 = all pass)
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills", "loopify", "scripts"))
from ticks_lint import lint_ticks  # noqa: E402

failures = []
_total = 0


def check(name, ok, detail=""):
    global _total
    _total += 1
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        failures.append(name)


GOOD = """tick: 3/30

## tick 1 · 2026-09-02T09:00:00Z · changed
- Rebased onto main; CI green. `gh pr checks 412` -> all checks passed.

## tick 2 · 2026-09-02T09:20:00Z · noop

## tick 3 · 2026-09-02T09:40:00Z · stopped
- PR #412 merged; STOPPED written.
"""

ok, why = lint_ticks(GOOD)
check("a well-formed log passes", ok, "; ".join(why))

# Each bad fixture: (name, text, a substring the failure message must carry)
BAD = [
    ("a missing counter line is caught",
     GOOD.replace("tick: 3/30", "# TICKS"), "check 1"),
    ("headers out of order are caught",
     GOOD.replace("## tick 3 ·", "## tick 2 ·"), "append-only"),
    ("an unknown status is caught",
     GOOD.replace("· changed", "· done"), "not one of"),
    ("a missing timestamp is caught",
     GOOD.replace("2026-09-02T09:00:00Z", "this morning"), "ISO-8601"),
    ("a malformed header is caught",
     GOOD.replace("## tick 2 · 2026-09-02T09:20:00Z · noop", "## tick 2 noop"), "header must read"),
    ("a counter past its cap is caught",
     GOOD.replace("tick: 3/30", "tick: 3/2"), "past its cap"),
]
for name, text, needle in BAD:
    ok, why = lint_ticks(text)
    joined = " ".join(why)
    check(name, (not ok) and needle in joined, f"ok={ok} msgs={joined[:160]}")

# Log rotation: SKILL.md renames TICKS.md past ~500 lines and starts a fresh one carrying the
# durable counter, so a rotated log holds fewer entries than the counter and is still correct.
ROTATED = """tick: 512/600

## tick 511 · 2026-09-02T09:00:00Z · changed
- Carried over after TICKS-2026-09-01.md was rotated out.

## tick 512 · 2026-09-02T09:20:00Z · noop
"""
ok, why = lint_ticks(ROTATED)
check("a rotated log passes (fewer entries than the counter, newest entry matches)", ok,
      "; ".join(why))

# A tick that exits on the LOCK check (STATE increments before that check) bumps the counter and
# never reaches LOG, so the counter legitimately runs ahead of the newest entry.
ok, why = lint_ticks(GOOD.replace("tick: 3/30", "tick: 5/30"))
check("a counter ahead of the newest entry passes (a tick exited on the LOCK check)", ok,
      "; ".join(why))

ok, why = lint_ticks(GOOD.replace("tick: 3/30", "tick: 2/30"))
check("a newest entry ahead of the counter is caught (logged without incrementing)",
      (not ok) and "check 2" in " ".join(why), "; ".join(why))

ok, why = lint_ticks("tick: 4/30\n")
check("a counter above zero with no entries at all is caught",
      (not ok) and "no entries" in " ".join(why), "; ".join(why))

# The counter may carry the template placeholder before the first tick runs.
ok, why = lint_ticks("tick: 0/<cap>\n")
check("a seeded, empty log passes (`tick: 0/<cap>`, no entries)", ok, "; ".join(why))

# A brief quoted inside the log is not an entry.
FENCED = GOOD + "\n```markdown\n## tick 9 · not-a-date · nonsense\n```\n"
ok, why = lint_ticks(FENCED)
check("a `## tick` line inside a fenced block is not counted as an entry", ok, "; ".join(why))

print("-" * 60)
print(f"{_total - len(failures)}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
