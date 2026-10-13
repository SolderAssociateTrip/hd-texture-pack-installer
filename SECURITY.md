# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.4.x   | yes       |
| 0.3.x   | security fixes only |
| < 0.3   | no        |

## Reporting a vulnerability

This tool extracts archives and writes files into game install
directories. The attack surface we care about:

- **Path traversal** in archive entries (`../../` escaping the target dir).
- **Zip-slip / tar-slip** via symlink or absolute-path members.
- **Manifest injection** where a pack manifest points writes outside the
  declared install root.
- **Privilege escalation** via a crafted `.hdtpi-cache` that redirects the
  staging dir to a protected path.

If you find one of these, email `security@hdtexturepack.dev` with a
reproducer. Do not open a public issue. We aim to acknowledge within 72
hours.

## What is out of scope

Packs that simply look bad, break game balance, or violate a game's EULA.
That's between the user and the game vendor.

## Hardening notes for pack authors

- Manifests must use relative paths only.
- No absolute symlinks in pack archives.
- Declare a `target_root` and keep every write inside it.