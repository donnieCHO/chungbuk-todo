# UI Timeline / Timetable / Admin Update Report

## 반영 요약

1. `index.html` 내 Action 화면의 Action 표시 방식을 하나의 날짜별 Timeline으로 재정리했습니다.
   - 선택한 담당자 기준의 미완료 Action Item 전체를 due date 빠른 순서로 표시합니다.
   - 기존처럼 `지금 해야 할 일`/`이번 주` 조건에 걸리지 않아 빈 화면처럼 보이는 문제를 줄였습니다.
   - due date가 없는 항목은 `미정` 그룹으로 모읍니다.

2. `timetable.html` 일정 카드 표시를 한 줄 구조로 변경했습니다.
   - 표시 순서: 제목 · 장소 · 시간
   - 긴 제목/장소는 CSS ellipsis로 줄입니다.
   - 일정 클릭 시 기존 편집 모달을 `상세 일정 / 편집` 용도로 사용합니다.

3. `admin.html` 관리 도구 배열을 명확히 정리했습니다.
   - 1. To Do 등록
   - 2. 전체 주요 과제 리스트
   - 3. 전체 Action Item 리스트
   - 4. 백업
   - 5. 스키마 메타
   - 6. 휴지통 / 복구
   - 7. 활동 로그

## Firebase 영향

- Firebase Rules/Auth 변경 없음
- DB 구조 변경 없음
- 기존 `tasks`, `timetable_events`, `timetable_locations` 구조 유지

## 배포 전 확인

- `index.html`에서 담당자 필터를 바꾸면 Timeline에 해당 담당자 관련 Action이 날짜별로 보이는지 확인합니다.
- `timetable.html`에서 일정 카드가 한 줄로 `제목 · 장소 · 시간` 순서로 보이는지 확인합니다.
- `admin.html`에서 입력 폼 아래 주요 과제/Action Item 전체 리스트가 보이는지 확인합니다.
