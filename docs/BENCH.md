# Benchmark

CleanYourPhone can record a local before/after snapshot of the phone. It is evidence for what changed,
not a promise that the phone will be faster.

## What it measures

- Available RAM and used swap.
- Process count.
- Installed, enabled, disabled, system and user package counts.
- Window, transition and animator animation scales.
- Peak refresh rate.
- Private DNS mode and specifier.
- Battery Saver state.

It does **not** store the serial, fingerprint, IMEI, IP, account, messages or app data. A custom
Private DNS hostname can contain a provider profile ID; use a preset hostname if that matters.

## Commands

Before the first change, after the backup:

```bash
python tools/phone.py bench snapshot --label before
```

After the reboot and verification:

```bash
python tools/phone.py bench snapshot --label after
python tools/phone.py bench list
python tools/phone.py bench compare <before.json> <after.json>
```

`bench compare` prints a table and writes a Markdown file under
`~/.cleanyourphone/bench/compare-<timestamp>.md`. `--json` returns `{"path": "...", "rows": [...]}`;
`bench snapshot --json` returns `{"path": "...", "data": {...}}`. `bench list` shows saved snapshots,
newest first. On Windows, use the paths printed by `bench snapshot` or `bench list`; `~` is not expanded
by PowerShell.

## Raw ADB fallback

The skill must work without the CLI. Capture the same fields manually:

```bash
adb shell cat /proc/meminfo
adb shell ps -A -o NAME
adb shell pm list packages -e
adb shell pm list packages -d
adb shell pm list packages -s
adb shell pm list packages -3
adb shell settings get global window_animation_scale
adb shell settings get global transition_animation_scale
adb shell settings get global animator_duration_scale
adb shell settings get system peak_refresh_rate
adb shell settings get global low_power
adb shell settings get global private_dns_mode
adb shell settings get global private_dns_specifier
```

Run the same commands after the change, under the same conditions.

## What the numbers mean

- **Available RAM** moves with background apps and cached processes. A higher value is not proof that
  apps are faster.
- **Process count** can fall after a reboot without any debloat.
- **Enabled package count** falls when packages are disabled; that is a direct count, not a performance
  claim.
- **Animation scales** lower means animations finish sooner. It does not make an app compute faster.
- **Peak refresh rate** affects smoothness and battery. Higher is not always better.
- **Private DNS** changing from `opportunistic` to `hostname` means a resolver is configured; run
  `dns check` to see whether ads are blocked.

## Conditions

Use the same phone, SIM, network, brightness, refresh setting, charging state and test window. Reboot
between snapshots if the debloat flow requires it. Do not compare different phones, different Android
versions or a run with Battery Saver on against one with it off.

The report says “measured on this phone; approximate; not causal”. Do not turn it into “60% more RAM”
or “2x faster”.
