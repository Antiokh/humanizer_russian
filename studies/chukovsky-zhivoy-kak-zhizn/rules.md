# Atomic rules — independent extraction from «Живой как жизнь»

Status: `EXTRACTED`.

These rules are intentionally expressed without mapping them to existing project rule classes. `Level` uses the neutral severity vocabulary from the book-study framework. Examples and counterexamples are original to this study.

---

## CHK-R01 — Separate current norm from generational taste

Source locator: `SRC:L68-L168`, `SRC:L286-L313`  
Scope: general; word/phrase; historical/current usage  
Basis: `SOURCE_REPEATED`  
Level: probable usage problem / unresolved question  
Confidence: high

### Что проверяет
Whether rejection of a form is based on current evidence or merely on the editor's older linguistic habit.

### Почему это важно
The book repeatedly shows once-shocking forms becoming ordinary.

### Семантический/функциональный инвариант
Do not change meaning merely to restore the editor's remembered norm.

### Trigger / признаки
`так раньше не говорили`; `звучит новомодно`; unfamiliar recent form.

### Диагностика
Is the objection synchronic or autobiographical? Is the form established beyond a narrow novelty cohort?

### Возможные исправления
Keep; mark as time/register-specific; verify current norm/usage before changing.

### Не применять автоматически
A genuinely nonstandard form can also be new.

### Do not infer
New = correct; old = obsolete.

### Взаимодействует с
CHK-R02, R03, R35.

### Positive example
`созвониться после релиза` is not rewritten solely because an older editor dislikes `созвониться`.

### Counterexample
A newly coined malformed case form still requires normative checking.

### Verification
The decision can be justified without reference to the editor's age or personal memory.

---

## CHK-R02 — Classify an innovation before judging it

Source locator: `SRC:L286-L313`, `SRC:L652-L664`, `SRC:L1178-L1203`  
Scope: word/phrase; general  
Basis: `SOURCE_REPEATED`  
Level: unresolved question  
Confidence: high

### Что проверяет
What kind of phenomenon a novel form is: lexical innovation, semantic shift, ellipsis, jargon, abbreviation, professional form, error, or register choice.

### Почему это важно
Blanket “language disease” diagnoses collapse unlike mechanisms.

### Семантический/функциональный инвариант
Preserve the phenomenon's actual function before choosing a remedy.

### Trigger / признаки
Unfamiliar word/meaning/form; categorical request to ban a class of forms.

### Диагностика
What changed: meaning, form, valency, audience, register, or only familiarity?

### Возможные исправления
Route to the relevant diagnostic rather than immediate replacement.

### Не применять автоматически
Classification does not itself establish acceptability.

### Do not infer
Every innovation belongs to a healthy language-development process.

### Взаимодействует с
R01, R04, R05, R06, R09, R11.

### Positive example
Before changing `зафиналить`, identify it as professional slang/code-switching rather than “incorrect Russian” by default.

### Counterexample
`инциндент` is not rescued merely by labeling it a “new form”; it is a norm candidate requiring verification.

### Verification
The edit rationale names the mechanism, not only the disliked token.

---

## CHK-R03 — Do not derive current meaning from historical meaning alone

Source locator: `SRC:L468-L488`, `SRC:L2473-L2582`  
Scope: word/phrase; diachronic semantics  
Basis: `SOURCE_DIRECT`  
Level: probable usage problem  
Confidence: high

### Что проверяет
Whether an objection depends only on etymology or an obsolete meaning.

### Почему это важно
Semantic change and bleaching make literal historical decomposition unreliable.

### Семантический/функциональный инвариант
Preserve the conventional current meaning.

### Trigger / признаки
`буквально это означает...`; objection based on root/origin.

### Диагностика
Is the old image still active for ordinary speakers? Does current usage establish a conventional meaning?

### Возможные исправления
Keep the current conventional form; verify modern usage if transition is incomplete.

### Не применять автоматически
Fresh accidental pleonasm or contamination is not protected by ancient semantic change.

### Do not infer
Etymology is irrelevant to all lexical analysis.

### Взаимодействует с
R29, R32, R34, R35.

### Positive example
Do not reject a conventional expression merely because one component historically denoted something incompatible with the literal scene.

### Counterexample
A newly invented phrase that accidentally duplicates the same concept twice may still be clumsy.

### Verification
The analysis distinguishes historical origin from current lexical meaning.

---

## CHK-R04 — Preserve recoverable ellipsis

Source locator: `SRC:L369-L376`  
Scope: phrase/sentence; spoken/informal written  
Basis: `SOURCE_DIRECT`  
Level: optional improvement / preservation  
Confidence: high

### Что проверяет
Whether an apparently incomplete construction omits material that both parties recover from context.

### Почему это важно
The source calls contextual omission a lawful economy of speech.

### Семантический/функциональный инвариант
The omitted element must remain uniquely or safely recoverable.

### Trigger / признаки
Missing noun/complement/measure that context supplies.

### Диагностика
Can a competent reader recover the same omitted material without guessing among materially different meanings?

### Возможные исправления
Keep ellipsis; restore only if context is insufficient or genre requires explicitness.

### Не применять автоматически
Legal, safety-critical or context-poor text may require explicit material.

### Do not infer
All missing complements are ellipsis.

### Взаимодействует с
R05, R24.

### Positive example
`Уже почти восемь. Пора выходить.` — do not expand to `восемь часов` without need.

### Counterexample
`Он передал.` with no recoverable object may be incomplete, not elegant ellipsis.

### Verification
After keeping the omission, reference resolution remains stable.

---

## CHK-R05 — Distinguish ellipsis from lexical reanalysis

Source locator: `SRC:L369-L379`  
Scope: word/phrase; semantics/valency  
Basis: `SOURCE_DIRECT`  
Level: unresolved question  
Confidence: high

### Что проверяет
Whether a seemingly omitted complement is actually absent because the verb/word has acquired a new meaning or valency.

### Почему это важно
The source explicitly contrasts recoverable ellipsis with `переживать` used in a newer intransitive sense.

### Семантический/функциональный инвариант
Do not fabricate an implicit object that speakers do not actually recover.

### Trigger / признаки
Verb historically associated with a complement used without one.

### Диагностика
If asked “what exactly?”, would speakers recover a specific object or interpret a standalone lexical meaning?

