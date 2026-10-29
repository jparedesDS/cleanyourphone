"""Packages that must never be disabled on an Android phone.

This module is the single source of truth for the hard denylist. `phone.py` refuses to disable a
package that matches it, and the tests assert the list. Do not add an override flag: a phone that
loses telephony, the permission controller or the package installer may not boot again.

The list is intentionally conservative. A package that is not here can still be dangerous; the
skill's role checks, backup requirement and "ask first" rule cover the rest.
"""

from __future__ import annotations

# Exact package names. The value is the reason shown to the user.
EXACT: dict[str, str] = {
    # Android framework and system UI
    "android": "Android framework",
    "com.android.systemui": "System UI: status bar, notifications, lock screen, navigation",
    "com.android.settings": "Android Settings",
    "com.android.shell": "ADB shell and system commands",
    "com.android.phone": "Telephony service: calls, mobile data, SIM",
    "com.android.server.telecom": "Telecom: call routing and in-call UI",
    "com.android.incallui": "In-call UI",
    "com.android.mms.service": "MMS service",
    "com.android.cellbroadcastreceiver": "Emergency alerts (cell broadcast)",
    "com.google.android.cellbroadcastreceiver": "Emergency alerts (cell broadcast)",
    "com.android.cellbroadcastservice": "Emergency alert service",
    "com.google.android.cellbroadcastservice": "Emergency alert service",
    "com.android.emergency": "Emergency information and emergency dialer",
    "com.android.ims": "IMS: VoLTE and Wi-Fi calling",
    "com.google.android.ims": "IMS: VoLTE, Wi-Fi calling and RCS",
    "com.android.carrierconfig": "Carrier configuration: APN, VoLTE, MMS",
    "com.android.carrierdefaultapp": "Carrier default app",
    "com.android.se": "Secure Element: eSIM and NFC payments",
    "com.android.nfc": "NFC: payments, transit, tags",
    "com.android.nfc_extras": "NFC secure-element extras",
    "com.android.keychain": "Certificate store: banking, VPN, enterprise Wi-Fi",
    "com.android.certinstaller": "Certificate installer",
    "com.android.vpndialogs": "VPN consent dialog",
    "com.android.documentsui": "System file picker used by other apps",
    "com.android.networkstack": "Network stack: Wi-Fi, mobile data, captive portals",
    "com.google.android.networkstack": "Network stack: Wi-Fi, mobile data, captive portals",
    "com.android.wifi": "Wi-Fi framework",
    "com.google.android.wifi": "Wi-Fi framework",
    "com.android.captiveportallogin": "Captive portal login",
    "com.android.connectivity.resources": "Connectivity resource overlay",

    # Package management and permissions
    "com.android.permissioncontroller": "Permission controller",
    "com.google.android.permissioncontroller": "Permission controller",
    "com.android.packageinstaller": "Package installer",
    "com.google.android.packageinstaller": "Package installer",
    "com.android.ext.services": "Android ext services",
    "com.android.ext.shared": "Android ext shared",
    "com.google.android.ext.services": "Google ext services",
    "com.google.android.ext.shared": "Google ext shared",
    "com.google.android.configupdater": "Security and carrier config updater",

    # Google core
    "com.google.android.gms": "Play Services: push, banking, backups, location, Play Integrity",
    "com.google.android.gsf": "Google Services Framework: accounts and push",
    "com.android.vending": "Google Play Store",
    "com.google.android.webview": "WebView: in-app browsers",
    "com.android.webview": "WebView: in-app browsers",

    # Samsung
    "com.samsung.android.incallui": "Samsung in-call UI",
    "com.samsung.android.app.telephonyui": "Samsung telephony UI",
    "com.samsung.android.dialer": "Samsung dialer",
    "com.samsung.android.messaging": "Samsung Messages",
    "com.samsung.android.app.settings": "Samsung Settings",
    "com.samsung.android.thermal": "Samsung thermal management",
    "com.samsung.android.spay": "Samsung Wallet/Pay",
    "com.samsung.android.samsungpass": "Samsung Pass: autofill and passwords",
    "com.samsung.android.authfw": "Samsung authentication framework",
    "com.samsung.android.kgclient": "Samsung Knox Guard client",

    # Xiaomi / HyperOS
    "com.miui.securitycenter": "MIUI/HyperOS Security app: permissions, battery, privacy",
    "com.miui.powerkeeper": "MIUI/HyperOS battery management",
    "com.miui.permcenter": "MIUI/HyperOS permission center",
    "com.miui.home": "MIUI/HyperOS launcher",
    "com.miui.telephony": "MIUI/HyperOS telephony",
    "com.xiaomi.xmsf": "Xiaomi push service",
    "com.xiaomi.push": "Xiaomi push service",

    # Huawei / Honor
    "com.huawei.systemmanager": "Huawei system manager: permissions, battery, privacy",
    "com.huawei.phone": "Huawei telephony",
    "com.huawei.contacts": "Huawei contacts",
    "com.huawei.mms": "Huawei Messages",
    "com.huawei.dialer": "Huawei dialer",
    "com.huawei.android.launcher": "Huawei launcher",
    "com.huawei.powergenie": "Huawei battery management",

    # Oppo / OnePlus / Realme
    "com.coloros.securitypermission": "ColorOS permission center",
    "com.oplus.battery": "Oppo/OnePlus battery management",
    "com.coloros.phonemanager": "ColorOS phone manager",
    "com.coloros.telephony": "ColorOS telephony",
    "com.oplus.telephony": "Oppo/OnePlus telephony",
}

