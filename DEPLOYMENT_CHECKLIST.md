# 배포 전 체크리스트

## 1. 파일 구조

- [ ] `index.html` 존재
- [ ] `details.html` 존재
- [ ] `drivelink.html` 존재
- [ ] `timetable.html` 존재
- [ ] `contact.html` 존재
- [ ] `dricelink.html` 존재
- [ ] `README.md`, `DEPLOYMENT_CHECKLIST.md`, `CHANGELOG.md`, `prompt.md` 포함

## 2. 메인 화면 UI

- [ ] 첫 화면 타이틀이 `충북교육청 AI 교원연수` / `To Do List management sheet` 줄바꿈으로 표시됨
- [ ] D-Day가 우측에서 크게 보임
- [ ] 전체 완료율이 숫자 `%`와 가로형 막대로 표시됨
- [ ] 사용법 안내가 처음에는 펼쳐져 있고, 버튼으로 접고 펼칠 수 있음
- [ ] 완료된 Action Item 섹션이 기본 접힘 상태임
- [ ] 완료된 Action Item 섹션 우측 버튼으로 펼치기/접기가 가능함

## 3. 2단계 To Do 구조

- [ ] `details.html`에서 카테고리를 선택할 수 있음
- [ ] 카테고리 값이 `강의`, `장소`, `운영`, `사후처리`로 고정됨
- [ ] 카테고리 아래에 주요 과제가 묶여 보임
- [ ] 주요 과제 안에 Action Item을 추가할 수 있음
- [ ] Action Item 완료/수정/삭제가 가능함
- [ ] Action Item 단위 메모/링크가 가능함
- [ ] 기존 평면형 데이터 변환 패널이 필요 시 표시됨
- [ ] 상세 관리 하단에 `주요 과제 관리/삭제` 리스트가 표시됨
- [ ] 하단 리스트에서 주요 과제 `수정`이 가능함
- [ ] 하단 리스트에서 주요 과제 `과제 삭제`가 가능함
- [ ] 주요 과제 삭제 전 내부 Action Item까지 삭제된다는 확인창이 표시됨

## 4. 페이지 연결

- [ ] 모든 페이지에서 `index.html`로 이동 가능
- [ ] 모든 페이지에서 `details.html`로 이동 가능
- [ ] 모든 페이지에서 `drivelink.html`로 이동 가능
- [ ] 모든 페이지에서 `timetable.html`로 이동 가능
- [ ] 운영 시간표 다음 메뉴로 `contact.html`이 표시됨
- [ ] `timetable.html`도 다른 페이지와 같은 공통 sticky nav 스타일로 표시됨
- [ ] `timetable.html`에서 `운영 시간표` 메뉴가 active 상태로 표시됨
- [ ] `dricelink.html`은 `drivelink.html`로 이동함

## 5. Contact 페이지

- [ ] `contact.html`에서 연락처 목록이 보임
- [ ] 담당자 이름/소속/담당 업무/전화번호/이메일/메모를 추가할 수 있음
- [ ] 연락처 수정이 가능함
- [ ] 연락처 삭제가 가능함
- [ ] 전화번호는 `tel:` 링크로 열림
- [ ] 이메일은 `mailto:` 링크로 열림

## 6. 시간표

- [ ] 빈 칸 드래그로 일정 추가 가능
- [ ] 일정 클릭으로 수정/삭제 가능
- [ ] 장소 태그 선택 가능
- [ ] 기본 장소 태그가 보임: `군자관 4층`, `군자관 6층 식당`, `대양AI관 만찬장`
- [ ] 장소 태그 추가/수정/삭제 가능
- [ ] 시간표 세로 간격이 제목/시간/장소를 읽기에 충분함

## 7. Firebase

- [ ] 모든 HTML의 `firebaseConfig`가 같은 프로젝트를 바라봄
- [ ] Realtime Database가 생성되어 있음
- [ ] `tasks` 읽기/쓰기 가능
- [ ] `contacts` 읽기/쓰기 가능
- [ ] `timetable_events` 읽기/쓰기 가능
- [ ] `timetable_locations` 읽기/쓰기 가능

