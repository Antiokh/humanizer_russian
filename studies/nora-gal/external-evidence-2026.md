# Nora Gal — external evidence audit (2026-08-19)

This document is a **modern evidence calibration layer**, not a replacement for the Nora Gal source study. `studies/nora-gal/claims.md` records what the supplied book argues; this file asks a separate question: **what can responsibly be asserted today without promoting a historical editorial judgment into current Russian `NORM`?**

The audit deliberately distinguishes:

- source-derived editorial method;
- current descriptive Russian linguistics;
- current normative/lexicographic evidence;
- empirical developmental/translation research;
- claims that are testable but have not yet been measured for this project;
- aesthetic or causal claims that should remain outside runtime truth claims.

No source below authorizes a detector score, blanket stop-list, grammatical degradation, or a universal rewrite rule.

## Status vocabulary

- `SUPPORTED_NARROWLY` — current evidence supports a narrower proposition than the source rhetoric.
- `REFINED_BY_CURRENT_LINGUISTICS` — the source observation has a useful core, but current Russian description requires explicit guards/variant structure.
- `REFINED_BY_CURRENT_USAGE/NORM` — modern lexical/normative practice rejects a source-level blanket rule while preserving a contextual question.
- `TESTABLE_NOT_YET_MEASURED` — a suitable corpus/method exists, but this project has not run the measurement; do not state the empirical conclusion.
- `OBSOLETE_AS_ABSOLUTE` — a historical technological/general claim is false as a present-day absolute, even though a narrower difficulty remains real.
- `NOT_ESTABLISHED_CAUSALLY` — the source makes or invites a causal/psychological inference not established by the evidence reviewed here.
- `SOURCE_METHOD` — useful editorial/professional workflow principle; external empirical confirmation is not required for its limited runtime role.
- `VALUE_JUDGMENT` — aesthetic/ethical position, not a machine-verifiable linguistic fact.

## Evidence matrix

