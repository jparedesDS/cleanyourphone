# The open-source OS question

Yes, open-source Android ROMs exist and work. No, installing one is not the first thing to do, and it
is not part of this skill. This page explains the real options and the real costs so you can give an
honest recommendation.

## The short version

| If the person... | Recommend |
|---|---|
| Has a Pixel 6–10 and cares about privacy/security | **GrapheneOS** |
| Has a supported non-Pixel and wants an easy install | **/e/OS** (check the device list first) |
| Is technical, has a supported device, wants control | **LineageOS** (official build) |
| Uses banking, Google Wallet, Netflix HD, a work profile or a carrier that needs VoLTE | **Stay on stock**, debloat + Private DNS |
| Has a Samsung | **Stay on stock**; unlocking Knox is permanent |
| Has a Huawei/Honor without Google services | Stay on stock; the ROM scene is device-specific and often closed |

A stock ROM with a careful debloat plus Private DNS removes much of the ad and telemetry surface for
many people, without the bootloader, Play Integrity and update-maintenance costs. It is not a
measurable percentage and it is not a hardened OS. A ROM is for someone who accepts the trade-offs
below.

## GrapheneOS

- **Devices:** Pixel 6, 6 Pro, 6a, 7, 7 Pro, 7a, 8, 8 Pro, 8a, 9, 9 Pro, 9 Pro XL, 9 Pro Fold, 9a,
  10, 10 Pro, 10 Pro XL, 10 Pro Fold, 10a, Pixel Fold, Pixel Tablet (as of October 2026).
- **What it is:** a hardened Android with sandboxed Google Play Services (optional), a locked
  bootloader, verified boot, per-app network/sensors toggles and fast security updates.
- **Why it is the best fit for "privacy + battery + no ads":** no OEM telemetry, no preloads, no
  always-on ad services, and Play Services only if you install them.
- **Costs:** Pixel-only; bootloader unlock wipes the phone; some banking apps and Google Wallet may
  refuse to work even with sandboxed Play Services; Netflix may drop to SD; some carrier features
  (VoLTE/Wi-Fi calling) depend on the carrier.
- **Not a magic battery upgrade:** standby is usually good, but measure it. The win is fewer
  background services, not a different kernel.

## /e/OS

- **Devices:** a broad list of supported phones, plus Murena phones sold with it preinstalled. Check
  the official device list for the exact model and build.
- **What it is:** a de-Googled Android with microG (an open implementation of the Google APIs) and
  the /e/ app store. The web installer is the easiest of the bunch.
- **Costs:** microG is not Play Services; some apps that depend on Play Integrity, push or Google
  login will fail or need workarounds. Camera quality and carrier features vary. Security patches
  depend on the maintainer.
- **Best for:** a non-Pixel phone where the person wants a guided install and accepts that a few
  apps will not work.

## LineageOS

- **Devices:** a large list, but "official" and "unofficial" builds are very different. An unofficial
  build may be maintained by one person and stop receiving patches.
- **What it is:** a clean Android without Google services by default. You can add Google apps or
  microG yourself.
- **Costs:** you are the maintainer of updates; Play Integrity fails without workarounds; banking,
  Wallet, Netflix HD and some games may break; VoLTE/Wi-Fi calling is carrier- and device-specific.
- **Best for:** a technical person with a well-supported device who does not need the Google/Banking
  stack on that phone.

## CalyxOS

- **Devices:** Pixel, Fairphone and some Motorola models; check the current list.
- **What it is:** a privacy-focused Android with microG optional and a friendly installer.
- **Costs:** same Play Integrity/banking trade-offs as the others; device support is narrower than
  LineageOS.

## postmarketOS and Ubuntu Touch

- **What they are:** Linux-based mobile systems, not Android. Great for experimentation, not a daily
  driver for most people: app compatibility, camera, calls, battery and carrier features are limited.
- **Best for:** a spare device, not someone's only phone.

## The costs nobody mentions

### Bootloader unlock wipes the phone

There is no "install a ROM and keep your data" path on a locked bootloader. The person needs a full
backup, and some apps (banking, authenticators) will need to be set up again.

### Play Integrity

Banking apps, Google Wallet, some games, some work apps and Netflix use Play Integrity. A custom ROM
usually fails `DEVICE` and `STRONG` integrity. There are community workarounds (Magisk modules,
PlayIntegrityFix, keyboxes), but they are an arms race, they are not something a product should
support, and they can break at any update. Do not promise them.

### VoLTE, Wi-Fi calling and RCS

Some carriers require the OEM's IMS configuration. A ROM may have calls over 2G/3G only, or no
Wi-Fi calling. Check the carrier and the device before recommending a ROM.

### Camera

The OEM camera pipeline (Samsung, Xiaomi, Pixel) is not fully available on AOSP ROMs. Photos may be
softer, video may lose stabilization, and some lenses may not work. On Pixel, the difference is
smaller; on Samsung/Xiaomi, it is noticeable.

### Security patches

A ROM is only as good as its maintainer. An abandoned build is worse than a stock ROM that still gets
monthly patches. Check the last update date before recommending one.

### Warranty and Knox

Unlocking the bootloader may affect the manufacturer's warranty and some DRM. On Samsung, it trips
the Knox e-fuse **permanently**: Samsung Wallet/Pay, Samsung Pass, Secure Folder and some work
features stop working, and a factory reset does not bring them back. Never recommend unlocking a
Samsung phone.

## How to check what a phone can do

```bash
adb shell getprop ro.product.model
adb shell getprop ro.product.device
adb shell getprop ro.build.version.release
adb shell getprop ro.boot.flash.locked      # 1 = locked, 0 = unlocked
adb shell getprop ro.boot.verifiedbootstate # green = verified, orange/yellow = modified
```

Then check the ROM's official device list for that exact codename. "Same marketing name" is not
enough: carrier variants and regional models often have different codenames and different support.

## What this skill does about ROMs

Nothing. It does not unlock, flash, root or install a ROM. It can tell the person what their phone
is, whether the bootloader is locked, and whether a ROM is a realistic option. The rest is a separate
decision with a separate backup.

## A useful product idea

Instead of shipping a ROM, ship a **compatibility checker**: the person enters their model, the page
says "stock + debloat", "GrapheneOS", "/e/OS", "LineageOS (official)" or "not worth it", and explains
the trade-offs in plain language. That is honest, low-risk, and more useful than a download button.
