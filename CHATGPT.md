# Humanizer Russian in ChatGPT / Codex

The repository is packaged as a **skill-only plugin** and as a GitHub plugin marketplace.

## Marketplace source

Use the repository itself as the marketplace source:

```text
https://github.com/Antiokh/humanizer_russian
```

The marketplace manifest is located at:

```text
.claude-plugin/marketplace.json
```

The plugin manifest is located at:

```text
.claude-plugin/plugin.json
```

The plugin exposes the repository root as the `humanizer-russian` Agent Skill, whose canonical instructions are in `SKILL.md`.

## Import in ChatGPT workspaces that support GitHub marketplaces

Open:

```text
Workspace settings → Plugins → Add → Import marketplace
```

Use:

```text
Source: https://github.com/Antiokh/humanizer_russian
Path:   <leave empty>
Branch: main
```

After import, install/enable `humanizer-russian` for the eligible role.

The repository is public, so no repository-specific GitHub permission is required beyond the GitHub connection used by the importer.

## Invocation

When the plugin/skill is available in the current surface, requests can explicitly name it, for example:

```text
Прогони этот текст через Humanizer Russian.
```

or use the plugin/skill picker where the product exposes it.

## Product availability

GitHub marketplace import and Agent Skills availability depend on the ChatGPT plan, workspace role, and product surface. Packaging this repository as a plugin makes it importable where those features are supported, but it does not bypass plan-level restrictions in ChatGPT Plus or older chat surfaces.

Where direct skill installation is not available but GitHub repository access is available, an agent can still load `SKILL.md` and the repository resources explicitly and apply the workflow from source.

## Updating

The marketplace points to the repository itself. Workspaces using GitHub marketplace sync can pull future updates from `main` without repackaging the skill manually.