### Возможные исправления
Treat as lexical sense/valency candidate; verify current usage.

### Не применять автоматически
True contextual ellipsis remains possible with the same verb in another sentence.

### Do not infer
Any intransitive use of a historically transitive verb is established norm.

### Взаимодействует с
R03, R04, R35.

### Positive example
Do not invent `что именно он переживает` if the context uses the verb simply for emotional anxiety.

### Counterexample
`Не нарушайте` at a clearly marked crossing can recover `правила`; that is contextual omission.

### Verification
The paraphrase matches what a speaker would understand, not an etymological reconstruction.

---

## CHK-R06 — Judge a borrowing by semantic work, not origin

Source locator: `SRC:L665-L1000`, especially `SRC:L937-L949`  
Scope: word/term; general/professional  
Basis: `SOURCE_REPEATED`  
Level: style warning / optional improvement  
Confidence: high

### Что проверяет
Whether a foreign-origin item contributes precision, established terminology or needed meaning.

### Почему это важно
The book rejects blanket anti-borrowing purism while mocking needless foreign display.

### Семантический/функциональный инвариант
Do not lose a technical or semantic distinction when replacing a term.

### Trigger / признаки
Foreign-looking word; request to “replace all anglicisms.”

### Диагностика
Is there an established Russian equivalent with the same scope and register? Does the borrowing fill a gap or merely decorate?

### Возможные исправления
Keep; gloss; replace with an equally precise native form; remove prestige-only code-switch.

### Не применять автоматически
A borrowing can be wrong, opaque or contextually pretentious.

### Do not infer
Borrowed = modern = better.

### Взаимодействует с
R07, R08, R35.

### Positive example
In a developer incident report, keep an established technical term if its Russian substitute is less precise.

### Counterexample
In a public notice, unexplained niche English jargon can be replaced or glossed.

### Verification
Meaning and audience comprehension are at least as good after the edit.

---

## CHK-R07 — Match terminology to the audience

Source locator: `SRC:L922-L936`  
Scope: audience-specific; word/phrase/document  
Basis: `SOURCE_DIRECT`  
Level: probable usage problem  
Confidence: high

### Что проверяет
Whether the intended reader can reasonably interpret the term.

### Почему это важно
The book explicitly makes reader education and background part of lexical admissibility.

### Семантический/функциональный инвариант
Preserve technical precision while lowering unnecessary decoding cost.

### Trigger / признаки
Specialist vocabulary in mixed/new/public audience; unexplained abbreviation.

### Диагностика
What does the audience already know? Is explanation needed once, everywhere, or not at all?

### Возможные исправления
Keep; define at first use; pair term with plain-language gloss; replace if precision survives.

### Не применять автоматически
Expert-to-expert prose need not explain common domain vocabulary.

### Do not infer
Simpler wording is always more respectful or more correct.

### Взаимодействует с
R06, R08, R09, R36.

### Positive example
For onboarding text, spell out an internal acronym on first mention.

### Counterexample
Do not expand `API` repeatedly in a backend engineering runbook.

### Verification
A target reader can act on the text without losing domain distinctions.

---

## CHK-R08 — Diagnose lexical fit in its communicative scene

Source locator: `SRC:L937-L949`, `SRC:L1195-L1210`, `SRC:L1562-L1588`  
Scope: phrase → document; genre/register/audience  
Basis: `SOURCE_DIRECT`  
Level: style warning  
Confidence: high

### Что проверяет
Whether a form belongs in this exact relation of speaker, addressee, genre and purpose.

### Почему это важно
The source says explicitly that one cannot be globally “for” or “against” a word outside context.

### Семантический/функциональный инвариант
Maintain social/genre function, not merely denotational meaning.

### Trigger / признаки
Form seems too official, too familiar, too technical, too colloquial or too literary.

### Диагностика
Who says it, to whom, where, why, and under what genre constraints?

### Возможные исправления
Change register; retain form; move explanation; separate official and conversational layers.

### Не применять автоматически
Register mixing can be deliberate comedy, characterization or irony.

### Do not infer
A word has one fixed style label sufficient for every context.

### Взаимодействует с
R06, R07, R11, R14, R15, R36, R37.

### Positive example
`Просьба приложить копию документа` may be natural in a service instruction but stiff in a partner's private chat.

### Counterexample
A comic narrator may intentionally insert a bureaucratic phrase into a domestic scene.

### Verification
The rewritten line still performs the same social act.

---

## CHK-R09 — Evaluate abbreviations by reader effort

Source locator: `SRC:L1122-L1140`, `SRC:L1178-L1210`  
Scope: token/word; abbreviation; audience/register  
Basis: `SOURCE_REPEATED`  
Level: style warning / optional improvement  
Confidence: high

### Что проверяет
Whether abbreviation genuinely compresses communication rather than creating opaque noise.

### Почему это важно
The book contrasts accepted short forms with long bureaucratic aggregates that are hard to pronounce and understand.

### Семантический/функциональный инвариант
Preserve the referent while minimizing reader/listener decoding work.

### Trigger / признаки
Long acronym/compound; rare initialism; unreadable clipped aggregate.

### Диагностика
Is it shorter in practice? pronounceable? recognizable? established for this audience? worth expansion?

### Возможные исправления
Keep; expand once; replace with ordinary name; introduce short label after full name.

### Не применять автоматически
Widely established short forms may be better than their full expansions.

### Do not infer
Every acronym is bureaucracy or every long word is bad.

### Взаимодействует с
R07, R10, R14.

### Positive example
An internal six-part abbreviation used once in a public FAQ is expanded to the actual department name.

### Counterexample
A common short form in the relevant community stays untouched.

### Verification
The revised form is easier to recognize without adding ambiguity.

---

## CHK-R10 — Do not ban word-formation classes wholesale

Source locator: `SRC:L1178-L1203`, `SRC:L1291-L1307`  
Scope: word; general/historical  
Basis: `SOURCE_DIRECT`  
Level: unresolved question  
Confidence: high

### Что проверяет
Whether a judgment targets a whole formation type rather than the actual item.

### Почему это важно
The source contrasts successful and failed compounds/clippings within the same structural class.

### Семантический/функциональный инвариант
Judge actual form, function, uptake and context.

### Trigger / признаки
`все сокращения плохи`; `все новые сложные слова искусственны`.

