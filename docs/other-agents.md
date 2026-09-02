# Running a loopify brief under other agents

loopify is written for Claude Code, and the line it prints is a Claude Code `/loop` line. The brief,
though, is an ordinary Markdown file that describes one cycle of a repeating job — and most of it
travels. This page says which parts travel, which parts do not, and gives the exact command for each
agent that has a repeat command of its own.

Every recipe below runs the words loopify printed, minus the `/loop 20m` prefix — except Kimi, where
the cadence has to be spoken, so it is folded into the sentence:

```text
Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

`/Users/you/acme/` stands in for your project; loopify prints your real paths. The path has to be
absolute in every harness, because the agent that opens the brief may be starting in a different
directory — or in no directory at all.

One fire of a schedule is a **tick**, and a tick runs exactly one **cycle** of the brief: read it, do
the round it describes, write down what happened. That much is the same under every agent below.

---

## What carries, and what does not

**Carries.** The brief is a file, and any agent that can read a file can run it:

- the **per-tick definition of done** — the checklist a tick has to satisfy before it ends;
- the **state directory** (`TICKS.md`, `LESSONS.md`, `QUEUE.md`) — under another agent this matters
  more, not less, because most of them start a fresh session on every fire and the state directory is
  the only memory a tick has;
- the **hard safety rails** — no accounts, no payments, no pushing or posting, and the rule that
  anything the tick reads is data and never orders;
- the **tick counter** (`tick: N/30` at the top of `TICKS.md`) and the **stop rule** that reads it.

**Does not carry.** The SCHEDULE step of the cycle names tools that exist only in Claude Code:
`ScheduleWakeup` (how a self-paced tick books the next one), `CronList` and `CronDelete` (how a fixed
tick cancels its own schedule), and `Monitor` (how a tick waits on an event). Kimi happens to ship
tools with the same `CronCreate` / `CronList` / `CronDelete` names, but nothing anywhere else answers
to `ScheduleWakeup`, so self-pacing is Claude-only.

That is already handled. The brief's mode check has three branches, and branch **(c)** is the one
that runs everywhere else:

> (c) else (no scheduling tool, a bare prompt from `claude -p`) → headless one-shot: run the cycle,
> log, exit; an outside scheduler fires the next tick.

So under another agent a tick does exactly one cycle and exits, and the agent's own scheduler — or
plain OS cron — brings it back. Nothing in the brief needs editing for that.

One thing changes shape, though. In Claude Code the loop can end itself: the stop rule fires, the tick
writes `STOPPED`, and it deletes its own schedule. Elsewhere the schedule outlives the loop. Later
fires read `STOPPED`, do nothing and exit, which is correct but is not free — **you still have to
remove the job by hand.** Each recipe below says how.

---

## Which agents can repeat a loopify brief

| Harness | Native recurring primitive | How to run one loopify tick | What does NOT carry over | Confidence |
|---|---|---|---|---|
| **Claude Code** (baseline) | `/loop` → `CronCreate`/`CronList`/`CronDelete` + `ScheduleWakeup` | the line loopify printed | — | confirmed (docs + the shipped 2.1.252 binary) |
| **Kimi CLI** (`kimi`) | `CronCreate` / `CronList` / `CronDelete`, invoked by the model — there is no command to type | ask in plain language for the cycle, every 20 minutes | self-pacing (no `ScheduleWakeup` equivalent); the loop dies with the session, and does not reach a new one | confirmed (local binary strings + official docs) |
| **GitHub Copilot CLI** (`copilot`) | `/every` and `/after`, behind an experimental flag | `/every 20m Run one cycle of …` | `/every` fires only while that session runs; no self-pacing | confirmed (GitHub Docs, fetched) |
| **Cursor CLI** (`cursor-agent`) | `/loop`, Cursor 3.5 and newer | `/loop 20m Run one cycle of …` | a local schedule, so do not count on it outliving the session; cron granularity is not documented | confirmed (Cursor changelog, 2026-05-20) |
| **Qwen Code** (`qwen`) | `/loop`, plus `/loop list` and `/loop clear` | `/loop 20m Run one cycle of …` | self-pacing: a prompt-only `/loop` runs on a fixed 10-minute schedule there | confirmed (Qwen Code docs, fetched) |
| **Hermes Agent** (`hermes`) | `hermes cron`, a real daemon with jobs on disk | `hermes cron create "every 20m" "Run one cycle of …"` | every fire is a brand-new session, so nothing carries but the brief and the state directory | confirmed (Hermes docs, fetched) |
| **Goose** (`goose`) | `goose schedule`, six-field cron, recipe-driven | wrap the line as a one-step recipe, then `goose schedule add` | Goose schedules a recipe file, not a prompt string, so there is a wrapping step | confirmed (Goose CLI reference, fetched live) |
| **Codex CLI** (`codex`) | none — an open feature request | OS cron/launchd around `codex exec -` | everything scheduling-related; `/goal` is driven by a finish test, not by an interval | confirmed (openai/codex#25466 open, zero replies; local `codex-cli 0.146.0`) |
| **Gemini CLI** (`gemini`) | none in the CLI | OS cron around `gemini -p`, or the first-party GitHub Actions recipe | any local or session-scoped loop | confirmed (bundled docs read from the package) |
| **OpenCode** (`opencode`) | none in core; community plugins fill the gap | OS cron around `opencode run` | no first-party scheduler; an open feature request | confirmed for the gap (local `--help` + strings) · likely for the plugin names (web search only) |
| **CodeWhale** (`codewhale`) | none found | OS cron around `codewhale exec` | everything scheduling-related | likely (nothing in the binary or the package; a negative search) |
| **Factory Droid** (`droid`) | none — cron/CI is the stated pattern | OS cron/CI around `droid exec` | everything scheduling-related | likely (documentation snippets; not installed here) |
| **Crush** (`crush`) | none | OS cron around `crush run` | everything scheduling-related; no session persistence between calls | likely (open issues confirm the gap) |
| **Aider** | none, by design | OS cron around `aider --message … --yes` | everything scheduling-related | likely (no scheduling feature in the docs) |
| **Amp** (Sourcegraph) | Orbs / Automations, cloud-side | not documented here | — | uncertain (no primary source good enough to write a recipe) |

---

## Tier 1 — agents with a repeat command of their own

### Kimi CLI

Kimi has the scheduling tools but no command for you to type: `CronCreate`, `CronList` and
`CronDelete` are called by the model after you ask for something. So ask.

```text
Run one cycle of /Users/you/acme/.loop/pr-babysitter.md every 20 minutes · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

