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

**Votre téléphone, sans le superflu.** Une skill open source et réversible pour nettoyer Android, pensée pour les agents. Elle désactive les applis et services préinstallés via ADB : sans root, sans ROM, sans désinstallation, et une commande pour tout annuler.

[Website](https://jparedesds.github.io/cleanyourphone-web/) · [SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [Safety](docs/SAFETY.md) · [157 profiles](docs/PROFILES.md)

## Démarrage rapide

1. Installez Android SDK Platform-Tools et ajoutez <code>adb</code> au PATH.
2. Activez Options pour les développeurs et le débogage USB ; branchez et autorisez l’ordinateur.
3. Clonez le dépôt et ouvrez votre agent dedans, ou copiez <code>SKILL.md</code> dans son dossier de skills.

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

## Sécurité

- Désactiver, jamais désinstaller. Le seul état modifié est <code>pm disable-user</code>.
- Sauvegarde des paquets, réglages, rôles et claviers avant le premier changement.
- Liste protégée et vérification du dialer, des SMS, de Home et du clavier.
- Lots de cinq paquets, redémarrage et vérification.
- Pas de root, de ROM, de compte, de télémétrie ni d’API tierce.

## Documentation

- [SKILL.md](SKILL.md) — the full procedure and safety rules.
- [PROMPT.md](PROMPT.md) — paste this if your agent does not load skills.
- [docs/SAFETY.md](docs/SAFETY.md) — protected packages, roles and restore.
- [docs/PROFILES.md](docs/PROFILES.md) — 157 model/firmware profiles.
- [README.md](README.md) / [README.es.md](README.es.md) — La documentation complète est en anglais et en espagnol.

MIT. No account. No telemetry.