### Диагностика
Does this concrete form work? Is it understood, adopted, pronounceable and context-fit?

### Возможные исправления
Evaluate item-by-item; use corpus/current norm if needed.

### Не применять автоматически
A structurally allowed class can contain terrible individual formations.

### Do not infer
Any coined word deserves preservation.

### Взаимодействует с
R01, R02, R09.

### Positive example
Do not delete a concise established clipping solely because it is a clipping.

### Counterexample
An unreadable one-off administrative agglomeration can still be rewritten.

### Verification
The reason refers to the concrete form, not its category alone.

---

## CHK-R11 — Preserve character/professional voice when it carries identity

Source locator: `SRC:L1371-L1396`  
Scope: author/character; scene; professional/social register  
Basis: `SOURCE_DIRECT`  
Level: author mismatch / preservation  
Confidence: high

### Что проверяет
Whether colloquial, rough or professional vocabulary is doing characterization work.

### Почему это важно
The source calls characteristic speech a central resource of fiction and distinguishes narrator speech from character speech.

### Семантический/функциональный инвариант
Preserve speaker identity, milieu and interpersonal relation.

### Trigger / признаки
Slang/professionalism in dialogue; temptation to neutralize every non-neutral word.

### Диагностика
Whose voice is this? What would become less true about the speaker if neutralized?

### Возможные исправления
Keep; normalize only genuine accidental error inconsistent with intended voice; tune degree rather than erase register.

### Не применять автоматически
Narrator exposition may require a different register; offensive/unclear wording can still be intentionally or unintentionally problematic.

### Do not infer
Every slang word is deliberate characterization.

### Взаимодействует с
R08, R12, R36, R37.

### Positive example
A mechanic's dialogue retains established shop-floor terminology that marks the job context.

### Counterexample
A neutral user manual accidentally containing the same shop-floor slang may need normalization.

### Verification
After editing, the character still sounds like the same person in the same scene.

---

## CHK-R12 — Do not infer a person's character directly from one slang marker

Source locator: `SRC:L1483-L1500`  
Scope: inference boundary; speaker/corpus  
Basis: `SOURCE_DIRECT` through explicit counterexample inside the chapter  
Level: unresolved question  
Confidence: high

### Что проверяет
Whether language analysis overclaims moral, intellectual or psychological traits from surface slang.

### Почему это важно
The book itself concedes that good, talented young people may use fashionable rough slang and that it need not reflect their inner life.

### Семантический/функциональный инвариант
Separate observable register choice from unsupported person-level inference.

### Trigger / признаки
`он говорит X, значит он глуп/груб/безнравственен`.

### Диагностика
What does the text actually show: a word, a stable repertoire, a scene, or independent behavioral evidence?

### Возможные исправления
Describe the register only; mark person-level conclusion unsupported.

### Не применять автоматически
A sustained voice across a corpus can still support stylistic characterization, but not sensitive psychological diagnosis without evidence.

### Do not infer
Absence of slang proves culture/intelligence either.

### Взаимодействует с
R11, R13.

### Positive example
`В сообщении есть подростковый сленг` rather than `автор незрелый`.

### Counterexample
A fictional character can intentionally be characterized by a sustained speech pattern plus narrative evidence.

### Verification
Every person-level statement has evidence beyond one lexical marker.

---

## CHK-R13 — Do not confuse a linguistic symptom with its extra-linguistic cause

Source locator: `SRC:L1471-L1494`  
Scope: diagnostic/meta  
Basis: `SOURCE_DIRECT`  
Level: unresolved question  
Confidence: high

### Что проверяет
Whether a proposed edit is being treated as a causal intervention beyond the text.

### Почему это важно
The source explicitly warns against fighting the linguistic consequence while ignoring an external cause.

### Семантический/функциональный инвариант
Keep causal claims separate from textual correction.

### Trigger / признаки
`уберём жаргон — исправим мышление/культуру/отношения`.

### Диагностика
Is the causal mechanism actually demonstrated, or is only a correlation/surface association visible?

### Возможные исправления
Limit claim to wording; place social causality in claims audit.

### Не применять автоматически
Some language choices can affect reception/behavior; the rule only blocks unsupported causal leaps.

### Do not infer
Textual style never influences people.

### Взаимодействует с
R12, claims audit.

### Positive example
Change an offensive phrase for audience fit without claiming the edit has changed the speaker's values.

### Counterexample
A controlled experiment demonstrating a wording effect would be external evidence, not a violation of this rule.

### Verification
The edit report does not claim more than the evidence supports.

---

## CHK-R14 — Preserve functional official formulas in official genres

Source locator: `SRC:L1562-L1580`  
Scope: official/legal/administrative; phrase/document  
Basis: `SOURCE_DIRECT`  
Level: preservation  
Confidence: high

### Что проверяет
Whether a formula exists because the genre requires stable, precise wording.

### Почему это важно
The book explicitly defends standard formulas in powers of attorney, acts, court documents and similar genres.

### Семантический/функциональный инвариант
Preserve formal force, precision, referential structure and institutional convention.

### Trigger / признаки
Formal cliché in a genuinely formal document.

### Диагностика
Does the formula carry legal/procedural function? Would conversational rewriting reduce precision or conventional validity?

### Возможные исправления
Keep; simplify only surrounding dead weight; verify external legal requirements when applicable.

### Не применять автоматически
Not every official-looking phrase is necessary even in an official document.

### Do not infer
Formal language is always clear or legally required.

### Взаимодействует с
R08, R15, R24, R36.

### Positive example
A standard authorization formula remains formal rather than being rewritten as casual speech.

### Counterexample
A personal birthday note inside a company does not need contract-like wording.

### Verification
Institutional function survives and unnecessary abstraction has not been added.

---

## CHK-R15 — Flag official-register leakage outside its function

Source locator: `SRC:L1572-L1588`, `SRC:L1650-L1698`  
Scope: phrase/document; nonofficial contexts  
Basis: `SOURCE_DIRECT`  
Level: style warning  
Confidence: high

### Что проверяет
Whether administrative wording has displaced a natural expression where no administrative function exists.

### Почему это важно
This is the source's core mechanism for cancelearite.

### Семантический/функциональный инвариант
Keep the same action/relation while restoring scene-appropriate register.

### Trigger / признаки
Official classifiers, process nouns, institutional verbs in domestic/emotional/literary prose.

