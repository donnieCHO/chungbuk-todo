# To Do List 관리서비스 — 배포 패키지

충북교육청 AI 교원연수 준비 업무를 관리하기 위한 정적 웹앱입니다. 빌드 도구 없이 HTML 파일만 GitHub Pages, Cloudflare Pages, Netlify, Vercel 같은 정적 호스팅에 올려 배포할 수 있습니다.

## 1. 파일 구조

```txt
[배포 루트]/
├── index.html              # 메인: 본인이 해야 하는 일 중심 대시보드
├── details.html            # 상세 관리: 전체 To Do, 메모, 링크, 타임라인, 연락처
├── timetable.html          # 운영 시간표: 3일치 시간표와 일정 편집
├── drivelink.html          # 파일 관리: To Do에 연결된 링크 모아보기
├── dricelink.html          # 오타 호환 리다이렉트: drivelink.html로 이동
├── DEPLOYMENT_CHECKLIST.md # 배포 전/후 점검 체크리스트
└── DEPLOYMENT_AUDIT_REPORT.txt # 이번 패키지의 정적 점검 결과
```

> `dricelink.html`은 사용자가 잘못 입력했을 때를 대비한 리다이렉트 파일입니다. 정식 파일명은 `drivelink.html`입니다.

## 2. 페이지별 역할

### `index.html` — 내 할 일 중심 메인

첫 화면에서 사용자가 바로 처리해야 할 업무를 확인하도록 단순화한 대시보드입니다.

- 담당자/기관 기준 보기
- 지금 해야 할 일
- 이번 주 해야 할 일
- 확인/대기 중인 일
- 나중에 볼 일
- 완료된 항목 접기/펼치기
- 빠른 업무 추가
- 업무 상세 모달
- 메모/링크 빠른 추가

### `details.html` — 상세 관리

기존 전체 관리형 To Do 페이지를 `details.html`로 분리했습니다.

- 전체 To Do 관리
- 카테고리별/우선순위별/날짜 임박순 보기
- 담당기관 필터
- 완료 항목 분리
- 메모 추가/수정/삭제
- 링크 추가/삭제
- 타임라인
- 연락처 관리

### `timetable.html` — 운영 시간표

`tasks`와 분리된 `timetable_events`, `timetable_locations` 노드를 사용합니다.

- 2026년 8월 12~14일 시간표
- 30분 단위 그리드
- 드래그로 일정 추가
- 일정 클릭으로 수정/삭제
- 공통/세종대/업스테이지 분류 색상
- 장소 태그 선택/추가/수정/삭제
- 기본 장소 태그: 군자관 4층, 군자관 6층 식당, 대양AI관 만찬장

### `drivelink.html` — 파일 링크 관리

`tasks/{taskKey}/links/{linkKey}`에 저장된 링크만 모아서 보여줍니다.

- 전체 링크 수
- 파일이 연결된 업무 수
- Google Drive 링크 수
- 최근 7일 추가 링크 수
- 파일명/URL/업무명 검색
- 담당자 필터
- 카테고리 필터
- 링크 삭제

## 3. Firebase 데이터 구조

이 패키지는 Firebase Realtime Database를 사용합니다.

```txt
Realtime Database
├── tasks
│   └── {taskKey}
│       ├── text
│       ├── owner
│       ├── writer
│       ├── agencies
│       ├── cat
│       ├── priority
│       ├── status
│       ├── deadline
│       ├── done
│       ├── waitingFor
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
├── timetable_events
│   └── {eventKey}
│       ├── title
│       ├── day
│       ├── start
│       ├── end
│       ├── cat
│       ├── locations
│       ├── memo
│       ├── createdAt
│       └── updatedAt
└── timetable_locations
    └── {locationKey}
        ├── label
        ├── order
        ├── createdAt
        └── updatedAt
```

## 4. 배포 방법

### GitHub Pages 기준

1. 새 GitHub 저장소를 만듭니다.
2. 이 폴더 안의 파일을 저장소 루트에 업로드합니다.
3. 저장소 `Settings → Pages`에서 배포 브랜치를 `main`으로 지정합니다.
4. 배포 URL에서 `index.html`이 열리는지 확인합니다.
5. 네비게이션 링크를 눌러 `details.html`, `timetable.html`, `drivelink.html`이 열리는지 확인합니다.

## 5. 배포 전 필수 확인

배포 전에는 `DEPLOYMENT_CHECKLIST.md`를 기준으로 아래 항목을 확인하세요.

- Firebase Realtime Database 보안 규칙
- Firebase 테스트 모드 만료 여부
- GitHub Pages 배포 루트에 모든 HTML 파일이 있는지
- 링크 파일명이 `drivelink.html`로 맞는지
- 파일 원본은 Google Drive 등 외부 저장소에 두고 URL만 저장하는지
- 모바일에서 메인/상세/시간표/파일관리 페이지가 모두 열리는지

## 6. 이번 점검에서 반영한 사항

- 모든 HTML 파일 UTF-8, BOM 없음, LF 줄바꿈으로 정규화
- `lang="ko"`, `charset="UTF-8"`, `viewport` 확인
- 내부 페이지 링크 검증
- JavaScript 문법 검사 통과
- 동적 출력부 이스케이프 보강
- 외부 링크 `http/https`만 열도록 안전 처리 보강
- 비동기 저장 오류 발생 시 동기화 배지에 오류 표시
- `details.html#ti-...` 직접 진입 시 Firebase 렌더링 후 해당 업무로 스크롤
- `timetable.html` 모바일 행 높이 계산 오류 방지
- `timetable.html` 장소 태그 선택/추가/수정/삭제 기능 추가
- 주요 HTML/CSS/JS 섹션 주석 보강

