const searchField = document.querySelector('#search');
const searchMenu = document.querySelector('#search-list');
if (searchField && window.List && document.querySelector('.note-entry')) {
  const notes = new List('notes', { valueNames: [{ data: ['search'] }] });
  const status = document.querySelector('#search-status');
  const storiesTitle = document.querySelector('.stories-title');
  const menuLimit = 8;
  let active = 0;

  const escapeRegExp = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  const highlight = (text, query) => {
    const fragment = document.createDocumentFragment();
    const words = [...new Set(query.toLowerCase().split(/\s+/).filter(Boolean))];
    if (!words.length) {
      fragment.append(text);
      return fragment;
    }
    const pattern = new RegExp(words.map(escapeRegExp).join('|'), 'ig');
    let last = 0;
    for (const match of text.matchAll(pattern)) {
      fragment.append(text.slice(last, match.index));
      const mark = document.createElement('mark');
      mark.textContent = match[0];
      fragment.append(mark);
      last = match.index + match[0].length;
    }
    fragment.append(text.slice(last));
    return fragment;
  };

  const closeMenu = () => {
    if (!searchMenu) return;
    searchMenu.hidden = true;
    searchMenu.replaceChildren();
    active = 0;
    searchField.setAttribute('aria-expanded', 'false');
    searchField.removeAttribute('aria-activedescendant');
  };

  const paintActive = () => {
    const options = [...searchMenu.querySelectorAll('[role="option"]')];
    options.forEach((option, index) => {
      const on = index === active;
      option.classList.toggle('is-active', on);
      option.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    const current = options[active];
    if (!current) {
      searchField.removeAttribute('aria-activedescendant');
      return;
    }
    searchField.setAttribute('aria-activedescendant', current.id);
    const top = current.offsetTop;
    const bottom = top + current.offsetHeight;
    if (top < searchMenu.scrollTop) searchMenu.scrollTop = top;
    else if (bottom > searchMenu.scrollTop + searchMenu.clientHeight) {
      searchMenu.scrollTop = bottom - searchMenu.clientHeight;
    }
  };

  const renderMenu = () => {
    if (!searchMenu) return;
    const query = searchField.value.trim();
    const matches = query ? notes.matchingItems : [];
    if (!matches.length) {
      closeMenu();
      return;
    }
    const shown = matches.slice(0, menuLimit);
    if (active >= shown.length) active = 0;
    const items = shown.map((item, index) => {
      const option = document.createElement('li');
      option.id = `search-option-${index}`;
      option.className = 'search-option';
      option.setAttribute('role', 'option');
      const link = document.createElement('a');
      link.href = item.elm.querySelector('a')?.getAttribute('href') || '#';
      link.tabIndex = -1;
      const title = document.createElement('span');
      title.className = 'search-option-title';
      title.append(highlight(item.elm.querySelector('h2, h3')?.textContent.trim() || 'Note', query));
      link.append(title);
      const kicker = item.elm.querySelector('.kicker');
      if (kicker) {
        const meta = document.createElement('span');
        meta.className = 'search-option-meta';
        const name = kicker.querySelector('.kicker-name')?.textContent.trim();
        const time = kicker.querySelector('time')?.textContent.trim();
        meta.textContent = [name, time].filter(Boolean).join(' · ');
        link.append(meta);
      }
      option.append(link);
      return option;
    });
    if (matches.length > shown.length) {
      const more = document.createElement('li');
      more.className = 'search-more';
      more.setAttribute('role', 'presentation');
      more.textContent = `${shown.length} of ${matches.length} notes`;
      items.push(more);
    }
    searchMenu.replaceChildren(...items);
    searchMenu.hidden = false;
    searchField.setAttribute('aria-expanded', 'true');
    paintActive();
  };

  const report = () => {
    const count = notes.matchingItems.length;
    const query = searchField.value.trim();
    status.textContent = query
      ? (count === 0 ? 'No matching notes.' : `${count} ${count === 1 ? 'note' : 'notes'} found.`)
      : '';
    if (storiesTitle) {
      const storyLeft = notes.matchingItems.some((item) => item.elm.classList.contains('story-entry'));
      storiesTitle.hidden = query.length > 0 && !storyLeft;
    }
    renderMenu();
  };

  notes.on('searchComplete', report);
  searchField.addEventListener('input', () => {
    active = 0;
    notes.search(searchField.value.trim());
  });
  searchField.addEventListener('focus', () => {
    if (searchField.value.trim()) renderMenu();
  });
  searchField.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      if (searchMenu && !searchMenu.hidden) {
        event.preventDefault();
        closeMenu();
      }
      return;
    }
    if (!searchMenu || searchMenu.hidden) return;
    const options = searchMenu.querySelectorAll('[role="option"]');
    if (!options.length) return;
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      active = (active + 1) % options.length;
      paintActive();
    } else if (event.key === 'ArrowUp') {
      event.preventDefault();
      active = (active - 1 + options.length) % options.length;
      paintActive();
    } else if (event.key === 'Enter') {
      const link = options[active]?.querySelector('a');
      if (!link) return;
      event.preventDefault();
      location.href = link.href;
    }
  });
  if (searchMenu) {
    searchMenu.addEventListener('mousedown', (event) => event.preventDefault());
    searchMenu.addEventListener('mousemove', (event) => {
      const option = event.target.closest('[role="option"]');
      if (!option || option.parentElement !== searchMenu) return;
      const index = [...searchMenu.querySelectorAll('[role="option"]')].indexOf(option);
      if (index < 0 || index === active) return;
      active = index;
      paintActive();
    });
  }
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.search-field')) closeMenu();
  });

  const focusSearch = () => {
    if (location.hash === '#search') searchField.focus();
  };
  focusSearch();
  window.addEventListener('hashchange', focusSearch);
} else if (searchField) {
  const status = document.querySelector('#search-status');
  searchField.addEventListener('input', () => {
    status.textContent = searchField.value.trim() ? 'No matching notes.' : '';
  });
}