### Диагностика
What official function does this wording perform here? If none, what direct expression carries the same meaning?

### Возможные исправления
Use direct noun/verb; reduce procedural framing; restore speaker-appropriate vocabulary.

### Не применять автоматически
Deliberate parody, irony or characterization may depend on the mismatch.

### Do not infer
Any formal word in informal prose is cancelearite.

### Взаимодействует с
R08, R14, R16, R17.

### Positive example
`После этого я сходил в магазин` instead of a procedural description of `посещение торговой точки` in a personal story.

### Counterexample
A satirical character may intentionally speak like a regulation at the dinner table.

### Verification
The rewrite preserves the event but removes only nonfunctional bureaucratic register.

---

## CHK-R16 — Prefer a direct name over a prestige classifier when no distinction is gained

Source locator: `SRC:L1650-L1698`  
Scope: word/phrase  
Basis: `PROJECT_DERIVED` from repeated source examples  
Level: optional improvement  
Confidence: high

### Что проверяет
Whether a generic classifier replaces an ordinary precise noun only to sound elevated.

### Почему это важно
The source repeatedly contrasts ordinary names with prestige-inflated labels.

### Семантический/функциональный инвариант
Do not remove a classifier that actually encodes a legal, scientific or taxonomic distinction.

### Trigger / признаки
`изделие`, `объект`, `средство`, `продукция`, broad class label where one concrete noun is available.

### Диагностика
What semantic feature is added by the classifier? Is that feature relevant here?

### Возможные исправления
Restore direct noun; keep technical classifier; combine classifier + plain name once.

### Не применять автоматически
Technical documentation may genuinely classify objects by category.

### Do not infer
Concrete nouns are always stylistically superior.

### Взаимодействует с
R10, R15, R17.

### Positive example
`палки` rather than `палочные изделия` when no product taxonomy is being specified.

### Counterexample
`медицинское изделие класса II` may be a meaningful regulatory category.

### Verification
The new noun does not narrow or broaden the referent incorrectly.

---

## CHK-R17 — Recover action from nominalized bureaucratic packaging

Source locator: `SRC:L1880-L1946`, `SRC:L1970-L2008`  
Scope: phrase/sentence; syntax  
Basis: `PROJECT_DERIVED` from repeated source analysis  
Level: optional improvement / probable usage problem  
Confidence: high

### Что проверяет
Whether real actors/actions are buried under chains of process nouns and light administrative verbs.

### Почему это важно
The source shows nominal chains creating opacity, ambiguity and semantic inversion.

### Семантический/функциональный инвариант
Preserve actor, action, patient/object, modality, causality and result.

### Trigger / признаки
Dense `-ение/-ание/-ция` chains; `осуществлять/производить/обеспечивать` + noun; nested genitives.

### Диагностика
Who acts? What happens? To what? Under what condition? What is the result? Which participant is unknown rather than merely hidden?

### Возможные исправления
Restore lexical verb; split clauses; name actor if source supplies it; retain nominalization if technically functional.

### Не применять автоматически
Nominalization is normal in headings, technical taxonomies and situations with intentionally suppressed/unknown agent.

### Do not infer
Every `-ение` noun is cancelearite.

### Взаимодействует с
R15, R18, R22, R23.

### Positive example
`Команда проверяет качество` instead of `осуществляется проведение контроля качества`, when the team is known.

### Counterexample
`Проверка оборудования обязательна перед запуском` can be concise and functional without naming an actor.

### Verification
Back-translate both versions into event roles and confirm they match.

---

## CHK-R18 — Test modifiers by semantic subtraction

Source locator: `SRC:L1744-L1756`  
Scope: word/phrase/sentence  
Basis: `SOURCE_EXAMPLE_ONLY` → operationalized as `PROJECT_DERIVED`  
Level: optional improvement  
Confidence: high

### Что проверяет
Whether an adjective/qualifier changes the proposition or merely adds prestige/intensity.

### Почему это важно
The source explicitly analyzes modifiers whose removal loses no real information.

### Семантический/функциональный инвариант
Keep scope, contrast, degree, chronology, technical distinction and stance.

### Trigger / признаки
Predictable qualifiers; doubled near-synonyms; intensifier-heavy formal prose.

### Диагностика
Delete the modifier in a comparison copy. What fact or distinction disappears?

### Возможные исправления
Delete; replace with precise dimension; keep if it distinguishes.

### Не применять автоматически
An apparently obvious adjective may contrast with another case in context.

### Do not infer
All intensifiers are filler.

### Взаимодействует с
R19, R20, R30.

### Positive example
Remove `имеющиеся` from `исправить имеющиеся ошибки` if no contrast with hypothetical errors exists.

### Counterexample
`исправить критические ошибки, остальные оставить` requires the modifier.

### Verification
The proposition after deletion has the same extension and intended contrast.

---

## CHK-R19 — Diagnose stamps by cluster/repetition and function

Source locator: `SRC:L1780-L1815`, `SRC:L2017-L2041`, note `SRC:L4463-L4470`  
Scope: phrase → document/corpus  
Basis: `SOURCE_REPEATED`  
Level: style warning  
Confidence: high

### Что проверяет
Whether a phrase has become a mechanical template through repeated use in the same rhetorical function.

### Почему это важно
The source explicitly says good words/phrases can become dead through mechanical repetition.

### Семантический/функциональный инвариант
Do not ban a legitimate word; remove predictability that substitutes for fresh content.

### Trigger / признаки
Same collocation, evaluative frame or verb appears repeatedly; content slots change while rhetoric stays fixed.

### Диагностика
Is the unit repeated? Does each occurrence add a distinct proposition? Is it functioning as an automatic label?

### Возможные исправления
Delete redundant frame; write the actual proposition; vary sentence operation, not synonyms; keep intentional refrain.

### Не применять автоматически
One occurrence is not a cluster; repetition can be rhetorical or terminological.

### Do not infer
A phrase is a cliché merely because it is common in a corpus.

### Взаимодействует с
R18, R20, R21, R26, R30.

### Positive example
Three paragraphs each beginning `Автор ярко показывает...` are rebuilt around three actual observations.

### Counterexample
A single `яркий пример` that accurately introduces a concrete example need not be altered.

### Verification
Each retained repeated form performs a distinguishable function or deliberate pattern.

---

