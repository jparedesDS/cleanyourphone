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

**你的手機，減去多餘。** 專為程式設計代理打造的開源、可逆 Android 精簡 Skill。透過 ADB 停用預裝應用與服務：免 root、免刷機、不解除安裝，一個指令即可全部復原。

[Website](https://jparedesds.github.io/cleanyourphone-web/) · [SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [Safety](docs/SAFETY.md) · [157 profiles](profiles/README.md)

## 快速開始

1. 安裝 Android SDK Platform-Tools，並把 <code>adb</code> 加入 PATH。
2. 開啟開發人員選項與 USB 偵錯，連接電腦並授權。
3. 複製倉庫並在裡面開啟代理，或把 <code>SKILL.md</code> 複製到 skills 資料夾。

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

## 安全

- 只停用，不解除安裝。唯一的狀態變更是 <code>pm disable-user</code>。
- 第一次修改前備份應用程式清單、設定、角色與輸入法。
- 保護清單，並檢查撥號、簡訊、Home 與鍵盤角色。
- 每批五個應用程式，重新開機並驗證。
- 不需要 root、ROM、帳號、遙測或第三方 API。

## 文件

- [SKILL.md](SKILL.md) — the full procedure and safety rules.
- [PROMPT.md](PROMPT.md) — paste this if your agent does not load skills.
- [docs/SAFETY.md](docs/SAFETY.md) — protected packages, roles and restore.
- [profiles/README.md](profiles/README.md) — 157 model/firmware profiles.
- [README.md](README.md) / [README.es.md](README.es.md) — 完整文件為英文與西班牙文。

MIT. No account. No telemetry.
