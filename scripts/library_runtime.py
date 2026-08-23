#!/usr/bin/env python3
"""Load knowledge libraries and normalize their findings for both product modes."""

from __future__ import annotations

import importlib.util
import inspect
import json
import re
from pathlib import Path
from typing import Any

from finding_contract import validate_normalized_finding

ROOT = Path(__file__).resolve().parents[1]
LIBRARIES = ROOT / "libraries"
REVIEWERS = ROOT / "reviewers"
STYLES = ROOT / "styles"

COMPACT_KIND_BY_PROJECT_CLASS = {
    "ARTIFACT": "ARTIFACT",
    "NORM": "LANGUAGE_ERROR",
    "NATIVE_USAGE": "NATIVE_WARNING",
    "EDITING": "STYLE_WARNING",
    "AI_CALQUE": "AI_PATTERN",
    "AUTHOR": "STYLE_WARNING",
}

# Internal rule ids stay stable and language-neutral. These labels are only the
# Russian human-facing surface used by Compact, Editorial Board and downstream
# consumers that render normalized findings.
DISPLAY_RULE_RU = {
    # Native/core
    "NATIVE-openai_citation_marker": "служебный маркер цитирования OpenAI",
    "NATIVE-tool_turn_marker": "служебный маркер вызова инструмента",
    "NATIVE-bracket_citation_placeholder": "служебная заглушка ссылки",
    "NATIVE-chatgpt_openai_utm": "служебная UTM-метка ChatGPT/OpenAI",
    "NATIVE-assistant_wrapper": "шаблонная реплика ассистента",
    "NATIVE-pseudo_depth": "шаблон псевдоглубины",
    "NATIVE-video_script": "сценарный шаблон",
    "NATIVE-generic_conclusion": "шаблонное заключение",
    "NATIVE-stack_connector": "цепочка однотипных связок",
    "NATIVE-calque_literal_possessives": "буквальный перенос притяжательных местоимений",
    "NATIVE-calque_address_a_problem": "калька «адресовать проблему»",
    "NATIVE-calque_deliver_value": "калька «доставлять ценность»",
    "NATIVE-calque_have_influence": "калька «иметь влияние»",
    "NATIVE-calque_be_ready_by": "калька конструкции «быть готовым к сроку»",
    "NATIVE-possessive_overexplication_candidate": "избыточные притяжательные местоимения",
    "NATIVE-repeated_common_element_in_contrast": "повтор общей части в противопоставлении",
    "NATIVE-repeated_contrast_formula": "повтор формулы противопоставления",
    "NATIVE-anglo_rhetorical_question_answer_cluster": "серия риторических вопросов и коротких ответов",
    "NATIVE-parcellated_enumeration": "разорванное перечисление",
    "NATIVE-short_fragment_cluster": "серия коротких фрагментов",
    "NATIVE-repeated_sentence_start": "повтор начала предложений",
    "NATIVE-repeated_explicit_context_candidate": "повтор явно названного контекста",
    "NATIVE-context_undercompression_candidate": "недостаточное контекстное сжатие",
    "NATIVE-ascii_hyphen_used_as_dash": "ASCII-дефис вместо тире",
    "NATIVE-high_dash_density": "высокая плотность тире",
    # Chukovsky
    "CHUK-R09": "плотность аббревиатур",
    "CHUK-R15": "скопление канцелярских маркеров",
    "CHUK-R17": "действие, спрятанное в отглагольной конструкции",
    "CHUK-R18": "кандидат на удаление избыточного определения",
    "CHUK-R19": "повтор оценочного штампа",
    "CHUK-R24": "вводная рамка перед сообщением",
    "CHUK-R25": "повтор упаковки через слово «вопрос»",
    # Nora Gal
    "GAL-KANZ-VERB": "действие, спрятанное в служебной конструкции",
    "GAL-KANZ-PSEUDOFORMAL": "избыточно официальная оболочка",
    "GAL-EXPLICITNESS": "избыточная явность",
    # Ilyakhov
    "ILY-M01": "дублирование действия служебной конструкцией",
    "ILY-R09": "оболочка «как известно»",
    "ILY-R11": "серия словесной нумерации",
    "ILY-R13": "скопление церемониальной вежливости",
    "ILY-R18": "скопление усилителей",
    "ILY-R22": "канцелярская оболочка",
    "ILY-R62": "мета-вступление",
    "ILY-R63": "ритуальное заключение",
    "ILY-R76": "подозрительно точная широкая статистика",
    "ILY-R85": "скопление общих рекламных преимуществ",
    # Golub
    "GOLUB-R40": "управление после «согласно»",
    "GOLUB-R41": "управление глаголов оплаты",
    "GOLUB-R44": "двойная сравнительная степень",
    "GOLUB-R59": "согласование парного союза",
    # Rosenthal
    "ROS-R30": "согласование парного союза",
    "ROS-R44": "управление после «согласно»",
    "ROS-R53": "двойная сравнительная степень",
    # Russian language layer
    "RU-NORM-HEADING-PERIOD": "точка в конце заголовка",
    "RU-STYLE-UNMARKED-HEADING": "неразмеченный заголовок",
    "RU-NORM-LIST-DOT-MARKER-CAPITAL": "оформление пункта после номера с точкой",
    "RU-LIST-CASE-PUNCTUATION-CONSISTENCY": "смешение схем оформления списка",
    "RU-SEM-MEMBER-COLLECTION-EQUATION": "приравнивание элемента к коллекции",
    "RU-REGISTER-JARGON-TERM": "жаргон или термин не по регистру",
    "RU-LEX-LATIN-IN-RUSSIAN": "латинское слово в русской фразе",
    "RU-NATIVE-SPLIT-CONTRAST": "разорванное противопоставление",
    # Visson
    "VISSON-NORM-ASK-QUESTION": "управление в конструкции «спросить вопрос»",
    "VISSON-CALQUE-PRETEND-CLAUSE": "ложный друг «претендовать, что…»",
    "VISSON-CALQUE-HAVE-NICE-DAY": "буквальная формула «имейте хороший день»",
    "VISSON-CALQUE-HAPPY-BIRTHDAY": "буквальная формула «счастливого дня рождения»",
    "VISSON-CALQUE-ENJOY-STANDALONE": "буквальная формула «наслаждайтесь!»",
}

