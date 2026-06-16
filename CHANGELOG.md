
## 2026-06-16 — 상세 등록 흐름/admin 이동 및 내 Action 타임라인 UI 개편

- `details.html` 상단의 주요 과제/Action Item 일괄 등록 UI를 제거하고, 조회·카드 내부 Action 추가·메모/링크 관리 중심으로 재정리했습니다.
- `admin.html`에 1단 세로 구성의 To Do 등록 영역을 추가했습니다.
- `index.html`의 지금 해야 할 일/이번 주 Action을 due date 타임라인 형태로 표시하도록 변경했습니다.
- `timetable.html` 일정 카드에서 제목과 장소를 우선 표시하고, 시간은 작은 보조 정보로 낮춰 좁은 세로 칸에서도 핵심 내용이 보이도록 정리했습니다.

# 변경 이력

## 2026-06-11 - 내 Action 대시보드/시간표 안내 정리

- `index.html`의 회신 대기 태그 UI를 `details.html`과 동일한 버튼 스타일로 통일했습니다.
- `확인/대기 중`, `나중에 볼 일` 리스트 섹션을 제거하고, 상단 `전체 Action 현황` 대시보드에서 회신 대기와 다음 마감을 확인하도록 바꿨습니다.
- 완료 버튼 라벨 크기를 줄이고 원형 체크 아이콘과 분리해 가독성을 개선했습니다.
- `timetable.html`의 빈 칸 드래그 안내 문구를 toolbar에서 제거하고 `운영 시간표 사용법` 카드 안으로 이동했습니다.
- 시간표 사용법의 `보기 개선` 안내 문구를 제거했습니다.


## 2026-06-11 — 운영 시간표 내비게이션 통일

### Changed

- `timetable.html`의 헤더 내부 이동 버튼을 제거하고 다른 페이지와 같은 공통 sticky nav로 통일했습니다.
- 메뉴 순서를 `내 Action → 상세 관리 → 파일 관리 → 운영 시간표 → Contact`로 맞췄습니다.
- 운영 시간표 메뉴에 active 상태를 적용하고, 장소 관리 버튼은 toolbar 전용 버튼으로 분리했습니다.



## 2026-06-11 — NSD 명칭 통일

### Changed

- 담당자/기관 화면 표시명을 `NSD`로 통일
- 메인 대시보드, 상세 관리, 파일 관리, Contact, prompt 문서의 담당자 표기 업데이트
- 기존 Firebase 데이터 호환을 위해 내부 key `ops`는 유지

## 2026-06-11 — Hero / Category / Contact 개편

### Added

- `contact.html` 신규 추가
  - Firebase `contacts` 노드 연동
  - 연락처 추가/수정/삭제
  - 소속별 카드 그룹
  - 전화 `tel:` 링크, 이메일 `mailto:` 링크
- 모든 주요 페이지 메뉴에 `Contact` 추가
- 메인 `index.html` 히어로 디자인 추가
- D-Day 대형 표시 추가
- 전체 완료율 숫자 `%` + 가로형 진행 막대 추가
- 사용법 안내 접기/펼치기 버튼 추가
- 완료된 Action Item 기본 접힘 처리
- 상세 관리 `details.html` 카테고리 섹션 추가
- 카테고리 고정값 적용
  - 강의
  - 장소
  - 운영
  - 사후처리

### Changed

- 드롭다운/select UI를 전역적으로 통일
- 주요 과제 추가/수정 시 카테고리를 직접 입력이 아닌 선택 방식으로 변경
- 기존 `강의`, `장소`, `운영` 표기를 화면 기준 `강의`, `장소`, `운영`으로 정리
- `deployment_audit.py`에 `contact.html` 검사 추가
- README와 배포 체크리스트를 최신 구조로 재작성

### Kept

- Firebase Realtime Database 기반 실시간 동기화
- `tasks/{majorTaskKey}/actions/{actionKey}` 2단계 To Do 구조
- 기존 평면형 데이터 마이그레이션 기능
- `drivelink.html` 파일 링크 모아보기
- `timetable.html` 장소 태그 및 세로 간격 개선

