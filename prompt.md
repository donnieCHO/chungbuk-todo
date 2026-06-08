# 동일 구조 To Do List 관리서비스 제작 프롬프트

이 파일은 현재 To Do List 관리서비스와 같은 구조의 정적 웹앱을 새 프로젝트용으로 다시 만들기 위한 **마스터 프롬프트**입니다.

새 대화에서 이 파일 전체를 붙여넣고, 아래의 `[프로젝트 입력값]`만 바꿔 사용하면 됩니다.

---

## 0. 프로젝트 입력값

아래 값을 먼저 채워 넣으세요. 아직 정해지지 않은 값은 `미정`으로 두고, AI에게 먼저 질문하게 하면 됩니다.

```txt
프로젝트명: [예: 충북교육청 AI 교원연수]
서비스명: [예: To Do List 관리서비스]
주요 일정: [예: 2026년 8월 12일 ~ 14일]
D-Day 기준일: [예: 2026-08-12]
장소: [예: 세종대학교]
참여 규모: [예: 50명 이하]

담당 주체/기관:
- 운영팀: #e8ecf4
- 네이버: #00c73c
- Upstage: #8b5cf6
- 세종대: #c3002f
- 교육청: #f5c842

업무 카테고리:
- 강사·커리큘럼: 🎓, #7c6af7
- 장소·시설: 🏛️, #3dd68c
- 운영·물품: ⚙️, #f7a34f
- 사후처리: 📊, #f76f6f

시간표 일정 구분:
- 공통: #3dd68c
- 세종대: #c3002f
- 업스테이지: #8b5cf6

시간표 날짜:
- 2026-08-12, 8월 12일, 수
- 2026-08-13, 8월 13일, 목
- 2026-08-14, 8월 14일, 금

시간표 시간 범위:
- 시작: 07:00
- 종료: 23:00
- 단위: 30분

Firebase 사용 여부: [예: 사용]
Firebase Realtime Database 노드:
- tasks
- contacts
- timetable_events

Firebase 설정값:
[아직 없으면 placeholder 유지. 실제 운영 전 firebaseConfig로 교체]
```

---

# 1. 마스터 프롬프트

아래 프롬프트를 그대로 붙여넣어 사용하세요.

```txt
너는 20년차 이상의 웹 퍼블리셔이자 프론트엔드 엔지니어야.
정적 HTML/CSS/JavaScript만으로 동작하는 Firebase Realtime Database 기반 협업 To Do 관리서비스를 만들어줘.

목표는 단순한 To Do 앱이 아니라, 아래 구조의 운영용 웹앱을 만드는 것이다.

[배포 루트]/
├── index.html              # 메인: 본인이 해야 하는 일 중심 대시보드
├── details.html            # 상세 관리: 전체 To Do, 메모, 링크, 타임라인, 연락처
├── timetable.html          # 운영 시간표: 30분 단위 시간표와 일정 편집
├── drivelink.html          # 파일 관리: To Do에 연결된 링크 모아보기
├── dricelink.html          # 오타 호환 리다이렉트: drivelink.html로 이동
├── README.md               # 배포/운영 안내
├── DEPLOYMENT_CHECKLIST.md # 배포 전후 점검 체크리스트
└── DEPLOYMENT_AUDIT_REPORT.txt 또는 deployment_audit.py # 정적 점검 결과 또는 점검 스크립트

중요한 방향은 다음과 같다.

1. index.html은 전체 관리 페이지가 아니라, 사용자가 “지금 내가 무엇을 해야 하는지” 바로 확인하는 메인 대시보드로 만든다.
2. 기존의 전체 관리형 페이지는 details.html로 분리한다.
3. timetable.html은 별도 운영 시간표 페이지로 둔다.
4. drivelink.html은 tasks 내부의 links 데이터만 모아서 보는 파일 링크 관리 페이지로 만든다.
5. 모든 페이지는 상호 이동 링크를 가져야 한다.
6. 모든 페이지는 빌드 도구 없이 GitHub Pages 같은 정적 호스팅에 바로 올릴 수 있어야 한다.
7. 코드에는 유지보수를 위한 주석을 꼼꼼하게 달아야 한다.
8. UTF-8, lang="ko", 반응형 viewport, HTTPS 외부 리소스, 접근성, 보안 이스케이프를 반드시 점검한다.
```

