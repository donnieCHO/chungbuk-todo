# Action Item 댓글/대댓글 스레드 업데이트 리포트

## 변경 범위

- `details.html` 댓글 UI를 댓글 → 대댓글 스레드 구조로 변경
- Firebase DB 구조 확장: `memos/{memoKey}/replies/{replyKey}`
- 댓글/대댓글 작성자별 색상 유지
- 댓글/대댓글 검색 포함
- 대댓글 추가/삭제 함수 추가
- `admin.html` 휴지통 수집 대상에 댓글/대댓글 추가
- README, CHANGELOG, DEPLOYMENT_CHECKLIST, prompt 문서 갱신

## DB 구조

```txt
tasks/{majorKey}/actions/{actionKey}/memos/{memoKey}
  writer
  text
  ts
  replies/{replyKey}
    writer
    text
    ts
```

삭제는 기존 운영 안전장치에 맞춰 `deleted:true`, `deletedAt`, `deletedBy` 필드로 처리합니다.
