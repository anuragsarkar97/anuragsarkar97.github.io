// Run with `node scripts/check_editor.js`; no test dependencies are needed.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../public/js/editor.js'), 'utf8');

function editor(saved = null, blocked = false, picker = undefined, confirm = () => true) {
  const elements = {};
  for (const name of ['title', 'date', 'description', 'body']) {
    elements[name] = { value: '', setCustomValidity(message) { this.error = message; }, reportValidity() {} };
  }
  const handlers = {};
  const form = { elements, hidden: true, addEventListener(name, fn) { handlers[name] = fn; } };
  const status = {};
  const link = { click() {}, remove() {} };
  const nodes = { 'post-editor': form, 'draft-status': status, 'save-post': {}, 'folder-help': {}, 'post-preview': {} };
  let blob;
  vm.runInNewContext(source, {
    Date, Blob, setTimeout(fn) { fn(); }, clearTimeout() {},
    window: { showDirectoryPicker: picker, confirm },
    MutationObserver: class { observe() {} },
    URL: { createObjectURL(value) { blob = value; return 'blob:test'; }, revokeObjectURL() {} },
    localStorage: {
      getItem() { if (blocked) throw Error('blocked'); return saved; },
      setItem(key, value) { if (blocked) throw Error('blocked'); saved = value; }
    },
    document: {
      getElementById(id) { return nodes[id]; }, documentElement: { dataset: {} },
      createElement() { return link; }, body: { appendChild() {} }
    }
  });
  return { elements, form, status, link, input() { handlers.input(); },
    submit(action = 'download') { return handlers.submit({ preventDefault() {}, submitter: { value: action } }); },
    saved() { return saved; }, blob() { return blob; } };
}

(async function () {
  const draft = editor();
  assert.equal(draft.form.hidden, false);
  Object.assign(draft.elements.title, { value: 'Draft: "quotes" & café' });
  draft.elements.date.value = '2020-01-02';
  draft.elements.description.value = 'Description: "quoted"';
  draft.elements.body.value = '## Section\n\n```go\nfmt.Println("hello")\n```\n';
  draft.input();
  const restored = editor(draft.saved());
  for (const name of ['title', 'date', 'description', 'body']) {
    assert.equal(restored.elements[name].value, draft.elements[name].value);
  }
  await restored.submit();
  assert.equal(restored.link.download, '2020-01-02-draft-quotes-cafe.md');
  const output = await restored.blob().text();
  assert(output.startsWith('---\nlayout: post\n'));
  assert.equal(JSON.parse(output.match(/^title: (.+)$/m)[1]), draft.elements.title.value);
  assert.equal(JSON.parse(output.match(/^dem: (.+)$/m)[1]), draft.elements.description.value);
  assert(output.endsWith(draft.elements.body.value));
  const unavailable = editor(null, true);
  unavailable.elements.title.value = 'A post';
  unavailable.elements.body.value = 'Keep this text';
  unavailable.input();
  assert(unavailable.status.textContent.includes('could not be saved'));
  await unavailable.submit();
  assert((await unavailable.blob().text()).endsWith('Keep this text\n'));
  const empty = editor('{broken json');
  empty.elements.title.value = '   ';
  await empty.submit();
  assert.equal(empty.elements.title.error, 'Enter a title.');
  assert.equal(empty.blob(), undefined);
  let written = null;
  let writes = 0;
  let replace = false;
  let pickerCalls = 0;
  const file = { async createWritable() {
    let pending;
    return { async write(text) { pending = text; }, async close() { written = pending; writes++; }, async abort() {} };
  } };
  const folder = { name: '_posts', async getFileHandle(name, options) {
    assert.equal(name, restored.link.download);
    if (written === null && !options?.create) throw Object.assign(Error('missing'), { name: 'NotFoundError' });
    return file;
  } };
  const direct = editor(draft.saved(), false, async () => { pickerCalls++; return folder; }, () => replace);
  await direct.submit('save');
  assert.equal(written, output);
  assert(direct.status.textContent.startsWith('Saved _posts/'));
  await direct.submit('save');
  assert.equal(writes, 1, 'Declining overwrite must preserve the existing file');
  replace = true;
  direct.elements.body.value = 'Updated body';
  await direct.submit('save');
  assert.equal(writes, 2);
  assert.equal(pickerCalls, 1, 'Reuse the selected folder during this editing session');
  assert(written.endsWith('Updated body\n'));
  const wrongFolder = editor(draft.saved(), false, async () => ({ name: 'Downloads' }));
  await wrongFolder.submit('save');
  assert(wrongFolder.status.textContent.startsWith('Choose the _posts'));
  const cancelled = editor(draft.saved(), false, async () => { throw Object.assign(Error('cancelled'), { name: 'AbortError' }); });
  await cancelled.submit('save');
  assert(cancelled.status.textContent.startsWith('Save cancelled'));
  const denied = editor(draft.saved(), false, async () => { throw Error('denied'); });
  await denied.submit('save');
  assert(denied.status.textContent.startsWith('Could not save'));
  let aborted = false;
  const failedWrite = editor(draft.saved(), false, async () => ({ name: '_posts', async getFileHandle() {
    return { async createWritable() { return { async write() { throw Error('disk full'); }, async abort() { aborted = true; } }; } };
  } }));
  await failedWrite.submit('save');
  assert(aborted);
  assert(failedWrite.status.textContent.startsWith('Could not save'));
  console.log('PASS: drafts, Markdown export, folder saving/reuse, overwrite refusal/approval, wrong-folder rejection, cancellation, permission failure and aborted writes.');
})().catch(error => { console.error(error); process.exitCode = 1; });