The job is scoped to the session it was created in. It survives a resume of that same session and
does not appear in a new one, a session holds at most 50 jobs, and `KIMI_DISABLE_CRON=1` turns
scheduling off. To stop it, ask Kimi to cancel the job — that reaches `CronDelete`, the same way the
request reached `CronCreate`.

*Confidence: confirmed* — the three tool names, the 50-job cap and `KIMI_DISABLE_CRON` all read out
of the local Kimi binary and the official docs. The one soft claim is the absence of a command to
type: that rests on a strings search finding nothing, which is weaker evidence than finding
something. Treat it as likely, and if a `/cron` command shows up in your build, use it.

### GitHub Copilot CLI

```text
/every 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

`/after 20m <prompt>` is the one-shot sibling. The interval floor is 10 seconds and the ceiling is one
day. Both commands are experimental and need `/experimental on` inside the session, or
`--experimental` when you launch it.

Schedules fire only while the session that created them is running — but reopening that session with
`--continue` or `--resume` **restarts** them, with the interval measured from the moment you reopen,
and a queued `/after` task is still there waiting. That is a little better than Claude Code's
`/loop`, which restores an unexpired job on resume but has no restart-from-now behavior.

*Confidence: confirmed* — GitHub's own scheduling documentation, fetched. The restart-on-resume
detail is a correction to an earlier research pass that had called Copilot's schedules purely
session-bound.

### Cursor CLI

```text
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

