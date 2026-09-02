<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-dark.svg">
    <img src="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-light.svg" alt="loopify：一个不用你盯着的循环。把一项会重复的工作交给 Claude，回来看每个 tick 做了什么的日志。" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="https://github.com/Aboudjem/loopify/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <a href="https://github.com/Aboudjem/loopify/stargazers"><img src="https://img.shields.io/github/stars/Aboudjem/loopify?color=2BE8C8&labelColor=0A0F1C" alt="stars"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <b>简体中文</b> · <a href="ja.md">日本語</a> · <a href="es.md">Español</a> · <a href="fr.md">Français</a>
</p>

<p align="center">
  <strong>把一项会重复的工作交给 Claude。回来时你看到的是每个 tick 做了什么的日志，而不是一个需要你盯着的循环。</strong>
</p>

<p align="center">
  <a href="#它做什么">它做什么</a> · <a href="#安装">安装</a> · <a href="#怎么用">怎么用</a> · <a href="#在你的编辑器里">在你的编辑器里</a> · <a href="#值得先知道的事">值得先知道的事</a> · <a href="#了解更多">了解更多</a>
</p>

<p align="center"><sub>本翻译可能落后于英文原文。<!-- may-lag --></sub></p>

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

## 它做什么

有些工作其实永远做不完。一个发布用的 pull request 需要有人盯着一整个下午；新的 bug 报告在夜里堆积，
最好在有人认真读之前先过一遍。Claude Code 已经有一个用来重复工作的命令 `/loop`：你给它一段提示词和一个
时间间隔，只要会话还开着，它就会一遍遍地运行这段提示词。它不替你写的，正是那段提示词。

loopify 来写这段提示词。你只用普通的话把工作描述一次。loopify 会趁 Claude 还带着你的上下文时读你的项目，
问你几个真正需要决定的问题（多久跑一次、什么时候停、可以改动什么），然后写出两样东西。

- **简报，一个文件。** 一轮工作的说明：读什么、可以改什么、绝对不能做什么、什么时候停、把发生的事写到
  哪里。循环在每次运行开始时都会重新打开这个文件，所以两次运行之间不会丢失任何东西，而且循环正在跑的
  时候你也可以改它。
- **一行命令，一个字符串。** 你把它粘贴进 `/loop`。简报的路径就在这一行里面，所以每次运行都知道该去哪里
  读。停止规则也在里面，所以循环会按你的条件结束。

每次运行就是一个 **tick**。每个 tick，Claude 会重新读简报，做一轮工作，然后把发生的事写进一个叫
`TICKS.md` 的日志。你不用熬夜等着，但你要读这份日志。

