#!/usr/bin/env python3
"""Temporary audit of the published Russian Patriarchy corpus.

This file exists only on the audit branch and is not intended for merge.
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://patriarchy.pages.dev"
ROOT = Path(__file__).resolve().parents[1]
UA = "humanizer_russian patriarchy audit/1.0"


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def sitemap_urls() -> list[str]:
    starts = [
        f"{BASE}/sitemap-index.xml",
        f"{BASE}/sitemap.xml",
        f"{BASE}/sitemap-0.xml",
    ]
    queue: list[str] = []
    for url in starts:
        try:
            fetch_text(url)
        except Exception:
            continue
        queue.append(url)
        break
    if not queue:
        raise RuntimeError("Не найден sitemap patriarchy.pages.dev")

    pages: set[str] = set()
    seen: set[str] = set()
    while queue:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        root = ET.fromstring(fetch_text(url))
        locs = [node.text.strip() for node in root.iter() if node.tag.endswith("loc") and node.text]
        for loc in locs:
            if loc.endswith(".xml"):
                queue.append(loc)
            else:
                pages.add(loc)
    return sorted(url for url in pages if "/ru/" in url)


class MainTextParser(HTMLParser):
    BLOCKS = {"p", "li", "h1", "h2", "h3", "h4", "blockquote", "dd", "dt", "tr"}
    IGNORE = {"script", "style", "svg", "code", "pre", "nav", "button"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.main_depth = 0
        self.ignore_depth = 0
        self.parts: list[str] = []
        self.saw_main = False

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "main":
            self.main_depth += 1
            self.saw_main = True
            self.parts.append("\n")
            return
        if self.main_depth and tag in self.IGNORE:
            self.ignore_depth += 1
            return
        if self.main_depth and not self.ignore_depth and tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag == "main" and self.main_depth:
            self.main_depth -= 1
            self.parts.append("\n")
            return
        if self.main_depth and tag in self.IGNORE and self.ignore_depth:
            self.ignore_depth -= 1
            return
        if self.main_depth and not self.ignore_depth and tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.main_depth and not self.ignore_depth:
            self.parts.append(data)

    def text(self) -> str:
        value = html.unescape("".join(self.parts))
        value = re.sub(r"[ \t\r\f\v]+", " ", value)
        value = re.sub(r" *\n *", "\n", value)
        value = re.sub(r"\n{3,}", "\n\n", value)
        return value.strip()


def page_text(url: str) -> str:
    parser = MainTextParser()
    parser.feed(fetch_text(url))
    if not parser.saw_main:
        raise RuntimeError(f"На странице нет <main>: {url}")
    return parser.text()


def run_json(args: list[str], text: str) -> dict:
    proc = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        input=text,
        text=True,
        capture_output=True,
        timeout=120,
    )
    try:
        payload = json.loads(proc.stdout)
    except Exception as exc:
        return {
            "returncode": proc.returncode,
            "parse_error": str(exc),
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    return {"returncode": proc.returncode, "payload": payload, "stderr": proc.stderr}


def main() -> None:
    urls = sitemap_urls()
    report: dict = {
        "source": BASE,
        "humanizer_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "pages_total": len(urls),
        "pages": [],
    }

    for index, url in enumerate(urls, 1):
        print(f"[{index}/{len(urls)}] {url}", file=sys.stderr, flush=True)
        try:
            text = page_text(url)
            compact = run_json(["scripts/check.py", "--extended", "--json"], text)
            board = run_json(["scripts/review.py", "--format", "json"], text)
            report["pages"].append({
                "url": url,
                "text_chars": len(text),
                "compact": compact,
                "board": board,
            })
        except Exception as exc:
            report["pages"].append({"url": url, "error": repr(exc)})

    out = ROOT / "patriarchy-humanizer-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = []
    total_compact = 0
    total_board = 0
    errors = 0
    for page in report["pages"]:
        if "error" in page:
            errors += 1
            summary.append({"url": page["url"], "error": page["error"]})
            continue
        compact_payload = page["compact"].get("payload") or {}
        board_payload = page["board"].get("payload") or {}
        compact_findings = compact_payload.get("findings", []) if isinstance(compact_payload, dict) else []
        board_findings = board_payload.get("findings", []) if isinstance(board_payload, dict) else []
        total_compact += len(compact_findings)
        total_board += len(board_findings)
        if compact_findings or board_findings:
            summary.append({
                "url": page["url"],
                "compact_findings": len(compact_findings),
                "board_findings": len(board_findings),
            })

    summary_payload = {
        "pages_total": len(urls),
        "pages_with_findings_or_errors": len(summary),
        "compact_findings": total_compact,
        "board_findings": total_board,
        "page_errors": errors,
        "pages": summary,
    }
    (ROOT / "patriarchy-humanizer-summary.json").write_text(
        json.dumps(summary_payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary_payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
