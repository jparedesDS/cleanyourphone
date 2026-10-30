<p align="center">
  <a href="https://jparedesds.github.io/cleanyourphone-web/">
    <img src="assets/banner.png" alt="CleanYourPhone" width="100%">
  </a>
</p>

<p align="center">
  <b>English</b> ·
  <a href="README.es.md">Español</a> ·
  <a href="README.pt-BR.md">Português (BR)</a> ·
  <a href="README.fr.md">Français</a> ·
  <a href="README.de.md">Deutsch</a> ·
  <a href="README.it.md">Italiano</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ko.md">한국어</a>
</p>

# CleanYourPhone

**불필요한 것을 뺀, 당신의 폰.** 코딩 에이전트를 위한 오픈소스·되돌릴 수 있는 Android 정리 Skill입니다. ADB로 사전 설치된 앱과 서비스를 비활성화합니다. root도, 커스텀 ROM도, 삭제도 필요 없고 명령 하나로 모두 되돌릴 수 있습니다.

[Website](https://jparedesds.github.io/cleanyourphone-web/) · [SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [Safety](docs/SAFETY.md) · [157 profiles](profiles/README.md)

## 빠른 시작

1. Android SDK Platform-Tools를 설치하고 <code>adb</code>를 PATH에 추가합니다.
2. 개발자 옵션과 USB 디버깅을 켜고 USB로 연결해 컴퓨터를 허용합니다.
3. 저장소를 clone해 에이전트에서 열거나 <code>SKILL.md</code>를 skills 폴더에 복사합니다.

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

## 안전

- 비활성화만 하고 삭제하지 않습니다. 유일한 상태 변경은 <code>pm disable-user</code>입니다.
- 첫 변경 전에 패키지, 설정, 역할, 키보드를 백업합니다.
- 보호 목록과 다이얼러, SMS, Home, 키보드 역할을 확인합니다.
- 5개씩 배치로 진행하고 재부팅 후 검증합니다.
- root, ROM, 계정, 텔레메트리, 외부 API가 없습니다.

## 문서

- [SKILL.md](SKILL.md) — the full procedure and safety rules.
- [PROMPT.md](PROMPT.md) — paste this if your agent does not load skills.
- [docs/SAFETY.md](docs/SAFETY.md) — protected packages, roles and restore.
- [profiles/README.md](profiles/README.md) — 157 model/firmware profiles.
- [README.md](README.md) / [README.es.md](README.es.md) — 전체 문서는 영어와 스페인어로 제공됩니다.

MIT. No account. No telemetry.
