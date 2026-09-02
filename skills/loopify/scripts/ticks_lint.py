#!/usr/bin/env python3
"""
The TICKS.md lint - the log format a loopify brief pins, as code.

TICKS.md is the deliverable a human actually reads, so its shape is fixed rather than free prose:
a durable counter on the first line, then one append-only entry per tick under a header the same
shape every time. skills/loopify/SKILL.md pins that shape; this file checks a log against it:

    python3 scripts/ticks_lint.py <STATE DIR>/TICKS.md

Five checks:
  1. the first line is `tick: N/<cap>` (the durable counter, incremented before any work);
  2. the newest header's number equals N (a header written without bumping the counter, or a
     counter bumped without a header, is the bug this catches); on a log that still starts at
     tick 1, the entry count must equal N too, which a rotated log is exempt from;
  3. header numbers are strictly increasing (the log is append-only, never reordered);
  4. every header carries an ISO-8601 timestamp in its second field;
  5. every header's status is one of changed | noop | stopped, and so is the last one.

Exit 0 = the log obeys the format; 1 = at least one check failed (each failure printed).
No third-party deps; standard library only.
"""
import re
import sys

STATUSES = ("changed", "noop", "stopped")
COUNTER_RE = re.compile(r"^tick:\s*(\d+)\s*/\s*(\d+|<cap>)\s*$")
HEADER_RE = re.compile(r"^##\s+tick\s+(\d+)\s*(?:·|\|)\s*(.+?)\s*(?:·|\|)\s*([A-Za-z]+)\s*$")
# ISO-8601: a date, optionally a T-separated time, optionally an offset or Z.
ISO_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}"
    r"(?:[T ]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?"
    r"(?:Z|[+-]\d{2}:?\d{2})?)?$"
)
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")


def lint_ticks(text):
    """Return (ok, failures). `text` is the whole TICKS.md."""
    failures = []
    lines = text.splitlines()

    # 1. the counter
    first = next((l for l in lines if l.strip()), "")
    m = COUNTER_RE.match(first.strip())
    if not m:
        failures.append("check 1: the first line must be the durable counter `tick: N/<cap>` "
                        f"(got {first.strip()[:60]!r})")
        counter = None
    else:
        counter = int(m.group(1))
        cap = m.group(2)
        if cap != "<cap>" and counter > int(cap):
            failures.append(f"check 1: the counter is past its cap ({counter}/{cap})")

    # collect headers outside fenced code (a brief quoted inside the log is not an entry)
    headers, fence = [], None
    for ln, line in enumerate(lines, 1):
        fm = FENCE_RE.match(line)
        if fm:
            if fence is None:
                fence = fm.group(1)[0]
            elif fm.group(1)[0] == fence:
                fence = None
            continue
        if fence is not None or not line.startswith("## tick"):
            continue
        hm = HEADER_RE.match(line.rstrip())
        if not hm:
            failures.append(f"line {ln}: header must read `## tick <N> · <ISO timestamp> · "
                            f"<{' | '.join(STATUSES)}>` (got {line.strip()[:70]!r})")
            continue
        headers.append((ln, int(hm.group(1)), hm.group(2).strip(), hm.group(3).lower()))

    # 2. the counter agrees with the entries. The counter is DURABLE and survives log rotation
    #    (SKILL.md: past ~500 lines TICKS.md is renamed and a fresh one starts with the counter
    #    line), so a rotated log legitimately holds fewer headers than N. The invariant that
    #    survives rotation is that the newest entry is the tick the counter is on. The stricter
    #    count check applies only to an unrotated log, one that still starts at tick 1.
    if counter is not None and headers:
        if headers[-1][1] != counter:
            failures.append(f"check 2: the counter says tick {counter} but the newest entry is "
                            f"tick {headers[-1][1]}; a tick that bumped the counter without "
                            "logging (or logged without bumping) leaves the stop rule reading the "
                            "wrong number")
        elif headers[0][1] == 1 and len(headers) != counter:
            failures.append(f"check 2: the log starts at tick 1 and has not rotated, so it should "
                            f"hold {counter} entries; it holds {len(headers)}")
    elif counter is not None and counter > 0 and not headers:
        failures.append(f"check 2: the counter says tick {counter} but the log has no entries")

    # 3. strictly increasing
    for (ln, n, _, _), (_, prev, _, _) in zip(headers[1:], headers):
        if n <= prev:
            failures.append(f"line {ln}: tick {n} follows tick {prev}; TICKS.md is append-only, "
                            "so the numbers only go up")

    # 4. ISO timestamps
    for ln, n, stamp, _ in headers:
        if not ISO_RE.match(stamp):
            failures.append(f"line {ln}: tick {n} has no ISO-8601 timestamp (got {stamp[:40]!r})")

    # 5. known statuses, including the last one
    for ln, n, _, status in headers:
        if status not in STATUSES:
            failures.append(f"line {ln}: tick {n} status {status!r} is not one of "
                            f"{' | '.join(STATUSES)}")
    if headers and headers[-1][3] not in STATUSES:
        failures.append(f"check 5: the last tick's status must be one of {' | '.join(STATUSES)}")

    return not failures, failures


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    try:
        with open(argv[1], encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"FAIL: {e}")
        return 1
    ok, failures = lint_ticks(text)
    for f in failures:
        print(f"FAIL: {f}")
    print(f"{'PASS' if ok else 'FAIL'}: ticks lint ({argv[1]})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
