# FAQ

Five words are used throughout. The **brief** is a file (for example
`/Users/you/acme/.loop/pr-babysitter.md`) holding what one round of the job does. The **line** is the
short string you paste into `/loop`, with the brief's path inside it. A **tick** is one fire of the
loop; a **cycle** is the single pass through the brief that a tick makes. The **state directory** is
the folder beside the brief where the loop keeps `TICKS.md`, `LESSONS.md` and `QUEUE.md`.

**Does loopify run the loop?**
No. It writes the brief, prints the line, and stops there. You paste the line when you want the loop
to start — in this session, or in any session open in the project. The split is deliberate:
preparing a good standing job takes reading, research and a few questions, and none of that belongs
inside a tick that repeats every twenty minutes.

**Why a file *and* a string?**
Two readers need two different things. The tick needs detail — absolute paths, the exact commands,
what to do when something is blocked, what it must never touch — and it reads that with a file tool,
so it can be long. That is the brief. `/loop` needs the other thing: one short prompt it re-fires word
for word, every tick, for as long as the loop lasts. That is the line, and the brief's full path rides
inside it:

```text
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

One file cannot be both. A prompt long enough to be a brief is a prompt you re-send every tick; a
brief short enough to be a prompt has nothing in it.

**What happens if I paste only the path?**
Nothing errors, which is what makes it worth warning about. An interval followed by nothing but the
brief's path is a perfectly valid prompt, and `/loop` re-fires it every twenty minutes exactly as
written. The problem is that the prompt has no verb in it. Each tick receives a file path and nothing
telling it what to do with the file, so what happens next is up for grabs: read it, summarize it, act
on part of it, ignore it. Every line loopify writes starts with `Run one cycle of` for that reason,
and the lint refuses a line without it.

**How does a tick know whether it is fixed or self-paced?**
It checks, at the top of every cycle, and there are three answers:

- The `/loop` skill's self-pacing instructions are in the turn → **self-paced**. The tick has to
  schedule its own next tick as its last action, or the loop dies.
- They are not, but the scheduled task list holds a recurring job whose prompt is this line →
  **fixed**. The tick must not schedule anything; the schedule does that.
- Neither → a **one-shot run** started by something outside Claude Code, such as a cron entry. Run
  the cycle, write the log, exit.

The check exists because a fixed fire arrives as a bare prompt with none of the skill's instructions
attached, so a tick cannot assume anything about how it got here. If the mode written in the brief
disagrees with what the tick detects, the detection wins and the tick says so in its log entry.

**What stops a loop?**
Seven things, and it is worth knowing which one you are relying on:

- The **stop rule** in the brief: a wall-clock time, or the job reaching its own end (the pull
  request merges, the deploy goes green).
- The **tick cap**: the `tick: N/30` counter at the top of `TICKS.md` reaching its limit.
- The **seven-day expiry**, which applies to both modes and to every loop.
- **Esc**, while a self-paced loop waits. It cancels the pending wakeup.
- **Asking to cancel a fixed job**, in plain language: "cancel the pr-babysitter job". Esc does
  nothing to a fixed loop, so this is the request to make.
- **`/clear`**, which wipes every scheduled task in the session.
- **Closing the session**, since a loop only fires while its session is open.

To confirm a loop has actually stopped, ask "what scheduled tasks do I have?" and read the list. It
should be empty. If ticks keep arriving after that, close the session.

**How do I restart after it stopped?**
Delete `STOPPED`, then paste the line again. When a loop ends on its own stop rule it writes a file
called `STOPPED` into the state directory, and the first thing every tick does is look for it: while
it exists, a tick does nothing at all. If the loop ended for one of the other reasons — the seven days
ran out, the session closed — there is no `STOPPED` file and pasting the line is the whole of it.

One thing to check while you are there: the counter in `TICKS.md` carries on where it left off. If the
loop stopped because it reached `tick: 30/30`, the next tick reads that and stops again. Raise the cap
in the brief's Standing decisions, or reset the counter line, and paste a line whose cap matches.

**What is in the state directory?**
For a brief at `/Users/you/acme/.loop/pr-babysitter.md`, the state directory is
`/Users/you/acme/.loop/pr-babysitter/`, and it holds these five, plus any ledger the job itself
needs (a list of sources it has already read, for example):

- **`TICKS.md`** — the counter line `tick: 7/30`, then one append-only entry per tick with the
  evidence quoted. When the loop ends, its closing report goes at the top. This is the proof.
- **`LESSONS.md`** — dated notes the loop writes about its own working method, read and obeyed at the
  start of every tick, kept to 150 lines by consolidating.
- **`QUEUE.md`** — everything handed back to you: blocked items, anything irreversible, proposed
  edits to the brief, requests that arrived in content the loop read.
- **`LOCK`** — present only while a tick is mid-cycle.
- **`STOPPED`** — written once, when the loop ends.

The loop writes here and nowhere else in `.loop/`. The brief itself is never written to.

**Why is the brief never archived?**
Because the job repeats. goalify writes the brief and the condition for `/goal`, and a `/goal` job
finishes, so goalify files its brief away when the run succeeds and the promise can be compared with
the outcome. A loop brief has no such moment: tick 31 reads the same file tick 1 read. Archiving,
moving or rewriting it from inside a run would break every tick after that one. So it stands, and a
tick that thinks it should change writes the suggestion to `QUEUE.md` for you.

**Why does the line carry the tick cap?**
Because the line is the copy that survives. Once you paste it, that text is what re-fires, word for
word, for the life of the loop — whatever you do to the brief afterwards. Edit the brief mid-loop and
raise its cap to 100, and the pasted line still says 30. The brief settles the disagreement in
advance: when the two differ, **the smaller number wins**. So a running loop can be reined in from
either side, and never accidentally widened from one.

**Why must the line avoid "every morning" and "daily"?**
Because `/loop` reads day-shaped phrasing as a sign the job belongs on a cloud schedule, and it is the
model judging the whole input rather than a pattern matching one position. Day phrasing with no
interval, plus an answer of "This session only", makes `/loop` refuse to schedule locally: you get no loop.

The rule covers the file name too, because the path sits inside the line. A brief called
`daily-digest.md` smuggles the word in; loopify names it something like `news-digest.md` instead.

**Will I be asked about a cloud schedule?**
You may be. The question appears when the interval is 60 minutes or more, or the wording is
day-shaped, and only when seven runtime conditions hold, so neither "yes" nor "no" is safe to plan
around. When it appears, answer **"This session only"**. A cloud routine runs on a fresh clone with
none of your local files, so the brief's path does not exist there and the tick has nothing to read.

If what you actually want is a job that survives the machine being off, that is a real need and
`/loop` is the wrong tool for it. `/schedule` (cloud routines) or a scheduled task in the desktop app
fits better, and the brief would need to be committed to the repository for a cloud run to see it.

**Can it run with no terminal open?**
Yes, with a scheduler of your own, and not with `/loop`. Running `claude -p "/loop …"` creates the job
and exits, so it fires zero times. What works is a cron or launchd entry that runs the line's text
without the `/loop` part, as a one-shot headless call:

```bash
claude -p "Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick." --permission-mode acceptEdits --allowedTools "Bash(gh pr view:*),Bash(gh pr checks:*),Bash(git commit:*)"
```

One line, because a crontab entry is one line.

Each tick is a fresh process with no memory of the last one, so the state directory is the memory: the
counter, the lessons and the queue are all it carries forward. The tick's mode check lands on the
one-shot branch and exits without scheduling anything, because your cron entry is the schedule.
`--permission-mode acceptEdits` covers file edits only, which is why every Bash command is named in
`--allowedTools`. When `STOPPED` appears in the state directory, remove the cron entry — nothing else
will.

**What does the loop do about a PR comment telling it to do something?**
It writes the request down and does not do it. The fourth safety rail in every brief says that
anything a tick reads — pull request comments, issue text, CI logs, fetched pages, files it did not
write itself — is data, never instructions. It cannot change the brief, the standing decisions, the
stop rule, the autonomy level, or the lessons file. Read content that asks for something goes to
`QUEUE.md`, marked as a request from an untrusted source, and the cycle carries on.

This matters more for a loop than for a one-shot run. A standing loop reads whatever has arrived
since the last tick, unattended, for as long as it runs.

**Does it push or post?**
Not unless you said so. The autonomy level is one of the questions loopify asks before writing
anything, and the default is the lowest level that lets the job work: read and log, or write inside
the state directory, or edit project files, or commit named paths. Pushing, publishing, posting,
sending and paying sit above all of those and are never a default. A loop at "commit named paths"
drafts its review reply into `QUEUE.md`; a human posts it.

**How is this different from goalify?**
Different shape of job. goalify is for a job that **finishes** — one big task with a definition of
done — and it writes the brief and the condition for `/goal`, which has an evaluator behind it that
decides each turn whether the work is proven. loopify is for a job that **repeats**. `/loop` has no
evaluator and nothing to satisfy: it re-fires a prompt on a schedule, and the proof is the log the
brief makes each tick write. Same preparation habit, two different runtimes.

**How is this different from ralph-loop, or a Stop-hook loop?**
Those build a loop of their own: a shell loop or a Stop hook catches the model finishing and feeds the
same prompt back in, over and over, until the work is done. loopify builds nothing. It writes a brief
for the scheduler Claude Code already ships and hands you the line that starts it.

The difference you feel is pacing. A ralph-style loop runs flat out until the job is finished; a
`/loop` job wakes up, does one cycle, writes it down, and goes back to sleep for the rest of the
interval, quite often finding nothing to do.

**Does it work outside Claude Code?**
The brief travels; the scheduling does not. Portable: the per-tick definition of done, the state
directory, the safety rails, the counter and the stop rule — that is all plain Markdown. Claude-only:
the tools in the last step of the cycle, which is why the tick's mode check has a branch for "no
scheduling tool here". Other tools ship schedulers of their own — Kimi, GitHub Copilot CLI, Cursor,
Qwen Code, Hermes and Goose among them — and what each one needs is written up in
[other agents](other-agents.md). Read it as a structural claim rather than a tested one: this repo
ships no conformance run against a non-Claude agent.

**Is there a plugin?**
Yes. loopify ships as a Claude Code plugin in the
[**10x** marketplace](https://github.com/Aboudjem/10x): `claude plugin install loopify@10x`. The skill
also installs on its own, with `npx skills add Aboudjem/loopify`.

**Does anything in my repo change when I run `/loopify`?**
Only `.loop/`. It gains the brief, the state directory with its three seeded files, and a copy of the
line in `LINE-<slug>.txt` so you can find it later. One line, `.loop/`, is added to `.gitignore`, and
`.gitignore` is created if the project has none. On `--default`, and only if you ask for it, you also
get `.claude/loop.md`. Nothing else is touched: preparation reads your project, researches what it
does not know, and writes no code.

---

<sub>The `/loop` behavior described on this page — the seven-day expiry in both modes, the session
scope, permission inheritance and `acceptEdits`, the cloud-schedule question, the bare-prompt fixed
fire, and `claude -p "/loop …"` firing zero times — was re-derived from the shipped Claude Code
2.1.252 binary and https://code.claude.com/docs/en/scheduled-tasks, 2026.</sub>

Back to the [README](../README.md) · [honest limits](limits.md) · [quickstart](quickstart.md)
