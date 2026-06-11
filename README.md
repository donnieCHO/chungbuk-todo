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
2. 지금 해야 할 일, 이번 주 Action, 확인/대기 중, 나중에 볼 일을 확인합니다.
3. 빠른 Action 추가 영역에서 주요 과제를 선택하고 Action Item을 추가합니다.
4. 완료된 Action은 기본 접힘 상태이며 필요할 때 펼칩니다.

### details.html — 상세 관리

1. 카테고리를 선택해 주요 과제를 만듭니다.
2. 각 주요 과제 안에 세부 Action Item을 추가합니다.
3. Action Item 단위로 메모와 링크를 관리합니다.
4. 기존 평면형 `tasks/{key}.text` 데이터가 있으면 변환 패널에서 2단계 구조로 변환합니다.

### drivelink.html — 파일 링크 관리

1. Action Item에 첨부된 링크를 한 화면에서 확인합니다.
2. 검색/필터로 필요한 파일을 찾습니다.
3. 링크 삭제는 Firebase DB의 URL 기록만 삭제하며, Google Drive 등 외부 원본 파일은 삭제하지 않습니다.

### timetable.html — 운영 시간표

1. 빈 시간 칸을 드래그해 새 일정을 추가합니다.
2. 장소 태그를 선택하거나 새 장소 태그를 추가합니다.
3. 상단 `장소 관리`에서 장소 태그를 수정/삭제할 수 있습니다.
4. 시간표는 `timetable_events`, 장소 태그는 `timetable_locations` 노드를 사용합니다.

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

details.html: 주요 과제 추가, 카테고리 선택, Action Item 추가/수정/삭제, 메모/링크

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
3. Action Item 내용, 담당자, 상태, 우선순위, due date를 입력합니다.
4. 저장하면 Firebase의 `tasks/{majorTaskKey}/actions/{actionKey}`에 기록됩니다.
5. 화면은 즉시 다시 렌더링되며, 각 주요 과제 내부의 Action Item은 due date가 빠른 순서로 표시됩니다.

`details.html`과 `index.html`의 주요 과제 기본 정렬은 가장 임박한 미완료 Action Item의 due date 기준입니다.


## 최신 UI 변경 요약

- 카테고리는 `강의`, `장소`, `운영`, `사후처리` 4개로 사용합니다. 기존 데이터의 과거 카테고리 표기는 화면에서 새 카테고리로 정규화됩니다.
- Action Item 등록 시 `상태`는 입력하지 않습니다. 새 Action Item은 기본적으로 `해야 함(todo)`으로 저장되고, 완료 버튼으로만 완료 상태를 바꿉니다.
- `회신을 기다리는 곳`은 NSD/네이버/업스테이지/세종대 태그로 선택합니다. 선택된 태그는 `waitingFor` 배열로 저장됩니다.
- 상세 관리 하단에는 임시 `주요 과제 관리` 목록이 있어 주요 과제를 보면서 수정/삭제할 수 있습니다.
