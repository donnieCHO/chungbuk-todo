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
- 기존 `강사·커리큘럼`, `장소·시설`, `운영·물품` 표기도 새 표기와 호환됩니다.

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
