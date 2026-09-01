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

loopify 是一个 Claude Code 技能，用于那些永远做不完的工作：在评审陆续到来时维持发布 PR 健康、盯着一次部署
直到它稳定下来、每小时清理一遍新的 bug 报告、整夜守着分支、让它保持绿色。你只需描述一次这项工作。loopify
会读取你的项目，问你几个真正需要你决定的问题，然后写下这项工作每一轮该做什么——趁 Claude 还掌握着你的
上下文。然后，它会交给你一行可以直接粘贴的命令。

它会写出两样东西。**简报**是一个文件：写清楚每一轮该做什么、绝不能做什么、什么时候停下来，以及笔记要写
在哪里。**那一行**是一小段字符串，你把它粘贴进 `/loop`——Claude Code 内置的重复执行命令。`/loop` 会按你
选定的时间间隔重新运行一段提示词，或者交给 Claude 自己把握节奏。每次运行称为一次 **tick**。每一次
tick，Claude 都会重新读一遍简报、完成一轮工作，并把发生的事写进日志。可以把它想象成一个拿着记录板巡夜
的守夜人：简报是贴在墙上的巡查表，那一行是你贴出的班次，日志则是你早上翻看的记录板。

## 你会得到什么

- ⚡ **一行就能交出去** — 粘贴一次即可；简报的路径已经藏在这行命令里。
- 📋 **简报常驻不变** — 一个固定不动的文件，每次 tick 都会重新读取，从不归档。
- 🧭 **先敲定那几个真正重要的选择** — 多久跑一次、什么时候停、它能碰哪些东西。
- 🛑 **那一行里自带停止规则和 tick 上限** — 循环按你定的条件结束，而不是意外撞上 7 天的默认上限。
- 🔒 **给无人值守的运行装上护栏** — 不碰账号、不碰支付，未经你允许不推送、不发布；它读到的一切都只是数据，从来不是指令。
- 🗒️ **一份你看得懂的日志** — `TICKS.md` 记录每一次 tick 并附上证据；`QUEUE.md` 保存它留给你处理的事项。
- 🧠 **一个会学习的循环** — `LESSONS.md` 保存有效的做法，并在每次 tick 时重新读取。
- 🔁 **粘贴一次即可重启** — 简报保持原样；再粘贴一次那一行就行。

## 三个步骤

在终端里安装一次即可（已针对 Claude Code 2.1.252 验证；更多内容见
[快速上手](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md)）：

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

或者用 [skills CLI](https://skills.sh)：`npx skills add Aboudjem/loopify`

然后，在 Claude Code 聊天框里：

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file — re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string — you paste it below

/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

1. **描述这项工作。** 输入 `/loopify`，加上你想重复做的事。loopify 会读取你的项目，问你几个真正需要
   回答的问题，然后写出简报和那一行命令。
2. **粘贴那一行。** 可以在当前会话，也可以在打开该项目的任意会话里粘贴。简报的路径就藏在这行命令
   里，因为每次 tick 都会重新打开这个文件。`/Users/you/acme/` 只是你项目路径的占位符；loopify 打印出来的会是你的真实路径。
3. **读日志。** 回来看 `TICKS.md`：每次 tick 一条记录，写着改了什么、证据是什么。它没法安全完成的
   事，会留在 `QUEUE.md` 里等你处理。

```text loop-antipattern
# 这行本身——loopify 打印出的原始字符串（144 个字符）
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.

# 不要这样写——"every morning" 这种说法可能会让 /loop 转而提供云端排期，而且这里没有停止规则
/loop every morning keep the release PR healthy

# 也不要只给路径——这样 tick 只拿到一个文件名，没有任何指令
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

> [!IMPORTANT]
> 循环在运行不代表它做的事是对的——请去读 tick 日志。没有任何机制会对
> `/loop` 做评判；简报里每次 tick 的检查清单和 `TICKS.md` 是仅有的证据。循环运行
> 在你粘贴它的那个 Claude Code 会话内部：只有那个会话保持打开，它才会触发。每个
> 循环都会在 7 天后停止；再粘贴一次那一行即可重新开始。

## 了解更多

- [快速上手](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md) — 你的第一个循环、其他安装方式、在不打开终端的情况下运行
- [一个完整示例](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md) — 一份真实的简报，以及它末尾附的那一行命令
- [如实说明的局限](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md) — loopify 不承诺做到的所有事
- [其他智能体](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) — 同一份简报在 Kimi、Copilot CLI、Cursor、Qwen Code、Hermes、Goose 和 cron 下的用法
- [常见问题](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) · [`loop.md` 指针文件](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) · [更新日志](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) · [贡献指南](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) · [技能本身](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

---

<sub>由 <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> 构建 · MIT 许可。`/loop` 的行为于
2026 年根据实际发布的 Claude Code 2.1.252 二进制文件与官方文档重新推导得出。是
<a href="https://github.com/Aboudjem/goalify">goalify</a> 的姊妹项目，goalify 为 `/goal` 做同样的事。
<a href="https://github.com/Aboudjem/loopify/issues">发现遗漏了吗？</a></sub>
