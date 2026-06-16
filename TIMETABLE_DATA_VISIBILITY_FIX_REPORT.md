# 운영 시간표 데이터 표시 문제 수정 리포트

## 문제

최신 패키지의 `timetable.html`에서 `locationFilter` 상태 변수가 선언되지 않은 상태로 사용되고 있었습니다.

문제가 발생하는 흐름은 다음과 같습니다.

```txt
Firebase timetable_events 데이터 수신
→ renderEvents() 실행
→ locationFilter 참조
→ ReferenceError 발생
→ 일정 카드 렌더링 중단
```

따라서 Firebase의 `timetable_events` 데이터가 실제로 삭제된 것이 아니라, 화면 렌더링이 중단되어 **모두 삭제된 것처럼 보일 수 있는 상태**였습니다.

## 수정

`timetable.html`의 상태 변수 선언부에 아래 기본값을 추가했습니다.

```js
let locationFilter = 'all';
```

기본값을 `all`로 두어 장소 필터가 아직 선택되지 않았을 때도 모든 일정이 정상 렌더링됩니다.

## Firebase 영향

이번 수정은 화면 렌더링 오류 수정입니다.

```txt
Firebase Rules 변경 없음
Firebase Auth 변경 없음
Realtime Database 구조 변경 없음
timetable_events 데이터 삭제/변경 없음
```

## 배포 후 확인

```txt
1. timetable.html 접속
2. 기존 일정 카드가 표시되는지 확인
3. 장소 필터가 전체 장소로 표시되는지 확인
4. 장소 필터를 바꿨다가 전체 장소로 되돌려도 일정이 정상 표시되는지 확인
5. 새 일정 추가/수정/삭제가 정상 동작하는지 확인
```
