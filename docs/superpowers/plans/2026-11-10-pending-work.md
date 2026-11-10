# Pending Work Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the existing 0.2.1 CLI to PyPI and remove the website's misleading app-download promises while the app is still an empty repository.

**Architecture:** Three repositories. `cleanyourphone` owns the PyPI release, install documentation and issue. `cleanyourphone-web` owns the bilingual copy and its tests. `cleanyourphone-app` gets only a status README. The GitHub social preview remains a manual repository setting.

**Tech Stack:** Python 3.10+, setuptools, GitHub Actions with OIDC, `unittest`, static HTML/CSS, GitHub CLI.

**Spec:** `docs/superpowers/specs/2026-11-10-pending-work-design.md`

## Global Constraints

- Publish version `0.2.1`; do not bump the version.
- PyPI project name is `cleanyourphone`; no API token is stored.
- Keep the claims **156 profiles** and **4 device-tested**.
- No invented app build, installer, download, date or test claim.
- Keep English/Spanish parity.
- Preserve the CSP, the JSON-LD hash, inline icons and the no-third-party-request rule.
- Website suite must stay at **27 tests**; the main suite goes from **109** to **110** after the docs test.
- Work from clean `main` in each repository.

## Review Focus

- Any app CTA must land on a real status README, never an empty repository, and must not say “Download”.
- `pipx install cleanyourphone` must work without Git or a token.
- English and Spanish must say the same thing and both must avoid download verbs.
- The website must keep its CSP hash valid and load no third-party requests.
- The GitHub social preview must change from the old upload, not just the repo file.

---

### Task 1: Add the app status README

**Files:**
- Create: `C:\Users\xht\Desktop\cleanyourphone-app\README.md`
- Test: none; verify the published raw URL and the copy.

**Interfaces:**
- Consumes: nothing.
- Produces: a public status page at `https://github.com/jparedesDS/cleanyourphone-app` that Task 2 links to.

- [ ] **Step 1: Clone the empty app repository**

Run:

```powershell
cd C:\Users\xht\Desktop
git clone https://github.com/jparedesDS/cleanyourphone-app.git
```

Expected: the directory is created. An empty-repository warning is fine.

Then make the local branch `main` so the first push matches GitHub:

```powershell
cd cleanyourphone-app
git branch -M main
```

- [ ] **Step 2: Create `README.md` with this exact content**

```markdown
# CleanYourPhone app

**Status: early MVP. There is no installer or public build yet.**

This repository will hold the optional local app for people who prefer buttons over prompts:
pick a profile, review every package, apply in small batches, and restore from the undo journal.
No root, no cloud, no telemetry.

The product available today is the agent skill:
[github.com/jparedesDS/cleanyourphone](https://github.com/jparedesDS/cleanyourphone).
The CLI lives in that repository too.

## Not available yet

- No installer.
- No public build.
- No release.

When the first build exists, it will be published in this repository's Releases.
```

- [ ] **Step 3: Verify the status copy is honest**

Run:

```powershell
python -c "from pathlib import Path; t=Path('README.md').read_text(encoding='utf-8'); assert 'No installer' in t; assert 'No public build' in t; assert 'Download' not in t; print('OK')"
```

Expected: `OK`.

- [ ] **Step 4: Commit and push**

```powershell
git add README.md
git commit -m "docs: add project status"
git push -u origin main
```

Expected: the empty repository now has a `main` branch with one commit.

- [ ] **Step 5: Verify the public URL**

```powershell
curl.exe -sS -o NUL -w "%{http_code}`n" https://raw.githubusercontent.com/jparedesDS/cleanyourphone-app/main/README.md
```

Expected: `200`.

---

### Task 2: Make the website app copy status-only

**Files:**
- Modify: `C:\Users\xht\Desktop\cleanyourphone-web\index.html`
- Modify: `C:\Users\xht\Desktop\cleanyourphone-web\es.html`
- Modify: `C:\Users\xht\Desktop\cleanyourphone-web\tests\test_site.py`

**Interfaces:**
- Consumes: the public app README from Task 1.
- Produces: app CTAs labelled `App status` / `Estado de la app`, linking to `https://github.com/jparedesDS/cleanyourphone-app`.

- [ ] **Step 1: Update the three website tests first**

In `tests/test_site.py`, replace the app-related assertions with these checks.

In `test_skill_first_hero_and_no_cli_section`, replace the `Download the app` ordering assertion with:

```python
        self.assertNotIn("Download the app", hero)
        self.assertIn("App status", hero)
        self.assertLess(hero.index("Open the skill"), hero.index("App status"))

        spanish = (ROOT / "es.html").read_text(encoding="utf-8")
        es_hero = spanish.split('<section class="hero">', 1)[1].split("</section>", 1)[0]
        self.assertNotIn("Descargar la app", es_hero)
        self.assertIn("Estado de la app", es_hero)
        self.assertLess(es_hero.index("Abrir la skill"), es_hero.index("Estado de la app"))
```

