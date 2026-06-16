#!/usr/bin/env python3
"""
Static deployment audit for the two-tier To Do management service.

이 스크립트는 GitHub Pages에 업로드하기 전 로컬 정적 검수를 수행합니다.
브라우저 기반 Firebase 실제 읽기/쓰기는 수동 테스트가 필요하지만,
배포 전 발견 가능한 인코딩, 링크, ID, JS 문법, inline handler 누락 문제는
여기서 최대한 자동으로 잡습니다.
"""
from __future__ import annotations

import codecs
import html.parser
import http.server
import os
import re
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML_FILES = ["index.html", "details.html", "timetable.html", "drivelink.html", "contact.html", "dricelink.html"]
DOC_FILES = ["README.md", "DEPLOYMENT_CHECKLIST.md", "CHANGELOG.md", "prompt.md", "CODE_REVIEW_REPORT.md"]
REQUIRED_FILES = HTML_FILES + DOC_FILES
LOGO_ASSETS = ["assets/cbe-logo.png", "assets/favicon.ico", "assets/favicon-64.png", "assets/favicon-32.png", "assets/favicon-16.png", "assets/apple-touch-icon.png"]
REQUIRED_LINKS = {
    "index.html": ["details.html", "drivelink.html", "timetable.html", "contact.html"],
    "details.html": ["index.html", "drivelink.html", "timetable.html", "contact.html"],
    "drivelink.html": ["index.html", "details.html", "timetable.html", "contact.html"],
    "timetable.html": ["index.html", "details.html", "drivelink.html", "contact.html"],
    "dricelink.html": ["drivelink.html"],
}
REQUIRED_DB_STRINGS = {
    "index.html": ["tasks", "actions"],
    "details.html": ["tasks", "actions", "migrateLegacyTasks", "majorAdminList", "deleteMajorTask"],
    "drivelink.html": ["tasks", "links"],
    "timetable.html": ["timetable_events", "timetable_locations"],
    "contact.html": ["contacts", "addContact", "saveContactEdit"],
}


class MiniHTMLParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.links: list[tuple[str, str, str]] = []
        self.handlers: list[tuple[str, str, str]] = []
        self.comments: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for attr, value in attrs:
            if value is None:
                continue
            if attr == "id":
                self.ids.append(value)
            if attr in {"href", "src"}:
                self.links.append((tag, attr, value))
            if attr.startswith("on"):
                self.handlers.append((tag, attr, value))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_comment(self, data: str) -> None:
        self.comments.append(data)


def read_bytes(name: str) -> bytes:
    return (ROOT / name).read_bytes()


def read_text(name: str) -> str:
    return read_bytes(name).decode("utf-8")


def parse_html(name: str) -> MiniHTMLParser:
    parser = MiniHTMLParser()
    parser.feed(read_text(name))
    return parser


def status_line(errors: list[str]) -> list[str]:
    return ["- OK"] if not errors else [f"- FAIL: {err}" for err in errors]


def check_files() -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        if not (ROOT / name).exists():
            errors.append(f"missing file: {name}")
    return errors


def check_logo_assets() -> list[str]:
    errors: list[str] = []
    for name in LOGO_ASSETS:
        path = ROOT / name
        if not path.exists():
            errors.append(f"missing logo/favicon asset: {name}")
        elif path.stat().st_size == 0:
            errors.append(f"empty logo/favicon asset: {name}")
    for name in HTML_FILES:
        text = read_text(name)
        if "assets/favicon.ico" not in text or "apple-touch-icon" not in text:
            errors.append(f"{name}: favicon/apple touch icon metadata missing")
        if "og:image" not in text or "twitter:image" not in text:
            errors.append(f"{name}: social image metadata missing")
        # 충북교육청 로고는 favicon/meta 전용입니다. 본문/Header/Hero에 img로 노출하면 안 됩니다.
        if re.search(r'<img[^>]+src=["\']assets/cbe-logo\.png["\']', text, flags=re.I):
            errors.append(f"{name}: page-visible cbe-logo img tag found")
    return errors