# Prefixes cover families that change suffix with the Android or OEM version.
PREFIXES: dict[str, str] = {
    "com.android.providers.": "Android content providers: telephony, contacts, media, settings, downloads",
    "com.android.server.": "Android system services",
    "com.android.internal.": "Android internal services",
    "com.android.systemui.": "System UI module",
    "com.android.settings.": "Android Settings module",
    "com.android.phone.": "Telephony module",
    "com.android.ims.": "IMS: VoLTE and Wi-Fi calling",
    "com.android.bluetooth": "Bluetooth stack: earbuds, car, wearables",
    "com.android.networkstack.": "Network stack module",
    "com.google.android.networkstack.": "Network stack module",
    "com.android.wifi.": "Wi-Fi module",
    "com.google.android.wifi.": "Wi-Fi module",
    "com.android.connectivity.": "Connectivity module",
    "com.android.cellbroadcast": "Emergency alerts (cell broadcast)",
    "com.google.android.cellbroadcast": "Emergency alerts (cell broadcast)",
    "com.android.packageinstaller.": "Package installer module",
    "com.google.android.packageinstaller.": "Package installer module",
    "com.android.documentsui.": "System file picker module",
    "com.android.vending.": "Google Play Store module",
    "com.android.ext.services.": "Android ext services module",
    "com.android.ext.shared.": "Android ext shared module",
    "com.google.android.ext.services.": "Google ext services module",
    "com.google.android.ext.shared.": "Google ext shared module",
    "com.android.nfc.": "NFC module",
    "com.android.se.": "Secure Element module",
    "com.android.emergency.": "Emergency module",
    "com.android.carrierconfig.": "Carrier configuration module",
    "com.google.android.ims.": "IMS module",
    "com.google.android.overlay.modules": "Module overlays: system UI and settings",
    "com.google.android.gms.": "Play Services module",
    "com.google.android.gsf.": "Google Services Framework module",
    "com.google.android.webview.": "WebView module",
    "com.android.webview.": "WebView module",
    "com.google.android.permissioncontroller.": "Permission controller module",
    "com.android.permissioncontroller.": "Permission controller module",
    "com.samsung.android.knox": "Samsung Knox: security, work profile, payments",
    "com.samsung.android.spay": "Samsung Wallet/Pay",
    "com.samsung.android.samsungpass": "Samsung Pass",
    "com.huawei.hwid": "Huawei ID: accounts and device services",
    "com.huawei.systemmanager.": "Huawei system manager",
    "com.coloros.securitypermission.": "ColorOS permission center",
    "com.oplus.battery.": "Oppo/OnePlus battery management",
}


def reason(package: str) -> str | None:
    """Return why `package` is protected, or None if it is not on the hard denylist."""
    if package in EXACT:
        return EXACT[package]
    for prefix, why in PREFIXES.items():
        if package.startswith(prefix):
            return why
    return None


def is_protected(package: str) -> bool:
    return reason(package) is not None


def patterns() -> list[tuple[str, str]]:
    """All patterns, for `phone.py protected` and the docs."""
    return sorted(EXACT.items()) + sorted(PREFIXES.items())