---

# 2. 기술 스택 요구사항

```txt
기술 스택:
- 순수 HTML/CSS/JavaScript
- 빌드 도구 없음
- 프레임워크 없음
- Firebase Realtime Database SDK v10.12.0 CDN ESM 방식
- Pretendard 폰트 사용
- DM Mono 폰트 사용
- 다크 테마 기본값
- GitHub Pages, Cloudflare Pages, Netlify, Vercel 같은 정적 호스팅 배포 가능

공통 UI:
- 우하단 고정 동기화 상태 배지
- 첫 로딩 스피너 오버레이
- 카드 기반 다크 UI
- 모바일 반응형
- 내부 페이지 이동 링크
- 외부 링크는 target="_blank" rel="noopener" 적용
- 동적 출력값은 escapeHtml, escapeAttr, safeExternalUrl 같은 헬퍼로 보호
```

---

# 3. 공통 설정 블록 요구사항

각 HTML 파일에는 하드코딩이 흩어지지 않도록 설정값을 상단에 모아둔다.

```js
const PROJECT_CONFIG = {
  title: '프로젝트명',
  serviceName: 'To Do List 관리서비스',
  dateText: '2026년 8월 12~14일',
  targetDate: '2026-08-12',
  location: '세종대학교',
  people: '50명 이하'
};

const ENTITY_CONFIG = {
  ops: { label: '운영팀', color: '#e8ecf4' },
  naver: { label: '네이버', color: '#00c73c' },
  upstage: { label: 'Upstage', color: '#8b5cf6' },
  sejong: { label: '세종대', color: '#c3002f' },
  education: { label: '교육청', color: '#f5c842' }
};

const CAT_CONFIG = {
  '강사·커리큘럼': { icon: '🎓', color: '#7c6af7' },
  '장소·시설': { icon: '🏛️', color: '#3dd68c' },
  '운영·물품': { icon: '⚙️', color: '#f7a34f' },
  '사후처리': { icon: '📊', color: '#f76f6f' }
};

const DB_PATHS = {
  tasks: 'tasks',
  contacts: 'contacts',
  timetableEvents: 'timetable_events'
};
```

Firebase 설정값은 placeholder로 두되, 사용자가 값을 제공하면 모든 HTML 파일에 동일하게 반영한다.

```js
const firebaseConfig = {
  apiKey: 'YOUR_API_KEY',
  authDomain: 'YOUR_PROJECT.firebaseapp.com',
  databaseURL: 'https://YOUR_PROJECT-default-rtdb.asia-southeast1.firebasedatabase.app',
  projectId: 'YOUR_PROJECT',
  storageBucket: 'YOUR_PROJECT.firebasestorage.app',
  messagingSenderId: 'YOUR_SENDER_ID',
  appId: 'YOUR_APP_ID'
};
```

---

# 4. Firebase 데이터 구조

Realtime Database는 아래 구조를 사용한다.

```txt
Realtime Database
├── tasks
│   └── {taskKey}
│       ├── text              # 업무 내용
│       ├── owner             # 최종 책임자 키: ops/naver/upstage/sejong/education
│       ├── writer            # 작성자 표시명
│       ├── agencies          # 협업 기관 배열
│       ├── cat               # 카테고리명
│       ├── priority          # high/mid/low
│       ├── status            # todo/doing/review/waiting/done
│       ├── deadline          # YYYY-MM-DD 또는 빈 문자열
│       ├── done              # 기존 호환용 boolean
│       ├── waitingFor        # 확인/대기 대상
│       ├── order             # 정렬용 timestamp
│       ├── createdAt
│       ├── updatedAt
│       ├── memos
│       │   └── {memoKey}
│       │       ├── writer
│       │       ├── text
│       │       └── ts
│       └── links
│           └── {linkKey}
│               ├── url
│               ├── label
│               └── ts
├── contacts
│   └── {contactKey}
│       ├── name
│       ├── org
│       ├── role
│       ├── phone
│       ├── email
│       └── order
└── timetable_events
    └── {eventKey}
        ├── title
        ├── day
        ├── start
        ├── end
        ├── cat
        ├── memo
        ├── createdAt
        └── updatedAt
```