REASON_RU = {
    # Native/core
    "NATIVE-openai_citation_marker": "Технический след; убрать перед публикацией.",
    "NATIVE-tool_turn_marker": "Технический след; убрать перед публикацией.",
    "NATIVE-bracket_citation_placeholder": "Технический след; убрать перед публикацией.",
    "NATIVE-chatgpt_openai_utm": "Технический след; убрать перед публикацией.",
    "NATIVE-assistant_wrapper": (
        "Слабый сигнал происхождения текста: сама формула ничего не доказывает. "
        "Оценивайте её по функции и повторяемости в тексте."
    ),
    "NATIVE-pseudo_depth": (
        "Слабый сигнал происхождения текста: сама формула ничего не доказывает. "
        "Оценивайте её по функции и повторяемости в тексте."
    ),
    "NATIVE-video_script": (
        "Слабый сигнал происхождения текста: сама формула ничего не доказывает. "
        "Оценивайте её по функции и повторяемости в тексте."
    ),
    "NATIVE-generic_conclusion": (
        "Слабый сигнал происхождения текста: сама формула ничего не доказывает. "
        "Оценивайте её по функции и повторяемости в тексте."
    ),
    "NATIVE-stack_connector": (
        "Слабый сигнал происхождения текста: сама формула ничего не доказывает. "
        "Оценивайте её по функции и повторяемости в тексте."
    ),
    "NATIVE-calque_literal_possessives": "Только кандидат на кальку: проверьте естественность сочетания, аудиторию и контекст.",
    "NATIVE-calque_address_a_problem": "Только кандидат на кальку: проверьте естественность сочетания, аудиторию и контекст.",
    "NATIVE-calque_deliver_value": "Только кандидат на кальку: проверьте естественность сочетания, аудиторию и контекст.",
    "NATIVE-calque_have_influence": "Только кандидат на кальку: проверьте естественность сочетания, аудиторию и контекст.",
    "NATIVE-calque_be_ready_by": "Только кандидат на кальку: проверьте естественность сочетания, аудиторию и контекст.",
    "NATIVE-possessive_overexplication_candidate": (
        "Русский часто опускает очевидное владение. Проверьте, можно ли убрать одно "
        "или несколько притяжательных местоимений без двусмысленности."
    ),
    "NATIVE-repeated_common_element_in_contrast": (
        "Общую часть, возможно, лучше назвать один раз, а затем заново проверить "
        "порядок слов, противопоставление и смысловой акцент."
    ),
    "NATIVE-repeated_contrast_formula": (
        "Конструкция «не X, а Y» нормативна. Замечание относится только к навязчивому "
        "повтору одного и того же риторического хода."
    ),
    "NATIVE-anglo_rhetorical_question_answer_cluster": (
        "Короткая пара «вопрос — ответ» естественна в диалоге. Проверяйте только "
        "серийное использование таких ударных реплик в объяснительном или рекламном тексте."
    ),
    "NATIVE-parcellated_enumeration": (
        "Проверьте, не вводит ли первая часть перечисление, которое по-русски естественнее "
        "собрать в одну конструкцию с двоеточием."
    ),
    "NATIVE-short_fragment_cluster": (
        "Парцелляция может быть намеренной. Проверьте, добавляет ли каждый разрыв акцент, "
        "а не маскирует одну синтаксическую конструкцию."
    ),
    "NATIVE-repeated_sentence_start": (
        "Возможен лишний повтор уже известного контекста. Сжимайте или меняйте порядок слов "
        "только если после этого всё остаётся однозначным."
    ),
    "NATIVE-repeated_explicit_context_candidate": (
        "Несколько соседних предложений заново называют один и тот же субъект. Проверьте, "
        "можно ли использовать местоимение, нулевой субъект, эллипсис или другой порядок темы и ремы."
    ),
    "NATIVE-context_undercompression_candidate": (
        "Соседние предложения повторяют несколько содержательных слов. Проверьте, может ли "
        "второе опереться на уже заданный контекст вместо повторного называния того же материала."
    ),
    "NATIVE-ascii_hyphen_used_as_dash": (
        "Проверьте типографику: в русской прозе здесь, вероятно, нужно тире. "
        "Не меняйте нормативное тире ради обхода AI-детекторов."
    ),
    "NATIVE-high_dash_density": (
        "Это только эвристика: проверьте, не повторяется ли одна и та же конструкция с тире."
    ),
    # Chukovsky
    "CHUK-R09": (
        "Если текст рассчитан на нового или неспециализированного читателя, проверьте, "
        "нужно ли расшифровать аббревиатуры при первом упоминании. Устоявшиеся отраслевые "
        "сокращения могут быть оптимальны."
    ),
    "CHUK-R15": (
        "Проверьте, соответствует ли такая плотность канцелярских оборотов жанру и можно ли "
        "сказать прямее. В официальном, юридическом или техническом тексте формулировка может быть уместной."
    ),
    "CHUK-R18": (
        "Сравните вариант без определения. Оставьте его, если меняются объём значения, "
        "противопоставление, степень, хронология, позиция автора, терминология или ритм."
    ),
    "CHUK-R19": (
        "Проверьте, не повторяется ли одна и та же оценочная функция. Если источник позволяет, "
        "лучше назвать наблюдение или факт; не придумывайте конкретику ради оживления текста."
    ),
    "CHUK-R24": (
        "Сравните вариант без вводной рамки. Оставьте её, если она действительно задаёт "
        "модальность, предупреждение, навигацию или противопоставление."
    ),
    "CHUK-R25": (
        "Проверьте, можно ли назвать само действие прямо. Слово «вопрос» оставьте там, "
        "где речь действительно идёт о вопросе, теме или проблеме."
    ),
    # Nora Gal
    "GAL-KANZ-VERB": (
        "По системе Норы Галь это кандидат на проверку: действие может быть спрятано "
        "в служебном глаголе и отглагольном существительном. Не меняйте механически "
        "в юридическом или терминологическом контексте."
    ),
    "GAL-KANZ-PSEUDOFORMAL": (
        "Многословная служебная оболочка. Проверьте, нужна ли такая степень официальности "
        "этому адресату и жанру."
    ),
    "GAL-EXPLICITNESS": (
        "Возможна лишняя явность. Убирайте только то, что однозначно восстанавливается "
        "из контекста; функциональный повтор сохраняйте."
    ),
    # Ilyakhov
    "ILY-M01": (
        "Действие продублировано служебным глаголом и отглагольным существительным. "
        "Упростите, только если не меняются официальный или юридический смысл и распределение ответственности."
    ),
    "ILY-R09": (
        "Проверьте, добавляет ли оборот вроде «как известно» реальный источник или противопоставление. "
        "Не превращайте неподтверждённую очевидность в факт."
    ),
    "ILY-R11": (
        "Только редакторский сигнал: явная нумерация нормальна в алгоритмах, списках со ссылками "
        "и намеренно пошаговой аргументации."
    ),
    "ILY-R13": (
        "Проверьте, не прячутся ли за церемониальными формулами причина, срок, нужный файл "
        "или следующее действие. Обычная вежливость и формальные конвенции нормальны."
    ),
    "ILY-R18": (
        "Скопление усилителей может подменять доказательства. Намеренная гипербола "
        "или эмоциональный авторский голос могут быть уместны."
    ),
    "ILY-R22": (
        "Это только поверхностный кандидат: юридический или процедурный регистр, распределение "
        "ответственности и терминологичность требуют контекста."
    ),
    "ILY-R62": (
        "Сравните с прямым началом. В академическом или длинном тексте такая навигационная рамка "
        "может быть полезна."
    ),
    "ILY-R63": (
        "У заключения должна быть функция помимо ритуального повтора. В некоторых формальных "
        "жанрах отдельный раздел с выводами действительно требуется."
    ),
    "ILY-R76": (
        "Это повод проверить источник, метод, охват и период. Необычная точность сама по себе "
        "не доказывает, что число неверно."
    ),
    "ILY-R85": (
        "В самопрезентации и рекламном тексте лучше заменить набор общих достоинств подтверждаемой "
        "конкретикой. Слоган может остаться вторичным слоем, если выполняет свою функцию."
    ),
    # Golub
    "GOLUB-R40": (
        "По современной норме «согласно» требует дательного падежа. Проверка срабатывает только "
        "на ограниченный набор надёжно распознаваемых форм; цитаты, код, URL и разметка исключены."
    ),
    "GOLUB-R41": (
        "Для проверяемого набора значений нормативно: «оплатить что» или «заплатить за что». "
        "Проверка намеренно не пытается охватить все употребления предлога «за»."
    ),
    "GOLUB-R44": "Два способа образования сравнительной степени не должны механически совмещаться.",
    "GOLUB-R59": (
        "Проверьте симметрию парного союза. Эта механическая проверка общая с системой Розенталя; "
        "сложную синтаксическую структуру нужно оценивать в контексте."
    ),
    # Visson
    "VISSON-NORM-ASK-QUESTION": (
        "Здесь английская модель `ask a question` перенесена на русский глагол «спросить». "
        "Нормативно: «задать вопрос» или «спросить кого-либо о чём-либо». Цитаты и метаязык "
        "исключены; намеренная языковая игра допустима."
    ),
    "VISSON-CALQUE-PRETEND-CLAUSE": (
        "Похоже на перенос английского `pretend that`: русское «претендовать» обычно требует "
        "предлога «на», а притворство выражается глаголами «притворяться» или «делать вид». "
        "Проверьте смысл; конструкция «претендовать на то, что…» этой механической проверкой не охватывается."
    ),
    "VISSON-CALQUE-HAVE-NICE-DAY": (
        "Вероятна буквальная калька `Have a nice day`. По-русски пожелание обычно обходится "
        "без глагола «иметь»: «Хорошего дня», «Всего доброго» и т. п."
    ),
    "VISSON-CALQUE-HAPPY-BIRTHDAY": (
        "Самостоятельное «Счастливого дня рождения!» похоже на буквальное `Happy Birthday`. "
        "Нейтральная русская формула — «С днём рождения!»."
    ),
    "VISSON-CALQUE-ENJOY-STANDALONE": (
        "Изолированное «Наслаждайтесь!» может калькировать универсальное английское `Enjoy!`. "
        "По-русски пожелание обычно называет ситуацию: «Приятного аппетита», «Приятного просмотра», "
        "«Хорошего отдыха». Оставьте «наслаждайтесь», если буквально это и имеется в виду."
    ),
}


def slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-zа-яё0-9]+", "_", value, flags=re.I)
    return value.strip("_") or "unknown"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def library_manifests(include_disabled: bool = False) -> list[dict[str, Any]]:
    manifests = []
    for path in sorted(LIBRARIES.glob("*/library.json")):
        if path.parent.name.startswith("_"):
            continue
        manifest = load_json(path)
        manifest["_manifest_path"] = str(path.relative_to(ROOT))
        if include_disabled or manifest.get("enabled_by_default", False):
            manifests.append(manifest)
    return manifests


def reviewer_profiles() -> dict[str, dict[str, Any]]:
    out = {}
    for path in sorted(REVIEWERS.glob("*.json")):
        if path.name.startswith("_"):
            continue
        item = load_json(path)
        out[item["id"]] = item
    return out


def load_style(style_id: str) -> dict[str, Any]:
    path = STYLES / f"{style_id}.json"
    if not path.is_file():
        raise ValueError(f"unknown style: {style_id}")
    return load_json(path)


def import_path(relative: str):
    path = ROOT / relative
    if not path.is_file():
        raise FileNotFoundError(f"library linter missing: {relative}")
    name = f"humanizer_library_{slug(relative)}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import library module: {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _localize_reason(out: dict[str, Any]) -> str:
    rule_id = str(out.get("rule_id") or "")
    reason = str(out.get("reason") or "")

    # CHUK-R17 has two detector routes. Preserve the useful count for a dense
    # nominalization sentence while keeping the wording idiomatic Russian.
    if rule_id == "CHUK-R17":
        count_match = re.match(r"\s*(\d+)\s+surface nominalization candidates\b", reason)
        if count_match:
            count = int(count_match.group(1))
            return (
                f"Отглагольных существительных по формальным признакам: {count}. "
                "Сначала восстановите действия и участников; только потом решайте, "
                "действительно ли фраза перегружена."
            )
        return (
            "Попробуйте восстановить схему «кто — что делает — с чем или с каким результатом». "
            "Не придумывайте неизвестного деятеля и не запрещайте отглагольные существительные как класс."
        )

    return REASON_RU.get(rule_id, reason)


