<p align="center">
  <a href="https://jparedesds.github.io/cleanyourphone-web/es.html">
    <img src="assets/banner.png" alt="CleanYourPhone — tu móvil, sin lo que sobra" width="100%">
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

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml"><img src="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/license-MIT-64f4c4?labelColor=061014" alt="MIT">
  <img src="https://img.shields.io/badge/python-3.10%2B-64f4c4?labelColor=061014" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/telemetry-none-64f4c4?labelColor=061014" alt="Sin telemetría">
  <img src="https://img.shields.io/badge/profiles-157-5ec8ff?labelColor=061014" alt="157 perfiles">
  <a href="https://github.com/jparedesDS/cleanyourphone/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone?color=64f4c4&labelColor=061014" alt="release"></a>
</p>

# CleanYourPhone

**Tu móvil, sin lo que sobra.** Una skill de código abierto y reversible para limpiar Android,
pensada para agentes. Desactiva apps y servicios preinstalados por ADB: sin root, sin ROM cocinada,
sin desinstalar nada y con un comando para deshacer todos los cambios.

La historia y el modelo de seguridad, en
**[jparedesds.github.io/cleanyourphone-web/es.html](https://jparedesds.github.io/cleanyourphone-web/es.html)**.

Es la versión móvil de [cleanyour.tv](https://cleanyour.tv), con la misma idea: un prompt, un comando,
reversible, open source y la persona siempre al mando.

[SKILL.md](SKILL.md) · [PROMPT.es.md](PROMPT.es.md) · [Seguridad](docs/SAFETY.md) · [157 perfiles](docs/PROFILES.md) · [Cambios](CHANGELOG.md)

<p align="center">
  <img src="assets/demo.gif" alt="Antes y después: WhatsApp, el banco y tus apps se quedan; Samsung Free, TV Plus, Bixby, Tips, Themes, Games y Cloud desaparecen" width="520">
</p>

## Empieza aquí

| Tienes | Empieza por |
|---|---|
| Un móvil y un agente de código | El inicio rápido de abajo. |
| Ganas de verlo primero | [La web](https://jparedesds.github.io/cleanyourphone-web/es.html). |
| Dudas de seguridad | [docs/SAFETY.md](docs/SAFETY.md). |
| Un modelo concreto | [Los 157 perfiles](docs/PROFILES.md). |

---

## Por qué una skill y no una app

Una app que desactiva otras apps necesita root, Shizuku o permisos de device-owner. Es mucho poder y
mucho riesgo para algo que un comando de shell ya hace. Una skill es solo texto: el agente de la
persona la lee, ejecuta `adb`, enseña un plan y pregunta antes de tocar nada. No hay nada instalado
en el móvil, nada corriendo en segundo plano y nada que mande datos a ningún sitio.

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

### 3. Clona y comprueba

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

El CLI es opcional. `SKILL.md` incluye también los comandos `adb` en crudo, así que un agente puede
trabajar sin Python. El CLI está para que el agente no se invente las protecciones.

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
`SKILL.md` y mantén el repo clonado para que el CLI esté disponible:

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
- Opcionalmente configura DNS privado (`dns.adguard-dns.com`, NextDNS o tu propio resolver).
- Genera un informe: qué cambió, por qué, qué se mantuvo, dónde está el backup y el comando de undo.
- Mide una línea base de batería antes/después (`docs/BATTERY.md`), sin prometer milagros.

## Qué no hace

- **No es una app.** No se instala nada en el móvil.
- **No root, no Magisk, no hace falta Shizuku.**
- **No ROM, no desbloqueo de bootloader, no flasheo.**
- **No desinstala.** `pm disable-user` es reversible; `pm uninstall` no.
- **No toca perfiles de trabajo ni MDM.** Si el móvil está gestionado, se para.
- **No bloquea anuncios de YouTube.** El DNS privado no toca anuncios del mismo dominio.
  `docs/FAQ.md` lo explica.
- **No promete "el doble de batería".** La ganancia realista en standby por debloat es 0–10%; lo que
  más ahorra es restringir fondo, bajar brillo/refresco y el DNS.
- **El CLI no necesita nube.** Es local; aun así, un agente alojado recibe la sesión (modelo, paquetes,
  fingerprint). Si eso importa, usa un modelo local o redacta esos datos.

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

El catálogo completo, modelo a modelo, está en [docs/PROFILES.md](docs/PROFILES.md).

| Marca | Perfiles | Probados en móvil | Tablets |
|---|---|---|---|
| **Google** | 5 | 1 | 0 |
| **Samsung** | 55 | 1 | 7 |
| **Xiaomi** | 15 | 1 | 2 |
| **Redmi** | 57 | 0 | 2 |
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
protegida, comprueba roles, hace backup y verifica por lotes. La recuperación está en
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
la librería estándar y no tiene dependencias.

## Contribuir

- Un perfil probado (`device`) de un modelo nuevo: PR con `profiles/<marca>/<modelo>.json` y los
  detalles de la prueba.
- Un perfil `documented`: usa `scripts/dump_inventory.py`, cita el dump primario en `sources` y deja
  `disable` vacío.
- Un guard, parser o arreglo del CLI: añade un test en `tests/`.
- Un cambio de regla de seguridad: abre un issue primero. Esas reglas son el producto.
- Lee [AGENTS.md](AGENTS.md) antes de cambiar el repo.

## Licencia

MIT. Ver [LICENSE](LICENSE).
