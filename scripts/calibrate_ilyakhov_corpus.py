#!/usr/bin/env python3
"""Manual natural-Russian calibration for the Ilyakhov mechanical library.

This development tool is network opt-in and is never a runtime or CI dependency.
It fetches plaintext snapshots from Russian Wikipedia, runs the same normalized
``review_v1`` detector used by compact/board, and reports aggregate rates plus
revision metadata. Fetched article text is not committed.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass

from lint_ilyakhov import review, word_count

API = "https://ru.wikipedia.org/w/api.php"
USER_AGENT = "humanizer_russian/ilyakhov-corpus-calibration (+https://github.com/Antiokh/humanizer_russian)"
DEFAULT_TITLES = [
    "Математика", "Физика", "Биология", "Медицина", "Психология",
    "Лингвистика", "Русский язык", "Философия", "Право", "Экономика",
    "Москва", "Санкт-Петербург", "Сербия", "История России", "Вторая мировая война",
    "Интернет", "Программирование", "Машинное обучение", "Искусственный интеллект", "Космос",
    "Солнечная система", "Железнодорожный транспорт", "Электроэнергетика", "Вода", "Архитектура",
    "Театр", "Музыка", "Александр Сергеевич Пушкин", "Лев Николаевич Толстой", "Фёдор Михайлович Достоевский",
]


@dataclass(frozen=True)
class Page:
    requested_title: str
    title: str
    pageid: int
    revid: int
    revision_timestamp: str
    text: str


def request(params: dict[str, str], timeout: float, retries: int) -> dict:
    req = urllib.request.Request(
        f"{API}?{urllib.parse.urlencode(params)}",
        headers={"User-Agent": USER_AGENT},
    )
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(0.8 * (attempt + 1))
    raise RuntimeError(f"MediaWiki request failed after {retries + 1} attempts: {last_error}")


def fetch_page(title: str, timeout: float, retries: int) -> Page:
    payload = request({
        "action": "query", "format": "json", "formatversion": "2", "redirects": "1",
        "prop": "extracts|revisions", "explaintext": "1", "exsectionformat": "plain",
        "rvprop": "ids|timestamp", "titles": title,
    }, timeout, retries)
    pages = payload.get("query", {}).get("pages", [])
    if len(pages) != 1 or pages[0].get("missing") is True:
        raise RuntimeError(f"Wikipedia page not found or ambiguous: {title!r}")
    raw = pages[0]
    revisions = raw.get("revisions") or []
    text = raw.get("extract", "")
    if not revisions or not text.strip():
        raise RuntimeError(f"Wikipedia page lacks revision/text: {title!r}")
    rev = revisions[0]
    return Page(title, raw["title"], int(raw["pageid"]), int(rev["revid"]), rev["timestamp"], text)


def calibrate(pages: list[Page], samples_per_rule: int) -> dict:
    counts: Counter[str] = Counter()
    samples: dict[str, list[dict]] = defaultdict(list)
    metrics_totals: Counter[str] = Counter()
    docs = []
    words_total = 0

    for page in pages:
        result = review(page.text)
        findings = result["findings"]
        wc = word_count(page.text)
        words_total += wc
        local = Counter(item["rule_id"] for item in findings)
        counts.update(local)
        for key, value in result["metrics"].items():
            if isinstance(value, (int, float)):
                metrics_totals[key] += value
        for item in findings:
            bucket = samples[item["rule_id"]]
            if len(bucket) < samples_per_rule:
                bucket.append({
                    "title": page.title,
                    "line": item.get("line", 0),
                    "excerpt": " ".join(item.get("excerpt", "").split())[:180],
                })
        docs.append({
            "requested_title": page.requested_title,
            "title": page.title,
            "pageid": page.pageid,
            "revid": page.revid,
            "revision_timestamp": page.revision_timestamp,
            "words": wc,
            "findings": dict(sorted(local.items())),
        })

    return {
        "schema": 2,
        "source": "Russian Wikipedia / MediaWiki API / plaintext extracts",
        "documents": len(docs),
        "words": words_total,
        "finding_counts": dict(sorted(counts.items())),
        "finding_hits_per_100k_words": {
            rid: round(count * 100000 / words_total, 3) if words_total else 0.0
            for rid, count in sorted(counts.items())
        },
        "metric_totals": dict(sorted(metrics_totals.items())),
        "samples": dict(sorted(samples.items())),
        "pages": docs,
    }


def render(report: dict) -> str:
    lines = [
        "Ilyakhov natural-Russian corpus calibration",
        f"documents: {report['documents']}",
        f"words: {report['words']}",
        "finding counts:",
    ]
    if not report["finding_counts"]:
        lines.append("  (none)")
    for rid, count in report["finding_counts"].items():
        lines.append(f"  {rid}: {count} ({report['finding_hits_per_100k_words'][rid]}/100k words)")
    lines.append("metric totals:")
    for key, value in report["metric_totals"].items():
        lines.append(f"  {key}: {value}")
    lines.append("revision snapshot:")
    for page in report["pages"]:
        lines.append(f"  - {page['title']}: revid={page['revid']} timestamp={page['revision_timestamp']} words={page['words']}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--network", action="store_true", help="explicitly allow MediaWiki network access")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--samples-per-rule", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--titles", nargs="*")
    args = parser.parse_args()
    if not args.network:
        parser.error("network calibration is opt-in; pass --network")
    if args.samples_per_rule < 0:
        parser.error("--samples-per-rule must be >= 0")

    pages = []
    for title in args.titles or DEFAULT_TITLES:
        print(f"fetch: {title}", file=sys.stderr)
        pages.append(fetch_page(title, args.timeout, args.retries))
    report = calibrate(pages, args.samples_per_rule)
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.as_json else render(report))


if __name__ == "__main__":
    main()
