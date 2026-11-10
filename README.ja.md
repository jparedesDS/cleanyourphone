<p align="center">
  <a href="https://jparedesds.github.io/cleanyourphone-web/">
    <img src="assets/banner.png" alt="CleanYourPhone — あなたのスマホを、余計なものなしで" width="100%">
  </a>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.es.md">Español</a> ·
  <a href="README.pt-BR.md">Português (BR)</a> ·
  <a href="README.fr.md">Français</a> ·
  <a href="README.de.md">Deutsch</a> ·
  <a href="README.it.md">Italiano</a> ·
  <b>日本語</b> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml"><img src="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/license-MIT-a78bfa?labelColor=121316" alt="MIT">
  <img src="https://img.shields.io/badge/python-3.10%2B-a78bfa?labelColor=121316" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/telemetry-none-a78bfa?labelColor=121316" alt="テレメトリーなし">
  <img src="https://img.shields.io/badge/profiles-156-a78bfa?labelColor=121316" alt="156 プロファイル">
  <a href="https://github.com/jparedesDS/cleanyourphone/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone?color=a78bfa&labelColor=121316" alt="release"></a>
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone-app?color=a78bfa&label=app&labelColor=121316" alt="app release"></a>
</p>

# CleanYourPhone

**あなたのスマホを、余計なものなしで。** コーディングエージェントのために作られた、オープンソースで元に戻せる Android 向けデブロート skill です。ADB 経由でプリインストールアプリとサービスを無効化します。root もカスタム ROM も不要、アンインストールも一切なく、CLI が記録した変更は 1 コマンドで復元できます。

