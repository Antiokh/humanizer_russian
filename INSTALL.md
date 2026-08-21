# Install humanizer-russian as an Agent Skill

`humanizer_russian` is packaged as an Agent Skills directory named `humanizer-russian` with `SKILL.md` at its root. Do not assemble a runtime installation by copying a few individual files: the current runtime depends on library manifests, reviewers, rules and source-specific linters.

## Build the portable package

From the repository root:

```bash
python3 scripts/package_skill.py --output dist/humanizer-russian.zip
```

The packager uses `skill-package.json` as an allowlist. The ZIP contains one top-level `humanizer-russian/` directory and an internal `_package/manifest.json` with SHA-256 and byte size for every packaged file.

Build output is deterministic for the same repository state: CI builds the archive twice and requires byte-for-byte equality.

## Inspect without installing

```bash
python3 scripts/install_skill.py \
  dist/humanizer-russian.zip \
  --dest-root /tmp/unused \
  --inspect
```

Inspection verifies archive paths, the `SKILL.md` name, package inventory and checksums without writing a skill directory.

## Install into a local skills root

```bash
python3 scripts/install_skill.py \
  dist/humanizer-russian.zip \
  --dest-root ~/.local/share/agent-skills
```

This creates:

```text
~/.local/share/agent-skills/humanizer-russian/
```

The destination root is explicit because different Agent Skills clients use different discovery locations. Point `--dest-root` at the skills directory used by your client.

Existing installations are not overwritten by default. To replace an existing directory after validating the new package:

```bash
python3 scripts/install_skill.py \
  dist/humanizer-russian.zip \
  --dest-root ~/.local/share/agent-skills \
  --force
```

## Upload to a Skills-compatible product

Products that support uploading Agent Skills can be given `dist/humanizer-russian.zip` directly. The package follows the portable Agent Skills directory structure; it does not rely on a proprietary `.skill` extension.

## What the runtime package contains

The installable package contains the runtime instruction files, Compact and Editorial Board code, enabled knowledge libraries, reviewers, styles, runtime references, profiles/schemas, and evidence-provider manifests.

Development-only material is deliberately excluded, including:

- `.github/` workflows;
- `tests/` regression fixtures;
- `studies/` source-research material;
- `evals/` model-eval suites;
- `gpt/` Custom GPT development setup;
- benchmark/validation/model-eval developer scripts.

These exclusions are recorded in `skill-package.json` and checked after clean installation in CI.

## Project-only functionality

Evidence-provider designs that are not implemented are packaged only as `PROJECT` manifests so the roadmap remains visible. They cannot be enabled. An explicit request such as:

```bash
printf '%s' 'Тест.' | python3 scripts/review.py \
  --evidence normative_reference \
  --format json
```

must fail until that provider has been implemented, audited and explicitly promoted to `OPERATIONAL`.

## Smoke-test an installed copy

Run from the installed `humanizer-russian` directory:

```bash
printf '%s' 'Командой осуществляется проведение проверки.' \
  | python3 scripts/check.py --json

printf '%s' 'Это ошибка не в расчёте, а в исходных данных.' \
  | python3 scripts/review.py --format json
```

CI runs these commands from a fresh temporary installation rather than from the checkout that built the package.

## Spec validation

The clean installed directory is also checked with the Agent Skills `skills-ref` reference validator pinned to a known upstream commit. This catches frontmatter/name/directory-format drift independently of the project's own packager tests.
