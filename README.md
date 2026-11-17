<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
    <img src="assets/hero-light.svg" alt="loopify banner: the headline Your loop, in one line; three chips No babysitting, Fewer stuck ticks, Stops by itself; a ring of 30 tick dots with 7 done; the install command and the status line STATUS: NEEDS YOU, tick 7/30." width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
</p>

<p align="center">
  <b>English</b> · <a href="READMEs/zh-CN.md">简体中文</a> · <a href="READMEs/ja.md">日本語</a> · <a href="READMEs/es.md">Español</a> · <a href="READMEs/fr.md">Français</a>
</p>

<p align="center"><strong>Check a repeating agent job in one line.</strong></p>

<p align="center">
  <a href="#install">Install</a> · <a href="#how-it-works">How it works</a> · <a href="#what-you-get">What you get</a> · <a href="#works-with">Works with</a> · <a href="#proof">Proof</a> · <a href="#faq">FAQ</a> · <a href="#limits">Limits</a>
</p>

loopify writes the `/loop` line and the brief. Then one command reads the log for you.

| No babysitting | Fewer stuck ticks | Stops by itself |
|:--|:--|:--|
| `loop_status.py` prints one of six verdicts, then up to three things to do. | loopify prints the commands to allow first, such as `gh pr view`. | The line carries a stop rule. Every `/loop` ends after 7 days. |

A tick is one run of the repeating job. `make test` checks every verdict and exit code.

**Works with:** Claude Code's `/loop`. The skill installs in any agent that reads skills. Install tested: Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode. It is not tied to one model: it is Markdown and three plain Python scripts.

```bash
npx skills add Aboudjem/loopify -g -a claude-code
# then, in Claude Code: /loopify keep our release PR healthy, every 20 minutes
```

The status command, run on the example that ships in this repo:

```bash
python3 skills/loopify/scripts/loop_status.py examples/loop-state/pr-babysitter --now 2026-09-01T09:50
```

```text
STATUS: NEEDS YOU · tick 7/30 · last tick 2026-09-01T09:40 (changed, 10 min ago) · 2 queued
Do next:
1. QUEUE.md, tick 4: Post the drafted reply on the `fetchAll` rename thread of PR #412
```

`--now` pins the clock, so the example prints `NEEDS YOU` every time.

**What it is:** a skill that writes the brief and the line for Claude Code's `/loop`.
**When to use it:** for a job that repeats, like watching a pull request all afternoon.
**What you get:** one status line that says if the loop needs you.

The loop lives in your open session and ends after 7 days.

## Install

**Pick your agent.** Each command installs loopify for all your projects.

