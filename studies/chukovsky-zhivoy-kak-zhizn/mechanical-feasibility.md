# Mechanical feasibility pass — Chukovsky

Date: `2026-08-19`  
Branch: `chukovsky`

This pass occurs after the independent study and integration matrix, and before any prompt/reference expansion.

Method order tried conceptually for every rule:

`regex → tokenizer/structure → morphology → dependency/statistical check → metric → MODEL_ONLY`

A cheap signal is accepted only when it can surface a useful candidate without pretending to decide the contextual rule.

## Rule-by-rule feasibility

| Rule | Mechanical path tried | Result | Why / implementation boundary |
|---|---|---|---|
| R01 | token novelty/frequency/date heuristics | MODEL_ONLY | unfamiliarity does not establish current norm; requires current authority and register |
| R02 | lexical-shape classifier | MODEL_ONLY | innovation type can be semantic shift, ellipsis, jargon, error, register, etc.; surface form is insufficient |
| R03 | etymology markers / lexicon | MODEL_ONLY | current lexicalized meaning is a semantic/usage question; a lexicon could assist later but cannot be inferred by regex |
| R04 | missing-constituent regex | MODEL_ONLY | recoverability requires discourse/coreference and genre |
| R05 | valency lexicon/morphology | MODEL_ONLY | morphology can identify verb form, but ellipsis vs lexical reanalysis requires current sense and context |
| R06 | Latin/English-token detection | MODEL_ONLY | origin does not decide semantic work or audience fit |
| R07 | tokenizer + acronym/term detection | MODEL_ONLY | reader knowledge is contextual; only R09 gets a separate soft acronym-density surface candidate |
| R08 | register marker lexicon | MODEL_ONLY | isolated lexical labels produce excessive false positives; speaker/addressee/genre/purpose required |
| R09 | regex/tokenizer for 4+ uppercase acronyms; count unique forms | EXTENDED_SOFT | surface density can cheaply raise an audience-effort review, but cannot decide opacity or required expansion |
| R10 | word-formation suffix/prefix classifier | MODEL_ONLY | the source explicitly rejects class-wide verdicts; actual item uptake/function is contextual |
| R11 | slang/professional lexicon | MODEL_ONLY | token can surface register but cannot decide whether it carries speaker identity/voice |
| R12 | slang-token count | MODEL_ONLY | source itself blocks person-level inference from isolated marker; no mechanical personality verdict |
| R13 | causal cue phrases | MODEL_ONLY | language does not contain enough evidence for extra-linguistic causation in general |
| R14 | official-formula lexicon | MODEL_ONLY | detection cannot decide whether genre function is genuinely official/legal/administrative |
| R15 | regex families + cluster threshold | EXTENDED_SOFT | require multiple markers from at least two relatively distinctive families; one ordinary business phrase is insufficient |
| R16 | abstract/classifier noun list | MODEL_ONLY | semantic extension/taxonomy/legal distinction must be compared; stop-list would corrupt technical language |
| R17 | light-verb + deverbal-noun regex; tokenizer suffix count | EXTENDED_SOFT | useful event-reconstruction candidate only; never “nominalization = error”; unknown actor must not be invented |
| R18 | small high-confidence modifier candidate list | EXTENDED_SOFT | only invokes semantic-subtraction A/B; final deletion depends on scope/contrast/degree/time/stance/prosody |
| R19 | phrase-family matching + repeated hit threshold | EXTENDED_SOFT | repetition can surface possible template behavior; final repeated discourse function remains contextual |
| R20 | cliché dictionary | MODEL_ONLY | cliché does not mechanically establish sincerity/insincerity |
| R21 | generic evaluative lexicon | MODEL_ONLY | recovery of source-supported proposition requires source/input semantics; mechanical rewrite risks invented specificity |
| R22 | token endings / repetition statistics | METRIC_ONLY | read-aloud quality is contextual; emit descriptive echo metrics only, never a verdict/finding |
| R23 | morphology/dependency parser | MODEL_ONLY | dependency tooling could later surface alternative attachments; regex case counts explicitly rejected |
| R24 | exact announcing-frame phrase list | EXTENDED_SOFT | cheap candidate for with/without A/B; preserve warning hierarchy, modality, navigation, contrast |
| R25 | procedural-verb + `вопрос` regex + repetition threshold | EXTENDED_SOFT | repeated shell can be surfaced; a genuine issue/topic/question remains valid |
| R26 | sentence-template statistics | MODEL_ONLY | similar skeleton may be deliberate comparison; subject individuality requires semantic evidence |
| R27 | discourse-marker list | MODEL_ONLY | grounding an interpretation requires primary object/source and inference tracking |
| R28 | lexical-diversity/readability metrics | MODEL_ONLY | source provides no defensible scalar “richness/liveliness” threshold; metrics would be pseudo-objective |
| R29 | antonym/collision regex; idiom lexicon | MODEL_ONLY | antonym pairs are often fully normal; lexicalized vs fresh incoherence requires semantics. Old collision regex rejected |
| R30 | repetition count | MODEL_ONLY | repeated material may be expressive, conventional, rhythmic or dead; function is decisive |
| R31 | suffix/ending/rhythm statistics | METRIC_ONLY | mechanics can expose echo candidates/counts, not aesthetic quality or correction mandate |
| R32 | phraseology lexicon + morphology | MODEL_ONLY | a future lexicon may assist recognition, but lexicalization/current variant status and context still decide |
| R33 | phraseology deviation detector | MODEL_ONLY | base idiom may be detectable, intentional effect is not |
| R34 | phraseology candidate matching | MODEL_ONLY | intentional play vs contamination needs two-hypothesis contextual reasoning; unresolved is allowed |
| R35 | historical lookup table | MODEL_ONLY | table can identify candidate only; current authoritative verification required item-by-item |
| R36 | professional variant lexicon | MODEL_ONLY | must be current and scoped to a community; requires authoritative/current evidence |
| R37 | informal-marker detection | MODEL_ONLY | relationship and situation determine familiar-register fit |
| R38 | none | MODEL_ONLY | meta-rule: mandatory normalization needs reproducible evidence; cannot be reduced to a surface pattern |

