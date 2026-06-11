# 변경 이력

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
  - 강사커리큘럼
  - 장소시설
  - 운영물품
  - 사후처리

### Changed

- 드롭다운/select UI를 전역적으로 통일
- 주요 과제 추가/수정 시 카테고리를 직접 입력이 아닌 선택 방식으로 변경
- 기존 `강사·커리큘럼`, `장소·시설`, `운영·물품` 표기를 화면 기준 `강사커리큘럼`, `장소시설`, `운영물품`으로 정리
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
