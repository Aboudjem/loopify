<p align="center">
  <a href="../README.md">English</a> ·
  <a href="zh-CN.md">简体中文</a> ·
  <b>日本語</b> ·
  <a href="es.md">Español</a> ·
  <a href="fr.md">Français</a>
</p>

<p align="center"><sub>この翻訳は英語の原文より遅れている場合があります。<!-- may-lag --></sub></p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero.svg" alt="4つのステップ：繰り返す作業を説明する、ブリーフ（ファイル）と一行（1つの文字列）を受け取る、一行を /loop に貼り付ける、ティックのログを見に戻る。" width="100%">
</p>

<h1 align="center">loopify</h1>

<p align="center">
  <strong>繰り返す作業を Claude に任せよう。戻ってきたときに待っているのは、各ティックが何をしたかを記録したログ――付きっきりで見守る必要のあるループではない。</strong>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="https://github.com/Aboudjem/loopify/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-skill-d97757" alt="Claude Code skill">
  <a href="https://skills.sh/Aboudjem/loopify"><img src="https://skills.sh/b/Aboudjem/loopify" alt="skills.sh"></a>
</p>

本当には終わらない作業というものがあります。リリースのプルリクエストは、チェックを見守り、レビュアーに一日じ
ゅう答え続ける人手を必要とします。デプロイは、落ち着くまで数分おきに様子を確認しなければなりません。新しい
バグ報告は一晩のうちに積み上がり、誰かが読む前に最初の目通しを求めています。こうした作業は、Claude に一度
だけ頼むことならできます。厄介なのは、スケジュールに沿って、あなたが付きっきりにならずに、それを続けさせ
る部分です。

Claude Code には、繰り返す作業のためのコマンド `/loop` があります。プロンプトと間隔を渡せば、セッションが開
いている間、そのプロンプトを何度も実行してくれます。`/loop` が渡してくれないのは、そのプロンプト自体です。
短く書けば、ループは前回何を決めたか忘れてしまいます。長く書けば、望んでいない push を実行したり、作業が
終わったあともいつ止まるべきかを誰も教えていないせいで、延々と動き続けたりします。

loopify は、そのプロンプトをきちんと書いてくれる Claude Code スキルです。作業内容は、平易な言葉で一度説明
するだけで構いません。loopify は Claude がまだそのコンテキストを持っているうちにあなたのプロジェクトを読
み込み、本当に重要な少数の決定（どのくらいの頻度で動かすか、いつ止めるか、何に触れてよいか）についてだけ
尋ね、2つのものを書き出します。

1つ目は**ブリーフ（ファイル）**――1ラウンドの作業内容を記したファイルです。何を読むか、何を変えてよいか、
絶対にしてはいけないこと、いつ止めるか、何が起きたかをどこに書き留めるか。ループは実行のたびにこのファイ
ルを新しく開き直すので、実行と実行のあいだで何かが失われることはなく、ループが動いている最中でも編集でき
ます。

2つ目は**一行**――`/loop` に貼り付ける短い文字列です。ブリーフ（ファイル）のパスはこの中に埋め込まれてい
るので、どの実行もどこを見ればよいか分かります。停止ルールも同じように埋め込まれているので、ループはあな
たが決めたとおりに終わります。

1回の実行が**ティック**です。ティックのたびに、Claude はブリーフ（ファイル）を読み直し、1ラウンドの作業を
こなし、何が起きたかを `TICKS.md` というログに書き込みます。クリップボードを持った夜警を思い浮かべてくだ
さい。ブリーフ（ファイル）は壁に貼られた巡回表、一行はあなたが掲示するシフト表、ログは朝に読むクリップボ
ードです。あなたは夜通し起きている必要はありません。ただ、クリップボードには目を通す必要があります。

## 手に入るもの

