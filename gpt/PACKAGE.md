# Custom GPT package

`humanizer_russian` has two separate distribution formats:

- Agent Skill package: `dist/humanizer-russian.zip` from `scripts/package_skill.py`;
- Custom GPT package: `dist/humanizer-russian-gpts.zip` from `scripts/package_gpt.py`.

They are not interchangeable.

## Build

```bash
python3 scripts/package_gpt.py --output dist/humanizer-russian-gpts.zip
```

Optional unpacked copy:

```bash
python3 scripts/package_gpt.py \
  --output dist/humanizer-russian-gpts.zip \
  --directory dist/humanizer-russian-gpts
```

Inspect an existing archive:

```bash
python3 scripts/package_gpt.py --inspect dist/humanizer-russian-gpts.zip
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
│   └── 14_ADDITIONAL_REFERENCE.md  # only when needed
├── README.md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
└── _manifest.json
```

## GPT Builder

1. Paste the contents of `Instructions/INSTRUCTIONS.md` into the GPT **Instructions** field.
2. Upload every Markdown file from `Knowledge/` into GPT **Knowledge**.
3. Copy the suggested name, description, capabilities and setup notes from `Instructions/GPT_BUILDER.md`.
4. Copy conversation starters from `Instructions/CONVERSATION_STARTERS.md` if desired.
5. Run the cases from `Instructions/TESTS.md` in Preview before publishing.

The packager keeps the Knowledge upload set at 20 files or fewer. It combines source references, canonical normalized rule libraries, reviewer definitions, style profiles, corrections and capability status into text-forward Markdown bundles.

## Runtime boundary

Custom GPT Knowledge is reference material. This archive intentionally does not pretend to install the Python mechanical runtime. The generated Instructions explicitly forbid claiming that `check.py`, Editorial Board runtime code or evidence providers ran unless a real external execution surface/action actually executed them.

Evidence providers with status `PROJECT` remain unavailable.

## Excluded material

The GPT package excludes CI, evals, development tests, source-study corpora, executable scripts, schemas used only for runtime validation, and `references/native-russian-user-context.md`.

The Agent Skill package remains the correct distribution when executable runtime behavior is required.
