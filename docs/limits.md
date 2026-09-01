# Honest limits

Everything loopify does not promise, in one place. The short version lives in the
[README](../README.md). This page is the whole list.

Five words first, because the rest of the page leans on them. **The brief** is the file loopify
writes (for example `/Users/you/acme/.loop/pr-babysitter.md`), and the loop reads it again at the
start of every run. **The line** is the short string you paste into `/loop`, with the brief's path
inside it. **A tick** is one of those runs: the loop fires, does one pass of the brief, writes down
what it did. That one pass is **a cycle** — one tick, one cycle. **The state directory** is the folder
beside the brief where the loop keeps its own files: the tick log `TICKS.md`, a lessons file, and a
queue of things it could not do.

## A running loop is not proof it is doing the right thing

Nothing behind `/loop` looks at a tick's work and decides whether it was any good. There is no judge
step in the `/loop` skill and the docs describe none. The schedule fires, the model reads the brief,
the tick ends, the next one is set up. That is the whole of it.

So the proof has to come from the loop itself. Every brief loopify writes ends each tick by adding
one entry to `TICKS.md`: what changed, the command output that shows it, and anything the tick handed
back instead of doing. That file is the record you get. A loop that has been fixing things all
afternoon and a loop that has found nothing to do all afternoon look the same from outside.

They look the same on screen too, and that is the part that catches people out. A tick with no work
in it is a **noop** — for example, the pull request had no new comments and its checks were already
green — and the terminal folds a run of noop ticks into a single line. Read the log, not the screen.

## Every loop stops after seven days

A `/loop` job is not permanent. Seven days after it starts it expires and stops firing, in either
mode. The docs say so about the self-paced mode in one line: "The jitter rules don't apply to it, but
the seven-day expiry does."

Nothing we found announces the expiry. The loop stops writing ticks, and as far as we can tell that
is the only sign of it. The fix
is to paste the line again, which starts a fresh seven days. A job you want running for a month is a
job you re-paste four times, so put it in your calendar — or use something built to outlive a
session, such as `/schedule` (cloud routines), a scheduled task in the desktop app, or a scheduled
GitHub Actions workflow.

## The loop lives in one session

It fires only while the session that created it is open, and only while that session is idle. If you
are mid-conversation, the tick waits its turn. If the window is closed or the machine is asleep, the
fire does not happen and it is not made up afterwards: a missed fire is skipped, not queued.

Things that end a loop early:

- `/clear` wipes every scheduled task in the session, the loop with them.
- Closing the session.
- `CLAUDE_CODE_DISABLE_CRON=1` in the environment turns scheduling off, so nothing is created at all.

Things that do not end it: `--resume` and `--continue` bring back loops that have not expired, and
backgrounding the session keeps them alive. One session holds at most 50 scheduled tasks.

And the one that surprises people: `claude -p "/loop 20m Run one cycle of …"` does not put a loop in
the background. It expands the skill, creates the job, and exits, and the job dies with the process.
It fires zero times. For a loop with no terminal open, see the headless recipe in the [FAQ](faq.md).

## The tick cap is a counter the loop maintains, not a limit anything enforces

`/loop` has no cost cap and no run-length cap of its own. So every brief loopify writes carries three
bounds instead: a stop rule, a tick cap, and a per-tick budget (at most so many subagents and so many
minutes of work in one cycle).

The tick cap lives at the top of `TICKS.md` as a line like `tick: 7/30`, and the brief tells each tick
to increment it before doing any work. That is a discipline the tick follows, not a switch in the
runtime. A tick that never reads the counter is not stopped by anything, and nobody is watching the
spend for you.

The numbers are yours. Raise or lower the cap in the brief's Standing decisions, or paste a line with
a different one; where the brief and the line disagree, the smaller number wins. loopify never
predicts what a loop will cost in money or tokens — the caps are the honest control, and a guess
dressed up as a figure is not.

## A permission prompt stops the tick, and fixed fires behind it collapse to one

`/loop` inherits its permissions from the session it runs in: the docs table for it reads
"Inherits from session". A tick that reaches a command nobody pre-approved stops and asks, then sits
there waiting for an answer. In fixed mode the schedule keeps its own time regardless, so a fire that
lands while the prompt is open is delivered once, late, when the prompt is answered — and any further
fires that pile up behind it are collapsed into that one, not queued (docs: "No catch-up for missed fires").