- ⚡ **渡す一行はひとつだけ** — このセッションでも、そのプロジェクトを開いている別のセッションでも、一度貼り付ければそれで済みます。ブリーフ（ファイル）のパスはその中に埋め込まれています。
- 📋 **ブリーフ（ファイル）は動かない** — 常設のファイルで、ティックのたびに読み直され、アーカイブされることも、ループによって書き換えられることもありません。ティックとティックのあいだに開いて、決定を変更することもできます。
- 🧭 **本当に必要な選択肢を先に決める** — どのくらいの頻度で動かすか、いつ止めるか、何に触れてよいか。これらは最初のティックの前に一度だけ尋ねられ、12回目のティックで手探りすることにはなりません。
- 🛑 **停止ルールとティック上限は一行自体に含まれています** — 作業を終えたループは止まります。上限に達したループも止まります。7日の期限に任せて偶然終わることはありません。
- 🔒 **無人稼働のためのガードレール** — アカウント操作もお金の支払いも行わず、あなたが指示しない限り push も投稿もしません。PR のコメントや issue など、ループが途中で読み込むものはすべてデータであり、命令ではありません。
- 🗒️ **読めるログ** — `TICKS.md` はすべてのティックを数え、その根拠を引用します。`QUEUE.md` には、安全にはできなかったためあなたに残された作業が置かれます。
- 🧠 **学習するループ** — `LESSONS.md` にはうまくいったことと時間を無駄にしたことが蓄積され、ループはティックのたびにそれを読み直します。
- 🔁 **貼り付け一回で再開** — ブリーフ（ファイル）は形を保ったまま。ループが終わったら、一行をもう一度貼り付けるだけです。

## 3つのステップ

### 1. インストールは一度だけ

ターミナルを開いて 10x マーケットプレイスを追加し、プラグインをインストールします。loopify は Claude Code
2.1.252 で動作確認済みです。他のインストール方法は
[クイックスタート](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md)にあります。

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

