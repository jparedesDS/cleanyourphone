<p align="center">
  <a href="https://cleanyourphone.org/es.html">
    <img src="assets/banner.png" alt="CleanYourPhone — tu móvil, sin lo que sobra" width="100%">
  </a>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <b>Español</b> ·
  <a href="README.pt-BR.md">Português (BR)</a> ·
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
  <img src="https://img.shields.io/badge/telemetry-none-a78bfa?labelColor=121316" alt="Sin telemetría">
  <img src="https://img.shields.io/badge/profiles-156-a78bfa?labelColor=121316" alt="156 perfiles">
  <a href="https://github.com/jparedesDS/cleanyourphone/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone?color=a78bfa&labelColor=121316" alt="release"></a>
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone-app?color=a78bfa&label=app&labelColor=121316" alt="app release"></a>
</p>

# CleanYourPhone

**Tu móvil, sin lo que sobra.** Una skill de código abierto y reversible para limpiar Android,
pensada para agentes. Desactiva apps y servicios preinstalados por ADB: sin root, sin ROM cocinada,
sin desinstalar nada y con un comando para restaurar los cambios que registró la CLI.

La historia y el modelo de seguridad, en
**[cleanyourphone.org/es.html](https://cleanyourphone.org/es.html)**.

También hay una **app opcional para Windows** para quien prefiere botones:
**[descarga la Early MVP](https://github.com/jparedesDS/cleanyourphone-app/releases/latest)**. Es una
GUI sobre la misma CLI. La skill sigue siendo el producto principal y el camino para móviles sin
perfil.

Es la versión móvil de [cleanyour.tv](https://cleanyour.tv), con la misma idea: un prompt, un comando,
reversible, open source y la persona siempre al mando.

[SKILL.md](SKILL.md) · [PROMPT.es.md](PROMPT.es.md) · [App](https://github.com/jparedesDS/cleanyourphone-app) · [Seguridad](docs/SAFETY.md) · [156 perfiles](docs/PROFILES.md) · [Feedback](docs/FEEDBACK.md) · [Cambios](CHANGELOG.md)

## Empieza aquí

| Tienes | Empieza por |
|---|---|
| Un móvil y un agente de código | El inicio rápido de abajo. |
| Prefieres botones a prompts | [Descarga la app de Windows](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) (Early MVP). |
| Ganas de verlo primero | [La web](https://cleanyourphone.org/es.html). |
| Dudas de seguridad | [docs/SAFETY.md](docs/SAFETY.md). |
| Un modelo concreto | [Los 156 perfiles](docs/PROFILES.md). |
| Tu móvil no está en la lista | Usa la skill manualmente o envía una [petición de perfil](docs/FEEDBACK.md). |
| Prefieres la terminal | [Instala el CLI](docs/CLI.md). |

| Parte | Estado |
|---|---|
| **Skill** | Producto principal, en este repositorio. |
| **CLI** | `0.3.2`, en PyPI como `cleanyourphone` / `cyp`. |
| **App Windows** | `0.2.0` Early MVP, opcional, sin firmar. |
| **Web** | 10 idiomas en [cleanyourphone.org](https://cleanyourphone.org/es.html). |
| **Feedback** | Formulario opcional app/web/skill a Discord; sin telemetría automática. |

---

## Por qué la skill va primero

Una app que desactiva otras apps necesita root, Shizuku o permisos de device-owner. Es mucho poder y
mucho riesgo para algo que un comando de shell ya hace. Una skill es solo texto: el agente de la
persona la lee, ejecuta `adb`, enseña un plan y pregunta antes de tocar nada. No hay nada instalado
en el móvil, nada corriendo en segundo plano y nada que mande datos a ningún sitio.

Ahora hay una app opcional para Windows, pero no sustituye a la skill. Es una GUI sobre la misma CLI
y solo continúa con un perfil `device` exacto y una build probada, o con un perfil `documented`
después de un aviso, una confirmación explícita y un paquete por lote. Si no encuentra el móvil, se
para y manda aquí. La skill puede inspeccionar la lista, preguntar por cada app y seguir manualmente.

El móvil es el dispositivo principal de la persona, así que la skill es conservadora a propósito:

- **Desactivar, nunca desinstalar.** Solo `pm disable-user --user 0`. La vuelta atrás es `pm enable`.
- **Backup primero.** Lista de paquetes, ajustes, roles, teclados y `getprop` antes del primer cambio.
- **Lista protegida.** Android core, telefonía, Play Services, WebView, permission controller,
  alertas de emergencia, IME/telecom, NFC/SE y paquetes de seguridad del fabricante: el CLI los rechaza.
- **Comprobación de roles.** No te deja sin dialer, sin SMS, sin Home ni sin teclado.
- **Lotes pequeños.** Cinco paquetes, verificar, seguir.
- **Preguntar primero.** Banca, pagos, WhatsApp, cámara, alarma, VPN, autenticador, smartwatch,
  eSIM, VoLTE/Wi-Fi calling y apps de trabajo van en un checklist, no por defecto.

## Cómo funciona

1. **En el móvil:** activa Opciones de desarrollador y Depuración USB. Conéctalo por USB.
2. **En el ordenador:** pásale `SKILL.md` a tu agente (o pega `PROMPT.md`).
3. **Sigue el proceso:** el agente identifica el móvil, hace backup, enseña una tabla de paquetes,
   pregunta qué usas, desactiva por lotes, reinicia y verifica. `python tools/phone.py restore` lo
   deshace.

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

## La app opcional para Windows

Para quien prefiere botones, la app envuelve la misma CLI en un flujo guiado: conectar, comprobar,
backup, revisar, aplicar, verificar y deshacer.

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases/latest">
    <img src="assets/app-review.png" alt="Pantalla Review de la app con aviso de perfil documentado y una app seleccionada" width="760">
  </a>
</p>

- **Wi-Fi o USB.** La app encuentra el móvil, comprueba la build y enseña el perfil exacto.
- **Perfiles `device`** siguen el camino probado. Los **`documented`** son manuales: aviso visible,
  confirmación explícita y una app por lote. Sin perfil, se para y manda a la skill.
- **Backup obligatorio.** Revisa cada paquete, aplica por lotes, verifica y deshaz todo el journal.
- **Extras opcionales:** DNS privado para anuncios (no YouTube) y benchmark local antes/después.
- **Feedback opcional:** checklist editable que solo se envía con consentimiento. Sin telemetría.
- **Sin root, sin desinstalar y sin app en el móvil.** El instalador no está firmado; verifica el
  SHA-256 antes de ejecutarlo.

[Descargar `v0.2.0`](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) ·
[Código](https://github.com/jparedesDS/cleanyourphone-app) ·
[Guía de conexión](docs/CONNECT.md).

## Empezar

### 1. Instala ADB

Descarga [Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools)
para Windows, macOS o Linux, descomprímelo y añádelo al `PATH`. Comprueba:

```bash
adb version
```

### 2. Prepara el móvil

Ajustes → Acerca del teléfono → toca **Número de compilación** 7 veces → atrás → **Opciones de
desarrollador** → activa **Depuración USB**. Conéctalo por USB y acepta el aviso **¿Permitir
depuración USB?**. Mantén el móvil desbloqueado y con más del 30% de batería.

Android 11 o posterior también puede usar **Depuración inalámbrica**: actívala, toca las palabras (no
solo el interruptor), elige **Emparejar dispositivo con código** y deja ese diálogo abierto. El
diálogo de emparejamiento tiene su propio puerto; no es el puerto de conexión de la pantalla
principal. La guía paso a paso y los problemas comunes están en [docs/CONNECT.md](docs/CONNECT.md).

### 3. Clona y comprueba

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

El CLI es opcional. `SKILL.md` incluye también los comandos `adb` en crudo, así que un agente puede
trabajar sin Python. El CLI está para que el agente no se invente las protecciones.

¿Prefieres la terminal? Instala el comando con [pipx](https://pipx.pypa.io/):

```bash
pipx install cleanyourphone
cleanyourphone doctor
```

Añade `cleanyourphone` y el alias corto `cyp`. [docs/CLI.md](docs/CLI.md) explica el wizard, dónde
quedan los backups instalados y las reglas de seguridad. `python tools/phone.py` sigue funcionando.

### 4. Pásale la skill a tu agente

| Agente | Dónde ponerla |
|---|---|
| **Claude Code** | `~/.claude/skills/cleanyourphone/SKILL.md` (personal) o `.claude/skills/cleanyourphone/SKILL.md` (proyecto) |
| **OpenCode** | `~/.config/opencode/skills/cleanyourphone/SKILL.md` (global) o `.opencode/skills/cleanyourphone/SKILL.md` (proyecto) |
| **Codex** | `AGENTS.md` en el proyecto, o `~/.codex/AGENTS.md`; pega `PROMPT.md` si tu versión no carga skills |
| **Cursor** | `.cursor/rules/cleanyourphone.mdc` con el contenido de `SKILL.md` |
| **Gemini CLI** | `GEMINI.md` en el proyecto |
| **Cualquier chat** | Pega `PROMPT.md` y, cuando lo pida, pega `SKILL.md` |

Lo más sencillo es clonar el repo y abrir el agente en esa carpeta: `SKILL.md` ya está en la raíz y
`python tools/phone.py` funciona. Si tu agente carga skills desde una carpeta global, copia ahí
`SKILL.md`; instala el CLI con pipx (arriba) y no necesitas mantener el repo clonado:

```bash
mkdir -p ~/.claude/skills/cleanyourphone
cp SKILL.md ~/.claude/skills/cleanyourphone/SKILL.md
```

Sin el repo, la skill también funciona: incluye los comandos `adb` en crudo y le dice al agente que
los use. También tienes el prompt en español en [PROMPT.es.md](PROMPT.es.md).

Luego pide: **"Limpia mi móvil"** o **"Usa cleanyourphone en mi Pixel"**.

## Qué hace

- Desactiva telemetría del fabricante, superficies de anuncios, filas de recomendaciones, navegadores
  y tiendas duplicadas, y apps preinstaladas que no usas.
- Opcionalmente configura DNS privado con presets (`adguard`, `adguard-family`, `controld`, `mullvad`)
  o tu propio resolver, y comprueba si los anuncios están bloqueados de verdad. No bloquea YouTube;
  consulta [docs/ADS.md](docs/ADS.md).
- Genera un informe: qué cambió, por qué, qué se mantuvo, dónde está el backup y el comando de undo.
- Trata los perfiles `documented` como evidencia manual: sin lista `disable`, sin auto-aplicar y un
  paquete cada vez después de revisar.
- Ofrece una GUI opcional para Windows con el mismo flujo (`device` automático, `documented` manual;
  lo demás se para y enlaza aquí).
- Mide RAM libre, procesos y número de paquetes antes/después con `bench snapshot` y `bench compare`;
  aproximado, local y sin afirmar causalidad. Ver [docs/BENCH.md](docs/BENCH.md).
- Mide una línea base de batería antes/después (`docs/BATTERY.md`), sin prometer milagros.

## Feedback y peticiones de perfil

Si tu móvil no está cubierto, puedes pedir un perfil o reportar un bug sin compartir número de serie,
IP, IMEI ni MAC:

- **Web:** [formulario de feedback](https://cleanyourphone.org/es.html#feedback).
- **App:** **Feedback** en la cabecera; el checklist viene relleno y se puede editar.
- **Skill:** `python scripts/feedback.py --kind profile --checklist-file feedback.txt` enseña el
  payload; añade `--yes` solo después de que la persona lo apruebe.

El mensaje va a un Worker de Cloudflare y luego al Discord del maintainer. No se envía nada al
arrancar ni durante un escaneo. La app y la web usan el mismo Worker; `tools/phone.py` sigue sin red.
Ver [docs/FEEDBACK.md](docs/FEEDBACK.md).

## Bloquear anuncios (opcional)

El DNS privado puede bloquear muchos dominios de anuncios y trackers dentro de apps. No bloquea
YouTube, no es una VPN y puede romper portales cautivos. Los presets son:

```bash
python tools/phone.py dns providers
python tools/phone.py dns set adguard
python tools/phone.py dns check
python tools/phone.py dns restore
```

`dns check` distingue “bloqueado” de “no se pudo comprobar” cuando el dominio de control no resuelve.
La checklist de ajustes por fabricante y las advertencias están en [docs/ADS.md](docs/ADS.md).

## Medir el resultado

Guarda una foto local antes/después; no se guarda el serial ni el fingerprint:

```bash
python tools/phone.py bench snapshot --label before
# aplica, reinicia y verifica
python tools/phone.py bench snapshot --label after
python tools/phone.py bench compare <before.json> <after.json>
```

La comparación es aproximada y no afirma causalidad. Ver [docs/BENCH.md](docs/BENCH.md).

## Qué no hace

- **No instala una app en el móvil.** La app opcional de Windows corre en el ordenador; el móvil solo
  recibe `pm disable-user` / `pm enable`.
- **No root, no Magisk, no hace falta Shizuku.**
- **No ROM, no desbloqueo de bootloader, no flasheo.**
- **No desinstala.** `pm disable-user` es reversible; `pm uninstall` no.
- **No toca perfiles de trabajo ni MDM.** Si el móvil está gestionado, se para.
- **No bloquea anuncios de YouTube.** El DNS privado no toca anuncios del mismo dominio.
  `docs/FAQ.md` lo explica.
- **No promete "el doble de batería".** La ganancia realista en standby por debloat es 0–10%; lo que
  más ahorra es restringir fondo, bajar brillo/refresco y el DNS.
- **Sin telemetría automática.** El CLI es local; el feedback opcional solo se envía al pulsar
  Enviar. Un agente alojado recibe la sesión (modelo, paquetes, fingerprint); usa un modelo local si
  eso importa.

## Seguridad

Lee [docs/SAFETY.md](docs/SAFETY.md) antes de la primera ejecución. Resumen:

- El CLI rechaza paquetes de la lista protegida, paquetes que ocupan un rol y cualquier cambio sin
  backup.
- Cada desactivación queda registrada. `python tools/phone.py restore` reactiva exactamente lo que
  desactivó la herramienta y deja intacto lo que ya estaba desactivado.
- Si el móvil entra en bootloop, [docs/RESTORE.md](docs/RESTORE.md) tiene la ruta de recuperación. No
  hagas un factory reset como primera medida.
- El debloat es reversible, pero tu fabricante puede verlo de otra forma. En la UE no anula por sí
  solo la garantía legal, pero un servicio técnico puede negarse a tocar software modificado. Sé
  honesto con la persona.

## Perfiles

Un perfil es una lista probada en un móvil real (`device`) o una lista construida desde un dump de
firmware primario (`documented`). Los perfiles documentados nunca se auto-aplican y no tienen lista
`disable`: sirven para preguntar paquete a paquete. `apply` solo se ejecuta para un perfil `device`
en un build incluido en `tested`. Los perfiles de tablet llevan `form_factor: tablet`; si falta el
rol de dialer/SMS es un aviso, no un fallo.

La app de Windows sigue la misma regla: `device` usa el flujo probado, `documented` exige aviso,
confirmación explícita y un paquete por lote. Si no hay perfil, se para y enlaza a esta skill.

El catálogo completo, modelo a modelo, está en [docs/PROFILES.md](docs/PROFILES.md).

| Marca | Perfiles | Probados en móvil | Tablets |
|---|---|---|---|
| **Google** | 5 | 1 | 0 |
| **Samsung** | 55 | 1 | 7 |
| **Xiaomi** | 15 | 1 | 2 |
| **Redmi** | 56 | 0 | 1 |
| **POCO** | 16 | 0 | 0 |
| **OnePlus** | 8 | 1 | 0 |
| **Genérico** | 1 | 0 | 0 |

¿Quieres añadir el tuyo? Lee [profiles/README.md](profiles/README.md). Un perfil `device` necesita
una prueba real; uno `documented` necesita un dump de firmware primario o un inventario del propio
dispositivo, y al menos una fuente.

## La pregunta del OS open source

Sí, existe. No, no es lo primero que hay que hacer. [docs/ROMS.md](docs/ROMS.md) explica los
trade-offs reales:

- **GrapheneOS** es excelente, pero solo en Pixel 6–10 (octubre 2026). La mejor seguridad y
  privacidad; Play Services en sandbox; bootloader bloqueado.
- **/e/OS** tiene la lista más amplia con instalación fácil, con microG en vez de Google.
- **LineageOS** es amplio pero exige más mantenimiento; las builds oficiales varían por dispositivo.
- **CalyxOS** cubre Pixel, Fairphone y algunos Motorola.

Los costes son reales: desbloquear borra el móvil, Play Integrity puede romper banca/Wallet y bajar
Netflix a SD, algunas operadoras pierden VoLTE/Wi-Fi calling, y tú te conviertes en el maintainer de
los parches. En Samsung, desbloquear dispara Knox para siempre. Por eso la skill se queda en la ROM
de fábrica: quita la superficie de anuncios y telemetría que la mayoría nota, sin esos costes. No es
un sistema endurecido ni sustituye a GrapheneOS en un Pixel.

## FAQ

**¿Anula la garantía?**
El debloat es configuración de software, no modificación de hardware, y es reversible. En la UE no
anula automáticamente la garantía legal, pero un servicio técnico puede negarse a tocar software
modificado. La skill no desbloquea el bootloader.

**¿Puedo dejar el móvil frito?**
Desactivar un paquete core equivocado puede provocar un bootloop. Por eso el CLI rechaza la lista
protegida, comprueba roles, hace backup y verifica por lotes. `restore` deshace exactamente lo que
desactivó la herramienta; si se pierde el journal, `restore --from-backup` reconstruye el cambio
desde el backup. La recuperación completa, incluido el modo seguro, está en
[docs/RESTORE.md](docs/RESTORE.md).

**¿Quita los anuncios de YouTube?**
No. Un resolver con bloqueo sobre DNS privado bloquea muchos anuncios y trackers dentro de apps, pero YouTube sirve los anuncios
desde el mismo dominio que el vídeo. La skill no instala apps parcheadas.

**¿Funciona en un móvil de empresa?**
No. Si `dumpsys device_policy` muestra un device owner o profile owner, o `pm list users` muestra más
de un usuario, la skill se para.

**¿Funciona en Samsung/Xiaomi/Huawei?**
El método funciona en cualquier Android 8+. Los nombres de paquetes y la lista segura cambian. Usa un
perfil de tu modelo exacto, o deja que el agente clasifique a mano y pregunte antes de cada paquete.
En Huawei/Honor sin servicios de Google, muchos paquetes `com.google.*` no existen.

**¿Hace falta Python?**
No. La skill incluye los comandos `adb` en crudo. El CLI es una protección y una comodidad; usa solo
la librería estándar y no tiene dependencias. La app de Windows incluye el CLI y no necesita Python.

**¿Hay una app?**
Sí, una app opcional de Windows en [cleanyourphone-app](https://github.com/jparedesDS/cleanyourphone-app).
Es una Early MVP, no está firmada y solo continúa con un perfil conocido. La skill sigue siendo el
camino para cualquier otro móvil.

**¿Cómo pido un perfil o mando feedback?**
Usa el [formulario web](https://cleanyourphone.org/es.html#feedback), **Feedback**
en la app, o `scripts/feedback.py` desde la skill. Es opt-in, enseña el payload y excluye serie, IP,
IMEI y MAC. Ver [docs/FEEDBACK.md](docs/FEEDBACK.md).

## Contribuir

- Un perfil probado (`device`) de un modelo nuevo: PR con `profiles/<marca>/<modelo>.json` y los
  detalles de la prueba.
- Un perfil `documented`: usa `scripts/dump_inventory.py`, cita el dump primario en `sources` y deja
  `disable` vacío.
- Un guard, parser o arreglo del CLI: añade un test en `tests/`.
- Un cambio de regla de seguridad: abre un issue primero. Esas reglas son el producto.
- Un móvil que no puedes probar: envía una [petición de perfil](https://cleanyourphone.org/es.html#feedback)
  con modelo, Android, build y fingerprint. Sin número de serie ni IP.
- Cambios de marca o logotipo: lee [docs/BRAND.md](docs/BRAND.md) antes de tocar los assets.
- Lee [AGENTS.md](AGENTS.md) antes de cambiar el repo.

## Licencia

MIT. Ver [LICENSE](LICENSE).
