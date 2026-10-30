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

**Dein Smartphone, ohne Ballast.** Eine Open-Source- und reversible Android-Debloat-Skill für Coding-Agenten. Sie deaktiviert vorinstallierte Apps und Dienste per ADB: kein Root, keine Custom-ROM, keine Deinstallation – und ein Befehl zum Rückgängigmachen.

[Website](https://jparedesds.github.io/cleanyourphone-web/) · [SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [Safety](docs/SAFETY.md) · [157 profiles](docs/PROFILES.md)

## Schnellstart

1. Android SDK Platform-Tools installieren und <code>adb</code> zum PATH hinzufügen.
2. Entwickleroptionen und USB-Debugging aktivieren, per USB verbinden und den Computer autorisieren.
3. Repository klonen und den Agenten darin öffnen oder <code>SKILL.md</code> in seinen Skills-Ordner kopieren.

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

## Sicherheit

- Deaktivieren, nie deinstallieren. Der einzige Zustandswechsel ist <code>pm disable-user</code>.
- Backup von Paketen, Einstellungen, Rollen und Tastaturen vor der ersten Änderung.
- Geschützte Liste und Prüfung von Dialer, SMS, Home und Tastatur.
- Fünf Pakete pro Batch, Neustart und Verifikation.
- Kein Root, keine ROM, kein Konto, keine Telemetrie und keine Drittanbieter-API.

## Dokumentation

- [SKILL.md](SKILL.md) — the full procedure and safety rules.
- [PROMPT.md](PROMPT.md) — paste this if your agent does not load skills.
- [docs/SAFETY.md](docs/SAFETY.md) — protected packages, roles and restore.
- [docs/PROFILES.md](docs/PROFILES.md) — 157 model/firmware profiles.
- [README.md](README.md) / [README.es.md](README.es.md) — Die vollständige Dokumentation ist auf Englisch und Spanisch.

MIT. No account. No telemetry.
