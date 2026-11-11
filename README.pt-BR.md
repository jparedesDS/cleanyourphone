<p align="center">
  <a href="https://cleanyourphone.org/">
    <img src="assets/banner.png" alt="CleanYourPhone — seu celular, sem o que sobra" width="100%">
  </a>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.es.md">Español</a> ·
  <b>Português (BR)</b> ·
  <a href="README.fr.md">Français</a> ·
  <a href="README.de.md">Deutsch</a> ·
  <a href="README.it.md">Italiano</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml"><img src="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/license-MIT-a78bfa?labelColor=121316" alt="MIT">
  <img src="https://img.shields.io/badge/python-3.10%2B-a78bfa?labelColor=121316" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/telemetry-none-a78bfa?labelColor=121316" alt="Sem telemetria">
  <img src="https://img.shields.io/badge/profiles-156-a78bfa?labelColor=121316" alt="156 perfis">
  <a href="https://github.com/jparedesDS/cleanyourphone/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone?color=a78bfa&labelColor=121316" alt="release"></a>
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone-app?color=a78bfa&label=app&labelColor=121316" alt="app release"></a>
</p>

# CleanYourPhone

**Seu celular, sem o que sobra.** Uma skill de código aberto e reversível para limpar o Android,
feita para agentes de código. Desativa apps e serviços pré-instalados via ADB: sem root, sem ROM
customizada, nada desinstalado e um comando para restaurar as mudanças que a CLI registrou.

