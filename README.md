# 충북교육청 AI 교원연수 — To Do List management sheet

Firebase Realtime Database와 GitHub Pages로 운영하는 정적 협업 웹앱입니다. 최신 버전은 **카테고리 → 주요 과제 → Action Item**의 3층 화면 구조, DB 기준으로는 **주요 과제 → Action Item** 2단계 To Do 구조를 사용합니다.

## 파일 구조

```txt
[배포 루트]/
├── index.html                  # 메인: 본인이 해야 할 Action Item 중심 대시보드
├── details.html                # 상세 관리: 카테고리/주요 과제/Action Item/메모/링크 관리
├── drivelink.html              # 파일 관리: Action Item에 첨부된 링크 모아보기
├── timetable.html              # 운영 시간표: 일정 + 장소 태그 관리
├── contact.html                # Contact: 담당자 연락처 추가/수정/삭제
├── dricelink.html              # 오타 호환: drivelink.html로 이동
├── DEPLOYMENT_CHECKLIST.md     # 배포 전 수동 확인표
├── DEPLOYMENT_AUDIT_REPORT.txt # 자동 정적 점검 결과
├── CODE_REVIEW_REPORT.md       # 코드 검수 요약
├── CHANGELOG.md                # 변경 이력
├── prompt.md                   # 동일 구조 재생성 프롬프트
└── deployment_audit.py         # 정적 배포 점검 스크립트
```

## 핵심 UI 변경사항

### 1. 메인 히어로

`index.html` 첫 화면은 아래 타이틀을 크게 보여줍니다.

```txt
충북교육청 AI 교원연수
To Do List management sheet
```

우측에는 D-Day를 크게 표시하고, 전체 완료율을 숫자와 가로 막대로 함께 보여줍니다.

### 2. 사용법 안내

사용법은 처음에는 펼쳐진 상태입니다. 우측 `접기/펼치기` 버튼으로 닫거나 다시 열 수 있습니다.

### 2-1. 담당자/기관 표기

화면에서 내부 key `ops`는 `NSD`로 표시됩니다. 기존 Firebase 데이터와의 호환을 위해 key 값은 그대로 유지합니다.

### 3. 카테고리와 2단계 To Do 구조

카테고리는 고정값으로 사용합니다.

```txt
강의
장소
운영
사후처리
```

DB상 주요 구조는 다음과 같습니다.

```txt
tasks
└── {majorTaskKey}
    ├── title                 # 주요 과제명
    ├── description           # 주요 과제 설명
    ├── cat                   # 카테고리: 강의/장소/운영/사후처리
    ├── owner                 # 주요 책임자
    ├── priority              # high/mid/low
    ├── deadline              # 대표 기한
    ├── status                # todo/doing/review/waiting/done
    ├── done
    └── actions
        └── {actionKey}
            ├── text          # 실제 실행할 Action Item
            ├── owner         # 담당자
            ├── agencies      # 협업기관 배열
            ├── priority
            ├── deadline
            ├── status
            ├── waitingFor
            ├── done
            ├── memos
            └── links
```

### 4. 완료 Action 기본 접힘

`index.html`의 완료된 Action Item 섹션은 기본적으로 접혀 있습니다. 섹션 우측의 `펼치기` 버튼으로 필요할 때만 확인합니다.

### 5. Contact 별도 페이지

주소록은 `contact.html`로 분리했습니다. 상단 메뉴에서 `운영 시간표` 다음에 `Contact` 메뉴가 보입니다. 연락처는 Firebase `contacts` 노드에 저장됩니다.

### 6. 공통 내비게이션 통일

모든 주요 페이지는 아래 순서와 같은 pill 스타일의 공통 내비게이션을 사용합니다. `timetable.html`도 별도 헤더 버튼 방식이 아니라 동일한 sticky nav를 사용하며, 현재 페이지는 active 상태로 표시됩니다.

```txt
내 Action → 상세 관리 → 파일 관리 → 운영 시간표 → Contact
```

```txt
contacts
└── {contactKey}
    ├── name
    ├── org                  # ops/naver/upstage/sejong/education
    ├── role
    ├── phone
    ├── email
    ├── memo
    ├── order
    ├── createdAt
    └── updatedAt
```

## 페이지별 사용 방법

### index.html — 내 Action 대시보드