<p align="center">
  <a href="#install-claude-code"><img src="https://img.shields.io/badge/Claude_Code-D97757?style=for-the-badge&logo=claude&logoColor=white" alt="Claude Code"></a>
  <a href="#install-codex"><img src="https://img.shields.io/badge/Codex-000000?style=for-the-badge&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyBmaWxsPSJ3aGl0ZSIgcm9sZT0iaW1nIiB2aWV3Qm94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI%2BPHRpdGxlPk9wZW5BSTwvdGl0bGU%2BPHBhdGggZD0iTTIyLjI4MTkgOS44MjExYTUuOTg0NyA1Ljk4NDcgMCAwIDAtLjUxNTctNC45MTA4IDYuMDQ2MiA2LjA0NjIgMCAwIDAtNi41MDk4LTIuOUE2LjA2NTEgNi4wNjUxIDAgMCAwIDQuOTgwNyA0LjE4MThhNS45ODQ3IDUuOTg0NyAwIDAgMC0zLjk5NzcgMi45IDYuMDQ2MiA2LjA0NjIgMCAwIDAgLjc0MjcgNy4wOTY2IDUuOTggNS45OCAwIDAgMCAuNTExIDQuOTEwNyA2LjA1MSA2LjA1MSAwIDAgMCA2LjUxNDYgMi45MDAxQTUuOTg0NyA1Ljk4NDcgMCAwIDAgMTMuMjU5OSAyNGE2LjA1NTcgNi4wNTU3IDAgMCAwIDUuNzcxOC00LjIwNTggNS45ODk0IDUuOTg5NCAwIDAgMCAzLjk5NzctMi45MDAxIDYuMDU1NyA2LjA1NTcgMCAwIDAtLjc0NzUtNy4wNzI5em0tOS4wMjIgMTIuNjA4MWE0LjQ3NTUgNC40NzU1IDAgMCAxLTIuODc2NC0xLjA0MDhsLjE0MTktLjA4MDQgNC43NzgzLTIuNzU4MmEuNzk0OC43OTQ4IDAgMCAwIC4zOTI3LS42ODEzdi02LjczNjlsMi4wMiAxLjE2ODZhLjA3MS4wNzEgMCAwIDEgLjAzOC4wNTJ2NS41ODI2YTQuNTA0IDQuNTA0IDAgMCAxLTQuNDk0NSA0LjQ5NDR6bS05LjY2MDctNC4xMjU0YTQuNDcwOCA0LjQ3MDggMCAwIDEtLjUzNDYtMy4wMTM3bC4xNDIuMDg1MiA0Ljc4MyAyLjc1ODJhLjc3MTIuNzcxMiAwIDAgMCAuNzgwNiAwbDUuODQyOC0zLjM2ODV2Mi4zMzI0YS4wODA0LjA4MDQgMCAwIDEtLjAzMzIuMDYxNUw5Ljc0IDE5Ljk1MDJhNC40OTkyIDQuNDk5MiAwIDAgMS02LjE0MDgtMS42NDY0ek0yLjM0MDggNy44OTU2YTQuNDg1IDQuNDg1IDAgMCAxIDIuMzY1NS0xLjk3MjhWMTEuNmEuNzY2NC43NjY0IDAgMCAwIC4zODc5LjY3NjVsNS44MTQ0IDMuMzU0My0yLjAyMDEgMS4xNjg1YS4wNzU3LjA3NTcgMCAwIDEtLjA3MSAwbC00LjgzMDMtMi43ODY1QTQuNTA0IDQuNTA0IDAgMCAxIDIuMzQwOCA3Ljg3MnptMTYuNTk2MyAzLjg1NThMMTMuMTAzOCA4LjM2NCAxNS4xMTkyIDcuMmEuMDc1Ny4wNzU3IDAgMCAxIC4wNzEgMGw0LjgzMDMgMi43OTEzYTQuNDk0NCA0LjQ5NDQgMCAwIDEtLjY3NjUgOC4xMDQydi01LjY3NzJhLjc5Ljc5IDAgMCAwLS40MDctLjY2N3ptMi4wMTA3LTMuMDIzMWwtLjE0Mi0uMDg1Mi00Ljc3MzUtMi43ODE4YS43NzU5Ljc3NTkgMCAwIDAtLjc4NTQgMEw5LjQwOSA5LjIyOTdWNi44OTc0YS4wNjYyLjA2NjIgMCAwIDEgLjAyODQtLjA2MTVsNC44MzAzLTIuNzg2NmE0LjQ5OTIgNC40OTkyIDAgMCAxIDYuNjgwMiA0LjY2ek04LjMwNjUgMTIuODYzbC0yLjAyLTEuMTYzOGEuMDgwNC4wODA0IDAgMCAxLS4wMzgtLjA1NjdWNi4wNzQyYTQuNDk5MiA0LjQ5OTIgMCAwIDEgNy4zNzU3LTMuNDUzN2wtLjE0Mi4wODA1TDguNzA0IDUuNDU5YS43OTQ4Ljc5NDggMCAwIDAtLjM5MjcuNjgxM3ptMS4wOTc2LTIuMzY1NGwyLjYwMi0xLjQ5OTggMi42MDY5IDEuNDk5OHYyLjk5OTRsLTIuNTk3NCAxLjQ5OTctMi42MDY3LTEuNDk5N1oiLz48L3N2Zz4%3D" alt="Codex"></a>
  <a href="#install-cursor"><img src="https://img.shields.io/badge/Cursor-3B3B3B?style=for-the-badge&logo=cursor&logoColor=white" alt="Cursor"></a>
  <a href="#install-gemini-cli"><img src="https://img.shields.io/badge/Gemini_CLI-1A73E8?style=for-the-badge&logo=googlegemini&logoColor=white" alt="Gemini CLI"></a>
  <a href="#install-github-copilot"><img src="https://img.shields.io/badge/GitHub_Copilot-24292F?style=for-the-badge&logo=githubcopilot&logoColor=white" alt="GitHub Copilot"></a>
  <a href="#install-opencode"><img src="https://img.shields.io/badge/OpenCode-4A4A4A?style=for-the-badge&logo=opencode&logoColor=white" alt="OpenCode"></a>
