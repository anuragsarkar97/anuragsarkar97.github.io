(function () {
  var filter = document.getElementById('note-filter');
  var count = document.getElementById('note-count');
  if (filter && count) {
    var rows = Array.prototype.slice.call(document.querySelectorAll('.note-table tbody tr'));
    filter.addEventListener('input', function () {
      var query = filter.value.trim().toLowerCase();
      var shown = 0;
      rows.forEach(function (row) {
        var match = !query || row.getAttribute('data-title').indexOf(query) !== -1;
        row.classList.toggle('is-hidden', !match);
        if (match) shown += 1;
      });
      count.textContent = 'Results: ' + shown;
    });
  }

  var prose = document.querySelector('.prose');
  if (!prose) return;

  var toc = document.querySelector('.toc');
  var heads = prose.querySelectorAll('h2[id], h3[id]');
  if (toc && heads.length) {
    var list = document.createElement('ol');
    heads.forEach(function (heading) {
      var item = document.createElement('li');
      if (heading.tagName === 'H3') item.className = 'toc-h3';
      var link = document.createElement('a');
      link.href = '#' + heading.id;
      link.textContent = heading.textContent;
      item.appendChild(link);
      list.appendChild(item);
    });
    toc.appendChild(list);
    toc.hidden = false;
  }

  prose.querySelectorAll('pre').forEach(function (pre) {
    pre.tabIndex = 0;
    pre.setAttribute('role', 'region');
    pre.setAttribute('aria-label', 'Code');
    var holder = pre.parentElement && pre.parentElement.classList.contains('highlight') ? pre.parentElement : pre;
    var marked = pre.querySelector('[class*="language-"]') || pre;
    var match = (marked.className || '').match(/language-([a-z0-9]+)/i);
    if (!match || match[1] === 'plaintext') return;
    var label = document.createElement('span');
    label.className = 'code-label';
    label.textContent = match[1];
    if (getComputedStyle(holder).position === 'static') holder.style.position = 'relative';
    holder.appendChild(label);
  });

  prose.querySelectorAll('table').forEach(function (table) {
    var scroll = document.createElement('div');
    scroll.className = 'table-scroll';
    scroll.tabIndex = 0;
    scroll.setAttribute('role', 'region');
    scroll.setAttribute('aria-label', 'Scrollable table');
    table.before(scroll);
    scroll.appendChild(table);
  });
})();
