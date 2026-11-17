<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-dark.svg">
    <img src="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-light.svg" alt="loopify：一个不用你盯着的循环。把重复的任务交给 Claude，回来时看到每个 tick 做了什么的日志。" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="https://github.com/Aboudjem/loopify/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <b>简体中文</b> · <a href="ja.md">日本語</a> · <a href="es.md">Español</a> · <a href="fr.md">Français</a>
</p>

<p align="center">
  <strong>别再盯着你的循环了。</strong>
</p>

<p align="center">
  <a href="#为什么用它">为什么用它</a> · <a href="#安装">安装</a> · <a href="#工作原理">工作原理</a> · <a href="#你会得到什么">你会得到什么</a> · <a href="#支持的智能体">支持的智能体</a> · <a href="#验证">验证</a> · <a href="#常见问题">常见问题</a> · <a href="#限制">限制</a>
</p>

<p align="center"><sub>本翻译可能落后于英文原文。<!-- may-lag --></sub></p>

把一个重复的任务交给 Claude。回来时看到的是每个 tick 做了什么的日志，而不是一个需要你盯着的循环。

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

然后在 Claude Code 里输入 `/loopify`，说出要重复的任务。一条命令就能告诉你循环现在的状态。
这里它运行在本仓库自带的示例上：

```bash
python3 skills/loopify/scripts/loop_status.py examples/loop-state/pr-babysitter --now 2026-09-01T09:50
```

```text
STATUS: NEEDS YOU · tick 7/30 · last tick 2026-09-01T09:40 (changed, 10 min ago) · 2 queued
Do next:
1. QUEUE.md, tick 4: Post the drafted reply on the `fetchAll` rename thread of PR #412
```

