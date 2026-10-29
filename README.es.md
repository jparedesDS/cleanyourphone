# CleanYourPhone

**Tu móvil, sin la morralla.**

CleanYourPhone es una **skill para agentes de código** (Claude Code, Codex, Cursor, Gemini CLI,
OpenCode y similares) que limpia un Android por ADB. Sin app que instalar, sin root, sin ROM cocinada
y sin desinstalar nada. Desactiva apps y servicios preinstalados, opcionalmente configura un DNS
privado, verifica el teléfono y puede deshacer todos los cambios con un comando.

Es la versión móvil de [cleanyour.tv](https://cleanyour.tv), con la misma idea: un prompt, un comando,
reversible, open source y la persona siempre al mando.

[Read in English](README.md)

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
git clone https://github.com/<tu-usuario>/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

El CLI es opcional. `SKILL.md` incluye también los comandos `adb` en crudo, así que un agente puede
trabajar sin Python. El CLI está para que el agente no se invente las protecciones.

### 4. Pásale la skill a tu agente

| Agente | Dónde ponerla |
|---|---|
| **Claude Code** | `~/.claude/skills/clean-your-phone/SKILL.md` (personal) o `.claude/skills/clean-your-phone/SKILL.md` (proyecto) |
| **OpenCode** | `~/.config/opencode/skills/clean-your-phone/SKILL.md` (global) o `.opencode/skills/clean-your-phone/SKILL.md` (proyecto) |
| **Codex** | `AGENTS.md` en el proyecto, o `~/.codex/AGENTS.md`; pega `PROMPT.md` si tu versión no carga skills |
| **Cursor** | `.cursor/rules/clean-your-phone.mdc` con el contenido de `SKILL.md` |
| **Gemini CLI** | `GEMINI.md` en el proyecto |
| **Cualquier chat** | Pega `PROMPT.md` y, cuando lo pida, pega `SKILL.md` |

Lo más sencillo es clonar el repo y abrir el agente en esa carpeta: `SKILL.md` ya está en la raíz y
`python tools/phone.py` funciona. Si tu agente carga skills desde una carpeta global, copia ahí
`SKILL.md` y mantén el repo clonado para que el CLI esté disponible:

```bash
mkdir -p ~/.claude/skills/clean-your-phone
cp SKILL.md ~/.claude/skills/clean-your-phone/SKILL.md
```

Sin el repo, la skill también funciona: incluye los comandos `adb` en crudo y le dice al agente que
los use. También tienes el prompt en español en [PROMPT.es.md](PROMPT.es.md).

Luego pide: **"Limpia mi móvil"** o **"Usa clean-your-phone en mi Pixel"**.

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
en un build incluido en `tested`.

| Perfil | Modelo | Android | Verificación |
|---|---|---|---|
| [`google-pixel-8`](profiles/google/pixel-8.json) | Pixel 8 (shiba) | 14–16 | device, build Android 16 probado |
| [`google-pixel-7a`](profiles/google/pixel-7a.json) | Pixel 7a (lynx) | 13 | documented, solo preguntar |
| [`google-pixel-6`](profiles/google/pixel-6.json) | Pixel 6 (oriole) | 12 | documented, solo preguntar |
| [`google-pixel-6-pro`](profiles/google/pixel-6-pro.json) | Pixel 6 Pro (raven) | 12 | documented, solo preguntar |
| [`samsung-sm-s918b`](profiles/samsung/sm-s918b.json) | Galaxy S23 Ultra (SM-S918B) | 13–16 | device, build Android 14 probado |
| [`samsung-sm-s938b`](profiles/samsung/sm-s938b.json) | Galaxy S25 Ultra (SM-S938B) | 16 | documented, solo preguntar |
| [`samsung-sm-a546e`](profiles/samsung/sm-a546e.json) | Galaxy A54 5G (SM-A546E) | 13 | documented, solo preguntar |
| [`oneplus-a6013`](profiles/oneplus/oneplus-a6013.json) | OnePlus 6T (ONEPLUS A6013) | 11 | device, build OxygenOS 11.1.2.2 probado |
| [`oneplus-cph2487`](profiles/oneplus/oneplus-cph2487.json) | OnePlus 11R 5G (CPH2487) | 16 | documented, solo preguntar |
| [`oneplus-cph2719`](profiles/oneplus/oneplus-cph2719.json) | OnePlus Nord CE5 (CPH2719) | 16 | documented, solo preguntar |
| [`xiaomi-15t`](profiles/xiaomi/xiaomi-15t.json) | Xiaomi 15T (25069PTEBG) | 16 | documented, solo preguntar |
| [`redmi-note-15-pro`](profiles/redmi/redmi-note-15-pro.json) | Redmi Note 15 Pro (`lapis`) | 16 | documented, solo preguntar |
| [`poco-f6`](profiles/poco/poco-f6.json) | POCO F6 (24069PC21G) | 16 | documented, solo preguntar |
| [`xiaomi-hyperos`](profiles/xiaomi/hyperos.json) | Xiaomi/Redmi/POCO, HyperOS | 14–16 | device, perfil de familia, sin auto-apply |
| [`generic-android`](profiles/generic/android.json) | Cualquier Android 8+ | 8+ | reference, sin auto-apply |

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
