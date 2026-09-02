# Contributing to loopify

Thanks for wanting to help. `loopify` is a Claude Code skill that authors a standing loop **brief**
(a file) plus the one `/loop` **line** (a string) that starts it. A **tick** is one fire of the loop,
and each tick runs one **cycle** of the brief. Because loopify's whole value is **reliable behavior in
ticks that are strangers to the session you prepared in**, it is built carefully and tested-first.
This guide explains how to add to it without breaking that contract.

Contributions of every size are welcome: a sharper trigger, a tighter template clause, a new eval
scenario, a clearer doc, a typo fix. Open an issue first if you want to discuss a larger change.

## Repo layout

```
.claude-plugin/
  plugin.json           the Claude Code manifest (the version 10x pins)
  marketplace.json      the single-plugin marketplace entry
.cursor-plugin/
  plugin.json           the same manifest under Cursor's directory name
.copilot-plugin/
  plugin.json           the same manifest under GitHub Copilot's directory name
skills/loopify/
  SKILL.md              the skill: two phases, the PREPARE procedure, how /loop
                        actually works, the 15-section brief template, the eight
                        loop-line rules, the mode-choice rule, the handoff format
evals/
  check_skill.py        deterministic assertions on SKILL.md (runs in CI)
  loop_line_lint.py     the eight loop-line rules as code; also a CLI for any line
                        you are about to paste (a shim over the copy in skills/)
  scenarios.md          behavioral scenarios + rubrics
  RED-baseline.md       the recorded RED: both deterministic suites + the cold run
  README.md             the two eval layers and how to reproduce them
tests/
  test_manifests.py     manifests, version parity across six manifests, the repo-wide
                        vocabulary lock, the example brief's clauses, the eight rules
                        run as code, i18n parity, the SVG/PNG gate (runs in CI)
  test_ticks_lint.py    the TICKS.md lint against good, rotated and malformed logs
                        (runs in CI)
examples/
  sample-loop-brief.md  an illustrative standing brief in the shape loopify produces
  loop.md               the <= 5-line .claude/loop.md pointer
assets/                 animated SVGs + the 1280x640 social preview card
docs/                   quickstart, limits, faq, editors, other-agents, loop-md, launch
                        (docs/audit/ is a local build journal, gitignored)
READMEs/                zh-CN, ja, es, fr translations of README.md
AGENTS.md               instructions for AI agents working in / invoking this repo
README.md               human-facing overview
llms.txt                the machine-readable map of this repo
LICENSE                 MIT
```

`AGENTS.md` is the source of truth for how the skill behaves and the rules it enforces. Read it before
changing anything in `skills/`.

## We build TEST-FIRST (RED → GREEN → REFACTOR)

This skill exists to fix specific, observed failures. Every guarantee traces back to something we
watched go wrong first.

**The rule: no new behavioral guarantee lands without a failing baseline first.**

The founding baseline is recorded in [`evals/RED-baseline.md`](evals/RED-baseline.md). Asked to
"loopify this: keep our release PR healthy, check it every 20 minutes" with no skill installed, a cold
model wrote a project slash command and handed the user `/loop 15m /pr-health-check`. That one line
carries most of the failures the skill exists to prevent: a **one-shot slash command as the prompt**,
re-invoked every tick; **no standing brief**, so nothing survives the session that produced it; **no
state directory**, so a tick has no memory of the last one; **no tick counter and no tick cap**; **no
stop rule** ("for as long as the loop is left running"); **no tick log**, so there is no proof of what
any tick did; **autonomy set too high by default** — it pushed commits and replied on the PR; and it
**did not know how to stop a loop** ("I'm not fully certain of the exact keystroke"). The deterministic
half of the baseline was recorded the same day, before `skills/loopify/SKILL.md` existed:
`check_skill.py` printed `0/98`, where the 98 was an estimate in the not-found path and not a count
of assertions that ran (see [`evals/RED-baseline.md`](evals/RED-baseline.md)), and
`test_manifests.py` printed `4/17`.

