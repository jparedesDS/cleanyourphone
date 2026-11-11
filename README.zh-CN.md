<p align="center">
  <a href="https://cleanyourphone.org/">
    <img src="assets/banner.png" alt="CleanYourPhone — 你的手机，减去多余" width="100%">
  </a>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.es.md">Español</a> ·
  <a href="README.pt-BR.md">Português (BR)</a> ·
  <a href="README.fr.md">Français</a> ·
  <a href="README.de.md">Deutsch</a> ·
  <a href="README.it.md">Italiano</a> ·
  <a href="README.ja.md">日本語</a> ·
  <b>简体中文</b> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml"><img src="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/license-MIT-a78bfa?labelColor=121316" alt="MIT">
  <img src="https://img.shields.io/badge/python-3.10%2B-a78bfa?labelColor=121316" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/telemetry-none-a78bfa?labelColor=121316" alt="无遥测">
  <img src="https://img.shields.io/badge/profiles-157-a78bfa?labelColor=121316" alt="157 个机型配置">
  <a href="https://github.com/jparedesDS/cleanyourphone/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone?color=a78bfa&labelColor=121316" alt="release"></a>
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone-app?color=a78bfa&label=app&labelColor=121316" alt="app release"></a>
</p>

# CleanYourPhone

**你的手机，减去多余。** 一个开源、可逆的 Android 精简 Skill，专为编程智能体打造。它通过 ADB 停用预装应用和服务：无需 root、无需自定义 ROM、不卸载任何东西，一条命令即可恢复 CLI 记录的所有更改。

