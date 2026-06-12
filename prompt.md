# 동일 구조 페이지 제작 프롬프트

아래 프롬프트를 새 대화에 붙여넣으면 현재와 같은 구조의 정적 Firebase 협업 웹앱을 다시 만들 수 있습니다.

---

## 프로젝트 입력값

```txt
프로젝트명: 충북교육청 AI 교원연수
영문/보조 타이틀: To Do List management sheet
기준일: 2026-08-12
일정: 2026년 8월 12~14일
장소: 세종대학교
담당자/기관: NSD, 네이버, 업스테이지, 세종대, 교육청
카테고리: 강의, 장소, 운영, 사후처리
DB: Firebase Realtime Database
배포: GitHub Pages
```

---

## 마스터 프롬프트

Firebase Realtime Database 기반 정적 협업 웹앱을 만들어줘. 빌드 도구 없이 GitHub Pages에 바로 배포 가능한 순수 HTML/CSS/JavaScript 파일 구조로 만들어줘.

### 파일 구조

```txt
index.html
  - details.html
  - drivelink.html
  - timetable.html
  - contact.html
  - dricelink.html
README.md
DEPLOYMENT_CHECKLIST.md
CHANGELOG.md
prompt.md
deployment_audit.py
```

### 공통 요구사항

- 한국어 UI
- 다크 테마
- Pretendard, DM Mono 사용
- Firebase SDK v10.12.0 CDN ESM 사용
- 우하단 동기화 상태 배지
- 첫 로딩 오버레이
- 사용자 입력을 `innerHTML`에 넣을 때 `escapeHtml` 처리
- 외부 링크는 `http/https`, 전화는 `tel:`, 이메일은 `mailto:` 사용
- 모든 inline handler 함수는 `window.*`로 노출
- UTF-8, BOM 없음, LF 줄바꿈
- 주석을 꼼꼼하게 작성

### 메인 `index.html`

첫 화면은 Hero page처럼 세련되게 구성해줘.

타이틀은 줄바꿈으로 표시:

```txt
충북교육청 AI 교원연수
To Do List management sheet
```

요구사항:

- D-Day를 크게 표시
- 완료율을 숫자 `%`와 가로형 막대로 표시
- 사용법 안내는 처음에는 펼쳐져 있고, 접기/펼치기 버튼 제공
- 본인이 해야 하는 Action Item 중심으로 표시
- 섹션: 지금 해야 할 일, 이번 주 Action, 완료된 Action. 확인/대기와 나중에 볼 일은 별도 리스트로 만들지 말고 상단 대시보드 지표로만 표시
- 완료된 Action은 기본 접힘 상태
- 완료된 Action 섹션 우측에 펼치기 버튼 배치
- 빠른 Action 추가 기능 제공
- 주요 과제별로 Action Item을 묶어서 표시

### DB 구조

```txt
tasks
└── {majorTaskKey}
    ├── title
    ├── description
    ├── cat
    ├── owner
    ├── priority
    ├── deadline
    ├── status
    ├── done
    └── actions
        └── {actionKey}
            ├── text
            ├── owner
            ├── agencies
            ├── priority
            ├── deadline
            ├── status
            ├── waitingFor
            ├── done
            ├── memos
            └── links
```

카테고리는 반드시 아래 고정값으로 선택하게 해줘.

```txt
강의
장소
운영
사후처리
```

기존 평면형 데이터가 있으면 `details.html`에서 카테고리별 주요 과제로 변환하는 패널을 제공해줘.

### `details.html`

- 상세 관리 페이지
- 카테고리 선택 방식으로 주요 과제 추가
- 카테고리별 섹션 아래 주요 과제 표시
- 주요 과제 안에 Action Item 추가
- 주요 과제 수정/삭제
- Action Item 수정/삭제/완료
- Action Item 단위 메모/링크 추가/삭제
- 기존 평면형 `tasks/{key}.text` 데이터를 2단계 구조로 변환하는 기능

### `drivelink.html`

- `tasks/{majorKey}/actions/{actionKey}/links`를 모아보기
- 기존 평면형 `tasks/{taskKey}/links`도 호환해서 표시
- 원본 파일 삭제가 아니라 DB의 링크 기록만 삭제한다는 안내 표시

