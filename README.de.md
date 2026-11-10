<p align="center">
  <a href="https://jparedesds.github.io/cleanyourphone-web/">
    <img src="assets/banner.png" alt="CleanYourPhone — dein Smartphone, ohne Ballast" width="100%">
  </a>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.es.md">Español</a> ·
  <a href="README.pt-BR.md">Português (BR)</a> ·
  <a href="README.fr.md">Français</a> ·
  <b>Deutsch</b> ·
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
  <img src="https://img.shields.io/badge/telemetry-none-a78bfa?labelColor=121316" alt="Keine Telemetrie">
  <img src="https://img.shields.io/badge/profiles-156-a78bfa?labelColor=121316" alt="156 Profile">
  <a href="https://github.com/jparedesDS/cleanyourphone/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone?color=a78bfa&labelColor=121316" alt="release"></a>
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone-app?color=a78bfa&label=app&labelColor=121316" alt="app release"></a>
</p>

# CleanYourPhone

**Dein Smartphone, ohne Ballast.** Eine Open-Source-Debloat-Skill für Android, deren Änderungen
sich vollständig rückgängig machen lassen, gebaut für Coding-Agenten. Sie deaktiviert vorinstallierte
Apps und Dienste über ADB: kein Root, keine Custom-ROM, nichts wird deinstalliert, und ein Befehl
macht die von der CLI protokollierten Änderungen rückgängig.

