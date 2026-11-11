<p align="center">
  <a href="https://cleanyourphone.org/">
    <img src="assets/banner.png" alt="CleanYourPhone — 불필요한 것을 뺀, 당신의 폰" width="100%">
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
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <b>한국어</b>
</p>

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml"><img src="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/license-MIT-a78bfa?labelColor=121316" alt="MIT">
  <img src="https://img.shields.io/badge/python-3.10%2B-a78bfa?labelColor=121316" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/telemetry-none-a78bfa?labelColor=121316" alt="텔레메트리 없음">
  <img src="https://img.shields.io/badge/profiles-156-a78bfa?labelColor=121316" alt="프로필 156개">
  <a href="https://github.com/jparedesDS/cleanyourphone/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone?color=a78bfa&labelColor=121316" alt="릴리스"></a>
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone-app?color=a78bfa&label=app&labelColor=121316" alt="앱 릴리스"></a>
</p>

# CleanYourPhone

**불필요한 것을 뺀, 당신의 폰.** 코딩 에이전트를 위해 만든 오픈소스 Android 디블로트 스킬입니다.
ADB로 사전 설치된 앱과 서비스를 비활성화합니다. root도, 커스텀 ROM도, 앱 삭제도 없고, CLI가
기록한 변경을 명령 하나로 되돌릴 수 있습니다.

