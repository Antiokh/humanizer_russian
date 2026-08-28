# Suggested severity mapping

- Missing/invalid mandatory formal element under an active, applicable norm: `LANGUAGE_ERROR` is not appropriate; introduce or map to a formal/document error class.
- Broken internal reference with high-confidence parse: `HARD_GATE` / document-structure error.
- Use-before-definition or competing defined term: `REVIEW` unless unambiguously broken.
- Genre composition mismatch: `REVIEW`.
- Legal ambiguity: `REVIEW` unless semantic contradiction is provable.
- Stylistic bureaucratic heaviness: `STYLE_WARNING`, never a hard gate by itself.