def _localize_excerpt(out: dict[str, Any]) -> str:
    rule_id = str(out.get("rule_id") or "")
    excerpt = str(out.get("excerpt") or "")

    if rule_id == "NATIVE-repeated_contrast_formula":
        match = re.fullmatch(r"\s*(\d+)\s+contrast formulae\s*", excerpt)
        if match:
            return f"{match.group(1)} формулы противопоставления"

    if rule_id == "NATIVE-anglo_rhetorical_question_answer_cluster":
        match = re.fullmatch(
            r"\s*(\d+)\s+slogan markers;\s*(\d+)\s+short question-answer pairs\s*",
            excerpt,
        )
        if match:
            return (
                f"{match.group(1)} маркера слогана; "
                f"{match.group(2)} коротких пар «вопрос — ответ»"
            )

    if rule_id == "NATIVE-high_dash_density":
        match = re.fullmatch(r"\s*(\d+)\s+dashes\s*/\s*(\d+)\s+sentences\s*", excerpt)
        if match:
            return f"{match.group(1)} тире / {match.group(2)} предложений"

    if rule_id == "CHUK-R15":
        labels = {
            "paper-deictic": "указательные канцеляризмы",
            "procedural-frame": "процедурные обороты",
            "existence-wrapper": "оболочки существования",
            "administrative-action": "административные глаголы",
        }
        for source, target in labels.items():
            excerpt = excerpt.replace(f"{source}:", f"{target}:")

    return excerpt


