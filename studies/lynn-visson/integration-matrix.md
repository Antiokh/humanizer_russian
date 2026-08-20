# Lynn Visson integration matrix

- Source fingerprint: `45cd09d0101caa90effa2f7943d4ddf45659536857ae548910fccad144c806ca`
- Study coverage: **55/55 content XHTML + 117/117 endnotes**.
- Atomic observations: **72**.
- Operational rules: **39**.

Canonical fields for every operational rule are machine-readable in `libraries/visson/rules.json`. The table below is the routing view; it does not replace those cards.

| rule_id | class | automation | phenomenon_id | trigger | context / FP risk | overlap | runtime |
|---|---|---|---|---|---|---|---|
| `VISSON-NORM-ASK-QUESTION` | NORM | DEFAULT_MECHANICAL | `norm.ask_question_valency` | формы спросить/спрашивать + optional у кого + вопрос(ы) | ['лексическая форма', 'цитатность/метаязык']; FP: low after quote/code masking | — | compact default + board |
| `VISSON-NORM-NEGATIVE-CONCORD` | NORM | MODEL_ONLY | `norm.negative_concord` | никто/ничего/никогда + predicate without required negation | синтаксическая связь и область отрицания; FP: high without dependency parse | — | board/model only |
| `VISSON-NATIVE-IMPERSONAL-DATIVE` | NATIVE_USAGE | MODEL_ONLY | `russian.impersonal_dative_experiencer` | explicit subject + analytic predicate mirroring English | event/state type, register; FP: high | russian.rki_like_syntactic_interference | board/model only |
| `VISSON-NATIVE-REFLEXIVE-STATE` | NATIVE_USAGE | MODEL_ONLY | `russian.reflexive_impersonal_state` | overexplicit agentive paraphrase | control/agency; FP: high | — | board/model only |
| `VISSON-NATIVE-WORD-ORDER-INFO` | NATIVE_USAGE | MODEL_ONLY | `native.information_structure_word_order` | repeated rigid subject-first clauses | previous discourse + prosodic focus; FP: very high | russian.rki_like_syntactic_interference | board/model only |
| `VISSON-NATIVE-SUBJECT-OMISSION` | NATIVE_USAGE | METRIC_ONLY | `native.explicit_subject_density` | sentence-initial personal-pronoun density | coreference and contrast; FP: metric only | native.context_undercompression | metrics in compact/board |
| `VISSON-NATIVE-ACTIVE-PASSIVE` | NATIVE_USAGE | MODEL_ONLY | `russian.voice_event_packaging` | passive shell or forced agent | agent salience, genre; FP: very high | russian.rki_like_syntactic_interference | board/model only |
| `VISSON-NATIVE-ASPECT-EVENT-CONSTRUAL` | NATIVE_USAGE | MODEL_ONLY | `russian.aspect_event_construal` | English tense/progressive mapped directly to one Russian aspect | lexical aspect + discourse; FP: very high | russian.rki_like_syntactic_interference, russian.break_state_transition | board/model only |
| `VISSON-NATIVE-MOTION-PREFIX-DEIXIS` | NATIVE_USAGE | MODEL_ONLY | `russian.motion_prefix_deixis` | broad motion verb with English-like semantics | speaker location/path; FP: high | — | board/model only |
| `VISSON-NATIVE-BORROW-LEND-ROLE` | NATIVE_USAGE | MODEL_ONLY | `russian.loan_role_valency` | verbs занять/одолжить around animate participants | semantic roles; FP: high | — | board/model only |
| `VISSON-NATIVE-OFFER-PROPOSE-VALENCY` | NATIVE_USAGE | MODEL_ONLY | `russian.offer_propose_valency` | предложить + suspicious complement frame | object/action/recipient; FP: high | — | board/model only |
| `VISSON-NATIVE-STAY-DURATION` | NATIVE_USAGE | MODEL_ONLY | `russian.stay_reside_duration` | broad stay/live translation | duration and residence type; FP: high | — | board/model only |
| `VISSON-NATIVE-MEET-VALENCY` | NATIVE_USAGE | MODEL_ONLY | `russian.meet_encounter_valency` | встретить + abstract operational noun | domain/register; FP: high | — | board/model only |
| `VISSON-NATIVE-REPAIR-EVENT-TYPE` | NATIVE_USAGE | MODEL_ONLY | `russian.repair_event_type` | generic ремонт used where event type matters | domain and event type; FP: high | — | board/model only |
| `VISSON-NATIVE-SUCH-FUNCTION` | NATIVE_USAGE | MODEL_ONLY | `russian.such_function` | frequent такой in English-like contexts | discourse antecedent and intensity; FP: high | — | board/model only |
| `VISSON-NATIVE-JUST-FUNCTION` | NATIVE_USAGE | MODEL_ONLY | `russian.just_function` | просто with English-like discourse function | pragmatics and timing; FP: high | — | board/model only |
| `VISSON-NATIVE-PROBLEM-ISSUE` | NATIVE_USAGE | MODEL_ONLY | `russian.problem_issue_semantics` | problem/проблема near meeting/discussion context | whether difficulty exists; FP: high | — | board/model only |
| `VISSON-NATIVE-MODAL-NEGATION` | NATIVE_USAGE | MODEL_ONLY | `russian.negative_modality_source` | generic negative modal phrase | speech act, source of rule; FP: very high | — | board/model only |
| `VISSON-NATIVE-NEGATED-INFINITIVE` | NATIVE_USAGE | MODEL_ONLY | `russian.negated_infinitive_dative` | analytic ability phrase | register, rhetorical force; FP: high | — | board/model only |
| `VISSON-NATIVE-REFERENCE-WE-WITH` | NATIVE_USAGE | MODEL_ONLY | `russian.we_with_reference` | coordination/pronoun pattern | discourse referents; FP: high | — | board/model only |
| `VISSON-NATIVE-POSSESSIVE-OMISSION` | NATIVE_USAGE | MODEL_ONLY | `native.recoverable_possessive_omission` | repeated мой/свой from English surface | coreference; FP: high | native.possessive_overexplication | board/model only |
| `VISSON-NATIVE-TIME-DAYPART` | NATIVE_USAGE | MODEL_ONLY | `russian.daypart_reference` | daypart lexical mapping | clock time/context; FP: high | — | board/model only |
| `VISSON-NATIVE-REST-SEMANTICS` | NATIVE_USAGE | MODEL_ONLY | `russian.rest_activity_semantics` | generic lexical calque around отдых | activity type; FP: high | — | board/model only |
| `VISSON-NATIVE-HOLIDAY-SEMANTICS` | NATIVE_USAGE | MODEL_ONLY | `russian.holiday_event_semantics` | generic holiday mapping | country/calendar context; FP: high | — | board/model only |
| `VISSON-EDIT-DIRECTNESS-PRAGMATICS` | EDITING | MODEL_ONLY | `editing.directness_pragmatic_fit` | multi-layer politeness shell | social relation/register; FP: very high | — | board/model only |
| `VISSON-EDIT-FORMULA-REGISTER` | EDITING | MODEL_ONLY | `editing.speech_formula_register` | literal formula surface | situation/register; FP: high | — | board/model only |
| `VISSON-CALQUE-PRETEND-CLAUSE` | AI_CALQUE | DEFAULT_MECHANICAL | `russian.false_friend_pretend_claim` | претендовать/претендует/претендовал + comma + что/будто/словно | clause semantics; FP: low for direct pattern | — | compact default + board |
| `VISSON-CALQUE-HAVE-NICE-DAY` | AI_CALQUE | EXTENDED_SOFT | `russian.literal_have_nice_day` | имейте + хороший/приятный/замечательный + день | speech-act context; FP: medium | — | compact --extended + board |
| `VISSON-CALQUE-HAPPY-BIRTHDAY` | AI_CALQUE | EXTENDED_SOFT | `russian.literal_happy_birthday` | sentence/line exactly счастливого дня рождения | surrounding verb; FP: medium | — | compact --extended + board |
| `VISSON-CALQUE-ENJOY-STANDALONE` | AI_CALQUE | EXTENDED_SOFT | `russian.literal_enjoy_formula` | isolated Наслаждайтесь! | object/situation/register; FP: medium-high | — | compact --extended + board |
| `VISSON-CALQUE-ACTUAL-AKTUALNY` | AI_CALQUE | MODEL_ONLY | `russian.false_friend_actual_aktualny` | актуальный near factual-data context | intended sense; FP: very high | — | board/model only |
| `VISSON-CALQUE-DECADE-DEKADA` | AI_CALQUE | MODEL_ONLY | `russian.false_friend_decade_dekada` | декада with year-scale context | dates; FP: medium-high | — | board/model only |
| `VISSON-CALQUE-ARGUMENT-ARGUMENT` | AI_CALQUE | MODEL_ONLY | `russian.false_friend_argument_scope` | аргумент with event syntax | event semantics; FP: high | — | board/model only |
| `VISSON-CALQUE-ARTIST-ARTIST` | AI_CALQUE | MODEL_ONLY | `russian.false_friend_artist_scope` | артист with visual-art context | profession; FP: high | — | board/model only |
| `VISSON-CALQUE-MEETING-MITING` | AI_CALQUE | MODEL_ONLY | `russian.false_friend_meeting_miting` | митинг near workplace/team context | domain/register; FP: high | russian.register_jargon_or_term | board/model only |
| `VISSON-CALQUE-ECONOMIC-ECONOMICAL` | AI_CALQUE | MODEL_ONLY | `russian.false_friend_economic_economical` | экономический/экономичный in semantic mismatch | head noun semantics; FP: high | — | board/model only |
| `VISSON-CALQUE-PROGRESSIVE-IMPERFECTIVE` | AI_CALQUE | MODEL_ONLY | `russian.progressive_aspect_calque` | present imperfective used to imitate ongoing English event | event type, subject class; FP: very high | russian.break_state_transition, russian.abstract_break_calque | board/model only |
| `VISSON-CALQUE-BROAD-LEXICAL-MAPPING` | AI_CALQUE | MODEL_ONLY | `russian.broad_english_lexeme_mapping` | semantically broad Russian calque | sense, arguments, register; FP: very high | russian.abstract_break_calque, russian.rki_like_syntactic_interference | board/model only |
| `VISSON-CALQUE-SVO-LOCK` | AI_CALQUE | METRIC_ONLY | `russian.svo_lock_metric` | sentence-initial pronoun/noun + verb regularity | full discourse; FP: metric only | russian.rki_like_syntactic_interference | metrics in compact/board |

