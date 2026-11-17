# LESSONS: what this loop observed about its own method

- 2026-09-01 tick 1: `gh pr checks 412 --required` is enough; the full list wastes a call.
- 2026-09-01 tick 4: a rename touches the test file too; run `npm test` before the commit, not after.
- 2026-09-01 tick 5: an `e2e` failure with a numeric diff is a logic bug. Queue it, do not retry.
- 2026-09-01 tick 7: no lesson this tick.
