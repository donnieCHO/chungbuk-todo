from pathlib import Path
import re
import subprocess
import sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import threading
import urllib.request
import time

ROOT = Path(__file__).resolve().parent
REQUIRED = [
    'index.html','details.html','drivelink.html','timetable.html','contact.html','admin.html','dricelink.html',
    'README.md','DEPLOYMENT_CHECKLIST.md','DEPLOYMENT_AUDIT_REPORT.txt','CODE_REVIEW_REPORT.md','CHANGELOG.md','prompt.md','robots.txt','OPERATIONS_SAFETY_GUIDE.md',
    'assets/app-config.js','assets/runtime-safety.js','assets/safety.css','assets/ui-select.js','assets/ui-select.css',
    'assets/cbe-logo.png','assets/favicon.ico','assets/favicon-64.png','assets/favicon-32.png','assets/favicon-16.png','assets/apple-touch-icon.png'
]
HTMLS = ['index.html','details.html','drivelink.html','timetable.html','contact.html','admin.html','dricelink.html']

errors = []
report = []

def ok(msg): report.append(f'- OK: {msg}')
def fail(msg):
    report.append(f'- FAIL: {msg}')
    errors.append(msg)

report.append('DEPLOYMENT AUDIT REPORT')
report.append('=======================')
report.append(time.strftime('Generated: %Y-%m-%d %H:%M:%S'))
report.append('')

report.append('FILE EXISTENCE CHECK')
for name in REQUIRED:
    if (ROOT/name).exists(): ok(name)
    else: fail(f'missing {name}')
report.append('')

report.append('ENCODING / HTML STATIC CHECK')
for name in HTMLS:
    p = ROOT/name
    text = p.read_text(encoding='utf-8')
    if text.startswith('\ufeff'): fail(f'{name}: BOM detected')
    if '<!DOCTYPE html>' not in text[:50]: fail(f'{name}: missing doctype')
    else: ok(f'{name}: doctype')
    if 'lang="ko"' not in text: fail(f'{name}: missing lang ko')
    if '<meta charset="UTF-8"' not in text: fail(f'{name}: missing charset')
    if '<meta name="viewport"' not in text: fail(f'{name}: missing viewport')
    if '<meta name="robots" content="noindex,nofollow,noarchive"' not in text: fail(f'{name}: missing noindex')
    if 'assets/cbe-logo.png' in text.split('<body',1)[-1]: fail(f'{name}: visible body logo reference')
    if '<img' in text.split('<body',1)[-1]: fail(f'{name}: body img tag detected')
report.append('')

report.append('NAVIGATION CHECK')
nav_labels = ['내 Action','상세 관리','파일 관리','운영 시간표','Contact']
for name in ['index.html','details.html','drivelink.html','timetable.html','contact.html','admin.html']:
    text = (ROOT/name).read_text(encoding='utf-8')
    for label in nav_labels:
        if label not in text: fail(f'{name}: nav missing {label}')
    if name != 'admin.html' and '관리 도구' not in text: fail(f'{name}: nav missing admin link')
    else: ok(f'{name}: nav basic')
report.append('')

report.append('FEATURE MARKER CHECK')
markers = {
    'admin.html':['backupAll','restorePath','hardDeletePath','updateMeta','activity_logs'],
    'assets/runtime-safety.js':['guardReadOnly','safeExternalUrl','downloadJson','recordSyncState'],
    'assets/app-config.js':['readOnlyMode','showContactPage','schemaVersion'],
    'details.html':['deleted:true','activity_logs','safeUpdate'],
    'timetable.html':['locationFilter','duplicateEvent','hasTimeOverlap','window.print'],
    'contact.html':['개인정보 운영 안내','deleted:true'],
    'robots.txt':['Disallow: /']
}
for name, pats in markers.items():
    text=(ROOT/name).read_text(encoding='utf-8')
    for pat in pats:
        if pat not in text: fail(f'{name}: marker missing {pat}')
    ok(f'{name}: feature markers')
report.append('')

report.append('JAVASCRIPT SYNTAX CHECK')
for js in ['assets/app-config.js','assets/runtime-safety.js','assets/ui-select.js']:
    r = subprocess.run(['node','--check',str(ROOT/js)],capture_output=True,text=True)
    if r.returncode == 0: ok(f'{js}: syntax')
    else:
        fail(f'{js}: syntax error')
        report.append(r.stderr)
for name in HTMLS:
    text=(ROOT/name).read_text(encoding='utf-8')
    for idx,(attrs,code) in enumerate(re.findall(r'<script([^>]*)>(.*?)</script>', text, flags=re.S|re.I)):
        if 'src=' in attrs: continue
        code=code.strip()
        if not code: continue
        tmp=ROOT/f'.audit_{Path(name).stem}_{idx}.mjs'
        tmp.write_text(code,encoding='utf-8')
        r=subprocess.run(['node','--check',str(tmp)],capture_output=True,text=True)
        tmp.unlink(missing_ok=True)
        if r.returncode==0: ok(f'{name} script {idx}: syntax')
        else:
            fail(f'{name} script {idx}: syntax error')
            report.append(r.stderr)
report.append('')

report.append('LOCAL STATIC SERVE CHECK')
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass

def serve():
    import os
    os.chdir(ROOT)
    ThreadingHTTPServer(('127.0.0.1', 9876), Quiet).serve_forever()
thread = threading.Thread(target=serve, daemon=True)
thread.start()
time.sleep(0.5)
for name in HTMLS + ['robots.txt','OPERATIONS_SAFETY_GUIDE.md','assets/runtime-safety.js','assets/app-config.js','assets/safety.css']:
    try:
        with urllib.request.urlopen(f'http://127.0.0.1:9876/{name}', timeout=3) as resp:
            if resp.status == 200: ok(f'{name}: HTTP 200')
            else: fail(f'{name}: HTTP {resp.status}')
    except Exception as exc:
        fail(f'{name}: HTTP failed {exc}')
report.append('')
report.append('SUMMARY')
report.append('PASS' if not errors else 'FAIL')
print('\n'.join(report))
sys.exit(1 if errors else 0)