## Action Item due date 정렬 개선

- 상세 관리 페이지의 To Do 등록을 `주요 과제 설정`과 `Action Item 등록` 2개 폼으로 분리했습니다.
- Action Item 등록 시 due date 입력을 필수화했습니다.
- 주요 과제 내부 Action Item은 due date가 빠른 순서로 자동 정렬됩니다.
- 메인 페이지와 상세 관리 페이지의 기본 주요 과제 정렬을 가장 임박한 Action Item due date 기준으로 변경했습니다.


## 2026-06-11 - 카테고리/회신 대기 태그/완료 UI/주요 과제 임시 관리 개선

- 카테고리를 `강의`, `장소`, `운영`, `사후처리`로 정리했습니다.
- Action Item 등록 시 상태 선택을 제거하고 기본 `todo`로 저장합니다.
- `회신을 기다리는 곳`을 NSD/네이버/업스테이지/세종대 태그 선택형으로 변경했습니다.
- 완료 버튼의 `완료 처리`/`완료됨` 문구를 제거하고, 글자 없는 원형 체크 UI로 되돌렸습니다.
- 상세 관리 하단에 주요 과제 임시 관리 목록을 추가했습니다.


## 2026-06-11 - 주요 과제 관리/삭제 영역 명확화

- `details.html` 하단 영역명을 `주요 과제 관리/삭제`로 명확히 변경했습니다.
- Action Item을 펼치지 않고 주요 과제만 보이는 전용 리스트를 강화했습니다.
- 각 행에 상세 위치 이동, 수정, 과제 삭제 버튼을 제공합니다.
- 삭제 버튼은 해당 주요 과제와 내부 Action Item/메모/링크가 함께 삭제된다는 확인창을 표시합니다.
- 삭제 전 Firebase JSON 백업을 권장하는 안내를 추가했습니다.

## 2026-06-11 — Action Item 등록 UI 정돈

- 상세 관리 Step 2 Action Item 등록 영역을 2열 카드형 그리드로 정리했습니다.
- 담당 dropdown을 NSD/네이버/업스테이지/세종대 단일 선택 태그 버튼으로 변경했습니다.
- 회신 대기 태그 UI와 담당 태그 UI의 스타일을 통일했습니다.
- 네이버 표시를 녹색으로 더 명확하게 적용했습니다.

## 2026-06-11 — 완료 체크 UI 문구 제거

- 내 Action과 상세 관리의 완료 버튼에서 `완료`, `완료됨`, `완료 처리` 텍스트 라벨을 제거했습니다.
- Action Item 왼쪽의 원형 체크 버튼만으로 완료 상태를 전환하도록 UI를 정리했습니다.
- 내 Action 사용법에 `왼쪽 원형 체크를 누르면 완료가 됩니다.` 안내를 추가했습니다.


## 로고 / favicon / 메타 정보 반영

- 충북교육청 로고 이미지를 `assets/cbe-logo.png`로 추가했습니다.
- 당시에는 주요 페이지의 헤더/Hero 영역에 로고를 노출했으나, 이후 본문 노출은 제거했습니다.
- `favicon.ico`, PNG favicon, Apple Touch Icon을 추가했습니다.
- Open Graph / Twitter Card 메타 이미지에 로고를 연결했습니다.
- GitHub Pages 하위 경로 배포를 고려해 모든 자산 경로는 상대 경로로 설정했습니다.

## 2026-06-12 — 라이트/다크 모드 전환 및 내 Action 로고 제거

- 모든 주요 페이지의 본문/헤더/Hero 영역에서 충북교육청 로고 이미지를 제거하고 타이포그래피 중심 구조로 정리했습니다.
- `index.html`, `details.html`, `drivelink.html`, `timetable.html`, `contact.html` 공통 내비게이션 우측에 라이트/다크 모드 전환 버튼을 추가했습니다.
- 선택한 테마는 `localStorage(todo.theme)`에 저장되어 모든 페이지에서 동일하게 유지됩니다.
- favicon, Apple Touch Icon, Open Graph/Twitter 이미지 메타는 기존 충북교육청 로고 자산을 유지합니다. 페이지 본문에는 로고 이미지를 사용하지 않습니다.