1. **RED — watch it fail.** Before you write skill text, run the scenario against a model that does
   *not* have your change (or doesn't have the skill at all) and record what it does wrong, verbatim.
   Test the weak case too — the skill must hold on cheaper models, not only the strongest one. Ticks
   are the weak case by construction: a fixed-mode fire arrives as a bare prompt with **no skill
   instructions in context**, so anything the tick needs must be in the brief.
2. **GREEN — write the minimum that fixes it.** Add the clause, rail or gate that makes that exact
   failure stop. Re-run the same scenario and show it now behaves. If the change is statically
   checkable, add an assertion to `evals/check_skill.py` (or `tests/test_manifests.py` if it spans
   the repo).
3. **REFACTOR — tighten.** Clean up wording, keep the skill body under 500 lines, deduplicate —
   without changing behavior. Re-run to confirm.

A PR that adds behavior but cites no baseline failure it fixes will be sent back for a RED step.
"I think a model might…" is not a baseline; "here is the model doing it" is.

## Hard rules you must keep

These mirror the skill's rules in `AGENTS.md` / `SKILL.md`. Don't look for loopholes.

- **Description stays WHEN-only.** Do not re-introduce a procedure summary into the `description` (it
  becomes a shortcut models follow instead of reading the body). Keep the disambiguation: goalify and
  `/goal` for a job that finishes, `autopilot` / `ultrawork` / `ralph` for work wanted right now.
- **Tool references must resolve in a fresh tick.** A tick is a stranger to the session that authored
  the brief. Use a capability plus a fallback, or a fully-qualified tool name — never a vague noun.
- **The persistence gate stays low-freedom.** The brief is standing: never archived, moved, deleted or
  rewritten from inside a run, and runs write only under the state directory. Do not soften the
  wording and do not add an escape hatch.
- **The vocabulary lock.** The **brief** is a file; the **line** is a string; a **tick** is one fire; a
  **cycle** is one pass of the brief; state lives in the **state directory**. Never call the line a
  "condition" — that word implies an evaluator `/loop` does not have — and never say that it judges,
  evaluates or checks whether anything is done. `tests/test_manifests.py` scans every tracked text file
  (Markdown, JSON, YAML and source; `tests/` and `evals/` are skipped, because they implement the lock)
  and fails the build on three families. First, *condition* used as the name of the line, in four
  shapes: straight after `/loop`; joined to *loop* by a space or a hyphen; the possessive form; and
  goalify's pairing, brief and the condition, which is allowed only on a line that also names goalify,
  since that contrast is the point of the exception. Second, the affirmative verbs — judges, evaluates,
  checks whether — when they are applied to `/loop`. Third, a bare path handed to `/loop` with no verb.
  Nothing else is caught, so a new way of getting it wrong needs a new pattern rather than a reader's
  goodwill. The `loop-antipattern` marker below is how you write about a banned form on purpose, and
  the test counts every use of it.
- **The `loop-antipattern` marker is for lines that TEACH the wrong form.** To write *about* a banned
  form (a wrong-example fence, the common-mistakes list), put `loop-antipattern` on that line or in the
  fence info string. The test counts those exemptions and pins the count, so the hatch cannot be used
  to smuggle the wrong form back in. Adding one is a deliberate act: confirm the line really teaches
  the wrong form, then bump `EXPECTED_EXEMPTIONS` in the same commit.
- **The eight loop-line rules stay in sync.** They exist twice on purpose: as prose in `SKILL.md`
  ("Loop-line rules") and as code in `evals/loop_line_lint.py`. Change one and you change the other in
  the same PR, with a lint self-test covering the new behavior. `tests/test_manifests.py` runs the code
  form against the shipped example line.
- **No hallucination, anywhere.** No invented flags, behaviors, metrics or "works with X" claims
  without a primary source. Every `/loop` fact in this repo is re-derived from the shipped Claude Code
  2.1.252 binary and https://code.claude.com/docs/en/scheduled-tasks; where the docs and the binary
  disagree (jitter), cite the docs and footnote the binary. Don't bake unverified third-party star or
  usage numbers into docs.
- **Keep the SVGs GitHub-safe.** No `<script>`, no external references, well-formed XML, and a
  `prefers-reduced-motion` guard in every animated one. CI enforces all four.
- **Frontmatter stays spec-clean.** `name` matches the directory and `^[a-z0-9]+(-[a-z0-9]+)*$` (no
  leading, trailing or consecutive hyphens); `description` ≤ 1024 chars; the version lives under
  `metadata` as a quoted string, and it must match `plugin.json`, `marketplace.json` and the latest
  `CHANGELOG.md` entry.

## How to test locally

```bash
# 1. Both deterministic suites must pass.
python3 evals/check_skill.py skills/loopify/SKILL.md      # expect: exit 0, all checks pass
python3 tests/test_manifests.py                           # expect: exit 0, all checks pass
python3 tests/test_ticks_lint.py                          # expect: exit 0, all checks pass

# 2. Lint any line you changed or added, the same way the skill does.
python3 evals/loop_line_lint.py "/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick."

# 3. Run the skill for real: drop it in and exercise the path you changed.
cp -r skills/loopify ~/.claude/skills/loopify
#   then ask Claude Code: "loopify this: <a recurring job that hits your change>"
```

For a behavioral change, re-run the relevant `evals/scenarios.md` case cold (RED) and with the skill
(GREEN) and paste the before/after into your PR. If your change touches what a tick does, read a real
`TICKS.md` afterwards — a loop that runs is not a loop that works.

## Commit and PR etiquette

- Branch off the default branch; don't commit directly to it.
- Keep commits focused; messages say what changed and *why* (link the baseline failure your change
  fixes).
- One logical change per PR. Smaller PRs get reviewed faster.
- In the PR description include: the RED baseline (the failure you observed), the GREEN fix, and how
  you verified it (`check_skill.py` output and/or a sample run).
- Never commit `.loop/` state, a real absolute path from your machine, or anything from `docs/audit/`.
- Be kind in review — see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## CI must pass

Every PR runs `.github/workflows/validate.yml`: the frontmatter check, the `check_skill.py` eval, the
`test_manifests.py` release gate, the loop-line lint on the canonical line, a secrets scan, the markup
safety gate (SVG and HTML, including the reduced-motion guard), the Markdown relative-link check, and
`claude plugin validate` when the CLI is present on the runner. It must be green before merge. If CI
fails, read the log and push a fix; don't ask for a merge override.

Thanks again — careful contributions to a tool people leave running unattended genuinely matter.