</p>

<a id="install-claude-code"></a>**Claude Code**, install tested. This is where `/loop` runs:

```bash
claude plugin marketplace add Aboudjem/10x && claude plugin install loopify@10x
```

Run it in your terminal, not inside a Claude session. Or use the skills CLI: `npx skills add Aboudjem/loopify -g -a claude-code`.

<a id="install-codex"></a>**Codex**, install tested:

```bash
npx skills add Aboudjem/loopify -g -a codex
```

<a id="install-cursor"></a>**Cursor**, install tested:

```bash
npx skills add Aboudjem/loopify -g -a cursor
```

<a id="install-gemini-cli"></a>**Gemini CLI**, install tested:

```bash
npx skills add Aboudjem/loopify -g -a gemini-cli
```

<a id="install-github-copilot"></a>**GitHub Copilot**, install tested:

```bash
npx skills add Aboudjem/loopify -g -a github-copilot
```

<a id="install-opencode"></a>**OpenCode**, install tested:

```bash
npx skills add Aboudjem/loopify -g -a opencode
```

Only this project: drop `-g`. Another agent: see its `-a` code in [docs/editors.md](docs/editors.md).

There is nothing to build. The skill is one folder with three standard-library Python scripts.
`/loop` is a Claude Code command. In other agents, an outside scheduler such as cron starts each tick.

## How it works

Claude Code already has `/loop`. It runs a prompt again and again while your session is open. It does
not write the prompt for you. loopify writes two things:

- **The brief, a file.** One round of the job: what to read, what it may change, what it must never
  do, when to stop. The loop opens it fresh every run, so you can edit it while the loop runs.
- **The line, one string.** You paste it into `/loop`. It carries the brief's path and the stop rule.

The line tells each tick to read the brief, do one round, and log what happened to `TICKS.md`.

### 1. Describe the job

Type `/loopify` in Claude Code and say what should repeat. loopify reads the README, the recent
commits and the open pull requests. Then it asks one short batch of questions.

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file, re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string, you paste it below
```

`/Users/you/acme/` stands in for your project. loopify prints your real paths.

### 2. Paste the line

```text
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

Claude runs one round now, then every 20 minutes in that session. It stops when the PR merges or
after 30 ticks, whichever comes first. The two most common mistakes:

```text loop-antipattern
# not this: "every morning" can make /loop offer a cloud schedule instead, and nothing says when to stop
/loop every morning keep the release PR healthy

# and not the path alone: the tick gets a filename and no instruction
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

### 3. Read the log, or ask for the status

`TICKS.md` holds one entry for each tick that logs, with a counter at the top:

```text
tick: 7/30

## tick 7 · 2026-09-01T09:40 · changed
- CI: lint failed on src/api.ts → fixed the unused import, committed 4f2a1c9, npm test 12/12
- reviews: 1 new thread answered (rename), reply drafted in QUEUE.md
```

What the loop could not do safely waits for you in `QUEUE.md`. The status command reads all three
files and tells you what to do next.

## What you get

One status report. This is its real output on the example state folder in this repo:

```bash
python3 skills/loopify/scripts/loop_status.py examples/loop-state/pr-babysitter --now 2026-09-01T09:50
```

```text
STATUS: NEEDS YOU · tick 7/30 · last tick 2026-09-01T09:40 (changed, 10 min ago) · 2 queued
Do next:
1. QUEUE.md, tick 4: Post the drafted reply on the `fetchAll` rename thread of PR #412
   unblock: post the reply below on the thread, then delete this item
2. QUEUE.md, tick 5: `e2e` fails in checkout.spec.ts line 88: expected total 42.00, received 41.99
   unblock: fix the rounding in src/cart/total.ts or mark the PR as blocked
