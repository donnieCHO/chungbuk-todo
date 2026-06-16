# UI/Admin/Timeline Update Report

## 반영 사항

1. 상세관리 상단 To Do 등록 UI 제거
2. 관리 도구(admin.html)에 1단 세로형 주요 과제/Action Item 등록 UI 추가
3. 상세관리 카드 내부 Action Item 추가/메모/링크 관리 흐름 유지
4. 내 Action의 지금 해야 할 일/이번 주 Action을 due date 타임라인 형태로 렌더링
5. 운영 시간표 일정 카드에서 제목·장소 우선 표시, 시간은 작게 보조 표시

## Firebase 영향

- Firebase Rules/Auth 변경 없음
- 기존 `tasks`, `timetable_events`, `timetable_locations` 구조 유지
- 신규 DB 노드 없음

## 수동 확인 권장

- admin.html에서 주요 과제 추가
- admin.html에서 Action Item 추가
- details.html에서 주요 과제 카드 내부 Action 추가 및 메모 입력
- index.html에서 due date 기준 타임라인 표시 확인
- timetable.html에서 30분/1시간 일정 카드의 제목·장소 표시 확인
