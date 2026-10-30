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

**Il tuo telefono, senza il superfluo.** Una skill open source e reversibile per pulire Android, pensata per gli agenti. Disattiva app e servizi preinstallati via ADB: senza root, senza ROM, senza disinstallare nulla e con un comando per annullare tutto.

[Website](https://jparedesds.github.io/cleanyourphone-web/) · [SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [Safety](docs/SAFETY.md) · [157 profiles](profiles/README.md)

## Avvio rapido

1. Installa Android SDK Platform-Tools e aggiungi <code>adb</code> al PATH.
2. Attiva Opzioni sviluppatore e debug USB; collega e autorizza il computer.
3. Clona il repository e apri il tuo agente lì, oppure copia <code>SKILL.md</code> nella cartella delle skill.

```bash
git clone https://github.com/jparedesDS/clean-your-phone
cd clean-your-phone
python tools/phone.py doctor
```

## Sicurezza

- Disattivare, mai disinstallare. L’unico stato modificato è <code>pm disable-user</code>.
- Backup di pacchetti, impostazioni, ruoli e tastiere prima del primo cambio.
- Lista protetta e controllo di dialer, SMS, Home e tastiera.
- Lotti da cinque pacchetti, riavvio e verifica.
- Niente root, ROM, account, telemetria o API di terze parti.

## Documentazione

- [SKILL.md](SKILL.md) — the full procedure and safety rules.
- [PROMPT.md](PROMPT.md) — paste this if your agent does not load skills.
- [docs/SAFETY.md](docs/SAFETY.md) — protected packages, roles and restore.
- [profiles/README.md](profiles/README.md) — 157 model/firmware profiles.
- [README.md](README.md) / [README.es.md](README.es.md) — La documentazione completa è in inglese e spagnolo.

MIT. No account. No telemetry.