1. 상단 `내 보기`에서 담당자를 선택합니다.
2. 상단 현황 대시보드에서 오늘·기한초과, 7일 이내, 회신 대기, 다음 마감 정보를 확인합니다.
3. 상세 리스트에서는 `지금 해야 할 일`과 `이번 주 Action`만 집중해서 확인합니다.
4. 빠른 Action 추가 영역에서 주요 과제를 선택하고 Action Item을 추가합니다.
5. 완료된 Action은 기본 접힘 상태이며 필요할 때 펼칩니다.

### details.html — 상세 관리

1. 카테고리를 선택해 주요 과제를 만듭니다.
2. 각 주요 과제 안에 세부 Action Item을 추가합니다.
3. Action Item 단위로 메모와 링크를 관리합니다.
4. 기존 평면형 `tasks/{key}.text` 데이터가 있으면 변환 패널에서 2단계 구조로 변환합니다.
5. 화면 하단 `주요 과제 관리/삭제` 영역에서 주요 과제만 따로 확인하고 수정 또는 삭제할 수 있습니다.

### drivelink.html — 파일 링크 관리

1. Action Item에 첨부된 링크를 한 화면에서 확인합니다.
2. 검색/필터로 필요한 파일을 찾습니다.
3. 링크 삭제는 Firebase DB의 URL 기록만 삭제하며, Google Drive 등 외부 원본 파일은 삭제하지 않습니다.

### timetable.html — 운영 시간표

1. `운영 시간표 사용법` 영역에서 빈 칸 드래그 방식과 장소 태그 사용법을 확인합니다.
2. 빈 시간 칸을 드래그해 새 일정을 추가합니다.
3. 장소 태그를 선택하거나 새 장소 태그를 추가합니다.
4. 상단 `장소 관리`에서 장소 태그를 수정/삭제할 수 있습니다.
5. 시간표는 `timetable_events`, 장소 태그는 `timetable_locations` 노드를 사용합니다.

기본 장소 태그는 다음과 같습니다.

```txt
군자관 4층
군자관 6층 식당
대양AI관 만찬장
```

### contact.html — Contact 관리

1. 담당자 이름과 소속을 입력해 연락처를 추가합니다.
2. 카드 우측 상단의 수정 버튼으로 정보를 업데이트합니다.
3. 전화번호는 `tel:`, 이메일은 `mailto:` 링크로 열립니다.
4. 삭제 버튼은 Firebase의 연락처 레코드만 삭제합니다.

## Firebase 사용 노드

```txt
tasks
contacts
timetable_events
timetable_locations
```

개발/테스트 단계에서는 아래 규칙으로 동작을 확인할 수 있습니다.

```json
{
  "rules": {
    "tasks": { ".read": true, ".write": true },
    "contacts": { ".read": true, ".write": true },
    "timetable_events": { ".read": true, ".write": true },
    "timetable_locations": { ".read": true, ".write": true }
  }
}
```

이 규칙은 링크를 아는 사용자가 누구나 읽고 쓸 수 있는 공개 편집 상태입니다. 실제 운영에서 외부 노출 가능성이 있다면 Firebase Auth 또는 더 엄격한 Rules를 적용하세요.

## 배포 방법

1. ZIP 파일을 풉니다.
2. GitHub Pages 저장소 루트에 모든 파일을 업로드합니다.
3. Settings → Pages → Deploy from a branch → `main`을 선택합니다.
4. 배포 주소에서 아래 동작을 수동 확인합니다.

```txt
index.html: D-Day, 완료율, 빠른 Action 추가, 완료 Action 펼치기

details.html: 주요 과제 추가, 카테고리 선택, Action Item 추가/수정/삭제, 메모/링크, 하단 주요 과제 관리/삭제

drivelink.html: 링크 모아보기, 링크 열기, 링크 삭제

timetable.html: 일정 추가/수정/삭제, 장소 태그 추가/수정/삭제

contact.html: 연락처 추가/수정/삭제, 전화/메일 링크
```

## 배포 전 자동 점검

로컬에서 다음 명령으로 정적 점검을 수행할 수 있습니다.

```bash
python3 deployment_audit.py
```

점검 항목은 UTF-8, BOM 없음, HTML 기본 메타, 중복 ID, 내부 링크, inline handler, JavaScript 문법, 필수 기능 문자열, 사용법 안내, 로컬 정적 서빙입니다.


