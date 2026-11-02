# CleanYourPhone brand

The name is **CleanYourPhone**. Do not rename it, translate it or change its capitalization.

## Idea

**Control with a way back.**

CleanYourPhone is not a cleaner app and not a battery miracle. It is an open, conservative tool
for disabling Android bloatware with evidence, approval and restoration. Cleaning means less noise,
never irreversible deletion.

| Element | Definition |
|---|---|
| Positioning | The reversible Android debloat skill and CLI that lets a person and their agent disable only what they approve, without root or uninstalling, with a backup, verification and a recorded restore path. |
| Audience | Technical or curious Android users who want to keep their stock ROM and stay in control; coding agents that need an explicit, safe procedure. |
| Promise | Review before changing, record every change, and always keep a way back. |
| Tagline | **Your phone, minus the bloat.** / **Tu móvil, sin lo que sobra.** |
| Character | "Safe by design. Boring on purpose." The brand should feel as disciplined as the product rules. |

## Attributes

1. **Reversible.** Every action and every message keeps the return path visible.
2. **Precise.** Contained geometry, exact language, no decorative noise.
3. **Evidence-first.** Profiles, plans, records and verification before promises.
4. **Calm and conservative.** No urgency, alarmism, "turbo" aesthetics or hype.
5. **Open and human.** Open source, limits explained, the person always in control.

## Voice

- Direct, concrete and technically competent, but understandable.
- Use **disable, review, verify, record, restore**. Avoid *destroy, purge, magically optimize* or
  *accelerate to the max*.
- Explain what the product does **not** do. Limits build trust.
- Short sentences and checkable facts. No fear, superlatives or battery miracles.

| Avoid | Use |
|---|---|
| "One command undoes everything." | "`restore` re-enables exactly what the CLI recorded." |
| "Your banking apps stay." | "Nothing user-facing is disabled without your approval." |
| "Completely safe." | "Guardrailed and reversible; you still review the plan." |
| "Make the phone yours again." | "Review the plan. Keep the undo." |
| "Double your battery." | "Measure it; the gain may be small or zero." |

## Color

| Color | Role |
|---|---|
| Graphite `#0F0D14` | Primary background, icon tile, one-color mark on light surfaces. |
| Purple `#A78BFA` | Phone, return gesture, primary actions, links, commands and the `Phone` wordmark. |
| Light purple `#C4B5FD` | Only `ASK` and warning states; a tint, never a second brand color. |
| Text `#F5F3FA` | Headlines and the `CleanYour` wordmark on graphite. |
| Muted `#B8B2C4` | Secondary text; never part of the essential symbol. |

Purple and white/graphite are the brand colors. The light purple is only a functional tint for `ASK`.

## Typography

- **Sans:** `Aptos`, `Segoe UI`, `system-ui`, `-apple-system`, `BlinkMacSystemFont`, sans-serif.
  Weights 700-800 for headlines and wordmark; 400-600 for body.
- **Mono:** `Cascadia Code`, `SFMono-Regular`, `Consolas`, `Liberation Mono`, monospace, for commands,
  package names, states and evidence.
- The wordmark is always **CleanYourPhone**, with no spaces or alternate capitalization. In the color
  version, **CleanYour** uses the text color and **Phone** uses the logo purple `#A78BFA`; the
  monochrome lockup stays one color.

## Logo

The final mark is **Contained return**: an intact phone outline with a single undo arrow inside. The
closed phone communicates device integrity; the arrow communicates restore, not deletion. The sparkle
from the previous mark is retired because it reads as generic "magic cleaner".

### Assets

| File | Use |
|---|---|
| `assets/logo.svg` | Primary app-icon tile, 64×64, dark background. |
| `assets/favicon.svg` | Simplified 32×32 favicon. |
| `assets/logo-mark.svg` | Mark-only, transparent, purple/white. |
| `assets/logo-mono.svg` | One-color mark for light backgrounds. |
| `assets/logo-lockup.svg` | Horizontal mark + wordmark for dark backgrounds. |
| `assets/logo-lockup-mono.svg` | Horizontal mark + wordmark for light backgrounds. |

The same files exist in `cleanyourphone-web/assets/` for the website.

### Clear space and minimum sizes

- Keep at least **8 units of the 64-unit viewBox** around the symbol.
- Full symbol: minimum **24 px** (8 mm in print).
- Simplified favicon: minimum **16 px**.
- Horizontal lockup: minimum **180 px** wide.

### Color use

- Dark backgrounds: primary tile or the purple/white mark.
- Light backgrounds: the monochrome `#0F0D14` mark or mono lockup. Do not put the purple/white mark on
  white or busy imagery.
- Do not use color as the only state indicator in UI; pair it with a label.

### Don'ts

1. Do not rotate, mirror or reverse the arrow.
2. Do not add sparkles, brooms, shields, locks, checks or text lines inside the phone.
3. Do not apply gradients, glows, shadows, bevels, filters or neon effects to the mark.
4. Do not stretch, crop or rebuild the phone and return proportions.
5. Do not change the color roles or place the color mark on light or noisy backgrounds.

## Application

- **Website header:** `assets/logo.svg` at 32 px, with "CleanYourPhone" as HTML text. Do not use the
  full lockup there; it would duplicate the name.
- **Footer:** the same tile at 26 px.
- **Favicon:** `assets/favicon.svg`; check it in light and dark browser tabs.
- **README banner:** graphite background, large lockup, tagline and plenty of negative space. Export PNG
  at high resolution and keep both repositories in sync.
- **Social preview:** 1280×640 with the lockup and tagline as the main hierarchy. No mockups,
  sparkles or small print; the symbol must survive the thumbnail.
- **Release notes:** start with the user-facing change, then the technical detail.
