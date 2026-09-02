<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-dark.svg">
    <img src="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-light.svg" alt="loopify：見張らなくていいループ。繰り返す作業を Claude に渡して、各ティックが何をしたかのログを見に戻る。" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="https://github.com/Aboudjem/loopify/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <a href="https://github.com/Aboudjem/loopify/stargazers"><img src="https://img.shields.io/github/stars/Aboudjem/loopify?color=2BE8C8&labelColor=0A0F1C" alt="stars"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <a href="zh-CN.md">简体中文</a> · <b>日本語</b> · <a href="es.md">Español</a> · <a href="fr.md">Français</a>
</p>

<p align="center">
  <strong>繰り返す作業を Claude に渡してください。戻ってきたら、見張らなければいけないループではなく、各ティックが何をしたかのログがあります。</strong>
</p>

<p align="center">
  <a href="#できること">できること</a> · <a href="#インストール">インストール</a> · <a href="#使い方">使い方</a> · <a href="#各エディタで使う">各エディタで使う</a> · <a href="#知っておくこと">知っておくこと</a> · <a href="#もっと詳しく">もっと詳しく</a>
</p>

<p align="center"><sub>この翻訳は英語の原文より古い場合があります。<!-- may-lag --></sub></p>

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

## できること

本当の意味で終わらない作業があります。リリース用のプルリクエストは午後じゅう見ていないといけませんし、
新しいバグ報告は夜のあいだにたまり、誰かが読む前にひととおり目を通しておきたくなります。Claude Code
には、作業を繰り返すためのコマンド `/loop` がすでにあります。プロンプトと間隔を渡せば、セッションが
開いているあいだ、そのプロンプトを何度も実行してくれます。ただし、そのプロンプト自体は用意してくれません。

loopify がそのプロンプトを書きます。あなたは作業を一度だけ、普通の言葉で説明します。loopify は Claude
があなたの意図をまだ把握しているうちにプロジェクトを読み、本当に決めるべき数点（どのくらいの頻度で、
いつ止めるか、何に触ってよいか）を尋ね、2 つのものを書きます。

- **ブリーフ、ファイル。** 作業の 1 巡分です。何を読むか、何を変更してよいか、絶対にしてはいけないこと、
  いつ止めるか、起きたことをどこに書くか。ループは毎回の実行の最初にこのファイルを新しく開くので、
  実行と実行のあいだで失われるものはなく、ループが動いている最中でも編集できます。
- **ライン、1 つの文字列。** これを `/loop` に貼り付けます。ブリーフのパスが中に入っているので、
  どの実行もどこを見ればよいか分かります。停止ルールも入っているので、ループはあなたの条件で終わります。

1 回の実行が 1 **ティック**です。ティックごとに Claude はブリーフを読み直し、作業を 1 巡し、起きたことを
`TICKS.md` というログに書きます。あなたが起きている必要はありません。ログを読む必要はあります。