## Mechanical-feasibility result

Exact/regex survived only for two default signals and three extended speech-formula candidates. Contextual valency, aspect, event type, information structure, reference and lexical-sense decisions remain `MODEL_ONLY`. Two document-level surfaces are metrics only. No book-derived `HARD_GATE` exists.

## Default mechanical controls

- `VISSON-NORM-ASK-QUESTION`: true positive `Я хочу спросить у вас вопрос`; negative `Я хочу задать вам вопрос`; boundary `спросить у вас о вопросе`; intentional/metalinguistic quoted use is masked; code/URL/Markdown non-prose excluded.
- `VISSON-CALQUE-PRETEND-CLAUSE`: true positive `Он претендует, что ничего не знает`; negative `Он претендует на должность`; boundary `не претендует на то, что...`; quoted/metalinguistic use excluded.

## Source-neutral overlap policy

- Existing Russian core remains the owner of `russian.break_state_transition` and `russian.abstract_break_calque`; Visson only contributes the broader aspect/event-construal mechanism.
- General RKI audit stays in Russian core. Visson’s narrower valency/reference/aspect rules provide source provenance without duplicating that mechanism.
- `митинг` is linked conceptually to `russian.register_jargon_or_term`; no unconditional word ban is created.

## Runtime context budget

Compact does not load the study or `model-only.md`; it imports only `scripts/lint_visson.py` through the normal library adapter. Board can retain source provenance in findings; contextual references remain addressable rather than mandatory.
