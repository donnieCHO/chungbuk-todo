# 관리 도구 To Do 관리 영역 이동 리포트

## 변경 요약

- `details.html` 하단의 주요 과제 관리/삭제 전용 영역을 제거했습니다.
- `details.html` 주요 과제 카드의 직접 수정/삭제 버튼을 제거하고, 관리 도구 이동 링크로 대체했습니다.
- `admin.html`에 `주요 과제 관리/삭제` 영역을 추가했습니다.
- `admin.html`에 전체 `Action Item 리스트 관리` 영역을 추가했습니다.
- 주요 과제와 Action Item 수정 모달, soft delete, Action 완료/재개 기능을 관리 도구에 추가했습니다.

## Firebase 영향

- Firebase Rules/Auth 변경 없음
- DB 노드 추가 없음
- 기존 `tasks/{majorKey}/actions/{actionKey}` 구조 유지
- 삭제는 기존 운영 안전장치와 동일하게 `deleted:true` soft delete로 처리

## 관리 도구에서 가능한 작업

- 주요 과제 검색/카테고리 필터
- 주요 과제 수정
- 주요 과제 휴지통 이동
- Action Item 검색/주요 과제 필터
- Action Item 수정
- Action Item 완료/재개
- Action Item 휴지통 이동
