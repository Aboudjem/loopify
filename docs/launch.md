# Launch checklist

This tracks every distribution target loopify — and its sibling goalify, for one entry below — can
reach, plus the ready-to-paste text for each. A row's status changes here only once the action it
describes has actually happened, not ahead of it: this file is updated as each step lands, not
written once and left to go stale.

## Targets

| Target | Action | Status | Link |
|---|---|---|---|
| ComposioHQ/awesome-claude-skills | Open a PR from the existing fork `Aboudjem/composio-awesome-claude-skills` (0 commits behind upstream `master`), one README row in category `Productivity & Organization` | done 2026-09-01 — PR open, link-only row under Productivity & Organization | https://github.com/ComposioHQ/awesome-claude-skills/pull/1792 |
| anthropics/skills | Open a PR adding the skill | done 2026-09-01 — PR open; expect a slow review — 861 open PRs against that repo at last check (2026-09-01) | https://github.com/anthropics/skills/pull/1702 |
| Anthropic plugin directory | Submit through the individual-author form (no Team/Enterprise org needed) | done 2026-09-01 — submitted for review from the Console (individual-author form; platform: Claude Code; license MIT; homepage docs/quickstart.md); "Your plugin submission has been received" | https://platform.claude.com/plugins/submit |
| skills.sh | Seed the listing with one real install, `npx skills add Aboudjem/loopify` (the README already carries the skills.sh badge for this repo) | done 2026-09-01 — one real install (`npx -y skills add Aboudjem/loopify -a claude-code -y` → "Installed 1 skill: loopify"); `npx skills find loopify` still lists two unrelated skills of the same name and not this repo — the index is telemetry-driven | https://skills.sh/Aboudjem/loopify |
| hesreallyhim/awesome-claude-code | Web issue form only — their `CONTRIBUTING.md` says PRs aren't accepted here — category `Skills`, ready description below | queued for 2026-09-15 — the repo must be public and 14 days old | https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml |
| skillsmp.com | None — the site auto-crawls listed skills, no submission form exists | auto-crawled — no action | https://skillsmp.com |
| smithery.ai | `smithery mcp publish` or the site's "Publish MCP Server" flow exists, but both are framed around MCP servers, not Agent Skills | unverified — check before acting | https://smithery.ai |
| mcpmarket.com/tools/skills | Unknown — every fetch attempt returned a bot challenge page, site could not be evaluated | unverified — check before acting | https://mcpmarket.com/tools/skills |
| claude-plugins.dev | Unknown — no documented add-your-own path found; the site looks GitHub-crawl-based | unverified — check before acting | https://claude-plugins.dev |
| claudedirectory.org | Likely a PR against `github.com/tmcpa/claudedirectory`, per its `CONTRIBUTING.md` — not yet read | unverified — check before acting | https://github.com/tmcpa/claudedirectory |
| GitHub social preview | Upload `assets/social-preview.png` (1280×640) at Settings → Social preview | done 2026-09-01 — uploaded; the card renders on the settings page | https://github.com/Aboudjem/loopify/settings |
| r/ClaudeCode | Post the draft below — the subreddit's rules could not be fetched on any attempt; check them, logged in, before posting | manual for the user | https://www.reddit.com/r/ClaudeCode |
| r/ClaudeAI | Post the draft below — same caveat, rules could not be fetched; check them, logged in, before posting | manual for the user | https://www.reddit.com/r/ClaudeAI |
| Show HN | Post the draft below | manual for the user | https://news.ycombinator.com/submit |
| X | Post the draft thread below | manual for the user | https://x.com/compose/post |
| Product Hunt | Post the draft below | manual for the user | https://www.producthunt.com/posts/new |

**Ready description for loopify's own `awesome-claude-code` submission** (their style rule: a
description, not a sales pitch; don't address the reader; one line; no emojis):

```
A Claude Code skill that writes a standing brief and one /loop line for jobs that repeat, such as babysitting a release PR or sweeping new bug reports on an interval. Each run of the loop re-reads the brief and logs what happened to a tick file.
```

---

## Ready-to-paste drafts

### 1. Show HN

**Title** (77 chars, ≤ 80):

```
Show HN: loopify – a brief plus one /loop line for repeating Claude Code jobs
```

**Body:**

loopify is a Claude Code skill for jobs that never quite finish: keeping a release PR healthy while
reviews trickle in, watching a deploy settle, sweeping new bug reports every hour, keeping a branch
green overnight.

You run `/loopify` once and describe the job. It reads your project, asks the few real questions —
how often, when to stop, what it can touch — then writes a brief (what one round does, when to stop)
and one line for `/loop`, Claude Code's built-in repeat command. Each firing is a tick: Claude
re-reads the brief, does one round, and logs what happened.

Honest parts: nothing judges whether a tick did the right thing — the log is the only
proof there is. Every `/loop` stops after 7 days. loopify never starts the loop itself.

One recorded run: cold, the release-PR scenario scored 1/7 against the skill's own rubric; with the
skill, 7/7.

Sibling of goalify, same idea for one-shot `/goal` runs.

Repo: https://github.com/Aboudjem/loopify (MIT)

Feedback wanted: does brief-plus-line make sense, or is it one abstraction too many?

### 2. r/ClaudeCode

*Preamble — not part of the post: r/ClaudeCode's self-promotion rules could not be fetched (checked
live and blocked on every attempt — see `docs/audit/distribution-live.md` §7, a local build journal).
Check the subreddit rules, logged in, before posting.*