Die Geschichte und das Sicherheitsmodell findest du unter
**[jparedesds.github.io/cleanyourphone-web](https://jparedesds.github.io/cleanyourphone-web/)**.

Außerdem gibt es eine optionale **Windows-App** für alle, die lieber Schaltflächen als Prompts mögen:
**[Lade die frühe MVP-Version herunter](https://github.com/jparedesDS/cleanyourphone-app/releases/latest)**.
Sie ist eine GUI auf Basis derselben CLI. Die Skill bleibt das Hauptprodukt und der Weg für Smartphones
ohne Profil.

CleanYourPhone ist die Smartphone-Version von [cleanyour.tv](https://cleanyour.tv), nach demselben
Prinzip gebaut: ein Prompt, ein Befehl, reversibel, Open Source, und die Person behält die Kontrolle.

[SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [App](https://github.com/jparedesDS/cleanyourphone-app) · [Sicherheit](docs/SAFETY.md) · [156 Profile](docs/PROFILES.md) · [Feedback](docs/FEEDBACK.md) · [Changelog](CHANGELOG.md)

## Hier starten

| Du hast | Starte mit |
|---|---|
| Ein Smartphone und einen Coding-Agenten | Der Schnellstart unten. |
| Lieber Schaltflächen als Prompts | [Lade die Windows-App herunter](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) (frühe MVP-Version). |
| Willst du es erst sehen | [Die Website](https://jparedesds.github.io/cleanyourphone-web/). |
| Brauchst du die Sicherheitsregeln | [docs/SAFETY.md](docs/SAFETY.md). |
| Brauchst du ein Modellprofil | [Durchsuche die 156 Profile](profiles/README.md). |
| Dein Smartphone ist nicht dabei | Nutze die Skill manuell oder schicke eine [Profilanfrage](docs/FEEDBACK.md). |
| Bevorzugst du ein Terminal | [Installiere die CLI](docs/CLI.md). |

| Teil | Status |
|---|---|
| **Skill** | Hauptprodukt, in diesem Repository. |
| **CLI** | `0.3.2`, auf PyPI als `cleanyourphone` / `cyp`. |
| **Windows-App** | `0.2.0` frühe MVP-Version, optional, nicht signiert. |
| **Website** | In 10 Sprachen unter [jparedesds.github.io/cleanyourphone-web](https://jparedesds.github.io/cleanyourphone-web/). |
| **Feedback** | Optionales Web-/App-/Skill-Formular an Discord; keine automatische Telemetrie. |

---

## Warum die Skill zuerst kommt

Eine App, die andere Apps deaktiviert, braucht Root, Shizuku oder Device-Owner-Rechte. Das ist viel
Macht und viel Risiko für etwas, das ein Shell-Befehl erledigen kann. Eine Skill ist nur Text: Der
Agent der Person liest sie, führt `adb` aus, zeigt einen Plan und fragt, bevor irgendetwas angefasst
wird. Es muss nichts auf dem Smartphone installiert werden, nichts läuft im Hintergrund, und nichts
telefoniert nach Hause.

Es gibt inzwischen eine optionale Windows-App, aber sie ersetzt die Skill nicht. Sie ist eine GUI
auf Basis derselben CLI und macht nur weiter, wenn sie ein exaktes `device`-Profil mit einem getesteten
Build findet oder ein `documented`-Profil nach einer ausdrücklichen Bestätigung – dann ein Paket pro
Batch. Wenn sie das Smartphone nicht zuordnen kann, stoppt sie und schickt die Person hierher. Die
Skill kann weiterhin die Paketliste prüfen, nach jeder App fragen und manuell fortfahren.

Das Smartphone ist das Hauptgerät der Person, deshalb ist die Skill bewusst konservativ:

- **Deaktivieren, nie deinstallieren.** Nur `pm disable-user --user 0`. `pm enable` ist der Rückweg.
- **Zuerst ein Backup.** Paketlisten, Einstellungen, Rollen, IMEs und `getprop` vor der ersten
  Änderung.
- **Geschützte Liste.** Android-Core, Telefonie, Play Services, WebView, Permission Controller,
  Notfallwarnungen, IME/Telecom, NFC/SE und OEM-Sicherheitspakete lehnt die CLI ab.
- **Rollenprüfungen.** Sie lässt dich nicht ohne Dialer, SMS-App, Home-App oder Tastatur zurück.
- **Kleine Batches.** Fünf Pakete auf einmal, verifizieren, dann weiter.
- **Erst fragen.** Banking, Zahlungen, WhatsApp, Kamera, Wecker, VPN, Authenticator, Smartwatch,
  eSIM, VoLTE/WLAN-Telefonie und Arbeits-Apps sind eine Checkliste, keine Standardauswahl.

## So funktioniert es

1. **Auf dem Smartphone:** Aktiviere die Entwickleroptionen und USB-Debugging. Verbinde es per USB.
2. **Auf dem Computer:** Gib deinem Agenten `SKILL.md` (oder füge `PROMPT.md` ein).
3. **Folge mit:** Der Agent identifiziert das Smartphone, legt ein Backup an, zeigt eine Tabelle der
   Pakete, fragt, was du nutzt, deaktiviert in Batches, startet neu und verifiziert.
   `python tools/phone.py restore` macht alles rückgängig.

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

## Die optionale Windows-App

Für alle, die Schaltflächen bevorzugen, verpackt die App dieselbe CLI in einen geführten
Windows-Ablauf: verbinden, prüfen, Backup, überprüfen, anwenden, verifizieren und rückgängig machen.

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases/latest">
    <img src="assets/app-review.png" alt="Review-Bildschirm der CleanYourPhone-App mit Warnung zu einem documented-Profil und einer ausgewählten App" width="760">
  </a>
</p>

- **Per WLAN oder USB verbinden.** Die App findet das Smartphone, prüft den Build und zeigt das
  exakte Profil.
- **Exakte `device`-Profile** folgen dem getesteten Pfad. **`documented`-Profile** sind manuell:
  sichtbare Warnung, ausdrückliche Bestätigung und eine App pro Batch. Ohne Profil stoppt die App
  und verweist auf die Skill.
- **Backup ist Pflicht.** Prüfe jedes Paket, wende in Batches an, verifiziere und mache das gesamte
  Journal rückgängig.
- **Optionale Extras:** Werbeblockierung per Private DNS (nicht YouTube) und ein lokaler
  Vorher-nachher-Benchmark.
- **Optionales Feedback:** Eine bearbeitbare Checkliste kann nach Zustimmung an den Maintainer
  gesendet werden. Keine automatische Telemetrie.
- **Kein Root, keine Deinstallation, keine App auf dem Smartphone installiert.** Der Installer ist
  nicht signiert; prüfe die SHA-256 vor dem Ausführen.

[Herunterladen `v0.2.0`](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) ·
[Quellcode](https://github.com/jparedesDS/cleanyourphone-app) ·
[Verbindungsanleitung](docs/CONNECT.md).

## Schnellstart

### 1. ADB installieren

Lade die [Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools)
für Windows, macOS oder Linux herunter, entpacke sie und füge sie dem `PATH` hinzu. Prüfe mit:

```bash
adb version
```

### 2. Smartphone vorbereiten

Einstellungen → Über das Telefon → 7-mal auf **Build-Nummer** tippen → zurück →
**Entwickleroptionen** → **USB-Debugging** einschalten. Verbinde das Smartphone per USB und
akzeptiere die Aufforderung **USB-Debugging zulassen?**. Halte es entsperrt und mit mehr als 30 %
Akku.

Android 11 und neuer kann stattdessen **Drahtloses Debugging** nutzen: einschalten, auf den Text
tippen (nicht nur auf den Schalter), **Gerät mit Kopplungscode koppeln** wählen und diesen Dialog
geöffnet lassen. Der Kopplungsdialog hat einen eigenen Port; er ist nicht der Verbindungsport auf dem
Hauptbildschirm. Die Schritt-für-Schritt-Anleitung für den ersten Start und die üblichen Lösungen
stehen in [docs/CONNECT.md](docs/CONNECT.md).

### 3. Klonen und prüfen

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

Die CLI ist optional. `SKILL.md` enthält auch die rohen `adb`-Befehle, sodass ein Agent ohne Python
arbeiten kann. Die CLI existiert, damit der Agent die Leitplanken nicht selbst improvisiert.

Lieber ein Terminal? Installiere den Befehl mit [pipx](https://pipx.pypa.io/):

```bash
pipx install cleanyourphone
cleanyourphone doctor
```

Das installiert `cleanyourphone` und den kurzen Alias `cyp`. [docs/CLI.md](docs/CLI.md) beschreibt
den Wizard, die Speicherorte der installierten Dateien und die Sicherheitsregeln.
`python tools/phone.py` funktioniert weiterhin.

### 4. Gib deinem Agenten die Skill

| Agent | Wohin damit |
|---|---|
| **Claude Code** | `~/.claude/skills/cleanyourphone/SKILL.md` (persönlich) oder `.claude/skills/cleanyourphone/SKILL.md` (Projekt) |
| **OpenCode** | `~/.config/opencode/skills/cleanyourphone/SKILL.md` (global) oder `.opencode/skills/cleanyourphone/SKILL.md` (Projekt) |
| **Codex** | `AGENTS.md` im Projekt oder `~/.codex/AGENTS.md`; füge `PROMPT.md` ein, wenn dein Build keine Skills lädt |
| **Cursor** | `.cursor/rules/cleanyourphone.mdc` mit dem Inhalt von `SKILL.md` |
| **Gemini CLI** | `GEMINI.md` im Projekt |
| **Jeder Chat-Agent** | Füge `PROMPT.md` ein und dann `SKILL.md`, wenn danach gefragt wird |

Spanischer Prompt: [PROMPT.es.md](PROMPT.es.md). Die Skill antwortet in der Sprache, in der die
Person schreibt.

Der einfachste Aufbau: Klone das Repository und öffne deinen Agenten in diesem Ordner. `SKILL.md`
liegt bereits im Root, also funktioniert `python tools/phone.py`. Wenn dein Agent Skills aus einem
globalen Ordner lädt, kopiere `SKILL.md` dorthin; installiere die CLI mit pipx (oben), dann musst du
das Repository nicht geklont halten:

```bash
mkdir -p ~/.claude/skills/cleanyourphone
cp SKILL.md ~/.claude/skills/cleanyourphone/SKILL.md
```

Auch ohne das Repository funktioniert die Skill: Sie enthält die rohen `adb`-Befehle und weist den
Agenten an, sie zu verwenden.

Dann frage: **„Räum mein Smartphone auf“** oder **„Nutze cleanyourphone auf meinem Pixel“**.

## Was sie macht

- Deaktiviert OEM-Telemetrie, Werbeflächen, Empfehlungszeilen, doppelte Browser/Stores und ungenutzte
  Vorinstallationen.
- Richtet optional Private DNS mit Presets (`adguard`, `adguard-family`, `controld`, `mullvad`) oder
  deinem eigenen Resolver ein und prüft, ob Werbung tatsächlich blockiert wird. Kein
  YouTube-Adblocker; siehe [docs/ADS.md](docs/ADS.md).
- Erstellt einen Bericht: was sich geändert hat, warum, was erhalten blieb, der Backup-Pfad und der
  Befehl zum Rückgängigmachen.
- Behandelt `documented`-Profile als manuelle Evidenz: keine `disable`-Liste, kein Auto-Apply, ein
  Paket nach dem anderen nach Prüfung.
- Bietet eine optionale Windows-GUI für denselben Ablauf (`device`-Profile automatisch, `documented`
  manuell, alles andere stoppt und verlinkt hierher).
- Misst freien RAM, Prozesse und Paketanzahl vorher/nachher mit `bench snapshot` und `bench compare`;
  approximativ, lokal und nicht kausal. Siehe [docs/BENCH.md](docs/BENCH.md).
- Misst eine Akku-Baseline vorher/nachher ([docs/BATTERY.md](docs/BATTERY.md)), ohne Wunder zu
  versprechen.

## Feedback und Profilanfragen

Wenn ein Smartphone nicht abgedeckt ist, kann die Person ein Profil anfragen oder einen Fehler
melden, ohne Seriennummer, IP-Adresse, IMEI oder MAC-Adresse zu teilen:

- **Web:** [Feedback-Formular von CleanYourPhone](https://jparedesds.github.io/cleanyourphone-web/#feedback).
- **App:** **Feedback** in der Kopfzeile; die Checkliste ist vorausgefüllt und bearbeitbar.
- **Skill:** `python scripts/feedback.py --kind profile --checklist-file feedback.txt` zeigt die
  Payload als Vorschau; füge `--yes` erst hinzu, nachdem die Person zugestimmt hat.

Die Nachricht geht an einen Cloudflare Worker und dann an den Discord des Maintainers. Beim Start
oder während eines Scans wird nichts gesendet. App und Website nutzen denselben Worker;
`tools/phone.py` bleibt ohne Netzwerk. Siehe [docs/FEEDBACK.md](docs/FEEDBACK.md) für Payload,
Schwärzung und Rate-Limit.

## Werbung blockieren (optional)

Private DNS kann viele In-App-Werbe- und Tracker-Domains blockieren. Es ist kein YouTube-Blocker,
kein VPN, und es kann Captive Portals stören. Die Presets sind:

```bash
python tools/phone.py dns providers
python tools/phone.py dns set adguard
python tools/phone.py dns check
python tools/phone.py dns restore
```

`dns check` unterscheidet „blockiert“ von „nicht testbar“, wenn die Kontroll-Domain nicht auflöst.
Die Checkliste für OEM-Werbeeinstellungen und die Einschränkungen stehen in
[docs/ADS.md](docs/ADS.md).

## Ergebnis messen

Erstelle einen lokalen Vorher-nachher-Schnappschuss; weder Seriennummer noch Fingerprint werden
gespeichert:

```bash
python tools/phone.py bench snapshot --label before
# apply, reboot and verify
python tools/phone.py bench snapshot --label after
python tools/phone.py bench compare <before.json> <after.json>
```

Der Vergleich ist approximativ und nicht kausal. Siehe [docs/BENCH.md](docs/BENCH.md).

## Was sie nicht macht

- **Keine App auf dem Smartphone installiert.** Die optionale Windows-App läuft auf dem Computer;
  das Smartphone erhält nur `pm disable-user` / `pm enable`.
- **Kein Root, kein Magisk, kein Shizuku erforderlich.**
- **Keine Custom-ROM, kein Bootloader-Unlock, kein Flashen.**
- **Keine Deinstallation.** `pm disable-user` ist reversibel; `pm uninstall` nicht.
- **Keine Änderungen an Arbeitsprofilen oder MDM.** Ist das Smartphone verwaltet, stoppt sie.
- **Kein YouTube-Adblocking.** Private DNS blockiert keine Werbung auf derselben Domain.
  [docs/FAQ.md](docs/FAQ.md) erklärt das.
- **Keine automatische Telemetrie.** Die CLI ist lokal; das optionale Feedback-Formular sendet erst,
  wenn eine Person auf Senden drückt. Ein gehosteter Agent erhält trotzdem die Sitzung (Modell,
  Paketnamen, Fingerprint); nutze ein lokales Modell, wenn dir das wichtig ist.
- **Keine „doppelte Akkulaufzeit“.** Der realistische Standby-Gewinn durch Debloat liegt bei 0–10 %;
  die großen Effekte kommen von Hintergrundbeschränkungen, Helligkeit/Bildwiederholrate und DNS.

## Sicherheit

Lies [docs/SAFETY.md](docs/SAFETY.md) vor dem ersten Durchlauf. Die Kurzfassung:

- Die CLI lehnt Pakete der geschützten Liste, Pakete, die eine Rolle belegen, und jede Änderung ohne
  Backup ab.
- Jede Deaktivierung wird protokolliert. `python tools/phone.py restore` aktiviert genau das wieder,
  was das Tool deaktiviert hat, und lässt alles unangetastet, was du schon deaktiviert hattest.
- Wenn das Smartphone in einen Bootloop gerät, enthält [docs/RESTORE.md](docs/RESTORE.md) den Weg
  zur Wiederherstellung. Mach nicht als Erstes einen Factory Reset.
- Debloating ist reversibel, aber dein OEM kann das anders sehen. In der EU erlischt die gesetzliche
  Gewährleistung dadurch nicht automatisch, aber ein Reparaturservice kann die Arbeit an modifizierter
  Software ablehnen. Sei ehrlich zu der Person.

## Profile

Ein Profil ist entweder eine Paketliste, die auf einem echten Smartphone getestet wurde (`device`),
oder eine Liste aus einem primären Firmware-Dump (`documented`). Dokumentierte Profile werden nie
automatisch angewendet und haben keine `disable`-Liste; nutze sie, um Paket für Paket zu fragen.
`apply` läuft nur für ein `device`-Profil auf einem Build, das in `tested` steht. Tablet-Profile
setzen `form_factor: tablet`; eine fehlende Dialer-/SMS-Rolle ist eine Warnung, kein Fehler.

Die Windows-App folgt derselben Regel: `device`-Profile dürfen den getesteten Ablauf nutzen,
`documented`-Profile verlangen eine Warnung und eine ausdrückliche Bestätigung und laufen mit einem
Paket pro Batch. Wenn kein Profil passt, stoppt die App und verlinkt auf diese Skill, statt zu raten.

Der vollständige Katalog, Modell für Modell, steht in [docs/PROFILES.md](docs/PROFILES.md).

| Marke | Profile | Am Gerät getestet | Tablets |
|---|---|---|---|
| **Google** | 5 | 1 | 0 |
| **Samsung** | 55 | 1 | 7 |
| **Xiaomi** | 15 | 1 | 2 |
| **Redmi** | 56 | 0 | 1 |
| **POCO** | 16 | 0 | 0 |
| **OnePlus** | 8 | 1 | 0 |
| **Generisch** | 1 | 0 | 0 |

Willst du deins hinzufügen? Lies [profiles/README.md](profiles/README.md). Ein `device`-Profil
braucht einen echten Test; ein `documented`-Profil braucht einen primären Firmware-Dump oder ein vom
Besitzer erstelltes Geräteinventar, plus mindestens eine Quell-URL.

## Die Frage nach dem Open-Source-Betriebssystem

Ja, es gibt Open-Source-Betriebssysteme. Nein, sie sind nicht das Erste, was du tun solltest.
[docs/ROMS.md](docs/ROMS.md) erklärt die realen Trade-offs:

- **GrapheneOS** ist hervorragend, aber nur auf Pixel 6–10 (Oktober 2026). Beste Sicherheit und
  Privatsphäre; sandboxed Play Services; gesperrter Bootloader.
- **/e/OS** hat die breiteste Liste für einfache Installation, mit microG statt Google.
- **LineageOS** ist breit, aber wartungsintensiver; offizielle Builds variieren je nach Gerät.
- **CalyxOS** deckt Pixel, Fairphone und einige Motorola-Modelle ab.

Die Kosten sind real: Ein Bootloader-Unlock löscht das Smartphone, Play Integrity kann Banking/Wallet
unbrauchbar machen und Netflix auf SD herunterstufen, manche Mobilfunkanbieter verlieren
VoLTE/WLAN-Telefonie, und du wirst zum Maintainer der Sicherheitspatches. Bei Samsung löst das
Entsperren Knox dauerhaft aus. Deshalb bleibt die Skill auf der Stock-ROM: Sie entfernt die Werbe- und
Telemetriefläche, die die meisten bemerken, ohne diese Kosten. Sie ist kein gehärtetes OS und kein
Ersatz für GrapheneOS auf einem Pixel.

## FAQ

**Erlischt meine Garantie?**
Debloating ist Softwarekonfiguration, keine Hardwareänderung, und es ist reversibel. In der EU
erlischt die gesetzliche Gewährleistung dadurch nicht automatisch, aber ein Reparaturservice kann
modifizierte Software ablehnen. Die Skill entsperrt den Bootloader nicht.

**Kann ich mein Smartphone bricken?**
Das Deaktivieren des falschen Core-Pakets kann einen Bootloop auslösen. Deshalb lehnt die CLI eine
geschützte Liste ab, prüft Rollen, legt zuerst ein Backup an und verifiziert in Batches. `restore`
macht genau das rückgängig, was das Tool deaktiviert hat; wenn sein Journal verloren geht,
rekonstruiert `restore --from-backup` die Änderung aus dem Backup. Der vollständige
Wiederherstellungsweg, inklusive abgesichertem Modus, steht in [docs/RESTORE.md](docs/RESTORE.md).

**Entfernt sie Werbung aus YouTube?**
Nein. Ein Ad-blocking-Resolver über Private DNS blockiert viele In-App-Anzeigen und Tracker, aber
YouTube liefert Werbung von derselben Domain wie das Video. Die Skill installiert keine gepatchten
Apps.

**Funktioniert sie auf einem Firmensmartphone?**
Nein. Wenn `dumpsys device_policy` einen Device- oder Profile-Owner zeigt oder `pm list users` mehr
als einen Benutzer ausgibt, stoppt die Skill.

**Funktioniert sie auf Samsung/Xiaomi/Huawei?**
Die Methode funktioniert auf jedem Smartphone ab Android 8. Die Paketnamen und die sichere Liste
unterscheiden sich. Nutze ein Profil für dein exaktes Modell oder lass den Agenten manuell
klassifizieren und vor jedem Paket fragen. Auf Huawei/Honor ohne Google-Dienste existieren viele
`com.google.*`-Pakete nicht.

**Brauche ich Python?**
Nein. Die Skill enthält die rohen `adb`-Befehle. Die CLI ist eine Leitplanke und eine Bequemlichkeit;
sie nutzt nur die Standardbibliothek und hat keine Abhängigkeiten. Die Windows-App bündelt die CLI
und benötigt kein Python.

**Gibt es eine GUI?**
Ja, eine optionale Windows-App in
[cleanyourphone-app](https://github.com/jparedesDS/cleanyourphone-app). Sie ist eine frühe
MVP-Version, nicht code-signiert und läuft nur bei einem bekannten Profil weiter. Die Skill bleibt der
Weg für jedes andere Smartphone.

**Wie melde ich ein Smartphone oder schicke Feedback?**
Nutze das [Webformular](https://jparedesds.github.io/cleanyourphone-web/#feedback), **Feedback** in
der App oder `scripts/feedback.py` aus der Skill. Es ist Opt-in, zeigt die Payload als Vorschau und
schließt Seriennummer, IP, IMEI und MAC-Adressen aus. Siehe [docs/FEEDBACK.md](docs/FEEDBACK.md).

## Mitmachen

- Ein getestetes (`device`) Profil für ein neues Modell: Öffne einen PR mit
  `profiles/<brand>/<model>.json` und den Testdetails.
- Ein `documented`-Profil: Nutze `scripts/dump_inventory.py`, zitiere den primären Dump in `sources`
  und halte `disable` leer.
- Ein Fix an Guard, Parser oder CLI: Füge einen Test in `tests/` hinzu.
- Eine Änderung an einer Sicherheitsregel: Öffne zuerst ein Issue. Diese Regeln sind das Produkt.
- Ein Smartphone, das du nicht selbst testen kannst: Schicke eine
  [Profilanfrage](https://jparedesds.github.io/cleanyourphone-web/#feedback) mit Modell, Android,
  Build und Fingerprint. Keine Seriennummer und keine IP.
- Änderungen an Marke oder Logo: Lies [docs/BRAND.md](docs/BRAND.md), bevor du Assets änderst.
- Lies [AGENTS.md](AGENTS.md), bevor du das Repository änderst.

## Lizenz

MIT. Siehe [LICENSE](LICENSE).
