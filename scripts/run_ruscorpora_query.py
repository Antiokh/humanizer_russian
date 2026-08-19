#!/usr/bin/env python3
"""Replay an exported NKRЯ lexicogrammatical query reproducibly.

The runner deliberately does not invent corpus queries. Build the intended
search and subcorpus in the NKRЯ UI, export its JSON (Ctrl+Shift+E on the
results page), save that fixture locally, then replay it here.

Authentication is read only from RUSCORPORA_API_TOKEN. Raw results are written
only when --output is supplied. The token is never included in reports and is
never sent outside the official ruscorpora.ru HTTPS API host.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_ENDPOINT = "https://ruscorpora.ru/api/v1/lex-gramm/concordance"
ALLOWED_API_HOST = "ruscorpora.ru"
ALLOWED_API_PATH = "/api/v1/lex-gramm/concordance"
RETRYABLE_HTTP = {408, 409, 429, 500, 502, 503, 504}


def load_query(path: Path) -> dict[str, Any]:
    """Load and minimally validate an exported LexGramQuery fixture."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("NKRЯ query fixture must be a JSON object")
    if not isinstance(value.get("corpus"), dict):
        raise ValueError("NKRЯ query fixture must contain object field `corpus`")
    if not isinstance(value.get("lexGramm"), dict):
        raise ValueError("NKRЯ lexicogrammatical fixture must contain object field `lexGramm`")
    return value


