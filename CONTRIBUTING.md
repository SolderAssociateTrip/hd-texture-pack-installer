# Contributing to hd-texture-pack-installer

Thanks for wanting to help the tater ship HD retextures. This repo is a
service-oriented Python desktop tool for installing, validating, and
applying HD texture packs into supported game installs on Windows.

## Ground rules

- One service, one responsibility. Handlers stay thin; business logic
  lives in `src/hdtpi/services/`.
- Platform-specific code goes in `src/hdtpi/adapters/`. Never import
  Windows-only APIs from a service directly — go through an adapter.
- Every public service method gets a type-annotated signature and a
  docstring stating inputs, outputs, and error modes.
- No blocking I/O on the UI thread. Handlers dispatch to services; services
  may run work on the executor pool.

## Dev setup

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest -q
```

## Adding a new pack format

1. Add a parser under `src/hdtpi/parsers/`.
2. Register it in `src/hdtpi/parsers/registry.py`.
3. Add fixtures under `tests/fixtures/`.
4. Cover the happy path and one malformed-manifest path.

## Commit style

Conventional commits. `feat:`, `fix:`, `refactor:`, `test:`, `docs:`.
Keep the subject line under 72 chars.

## Reporting texture conflicts

If a pack overwrites engine-native textures in a way that breaks LOD
chains, open an issue with the pack name, target game, and the offending
manifest entry. Attach the `--dry-run` output.