`--now` 固定了时钟，所以示例每次都输出 `NEEDS YOU`。完整报告见[你会得到什么](#你会得到什么)。

有些任务永远不会结束。发布用的 pull request 需要盯一整个下午，bug 报告会在夜里堆积。你启动了 `/loop`，
两小时后却说不清它到底做了没有。loopify 写出 `/loop` 每个 tick 都会重读的 brief，状态命令用一行读出日志。

循环只活在你打开的会话里，7 天后结束。没有评估器检查它，所以日志是唯一的证据。

## 为什么用它

- **一眼看清。** 一行状态给出 `OK`、`NEEDS YOU`、`STALE`、`STOPPED`、`NOT STARTED` 或 `BROKEN LOG`，
  再告诉你下一步做什么。证据：上面的示例，`make test` 会检查每个判定和退出码。
- **每个 tick 都看得到。** 每个 tick 往 `TICKS.md` 写一条记录。只要间隔已知，缺失的那条会显示为 `STALE`。
  loopify 会保存那一行，状态命令从中读取间隔。
  证据：超过两个间隔都没有新记录时，`loop_status.py` 会输出 `STALE`。
- **它有终点。** 停止规则就写在那一行里，而且每个循环 7 天后到期。
  证据：loopify 在输出这一行之前，会用八条规则检查它（`loop_line_lint.py`）。
- **更少卡住的 tick。** loopify 会列出需要预先批准的命令，例如 `gh pr view`。
  证据：它输出的交接说明第 1 步，见 [skill](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)。

## 安装

对于 Claude Code，在终端里运行这两条命令（不是在 Claude 会话里）：

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

其他智能体可以通过 [skills CLI](https://github.com/vercel-labs/skills) 用一行命令安装同一个 skill。用 `-a` 指定你的智能体，例如 `cursor`：

```bash
npx skills add Aboudjem/loopify -a cursor
```

不加 `-a` 时，CLI 会为它在你机器上检测到的每个智能体安装。

无需构建。这个 skill 是一个文件夹，里面有三个只用标准库的 Python 脚本。

## 工作原理

Claude Code 已经有 `/loop`：只要会话开着，它就会反复运行一个提示词。但它不会替你写这个提示词。

loopify 来写。它读取你的项目，只问几个真正重要的决定，然后写出两样东西。

- **brief，一个文件。** 任务的一轮：读什么、可以改什么、绝不能做什么、何时停止。循环每次都会重新打开它，
  所以运行中也可以编辑。
- **line，一个字符串。** 你把它粘贴到 `/loop` 里。它带着 brief 的路径和停止规则。

每一轮叫一个 **tick**。每个 tick，Claude 重读 brief，做一轮工作，并把发生的事写进 `TICKS.md`。

### 1. 描述任务

在 Claude Code 中输入 `/loopify`，说明要重复什么。loopify 会读 README、最近的提交和打开的 pull request，
然后一次性问几个简短的问题。

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file, re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string, you paste it below
```

`/Users/you/acme/` 代表你的项目。loopify 会打印你的真实路径。

### 2. 粘贴 line

```text
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

Claude 会立刻运行一轮，之后在该会话中每 20 分钟运行一次。PR 合并或满 30 个 tick 时停止，以先到者为准。
最常见的两个错误：

```text loop-antipattern
# not this: "every morning" can make /loop offer a cloud schedule instead, and nothing says when to stop
/loop every morning keep the release PR healthy

# and not the path alone: the tick gets a filename and no instruction
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

### 3. 读日志，或查看状态

`TICKS.md` 每个 tick 一条记录，顶部有一个计数器：

```text
tick: 7/30

## tick 7 · 2026-09-01T09:40 · changed
- CI: lint failed on src/api.ts → fixed the unused import, committed 4f2a1c9, npm test 12/12
- reviews: 1 new thread answered (rename), reply drafted in QUEUE.md
```

循环无法安全完成的事会在 `QUEUE.md` 里等你。一条命令就能读完这三个文件，并告诉你下一步做什么。见下一节。

## 你会得到什么

这是状态报告在本仓库示例状态目录上的真实输出：

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

`--now` 固定时钟，让示例每次输出都一样。真实循环中不要加它。

第 1 行永远是结论：`OK`、`NEEDS YOU`、`STALE`、`STOPPED`、`NOT STARTED` 或 `BROKEN LOG`。
然后最多三件要做的事，再然后是细节。`lessons` 统计 `LESSONS.md` 里的条目数。

退出码带着结论，脚本或 cron 任务可以据此行动：

| 退出码 | 结论 | 含义 |
| ------ | ---- | ---- |
| `0` | `OK`、`STOPPED`、`NOT STARTED` | 不需要你处理 |
| `1` | `NEEDS YOU`、`STALE`、`BROKEN LOG` | 去看看循环 |
| `2` | 无 | 用法错误，或状态目录不存在 |

`loop_status.py --help` 会打印同一张表。

loopify 写的每份 brief 还会给你：

- **line 里的停止规则和 tick 上限。** 完成任务的循环会停止，达到上限的循环也会停止。
- **无人值守运行的护栏。** 不碰账户，不付款，未经你同意不 push、不发布。循环读到的内容，比如 PR 评论，
  只是数据，绝不是指令。
- **可安全重复的条款。** brief 指定一个 tick 动手前要找的标记。运行两次的 tick 能看出工作已经做过。
- **格式固定的日志。** 每条记录都以 `## tick <n> · <ISO timestamp> · changed |
noop | stopped` 开头。`ticks_lint.py` 会检查它。
- **会学习的循环。** `LESSONS.md` 记下什么有效、什么浪费时间。

## 支持的智能体

下面每一行都是我在 2026-11-17 于一个空的临时文件夹中实际完成的安装。

| 智能体                   | 安装命令                                                              | 测试日期                               |
| ------------------------ | --------------------------------------------------------------------- | -------------------------------------- |
| Claude Code 2.1.326      | 从仓库的 marketplace 执行 `claude plugin install`，使用干净的配置目录 | 2026-11-17，插件已启用，脚本齐全       |
| Claude Code (skills CLI) | `npx skills add Aboudjem/loopify -a claude-code`                      | 2026-11-17，已复制到 `.claude/skills/` |
| Cursor                   | `npx skills add Aboudjem/loopify -a cursor`                           | 2026-11-17，位于 `.agents/skills/`     |
| Codex                    | `npx skills add Aboudjem/loopify -a codex`                            | 2026-11-17，位于 `.agents/skills/`     |
| GitHub Copilot           | `npx skills add Aboudjem/loopify -a github-copilot`                   | 2026-11-17，位于 `.agents/skills/`     |
| Gemini CLI               | `npx skills add Aboudjem/loopify -a gemini-cli`                       | 2026-11-17，位于 `.agents/skills/`     |

“测试”指文件已就位，且三个脚本能从安装后的副本运行。这不代表在该智能体里跑过一个循环。

有文档但未测试：OpenCode、Windsurf、Zed、Kimi Code CLI，以及手动复制 `skills/loopify/`。
见 [docs/editors.md](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md)。

brief 可以带走，line 不行。line 是 Claude Code 的 `/loop` 专用。在别处，brief 运行一轮、记录并退出，
由外部调度器触发下一个 tick。[docs/other-agents.md](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md)
介绍了 Kimi、Copilot CLI、Cursor、Goose 和 cron。

## 验证

下面每个数字都由 `make test` 打印。CI 在每次 push 和 pull request 时运行它。

```bash
make test
```

| 测试套件                    | 检查内容                                          | 结果    |
| --------------------------- | ------------------------------------------------- | ------- |
| `evals/check_skill.py`      | 以断言形式检查 skill 的契约                       | 161/161 |
| `tests/test_manifests.py`   | 清单、版本、示例 brief、翻译、SVG、密钥、长破折号 | 170/170 |
| `tests/test_ticks_lint.py`  | tick 日志格式                                     | 13/13   |
| `tests/test_loop_status.py` | 每种结论、退出码，以及本 README 示例的逐字节一致  | 62/62   |
| `tests/test_no_network.py`  | 发布的脚本不导入网络模块，也不调用 curl 或 wget   | 18/18   |
| `tests/test_dated_facts.py` | 以旧版本核对的 `/loop` 事实，在每处出现时都注明该版本 | 5/5 |
| `evals/loop_line_lint.py`   | 标准 line 通过八条规则                            | PASS    |

CI 还会在固定版本的 Claude Code 上运行 `claude plugin validate . --strict`，并检查
`npx skills@1.9.0 add . --list` 能找到这个 skill。

我在 2026-11-17 用 Claude Code 2.1.326 及其文档核对了 `/loop` 的事实。有一条无法在 2.1.326 上重新确认：
`/clear` 会清除计划。它仍标注为 2.1.252（2026-09-01）。逐条对照表见
[docs/limits.md](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md#which-version-each-fact-was-checked-on)。

## 常见问题

**loopify 会替我启动循环吗？**
不会。它写好 brief，打印 line，然后停下。你想开始时再粘贴 line。

**为什么是一个文件加一个字符串，而不是一个提示词？**
tick 需要细节：路径、命令、卡住时怎么办。`/loop` 需要一个每个 tick 都会重发的短提示词。brief 保存细节，
line 带着它的路径。

**怎么知道循环还活着？**
对状态目录运行 `loop_status.py`。如果超过两个间隔都没有新的 tick，它会显示 `STALE`。你也可以问 Claude
"what scheduled tasks do I have?"。

**什么会让循环停止？**
brief 里的停止规则、tick 上限、七天过期，或者你自己。完整列表见
[docs/faq.md](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md)。

**它会把我的代码发到别处吗？**
不会。loopify 的脚本不发起任何网络请求：只要有脚本导入网络模块或调用 curl、wget，
`tests/test_no_network.py` 就会失败。tick 只做你的 brief 允许的事。

## 限制

> [!IMPORTANT]
> 循环在运行，并不证明它在做正确的事。`/loop` 背后没有评估者。tick 日志和状态报告是唯一的证据。

- **循环活在你粘贴它的那个会话里。** 关掉终端它就停止。在 2.1.252 上，`/clear` 也会清除计划。问一句 "what scheduled tasks do I have?" 来确认。
- **每个循环 7 天后结束。** 一个会话最多容纳 50 个计划任务。这两条都是 Claude Code 的限制。重新粘贴 line 即可继续。
- **预先批准 tick 要运行的命令。** 遇到权限提示的 tick 会一直等待回答。loopify 会打印需要允许的命令，
  比如 `gh pr view` 或 `git commit`。
- **状态报告需要知道间隔**，才能区分活着的循环和停掉的循环。它从保存的 line 或 `--interval` 读取。

带出处的完整列表：[docs/limits.md](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md)。

## 了解更多

- [快速开始](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md)：一步步建立你的第一个循环
- [在编辑器中安装](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md)：智能体代码和两种安装方式
- [完整示例](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md)：一份完整的 brief，line 在末尾
- [其他智能体](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md)：同一份 brief 在 Kimi、Cursor、Goose 和 cron 下
- [FAQ](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) · [`loop.md` 指针](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) · [Changelog](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) · [贡献](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) · [skill 本身](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

如果你用过 [goalify](https://github.com/Aboudjem/goalify)，会觉得很熟悉。goalify 用于会结束的任务，
loopify 用于会重复的任务。

---

<sub>作者 <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT。`/loop` 的行为于 2026-11-17
依据 Claude Code 2.1.326 和官方文档核对，`/clear` 除外，它最后一次核对是在 2.1.252（2026-09-01）。<a href="https://github.com/Aboudjem/loopify/blob/main/docs/limits.md#which-version-each-fact-was-checked-on">逐条对照表</a>。姊妹项目 <a href="https://github.com/Aboudjem/goalify">goalify</a> 为 `/goal` 做同样的事。
<a href="https://github.com/Aboudjem/loopify/issues">发现缺漏了吗？</a></sub>

<sub>本译文由机器辅助翻译并经过校对，以英文版 <a href="../README.md">README.md</a> 为准。</sub>