## Action Item due date 정렬 업데이트

상세 관리 페이지의 To Do 등록은 `주요 과제 설정`과 `Action Item 등록` 두 단계로 나뉩니다.

1. 주요 과제를 먼저 생성합니다.
2. Action Item 등록 폼에서 주요 과제를 선택합니다.
3. Action Item 내용, 담당자, 회신을 기다리는 곳, 우선순위, due date를 입력합니다.
4. 저장하면 Firebase의 `tasks/{majorTaskKey}/actions/{actionKey}`에 기록됩니다.
5. 화면은 즉시 다시 렌더링되며, 각 주요 과제 내부의 Action Item은 due date가 빠른 순서로 표시됩니다.

`details.html`과 `index.html`의 주요 과제 기본 정렬은 가장 임박한 미완료 Action Item의 due date 기준입니다.


## 최신 UI 변경 요약

- 카테고리는 `강의`, `장소`, `운영`, `사후처리` 4개로 사용합니다. 기존 데이터의 과거 카테고리 표기는 화면에서 새 카테고리로 정규화됩니다.
- Action Item 등록 시 `상태`는 입력하지 않습니다. 새 Action Item은 기본적으로 `해야 함(todo)`으로 저장되고, 완료 버튼으로만 완료 상태를 바꿉니다.
- `회신을 기다리는 곳`은 NSD/네이버/업스테이지/세종대 태그로 선택합니다. 선택된 태그는 `waitingFor` 배열로 저장됩니다.
- 상세 관리 하단에는 임시 `주요 과제 관리` 목록이 있어 주요 과제를 보면서 수정/삭제할 수 있습니다.


## 주요 과제 관리/삭제 업데이트

`details.html` 하단에는 `주요 과제 관리/삭제` 영역이 있습니다. 이 영역은 Action Item을 펼치지 않고 주요 과제만 리스트로 보여주며, 각 주요 과제별로 다음 작업을 제공합니다.

```txt
상세 위치로 이동
수정
과제 삭제
```

`과제 삭제`를 누르면 해당 주요 과제와 그 내부의 Action Item, 메모, 링크 기록이 함께 삭제됩니다. 삭제 전 확인창에 삭제 범위가 표시되며, 운영 데이터가 있는 경우 Firebase Console에서 JSON 백업 후 사용하는 것을 권장합니다.

## 2026-06-11 추가 업데이트 — Action Item 등록 UI 정돈

- 상세 관리 페이지 Step 2의 Action Item 등록 폼을 네모형 2열 그리드로 재정돈했습니다.
- `주요 과제 선택창`, `Action Item 입력 창`, `담당`, `회신을 기다리는 곳`, `우선 순위`, `Due Date` 순서로 보이도록 정리했습니다.
- 담당은 dropdown select가 아니라 NSD/네이버/업스테이지/세종대 태그 버튼 중 1개를 선택하는 방식으로 바꿨습니다.
- 회신을 기다리는 곳은 동일한 태그 버튼 UI로 복수 선택할 수 있습니다.
- 네이버 태그는 비활성/활성 상태 모두 녹색 계열로 명확하게 표시됩니다.


## 2026-06-11 추가 업데이트 — 내 Action 대시보드와 시간표 안내 정리

- `index.html`의 회신 대기 선택 UI를 `details.html`과 동일한 태그 버튼 스타일로 맞췄습니다. 네이버는 녹색 계열로 표시됩니다.
- 메인 목록에서 `확인/대기 중`, `나중에 볼 일` 섹션을 제거하고, 대신 상단 `전체 Action 현황` 대시보드에서 회신 대기와 다음 마감 정보를 확인하도록 정리했습니다.
- 완료 버튼은 글자 없이 왼쪽 원형 체크만 표시하도록 정리했습니다. 사용법에는 `왼쪽 원형 체크를 누르면 완료가 됩니다.` 안내를 추가했습니다.
- `timetable.html` 상단 toolbar의 드래그 안내 문구를 제거하고, 같은 내용을 `운영 시간표 사용법` 카드 안으로 이동했습니다.
- 시간표 사용법의 `보기 개선` 안내 문구는 제거했습니다.


## 로고 및 웹페이지 메타

운영 원칙:

```txt
페이지 본문/Header/Hero: 로고 이미지 미노출
favicon/apple-touch-icon: 로고 사용
Open Graph/Twitter image: 로고 사용
```


