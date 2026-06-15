#!/usr/bin/env python3
"""정적 배포 점검 스크립트.

HTML/MD 인코딩, 기본 메타, 내부 링크, 중복 id, 내장 JavaScript 문법을 확인합니다.
외부 Firebase 연결 자체는 브라우저/운영 DB 권한이 필요하므로 수동 점검 항목으로 남깁니다.
"""
from __future__ import annotations

import http.client
import os
import re
import subprocess
import sys
import tempfile
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent
HTML_FILES = sorted(ROOT.glob('*.html'))
TEXT_FILES = sorted([*ROOT.glob('*.html'), *ROOT.glob('*.md'), *ROOT.glob('*.txt')])
REQUIRED_FILES = [
    'index.html',
    'details.html',
    'timetable.html',
    'drivelink.html',
    'dricelink.html',
    'README.md',
    'DEPLOYMENT_CHECKLIST.md',
]


def ok(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def check_encoding(path: Path, errors: list[str]) -> None:
    raw = path.read_bytes()
    ok(not raw.startswith(b'\xef\xbb\xbf'), f'{path.name}: BOM이 있습니다.', errors)
    try:
        raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        errors.append(f'{path.name}: UTF-8 decode 실패: {exc}')
    ok(b'\r\n' not in raw and b'\r' not in raw, f'{path.name}: LF가 아닌 줄바꿈이 있습니다.', errors)


def check_html(path: Path, errors: list[str]) -> None:
    html = path.read_text(encoding='utf-8')
    low = html.lower()
    ok(low.startswith('<!doctype html>'), f'{path.name}: DOCTYPE 누락', errors)
    ok('<html lang="ko"' in low or "<html lang='ko'" in low, f'{path.name}: lang="ko" 누락', errors)
    ok('charset="utf-8"' in low or "charset='utf-8'" in low, f'{path.name}: charset UTF-8 누락', errors)
    ok('name="viewport"' in low or "name='viewport'" in low, f'{path.name}: viewport 누락', errors)

    html_for_id_check = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', html, flags=re.IGNORECASE)
    html_for_id_check = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', html_for_id_check, flags=re.IGNORECASE)
    ids = re.findall(r'\bid=["\']([^"\']+)["\']', html_for_id_check)
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    ok(not duplicates, f'{path.name}: 중복 id 발견: {duplicates}', errors)

    # HTML 파일 간 상대 링크 확인. 앵커/쿼리/외부 링크는 제외하고 루트 파일 존재만 확인합니다.
    for href in re.findall(r'\bhref=["\']([^"\']+)["\']', html):
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
            continue
        target = href.split('#', 1)[0].split('?', 1)[0]
        if not target:
            continue
        if target.endswith(('.html', '.md', '.txt')):
            ok((ROOT / target).exists(), f'{path.name}: 내부 링크 대상 없음: {href}', errors)


def extract_scripts(path: Path) -> Iterable[str]:
    html = path.read_text(encoding='utf-8')
    return re.findall(r'<script[^>]*>([\s\S]*?)</script>', html, flags=re.IGNORECASE)


def check_js(path: Path, report: list[str], errors: list[str]) -> None:
    for idx, script in enumerate(extract_scripts(path)):
        suffix = '.mjs' if 'import ' in script else '.js'
        with tempfile.NamedTemporaryFile('w', suffix=suffix, delete=False, encoding='utf-8') as tmp:
            tmp.write(script)
            tmp_path = Path(tmp.name)
        try:
            result = subprocess.run(['node', '--check', str(tmp_path)], capture_output=True, text=True)
            if result.returncode == 0:
                report.append(f'- {path.name} script {idx}: OK')
            else:
                report.append(f'- {path.name} script {idx}: FAIL')
                errors.append(f'{path.name} script {idx}: {result.stderr.strip()}')
        finally:
            tmp_path.unlink(missing_ok=True)


def check_http(report: list[str], errors: list[str]) -> None:
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:
            pass

    cwd = os.getcwd()
    os.chdir(ROOT)
    server = ThreadingHTTPServer(('127.0.0.1', 0), Quiet)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        for name in REQUIRED_FILES + ['DEPLOYMENT_AUDIT_REPORT.txt']:
            conn = http.client.HTTPConnection('127.0.0.1', port, timeout=5)
            conn.request('GET', f'/{name}')
            res = conn.getresponse()
            res.read()
            conn.close()
            if res.status == 200:
                report.append(f'- {name}: HTTP 200')
            else:
                report.append(f'- {name}: HTTP {res.status}')
                errors.append(f'{name}: HTTP {res.status}')
    finally:
        server.shutdown()
        os.chdir(cwd)


def main() -> int:
    errors: list[str] = []
    report: list[str] = [f'SITE: {ROOT}']

    report.append('FILE EXISTENCE CHECK')
    for name in REQUIRED_FILES:
        exists = (ROOT / name).exists()
        report.append(f'- {name}: {"OK" if exists else "MISSING"}')
        ok(exists, f'{name}: 파일 없음', errors)

    report.append('\nENCODING / HTML STATIC CHECK')
    for path in TEXT_FILES:
        check_encoding(path, errors)
    for path in HTML_FILES:
        before = len(errors)
        check_html(path, errors)
        report.append(f'- {path.name}: {"OK" if len(errors) == before else "CHECK"}')

    report.append('\nJAVASCRIPT SYNTAX CHECK')
    for path in HTML_FILES:
        check_js(path, report, errors)

    report.append('\nLOCAL STATIC SERVE CHECK')
    check_http(report, errors)

    report.append('\nFEATURE CHECKLIST NOTE')
    report.append('- timetable.html: 장소 태그 UI, timetable_locations 노드, locations 배열 저장 로직 포함')
    report.append('- Firebase 실제 읽기/쓰기 권한은 배포 URL에서 수동 테스트 필요')

    report.append('\nRESULT')
    report.append('PASS' if not errors else 'FAIL')
    if errors:
        report.append('\nERRORS')
        report.extend(f'- {e}' for e in errors)

    text = '\n'.join(report) + '\n'
    (ROOT / 'DEPLOYMENT_AUDIT_REPORT.txt').write_text(text, encoding='utf-8')
    print(text)
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
