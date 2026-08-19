# Completeness, loss and overgeneralization audit

Study state: **AUDITED** for the supplied EPUB fingerprint. Runtime/library integration is a separate later pass.

## Source-completeness gate

- 35/35 OPF spine documents were read sequentially.
- 30 content-bearing documents are `VERIFIED`.
- 5 structural/title documents are `NO_OPERATIONAL_CONTENT`.
- 34/34 NCX navPoints are mapped.
- Both non-TOC spine continuations (`ch1-7.xhtml`, `ch1-29.xhtml`) were explicitly read.
- Inaccessible/unread source parts: **none**.

Therefore the study satisfies the framework's strict chapter/source coverage gate for this file. It does **not** assert equivalence to every print edition.

## Loss audit

The second pass rechecked each content-bearing spine document for decision-relevant distinctions, not just chapter summaries.

### «Для ясности»

Preserved: the book is practical and example/comparison driven, not an exhaustive theory; an editor must compare variants and preserve both meaning and living language. Lost-by-simplification risk: turning examples into a complete blacklist.

### «Откуда что берется?» / «Жечь или сушить?»

Preserved: chancery is a system (nominalization, noun chains, passive, pseudoformality, stamps), while grammatical forms themselves are not uniformly forbidden. Event order and agent visibility are separate dimensions. Lost-by-simplification risk: `nominalization/passive/participle = error`.

### «Словесная алгебра»

Preserved: concreteness is desirable only when supplied by context; generic containers can hide meaning; literal pronoun/general-noun patterns from another language can over-explicitate Russian. Lost-by-simplification risk: inventing specificity or banning abstract nouns.

### «А если без них?» + unlisted `ch1-7.xhtml` + «Куда же идет язык?»

Preserved: borrowing concerns are about function, register and audience, but Gal also expresses historically strong purist judgments. Crucial limiting idea preserved: there are no globally bad words; placement/function matters. Lost-by-simplification risk: `foreign word = error`.

### «Мертвый хватает живого»

Preserved: lexical precision, exact collocation, marked/rare-word fit and register; a rare word can be excellent. Historical claims about vocabulary decline are separated into claims audit. Lost-by-simplification risk: replacing rare vocabulary with neutral vocabulary.

### «Туманы…»

Preserved: long sentences are legitimate if their structure remains graspable; foreign syntactic frames need Russian restructuring; sentence boundaries and word order carry function. The source's emphasis on sentence-final stress is not universalized. Lost-by-simplification risk: length thresholds or `important = sentence-final`.

### «Не своим голосом»

Preserved: persona, situation, internal monologue, age, explicitness and relationship are distinct. Oral/internal speech may need different syntax from narration. Lost-by-simplification risk: one generic colloquial voice or blind subject/pronoun deletion.

### «Веревка — вервие простое»

Preserved: scientific/technical precision and accessibility can coexist; terminology is not the enemy, pseudo-scientific surrounding language is the target. Lost-by-simplification risk: replacing technical terms with imprecise everyday words.

### «Мистер с аршином»

Preserved: cultural/era fit and the danger of target-culture idioms that create the wrong world; also the opposite guard — domestication can be functional. Lost-by-simplification risk: banning all local idioms in translation.

### «На ножах»

Preserved: image-system collision, accidental literalization, polysemy, physical plausibility and sound effects are separate but interacting mechanisms. Lost-by-simplification risk: `mixed metaphor = always error` without intentionality/context.

### «Свинки замяукали»

Preserved: accidental idiom contamination differs from deliberate transformation and wordplay; functional equivalence matters more than literal structure. Lost-by-simplification risk: automatically normalizing playful idioms.

### «Предки Адама»

Preserved: uncertain references must be checked rather than guessed; editor ignorance is not proof of source error; jokes/intentional distortion are possible. Lost-by-simplification risk: treating verification need as a correction verdict.

### «Когда глохнет душа»

Preserved: emotional tact is contextual, not moral censorship; a semantically possible word can be tonally cruel/trivializing, while deliberate coldness/cynicism must remain possible. Lost-by-simplification risk: making all grave topics solemn.

### «Сотри случайные черты…»

Preserved: whole-before-detail, cumulative character drift, POV consistency, physical visualization and emotional temperature. Lost-by-simplification risk: optimizing each sentence independently.

### «Мадам де Займи и другие»

Preserved: names/puns are functions, not merely strings; translation may require compensation or another solution; not every proper name should be translated. Lost-by-simplification risk: universal name localization.

### «Буква…» / «… Или Дух?»

Preserved: context beats first dictionary meaning; Russian syntax and focus may require structural departure from the source; rhythm/word order matter; editor can seek a third solution. Historical claims about machine translation are quarantined. Lost-by-simplification risk: surface equivalence as fidelity.

