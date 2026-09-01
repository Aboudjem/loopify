<p align="center">
  <a href="../README.md">English</a> ·
  <b>简体中文</b> ·
  <a href="ja.md">日本語</a> ·
  <a href="es.md">Español</a> ·
  <a href="fr.md">Français</a>
</p>

<p align="center"><sub>此译文可能落后于英文原版。<!-- may-lag --></sub></p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero.svg" alt="四个步骤：描述一项要重复的工作，得到一份简报（一个文件）和一行命令（一个字符串），把这一行粘贴进 /loop，然后回来查看 tick 日志。" width="100%">
</p>

<h1 align="center">loopify</h1>

<p align="center">
  <strong>把一项会反复出现的工作交给 Claude。回来看到的是每次 tick 都做了什么的日志——而不是一个需要你盯着的循环。</strong>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="https://github.com/Aboudjem/loopify/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-skill-d97757" alt="Claude Code skill">
  <a href="https://skills.sh/Aboudjem/loopify"><img src="https://skills.sh/b/Aboudjem/loopify" alt="skills.sh"></a>
</p>

有些工作从来做不完。一个发布 PR 需要有人整个下午盯着它的检查项、回复评审者的意见。一次部署需要每隔几分钟查看一次，直到它稳定下来。新的 bug 报告会在夜里不断堆积，需要有人在别人看到之前先看一遍。你可以让 Claude 把这些事各做一次。真正麻烦的，是让它按计划持续做下去，而你不用守在旁边。

Claude Code 有一个用来重复工作的命令：`/loop`。你给它一段提示词和一个时间间隔，只要你的会话保持打开，它就会一遍遍运行这段提示词。但它不会替你把提示词写好。写得太短，循环会忘记自己上一次决定过什么；写得太长，它可能会推送你从未想要推送的东西，或者在工作早就完成之后还继续运行——因为没有人告诉它该在什么时候停下。

loopify 是一个 Claude Code 技能，会替你把这段提示词好好写出来。你只需用大白话描述一次这项工作。趁 Claude 还掌握着你的上下文，loopify 会读取你的项目，问你几个真正重要的决定（多久跑一次、什么时候停、它能碰哪些东西），然后写出两样东西。

第一样是**简报**：一个描述这项工作每一轮该做什么的文件——该读什么、能改什么、绝不能做什么、什么时候停下来，以及要把发生的事写在哪里。循环每次运行开始时都会重新打开这个文件，所以不会在两次运行之间遗漏什么；而且你可以在循环运行期间编辑它。

第二样是**那一行**：一小段你粘贴进 `/loop` 的字符串。简报的路径就藏在这行里，所以每次运行都知道该去哪里找；停止规则也在里面，所以循环几时结束由你决定。

每一次运行称为一次 **tick**。每次 tick，Claude 都会重新读一遍简报，完成一轮工作，并把发生的事写进一份叫 `TICKS.md` 的日志。可以把它想象成一个拿着记录板巡夜的守夜人：简报是钉在墙上的巡查表，那一行是你贴出的排班，日志则是你早上翻看的那块记录板。你不必熬夜守着，但你得看那块记录板。

## 你会得到什么

- ⚡ **一行就能交出去。** 粘贴一次即可——无论是在当前会话，还是那个项目下打开的任意会话里。简报的路径就藏在这行命令里。
- 📋 **简报常驻不变。** 它是一个固定不动的文件：每次 tick 都会重新读取，从不归档，也不会被循环改写。你可以在两次 tick 之间打开它，改动其中的某个决定。
- 🧭 **先把那几个真正重要的选择定下来。** 多久跑一次、什么时候停、它能碰哪些东西——这些问题只在第一次 tick 之前问一次，而不是留到第 12 次 tick 才临时猜。
- 🛑 **那一行里自带停止规则和 tick 上限。** 完成了工作的循环会停下来，达到上限的循环也会停下来。不会有循环在无人留意的情况下意外撞上 7 天的默认上限。
- 🔒 **给无人值守的运行装上护栏。** 不碰账号、不碰支付，未经你允许不推送、不发布。循环沿途读到的一切——比如一条 PR 评论或一个 issue——都只是数据，从来不是指令。
- 🗒️ **一份你看得懂的日志。** `TICKS.md` 记录每一次 tick，并附上它做了什么的证据；`QUEUE.md` 保存它没法安全完成、留给你处理的事项。
- 🧠 **一个会学习的循环。** `LESSONS.md` 保存哪些做法有效、哪些白费了时间，循环每次 tick 都会重新读取它。
- 🔁 **粘贴一次即可重启。** 简报保持原样不变；循环结束后，再粘贴一次那一行就行。

## 三个步骤

### 1. 先安装一次

打开终端，添加 10x 应用市场，然后安装这个插件。loopify 已针对 Claude Code 2.1.252 验证过；[快速上手](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md) 里还有其他安装方式。

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

