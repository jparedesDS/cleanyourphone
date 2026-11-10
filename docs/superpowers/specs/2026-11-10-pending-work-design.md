# Pending work: distribution and app honesty

Date: 2026-11-10

## Goal

Close the public distribution gaps without starting the app MVP: publish the existing CLI release
to PyPI, point the repository install instructions at PyPI, stop presenting an empty app repository
as a downloadable product, and give the app repository an honest status page.

## Why now

- PyPI returns 404, so the documented install still uses a Git URL.
- The website says “Download the app” in the hero, the path card and the final CTA, and all three
  links lead to an empty repository.
- The app repository is empty, so “runs locally from source” is not true yet.
- The GitHub social preview still points to the previous upload.
- The brand sync is complete; these are the remaining public-facing gaps.

## Goals

1. `pipx install cleanyourphone` installs 0.2.1 from PyPI.
2. `README.md`, `README.es.md` and `docs/CLI.md` use the PyPI command.
3. The website labels the app “Early MVP” and links to a status page, never a download.
4. `cleanyourphone-app` has a README that states what is not available yet.
5. The GitHub social preview uses `assets/social-preview.png`.

## Non-goals

- Building the app MVP, publishing app source or creating an installer.
- New profiles, new device testing or a new CLI version.
- A custom domain, analytics or new website sections.
- Rewriting historical changelog entries.
- Refreshing the PyPI long description; it is generated from the tagged README and updates with the
  next release.

## Constraints

- Keep the 156 profiles and 4 device-tested claims.
- No invented downloads, user counts, dates or test claims.
- Keep English/Spanish parity.
- Preserve the CSP, the JSON-LD hash, inline icons and the no-third-party-request rule.
- PyPI uses OIDC trusted publishing; no API token is stored.
- Publish the existing `v0.2.1` tag; do not bump the version.

## Approaches

### A. Publish 0.2.1 and make the app status-only (chosen)

Publish the tested 0.2.1 tag, update the install documentation, add a status README to the app
repository, and change app CTAs to “App status”. This keeps the optional-app story without
pretending a build exists.

### B. Remove the app from the site until it exists

Simpler and impossible to mislead, but it throws away the secondary path and the existing copy.
Revisit when the app ships.

### C. Build the app MVP now

Solves the empty repository but is a separate product project with UI, packaging, releases and
testing. It is not part of closing distribution.

## Decisions

- Publish from tag `v0.2.1`.
- Use “App status” / “Estado de la app” instead of “Download the app”.
- Add `README.md` to `cleanyourphone-app`; do not add app code.
- The social preview remains a manual GitHub setting because no upload API exists.
- Close issue #1 after PyPI and the documentation are verified.

## Risks and mitigations

- Pending publisher mismatch: verify the five fields before running; stop on an OIDC failure.
- Website claims: tests assert the download verbs are absent and the status labels are present.
- Spanish drift: update both pages and assert both languages.
- Social preview cache: verify that the `og:image` hash changes and recheck after a short wait.