### `timetable.html`

- 드래그로 일정 추가
- 일정 클릭으로 수정/삭제
- Firebase 노드: `timetable_events`
- 장소 태그 노드: `timetable_locations`
- 기본 장소: `군자관 4층`, `군자관 6층 식당`, `대양AI관 만찬장`
- 장소 태그 선택/추가/수정/삭제
- 세로 간격을 넉넉하게 해서 제목, 시간, 장소가 한눈에 보이게 구성

### `contact.html`

- 상단 메뉴에서 운영 시간표 다음에 `Contact` 메뉴로 연결
- Firebase 노드: `contacts`
- 담당자 연락처 추가/수정/삭제
- 필드: 이름, 소속, 담당 업무, 전화번호, 이메일, 메모
- 소속별 카드 그룹
- 전화번호는 `tel:`, 이메일은 `mailto:` 링크

### 문서와 점검

- README.md 최신화
- DEPLOYMENT_CHECKLIST.md 작성
- CHANGELOG.md 작성
- deployment_audit.py 작성
- 정적 점검 항목: 파일 존재, UTF-8, BOM 없음, HTML 메타, 중복 ID, 내부 링크, JS 문법, 필수 기능 문자열, 사용법 안내, 로컬 정적 서빙


## 추가 요구사항 — 주요 과제 / Action Item / due date 기준 정렬

동일 구조의 페이지를 만들 때 상세 관리 페이지는 반드시 다음 구조를 따른다.

- To Do 등록 영역은 `주요 과제 설정`과 `Action Item 등록`으로 분리한다.
- Action Item은 반드시 특정 주요 과제 내부에 저장한다.
- Action Item 등록 시 due date를 필수 입력으로 받는다.
- 저장 위치는 `tasks/{majorTaskKey}/actions/{actionKey}`이다.
- 화면 렌더링 시 각 주요 과제 내부 Action Item은 due date가 빠른 순서로 정렬한다.
- 주요 과제 정렬 기본값도 가장 임박한 미완료 Action Item due date 기준으로 한다.


## 공통 내비게이션 요구사항

모든 페이지의 공통 내비게이션은 같은 순서와 같은 pill 스타일을 사용한다.

```txt
내 Action → 상세 관리 → 파일 관리 → 운영 시간표 → Contact
```

`timetable.html`도 헤더 내부의 별도 이동 버튼을 쓰지 말고, 다른 페이지와 같은 sticky nav를 사용하며 `운영 시간표` 메뉴를 active 상태로 표시한다. 장소 관리처럼 페이지 내부에서만 쓰는 기능은 nav가 아니라 toolbar 버튼으로 분리한다.


## 동일 구조 생성 시 최신 요구사항

- 카테고리는 `강의`, `장소`, `운영`, `사후처리`로 고정한다.
- 주요 과제 아래에 Action Item을 등록하며 Action Item의 due date는 필수다.
- Action Item 등록 폼에는 `담당` 아래 `회신을 기다리는 곳` 태그 메뉴를 둔다. 태그는 NSD/네이버/업스테이지/세종대다.
- Action Item 등록 시 상태 선택은 두지 않는다. 새 항목은 기본 todo로 저장하고 완료 버튼으로만 done/status를 변경한다.
- 상세 관리 하단에는 주요 과제 목록을 보며 수정/삭제할 수 있는 임시 관리 영역을 둔다.


## 추가 요구사항 — 상세 관리 하단 주요 과제 삭제 관리

동일한 구조의 페이지를 만들 때 `details.html` 하단에는 반드시 `주요 과제 관리/삭제` 영역을 둔다.

요구사항:

- Action Item 목록과 별개로 주요 과제만 리스트로 보여준다.
- 각 주요 과제 행에는 카테고리, 책임자, 우선순위, Action 완료 수, 다음 due date, 진행률을 표시한다.
- 각 행에는 `상세 위치로 이동`, `수정`, `과제 삭제` 버튼을 둔다.
- `과제 삭제`는 Firebase `tasks/{majorTaskKey}`를 삭제하므로 내부 Action Item, 메모, 링크도 함께 삭제된다는 안내를 confirm 창에 표시한다.
- 삭제 오류 발생 시 sync 상태 배지에 오류를 표시하고, Firebase Rules 또는 네트워크 확인 안내를 alert로 보여준다.
- 이 영역은 접거나 숨기지 않고 상세 관리 페이지 맨 아래에 항상 보이도록 한다.