Pre-approve what a tick runs before you paste the line. loopify prints the list of commands it probed,
so you can allowlist them or turn on auto mode first.

Running headless changes the shape of this. `--permission-mode acceptEdits` auto-accepts file edits, a few filesystem commands (`mkdir`, `touch`, `mv`, `cp`) and the read-only command set, and nothing else
only; every Bash command a tick needs has to be named in `--allowedTools`, as in
`--allowedTools "Bash(gh pr view:*),Bash(git commit:*)"`. `auto` is not a general answer either: it
is gated by plan ("Auto mode is unavailable for your plan") and driven by a classifier.

One uncertainty, named as one. The binary contains the string
`Scheduling a /loop wakeup requires classifier review.` We know it is there. We do not know what
makes it appear, so we cannot tell you when a tick will hit it.

## A fixed tick arrives late on purpose

Fixed-interval fires carry jitter, a deliberate delay so that many schedules do not land at once. The
docs give the size of it: up to 30 minutes late, or up to half the interval when the interval is more
often than hourly. A 20-minute loop can therefore fire up to 10 minutes after the mark.

Write briefs that do not care. A cycle that has to happen at 09:00 exactly is not a `/loop` job.

<sub>The 30-minute figure is the docs'. The binary's own `CronCreate` text gives a different rule —
10 % of the period, up to 15 minutes — so the two disagree; the scheduler's own constants (`recurringFrac: 0.5`, a
30-minute cap) implement the docs' rule, so that is the one to plan for. Jitter applies to fixed mode only; a self-paced loop sets its own delay.</sub>

## You may be asked about a cloud schedule. "May", not "will"

When the interval is 60 minutes or more, or the request is phrased around a day ("every morning",
"daily", "every day", "each night", "every weekday" — judged by the model over the whole input, not
matched against a fixed pattern), `/loop` can offer to make the job a cloud schedule instead. Seven
runtime conditions have to hold before the question appears, so it is not something to count on in
either direction.

Answer "This session only". A cloud routine runs on a fresh clone with none of your local files, so
the brief's path does not exist there and the tick would have nothing to read.

There is a corner worth knowing. Day-shaped phrasing with no interval, plus an answer of "This
session only", makes `/loop` refuse to schedule locally at all: you get no loop. That is why loopify
keeps day words out of the line, including out of the file name inside the path.

## Fixed mode runs the first cycle at once, and again at the next boundary

Paste `/loop 20m …` at 11:19 and two ticks land close together: one straight away, one at 11:20.
Fixed mode creates the schedule and then runs the prompt immediately, and the schedule it creates is
`*/20 * * * *` — on the clock, not twenty minutes from when you pasted.

This is normal rather than a fault, but it is worth knowing before you write a brief whose cycle is
expensive or writes to something shared.

## A fixed fire arrives with no skill instructions

Every fire after the first delivers the line's text as a fresh turn on its own, with none of the
`/loop` skill's instructions in context. The tick sees one sentence telling it to read a file. It has
no way of knowing, from the prompt alone, that it is part of a loop at all.

That is what the mode check at the top of every loopify brief is for: the tick works out for itself
whether it is self-paced, fixed, or a one-shot run under an outside scheduler, and behaves
accordingly. Without that check, a tick either schedules a duplicate or schedules nothing and the
loop dies quietly.

## Esc stops a self-paced loop, but it does nothing to a fixed one

Pressing Esc while a self-paced loop is waiting cancels the pending wakeup, and the loop is over. Esc
does nothing to a fixed loop: the schedule is a job in its own right and keeps firing. To end that
one, ask in the session for it: "cancel the pr-babysitter job". That deletes the job.

Then confirm it. Ask "what scheduled tasks do I have?" and read the list; it should be empty. If ticks
keep arriving, close the session.

## Two sessions running the same brief are two loops

Paste the line in two windows and you get two loops over one brief: two ticks doing the same work,
two sets of entries in one `TICKS.md`, two lots of commits.

The brief defends itself as far as it can. The first thing a tick does is write a `LOCK` file into the
state directory, and a tick that finds a fresh LOCK already there writes the reason to `QUEUE.md` and
stops itself. Note what that means: the second loop ends. It cannot fold itself into the first, and
nothing merges the two. If the loop you wanted was the one that stopped, you have to start it again.