**Post:**

# loopify: a brief plus one /loop line for jobs that repeat

If you've used `/loop` for a standing job — babysitting a release PR, watching a deploy, sweeping
bug reports hourly — you've hit the gap: `/loop` re-runs a prompt, but a prompt doesn't remember the
last run, doesn't know when to stop, and leaves no record of what happened.

loopify writes two things before the loop starts:

- **A brief** — a standing file: what one round does, what it must never touch, a stop rule.
- **One line for `/loop`**, with the brief's path inside it:

```
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

Every tick re-reads the brief, does one round, and logs it to `TICKS.md` with a running `tick: N/30`
counter. Five safety rails are baked in, including: anything the loop reads is data, never
instructions.

Honest limit: nothing judges whether a tick did good work — you read the log. Every
`/loop` expires after 7 days.

Install: `claude plugin marketplace add Aboudjem/10x` then `claude plugin install loopify@10x`, or
`npx skills add Aboudjem/loopify`. Repo: https://github.com/Aboudjem/loopify

### 3. r/ClaudeAI

*Preamble — not part of the post: r/ClaudeAI's self-promotion rules could not be fetched (checked
live and blocked on every attempt — see `docs/audit/distribution-live.md` §7, a local build journal).
Check the subreddit rules, logged in, before posting.*

**Post:**

loopify is a skill for Claude Code (the CLI) for jobs that repeat instead of finishing once —
keeping a pull request healthy while reviews come in, checking on a deploy, sweeping new bug reports
every hour.

You describe the job once. loopify writes a **brief** (a file with what one round does, and when to
stop) and hands you **one line** to paste into `/loop`, Claude Code's built-in repeat command. Each
firing is a "tick": Claude re-reads the brief, does one round, and logs what happened, so you get a
record instead of a black box.

Honest limits, upfront: nothing checks whether a tick did the right thing — you read the log
yourself — and every `/loop` stops after 7 days no matter what.

If you're on Claude Code: `claude plugin install loopify@10x` (after
`claude plugin marketplace add Aboudjem/10x`). Repo: https://github.com/Aboudjem/loopify

### 4. X (3-tweet thread)

**Tweet 1 (hook):**

```
Claude Code's /loop re-runs a prompt on a schedule. It doesn't remember the last run, doesn't know when to stop, and doesn't log what happened.

loopify writes a standing brief and one /loop line so it does all three. #ClaudeCode
```

**Tweet 2 (the line + what a tick does):**

```
The line loopify hands you:

/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.

Each firing is a tick: re-read the brief, do one round, log it to TICKS.md.
```

**Tweet 3 (honest caveat + CTA):**

```
Honest limit: nothing judges whether a tick did good work — you read the log yourself. Every /loop stops after 7 days regardless.

Repo + install: https://github.com/Aboudjem/loopify
```

### 5. Product Hunt

**Tagline** (47 chars, ≤ 60):

```
A brief and one /loop line for jobs that repeat
```

**Description:**

loopify is a skill for Claude Code that handles jobs which repeat instead of finishing once —
babysitting a release PR, watching a deploy, sweeping bug reports every hour. It writes a standing
brief (what one round does, when to stop) and one line you paste into `/loop`, Claude Code's built-in
repeat command. Every run re-reads the brief and logs what happened, so you come back to a record
instead of a guess.

**First comment:**

loopify is a skill for Claude Code, the CLI, for jobs that never quite finish — keeping a release PR
healthy while reviews trickle in, watching a deploy settle, sweeping new bug reports every hour.

You describe the job once. loopify writes a brief — what one round does, when to stop — and one
line to paste into `/loop`, Claude Code's built-in repeat command. Each run re-reads the brief and
logs what happened, so you get a record instead of a loop you babysit.

Honest limit: nothing judges whether a tick did good work — you read the log. Every `/loop` stops
after 7 days regardless.

Sibling of goalify, same idea for one-shot `/goal` runs. Happy to answer questions.

---

## The goalify entry for awesome-claude-code

**Submitted 2026-09-01 as [issue #2692](https://github.com/hesreallyhim/awesome-claude-code/issues/2692), category
Skills — and auto-closed a minute later.** The validator's log says why: `INELIGIBLE: author has open
submission(s). #1809`. Their workflow rejects any new recommendation while the same author has another
open resource submission, and [#1809](https://github.com/hesreallyhim/awesome-claude-code/issues/1809)
(Humanizer, opened 2026-05-13) is still open. goalify itself meets both written conditions (first commit
2026-05-29, 26 commits since). What the user can do: wait for #1809 to be processed, or close #1809 and
submit goalify again with the values below (a closed issue cannot be reopened by the submitter).


Unlike loopify, goalify doesn't need to wait. It was created 2026-05-29 and pushed to as recently as
2026-08-10, so it already clears the 14-day-old-with-active-development bar on its own, independent
of loopify's release date. A direct check of the live `awesome-claude-code` README turned up zero
mentions of goalify, so it isn't listed yet.

Submit it through the same web form, filled in with these values:

- **Display Name:** `goalify`
- **Category:** `Skills`
- **Link:** `https://github.com/Aboudjem/goalify`
- **Author Name:** `Adam Boudjemaa`
- **Author Link:** `https://github.com/Aboudjem`
- **Description:**

  ```
  goalify writes a self-contained implementation brief and the /goal condition derived from it, so a fresh Claude Code session runs a big task and proves completion.
  ```

Form: https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml
