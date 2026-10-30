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

**Seu celular, sem o que sobra.** Uma skill de código aberto e reversível para limpar Android, feita para agentes. Desativa apps e serviços pré-instalados via ADB: sem root, sem ROM, sem desinstalar nada e com um comando para desfazer tudo.

[Website](https://jparedesds.github.io/cleanyourphone-web/) · [SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [Safety](docs/SAFETY.md) · [157 profiles](profiles/README.md)

## Início rápido

1. Instale o Android SDK Platform-Tools e adicione <code>adb</code> ao PATH.
2. Ative Opções do desenvolvedor e depuração USB; conecte e autorize o computador.
3. Clone o repositório e abra seu agente nele, ou copie <code>SKILL.md</code> para a pasta de skills.

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

## Segurança

- Desativar, nunca desinstalar. O único estado é <code>pm disable-user</code>.
- Backup de pacotes, ajustes, papéis e teclados antes do primeiro cambio.
- Lista protegida e checagem de dialer, SMS, Home e teclado.
- Lotes de cinco pacotes, reinício e verificação.
- Sem root, ROM, conta, telemetria ou API de terceiros.

## Documentação

- [SKILL.md](SKILL.md) — the full procedure and safety rules.
- [PROMPT.md](PROMPT.md) — paste this if your agent does not load skills.
- [docs/SAFETY.md](docs/SAFETY.md) — protected packages, roles and restore.
- [profiles/README.md](profiles/README.md) — 157 model/firmware profiles.
- [README.md](README.md) / [README.es.md](README.es.md) — A documentação completa está em inglês e espanhol.

MIT. No account. No telemetry.
