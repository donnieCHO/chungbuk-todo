# 오픈 Firebase 운영 안전 가이드

이 문서는 Firebase Realtime Database를 일정 기간 오픈 규칙으로 운영할 때, 코드와 운영 절차에서 실수를 줄이기 위한 가이드입니다.

## 핵심 전제

- URL 공유를 제한하더라도 기술적으로는 Firebase Rules가 허용하는 범위에서 접근이 가능합니다.
- 현재 배포본은 Auth를 추가하지 않았고, 기존 Firebase 설정을 유지합니다.
- 이 가이드는 보안 대체책이 아니라 운영 안전장치입니다.

## 매일 운영 전

1. `admin.html` 접속
2. 작업자 라벨 입력
3. 전체 백업 JSON 다운로드
4. 휴지통 항목 확인
5. 활동 로그 확인

## 대량 수정 전

1. 전체 백업 JSON 다운로드
2. 수정할 노드별 백업 다운로드
3. 수정 후 화면에서 확인
4. 문제가 있으면 Firebase Console에서 백업 JSON을 참고해 복구

## 삭제 정책

일반 페이지의 삭제는 바로 지우지 않고 `deleted:true`로 표시합니다.

```js
deleted: true
deletedAt: Date.now()
deletedBy: '작업자 라벨'
```

삭제된 항목은 일반 화면에서 숨겨지고, `admin.html`에서 복구 또는 완전 삭제할 수 있습니다.

## 행사 종료 후 권장

- `assets/app-config.js`에서 `readOnlyMode: true`로 변경해 UI상 수정 버튼을 차단합니다.
- Firebase Rules를 읽기 전용 또는 Auth 기반으로 전환하는 것을 권장합니다.
- Contact에 포함된 개인정보성 데이터는 보관 필요성이 없으면 삭제합니다.

## 검색 노출 방지

모든 HTML에는 `noindex,nofollow,noarchive` 메타가 들어 있으며, 루트에는 `robots.txt`가 포함되어 있습니다.

```txt
User-agent: *
Disallow: /
```

이 설정은 검색 노출을 줄이는 장치일 뿐, 접근 권한을 막는 보안 장치는 아닙니다.