기존 데이터와 호환되도록 아래 보정 함수를 반드시 둔다.

```js
function normalizeTask(task) {
  return {
    ...task,
    owner: task.owner || inferOwner(task),
    status: task.status || (task.done ? 'done' : 'todo'),
    agencies: Array.isArray(task.agencies) ? task.agencies : [],
    priority: task.priority || 'mid',
    deadline: task.deadline || '',
    waitingFor: task.waitingFor || ''
  };
}
```

---

# 5. index.html 요구사항 — 내 할 일 중심 메인

`index.html`은 사용자가 본인에게 필요한 업무만 빠르게 확인하는 화면이다.

필수 기능:

```txt
- 상단 히어로 영역
  - “오늘은 무엇부터 처리하면 될까요?” 같은 행동 중심 문구
  - 프로젝트명, 일정, 장소, D-Day
  - 전체 진행률 요약

- 상단 네비게이션
  - 상세 관리(details.html)
  - 시간표(timetable.html)
  - 파일 관리(drivelink.html)

- 내 보기 필터
  - 전체
  - 운영팀
  - 네이버
  - Upstage
  - 세종대
  - 교육청

- 빠른 업무 추가
  - 다음 행동 입력
  - 책임자 선택
  - 기한 선택
  - 세부 옵션 접기/펼치기
    - 상태
    - 우선순위
    - 카테고리
    - 기다리는 대상
    - 협업기관

- 업무 그룹
  - 🔥 지금 해야 할 일
  - 🗓 이번 주에 해야 할 일
  - ⏳ 확인/대기 중
  - 🌙 나중에 볼 일
  - ✅ 완료된 항목

- 카드 기본 표시
  - 완료 체크
  - 업무명
  - 기한
  - 책임자
  - 우선순위
  - 메모 수
  - 링크 수
  - 상세 버튼
  - 파일 버튼

- 카드 클릭 시 상세 모달
  - 상태
  - 책임자
  - 협업기관
  - 카테고리
  - 기한
  - waitingFor
  - 최근 메모
  - 링크 목록
  - 메모 빠른 추가
  - 링크 빠른 추가
  - 완료 처리
  - details.html#ti-{taskKey}로 이동
```

업무 분류 기준:

```txt
지금 해야 할 일:
- 기한 초과
- 오늘 마감
- 3일 이내 마감이면서 high
- status가 doing 또는 review

이번 주에 해야 할 일:
- 7일 이내 마감
- 아직 완료되지 않음
- 현재 내 보기 대상과 관련 있음

확인/대기 중:
- status가 review 또는 waiting
- waitingFor 값이 있음

나중에 볼 일:
- 위 조건에 해당하지 않는 미완료 업무

완료된 항목:
- done === true 또는 status === 'done'
```

정렬 기준:

```txt
1. 기한 초과
2. 오늘 마감
3. 3일 이내
4. high 우선순위
5. doing/review 상태
6. 이번 주 마감
7. updatedAt 최신순
```

---

# 6. details.html 요구사항 — 상세 관리

`details.html`은 전체 관리 페이지다. 기존의 종합 To Do 관리 기능을 이 파일에 넣는다.

필수 기능:

```txt
- 전체 To Do 관리
- 새 항목 추가 상세 폼
- 카테고리별 보기
- 우선순위별 보기
- 날짜 임박순 보기
- 업무 구분 필터
- 담당기관 필터
- 완료 항목 별도 접이식 섹션
- 메모 추가/수정/삭제
- 링크 추가/삭제
- 업무 수정 모달
- 업무 삭제
- 완료 토글
- 타임라인
- 연락처 관리
- index.html, timetable.html, drivelink.html로 이동하는 상단 링크
```

중요 구현 조건:

```txt
- 각 업무 카드 id는 ti-{taskKey} 형식으로 둔다.
- index.html 또는 drivelink.html에서 details.html#ti-{taskKey}로 이동하면 Firebase 데이터 렌더링 후 해당 카드로 스크롤한다.
- 메모 입력은 Enter 키를 지원한다.
- 링크 입력은 http/https가 없으면 https://를 자동 보정한다.
- 완료된 항목은 메인 미완 목록에서 분리한다.
- 동적 출력은 반드시 escapeHtml 처리한다.
```

