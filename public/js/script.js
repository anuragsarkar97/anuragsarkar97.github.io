(function () {
  document.querySelectorAll('.prose pre').forEach(function (pre) {
    pre.tabIndex = 0;
    pre.setAttribute('role', 'region');
    pre.setAttribute('aria-label', 'Code or preformatted text');
  });
  document.querySelectorAll('.prose h2[id], .prose h3[id]').forEach(function (heading) {
    var link = document.createElement('a');
    link.className = 'heading-anchor';
    link.href = '#' + heading.id;
    link.textContent = '#';
    link.setAttribute('aria-label', 'Link to this section');
    heading.appendChild(link);
  });
  document.querySelectorAll('.prose table').forEach(function (table) {
    var scroll = document.createElement('div');
    scroll.className = 'table-scroll';
    scroll.tabIndex = 0;
    scroll.setAttribute('role', 'region');
    scroll.setAttribute('aria-label', 'Scrollable table');
    table.before(scroll);
    scroll.appendChild(table);
  });
})();