충북교육청 로고는 `assets/cbe-logo.png`에 저장되어 있으며, **페이지 본문/Header/Hero에는 노출하지 않고 favicon 및 웹페이지 메타 이미지에서만 사용**합니다.

```txt
assets/
├── cbe-logo.png
├── favicon.ico
├── favicon-64.png
├── favicon-32.png
├── favicon-16.png
└── apple-touch-icon.png
```

적용 페이지는 `index.html`, `details.html`, `drivelink.html`, `timetable.html`, `contact.html`, `dricelink.html`입니다. GitHub Pages의 하위 경로 배포에서도 동작하도록 모두 상대 경로를 사용합니다.

## 라이트/다크 모드

전 페이지 공통 내비게이션 오른쪽의 `Light` / `Dark` 버튼으로 화면 테마를 전환할 수 있습니다. 선택값은 브라우저 `localStorage(todo.theme)`에 저장되어 `index.html`, `details.html`, `drivelink.html`, `timetable.html`, `contact.html`에서 동일하게 적용됩니다.

모든 주요 페이지의 본문/Header/Hero에는 로고 이미지를 노출하지 않습니다. favicon, Apple Touch Icon, Open Graph/Twitter 공유 메타에만 `assets/cbe-logo.png`를 사용합니다.


## 2026-06-12 추가 업데이트 — 내 Action 필터와 메모 색상
- 내 Action 페이지의 내 보기 설정은 선택한 담당자와 직접 관련된 Action Item만 보여주도록 정밀화했습니다.
- 관련 기준은 Action Item 담당, 협업기관, 회신 대기 대상입니다. 주요 과제 책임자만 같다는 이유로 관련 없는 Action Item이 노출되지 않도록 조정했습니다.
- Action Item 메모는 작성자별 고유 색상으로 표시됩니다. NSD는 밝은 회색, 네이버는 녹색, 업스테이지는 보라, 세종대는 크림슨, 교육청은 노랑 기준입니다.


## UI 업데이트 — 커스텀 드롭다운 통일

모든 주요 페이지의 `<select>` 입력은 기본 브라우저 UI 대신 공통 커스텀 드롭다운으로 표시됩니다. 원본 `<select>` 요소는 Firebase 연동, `value` 읽기, `change` 이벤트 처리를 위해 DOM에 그대로 유지하고 화면에는 `.custom-select-wrap` 컴포넌트를 렌더링합니다.

적용 페이지:

```txt
index.html
details.html
drivelink.html
timetable.html
contact.html
```

특징:

```txt
라이트/다크 모드 색상 자동 대응
네이버/업스테이지/세종대/NSD/교육청/우선순위 색상 점 표시
동적 option 변경 시 자동 동기화
원본 select의 onchange 로직 유지
```


## 2026-06-12 헤드라인 통일 및 본문 로고 제거 재검수

- details.html, drivelink.html, timetable.html의 상단 헤드라인을 내 Action(index.html) Hero 스타일과 같은 톤으로 통일했습니다.
- 페이지 본문에서는 충북교육청 로고 이미지를 사용하지 않도록 재검수했습니다. 로고는 favicon, apple-touch-icon, Open Graph/Twitter meta 이미지에만 사용합니다.
- drivelink.html Hero의 전체 링크 수가 파일 링크 요약과 함께 갱신되도록 보강했습니다.


## 2026-06-12 추가 정리 — 본문 로고 제거와 Hero 헤드라인 통일

- 충북교육청 로고 이미지는 페이지 본문, Header, Hero 영역에 노출하지 않습니다.
- 로고 자산은 favicon, apple-touch-icon, Open Graph/Twitter meta 이미지 용도로만 유지합니다.
- 5개 주요 페이지(index/details/drivelink/timetable/contact)의 첫 화면은 텍스트 기반 Hero 헤드라인과 우측 상태 카드 구조로 통일합니다.

---

## 🛡️ 오픈 Firebase 운영 안전장치

현재 배포본은 Firebase Realtime Database를 일정 기간 오픈 규칙으로 운영하는 상황을 고려해, 보안 규칙을 바꾸지 않고도 운영 실수를 줄일 수 있는 보조 기능을 포함합니다. 이 기능들은 Firebase Security Rules를 대체하지 않으며, URL을 아는 사람이 접근할 수 있다는 전제를 유지합니다.