In `test_choose_path_puts_skill_before_app`, replace the `Download the app` assertion with:

```python
        self.assertIn("App · Early MVP", path)
        self.assertNotIn("Download the app", path)
        self.assertLess(path.index("Use the skill"), path.index("App · Early MVP"))

        spanish = (ROOT / "es.html").read_text(encoding="utf-8")
        es_path = spanish.split('id="start"', 1)[1].split("</section>", 1)[0]
        self.assertIn("App · MVP temprano", es_path)
        self.assertNotIn("Descargar la app", es_path)
        self.assertLess(es_path.index("Usa la skill"), es_path.index("App · MVP temprano"))
```

Replace `test_app_is_labelled_early_mvp` with:

```python
    def test_app_is_labelled_early_mvp(self):
        for name, label, note in (
            ("index.html", "Early MVP", "no installer yet"),
            ("es.html", "MVP temprano", "aún sin instalador"),
        ):
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertIn(label, text)
                self.assertIn(note, text)
                self.assertIn("cleanyourphone-app", text)
                self.assertNotIn("Download the app", text)
                self.assertNotIn("Descargar la app", text)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```powershell
python -m unittest discover -s tests -p "test_site.py" -v
```

Expected: three failures naming `Download the app` or the status labels.

- [ ] **Step 3: Replace the hero app CTA in both pages**

`index.html` — change the hero button to use the `i-app` icon and the label `App status`:

```html
<a class="button button-ghost" href="https://github.com/jparedesDS/cleanyourphone-app" rel="noopener"><svg class="icon" aria-hidden="true" focusable="false"><use href="#i-app"/></svg> App status</a>
```

`es.html` — same change with `Estado de la app`:

```html
<a class="button button-ghost" href="https://github.com/jparedesDS/cleanyourphone-app" rel="noopener"><svg class="icon" aria-hidden="true" focusable="false"><use href="#i-app"/></svg> Estado de la app</a>
```

- [ ] **Step 4: Replace the app card copy in both pages**

In `index.html`, change the card title, paragraph, button and note to:

```html
<h3>App, still in development</h3>
<p>The app is the simple path for people who prefer buttons over prompts. It is still in development; there is no installer yet. The first build will be published in the app repository.</p>
<a class="button button-ghost" href="https://github.com/jparedesDS/cleanyourphone-app" rel="noopener"><svg class="icon" aria-hidden="true" focusable="false"><use href="#i-app"/></svg> App status</a>
<p class="path-note">Early MVP · no installer yet</p>
```

In `es.html`, change the same block to:

```html
<h3>La app, aún en desarrollo</h3>
<p>La app es el camino sencillo para quien prefiere botones a prompts. Aún está en desarrollo; todavía no hay instalador. La primera compilación se publicará en el repositorio de la app.</p>
<a class="button button-ghost" href="https://github.com/jparedesDS/cleanyourphone-app" rel="noopener"><svg class="icon" aria-hidden="true" focusable="false"><use href="#i-app"/></svg> Estado de la app</a>
<p class="path-note">MVP temprano · aún sin instalador</p>
```

- [ ] **Step 5: Replace the final CTA app button**

In `index.html`, change the final CTA paragraph and button to:

```html
<p>Give the skill to your agent. The app is still in development.</p>
...
<a class="button button-ghost" href="https://github.com/jparedesDS/cleanyourphone-app" rel="noopener"><svg class="icon" aria-hidden="true" focusable="false"><use href="#i-app"/></svg> App status</a>
```

In `es.html`, use:

```html
<p>Dale la skill a tu agente. La app aún está en desarrollo.</p>
...
<a class="button button-ghost" href="https://github.com/jparedesDS/cleanyourphone-app" rel="noopener"><svg class="icon" aria-hidden="true" focusable="false"><use href="#i-app"/></svg> Estado de la app</a>
```

Leave the footer `App` link unchanged; it now reaches the README from Task 1.

- [ ] **Step 6: Run the website suite**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: `Ran 27 tests ... OK`.

- [ ] **Step 7: Preview desktop and mobile**

Run:

```powershell
npx --yes playwright screenshot -b chromium --channel chrome --viewport-size "1440,1000" --full-page "file:///C:/Users/xht/Desktop/cleanyourphone-web/index.html" C:\Users\xht\AppData\Local\Temp\opencode\app-status-desktop.png
npx --yes playwright screenshot -b chromium --channel chrome --viewport-size "390,844" --full-page "file:///C:/Users/xht/Desktop/cleanyourphone-web/index.html" C:\Users\xht\AppData\Local\Temp\opencode\app-status-mobile.png
```

Expected: no horizontal overflow; the app card reads as in development and has no download verb.

- [ ] **Step 8: Commit, push and verify the live page**

```powershell
git add index.html es.html tests/test_site.py
git commit -m "site: describe the app as in development"
git push origin main
```

Then wait for the Pages workflow:

```powershell
gh run list --limit 2
gh run watch <pages-run-id> --exit-status
curl.exe -sS -L "https://jparedesds.github.io/cleanyourphone-web/?v=appstatus" | Select-String -Pattern "Download the app|App status|Descargar la app|Estado de la app"
```

Expected: only `App status` and `Estado de la app` appear; the download strings are absent.

---

### Task 3: Publish 0.2.1 to PyPI

**Files:**
- No repository files. This is a GitHub Actions run.
- Human prerequisite: PyPI pending publisher fields.

**Interfaces:**
- Consumes: the `v0.2.1` tag and `.github/workflows/publish.yml`.
- Produces: `cleanyourphone==0.2.1` on PyPI for Task 4.

- [ ] **Step 1: Human configures the PyPI pending publisher**

In PyPI: **Publishing → Add a new pending publisher** with:

| Field | Value |
|---|---|
| PyPI project | `cleanyourphone` |
| Owner | `jparedesDS` |
| Repository | `cleanyourphone` |
| Workflow name | `publish.yml` |
| Environment | `pypi` |

Do not run the workflow until this exists.

- [ ] **Step 2: Confirm the workflow is available**

Run:

```powershell
gh workflow view publish.yml --repo jparedesDS/cleanyourphone
```

Expected: the workflow is listed and has a manual trigger.

- [ ] **Step 3: Run the workflow from the release tag**

```powershell
gh workflow run publish.yml --repo jparedesDS/cleanyourphone --ref v0.2.1
```

- [ ] **Step 4: Watch the run**

```powershell
gh run list --repo jparedesDS/cleanyourphone --workflow publish.yml --limit 1
gh run watch <run-id> --repo jparedesDS/cleanyourphone --exit-status
```

Expected: the run succeeds.

If the OIDC exchange fails, stop. Fix the pending publisher fields and re-run; do not update the documentation.

- [ ] **Step 5: Verify the PyPI metadata**

```powershell
python -c "import json, urllib.request; d=json.load(urllib.request.urlopen('https://pypi.org/pypi/cleanyourphone/json')); print(d['info']['version'])"
```

Expected: `0.2.1`.

- [ ] **Step 6: Install from PyPI in a clean environment**

```powershell
python -m venv C:\Users\xht\AppData\Local\Temp\opencode\cyp-pypi-venv
C:\Users\xht\AppData\Local\Temp\opencode\cyp-pypi-venv\Scripts\python -m pip install --upgrade pip
C:\Users\xht\AppData\Local\Temp\opencode\cyp-pypi-venv\Scripts\pip install cleanyourphone==0.2.1
C:\Users\xht\AppData\Local\Temp\opencode\cyp-pypi-venv\Scripts\cleanyourphone --version
C:\Users\xht\AppData\Local\Temp\opencode\cyp-pypi-venv\Scripts\cleanyourphone validate
```

Expected: `CleanYourPhone 0.2.1` and `OK: 156 profile(s) valid.`

---

### Task 4: Point the install documentation at PyPI

**Files:**
- Create: `C:\Users\xht\Desktop\cleanyourphone\tests\test_docs.py`
- Modify: `C:\Users\xht\Desktop\cleanyourphone\README.md:144`
- Modify: `C:\Users\xht\Desktop\cleanyourphone\README.es.md:145`
- Modify: `C:\Users\xht\Desktop\cleanyourphone\docs\CLI.md:25`
- Modify: `C:\Users\xht\Desktop\cleanyourphone\CHANGELOG.md` under `[Unreleased]`

**Interfaces:**
- Consumes: the verified PyPI release from Task 3.
- Produces: public install instructions that use `pipx install cleanyourphone`.

- [ ] **Step 1: Write the failing documentation test**

Create `tests/test_docs.py`:

```python
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocsTest(unittest.TestCase):
    def test_public_install_uses_pypi(self):
        for name in ("README.md", "README.es.md", "docs/CLI.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(document=name):
                self.assertIn("pipx install cleanyourphone", text)
                self.assertNotIn(
                    "pipx install git+https://github.com/jparedesDS/cleanyourphone.git",
                    text,
                )
```

- [ ] **Step 2: Run the test to verify it fails**

```powershell
python -m unittest discover -s tests -p "test_docs.py" -v
```

Expected: FAIL because the three documents still contain the Git URL.

- [ ] **Step 3: Replace the install commands**

In `README.md`, `README.es.md` and `docs/CLI.md`, replace:

```text
pipx install git+https://github.com/jparedesDS/cleanyourphone.git
```

with:

```text
pipx install cleanyourphone
```

In `docs/CLI.md`, also replace the now-stale sentence:

```text
With [pipx](https://pipx.pypa.io/), from a clone or directly from GitHub:
```

with:

```text
From PyPI with [pipx](https://pipx.pypa.io/):
```

Leave the wheel and editable-install examples in `docs/CLI.md` unchanged.

- [ ] **Step 4: Add the release line to the changelog**

Under `## [Unreleased]`, add:

```markdown
- Published to PyPI: `pipx install cleanyourphone` installs the CLI and the `cyp` alias.
```

Note: the PyPI project page builds its long description from the tagged `README.md`. It will keep
the Git command until the next release; do not rewrite the `v0.2.1` tag for this.

- [ ] **Step 5: Run the docs test and the full suite**

```powershell
python -m unittest discover -s tests -p "test_docs.py" -v
python -m unittest discover -s tests -v
```

Expected: the docs test passes; the full suite reports `Ran 110 tests ... OK`.

- [ ] **Step 6: Commit and push**

```powershell
git add tests/test_docs.py README.md README.es.md docs/CLI.md CHANGELOG.md
git commit -m "docs: install from PyPI"
git push origin main
```

- [ ] **Step 7: Watch CI**

```powershell
gh run list --repo jparedesDS/cleanyourphone --workflow ci.yml --limit 1
gh run watch <run-id> --repo jparedesDS/cleanyourphone --exit-status
```

Expected: CI succeeds.

---

### Task 5: Upload the social preview

**Files:**
- No repository files.
- Asset: `C:\Users\xht\Desktop\cleanyourphone\assets\social-preview.png`

**Interfaces:**
- Consumes: the current 1280×640 purple/white/graphite social preview.
- Produces: the GitHub repository's uploaded social preview.

- [ ] **Step 1: Human uploads the image**

GitHub → `jparedesDS/cleanyourphone` → **Settings** → **Social preview** → **Edit** → upload
`assets/social-preview.png`.

- [ ] **Step 2: Verify the Open Graph image changed**

```powershell
curl.exe -sS -L "https://github.com/jparedesDS/cleanyourphone" | Select-String -Pattern "og:image"
```

Expected: the `og:image` URL no longer contains the old hash
`9866565e-2746-4b17-b891-aa6205b936b4`.

If it is unchanged, wait a minute and repeat; do not change repository files.

---

### Task 6: Close the PyPI issue

**Files:**
- No repository files.

**Interfaces:**
- Consumes: Tasks 3 and 4.
- Produces: issue #1 closed with the verification evidence.

- [ ] **Step 1: Comment with the exact verification**

```powershell
gh issue comment 1 --repo jparedesDS/cleanyourphone --body '0.2.1 is published on PyPI. Verified in a clean venv: `pip install cleanyourphone==0.2.1`; `cleanyourphone --version` reports 0.2.1 and `cleanyourphone validate` reports 156 valid profiles. README, README.es and docs/CLI now use `pipx install cleanyourphone`.'
```

- [ ] **Step 2: Close the issue**

```powershell
gh issue close 1 --repo jparedesDS/cleanyourphone
gh issue view 1 --repo jparedesDS/cleanyourphone --json state --jq .state
```

Expected: `CLOSED`.

---

### Task 7: Final verification

**Files:**
- No changes.

**Interfaces:**
- Consumes: all previous tasks.
- Produces: a verified, clean handoff.

- [ ] **Step 1: Verify all repositories are clean**

```powershell
git -C C:\Users\xht\Desktop\cleanyourphone status --short
git -C C:\Users\xht\Desktop\cleanyourphone-web status --short
git -C C:\Users\xht\Desktop\cleanyourphone-app status --short
```

Expected: no output from any command.

- [ ] **Step 2: Run both test suites and the profile validator**

```powershell
cd C:\Users\xht\Desktop\cleanyourphone
python -m unittest discover -s tests -v
python tools\phone.py validate

cd C:\Users\xht\Desktop\cleanyourphone-web
python -m unittest discover -s tests -v
```

Expected: `Ran 110 tests ... OK`, `OK: 156 profile(s) valid.`, `Ran 27 tests ... OK`.

- [ ] **Step 3: Verify the public surfaces**

```powershell
curl.exe -sS -L "https://jparedesds.github.io/cleanyourphone-web/?v=final" | Select-String -Pattern "Download the app|App status|Descargar la app|Estado de la app"
curl.exe -sS -L "https://github.com/jparedesDS/cleanyourphone-app" | Select-String -Pattern "no installer|Not available yet"
python -c "import json, urllib.request; d=json.load(urllib.request.urlopen('https://pypi.org/pypi/cleanyourphone/json')); print(d['info']['version'])"
```

Expected: only status labels on the website, the app README is reachable, and PyPI reports `0.2.1`.
