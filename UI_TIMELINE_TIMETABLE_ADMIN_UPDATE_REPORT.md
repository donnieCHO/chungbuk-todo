# UI Timeline / Timetable / Admin Update Report

## 반영 사항

1. `index.html`
   - 내 Action 기본 담당자 필터를 `전체`로 변경해 최초 접속 시 데이터가 비어 보이는 상황을 줄였습니다.
   - `지금 해야 할 일`, `이번 주 Action` 외에 `전체 Action Timeline`을 추가해 due date가 먼 항목과 미정 항목도 날짜별로 확인할 수 있게 했습니다.
   - 검색 대상에 댓글/대댓글 텍스트를 포함했습니다.

2. `timetable.html`
   - 시간표 카드 표시를 `제목 - 장소 - 시간` 1줄 구조로 변경했습니다.
   - 긴 제목/장소는 말줄임표로 처리합니다.
   - 일정 클릭 시 기존 편집 모달에서 전체 상세 내용을 확인하고 수정할 수 있습니다.

3. `admin.html`
   - To Do 등록 폼 바로 아래에 전체 주요 과제 리스트와 전체 Action Item 리스트가 명확히 표시되도록 섹션명을 정리했습니다.
   - 백업/메타/휴지통/활동 로그 영역은 그 아래 운영 안전 도구 영역으로 정리했습니다.

## Firebase 영향

- Firebase Rules/Auth 변경 없음
- DB 노드 구조 변경 없음
- 기존 `tasks`, `timetable_events`, `timetable_locations` 구조 유지
