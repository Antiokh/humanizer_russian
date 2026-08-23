#!/usr/bin/env python3
"""Собирает детерминированный пакет Custom GPT из текущего репозитория.

Пакет намеренно отличается от пакета Agent Skill:
- Instructions/ содержит текст для настройки GPT Builder;
- Knowledge/ содержит не более 20 текстовых файлов для загрузки в GPT Knowledge;
- исполняемые скрипты рабочего контура сюда не входят: GPT Knowledge служит
  справочным материалом, а не способом установки Python-кода.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = "humanizer-russian-gpts"
MAX_KNOWLEDGE_FILES = 20
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)

REFERENCE_EXCLUDE = {
    "native-russian-user-context.md",  # материал разработки и исследования источников
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip() + "\n"


def skill_version() -> str:
    text = read_text(ROOT / "SKILL.md")
    match = re.search(r"(?m)^\s*version:\s*[\"']?([^\"'\n]+)", text)
    return match.group(1).strip() if match else "unversioned"


def existing(paths: Iterable[str]) -> list[Path]:
    result: list[Path] = []
    for rel in paths:
        path = ROOT / rel
        if path.is_file():
            result.append(path)
    return result


def all_files(rel_dir: str) -> list[Path]:
    base = ROOT / rel_dir
    if not base.exists():
        return []
    return sorted(p for p in base.rglob("*") if p.is_file())


def format_source(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    text = read_text(path)
    suffix = path.suffix.lower()
    if suffix == ".md":
        body = text
    elif suffix == ".json":
        body = f"```json\n{text.rstrip()}\n```\n"
    else:
        body = f"```text\n{text.rstrip()}\n```\n"
    return f"\n---\n\n## Источник: `{rel}`\n\n{body}"


def write_bundle(path: Path, title: str, purpose: str, sources: Iterable[Path]) -> list[str]:
    unique = sorted(
        {p.resolve(): p for p in sources}.values(),
        key=lambda p: p.relative_to(ROOT).as_posix(),
    )
    rels = [p.relative_to(ROOT).as_posix() for p in unique]
    body = [
        f"# {title}\n\n",
        "Сгенерировано из канонического репозитория `humanizer_russian`.\n\n",
        f"Назначение: {purpose}\n\n",
        "Используйте этот файл как справочный материал. Приоритеты поведения и рабочий процесс заданы в `Instructions/INSTRUCTIONS.md`.\n",
    ]
    for src in unique:
        body.append(format_source(src))
    path.write_text("".join(body).rstrip() + "\n", encoding="utf-8")
    return rels


def reference_files() -> list[Path]:
    base = ROOT / "references"
    if not base.exists():
        return []
    return sorted(
        p for p in base.glob("*.md")
        if p.name not in REFERENCE_EXCLUDE
    )


def select_refs(refs: list[Path], *needles: str) -> list[Path]:
    selected: list[Path] = []
    for p in refs:
        name = p.name.lower()
        if any(needle.lower() in name for needle in needles):
            selected.append(p)
    return selected


def make_instructions(out: Path) -> None:
    source = read_text(ROOT / "gpt" / "INSTRUCTIONS.md")
    boundary = """# Граница рабочего контура Custom GPT\n\nЭтот пакет настраивает Custom GPT. Файлы в `Knowledge/` — справочный материал, а не установленный Python-runtime.\n\n- Не утверждай, что `scripts/check.py`, `review.py`, механический линтер или провайдер доказательств были запущены, если реальный внешний рабочий контур или Action не выполнил их и не вернул результат.\n- Канонические механические правила включены в пакет как знания и могут использоваться при модельном ревью, но это не равнозначно детерминированному запуску.\n- Провайдеры доказательств со статусом `PROJECT` остаются недоступными и не должны представляться как рабочие.\n- Сохраняй факты и намерение пользователя до стилевой оптимизации.\n\nИмена справочных пакетов перечислены в `Knowledge/00_INDEX.md`.\n\n---\n\n"""
    out.write_text(boundary + source, encoding="utf-8")