[goalify](https://github.com/Aboudjem/goalify) を使ったことがあれば、感覚は同じです。goalify は終わる
作業のためのもので、1 つの大きなタスク、1 つの完了の定義、そして `/goal` です。loopify は繰り返す作業の
ためのものです。

## インストール

上の 2 つのコマンドは 10x マーケットプレイスを追加し、Claude Code にプラグインを入れます。loopify は
Claude Code 2.1.252 で動作を確認しています。ほかのエージェントでも、
[skills CLI](https://github.com/vercel-labs/skills) で同じスキルディレクトリを 1 行で入れられます。

```bash
npx skills add Aboudjem/loopify
```

## 使い方

### 1. 作業を説明する

Claude Code のチャットで `/loopify` と入力し、何を繰り返すか伝えます。loopify は README、最近のコミット、
開いているプルリクエストを読んでから、短い質問をまとめて 1 度だけ尋ねます。

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file, re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string, you paste it below
```

`/Users/you/acme/` はあなたのプロジェクトの代わりです。loopify は実際のパスを表示します。

### 2. ラインを貼り付ける

```text
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

Claude はすぐに 1 巡を実行し、そのあとはそのセッションの中で 20 分ごとに、プルリクエストがマージされるか
30 ティックが過ぎるか、早いほうまで続けます。間隔を書かなければ、Claude が自分でペースを決めます。
よくある間違いは 2 つです。

```text loop-antipattern
# これはダメ："every morning" のような書き方だと /loop がクラウドスケジュールを提案することがあり、停止ルールもありません
/loop every morning keep the release PR healthy

# パスだけもダメ：ティックはファイル名だけを受け取り、指示を受け取りません
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

### 3. ログを読む

`TICKS.md` にはティックごとに 1 件、何が変わったかとその証拠が入り、先頭にカウンターがあります。

```text
tick: 7/30

## tick 7 · 2026-09-01T09:40 · changed
- CI: lint failed on src/api.ts → fixed the unused import, committed 4f2a1c9, npm test 12/12
- reviews: 1 new thread answered (rename), reply drafted in QUEUE.md
```

ループが安全に実行できなかったことは、`QUEUE.md` であなたを待っています。

## 手に入るもの

- **動かないブリーフ。** 毎ティック読み直され、アーカイブされず、ループに書き換えられません。どのくらいの
  頻度で動くか、いつ止まるか、何に触ってよいかは、最初のティックより前に決まります。
- **ライン自体に入った停止ルールとティック上限。** 作業を終えたループは止まり、上限に達したループも止まります。
- **無人実行のためのガードレール。** アカウントなし、支払いなし、あなたが言わないかぎり push も投稿も
  しません。ループが読むもの、たとえばプルリクエストのコメントは、データであって指示ではありません。
- **すべてのブリーフに入る「繰り返しても安全」の条項。** ブリーフには、ティックが動く前に探す目印が書かれて
  いるので、もう一度走ったティックは作業がすでに済んでいることを判断できます。
- **形の決まったログ。** `TICKS.md` の各エントリは同じヘッダー
  `## tick <n> · <ISO timestamp> · changed | noop | stopped` で始まり、
  `skills/loopify/scripts/ticks_lint.py` で検査できます。`QUEUE.md` のブロックされた項目には `reason:` 行と
  `unblock:` 行が付きます。
- **学ぶループ。** `LESSONS.md` はうまくいったことと時間を無駄にしたことを残し、ループは毎ティックそれを
  読み直します。

## 各エディタで使う

Claude Code、Cursor、Codex、Copilot、Gemini CLI、そして `npx skills add` 経由で 70 以上のほかの
エージェントで動きます。

| どこで | どうやって |
| --- | --- |
| Claude Code | `claude plugin install loopify@10x` |
| Cursor、Codex、Gemini CLI、OpenCode、Windsurf、Zed、Kimi Code CLI | `npx skills add Aboudjem/loopify -a <agent>` |
| VS Code と GitHub Copilot | `npx skills add Aboudjem/loopify -a github-copilot` |
| そのほか全部 | `skills/loopify/` をエージェントのスキルディレクトリにコピー |

loopify は標準ライブラリだけの Python スクリプト 2 本が隣にある 1 つのスキルディレクトリなので、動かす
サーバーもコンパイルするものもありません。`-a` のコード、エージェントごとの 2 つのインストール先、手動
コピーの手順は [docs/editors.md](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md) にあります。

ブリーフは持ち運べますが、ラインは持ち運べません。ラインは Claude Code の `/loop` 行であり、ブリーフの
スケジュール手順は Claude Code のツールを指します。ブリーフにはその場合の分岐があります。1 巡だけ実行し、
記録し、終了して、次のティックは外部のスケジューラに任せます。
[docs/other-agents.md](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) が Kimi、
Copilot CLI、Cursor、Qwen Code、Hermes、Goose、素の cron を扱っています。

## 知っておくこと

> [!IMPORTANT]
> ループが動いていることは、正しいことをしている証拠にはなりません。ティックログを読んでください。
> `/loop` の裏に評価器はいないので、ブリーフのティックごとのチェックリストと `TICKS.md` が唯一の証拠です。

- **ループは貼り付けたセッションの中で生きています。** そのセッションが開いているあいだだけ動きます。
  ターミナルを閉じれば止まりますし、`/clear` でもスケジュールは消えます。Claude Code をバックグラウンドで
  動かせば、ウィンドウなしで生かしておけます。
- **どのループも 7 日で終わり**、1 セッションが持てるスケジュール済みタスクは最大 50 件です。どちらも
  スケジュール実行に関する Claude Code 側の制限で、loopify の制限ではありません。続けるにはラインをもう
  一度貼り付けてください。
- **ティックが実行するものを事前に許可しておく。** loopify は `gh pr view` や `git commit` など、ループに
  必要なコマンドを表示します。許可のプロンプトに当たったティックは、誰かが答えるまでそこで待ちます。

## もっと詳しく

- [クイックスタート](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md)、最初のループを
  順番に、ターミナルを開かない場合も
- [エディタへのインストール](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md)、
  エージェントコードと skills CLI の 2 つのパス
- [完全な実例](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md)、末尾に
  ラインが付いたブリーフ 1 本まるごと
- [正直な限界](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md)、loopify が約束しないことと、
  その根拠となるバイナリまたは公式ドキュメント
- [ほかのエージェント](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md)、同じブリーフを
  Kimi、Cursor、Goose、素の cron で
- [FAQ](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) · [`loop.md` ポインタ](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) · [変更履歴](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) · [コントリビュート](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) · [スキル本体](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

---

<sub>作者 <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT。`/loop` の挙動は、配布されている
Claude Code 2.1.252 のバイナリと公式ドキュメントから 2026 年に導き出したものです。`/goal` に対して同じことを
する <a href="https://github.com/Aboudjem/goalify">goalify</a> の姉妹プロジェクトです。
<a href="https://github.com/Aboudjem/loopify/issues">足りないところを見つけたら</a></sub>

<sub>この翻訳は機械支援によるもので、レビュー済みです。正典は英語版の <a href="../README.md">README.md</a> です。</sub>
