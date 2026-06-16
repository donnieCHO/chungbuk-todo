/*
  App-wide configuration
  ----------------------
  - Firebase/Auth 구조를 변경하지 않고, 오픈 운영을 전제로 한 UI/안전장치 설정만 관리합니다.
  - 모든 페이지에서 동일한 프로젝트명, 담당자 색상, 카테고리, feature flag를 참조할 수 있도록 전역 객체로 노출합니다.
*/
window.TODO_APP_CONFIG = Object.freeze({
  appVersion: '2026.06.16-open-ops-safety',
  schemaVersion: 3,
  project: {
    id: 'chungbuk-ai-training2026',
    title: '충북교육청 AI 교원연수',
    targetDate: '2026-08-12',
    location: '세종대학교',
    period: '2026년 8월 12~14일 · 2박 3일'
  },
  featureFlags: {
    // 오픈 규칙 운영 중 실수 방지용입니다. true로 바꾸면 UI상 쓰기 버튼을 차단합니다.
    readOnlyMode: false,
    // 외부 공유용으로 Contact 페이지를 잠시 숨기고 싶을 때 false로 바꿉니다.
    showContactPage: true,
    // 운영 도구는 URL을 아는 운영자만 쓰는 것을 전제로 합니다.
    showAdminPage: true
  },
  entities: {
    ops: { label: 'NSD', color: '#e8ecf4' },
    naver: { label: '네이버', color: '#00c73c' },
    upstage: { label: '업스테이지', color: '#8b5cf6' },
    sejong: { label: '세종대', color: '#c3002f' },
    education: { label: '교육청', color: '#f5c842' }
  },
  categories: {
    curriculum: { label: '강의', icon: '🎓', color: '#7c6af7' },
    facility: { label: '장소', icon: '🏛️', color: '#3dd68c' },
    operation: { label: '운영', icon: '⚙️', color: '#f7a34f' },
    followup: { label: '사후처리', icon: '📊', color: '#f76f6f' }
  },
  textLimits: {
    majorTitle: 80,
    actionText: 160,
    memo: 500,
    linkLabel: 80,
    contactMemo: 300,
    timetableTitle: 80,
    timetableMemo: 300,
    locationLabel: 60
  },
  nodes: ['tasks', 'contacts', 'timetable_events', 'timetable_locations', 'meta', 'activity_logs']
});
