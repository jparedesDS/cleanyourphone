param(
    [string]$OutDir = (Join-Path $PWD "oneplus6t-dump")
)

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

function Find-Adb {
    if ($env:ADB -and (Test-Path $env:ADB)) { return (Resolve-Path $env:ADB).Path }
    $cmd = Get-Command adb -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $local = Join-Path $PSScriptRoot "..\work\platform-tools\adb.exe"
    if (Test-Path $local) { return (Resolve-Path $local).Path }
    $temp = Join-Path $env:TEMP "cleanyourphone-platform-tools\platform-tools\adb.exe"
    if (Test-Path $temp) { return $temp }
    return $null
}

function Install-Adb {
    $toolsRoot = Join-Path $env:TEMP "cleanyourphone-platform-tools"
    $adb = Join-Path $toolsRoot "platform-tools\adb.exe"
    if (Test-Path $adb) { return $adb }
    New-Item -ItemType Directory -Force -Path $toolsRoot | Out-Null
    $zip = Join-Path $toolsRoot "platform-tools.zip"
    Write-Host "Descargando Android SDK Platform-Tools..."
    Invoke-WebRequest -Uri "https://dl.google.com/android/repository/platform-tools-latest-windows.zip" -OutFile $zip -UseBasicParsing
    Expand-Archive -Path $zip -DestinationPath $toolsRoot -Force
    return $adb
}

function Save-AdbText {
    param([string]$Adb, [string]$Serial, [string]$Name, [string]$Command)
    $output = & $Adb -s $Serial shell $Command 2>&1
    $text = ($output | Out-String).TrimEnd()
    Set-Content -Path (Join-Path $OutDir "$Name.txt") -Value $text -Encoding utf8
    return $text
}

$adb = Find-Adb
if (-not $adb) { $adb = Install-Adb }
if (-not $adb -or -not (Test-Path $adb)) {
    Write-Host "No se pudo encontrar ni descargar adb." -ForegroundColor Red
    exit 2
}

& $adb start-server | Out-Null
$lines = & $adb devices -l | Select-Object -Skip 1 | Where-Object { $_.Trim() -ne "" }
$devices = @()
foreach ($line in $lines) {
    $parts = ($line -split "\s+")
    if ($parts.Count -ge 2 -and $parts[1] -eq "device") { $devices += $parts[0] }
}
if ($devices.Count -eq 0) {
    Write-Host ""
    Write-Host "No hay ningún móvil autorizado por ADB." -ForegroundColor Yellow
    Write-Host "En el OnePlus 6T: Opciones de desarrollador -> Depuración USB activada."
    Write-Host "Conecta el cable de datos, desbloquea el móvil y acepta '¿Permitir depuración USB?'."
    Write-Host ""
    & $adb devices -l
    exit 2
}
if ($devices.Count -gt 1) {
    Write-Host "Hay más de un dispositivo conectado. Deja solo el OnePlus 6T y vuelve a ejecutar." -ForegroundColor Yellow
    & $adb devices -l
    exit 2
}

$serial = $devices[0]
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$props = [ordered]@{
    brand = "ro.product.brand"
    manufacturer = "ro.product.manufacturer"
    model = "ro.product.model"
    device = "ro.product.device"
    android = "ro.build.version.release"
    sdk = "ro.build.version.sdk"
    build = "ro.build.display.id"
    fingerprint = "ro.build.fingerprint"
    security_patch = "ro.build.version.security_patch"
    characteristics = "ro.build.characteristics"
}
$summary = New-Object System.Collections.Generic.List[string]
$summary.Add("CleanYourPhone device summary")
$summary.Add("Collected: $(Get-Date -Format o)")
foreach ($key in $props.Keys) {
    $value = (& $adb -s $serial shell getprop $props[$key] 2>&1 | Out-String).Trim()
    $summary.Add("${key}: $value")
}

$battery = (& $adb -s $serial shell dumpsys battery 2>&1 | Select-String "level:" | Select-Object -First 1)
$summary.Add("battery: $battery")

$summary.Add("")
$summary.Add("Package files: packages.txt, packages-disabled.txt, packages-enabled.txt, packages-system.txt, packages-user.txt")
$summary.Add("Roles: roles.txt")
$summary.Add("IME: ime.txt")
$summary.Add("Users: users.txt")
$summary.Add("Device policy owner lines: device-policy-owner.txt")

Set-Content -Path (Join-Path $OutDir "summary.txt") -Value ($summary -join "`n") -Encoding utf8

Save-AdbText -Adb $adb -Serial $serial -Name "packages" -Command "pm list packages -f" | Out-Null
Save-AdbText -Adb $adb -Serial $serial -Name "packages-disabled" -Command "pm list packages -d" | Out-Null
Save-AdbText -Adb $adb -Serial $serial -Name "packages-enabled" -Command "pm list packages -e" | Out-Null
Save-AdbText -Adb $adb -Serial $serial -Name "packages-system" -Command "pm list packages -s" | Out-Null
Save-AdbText -Adb $adb -Serial $serial -Name "packages-user" -Command "pm list packages -3" | Out-Null
Save-AdbText -Adb $adb -Serial $serial -Name "ime" -Command "ime list -s" | Out-Null
Save-AdbText -Adb $adb -Serial $serial -Name "users" -Command "pm list users" | Out-Null

$roles = @()
foreach ($role in @("DIALER", "SMS", "HOME", "EMERGENCY")) {
    $roles += "### $role"
    $roles += (& $adb -s $serial shell cmd role get-role-holders "android.app.role.$role" 2>&1 | Out-String).Trim()
}
$roles += "### default_input_method"
$roles += (& $adb -s $serial shell settings get secure default_input_method 2>&1 | Out-String).Trim()
Set-Content -Path (Join-Path $OutDir "roles.txt") -Value ($roles -join "`n") -Encoding utf8

$owner = (& $adb -s $serial shell dumpsys device_policy 2>&1 | Select-String "Device Owner|Profile Owner")
Set-Content -Path (Join-Path $OutDir "device-policy-owner.txt") -Value (($owner | Out-String).Trim()) -Encoding utf8

$zipPath = "$OutDir.zip"
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
Compress-Archive -Path (Join-Path $OutDir "*") -DestinationPath $zipPath -Force

Write-Host ""
Write-Host "Listo. Datos guardados en:" -ForegroundColor Green
Write-Host "  $OutDir"
Write-Host "  $zipPath"
Write-Host ""
Write-Host "Abre summary.txt y pégame su contenido. Si puedes, adjunta también packages.txt y packages-disabled.txt."
Write-Host "No se ha modificado nada en el móvil."
