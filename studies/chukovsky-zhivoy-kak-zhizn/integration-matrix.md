# Integration matrix — Chukovsky → current `humanizer_russian`

Created only after the independent study re-audit passed.

Automation vocabulary follows `AGENTS.md` and `docs/source-integration-runbook.md`.

## Summary

- rules classified: `38 / 38`;
- `HARD_GATE`: `0`;
- `DEFAULT_MECHANICAL`: `0`;
- `EXTENDED_SOFT`: `7`;
- `METRIC_ONLY`: `2`;
- `MODEL_ONLY`: `29`.

Project classes:

- `NORM`: 4;
- `NATIVE_USAGE`: 7;
- `EDITING`: 23;
- `AUTHOR`: 4;
- `AI_CALQUE`: 0;
- `ARTIFACT`: 0.

The zero `DEFAULT_MECHANICAL` count is intentional. The source mostly supplies contextual distinctions, preservation rules and editing A/B tests. A surface trigger is not promoted to default merely because it is easy to regex.

## Matrix

| Rule | Source locator | Project class | Automation | Surface trigger / feasible mechanic | Required context | FP risk | Positive case | Natural negative / boundary | Existing overlap | NATIVE_USAGE conflict risk | Runtime plan |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R01 | `L68-L168`, `L286-L313` | NORM | MODEL_ONLY | novelty/time markers are not decisive | current norm + date/register | high | verify unfamiliar form before correction | genuinely new error can still be wrong | evidence-audit | purism may erase current living usage | current-authority check only when needed |
| R02 | `L286-L313`, `L652-L664`, `L1178-L1203` | EDITING | MODEL_ONLY | none reliable | mechanism: semantic shift/ellipsis/jargon/error/etc. | high | classify `зафиналить` before verdict | classification does not acquit malformed form | rule-audit | premature class ban | model routing step |
| R03 | `L468-L488`, `L2473-L2582` | NATIVE_USAGE | MODEL_ONLY | etymology wording can only surface discussion | current conventional meaning | high | preserve lexicalized current meaning | fresh pleonasm/collision still editable | partial russian-language | literal “repair” can damage idiom/usage | lexicalization check |
| R04 | `L369-L376` | NATIVE_USAGE | MODEL_ONLY | missing constituent cannot be judged by regex | discourse/coreference + genre | high | keep recoverable ellipsis | context-poor/safety/legal text may require explicitness | strong native-russian | over-expansion destroys context economy | preserve if safely recoverable |
| R05 | `L369-L379` | NATIVE_USAGE | MODEL_ONLY | no reliable surface distinction | current valency/lexical sense + context | high | do not invent complement for reanalysed verb | true contextual ellipsis remains possible | partial russian-language | fabricated object changes meaning | lexical/valency fork |
| R06 | `L665-L1000`, `L937-L949` | EDITING | MODEL_ONLY | foreign token detection is not a verdict | audience + term precision + domain | high | keep precise established term | opaque prestige borrowing may be replaced/glossed | code-switching guidance | “purifying” can reduce precision | term A/B |
| R07 | `L922-L936` | EDITING | MODEL_ONLY | acronym/term shape only candidate | target audience knowledge | high | expand once for onboarding | expert runbook need not explain API repeatedly | partial author/audience | oversimplification can erase domain distinctions | audience decision |
| R08 | `L937-L949`, `L1195-L1210`, `L1562-L1588` | EDITING | MODEL_ONLY | register lexeme lists are insufficient | speaker + addressee + genre + purpose | high | informalize accidental officialese | deliberate parody/characterization may mix registers | Nora voice + author | normalization can erase scene/voice | scene-first check |
| R09 | `L1122-L1140`, `L1178-L1210` | EDITING | EXTENDED_SOFT | tokenizer/regex: 4+ uppercase acronym clusters | audience + first-use expansion + establishment | medium-high | surface 3+ opaque abbreviations for review | established domain acronyms may be optimal | little existing coverage | automatic expansion adds noise | source linter; never default |
| R10 | `L1178-L1203`, `L1291-L1307` | EDITING | MODEL_ONLY | category words in request, not text property | concrete item + uptake/context | high | judge formation item-by-item | structurally allowed coinage can still be bad | rule-audit anti-ban | class-wide cleanup destroys living formations | guardrail only |
| R11 | `L1371-L1396` | AUTHOR | MODEL_ONLY | slang/pro markers can be surfaced but intent cannot | speaker identity + scene | high | preserve mechanic/gamer/teen voice | neutral narrator may not need same vocabulary | Nora voice + author-profile | sterilization destroys voice | author/scene layer |
| R12 | `L1483-L1500` | AUTHOR | MODEL_ONLY | single slang token is explicitly insufficient | corpus + independent evidence | extreme | report register without person diagnosis | one `жесть` proves nothing about intellect/morality | author-profile policy | moralizing native speech | inference boundary |
| R13 | `L1471-L1494` | EDITING | MODEL_ONLY | no trustworthy surface causal signal | causal evidence outside text | extreme | describe linguistic symptom only | token does not prove social/psych cause | semantics/no-invention | invented causal story | inference boundary |
| R14 | `L1562-L1580` | EDITING | MODEL_ONLY | formal formula detection cannot prove function | official/legal/admin genre | high | retain functional official wording | same wording can leak into private chat | missing explicit positive rule | conversationalization can break institutional function | genre preservation |
| R15 | `L1572-L1588`, `L1650-L1698` | EDITING | EXTENDED_SOFT | conservative cluster across multiple bureaucratic marker families | genre + irony + technical context | medium-high | dense nonfunctional officialese → review | one `в рамках` / routine technical wording is insufficient | Nora voice partial | false positive can over-colloquialize business text | source linter; cluster only |
| R16 | `L1650-L1698` | EDITING | MODEL_ONLY | prestige classifiers cannot be safely enumerated | referent taxonomy/legal/technical distinction | high | ordinary exact noun if classifier adds nothing | `медицинское изделие` may be a real category | missing | simplification can change extension | semantic A/B |
| R17 | `L1880-L1946`, `L1970-L2008` | EDITING | EXTENDED_SOFT | regex/tokenizer: light verb + nominalization; nominalization cluster | event roles + agent availability | medium-high | surface `осуществляется проведение...` for reconstruction | `Проверка оборудования обязательна` can be functional | rule-audit partial | blanket verbification can invent actor/change focus | source linter; soft only |
| R18 | `L1744-L1756` | EDITING | EXTENDED_SOFT | small candidate lexeme list for subtraction test | scope/contrast/degree/time/stance/prosody | high | `имеющиеся ошибки` → compare without modifier | `критические ошибки` must keep restriction | missing | deletion can erase information | source linter; A/B only |
| R19 | `L1780-L1815`, `L2017-L2041`, `L4463-L4470` | EDITING | EXTENDED_SOFT | repeated phrase/function proxies, phrase-family clustering | document function + semantic gain | medium-high | repeated generic praise → review | one cliché-like collocation with real content is fine | AI cluster heuristics partial | random synonymization can worsen native text | source linter + AI-family threshold correction |
| R20 | `L1744-L1778` | AUTHOR | MODEL_ONLY | cliché token cannot infer sincerity | independent speaker/context evidence | extreme | keep psychological conclusion out of edit | sincere emotion may use conventional phrase | missing | moral/psychologizing rewrite | inference boundary |
| R21 | `L1738-L1756`, `L2017-L2063`, `L2088-L2103` | EDITING | MODEL_ONLY | generic evaluators can be surfaced but proposition recovery is semantic | source/input evidence | high | lead with observed fact already in source | never invent “specificity” absent in source | Nora specificity | fake detail is worse than abstraction | proposition-first + no-invention |
| R22 | `L1880-L1911`, `L1970-L1988`, `L2135-L2159`, `L2400-L2472` | EDITING | METRIC_ONLY | token/statistical: repeated long-word endings, density metrics | intended rhythm + technical terminology | high if judged | expose echo count for read-aloud | technical morphology may naturally repeat endings | missing | automatic smoothing can flatten cadence | metrics only; no finding |
| R23 | `L1880-L1946` | EDITING | MODEL_ONLY | dependency parser could surface ambiguous attachments; regex case-count rejected | syntax + semantic roles | high | reconstruct actor/action/object before rewrite | multiple genitives can be perfectly clear | rule-audit rejects counts | forced simplification can change roles | future dependency experiment; model now |
| R24 | `L1940-L1962` | EDITING | EXTENDED_SOFT | exact announcing-frame phrases | modality + warning hierarchy + navigation | medium | `Следует отметить, что...` → deletion A/B | `Важно:` warning hierarchy may be functional | existing AI list misclassified | deleting particles/metadiscourse can change pragmatic force | source linter; remove AI attribution |
| R25 | `L1948-L1968` | EDITING | EXTENDED_SOFT | repeated procedural verb + `вопрос` packaging | whether referent really is issue/topic/question | medium-high | repeated `проработать вопрос...` → review | one genuine `поставить вопрос` can be exact | missing | direct rewrite may change speech act | source linter; require repetition |
| R26 | `L2042-L2063` | EDITING | MODEL_ONLY | repeated sentence skeletons are only proxies | subject-specific evidence + document task | high | differentiate objects by actual properties | comparison matrix may intentionally use same schema | author/template partial | forced variation harms clarity | document-level model |
| R27 | `L2088-L2103` | EDITING | MODEL_ONLY | generic interpretation markers insufficient | primary object/source + inference boundary | high | separate observation from interpretation | evaluation/criticism can itself be required | Nora specificity | “grounding” must not fabricate evidence | model-only |
| R28 | `L2135-L2159`, `L2660-L2677` | EDITING | MODEL_ONLY | no defensible richness scalar | genre + voice + purpose | extreme | improve dead but correct prose when evidence supports | formally simple text can be exactly right | core architecture | synonym diversity pressure creates fake prose | meta quality rule |
| R29 | `L2343-L2400`, `L2473-L2582` | NATIVE_USAGE | MODEL_ONLY | lexicalized idiom dictionary needed; antonym regex rejected | current conventional meaning | high | preserve established conventional oddity | fresh semantic nonsense not protected | missing/Nora boundary | literal cleanup damages idiom | lexicalization guard |
| R30 | `L2400-L2449`, `L4463-L4470` | NATIVE_USAGE | MODEL_ONLY | repetition counts cannot decide function | emphasis/rhythm/idiom/history in passage | high | preserve expressive repetition | mechanical stamp may still be dead | native intentional-repeat rule | aggressive dedup destroys emphasis | preservation model |
| R31 | `L2400-L2472` | EDITING | METRIC_ONLY | suffix/ending/rhythm statistics only | semantics + intended prosody | high if judged | compare readings after semantic edit | repeated endings may be technical/expressive | missing | “euphony score” would be pseudo-linguistics | metrics/read-aloud aid only |
| R32 | `L2583-L2630` | NATIVE_USAGE | MODEL_ONLY | phraseology lexicon could help but free regex cannot | lexicalized idiom status + current usage | high | process fixed idiom as whole | non-idiomatic fresh metaphor still compositional | Nora needs boundary | synonym replacement can break idiom | idiom boundary in reference/model |
| R33 | `L2605-L2671` | AUTHOR | MODEL_ONLY | deviation from idiom can be detected only with lexicon, not intent | recoverable base + authorial effect | extreme | preserve motivated deformation | accidental blend may need correction | Nora humor partial | canonicalization erases joke/voice | model-only |
| R34 | `L2648-L2671` | EDITING | MODEL_ONLY | candidate idiom mismatch requires phraseology + semantics | intention/effect/context | extreme | compare play vs contamination hypotheses | unresolved is allowed | Nora collocation/metaphor partial | overcorrection of creative language | model-only |
| R35 | `L2759-L4146`, caveats `L2762-L2777`, notes `L4147-L4530` | NORM | MODEL_ONLY | historical pair lookup only creates candidate | current authoritative norm + register | high | verify item before correction | historical “wrong” form may now be accepted/variant | evidence-audit | old prescription can fight current native use | current-source verification |
| R36 | `L2762-L2768` | NORM | MODEL_ONLY | professional label alone insufficient | current authoritative source + community | high | preserve verified professional variant in-domain | do not export it to general speech | professional jargon partial | generalization creates false norm | scoped norm lookup |
| R37 | `L2769-L2777` | NATIVE_USAGE | MODEL_ONLY | informal markers cannot define situation | relationship + scene + intent | high | keep plausible familiar wording | familiar speech is not free from semantics/norm | author/native informal | formalization can destroy relationship signal | scene model |
| R38 | `L2276-L2342`, `L2660-L2677` | NORM | MODEL_ONLY | no surface substitute for evidence | current norm evidence + scope | high | intuition raises question, authority supports mandate | taste alone is not correction | evidence-audit | arbitrary purism can suppress native usage | meta gate for all NORM promotion |

## Automation consequences

### HARD_GATE

None. The book contributes no rule that is both reliably machine-decidable and publication-blocking without external/contextual interpretation.

### DEFAULT_MECHANICAL

None in this integration cycle. The existing default checker remains unchanged.

### EXTENDED_SOFT

`R09, R15, R17, R18, R19, R24, R25`.

All findings must use `EDITING_SUGGESTION`, never `LANGUAGE_ERROR`, `AI_PATTERN` or publication failure solely on this source.

### METRIC_ONLY

`R22, R31`.

Mechanical output may count ending/suffix echo and nominalization density, but no threshold may be labeled bad Russian, cancelearite, AI writing or poor style without calibration/context.

### MODEL_ONLY

All remaining 29 rules. Several could benefit from future morphology/dependency/phraseology tooling, but the current project must not fake semantic certainty with regex.

## Core compatibility decision

No Chukovsky rule may override:

- current `NORM`;
- recoverable ellipsis/context economy;
- natural information structure;
- functional repetition;
- pragmatic particles;
- intentional parcellation;
- professional/author register;
- current author profile.

When conflict remains after scope narrowing, `NATIVE_USAGE`/`AUTHOR` outrank the book's `EDITING` recommendation under the repository architecture.
