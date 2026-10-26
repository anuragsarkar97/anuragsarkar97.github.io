(function () {
  var form = document.getElementById('post-editor');
  var fields = ['title', 'date', 'description', 'body'];
  var status = document.getElementById('draft-status');
  var key = 'blog.markdown-draft.v1';
  var saveButton = document.getElementById('save-post');
  var preview = document.getElementById('post-preview');
  var directory = null;
  var previewTimer;
  saveButton.disabled = typeof window.showDirectoryPicker !== 'function';
  document.getElementById('folder-help').hidden = !saveButton.disabled;

  function escapeHTML(text) {
    return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function renderPreview() {
    if (!window.marked) return;
    var stylesheet = new URL(preview.dataset.stylesheet, document.baseURI);
    var theme = document.documentElement.dataset.theme || '';
    // Draft HTML lives in an opaque-origin sandbox with scripts and active content blocked.
    preview.srcdoc = '<!doctype html><html lang="en" data-theme="' + theme + '"><head>' +
      '<meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="' +
      escapeHTML("default-src 'none'; style-src 'unsafe-inline' " + stylesheet.origin +
        "; img-src https: data:; base-uri 'none'; form-action 'none'") + '">' +
      '<link rel="stylesheet" href="' + escapeHTML(stylesheet.href) + '">' +
      '<style>body{padding:1.5rem}pre,table{max-width:100%;overflow-x:auto}table{display:block}</style>' +
      '</head><body><main class="prose"><h1>' + escapeHTML(form.elements.title.value || 'Untitled post') +
      '</h1>' + window.marked.parse(form.elements.body.value, { async: false }) + '</main></body></html>';
  }
  var today = new Date();
  today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
  form.elements.date.value = today.toISOString().slice(0, 10);

  try {
    var draft = JSON.parse(localStorage.getItem(key));
    if (draft && fields.every(function (name) { return typeof draft[name] === 'string'; })) {
      fields.forEach(function (name) { form.elements[name].value = draft[name]; });
      status.textContent = 'Draft restored from this browser. Save a file to keep it.';
    }
  } catch (e) {
    status.textContent = 'Draft storage is unavailable. Save a file before leaving.';
  }
  form.hidden = false;
  renderPreview();
  new MutationObserver(renderPreview).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  form.addEventListener('input', function () {
    clearTimeout(previewTimer);
    previewTimer = setTimeout(renderPreview, 150);
    var draft = {};
    fields.forEach(function (name) {
      form.elements[name].setCustomValidity('');
      draft[name] = form.elements[name].value;
    });
    try {
      localStorage.setItem(key, JSON.stringify(draft));
      status.textContent = 'Draft saved in this browser. Save a file to keep it.';
    } catch (e) {
      status.textContent = 'Draft could not be saved. Save a file before leaving.';
    }
  });

  function buildPost() {
    var title = form.elements.title.value.trim();
    var body = form.elements.body.value;
    var slug = title.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
      .replace(/[^a-z0-9]+/g, '-').slice(0, 80).replace(/^-|-$/g, '') || 'post';
    var markdown = '---\nlayout: post\ntitle: ' + JSON.stringify(title) + '\ndem: ' +
      JSON.stringify(form.elements.description.value.trim()) + '\n---\n\n' + body;
    if (!markdown.endsWith('\n')) markdown += '\n';
    return { filename: form.elements.date.value + '-' + slug + '.md', markdown: markdown };
  }

  form.addEventListener('submit', async function (event) {
    event.preventDefault();
    if (!form.elements.title.value.trim() || !form.elements.body.value.trim()) {
      var empty = !form.elements.title.value.trim() ? form.elements.title : form.elements.body;
      empty.setCustomValidity(empty === form.elements.title ? 'Enter a title.' : 'Write some Markdown first.');
      empty.reportValidity();
      return;
    }
    var post = buildPost();
    if (event.submitter && event.submitter.value === 'save') {
      saveButton.disabled = true;
      try {
        if (!directory) directory = await window.showDirectoryPicker({ id: 'blog-posts', mode: 'readwrite' });
        if (directory.name !== '_posts') {
          directory = null;
          status.textContent = 'Choose the _posts folder inside your blog repository.';
          return;
        }
        var file;
        try {
          file = await directory.getFileHandle(post.filename);
        } catch (error) {
          if (error.name !== 'NotFoundError') throw error;
        }
        if (file && !window.confirm('Replace ' + post.filename + ' in _posts?')) {
          status.textContent = 'Existing file kept. Your draft is still in the editor.';
          return;
        }
        if (!file) file = await directory.getFileHandle(post.filename, { create: true });
        var writable = await file.createWritable();
        try {
          await writable.write(post.markdown);
          await writable.close();
        } catch (error) {
          await writable.abort().catch(function () {});
          throw error;
        }
        var current = buildPost();
        status.textContent = 'Saved _posts/' + post.filename +
          (current.markdown === post.markdown && current.filename === post.filename ?
            '. Publish the site when ready.' : '. Save again to include your latest edits.');
      } catch (error) {
        directory = null;
        status.textContent = error.name === 'AbortError' ?
          'Save cancelled. Your draft is still in the editor.' :
          'Could not save the file. Try choosing the folder again, or download a copy.';
      } finally {
        saveButton.disabled = false;
      }
      return;
    }
    var url = URL.createObjectURL(new Blob([post.markdown], { type: 'text/markdown;charset=utf-8' }));
    var link = document.createElement('a');
    link.href = url;
    link.download = post.filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  });
})();
