<p align="center">
  <a href="https://cleanyourphone.org/">
    <img src="assets/banner.png" alt="CleanYourPhone — il tuo telefono, senza il superfluo" width="100%">
  </a>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.es.md">Español</a> ·
  <a href="README.pt-BR.md">Português (BR)</a> ·
  <a href="README.fr.md">Français</a> ·
  <a href="README.de.md">Deutsch</a> ·
  <b>Italiano</b> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml"><img src="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/license-MIT-a78bfa?labelColor=121316" alt="MIT">
  <img src="https://img.shields.io/badge/python-3.10%2B-a78bfa?labelColor=121316" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/telemetry-none-a78bfa?labelColor=121316" alt="Nessuna telemetria">
  <img src="https://img.shields.io/badge/profiles-157-a78bfa?labelColor=121316" alt="157 profili">
  <a href="https://github.com/jparedesDS/cleanyourphone/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone?color=a78bfa&labelColor=121316" alt="release"></a>
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone-app?color=a78bfa&label=app&labelColor=121316" alt="app release"></a>
</p>

# CleanYourPhone

**Il tuo telefono, senza il superfluo.** Una skill open source e reversibile per il debloat di
Android, pensata per gli agenti di programmazione. Disattiva app e servizi preinstallati via ADB:
niente root, niente ROM personalizzate, senza disinstallare nulla e un solo comando per ripristinare
le modifiche registrate dalla CLI.