## The 25,000-byte cut belongs to `loop.md`, not to the brief

The optional pointer file loopify writes on `--default` is Claude Code's own feature, with its own
rules: it is read only for a bare `/loop` or an interval-only `/loop 20m`, it is ignored the moment
you type a prompt after `/loop`, and content past 25,000 bytes is truncated at the last newline before
the cut, with a warning line added.

That cap belongs to `loop.md`. It is not a limit on the brief — a tick opens the brief with a file
tool, like any other file. loopify still keeps briefs under about 12,000 bytes, for an unrelated
reason: the brief is re-read at the start of every tick, so its size is a cost you pay again and
again. Full details on the pointer: [the `.claude/loop.md` pointer](loop-md.md).

## The "~$300 over a weekend" report is real, and it is against an older build

Issue [#64744](https://github.com/anthropics/claude-code/issues/64744) is open: a loop that outlived
Ctrl+C, with a daemon respawning behind it, and a reported "~$300 over a weekend". Quote that figure
only with the version attached — it was filed against Claude Code **2.1.160**, and it is not a
measurement of what 2.1.252 does. It is a reason to verify a stop rather than assume one, which is
what "what scheduled tasks do I have?" is for.

The two older re-fire reports, #51304 and #54086 (a one-shot slash command re-fired on every wakeup),
are closed as stale. They are history, not current behavior. loopify still keeps slash commands out
of the line, for a different reason: a command re-run every tick does its one-shot work every tick,
and only model-invocable skills expand at all — built-ins, skills marked
`disable-model-invocation` and MCP prompts arrive as plain text the tick cannot act on.

## Agent Skills portability is a structural claim, not a tested one

loopify is a plain [Agent Skill](https://agentskills.io): a name and a description at the top, then
Markdown. On that basis it should load in any agent that implements the
[Agent Skills standard](https://agentskills.io), of which
[VS Code's Copilot customization page](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
is one implementation. The brief it writes is ordinary Markdown that any agent can follow.

This repo ships **no conformance run against a non-Claude agent**. What we know about other tools'
schedulers comes from their own documentation, not from our runs, and it is written up with that
caveat in [other agents](other-agents.md).

## The eval baseline is a static check plus two runs of one scenario

loopify is built test-first against a baseline you can reproduce, and the baseline is honest about its
own size. `evals/check_skill.py` holds 136 assertions that count exact strings in the shipped skill:
a file of the wrong shape (goalify's own skill, which is a real skill for a different job) scores
**31/136**, and loopify's scores **136/136**. Beside that sit a recorded cold run and one judged
with-skill run of the same scenario — RED 1/7 → GREEN 7/7, sonnet, one run, scored by a separate
opus judge ([baseline](../evals/RED-baseline.md), 2026-09-01). It is not a multi-model suite.

Read those numbers for what they are: a comparison of two files against a checklist, plus two runs of
one scenario.
Nobody has yet driven a loop through thirty ticks in each mode and scored what came out. The checks
prove the shipped text says what it should. They do not prove a loop behaves.

## What loopify does not do

- **It does not run the loop.** It writes the brief and prints the line. Pasting the line is yours.
- **It does not fetch remote content and run it.** Research during preparation is read, cited, and
  written into the brief as text.
- **It never edits its own brief from inside a run.** A tick that thinks the brief should change
  writes the suggestion to `QUEUE.md` and leaves the file alone.
- **It never writes a credential's value** into the brief or the state directory. It names where one
  lives (the name of an environment variable, a keychain entry) and never the value itself.

A standing unattended loop has a bigger blast radius than a one-shot run, and the rails in the brief
are the author's responsibility. That is the subject of [SECURITY.md](../SECURITY.md).

---

<sub>The `/loop` behavior on this page — the seven-day expiry in both modes, the session scope and
50-task cap, permission inheritance and `acceptEdits`, the jitter numbers, the cloud-schedule
question, the immediate first fire in fixed mode, and the 25,000-byte `loop.md` cut — was re-derived
from the shipped Claude Code 2.1.252 binary and https://code.claude.com/docs/en/scheduled-tasks,
2026.</sub>

Back to the [README](../README.md) · [FAQ](faq.md) · [quickstart](quickstart.md)