---

# 7. timetable.html 요구사항 — 운영 시간표

`timetable.html`은 `timetable_events` 노드를 사용한다.

필수 기능:

```txt
- 별도 페이지
- 상단 링크
  - ← 메인(index.html)
  - 상세 관리(details.html)
  - 파일 관리(drivelink.html)

- 시간표 그리드
  - 날짜 N일치
  - 시작 시간 ~ 종료 시간
  - 30분 단위
  - 1시간 단위 실선
  - 30분 단위 점선

- 일정 추가
  - 빈 칸을 마우스로 드래그하면 시간 범위 선택
  - 드래그 종료 시 모달 자동 오픈

- 일정 수정/삭제
  - 일정 카드를 클릭하면 편집 모달
  - 삭제 버튼 포함

- 일정 필드
  - 제목
  - 날짜
  - 시작 시간
  - 종료 시간
  - 분류
  - 메모

- 카테고리 색상
  - 공통
  - 세종대
  - 업스테이지

- UX
  - Esc로 모달 닫기
  - 모달 바깥 클릭으로 닫기
  - 모바일에서 CSS row height와 JS 위치 계산이 어긋나지 않도록 실제 CSS 변수 값을 읽어 계산
```

---

# 8. drivelink.html 요구사항 — 파일 링크 관리

`drivelink.html`은 파일 원본을 저장하지 않는다. Firebase `tasks/{taskKey}/links/{linkKey}`에 저장된 링크만 모아 보여준다.

필수 기능:

```txt
- 전체 첨부 링크 목록
- 연결된 업무명 표시
- 업무 카테고리 표시
- 책임자/담당기관 표시
- 링크 라벨 표시
- URL 표시
- 추가일 표시
- 링크 열기
- details.html#ti-{taskKey}로 업무 상세 이동
- 링크 삭제
- 검색
  - 파일명
  - URL
  - 업무명
- 담당자 필터
- 카테고리 필터
- ?task={taskKey} 쿼리가 있으면 해당 업무 링크만 우선 표시
```

통계 카드:

```txt
- 전체 링크 수
- 파일이 있는 업무 수
- Google Drive 링크 수
- 최근 7일 추가 링크 수
```

보안 조건:

```txt
- 삭제는 Firebase의 링크 레코드만 삭제한다.
- Google Drive 원본 파일 삭제가 아님을 UI에 명확히 표시한다.
- 링크 열기는 safeExternalUrl을 통과한 http/https만 허용한다.
- javascript:, data:, vbscript: 등은 열지 않는다.
```

---

# 9. dricelink.html 요구사항 — 오타 호환

사용자가 `dricelink.html`로 잘못 접속해도 `drivelink.html`로 이동하도록 매우 작은 리다이렉트 파일을 만든다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="0; url=drivelink.html">
  <title>파일 관리로 이동</title>
</head>
<body>
  <script>location.replace('drivelink.html');</script>
  <p><a href="drivelink.html">파일 관리 페이지로 이동</a></p>
</body>
</html>
```

---

# 10. README.md 요구사항

README는 단순 소개가 아니라 실제 배포자가 따라 할 수 있는 운영 문서로 작성한다.

포함 내용:

```txt
- 서비스 개요
- 파일 구조
- 페이지별 역할
- Firebase 데이터 구조
- GitHub Pages 배포 방법
- Cloudflare Pages 배포 방법
- Firebase 설정 위치
- Firebase 보안 규칙 주의사항
- 파일은 직접 DB에 저장하지 않고 Google Drive 등 외부 링크만 저장한다는 안내
- 배포 전 점검 목록
- 배포 후 브라우저 수동 테스트 목록
- 문제 해결
```

---

# 11. DEPLOYMENT_CHECKLIST.md 요구사항

배포 전후 체크리스트를 별도 파일로 만든다.

체크 항목:

```txt
인코딩/문서:
- UTF-8
- BOM 없음
- LF 줄바꿈
- <!DOCTYPE html>
- html lang="ko"
- meta charset="UTF-8"
- viewport

