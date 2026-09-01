# The `.claude/loop.md` pointer

Optional, and written only when you ask for it — `/loopify --default <job>`, or "make it the project
default" in the question batch. This page covers what the file is, what loopify puts in it, and what
changes in the project once it exists.

You never need it. The **line** loopify prints (the short string you paste into `/loop`) already
carries the path of the **brief** inside it, so it works with or without a pointer. The brief is the
standing file (for example `/Users/you/acme/.loop/pr-babysitter.md`) that the loop re-reads at the
start of every **tick**; one tick runs one **cycle** of it.

## What `loop.md` is

`loop.md` is Claude Code's own file, not loopify's. It holds a default prompt for `/loop`: type
`/loop` with nothing after it and Claude Code reads `loop.md` and uses its contents as the prompt for
the loop.

Four rules govern it:

- **The project file wins.** `.claude/loop.md` in the project beats `~/.claude/loop.md` in your home
  directory. One default per project.
- **It is read only for a bare `/loop`,** or an interval-only one such as `/loop 20m`. Type any
  prompt after `/loop` and the file is ignored completely.
- **Edits take effect on the next tick,** not on the tick that is running when you save.
- **It is cut at 25,000 bytes** — at the last newline before the cut, with a warning line added. A
  file that is empty or only whitespace counts as absent, and Claude Code falls back to its built-in
  maintenance prompt — continue unfinished work, tend the branch's PR, then cleanup passes.

That 25,000-byte cut is a property of `loop.md` and of nothing else. It is not a limit on the brief,
which a tick opens with a file tool like any other file.

## What loopify writes

A pointer, four lines long (five at the outside):

```markdown
# loopify default loop — written by loopify 2026-09-01
Run one cycle of `/Users/you/acme/.loop/pr-babysitter.md` — read it first, obey its stop rule, log the tick.
Bare `/loop` (or `/loop 20m`) runs this. Typing any prompt after `/loop` ignores this file.
One default per project (`.claude/loop.md` beats `~/.claude/loop.md`); edit this pointer to change it.
```

Short on purpose. It points at the brief instead of repeating it, so there is still exactly one file
holding the instructions, and it is the same file the pasted line points at. A pointer that carried
the instructions would be a second copy to keep in step, and the one that drifts is the one you did
not think to edit.

## The two caveats, said out loud

**One default per project.** `.claude/loop.md` takes precedence whenever both files exist, so a
default you keep in `~/.claude/loop.md` for everything else becomes invisible inside this project.
Changing which brief is the default means editing this pointer.

**It is ignored the moment you type a prompt.** `/loop 20m Run one cycle of …` never looks at
`loop.md`. The pointer changes what a bare `/loop` does, and changes nothing about the line loopify
printed for you — that line keeps working exactly as before, and keeps naming the brief itself.

## What a bare `/loop` does once the pointer exists

- **`/loop`** with nothing after it runs **self-paced**: the pointer's text becomes the prompt, the
  tick runs one cycle of the brief, and the tick schedules its own next tick before it finishes.
- **`/loop 20m`** runs **fixed**, every twenty minutes: the first cycle immediately, then on the
  clock. Two ticks landing close together at the start is normal.

Either way, the pointer's content is put in front of the tick when the loop fires: in full on the
first delivery, and again in full whenever `loop.md` has been edited since the last fire; on later
unchanged fires it arrives as a short reminder to re-read the file (re-derived from the shipped
2.1.252 skill source; docs: edits take effect on the next iteration). That is why an edit lands on
the next tick rather than the one already running.

Note which mode you get. A bare `/loop` is self-paced whatever the brief's Standing decisions say, and
the tick's own mode check will detect that and behave accordingly, noting the difference in its log
entry. If the brief was written for a fixed cadence, paste the fixed line rather than relying on the
pointer.

## Why the pointer starts with a verb

`Run one cycle of` is doing real work in that second line. The pointer's contents become the tick's
whole prompt, so a pointer holding only a path hands the tick a file name and no instruction — the
same failure as pasting a bare path into `/loop`. The verb is what turns it into something a tick can
act on.

## Should you commit it?

Usually not, and it is your call.

The pointer holds an absolute path, `/Users/you/acme/…`, which is right on your machine and wrong on
everyone else's. It points into `.loop/`, which loopify adds to `.gitignore`, so the brief it names is
not in the repository at all. Commit the pointer and a colleague's bare `/loop` aims at a file they do
not have.

Commit it when everyone genuinely shares the path — a container, or a dev box where every checkout
sits at the same absolute location. Outside that, keep it local.

## How to remove the pointer

Delete `.claude/loop.md`. There is nothing else to undo: the brief and its state directory are
untouched, and the line loopify printed keeps working, because the brief's path is inside the line
rather than in the pointer. A bare `/loop` afterwards falls back to `~/.claude/loop.md` if you have
one, and to Claude Code's built-in maintenance prompt if you do not — continue unfinished work, tend
the branch's PR, then cleanup passes.

One timing detail. A loop you started **from a bare `/loop`** reads the pointer again on later fires,
so deleting the file while that loop runs takes its instructions away mid-loop. Stop that loop first,
then delete. A loop you started **by pasting the line** is unaffected either way.

---

<sub>The `loop.md` behavior on this page — project file over user file, bare and interval-only use
only, ignored when a prompt is typed, edits landing on the next tick, the 25,000-byte cut at the last
newline, an empty file counting as absent, and the full-then-reminder delivery of its contents — was
re-derived from the shipped Claude Code 2.1.252 binary and
https://code.claude.com/docs/en/scheduled-tasks, 2026.</sub>

Back to the [README](../README.md) · [FAQ](faq.md) · [honest limits](limits.md) ·
[quickstart](quickstart.md)