def builder_guide() -> str:
    return """# Настройка GPT Builder\n\n## Название\n\n`humanizer_russian · Русский редактор`\n\n## Описание\n\nРусский редактор: естественный русский без кальки с английского, с сохранением смысла, нормы, жанра и авторского голоса.\n\n## Что загрузить\n\n1. Откройте редактор GPT.\n2. Вставьте всё содержимое `Instructions/INSTRUCTIONS.md` в поле GPT **Instructions**.\n3. Загрузите каждый `.md` из `Knowledge/` в раздел **Knowledge**. Файлы из `Instructions/` не загружайте как Knowledge.\n4. Оставьте **Code Interpreter & Data Analysis** включённым, если GPT должен редактировать или возвращать пользовательские файлы.\n5. Включайте **Web Search** только когда нужны актуальные факты или внешняя проверка спорной либо изменившейся языковой нормы.\n6. Проверьте сборку в Preview по `Instructions/TESTS.md`.\n\n## Важная граница\n\nЭтот пакет Custom GPT содержит модель, инструкции и знания. Он не устанавливает детерминированный Python-runtime репозитория. Чтобы GPT мог правдиво сказать, что `check.py` или провайдер доказательств действительно запускался, нужен GPT Action или другая реальная среда выполнения.\n\n## Обновление\n\nПересобирайте архив из репозитория, а не копируйте справочные файлы вручную. Сборщик объединяет канонические библиотеки в совместимый с GPT набор, не превышающий лимит файлов Knowledge.\n"""


def conversation_starters() -> str:
    return """# Заготовки начала диалога\n\n1. Отредактируй текст: сохрани смысл и голос автора, убери кальки и неестественные конструкции.\n2. Проведи глубокий аудит русского текста: норма, естественность, редактура и возможные AI-кальки.\n3. Переведи на русский так, чтобы результат звучал как оригинальный русский текст, а не перевод с английского.\n4. Сравни исходник и редактуру и покажи только изменения, которые действительно улучшают текст.\n"""