def canonical_bytes(value: dict[str, Any]) -> bytes:
    """Serialize query deterministically for hashing without changing API payload semantics."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def query_sha256(value: dict[str, Any]) -> str:
    """Return the SHA-256 fingerprint of canonical query JSON."""
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def validate_endpoint(endpoint: str) -> str:
    """Allow bearer-token requests only to the official HTTPS NKRЯ endpoint."""
    parsed = urllib.parse.urlsplit(endpoint)
    if (
        parsed.scheme != "https"
        or parsed.hostname != ALLOWED_API_HOST
        or parsed.port not in {None, 443}
        or parsed.path != ALLOWED_API_PATH
        or parsed.query
        or parsed.fragment
        or parsed.username is not None
        or parsed.password is not None
    ):
        raise ValueError(
            "--endpoint must be the official NKRЯ HTTPS lex-gramm concordance endpoint "
            f"({DEFAULT_ENDPOINT})"
        )
    return urllib.parse.urlunsplit(("https", ALLOWED_API_HOST, ALLOWED_API_PATH, "", ""))


def request_shape(endpoint: str, token: str, query: dict[str, Any]) -> urllib.request.Request:
    """Build the authenticated POST request after validating the credential destination."""
    safe_endpoint = validate_endpoint(endpoint)
    return urllib.request.Request(
        safe_endpoint,
        data=json.dumps(query, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "humanizer_russian-ruscorpora-calibration/1",
        },
        method="POST",
    )


def post_query(
    endpoint: str,
    token: str,
    query: dict[str, Any],
    *,
    timeout: float,
    retries: int,
) -> dict[str, Any]:
    """POST one NKRЯ query with bounded retries for transient failures."""
    safe_endpoint = validate_endpoint(endpoint)
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        request = request_shape(safe_endpoint, token, query)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read().decode("utf-8")
            value = json.loads(raw)
            if not isinstance(value, dict):
                raise RuntimeError("NKRЯ API returned a non-object JSON value")
            return value
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:1200]
            last_error = RuntimeError(f"NKRЯ API HTTP {exc.code}: {body}")
            if exc.code not in RETRYABLE_HTTP or attempt >= retries:
                raise last_error from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = RuntimeError(f"NKRЯ API transport error: {exc}")
            if attempt >= retries:
                raise last_error from exc
        time.sleep(min(2**attempt, 8))
    raise RuntimeError(f"NKRЯ API request failed: {last_error}")


def concordance_shape(response: dict[str, Any]) -> dict[str, int]:
    """Describe only material actually returned in this response page.

    These counts are deliberately *not* labelled corpus prevalence or total hit
    counts. The concordance API is paginated, and a returned page must not be
    silently promoted to a population estimate.
    """
    data = response.get("concordanceData")
    groups = data.get("groups", []) if isinstance(data, dict) else []
    if not isinstance(groups, list):
        groups = []
    documents = 0
    snippet_groups = 0
    snippets = 0
    for group in groups:
        docs = group.get("docs", []) if isinstance(group, dict) else []
        if not isinstance(docs, list):
            continue
        documents += len(docs)
        for document in docs:
            items = document.get("snippetGroups", []) if isinstance(document, dict) else []
            if not isinstance(items, list):
                continue
            snippet_groups += len(items)
            for snippet_group in items:
                rows = snippet_group.get("snippets", []) if isinstance(snippet_group, dict) else []
                if isinstance(rows, list):
                    snippets += len(rows)
    return {
        "returned_groups": len(groups),
        "returned_documents": documents,
        "returned_snippet_groups": snippet_groups,
        "returned_snippets": snippets,
    }


def build_report(
    *,
    fixture: Path,
    endpoint: str,
    query: dict[str, Any],
    response: dict[str, Any] | None,
    dry_run: bool,
) -> dict[str, Any]:
    """Build a provenance-first report without authentication material."""
    safe_endpoint = validate_endpoint(endpoint)
    report: dict[str, Any] = {
        "schema_version": 1,
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "dry_run": dry_run,
        "fixture_name": fixture.name,
        "query_sha256": query_sha256(query),
        "endpoint": safe_endpoint,
        "corpus": query.get("corpus"),
        "has_subcorpus": isinstance(query.get("subcorpus"), dict),
        "params": query.get("params", {}),
        "interpretation_boundary": (
            "Returned-page counts are not corpus prevalence. Publish normalized rates only "
            "after validating the relevant total/denominator from NKRЯ documentation/output."
        ),
    }
    if response is not None:
        report["response_sha256"] = hashlib.sha256(
            json.dumps(response, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        report["returned_page"] = concordance_shape(response)
        report["response"] = response
    return report


def self_test() -> None:
    """Validate hashing, endpoint safety, request redaction, and page counting offline."""
    query = {
        "corpus": {"type": "MAIN"},
        "lexGramm": {
            "sectionValues": [
                {
                    "subsectionValues": [
                        {
                            "conditionValues": [
                                {"fieldName": "lex", "text": {"v": "кот"}}
                            ]
                        }
                    ]
                }
            ]
        },
    }
    first = query_sha256(query)
    second = query_sha256(json.loads(json.dumps(query, ensure_ascii=False)))
    if first != second or len(first) != 64:
        raise AssertionError("query hashing is not deterministic")

    request = request_shape(DEFAULT_ENDPOINT, "secret-test-token", query)
    if request.method != "POST":
        raise AssertionError(request.method)
    if request.full_url != DEFAULT_ENDPOINT:
        raise AssertionError(request.full_url)
    if request.headers.get("Authorization") != "Bearer secret-test-token":
        raise AssertionError("Bearer header not constructed")
    body = json.loads((request.data or b"").decode("utf-8"))
    if body != query:
        raise AssertionError("request body changed query fixture")

    for malicious in [
        "http://ruscorpora.ru/api/v1/lex-gramm/concordance",
        "https://evil.example/api/v1/lex-gramm/concordance",
        "https://ruscorpora.ru.evil.example/api/v1/lex-gramm/concordance",
        "https://ruscorpora.ru/api/v1/word-portrait/",
        "https://user:pass@ruscorpora.ru/api/v1/lex-gramm/concordance",
    ]:
        try:
            request_shape(malicious, "secret-test-token", query)
        except ValueError:
            pass
        else:
            raise AssertionError(f"unsafe credential destination accepted: {malicious}")

    fake_response = {
        "concordanceData": {
            "groups": [
                {
                    "docs": [
                        {"snippetGroups": [{"snippets": [{}, {}]}, {"snippets": [{}]}]},
                        {"snippetGroups": []},
                    ]
                },
                {"docs": [{"snippetGroups": [{"snippets": [{}]}]}]},
            ]
        }
    }
    shape = concordance_shape(fake_response)
    if shape != {
        "returned_groups": 2,
        "returned_documents": 3,
        "returned_snippet_groups": 3,
        "returned_snippets": 4,
    }:
        raise AssertionError(shape)

    report = build_report(
        fixture=Path("fixture.json"),
        endpoint=DEFAULT_ENDPOINT,
        query=query,
        response=fake_response,
        dry_run=False,
    )
    serialized = json.dumps(report, ensure_ascii=False)
    if "secret-test-token" in serialized or "Authorization" in serialized:
        raise AssertionError("report leaked authentication material")
    if "prevalence" not in report["interpretation_boundary"].lower():
        raise AssertionError("report lost prevalence boundary")

    print("NKRЯ query replay self-test: OK")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments; no token is required for dry-run/self-test."""
    parser = argparse.ArgumentParser(description="Replay an exported NKRЯ lexicogrammatical query")
    parser.add_argument("fixture", nargs="?", type=Path, help="JSON exported from the NKRЯ results UI")
    parser.add_argument("--output", type=Path, help="write provenance + raw response JSON here")
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help="official NKRЯ endpoint; alternate hosts/paths are rejected before bearer auth",
    )
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> None:
    """Run an offline check/dry run or replay a supplied query fixture live."""
    args = parse_args()
    if args.self_test:
        self_test()
        return
    if args.fixture is None:
        raise SystemExit("fixture path is required unless --self-test is used")
    if args.retries < 0:
        raise SystemExit("--retries must be >= 0")

    safe_endpoint = validate_endpoint(args.endpoint)
    query = load_query(args.fixture)
    if args.dry_run:
        report = build_report(
            fixture=args.fixture,
            endpoint=safe_endpoint,
            query=query,
            response=None,
            dry_run=True,
        )
    else:
        token = os.environ.get("RUSCORPORA_API_TOKEN")
        if not token:
            raise SystemExit("RUSCORPORA_API_TOKEN is required for a live NKRЯ request")
        response = post_query(
            safe_endpoint,
            token,
            query,
            timeout=args.timeout,
            retries=args.retries,
        )
        report = build_report(
            fixture=args.fixture,
            endpoint=safe_endpoint,
            query=query,
            response=response,
            dry_run=False,
        )

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