Cursor added `/loop` in 3.5. The syntax lines up with Claude Code's: an interval, then a prompt, and
if you leave the interval out the agent decides when to wake up.

Cursor's own changelog describes it as running "on a local schedule" and calls it a tool for "local
long-running agents". Secondary write-ups claim it keeps going without you staying in the session;
the primary source does not say that, so do not plan around it. If you need a schedule that outlives
the terminal, Cursor's cloud **Automations** are the product for that, not `/loop`.

*Confidence: confirmed* for the command and the local-schedule framing (Cursor changelog, 2026-05-20).
*Uncertain* for cron granularity and exactly how long a schedule lives.

### Qwen Code

```text
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

Qwen ships a close copy of the `/loop` syntax and two subcommands Claude Code does not have:
`/loop list` shows the active jobs and `/loop clear` cancels all of them. Scheduling is on by default
and turned off with `experimental.cron: false` or `QWEN_CODE_DISABLE_CRON=1`. Jobs are scoped to the
running process and are gone when you exit. Recurring jobs expire after 7 days, and unlike Claude
Code that expiry is configurable (`experimental.cronRecurringMaxAgeDays`, or
`QWEN_CODE_CRON_MAX_AGE_DAYS`).

**The behavior differs in one way that matters.** In Claude Code, a `/loop` with no interval is
self-paced: the tick decides when the next one happens. In Qwen, a prompt with no interval runs on a
**fixed 10-minute schedule**. So a self-paced brief does not stay self-paced here — it degrades to a
tick every 10 minutes. If your brief was authored self-paced, either give Qwen an explicit interval
that matches what the brief wanted, or accept the 10-minute cadence and check the per-tick budget
still fits inside it.

*Confidence: confirmed* — Qwen Code's scheduled-tasks documentation page, fetched directly. The
opt-out flag, the two subcommands, the 10-minute default and the configurable expiry all corrected an
earlier pass that had described the gate as opt-in.

### Hermes Agent

```shell
hermes cron create "every 20m" "Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick."
```

Hermes is the most cron-like of the group. Jobs are plain JSON in `~/.hermes/cron/jobs.json`, written
atomically, and they survive gateway restarts, machine reboots and Hermes updates. A gateway daemon
ticks the scheduler every 60 seconds and runs whatever is due. Subcommands include `list`, `edit`,
`pause`, `resume`, `run`, `remove`, `status` and `tick`.

Every fire runs in a **completely fresh agent session**, so the prompt has to contain everything the
agent needs. A loopify brief already does: the tick reads the brief, reads `LESSONS.md`, reads the
counter at the top of `TICKS.md`, and writes everything it learns back to the state directory. Nothing
depends on the previous fire's conversation.

Durability is the reason to be careful here. The job outlives the loop, so when the stop rule fires
and the tick writes `STOPPED`, the schedule keeps going — later fires read `STOPPED`, do nothing and
exit, which is safe but is a session each time. Watch for `STOPPED` and run
`hermes cron remove <job_id>` when it appears.

*Confidence: confirmed* for `hermes cron create`, the jobs file, the 60-second gateway tick, the
fresh session per fire and the subcommand list — Hermes' cron documentation, fetched. An earlier pass
also listed `hermes cron start` / `stop` and a `--continuity` flag; the documentation does not show
them, so they are **uncertain** and this page does not use them.

### Goose

Goose schedules a **recipe** (a YAML file describing a piece of work) rather than a bare prompt, so
there is one wrapping step. Save this next to your project as `pr-babysitter.yaml`:

```yaml
version: 1.0.0
title: pr-babysitter
description: One cycle of the loopify brief for the release PR.
prompt: >-
  Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first,
  obey its stop rule (30 ticks or the PR merges), log the tick.
