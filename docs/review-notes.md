# Pre-migration review notes

The old `Antiokh/humanizer--ru` PR #2 received an automated CodeRabbit review before the project moved here. The useful findings were treated as review input, not blindly applied.

## Applied

### Preserve document boundaries in author profiling

The profiler previously joined source documents before sentence and n-gram analysis. This could create a sentence/n-gram across two unrelated files. Fixed by aggregating these statistics per document.

### Do not emit source paths

Raw caller paths could expose usernames/home directories when a profile is shared. `corpus.files` was removed from generated profiles.

### One canonical profile contract

The old profiler/docs/schema had drifted. v1 is now defined by `profiles/schema.json`, emitted by `profile_author.py`, documented in `author-profile.md`, and validated in CI.

### Keep NATIVE_WARNING non-gating

Native-use findings are preferences, not proof of error. Only semantic/norm errors and reliable technical artifacts are automatic blockers.

### Cover `но` in repeated-common-material candidates

The linter now checks common repeated material across both `а` and `но` patterns, while remaining a soft warning.

### Update eval count

The Russian suite is documented through `ru-21`.

### Fix the zero-subject/ellipsis source mapping

A citation to a general preposition chapter did not support the exact combined claim. The normative reference now distinguishes zero-subject constructions from other ellipsis mechanisms and links them separately.

## Rejected

### “Only Business/Enterprise/Edu can create GPTs”

Rejected after checking current official OpenAI documentation. The current guidance says building/editing GPTs applies to paid ChatGPT users; managed workspaces can impose additional role/permission controls. The project therefore does not encode the narrower automated-review claim.

## Principle

Review comments are evidence to verify, not instructions to execute mechanically. This is especially important in a language-editing project where the core problem is already over-mechanical rule application.