## CHK-R20 — Do not infer sincerity from cliché use

Source locator: `SRC:L1744-L1778`  
Scope: inference boundary; emotional speech  
Basis: `SOURCE_DIRECT` through source counterexample  
Level: unresolved question  
Confidence: high

### Что проверяет
Whether formulaic wording is being treated as proof that the feeling is fake.

### Почему это важно
The source itself gives a sincere mourner who nevertheless uses a stereotyped phrase, contradicting a stronger deterministic inference.

### Семантический/функциональный инвариант
Separate stylistic deadness from claims about inner state.

### Trigger / признаки
`штамп → автор неискренен/равнодушен`.

### Диагностика
Is there independent evidence about sincerity? Could convention constrain expression despite genuine feeling?

### Возможные исправления
Describe the phrase as formulaic without diagnosing emotion.

### Не применять автоматически
A document can still show systematic evasiveness through more evidence than one cliché.

### Do not infer
Clichés are harmless; this rule only limits person-level inference.

### Взаимодействует с
R12, R19, R21.

### Positive example
`Фраза шаблонная и малоиндивидуальная` rather than `автору всё равно`.

### Counterexample
If the surrounding facts explicitly show deliberate concealment, stronger interpretation may be justified.

### Verification
Psychological claims are independently evidenced.

---

## CHK-R21 — Put the proposition before generic evaluation when the source supports it

Source locator: `SRC:L1738-L1756`, `SRC:L2017-L2063`, `SRC:L2088-L2103`  
Scope: sentence/paragraph; analytical/expository  
Basis: `PROJECT_DERIVED`  
Level: optional improvement  
Confidence: high

### Что проверяет
Whether an evaluative shell replaces rather than summarizes substantive observation.

### Почему это важно
The book attacks formulas that can be produced without engaging the underlying text/object.

### Семантический/функциональный инвариант
Never invent missing evidence or a more specific proposition than the source supports.

### Trigger / признаки
`важный`, `ярко показывает`, `глубоко раскрывает`, generic praise/condemnation with little proposition.

### Диагностика
What exactly is being asserted? What evidence in the source supports it? Does the evaluation add anything after the assertion?

### Возможные исправления
State concrete observation first; move evaluation after it; remove empty frame; ask for missing evidence.

### Не применять автоматически
Evaluation itself can be the requested speech act (review, verdict, recommendation).

### Do not infer
Specificity may be fabricated to “improve” a vague source.

### Взаимодействует с
R19, R26, R27.

### Positive example
Instead of `Отчёт убедительно показывает серьёзную проблему`, state the reported failure rate if the source contains it.

### Counterexample
`Мне фильм понравился` is a legitimate personal evaluation even without analytical evidence if that is the task.

### Verification
Every new specific statement can be traced to input evidence.

---

## CHK-R22 — Read dense prose aloud after semantic editing

Source locator: `SRC:L1880-L1911`, `SRC:L1970-L1988`, `SRC:L2135-L2159`, `SRC:L2400-L2472`  
Scope: sentence/document; prosody  
Basis: `SOURCE_REPEATED`  
Level: style warning  
Confidence: high

### Что проверяет
Whether syntax and sound produce clumsiness, accidental rhyme, monotony or hidden ambiguity that silent semantic inspection missed.

### Почему это важно
The source repeatedly uses hearing/read-aloud as an independent diagnostic channel.

### Семантический/функциональный инвариант
Sound editing must not change facts, relations or intended emphasis.

### Trigger / признаки
Long syntactic chain; repeated suffixes/endings; tongue-twisting sequence; rhythmically flattened prose.

### Диагностика
Where does reading stumble? Is the acoustic pattern intentional, conventional, technical, or accidental?

### Возможные исправления
Reorder; split; restore verb; change one redundant form; preserve deliberate rhythm.

### Не применять автоматически
Poetry, comic prose, refrains and terminology may intentionally sound marked.

### Do not infer
There is one objective numerical euphony score.

### Взаимодействует с
R17, R23, R30, R31.

### Positive example
A sentence with four adjacent nominalizations is restructured after the repeated endings become intrusive aloud.

### Counterexample
A deliberate alliterative slogan retains its sound pattern.

### Verification
Read original and revision aloud; revision is easier without flattening intended energy.

---

## CHK-R23 — Resolve dependency/case ambiguity, not case counts

Source locator: `SRC:L1880-L1946`  
Scope: sentence; syntax/morphology  
Basis: `SOURCE_DIRECT` + `PROJECT_REFINED` operational boundary  
Level: formal/normative error or probable usage problem depending on case  
Confidence: high

### Что проверяет
Whether chains of genitives/instrumentals make participant roles unclear or attach modifiers to the wrong head.

### Почему это важно
The source's examples show genuine ambiguous role assignment, not merely aesthetic dislike of a case.

### Семантический/функциональный инвариант
Preserve who did what, with what, to whom and in what capacity.

### Trigger / признаки
Long noun dependency chains; adjacent instrumentals with different semantic roles; parse requiring rereading.

### Диагностика
Build dependency/role reading(s). Are multiple plausible parses available? Can roles be expressed directly?

### Возможные исправления
Restore verb; reorder constituents; split sentence; name role explicitly.

### Не применять автоматически
A technical genitive chain may be perfectly unambiguous to its audience.

### Do not infer
`N genitives` = error, or instrumental case itself is bad.

### Взаимодействует с
R17, R22.

### Positive example
Rewrite a sentence where `руководителем отделом` leaves it unclear who holds which role.

### Counterexample
A stable domain term with several dependent nouns may remain compact if parsing is unambiguous.

### Verification
Only one intended role assignment remains available after editing.

---

## CHK-R24 — Run a deletion test on announcing metadiscourse

Source locator: `SRC:L1940-L1962`  
Scope: phrase/sentence/document navigation  
Basis: `PROJECT_DERIVED` from direct source criticism  
Level: optional improvement  
Confidence: high

### Что проверяет
Whether phrases like `нужно отметить / необходимо указать` contribute modality/navigation or merely announce that the writer is about to write.

### Почему это важно
The source argues that writers already implicitly select what they consider worth saying and notes context where official formulations can be appropriate.

### Семантический/функциональный инвариант
Preserve genuine necessity, epistemic stance, structural signposting and contrast.

### Trigger / признаки
Repeated “note/point out/emphasize” frames.