## Accepted mechanical surface checks

Seven source rules become `EXTENDED_SOFT` candidates:

1. `R09` — abbreviation-density candidate;
2. `R15` — bureaucratic-register cluster;
3. `R17` — light verb + nominalization / dense nominalization candidate;
4. `R18` — modifier semantic-subtraction candidate;
5. `R19` — evaluative/template cluster;
6. `R24` — announcing metadiscourse deletion test;
7. `R25` — repeated `вопрос` procedural packaging.

They all emit `EDITING_SUGGESTION`. None enters default `scripts/check.py`.

## Accepted metrics

Two rules contribute descriptive metrics only:

- `R22` / `R31`: ending/suffix echo / read-aloud candidate statistics;
- R17 additionally contributes nominalization counts/density as descriptive metrics, although its narrow light-verb surface pattern can emit an extended suggestion.

No numeric threshold is interpreted as “bad Russian”, AI generation or cancelearite.

## Rejected mechanical candidates

The following tempting implementations are explicitly rejected:

- case/genitive counts for R23;
- antonym pair regexes (`наличие/отсутствие`, `сила/слабость`) for R29;
- one formal marker as cancelearite for R15;
- bare `-ние/-ция` count as an error for R17;
- one cliché-like phrase as R19;
- suffix echo as style defect for R22/R31;
- slang tokens as personality/intellect signal for R12;
- foreign-origin token as defect for R06;
- historical dictionary pair as current automatic correction for R35.

## Precision policy for the source module

The Chukovsky linter must prefer under-triggering over noisy “linguistic” automation. Its output is a list of places where a specific editing comparison should be run, not a substitute for the comparison itself.

`DEFAULT_MECHANICAL` remains unchanged: `0` Chukovsky-specific rules in this cycle.
