<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-dark.svg">
    <img src="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-light.svg" alt="loopify のバナー: 見出し Your loop, in one line、3 つのチップ No babysitting、Fewer stuck ticks、Stops by itself、7 個が済んだ 30 個の tick の輪、インストールコマンドと状態行 STATUS: NEEDS YOU, tick 7/30。" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="https://github.com/Aboudjem/loopify/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <a href="zh-CN.md">简体中文</a> · <b>日本語</b> · <a href="es.md">Español</a> · <a href="fr.md">Français</a>
</p>

<p align="center"><strong>繰り返すエージェントの仕事を、1 行で確認。</strong></p>

<p align="center">
  <a href="#インストール">インストール</a> · <a href="#しくみ">しくみ</a> · <a href="#得られるもの">得られるもの</a> · <a href="#対応エージェント">対応エージェント</a> · <a href="#検証">検証</a> · <a href="#faq">FAQ</a> · <a href="#制限">制限</a>
</p>

<p align="center"><sub>この翻訳は英語の原文より古い場合があります。<!-- may-lag --></sub></p>

loopify は `/loop` の line と brief を書きます。あとは 1 つのコマンドがログを読みます。

| 見張らなくていい | 止まる tick が減る | 自分で止まる |
|:--|:--|:--|
| `loop_status.py` は 6 つの判定のどれかと、やることを最大 3 つ出します。 | loopify は `gh pr view` など、先に許可するコマンドを出します。 | line には停止ルールが入っています。どの `/loop` も 7 日で終わります。 |

tick は、繰り返す仕事の 1 回分の実行です。`make test` がすべての判定と終了コードを確認します。

**対応:** Claude Code の `/loop`。skill は、skill を読むどのエージェントにもインストールできます。インストールを確認済み: Claude Code、Codex、Cursor、Gemini CLI、GitHub Copilot、OpenCode。特定のモデルに依存しません。中身は Markdown と 3 つのシンプルな Python スクリプトです。

```bash
npx skills add Aboudjem/loopify -g -a claude-code
# then, in Claude Code: /loopify keep our release PR healthy, every 20 minutes
```

このリポジトリにある例で状態コマンドを実行した結果:

```bash
python3 skills/loopify/scripts/loop_status.py examples/loop-state/pr-babysitter --now 2026-09-01T09:50
```

```text
STATUS: NEEDS YOU · tick 7/30 · last tick 2026-09-01T09:40 (changed, 10 min ago) · 2 queued
Do next:
1. QUEUE.md, tick 4: Post the drafted reply on the `fetchAll` rename thread of PR #412
```

`--now` で時計を固定しているので、この例はいつも `NEEDS YOU` を出します。

**何か:** Claude Code の `/loop` 用に brief と line を書く skill です。
**いつ使うか:** 午後ずっと pull request を見守るような、繰り返す仕事に。
**得られるもの:** ループがあなたを必要としているかを示す 1 行の状態。

ループは開いているセッションの中で動き、7 日で終わります。

## インストール


**おすすめ: Vercel の skills CLI。** `npx skills` は、エージェント skill 用の Vercel のオープンなインストーラーです。

```bash
npx skills add Aboudjem/loopify -g
```

