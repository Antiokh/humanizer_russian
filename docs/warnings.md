# Warning severity

- `ARTIFACT`: reliable technical trace; default gate.
- `LANGUAGE_ERROR`: actual language error; default gate.
- `SEMANTIC_ERROR`: meaning/factual error; default gate.
- `NATIVE_WARNING`: native-usage candidate; never a gate by itself.
- `STYLE_WARNING`: contextual style candidate; never a gate by itself.
- `AI_PATTERN`: probabilistic pattern; never a gate by itself.
- `AUTHOR_MISMATCH`: corpus-based mismatch; never a gate by itself.

A warning becomes a rewrite only after contextual review confirms that the construction is not intentional and the rewrite does not damage a higher-priority layer.