링크:
- index.html → details.html
- index.html → timetable.html
- index.html → drivelink.html
- details.html → index.html
- details.html → timetable.html
- details.html → drivelink.html
- timetable.html → index.html
- timetable.html → details.html
- timetable.html → drivelink.html
- drivelink.html → index.html
- drivelink.html → details.html
- drivelink.html → timetable.html
- dricelink.html → drivelink.html

JavaScript:
- 모든 inline script 문법 검사
- onclick 함수는 window.*에 연결
- 네이티브 API 이름 덮어쓰기 금지
- Firebase onValue 에러 핸들러 포함
- async 저장 오류 catch 또는 try/catch 포함

보안:
- 동적 HTML escape
- 외부 URL safe 처리
- target="_blank"에는 rel="noopener"
- Firebase secret/service key 노출 금지
- 파일 원본을 DB에 저장하지 않음

브라우저 수동 확인:
- 업무 추가
- 업무 완료 토글
- 상세 페이지 반영
- 메모 추가
- 링크 추가
- drivelink에서 링크 확인
- 시간표 일정 추가/수정/삭제
- 모바일 화면 확인
- 다른 브라우저에서 실시간 동기화 확인
```

---

# 12. 코드 품질 및 주석 요구사항

각 파일에는 아래 수준의 주석을 달아야 한다.

```txt
- 파일 상단: 이 페이지의 역할과 연결되는 Firebase 노드 설명
- CSS: 큰 섹션별 주석
- JavaScript: 설정/상태/Firebase/렌더링/이벤트/헬퍼/초기화 구분
- 복잡한 로직: 왜 필요한지 설명
- 보안 헬퍼: 어떤 공격을 막는지 설명
- 데이터 보정 함수: 기존 데이터 호환 목적 설명
```

예시:

```js
/* =========================================================
   Firebase Realtime Database 연결
   - tasks: To Do 업무, 메모, 첨부 링크
   - contacts: 참여자 연락처
   - timetable_events: 운영 시간표 일정
   ========================================================= */
```

---

# 13. 보안/안정성 필수 헬퍼

아래 계열의 헬퍼를 반드시 구현한다.

```js
function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, ch => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[ch]));
}

