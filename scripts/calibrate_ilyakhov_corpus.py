#!/usr/bin/env python3
"""Calibrate the Ilyakhov mechanical layer on edited natural Russian prose.

This is a development/calibration tool, not a runtime dependency and not a CI
quality gate. It downloads a fixed snapshot-shaped sample from Russian
Wikipedia through the MediaWiki API, runs scripts/lint_ilyakhov.py, and reports
aggregate finding rates plus compact excerpts for manual false-positive review.

The downloaded article text is never written to the repository by this script.
Only metadata, counts and short excerpts are emitted.
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
from typing import Iterable

from lint_ilyakhov import lint, word_count

API = "https://ru.wikipedia.org/w/api.php"
USER_AGENT = "humanizer_russian/ilyakhov-corpus-calibration (+https://github.com/Antiokh/humanizer_russian)"

# Fixed and deliberately mixed expository corpus. These are page titles, not
# frozen article bytes: every report records revision IDs/timestamps so a later
# calibration can be compared honestly instead of pretending the web is static.
DEFAULT_TITLES = [
    "Математика",
    "Физика",
    "Биология",
    "Медицина",
    "Психология",
    "Лингвистика",
    "Русский язык",
    "Философия",
    "Право",
    "Экономика",
    "Москва",
    "Санкт-Петербург",
    "Сербия",
    "История России",
    "Вторая мировая война",
    "Интернет",
    "Программирование",
    "Машинное обучение",
    "Искусственный интеллект",
    "Космос",
    "Солнечная система",
    "Железнодорожный транспорт",
    "Электроэнергетика",
    "Вода",
    "Архитектура",
    "Театр",
    "Музыка",
    "Александр Сергеевич Пушкин",
    "Лев Николаевич Толстой",
    "Фёдор Михайлович Достоевский",
]


@dataclass(frozen=True)
class Page:
    requested_title: str
    title: str
    pageid: int
    revid: int
    revision_timestamp: str
    text: str


def _request(params: dict[str, str], *, timeout: float, retries: int) -> dict:
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{API}?{query}", headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt >= retries:
                break
            time.sleep(0.8 * (attempt + 1))
    raise RuntimeError(f"MediaWiki request failed after {retries + 1} attempts: {last_error}")


def fetch_page(title: str, *, timeout: float = 20.0, retries: int = 2) -> Page:
    payload = _request(
        {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "redirects": "1",
            "prop": "extracts|revisions",
            "explaintext": "1",
            "exsectionformat": "plain",
            "rvprop": "ids|timestamp",
            "titles": title,
        },
        timeout=timeout,
        retries=retries,
    )
    pages = payload.get("query", {}).get("pages", [])
    if len(pages) != 1 or pages[0].get("missing") is True:
        raise RuntimeError(f"Wikipedia page not found or ambiguous: {title!r}")
    raw = pages[0]
    revisions = raw.get("revisions") or []
    if not revisions:
        raise RuntimeError(f"Wikipedia page has no revision metadata: {title!r}")
    rev = revisions[0]
    text = raw.get("extract", "")
    if not text.strip():
        raise RuntimeError(f"Wikipedia page has empty extract: {title!r}")
    return Page(
        requested_title=title,
        title=raw["title"],
        pageid=int(raw["pageid"]),
        revid=int(rev["revid"]),
        revision_timestamp=rev["timestamp"],
        text=text,
    )


def excerpt(item: dict, limit: int = 180) -> str:
    value = " ".join(item.get("excerpt", "").split())
    return value[:limit]


def calibrate(pages: Iterable[Page], *, samples_per_rule: int = 8) -> dict:
    rule_counts: Counter[str] = Counter()
    samples: dict[str, list[dict]] = defaultdict(list)
    docs: list[dict] = []
    total_words = 0
    total_findings = 0
    default_rule = "ilyakhov: bureaucratic tautology"

    for page in pages:
        findings, metrics = lint(page.text)
        wc = word_count(page.text)
        total_words += wc
        total_findings += len(findings)
        local_counts = Counter(item["rule"] for item in findings)
        rule_counts.update(local_counts)

        for item in findings:
            bucket = samples[item["rule"]]
            if len(bucket) < samples_per_rule:
                bucket.append(
                    {
                        "title": page.title,
                        "line": item.get("line", 0),
                        "excerpt": excerpt(item),
                    }
                )

        docs.append(
            {
                "requested_title": page.requested_title,
                "title": page.title,
                "pageid": page.pageid,
                "revid": page.revid,
                "revision_timestamp": page.revision_timestamp,
                "words": wc,
                "findings": dict(sorted(local_counts.items())),
                "metrics": {
                    key: value
                    for key, value in metrics.items()
                    if key.startswith("ilyakhov_")
                },
            }
        )

    per_100k = {
        rule: (count * 100_000 / total_words if total_words else 0.0)
        for rule, count in sorted(rule_counts.items())
    }
    return {
        "schema": 1,
        "source": "Russian Wikipedia / MediaWiki API / plaintext extracts",
        "documents": len(docs),
        "words": total_words,
        "findings_total": total_findings,
        "default_rule": default_rule,
        "default_rule_hits": rule_counts.get(default_rule, 0),
        "rule_counts": dict(sorted(rule_counts.items())),
        "rule_hits_per_100k_words": {
            rule: round(rate, 3) for rule, rate in per_100k.items()
        },
        "samples": dict(sorted(samples.items())),
        "pages": docs,
    }


def render_text(report: dict) -> str:
    lines = [
        "Ilyakhov natural-Russian corpus calibration",
        f"documents: {report['documents']}",
        f"words: {report['words']}",
        f"findings: {report['findings_total']}",
        f"default ILY-M01 hits: {report['default_rule_hits']}",
        "rule counts:",
    ]
    if not report["rule_counts"]:
        lines.append("  (none)")
    for rule, count in report["rule_counts"].items():
        rate = report["rule_hits_per_100k_words"][rule]
        lines.append(f"  {rule}: {count} ({rate}/100k words)")
    lines.append("samples:")
    for rule, examples in report["samples"].items():
        lines.append(f"  [{rule}]")
        for item in examples:
            lines.append(f"    - {item['title']}: {item['excerpt']}")
    lines.append("revision snapshot:")
    for page in report["pages"]:
        lines.append(
            f"  - {page['title']}: pageid={page['pageid']} revid={page['revid']} "
            f"timestamp={page['revision_timestamp']} words={page['words']}"
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calibrate Ilyakhov surface checks on a fixed natural-Russian Wikipedia sample"
    )
    parser.add_argument(
        "--network",
        action="store_true",
        help="explicitly allow network access; required to download the calibration corpus",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--samples-per-rule", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument(
        "--titles",
        nargs="*",
        help="optional page-title override; default is the fixed 30-page corpus",
    )
    args = parser.parse_args()

    if not args.network:
        parser.error("network calibration is opt-in; pass --network")
    if args.samples_per_rule < 0:
        parser.error("--samples-per-rule must be >= 0")

    titles = args.titles or DEFAULT_TITLES
    pages: list[Page] = []
    for title in titles:
        print(f"fetch: {title}", file=sys.stderr)
        pages.append(fetch_page(title, timeout=args.timeout, retries=args.retries))

    report = calibrate(pages, samples_per_rule=args.samples_per_rule)
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))


if __name__ == "__main__":
    main()