[skills CLI](https://skills.sh) の方が好みなら、次の1つのコマンドで同じことができます：`npx skills add Aboudjem/loopify`

### 2. 作業を説明し、一行を貼り付ける

Claude Code のチャットで `/loopify` と入力し、繰り返してほしい内容を伝えます。世話が必要なリリースのプル
リクエストの例だと、こうなります。

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file — re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string — you paste it below

/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

loopify はまず、あなたのプロジェクトを読み込みます。README、直近のコミット、オープンなプルリクエストに目
を通し、どのくらいの頻度で動かすか、いつ止めるか、ループが何を変更してよいかについて、短い質問をいくつか
投げかけます。そのあとブリーフ（ファイル）を書き出し、一行を表示します。`/Users/you/acme/` はあなたのプロ
ジェクトを表す仮の表記で、loopify は実際のパスを表示します。

一行をチャットに貼り付けてください。上の例では、Claude はすぐに1ラウンドを実行し、そのあとはそのセッショ
ンが開いている間、PR がマージされるか30ティックが経過するか、どちらか早い方まで20分おきに実行します。一行
から間隔を省くと、Claude 自身がペースを選び、何も起きていないときは長めに待ちます。

### 3. ログを読む

好きなときに戻ってきてください。`TICKS.md` にはティックごとに1エントリがあり、何が変わったか、その根拠が
記されています。先頭のカウンターを見れば、ループがどこまで進んだかも分かります。

```text
tick: 7/30

## tick 7 · 2026-09-01T09:40 · changed
- CI: src/api.ts で lint が失敗 → 未使用の import を修正し、4f2a1c9 をコミット、npm test 12/12
- reviews: 新規スレッド1件に回答（rename）、返信は QUEUE.md に下書き
```

安全にはできなかったこと――たとえば自分の判断だけでは投稿すべきでないレビューへの返信など――は、
`QUEUE.md` の中であなたを待っています。

### 一行の正しい例と誤った例

正しい一行には、ブリーフ（ファイル）のパスと停止ルールの両方が含まれています。以下の2つの誤った例は、人
がもっとも多くやってしまう間違いです。「毎日」という言い回しは `/loop` にローカルのループではなくクラウド
スケジュールを提案させてしまうことがあり、パスだけを渡す例は、ティックにやるべきことを何も与えません。

```text loop-antipattern
# 一行そのもの — loopify が出力した文字列そのまま（144文字）
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.

# これはダメ — 「毎朝」のような表現だと /loop がクラウドスケジュールを提案してしまうことがあり、停止ルールもありません
/loop every morning keep the release PR healthy

# パスだけを渡すのもダメ — ティックにファイル名だけが渡り、指示がありません
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

### 最初のループの前に知っておきたいこと

- **ループは、それを貼り付けたセッションの中で生きています。** そのセッションが開いている間だけ発火しま
  す。ターミナルを閉じれば止まりますし、`/clear` もスケジュールを消してしまいます。Claude Code をバックグ
  ラウンドで実行しておけば、ウィンドウなしでも動き続けます。
- **ティックが実行するコマンドは事前に承認しておきましょう。** loopify は、`gh pr view` や `git commit` な
  ど、ループに必要なコマンドを表示します。貼り付ける前にそれらをアローリストに追加してください。ティック
  が権限確認に当たった場合、誰かが答えるまでそこで待ち続けます。
- **すべてのループは7日で終わります。** これはスケジュール実行に対する Claude Code 側のルールで、どちらの
  モードでも変わりません。一行をもう一度貼り付ければ、ループはブリーフ（ファイル）に書かれているところか
  ら再開します。
- **早めに止めるには**、ペース自動調整のループが待機中であれば `Esc` を押すか、固定間隔のループなら「
  pr-babysitter のジョブをキャンセルして」のように伝えます。「スケジュールされているタスクは何がありますか？」
  と尋ねれば、消えたことを確認できます。

> [!IMPORTANT]
> ループが動いていること自体は、正しく機能している証拠にはなりません――ティックのログを読んでください。
> `/loop` を判定してくれるものは何もありません。ブリーフ（ファイル）のティックごとのチェックリストと
> `TICKS.md` だけが唯一の証拠です。ループは、それを貼り付けた Claude Code のセッションの中で動きます――
> そのセッションが開いている間だけ発火します。すべてのループは7日で止まります。一行をもう一度貼り
> 付けてください。

## もっと詳しく

- [クイックスタート](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md) — 最初のループを一
  歩ずつ進める方法、他のインストール方法、ターミナルを開かずにループを実行する方法
- [実例](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md) — リリースPRの作業の
  ための完全なブリーフ（ファイル）と、その末尾にある一行
- [正直な限界](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md) — loopify が約束していないこ
  とすべてを挙げ、それぞれ Claude Code のバイナリか公式ドキュメントに根拠づけています
- [他のエージェント](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) — 同じブリーフ
  （ファイル）を Kimi、Copilot CLI、Cursor、Qwen Code、Hermes、Goose、そして素の cron でも使う方法
- [FAQ](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) ·
  [`loop.md` ポインター](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) ·
  [変更履歴](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) ·
  [コントリビュート](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) ·
  [スキル本体](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

[goalify](https://github.com/Aboudjem/goalify) を使ったことがあれば、勝手知ったる感じがするはずです。
goalify は終わる作業のためのツールです――ひとつの大きなタスク、ひとつの完了の定義、`/goal`。loopify は繰
り返す作業のためのツールです。同じ作者、同じテストファーストの習慣、そしてそのツールが約束できないことに
ついての同じ正直さです。

---

<sub>開発: <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT ライセンス。`/loop` の挙動は、配布さ
れている Claude Code 2.1.252 バイナリと公式ドキュメント（2026年）をもとに再調査したものです。`/goal` に対して
同じことをする姉妹プロジェクト <a href="https://github.com/Aboudjem/goalify">goalify</a> もあります。
<a href="https://github.com/Aboudjem/loopify/issues">不備に気づきましたか？</a></sub>