function escapeAttr(value) {
  return escapeHtml(value).replace(/`/g, '&#96;');
}

function safeExternalUrl(rawUrl) {
  const value = String(rawUrl || '').trim();
  if (!value) return '';
  const normalized = /^https?:\/\//i.test(value) ? value : `https://${value}`;
  try {
    const url = new URL(normalized);
    if (!['http:', 'https:'].includes(url.protocol)) return '';
    return url.href;
  } catch (error) {
    return '';
  }
}
```

동적 HTML을 template literal로 만들 때는 반드시 이 헬퍼를 사용한다.

---

# 14. 배포 전 최종 점검 프롬프트

코드를 생성한 뒤, 아래 점검을 반드시 수행해라.

```txt
생성한 모든 파일을 배포 전 기준으로 다시 점검해줘.

점검 항목:
1. 파일 구조가 정확한가?
2. index.html, details.html, timetable.html, drivelink.html, dricelink.html이 모두 있는가?
3. 모든 HTML이 UTF-8, BOM 없음, LF 줄바꿈인가?
4. 모든 HTML에 DOCTYPE, lang="ko", charset, viewport가 있는가?
5. 내부 링크가 모두 존재하는 파일을 가리키는가?
6. drivelink.html 철자가 정확한가?
7. dricelink.html은 drivelink.html로 이동하는가?
8. 모든 Firebase SDK import가 HTTPS인가?
9. Firebase config가 모든 파일에 동일하게 적용되었는가?
10. tasks, contacts, timetable_events 노드가 분리되어 있는가?
11. index.html은 내 할 일 중심인가?
12. details.html은 전체 관리 기능을 포함하는가?
13. timetable.html은 시간표 기능을 포함하는가?
14. drivelink.html은 links만 모아보는가?
15. 동적 출력값이 escape 처리되는가?
16. 외부 URL이 safeExternalUrl을 통과하는가?
17. target="_blank"에 rel="noopener"가 있는가?
18. onclick에서 호출되는 함수가 window.*로 노출되어 있는가?
19. window.scrollTo 같은 네이티브 API 이름을 덮어쓰지 않았는가?
20. JS 문법 오류가 없는가?
21. 모바일 미디어쿼리가 있는가?
22. 로딩 오버레이가 사라지는가?
23. Firebase onValue 에러 핸들러가 있는가?
24. async 저장 실패 시 사용자가 오류를 알 수 있는가?
25. 배포 문서와 체크리스트가 포함되었는가?

문제가 있으면 즉시 수정하고, 최종 배포 가능한 ZIP 구조로 정리해줘.
```

---

# 15. 최종 산출물 요구사항

AI가 최종적으로 제공해야 할 산출물은 다음과 같다.

```txt
필수 파일:
- index.html
- details.html
- timetable.html
- drivelink.html
- dricelink.html
- README.md
- DEPLOYMENT_CHECKLIST.md

권장 파일:
- DEPLOYMENT_AUDIT_REPORT.txt
- deployment_audit.py

압축 파일:
- release_ready.zip
```

최종 답변에는 아래 내용을 포함한다.

```txt
- 다운로드 링크
- 파일 구조
- 페이지별 역할 요약
- 배포 방법
- 배포 후 수동 확인 목록
- 자동 점검에서 확인한 내용
- 아직 사용자가 직접 확인해야 하는 내용
```

---

# 16. 대화형 정보 수집용 짧은 프롬프트

처음부터 바로 코딩하지 않고 정보를 먼저 모으고 싶다면 아래 프롬프트를 사용한다.

```txt
Firebase 실시간 동기화 기반 To Do List 관리서비스를 만들려고 해.
파일 구조는 index.html, details.html, timetable.html, drivelink.html, dricelink.html로 구성할 거야.

index.html은 본인이 해야 하는 일 중심의 메인 대시보드,
details.html은 전체 상세 관리,
timetable.html은 운영 시간표,
drivelink.html은 첨부 파일 링크 모아보기,
dricelink.html은 drivelink.html로 이동하는 오타 호환 페이지야.

앱을 만들기 전에 아래 정보를 2~3개씩 묶어서 질문해줘.

1. 프로젝트명, 일정, D-Day 기준일, 장소, 참여 규모
2. 담당 주체/기관 목록과 색상
3. 업무 카테고리와 색상/이모지
4. 시간표 날짜와 시간 범위
5. 초기 할 일 목록
6. Firebase 프로젝트가 있는지
7. GitHub Pages 또는 다른 정적 호스팅 배포 방식
```

---

# 17. 기존 프로젝트를 이 구조로 리팩터링하는 프롬프트

이미 `index.html`, `timetable.html`, `README.md`가 있는 기존 프로젝트를 이 구조로 바꿀 때는 아래 프롬프트를 사용한다.

```txt
첨부한 기존 소스를 분석해서 파일 구조를 다시 잡아줘.

새 구조:
[배포 루트]/
├── index.html       # 새 메인: 본인이 해야 하는 일 중심
├── details.html     # 기존 index.html의 상세 관리 기능 이동
├── timetable.html   # 기존 시간표 유지, 네비게이션 보강
├── drivelink.html   # tasks 내부 links만 모아서 보는 파일 관리 페이지 신규 생성
├── dricelink.html   # drivelink.html로 리다이렉트
└── README.md        # 새 구조에 맞게 수정

요구사항:
- 기존 Firebase 설정은 유지한다.
- 기존 tasks, contacts, timetable_events 데이터 구조와 호환되게 만든다.
- 새 index.html에는 owner, status, waitingFor 필드를 사용하되 기존 데이터는 자동 보정한다.
- details.html은 기존 전체 To Do 관리 기능을 유지한다.
- 모든 페이지에 서로 이동하는 링크를 추가한다.
- drivelink.html은 첨부 링크만 모아서 보여준다.
- 코드 주석을 꼼꼼하게 보강한다.
- 배포 전 UTF-8, JS 문법, 내부 링크, 보안 이스케이프를 점검한다.
- 최종 배포 가능한 ZIP으로 정리한다.
```