## 8. 정적 배포 점검

- [ ] UTF-8 인코딩
- [ ] BOM 없음
- [ ] LF 줄바꿈
- [ ] HTML `DOCTYPE`, `lang="ko"`, `charset="UTF-8"`, `viewport` 확인
- [ ] 중복 ID 없음
- [ ] JavaScript 문법 오류 없음
- [ ] 내부 링크 깨짐 없음
- [ ] `python3 deployment_audit.py` 결과 PASS

## 9. 배포 후 브라우저 수동 테스트

- [ ] `index.html`에서 빠른 Action 추가 후 Firebase에 저장됨
- [ ] `details.html`에서 같은 Action Item 확인 가능
- [ ] `details.html`에서 메모/링크 추가 가능
- [ ] `drivelink.html`에서 추가한 링크가 보임
- [ ] `timetable.html`에서 일정과 장소 태그가 저장됨
- [ ] `contact.html`에서 연락처 추가/수정/삭제가 저장됨
- [ ] 다른 브라우저나 다른 기기에서 실시간 반영됨


## Action Item due date 정렬 수동 테스트

- [ ] details.html에서 주요 과제를 새로 추가한다.
- [ ] 상단 Action Item 등록 폼에서 주요 과제를 선택하고 due date를 입력해 저장한다.
- [ ] 같은 주요 과제에 due date가 더 빠른 Action Item을 추가했을 때 카드 내부에서 위로 올라오는지 확인한다.
- [ ] index.html에서도 가장 임박한 Action Item이 먼저 보이는지 확인한다.
- [ ] due date를 입력하지 않으면 저장이 막히는지 확인한다.


## 추가 수동 점검 - 카테고리/회신 태그 개선

- [ ] 상세 관리에서 카테고리가 `강의`, `장소`, `운영`, `사후처리`로 보이는지 확인
- [ ] Action Item 등록 폼에서 상태 선택이 사라졌는지 확인
- [ ] `회신을 기다리는 곳`에서 NSD/네이버/업스테이지/세종대 태그를 선택해 저장되는지 확인
- [ ] 저장된 Action Item이 due date 빠른 순서로 바로 정렬되는지 확인
- [ ] 왼쪽 원형 체크 버튼을 눌렀을 때 완료 상태로 전환되는지 확인
- [ ] 상세 페이지 하단 `주요 과제 관리/삭제`에서 주요 과제만 모아 보이는지 확인
- [ ] 하단 리스트에서 `상세 위치로 이동`, `수정`, `과제 삭제`가 가능한지 확인

## 추가 점검 — Action Item 등록 UI

- [ ] `details.html` Step 2에서 주요 과제 선택창이 정상 표시되는지 확인
- [ ] Action Item 입력 창이 2열 그리드에서 넓고 명확하게 보이는지 확인
- [ ] 담당 태그에서 NSD/네이버/업스테이지/세종대 중 1개만 선택되는지 확인
- [ ] 회신을 기다리는 곳 태그에서 복수 선택이 가능한지 확인
- [ ] 네이버 태그가 녹색으로 표시되는지 확인
- [ ] Due Date 입력 후 저장하면 마감 임박순으로 정렬되는지 확인


## 내 Action 대시보드 간소화 확인

- [ ] `index.html` 상단에 `전체 Action 현황` 대시보드가 보이는지 확인
- [ ] `확인/대기 중`, `나중에 볼 일` 리스트 섹션이 노출되지 않는지 확인
- [ ] 빠른 Action 추가의 `회신을 기다리는 곳` 태그가 상세 관리와 같은 스타일로 보이는지 확인
- [ ] 완료 버튼에 텍스트 라벨이 노출되지 않고 원형 체크만 보이는지 확인
- [ ] `timetable.html`의 드래그 안내가 toolbar가 아니라 `운영 시간표 사용법` 안에 보이는지 확인
- [ ] 시간표 사용법에서 `보기 개선` 문구가 보이지 않는지 확인
