# Install loopify in your editor

loopify is one Agent Skill: a `SKILL.md` with `name` and `description` frontmatter, Markdown
underneath, with two standard-library Python scripts beside it. There is no server to run and nothing
to compile. Claude Code has a first-party path; every other agent installs the same directory
through the skills CLI.

## Claude Code

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

Then say "loopify this: `<your recurring job>`" or run `/loopify <job>`.

## Any other agent, in one line

```bash
npx skills add Aboudjem/loopify -a <agent>
```

The agent codes below were read from the supported-agents table in
[vercel-labs/skills](https://github.com/vercel-labs/skills#supported-agents) on 2026-09-02, along
with the directory each agent reads. That table lists 77 codes in all, so if yours is not here, it
is almost certainly in the table.

| Agent | `-a` code | Project path | Global path |
| --- | --- | --- | --- |
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `cursor` | `.agents/skills/` | `~/.cursor/skills/` |
| Codex | `codex` | `.agents/skills/` | `~/.codex/skills/` |
| GitHub Copilot | `github-copilot` | `.agents/skills/` | `~/.copilot/skills/` |
| Gemini CLI | `gemini-cli` | `.agents/skills/` | `~/.gemini/skills/` |
| OpenCode | `opencode` | `.agents/skills/` | `~/.config/opencode/skills/` |
| Windsurf | `windsurf` | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| Zed | `zed` | `.agents/skills/` | `~/.agents/skills/` |
| Kimi Code CLI | `kimi-code-cli` | `.agents/skills/` | `~/.agents/skills/` |

So, for Cursor:

```bash
npx skills add Aboudjem/loopify -a cursor
```

Three flags worth knowing:

- `-g` installs to the global path in the table instead of the project one.
- `-y` skips the confirmation prompts, which is what you want in a script.
- `--list` prints what a repository offers and installs nothing. For this repo it reports one skill.

## Copy it in by hand

The skill is a directory. Copying it works anywhere, and it is the fallback if the CLI does not know
your agent:

```bash
git clone https://github.com/Aboudjem/loopify
cp -R loopify/skills/loopify ~/.claude/skills/
```

Swap the destination for your own agent's path from the table above. Copy the whole directory, not
just `SKILL.md`: `scripts/loop_line_lint.py` and `scripts/ticks_lint.py` live beside it and the
skill calls them by relative path. Nothing else in the repository is needed at run time.

## What changes outside Claude Code

The skill itself is portable, and so is the brief it writes: the per-tick definition of done, the
state directory, the safety rails, the counter and the stop rule are ordinary Markdown that any
agent can read. What does not travel is the second artifact. The line is a Claude Code `/loop`
line, and the brief's SCHEDULE step names `ScheduleWakeup`, `CronList`, `CronDelete` and `Monitor`,
which are Claude Code tools.

That case is already handled inside the brief. Its mode check has three branches, and branch (c) is
the one that runs everywhere else: run one cycle, log it, exit, and let an outside scheduler fire
the next tick.

Some agents have a repeat primitive of their own, and the exact command for each one is in
[running a brief under other agents](other-agents.md): Kimi CLI, GitHub Copilot CLI (`/every`),
Cursor (`/loop`), Qwen Code (`/loop`), Hermes (`hermes cron`) and Goose (`goose schedule`). The rest
wrap a one-shot headless call in OS cron or launchd. One thing changes shape there: outside Claude
Code the schedule outlives the loop, so when the stop rule fires you still have to remove the job by
hand.

## Next

- [Quickstart](quickstart.md), a first loop end to end.
- [The brief and the line](loop-md.md), what each artifact is for.
- [Honest limits](limits.md), what a running loop does and does not prove.
