# El prompt (español)

Pega esto en Claude Code, Codex, Cursor, Gemini CLI, OpenCode o cualquier agente de código con
acceso a shell, en un ordenador conectado al móvil por USB. Funciona en móviles y tablets Android
(Android 8 o superior). **No** funciona en iPhone, en Android TV ni en un móvil gestionado por una
empresa.

Antes de empezar, en el móvil: Ajustes → Acerca del teléfono → toca **Número de compilación** 7
veces → atrás → **Opciones de desarrollador** → activa **Depuración USB**. Conecta el móvil por USB y
acepta el aviso **¿Permitir depuración USB?**. Mantén el móvil desbloqueado y con más del 30% de
batería.

Si has clonado el repo, dilo: el agente puede usar `tools/phone.py`, `profiles/` y `docs/` en vez de
inventarse los comandos. El `SKILL.md` está en inglés, pero el agente debe contestarte en español.

[English version](PROMPT.md)

---

Quiero limpiar mi móvil Android: desactivar apps preinstaladas, anuncios y telemetría, y mejorar la
batería, sin root y sin desinstalar nada. Mi móvil es: **<MODELO AQUÍ>**.

Lee `SKILL.md` de este repo y síguelo al pie de la letra. Si no puedes leerlo, para y pídeme que te
lo pegue; no improvises. Trabaja sobre el móvil real, paso a paso, y enséñame el plan antes de
cambiar nada.

Lo no negociable:

- **Desactivar, nunca desinstalar.** Solo `pm disable-user --user 0`, un paquete por llamada de
  shell. Nada de `pm uninstall`, `pm hide`, `pm clear`, root, ROM ni restablecimiento de fábrica.
- **Backup primero.** Ejecuta `python tools/phone.py backup` antes del primer cambio. Dime dónde
  está.
- **Nunca desactives un paquete protegido.** La lista está en `tools/protected.py` y en
  `docs/SAFETY.md`. Si un paquete está ahí, recházalo. Sin excepciones.
- **No me dejes sin teléfono, SMS, Home ni teclado.** Comprueba qué app tiene cada rol antes de
  desactivar, y vuelve a comprobarlo después de cada lote.
- **Pregúntame antes de tocar nada que use**: banca, pagos, WhatsApp, cámara, galería, alarma, VPN,
  gestor de contraseñas, autenticador, smartwatch, eSIM, VoLTE/Wi-Fi calling, hotspot,
  accesibilidad, apps de trabajo. Hazme un checklist y desactiva solo lo que no marque.
- **Lotes pequeños, verificar entre medias.** Como máximo 5 paquetes por lote, luego
  `python tools/phone.py verify`. Si algo falla, reactiva el lote y para.
- **Reiniciar una vez al final, esperar y verificar otra vez.** Algunos móviles reactivan paquetes
  al arrancar; anótalos en vez de pelearte con ellos.
- **Cerrar ADB al terminar.** Desactiva la depuración inalámbrica y la depuración USB, revoca las
  autorizaciones y confirma que `adb devices` ya no lista mi móvil.
- **Háblame en mi idioma.** Si te escribo en español, contéstame en español.

Empieza haciéndome las preguntas de la sección "First response" de `SKILL.md`, luego conéctate con
`adb devices -l` y ejecuta `python tools/phone.py doctor` y `python tools/phone.py probe`.

Al terminar, dame: la ruta del backup, la lista de paquetes que desactivaste y por qué, lo que
mantuviste y por qué, el estado del DNS, la línea base de batería si la medimos, y el comando exacto
para deshacerlo (`python tools/phone.py restore`).
