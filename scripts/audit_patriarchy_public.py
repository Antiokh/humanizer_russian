#!/usr/bin/env python3
"""Temporary audit of the current Patriarchy editing branch."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path('/tmp/patriarchy-audit')
REPO = 'https://github.com/Antiokh/patriarchy.git'
BRANCH = 'edit/humanizer-russian-full-pass'


def run_json(args: list[str], path: Path) -> dict:
    proc = subprocess.run(
        [sys.executable, *args, str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=180,
    )
    try:
        payload = json.loads(proc.stdout)
    except Exception as exc:
        return {
            'returncode': proc.returncode,
            'parse_error': str(exc),
            'stdout': proc.stdout,
            'stderr': proc.stderr,
        }
    return {'returncode': proc.returncode, 'payload': payload, 'stderr': proc.stderr}


def main() -> None:
    if TARGET.exists():
        shutil.rmtree(TARGET)
    subprocess.run(
        ['git', 'clone', '--depth', '1', '--branch', BRANCH, REPO, str(TARGET)],
        check=True,
        text=True,
    )

    files = sorted((TARGET / 'src/content/docs/ru').rglob('*.mdx'))
    target_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=TARGET, text=True).strip()
    humanizer_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    report = {
        'source_repository': 'Antiokh/patriarchy',
        'source_branch': BRANCH,
        'source_commit': target_sha,
        'humanizer_commit': humanizer_sha,
        'files_total': len(files),
        'files': [],
    }

    for index, path in enumerate(files, 1):
        rel = path.relative_to(TARGET).as_posix()
        print(f'[{index}/{len(files)}] {rel}', file=sys.stderr, flush=True)
        compact = run_json(['scripts/check.py', '--extended', '--json'], path)
        board = run_json(['scripts/review.py', '--format', 'json'], path)
        report['files'].append({
            'path': rel,
            'compact': compact,
            'board': board,
        })

    (ROOT / 'patriarchy-humanizer-report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8'
    )

    summary = []
    total_compact = 0
    total_board = 0
    errors = 0
    for item in report['files']:
        compact_payload = item['compact'].get('payload') or {}
        board_payload = item['board'].get('payload') or {}
        compact_findings = compact_payload.get('findings', []) if isinstance(compact_payload, dict) else []
        board_findings = board_payload.get('findings', []) if isinstance(board_payload, dict) else []
        total_compact += len(compact_findings)
        total_board += len(board_findings)
        if item['compact'].get('parse_error') or item['board'].get('parse_error'):
            errors += 1
        if compact_findings or board_findings or item['compact'].get('parse_error') or item['board'].get('parse_error'):
            summary.append({
                'path': item['path'],
                'compact_findings': len(compact_findings),
                'board_findings': len(board_findings),
                'compact_parse_error': item['compact'].get('parse_error'),
                'board_parse_error': item['board'].get('parse_error'),
            })

    summary_payload = {
        'source_commit': target_sha,
        'files_total': len(files),
        'files_with_findings_or_errors': len(summary),
        'compact_findings': total_compact,
        'board_findings': total_board,
        'file_errors': errors,
        'files': summary,
    }
    (ROOT / 'patriarchy-humanizer-summary.json').write_text(
        json.dumps(summary_payload, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    print(json.dumps(summary_payload, ensure_ascii=False))


if __name__ == '__main__':
    main()