Leia a história e o modelo de segurança em
**[cleanyourphone.org](https://cleanyourphone.org/)**.

Também existe um **app opcional para Windows** para quem prefere botões a prompts:
**[baixe o Early MVP](https://github.com/jparedesDS/cleanyourphone-app/releases/latest)**. É uma GUI
sobre a mesma CLI. A skill continua sendo o produto principal e o caminho para celulares sem perfil.

É a versão para celular do [cleanyour.tv](https://cleanyour.tv), construída do mesmo jeito: um prompt,
um comando, reversível, código aberto e a pessoa no controle.

[SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [App](https://github.com/jparedesDS/cleanyourphone-app) · [Segurança](docs/SAFETY.md) · [156 perfis](docs/PROFILES.md) · [Feedback](docs/FEEDBACK.md) · [Changelog](CHANGELOG.md)

## Comece aqui

| Você tem | Comece por |
|---|---|
| Um celular e um agente de código | O início rápido abaixo. |
| Prefere botões a prompts | [Baixe o app para Windows](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) (Early MVP). |
| Quer ver primeiro | [O site](https://cleanyourphone.org/). |
| Precisa das regras de segurança | [docs/SAFETY.md](docs/SAFETY.md). |
| Precisa de um perfil para seu modelo | [Veja os 156 perfis](profiles/README.md). |
| Seu celular não está na lista | Use a skill manualmente ou envie um [pedido de perfil](docs/FEEDBACK.md). |
| Prefere o terminal | [Instale a CLI](docs/CLI.md). |

| Parte | Status |
|---|---|
| **Skill** | Produto principal, neste repositório. |
| **CLI** | `0.3.3`, publicada no PyPI como `cleanyourphone` / `cyp`. |
| **App para Windows** | `0.2.1` Early MVP, opcional, sem assinatura. |
| **Site** | 10 idiomas em [cleanyourphone.org](https://cleanyourphone.org/). |
| **Feedback** | Formulário opcional no site/app/skill para o Discord; sem telemetria automática. |

---

## Por que a skill vem primeiro

Um app que desativa outros apps precisa de root, Shizuku ou privilégios de device-owner. É muito poder
e muito risco para algo que um comando de shell já faz. Uma skill é só texto: o agente da pessoa lê,
executa `adb`, mostra um plano e pergunta antes de tocar em qualquer coisa. Não há nada instalado no
celular, nada rodando em segundo plano e nada enviando dados para lugar nenhum.

Agora existe um app opcional para Windows, mas ele não substitui a skill. É uma GUI sobre a mesma CLI
e só continua quando consegue casar um perfil `device` exato com uma build testada, ou um perfil
`documented` depois de uma confirmação explícita e um pacote por lote. Se não encontra um perfil
correspondente, ele para e manda a pessoa para cá. A skill ainda pode inspecionar a lista de pacotes,
perguntar sobre cada app e seguir manualmente.

O celular é o aparelho do dia a dia, então a skill é conservadora de propósito:

- **Desativar, nunca desinstalar.** Somente `pm disable-user --user 0`. `pm enable` é o desfazer.
- **Backup primeiro.** Listas de pacotes, ajustes, papéis, teclados e `getprop` antes da primeira
  mudança.
- **Lista protegida.** Android core, telefonia, Play Services, WebView, permission controller, alertas
  de emergência, IME/telecom, NFC/SE e pacotes de segurança do fabricante são recusados pela CLI.
- **Checagem de papéis.** Não vai te deixar sem discador, app de SMS, app de Home ou teclado.
- **Lotes pequenos.** Cinco pacotes por vez, verificar, depois continuar.
- **Perguntar primeiro.** Bancos, pagamentos, WhatsApp, câmera, alarme, VPN, autenticador, smartwatch,
  eSIM, VoLTE/Wi-Fi calling e apps de trabalho entram num checklist, não no padrão.

## Como funciona

1. **No celular:** ative as Opções do desenvolvedor e a depuração USB. Conecte por USB.
2. **No computador:** entregue o `SKILL.md` ao seu agente (ou cole o `PROMPT.md`).
3. **Acompanhe:** o agente identifica o celular, faz backup, mostra uma tabela de pacotes, pergunta o
   que você usa, desativa em lotes, reinicia e verifica. `python tools/phone.py restore` desfaz tudo.

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

## O app opcional para Windows

Para quem prefere botões, o app envolve a mesma CLI num fluxo guiado para Windows: conectar, conferir,
fazer backup, revisar, aplicar, verificar e desfazer.

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases/latest">
    <img src="assets/app-review.png" alt="Tela de revisão do app CleanYourPhone com aviso de perfil documentado e um app selecionado" width="760">
  </a>
</p>

- **Conecte por Wi-Fi ou USB.** O app encontra o celular, confere a build e mostra o perfil exato.
- **Perfis `device` exatos** seguem o caminho testado. **Perfis `documented`** são manuais: aviso
  visível, confirmação explícita e um app por lote. Sem perfil, o app para e indica a skill.
- **Backup obrigatório.** Revise cada pacote, aplique em lotes, verifique e desfaça todo o journal.
- **Extras opcionais:** bloqueio de anúncios por DNS privado (não no YouTube) e um benchmark local
  antes/depois.
- **Feedback opcional:** um checklist editável pode ser enviado ao mantenedor após consentimento. Sem
  telemetria automática.
- **Sem root, sem desinstalar, sem app instalado no celular.** O instalador não é assinado; confira o
  SHA-256 antes de executá-lo.

[Baixar `v0.2.1`](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) ·
[Código-fonte](https://github.com/jparedesDS/cleanyourphone-app) ·
[Guia de conexão](docs/CONNECT.md).

## Início rápido

### 1. Instale o ADB

Baixe o [Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools)
para Windows, macOS ou Linux, descompacte e adicione ao `PATH`. Confira com:

```bash
adb version
```

### 2. Prepare o celular

Configurações → Sobre o telefone → toque **Número da versão** 7 vezes → volte → **Opções do
desenvolvedor** → ative a **Depuração USB**. Conecte o celular por USB e aceite o aviso **Permitir
depuração USB?**. Mantenha o celular desbloqueado e com mais de 30% de bateria.

Android 11 e mais recentes também podem usar a **Depuração sem fio**: ative, toque nas palavras (não
só no interruptor), escolha **Parear dispositivo usando código de pareamento** e mantenha esse diálogo
aberto. O diálogo de pareamento tem a própria porta; não é a porta de conexão da tela principal. Veja
[docs/CONNECT.md](docs/CONNECT.md) para o passo a passo da primeira vez e as correções mais comuns.

### 3. Clone e confira

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

A CLI é opcional. O `SKILL.md` também traz os comandos `adb` puros, então um agente consegue trabalhar
sem Python. A CLI existe para o agente não improvisar as proteções.

Prefere o terminal? Instale o comando com [pipx](https://pipx.pypa.io/):

```bash
pipx install cleanyourphone
cleanyourphone doctor
```

Isso adiciona `cleanyourphone` e o alias curto `cyp`. [docs/CLI.md](docs/CLI.md) cobre o wizard, os
locais dos arquivos instalados e as regras de segurança. `python tools/phone.py` continua funcionando.

### 4. Entregue a skill ao seu agente

| Agente | Onde colocar |
|---|---|
| **Claude Code** | `~/.claude/skills/cleanyourphone/SKILL.md` (pessoal) ou `.claude/skills/cleanyourphone/SKILL.md` (projeto) |
| **OpenCode** | `~/.config/opencode/skills/cleanyourphone/SKILL.md` (global) ou `.opencode/skills/cleanyourphone/SKILL.md` (projeto) |
| **Codex** | `AGENTS.md` no projeto, ou `~/.codex/AGENTS.md`; cole o `PROMPT.md` se sua versão não carrega skills |
| **Cursor** | `.cursor/rules/cleanyourphone.mdc` com o conteúdo do `SKILL.md` |
| **Gemini CLI** | `GEMINI.md` no projeto |
| **Qualquer agente de chat** | Cole o `PROMPT.md` e, quando ele pedir, cole o `SKILL.md` |

Prompt em espanhol: [PROMPT.es.md](PROMPT.es.md). A skill responde no idioma em que a pessoa escreve.

O mais simples é clonar o repositório e abrir o agente nessa pasta: o `SKILL.md` já está na raiz, então
`python tools/phone.py` funciona. Se o seu agente carrega skills de uma pasta global, copie o `SKILL.md`
para lá; instale a CLI com pipx (acima) e você não precisa manter o repositório clonado:

```bash
mkdir -p ~/.claude/skills/cleanyourphone
cp SKILL.md ~/.claude/skills/cleanyourphone/SKILL.md
```

Sem o repositório, a skill continua funcionando: ela inclui os comandos `adb` puros e diz ao agente
para usá-los.

Depois peça: **"Limpe meu celular"** ou **"Use o cleanyourphone no meu Pixel"**.

## O que ele faz

- Desativa telemetria do fabricante, superfícies de anúncios, fileiras de recomendações, navegadores e
  lojas duplicados e apps pré-instalados que você não usa.
- Opcionalmente configura DNS privado com presets (`adguard`, `adguard-family`, `controld`, `mullvad`)
  ou seu próprio resolver, e confere se os anúncios estão realmente bloqueados. Não é um bloqueador de
  anúncios do YouTube; veja [docs/ADS.md](docs/ADS.md).
- Gera um relatório: o que mudou, por quê, o que foi mantido, o caminho do backup e o comando de
  desfazer.
- Trata perfis `documented` como evidência manual: sem lista `disable`, sem auto-aplicar e um pacote
  por vez depois da revisão.
- Oferece uma GUI opcional para Windows com o mesmo fluxo (perfis `device` automáticos, `documented`
  manuais; todo o resto para e indica a skill).
- Mede RAM livre, processos e quantidade de pacotes antes/depois com `bench snapshot` e
  `bench compare`; aproximado, local e sem afirmar causalidade. Veja [docs/BENCH.md](docs/BENCH.md).
- Mede uma linha de base da bateria antes/depois ([docs/BATTERY.md](docs/BATTERY.md)), sem prometer
  milagres.

## Feedback e pedidos de perfil

Se um celular não está coberto, a pessoa pode pedir um perfil ou reportar um bug sem compartilhar
número de série, endereço IP, IMEI ou endereço MAC:

- **Site:** [formulário de feedback do cleanyourphone](https://cleanyourphone.org/#feedback).
- **App:** **Feedback** no cabeçalho; o checklist vem preenchido e editável.
- **Skill:** `python scripts/feedback.py --kind profile --checklist-file feedback.txt` mostra o payload;
  adicione `--yes` só depois que a pessoa aprovar.

A mensagem vai para um Worker da Cloudflare e depois para o Discord do mantenedor. Nada é enviado na
inicialização nem durante uma varredura. O app e o site usam o mesmo Worker; `tools/phone.py` continua
sem rede. Veja [docs/FEEDBACK.md](docs/FEEDBACK.md) para o payload, a remoção de dados sensíveis e o
limite de requisições.

## Bloquear anúncios (opcional)

O DNS privado pode bloquear muitos domínios de anúncios e rastreadores dentro de apps. Não é um
bloqueador de YouTube, não é uma VPN e pode quebrar portais cativos. Os presets são:

```bash
python tools/phone.py dns providers
python tools/phone.py dns set adguard
python tools/phone.py dns check
python tools/phone.py dns restore
```

`dns check` distingue "bloqueado" de "não foi possível testar" quando o domínio de controle não resolve.
Veja [docs/ADS.md](docs/ADS.md) para o checklist de ajustes de anúncios por fabricante e as ressalvas.

## Meça o resultado

Grave um snapshot local antes/depois; nenhum serial ou fingerprint é armazenado:

```bash
python tools/phone.py bench snapshot --label before
# aplique, reinicie e verifique
python tools/phone.py bench snapshot --label after
python tools/phone.py bench compare <before.json> <after.json>
```

A comparação é aproximada e não é causal. Veja [docs/BENCH.md](docs/BENCH.md).

## O que ele não faz

- **Nenhum app instalado no celular.** O app opcional para Windows roda no computador; o celular só
  recebe `pm disable-user` / `pm enable`.
- **Sem root, sem Magisk, sem exigir Shizuku.**
- **Sem ROM customizada, sem desbloqueio de bootloader, sem flash.**
- **Sem desinstalar.** `pm disable-user` é reversível; `pm uninstall` não é.
- **Sem mudanças em perfil de trabalho ou MDM.** Se o celular é gerenciado, ele para.
- **Sem bloqueio de anúncios do YouTube.** O DNS privado não toca em anúncios do mesmo domínio. O
  `docs/FAQ.md` explica.
- **Sem telemetria automática.** A CLI é local; o formulário de feedback opcional só envia quando a
  pessoa aperta Enviar. Um agente hospedado ainda recebe a sessão (modelo, nomes de pacotes,
  fingerprint), então use um modelo local se isso importa.
- **Sem promessa de "bateria em dobro".** O ganho realista em standby com debloat é de 0–10%; os
  grandes ganhos vêm de restrições em segundo plano, brilho/taxa de atualização e DNS.

## Segurança

Leia [docs/SAFETY.md](docs/SAFETY.md) antes da primeira execução. A versão curta:

- A CLI recusa pacotes da lista protegida, pacotes que ocupam um papel e qualquer mudança sem backup.
- Cada desativação fica registrada. `python tools/phone.py restore` reativa exatamente o que a
  ferramenta desativou e deixa intacto o que você já tinha desativado.
- Se o celular entrar em bootloop, [docs/RESTORE.md](docs/RESTORE.md) tem o caminho de recuperação.
  Não faça um factory reset como primeira medida.
- O debloat é reversível, mas seu fabricante pode ver de outra forma. Na UE isso não anula por si só a
  garantia legal, mas uma assistência técnica pode se recusar a mexer em software modificado. Seja
  honesto com a pessoa.

## Perfis

Um perfil é uma lista de pacotes testada em um celular real (`device`) ou uma lista construída a partir
de um dump de firmware primário (`documented`). Perfis documentados nunca são auto-aplicados e não têm
lista `disable`; use-os para perguntar pacote a pacote. `apply` só roda para um perfil `device` em uma
build listada em `tested`. Perfis de tablet definem `form_factor: tablet`; a falta do papel de
discador/SMS é um aviso, não uma falha.

O app para Windows segue a mesma regra: perfis `device` podem usar o fluxo testado, perfis `documented`
exigem um aviso, uma confirmação explícita e um pacote por lote. Se nenhum perfil corresponder, o app
para e indica esta skill em vez de adivinhar.

O catálogo completo, modelo a modelo, está em [docs/PROFILES.md](docs/PROFILES.md).

| Marca | Perfis | Testados em celular | Tablets |
|---|---|---|---|
| **Google** | 5 | 1 | 0 |
| **Samsung** | 55 | 1 | 7 |
| **Xiaomi** | 15 | 1 | 2 |
| **Redmi** | 56 | 0 | 1 |
| **POCO** | 16 | 0 | 0 |
| **OnePlus** | 8 | 1 | 0 |
| **Genérica** | 1 | 0 | 0 |

Quer adicionar o seu? Leia [profiles/README.md](profiles/README.md). Um perfil `device` precisa de um
teste real; um perfil `documented` precisa de um dump de firmware primário ou de um inventário
coletado pelo dono do aparelho, além de pelo menos uma URL de fonte.

## A questão do sistema operacional open source

Sim, ele existe. Não, ele não é a primeira coisa a fazer. [docs/ROMS.md](docs/ROMS.md) explica os
trade-offs reais:

- **GrapheneOS** é excelente, mas só em Pixel 6–10 (outubro de 2026). A melhor segurança e
  privacidade; Play Services em sandbox; bootloader bloqueado.
- **/e/OS** tem a lista mais ampla de instalação fácil, com microG em vez de Google.
- **LineageOS** é amplo, mas exige mais manutenção; as builds oficiais variam por aparelho.
- **CalyxOS** cobre Pixel, Fairphone e alguns modelos Motorola.

Os custos são reais: desbloquear o bootloader apaga o celular, o Play Integrity pode quebrar bancos e
Wallet e derrubar o Netflix para SD, algumas operadoras perdem VoLTE/Wi-Fi calling, e você vira o
mantenedor dos patches de segurança. Na Samsung, desbloquear dispara o Knox para sempre. É por isso que
a skill fica na ROM de fábrica: ela remove a superfície de anúncios e telemetria que a maioria das
pessoas nota, sem esses custos. Não é um sistema endurecido e não substitui o GrapheneOS em um Pixel.

## FAQ

**Isso anula minha garantia?**
O debloat é configuração de software, não modificação de hardware, e é reversível. Na UE, uma garantia
legal não é anulada automaticamente, mas uma assistência técnica pode se recusar a mexer em software
modificado. A skill não desbloqueia o bootloader.

**Posso brickar meu celular?**
Desativar o pacote core errado pode causar um bootloop. Por isso a CLI recusa a lista protegida, checa
papéis, faz backup primeiro e verifica em lotes. `restore` desfaz exatamente o que a ferramenta
desativou; se o journal for perdido, `restore --from-backup` reconstrói a mudança a partir do backup. O
caminho completo de recuperação, incluindo o modo seguro, está em [docs/RESTORE.md](docs/RESTORE.md).

**Isso remove os anúncios do YouTube?**
Não. Um resolver com bloqueio sobre DNS privado bloqueia muitos anúncios e rastreadores dentro de apps,
mas o YouTube serve os anúncios do mesmo domínio do vídeo. A skill não instala apps modificados.

**Funciona em um celular da empresa?**
Não. Se `dumpsys device_policy` mostrar um device owner ou profile owner, ou se `pm list users` mostrar
mais de um usuário, a skill para.

**Funciona em Samsung/Xiaomi/Huawei?**
O método funciona em qualquer Android 8+. Os nomes de pacotes e a lista segura mudam. Use um perfil para
o seu modelo exato, ou deixe o agente classificar manualmente e perguntar antes de cada pacote. Em
Huawei/Honor sem serviços do Google, muitos pacotes `com.google.*` não existem.

**Preciso de Python?**
Não. A skill inclui os comandos `adb` puros. A CLI é uma proteção e uma comodidade; usa só a biblioteca
padrão e não tem dependências. O app para Windows inclui a CLI e não exige Python.

**Existe uma interface gráfica?**
Sim, um app opcional para Windows em [cleanyourphone-app](https://github.com/jparedesDS/cleanyourphone-app).
É um Early MVP, não tem assinatura de código e só continua em um perfil conhecido. A skill continua
sendo o caminho para qualquer outro celular.

**Como reporto um celular ou envio feedback?**
Use o [formulário web](https://cleanyourphone.org/#feedback), o **Feedback** no
app ou `scripts/feedback.py` da skill. É opt-in, mostra o payload antes e exclui número de série, IP,
IMEI e endereços MAC. Veja [docs/FEEDBACK.md](docs/FEEDBACK.md).

## Contribuindo

- Um perfil testado (`device`) para um modelo novo: abra um PR com `profiles/<marca>/<modelo>.json` e
  os detalhes do teste.
- Um perfil `documented`: use `scripts/dump_inventory.py`, cite o dump primário em `sources` e mantenha
  `disable` vazio.
- Um guard, parser ou correção de CLI: adicione um teste em `tests/`.
- Uma mudança em regra de segurança: abra uma issue primeiro. Essas regras são o produto.
- Um celular que você não consegue testar: envie um [pedido de perfil](https://cleanyourphone.org/#feedback)
  com modelo, Android, build e fingerprint. Sem número de série nem IP.
- Mudanças de marca ou logo: leia [docs/BRAND.md](docs/BRAND.md) antes de mexer nos assets.
- Leia [AGENTS.md](AGENTS.md) antes de mudar o repositório.

## Licença

MIT. Veja [LICENSE](LICENSE).