def check_encoding_and_html() -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        path = ROOT / name
        if not path.exists():
            continue
        data = path.read_bytes()
        if data.startswith(codecs.BOM_UTF8):
            errors.append(f"{name}: BOM detected")
        if b"\r\n" in data:
            errors.append(f"{name}: CRLF line endings detected")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{name}: not UTF-8 ({exc})")
            continue
        if name.endswith(".html"):
            lower = text.lower()
            if "<!doctype html>" not in lower:
                errors.append(f"{name}: missing DOCTYPE")
            if 'lang="ko"' not in lower:
                errors.append(f"{name}: missing lang=ko")
            if 'charset="utf-8"' not in lower:
                errors.append(f"{name}: missing charset")
            if 'name="viewport"' not in lower:
                errors.append(f"{name}: missing viewport")
            if "http://" in lower:
                errors.append(f"{name}: insecure http:// resource found")
    return errors


def check_duplicate_ids() -> list[str]:
    errors: list[str] = []
    for name in HTML_FILES:
        parser = parse_html(name)
        dupes = [item for item, count in Counter(parser.ids).items() if count > 1]
        if dupes:
            errors.append(f"{name}: duplicate id values: {', '.join(dupes)}")
    return errors


def check_internal_links() -> list[str]:
    errors: list[str] = []
    for name in HTML_FILES:
        parser = parse_html(name)
        found_links = [value for _, _, value in parser.links]
        for link in found_links:
            if "${" in link:
                continue
            if link.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
                continue
            target = link.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue
            # 상대 경로 자산(assets/...)과 HTML 파일 링크를 모두 실제 파일 경로 기준으로 확인합니다.
            if not (ROOT / target).exists():
                errors.append(f"{name}: broken local link -> {link}")
        for required in REQUIRED_LINKS.get(name, []):
            if not any(required in link for link in found_links):
                errors.append(f"{name}: expected navigation link missing -> {required}")
    return errors


def extract_inline_scripts(html: str) -> list[tuple[str, str]]:
    scripts: list[tuple[str, str]] = []
    for match in re.finditer(r"<script([^>]*)>(.*?)</script>", html, flags=re.S | re.I):
        attrs = match.group(1)
        body = match.group(2).strip()
        if not body or "src=" in attrs.lower():
            continue
        scripts.append((attrs, body))
    return scripts


def check_js_syntax() -> list[str]:
    errors: list[str] = []
    node = subprocess.run(["bash", "-lc", "command -v node"], capture_output=True, text=True)
    if node.returncode != 0:
        return ["node is not available; skipped JS syntax check"]
    with tempfile.TemporaryDirectory() as td:
        tmpdir = Path(td)
        for name in HTML_FILES:
            for idx, (attrs, script) in enumerate(extract_inline_scripts(read_text(name))):
                suffix = ".mjs" if "module" in attrs.lower() else ".js"
                js_path = tmpdir / f"{name}.{idx}{suffix}"
                js_path.write_text(script, encoding="utf-8")
                result = subprocess.run(["node", "--check", str(js_path)], capture_output=True, text=True)
                if result.returncode != 0:
                    errors.append(f"{name} script {idx}: {result.stderr.strip()}")
    return errors


def check_inline_handlers() -> list[str]:
    errors: list[str] = []
    call_pattern = re.compile(r"^\s*([A-Za-z_$][\w$]*)\s*\(")
    for name in HTML_FILES:
        text = read_text(name)
        parser = parse_html(name)
        for _tag, attr, code in parser.handlers:
            match = call_pattern.match(code)
            if not match:
                continue
            fn = match.group(1)
            if f"window.{fn}" not in text and f"function {fn}" not in text:
                errors.append(f"{name}: inline {attr} calls undefined function {fn}()")
    return errors


def check_required_strings() -> list[str]:
    errors: list[str] = []
    for name, strings in REQUIRED_DB_STRINGS.items():
        text = read_text(name)
        for needle in strings:
            if needle not in text:
                errors.append(f"{name}: expected implementation marker missing -> {needle}")
    return errors


def check_usage_guides_and_comments() -> list[str]:
    errors: list[str] = []
    for name in ["index.html", "details.html", "drivelink.html", "timetable.html", "contact.html"]:
        text = read_text(name)
        if "사용법" not in text:
            errors.append(f"{name}: usage guide text not found")
        comment_count = len(re.findall(r"<!--|/\*|// ", text))
        minimum = 15 if name != "timetable.html" else 20
        if comment_count < minimum:
            errors.append(f"{name}: comment count looks low ({comment_count})")
    return errors