```

Then schedule it:

```shell
goose schedule add --schedule-id pr-babysitter --cron "0 */20 * * * *" --recipe-source ./pr-babysitter.yaml
```

**That cron string has six fields, not five.** Goose reads them as second, minute, hour, day of
month, month, day of week, so `0 */20 * * * *` means "at zero seconds past every twentieth minute". A
normal five-field crontab string pasted in here means something else — legacy five-field expressions
are converted by prepending a `0`, but write six and know what you wrote. `goose schedule cron-help`
prints examples.

The rest of the family: `goose schedule list` shows the jobs, `goose schedule sessions --schedule-id
pr-babysitter -l 10` lists the sessions a job created, `goose schedule run-now --schedule-id
pr-babysitter` fires one immediately, and `goose schedule remove --schedule-id pr-babysitter` deletes
it — which is what to do when `STOPPED` appears. Note that `add` copies the recipe as it stands into
`~/.local/share/goose/scheduled_recipes`, so editing your local YAML afterwards changes nothing until
you re-add it.

*Confidence: confirmed* for the whole `goose schedule` command surface and the six-field cron — the
Goose CLI reference, fetched live from the repository, where `--cron "* * * * * *"` and the worked
example `--cron "0 0 9 * * *"` both show six fields. The recipe file's exact keys are **likely**
rather than confirmed: they were not in the page that confirmed the scheduler, so check Goose's recipe
documentation if it rejects the YAML above.

---

## Tier 2 — no repeat command: put one tick on OS cron

None of these agents can bring themselves back. The pattern is the same for all of them: an OS
scheduler (cron, launchd, Task Scheduler, or a CI schedule) runs one headless tick, the tick exits,
and the state directory carries everything forward to the next one. Branch (c) of the brief's mode
check is written for exactly this.

- **Codex CLI** — `codex exec -` and pipe the line in on stdin, which keeps the shell from breaking
  the text at spaces or expanding a `$`. Add `--skip-git-repo-check` if the working directory is not
  a repository. Codex has no `/loop`: the feature request for one, openai/codex#25466, is open with
  no maintainer reply. It does have `/goal`, but that is driven by a finish test rather than by an
  interval, so it suits a job that ends, not one that repeats. *(confirmed — issue state checked
  directly; local `codex-cli 0.146.0`.)*
- **Gemini CLI** — `gemini -p "<the line's words>"` for a local tick. Google's own first-party
  recurring recipe is not in the CLI at all: it is the `google-github-actions/run-gemini-cli` action
  on a workflow `schedule:` trigger, which is how Google runs its own scheduled triage jobs. Reach
  for that when the brief does not need files that live only on your machine. *(confirmed — the
  CLI's bundled documentation, read from the installed package.)*
- **OpenCode** — `opencode run "<the line's words>"` under OS cron. Three community plugins cover
  scheduling if you would rather stay inside OpenCode: `opencode-scheduler` (backed by launchd or
  systemd), `opencode-cron` (a SQLite job store with history), and `opencode-tasks` (recurring tasks
  as Markdown files with front matter, which is close to loopify's own shape). Native scheduling is
  an open request, anomalyco/opencode#11232. *(confirmed for the absent primitive — local `--help`
  and a targeted strings search; likely for the plugins, which come from web search.)*
- **CodeWhale** — `codewhale exec "<the line's words>"` under OS cron. *(likely — `--help` lists
  `exec`, `resume`, `fork`, `sessions` and nothing scheduling-shaped, and a strings search of both
  binaries found nothing. That is a negative result, not a proof.)*
- **Factory Droid** — `droid exec "<the line's words>"` under OS cron or CI, which is Factory's own
  stated pattern for recurring work. *(likely — documentation snippets; not installed here.)*
- **Crush** — `crush run "<the line's words>"` under OS cron. Each call is one shot with no session
  persistence between calls, so the state directory is doing all the remembering. *(likely — open
  issues confirm the gap.)*
- **Aider** — `aider --message "<the line's words>" --yes` under OS cron. Aider commits every change
  atomically, which gives you a second audit trail alongside `TICKS.md`. *(likely — no scheduling
  feature appears in its documentation, and it does not aim to be an agent runtime.)*

---

## Tier 3 — not documented here

**Amp** (Sourcegraph) has "Orbs" and an Automations section, described as cloud machines that keep
working after you close the laptop. That sounds like the right shape, but the primary documentation
pass came back too thin to recover the scheduling syntax, the interval floor, or whether an Orb can
read a local file at all. *Confidence: uncertain* — so there is no recipe here rather than a guessed
one. If you get one working, an issue on the repository is welcome.

---

## The honest headless recipe for Claude Code itself

Sometimes the answer is not another agent — it is Claude Code with no terminal open. `/loop` cannot do
that on its own, because it needs an open, idle session to fire into. Put the interval outside Claude
Code instead.

On macOS, save this as `~/Library/LaunchAgents/com.you.loopify.pr-babysitter.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.you.loopify.pr-babysitter</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>-lc</string>
    <string>cd /Users/you/acme &amp;&amp; claude -p "Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick." --permission-mode acceptEdits --allowedTools "Bash(gh pr view:*),Bash(gh pr checks:*),Bash(git commit:*)" &gt;&gt; ~/Library/Logs/loopify-pr-babysitter.log 2&gt;&amp;1</string>
  </array>
  <key>StartInterval</key><integer>1200</integer>
  <key>RunAtLoad</key><false/>