## 2026-06-12 추가 업데이트 — 내 Action 필터와 메모 색상
- 내 Action 페이지의 내 보기 설정은 선택한 담당자와 직접 관련된 Action Item만 보여주도록 정밀화했습니다.
- 관련 기준은 Action Item 담당, 협업기관, 회신 대기 대상입니다. 주요 과제 책임자만 같다는 이유로 관련 없는 Action Item이 노출되지 않도록 조정했습니다.
- Action Item 메모는 작성자별 고유 색상으로 표시됩니다. NSD는 밝은 회색, 네이버는 녹색, 업스테이지는 보라, 세종대는 크림슨, 교육청은 노랑 기준입니다.


## UI 개선 — 드롭다운 디자인 통일

- 모든 페이지의 기본 브라우저 select UI를 공통 커스텀 드롭다운으로 대체했습니다.
- 원본 `<select>`는 데이터 연동용으로 유지하여 기존 Firebase 저장/필터 로직과 호환됩니다.
- 라이트/다크 모드에서 드롭다운 버튼, 메뉴, 선택 옵션 색상이 일관되게 보이도록 CSS 변수를 정리했습니다.
- 네이버는 녹색, 업스테이지는 보라, 세종대는 크림슨, NSD는 밝은 회색 계열로 드롭다운 옵션 점 색상이 표시됩니다.

## 2026-06-12 — 페이지 본문 로고 제거 범위 확대

- `details.html`, `drivelink.html`, `timetable.html`, `contact.html`에 남아 있던 충북교육청 로고 `<img>` 표시를 제거했습니다.
- `assets/cbe-logo.png`는 favicon, apple-touch-icon, Open Graph/Twitter 메타 이미지 용도로만 유지합니다.
- 배포 점검 스크립트에 페이지 본문 로고 노출 금지 검사를 추가했습니다.


## 2026-06-12 — 페이지 본문 로고 제거 확정

- `details.html`, `drivelink.html`, `timetable.html`, `contact.html`의 헤더/Hero에서 `assets/cbe-logo.png` 이미지 태그를 제거했습니다.
- `assets/cbe-logo.png`는 favicon, Apple Touch Icon, Open Graph/Twitter Card 메타 이미지 용도로만 유지합니다.


## 2026-06-12 헤드라인 통일 및 본문 로고 제거 재검수

- details.html, drivelink.html, timetable.html의 상단 헤드라인을 내 Action(index.html) Hero 스타일과 같은 톤으로 통일했습니다.
- 페이지 본문에서는 충북교육청 로고 이미지를 사용하지 않도록 재검수했습니다. 로고는 favicon, apple-touch-icon, Open Graph/Twitter meta 이미지에만 사용합니다.
- drivelink.html Hero의 전체 링크 수가 파일 링크 요약과 함께 갱신되도록 보강했습니다.


## 2026-06-12 추가 정리 — 본문 로고 제거와 Hero 헤드라인 통일

- 충북교육청 로고 이미지는 페이지 본문, Header, Hero 영역에 노출하지 않습니다.
- 로고 자산은 favicon, apple-touch-icon, Open Graph/Twitter meta 이미지 용도로만 유지합니다.
- 5개 주요 페이지(index/details/drivelink/timetable/contact)의 첫 화면은 텍스트 기반 Hero 헤드라인과 우측 상태 카드 구조로 통일합니다.

## 2026-06-16 — 오픈 Firebase 운영 안전장치 일괄 반영

- Firebase/Auth 구조는 변경하지 않고, 180일 오픈 규칙 운영을 전제로 한 클라이언트 안전장치를 추가했습니다.
- `admin.html` 관리 도구를 추가했습니다.
  - 전체 DB JSON 백업
  - 노드별 백업(tasks, contacts, timetable_events, timetable_locations, meta, activity_logs)
  - 스키마 메타 갱신
  - 휴지통 항목 복구 / 완전 삭제
  - 활동 로그 확인
  - 작업자 라벨 저장
