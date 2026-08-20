#!/usr/bin/env python3
"""Conservative reverse-interference checks for Lynn Visson's contrastive source.

The source mainly teaches Russian speakers English. This adapter only emits
Russian findings after reversing an audited contrast. Semantic/valency/aspect
cases remain MODEL_ONLY; regex is used only for narrow surfaces that survived
negative controls.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from lint import URL_OR_CODE, strip_frontmatter
except ImportError:  # package context
    from scripts.lint import URL_OR_CODE, strip_frontmatter

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_NON_PROSE_LINE = re.compile(r"^\s*(#|\||[-*+]\s|\d+\.\s|>)")

ASK_VERB = r"(?:спросить|спрошу|спросишь|спросит|спросим|спросите|спросят|спросил(?:а|и)?|спрашивать|спрашиваю|спрашиваешь|спрашивает|спрашиваем|спрашиваете|спрашивают|спрашивал(?:а|и)?)"
ASK_QUESTION = re.compile(
    rf"\b{ASK_VERB}\s+(?:(?:у\s+[А-Яа-яЁё-]+|вам|тебе|ему|ей|нам|им)\s+)?"
    r"(?:(?:один|этот|следующий|важный|короткий)\s+)?вопрос(?:ы)?\b",
    re.I,
)
PRETEND_CLAUSE = re.compile(
    r"\bпретенд(?:овать|ую|уешь|ует|уем|уете|уют|овал(?:а|и)?)\s*,\s*(?:что|будто|словно)\b",
    re.I,
)
HAVE_NICE_DAY = re.compile(
    r"\bимейте?\s+(?:хороший|приятный|замечательный|прекрасный)\s+день\b",
    re.I,
)
HAPPY_BIRTHDAY_LINE = re.compile(r"^\s*счастливого\s+дня\s+рождения\s*[!?.…]*\s*$", re.I)
ENJOY_LINE = re.compile(r"^\s*наслаждайтесь\s*[!?.…]*\s*$", re.I)
SENTENCE_INITIAL_PRONOUN = re.compile(r"(?:^|(?<=[.!?])\s+)(?:я|мы|ты|вы|он|она|оно|они)\b", re.I)
SVO_LIKE = re.compile(
    r"(?:^|(?<=[.!?])\s+)(?:я|мы|ты|вы|он|она|оно|они)\s+"
    r"[А-Яа-яЁё-]{3,}(?:л(?:а|и)?|ет|ют|ит|ат|ят|ем|им|ете|ите|у|ю)\b",
    re.I,
)
METRIC_RULE_IDS = ["VISSON-NATIVE-SUBJECT-OMISSION", "VISSON-CALQUE-SVO-LOCK"]


def _line(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _blank_same_length(match: re.Match[str]) -> str:
    value = match.group(0)
    return "".join("\n" if ch == "\n" else " " for ch in value)


def _mask_quotes(text: str) -> str:
    # Precision-first: ordinary quoted language is treated as citation/metalinguistic
    # material. This sacrifices recall in dialogue, which is preferable to flagging
    # examples such as «спросить вопрос» in linguistic prose.
    patterns = [r"«[^»\n]*»", r"“[^”\n]*”", r'"[^"\n]*"']
    for pattern in patterns:
        text = re.sub(pattern, _blank_same_length, text)
    return text


def _line_preserving_prose(text: str) -> str:
    clean = URL_OR_CODE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    lines = strip_frontmatter(clean.splitlines())
    kept: list[str] = []
    for line in lines:
        if not line.strip() or MARKDOWN_NON_PROSE_LINE.match(line):
            kept.append("")
            continue
        kept.append(_mask_quotes(line))
    return "\n".join(kept)


def _finding(*, rule_id: str, phenomenon_id: str, project_class: str,
             automation_level: str, verdict: str, excerpt: str, line: int,
             reason: str, operation: str, reviewer_id: str | None = "visson") -> dict:
    item = {
        "rule_id": rule_id,
        "phenomenon_id": phenomenon_id,
        "project_class": project_class,
        "automation_level": automation_level,
        "verdict": verdict,
        "line": line,
        "excerpt": excerpt[:180],
        "reason": reason,
        "operation": operation,
        "confidence": None,
    }
    if reviewer_id is None:
        item["reviewer_id"] = None
    return item


def review(text: str, context: dict | None = None) -> dict:
    findings: list[dict] = []
    prose = _line_preserving_prose(text)

    for match in ASK_QUESTION.finditer(prose):
        findings.append(_finding(
            rule_id="VISSON-NORM-ASK-QUESTION",
            phenomenon_id="norm.ask_question_valency",
            project_class="NORM",
            automation_level="DEFAULT_MECHANICAL",
            verdict="CHANGE",
            excerpt=match.group(0),
            line=_line(prose, match.start()),
            reason=("Английская рамка ask a question перенесена на русский `спросить`. "
                    "Нормативно: `задать вопрос` либо `спросить кого-либо о чём-либо`. "
                    "Цитаты/метаязык маскируются; намеренная языковая игра не является ошибкой текста."),
            operation="restore_ask_question_valency",
            reviewer_id=None,
        ))

    for match in PRETEND_CLAUSE.finditer(prose):
        findings.append(_finding(
            rule_id="VISSON-CALQUE-PRETEND-CLAUSE",
            phenomenon_id="russian.false_friend_pretend_claim",
            project_class="AI_CALQUE",
            automation_level="DEFAULT_MECHANICAL",
            verdict="REVIEW",
            excerpt=match.group(0),
            line=_line(prose, match.start()),
            reason=("Похоже на перенос English `pretend that`: русское `претендовать` обычно строится "
                    "с `на`, а значение притворства выражается `притворяться / делать вид`. "
                    "Проверить смысл; `претендовать на то, что...` этим regex не охватывается."),
            operation="replace_false_friend_pretend_frame",
        ))

    for match in HAVE_NICE_DAY.finditer(prose):
        findings.append(_finding(
            rule_id="VISSON-CALQUE-HAVE-NICE-DAY",
            phenomenon_id="russian.literal_have_nice_day",
            project_class="AI_CALQUE",
            automation_level="EXTENDED_SOFT",
            verdict="REVIEW",
            excerpt=match.group(0),
            line=_line(prose, match.start()),
            reason="Вероятная буквальная формула `Have a nice day`; в русском обычно выражают пожелание без `иметь`: `Хорошего дня`, `Всего доброго` и т. п.",
            operation="replace_literal_farewell_formula",
        ))

    for offset, line_text in _iter_lines(prose):
        if HAPPY_BIRTHDAY_LINE.match(line_text):
            findings.append(_finding(
                rule_id="VISSON-CALQUE-HAPPY-BIRTHDAY",
                phenomenon_id="russian.literal_happy_birthday",
                project_class="AI_CALQUE",
                automation_level="EXTENDED_SOFT",
                verdict="REVIEW",
                excerpt=line_text.strip(),
                line=_line(prose, offset),
                reason="Самостоятельное `Счастливого дня рождения!` похоже на буквальное `Happy Birthday`; нейтральная русская формула — `С днём рождения!`.",
                operation="replace_literal_birthday_formula",
            ))
        if ENJOY_LINE.match(line_text):
            findings.append(_finding(
                rule_id="VISSON-CALQUE-ENJOY-STANDALONE",
                phenomenon_id="russian.literal_enjoy_formula",
                project_class="AI_CALQUE",
                automation_level="EXTENDED_SOFT",
                verdict="REVIEW",
                excerpt=line_text.strip(),
                line=_line(prose, offset),
                reason="Изолированное `Наслаждайтесь!` может калькировать универсальное English `Enjoy!`; по-русски формула обычно называет ситуацию (`Приятного аппетита/просмотра`, `Хорошего отдыха`). Оставить, если буквально нужно `наслаждаться`.",
                operation="replace_generic_enjoy_formula_by_context",
            ))

    metrics = {
        "metric_rule_ids": METRIC_RULE_IDS,
        "explicit_subject_pronoun_starts": len(SENTENCE_INITIAL_PRONOUN.findall(prose)),
        "svo_like_pronoun_starts": len(SVO_LIKE.findall(prose)),
        "metrics_are_descriptive": True,
        "thresholds_calibrated": False,
    }
    return {"findings": findings, "metrics": metrics}


def _iter_lines(text: str):
    offset = 0
    for line in text.splitlines(keepends=True):
        raw = line[:-1] if line.endswith("\n") else line
        yield offset, raw
        offset += len(line)
    if text and not text.endswith("\n"):
        return


def self_test() -> None:
    def ids(text: str):
        return {x["rule_id"] for x in review(text)["findings"]}

    assert "VISSON-NORM-ASK-QUESTION" in ids("Я хочу спросить у вас вопрос о сроках.")
    assert "VISSON-NORM-ASK-QUESTION" in ids("Можно спросить один вопрос?")
    assert "VISSON-NORM-ASK-QUESTION" not in ids("Я хочу задать вам вопрос о сроках.")
    assert "VISSON-NORM-ASK-QUESTION" not in ids("Я хочу спросить у вас о вопросе, который вчера обсуждали.")
    assert "VISSON-NORM-ASK-QUESTION" not in ids("В статье разбирается выражение «спросить вопрос».")
    assert not review("```text\nЯ хочу спросить у вас вопрос.\n```")["findings"]

    assert "VISSON-CALQUE-PRETEND-CLAUSE" in ids("Он претендует, что ничего не знает.")
    assert "VISSON-CALQUE-PRETEND-CLAUSE" not in ids("Он претендует на должность директора.")
    assert "VISSON-CALQUE-PRETEND-CLAUSE" not in ids("Он не претендует на то, что теория окончательна.")
    assert "VISSON-CALQUE-PRETEND-CLAUSE" not in ids("Калька «претендует, что» приведена как пример.")

    assert "VISSON-CALQUE-HAVE-NICE-DAY" in ids("Имейте хороший день!")
    assert "VISSON-CALQUE-HAVE-NICE-DAY" not in ids("Имейте в виду: день будет сложным.")
    assert "VISSON-CALQUE-HAPPY-BIRTHDAY" in ids("Счастливого дня рождения!")
    assert "VISSON-CALQUE-HAPPY-BIRTHDAY" not in ids("Желаю тебе счастливого дня рождения!")
    assert "VISSON-CALQUE-ENJOY-STANDALONE" in ids("Наслаждайтесь!")
    assert "VISSON-CALQUE-ENJOY-STANDALONE" not in ids("Наслаждайтесь тишиной, пока есть возможность.")

    metrics = review("Я открыл файл. Я проверил данные. Мы отправили отчёт.")["metrics"]
    assert metrics["explicit_subject_pronoun_starts"] >= 3, metrics
    assert set(metrics["metric_rule_ids"]) == set(METRIC_RULE_IDS)
    print("visson linter self-test: OK")


def main() -> None:
    parser = argparse.ArgumentParser(description="Lynn Visson reverse-interference reviewer")
    parser.add_argument("file", nargs="?")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test(); return
    text = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    result = review(text)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in result["findings"]:
            print(f"{item['rule_id']}:{item['line']} {item['excerpt']} — {item['reason']}")
        print(json.dumps(result["metrics"], ensure_ascii=False))

if __name__ == "__main__":
    main()