故事与安全模型见 **[cleanyourphone.org](https://cleanyourphone.org/)**。

另外还有一个可选的 **Windows 应用**，适合更喜欢点按钮而不是输入提示词的人：**[下载早期 MVP](https://github.com/jparedesDS/cleanyourphone-app/releases/latest)**。它是同一套 CLI 之上的图形界面。Skill 仍是主要产品，也是没有机型配置的手机所走的路径。

它是 [cleanyour.tv](https://cleanyour.tv) 的手机版，构建方式相同：一个提示词、一条命令、可逆、开源，而且始终由使用者掌控。

[SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [应用](https://github.com/jparedesDS/cleanyourphone-app) · [安全](docs/SAFETY.md) · [157 个机型配置](docs/PROFILES.md) · [反馈](docs/FEEDBACK.md) · [更新日志](CHANGELOG.md)

## 从这里开始

| 你的情况 | 从这里开始 |
|---|---|
| 有一部手机和一个编程智能体 | 下面的快速开始。 |
| 更喜欢按钮而不是提示词 | [下载 Windows 应用](https://github.com/jparedesDS/cleanyourphone-app/releases/latest)（早期 MVP）。 |
| 想先看看效果 | [官网](https://cleanyourphone.org/)。 |
| 需要安全规则 | [docs/SAFETY.md](docs/SAFETY.md)。 |
| 需要机型配置 | [浏览 157 个机型配置](profiles/README.md)。 |
| 你的手机不在列表中 | 手动使用 Skill，或发送[机型配置请求](docs/FEEDBACK.md)。 |
| 更喜欢终端 | [安装 CLI](docs/CLI.md)。 |

| 部分 | 状态 |
|---|---|
| **Skill** | 主要产品，位于本仓库。 |
| **CLI** | `0.3.4`，以 `cleanyourphone` / `cyp` 发布在 PyPI。 |
| **Windows 应用** | `0.2.1` 早期 MVP，可选，未签名。 |
| **网站** | 10 种语言，见 [cleanyourphone.org](https://cleanyourphone.org/)。 |
| **反馈** | 可选的 Web/应用/Skill 表单，发送到 Discord；没有自动遥测。 |

---

## 为什么以 Skill 为先

一个能停用其他应用的程序，需要 root、Shizuku 或 device-owner 权限。对于一条 shell 命令就能完成的事来说，这意味着太大的权力和风险。Skill 只是文本：使用者的智能体读它、运行 `adb`、展示计划，并在改动任何东西之前先询问。手机上不需要安装任何东西，后台没有程序运行，也不会有任何数据回传。

现在有了一个可选的 Windows 应用，但它并不取代 Skill。它是同一套 CLI 之上的图形界面，只有在能匹配到经过测试的精确 `device` 机型配置，或在明确确认后匹配 `documented` 机型配置并每批只处理一个应用包时，才会继续。如果匹配不到手机，它会停下来，把使用者引导到这里。Skill 仍然可以检查应用包列表、逐个询问每个应用并手动继续。

手机是日常主力设备，所以 Skill 刻意保持保守：

- **只停用，不卸载。** 只用 `pm disable-user --user 0`。`pm enable` 就是撤销。
- **先备份。** 第一次更改前，备份应用包列表、设置、角色、输入法和 `getprop`。
- **保护列表。** Android 核心组件、电话功能、Google Play 服务、WebView、permission controller、紧急警报、IME/telecom、NFC/SE 和 OEM 安全应用包都会被 CLI 拒绝。
- **角色检查。** 不会让你失去拨号器、短信应用、桌面或键盘。
- **小批量。** 每次五个应用包，验证后再继续。
- **先询问。** 银行、支付、WhatsApp、相机、闹钟、VPN、身份验证器、智能手表、eSIM、VoLTE/Wi-Fi 通话和工作应用都会逐项确认，而不是默认处理。

## 工作原理

1. **在手机上：** 启用开发者选项和 USB 调试。用 USB 连接手机。
2. **在电脑上：** 把 `SKILL.md` 交给你的智能体（或粘贴 `PROMPT.md`）。
3. **跟着流程走：** 智能体识别手机、备份、展示应用包表格、询问你使用哪些、分批停用、重启并验证。`python tools/phone.py restore` 可以撤销。

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

## 可选的 Windows 应用

对于更喜欢按钮的人，应用把同一套 CLI 包装成引导式的 Windows 流程：连接、检查、备份、审阅、执行、验证和撤销。

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases/latest">
    <img src="assets/app-review.png" alt="CleanYourPhone 应用审阅界面，显示 documented 机型配置警告和一个已选中的应用" width="760">
  </a>
</p>

- **通过 Wi-Fi 或 USB 连接。** 应用会找到手机、检查构建并显示精确匹配的机型配置。
- **精确的 `device` 机型配置**走经过测试的流程。**`documented` 机型配置**是手动的：显示警告、要求明确确认，并且每批只处理一个应用。没有匹配的机型配置时，停止并转用 Skill。
- **备份是强制步骤。** 逐个审阅应用包，分批执行，验证并撤销整份操作日志。
- **可选附加功能：** 私人 DNS 广告拦截（不包含 YouTube）和本地前后对比基准测试。
- **可选反馈：** 经同意后，可以把一份可编辑的清单发送给维护者。没有自动遥测。
- **无需 root、不卸载、手机上不安装应用。** 安装程序未签名；运行前请校验 SHA-256。

[下载 `v0.2.1`](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) · [源代码](https://github.com/jparedesDS/cleanyourphone-app) · [连接指南](docs/CONNECT.md)。

## 快速开始

### 1. 安装 ADB

下载适用于 Windows、macOS 或 Linux 的 [Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools)，解压后加入 `PATH`。用以下命令检查：

```bash
adb version
```

### 2. 准备手机

设置 → 关于手机 → 连续点按 **版本号** 7 次 → 返回 → **开发者选项** → 开启 **USB 调试**。用 USB 连接手机，并接受 **允许 USB 调试吗？** 提示。保持手机解锁，电量高于 30%。

Android 11 及更高版本可以改用 **无线调试**：开启它，点按文字（而不只是开关），选择**使用配对码配对设备**，并让该对话框保持打开。配对对话框有自己的端口；它不是主界面上的连接端口。首次操作步骤和常见问题的解决办法见 [docs/CONNECT.md](docs/CONNECT.md)。

### 3. 克隆并检查

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

CLI 是可选的。`SKILL.md` 也包含原始的 `adb` 命令，所以智能体没有 Python 也能工作。CLI 的存在是为了避免智能体自行临时拼凑防护规则。

更喜欢终端？用 [pipx](https://pipx.pypa.io/) 安装这个命令：

```bash
pipx install cleanyourphone
cleanyourphone doctor
```

这会添加 `cleanyourphone` 和短别名 `cyp`。[docs/CLI.md](docs/CLI.md) 介绍了向导、安装后的文件位置和安全规则。`python tools/phone.py` 仍然可用。

### 4. 把 Skill 交给你的智能体

| 智能体 | 放在哪里 |
|---|---|
| **Claude Code** | `~/.claude/skills/cleanyourphone/SKILL.md`（个人）或 `.claude/skills/cleanyourphone/SKILL.md`（项目） |
| **OpenCode** | `~/.config/opencode/skills/cleanyourphone/SKILL.md`（全局）或 `.opencode/skills/cleanyourphone/SKILL.md`（项目） |
| **Codex** | 项目中的 `AGENTS.md`，或 `~/.codex/AGENTS.md`；如果你的版本不加载 Skill，就粘贴 `PROMPT.md` |
| **Cursor** | `.cursor/rules/cleanyourphone.mdc`，内容为 `SKILL.md` |
| **Gemini CLI** | 项目中的 `GEMINI.md` |
| **任意聊天智能体** | 粘贴 `PROMPT.md`，当它要求时再粘贴 `SKILL.md` |

西班牙语提示词：[PROMPT.es.md](PROMPT.es.md)。Skill 会用使用者书写的语言回答。

最简单的做法是克隆仓库，并在该文件夹中打开你的智能体：`SKILL.md` 已经在根目录，所以 `python tools/phone.py` 可以直接使用。如果你的智能体从全局文件夹加载 Skill，请把 `SKILL.md` 复制到那里；用 pipx 安装 CLI（见上文）后，就不需要保留克隆的仓库：

```bash
mkdir -p ~/.claude/skills/cleanyourphone
cp SKILL.md ~/.claude/skills/cleanyourphone/SKILL.md
```

即使没有仓库，Skill 仍然可用：它包含原始的 `adb` 命令，并会告诉智能体使用它们。

然后说：**“清理我的手机”** 或 **“在我的 Pixel 上使用 cleanyourphone”**。

## 它能做什么

- 停用 OEM 遥测、广告展示面、推荐栏、重复的浏览器/应用商店和未使用的预装应用。
- 可选地用预设（`adguard`、`adguard-family`、`controld`、`mullvad`）或你自己的解析器设置私人 DNS，并检查广告是否真的被拦截。它不是 YouTube 广告拦截器；见 [docs/ADS.md](docs/ADS.md)。
- 生成报告：改了什么、为什么改、保留了什么、备份路径和撤销命令。
- 把 `documented` 机型配置当作人工证据：没有 `disable` 列表、不自动执行，审阅后一次只处理一个应用包。
- 为同一流程提供可选的 Windows 图形界面（`device` 机型配置自动执行，`documented` 手动，其他情况停止并链接到这里）。
- 用 `bench snapshot` 和 `bench compare` 测量前后的可用 RAM、进程数和应用包数量；结果近似、仅限本地，不代表因果关系。见 [docs/BENCH.md](docs/BENCH.md)。
- 测量前后的电池基线（`docs/BATTERY.md`），不承诺奇迹。

## 反馈与机型配置请求

如果某款手机尚未覆盖，使用者可以请求机型配置或报告 bug，而无需提供序列号、IP 地址、IMEI 或 MAC 地址：

- **Web：** [cleanyourphone 反馈表单](https://cleanyourphone.org/#feedback)。
- **应用：** 顶栏中的 **反馈**；清单已预填且可编辑。
- **Skill：** `python scripts/feedback.py --kind profile --checklist-file feedback.txt` 会预览 payload；只有在使用者同意后才添加 `--yes`。

消息会发送到 Cloudflare Worker，然后转发到维护者的 Discord。启动时或扫描期间不会发送任何内容。应用和网站使用同一个 Worker；`tools/phone.py` 保持无网络访问。payload、脱敏和频率限制见 [docs/FEEDBACK.md](docs/FEEDBACK.md)。

## 拦截广告（可选）

私人 DNS 可以拦截许多应用内的广告和跟踪器域名。它不是 YouTube 拦截器，也不是 VPN，还可能导致强制门户（captive portal）无法正常使用。预设包括：

```bash
python tools/phone.py dns providers
python tools/phone.py dns set adguard
python tools/phone.py dns check
python tools/phone.py dns restore
```

当对照域名无法解析时，`dns check` 会区分“已拦截”和“无法测试”。OEM 广告开关清单和注意事项见 [docs/ADS.md](docs/ADS.md)。

## 衡量结果

记录一份本地的前后快照；不会保存序列号或构建指纹：

```bash
python tools/phone.py bench snapshot --label before
# apply, reboot and verify
python tools/phone.py bench snapshot --label after
python tools/phone.py bench compare <before.json> <after.json>
```

对比结果是近似的，不代表因果关系。见 [docs/BENCH.md](docs/BENCH.md)。

## 它不做什么

- **不在手机上安装应用。** 可选的 Windows 应用在电脑上运行；手机只会收到 `pm disable-user` / `pm enable`。
- **不需要 root、Magisk 或 Shizuku。**
- **不使用自定义 ROM、不解锁 bootloader、不刷写固件。**
- **不卸载。** `pm disable-user` 可逆；`pm uninstall` 不可逆。
- **不改动工作资料或 MDM。** 如果手机受管理，它会停止。
- **不拦截 YouTube 广告。** 私人 DNS 不会影响同域广告。`docs/FAQ.md` 中有解释。
- **没有自动遥测。** CLI 是本地工具；可选反馈表单只在使用者按下“发送”时发送。托管式智能体仍会收到会话内容（模型、应用包名、构建指纹），如果这很重要，请使用本地模型。
- **不宣称“电池翻倍”。** 精简带来的真实待机收益是 0–10%；真正的大头是后台限制、亮度和刷新率，以及 DNS。

## 安全

第一次运行前请阅读 [docs/SAFETY.md](docs/SAFETY.md)。简要版：

- CLI 会拒绝保护列表上的应用包、持有角色的应用包，以及任何没有备份的更改。
- 每一次停用都会被记录。`python tools/phone.py restore` 会精确重新启用工具停用的内容，并且不会碰你此前已经停用的项目。
- 如果手机陷入启动循环，[docs/RESTORE.md](docs/RESTORE.md) 提供了恢复路径。不要把恢复出厂设置当作第一步。
- 精简是可逆的，但你的 OEM 可能不这么看。在欧盟，它本身不会让法定保修失效，但维修中心可以拒绝处理被修改过的软件。请如实告诉使用者。

## 机型配置

机型配置要么是在真机上测试过的应用包列表（`device`），要么是根据原始固件转储构建的列表（`documented`）。`documented` 机型配置从不自动执行，也没有 `disable` 列表；用它们逐个应用包地询问使用者。`apply` 只会在 `tested` 中列出的构建上、针对 `device` 机型配置运行。平板机型配置会设置 `form_factor: tablet`；缺少拨号器/短信角色是警告，不是失败。

Windows 应用遵循同样的规则：`device` 机型配置可以使用经过测试的流程，`documented` 机型配置需要警告和明确确认，并且每批只处理一个应用包。如果没有匹配的机型配置，应用会停止并链接到本 Skill，而不是猜测。

按机型排列的完整目录见 [docs/PROFILES.md](docs/PROFILES.md)。

| 品牌 | 机型配置 | 真机测试 | 平板 |
|---|---|---|---|
| **Google** | 5 | 1 | 0 |
| **Samsung** | 55 | 1 | 7 |
| **Xiaomi** | 15 | 1 | 2 |
| **Redmi** | 56 | 0 | 1 |
| **POCO** | 16 | 0 | 0 |
| **OnePlus** | 8 | 1 | 0 |
| **Motorola** | 1 | 0 | 0 |
| **通用** | 1 | 0 | 0 |

想添加自己的机型？请阅读 [profiles/README.md](profiles/README.md)。`device` 机型配置需要真实测试；`documented` 机型配置需要原始固件转储或机主自行收集的设备清单，并至少提供一个来源 URL。

## 开源操作系统的问题

是的，它存在。不，它不是首先要做的事。[docs/ROMS.md](docs/ROMS.md) 解释了真实的取舍：

- **GrapheneOS** 很出色，但只支持 Pixel 6–10（2026 年 10 月）。安全与隐私最佳；Play 服务运行在沙盒中；bootloader 处于锁定状态。
- **/e/OS** 拥有最广泛的简易安装机型列表，用 microG 代替 Google。
- **LineageOS** 覆盖面广，但维护成本更高；官方构建因设备而异。
- **CalyxOS** 覆盖 Pixel、Fairphone 和部分 Motorola 机型。

代价是真实存在的：解锁 bootloader 会清空手机；Play Integrity 可能导致银行/钱包应用无法使用，并让 Netflix 只能播放 SD 画质；部分运营商会失去 VoLTE/Wi-Fi 通话；而你要自己负责安全补丁的维护。在三星设备上，解锁会永久触发 Knox。这就是 Skill 留在官方 ROM 上的原因：它去除大多数人会注意到的广告与遥测暴露面，而不必付出这些代价。它不是一个加固的操作系统，也不能在 Pixel 上替代 GrapheneOS。

## FAQ

**会让我失去保修吗？**
精简属于软件配置，不是硬件改装，而且可逆。在欧盟，法定保修不会因此自动失效，但维修中心可能拒绝处理被修改过的软件。Skill 不会解锁 bootloader。

**会把手机变砖吗？**
停用错误的核心应用包可能导致启动循环。因此 CLI 会拒绝保护列表、检查角色、先备份并分批验证。`restore` 会精确撤销工具停用的内容；如果日志丢失，`restore --from-backup` 会从备份重建更改。包括安全模式在内的完整恢复路径见 [docs/RESTORE.md](docs/RESTORE.md)。

**会移除 YouTube 广告吗？**
不会。基于私人 DNS 的广告拦截解析器可以拦截许多应用内广告和跟踪器，但 YouTube 的广告与视频来自同一域名。Skill 不会安装修改版应用。

**能在工作手机上使用吗？**
不能。如果 `dumpsys device_policy` 显示 device owner 或 profile owner，或者 `pm list users` 显示多个用户，Skill 就会停止。

**支持三星/小米/华为吗？**
这个方法适用于任何 Android 8+ 手机。应用包名和安全列表各不相同。请使用匹配你具体机型的配置，或让智能体手动分类，并在每个应用包前询问。在没有 Google 服务的华为/荣耀设备上，许多 `com.google.*` 应用包并不存在。

**需要 Python 吗？**
不需要。Skill 包含原始的 `adb` 命令。CLI 是防护栏，也是便利工具；它只使用标准库，没有依赖。Windows 应用内置 CLI，不需要 Python。

**有图形界面吗？**
有，[cleanyourphone-app](https://github.com/jparedesDS/cleanyourphone-app) 中有一个可选的 Windows 应用。它是早期 MVP，未进行代码签名，只会在已知机型配置上继续。其他所有手机仍然走 Skill。

**如何报告新机型或发送反馈？**
使用[网页表单](https://cleanyourphone.org/#feedback)、应用中的 **反馈**，或 Skill 里的 `scripts/feedback.py`。它是自愿加入的，会预览 payload，并排除序列号、IP、IMEI 和 MAC 地址。见 [docs/FEEDBACK.md](docs/FEEDBACK.md)。

## 参与贡献

- 为新机型提供经过测试的（`device`）机型配置：提交 PR，包含 `profiles/<brand>/<model>.json` 和测试详情。
- `documented` 机型配置：使用 `scripts/dump_inventory.py`，在 `sources` 中引用原始转储，并让 `disable` 保持为空。
- 防护逻辑、解析器或 CLI 修复：在 `tests/` 中添加测试。
- 安全规则变更：先开 issue。这些规则就是产品。
- 你无法亲自测试的手机：发送[机型配置请求](https://cleanyourphone.org/#feedback)，附上型号、Android 版本、构建和构建指纹。不要提供序列号或 IP。
- 品牌或标志变更：修改资源前请阅读 [docs/BRAND.md](docs/BRAND.md)。
- 修改仓库前请阅读 [AGENTS.md](AGENTS.md)。

## 许可证

MIT。见 [LICENSE](LICENSE)。