프로젝트 이야기와 안전 모델은
**[cleanyourphone.org](https://cleanyourphone.org/)**에서
볼 수 있습니다.

프롬프트보다 버튼이 편한 사람을 위한 **선택 사항인 Windows 앱**도 있습니다:
**[Early MVP 다운로드](https://github.com/jparedesDS/cleanyourphone-app/releases/latest)**. 같은
CLI를 감싼 GUI입니다. 스킬은 여전히 주요 제품이며, 프로필이 없는 폰을 위한 경로입니다.

[cleanyour.tv](https://cleanyour.tv)의 폰 버전이며, 같은 방식으로 만들었습니다. 프롬프트 하나,
명령 하나, 되돌릴 수 있고, 오픈소스이며, 결정권은 언제나 사용자에게 있습니다.

[SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [앱](https://github.com/jparedesDS/cleanyourphone-app) · [안전](docs/SAFETY.md) · [프로필 156개](docs/PROFILES.md) · [피드백](docs/FEEDBACK.md) · [변경 내역](CHANGELOG.md)

## 여기서 시작하세요

| 보유 상황 | 시작 지점 |
|---|---|
| 폰과 코딩 에이전트가 있다 | 아래 빠른 시작을 따르세요. |
| 프롬프트보다 버튼이 좋다 | [Windows 앱 다운로드](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) (Early MVP). |
| 먼저 보고 싶다 | [웹사이트](https://cleanyourphone.org/). |
| 안전 규칙이 필요하다 | [docs/SAFETY.md](docs/SAFETY.md). |
| 모델 프로필이 필요하다 | [프로필 156개 둘러보기](profiles/README.md). |
| 내 폰이 목록에 없다 | 스킬을 직접 사용하거나 [프로필 요청](docs/FEEDBACK.md)을 보내세요. |
| 터미널이 좋다 | [CLI 설치](docs/CLI.md). |

| 구성 요소 | 상태 |
|---|---|
| **스킬** | 주요 제품, 이 저장소에 있습니다. |
| **CLI** | `0.3.3`, PyPI에 `cleanyourphone` / `cyp`로 배포됩니다. |
| **Windows 앱** | `0.2.1` Early MVP, 선택 사항, 서명되지 않음. |
| **웹사이트** | [cleanyourphone.org](https://cleanyourphone.org/)에서 10개 언어로 제공. |
| **피드백** | 웹/앱/스킬에서 Discord로 보내는 선택형 양식, 자동 텔레메트리 없음. |

---

## 스킬이 먼저인 이유

다른 앱을 비활성화하는 앱은 root, Shizuku 또는 device-owner 권한이 필요합니다. 셸 명령 하나로
할 수 있는 일 치고는 권한도 너무 크고 위험도 큽니다. 스킬은 그저 텍스트입니다. 사용자의
에이전트가 이를 읽고 `adb`를 실행하며 계획을 보여 주고, 무엇이든 건드리기 전에 물어봅니다. 폰에
설치할 것도, 백그라운드에서 실행되는 것도, 외부로 데이터를 보내는 것도 없습니다.

이제 선택 사항인 Windows 앱이 있지만 스킬을 대체하지는 않습니다. 같은 CLI를 감싼 GUI이며,
테스트된 빌드에 정확히 맞는 `device` 프로필이 있거나, 명시적으로 확인한 뒤 배치당 패키지 하나씩
적용하는 조건으로 `documented` 프로필이 맞을 때만 계속합니다. 폰을 매칭하지 못하면 멈추고
사용자를 이곳으로 안내합니다. 스킬은 여전히 패키지 목록을 살펴보고, 앱마다 물어보고, 수동으로
계속할 수 있습니다.

폰은 매일 쓰는 기기이므로 스킬은 의도적으로 보수적입니다:

- **비활성화만, 삭제는 없음.** `pm disable-user --user 0`만 사용합니다. 되돌리기는 `pm enable`입니다.
- **먼저 백업.** 첫 변경 전에 패키지 목록, 설정, 역할, IME, `getprop`을 백업합니다.
- **보호 목록.** 핵심 Android, 통신, Play Services, WebView, 권한 컨트롤러, 긴급 경보,
  IME/통신, NFC/SE, 제조사 보안 패키지는 CLI가 거부합니다.
- **역할 확인.** 다이얼러, 문자 앱, Home 앱, 키보드가 없는 상태로 남지 않게 합니다.
- **작은 배치.** 한 번에 5개 패키지씩, 확인한 뒤 계속합니다.
- **먼저 질문.** 뱅킹, 결제, WhatsApp, 카메라, 알람, VPN, 인증 앱, 스마트워치, eSIM,
  VoLTE/Wi-Fi 통화, 업무 앱은 기본값이 아니라 체크리스트입니다.

## 작동 방식

1. **폰에서:** 개발자 옵션과 USB 디버깅을 켭니다. USB로 연결합니다.
2. **컴퓨터에서:** 에이전트에 `SKILL.md`를 주거나 `PROMPT.md`를 붙여 넣습니다.
3. **따라가기:** 에이전트가 폰을 식별하고, 백업하고, 패키지 표를 보여 주고, 무엇을 쓰는지 묻고,
   배치로 비활성화하고, 재부팅 후 검증합니다. `python tools/phone.py restore`로 되돌립니다.

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

## 선택 사항인 Windows 앱

버튼이 편한 사람을 위해, 앱은 같은 CLI를 연결, 확인, 백업, 검토, 적용, 검증, 되돌리기의
안내형 Windows 흐름으로 감쌉니다.

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases/latest">
    <img src="assets/app-review.png" alt="documented 프로필 경고와 선택된 앱 하나가 보이는 CleanYourPhone 앱 검토 화면" width="760">
  </a>
</p>

- **Wi-Fi 또는 USB로 연결.** 앱이 폰을 찾고 빌드를 확인한 뒤 정확한 프로필을 보여 줍니다.
- **정확한 `device` 프로필**은 테스트된 경로를 따릅니다. **`documented` 프로필**은 수동입니다:
  눈에 보이는 경고, 명시적 확인, 배치당 앱 하나. 프로필이 없으면 멈추고 스킬을 사용합니다.
- **백업은 필수.** 모든 패키지를 검토하고, 배치로 적용하고, 검증한 뒤 저널 전체를 되돌립니다.
- **선택 기능:** 비공개 DNS 광고 차단(YouTube 제외)과 로컬 전/후 벤치마크.
- **선택형 피드백:** 동의 후 메인테이너에게 보낼 수 있는 편집 가능한 체크리스트. 자동
  텔레메트리는 없습니다.
- **root 없음, 삭제 없음, 폰에 설치되는 앱 없음.** 설치 프로그램은 서명되지 않았으므로 실행 전에
  SHA-256을 확인하세요.

[`v0.2.1` 다운로드](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) ·
[소스](https://github.com/jparedesDS/cleanyourphone-app) ·
[연결 가이드](docs/CONNECT.md).

## 빠른 시작

### 1. ADB 설치

Windows, macOS 또는 Linux용
[Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools)를
내려받아 압축을 풀고 `PATH`에 추가합니다. 다음으로 확인하세요:

```bash
adb version
```

### 2. 폰 준비

설정 → 휴대전화 정보 → **빌드 번호**를 7번 탭 → 뒤로 → **개발자 옵션** → **USB 디버깅**을
켭니다. 폰을 USB로 연결하고 **USB 디버깅을 허용하시겠습니까?** 프롬프트를 수락합니다. 폰은 잠금
해제 상태로 두고 배터리를 30% 이상 유지하세요.

Android 11 이상에서는 **무선 디버깅**을 대신 사용할 수 있습니다. 무선 디버깅을 켜고, 스위치가
아니라 문구를 탭한 뒤 **페어링 코드로 기기 페어링**을 선택하고 그 대화상자를 열어 두세요. 페어링
대화상자에는 자체 포트가 있으며, 메인 화면의 연결 포트와 다릅니다. 처음 연결하는 방법과 흔한
해결법은 [docs/CONNECT.md](docs/CONNECT.md)를 참고하세요.

### 3. 클론 및 확인

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

CLI는 선택 사항입니다. `SKILL.md`에 `adb` 명령이 그대로 들어 있어 에이전트가 Python 없이 작업할
수 있습니다. CLI가 있는 이유는 에이전트가 안전장치를 임의로 만들지 않게 하기 위해서입니다.

터미널이 좋다면 [pipx](https://pipx.pypa.io/)로 명령을 설치하세요:

```bash
pipx install cleanyourphone
cleanyourphone doctor
```

`cleanyourphone`과 짧은 별칭 `cyp`가 추가됩니다. [docs/CLI.md](docs/CLI.md)에서 마법사, 설치
파일 위치, 안전 규칙을 설명합니다. `python tools/phone.py`도 계속 작동합니다.

### 4. 에이전트에 스킬 전달

| 에이전트 | 넣을 위치 |
|---|---|
| **Claude Code** | `~/.claude/skills/cleanyourphone/SKILL.md` (개인) 또는 `.claude/skills/cleanyourphone/SKILL.md` (프로젝트) |
| **OpenCode** | `~/.config/opencode/skills/cleanyourphone/SKILL.md` (전역) 또는 `.opencode/skills/cleanyourphone/SKILL.md` (프로젝트) |
| **Codex** | 프로젝트의 `AGENTS.md` 또는 `~/.codex/AGENTS.md`; 스킬을 불러오지 않는 빌드라면 `PROMPT.md`를 붙여 넣으세요 |
| **Cursor** | `SKILL.md` 내용을 담은 `.cursor/rules/cleanyourphone.mdc` |
| **Gemini CLI** | 프로젝트의 `GEMINI.md` |
| **모든 채팅 에이전트** | `PROMPT.md`를 붙여 넣고, 요청하면 `SKILL.md`를 붙여 넣으세요 |

스페인어 프롬프트: [PROMPT.es.md](PROMPT.es.md). 스킬은 사용자가 쓰는 언어로 답합니다.

가장 간단한 방법은 저장소를 클론하고 그 폴더에서 에이전트를 여는 것입니다. `SKILL.md`가 이미
루트에 있어 `python tools/phone.py`가 바로 작동합니다. 에이전트가 전역 폴더에서 스킬을
불러온다면 `SKILL.md`를 그곳에 복사하세요. 위에서 pipx로 CLI를 설치했다면 저장소를 계속 클론해
둘 필요가 없습니다:

```bash
mkdir -p ~/.claude/skills/cleanyourphone
cp SKILL.md ~/.claude/skills/cleanyourphone/SKILL.md
```

저장소가 없어도 스킬은 작동합니다. `adb` 명령이 그대로 들어 있고 에이전트에게 그 명령을 쓰라고
알려 줍니다.

그다음 이렇게 요청하세요: **"내 폰 좀 정리해 줘"** 또는 **"내 Pixel에서 cleanyourphone을 써 줘"**.

## 하는 일

- 제조사 텔레메트리, 광고 영역, 추천 행, 중복 브라우저/스토어, 사용하지 않는 사전 설치 앱을
  비활성화합니다.
- 선택적으로 프리셋(`adguard`, `adguard-family`, `controld`, `mullvad`) 또는 직접 지정한
  리졸버로 비공개 DNS를 설정하고, 광고가 실제로 차단되는지 확인합니다. YouTube 광고 차단기는
  아닙니다. [docs/ADS.md](docs/ADS.md)를 참고하세요.
- 보고서를 만듭니다: 무엇이 바뀌었는지, 왜인지, 무엇을 남겼는지, 백업 경로, 되돌리기 명령.
- `documented` 프로필을 수동 증거로 취급합니다: `disable` 목록 없음, 자동 적용 없음, 검토 후
  한 번에 패키지 하나.
- 같은 흐름을 위한 선택형 Windows GUI를 제공합니다(`device` 프로필은 자동, `documented`는 수동,
  나머지는 멈추고 이곳으로 연결).
- `bench snapshot`과 `bench compare`로 전/후 사용 가능한 RAM, 프로세스, 패키지 수를 측정합니다.
  대략적이며 로컬이고 인과 관계를 주장하지 않습니다. [docs/BENCH.md](docs/BENCH.md)를 참고하세요.
- 전/후 배터리 기준선을 측정합니다(`docs/BATTERY.md`). 기적을 약속하지는 않습니다.

## 피드백과 프로필 요청

폰이 지원되지 않는다면 시리얼 번호, IP 주소, IMEI, MAC 주소를 공유하지 않고도 프로필을
요청하거나 버그를 보고할 수 있습니다:

- **웹:** [cleanyourphone 피드백 양식](https://cleanyourphone.org/#feedback).
- **앱:** 헤더의 **피드백**; 체크리스트가 미리 채워져 있고 편집할 수 있습니다.
- **스킬:** `python scripts/feedback.py --kind profile --checklist-file feedback.txt`로
  페이로드를 미리 봅니다. 사용자가 승인한 뒤에만 `--yes`를 추가하세요.

메시지는 Cloudflare Worker를 거쳐 메인테이너의 Discord로 전달됩니다. 시작할 때나 스캔 중에는
아무것도 전송되지 않습니다. 앱과 웹사이트는 같은 Worker를 사용하며, `tools/phone.py`는 네트워크를
쓰지 않습니다. 페이로드, 민감 정보 제거, 속도 제한은 [docs/FEEDBACK.md](docs/FEEDBACK.md)를
참고하세요.

## 광고 차단(선택 사항)

비공개 DNS는 앱 내부의 많은 광고·트래커 도메인을 차단할 수 있습니다. YouTube 차단기가 아니고
VPN도 아니며, 캡티브 포털을 깨뜨릴 수 있습니다. 프리셋은 다음과 같습니다:

```bash
python tools/phone.py dns providers
python tools/phone.py dns set adguard
python tools/phone.py dns check
python tools/phone.py dns restore
```

`dns check`는 제어 도메인이 확인되지 않을 때 “차단됨”과 “테스트할 수 없음”을 구분합니다. 제조사
광고 스위치 체크리스트와 주의 사항은 [docs/ADS.md](docs/ADS.md)를 참고하세요.

## 결과 측정

로컬 전/후 스냅샷을 기록합니다. 시리얼이나 fingerprint는 저장하지 않습니다:

```bash
python tools/phone.py bench snapshot --label before
# apply, reboot and verify
python tools/phone.py bench snapshot --label after
python tools/phone.py bench compare <before.json> <after.json>
```

비교는 근사치이며 인과 관계를 뜻하지 않습니다. [docs/BENCH.md](docs/BENCH.md)를 참고하세요.

## 하지 않는 일

- **폰에 앱을 설치하지 않습니다.** 선택형 Windows 앱은 컴퓨터에서 실행되고, 폰은
  `pm disable-user` / `pm enable`만 받습니다.
- **root, Magisk, Shizuku가 필요 없습니다.**
- **커스텀 ROM, 부트로더 잠금 해제, 플래싱이 없습니다.**
- **삭제하지 않습니다.** `pm disable-user`는 되돌릴 수 있지만 `pm uninstall`은 아닙니다.
- **업무 프로필이나 MDM을 변경하지 않습니다.** 폰이 관리되고 있으면 멈춥니다.
- **YouTube 광고를 차단하지 않습니다.** 비공개 DNS는 동일 도메인 광고를 건드리지 않습니다.
  `docs/FAQ.md`에서 설명합니다.
- **자동 텔레메트리가 없습니다.** CLI는 로컬에서 동작하며, 선택형 피드백 양식은 사용자가 전송을
  누를 때만 보냅니다. 호스팅된 에이전트는 여전히 세션(모델, 패키지 이름, fingerprint)을
  받으므로 민감하다면 로컬 모델을 사용하세요.
- **"배터리 두 배" 같은 주장은 없습니다.** 디블로트로 얻는 현실적인 대기 시간 이득은 0–10%이며,
  큰 효과는 백그라운드 제한, 밝기/주사율, DNS에서 나옵니다.

## 안전

첫 실행 전에 [docs/SAFETY.md](docs/SAFETY.md)를 읽으세요. 요약하면:

- CLI는 보호 목록의 패키지, 역할을 보유한 패키지, 백업 없는 변경을 거부합니다.
- 모든 비활성화가 기록됩니다. `python tools/phone.py restore`는 도구가 비활성화한 것만 정확히
  다시 활성화하고, 이미 비활성화해 둔 것은 그대로 둡니다.
- 폰이 부팅 루프에 빠지면 [docs/RESTORE.md](docs/RESTORE.md)에 복구 경로가 있습니다. 첫 조치로
  공장 초기화를 하지 마세요.
- 디블로트는 되돌릴 수 있지만 제조사는 다르게 볼 수 있습니다. EU에서는 그 자체로 법적 보증이
  무효가 되지 않지만, 수리 센터가 수정된 소프트웨어 처리를 거부할 수 있습니다. 사용자에게
  솔직하게 알리세요.

## 프로필

프로필은 실제 폰에서 테스트한 패키지 목록(`device`)이거나 1차 펌웨어 덤프로 만든
목록(`documented`)입니다. `documented` 프로필은 절대 자동 적용되지 않고 `disable` 목록이
없습니다. 패키지마다 물어보는 데 사용하세요. `apply`는 `tested`에 나열된 빌드의 `device`
프로필에서만 실행됩니다. 태블릿 프로필은 `form_factor: tablet`을 설정하며, 다이얼러/SMS 역할이
없으면 실패가 아니라 경고입니다.

Windows 앱도 같은 규칙을 따릅니다: `device` 프로필은 테스트된 흐름을 사용할 수 있고,
`documented` 프로필은 경고와 명시적 확인이 필요하며 배치당 패키지 하나씩 실행합니다. 일치하는
프로필이 없으면 앱은 추측하지 않고 멈춘 뒤 이 스킬로 연결합니다.

모델별 전체 카탈로그는 [docs/PROFILES.md](docs/PROFILES.md)에 있습니다.

| 브랜드 | 프로필 | 실제 기기 테스트 | 태블릿 |
|---|---|---|---|
| **Google** | 5 | 1 | 0 |
| **Samsung** | 55 | 1 | 7 |
| **Xiaomi** | 15 | 1 | 2 |
| **Redmi** | 56 | 0 | 1 |
| **POCO** | 16 | 0 | 0 |
| **OnePlus** | 8 | 1 | 0 |
| **일반** | 1 | 0 | 0 |

내 폰을 추가하고 싶나요? [profiles/README.md](profiles/README.md)를 읽어 보세요. `device`
프로필에는 실제 테스트가 필요하고, `documented` 프로필에는 1차 펌웨어 덤프 또는 소유자가 수집한
기기 인벤토리와 최소 하나의 출처 URL이 필요합니다.

## 오픈소스 OS 문제

있습니다. 하지만 가장 먼저 할 일은 아닙니다. [docs/ROMS.md](docs/ROMS.md)에서 실제
트레이드오프를 설명합니다:

- **GrapheneOS**는 훌륭하지만 Pixel 6–10(2026년 10월)에서만 쓸 수 있습니다. 보안과 개인정보
  보호가 가장 뛰어나고, Play Services가 샌드박스로 격리되며, 부트로더가 잠겨 있습니다.
- **/e/OS**는 설치가 쉬운 기기 목록이 가장 넓고, Google 대신 microG를 씁니다.
- **LineageOS**는 폭넓지만 유지 관리 부담이 크고, 공식 빌드는 기기마다 다릅니다.
- **CalyxOS**는 Pixel, Fairphone, 일부 Motorola 모델을 지원합니다.

비용도 현실적입니다. 부트로더 잠금을 해제하면 폰이 초기화되고, Play Integrity 때문에
뱅킹/Wallet이 깨지거나 Netflix가 SD 화질로 떨어질 수 있으며, 일부 통신사에서는 VoLTE/Wi-Fi
통화를 쓸 수 없게 되고, 보안 패치의 메인테이너가 사용자가 됩니다. Samsung에서 부트로더 잠금을
해제하면 Knox가 영구적으로 트립됩니다. 그래서 이 스킬은 순정 ROM에 머뭅니다. 대부분의 사람이
체감하는 광고와 텔레메트리 영역을 그런 비용 없이 줄여 주기 때문입니다. 강화된 OS가 아니며
Pixel에서 GrapheneOS를 대신하지도 않습니다.

## FAQ

**보증이 무효가 되나요?**
디블로트는 하드웨어 개조가 아니라 소프트웨어 설정이며 되돌릴 수 있습니다. EU에서는 법적 보증이
자동으로 무효가 되지 않지만, 수리 센터가 수정된 소프트웨어 처리를 거부할 수 있습니다. 이 스킬은
부트로더 잠금을 해제하지 않습니다.

**폰이 벽돌이 될 수 있나요?**
잘못된 핵심 패키지를 비활성화하면 부팅 루프가 발생할 수 있습니다. 그래서 CLI는 보호 목록을
거부하고, 역할을 확인하고, 먼저 백업하고, 배치로 검증합니다. `restore`는 도구가 비활성화한 것만
정확히 되돌리며, 저널을 잃어버렸다면 `restore --from-backup`이 백업에서 변경을 재구성합니다. 안전
모드를 포함한 전체 복구 경로는 [docs/RESTORE.md](docs/RESTORE.md)에 있습니다.

**YouTube 광고를 제거하나요?**
아니요. 비공개 DNS를 통한 광고 차단 리졸버는 앱 내부의 많은 광고와 트래커를 차단하지만,
YouTube는 영상과 같은 도메인에서 광고를 제공합니다. 이 스킬은 패치된 앱을 설치하지 않습니다.

**업무용 폰에서도 작동하나요?**
아니요. `dumpsys device_policy`에 device owner 또는 profile owner가 표시되거나 `pm list users`에
사용자가 둘 이상이면 스킬은 멈춥니다.

**Samsung/Xiaomi/Huawei에서도 작동하나요?**
이 방법은 Android 8 이상 폰이면 어디든 작동합니다. 패키지 이름과 안전 목록은 모델마다 다릅니다.
정확한 모델의 프로필을 사용하거나, 에이전트가 수동으로 분류하고 패키지마다 물어보게 하세요.
Google 서비스가 없는 Huawei/Honor에서는 많은 `com.google.*` 패키지가 존재하지 않습니다.

**Python이 필요한가요?**
아니요. 스킬에는 `adb` 명령이 그대로 포함되어 있습니다. CLI는 안전장치이자 편의 기능이며, 표준
라이브러리만 쓰고 의존성이 없습니다. Windows 앱은 CLI를 포함하므로 Python이 필요 없습니다.

**GUI가 있나요?**
네, [cleanyourphone-app](https://github.com/jparedesDS/cleanyourphone-app)에 선택 사항인 Windows
앱이 있습니다. Early MVP이고 코드 서명이 없으며, 알려진 프로필에서만 계속합니다. 그 외의 모든
폰에서는 스킬이 여전히 경로입니다.

**폰 모델을 알리거나 피드백을 보내려면 어떻게 하나요?**
[웹 양식](https://cleanyourphone.org/#feedback), 앱의 **피드백**, 또는 스킬의
`scripts/feedback.py`를 사용하세요. 옵트인 방식이며 페이로드를 미리 보여 주고 시리얼, IP, IMEI,
MAC 주소를 제외합니다. [docs/FEEDBACK.md](docs/FEEDBACK.md)를 참고하세요.

## 기여

- 새 모델의 테스트된(`device`) 프로필: `profiles/<brand>/<model>.json`과 테스트 세부 정보를 담아
  PR을 여세요.
- `documented` 프로필: `scripts/dump_inventory.py`를 사용하고 `sources`에 기본 덤프를 인용하며
  `disable`은 비워 두세요.
- 가드, 파서, CLI 수정: `tests/`에 테스트를 추가하세요.
- 안전 규칙 변경: 먼저 이슈를 여세요. 그 규칙들이 곧 제품입니다.
- 직접 테스트할 수 없는 폰: 모델, Android, 빌드, fingerprint와 함께
  [프로필 요청](https://cleanyourphone.org/#feedback)을 보내세요. 시리얼과
  IP는 보내지 마세요.
- 브랜드나 로고 변경: 에셋을 바꾸기 전에 [docs/BRAND.md](docs/BRAND.md)를 읽으세요.
- 저장소를 변경하기 전에 [AGENTS.md](AGENTS.md)를 읽으세요.

## 라이선스

MIT. [LICENSE](LICENSE)를 참고하세요.
