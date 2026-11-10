# Ads and Private DNS

CleanYourPhone can point Android's Private DNS at a resolver that blocks many ad and tracker domains.
It is not a full ad blocker: it works at DNS level and has no access to traffic inside an app.

## What it does

- Blocks many in-app and browser ads whose domains are on the resolver's blocklist.
- Reduces some background network requests and wakeups.
- Is journaled: `restore` puts the previous Private DNS mode and specifier back.
- Is optional and off by default.

## What it does not do

- **It does not block YouTube ads.** YouTube serves the video and the ad from the same domain.
- It is not a VPN and does not hide your IP or encrypt traffic.
- It does not stop an app from using data it already collected.
- It does not replace a browser content blocker.
- It can break captive portals, some banking apps or a work network. Test and undo if needed.

## Presets

| Preset | Hostname | Notes |
|---|---|---|
| `adguard` | `dns.adguard-dns.com` | Ads and trackers |
| `adguard-family` | `family.adguard-dns.com` | Ads, trackers and adult sites |
| `controld` | `p2.freedns.controld.com` | Control D free resolver |
| `mullvad` | `adblock.dns.mullvad.net` | Mullvad ad-blocking DNS |

List them with:

```bash
python tools/phone.py dns providers
```

Set one:

```bash
python tools/phone.py dns set adguard
```

A raw hostname still works:

```bash
python tools/phone.py dns set dns.nextdns.io
```

Do not overwrite a resolver that is already doing the job. A router-level Pi-hole, AdGuard Home,
NextDNS or a VPN may be a better fit. Private DNS bypasses the router's DNS, so its rules stop
applying.

## Check it

```bash
python tools/phone.py dns check
```

The command resolves `doubleclick.net` and `wikipedia.org` from the phone. `ad_blocked` is true when
the ad domain does not resolve or resolves to a sinkhole (`0.0.0.0`, `::`, `127.0.0.1`, `::1`). If
`wikipedia.org` does not resolve, the result is “cannot test” because the phone is offline; it is not
proof that ads are blocked. A real ad IP with no ping reply is also not proof of blocking.

The raw ADB check is:

```bash
adb shell ping -c 1 -W 3 doubleclick.net
adb shell ping -c 1 -W 3 wikipedia.org
```

## Undo

```bash
python tools/phone.py dns off
python tools/phone.py restore
```

`dns off` returns to `opportunistic`; `restore` puts back the exact mode and specifier recorded before
the first change.

## OEM ad switches

These are manual settings, not ADB changes. The names vary by version; use the search box in Settings
if a path is not exact.

### Samsung One UI

- Settings → Security and privacy → More privacy settings → Customization Service: off.
- Settings → Privacy → Send diagnostic data: off.
- Galaxy Store → Menu → Settings → Marketing notifications: off.

### Xiaomi / Redmi / POCO (MIUI/HyperOS)

- Settings → Passwords & security → Authorization & revocation → `msa`: revoke.
- Settings → Privacy protection → Ads → Personalized ad recommendations: off.
- Security, Cleaner, File Manager, Music, Themes and Downloads → Settings → Receive recommendations:
  off.
- Settings → Additional settings → Privacy → User Experience Program: off.

### realme / OPPO (realme UI / ColorOS)

- Lock screen → Glance / Lock screen magazine: off (if still installed).
- Settings → Additional settings → Privacy → Get recommendations / Personalised recommendations: off.
- App Market → Settings → Push notifications and recommendations: off.
- Phone Manager / Security → Settings → Get recommendations: off.

### Generic Android

- Settings → Google → Ads → Delete advertising ID.
- Turn off personalization in the apps that show “recommended” rows.

## See also

- [CLI](CLI.md)
- [FAQ](FAQ.md)
- [Battery](BATTERY.md)