如果你更喜欢用 [skills CLI](https://skills.sh)，一条命令就能达到同样效果：`npx skills add Aboudjem/loopify`

### 2. 描述这项工作，然后粘贴那一行

在 Claude Code 聊天框里输入 `/loopify`，说出你想让它重复做的事。以下是一个需要持续照看的发布 PR 会是什么样子：

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file — re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string — you paste it below

/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

loopify 会先读取你的项目：查看 README、最近的提交，还有未合并的 PR，然后问你一小批问题——多久跑一次、什么时候停、循环能改动什么。接着它会写出简报并打印出那一行。`/Users/you/acme/` 只是你项目路径的占位符；loopify 打印出来的会是你的真实路径。

把那一行粘贴进聊天框。在上面的例子里，Claude 会立刻运行一轮，然后在那个会话里每 20 分钟运行一次，直到 PR 合并或者跑满 30 次 tick，以先到者为准。如果那一行里不写时间间隔，Claude 会自己把握节奏，在没什么动静时等得更久一些。

### 3. 读日志

你可以随时回来看看。`TICKS.md` 里每次 tick 一条记录，写着改了什么、证据是什么，顶部还有一个计数器，让你看出循环跑到哪一步了：

```text
tick: 7/30

## tick 7 · 2026-09-01T09:40 · changed
- CI: src/api.ts 的 lint 检查失败 → 修复了未使用的 import，提交 4f2a1c9，npm test 12/12
- reviews: 回复了 1 个新评审串（重命名），回复草稿写在 QUEUE.md 里
```

循环没法安全完成的事——比如一条它不该擅自发出的评审回复——会留在 `QUEUE.md` 里等你处理。

### 那一行，对的写法和错的写法

写对的那一行会带着简报的路径和停止规则。下面两个错误示例是大家最常犯的错：一种是按天描述的说法，可能会让 `/loop` 转而提供云端排期，而不是本地循环；另一种是只给路径，这样 tick 就没有任何指令可执行。

```text loop-antipattern
# 这行本身——loopify 打印出的原始字符串（144 个字符）
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.

# 不要这样写——"every morning" 这种说法可能会让 /loop 转而提供云端排期，而且这里没有停止规则
/loop every morning keep the release PR healthy

# 也不要只给路径——这样 tick 只拿到一个文件名，没有任何指令
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

### 在你第一次运行循环之前，值得了解的几件事

- **循环活在你粘贴它的那个会话里。** 只有那个会话保持打开，它才会触发。关掉终端它就停了；`/clear` 也会把排期一并清掉。在后台运行 Claude Code 可以让它在没有窗口的情况下继续存活。
- **提前批准 tick 要运行的命令。** loopify 会打印出循环需要用到的命令，比如 `gh pr view` 或 `git commit`。在粘贴那一行之前，把它们加进你的许可清单。如果某次 tick 撞上了权限确认提示，它会停在那里，直到有人回应。
- **每个循环都会在 7 天后结束。** 这是 Claude Code 对排期工作的规定，两种模式都一样。再粘贴一次那一行，循环就会按简报里写的地方继续。
- **想提前停下**，可以在自定节奏的循环等待时按 `Esc`；对固定间隔的循环，就说"取消 pr-babysitter 任务"。可以问一句"我有哪些排期任务？"来确认它已经没了。

> [!IMPORTANT]
> 循环在运行不代表它做的事是对的——请去读 tick 日志。没有任何机制会对
> `/loop` 做评判；简报里每次 tick 的检查清单和 `TICKS.md` 是仅有的证据。循环运行
> 在你粘贴它的那个 Claude Code 会话内部：只有那个会话保持打开，它才会触发。每个
> 循环都会在 7 天后停止；再粘贴一次那一行即可重新开始。

## 了解更多

- [快速上手](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md) — 你的第一个循环、其他安装方式、在不打开终端的情况下运行
- [一个完整示例](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md) — 一份完整的发布 PR 简报，末尾附着那一行
- [如实说明的局限](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md) — loopify 不承诺做到的所有事，每一条都能追溯到 Claude Code 的二进制文件或官方文档
- [其他智能体](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) — 同一份简报在 Kimi、Copilot CLI、Cursor、Qwen Code、Hermes、Goose 和普通 cron 下的用法
- [常见问题](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) · [`loop.md` 指针文件](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) · [更新日志](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) · [贡献指南](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) · [技能本身](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

如果你用过 [goalify](https://github.com/Aboudjem/goalify)，这一切会显得很眼熟。goalify 面向的是能做完的工作：一个大任务、一个明确的完成标准、`/goal`。loopify 面向的是会反复出现的工作。同一个作者，同样先写测试的习惯，同样如实说明工具做不到什么。

---

<sub>由 <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> 构建 · MIT 许可。`/loop` 的行为于
2026 年根据实际发布的 Claude Code 2.1.252 二进制文件与官方文档重新推导得出。是
<a href="https://github.com/Aboudjem/goalify">goalify</a> 的姊妹项目，goalify 为 `/goal` 做同样的事。
<a href="https://github.com/Aboudjem/loopify/issues">发现遗漏了吗？</a></sub>
