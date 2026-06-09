# 배포 전/후 점검 체크리스트

## A. 파일 구조

- [ ] 배포 루트에 `index.html`이 있다.
- [ ] 배포 루트에 `details.html`이 있다.
- [ ] 배포 루트에 `timetable.html`이 있다.
- [ ] 배포 루트에 `drivelink.html`이 있다.
- [ ] 오타 호환용 `dricelink.html`이 있다.
- [ ] 모든 내부 링크가 상대 경로로 연결되어 있다.

## B. 인코딩/언어/메타

- [ ] 모든 HTML/MD 파일이 UTF-8이다.
- [ ] BOM이 없다.
- [ ] 줄바꿈은 LF이다.
- [ ] 모든 HTML 파일에 `<!DOCTYPE html>`이 있다.
- [ ] 모든 HTML 파일에 `<html lang="ko">`가 있다.
- [ ] 모든 HTML 파일에 `<meta charset="UTF-8">`가 있다.
- [ ] 모든 HTML 파일에 viewport 메타가 있다.

## C. 페이지 이동

- [ ] `index.html → details.html` 이동이 된다.
- [ ] `index.html → timetable.html` 이동이 된다.
- [ ] `index.html → drivelink.html` 이동이 된다.
- [ ] `details.html → index.html` 이동이 된다.
- [ ] `details.html → drivelink.html` 이동이 된다.
- [ ] `details.html → timetable.html` 이동이 된다.
- [ ] `timetable.html → index/details/drivelink` 이동이 된다.
- [ ] `drivelink.html → index/details/timetable` 이동이 된다.
- [ ] `dricelink.html` 접근 시 `drivelink.html`로 이동한다.

## D. Firebase 연결

- [ ] 모든 HTML 파일의 `firebaseConfig`가 같은 프로젝트를 가리킨다.
- [ ] `index.html`, `details.html`, `drivelink.html`은 `tasks` 노드를 사용한다.
- [ ] `details.html`은 `contacts` 노드를 사용한다.
- [ ] `timetable.html`은 `timetable_events` 노드를 사용한다.
- [ ] `timetable.html`은 장소 태그 관리를 위해 `timetable_locations` 노드를 사용한다.
- [ ] 우하단 동기화 배지가 `연결 중 → 실시간 동기화 중`으로 바뀐다.
- [ ] 저장 실패 시 오류 상태가 표시된다.

## E. 주요 기능 수동 테스트

### index.html

- [ ] 담당자 탭이 정상 동작한다.
- [ ] 빠른 업무 추가가 된다.
- [ ] 업무 완료/미완료 토글이 된다.
- [ ] 업무 카드를 클릭하면 상세 모달이 열린다.
- [ ] 모달에서 상태 변경이 된다.
- [ ] 모달에서 메모 추가가 된다.
- [ ] 모달에서 링크 추가가 된다.

### details.html

- [ ] 카테고리/우선순위/날짜 임박순 보기 전환이 된다.
- [ ] 담당기관 필터가 된다.
- [ ] 업무 추가/수정/삭제가 된다.
- [ ] 링크 추가/삭제가 된다.
- [ ] 메모 추가/수정/삭제가 된다.
- [ ] 완료된 항목 섹션 접기/펼치기가 된다.
- [ ] 연락처 추가/삭제가 된다.
- [ ] `details.html#ti-{taskKey}` 형태로 접근하면 해당 업무로 이동한다.

### timetable.html

- [ ] 빈 시간 칸 드래그로 새 일정 모달이 열린다.
- [ ] 일정 저장이 된다.
- [ ] 일정 클릭으로 수정 모달이 열린다.
- [ ] 일정 모달에서 장소 태그를 선택해 저장할 수 있다.
- [ ] 새 장소를 입력하면 장소 태그 목록에 추가된다.
- [ ] 장소 관리 모달에서 장소 이름 수정/삭제가 된다.
- [ ] 일정 삭제가 된다.
- [ ] 모바일 폭에서 일정 카드 위치가 어긋나지 않는다.

### drivelink.html

- [ ] To Do에 연결된 링크가 모아 보인다.
- [ ] 검색이 된다.
- [ ] 담당자 필터가 된다.
- [ ] 카테고리 필터가 된다.
- [ ] `?task={taskKey}` 파라미터로 특정 업무 링크만 볼 수 있다.
- [ ] 링크 삭제 시 원본 파일이 아니라 To Do의 링크만 제거된다.

## F. 보안/운영

- [ ] Firebase Realtime Database 규칙이 운영 목적에 맞게 설정되어 있다.
- [ ] 외부 공개 URL로 운영한다면 인증 또는 쓰기 제한을 검토했다.
- [ ] 파일 원본은 Firebase DB에 넣지 않고 외부 저장소 URL만 저장한다.
- [ ] 실제 개인정보가 들어가는 연락처는 공유 범위를 확인했다.
- [ ] 브라우저 콘솔에 치명적인 오류가 없다.

## G. 배포 후 확인

- [ ] 배포 URL에서 `index.html`이 기본으로 열린다.
- [ ] 새로고침해도 라우팅 문제가 없다.
- [ ] 모바일 사파리/크롬에서 폰트와 레이아웃이 깨지지 않는다.
- [ ] 다른 사용자 브라우저에서 실시간 동기화가 반영된다.
- [ ] 배포 URL을 QR 또는 짧은 링크로 공유할 준비가 되었다.
