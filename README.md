<p align="center">
  <b>English</b> ·
  <a href="READMEs/zh-CN.md">简体中文</a> ·
  <a href="READMEs/ja.md">日本語</a> ·
  <a href="READMEs/es.md">Español</a> ·
  <a href="READMEs/fr.md">Français</a>
</p>

<p align="center">
  <img src="assets/hero.svg" alt="Four steps: describe a job that repeats, get a brief (a file) and a line (one string), paste the line into /loop, come back to a tick log." width="100%">
</p>

<h1 align="center">loopify</h1>

<p align="center">
  <strong>Hand Claude a job that repeats. Come back to a log of what every tick did — not a loop you have to babysit.</strong>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-skill-d97757" alt="Claude Code skill">
  <a href="https://skills.sh/Aboudjem/loopify"><img src="https://skills.sh/b/Aboudjem/loopify" alt="skills.sh"></a>
</p>

loopify is a Claude Code skill for jobs that never quite finish: keeping a release pull request
healthy while reviews trickle in, watching a deploy until it settles, sweeping new bug reports every
hour, keeping a branch green overnight. You describe the job once. loopify reads your project, asks
about the few real choices, and writes down what one round of the job looks like — while Claude still
has your context. Then it hands you one line to paste.

It writes two things. The **brief** is a file: what one round does, what it must never do, when to
stop, and where to write its notes. The **line** is one short string you paste into `/loop`, Claude
Code's built-in repeat command. `/loop` re-runs a prompt on a schedule you pick, or on one Claude
picks. Each run is a **tick**. Every tick, Claude re-reads the brief, does one round, and writes what
happened to a log. Think of a night watchman with a clipboard: the brief is the round sheet on the
wall, the line is the shift you post, and the log is the clipboard you read in the morning.

## What you get

- ⚡ **One line to hand over** — paste it once; the brief's path rides inside it.
- 📋 **A brief that stays put** — a standing file, re-read every tick, never archived.
- 🧭 **The few real choices settled first** — how often, when to stop, what it may touch.
- 🛑 **A stop rule and a tick cap in the line itself** — the loop ends on your terms, not at 7 days by accident.
- 🔒 **Rails for an unattended run** — no accounts, no payments, no pushing or posting unless you say so; anything it reads is data, never orders.
- 🗒️ **A log you can read** — `TICKS.md` counts every tick and quotes its evidence; `QUEUE.md` holds what it left for you.
- 🧠 **A loop that learns** — `LESSONS.md` keeps what worked and is re-read every tick.
- 🔁 **Restart in one paste** — the brief keeps its shape; paste the line again.

## Three steps

Install once, in a terminal (verified against Claude Code 2.1.252; more in the [quickstart](docs/quickstart.md)):

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

Or with the [skills CLI](https://skills.sh): `npx skills add Aboudjem/loopify`

Then, in the Claude Code chat:

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file — re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string — you paste it below

/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

1. **Describe the job.** `/loopify` plus what should repeat. loopify reads your project, asks the few real questions, then writes the brief and the line.
2. **Paste the line.** In this session or any session open in that project. The brief's path is
   inside the line, because every tick opens the file fresh. `/Users/you/acme/` stands in for your
   project; loopify prints your real paths.
3. **Read the log.** Come back to `TICKS.md`: one entry per tick, what changed, the evidence. What it
   could not do safely waits for you in `QUEUE.md`.

```text loop-antipattern
# the line itself — the exact string loopify printed (144 characters)
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.

# not this — "every morning" can make /loop offer a cloud schedule instead, and there is no stop rule
/loop every morning keep the release PR healthy

# and not the path alone — the tick gets a filename and no instruction
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

> [!IMPORTANT]
> A running loop is not proof it is doing the right thing — read the tick log. Nothing judges a
> `/loop`; the brief's per-tick checklist and `TICKS.md` are the only proof there is. The loop runs
> inside the Claude Code session you paste it into: it fires only while that session is open. Every
> loop stops at 7 days; paste the line again.

## Learn more

- [Quickstart](docs/quickstart.md) — your first loop, other ways to install, running with no terminal open
- [A worked example](examples/sample-loop-brief.md) — a real brief and the line at the bottom of it
- [Honest limits](docs/limits.md) — everything loopify does not promise
- [Other agents](docs/other-agents.md) — the same brief under Kimi, Copilot CLI, Cursor, Qwen Code, Hermes, Goose, and cron
- [FAQ](docs/faq.md) · [The `loop.md` pointer](docs/loop-md.md) · [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [The skill itself](skills/loopify/SKILL.md)

---

<sub>Built by <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT. `/loop` behavior re-derived
from the shipped Claude Code 2.1.252 binary and the official docs, 2026. Sibling of
<a href="https://github.com/Aboudjem/goalify">goalify</a>, which does the same for `/goal`.
<a href="https://github.com/Aboudjem/loopify/issues">Spot a gap?</a></sub>