- `robots.txt`와 모든 HTML의 `noindex,nofollow,noarchive` 메타를 추가했습니다.
- `assets/app-config.js`, `assets/runtime-safety.js`, `assets/safety.css`를 추가해 공통 feature flag, read-only 모드, 입력 제한, URL 검증, 동기화 재연결 버튼을 관리합니다.
- 주요 과제, Action Item, Contact, 시간표 일정, 장소 태그, 링크 삭제를 즉시 삭제 대신 `deleted:true` 기반 soft delete로 변경했습니다.
- 메인/상세/파일/시간표/Contact 페이지의 목록 렌더링은 `deleted:true` 항목을 기본적으로 숨깁니다.
- Action 생성/완료/삭제, 주요 과제 삭제, Contact 삭제, 시간표 생성/수정/복제/삭제 등 주요 액션에 `activity_logs` 기록을 추가했습니다.
- 입력 길이 제한을 적용했습니다.
  - 주요 과제명 80자
  - Action Item 160자
  - 메모 500자
  - 링크 라벨 80자
  - 연락처 메모 300자
  - 시간표 제목 80자
  - 시간표 메모 300자
  - 장소명 60자
- 파일 링크는 `http://`, `https://`만 허용하도록 안전 URL 검증을 보강했습니다.
- Contact 페이지에 개인정보 운영 안내를 추가했습니다.
- Contact 페이지 숨김용 feature flag와 전체 read-only feature flag를 `app-config.js`에 추가했습니다.
- 운영 시간표에 장소 필터, 인쇄 버튼, 일정 복제 버튼, 시간 겹침 경고, 인쇄용 CSS를 추가했습니다.


## 2026-06-16 Contact CSS 복구

- contact.html에서 연락처 전용 CSS 블록이 누락되어 summary-card, panel, form-grid, contact-card, modal 등이 브라우저 기본 스타일로 보이는 문제를 수정했습니다.
- Contact 전용 layout/form/card/modal/usage-guide 스타일을 복구했습니다.
- soft delete 안내 문구를 현재 동작에 맞게 수정했습니다.
- class 사용/정의 정적 점검 결과, contact.html의 본문 주요 클래스 누락 0건을 확인했습니다.

## 2026-06-16 — 운영 시간표 데이터 표시 오류 수정

- `timetable.html`에서 장소 필터 상태 변수 `locationFilter`가 선언되지 않아 Firebase `timetable_events` 데이터가 있어도 일정 카드 렌더링이 중단될 수 있던 문제를 수정했습니다.
- 기본값을 `all`로 선언해 장소 필터가 초기화되기 전에도 전체 일정이 정상 표시되도록 했습니다.
- Firebase Rules, Auth, DB 구조, 실제 시간표 데이터는 변경하지 않았습니다.



## 2026-06-16 — Action Item 댓글/대댓글 스레드 추가

- `details.html`의 Action Item 댓글 영역을 댓글 → 대댓글 구조로 확장했습니다.
- DB 구조는 기존 `memos` 노드 아래 `replies` 하위 노드를 추가하는 방식으로 설계했습니다.
- 댓글/대댓글 작성자 색상은 기존 담당자 고유 색상을 그대로 사용합니다.
- 검색 대상에 댓글과 대댓글 텍스트를 모두 포함했습니다.
- 댓글/대댓글 삭제는 `deleted:true` soft delete 방식으로 처리합니다.
- `admin.html` 휴지통에서 댓글과 대댓글도 복구/완전 삭제할 수 있게 했습니다.

## 2026-06-16 관리 도구 업데이트

- 상세 관리 페이지 하단의 주요 과제 관리/삭제 영역을 관리 도구(`admin.html`)로 이동했습니다.
- 관리 도구에 주요 과제 관리/삭제 리스트와 전체 Action Item 리스트 관리 영역을 추가했습니다.
- 상세 관리 페이지는 주요 과제 상세 보기, 카드 내부 Action 추가, 댓글·대댓글, 링크 관리에 집중하도록 정리했습니다.
