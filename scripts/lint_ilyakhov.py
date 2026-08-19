#!/usr/bin/env python3
"""Precision-first Ilyakhov/Sarycheva knowledge-library adapter.

The complete source model lives in studies/pishi-sokrashchay/. This module
implements only the mechanically defensible residue:

- ILY-M01: one project-derived DEFAULT_MECHANICAL operator;
- nine source EXTENDED_SOFT candidates;
- four descriptive METRIC_ONLY signals.

All consumers use review_v1. ``lint()`` is retained only as a small internal /
calibration compatibility surface and is not a second runtime implementation.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

try:
    from lint import prose_text, sentences
except ImportError:  # package/import context
    from scripts.lint import prose_text, sentences

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "libraries" / "ilyakhov" / "rules.json"
WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+(?:-[A-Za-zА-Яа-яЁё0-9]+)?", re.U)
SENTENCE_RE = re.compile(r"[^.!?\n]+[.!?]?", re.U)

# ILY-M01: deliberately tiny light-verb/nominalization duplication. This is a
# project-derived subset of PS-R22 + PS-R29, not a general nominalization ban.
BUREAUCRATIC_TAUTOLOGY_RE = re.compile(
    r"(?:"
    r"\bосуществ(?:ить|лять|ляет|ляют|лял|ляла|ляли|лено|лена|лены|ляется|ляются)\s+"
    r"(?:проведен(?:ие|ия)|выполнен(?:ие|ия)|осуществлен(?:ие|ия))\b"
    r"|\b(?:произвести|производить|производит|производят|производил|производила|производили|"
    r"произведено|произведена|произведены)\s+"
    r"(?:выполнен(?:ие|ия)|проведен(?:ие|ия))\b"
    r"|\b(?:провести|проводить|проводит|проводят|провёл|провел|провела|провели)\s+"
    r"осуществлен(?:ие|ия)\b"
    r")",
    re.I,
)

COMMON_KNOWLEDGE_RE = re.compile(
    r"\b(?:как\s+известно|общеизвестно|всем\s+известно|не\s+секрет(?:,?\s+что)?)\b",
    re.I,
)
NUMBERING_PATTERNS = [
    re.compile(r"\bво[- ]?первых\b", re.I),
    re.compile(r"\bво[- ]?вторых\b", re.I),
    re.compile(r"\bв[- ]?третьих\b", re.I),
    re.compile(r"\bв[- ]?четв[её]ртых\b", re.I),
]
POLITENESS_PATTERNS = [
    re.compile(p, re.I)
    for p in [
        r"\bобращаем\s+ваше\s+внимание\b",
        r"\bубедительно\s+просим\b",
        r"\bпросим\s+вас\b",
        r"\bбудьте\s+добры\b",
        r"\bзаранее\s+благодарим\b",
        r"\bвыражаем\s+благодарность\b",
        r"\bс\s+уважением\b",
    ]
]
INTENSIFIER_RE = re.compile(
    r"\b(?:очень|крайне|чрезвычайно|невероятно|максимально|абсолютно|"
    r"исключительно|по[- ]настоящему|действительно|безусловно|несомненно)\b",
    re.I,
)
PRESENT_TIME_RE = re.compile(
    r"\b(?:в\s+настоящее\s+время|на\s+сегодняшний\s+день|"
    r"в\s+текущий\s+момент|на\s+данный\s+момент|в\s+современных\s+условиях)\b",
    re.I,
)
TEMPORAL_CONTRAST_RE = re.compile(
    r"\b(?:раньше|прежде|ранее|теперь|в\s+прошлом|в\s+будущем|"
    r"по\s+сравнению|до\s+\d{4}|после\s+\d{4}|с\s+\d{4})\b",
    re.I,
)
BUREAUCRATIC_SHELL_PATTERNS = [
    re.compile(r"\bв\s+рамках\s+(?:проведения|реализации|осуществления)\b", re.I),
    re.compile(r"\bв\s+целях\s+(?:осуществления|обеспечения|проведения)\b", re.I),
    re.compile(r"\bбыло\s+осуществлено\s+(?!проведение\b|выполнение\b)", re.I),
]
META_INTRO_RE = re.compile(
    r"\b(?:в\s+(?:данной|этой)\s+(?:статье|главе|разделе)|далее)\s+"
    r"(?:мы\s+)?(?:рассмотрим|разбер[её]м|поговорим|расскажем)\b",
    re.I,
)
RITUAL_CONCLUSION_RE = re.compile(
    r"\b(?:подводя\s+итог|резюмируя(?:\s+сказанное)?|"
    r"в\s+заключение\s+(?:хочется|можно|следует|необходимо))\b",
    re.I,
)
BROAD_PRECISION_RE = re.compile(
    r"\b(?:9[5-9]|100)\s*%\s+(?:всех\s+)?"
    r"(?:людей|пользователей|россиян|покупателей|клиентов|компаний|читателей)\b",
    re.I,
)
GENERIC_BENEFIT_PATTERNS = [
    re.compile(p, re.I)
    for p in [
        r"\bвысококвалифицированн\w*\b",
        r"\bиндивидуальн\w*\s+подход\w*\b",
        r"\bширок\w*\s+спектр\w*\b",
        r"\bвысок\w*\s+качеств\w*\b",
        r"\bэффективн\w*\s+решени\w*\b",
        r"\bкоманд\w*\s+профессионал\w*\b",
        r"\bмноголетн\w*\s+опыт\w*\b",
        r"\bнад[её]жн\w*\s+партн[её]р\w*\b",
    ]
]
STATE_PREDICATE_RE = re.compile(
    r"\b(?:является|являются|представляет\s+собой|представляют\s+собой|"
    r"характеризуется|характеризуются|обладает|обладают)\b",
    re.I,
)
CORRELATIVE_PATTERNS = [
    ("не только…но и", re.compile(r"\bне\s+только\b(?P<body>.*?)\bно\s+и\b", re.I | re.S)),
    ("как…так и", re.compile(r"\bкак\b(?P<body>.*?)\bтак\s+и\b", re.I | re.S)),
    ("если…то", re.compile(r"\bесли\b(?P<body>.*?)\bто\b", re.I | re.S)),
]

LABEL_TO_RULE = {
    "ilyakhov: bureaucratic tautology": "ILY-M01",
    "ilyakhov: common-knowledge wrapper": "ILY-R09",
    "ilyakhov: verbal-numbering cluster": "ILY-R11",
    "ilyakhov: ceremonial-politeness cluster": "ILY-R13",
    "ilyakhov: intensifier cluster": "ILY-R18",
    "ilyakhov: bureaucratic-shell candidate": "ILY-R22",
    "ilyakhov: meta-intro candidate": "ILY-R62",
    "ilyakhov: ritual-conclusion candidate": "ILY-R63",
    "ilyakhov: suspicious broad precision": "ILY-R76",
    "ilyakhov: generic-benefit cluster": "ILY-R85",
}
OPERATIONS = {
    "ILY-M01": "replace_tautological_light_verb_shell_with_direct_action",
    "ILY-R09": "compare_without_common_knowledge_frame",
    "ILY-R11": "compare_numbering_with_structural_alternative",
    "ILY-R13": "surface_reason_deadline_action_before_ceremony",
    "ILY-R18": "compare_without_excess_intensifiers",
    "ILY-R22": "recover_event_and_roles_without_register_loss",
    "ILY-R62": "compare_without_topic_announcement",
    "ILY-R63": "remove_or_replace_ritual_conclusion_with_function",
    "ILY-R76": "verify_source_method_scope_and_period",
    "ILY-R85": "replace_generic_benefit_with_supported_specificity",
}


def _load_registry() -> dict[str, dict]:
    payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    items = payload["rules"] + payload.get("project_derived_rules", [])
    return {item["rule_id"]: item for item in items}


RULES = _load_registry()


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def _sentence_chunks(prose: str) -> list[tuple[str, int]]:
    return [(m.group(0).strip(), m.start()) for m in SENTENCE_RE.finditer(prose) if m.group(0).strip()]


def _line(text: str, start: int) -> int:
    return text.count("\n", 0, max(0, start)) + 1


def _add(findings: list[dict], prose: str, label: str, excerpt: str, start: int, note: str) -> None:
    findings.append({
        "label": label,
        "line": _line(prose, start),
        "excerpt": " ".join(excerpt.split())[:220],
        "reason": note,
    })


def _hits(text: str, patterns: list[re.Pattern[str]]) -> list[re.Match[str]]:
    out: list[re.Match[str]] = []
    for rx in patterns:
        out.extend(rx.finditer(text))
    return sorted(out, key=lambda m: m.start())


def _common_knowledge_has_named_basis(prose: str, match: re.Match[str]) -> bool:
    # Avoid the obvious false-positive family “как известно из/по ...”. This
    # does not try to solve attribution semantically; ambiguous cases remain
    # extended/model-side.
    tail = prose[match.end(): match.end() + 70]
    return bool(re.match(r"\s*,?\s*(?:из\b|по\s+данным\b|по\s+материалам\b|нам\s+из\b)", tail, re.I))


def lint(text: str) -> tuple[list[dict], dict]:
    """Return one internal detector stream plus metrics.

    ``review`` is the public normalized adapter. Keeping this helper lets the
    one-off corpus calibration reuse the exact same detector implementation.
    """
    prose = prose_text(text)
    findings: list[dict] = []

    for match in BUREAUCRATIC_TAUTOLOGY_RE.finditer(prose):
        _add(
            findings, prose, "ilyakhov: bureaucratic tautology", match.group(0), match.start(),
            "ILY-M01 / PS-R22+PS-R29: explicit light-verb duplication; simplify only if official/legal meaning and responsibility remain unchanged",
        )

    for match in COMMON_KNOWLEDGE_RE.finditer(prose):
        if _common_knowledge_has_named_basis(prose, match):
            continue
        _add(
            findings, prose, "ilyakhov: common-knowledge wrapper", match.group(0), match.start(),
            "PS-R09: check whether the frame contributes a real source or contrast; never turn unsupported obviousness into fact",
        )

    numbering = _hits(prose, NUMBERING_PATTERNS)
    if len(numbering) >= 3:
        _add(
            findings, prose, "ilyakhov: verbal-numbering cluster",
            " … ".join(m.group(0) for m in numbering[:4]), numbering[0].start(),
            "PS-R11: review only; explicit ordering is normal in algorithms, referenced lists and deliberate argument structure",
        )

    politeness = _hits(prose, POLITENESS_PATTERNS)
    if len(politeness) >= 3:
        _add(
            findings, prose, "ilyakhov: ceremonial-politeness cluster",
            " … ".join(m.group(0) for m in politeness[:4]), politeness[0].start(),
            "PS-R13: check whether ceremony hides reason, deadline, file or next action; ordinary politeness and formal convention are valid",
        )

    intensifier_clusters = 0
    for sent, pos in _sentence_chunks(prose):
        if len(list(INTENSIFIER_RE.finditer(sent))) >= 3:
            intensifier_clusters += 1
            _add(
                findings, prose, "ilyakhov: intensifier cluster", sent, pos,
                "PS-R18: clustered intensification may substitute for evidence; deliberate hyperbole or emotional voice can be functional",
            )

    present = list(PRESENT_TIME_RE.finditer(prose))
    present_without_contrast = 0
    for match in present:
        window = prose[max(0, match.start() - 120): min(len(prose), match.end() + 160)]
        if not TEMPORAL_CONTRAST_RE.search(window):
            present_without_contrast += 1

    bureaucratic_shell_hits = 0
    for rx in BUREAUCRATIC_SHELL_PATTERNS:
        for match in rx.finditer(prose):
            bureaucratic_shell_hits += 1
            _add(
                findings, prose, "ilyakhov: bureaucratic-shell candidate", match.group(0), match.start(),
                "PS-R22: surface candidate only; legal/procedural register, responsibility and term-of-art status require context",
            )

    for match in META_INTRO_RE.finditer(prose):
        _add(
            findings, prose, "ilyakhov: meta-intro candidate", match.group(0), match.start(),
            "PS-R62: compare with a direct opening; academic roadmap and long-form navigation may make the frame functional",
        )

    for match in RITUAL_CONCLUSION_RE.finditer(prose):
        _add(
            findings, prose, "ilyakhov: ritual-conclusion candidate", match.group(0), match.start(),
            "PS-R63: a conclusion needs a function beyond ritual repetition; some formal genres legitimately require a conclusion section",
        )

    for match in BROAD_PRECISION_RE.finditer(prose):
        _add(
            findings, prose, "ilyakhov: suspicious broad precision", match.group(0), match.start(),
            "PS-R76: verification prompt only; unusual precision is not proof that the number is false",
        )

    generic_benefit_clusters = 0
    for sent, pos in _sentence_chunks(prose):
        if sum(bool(rx.search(sent)) for rx in GENERIC_BENEFIT_PATTERNS) >= 2:
            generic_benefit_clusters += 1
            _add(
                findings, prose, "ilyakhov: generic-benefit cluster", sent, pos,
                "PS-R85: in self-presentation/commercial prose, prefer supported specificity; a broad slogan may still be functional as a secondary layer",
            )

    correlative_spans: list[int] = []
    correlative_count = 0
    for _label, rx in CORRELATIVE_PATTERNS:
        for match in rx.finditer(prose):
            body = match.group("body")
            if "\n\n" in body:
                continue
            correlative_count += 1
            correlative_spans.append(word_count(body))

    sents = sentences(text)
    state_predicate_sentences = sum(1 for sent in sents if STATE_PREDICATE_RE.search(sent))
    comma_count = prose.count(",")
    multi_comma_sentences = sum(1 for sent in sents if sent.count(",") >= 3)
    metrics = {
        "ilyakhov_correlative_pairs": correlative_count,
        "ilyakhov_correlative_max_inner_words": max(correlative_spans, default=0),
        "ilyakhov_state_predicate_sentences": state_predicate_sentences,
        "ilyakhov_comma_count": comma_count,
        "ilyakhov_multi_comma_sentences_ge_3": multi_comma_sentences,
        "ilyakhov_present_time_wrappers": len(present),
        "ilyakhov_present_time_wrappers_without_local_contrast": present_without_contrast,
        "ilyakhov_intensifier_clusters": intensifier_clusters,
        "ilyakhov_bureaucratic_shell_candidates": bureaucratic_shell_hits,
        "ilyakhov_generic_benefit_clusters": generic_benefit_clusters,
    }
    return findings, metrics


def review(text: str) -> dict:
    raw, metrics = lint(text)
    normalized = []
    for item in raw:
        label = item["label"]
        rule_id = LABEL_TO_RULE[label]
        rule = RULES[rule_id]
        normalized.append({
            "rule_id": rule_id,
            "phenomenon_id": rule["phenomenon_id"],
            "project_class": rule["project_class"],
            "automation_level": rule["automation_level"],
            "verdict": "CHANGE" if rule_id == "ILY-M01" else "REVIEW",
            "line": item.get("line", 0),
            "excerpt": item.get("excerpt", ""),
            "reason": item.get("reason", ""),
            "operation": OPERATIONS.get(rule_id),
            "confidence": None,
        })
    return {"findings": normalized, "metrics": metrics}


def _ids(text: str) -> set[str]:
    return {item["rule_id"] for item in review(text)["findings"]}


def self_test() -> None:
    # DEFAULT project-derived operator: TP plus natural/boundary controls.
    assert "ILY-M01" in _ids("В рамках проекта было осуществлено проведение проверки.")
    assert "ILY-M01" in _ids("Подрядчик должен произвести выполнение работ до пятницы.")
    for safe in [
        "Мы провели исследование и отправили отчёт.",
        "Было проведено исследование условий труда.",
        "Нужно осуществить переход на новый тариф до пятницы.",
        "Комиссия выполнит проверку в установленный срок.",
        "Решение принято в рамках закона.",
    ]:
        assert "ILY-M01" not in _ids(safe), (safe, review(safe))

    # EXTENDED signals and negative controls.
    assert "ILY-R09" in _ids("Как известно, этот способ используют давно.")
    assert "ILY-R09" not in _ids("Как известно из отчёта комиссии, этот способ используют давно.")
    assert "ILY-R11" in _ids("Во-первых, цена. Во-вторых, срок. В-третьих, гарантия.")
    assert "ILY-R11" not in _ids("Во-первых, это один аргумент. Во-вторых, это второй.")
    assert "ILY-R13" in _ids("Обращаем ваше внимание на срок. Просим вас прислать файл. С уважением, отдел.")
    assert "ILY-R13" not in _ids("Пожалуйста, пришлите файл до пятницы.")
    assert "ILY-R18" in _ids("Это абсолютно, невероятно и действительно важный результат.")
    assert "ILY-R18" not in _ids("Это очень важный для меня результат.")
    assert "ILY-R62" in _ids("В данной статье мы рассмотрим три способа резервного копирования.")
    assert "ILY-R63" in _ids("Подводя итог, можно повторить сказанное выше.")
    assert "ILY-R76" in _ids("99% всех людей выбирают этот вариант.")
    assert "ILY-R85" in _ids("Предлагаем эффективные решения, индивидуальный подход и высокое качество.")

    # R21 stays metric-only after corpus calibration.
    result = review("В настоящее время компания выпускает три модели.")
    assert result["metrics"]["ilyakhov_present_time_wrappers"] == 1, result
    assert "ILY-R21" not in {x["rule_id"] for x in result["findings"]}, result

    # Native-Russian controls must not be mechanically 'fixed'.
    for safe in [
        "Я считаю, что решение рискованное.",
        "Мне кажется, данных пока недостаточно.",
        "Платёж отклонён банком.",
        "Контроллер является частью системы.",
        "Кого пригласили? Машу.",
        "Никогда. Никогда больше.",
    ]:
        assert not _ids(safe), (safe, review(safe))

    long_clear = (
        "Если договор уже подписан и оплата поступила на счёт после проверки реквизитов, "
        "то заказ отправим в понедельник, когда откроется склад."
    )
    result = review(long_clear)
    assert result["metrics"]["ilyakhov_correlative_pairs"] >= 1, result
    assert not result["findings"], result

    # Current-main prose normalization excludes headings/code/quotes/URLs.
    protected = """# Как известно

> Как известно, это цитата.

```text
осуществить проведение
```

https://example.test/как-известно
"""
    assert not review(protected)["findings"], review(protected)

    for item in review("Как известно, это абсолютно, невероятно и действительно важно.")["findings"]:
        assert item["rule_id"] in RULES, item
        assert item["phenomenon_id"] == RULES[item["rule_id"]]["phenomenon_id"], item
        assert item["project_class"] in {"EDITING", "NATIVE_USAGE"}, item


if __name__ == "__main__":
    self_test()
    print("lint_ilyakhov review_v1 self-test: OK")