La storia e il modello di sicurezza sono su
**[cleanyourphone.org](https://cleanyourphone.org/)**.

C'è anche un'**app opzionale per Windows** per chi preferisce i pulsanti ai prompt:
**[scarica la Early MVP](https://github.com/jparedesDS/cleanyourphone-app/releases/latest)**. È una
GUI sopra la stessa CLI. La skill resta il prodotto principale e il percorso per i telefoni senza un
profilo.

È la versione per telefono di [cleanyour.tv](https://cleanyour.tv), costruita allo stesso modo: un
prompt, un comando, reversibile, open source e la persona resta al comando.

[SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [App](https://github.com/jparedesDS/cleanyourphone-app) · [Sicurezza](docs/SAFETY.md) · [157 profili](docs/PROFILES.md) · [Feedback](docs/FEEDBACK.md) · [Changelog](CHANGELOG.md)

## Inizia da qui

| Hai | Inizia con |
|---|---|
| Un telefono e un agente di programmazione | L'avvio rapido qui sotto. |
| Preferisci i pulsanti ai prompt | [Scarica l'app per Windows](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) (Early MVP). |
| Vuoi vederlo prima | [Il sito](https://cleanyourphone.org/). |
| Ti servono le regole di sicurezza | [docs/SAFETY.md](docs/SAFETY.md). |
| Ti serve un profilo per il tuo modello | [Sfoglia i 157 profili](profiles/README.md). |
| Il tuo telefono non è in elenco | Usa la skill manualmente o invia una [richiesta di profilo](docs/FEEDBACK.md). |
| Preferisci il terminale | [Installa la CLI](docs/CLI.md). |

| Parte | Stato |
|---|---|
| **Skill** | Prodotto principale, in questo repository. |
| **CLI** | `0.3.4`, pubblicata su PyPI come `cleanyourphone` / `cyp`. |
| **App per Windows** | `0.2.3` Early MVP, opzionale, non firmata. |
| **Sito web** | Disponibile in 10 lingue su [cleanyourphone.org](https://cleanyourphone.org/). |
| **Feedback** | Modulo opzionale web/app/skill verso Discord; nessuna telemetria automatica. |

---

## Perché la skill viene prima

Un'app che disattiva altre app richiede root, Shizuku o privilegi di device owner. È molto potere e
molto rischio per qualcosa che un comando shell può già fare. Una skill è solo testo: l'agente della
persona la legge, esegue `adb`, mostra un piano e chiede prima di toccare qualsiasi cosa. Non c'è
nulla da installare sul telefono, nulla in esecuzione in background e nulla che invii dati a casa.

Ora c'è un'app opzionale per Windows, ma non sostituisce la skill. È una GUI sopra la stessa CLI e
continua solo quando riesce a trovare un profilo `device` esatto con una build testata, oppure un
profilo `documented` dopo una conferma esplicita e un pacchetto per lotto. Se non riesce a riconoscere
il telefono, si ferma e manda la persona qui. La skill può comunque ispezionare l'elenco dei pacchetti,
chiedere di ogni app e continuare manualmente.

Il telefono è quello che usi ogni giorno, quindi la skill è volutamente prudente:

- **Disattivare, mai disinstallare.** Solo `pm disable-user --user 0`. `pm enable` è l'annullamento.
- **Prima il backup.** Elenchi dei pacchetti, impostazioni, ruoli, tastiere (IME) e `getprop` prima
  della prima modifica.
- **Lista protetta.** Android core, telefonia, Play Services, WebView, permission controller, avvisi
  di emergenza, IME/telecom, NFC/SE e pacchetti di sicurezza OEM: la CLI li rifiuta.
- **Controllo dei ruoli.** Non ti lascia senza dialer, app SMS, Home o tastiera.
- **Lotti piccoli.** Cinque pacchetti alla volta, verifica, poi continua.
- **Chiedere prima.** Banking, pagamenti, WhatsApp, fotocamera, sveglia, VPN, authenticator,
  smartwatch, eSIM, VoLTE/chiamate Wi-Fi e app di lavoro sono una checklist, non un default.

## Come funziona

1. **Sul telefono:** attiva le Opzioni sviluppatore e il debug USB. Collegalo via USB.
2. **Sul computer:** passa `SKILL.md` al tuo agente (oppure incolla `PROMPT.md`).
3. **Segui il processo:** l'agente identifica il telefono, esegue il backup, mostra una tabella dei
   pacchetti, chiede cosa usi, disattiva a lotti, riavvia e verifica. `python tools/phone.py restore`
   annulla tutto.

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

## L'app opzionale per Windows

Per chi preferisce i pulsanti, l'app avvolge la stessa CLI in un flusso guidato su Windows: connetti,
controlla, backup, rivedi, applica, verifica e annulla.

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases/latest">
    <img src="assets/app-review.png" alt="Schermata di revisione dell'app CleanYourPhone con avviso di profilo documented e un'app selezionata" width="760">
  </a>
</p>

- **Connetti via Wi-Fi o USB.** L'app trova il telefono, controlla la build e mostra il profilo esatto.
- **I profili `device` esatti** seguono il percorso testato. I **profili `documented`** sono manuali:
  avviso visibile, conferma esplicita e un'app per lotto. Se non c'è un profilo, si ferma e rimanda
  alla skill.
- **Il backup è obbligatorio.** Rivedi ogni pacchetto, applica a lotti, verifica e annulla l'intero
  journal.
- **Extra opzionali:** blocco degli annunci via DNS privato (non YouTube) e benchmark locale
  prima/dopo.
- **Feedback opzionale:** una checklist modificabile può essere inviata al maintainer dopo il
  consenso. Nessuna telemetria automatica.
- **Niente root, niente disinstallazione, nessuna app installata sul telefono.** L'installer non è
  firmato; verifica lo SHA-256 prima di eseguirlo.

[Scarica `v0.2.3`](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) ·
[Sorgente](https://github.com/jparedesDS/cleanyourphone-app) ·
[Guida alla connessione](docs/CONNECT.md).

## Avvio rapido

### 1. Installa ADB

Scarica [Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools) per
Windows, macOS o Linux, scompattalo e aggiungilo al `PATH`. Verifica con:

```bash
adb version
```

### 2. Prepara il telefono

Impostazioni → Informazioni sul telefono → tocca **Numero build** 7 volte → indietro → **Opzioni
sviluppatore** → attiva **Debug USB**. Collega il telefono via USB e accetta il prompt **Consentire
il debug USB?**. Tieni il telefono sbloccato e con più del 30% di batteria.

Android 11 e versioni successive possono usare il **Debug wireless**: attivalo, tocca le parole (non
solo l'interruttore), scegli **Associa dispositivo con codice** e lascia aperta quella finestra. La
finestra di associazione ha una sua porta; non è la porta di connessione della schermata principale.
Vedi [docs/CONNECT.md](docs/CONNECT.md) per la procedura iniziale e le soluzioni ai problemi comuni.

### 3. Clona e controlla

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

La CLI è opzionale. `SKILL.md` contiene anche i comandi `adb` grezzi, quindi un agente può lavorare
senza Python. La CLI esiste perché l'agente non improvvisi le protezioni.

Preferisci il terminale? Installa il comando con [pipx](https://pipx.pypa.io/):

```bash
pipx install cleanyourphone
cleanyourphone doctor
```

Questo aggiunge `cleanyourphone` e l'alias breve `cyp`. [docs/CLI.md](docs/CLI.md) descrive la
procedura guidata, i percorsi dei file installati e le regole di sicurezza. `python tools/phone.py`
continua a funzionare.

### 4. Passa la skill al tuo agente

| Agente | Dove metterla |
|---|---|
| **Claude Code** | `~/.claude/skills/cleanyourphone/SKILL.md` (personale) o `.claude/skills/cleanyourphone/SKILL.md` (progetto) |
| **OpenCode** | `~/.config/opencode/skills/cleanyourphone/SKILL.md` (globale) o `.opencode/skills/cleanyourphone/SKILL.md` (progetto) |
| **Codex** | `AGENTS.md` nel progetto, o `~/.codex/AGENTS.md`; incolla `PROMPT.md` se la tua versione non carica le skill |
| **Cursor** | `.cursor/rules/cleanyourphone.mdc` con il contenuto di `SKILL.md` |
| **Gemini CLI** | `GEMINI.md` nel progetto |
| **Qualsiasi agente di chat** | Incolla `PROMPT.md`, poi incolla `SKILL.md` quando lo chiede |

Prompt in spagnolo: [PROMPT.es.md](PROMPT.es.md). La skill risponde nella lingua in cui scrive la
persona.

La configurazione più semplice è clonare il repository e aprire l'agente in quella cartella:
`SKILL.md` è già nella root, quindi `python tools/phone.py` funziona. Se il tuo agente carica le skill
da una cartella globale, copia lì `SKILL.md`; installa la CLI con pipx (sopra) e non devi tenere il
repository clonato:

```bash
mkdir -p ~/.claude/skills/cleanyourphone
cp SKILL.md ~/.claude/skills/cleanyourphone/SKILL.md
```

Anche senza il repository la skill funziona: include i comandi `adb` grezzi e dice all'agente di
usarli.

Poi chiedi: **"Pulisci il mio telefono"** o **"Usa cleanyourphone sul mio Pixel"**.

## Cosa fa

- Disattiva telemetria OEM, spazi pubblicitari, righe di raccomandazione, browser e store duplicati
  e app precaricate inutilizzate.
- Imposta opzionalmente il DNS privato con preset (`adguard`, `adguard-family`, `controld`,
  `mullvad`) o il tuo resolver, e controlla se gli annunci sono davvero bloccati. Non è un blocco
  degli annunci per YouTube; vedi [docs/ADS.md](docs/ADS.md).
- Produce un report: cosa è cambiato, perché, cosa è stato mantenuto, il percorso del backup e il
  comando di annullamento.
- Tratta i profili `documented` come prova manuale: nessuna lista `disable`, nessuna applicazione
  automatica, un pacchetto alla volta dopo la revisione.
- Offre una GUI opzionale per Windows per lo stesso flusso (profili `device` automatici,
  `documented` manuali, tutto il resto si ferma e rimanda qui).
- Misura RAM libera, processi e numero di pacchetti prima/dopo con `bench snapshot` e
  `bench compare`; approssimativo, locale e non causale. Vedi [docs/BENCH.md](docs/BENCH.md).
- Misura un valore di riferimento della batteria prima/dopo (`docs/BATTERY.md`), senza promettere
  miracoli.

## Feedback e richieste di profilo

Se un telefono non è coperto, la persona può chiedere un profilo o segnalare un bug senza condividere
numero di serie, indirizzo IP, IMEI o indirizzo MAC:

- **Web:** [modulo di feedback di cleanyourphone](https://cleanyourphone.org/#feedback).
- **App:** **Feedback** nell'intestazione; la checklist è precompilata e modificabile.
- **Skill:** `python scripts/feedback.py --kind profile --checklist-file feedback.txt` mostra
  l'anteprima del payload; aggiungi `--yes` solo dopo che la persona ha approvato.

Il messaggio arriva a un Cloudflare Worker e poi al Discord del maintainer. Non viene inviato nulla
all'avvio né durante una scansione. L'app e il sito usano lo stesso Worker; `tools/phone.py` resta
senza rete. Vedi [docs/FEEDBACK.md](docs/FEEDBACK.md) per payload, oscuramento dei dati e rate limit.

## Bloccare gli annunci (opzionale)

Il DNS privato può bloccare molti domini di annunci e tracker dentro le app. Non è un blocco per
YouTube, non è una VPN e può rompere i portali captive. I preset sono:

```bash
python tools/phone.py dns providers
python tools/phone.py dns set adguard
python tools/phone.py dns check
python tools/phone.py dns restore
```

`dns check` distingue «bloccato» da «impossibile verificare» quando il dominio di controllo non si
risolve. Vedi [docs/ADS.md](docs/ADS.md) per la checklist degli interruttori annunci OEM e le
avvertenze.

## Misura il risultato

Registra uno snapshot locale prima/dopo; non viene salvato alcun numero di serie o fingerprint:

```bash
python tools/phone.py bench snapshot --label before
# apply, reboot and verify
python tools/phone.py bench snapshot --label after
python tools/phone.py bench compare <before.json> <after.json>
```

Il confronto è approssimativo e non causale. Vedi [docs/BENCH.md](docs/BENCH.md).

## Cosa non fa

- **Nessuna app installata sul telefono.** L'app opzionale per Windows gira sul computer; il telefono
  riceve solo `pm disable-user` / `pm enable`.
- **Niente root, niente Magisk, nessun requisito Shizuku.**
- **Niente ROM personalizzate, niente sblocco del bootloader, niente flashing.**
- **Nessuna disinstallazione.** `pm disable-user` è reversibile; `pm uninstall` no.
- **Nessuna modifica ai profili di lavoro o MDM.** Se il telefono è gestito, si ferma.
- **Nessun blocco degli annunci di YouTube.** Il DNS privato non tocca gli annunci sullo stesso
  dominio. `docs/FAQ.md` lo spiega.
- **Nessuna telemetria automatica.** La CLI è locale; il modulo di feedback opzionale invia solo
  quando una persona preme Invia. Un agente in cloud riceve comunque la sessione (modello, nomi dei
  pacchetti, fingerprint), quindi usa un modello locale se la cosa conta.
- **Nessuna promessa di "doppia batteria".** Il guadagno realistico in standby dal debloat è 0–10%;
  i guadagni principali vengono dalle restrizioni in background, da luminosità/refresh rate e dal DNS.

## Sicurezza

Leggi [docs/SAFETY.md](docs/SAFETY.md) prima della prima esecuzione. In breve:

- La CLI rifiuta i pacchetti della lista protetta, i pacchetti che occupano un ruolo e qualsiasi
  modifica senza backup.
- Ogni disattivazione viene registrata. `python tools/phone.py restore` riattiva esattamente ciò che
  lo strumento ha disattivato e lascia intatto ciò che avevi già disattivato.
- Se il telefono entra in boot loop, [docs/RESTORE.md](docs/RESTORE.md) contiene il percorso di
  recupero. Non fare un factory reset come prima mossa.
- Il debloat è reversibile, ma il tuo OEM potrebbe vederla diversamente. Nell'UE non annulla di per
  sé la garanzia legale, ma un centro di riparazione può rifiutarsi di lavorare su software
  modificato. Sii onesto con la persona.

## Profili

Un profilo è una lista di pacchetti testata su un telefono reale (`device`) oppure una lista
costruita da un dump del firmware primario (`documented`). I profili `documented` non si applicano mai
automaticamente e non hanno una lista `disable`; usali per chiedere pacchetto per pacchetto. `apply`
viene eseguito solo per un profilo `device` su una build elencata in `tested`. I profili tablet
impostano `form_factor: tablet`; un ruolo dialer/SMS mancante è un avviso, non un errore.

L'app per Windows segue la stessa regola: i profili `device` possono usare il flusso testato, i
profili `documented` richiedono un avviso e una conferma esplicita e applicano un pacchetto per lotto.
Se nessun profilo corrisponde, l'app si ferma e rimanda a questa skill invece di indovinare.

Il catalogo completo, modello per modello, è in [docs/PROFILES.md](docs/PROFILES.md).

| Marca | Profili | Testati su dispositivo | Tablet |
|---|---|---|---|
| **Google** | 5 | 1 | 0 |
| **Samsung** | 55 | 1 | 7 |
| **Xiaomi** | 15 | 1 | 2 |
| **Redmi** | 56 | 0 | 1 |
| **POCO** | 16 | 0 | 0 |
| **OnePlus** | 8 | 1 | 0 |
| **Motorola** | 1 | 0 | 0 |
| **Generico** | 1 | 0 | 0 |

Vuoi aggiungere il tuo? Leggi [profiles/README.md](profiles/README.md). Un profilo `device` richiede
un test reale; un profilo `documented` richiede un dump del firmware primario o un inventario del
dispositivo raccolto dal proprietario, più almeno un URL di fonte.

## La questione del sistema operativo open source

Sì, esiste. No, non è la prima cosa da fare. [docs/ROMS.md](docs/ROMS.md) spiega i compromessi reali:

- **GrapheneOS** è eccellente, ma solo su Pixel 6–10 (ottobre 2026). Massima sicurezza e privacy;
  Play Services in sandbox; bootloader bloccato.
- **/e/OS** ha la lista più ampia per un'installazione facile, con microG al posto di Google.
- **LineageOS** è ampio ma richiede più manutenzione; le build ufficiali variano da dispositivo a
  dispositivo.
- **CalyxOS** copre Pixel, Fairphone e alcuni modelli Motorola.

I costi sono reali: sbloccare il bootloader azzera il telefono, Play Integrity può rompere
banking/Wallet e costringere Netflix alla qualità SD, alcuni operatori perdono VoLTE/chiamate Wi-Fi e
diventi tu il maintainer delle patch di sicurezza. Su Samsung, lo sblocco fa scattare Knox in modo
permanente. Per questo la skill resta sulla ROM stock: rimuove gli annunci e la telemetria che la
maggior parte delle persone nota, senza quei costi. Non è un sistema operativo hardened e non
sostituisce GrapheneOS su un Pixel.

## FAQ

**Il debloat annulla la garanzia?**
Il debloat è configurazione software, non modifica hardware, ed è reversibile. Nell'UE una garanzia
legale non viene annullata automaticamente, ma un centro di riparazione può rifiutarsi di intervenire
su software modificato. La skill non sblocca il bootloader.

**Posso brickare il telefono?**
Disattivare il pacchetto core sbagliato può causare un boot loop. Per questo la CLI rifiuta una lista
protetta, controlla i ruoli, esegue prima il backup e verifica a lotti. `restore` annulla esattamente
ciò che lo strumento ha disattivato; se il suo journal è perso, `restore --from-backup` ricostruisce
la modifica dal backup. Il percorso di recupero completo, inclusa la modalità sicura, è in
[docs/RESTORE.md](docs/RESTORE.md).

**Rimuove gli annunci da YouTube?**
No. Un resolver DNS privato con blocco degli annunci intercetta molti annunci e tracker nelle app,
ma YouTube serve gli annunci dallo stesso dominio del video. La skill non installa app modificate.

**Funziona su un telefono di lavoro?**
No. Se `dumpsys device_policy` mostra un device owner o profile owner, o `pm list users` mostra più di
un utente, la skill si ferma.

**Funziona su Samsung/Xiaomi/Huawei?**
Il metodo funziona su qualsiasi telefono Android 8+. I nomi dei pacchetti e la lista sicura cambiano.
Usa un profilo per il tuo modello esatto, oppure lascia che l'agente classifichi manualmente e chieda
prima di ogni pacchetto. Su Huawei/Honor senza servizi Google, molti pacchetti `com.google.*` non
esistono.

**Serve Python?**
No. La skill include i comandi `adb` grezzi. La CLI è una protezione e una comodità; usa solo la
standard library e non ha dipendenze. L'app per Windows include la CLI e non richiede Python.

**Esiste una GUI?**
Sì, un'app opzionale per Windows in
[cleanyourphone-app](https://github.com/jparedesDS/cleanyourphone-app). È una Early MVP, non è
firmata e continua solo con un profilo conosciuto. La skill resta il percorso per ogni altro telefono.

**Come segnalo un telefono o invio feedback?**
Usa il [modulo web](https://cleanyourphone.org/#feedback), **Feedback** nell'app,
o `scripts/feedback.py` dalla skill. È opt-in, mostra l'anteprima del payload ed esclude numero di
serie, IP, IMEI e indirizzi MAC. Vedi [docs/FEEDBACK.md](docs/FEEDBACK.md).

## Contribuire

- Un profilo testato (`device`) per un nuovo modello: apri una PR con `profiles/<brand>/<model>.json`
  e i dettagli del test.
- Un profilo `documented`: usa `scripts/dump_inventory.py`, cita il dump primario in `sources` e
  lascia `disable` vuoto.
- Una correzione a un guard, a un parser o alla CLI: aggiungi un test in `tests/`.
- Una modifica alle regole di sicurezza: apri prima una issue. Quelle regole sono il prodotto.
- Un telefono che non puoi testare di persona: invia una
  [richiesta di profilo](https://cleanyourphone.org/#feedback) con modello,
  Android, build e fingerprint. Nessun numero di serie o IP.
- Modifiche al marchio o al logo: leggi [docs/BRAND.md](docs/BRAND.md) prima di modificare gli asset.
- Leggi [AGENTS.md](AGENTS.md) prima di modificare il repository.

## Licenza

MIT. Vedi [LICENSE](LICENSE).