ストーリーと安全モデルは **[jparedesds.github.io/cleanyourphone-web](https://jparedesds.github.io/cleanyourphone-web/)** で読めます。

ボタン操作を好む人向けに、**オプションの Windows アプリ**も用意しています: **[Early MVP をダウンロード](https://github.com/jparedesDS/cleanyourphone-app/releases/latest)**。同じ CLI の GUI です。skill が主力プロダクトであり、プロファイルのないスマホのための道でもあります。

[cleanyour.tv](https://cleanyour.tv) のスマホ版で、作りも同じです。プロンプト 1 つ、コマンド 1 つ、元に戻せて、オープンソース。そして、常に本人が主導権を握ります。

[SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [アプリ](https://github.com/jparedesDS/cleanyourphone-app) · [安全性](docs/SAFETY.md) · [156 プロファイル](docs/PROFILES.md) · [フィードバック](docs/FEEDBACK.md) · [変更履歴](CHANGELOG.md)

## ここから始める

| あなたの状況 | ここから始める |
|---|---|
| スマホとコーディングエージェントがある | 下のクイックスタート。 |
| プロンプトよりボタンがいい | [Windows アプリをダウンロード](https://github.com/jparedesDS/cleanyourphone-app/releases/latest)（Early MVP）。 |
| まず動きを見たい | [ウェブサイト](https://jparedesds.github.io/cleanyourphone-web/)。 |
| 安全ルールが必要 | [docs/SAFETY.md](docs/SAFETY.md)。 |
| モデル用のプロファイルが必要 | [156 個のプロファイルを見る](profiles/README.md)。 |
| 自分のスマホが一覧にない | skill を手動で使うか、[プロファイルのリクエスト](docs/FEEDBACK.md)を送ってください。 |
| ターミナルがいい | [CLI をインストール](docs/CLI.md)。 |

| 部分 | 状態 |
|---|---|
| **Skill** | 主力プロダクト。このリポジトリにあります。 |
| **CLI** | `0.3.2`、PyPI で `cleanyourphone` / `cyp` として公開。 |
| **Windows アプリ** | `0.2.0` Early MVP、オプション、未署名。 |
| **ウェブサイト** | 10言語対応: [jparedesds.github.io/cleanyourphone-web](https://jparedesds.github.io/cleanyourphone-web/)。 |
| **フィードバック** | オプションの web/アプリ/skill フォームから Discord へ。自動テレメトリーはありません。 |

---

## なぜ skill が先なのか

他のアプリを無効化するアプリには、root、Shizuku、device-owner の権限が必要です。シェルコマンド 1 つで済むことにしては、権限もリスクも大きすぎます。skill はただのテキストです。本人のエージェントがそれを読み、`adb` を実行し、計画を示し、何かに触る前に確認します。スマホにインストールするものも、バックグラウンドで動くものも、外部へ通信するものもありません。

今はオプションの Windows アプリもありますが、skill の代わりではありません。同じ CLI の GUI で、テスト済みビルドを持つ完全一致の `device` プロファイルか、明示的な確認と 1 バッチ 1 パッケージを条件に `documented` プロファイルに一致したときだけ先へ進みます。一致しなければ停止し、本人をここへ案内します。skill ならパッケージ一覧を調べ、各アプリについて質問し、手動で続けられます。

スマホは毎日使うものなので、skill は意図的に保守的に作られています:

- **無効化のみ、アンインストールはしない。** `pm disable-user --user 0` だけ。`pm enable` が元に戻す操作です。
- **まずバックアップ。** 最初の変更前に、パッケージ一覧、設定、ロール、IME、`getprop` を保存します。
- **保護リスト。** Android のコア機能、電話、Play Services、WebView、permission controller、緊急アラート、IME/telecom、NFC/SE、メーカーのセキュリティパッケージは CLI が拒否します。
- **ロールの確認。** ダイヤラー、SMS アプリ、Home アプリ、キーボードを失うことはありません。
- **小さなバッチ。** 5 パッケージずつ、確認してから次へ。
- **まず本人に確認。** 銀行、決済、WhatsApp、カメラ、目覚まし、VPN、認証アプリ、スマートウォッチ、eSIM、VoLTE/Wi-Fi 通話、仕事用アプリはデフォルトではなくチェックリストです。

## 仕組み

1. **スマホ側:** 開発者向けオプションと USB デバッグを有効にします。USB で接続します。
2. **パソコン側:** エージェントに `SKILL.md` を渡します（または `PROMPT.md` を貼り付けます）。
3. **流れに沿って:** エージェントがスマホを識別し、バックアップし、パッケージの表を示し、何を使っているか尋ね、バッチで無効化し、再起動して確認します。`python tools/phone.py restore` で元に戻せます。

```text
$ python tools/phone.py doctor
ADB ......... C:\platform-tools\adb.exe
ADB version . Android Debug Bridge version 1.0.41
Devices ..... <serial> (device)

Device ...... Google Pixel 8 (shiba)
Android ..... 16 (SDK 36)
Managed ..... no
Users ....... 1
Battery ..... 82%
Backup ...... none (run: python tools/phone.py backup)
Profiles .... google-pixel-8
Auto-apply .. google-pixel-8

$ python tools/phone.py plan --profile google-pixel-8
Profile: google-pixel-8 (Google Pixel 8)
Phone:   Google Pixel 8 (shiba), Android 16
Match:   yes
Auto-apply: yes

DISABLE  com.google.android.apps.wellbeing
         why: Digital Wellbeing: screen-time tracking and telemetry
         breaks: Screen-time dashboard and app timers
ASK      com.google.android.apps.turbo
         why: Adaptive Battery and Device Health
         breaks: Adaptive Battery, battery diagnostics
```

## オプションの Windows アプリ

ボタン操作を好む人向けに、アプリは同じ CLI をガイド付きの Windows フローで包みます。接続、確認、バックアップ、レビュー、適用、検証、元に戻す、まで。

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases/latest">
    <img src="assets/app-review.png" alt="CleanYourPhone アプリのレビュー画面。documented プロファイルの警告と、選択されたアプリ 1 つを表示" width="760">
  </a>
</p>

- **Wi-Fi でも USB でも接続。** アプリがスマホを見つけ、ビルドを確認し、正確なプロファイルを表示します。
- **完全一致の `device` プロファイル**はテスト済みの経路を通ります。**`documented` プロファイル**は手動です。警告を表示し、明示的な確認を取り、1 バッチ 1 アプリにします。プロファイルがなければ停止し、skill を使うよう案内します。
- **バックアップは必須。** すべてのパッケージをレビューし、バッチで適用し、検証し、ジャーナル全体を元に戻します。
- **オプションの追加機能:** プライベート DNS による広告ブロック（YouTube を除く）と、ローカルの前後ベンチマーク。
- **オプションのフィードバック:** 編集可能なチェックリストを、同意後にメンテナーへ送れます。自動テレメトリーはありません。
- **root なし、アンインストールなし、スマホにアプリを入れない。** インストーラーは未署名なので、実行前に SHA-256 を確認してください。

[`v0.2.0` をダウンロード](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) · [ソース](https://github.com/jparedesDS/cleanyourphone-app) · [接続ガイド](docs/CONNECT.md).

## クイックスタート

### 1. ADB をインストール

Windows、macOS、Linux 向けの [Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools) をダウンロードして解凍し、`PATH` に追加します。確認:

```bash
adb version
```

### 2. スマホを準備

設定 → スマホについて → **ビルド番号**を 7 回タップ → 戻る → **開発者向けオプション** → **USB デバッグ**をオン。USB で接続し、**USB デバッグを許可しますか？** のプロンプトを承認します。スマホのロックを解除したまま、バッテリー残量 30% 以上で行ってください。

Android 11 以降では **ワイヤレスデバッグ**も使えます。オンにして、スイッチだけでなく文字の部分をタップし、**ペア設定コードによるデバイスのペア設定**を選んで、そのダイアログを開いたままにします。ペア設定ダイアログには専用のポートがあり、メイン画面の接続ポートとは異なります。初回の手順とよくある対処は [docs/CONNECT.md](docs/CONNECT.md) にあります。

### 3. クローンして確認

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

CLI は任意です。`SKILL.md` には生の `adb` コマンドも載っているので、Python なしでもエージェントは作業できます。CLI があるのは、エージェントがガードレールを自己流にしないためです。

ターミナルのほうがよければ、[pipx](https://pipx.pypa.io/) でコマンドをインストールします:

```bash
pipx install cleanyourphone
cleanyourphone doctor
```

`cleanyourphone` と短い別名 `cyp` が使えるようになります。[docs/CLI.md](docs/CLI.md) ではウィザード、インストール先、安全ルールを説明しています。`python tools/phone.py` も引き続き動作します。

### 4. skill をエージェントに渡す

| エージェント | 置き場所 |
|---|---|
| **Claude Code** | `~/.claude/skills/cleanyourphone/SKILL.md`（個人）または `.claude/skills/cleanyourphone/SKILL.md`（プロジェクト） |
| **OpenCode** | `~/.config/opencode/skills/cleanyourphone/SKILL.md`（グローバル）または `.opencode/skills/cleanyourphone/SKILL.md`（プロジェクト） |
| **Codex** | プロジェクトの `AGENTS.md`、または `~/.codex/AGENTS.md`。skill を読み込まないビルドなら `PROMPT.md` を貼り付け |
| **Cursor** | `SKILL.md` の内容を `.cursor/rules/cleanyourphone.mdc` に |
| **Gemini CLI** | プロジェクトの `GEMINI.md` |
| **任意のチャットエージェント** | `PROMPT.md` を貼り、要求されたら `SKILL.md` を貼る |

スペイン語のプロンプト: [PROMPT.es.md](PROMPT.es.md)。skill は本人が書いた言語で答えます。

いちばん簡単なのは、リポジトリをクローンしてそのフォルダでエージェントを開くことです。`SKILL.md` はすでにルートにあるので、`python tools/phone.py` がそのまま動きます。エージェントがグローバルフォルダから skill を読み込む場合は、`SKILL.md` をそこへコピーします。CLI を pipx でインストールすれば（上記）、リポジトリをクローンしたままにする必要はありません:

```bash
mkdir -p ~/.claude/skills/cleanyourphone
cp SKILL.md ~/.claude/skills/cleanyourphone/SKILL.md
```

リポジトリがなくても skill は動きます。生の `adb` コマンドを含み、エージェントにそれを使うよう指示します。

あとは **「スマホをきれいにして」** または **「Pixel で cleanyourphone を使って」** と頼むだけです。

## できること

- メーカーのテレメトリー、広告の表示面、おすすめアプリの行、重複したブラウザ/ストア、使っていないプリロードを無効化します。
- 任意で、プリセット（`adguard`、`adguard-family`、`controld`、`mullvad`）または独自リゾルバーを使ってプライベート DNS を設定し、広告が実際にブロックされているか確認します。YouTube の広告ブロッカーではありません。[docs/ADS.md](docs/ADS.md) を参照。
- レポートを生成します。何が変わったか、なぜか、何を残したか、バックアップの場所、元に戻すコマンド。
- `documented` プロファイルは手動で作成した証拠として扱います。`disable` リストなし、自動適用なし、レビュー後に 1 パッケージずつ。
- 同じ流れのオプションの Windows GUI を提供します（`device` は自動、`documented` は手動、それ以外は停止してここへリンク）。
- `bench snapshot` と `bench compare` で、空き RAM、プロセス数、パッケージ数を前後で測定します。概算であり、ローカルで、因果関係を示すものではありません。[docs/BENCH.md](docs/BENCH.md) を参照。
- 奇跡を約束せずに、バッテリーのベースラインを前後で測定します（`docs/BATTERY.md`）。

## フィードバックとプロファイルのリクエスト

対象外のスマホがある場合、シリアル番号、IP アドレス、IMEI、MAC アドレスを共有せずに、プロファイルを依頼したりバグを報告したりできます:

- **Web:** [cleanyourphone フィードバックフォーム](https://jparedesds.github.io/cleanyourphone-web/#feedback)。
- **アプリ:** ヘッダーの **Feedback**。チェックリストは入力済みで編集できます。
- **Skill:** `python scripts/feedback.py --kind profile --checklist-file feedback.txt` で送信内容をプレビューします。`--yes` は本人が承認したあとだけ付けてください。

メッセージは Cloudflare Worker を経由してメンテナーの Discord に届きます。起動時やスキャン中には何も送信されません。アプリとウェブサイトは同じ Worker を使い、`tools/phone.py` はネットワークに接続しません。送信内容、秘匿化、レート制限は [docs/FEEDBACK.md](docs/FEEDBACK.md) にあります。

## 広告をブロックする（任意）

プライベート DNS は、アプリ内の多くの広告・トラッカードメインをブロックできます。YouTube のブロッカーではなく、VPN でもなく、キャプティブポータルを壊すことがあります。プリセットは:

```bash
python tools/phone.py dns providers
python tools/phone.py dns set adguard
python tools/phone.py dns check
python tools/phone.py dns restore
```

`dns check` は、コントロール用ドメインが解決しない場合に「ブロック済み」と「テストできない」を区別します。メーカー別の広告設定チェックリストと注意点は [docs/ADS.md](docs/ADS.md) にあります。

## 結果を測定する

ローカルに前後のスナップショットを記録します。シリアルもフィンガープリントも保存しません:

```bash
python tools/phone.py bench snapshot --label before
# apply, reboot and verify
python tools/phone.py bench snapshot --label after
python tools/phone.py bench compare <before.json> <after.json>
```

比較は概算で、因果関係を示すものではありません。[docs/BENCH.md](docs/BENCH.md) を参照。

## やらないこと

- **スマホにアプリをインストールしません。** オプションの Windows アプリはパソコン上で動き、スマホは `pm disable-user` / `pm enable` を受け取るだけです。
- **root も Magisk も Shizuku も不要。**
- **カスタム ROM なし、ブートローダー解除なし、ファームウェアの書き込みなし。**
- **アンインストールしません。** `pm disable-user` は元に戻せますが、`pm uninstall` は戻せません。
- **仕事用プロファイルや MDM は変更しません。** 管理されたスマホなら停止します。
- **YouTube の広告ブロックはしません。** プライベート DNS は同一ドメインの広告には効きません。`docs/FAQ.md` で説明しています。
- **自動テレメトリーはありません。** CLI はローカルです。オプションのフィードバックフォームは、本人が送信を押したときだけ送ります。ホスト型エージェントはセッション（モデル、パッケージ名、フィンガープリント）を受け取るので、それが気になるならローカルモデルを使ってください。
- **「バッテリー 2 倍」とは言いません。** デブロートによる現実的な待機時間の改善は 0〜10% です。大きく効くのはバックグラウンド制限、画面輝度/リフレッシュレート、DNS です。

## 安全性

初回実行前に [docs/SAFETY.md](docs/SAFETY.md) を読んでください。要点:

- CLI は保護リストのパッケージ、ロールを保持しているパッケージ、バックアップのない変更を拒否します。
- すべての無効化は記録されます。`python tools/phone.py restore` はツールが無効化したものだけを元に戻し、すでに無効化していたものには触れません。
- スマホがブートループした場合の復旧手順は [docs/RESTORE.md](docs/RESTORE.md) にあります。最初の一手として工場出荷状態へのリセットをしないでください。
- デブロートは元に戻せますが、メーカーの見解は違うかもしれません。EU ではそれ自体で法的保証が失われることはありませんが、修理センターが改造されたソフトウェアの作業を断ることがあります。本人には正直に伝えてください。

## プロファイル

プロファイルは、実機でテストしたパッケージ一覧（`device`）か、一次ファームウェアダンプから作った一覧（`documented`）です。documented プロファイルは自動適用されず、`disable` リストを持ちません。パッケージごとに尋ねるために使います。`apply` は `tested` に載っているビルド上の `device` プロファイルでのみ実行されます。タブレットのプロファイルは `form_factor: tablet` を設定します。ダイヤラー/SMS のロールがない場合は失敗ではなく警告です。

Windows アプリも同じルールに従います。`device` プロファイルはテスト済みの流れを使え、`documented` プロファイルは警告と明示的な確認を必要とし、1 バッチ 1 パッケージで実行します。一致するプロファイルがなければ、アプリは推測せずに停止し、この skill へリンクします。

モデル別の完全なカタログは [docs/PROFILES.md](docs/PROFILES.md) にあります。

| ブランド | プロファイル | 実機テスト済み | タブレット |
|---|---|---|---|
| **Google** | 5 | 1 | 0 |
| **Samsung** | 55 | 1 | 7 |
| **Xiaomi** | 15 | 1 | 2 |
| **Redmi** | 56 | 0 | 1 |
| **POCO** | 16 | 0 | 0 |
| **OnePlus** | 8 | 1 | 0 |
| **汎用** | 1 | 0 | 0 |

自分のモデルを追加したいですか？[profiles/README.md](profiles/README.md) を読んでください。`device` プロファイルには実機テストが必要です。`documented` プロファイルには一次ファームウェアダンプ、または所有者が収集した端末インベントリと、少なくとも 1 つのソース URL が必要です。

## オープンソース OS という選択肢

はい、あります。いいえ、最初にやることではありません。[docs/ROMS.md](docs/ROMS.md) が現実のトレードオフを説明しています:

- **GrapheneOS** は優れていますが、Pixel 6〜10（2026 年 10 月）のみ。最高のセキュリティとプライバシー、サンドボックス化された Play Services、ロックされたブートローダー。
- **/e/OS** は簡単にインストールできる範囲が最も広く、Google の代わりに microG を使います。
- **LineageOS** は対応が広いもののメンテナンス負荷が高く、公式ビルドは端末ごとに異なります。
- **CalyxOS** は Pixel、Fairphone、一部の Motorola をカバーします。

コストは現実です。ブートローダーの解除でスマホは初期化され、Play Integrity で銀行/Wallet が壊れたり Netflix が SD 画質になったりし、一部のキャリアでは VoLTE/Wi-Fi 通話が使えなくなり、セキュリティパッチのメンテナーは自分になります。Samsung では解除すると Knox が恒久的に切れます。だからこそ skill は純正 ROM にとどまります。多くの人が気づく広告とテレメトリーの面を、そうしたコストなしで減らせるからです。堅牢化された OS ではなく、Pixel 上の GrapheneOS の代わりにもなりません。

## FAQ

**保証は無効になりますか？**デブロートはソフトウェア設定であり、ハードウェアの改造ではありません。元に戻せます。EU では法的保証が自動的に無効になることはありませんが、修理センターが改造されたソフトウェアの作業を断ることがあります。skill はブートローダーを解除しません。

**スマホを文鎮化（ブリック）できますか？**間違った中核パッケージを無効化すると、ブートループになる可能性があります。だから CLI は保護リストのパッケージを拒否し、ロールを確認し、最初にバックアップし、バッチで検証します。`restore` はツールが無効化したものだけを元に戻します。ジャーナルが失われた場合は、`restore --from-backup` がバックアップから変更を再構築します。セーフモードを含む完全な復旧手順は [docs/RESTORE.md](docs/RESTORE.md) にあります。

**YouTube の広告は消えますか？**いいえ。プライベート DNS 上の広告ブロックリゾルバーは、アプリ内の多くの広告とトラッカーをブロックしますが、YouTube は動画と同じドメインから広告を配信します。skill はパッチ済みアプリをインストールしません。

**仕事用のスマホでも動きますか？**いいえ。`dumpsys device_policy` が device owner または profile owner を示す場合、または `pm list users` が複数ユーザーを示す場合、skill は停止します。

**Samsung/Xiaomi/Huawei でも動きますか？**この方法は Android 8 以上のスマホならどれでも動きます。パッケージ名と安全リストは異なります。自分のモデルに合うプロファイルを使うか、エージェントに手動で分類させ、パッケージごとに確認してください。Google サービスがない Huawei/Honor では、多くの `com.google.*` パッケージが存在しません。

**Python は必要ですか？**いいえ。skill には生の `adb` コマンドが含まれています。CLI はガードレールと利便性のためのもので、標準ライブラリだけで動き、依存関係はありません。Windows アプリは CLI を同梱し、Python を必要としません。

**GUI はありますか？**はい、[cleanyourphone-app](https://github.com/jparedesDS/cleanyourphone-app) にオプションの Windows アプリがあります。Early MVP でコード署名はなく、既知のプロファイルでのみ続行します。それ以外のスマホでは skill が道です。

**スマホの情報提供やフィードバックはどう送りますか？** [ウェブフォーム](https://jparedesds.github.io/cleanyourphone-web/#feedback)、アプリの **Feedback**、または skill の `scripts/feedback.py` を使ってください。オプトインで、送信内容をプレビューし、シリアル、IP、IMEI、MAC アドレスを除外します。詳細は [docs/FEEDBACK.md](docs/FEEDBACK.md)。

## コントリビュート

- 新しいモデルのテスト済み（`device`）プロファイル: `profiles/<brand>/<model>.json` とテスト詳細を添えて PR を開きます。
- `documented` プロファイル: `scripts/dump_inventory.py` を使い、`sources` に一次ダンプを引用し、`disable` は空のままにします。
- ガード、パーサー、CLI の修正: `tests/` にテストを追加します。
- 安全ルールの変更: まず issue を開いてください。そのルールこそが製品です。
- 自分ではテストできないスマホ: モデル、Android、ビルド、フィンガープリントを添えて [プロファイルのリクエスト](https://jparedesds.github.io/cleanyourphone-web/#feedback)を送ってください。シリアルも IP も不要です。
- ブランドやロゴの変更: アセットを変更する前に [docs/BRAND.md](docs/BRAND.md) を読んでください。
- リポジトリを変更する前に [AGENTS.md](AGENTS.md) を読んでください。

## ライセンス

MIT。[LICENSE](LICENSE) を参照。