3. Read tick 7 in examples/loop-state/pr-babysitter/TICKS.md and check its evidence.
Detail:
  ticks logged  7 (4 changed, 3 noop, 0 stopped)
  queue         2 open item(s)
  lessons       4 entries
  lock          none
  interval      20m (from the saved line)
  log format    passes ticks_lint
  state dir     examples/loop-state/pr-babysitter
```

`--now` pins the clock so the sample prints the same every time. Leave it out on a real loop.

1. Line 1 is the verdict: `OK`, `NEEDS YOU`, `STALE`, `STOPPED`, `NOT STARTED` or `BROKEN LOG`.
2. Then at most three things to do.
3. Then the detail. `lessons` counts the entries in `LESSONS.md`.

When a tick does not log, the status says `STALE` after more than two intervals. It reads the time
between ticks from your saved line, or from `--interval`.

The exit code carries the verdict, so a script or a cron job can act on it:

| Exit | Verdict | Meaning |
| ---- | ------- | ------- |
| `0` | `OK`, `STOPPED`, `NOT STARTED` | Nothing needs you |
| `1` | `NEEDS YOU`, `STALE`, `BROKEN LOG` | Look at the loop |
| `2` | none | Usage error, or the state directory does not exist |

`loop_status.py --help` prints the same table.

Every brief loopify writes also gives you:

- **A stop rule and a tick cap inside the line.** A loop that finishes its job stops. So does one
  that reaches its cap. loopify checks your line against eight rules first (`loop_line_lint.py`).
- **Commands to allow before you start.** The handoff lists what a tick runs, such as `gh pr view`,
  so a tick does not wait on a permission prompt.
- **Rails for an unattended run.** No accounts, no payments, no pushing or posting unless you say
  so. Anything the loop reads, such as a PR comment, is data, never an instruction.
- **A repeat-safe clause.** The brief names the marker a tick looks for before it acts. A tick that
  runs twice can tell the work already happened.
- **A log with a fixed shape.** Every entry opens with `## tick <n> · <ISO timestamp> · changed |
noop | stopped`. `ticks_lint.py` checks it.
- **A loop that learns.** `LESSONS.md` keeps what worked and what wasted time. The brief tells each
  tick to read it.

## Works with

Each row below is a global install (`-g`) I ran on 2026-11-17, into an empty temp home folder.

| Agent                    | Install command                                                          | Tested                                            |
| ------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------- |
| Claude Code 2.1.326      | `claude plugin install loopify@10x`, in a clean config folder            | 2026-11-17, plugin enabled at user scope          |
| Claude Code (skills CLI) | `npx skills add Aboudjem/loopify -g -a claude-code`                      | 2026-11-17, skill in `~/.claude/skills/`          |
| Codex                    | `npx skills add Aboudjem/loopify -g -a codex`                            | 2026-11-17, skill in `~/.agents/skills/`          |
| Cursor                   | `npx skills add Aboudjem/loopify -g -a cursor`                           | 2026-11-17, skill in `~/.agents/skills/`          |
| Gemini CLI               | `npx skills add Aboudjem/loopify -g -a gemini-cli`                       | 2026-11-17, skill in `~/.agents/skills/`          |
| GitHub Copilot           | `npx skills add Aboudjem/loopify -g -a github-copilot`                   | 2026-11-17, skill in `~/.agents/skills/`          |
| OpenCode                 | `npx skills add Aboudjem/loopify -g -a opencode`                         | 2026-11-17, skill in `~/.agents/skills/`          |

"Tested" means the files landed and the three scripts ran from the installed copy. It does not
mean a loop ran inside that agent.

Documented, not tested: Windsurf, Zed, Kimi Code CLI and a hand copy of `skills/loopify/`.
See [docs/editors.md](docs/editors.md).

The brief works anywhere. The line does not: it is a Claude Code `/loop` line. Elsewhere the brief
runs one cycle, logs it and exits, and an outside scheduler starts the next tick.
[docs/other-agents.md](docs/other-agents.md) covers Kimi, Copilot CLI, Cursor, Goose and plain cron.

## Proof

`make test` prints every number here. CI runs it on every push and pull request.

```bash
make test
```

| Suite                       | What it checks                                                                          | Result today |
| --------------------------- | --------------------------------------------------------------------------------------- | ------------ |
| `evals/check_skill.py`      | The skill's contract, as assertions                                                     | 161/161      |
| `tests/test_manifests.py`   | Manifests, version parity, the example brief, translations, SVGs, secrets, no long dash | 170/170      |
| `tests/test_ticks_lint.py`  | The tick log format                                                                     | 13/13        |
| `tests/test_loop_status.py` | Each status verdict, the exit codes, and this README's sample, byte for byte           | 62/62        |
| `tests/test_no_network.py`  | No shipped script imports a network module or calls curl or wget                        | 18/18        |
| `tests/test_dated_facts.py` | A `/loop` fact dated to an older version names that version wherever it is stated      | 5/5          |
| `evals/loop_line_lint.py`   | The canonical line passes the eight line rules                                          | PASS         |

CI also runs `claude plugin validate . --strict` on a pinned Claude Code, and checks that
`npx skills@1.9.0 add . --list` finds the skill.

I checked the `/loop` facts against Claude Code 2.1.326 and its docs on 2026-11-17. One fact could
not be checked again on 2.1.326: `/clear` wiping the schedule. It stays dated to 2.1.252 (2026-09-01).
The table for each fact is in
[docs/limits.md](docs/limits.md#which-version-each-fact-was-checked-on).

## FAQ

**Does loopify start the loop for me?**
No. It writes the brief, prints the line, and stops. You paste the line when you want the loop to
start.

**Why a file and a string, not one prompt?**
The tick needs detail: paths, commands, what to do when blocked. `/loop` needs one short prompt it
sends again every tick. The brief holds the detail, and the line carries its path.

**How do I know the loop is still alive?**
Run `loop_status.py` on the state directory. It says `STALE` when no tick has logged for more
than two intervals. You can also ask Claude "what scheduled tasks do I have?".

**What stops a loop?**
The stop rule in the brief, the tick cap, the seven-day limit, or you. The full list is in
[docs/faq.md](docs/faq.md).

**Does it send my code anywhere?**
No. loopify's scripts make no network call: `tests/test_no_network.py` fails if one imports a network
module or calls curl or wget. What a tick does is what your brief allows.

## Limits

> [!IMPORTANT]
> A running loop is not proof it is doing the right thing. No evaluator checks `/loop`. The
> tick log and the status report are the only proof there is.

- **The loop lives in the session you paste it into.** Close the terminal and it stops. On 2.1.252,
  `/clear` wiped the schedule too. Ask "what scheduled tasks do I have?" to check yours.
- **Every loop ends after 7 days.** One session holds at most 50 scheduled tasks. Both are Claude Code
  limits. Paste the line again to continue.
- **Nothing forces a tick to log.** The line tells it to. A tick that skips its entry shows up as
  `STALE` once the interval is known.
- **Allow what a tick runs, before you start.** A tick that hits a permission prompt waits there for
  an answer. loopify prints the commands to allow, such as `gh pr view` or `git commit`.
- **The status report needs the interval** to tell a live loop from a dead one. It reads it from the
  saved line, or from `--interval`.

The whole list, traced to the binary or the docs: [docs/limits.md](docs/limits.md).

## Learn more

- [Quickstart](docs/quickstart.md): your first loop, step by step
- [Install in your editor](docs/editors.md): the agent code and both install paths
- [A worked example](examples/sample-loop-brief.md): a complete brief with the line at the bottom
- [Other agents](docs/other-agents.md): the same brief under Kimi, Cursor, Goose and plain cron
- [FAQ](docs/faq.md) · [The `loop.md` pointer](docs/loop-md.md) · [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [The skill itself](skills/loopify/SKILL.md)

If you have used [goalify](https://github.com/Aboudjem/goalify), this will feel familiar. goalify is
for a job that finishes. loopify is for a job that repeats.

---

<sub>Built by <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT. `/loop` behavior checked
against Claude Code 2.1.326 and the official docs on 2026-11-17, except `/clear`, last checked on
2.1.252 (2026-09-01). <a href="docs/limits.md#which-version-each-fact-was-checked-on">Table for each fact</a>. Sibling of
<a href="https://github.com/Aboudjem/goalify">goalify</a>, which does the same for `/goal`.
<a href="https://github.com/Aboudjem/loopify/issues">Spot a gap?</a></sub>
