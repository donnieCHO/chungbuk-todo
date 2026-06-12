# 코드 검수 리포트

## 대상 파일

```txt
index.html
details.html
drivelink.html
timetable.html
contact.html
dricelink.html
README.md
DEPLOYMENT_CHECKLIST.md
CHANGELOG.md
prompt.md
deployment_audit.py
```

## 검수 요약

이번 검수에서는 사용자가 요청한 화면/구조 개편을 기준으로 전체 파일을 다시 확인했습니다.

| 항목 | 결과 |
|---|---|
| 메인 히어로 디자인 | 반영 |
| D-Day 대형 표시 | 반영 |
| 완료율 숫자 + 가로 막대 | 반영 |
| 사용법 기본 펼침 + 접기 버튼 | 반영 |
| 완료 Action 기본 접힘 | 반영 |
| 카테고리 고정값 | 반영 |
| 주요 과제 → Action Item 2단계 구조 | 유지/보강 |
| 드롭다운 UI 통일 | 반영 |
| Contact 별도 페이지 | 신규 추가 |
| 운영 시간표 내비게이션 통일 | 반영 |
| Firebase 노드 문서화 | 반영 |
| 정적 배포 점검 | 통과 |

## 주요 변경 파일

### index.html

- 첫 화면을 Hero page 스타일로 개편했습니다.
- 타이틀을 `충북교육청 AI 교원연수` / `To Do List management sheet` 줄바꿈 구조로 변경했습니다.
- D-Day와 전체 완료율을 우측 히어로 카드에서 크게 표시합니다.
- 완료율은 숫자 `%`와 가로형 진행 막대를 함께 제공합니다.
- 사용법 안내는 기본 펼침 상태이며 버튼으로 닫을 수 있습니다.
- 완료된 Action Item 섹션은 기본 접힘 상태입니다.
- 카테고리명 정규화 헬퍼를 추가했습니다.
- 기존 `강의`, `장소`, `운영` 표기도 새 표기와 호환됩니다.

### details.html

- 주요 과제 입력의 카테고리를 텍스트 입력에서 드롭다운 선택으로 변경했습니다.
- 주요 과제를 카테고리 섹션별로 묶어 표시합니다.
- 카테고리 고정값을 적용했습니다.
- 기존 데이터의 카테고리 표기를 새 표기로 정규화하는 헬퍼를 추가했습니다.

### contact.html

- 신규 페이지입니다.
- Firebase `contacts` 노드를 사용합니다.
- 연락처 추가, 수정, 삭제를 지원합니다.
- 소속별 그룹과 검색/필터를 제공합니다.
- 전화번호와 이메일은 각각 `tel:`, `mailto:` 링크로 연결됩니다.

### timetable.html

- 기존 장소 태그 기능과 세로 간격 개선을 유지했습니다.
- 헤더 안에 따로 있던 이동 버튼을 제거하고, 다른 페이지와 동일한 공통 sticky nav를 적용했습니다.
- 메뉴 순서는 `내 Action → 상세 관리 → 파일 관리 → 운영 시간표 → Contact`로 통일했습니다.
- 현재 페이지인 `운영 시간표` 메뉴는 active 상태로 표시됩니다.
- 장소 관리 버튼은 페이지 이동 메뉴가 아니라 toolbar 액션 버튼으로 분리했습니다.
- 드롭다운 UI 스타일을 통일했습니다.

### drivelink.html

- 상단 메뉴에 `Contact` 링크를 추가했습니다.
- 드롭다운 UI 스타일을 통일했습니다.

## 보안/안정성 확인

- 사용자 입력 출력부는 `escapeHtml` 계열 처리를 사용합니다.
- 외부 파일 링크는 DB에 저장된 URL 기록만 삭제하며 원본 파일은 삭제하지 않습니다.
- Firebase 실제 접근 권한은 Realtime Database Rules에서 제어해야 합니다.
- 개인정보가 포함될 수 있는 `contacts` 노드는 운영 전 보안 규칙을 반드시 확인해야 합니다.

## 남은 수동 확인

정적 점검은 통과했지만, 아래 항목은 배포 후 브라우저에서 Firebase 실제 연결 상태로 확인해야 합니다.

```txt
index.html: 빠른 Action 추가 / 완료 전환

details.html: 주요 과제 추가 / Action 추가 / 메모 / 링크

drivelink.html: 링크 모아보기

timetable.html: 일정 및 장소 태그 저장

contact.html: 연락처 추가 / 수정 / 삭제
```


## Action due date 검수

- `details.html`의 To Do 등록 UI가 주요 과제 설정과 Action Item 등록으로 분리되었습니다.
- Action Item 등록 시 due date 미입력 저장을 차단합니다.
- `sortedActionsForMajor()`와 `majorNextDueDate()`로 상세/메인 화면의 정렬 기준을 일관화했습니다.


## 추가 검수: 카테고리/회신 태그/완료 UI

- 카테고리 표시와 선택값을 `강의`, `장소`, `운영`, `사후처리`로 정리했습니다.
- Action Item 상태 선택 UI를 등록/수정 폼에서 제거하고 완료 버튼 중심 UX로 단순화했습니다.
- 회신 대기 대상은 텍스트 입력 대신 태그 선택 버튼으로 통일했습니다.
- 완료 버튼은 `완료 처리` 문구 없이 원형 체크만 보이는 형태로 정리했습니다. 동작 설명은 사용법 안내에 분리했습니다.


