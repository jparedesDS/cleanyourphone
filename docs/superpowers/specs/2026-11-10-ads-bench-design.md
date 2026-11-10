# Ads and proof: design

Date: 2026-11-10

## Goal

Add the two useful ideas from the external `alok722/cleanyourphone` review without copying its unsafe
parts: a first-class Private DNS ad-block flow and a reproducible before/after benchmark. Both ship in
the CLI/skill first and then in the Windows app.

## Why

CleanYourPhone already has `dns set` and a `report`, but they are hard to discover and not comparable.
The external project makes ads and measurements part of the main story. We can do the same with more
honest claims: DNS blocks many in-app ads but not YouTube; measurements are approximate and device-local,
not a guarantee.

## Goals

1. `dns providers` lists four presets and `dns set <preset|hostname>` accepts them.
2. `dns check` verifies an ad domain is blocked and a control domain still resolves.
3. `docs/ADS.md` documents the presets, OEM ad switches and limits.
4. `bench snapshot --label before|after` saves a comparable local JSON.
5. `bench compare BEFORE AFTER` prints a table and writes a Markdown comparison.
6. The app offers an optional ad-block choice on Review and shows the DNS check result.
7. The app takes a before snapshot when Apply starts and an after snapshot when it finishes, then shows
   the comparison on Done. A bench failure never blocks the debloat.
8. CLI version `0.3.0`; app sidecar pinned to `v0.3.0`; app version stays `0.1.0` until the first
   public app release.

## Non-goals

- Uninstall, suspend or any fallback that removes packages. The only write remains
  `pm disable-user --user 0`.
- “60% more RAM”, “2x faster” or any headline performance guarantee.
- App-start and jank benchmarks in the first pass; they are noisy and device-specific.
- Unused-app detection (`usage`) and animation/refresh tuning (`tune`); deferred.
- A public app release before a real supported phone test.

## Constraints

- No root, no ROM, no Shizuku, no uninstall.
- No telemetry, account or cloud.
- The CLI remains stdlib-only and Python 3.10+.
- The app remains Windows 10/11 x64, Python 3.12, PySide6.
- DNS changes are journaled and `restore` puts them back.
- Bench data is local, contains model/build but never serial, IMEI, IP or account data.
- Bench reports say “measured on this phone, approximate” and do not claim causality.

## CLI: ads

Add to `tools/extra.py`:

```python
DNS_PROVIDERS = {
    "adguard": ("dns.adguard-dns.com", "AdGuard DNS: ads and trackers"),
    "adguard-family": ("family.adguard-dns.com", "AdGuard Family: ads, trackers and adult sites"),
    "controld": ("p2.freedns.controld.com", "Control D free: ads and trackers"),
    "mullvad": ("adblock.dns.mullvad.net", "Mullvad DNS: ads and trackers"),
}
```

Commands:

- `cleanyourphone dns providers` — text table or `--json`.
- `cleanyourphone dns set adguard` — resolves the preset; a raw hostname still works.
- `cleanyourphone dns check` — sends `ping -c 1 -W 3 doubleclick.net` and
  `ping -c 1 -W 3 wikipedia.org` through `adb.shell`. `ad_blocked` is true when the ad host does not
  resolve or resolves to `0.0.0.0`/`::`; `online` is true when the control host resolves.
- `dns check --json` returns:
  ```json
  {
    "ad_domain": "doubleclick.net",
    "ad_ip": "",
    "ad_blocked": true,
    "control_domain": "wikipedia.org",
    "control_ip": "208.80.154.224",
    "online": true
  }
  ```
- `dns check` exits 0 only when `ad_blocked` and `online`; otherwise 1 with a warning.

`docs/ADS.md` covers the four presets, the YouTube limitation, VPN/router conflicts, and the OEM ad
switch checklist (Samsung One UI, Xiaomi/HyperOS, realme/OPPO, generic Android). The checklist is
manual: the CLI does not tap through Settings.

## CLI: bench

Add `tools/bench.py` with:

