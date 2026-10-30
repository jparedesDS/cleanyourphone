<p align="center">
  <a href="https://jparedesds.github.io/cleanyourphone-web/">
    <img src="assets/banner.png" alt="CleanYourPhone" width="100%">
  </a>
</p>

<p align="center">
  <b>English</b> ·
  <a href="README.es.md">Español</a> ·
  <a href="README.pt-BR.md">Português (BR)</a> ·
  <a href="README.fr.md">Français</a> ·
  <a href="README.de.md">Deutsch</a> ·
  <a href="README.it.md">Italiano</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ko.md">한국어</a>
</p>

# CleanYourPhone

**あなたのスマホを、余計なものなしで。** コーディングエージェント向けの、オープンソースで元に戻せる Android デブロート Skill です。ADB でプリインストールアプリとサービスを無効化します。root もカスタム ROM も不要、アンインストールはせず、1 コマンドで元に戻せます。

[Website](https://jparedesds.github.io/cleanyourphone-web/) · [SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [Safety](docs/SAFETY.md) · [157 profiles](profiles/README.md)

## クイックスタート

1. Android SDK Platform-Tools を入れ、<code>adb</code> を PATH に追加します。
2. 開発者向けオプションと USB デバッグを有効にし、USB で接続して許可します。
3. リポジトリを clone してエージェントで開くか、<code>SKILL.md</code> を skills フォルダにコピーします。

```bash
git clone https://github.com/jparedesDS/clean-your-phone
cd clean-your-phone
python tools/phone.py doctor
```

## 安全性

- 無効化のみ。アンインストールはしません。変更は <code>pm disable-user</code> だけです。
- 最初の変更前にパッケージ、設定、ロール、キーボードをバックアップします。
- 保護リストと、ダイヤラー、SMS、Home、キーボードのロール確認。
- 5 個ずつのバッチ、再起動、確認。
- root、ROM、アカウント、テレメトリー、外部 API はありません。

## ドキュメント

- [SKILL.md](SKILL.md) — the full procedure and safety rules.
- [PROMPT.md](PROMPT.md) — paste this if your agent does not load skills.
- [docs/SAFETY.md](docs/SAFETY.md) — protected packages, roles and restore.
- [profiles/README.md](profiles/README.md) — 157 model/firmware profiles.
- [README.md](README.md) / [README.es.md](README.es.md) — 完全なドキュメントは英語とスペイン語です。

MIT. No account. No telemetry.