document.addEventListener('keydown', (event) => {
  if (!(event.metaKey || event.ctrlKey) || event.key.toLowerCase() !== 'k' || event.altKey) return;
  const field = document.querySelector('#search');
  if (!field) return;
  event.preventDefault();
  field.focus();
  field.select();
});

const share = document.querySelector('.share-note');
if (share && navigator.clipboard?.writeText) {
  const shareStatus = document.querySelector('.share-status');
  share.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(share.dataset.url);
      shareStatus.textContent = 'Link copied.';
    } catch {
      shareStatus.textContent = 'Could not copy.';
    }
  });
}

const headings = '.article-body :is(h2, h3, h4)';
if (document.querySelector(headings)) {
  const outline = document.querySelector('.article-outline');
  if (window.tocbot && document.querySelector('.article-body :is(h2, h3, h4)[id]')) {
    const disclosure = outline.querySelector('details');
    const mobile = matchMedia('(max-width: 56rem)');
    const updateOutline = () => {
      disclosure.open = !mobile.matches;
    };
    updateOutline();
    mobile.addEventListener('change', updateOutline);
    disclosure.addEventListener('click', (event) => {
      if (mobile.matches && event.target.closest('.js-toc a') &&
          !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey) {
        disclosure.open = false;
      }
    });
    outline.hidden = false;
    tocbot.init({
      tocSelector: '.js-toc',
      contentSelector: '.article-body',
      headingSelector: 'h2[id], h3[id], h4[id]',
      collapseDepth: 4,
      headingsOffset: 88,
      scrollSmooth: false,
    });
  }

  if (window.anchors) {
    anchors.options = { placement: 'right', visible: 'always', icon: '#', ariaLabel: 'Link to this section' };
    anchors.add(headings);
  }

  // The outline adds height above the article on narrow screens.
  const target = document.querySelector('.article-body :target');
  if (target) requestAnimationFrame(() => target.scrollIntoView({ block: 'start', behavior: 'instant' }));
}

for (const code of document.querySelectorAll('.article-body pre > code')) {
  const block = code.parentElement;
  block.tabIndex = 0;
  if (!navigator.clipboard?.writeText) continue;

  const wrapper = document.createElement('div');
  wrapper.className = 'code-block';
  const toolbar = document.createElement('div');
  toolbar.className = 'code-toolbar';
  const status = document.createElement('span');
  status.setAttribute('role', 'status');
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'btn btn-ghost btn-xs';
  button.textContent = 'Copy';

  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(code.textContent);
      status.textContent = 'Copied';
    } catch {
      status.textContent = 'Could not copy';
    }
  });

  toolbar.append(status, button);
  block.before(wrapper);
  wrapper.append(toolbar, block);
}
