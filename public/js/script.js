(function () {
  var button = document.querySelector('.theme-toggle');
  var system = window.matchMedia('(prefers-color-scheme: dark)');
  function isDark() {
    return document.documentElement.dataset.theme === 'dark' ||
      (!document.documentElement.dataset.theme && system.matches);
  }
  function update() {
    button.textContent = isDark() ? 'Light mode' : 'Dark mode';
    button.setAttribute('aria-label', 'Switch to ' + (isDark() ? 'light' : 'dark') + ' mode');
  }
  if (button) {
    button.hidden = false;
    update();
    system.addEventListener('change', update);
    button.addEventListener('click', function () {
      var theme = isDark() ? 'light' : 'dark';
      document.documentElement.dataset.theme = theme;
      try { localStorage.setItem('theme', theme); } catch (e) { /* The toggle still works. */ }
      update();
    });
  }
  document.querySelectorAll('.prose pre').forEach(function (pre) {
    pre.tabIndex = 0;
    pre.setAttribute('role', 'region');
    pre.setAttribute('aria-label', 'Code or preformatted text');
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