| Claim | 2026 status | External evidence / boundary | Runtime consequence |
|---|---|---|---|
| `GAL-CLAIM-01` | `TESTABLE_NOT_YET_MEASURED` | The National Corpus of the Russian Language (NCRL/NKRЯ) explicitly provides representative written collections across centuries and genres, plus dedicated newspaper, social-media and spoken corpora. That makes register/time comparison feasible. **This audit did not measure diffusion of bureaucratic constructions**, so it does not confirm the source's prevalence/spread narrative. | Diagnose concrete bureaucratic constructions; do not claim that they are broadly “spreading” without a defined corpus query and result. |
| `GAL-CLAIM-02` | `REFINED_BY_CURRENT_USAGE/NORM` | Modern Russian normative infrastructure explicitly includes a **Dictionary of Foreign Words** among the dictionaries fixing norms of Russian as a state language. Gramota's 2026 guidance also distinguishes dictionary-attested foreign-origin words from excluded foreign wording in the relevant legal context. Origin alone therefore cannot be a general linguistic defect criterion. | Keep `GAL-BORROWING-FIT` contextual: exactness, audience, domain, register and established usage; never build a foreign-word stop-list. |
| `GAL-CLAIM-03` | `REFINED_BY_CURRENT_LINGUISTICS` + `TESTABLE_NOT_YET_MEASURED` | RusGram treats the gerund/converb as a productive grammatical form with detailed syntax, taxis, norm and text functions, including narrative, descriptive and poetic uses. Its corpus discussion also shows register-sensitive distributions. Current description therefore does not support a class-level “alien to living speech” ban. A narrower genre/frequency claim would require an explicit modern corpus comparison. | Preserve the current metric/clarity approach. Ban neither participles nor gerunds as classes; measure overload only where a surface proxy is defensible. |
| `GAL-CLAIM-04` | `REFINED_BY_CURRENT_LINGUISTICS` | RusGram describes information structure through theme/rheme **together with prosody and linear order**, and explicitly gives secondary structures with preposed/fronted rheme. Sentence-final focus is a useful tendency in some structures, not a universal placement rule. | Keep `GAL-FOCUS-WORD-ORDER` model/context-only; `NATIVE_USAGE` chooses focus from context. Never enforce “important information goes last.” |
| `GAL-CLAIM-05` | `NOT_ESTABLISHED_CAUSALLY` | The scoped modern review did not locate evidence that muddy/pretentious wording licenses a causal diagnosis of muddy thinking in the author. Readability, processing difficulty and conceptual clarity are separable research questions from the author's cognitive quality. | Diagnose the text only. Never infer intelligence, thought quality, honesty or personality from a stylistic finding. |
| `GAL-CLAIM-06` | `OBSOLETE_AS_ABSOLUTE` | Document-level literary machine translation is now an active empirical task. WMT/ACL work shows that LLMs can use document context and reduce some mistranslation, grammar and style inconsistencies, while critical errors and author-voice failures remain. 2025 human evaluation still finds published human literary translations consistently stronger and machine output often more literal/less diverse. | Do not assert that machines *cannot* do contextual literary translation. Also do not assert that the problem is solved. Treat context, omission and authorial voice as live quality risks. |
| `GAL-CLAIM-07` | `VALUE_JUDGMENT` | “A great translation ages mainly in details while the whole remains alive” is an evaluative historical proposition without a sufficiently operational modern metric in this project. | No runtime rule or quality score. It may motivate whole-text review, not empirical claims. |
| `GAL-CLAIM-08` | `SUPPORTED_NARROWLY` | Longitudinal work links the quantity and especially quality of caregiver linguistic input to later child vocabulary, and a 2021 meta-analysis reports positive associations between parental input quality/quantity and children's language skills. These studies support a developmental input claim, **not** the broader societal claim that adults' or books' language determines “the future of the language.” | Voice-age/tact rules may cite child-language development only narrowly. Do not use developmental evidence to moralize individual wording or predict language-wide historical outcomes. |
| `GAL-CLAIM-09` | `SOURCE_METHOD` | Variant comparison is a method explicitly represented in the source study. It does not depend on a contemporary empirical prevalence claim. | Supports A/B comparison and counterexample-driven eval design; does not define `NORM`. |
| `GAL-CLAIM-10` | `SOURCE_METHOD` | “Correct diagnosis does not guarantee a good first replacement” is an editorial workflow safeguard, not a statistical claim about Russian. | Preserve separation of finding vs operation and `GAL-EDITOR-THIRD-SOLUTION`. |
| `GAL-CLAIM-11` | `SUPPORTED_NARROWLY` | Modern translation research treats authorial/translator style as measurable rather than noise. Work on preservation of authorial style, translator-style adaptation, and literary MT evaluation all finds stylistic/authorial voice to be a distinct translation-quality dimension. This supports guarding against flattening authors. It does **not** prove a single universal profile of what a “strong translator” must do. | Preserve source/author voice as a contextual invariant. Do not force one Gal-like surface style across authors or genres. |
| `GAL-CLAIM-12` | `SUPPORTED_NARROWLY` | Parallel-corpus and literary-translation studies explicitly analyze non-literal translation techniques, restructuring and stylistic adaptations. Recent professional literary-translation research finds human translators use more non-literal strategies than MT post-editing in the studied material. This supports rejecting word-for-word/formal correspondence as a universal target; it does not establish a universal rule about how many words or which syntax every translation should use. | Word count, source syntax and surface similarity are not optimization targets by themselves. Preserve semantic/function constraints and evaluate form contextually. |
| `GAL-CLAIM-13` | `SOURCE_METHOD` | Checking a doubtful factual/cultural reference before “correcting” it is an epistemic/professional workflow rule. It does not require treating unfamiliarity as evidence of error. | `NEEDS_VERIFICATION` remains distinct from `CHANGE`; use external sources when available, otherwise do not guess. |
| `GAL-CLAIM-14` | `TESTABLE_NOT_YET_MEASURED` | NKRЯ supports diachronic and genre-controlled quantitative work, but “vocabulary impoverishment” is not yet an operational metric here. A defensible study would first define diversity/dispersion/register measures and comparable time/genre slices. | Keep broad decline/impoverishment rhetoric out of runtime and public product claims until a reproducible metric/query is defined and run. |
| `GAL-CLAIM-15` | `VALUE_JUDGMENT` | “Truth/humanity/tact” is an aesthetic/ethical editorial value. No machine-detectable linguistic property follows automatically from it. | Use only as a humility/intent guard; never emit a “humanity” or “truth” score. |

## Primary / authoritative evidence used

### Russian corpus and grammar

1. National Corpus of the Russian Language, **Состав и структура Корпуса**. The project describes its component corpora as large and representative collections for quantitative and qualitative linguistic research, with the main corpus spanning diverse written genres over more than three centuries.  
   https://ruscorpora.ru/page/corpora-structure/
2. National Corpus of the Russian Language, **О Корпусе**. The corpus covers historical and modern Russian in literary, conversational, vernacular and dialectal varieties.  
   https://ruscorpora.ru/page/corpora-about/
3. National Corpus of the Russian Language, current search interface. Used only to confirm that the corpus remains operational/current; **current counts are not used as evidence for any Gal claim** because corpus size changes.  
   https://ruscorpora.ru/search
4. E. V. Paducheva, **Коммуникативная структура предложения**, RusGram. Current project copy modified 2024-03-31. Theme/rheme is described as a pragmatic structure interacting with word order/prosody; fronted/preposed rheme is explicitly represented.  
   https://rusgram.ru/new/chapter/clauseintro/information_structure/
