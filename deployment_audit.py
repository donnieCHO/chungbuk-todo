#!/usr/bin/env python3
"""
정적 배포 점검 스크립트
- UTF-8/BOM/LF
- HTML 기본 메타
- 중복 id
- 내부 링크 존재 여부
- onclick 함수 정의 여부
- <script> JavaScript 문법(node --check)
"""
from pathlib import Path
from bs4 import BeautifulSoup
import os, re, subprocess, tempfile

SITE = Path(__file__).resolve().parent
HTML_FILES = sorted(SITE.glob('*.html'))
FUNC_RE = re.compile(r"(?:window\.)?([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>|function\s+([A-Za-z_$][\w$]*)\s*\(")
ONCLICK_RE = re.compile(r"\b([A-Za-z_$][\w$]*)\s*\(")

def inspect_html(path: Path):
    issues = []
    raw = path.read_bytes()
    if raw.startswith(b'\xef\xbb\xbf'):
        issues.append('BOM present')
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        issues.append(f'UTF-8 decode error: {exc}')
        text = raw.decode('utf-8', 'replace')
    if '\r' in text:
        issues.append('line ending is not LF-only')

    soup = BeautifulSoup(text, 'html.parser')
    if not text.lstrip().lower().startswith('<!doctype html>'):
        issues.append('missing or misplaced DOCTYPE')
    if soup.find('html', attrs={'lang':'ko'}) is None:
        issues.append('missing html lang="ko"')
    if not soup.find('meta', attrs={'charset': re.compile('utf-8', re.I)}):
        issues.append('missing meta charset UTF-8')
    if not soup.find('meta', attrs={'name':'viewport'}):
        issues.append('missing viewport meta')

    ids = {}
    for tag in soup.find_all(attrs={'id': True}):
        ids.setdefault(tag['id'], 0)
        ids[tag['id']] += 1
    duplicated = sorted(k for k, count in ids.items() if count > 1)
    if duplicated:
        issues.append('duplicated id: ' + ', '.join(duplicated))

    for tag in soup.find_all(['a', 'script', 'link']):
        attr = 'href' if tag.name in ['a', 'link'] else 'src'
        value = tag.get(attr)
        if not value or value.startswith('#') or value.startswith('mailto:') or value.startswith('tel:') or value.startswith('javascript:'):
            continue
        if re.match(r'https?://', value):
            if not value.startswith('https://'):
                issues.append(f'external resource is not HTTPS: {value}')
        elif '.html' in value:
            local = value.split('#')[0].split('?')[0]
            if local and not (SITE / local).exists():
                issues.append(f'broken local link: {value}')

    scripts = '\n'.join(script.get_text() for script in soup.find_all('script'))
    functions = set()
    for match in FUNC_RE.finditer(scripts):
        functions.add(match.group(1) or match.group(2))
    onclick_functions = set()
    for tag in soup.find_all(attrs={'onclick': True}):
        for match in ONCLICK_RE.finditer(tag['onclick']):
            onclick_functions.add(match.group(1))
    builtins = {'alert', 'confirm', 'event', 'encodeURIComponent'}
    missing = sorted(fn for fn in onclick_functions if fn not in functions and fn not in builtins)
    if missing:
        issues.append('onclick function not found: ' + ', '.join(missing))
    return issues

def check_js_syntax(path: Path, index: int, code: str, module: bool):
    suffix = '.mjs' if module else '.js'
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', suffix=suffix, delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name
    try:
        result = subprocess.run(['node', '--check', tmp_path], capture_output=True, text=True)
        return result.returncode == 0, result.stderr.strip()
    finally:
        os.unlink(tmp_path)

def main():
    exit_code = 0
    print(f'SITE: {SITE}')
    print('HTML STATIC CHECK')
    for path in HTML_FILES:
        issues = inspect_html(path)
        print(f'- {path.name}: ' + ('OK' if not issues else 'ISSUES'))
        for issue in issues:
            print(f'  * {issue}')
        if issues:
            exit_code = 1

    print('\nJAVASCRIPT SYNTAX CHECK')
    for path in HTML_FILES:
        soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
        for idx, script in enumerate(soup.find_all('script')):
            code = script.get_text()
            if not code.strip():
                continue
            ok, err = check_js_syntax(path, idx, code, script.get('type') == 'module')
            print(f'- {path.name} script {idx}: ' + ('OK' if ok else 'FAIL'))
            if not ok:
                print(err)
                exit_code = 1
    raise SystemExit(exit_code)

if __name__ == '__main__':
    main()