### «Кто мы и зачем мы?»

Preserved: editor-not-dictator, distinction between real defect and taste, third solution, preserving valid unusual words, self-edit after changes. Lost-by-simplification risk: treating reviewer preference as mandatory CHANGE.

### «SOS!»

Preserved: multiple local defects can form a systemic/compound failure; local patching can be inferior to reconstruction from the semantic skeleton. Lost-by-simplification risk: summing warnings into a detector score or using compound failure as license to rewrite freely.

### «Поклон мастерам» / «Уходя, оставить свет…»

Preserved: positive model of adapting translator surface manner to the author; whole-style fidelity; individual translator voice must not overwrite author voice. Lost-by-simplification risk: one universal house voice.

### «Открытие Хэмингуэя» + unlisted `ch1-29.xhtml`

Preserved: restraint/subtext, context-sensitive lexical choice, rhythmic equivalence, functional omission/repetition. Strong positive evidence against a generic `repetition = bad` rule. Lost-by-simplification risk: explicating subtext or deleting purposeful repetition.

### «Многоликость таланта»

Preserved: the same translator can render radically different voices; meaningful grammatical/lexical irregularity of characters can require functional rather than form-identical reproduction; sound/wordplay/rhythm interact. Lost-by-simplification risk: normalization of marked character speech.

### «От миссис Уоррен до Маугли»

Preserved: stage speakability, speaker-specific voice, child/animal perspective, viewpoint-relative lexical choice, anti-sweetening guard. Lost-by-simplification risk: generic «natural dialogue» detached from character and medium.

### «От Джойса до Голсуорси»

Preserved: register-specific voice, child information structure, context-driven omission, functional repetition and whole-character rendering. Lost-by-simplification risk: treating repeated words or unusual child forms as defects.

### «Свет и сумрак Фицджеральда»

Preserved: tonal/image continuity across the whole novel, character development through small lexical choices, rhythm as carrier of unease and change. Lost-by-simplification risk: maximizing local vividness while flattening the arc.

### «Музыка перевода» / «Пять чувств — и еще шестое»

Preserved: rhythmic/sound equivalence may require different word count/syntax; child language especially exposes false formality/sweetening; emotional tact and «truth» are limits on mechanical editing. Lost-by-simplification risk: word-count fidelity, numeric rhythm rules, deliberate baby talk.

## Overgeneralization audit — rejected stronger rules

The full source does **not** justify any of the following universal rules:

1. foreign word = error;
2. passive = error;
3. participle or gerund = error;
4. nominalization = error;
5. long sentence = error;
6. important information must always be sentence-final;
7. rare/archaic word = bad style;
8. idiom deformation = error;
9. metaphor collision is always accidental;
10. repetition = bad style;
11. explicit expression is always clearer;
12. children must speak with deliberate grammatical errors;
13. editor's first replacement is authoritative;
14. translation-specific advice automatically applies to original Russian;
15. more vivid wording is always better;
16. every ambiguity should be removed;
17. a suspicious reference should be corrected from memory;
18. a surface regex hit proves a contextual editing defect;
19. several style warnings can be added into a meaningful quality/AI score;
20. the book itself defines current academic `NORM`.

## Preservation audit

The source-layer must explicitly preserve at least these natural/intentional cases:

- functional passive with unknown/unimportant agent;
- clear participial/deverbal constructions;
- professional borrowings and exact specialist terms;
- intentional official/cold register;
- rare but precise words;
- long clear periods;
- strong sentence-initial focus;
- functional parceling;
- intentional lexical/syntactic repetition;
- character-specific irregular speech;
- deliberate mixed imagery, surrealism and wordplay;
- purposeful POV system and ambiguity;
- subtext and emotional restraint;
- author-valid wording that the editor merely dislikes.

The canonical `evals/nora-gal.json` contains original project positive/preservation/context cases and is mapped to all 42 rules by `evals/nora-gal-map.json`.

## Claims requiring modern/external work

See `claims.md`. In particular, current runtime must not rely on unverified historical statements about borrowing prevalence, language decline, conversational participle/gerund frequency, child-language causality, or historical machine translation. If any becomes product-facing factual guidance, it needs appropriate modern corpus/normative/research verification.

## Remaining study limitations

- Exact print edition and stable page numbers: unresolved.
- Model-judge performance on contextual rules: not yet measured by an actual model run.
- Modern corpus calibration of historically conditioned claims: deliberately not performed as part of source extraction.

## Completion verdict

There are **no inaccessible or unread source parts** in the supplied EPUB. All decision-relevant distinctions found during the sequential pass are represented in concepts, 42 atomic rules, interactions, claims, preservation cases and this loss/overgeneralization audit. The source study is therefore ready for a separate architecture integration pass.