def check_theme_toggle() -> list[str]:
    errors: list[str] = []
    theme_pages = ["index.html", "details.html", "drivelink.html", "timetable.html", "contact.html"]
    for name in theme_pages:
        text = read_text(name)
        if 'id="themeToggle"' not in text:
            errors.append(f"{name}: theme toggle button missing")
        if 'todo.theme' not in text:
            errors.append(f"{name}: theme persistence script missing")
        if 'html[data-theme="light"]' not in text:
            errors.append(f"{name}: light theme CSS missing")
        body_start = text.lower().find('<body')
        body_text = text[body_start:] if body_start != -1 else text
        if 'assets/cbe-logo.png' in body_text:
            errors.append(f"{name}: cbe logo should not be rendered in page body/header/hero")
    return errors



def check_custom_dropdown() -> list[str]:
    errors: list[str] = []
    css_path = ROOT / "assets/ui-select.css"
    js_path = ROOT / "assets/ui-select.js"
    if not css_path.exists():
        errors.append("assets/ui-select.css missing")
    elif "native-select-hidden" not in css_path.read_text(encoding="utf-8"):
        errors.append("assets/ui-select.css: native-select-hidden marker missing")
    if not js_path.exists():
        errors.append("assets/ui-select.js missing")
    else:
        js_text = js_path.read_text(encoding="utf-8")
        if "window.refreshCustomSelects" not in js_text:
            errors.append("assets/ui-select.js: refreshCustomSelects marker missing")
        node = subprocess.run(["bash", "-lc", "command -v node"], capture_output=True, text=True)
        if node.returncode == 0:
            result = subprocess.run(["node", "--check", str(js_path)], capture_output=True, text=True)
            if result.returncode != 0:
                errors.append(f"assets/ui-select.js: {result.stderr.strip()}")
    pages = ["index.html", "details.html", "drivelink.html", "timetable.html", "contact.html"]
    for name in pages:
        text = read_text(name)
        if 'href="assets/ui-select.css"' not in text:
            errors.append(f"{name}: ui-select.css link missing")
        if 'src="assets/ui-select.js"' not in text:
            errors.append(f"{name}: ui-select.js script link missing")
    return errors


def check_static_serve() -> list[str]:
    errors: list[str] = []

    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:
            pass

    cwd = os.getcwd()
    os.chdir(ROOT)
    try:
        with socketserver.TCPServer(("127.0.0.1", 0), Handler) as httpd:
            port = httpd.server_address[1]
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()
            time.sleep(0.1)
            for name in REQUIRED_FILES:
                try:
                    with urllib.request.urlopen(f"http://127.0.0.1:{port}/{name}", timeout=5) as resp:
                        _ = resp.read()
                        if resp.status != 200:
                            errors.append(f"{name}: HTTP {resp.status}")
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"{name}: HTTP check failed ({exc})")
            httpd.shutdown()
    finally:
        os.chdir(cwd)
    return errors


def main() -> int:
    sections = [
        ("FILE EXISTENCE CHECK", check_files),
        ("LOGO / FAVICON ASSET CHECK", check_logo_assets),
        ("ENCODING / HTML STATIC CHECK", check_encoding_and_html),
        ("DUPLICATE ID CHECK", check_duplicate_ids),
        ("INTERNAL LINK / NAVIGATION CHECK", check_internal_links),
        ("INLINE HANDLER CHECK", check_inline_handlers),
        ("JAVASCRIPT SYNTAX CHECK", check_js_syntax),
        ("REQUIRED FEATURE MARKER CHECK", check_required_strings),
        ("USAGE GUIDE / COMMENT CHECK", check_usage_guides_and_comments),
        ("THEME TOGGLE / BODY LOGO CHECK", check_theme_toggle),
        ("CUSTOM DROPDOWN UI CHECK", check_custom_dropdown),
        ("LOCAL STATIC SERVE CHECK", check_static_serve),
    ]
    all_errors: list[str] = []
    report_lines: list[str] = [
        "DEPLOYMENT AUDIT REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Root: {ROOT}",
        "",
    ]
    for title, fn in sections:
        errors = fn()
        report_lines.append(title)
        report_lines.extend(status_line(errors))
        report_lines.append("")
        all_errors.extend(errors)

    report_lines.append("SUMMARY")
    report_lines.append("PASS" if not all_errors else "FAIL")
    if not all_errors:
        report_lines.append("Static deployment checks passed. Firebase live read/write still requires browser-based manual verification after deployment.")
    else:
        report_lines.append(f"{len(all_errors)} issue(s) found. Fix before deployment.")

    report = "\n".join(report_lines) + "\n"
    print(report)
    (ROOT / "DEPLOYMENT_AUDIT_REPORT.txt").write_text(report, encoding="utf-8")
    return 0 if not all_errors else 1


if __name__ == "__main__":
    sys.exit(main())