### Диагностика
Delete the frame in a comparison copy. What semantic or document-structural function disappears?

### Возможные исправления
Delete; replace with explicit modality; retain as navigation if it genuinely marks hierarchy.

### Не применять автоматически
`Важно различать два случая` can be real navigation in a dense argument.

### Do not infer
Every occurrence is an AI marker or bureaucratic error.

### Взаимодействует с
R14, R15, R19.

### Positive example
`Следует отметить, что сервер перезапустился` → `Сервер перезапустился`, if no modality is lost.

### Counterexample
`Важно: после миграции старые токены перестанут работать` carries warning hierarchy and should not be deleted merely by form.

### Verification
Compare proposition, modality and navigation before/after deletion.

---

## CHK-R25 — Replace “question packaging” with the actual action when `вопрос` is only a shell

Source locator: `SRC:L1948-L1968`  
Scope: phrase/sentence  
Basis: `SOURCE_DIRECT`  
Level: optional improvement  
Confidence: high

### Что проверяет
Whether `вопрос` names a genuine issue under discussion or is a bureaucratic wrapper for another action.

### Почему это важно
The source explicitly says the word itself is useful but often replaces simpler direct verbs in live speech.

### Семантический/функциональный инвариант
Preserve whether the object really is a question/problem/topic versus an action.

### Trigger / признаки
`осветить/увязать/продвинуть/поднять/поставить вопрос...`.

### Диагностика
Can the phrase name the actual action: explain, compare, propose, decide, discuss?

### Возможные исправления
Use direct action; keep `вопрос` if topic/problem status matters.

### Не применять автоматически
`Вопрос безопасности остаётся открытым` genuinely refers to an issue.

### Do not infer
The noun `вопрос` is undesirable.

### Взаимодействует с
R15, R17.

### Positive example
`поставили вопрос об обмене данными` → `предложили обмениваться данными`, if that is the intended act.

### Counterexample
`Вопрос о сроках пока не решён` should remain about the unresolved issue.

### Verification
The speech act remains the same.

---

## CHK-R26 — Preserve individual differences instead of mapping every subject to one template

Source locator: `SRC:L2042-L2063`  
Scope: paragraph/document; analytical writing; author-specific  
Basis: `SOURCE_DIRECT`  
Level: style warning  
Confidence: high

### Что проверяет
Whether a generic schema erases the distinctions that make the subject specific.

### Почему это важно
The source explicitly criticizes descriptions that make very different writers indistinguishable.

### Семантический/функциональный инвариант
Retain the actual differentiating properties of the subject.

### Trigger / признаки
Same descriptor set applied across unrelated subjects; `типичный представитель` used instead of observed distinctions.

### Диагностика
What distinguishes this case from neighboring cases? Which claims are source-specific versus template slots?

### Возможные исправления
Replace generic category labels with observed differences; retain valid categories but subordinate them to specifics.

### Не применять автоматически
Taxonomy/classification tasks legitimately foreground shared traits.

### Do not infer
Generalization is inherently bad.

### Взаимодействует с
R19, R21, R27.

### Positive example
Two product reviews stop using identical `мощный и универсальный` framing and state different actual trade-offs.

### Counterexample
A standards matrix intentionally compares products by the same fixed criteria.

### Verification
A reader could distinguish the subjects from the prose alone.

---

## CHK-R27 — Ground interpretation in the object before adding interpretive boilerplate

Source locator: `SRC:L2088-L2103`  
Scope: analytical/educational writing  
Basis: `SOURCE_DIRECT` within literary-education scope; generalization is limited  
Level: optional improvement  
Confidence: medium-high

### Что проверяет
Whether commentary is detached from the primary object/text and could be written without examining it.

### Почему это важно
The source criticizes formulaic interpretation standing between reader and work.

### Семантический/функциональный инвариант
Do not invent authorial intention or evidence.

### Trigger / признаки
`автор хотел сказать`; generic analysis with no cited/observable feature.

### Диагностика
What in the object supports the interpretation? Can the analysis be stated as observation before intention attribution?

### Возможные исправления
Describe observable feature; qualify inference; omit unsupported intent attribution.

### Не применять автоматически
Some tasks explicitly require a secondary interpretation or summary.

### Do not infer
Primary experience is sufficient for all scholarship.

### Взаимодействует с
R21, R26.

### Positive example
`В сцене герой дважды отказывается отвечать` before `это можно прочитать как...`.

### Counterexample
A literature-review task may appropriately summarize established interpretations if sources are given.

### Verification
Interpretive claims can be separated into observation and inference.

---

## CHK-R28 — Treat correctness as necessary but not sufficient for verbal quality

Source locator: `SRC:L2135-L2159`, `SRC:L2660-L2677`  
Scope: document/voice  
Basis: `SOURCE_DIRECT`  
Level: optional improvement  
Confidence: high

### Что проверяет
Whether a formally correct text is nevertheless dominated by dead templates, lexical poverty or monotonous intonation.

### Почему это важно
The source explicitly distinguishes spelling/pronunciation correctness from richer verbal culture.

### Семантический/функциональный инвариант
Never degrade correctness merely to create variety.

### Trigger / признаки
No obvious errors but repetitive stock phrasing and flat discourse operations.

### Диагностика
Does the text make specific distinctions? Does it have functional variation of syntax/intonation? Is vocabulary exact or merely rotated?

### Возможные исправления
Improve propositions, structure, rhythm and specificity; leave a good plain text alone.

### Не применять автоматически
Minimal technical instructions may intentionally be lexically narrow and repetitive.

### Do not infer
Rich vocabulary = many synonyms; “liveliness” has a numeric threshold.

### Взаимодействует с
R19, R21, R30, R31.

### Positive example
A repetitive essay is improved by making each paragraph perform a different thought operation rather than swapping synonyms.

### Counterexample
A safety checklist repeats exact terminology for reliability and should stay repetitive.

### Verification
Quality improves without introducing error, obscurity or fake ornament.

---

## CHK-R29 — Do not apply literal logic to established conventional expressions

Source locator: `SRC:L2343-L2400`, `SRC:L2473-L2582`  
Scope: word/phrase; established usage  
Basis: `SOURCE_REPEATED`  
Level: preservation  
Confidence: high

### Что проверяет
Whether an apparently contradictory phrase is conventional and lexicalized rather than a fresh logical error.

