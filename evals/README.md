# loopify evals

Two layers, both built test-first (RED → GREEN → REFACTOR). The recorded baselines live in
[`RED-baseline.md`](RED-baseline.md).

## 1. Deterministic — runs in CI

### `check_skill.py` — the design lock as assertions on `SKILL.md`

Encodes the locked design as pass/fail checks on `skills/loopify/SKILL.md`. It is the regression
guard: if a future edit drops the WHEN-only description, the vocabulary lock, a `/loop` fact, one of
the 15 template sections, a locked verbatim fragment, one of the eight loop-line rules, the mode-choice
rule, the handoff clauses or a PREPARE rule, CI goes red.

```bash
python3 evals/check_skill.py skills/loopify/SKILL.md      # GREEN: exit 0
```

The GREEN count is whatever the current run prints — **136/136** on the run recorded 2026-09-01 at
v1.0.0. The number moves whenever an assertion is added, which is the point; the exit code is the
gate, not the number.

**The RED.** This suite was written and run before `skills/loopify/SKILL.md` existed. That run printed:

```text
FAIL: skills/loopify/SKILL.md not found
0/98 checks passed for skills/loopify/SKILL.md
```

`98` was an estimate baked into the not-found path, not a count of assertions that ran. The file now
prints `0 checks passed for <path> (nothing to check: RED)` instead: a denominator nobody counted is
exactly the kind of unfalsifiable number `CONTRIBUTING.md` tells contributors not to accept. The real
suite holds 136 assertions today.

Two RED targets you can reproduce right now:

```bash
# (i) the missing-file RED, the original baseline's shape
python3 evals/check_skill.py /nonexistent/loopify/SKILL.md     # exit 1, 0 checks ran

# (ii) a real sibling skill of the wrong shape: goalify's SKILL.md
git clone https://github.com/Aboudjem/goalify /tmp/goalify
python3 evals/check_skill.py /tmp/goalify/skills/goalify/SKILL.md   # exit 1, 31/136 at goalify v2.5.0
```

(ii) is the useful one. goalify is a well-formed, shipping Agent Skill built by the same author to the
same standards, so the 105 assertions it fails are precisely the loopify-specific contract: the story,
the brief-and-line vocabulary, every `/loop` fact, the 15-section standing-brief template, the eight
loop-line rules, the mode check, the pacing rule, the cross-harness table. It passes the generic ones
(spec-clean frontmatter, a body under 500 lines, a documented `$ARGUMENTS`). The exact figure depends
on which goalify version you clone; 31/136 was measured against v2.5.0 on 2026-09-01.

A note on why there is no `git show <first-commit>` recipe: goalify reproduces its RED from its own
history because it has one. loopify is at its first public release, so there is no earlier version of
the skill to score. When v1.1.0 lands, the RED target becomes `git show v1.0.0:skills/loopify/SKILL.md`
and this section should be rewritten to use it.

### `test_manifests.py` — the release gate

Manifest validity, version parity across `SKILL.md`, `plugin.json`, `marketplace.json` and
`CHANGELOG.md`, the repo-wide vocabulary lock (with the `loop-antipattern` exemption count pinned),
the shipped example brief's sections and locked fragments, the eight loop-line rules run as code
against the shipped line, README i18n parity, the SVG and social-preview gate, and a secrets scan.

```bash
python3 tests/test_manifests.py                           # GREEN: exit 0
```

Its RED, recorded the same day against an empty scaffold: **4/17 checks passed, 13 failed** — the three
gate self-tests passed and the secrets scan passed vacuously; everything that needed a real file failed.

### `ticks_lint.py`: the pinned per-tick header as code

`TICKS.md` is what a human reads to find out what the loop did, so its shape is fixed rather than
free prose. `skills/loopify/scripts/ticks_lint.py` checks a log against it: the durable counter on
the first line, the newest entry matching the counter, header numbers that only go up, an ISO
timestamp per header, and a status from the fixed set. A rotated log (the counter keeps climbing
after `TICKS.md` is renamed) passes, which is the case the check is written around.

```bash
python3 skills/loopify/scripts/ticks_lint.py <STATE DIR>/TICKS.md   # exit 0 when the log obeys it
python3 tests/test_ticks_lint.py                                    # the fixtures, in CI
```

### `loop_line_lint.py` — the eight rules as code, and a tool you can run

The same eight rules the skill applies in prose before printing a line. Run it on any line you are
about to paste:

```bash
python3 evals/loop_line_lint.py "/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick."
# PASS: loop-line lint (144 chars)

python3 evals/loop_line_lint.py "/loop 20m /deploy-now"
# FAIL: rule 6: the prompt is a slash command — a one-shot command re-run every tick does its one-shot work every tick
```

An optional second argument is the brief's mode (`fixed` or `self-paced`), which turns on rule 8 — the
line's mode must match the brief's Standing decision 1. Exit 0 = passes, 1 = at least one rule failed.
Notes (rule 7, the cloud caveat for intervals of 60 minutes or more) are advisory and do not fail.

## 2. Behavioral — `scenarios.md` (judged transcripts)

Three scenarios: the core case (a job that repeats), one that must be declined (a one-time reminder),
and one that must be redirected to goalify (a job that finishes). Each has a RED expectation and a
GREEN rubric of seven dimensions, all checkable from a transcript.

**Be honest about what exists here.** The behavioral evidence is **two runs of scenario 1**, both on
sonnet, both 2026-09-01: one cold RED run with no skill installed, and one judged with-skill GREEN run
scored **7/7** by a separate opus judge, `green_beats_red: true`. Both are written up in
[`RED-baseline.md`](RED-baseline.md), §2 and §3. The caveat travels with them: **one model, one
scenario, and no interactive question batch** — the two genuine forks were answered by the skill's own
defaults rather than by a user, so the batch itself is untested, and S2 (must decline) and S3 (must
redirect) have no with-skill transcript on any model. So the eval baseline for v1.0.0 is a static suite
(136 assertions, plus the release gate and the line lint), one cold RED run, and one judged GREEN run
of the same scenario. Recording the full matched set — each scenario, cold and with the skill, on at
least two model tiers, scored by a separate judge — is the top open task for the next release.

To run it yourself: prompt a model twice per scenario, once with no skill and once with
`skills/loopify/SKILL.md` active, against a real project (for S1, a repo with an open PR and CI makes
the authoring dimensions genuinely testable), and score each transcript against the rubric. Never let
the model that produced the transcript score it.
