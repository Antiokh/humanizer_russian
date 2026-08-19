#!/usr/bin/env python3
"""Precision-first mechanical layer derived from the Ilyakhov/Sarycheva study.

This module is deliberately narrower than the book. It reports surface
candidates and descriptive metrics; it does not turn editorial advice into
Russian-language errors.

Source provenance: studies/pishi-sokrashchay/ (PS-R*).
Project-derived default operator: ILY-M01, a narrow subset of PS-R22 + PS-R29.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
FENCED_RE = re.compile(r"```.*?```|~~~.*?~~~", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((?:[^()]|\([^)]*\))*\)")
QUOTE_LINE_RE = re.compile(r"(?m)^\s*>.*$")
SENTENCE_RE = re.compile(r"[^.!?\n]+[.!?]?", re.U)
WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+(?:-[A-Za-zА-Яа-яЁё0-9]+)?", re.U)

# ILY-M01: intentionally tiny. These are explicit light-verb + nominalization
# duplications, not a general ban on nominalizations or official register.
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


def strip_non_prose(text: str) -> str:
    """Remove areas where source-specific prose heuristics should not fire."""
    text = FENCED_RE.sub(" ", text)
    text = QUOTE_LINE_RE.sub(" ", text)
    text = INLINE_CODE_RE.sub(" ", text)
    text = MARKDOWN_LINK_RE.sub(r"\1", text)
    text = URL_RE.sub(" ", text)
    return text


def sentences(text: str) -> list[str]:
    return [m.group(0).strip() for m in SENTENCE_RE.finditer(text) if m.group(0).strip()]


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def line_number(text: str, start: int) -> int:
    return text.count("\n", 0, max(start, 0)) + 1


def add(findings: list[dict], text: str, rule: str, match_text: str, start: int, note: str) -> None:
    findings.append(
        {
            "kind": "STYLE_WARNING",
            "line": line_number(text, start),
            "rule": rule,
            "excerpt": " ".join(match_text.split())[:220],
            "note": note,
        }
    )


def _count_patterns(text: str, patterns: list[re.Pattern[str]]) -> list[re.Match[str]]:
    out: list[re.Match[str]] = []
    for rx in patterns:
        out.extend(rx.finditer(text))
    return sorted(out, key=lambda m: m.start())


def lint(text: str) -> tuple[list[dict], dict]:
    prose = strip_non_prose(text)
    findings: list[dict] = []

    # DEFAULT-capable PROJECT_DERIVED operator ILY-M01.
    for m in BUREAUCRATIC_TAUTOLOGY_RE.finditer(prose):
        add(
            findings,
            text,
            "ilyakhov: bureaucratic tautology",
            m.group(0),
            m.start(),
            "ILY-M01 / PS-R22+PS-R29: explicit light-verb duplication; simplify the action without changing official/legal meaning",
        )

    # EXTENDED_SOFT source candidates.
    for m in COMMON_KNOWLEDGE_RE.finditer(prose):
        add(
            findings,
            text,
            "ilyakhov: common-knowledge wrapper",
            m.group(0),
            m.start(),
            "PS-R09: check whether the wrapper contributes source/contrast; do not delete a real attribution",
        )

    numbering_hits = _count_patterns(prose, NUMBERING_PATTERNS)
    if len(numbering_hits) >= 2:
        first = numbering_hits[0]
        add(
            findings,
            text,
            "ilyakhov: verbal-numbering cluster",
            " … ".join(m.group(0) for m in numbering_hits[:4]),
            first.start(),
            "PS-R11: extended review only; numbering is normal in algorithms, referenced lists and explicit argument structure",
        )

    politeness_hits = _count_patterns(prose, POLITENESS_PATTERNS)
    if len(politeness_hits) >= 2:
        first = politeness_hits[0]
        add(
            findings,
            text,
            "ilyakhov: ceremonial-politeness cluster",
            " … ".join(m.group(0) for m in politeness_hits[:4]),
            first.start(),
            "PS-R13: check whether ceremony obscures reason, deadline, file or next action; ordinary politeness is not a defect",
        )

    intensifier_clusters = 0
    offset = 0
    for sent in sentences(prose):
        pos = prose.find(sent, offset)
        offset = max(pos + len(sent), offset)
        hits = list(INTENSIFIER_RE.finditer(sent))
        if len(hits) >= 3:
            intensifier_clusters += 1
            add(
                findings,
                text,
                "ilyakhov: intensifier cluster",
                sent,
                max(pos, 0),
                "PS-R18: clustered intensification may be substituting for evidence; one intensifier or deliberate hyperbole is normal",
            )

    for m in PRESENT_TIME_RE.finditer(prose):
        window = prose[max(0, m.start() - 120) : min(len(prose), m.end() + 160)]
        if TEMPORAL_CONTRAST_RE.search(window):
            continue
        add(
            findings,
            text,
            "ilyakhov: present-time wrapper",
            m.group(0),
            m.start(),
            "PS-R21: check whether the present-time marker creates an actual temporal contrast or date coordinate",
        )

    bureaucratic_shell_hits = 0
    for rx in BUREAUCRATIC_SHELL_PATTERNS:
        for m in rx.finditer(prose):
            bureaucratic_shell_hits += 1
            add(
                findings,
                text,
                "ilyakhov: bureaucratic-shell candidate",
                m.group(0),
                m.start(),
                "PS-R22: extended candidate only; legal/procedural register and responsibility may require the construction",
            )

    for m in META_INTRO_RE.finditer(prose):
        add(
            findings,
            text,
            "ilyakhov: meta-intro candidate",
            m.group(0),
            m.start(),
            "PS-R62: check whether this roadmap helps the genre; academic and long-form navigation may need it",
        )

    for m in RITUAL_CONCLUSION_RE.finditer(prose):
        add(
            findings,
            text,
            "ilyakhov: ritual-conclusion candidate",
            m.group(0),
            m.start(),
            "PS-R63: conclusion must add a function, not merely restate the text; formal genres may require a conclusion section",
        )

    for m in BROAD_PRECISION_RE.finditer(prose):
        add(
            findings,
            text,
            "ilyakhov: suspicious broad precision",
            m.group(0),
            m.start(),
            "PS-R76: verification prompt only; unusual precision is not evidence that a number is false",
        )

    generic_benefit_clusters = 0
    offset = 0
    for sent in sentences(prose):
        pos = prose.find(sent, offset)
        offset = max(pos + len(sent), offset)
        hit_count = sum(bool(rx.search(sent)) for rx in GENERIC_BENEFIT_PATTERNS)
        if hit_count >= 2:
            generic_benefit_clusters += 1
            add(
                findings,
                text,
                "ilyakhov: generic-benefit cluster",
                sent,
                max(pos, 0),
                "PS-R85: in self-presentation/commercial prose, replace generic praise only when the source already contains more specific benefit or evidence",
            )

    # METRIC_ONLY. No finding is emitted solely from these measurements.
    correlative_spans: list[int] = []
    correlative_count = 0
    for _label, rx in CORRELATIVE_PATTERNS:
        for m in rx.finditer(prose):
            body = m.group("body")
            if "\n\n" in body:
                continue
            correlative_count += 1
            correlative_spans.append(word_count(body))

    sents = sentences(prose)
    state_predicate_sentences = sum(1 for sent in sents if STATE_PREDICATE_RE.search(sent))
    comma_count = prose.count(",")
    multi_comma_sentences = sum(1 for sent in sents if sent.count(",") >= 3)

    metrics = {
        "ilyakhov_correlative_pairs": correlative_count,
        "ilyakhov_correlative_max_inner_words": max(correlative_spans, default=0),
        "ilyakhov_state_predicate_sentences": state_predicate_sentences,
        "ilyakhov_comma_count": comma_count,
        "ilyakhov_multi_comma_sentences_ge_3": multi_comma_sentences,
        "ilyakhov_intensifier_clusters": intensifier_clusters,
        "ilyakhov_bureaucratic_shell_candidates": bureaucratic_shell_hits,
        "ilyakhov_generic_benefit_clusters": generic_benefit_clusters,
    }
    return findings, metrics


def rules(text: str) -> set[str]:
    return {item["rule"] for item in lint(text)[0]}


def self_test() -> None:
    # ILY-M01 true positives.
    assert "ilyakhov: bureaucratic tautology" in rules(
        "В рамках проекта было осуществлено проведение проверки."
    )
    assert "ilyakhov: bureaucratic tautology" in rules(
        "Подрядчик должен произвести выполнение работ до пятницы."
    )

    # ILY-M01 natural negatives / boundaries / intentional official use.
    for safe in [
        "Мы провели исследование и отправили отчёт.",
        "Было проведено исследование условий труда.",
        "Нужно осуществить переход на новый тариф до пятницы.",
        "Комиссия выполнит проверку в установленный срок.",
        "Решение принято в рамках закона.",
    ]:
        assert "ilyakhov: bureaucratic tautology" not in rules(safe), (safe, lint(safe))

    assert "ilyakhov: common-knowledge wrapper" in rules("Как известно, этот способ используют давно.")
    assert "ilyakhov: common-knowledge wrapper" not in rules(
        "По данным отчёта за июль, этот способ используют 12 команд."
    )

    assert "ilyakhov: verbal-numbering cluster" in rules(
        "Во-первых, проверим данные. Во-вторых, сравним версии."
    )
    assert "ilyakhov: verbal-numbering cluster" not in rules("Во-первых, это только один аргумент.")

    assert "ilyakhov: ceremonial-politeness cluster" in rules(
        "Обращаем ваше внимание на срок. Просим вас прислать файл. С уважением, отдел."
    )
    assert "ilyakhov: ceremonial-politeness cluster" not in rules(
        "Пожалуйста, пришлите файл до пятницы."
    )

    assert "ilyakhov: intensifier cluster" in rules(
        "Это абсолютно, невероятно и действительно важный результат."
    )
    assert "ilyakhov: intensifier cluster" not in rules("Это очень важный для меня результат.")

    assert "ilyakhov: present-time wrapper" in rules(
        "В настоящее время компания выпускает три модели."
    )
    assert "ilyakhov: present-time wrapper" not in rules(
        "Раньше выпускали одну модель, а в настоящее время выпускаем три."
    )

    # Do not revive the old harmful cognitive-frame/state/passive checks.
    for safe in [
        "Я считаю, что решение рискованное.",
        "Мне кажется, данных пока недостаточно.",
        "По моим наблюдениям, очередь стала длиннее.",
        "Платёж отклонён банком.",
        "Контроллер является частью системы.",
        "Кого пригласили? Машу.",
    ]:
        bad = [r for r in rules(safe) if "cognitive" in r or "state" in r or "passive" in r]
        assert not bad, (safe, bad)

    long_clear = (
        "Если договор уже подписан и оплата поступила на счёт после проверки реквизитов, "
        "то заказ отправим в понедельник, когда откроется склад."
    )
    findings, metrics = lint(long_clear)
    assert metrics["ilyakhov_correlative_pairs"] >= 1
    assert metrics["ilyakhov_comma_count"] >= 2
    assert not [f for f in findings if "correlative" in f["rule"] or "comma" in f["rule"]]

    protected = "> Как известно, это цитата.\n\n`осуществить проведение` https://example.com/как-известно"
    protected_rules = rules(protected)
    assert "ilyakhov: bureaucratic tautology" not in protected_rules
    assert "ilyakhov: common-knowledge wrapper" not in protected_rules

    print("ilyakhov self-test: OK")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    text = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    findings, metrics = lint(text)
    if args.as_json:
        print(json.dumps({"findings": findings, "metrics": metrics}, ensure_ascii=False, indent=2))
    else:
        for item in findings:
            loc = f":{item['line']}" if item["line"] else ""
            note = f" — {item['note']}" if item["note"] else ""
            print(f"{item['kind']}{loc} [{item['rule']}]: {item['excerpt']}{note}")
        print(json.dumps(metrics, ensure_ascii=False))


if __name__ == "__main__":
    main()
