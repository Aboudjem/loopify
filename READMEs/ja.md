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

loopify は、なかなか終わらない作業のための Claude Code スキルです――レビューが少しずつ入ってくる間もリリース PR
を健全に保つ、デプロイが安定するまで見守る、1時間ごとに新しいバグ報告を洗い出す、一晩中ブランチをグリーンに保
つ、といった作業です。作業内容は一度説明するだけで構いません。loopify があなたのプロジェクトを読み込み、本当
に必要な選択肢だけを尋ね、Claude がまだそのコンテキストを持っているうちに、その作業の1ラウンドがどういうもの
かを書き出します。そして最後に、貼り付けるだけの一行を渡してくれます。

loopify が書き出すものは2つです。**ブリーフ（ファイル）**は、1ラウンドで何をするか、絶対にしてはいけないこと、
いつ止めるか、メモをどこに書くかを記したファイルです。**一行**は、Claude Code に組み込まれた繰り返
しコマンドである `/loop` に貼り付ける短い文字列です。`/loop` は、あなたが選んだスケジュール、あるいは Claude
が選んだスケジュールでプロンプトを再実行します。1回の実行が**ティック**です。ティックのたびに、Claude はブリ
ーフ（ファイル）を読み直し、1ラウンドをこなし、何が起きたかをログに書き込みます。クリップボードを持った夜警
を思い浮かべてください。ブリーフ（ファイル）は壁に貼られた巡回表、一行はあなたが掲示するシフト表、
ログは朝に読むクリップボードです。

## 手に入るもの

- ⚡ **渡す一行はひとつだけ** — 一度貼り付ければ、ブリーフ（ファイル）のパスはその中に埋め込まれています。
- 📋 **ブリーフ（ファイル）は動かない** — 常設のファイルで、ティックのたびに読み直され、アーカイブされることはありません。
- 🧭 **本当に必要な選択肢を先に決める** — 頻度、止めどき、触ってよい範囲。
- 🛑 **停止ルールとティック上限は一行自体に含まれています** — ループはあなたが決めた条件で終わります。7日の期限に任せて偶然終わるのではありません。
- 🔒 **無人稼働のためのガードレール** — アカウント操作もお金の支払いも行わず、あなたが指示しない限り push も投稿もしません。読み込むものはすべてデータであり、命令ではありません。
- 🗒️ **読めるログ** — `TICKS.md` はすべてのティックを数え、その根拠を引用します。`QUEUE.md` にはあなたに残された作業が置かれます。
- 🧠 **学習するループ** — `LESSONS.md` にうまくいったことが蓄積され、ティックのたびに読み直されます。
- 🔁 **貼り付け一回で再開** — ブリーフ（ファイル）は形を保ったまま。一行をもう一度貼り付けるだけです。

## 3つのステップ

ターミナルで一度だけインストールします（Claude Code 2.1.252 で動作確認済み。詳しくは
[クイックスタート](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md)を参照）：

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

または [skills CLI](https://skills.sh) を使う場合：`npx skills add Aboudjem/loopify`

その後、Claude Code のチャットで：

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file — re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string — you paste it below

/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

1. **作業を説明する。** `/loopify` に続けて、繰り返してほしい内容を書きます。loopify があなたのプロジェクトを
   読み込み、本当に必要な質問だけをして、ブリーフ（ファイル）と一行を書き出します。
2. **一行を貼り付ける。** このセッションでも、そのプロジェクトを開いている別のセッションでも構いま
   せん。ブリーフ（ファイル）のパスは一行の中に含まれています。ティックのたびにファイルを新しく開
   き直すからです。`/Users/you/acme/` はあなたのプロジェクトを表す仮の表記で、loopify は実際のパスを表示しま
   す。
3. **ログを読む。** `TICKS.md` に戻ってきましょう――ティックごとに1エントリ、何が変わったか、その根拠が書か
   れています。安全にできなかったことは `QUEUE.md` であなたを待っています。

```text loop-antipattern
# 一行そのもの — loopify が出力した文字列そのまま（144文字）
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.

# これはダメ — 「毎朝」のような表現だと /loop がクラウドスケジュールを提案してしまうことがあり、停止ルールもありません
/loop every morning keep the release PR healthy

# パスだけを渡すのもダメ — ティックにファイル名だけが渡り、指示がありません
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

> [!IMPORTANT]
> ループが動いていること自体は、正しく機能している証拠にはなりません――ティックのログを読んでください。
> `/loop` を判定してくれるものは何もありません。ブリーフ（ファイル）のティックごとのチェックリストと
> `TICKS.md` だけが唯一の証拠です。ループは、それを貼り付けた Claude Code のセッションの中で動きます――
> そのセッションが開いている間だけ発火します。すべてのループは7日で止まります。一行をもう一度貼り
> 付けてください。

## もっと詳しく

- [クイックスタート](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md) — 最初のループ、他の
  インストール方法、ターミナルを開かずに実行する方法
- [実例](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md) — 実際のブリーフ（ファ
  イル）と、その末尾にある一行
- [正直な限界](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md) — loopify が約束していないこと全部
- [他のエージェント](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) — Kimi、Copilot CLI、
  Cursor、Qwen Code、Hermes、Goose、cron でも同じブリーフ（ファイル）を使う方法
- [FAQ](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) ·
  [`loop.md` ポインター](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) ·
  [変更履歴](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) ·
  [コントリビュート](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) ·
  [スキル本体](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

---

<sub>開発: <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT ライセンス。`/loop` の挙動は、配布さ
れている Claude Code 2.1.252 バイナリと公式ドキュメント（2026年）をもとに再調査したものです。`/goal` に対して
同じことをする姉妹プロジェクト <a href="https://github.com/Aboudjem/goalify">goalify</a> もあります。
<a href="https://github.com/Aboudjem/loopify/issues">不備に気づきましたか？</a></sub>
