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


## 로고와 favicon 점검

- [ ] `assets/cbe-logo.png`가 배포 루트 기준으로 존재하는지 확인
- [ ] `assets/favicon.ico`, `favicon-64.png`, `favicon-32.png`, `favicon-16.png`, `apple-touch-icon.png`가 존재하는지 확인
- [ ] `index.html`, `details.html`, `drivelink.html`, `timetable.html`, `contact.html` 본문/Header/Hero에 로고 이미지가 보이지 않는지 확인
- [ ] 브라우저 탭 favicon이 충북교육청 로고로 표시되는지 확인
- [ ] 카카오톡/메신저 공유 시 Open Graph 이미지가 노출되는지 확인

## 테마 전환 점검

- [ ] 공통 내비게이션 오른쪽에 `Light` / `Dark` 테마 전환 버튼이 보인다.
- [ ] `index.html`, `details.html`, `drivelink.html`, `timetable.html`, `contact.html`에서 동일하게 테마가 전환된다.
- [ ] 새로고침 후에도 마지막 선택 테마가 유지된다.
- [ ] 모든 주요 페이지 본문에는 로고 이미지가 보이지 않고, favicon은 정상 표시된다.


## 2026-06-12 추가 업데이트 — 내 Action 필터와 메모 색상
- 내 Action 페이지의 내 보기 설정은 선택한 담당자와 직접 관련된 Action Item만 보여주도록 정밀화했습니다.
- 관련 기준은 Action Item 담당, 협업기관, 회신 대기 대상입니다. 주요 과제 책임자만 같다는 이유로 관련 없는 Action Item이 노출되지 않도록 조정했습니다.
- Action Item 메모는 작성자별 고유 색상으로 표시됩니다. NSD는 밝은 회색, 네이버는 녹색, 업스테이지는 보라, 세종대는 크림슨, 교육청은 노랑 기준입니다.


## 드롭다운 UI 확인

배포 후 아래 페이지에서 드롭다운 메뉴가 기본 브라우저 UI로 보이지 않고 동일한 커스텀 UI로 열리는지 확인합니다.

```txt
index.html: 내 보기 설정, 주요 과제, 담당
details.html: 주요 과제 선택창, 우선순위, 필터, 수정 모달
drivelink.html: 담당자, 위치 필터
timetable.html: 일정 날짜 선택
contact.html: 소속 필터, 연락처 소속, 수정 모달
```

## 페이지 본문 로고 노출 금지

- [ ] HTML 본문에 `<img src="assets/cbe-logo.png">`가 남아 있지 않은지 확인
- [ ] `assets/cbe-logo.png`는 favicon, apple-touch-icon, OG/Twitter meta에서만 사용


## 2026-06-12 헤드라인 통일 및 본문 로고 제거 재검수

- details.html, drivelink.html, timetable.html의 상단 헤드라인을 내 Action(index.html) Hero 스타일과 같은 톤으로 통일했습니다.
- 페이지 본문에서는 충북교육청 로고 이미지를 사용하지 않도록 재검수했습니다. 로고는 favicon, apple-touch-icon, Open Graph/Twitter meta 이미지에만 사용합니다.
- drivelink.html Hero의 전체 링크 수가 파일 링크 요약과 함께 갱신되도록 보강했습니다.


## 2026-06-12 추가 정리 — 본문 로고 제거와 Hero 헤드라인 통일

- 충북교육청 로고 이미지는 페이지 본문, Header, Hero 영역에 노출하지 않습니다.
- 로고 자산은 favicon, apple-touch-icon, Open Graph/Twitter meta 이미지 용도로만 유지합니다.
- 5개 주요 페이지(index/details/drivelink/timetable/contact)의 첫 화면은 텍스트 기반 Hero 헤드라인과 우측 상태 카드 구조로 통일합니다.

---

## 오픈 Firebase 운영 안전장치 점검

- [ ] `admin.html`이 배포 루트에 포함되어 있는가?
- [ ] `robots.txt`가 배포 루트에 포함되어 있는가?
- [ ] `assets/app-config.js`, `assets/runtime-safety.js`, `assets/safety.css`가 업로드되어 있는가?
- [ ] 모든 HTML에 `noindex,nofollow,noarchive` 메타가 들어 있는가?
- [ ] 내비게이션에 `관리 도구` 링크가 표시되는가?
- [ ] `admin.html`에서 전체 백업 JSON이 다운로드되는가?
- [ ] 주요 과제 삭제 후 일반 화면에서는 숨겨지고, 관리 도구 휴지통에는 표시되는가?
- [ ] 휴지통에서 복구하면 일반 화면에 다시 표시되는가?
- [ ] 휴지통에서 완전 삭제하면 Firebase 경로가 제거되는가?
- [ ] 활동 로그가 생성되는가?
- [ ] Contact 페이지에 개인정보 운영 안내가 표시되는가?
- [ ] 시간표에서 장소 필터, 인쇄 버튼, 일정 복제, 겹침 경고가 동작하는가?


## 댓글 / 대댓글 점검

- [ ] `details.html`에서 Action Item에 댓글을 추가할 수 있다.
- [ ] 각 댓글 아래에서 대댓글을 추가할 수 있다.
- [ ] 댓글과 대댓글이 담당자 고유 색상으로 표시된다.
- [ ] 검색어가 댓글/대댓글 텍스트에도 반응한다.
- [ ] 댓글/대댓글 삭제 시 일반 화면에서 사라지고 `admin.html` 휴지통에서 확인된다.

## 2026-06-16 관리 도구 업데이트

- 상세 관리 페이지 하단의 주요 과제 관리/삭제 영역을 관리 도구(`admin.html`)로 이동했습니다.
- 관리 도구에 주요 과제 관리/삭제 리스트와 전체 Action Item 리스트 관리 영역을 추가했습니다.
- 상세 관리 페이지는 주요 과제 상세 보기, 카드 내부 Action 추가, 댓글·대댓글, 링크 관리에 집중하도록 정리했습니다.