如果你用过 [goalify](https://github.com/Aboudjem/goalify)，这会很眼熟。goalify 面向的是会结束的工作：
一个大任务、一个完成的定义、`/goal`。loopify 面向的是会重复的工作。

## 安装

上面两条命令会添加 10x 插件市场，并把插件装进 Claude Code；loopify 是在 Claude Code 2.1.252 上验证过的。
其他智能体也可以用 [skills CLI](https://github.com/vercel-labs/skills) 一行装上同一个技能目录：

```bash
npx skills add Aboudjem/loopify
```

## 怎么用

### 1. 描述这项工作

在 Claude Code 的对话里输入 `/loopify`，说清楚要重复什么。loopify 会读 README、最近的提交和打开的 pull
request，然后集中问你一轮简短的问题。

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file, re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string, you paste it below
```

`/Users/you/acme/` 代表你的项目；loopify 会打印你真实的路径。

### 2. 粘贴这一行

```text
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

Claude 会立刻跑一轮，之后在那个会话里每 20 分钟跑一次，直到这个 pull request 被合并，或者跑满 30 个
tick，以先到者为准。不写时间间隔，Claude 就自己掌握节奏。最常见的两个写法错误：

```text loop-antipattern
# 不要这样写："every morning" 这种说法可能会让 /loop 转而提供云端排期，而且这里没有停止规则
/loop every morning keep the release PR healthy

# 也不要只给路径：这个 tick 只拿到一个文件名，没有任何指令
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

### 3. 读日志

`TICKS.md` 里每个 tick 一条记录，写明改了什么以及对应的证据，顶部还有一个计数器：

```text
tick: 7/30

## tick 7 · 2026-09-01T09:40 · changed
- CI: lint failed on src/api.ts → fixed the unused import, committed 4f2a1c9, npm test 12/12
- reviews: 1 new thread answered (rename), reply drafted in QUEUE.md
```

循环不能安全完成的事情，都会留在 `QUEUE.md` 里等你。

## 你会得到什么

- **一份不会乱动的简报。** 每个 tick 都重新读一遍，从不归档，也不会被循环改写。多久跑一次、什么时候停、
  可以改动什么，都在第一个 tick 之前就定好了。
- **停止规则和 tick 上限就写在那一行里。** 做完工作的循环会停，跑到上限的循环也会停。
- **无人值守运行的护栏。** 不碰账号，不付款，除非你明确同意，否则不 push 也不发布。循环读到的任何东西，
  比如一条 pull request 评论，都是数据，绝不是指令。
- **每份简报都有一条“重复运行也安全”的条款。** 简报会写明一个 tick 动手之前要找的标记，这样再跑一次的
  tick 就能判断这件事已经做过了。
- **有固定格式的日志。** `TICKS.md` 的每条记录都以同样的表头开头，
  `## tick <n> · <ISO timestamp> · changed | noop | stopped`，可以用
  `skills/loopify/scripts/ticks_lint.py` 检查。`QUEUE.md` 里被卡住的条目会带上 `reason:` 行和
  `unblock:` 行。
- **一个会学习的循环。** `LESSONS.md` 记下哪些做法有效、哪些在浪费时间，循环每个 tick 都会重新读它。

## 在你的编辑器里

可以在 Claude Code、Cursor、Codex、Copilot、Gemini CLI，以及通过 `npx skills add` 支持的另外 70 多个
智能体里使用。

| 在哪里 | 怎么装 |
| --- | --- |
| Claude Code | `claude plugin install loopify@10x` |
| Cursor、Codex、Gemini CLI、OpenCode、Windsurf、Zed、Kimi Code CLI | `npx skills add Aboudjem/loopify -a <agent>` |
| VS Code 和 GitHub Copilot | `npx skills add Aboudjem/loopify -a github-copilot` |
| 其他所有情况 | 把 `skills/loopify/` 复制到你的智能体的技能目录 |

loopify 只是一个技能目录，旁边放着两个只用标准库的 Python 脚本，没有服务要跑，也没有东西要编译。每个
智能体的 `-a` 代号、两个安装路径，以及手动复制的做法，都在
[docs/editors.md](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md) 里。

简报可以跨工具带走，那一行不行。那一行是 Claude Code 的 `/loop` 命令行，而简报里的排期步骤用的是
Claude Code 的工具。简报本身留好了这个分支：跑一轮、记录、退出，让外部的调度器触发下一个 tick。
[docs/other-agents.md](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) 覆盖了 Kimi、
Copilot CLI、Cursor、Qwen Code、Hermes、Goose 和普通的 cron。

## 值得先知道的事

> [!IMPORTANT]
> 循环在跑，并不证明它在做对的事。请读 tick 日志。`/loop` 背后没有任何评估器，简报里逐 tick 的检查清单
> 和 `TICKS.md` 是仅有的证据。

- **循环活在你粘贴它的那个会话里。** 只有那个会话开着它才会触发。关掉终端它就停了，`/clear` 也会清掉
  排期。把 Claude Code 放到后台运行，可以在没有窗口的情况下让它继续活着。
- **任何循环都会在 7 天时结束**，而且一个会话最多容纳 50 个已排期的任务。这两条都是 Claude Code 对排期
  工作的限制，不是 loopify 的限制。想继续，把那一行再粘贴一次。
- **提前批准 tick 会执行的命令。** loopify 会打印循环需要的命令，比如 `gh pr view` 或 `git commit`。
  撞上权限询问的 tick 会一直等在那里，直到有人回答。

## 了解更多

- [快速上手](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md)：第一个循环的完整步骤，
  以及不开终端时怎么跑
- [装进你的编辑器](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md)：智能体代号和 skills
  CLI 的两个路径
- [一个完整示例](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md)：一份完整
  简报，那一行就在末尾
- [如实说明的局限](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md)：loopify 不承诺的所有
  事情，每条都能追溯到二进制文件或官方文档
- [其他智能体](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md)：同一份简报在 Kimi、
  Cursor、Goose 和普通 cron 下怎么跑
- [常见问题](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) · [`loop.md` 指针](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) · [更新日志](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) · [参与贡献](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) · [技能本身](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

---

<sub>由 <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> 制作 · MIT。`/loop` 的行为是 2026 年从
已发布的 Claude Code 2.1.252 二进制文件和官方文档重新推导的。它是
<a href="https://github.com/Aboudjem/goalify">goalify</a> 的姊妹项目，后者为 `/goal` 做同样的事。
<a href="https://github.com/Aboudjem/loopify/issues">发现缺漏了吗？</a></sub>

<sub>本译文由机器辅助翻译并经过校对，以英文版 <a href="../README.md">README.md</a> 为准。</sub>