70 以上のエージェントで使えます。メニューから選んでください（[対応エージェント](https://github.com/vercel-labs/skills#supported-agents)）。すべてのプロジェクト向けに入ります。

ターミナルではエージェントのメニューが出ます。スクリプトではすべてのエージェントのフォルダに入るので、`-a <agent>` を付けてください。

<a href="https://skills.sh/aboudjem/loopify"><img src="https://img.shields.io/badge/skills.sh-000000?style=flat-square&logo=vercel&logoColor=white" alt="skills.sh" height="24"></a> loopify のページ: [skills.sh/aboudjem/loopify](https://skills.sh/aboudjem/loopify).

**または、1 つのエージェントに直接インストール。** どのコマンドも、すべてのプロジェクト向けに入ります。

<p align="center">
  <a href="#install-claude-code"><img src="https://img.shields.io/badge/Claude_Code-D97757?style=flat-square&logo=claude&logoColor=white" alt="Claude Code" height="24"></a>
  <a href="#install-codex"><img src="https://img.shields.io/badge/Codex-000000?style=flat-square&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyBmaWxsPSJ3aGl0ZSIgcm9sZT0iaW1nIiB2aWV3Qm94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI%2BPHRpdGxlPk9wZW5BSTwvdGl0bGU%2BPHBhdGggZD0iTTIyLjI4MTkgOS44MjExYTUuOTg0NyA1Ljk4NDcgMCAwIDAtLjUxNTctNC45MTA4IDYuMDQ2MiA2LjA0NjIgMCAwIDAtNi41MDk4LTIuOUE2LjA2NTEgNi4wNjUxIDAgMCAwIDQuOTgwNyA0LjE4MThhNS45ODQ3IDUuOTg0NyAwIDAgMC0zLjk5NzcgMi45IDYuMDQ2MiA2LjA0NjIgMCAwIDAgLjc0MjcgNy4wOTY2IDUuOTggNS45OCAwIDAgMCAuNTExIDQuOTEwNyA2LjA1MSA2LjA1MSAwIDAgMCA2LjUxNDYgMi45MDAxQTUuOTg0NyA1Ljk4NDcgMCAwIDAgMTMuMjU5OSAyNGE2LjA1NTcgNi4wNTU3IDAgMCAwIDUuNzcxOC00LjIwNTggNS45ODk0IDUuOTg5NCAwIDAgMCAzLjk5NzctMi45MDAxIDYuMDU1NyA2LjA1NTcgMCAwIDAtLjc0NzUtNy4wNzI5em0tOS4wMjIgMTIuNjA4MWE0LjQ3NTUgNC40NzU1IDAgMCAxLTIuODc2NC0xLjA0MDhsLjE0MTktLjA4MDQgNC43NzgzLTIuNzU4MmEuNzk0OC43OTQ4IDAgMCAwIC4zOTI3LS42ODEzdi02LjczNjlsMi4wMiAxLjE2ODZhLjA3MS4wNzEgMCAwIDEgLjAzOC4wNTJ2NS41ODI2YTQuNTA0IDQuNTA0IDAgMCAxLTQuNDk0NSA0LjQ5NDR6bS05LjY2MDctNC4xMjU0YTQuNDcwOCA0LjQ3MDggMCAwIDEtLjUzNDYtMy4wMTM3bC4xNDIuMDg1MiA0Ljc4MyAyLjc1ODJhLjc3MTIuNzcxMiAwIDAgMCAuNzgwNiAwbDUuODQyOC0zLjM2ODV2Mi4zMzI0YS4wODA0LjA4MDQgMCAwIDEtLjAzMzIuMDYxNUw5Ljc0IDE5Ljk1MDJhNC40OTkyIDQuNDk5MiAwIDAgMS02LjE0MDgtMS42NDY0ek0yLjM0MDggNy44OTU2YTQuNDg1IDQuNDg1IDAgMCAxIDIuMzY1NS0xLjk3MjhWMTEuNmEuNzY2NC43NjY0IDAgMCAwIC4zODc5LjY3NjVsNS44MTQ0IDMuMzU0My0yLjAyMDEgMS4xNjg1YS4wNzU3LjA3NTcgMCAwIDEtLjA3MSAwbC00LjgzMDMtMi43ODY1QTQuNTA0IDQuNTA0IDAgMCAxIDIuMzQwOCA3Ljg3MnptMTYuNTk2MyAzLjg1NThMMTMuMTAzOCA4LjM2NCAxNS4xMTkyIDcuMmEuMDc1Ny4wNzU3IDAgMCAxIC4wNzEgMGw0LjgzMDMgMi43OTEzYTQuNDk0NCA0LjQ5NDQgMCAwIDEtLjY3NjUgOC4xMDQydi01LjY3NzJhLjc5Ljc5IDAgMCAwLS40MDctLjY2N3ptMi4wMTA3LTMuMDIzMWwtLjE0Mi0uMDg1Mi00Ljc3MzUtMi43ODE4YS43NzU5Ljc3NTkgMCAwIDAtLjc4NTQgMEw5LjQwOSA5LjIyOTdWNi44OTc0YS4wNjYyLjA2NjIgMCAwIDEgLjAyODQtLjA2MTVsNC44MzAzLTIuNzg2NmE0LjQ5OTIgNC40OTkyIDAgMCAxIDYuNjgwMiA0LjY2ek04LjMwNjUgMTIuODYzbC0yLjAyLTEuMTYzOGEuMDgwNC4wODA0IDAgMCAxLS4wMzgtLjA1NjdWNi4wNzQyYTQuNDk5MiA0LjQ5OTIgMCAwIDEgNy4zNzU3LTMuNDUzN2wtLjE0Mi4wODA1TDguNzA0IDUuNDU5YS43OTQ4Ljc5NDggMCAwIDAtLjM5MjcuNjgxM3ptMS4wOTc2LTIuMzY1NGwyLjYwMi0xLjQ5OTggMi42MDY5IDEuNDk5OHYyLjk5OTRsLTIuNTk3NCAxLjQ5OTctMi42MDY3LTEuNDk5N1oiLz48L3N2Zz4%3D" alt="Codex" height="24"></a>
  <a href="#install-cursor"><img src="https://img.shields.io/badge/Cursor-3B3B3B?style=flat-square&logo=cursor&logoColor=white" alt="Cursor" height="24"></a>
  <a href="#install-gemini-cli"><img src="https://img.shields.io/badge/Gemini-1A73E8?style=flat-square&logo=googlegemini&logoColor=white" alt="Gemini CLI" height="24"></a>
  <a href="#install-github-copilot"><img src="https://img.shields.io/badge/Copilot-24292F?style=flat-square&logo=githubcopilot&logoColor=white" alt="GitHub Copilot" height="24"></a>
  <a href="#install-opencode"><img src="https://img.shields.io/badge/OpenCode-4A4A4A?style=flat-square&logo=opencode&logoColor=white" alt="OpenCode" height="24"></a>
</p>

<a id="install-claude-code"></a>**Claude Code**, インストール確認済み。`/loop` は Claude Code にしかありません:

```bash
npx skills add Aboudjem/loopify -g -a claude-code
```

<a id="install-codex"></a>**Codex**, インストール確認済み:

```bash
npx skills add Aboudjem/loopify -g -a codex
```

<a id="install-cursor"></a>**Cursor**, インストール確認済み:

```bash
npx skills add Aboudjem/loopify -g -a cursor
```

<a id="install-gemini-cli"></a>**Gemini CLI**, インストール確認済み:

```bash
npx skills add Aboudjem/loopify -g -a gemini-cli
```

<a id="install-github-copilot"></a>**GitHub Copilot**, インストール確認済み:

```bash
npx skills add Aboudjem/loopify -g -a github-copilot
```

<a id="install-opencode"></a>**OpenCode**, インストール確認済み:

```bash
npx skills add Aboudjem/loopify -g -a opencode
```

このプロジェクトだけに入れるなら `-g` を外します。ほかのエージェントの `-a` コードは [docs/editors.md](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md) にあります。

**または Claude Code プラグイン。** skill に加えるコマンドや hook はありません。10x マーケットプレイスからの更新が加わります。Claude のセッションの中ではなく、ターミナルで実行します:

```bash
claude plugin marketplace add Aboudjem/10x && claude plugin install loopify@10x
```

そのあと Claude Code で `/loopify` と入力し、何を繰り返すかを伝えます。

ビルドは不要です。skill は 1 つのフォルダで、標準ライブラリだけの Python スクリプトが 3 つ入っています。
`/loop` は Claude Code のコマンドです。ほかのエージェントでは、cron などの外部スケジューラーが各 tick を起動します。

## しくみ

Claude Code にはもともと `/loop` があります。セッションが開いている間、同じプロンプトを何度も実行します。
プロンプトは書いてくれません。loopify が 2 つのものを書きます:

- **brief（ファイル）。** 仕事の 1 回分: 何を読むか、何を変えてよいか、決してしないこと、いつ止まるか。
  ループは毎回これを開き直すので、動いている間も編集できます。
- **line（1 本の文字列）。** `/loop` に貼り付けます。brief のパスと停止ルールが入っています。

line は各 tick に、brief を読み、1 回分を実行し、起きたことを `TICKS.md` に記録するよう指示します。

### 1. 仕事を説明する

Claude Code で `/loopify` と入力し、何を繰り返すかを伝えます。loopify は README、最近のコミット、
開いている pull request を読みます。それから短い質問をまとめて 1 回だけします。

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file, re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string, you paste it below
```

`/Users/you/acme/` はあなたのプロジェクトの代わりです。loopify は実際のパスを出します。

### 2. line を貼り付ける

```text
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

Claude はすぐに 1 回実行し、そのセッションで 20 分ごとに続けます。PR がマージされるか 30 tick に
達した時点で、早いほうで止まります。よくある 2 つの間違い:

```text loop-antipattern
# not this: "every morning" can make /loop offer a cloud schedule instead, and nothing says when to stop
/loop every morning keep the release PR healthy

# and not the path alone: the tick gets a filename and no instruction
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

### 3. ログを読む、または状態を聞く

`TICKS.md` には、記録した tick ごとに 1 つのエントリがあり、先頭にカウンターがあります:

```text
tick: 7/30

## tick 7 · 2026-09-01T09:40 · changed
- CI: lint failed on src/api.ts → fixed the unused import, committed 4f2a1c9, npm test 12/12
- reviews: 1 new thread answered (rename), reply drafted in QUEUE.md
```

ループが安全にできなかったことは `QUEUE.md` であなたを待っています。状態コマンドが 3 つのファイルを読み、
次にやることを教えます。

## 得られるもの

状態レポートです。このリポジトリの例の状態フォルダで実行した、実際の出力です:

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

`--now` で時計を固定しているので、例はいつも同じに出ます。本物のループでは付けないでください。

1. 1 行目は判定です: `OK`、`NEEDS YOU`、`STALE`、`STOPPED`、`NOT STARTED`、`BROKEN LOG`。
2. 次に、やることが最大 3 つ。
3. 次に詳細。`lessons` は `LESSONS.md` のエントリ数です。

tick が記録しないと、2 間隔を超えたところで状態は `STALE` になります。tick の間隔は、保存した line か
`--interval` から読みます。

終了コードが判定を表すので、スクリプトや cron から使えます:

| 終了コード | 判定 | 意味 |
| ---------- | ---- | ---- |
| `0` | `OK`, `STOPPED`, `NOT STARTED` | 対応は不要 |
| `1` | `NEEDS YOU`, `STALE`, `BROKEN LOG` | ループを確認する |
| `2` | なし | 使い方の誤り、または状態フォルダがない |

`loop_status.py --help` も同じ表を出します。

loopify が書く brief には、ほかにも次のものが入ります:

- **line の中の停止ルールと tick 上限。** 仕事を終えたループは止まります。上限に達したループも
  止まります。loopify は先に 8 つのルールで line を確認します（`loop_line_lint.py`）。
- **始める前に許可するコマンド。** 最後のメッセージが、`gh pr view` など tick が実行するものを
  並べます。tick が許可の確認で待たされないようにするためです。
- **無人で動くための安全柵。** アカウント、支払い、push や投稿は、あなたが許可しない限りしません。
  PR のコメントなどループが読むものはデータであり、指示ではありません。
- **繰り返しに強い条項。** brief は、tick が動く前に探す目印を決めています。2 回動いた tick も、
  仕事が済んでいることがわかります。
- **形の決まったログ。** 各エントリは `## tick <n> · <ISO timestamp> · changed |
noop | stopped` で始まります。`ticks_lint.py` が確認します。
- **学ぶループ。** `LESSONS.md` は、うまくいったことと時間を無駄にしたことを残します。brief は各 tick に
  これを読むよう指示します。

## 対応エージェント

各行は、2026-11-17 に空のホームフォルダへ行ったグローバルインストール（`-g`）です。

| エージェント             | インストールコマンド                                      | 確認                                         |
| ------------------------ | --------------------------------------------------------- | -------------------------------------------- |
| Claude Code 2.1.326      | `claude plugin install loopify@10x`、まっさらな設定       | 2026-11-17、ユーザー範囲でプラグイン有効     |
| Claude Code（skills CLI）| `npx skills add Aboudjem/loopify -g -a claude-code`       | 2026-11-17、skill は `~/.claude/skills/`     |
| Codex                    | `npx skills add Aboudjem/loopify -g -a codex`             | 2026-11-17、skill は `~/.agents/skills/`     |
| Cursor                   | `npx skills add Aboudjem/loopify -g -a cursor`            | 2026-11-17、skill は `~/.agents/skills/`     |
| Gemini CLI               | `npx skills add Aboudjem/loopify -g -a gemini-cli`        | 2026-11-17、skill は `~/.agents/skills/`     |
| GitHub Copilot           | `npx skills add Aboudjem/loopify -g -a github-copilot`    | 2026-11-17、skill は `~/.agents/skills/`     |
| OpenCode                 | `npx skills add Aboudjem/loopify -g -a opencode`          | 2026-11-17、skill は `~/.agents/skills/`     |

「確認」とは、ファイルが入り、インストールしたコピーから 3 つのスクリプトが動いたという意味です。
そのエージェントの中でループを動かしたという意味ではありません。

文書のみで未確認: Windsurf、Zed、Kimi Code CLI、`skills/loopify/` の手動コピー。
[docs/editors.md](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md) を見てください。

brief はどこでも使えます。line は違います。Claude Code の `/loop` 用の line です。ほかの環境では、brief が
1 回分を実行して記録し、終了します。次の tick は外部のスケジューラーが起動します。
[docs/other-agents.md](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) に Kimi、Copilot CLI、Cursor、Goose、cron の説明があります。

## 検証

`make test` が、ここにあるすべての数字を出します。CI は push と pull request のたびに実行します。

```bash
make test
```

| スイート                    | 確認すること                                                               | 今日の結果 |
| --------------------------- | -------------------------------------------------------------------------- | ---------- |
| `evals/check_skill.py`      | skill の約束事を assertion で                                              | 161/161    |
| `tests/test_manifests.py`   | マニフェスト、バージョン、例の brief、翻訳、SVG、秘密情報、長いダッシュ    | 170/170    |
| `tests/test_ticks_lint.py`  | tick ログの形式                                                            | 13/13      |
| `tests/test_loop_status.py` | 各判定、終了コード、この README のサンプルのバイト一致                     | 62/62      |
| `tests/test_no_network.py`  | 同梱スクリプトがネットワークモジュールを読み込まず、curl も wget も呼ばない | 18/18      |
| `tests/test_dated_facts.py` | 古いバージョンで確認した `/loop` の事実は、どこでもそのバージョンを書く    | 5/5        |
| `evals/loop_line_lint.py`   | 正規の line が 8 つのルールを通る                                          | PASS       |

CI は固定した Claude Code で `claude plugin validate . --strict` も実行し、
`npx skills@1.9.0 add . --list` が skill を見つけることも確認します。

`/loop` の事実は 2026-11-17 に Claude Code 2.1.326 とそのドキュメントで確認しました。1 つだけ 2.1.326 で
確認し直せなかった事実があります: `/clear` が予定を消すことです。これは 2.1.252（2026-09-01）の日付のままです。
事実ごとの表は [docs/limits.md](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md#which-version-each-fact-was-checked-on) にあります。

## FAQ

**loopify はループを始めてくれますか?**
いいえ。brief を書き、line を出して止まります。始めたいときに、あなたが line を貼り付けます。

**なぜ 1 つのプロンプトではなく、ファイルと文字列なのですか?**
tick には詳細が必要です: パス、コマンド、行き詰まったときの対応。`/loop` には、tick ごとに送り直す短い
プロンプトが必要です。brief が詳細を持ち、line がそのパスを運びます。

**ループがまだ動いているかは、どうわかりますか?**
状態フォルダに対して `loop_status.py` を実行します。2 間隔を超えて tick の記録がないと `STALE` と出ます。
Claude に "what scheduled tasks do I have?" と聞くこともできます。

**ループを止めるものは何ですか?**
brief の停止ルール、tick の上限、7 日の上限、またはあなたです。全体の一覧は
[docs/faq.md](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) にあります。

**コードがどこかに送られますか?**
いいえ。loopify のスクリプトはネットワークを使いません。ネットワークモジュールを読み込むか curl や wget を
呼ぶと `tests/test_no_network.py` が失敗します。tick がすることは、brief が許すことだけです。

## 制限

> [!IMPORTANT]
> ループが動いていることは、正しいことをしている証拠ではありません。`/loop` を確認する評価役はいません。
> tick のログと状態レポートだけが証拠です。

- **ループは、貼り付けたセッションの中で動きます。** ターミナルを閉じると止まります。2.1.252 では
  `/clear` も予定を消しました。"what scheduled tasks do I have?" と聞いて確認してください。
- **どのループも 7 日で終わります。** 1 つのセッションで予定できるタスクは最大 50 個です。どちらも
  Claude Code の制限です。続けるには line をもう一度貼り付けます。
- **tick に記録を強制するものはありません。** line がそう指示するだけです。記録を飛ばした tick は、
  間隔がわかっていれば `STALE` として現れます。
- **tick が実行するものは、始める前に許可してください。** 許可の確認に当たった tick は、そこで答えを
  待ちます。loopify は `gh pr view` や `git commit` など、許可するコマンドを出します。
- **状態レポートには間隔が必要です。** 生きているループと止まったループを見分けるためです。保存した
  line か `--interval` から読みます。

出典つきの全一覧: [docs/limits.md](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md)。

## さらに詳しく

- [クイックスタート](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md): 最初のループを一歩ずつ
- [エディターへのインストール](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md): エージェントのコードと 2 つのインストール方法
- [完全な例](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md): 最後に line がある brief 全体
- [ほかのエージェント](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md): Kimi、Cursor、Goose、cron での同じ brief
- [FAQ](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) · [`loop.md` ポインター](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) · [Changelog](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) · [コントリビュート](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) · [skill 本体](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

[goalify](https://github.com/Aboudjem/goalify) を使ったことがあれば、なじみがあるはずです。goalify は
終わる仕事のため、loopify は繰り返す仕事のためのものです。

---

<sub>作者 <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT。`/loop` の挙動は 2026-11-17 に Claude Code 2.1.326 と
公式ドキュメントで確認しました（`/clear` だけは 2.1.252、2026-09-01 が最後の確認です。<a href="https://github.com/Aboudjem/loopify/blob/main/docs/limits.md#which-version-each-fact-was-checked-on">事実ごとの表</a>）。兄弟プロジェクトの
<a href="https://github.com/Aboudjem/goalify">goalify</a> は `/goal` に同じことをします。
<a href="https://github.com/Aboudjem/loopify/issues">足りないところを見つけたら</a></sub>

<sub>この翻訳は機械支援によるもので、レビュー済みです。正典は英語版の <a href="../README.md">README.md</a> です。</sub>
