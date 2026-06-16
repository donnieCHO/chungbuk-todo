/*
  Runtime safety helpers
  ----------------------
  Firebase를 오픈 규칙으로 일정 기간 운영할 때 필요한 클라이언트 측 안전장치입니다.
  이 파일은 보안 규칙을 대체하지 않습니다. 실수 방지, 검색 노출 감소, 복구 편의성을 높이는 보조 계층입니다.
*/
(function () {
  'use strict';

  const config = window.TODO_APP_CONFIG || {};
  const textLimits = config.textLimits || {};
  const readOnlyMessage = '현재 읽기 전용 모드입니다. app-config.js의 featureFlags.readOnlyMode를 확인해주세요.';

  function isReadOnly() {
    return Boolean(config.featureFlags && config.featureFlags.readOnlyMode);
  }

  function showReadOnlyMessage() {
    alert(readOnlyMessage);
  }

  function guardReadOnly() {
    if (!isReadOnly()) return false;
    showReadOnlyMessage();
    return true;
  }

  function limitText(value, max, label) {
    const text = String(value || '').trim();
    if (text.length > max) {
      alert(`${label}은 ${max}자 이내로 입력해주세요.`);
      return '';
    }
    return text;
  }

  function limitByType(value, type, label) {
    const max = textLimits[type] || 300;
    return limitText(value, max, label || type);
  }

  function safeExternalUrl(rawUrl) {
    let url = String(rawUrl || '').trim();
    if (!url) return '';
    if (!/^https?:\/\//i.test(url)) url = `https://${url}`;
    try {
      const parsed = new URL(url);
      if (!['http:', 'https:'].includes(parsed.protocol)) return '';
      return parsed.href;
    } catch (err) {
      return '';
    }
  }

  function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, ch => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[ch]));
  }

  function downloadJson(filename, data) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function timestampForFile(date = new Date()) {
    const pad = n => String(n).padStart(2, '0');
    return `${date.getFullYear()}${pad(date.getMonth() + 1)}${pad(date.getDate())}-${pad(date.getHours())}${pad(date.getMinutes())}`;
  }

  function actorLabel() {
    try {
      return localStorage.getItem('todo.actorLabel') || 'unknown';
    } catch (err) {
      return 'unknown';
    }
  }

  function setActorLabel(value) {
    try {
      localStorage.setItem('todo.actorLabel', String(value || '').trim() || 'unknown');
    } catch (err) {}
  }

  function recordSyncState(state, text) {
    const status = document.getElementById('syncStatus');
    if (!status) return;
    status.dataset.state = state || '';
    status.dataset.text = text || '';
    const last = status.querySelector('.sync-last');
    if (last && state === 'synced') {
      const now = new Date();
      last.textContent = ` · ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')} 동기화`;
    }
  }

  function enhanceSyncStatus() {
    const status = document.getElementById('syncStatus');
    if (!status || status.dataset.safetyEnhanced === '1') return;
    status.dataset.safetyEnhanced = '1';
    const last = document.createElement('span');
    last.className = 'sync-last';
    last.setAttribute('aria-hidden', 'true');
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'sync-refresh-btn';
    button.textContent = '다시 연결';
    button.title = '페이지를 새로고침해 Firebase 연결을 다시 시도합니다.';
    button.addEventListener('click', () => window.location.reload());
    status.appendChild(last);
    status.appendChild(button);
  }

  function applyFeatureFlags() {
    const flags = config.featureFlags || {};
    document.documentElement.toggleAttribute('data-readonly', Boolean(flags.readOnlyMode));
    document.querySelectorAll('[href="contact.html"]').forEach(el => {
      if (flags.showContactPage === false) el.style.display = 'none';
    });
    document.querySelectorAll('[href="admin.html"]').forEach(el => {
      if (flags.showAdminPage === false) el.style.display = 'none';
    });
    if (flags.readOnlyMode) {
      const banner = document.createElement('div');
      banner.className = 'safety-banner readonly-banner';
      banner.textContent = '읽기 전용 모드입니다. 추가, 수정, 삭제, 완료 처리가 비활성화됩니다.';
      document.body.prepend(banner);
    }
    if (location.pathname.endsWith('/contact.html') && flags.showContactPage === false) {
      document.body.innerHTML = '<main class="shell"><section class="panel"><h1>Contact 페이지 비공개</h1><p>현재 Contact 페이지는 feature flag에 의해 숨김 처리되었습니다.</p><p><a href="index.html">내 Action으로 이동</a></p></section></main>';
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    enhanceSyncStatus();
    applyFeatureFlags();
  });

  window.TodoSafe = Object.freeze({
    config,
    isReadOnly,
    guardReadOnly,
    showReadOnlyMessage,
    limitText,
    limitByType,
    safeExternalUrl,
    escapeHtml,
    downloadJson,
    timestampForFile,
    actorLabel,
    setActorLabel,
    recordSyncState,
    enhanceSyncStatus,
    applyFeatureFlags
  });
})();
