const searchField = document.querySelector('#search');
if (searchField && window.List) {
  const notes = new List('notes', { valueNames: [{ data: ['search'] }] });
  const status = document.querySelector('#search-status');
  searchField.closest('.archive-search').hidden = false;

  notes.on('searchComplete', () => {
    const count = notes.matchingItems.length;
    status.textContent = searchField.value.trim()
      ? (count === 0 ? 'No matching notes.' : `${count} ${count === 1 ? 'note' : 'notes'} found.`)
      : '';
  });

  searchField.addEventListener('input', () => notes.search(searchField.value.trim()));

  const focusSearch = () => {
    if (location.hash === '#search') searchField.focus();
  };
  focusSearch();
  window.addEventListener('hashchange', focusSearch);
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
      headingsOffset: 110,
      scrollSmooth: false,
    });
  }

  if (window.anchors) {
    anchors.options = { placement: 'right', visible: 'always', icon: '#', ariaLabel: 'Link to this section' };
    anchors.add(headings);
  }

  // The outline adds height above the article on narrow screens.
  const target = document.querySelector('.article-body :target');
  if (target) requestAnimationFrame(() => target.scrollIntoView());
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
  button.textContent = 'Copy code';

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
