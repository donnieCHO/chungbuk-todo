/*
  Global custom select/dropdown UI
  --------------------------------
  - 모든 native <select>를 동일한 디자인의 커스텀 드롭다운으로 보여줍니다.
  - 실제 값은 원본 select에 그대로 저장하므로 기존 onchange, Firebase 저장 로직은 그대로 동작합니다.
  - JS가 실패해도 원본 select는 남아 있으므로 기능 복구가 가능한 progressive enhancement 구조입니다.
*/
(function () {
  'use strict';

  const SELECTOR = 'select:not([data-native-select])';
  const ENHANCED = 'data-ui-select-enhanced';
  const cssEscape = window.CSS && typeof window.CSS.escape === 'function'
    ? window.CSS.escape
    : value => String(value).replace(/[^a-zA-Z0-9_-]/g, match => `\\${match}`);
  const menus = new Map();
  let activeSelect = null;
  let syncTimer = null;

  function textOfOption(option) {
    return option ? option.textContent.trim() : '';
  }

  function getSelectLabel(select) {
    const option = select.options[select.selectedIndex];
    return textOfOption(option) || select.getAttribute('aria-label') || select.getAttribute('placeholder') || '선택';
  }

  function closeActive() {
    if (!activeSelect) return;
    const wrap = getWrapper(activeSelect);
    const menu = menus.get(activeSelect);
    if (wrap) wrap.classList.remove('open');
    if (menu) {
      menu.classList.remove('open');
      menu.innerHTML = '';
      menu.removeAttribute('style');
    }
    const button = wrap ? wrap.querySelector('.ui-select-trigger') : null;
    if (button) button.setAttribute('aria-expanded', 'false');
    activeSelect = null;
  }

  function getWrapper(select) {
    const id = select.dataset.uiSelectId;
    return id ? document.querySelector(`.ui-select[data-select-id="${cssEscape(id)}"]`) : null;
  }

  function syncSelect(select) {
    const wrap = getWrapper(select);
    if (!wrap) return;
    const button = wrap.querySelector('.ui-select-trigger');
    const value = wrap.querySelector('.ui-select-value');
    if (!button || !value) return;
    value.textContent = getSelectLabel(select);
    const hasValue = Boolean(select.value);
    wrap.classList.toggle('ui-select-placeholder', !hasValue);
    wrap.classList.toggle('ui-select-disabled', Boolean(select.disabled));
    button.disabled = Boolean(select.disabled);
    button.setAttribute('aria-label', `${select.labels && select.labels[0] ? select.labels[0].textContent.trim() + ': ' : ''}${value.textContent}`);
  }

  function syncAll() {
    document.querySelectorAll(SELECTOR).forEach(select => {
      if (select.getAttribute(ENHANCED) === 'true') syncSelect(select);
      else enhanceSelect(select);
    });
  }

  function buildMenu(select) {
    const menu = menus.get(select);
    if (!menu) return;
    menu.innerHTML = '';
    Array.from(select.options).forEach((option, index) => {
      const item = document.createElement('button');
      item.type = 'button';
      item.className = 'ui-select-option';
      item.setAttribute('role', 'option');
      item.dataset.value = option.value;
      item.dataset.index = String(index);
      item.textContent = textOfOption(option);
      if (option.selected) item.classList.add('selected');
      if (option.disabled) {
        item.disabled = true;
        item.classList.add('disabled');
        item.setAttribute('aria-disabled', 'true');
      }
      item.addEventListener('click', () => {
        if (option.disabled) return;
        select.selectedIndex = index;
        select.dispatchEvent(new Event('input', { bubbles: true }));
        select.dispatchEvent(new Event('change', { bubbles: true }));
        syncSelect(select);
        closeActive();
      });
      menu.appendChild(item);
    });
  }

  function positionMenu(select) {
    const wrap = getWrapper(select);
    const menu = menus.get(select);
    if (!wrap || !menu) return;
    const button = wrap.querySelector('.ui-select-trigger');
    if (!button) return;
    const rect = button.getBoundingClientRect();
    const gap = 6;
    const viewportH = window.innerHeight || document.documentElement.clientHeight;
    const menuH = Math.min(menu.scrollHeight || 260, Math.round(viewportH * 0.52));
    const openUp = rect.bottom + gap + menuH > viewportH && rect.top > menuH;
    const top = openUp ? Math.max(8, rect.top - gap - menuH) : Math.min(viewportH - 8, rect.bottom + gap);
    menu.style.left = `${Math.max(8, rect.left)}px`;
    menu.style.top = `${top}px`;
    menu.style.width = `${Math.max(rect.width, 140)}px`;
    menu.style.maxHeight = `${Math.max(140, Math.min(320, openUp ? rect.top - 14 : viewportH - rect.bottom - 14))}px`;
  }

  function focusSelectedOption(select) {
    const menu = menus.get(select);
    if (!menu) return;
    const selected = menu.querySelector('.ui-select-option.selected:not(:disabled)') || menu.querySelector('.ui-select-option:not(:disabled)');
    if (selected) selected.focus({ preventScroll: true });
  }

  function openSelect(select) {
    if (select.disabled) return;
    if (activeSelect === select) {
      closeActive();
      return;
    }
    closeActive();
    buildMenu(select);
    const wrap = getWrapper(select);
    const menu = menus.get(select);
    const button = wrap ? wrap.querySelector('.ui-select-trigger') : null;
    if (!wrap || !menu || !button) return;
    activeSelect = select;
    wrap.classList.add('open');
    button.setAttribute('aria-expanded', 'true');
    menu.classList.add('open');
    positionMenu(select);
    requestAnimationFrame(() => positionMenu(select));
  }

  function moveFocus(menu, direction) {
    const items = Array.from(menu.querySelectorAll('.ui-select-option:not(:disabled)'));
    if (!items.length) return;
    const current = document.activeElement;
    const currentIndex = items.indexOf(current);
    const nextIndex = currentIndex === -1
      ? 0
      : (currentIndex + direction + items.length) % items.length;
    items[nextIndex].focus({ preventScroll: true });
  }

  function enhanceSelect(select) {
    if (!select || select.getAttribute(ENHANCED) === 'true') return;
    const id = select.id || `ui-select-${Math.random().toString(36).slice(2)}`;
    select.dataset.uiSelectId = id;
    select.setAttribute(ENHANCED, 'true');
    select.classList.add('native-select-hidden');

    const wrap = document.createElement('span');
    wrap.className = 'ui-select';
    wrap.dataset.selectId = id;

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'ui-select-trigger';
    button.setAttribute('aria-haspopup', 'listbox');
    button.setAttribute('aria-expanded', 'false');
    button.innerHTML = '<span class="ui-select-value"></span>';

    const menu = document.createElement('div');
    menu.className = 'ui-select-menu';
    menu.setAttribute('role', 'listbox');
    document.body.appendChild(menu);
    menus.set(select, menu);

    select.insertAdjacentElement('afterend', wrap);
    wrap.appendChild(button);

    button.addEventListener('click', () => openSelect(select));
    button.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openSelect(select);
        focusSelectedOption(select);
      }
      if (event.key === 'ArrowDown') {
        event.preventDefault();
        openSelect(select);
        focusSelectedOption(select);
      }
    });

    menu.addEventListener('keydown', event => {
      if (event.key === 'Escape') {
        event.preventDefault();
        closeActive();
        button.focus({ preventScroll: true });
      }
      if (event.key === 'ArrowDown') {
        event.preventDefault();
        moveFocus(menu, 1);
      }
      if (event.key === 'ArrowUp') {
        event.preventDefault();
        moveFocus(menu, -1);
      }
      if (event.key === 'Tab') closeActive();
    });

    select.addEventListener('change', () => syncSelect(select));
    select.addEventListener('input', () => syncSelect(select));

    const optionObserver = new MutationObserver(() => syncSelect(select));
    optionObserver.observe(select, { childList: true, subtree: true, attributes: true, attributeFilter: ['selected', 'disabled', 'label', 'value'] });

    syncSelect(select);
  }

  function init() {
    syncAll();

    const bodyObserver = new MutationObserver(() => {
      window.requestAnimationFrame(syncAll);
    });
    bodyObserver.observe(document.body, { childList: true, subtree: true });

    document.addEventListener('click', event => {
      const target = event.target;
      const inSelect = target.closest && (target.closest('.ui-select') || target.closest('.ui-select-menu'));
      if (!inSelect) closeActive();
    });

    window.addEventListener('resize', () => {
      if (activeSelect) positionMenu(activeSelect);
    });
    window.addEventListener('scroll', () => {
      if (activeSelect) positionMenu(activeSelect);
    }, true);

    if (!syncTimer) syncTimer = window.setInterval(syncAll, 700);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }

  window.refreshCustomSelects = syncAll;
})();
