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

**你的手机，减去多余。** 面向编程智能体的开源、可逆 Android 精简 Skill。通过 ADB 停用预装应用和服务：无需 root、无需刷机、不卸载任何应用，一条命令即可全部恢复。

[Website](https://jparedesds.github.io/cleanyourphone-web/) · [SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [Safety](docs/SAFETY.md) · [157 profiles](profiles/README.md)

## 快速开始

1. 安装 Android SDK Platform-Tools，并把 <code>adb</code> 加入 PATH。
2. 开启开发者选项和 USB 调试，连接电脑并授权。
3. 克隆仓库并在其中打开智能体，或把 <code>SKILL.md</code> 复制到 skills 目录。

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

## 安全

- 只停用，不卸载。唯一的状态变更就是 <code>pm disable-user</code>。
- 第一次修改前备份应用列表、设置、角色和输入法。
- 保护列表，并检查拨号、短信、Home 和键盘角色。
- 每批五个应用，重启并验证。
- 不需要 root、ROM、账号、遥测或第三方 API。

## 文档

- [SKILL.md](SKILL.md) — the full procedure and safety rules.
- [PROMPT.md](PROMPT.md) — paste this if your agent does not load skills.
- [docs/SAFETY.md](docs/SAFETY.md) — protected packages, roles and restore.
- [profiles/README.md](profiles/README.md) — 157 model/firmware profiles.
- [README.md](README.md) / [README.es.md](README.es.md) — 完整文档为英文和西班牙文。

MIT. No account. No telemetry.