def build_directory(dest: Path) -> dict:
    if dest.exists():
        shutil.rmtree(dest)
    instructions = dest / "Instructions"
    knowledge = dest / "Knowledge"
    instructions.mkdir(parents=True)
    knowledge.mkdir(parents=True)

    make_instructions(instructions / "INSTRUCTIONS.md")
    (instructions / "GPT_BUILDER.md").write_text(builder_guide(), encoding="utf-8")
    (instructions / "CONVERSATION_STARTERS.md").write_text(
        conversation_starters(), encoding="utf-8"
    )
    shutil.copy2(ROOT / "gpt" / "TESTS.md", instructions / "TESTS.md")

    refs = reference_files()
    assigned: set[Path] = set()
    source_map: dict[str, list[str]] = {}

    def bundle(filename: str, title: str, purpose: str, sources: Iterable[Path]) -> None:
        src = [p for p in sources if p.is_file()]
        for p in src:
            if p.parent == ROOT / "references":
                assigned.add(p)
        source_map[filename] = write_bundle(knowledge / filename, title, purpose, src)

    bundle(
        "01_RUSSIAN_LANGUAGE.md",
        "Норма русского языка и механические правила",
        "Норма, пунктуационные и грамматические поверхности, проверки из РКИ и метаданные канонической русской библиотеки.",
        select_refs(refs, "russian-language")
        + all_files("libraries/russian")
        + existing(["docs/anti-calque.md"]),
    )
    bundle(
        "02_NATIVE_RUSSIAN.md",
        "Живое русское употребление",
        "Естественная информационная структура, контекстная экономия, противопоставление, частицы, эллипсис и рекомендации против кальки.",
        select_refs(refs, "native-russian")
        + all_files("libraries/native")
        + existing(["docs/context-economy.md", "docs/contrast.md"]),
    )
    bundle(
        "03_NORA_GAL.md",
        "Редакторский слой Норы Галь",
        "Семантическая и литературная редактура, канонические метаданные правил Галь и карты происхождения.",
        select_refs(refs, "nora-gal") + all_files("libraries/gal"),
    )
    bundle(
        "04_CHUKOVSKY.md",
        "Редакторский слой Корнея Чуковского",
        "Рекомендации по русской прозе и стилю, полученные из библиотеки Чуковского.",
        select_refs(refs, "chukovsky") + all_files("libraries/chukovsky"),
    )
    bundle(
        "05_ILYAKHOV.md",
        "Редакторский слой Максима Ильяхова",
        "Эвристики информационного стиля, где предупреждения отделены от жёстких языковых ошибок.",
        select_refs(refs, "ilyakhov") + all_files("libraries/ilyakhov"),
    )
    bundle(
        "06_VISSON.md",
        "Переводческий слой Линн Виссон",
        "Русско-английская интерференция, информационная структура и проверки, производные от Виссон.",
        select_refs(refs, "visson") + all_files("libraries/visson"),
    )
    bundle(
        "07_ROSENTHAL.md",
        "Нормативный и редакторский слой Розенталя",
        "Проверки нормы русского языка и стилистики, производные от Розенталя.",
        select_refs(refs, "rosenthal") + all_files("libraries/rosenthal"),
    )
    bundle(
        "08_GOLUB.md",
        "Стилистический слой Голуб",
        "Русская стилистика, лексические и синтаксические редакторские проверки из библиотеки Голуб.",
        select_refs(refs, "golub") + all_files("libraries/golub"),
    )
    bundle(
        "09_AUTHOR_PROFILE.md",
        "Авторский профиль и идиолект",
        "Как сохранять подтверждённый авторский голос, не копируя ошибки.",
        select_refs(refs, "author-profile")
        + all_files("profiles")
        + existing(["docs/author-layer.md"]),
    )
    bundle(
        "10_AUDITS_AND_CORRECTIONS.md",
        "Аудит правил, доказательств и исправлений",
        "Регрессионные знания, работа со спорными правилами, границы доказательств и накопленные исправления.",
        select_refs(refs, "rule-audit", "evidence-audit")
        + existing(["knowledge/corrections.md"]),
    )
    bundle(
        "11_EDITORIAL_BOARD.md",
        "Редакционная коллегия",
        "Роли рецензентов и правила синтеза на уровне редколлегии.",
        existing(["BOARD_SKILL.md"])
        + [p for p in all_files("reviewers") if p.name != "_template.json"],
    )
    bundle(
        "12_STYLES.md",
        "Редакционные стили",
        "Доступные профили стиля и их ограничения.",
        all_files("styles"),
    )
    bundle(
        "13_CAPABILITIES_AND_STATUS.md",
        "Возможности и статус проекта",
        "Что действительно работает, что является диагностикой, а что остаётся только PROJECT; не даёт GPT заявлять о недоступных интеграциях.",
        existing(["docs/capabilities.md", "PROJECT_STATUS.md"]),
    )

    leftovers = [p for p in refs if p not in assigned]
    if leftovers:
        bundle(
            "14_ADDITIONAL_REFERENCE.md",
            "Дополнительные справочные материалы рабочего контура",
            "Справочные материалы, не вошедшие в отдельный пакет редакторской библиотеки.",
            leftovers,
        )

    knowledge_files = sorted(knowledge.glob("*.md"))
    index_lines = [
        "# Индекс Knowledge humanizer_russian\n\n",
        "Загрузите каждый `.md` из этого каталога в раздел GPT Knowledge.\n\n",
        "Эти файлы служат справочными материалами. Инструкции и правила рабочего процесса находятся в `Instructions/INSTRUCTIONS.md`.\n\n",
    ]
    for p in knowledge_files:
        index_lines.append(f"- `{p.name}`\n")
    (knowledge / "00_INDEX.md").write_text("".join(index_lines), encoding="utf-8")

    knowledge_files = sorted(knowledge.glob("*.md"))
    if len(knowledge_files) > MAX_KNOWLEDGE_FILES:
        raise RuntimeError(
            f"Превышен лимит файлов Knowledge: {len(knowledge_files)} > {MAX_KNOWLEDGE_FILES}"
        )

    if any(
        "native-russian-user-context" in p.read_text(encoding="utf-8")
        for p in knowledge_files
    ):
        raise RuntimeError(
            "материал разработки native-russian-user-context попал в GPT Knowledge"
        )

    root_readme = f"""# humanizer_russian — пакет Custom GPT\n\nВерсия: `{skill_version()}`\n\nЭтот архив предназначен для настройки **Custom GPT (GPTs)**, а не для установки рабочего контура Agent Skill.\n\n- Вставьте `Instructions/INSTRUCTIONS.md` в поле GPT Instructions.\n- Загрузите все {len(knowledge_files)} файлов Markdown из `Knowledge/` в GPT Knowledge.\n- Остальные настройки Builder описаны в `Instructions/GPT_BUILDER.md`.\n- Перед публикацией проверьте сборку в Preview по `Instructions/TESTS.md`.\n\nПакет намеренно исключает исполняемые скрипты, CI, наборы проверок, корпуса исследования источников и код провайдеров доказательств со статусом PROJECT. Канонические данные правил, нужные для модельного ревью, встроены в пакеты Knowledge.\n"""
    (dest / "README.md").write_text(root_readme, encoding="utf-8")
    shutil.copy2(ROOT / "LICENSE", dest / "LICENSE")
    if (ROOT / "THIRD_PARTY_NOTICES.md").exists():
        shutil.copy2(ROOT / "THIRD_PARTY_NOTICES.md", dest / "THIRD_PARTY_NOTICES.md")

    inventory = []
    for p in sorted(
        x for x in dest.rglob("*") if x.is_file() and x.name != "_manifest.json"
    ):
        data = p.read_bytes()
        inventory.append(
            {
                "path": p.relative_to(dest).as_posix(),
                "sha256": sha256_bytes(data),
                "size": len(data),
            }
        )

    manifest = {
        "schema_version": 1,
        "package": "humanizer-russian-gpts",
        "skill_version": skill_version(),
        "knowledge_file_count": len(knowledge_files),
        "knowledge_file_limit": MAX_KNOWLEDGE_FILES,
        "source_map": source_map,
        "files": inventory,
    }
    (dest / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def zip_directory(source: Path, output: Path) -> str:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as zf:
        for path in sorted(p for p in source.rglob("*") if p.is_file()):
            rel = Path(PACKAGE_ROOT) / path.relative_to(source)
            info = zipfile.ZipInfo(rel.as_posix(), FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(
                info,
                path.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )
    return sha256_bytes(output.read_bytes())


def inspect_zip(path: Path) -> dict:
    with zipfile.ZipFile(path, "r") as zf:
        names = zf.namelist()
        if not names:
            raise RuntimeError("архив пуст")
        prefix = PACKAGE_ROOT + "/"
        if any(not name.startswith(prefix) for name in names):
            raise RuntimeError("архив содержит файлы за пределами корня пакета")
        required = {
            f"{PACKAGE_ROOT}/Instructions/INSTRUCTIONS.md",
            f"{PACKAGE_ROOT}/Instructions/GPT_BUILDER.md",
            f"{PACKAGE_ROOT}/Knowledge/00_INDEX.md",
            f"{PACKAGE_ROOT}/README.md",
            f"{PACKAGE_ROOT}/_manifest.json",
        }
        missing = sorted(required - set(names))
        if missing:
            raise RuntimeError(f"в архиве нет обязательных файлов: {missing}")
        knowledge = [
            n
            for n in names
            if n.startswith(f"{PACKAGE_ROOT}/Knowledge/") and n.endswith(".md")
        ]
        if len(knowledge) > MAX_KNOWLEDGE_FILES:
            raise RuntimeError("архив превышает лимит файлов Custom GPT Knowledge")
        manifest = json.loads(zf.read(f"{PACKAGE_ROOT}/_manifest.json"))
        if manifest["knowledge_file_count"] != len(knowledge):
            raise RuntimeError("число файлов Knowledge в манифесте не совпадает с архивом")
    return {
        "archive": str(path),
        "sha256": sha256_bytes(path.read_bytes()),
        "bytes": path.stat().st_size,
        "knowledge_files": len(knowledge),
        "skill_version": manifest["skill_version"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "dist" / "humanizer-russian-gpts.zip",
        help="путь к выходному ZIP-архиву",
    )
    parser.add_argument(
        "--directory",
        type=Path,
        help="необязательный каталог, в котором оставить распакованный пакет",
    )
    parser.add_argument(
        "--inspect",
        type=Path,
        help="проверить существующий пакет GPT и завершить работу",
    )
    args = parser.parse_args()

    if args.inspect:
        print(
            json.dumps(
                inspect_zip(args.inspect), ensure_ascii=False, indent=2, sort_keys=True
            )
        )
        return 0

    with tempfile.TemporaryDirectory(prefix="humanizer-russian-gpts-") as td:
        build = Path(td) / PACKAGE_ROOT
        manifest = build_directory(build)
        digest = zip_directory(build, args.output)
        if args.directory:
            if args.directory.exists():
                shutil.rmtree(args.directory)
            shutil.copytree(build, args.directory)

    result = inspect_zip(args.output)
    result["sha256"] = digest
    result["manifest_files"] = len(manifest["files"])
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