5. O. S. Bikkulova, **Деепричастие**, RusGram. Current project copy modified 2024-03-31. Describes formation, syntax, norm, taxis and text functions rather than treating the form as globally defective.  
   https://rusgram.ru/new/chapter/verbpar/converb/

### Current Russian normative/lexicographic context

6. Gramota.ru, **Нормативные словари, фиксирующие нормы современного русского литературного языка при его использовании в качестве государственного языка Российской Федерации**. The official list includes a Dictionary of Foreign Words.  
   https://gramota.ru/biblioteka/spravochniki/ofitsialno-o-russkom-yazyke/normativnye-slovari
7. Gramota.ru, answer №329949 (2026-02-12), explaining the four normative dictionaries relevant to the 2026 legal context, including the Dictionary of Foreign Words.  
   https://gramota.ru/spravka/vopros/329949

### Translation and literary-MT research

8. Karpinska, Marzena; Iyyer, Mohit (2023), **Large Language Models Effectively Leverage Document-level Context for Literary Translation, but Critical Errors Persist**, WMT/ACL.  
   https://aclanthology.org/2023.wmt-1.41/
9. Zhang, Ran; Zhao, Wei; Eger, Steffen (2025), **How Good Are LLMs for Literary Translation, Really? Literary Translation Evaluation with Humans and LLMs**, NAACL/ACL.  
   https://aclanthology.org/2025.naacl-long.548/
10. Lynch, Gerard (2014), **A Supervised Learning Approach Towards Profiling the Preservation of Authorial Style in Literary Translations**, COLING/ACL.  
    https://aclanthology.org/C14-1037/
11. Yirmibeşoğlu et al. (2023), **Incorporating Human Translator Style into English-Turkish Literary Machine Translation**, EAMT/ACL.  
    https://aclanthology.org/2023.eamt-1.40/
12. Macken, Lieve; Ruffo, Paola; Daems, Joke (2025), **The Role of Translation Workflows in Overcoming Translation Difficulties: A Comparative Analysis of Human and Machine Translation (Post-Editing) Approaches**, CTT/EAMT/ACL.  
    https://aclanthology.org/2025.ctt-1.1/
13. Zhai et al. (2020), **Building an English-Chinese Parallel Corpus Annotated with Sub-sentential Translation Techniques**, LREC/ACL. Documents human use of non-literal techniques such as idiom equivalence, generalization, particularization and semantic modulation.  
    https://aclanthology.org/2020.lrec-1.496/

### Child-language development

14. Rowe, Meredith L. (2012), **A longitudinal investigation of the role of quantity and quality of child-directed speech in vocabulary development**, *Child Development*, PMID 22716950.  
    https://pubmed.ncbi.nlm.nih.gov/22716950/
15. Anderson et al. (2021), **Linking Quality and Quantity of Parental Linguistic Input to Child Language Skills: A Meta-Analysis**, *Child Development*, PMID 33521953.  
    https://pubmed.ncbi.nlm.nih.gov/33521953/

## What this audit does *not* establish

### No corpus result for `GAL-CLAIM-01`

The existence of representative genre/time corpora proves **feasibility of testing**, not the claim that bureaucratese spreads from official registers into everyday language. To upgrade the status, the project needs a predeclared set of constructions, comparable periods/registers, normalization by corpus size and a reproducible result table.

### No corpus result for `GAL-CLAIM-03`

RusGram establishes that participles/gerunds are normal grammatical resources with register- and construction-specific behavior. It does not answer whether a particular density is perceived as “dry.” That requires a genre-controlled usage/readability study; the current runtime correctly treats density as a signal/metric, not an error.

### No “vocabulary decline” result for `GAL-CLAIM-14`

Lexical diversity depends on corpus composition, genre, token count, lemmatization, topic and sampling. Before testing “impoverishment,” the project must define an observable outcome (for example, lemma diversity/dispersion within matched genres) and avoid comparing incomparable corpora.

### No psychological diagnosis from `GAL-CLAIM-05`

This review did not find a basis for inferring the quality of a person's thinking from one textual style pattern. Even if future readability/processing evidence is added, that would still not license an author-level cognitive diagnosis without separate evidence.

## Corpus work still required

For the three empirical historical claims most worth testing (`01`, `03`, `14`), use this order:

1. write a falsifiable operational definition before querying;
2. choose comparable NKRЯ subcorpora by period and genre;
3. publish exact query strings / grammatical filters;
4. normalize frequencies by words/documents as appropriate;
5. manually inspect a sample for polysemy/false matches;
6. report confidence/limitations rather than only a direction of change;
7. keep the result outside `NORM` unless an independent normative source supports a norm claim.

Until those measurements exist, the statuses above are the strongest claims this project should make.
