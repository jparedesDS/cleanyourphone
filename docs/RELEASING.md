# Releasing CleanYourPhone

The version has one source of truth: `VERSION` in `tools/phone.py`. `pyproject.toml` reads it with
`setuptools.dynamic`, so do not bump the version in two places.

## Checklist

1. Start from a clean `main`:

   ```bash
   git pull --ff-only
   git status --short
   ```

2. Bump `VERSION` in `tools/phone.py` (for example `0.2.0` to `0.3.0`).

3. Add the release to `CHANGELOG.md` with the date and a link to the tag. Keep `[Unreleased]` at the
   top.

4. If profiles changed, rebuild the catalog:

   ```bash
   python scripts/update_profile_docs.py
   ```

5. Run the checks:

   ```bash
   python -m unittest discover -s tests -v
   python tools/phone.py validate
   python tools/phone.py --help
   python tools/phone.py protected
   python tools/phone.py profiles
   python tools/phone.py wizard --help
   ```

6. Build and test the exact artifacts:

   ```bash
   python -m pip install build
   python -m build
   python -m pip install --force-reinstall dist/*.whl
   cleanyourphone --version
   cleanyourphone validate
   ```

7. Commit, tag and push:

   ```bash
   git add -A
   git commit -m "release: vX.Y.Z"
   git tag -a vX.Y.Z -m "CleanYourPhone X.Y.Z"
   git push origin main
   git push origin vX.Y.Z
   ```

8. Create the GitHub release with curated notes. The `Release assets` workflow builds the wheel and
   sdist and attaches them to the release automatically.

9. Publish to PyPI. This is a one-time setup, then one workflow run per release.

   On PyPI, go to **Publishing → Add a new pending publisher** and use:

   | Field | Value |
   |---|---|
   | PyPI project | `cleanyourphone` |
   | Owner | `jparedesDS` |
   | Repository | `cleanyourphone` |
   | Workflow name | `publish.yml` |
   | Environment | `pypi` |

   Then open **Actions → Publish to PyPI → Run workflow**. The workflow uses GitHub OIDC and
   `pypa/gh-action-pypi-publish`; no API token is stored in the repository.

   Verify from a clean environment:

   ```bash
   pipx install cleanyourphone
   cleanyourphone --version
   cleanyourphone validate
   ```

10. Update the website:

    - Bump `softwareVersion` in `index.html` and `es.html`.
    - Recompute the CSP `sha256` hash for the JSON-LD block. The site test
      `test_csp_hash_matches_json_ld` fails if it is stale.
    - If the install command changes from the Git URL to PyPI, update both pages, `README.md`,
      `README.es.md` and `docs/CLI.md`.
    - Run `python -m unittest discover -s tests` in `cleanyourphone-web`, then commit and push. The
      Pages workflow deploys automatically.

11. After the release, check:

    - CI and the tag run are green.
    - The GitHub release has the wheel and sdist.
    - `pipx install cleanyourphone` works.
    - The website shows the new version and install command.
    - `CHANGELOG.md`, `README.md` and the catalog agree on the profile count.

## If PyPI is not configured yet

The GitHub release is still a complete distribution: the wheel and sdist are attached, and the
documented install works:

```bash
pipx install git+https://github.com/jparedesDS/cleanyourphone.git
```

Do not run the `Publish to PyPI` workflow until the pending publisher exists; it will fail at the
OIDC exchange.