## 추가 요구사항 — 상세 관리 Step 2 UI

상세 관리 페이지의 Action Item 등록 영역은 다음 순서와 UI로 만든다.

1. 주요 과제 선택창
2. Action Item 입력 창 — 다른 입력보다 넓고 잘 보이게 표시
3. 담당 — NSD/네이버/업스테이지/세종대 태그 버튼 중 단일 선택
4. 회신을 기다리는 곳 — NSD/네이버/업스테이지/세종대 태그 버튼 복수 선택
5. 우선 순위
6. Due Date

전체 입력 영역은 네모형 카드/그리드로 정돈하고, 네이버는 녹색으로 표시한다.


## 추가 제작 지시 — 내 Action 대시보드 간소화

- `index.html`은 Hero 아래에 `전체 Action 현황` 대시보드 패널을 둔다.
- 대시보드 지표는 오늘·기한초과, 7일 이내, 회신 대기, 다음 마감으로 구성한다.
- 상세 리스트 섹션은 `지금 해야 할 일`, `이번 주 Action`, `완료된 Action`만 사용한다.
- `회신을 기다리는 곳`은 `details.html`과 같은 태그 버튼 UI로 구현한다.
- 완료 버튼은 원형 체크 아이콘과 작은 라벨을 분리해 라벨이 원형보다 과하게 커 보이지 않게 한다.
- `timetable.html`의 드래그 안내는 toolbar가 아니라 `운영 시간표 사용법` 영역의 첫 번째 카드에 넣고, 별도의 `보기 개선` 안내 문구는 넣지 않는다.


## UI 유지 규칙 — 완료 버튼

- 완료 버튼은 글자 없는 원형 체크만 표시한다.
- 버튼 안에 `완료`, `완료됨`, `완료 처리` 텍스트를 넣지 않는다.
- 사용법 안내에는 `왼쪽 원형 체크를 누르면 완료가 됩니다.` 문구를 넣는다.


## 로고와 favicon 요구사항

동일 구조의 페이지를 새로 만들 때는 아래 요구사항을 포함하세요.

- 로고 파일은 `assets/cbe-logo.png`로 저장한다.
- 모든 주요 HTML 페이지의 헤더 또는 Hero 영역에 로고를 표시한다.
- `favicon.ico`, `favicon-64.png`, `favicon-32.png`, `favicon-16.png`, `apple-touch-icon.png`를 생성한다.
- 모든 HTML 파일의 `<head>`에 favicon, theme-color, description, Open Graph, Twitter Card 메타를 넣는다.
- GitHub Pages 하위 경로 배포를 고려해 자산 경로는 상대 경로를 사용한다.

## 전역 테마 전환 요구사항

동일 구조의 페이지를 다시 만들 때는 모든 주요 페이지의 Global Navigation 오른쪽에 라이트/다크 모드 전환 버튼을 추가합니다. 테마 선택값은 `localStorage(todo.theme)`에 저장하고, `html[data-theme="light"]` / `html[data-theme="dark"]` CSS 변수로 화면 색상을 전환합니다. 내 Action Hero에는 로고 이미지를 노출하지 않고, favicon/meta에는 로고 자산을 사용할 수 있습니다.


## 2026-06-12 추가 업데이트 — 내 Action 필터와 메모 색상
- 내 Action 페이지의 내 보기 설정은 선택한 담당자와 직접 관련된 Action Item만 보여주도록 정밀화했습니다.
- 관련 기준은 Action Item 담당, 협업기관, 회신 대기 대상입니다. 주요 과제 책임자만 같다는 이유로 관련 없는 Action Item이 노출되지 않도록 조정했습니다.
- Action Item 메모는 작성자별 고유 색상으로 표시됩니다. NSD는 밝은 회색, 네이버는 녹색, 업스테이지는 보라, 세종대는 크림슨, 교육청은 노랑 기준입니다.
