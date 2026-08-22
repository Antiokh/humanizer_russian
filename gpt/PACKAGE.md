# Custom GPT package

`humanizer_russian` has two distribution formats:

- Agent Skill: `dist/humanizer-russian.zip` from `scripts/package_skill.py`;
- full Custom GPT package: `dist/humanizer-russian-gpts.zip` from `scripts/package_gpt_runtime.py`.

The Custom GPT build reuses the existing Knowledge bundler, then adds a self-contained Code Interpreter runtime generated from the same `skill-package.json` allowlist as the Agent Skill package.

## Build

```bash
python3 scripts/package_gpt_runtime.py --output dist/humanizer-russian-gpts.zip
```

Optional unpacked copy:

```bash
python3 scripts/package_gpt_runtime.py \
  --output dist/humanizer-russian-gpts.zip \
  --directory dist/humanizer-russian-gpts
```

Inspect:

```bash
python3 scripts/package_gpt_runtime.py --inspect dist/humanizer-russian-gpts.zip
```

## Archive layout

```text
humanizer-russian-gpts/
├── Instructions/
│   ├── INSTRUCTIONS.md
│   ├── GPT_BUILDER.md
│   ├── CONVERSATION_STARTERS.md
│   └── TESTS.md
├── Knowledge/
│   ├── 00_INDEX.md
│   ├── 01_RUSSIAN_LANGUAGE.md
│   ├── 02_NATIVE_RUSSIAN.md
│   ├── 03_NORA_GAL.md
│   ├── 04_CHUKOVSKY.md
│   ├── 05_ILYAKHOV.md
│   ├── 06_VISSON.md
│   ├── 07_ROSENTHAL.md
│   ├── 08_GOLUB.md
│   ├── 09_AUTHOR_PROFILE.md
│   ├── 10_AUDITS_AND_CORRECTIONS.md
│   ├── 11_EDITORIAL_BOARD.md
│   ├── 12_STYLES.md
│   ├── 13_CAPABILITIES_AND_STATUS.md
│   └── 14_ADDITIONAL_REFERENCE.md  # when needed
├── Runtime/
│   └── humanizer_runtime.py
├── README.md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
└── _manifest.json
```

## What to upload to GPT Builder

1. Paste `Instructions/INSTRUCTIONS.md` into **Instructions**.
2. Upload every `.md` file from `Knowledge/`.
3. Upload `Runtime/humanizer_runtime.py`.
4. Enable **Code Interpreter & Data Analysis**.
5. Copy conversation starters if desired.
6. Run `humanizer_runtime.py verify` and the Preview cases from `Instructions/TESTS.md` before publishing.

The current package uses 15 Knowledge files + 1 runtime file = **16 GPT uploads**, below the 20-file GPT limit.

## Runtime contents

`humanizer_runtime.py` is generated; it is not a second handwritten implementation. It embeds the deterministic Agent Skill ZIP produced from `skill-package.json`, so it carries the supported runtime scripts and data together:

- `check.py`, `review.py`, `lint.py`;
- all current `lint_*` entrypoints for Russian, native usage, Chukovsky, Ilyakhov, Gal, Visson, Rosenthal and Golub;
- Editorial Board and author-profile runtime;
- normalized libraries, reviewers, styles, references, schemas and evidence runtime data included by the Agent Skill allowlist.

The launcher verifies the embedded ZIP hash, can verify every embedded file against the Agent Skill manifest, and compiles every embedded Python file.

## Runtime commands

```bash
python3 humanizer_runtime.py verify
python3 humanizer_runtime.py list
python3 humanizer_runtime.py check --json text.md
python3 humanizer_runtime.py check --extended --json text.md
```

Additional commands listed by `list` expose the packaged review/lint entrypoints.

## Truthfulness boundary

The GPT may say that a mechanical pass ran only after Code Interpreter actually executed `humanizer_runtime.py`. Knowledge-only reasoning is not a deterministic run.

Evidence providers marked `PROJECT` remain unavailable even though the generic evidence runtime module is present in the embedded Agent Skill payload.

## CI guarantees

The GPT package workflow must:

- build the final archive twice and byte-compare it;
- keep the total GPT-upload set at 20 files or fewer;
- run `humanizer_runtime.py verify`;
- compare packaged-runtime `check --json` output and exit code against the repository's direct `scripts/check.py` for both mechanical and extended modes;
- upload the exact tested ZIP as the workflow artifact.