```python
BENCH_DIR = Path(os.environ.get("CLEANYOURPHONE_BENCH", adb.STATE_DIR / "bench"))
def measure(serial: str) -> dict
def save(data: dict, label: str) -> Path
def load(path: Path) -> dict
def compare(before: dict, after: dict) -> list[dict]
def write_markdown(before: dict, after: dict, rows: list[dict]) -> Path
```

Metrics:

- `model`, `android`, `build`
- `ram_available_mb` (`/proc/meminfo` `MemAvailable`)
- `swap_used_mb` (`SwapTotal - SwapFree`)
- `processes` (`ps -A -o NAME` line count minus header)
- `packages_installed`, `packages_enabled`, `packages_disabled`, `packages_system`, `packages_user`
- `animation_window`, `animation_transition`, `animation_duration` (global settings, default 1.0)
- `peak_refresh_rate` (system setting, default 60)
- `private_dns_mode`, `private_dns_specifier`
- `battery_saver` (global `low_power == "1"`)

Commands:

- `cleanyourphone bench snapshot [--label before|after]` — saves
  `~/.cleanyourphone/bench/<timestamp>_<label>.json`, prints the path; `--json` prints the data.
- `cleanyourphone bench compare BEFORE AFTER` — prints a metric/before/after/change table, writes
  `~/.cleanyourphone/bench/compare-<timestamp>.md`, and prints the path; `--json` returns the rows.
- `cleanyourphone bench list` — lists snapshots, newest first.

Comparison rows show absolute values and a signed percentage/absolute delta. No “better/worse” labels
for ambiguous metrics like refresh rate; the report says what changed, not that it is universally good.

## App: ads

- `CliClient` adds `dns_providers()`, `dns_status()`, `dns_set(provider)`, `dns_off()`, `dns_check()`.
- Review page gains an optional collapsed card: **“Bloquear anuncios (opcional)”**.
  - Checkbox default off.
  - Provider combo, default AdGuard.
  - Caveat: “Bloquea muchos anuncios y trackers. No bloquea los anuncios de YouTube.”
- Apply page applies the package batches first, then, if selected, `dns set <provider>` and
  `dns check`. A DNS failure is shown but does not undo the package changes.
- Done page shows `Anuncios: AdGuard DNS · bloqueo activo` or the DNS error.

## App: proof

- Apply page takes `bench snapshot --label before` before the first batch, after the backup and review.
- After the last batch, it takes `bench snapshot --label after` and `bench compare`; both paths and the
  rows go into `ApplyResult`.
- Done page shows a **Resultados** card: free RAM before/after, enabled packages before/after,
  processes before/after, and Private DNS. It says “Medido en este móvil; aproximado, no causal.”
- A bench failure sets `bench_error` and the debloat continues; the card says “No se pudo medir”.
- Sidecar pinned to CLI `v0.3.0`; app version remains `0.1.0`.

## Release

- CLI `0.3.0`: changelog, tag, GitHub release, PyPI, website `softwareVersion` `0.3.0` and CSP hash.
- App: sidecar `v0.3.0`, rebuild installer, tests; public app release still waits for a real phone test.
- README/SKILL/CLI: add “Block ads” and “Measure” sections with exact commands and caveats.

## Risks

- `ping` may be blocked by the network or return a different format; `dns check` must report “cannot
  test” rather than claiming blocked.
- Private DNS providers can be unavailable or blocked by a router/VPN; the user must be able to turn it
  off and restore the previous state.
- Bench values vary with background apps, charging, battery saver and time since boot. The report must
  say so; no cross-phone comparisons.
- CLI 0.3.0 changes the app sidecar pin; the app build must be rebuilt and smoke-tested.
- The app release still needs a real supported phone.

## What is left to the builder

- Exact wording/layout of the app ads card and results card.
- Exact Markdown template and rounding in `bench compare`.
- The OEM checklist wording in `docs/ADS.md`.
- The release notes for CLI 0.3.0 and the app rebuild.