### Почему это важно
The book supplies many normal expressions that fail naive compositional logic.

### Семантический/функциональный инвариант
Preserve current conventional meaning.

### Trigger / признаки
`X literally means Y, so this phrase is illogical`.

### Диагностика
Is the expression established? Is the literal component still semantically active?

### Возможные исправления
Keep; explain only if audience needs it; verify current norm when usage is transitional.

### Не применять автоматически
New semantic collisions and accidental contradictory abstractions can still be defects.

### Do not infer
Logic never matters in language.

### Взаимодействует с
R03, R30, R32, R35.

### Positive example
Keep an established intensifier whose original negative meaning is no longer compositionally active.

### Counterexample
A newly coined `наличие отсутствия доступа` can still be needlessly opaque even if individually familiar words are conventional.

### Verification
Check contemporary lexicalized meaning rather than etymological arithmetic.

---

## CHK-R30 — Preserve semantic repetition when it carries rhythm, emphasis or conventional force

Source locator: `SRC:L2400-L2449`, note `SRC:L4463-L4470`  
Scope: phrase/sentence; rhetoric/prosody  
Basis: `SOURCE_DIRECT`  
Level: preservation / optional improvement  
Confidence: high

### Что проверяет
Whether a logically redundant component performs expressive work.

### Почему это важно
The source explicitly rejects “penny-pinching” economy that destroys rhythm and emotional duration.

### Семантический/функциональный инвариант
Preserve intensity, cadence and conventional phrase force when intended.

### Trigger / признаки
Synonym pair/reduplicative phrase; temptation to delete one half solely as redundant.

### Диагностика
Compare versions aloud. Does deletion change emotional weight, rhythm, sound or idiomatic status?

### Возможные исправления
Keep both; compress if function is dead; replace whole formula if it has become a stamp in this context.

### Не применять автоматически
The source itself notes expressive pairs can become bureaucratic templates through repetition.

### Do not infer
Redundancy is always expressive.

### Взаимодействует с
R18, R19, R22, R31.

### Positive example
`стыд и срам` may be preserved as a conventional emphatic pair.

### Counterexample
Three near-synonymous adjectives in a neutral technical sentence may add no force and can be reduced.

### Verification
A/B read-aloud comparison preserves intended force while removing only dead repetition.

---

## CHK-R31 — Use sound/rhythm as a comparison criterion, not a hard formula

Source locator: `SRC:L2400-L2472`  
Scope: word/sentence; prosody/phonetics  
Basis: `SOURCE_DIRECT` for importance; `PROJECT_REFINED` for non-deterministic implementation  
Level: style warning  
Confidence: high

### Что проверяет
Whether one semantically acceptable variant is markedly easier/more expressive in sound than another.

### Почему это важно
The chapter makes sound and rhythm central to linguistic form.

### Семантический/функциональный инвариант
Meaning, norm and voice outrank cosmetic euphony.

### Trigger / признаки
Alternative word orders/forms with equivalent core meaning; awkward repetition of sounds/endings.

### Диагностика
Compare aloud; consider stress/rhythm/articulation; distinguish language convention from personal taste.

### Возможные исправления
Choose smoother variant; keep marked variant if it serves voice/genre.

### Не применять автоматически
No universal suffix-density or sentence-length score follows from the source.

### Do not infer
The historically selected form exists *only* because it sounds prettier.

### Взаимодействует с
R09, R22, R30.

### Positive example
Choose the clearer of two equivalent orders after hearing an accidental tongue-twister.

### Counterexample
A technical term remains even if acoustically heavy because it encodes needed precision.

### Verification
Sound improves without semantic or register regression.

---

## CHK-R32 — Treat an established idiom as a lexical whole

Source locator: `SRC:L2583-L2630`  
Scope: phrase; phraseology  
Basis: `SOURCE_DIRECT`  
Level: preservation  
Confidence: high

### Что проверяет
Whether a phrase is a conventional idiom whose internal words are not freely substitutable.

### Почему это важно
The source explicitly says synonym substitution can destroy the phraseological unit.

### Семантический/функциональный инвариант
Preserve idiomatic meaning and conventional form.

### Trigger / признаки
Temptation to replace one idiom component “for logic”, “variety” or literal precision.

### Диагностика
Is the expression fixed/current? Is the literal image normally active? Would substitution destroy recognizability?

### Возможные исправления
Keep idiom; replace the whole idiom with a nonidiomatic paraphrase if register/audience requires.

### Не применять автоматически
An author may intentionally deform the idiom.

### Do not infer
Every familiar collocation is a fixed idiom.

### Взаимодействует с
R03, R29, R33, R34.

### Positive example
Do not replace one noun inside a fixed idiom with a “more logical” body part.

### Counterexample
A free collocation like `быстрый поезд` permits normal lexical substitution when meaning allows.

### Verification
Phraseological meaning remains recognizable.

---

## CHK-R33 — Preserve deliberate idiom deformation when the effect depends on it

Source locator: `SRC:L2605-L2671`  
Scope: phrase; literary/humorous/author-specific  
Basis: `SOURCE_DIRECT`  
Level: author mismatch / preservation  
Confidence: high

### Что проверяет
Whether deviation from a fixed idiom is intentional artistic reactivation.

### Почему это важно
The source gives multiple cases where breaking the model creates humor or vividness.

### Семантический/функциональный инвариант
Preserve both recoverability of the base idiom and the new effect.

### Trigger / признаки
Near-idiom with one strikingly altered component in a context where the alteration creates a second meaning.

### Диагностика
Can the reader recover the base model? Does the change add a coherent effect? Would “correction” remove it?

### Возможные исправления
Keep; sharpen only if intended play is currently obscure and author intent is known.

### Не применять автоматически
Accidental contamination can look identical superficially.

### Do not infer
Every malformed idiom is wordplay.

### Взаимодействует с
R32, R34.

### Positive example
A comic line twists a familiar idiom so its literal image becomes relevant to the scene; preserve it.

### Counterexample
An accidental merge of two unrelated sayings with no recoverable joke should be corrected.

### Verification
A reader can explain both the base idiom and the added effect.

---

## CHK-R34 — Distinguish intentional idiom play from accidental contamination

Source locator: `SRC:L2648-L2671`  
Scope: phrase; phraseology  
Basis: `SOURCE_DIRECT`  
Level: probable usage problem / unresolved question  
Confidence: high

