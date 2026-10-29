# Maintainer scripts

These scripts are for people adding or reviewing profiles. They are **not** used by the skill at
runtime and they are not imported by `tools/phone.py`. They may make network requests to read public
firmware metadata.

## `dump_inventory.py`

Builds a documented-profile draft from an Android Dumps repository.

```bash
python scripts/dump_inventory.py \
  --project Android-Dumps/samsung/pa3q \
  --marketing-name "Galaxy S25 Ultra" \
  --out work/pa3q
```

It writes:

- `work/pa3q/inventory.json`: dump metadata, build props, and package candidates with the evidence
  path for each one.
- `work/pa3q/draft-profile.json`: a draft with `verification: "documented"`, `auto_apply: false`,
  `tested: []`, `disable: []` and an empty `ask` list.

Downloads are cached under `work/cache`. If GitLab returns HTTP 429, wait a minute, set
`GITLAB_TOKEN` to a personal access token, or reuse the cache with `--cache-dir`.

The draft is intentionally incomplete. Curate `ask` by hand, copy the file to
`profiles/<brand>/<id>.json`, remove the `_draft` block, and run:

```bash
python tools/phone.py validate
```

Do not commit a documented profile until every `ask` entry has a real `why` and `breaks` text and
every package appears in the dump inventory. Documented profiles are never auto-applied.
