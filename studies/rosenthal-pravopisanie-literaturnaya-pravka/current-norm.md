# Current-norm verification (2026-08-20)

Historical source prescriptions are not promoted to current NORM by author authority. The first pass checked only the claims needed for runtime or high-value guardrails.

| Claim | Source | Current evidence | Disposition |
|---|---|---|---|
| `согласно` governs dative | §200.1 | Gramota.ru, «Словарь-справочник трудностей русского языка»: current Russian requires dative, including official/business style | CURRENT_CONFIRMED; narrow EXTENDED_SOFT detector ROS-R44 |
| Gerund action normally shares semantic actor; impersonal + infinitive can be valid | §212.1 | Gramota.ru answer №317697 (2024): confirms impersonal+infinitive exception and rejects impersonal clauses without controlling infinitive | CURRENT_CONFIRMED; reuse `norm.gerund_subject_attachment`, MODEL_ONLY |
| `оплатить` vs `заплатить/уплатить` government | §§139, 202 | Gramota.ru current search/dictionary answers: `оплатить проезд`; `заплатить за проезд`; `уплатить` without preposition with money/sum nouns | CURRENT_CONFIRMED, but MODEL_ONLY because regex can confuse beneficiary `за него` with governed object |
| paired conjunction baseline `не только … но и` | §208.8 | Gramota current reference grammar lists `не только...но и` among paired conjunctions; source-specific `не только…а также` remains a mixed-pair review candidate | CURRENT_CONFIRMED_AS_BASELINE; EXTENDED_SOFT/REVIEW ROS-R30 |

External URLs (accessed 2026-08-20):
- https://gramota.ru/biblioteka/spravochniki/slovar-trudnostey/soglasno
- https://gramota.ru/spravka/vopros/317697
- https://gramota.ru/biblioteka/spravochniki/pravila-russkoy-orfografii-i-punktuatsii/znaki-prepinaniya-pri-odnorodnykh-chlenakh-predlozheniya
- https://gramota.ru/poisk?mode=all&query=%D1%83%D0%BF%D0%BB%D0%B0%D1%82%D0%B8%D1%82%D1%8C+%D0%B7%D0%B0+%D0%BF%D1%80%D0%BE%D0%B5%D0%B7%D0%B4

All other historically sensitive lexical/morphological variant lists remain `VERIFY_CURRENT_USAGE` until individually needed and checked.