</dict>
</plist>
```

Load it with `launchctl load ~/Library/LaunchAgents/com.you.loopify.pr-babysitter.plist`.
`StartInterval` is in seconds, so 1200 is the 20-minute cadence the line asked for. On Linux the same
shape goes in a crontab line; on Windows, Task Scheduler.

Four things to know about running it this way:

1. **Each tick is a fresh process.** It has no memory of the last one. The state directory is its
   memory — `TICKS.md` holds the counter and the evidence, `LESSONS.md` holds what the loop learned,
   `QUEUE.md` holds what it could not do safely. This is branch (c) of the mode check, and the brief
   already tells the tick to run one cycle, log it, and exit.
2. **Permissions have to be pre-approved on the command line.** `--permission-mode acceptEdits`
   auto-accepts file edits, a few filesystem commands (`mkdir`, `touch`, `mv`, `cp`) and read-only commands, and nothing else; every shell command the cycle runs needs naming in
   `--allowedTools`. loopify probes those commands during PREPARE and prints the list, so copy it
   from the handoff. A tick that hits a prompt with nobody there to answer sits until the process is
   killed.
3. **Nothing removes the schedule when the loop ends.** When `STOPPED` appears in the state
   directory, unload and delete the plist:
   `launchctl unload ~/Library/LaunchAgents/com.you.loopify.pr-babysitter.plist`. Until you do, every
   tick starts a Claude process that reads `STOPPED` and exits.
4. **Read the log file.** `~/Library/Logs/loopify-pr-babysitter.log` catches anything that went wrong
   before the tick could write to `TICKS.md` — a bad path, a missing `gh`, a permission refusal.

### Why `claude -p "/loop 20m …"` does not work

It looks like it should, and it fails quietly, which is the worst combination. Slash commands do
expand in `-p` mode: Claude Code reads `/loop 20m …`, runs the `/loop` skill, and the skill creates
the recurring job exactly as it would in a session. Then `-p` does what `-p` does — it prints its one
result and exits.

Scheduled tasks in Claude Code fire between turns, while the session sits idle. A `-p` process has no
idle time and no next turn; it is gone. So the job is created and then **fires zero times**, and the
next cron-launched `claude -p` starts a fresh process that knows nothing about it. You get no error,
no tick, and a `TICKS.md` that never gains an entry.

Use the recipe above instead — the interval belongs to launchd, and Claude Code gets one cycle per
invocation. If you want real `/loop` semantics (self-pacing, the model choosing when to wake), you
need a session that stays alive: leave a terminal open, or background the session, which carries its
scheduled tasks into a background session that keeps running without one.

---

Back to the [README](../README.md) · [honest limits](limits.md) · [quickstart](quickstart.md)