def _apply_russian_surface(out: dict[str, Any]) -> dict[str, Any]:
    rule_id = str(out.get("rule_id") or "")
    display_rule = DISPLAY_RULE_RU.get(rule_id)
    if display_rule:
        out["display_rule_ru"] = display_rule
    out["reason"] = _localize_reason(out)
    out["excerpt"] = _localize_excerpt(out)
    return out


def normalize_review_v1(item: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    out = dict(item)
    out.setdefault("line", 0)
    out.setdefault("excerpt", "")
    out.setdefault("reason", "")
    out.setdefault("operation", None)
    out.setdefault("confidence", None)
    out["library_id"] = manifest["id"]
    out["source_namespace"] = manifest["source_namespace"]
    out.setdefault("reviewer_id", manifest.get("reviewer_id"))
    validate_normalized_finding(out, manifest["id"])
    return _apply_russian_surface(out)


def _call_review(module: Any, text: str, context: dict[str, Any] | None) -> dict[str, Any]:
    """Pass optional runtime context only to adapters that declare it."""
    params = inspect.signature(module.review).parameters
    if "context" in params:
        return module.review(text, context=context or {})
    return module.review(text)


def run_library(
    manifest: dict[str, Any],
    text: str,
    context: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    module = import_path(manifest["linter_path"])
    adapter = manifest["adapter"]
    if adapter != "review_v1":
        raise ValueError(f"unsupported adapter: {adapter}; operational libraries must use review_v1")
    result = _call_review(module, text, context)
    return [
        normalize_review_v1(item, manifest)
        for item in result.get("findings", [])
    ], result.get("metrics", {})


def run_libraries(
    text: str,
    library_ids: list[str] | None = None,
    context: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifests = library_manifests(include_disabled=bool(library_ids))
    if library_ids:
        wanted = set(library_ids)
        manifests = [m for m in manifests if m["id"] in wanted]
        missing = wanted - {m["id"] for m in manifests}
        if missing:
            raise ValueError(f"unknown libraries: {', '.join(sorted(missing))}")
    findings: list[dict[str, Any]] = []
    metrics: dict[str, Any] = {}
    for manifest in manifests:
        lib_findings, lib_metrics = run_library(manifest, text, context=context)
        findings.extend(lib_findings)
        metrics[manifest["id"]] = lib_metrics
    return findings, metrics


def compact_shape(item: dict[str, Any]) -> dict[str, Any]:
    """Stable compact shape compatible with the existing check/benchmark interface."""
    project_class = item.get("project_class")
    display_kind = item.get("display_kind")
    if display_kind:
        kind = display_kind
    else:
        try:
            kind = COMPACT_KIND_BY_PROJECT_CLASS[project_class]
        except KeyError as exc:
            raise ValueError(f"unsupported compact project_class: {project_class!r}") from exc
    return {
        "kind": kind,
        "line": item.get("line", 0),
        "rule": item.get("display_rule") or item["rule_id"],
        "excerpt": item.get("excerpt", ""),
        "note": item.get("reason", ""),
        "library_id": item.get("library_id"),
        "reviewer_id": item.get("reviewer_id"),
        "phenomenon_id": item.get("phenomenon_id"),
        "project_class": project_class,
        "automation_level": item.get("automation_level"),
        "verdict": item.get("verdict"),
    }