### Что проверяет
Whether a changed phraseological unit is authored play or a mistake caused by mixing formulas.

### Почему это важно
The source explicitly contrasts deliberate literary renewal with careless mixture.

### Семантический/функциональный инвариант
Do not erase an intended effect; do not protect an accidental error by romanticizing it.

### Trigger / признаки
Near-match to one or two known idioms.

### Диагностика
Is the base expression recoverable? Does context motivate the change? Is there a new meaning/joke/image? Is the author's style known?

### Возможные исправления
Preserve deliberate play; restore conventional idiom; rephrase if intent cannot be safely inferred.

### Не применять автоматически
Without context, classification may remain unresolved.

### Do not infer
Novelty itself proves intention.

### Взаимодействует с
R32, R33.

### Positive example
A deliberate animal substitution fits the paragraph's running joke and is kept.

### Counterexample
`играть значение` produced by mixing `играть роль` and `иметь значение` is corrected when no wordplay exists.

### Verification
The choice is explainable from context, not only surface resemblance.

---

## CHK-R35 — Treat historical prescriptions as verification candidates, not current rewrite commands

Source locator: `SRC:L2759-L4146`, caveats `SRC:L2762-L2777`, notes `SRC:L4147-L4530`  
Scope: historical; norm  
Basis: `PROJECT_DERIVED` from source structure and explicit caveats  
Level: unresolved question until current verification  
Confidence: high

### Что проверяет
Whether a prescriptive pair from the book is being applied as current norm solely because it appears in the historical dictionary.

### Почему это важно
The list is decades old, mixes phenomena, and is explicitly preceded by professional/familiar exceptions.

### Семантический/функциональный инвариант
Do not “correct” a form into a historically preferred variant that is now obsolete, variable or context-bound.

### Trigger / признаки
`Чуковский пишет «нельзя», значит заменяем всегда`.

### Диагностика
What phenomenon is this? What do current authoritative sources say? Are variants/registers recognized today?

### Возможные исправления
Verify externally; classify as current norm, variant, historical, register-specific, or obsolete recommendation.

### Не применять автоматически
Some entries may still represent current unambiguous norm.

### Do not infer
Historical source is useless for norm candidates.

### Взаимодействует с
R01, R03, R05, R36, R37; claims audit.

### Positive example
A stress recommendation is checked against current dictionaries before being encoded.

### Counterexample
A current authoritative rule can confirm the same pair and make it safe for a modern norm layer.

### Verification
Every active prescription has a current external authority, not only this book.

---

## CHK-R36 — Scope professional variants to the professional community

Source locator: `SRC:L2762-L2768`  
Scope: professional/domain-specific  
Basis: `SOURCE_DIRECT`  
Level: probable usage problem / preservation  
Confidence: high as source position; current examples require verification

### Что проверяет
Whether a variant is conventional inside a specific profession but unsuitable as a general-language default.

### Почему это важно
The source states this exception immediately before its dictionary.

### Семантический/функциональный инвариант
Preserve community-recognized usage inside the relevant setting while not universalizing it.

### Trigger / признаки
Profession-specific pronunciation, gender, stress, lexical form or term.

### Диагностика
Is the speaker/member actually in that community? Is the usage conventional there today?

### Возможные исправления
Keep in-domain; use current general norm outside; document variant.

### Не применять автоматически
The book's specific 1960s examples may no longer describe current professional practice.

### Do not infer
Professional communities can override any formal requirement in any document.

### Взаимодействует с
R07, R08, R11, R35.

### Positive example
A domain-specific conventional stress is preserved in specialist dialogue after current verification.

### Counterexample
The same form is not forced into a general-audience narration merely because specialists use it.

### Verification
Current domain evidence supports the scoped variant.

---

## CHK-R37 — Treat familiar/home register as situation-dependent

Source locator: `SRC:L2769-L2777`  
Scope: familiar/home; spoken/informal written  
Basis: `SOURCE_DIRECT`  
Level: preservation / style warning  
Confidence: high

### Что проверяет
Whether informal expressive wording is being normalized as if it were public formal speech.

### Почему это важно
The source explicitly says familiar style depends on individual conversational situation.

### Семантический/функциональный инвариант
Preserve interpersonal tone and intimacy.

### Trigger / признаки
Informal verbs, playful speech, clipped forms, family/friend messages.

### Диагностика
Is this private/familiar communication? Does the form fit the relationship and speaker?

### Возможные исправления
Keep; normalize only genuine misunderstanding/error that conflicts with task intent.

### Не применять автоматически
Familiarity does not legalize every grammatical error or harmful ambiguity.

### Do not infer
Private speech has no norms at all.

### Взаимодействует с
R08, R11, R35.

### Positive example
A playful `звякну вечером` in a close-friend message is not replaced with ceremonial wording.

### Counterexample
A formal complaint to a regulator may need a different register even from the same author.

### Verification
The edited version still sounds plausible between the same participants.

---

## CHK-R38 — Prefer evidence-based normalization over arbitrary purism

Source locator: `SRC:L2276-L2342`, `SRC:L2660-L2677`  
Scope: meta/editorial; general  
Basis: `SOURCE_REPEATED`  
Level: process rule  
Confidence: high

### Что проверяет
Whether the editor's prescription is grounded in norm, established usage, context and language history rather than taste alone.

### Почему это важно
The book simultaneously defends normative conservatism and attacks uninformed “common-sense” judgments.

### Семантический/функциональный инвариант
Do not change valid language to satisfy personal neatness.

### Trigger / признаки
Rule justified only by `sounds wrong to me`, literal logic, age, etymology or a universal ban.

### Диагностика
What evidence supports the prescription? Does counterevidence exist in established usage? Is the rule scoped?

### Возможные исправления
Downgrade to question/warning; seek current normative evidence; add exceptions.

### Не применять автоматически
Not every intuitive judgment is wrong; some reflect real native competence.

### Do not infer
Only formal dictionaries matter; usage and genre remain relevant.

### Взаимодействует с
R01–R37 as a meta-rule.

### Positive example
A disputed construction is left unresolved until current norm and usage are checked.

### Counterexample
A clear agreement error can be corrected directly when current norm is unambiguous.

### Verification
A reviewer can reproduce the rationale from evidence and scope rather than taste.