## 추가 검수: 주요 과제 관리/삭제

- `details.html` 하단에 Action Item을 펼치지 않는 주요 과제 전용 관리 리스트를 명확히 배치했습니다.
- 리스트 행에는 주요 과제명, 카테고리, 책임자, 우선순위, Action 완료 수, 다음 due date, 진행률이 표시됩니다.
- 각 주요 과제는 `상세 위치로 이동`, `수정`, `과제 삭제` 버튼을 제공합니다.
- `deleteMajorTask()`는 삭제 전 삭제 범위와 되돌릴 수 없음을 확인창으로 안내합니다.
- 삭제 실패 시 동기화 배지를 `삭제 오류`로 변경하고 사용자에게 Firebase 권한/네트워크 확인을 안내합니다.

## 추가 검수 — Action Item 등록 UI

- 상세 관리 페이지 Step 2의 입력 순서와 시각적 그리드를 재검수했습니다.
- 담당 선택 로직은 `selectedOwner()`와 `selectOwnerTag()`로 단일 선택되도록 구성했습니다.
- 회신 대기 선택 로직은 기존 `selectedWaitingFor()` 복수 선택 방식을 유지했습니다.
- 네이버는 `--naver:#00c73c` 기반 녹색 태그로 통일했습니다.


## 내 Action 대시보드 간소화 검수

- 메인 화면의 회신 대기 태그 버튼 스타일을 상세 관리 페이지와 동일 계열로 맞췄습니다.
- 확인/대기 및 나중에 볼 일은 목록 섹션으로 분리하지 않고, 대시보드 지표로만 확인하도록 정리했습니다.
- 완료 버튼은 원형 체크 아이콘과 작은 텍스트 라벨로 분리해 텍스트 크기 문제를 완화했습니다.
- 시간표의 드래그 안내는 사용법 카드 안으로 이동했고, toolbar에는 장소 관리 버튼만 남겼습니다.


## 로고/메타 검수

- `assets/cbe-logo.png`를 기준 로고 파일로 추가했습니다.
- 모든 주요 HTML 파일에 favicon, Apple Touch Icon, Open Graph, Twitter Card 메타를 추가했습니다.
- 최신 기준으로 각 페이지의 Header/Hero 본문 로고 표시는 제거했습니다.
- 로고 경로는 GitHub Pages 하위 경로에서도 동작하도록 상대 경로를 사용합니다.

## Theme Toggle Review

- 공통 내비게이션에 라이트/다크 모드 버튼을 추가했습니다.
- 테마 적용은 CSS 변수 오버라이드 방식으로 처리해 Firebase 데이터 구조와 CRUD 로직을 변경하지 않았습니다.
- 모든 주요 페이지 본문/헤더/Hero의 로고 이미지는 제거했으며, favicon/meta 자산은 유지했습니다.


## 2026-06-12 추가 업데이트 — 내 Action 필터와 메모 색상
- 내 Action 페이지의 내 보기 설정은 선택한 담당자와 직접 관련된 Action Item만 보여주도록 정밀화했습니다.
- 관련 기준은 Action Item 담당, 협업기관, 회신 대기 대상입니다. 주요 과제 책임자만 같다는 이유로 관련 없는 Action Item이 노출되지 않도록 조정했습니다.
- Action Item 메모는 작성자별 고유 색상으로 표시됩니다. NSD는 밝은 회색, 네이버는 녹색, 업스테이지는 보라, 세종대는 크림슨, 교육청은 노랑 기준입니다.


## UI 코드 검수 — 드롭다운 컴포넌트

- 기본 브라우저 select가 OS별로 다르게 노출되는 문제를 줄이기 위해 공통 커스텀 드롭다운 레이어를 추가했습니다.
- 기존 `<select>`는 숨김 처리만 하고 제거하지 않아 기존 `document.getElementById(...).value`, `onchange`, Firebase 저장 로직이 그대로 동작합니다.
- 동적으로 option이 채워지는 select는 MutationObserver와 주기적 동기화로 표시값을 갱신합니다.
- 메뉴 외부 클릭과 ESC 키로 닫히도록 처리했습니다.

## 본문 로고 노출 검수

- `assets/cbe-logo.png`는 favicon/meta 자산으로만 유지합니다.
- 주요 HTML 페이지의 본문에는 `assets/cbe-logo.png`를 사용하는 `<img>` 태그가 남아 있지 않도록 점검했습니다.


## 본문 로고 이미지 미노출 검수

- `assets/cbe-logo.png`는 favicon/meta 용도로만 유지합니다.
- HTML 본문에는 `<img src="assets/cbe-logo.png">`가 남지 않도록 전수 검색했습니다.


## 2026-06-12 헤드라인 통일 및 본문 로고 제거 재검수

- details.html, drivelink.html, timetable.html의 상단 헤드라인을 내 Action(index.html) Hero 스타일과 같은 톤으로 통일했습니다.
- 페이지 본문에서는 충북교육청 로고 이미지를 사용하지 않도록 재검수했습니다. 로고는 favicon, apple-touch-icon, Open Graph/Twitter meta 이미지에만 사용합니다.
- drivelink.html Hero의 전체 링크 수가 파일 링크 요약과 함께 갱신되도록 보강했습니다.