### 추가된 관리 도구

`admin.html`에서 아래 기능을 사용할 수 있습니다.

- 전체 데이터 JSON 백업 다운로드
- 노드별 백업 다운로드
- 삭제된 항목 휴지통 보기
- 휴지통 항목 복구
- 휴지통 항목 완전 삭제
- 활동 로그 확인
- `meta` 노드에 schemaVersion/appVersion 기록
- 작업자 라벨 저장

### 새로 추가된 공통 파일

```txt
assets/app-config.js       # 프로젝트 공통 설정, feature flag, 입력 길이 제한
assets/runtime-safety.js   # read-only guard, URL 검증, JSON 다운로드, 동기화 재연결 버튼
assets/safety.css          # 운영 안전장치 UI, print CSS
robots.txt                 # 검색엔진 색인 차단 요청
admin.html                 # 백업/휴지통/로그 관리 도구
```

### 삭제 정책

주요 데이터 삭제는 즉시 삭제하지 않고 기본적으로 아래 필드를 추가합니다.

```js
deleted: true
deletedAt: Date.now()
deletedBy: '작업자 라벨'
```

화면에서는 `deleted:true` 항목을 숨기고, `admin.html`에서 복구하거나 완전 삭제할 수 있습니다.

### 검색 노출 최소화

모든 HTML에는 아래 메타가 포함되어 있습니다.

```html
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="googlebot" content="noindex,nofollow,noarchive">
```

루트에는 `robots.txt`도 포함되어 있습니다. 단, 이는 보안 장치가 아니라 검색 노출을 줄이는 장치입니다.

### 운영 권장 흐름

```txt
1. 대량 수정 전 admin.html에서 전체 백업
2. 작업자 라벨 저장
3. 상세 관리 / 시간표 / Contact에서 수정
4. 삭제가 필요하면 soft delete 처리
5. 실수 삭제 시 admin.html에서 복구
6. 행사 종료 후 readOnlyMode를 true로 전환하거나 Firebase Rules를 읽기 전용으로 변경
```

자세한 운영 절차는 `OPERATIONS_SAFETY_GUIDE.md`를 참고하세요.

### 운영 시간표 데이터가 사라진 것처럼 보일 때

최신 버전에서는 일정 삭제가 즉시 삭제가 아니라 `deleted:true` soft delete로 처리됩니다. 삭제된 일정은 일반 시간표에서 숨겨지고 `admin.html`의 휴지통에서 복구할 수 있습니다.

또한 2026-06-16 배포본에서 `timetable.html`의 장소 필터 상태 변수 `locationFilter` 누락으로 일정 렌더링이 중단될 수 있던 문제를 수정했습니다. Firebase의 `timetable_events` 데이터 자체는 변경하지 않았고, 화면 표시 오류만 수정했습니다.



### 최신 UI 운영 흐름

- 주요 과제 생성과 일괄 Action Item 등록은 `admin.html`의 **To Do 등록** 영역에서 진행합니다.
- `details.html`은 상세 조회, 주요 과제 카드 내부 Action Item 추가, 메모/링크 관리 중심으로 사용합니다.
- `index.html`은 due date 기준 타임라인 형태로 내 Action을 보여줍니다.
- `timetable.html` 일정 카드는 제목과 장소를 우선 표시하고 시간은 보조 정보로 작게 표시합니다.


### 댓글 / 대댓글 스레드 구조

상세 관리 페이지의 Action Item 댓글은 기존 `memos` 노드를 유지하면서, 각 댓글 아래에 `replies` 하위 노드를 추가하는 방식으로 확장했습니다. 기존 댓글 데이터와 호환됩니다.

```txt
tasks
└── {majorTaskKey}
    └── actions
        └── {actionKey}
            └── memos
                └── {memoKey}
                    ├── writer
                    ├── text
                    ├── ts
                    └── replies
                        └── {replyKey}
                            ├── writer
                            ├── text
                            └── ts
```

운영자는 Action Item에 1차 댓글을 남기고, 각 댓글 아래에서 바로 대댓글을 달아 회신·확인 과정을 이어갈 수 있습니다. 댓글과 대댓글 삭제는 `deleted:true` soft delete 방식으로 처리되며, 관리 도구의 휴지통에서 복구 또는 완전 삭제할 수 있습니다.
