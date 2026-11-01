const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const html = fs.readFileSync(`${__dirname}/index.html`, 'utf8');
const script = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)].map(match => match[1]).join('\n');
const raw = JSON.parse(script.match(/const RAW_VOCAB = (\[[\s\S]*?\]);/)[1]);
const original = JSON.parse(fs.readFileSync(`${__dirname}/backups/index.before-education-2026-11-01.html`, 'utf8').match(/const RAW_VOCAB = (\[[\s\S]*?\]);/)[1]);
const decodeHtml = value => value.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');

function runtime(options = {}) {
  const elements = new Map();
  const callbacks = {};
  const storage = new Map();
  const timers = new Map();
  const media = [];
  const utterances = [];
  const alerts = [];
  let timerId = 0;
  let document;
  class Element {
    constructor(tagName = 'div', attributes = '') {
      this.tagName = tagName.toUpperCase();
      this.dataset = {};
      this.style = {};
      this.listeners = {};
      this.attributes = {};
      this.value = '';
      this.checked = false;
      this.children = [];
      this.className = '';
      this.parentElement = null;
      const classes = new Set();
      this.classList = {
        add: (...values) => values.forEach(value => classes.add(value)),
        remove: (...values) => values.forEach(value => classes.delete(value)),
        contains: value => classes.has(value) || this.className.split(' ').includes(value),
        toggle: (value, force) => { const enabled = force ?? !classes.has(value); if (enabled) classes.add(value); else classes.delete(value); return enabled; }
      };
      for (const match of attributes.matchAll(/([\w-]+)="([^"]*)"/g)) this.setAttribute(match[1], decodeHtml(match[2]));
    }
    setAttribute(key, value) {
      this.attributes[key] = String(value);
      if (key === 'id') { this.id = value; elements.set(value, this); }
      if (key === 'class') this.className = value;
      if (key.startsWith('data-')) this.dataset[key.slice(5).replace(/-([a-z])/g, (match, letter) => letter.toUpperCase())] = value;
    }
    getAttribute(key) { return this.attributes[key]; }
    removeAttribute(key) { delete this.attributes[key]; }
    set innerHTML(value) {
      this._html = String(value);
      this.children = [];
      for (const match of this._html.matchAll(/<(button|input|select|textarea|div|h2|h3|a)\b([^>]*)>/g)) {
        const child = new Element(match[1], match[2]);
        child.parentElement = this;
        this.children.push(child);
      }
    }
    get innerHTML() { return this._html || ''; }
    matches(selector) {
      if (selector.includes(',')) return selector.split(',').some(item => this.matches(item.trim()));
      if (selector.startsWith('.')) return selector.slice(1).split('.').every(value => this.classList.contains(value));
      if (selector.startsWith('[')) {
        const match = selector.match(/^\[([^=\]]+)(?:="([^"]*)")?\]$/);
        return match ? this.attributes[match[1]] !== undefined && (match[2] === undefined || this.attributes[match[1]] === match[2]) : false;
      }
      return selector.replace(/:.*/, '').toUpperCase() === this.tagName;
    }
    querySelectorAll(selector) { return this.children.filter(child => child.matches(selector)); }
    querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
    addEventListener(event, handler) { (this.listeners[event] ||= []).push(handler); }
    click() { this.listeners.click?.forEach(handler => handler({ target: this, preventDefault() {}, stopPropagation() {} })); this.onclick?.({ target: this }); }
    focus() { document.activeElement = this; }
    getClientRects() { return [{}]; }
    contains(element) { return element === this || this.children.includes(element); }
    appendChild(element) { this.children.push(element); element.parentElement = this; }
    before(element) { this.parentElement?.appendChild(element); }
    remove() { if (this.parentElement) this.parentElement.children = this.parentElement.children.filter(child => child !== this); }
    reset() { this.resetCount = (this.resetCount || 0) + 1; }
    getContext() { return options.canvasUnavailable ? null : { clearRect() {}, save() {}, restore() {}, translate() {}, rotate() {}, fillRect() {} }; }
  }
  for (const match of html.matchAll(/<([a-z][\w-]*)\b([^>]*\bid="[^"]+"[^>]*)>/g)) new Element(match[1], match[2]);
  document = {
    getElementById: id => elements.get(id) || null,
    createElement: tag => new Element(tag),
    querySelectorAll: selector => [...elements.values()].filter(element => element.matches(selector)),
    querySelector: selector => [...elements.values()].find(element => element.matches(selector)) || null,
    addEventListener: (event, handler) => (callbacks[event] ||= []).push(handler),
    removeEventListener() {},
    documentElement: new Element('html'), body: new Element('body'), activeElement: null
  };
  const speechSynthesis = {
    getVoices: () => options.voices ?? [{ name: 'English US', lang: 'en-US', localService: true }, { name: 'English UK', lang: 'en-GB', localService: true }],
    addEventListener() {},
    cancel() {},
    speak: utterance => utterances.push(utterance)
  };
  class Audio {
    constructor(url) { this.url = url; this.paused = false; media.push(this); }
    play() { if (options.throwAudioPlay) throw new Error('Playback unavailable'); return Promise.resolve(); }
    pause() { this.paused = true; }
    removeAttribute() {}
    load() {}
  }
  const window = { innerWidth: 1280, innerHeight: 800, addEventListener() {}, scrollTo() {}, matchMedia: () => ({ matches: false }) };
  if (options.native !== false) window.speechSynthesis = speechSynthesis;
  const context = vm.createContext({
    document, window, navigator: { onLine: options.online !== false }, Audio,
    SpeechSynthesisUtterance: class { constructor(text) { this.text = text; } },
    localStorage: { getItem: key => storage.get(key) ?? null, setItem: (key, value) => { if (key === options.failStorageKey) throw new Error('QuotaExceededError'); storage.set(key, value); }, removeItem: key => storage.delete(key) },
    setTimeout: (handler, delay) => { const id = ++timerId; timers.set(id, { handler, delay }); return id; },
    clearTimeout: id => timers.delete(id), requestAnimationFrame: () => 1, cancelAnimationFrame() {},
    alert: message => alerts.push(message), console: options.failStorageKey ? { ...console, warn() {} } : console, location: { reload() {} }, URL, Blob
  });
  vm.runInContext(script, context, { timeout: 10000 });
  const evaluate = source => vm.runInContext(source, context, { timeout: 10000 });
  evaluate('initAppState();');
  return { evaluate, context, elements, document, callbacks, storage, timers, media, utterances, alerts, boot: () => callbacks.DOMContentLoaded.forEach(handler => handler()) };
}

test('standalone script compiles and old identifiers remain attached to the same words', () => {
  new vm.Script(script);
  const markup = html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/g, '');
  const staticIds = [...markup.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
  assert.equal(new Set(staticIds).size, staticIds.length, 'Duplicate static DOM ID');
  const policy = JSON.parse(fs.readFileSync(`${__dirname}/curriculum-policy.json`, 'utf8'));
  const retained = new Set(policy.c1Core);
  assert.equal(raw.length, original.filter(row => row[3] !== 'C1' || retained.has(row[0])).length + 320);
  const byWord = new Map(raw.map(row => [row[0], row]));
  for (const [index, row] of original.entries()) {
    if (row[3] === 'C1' && !retained.has(row[0])) {
      assert(!byWord.has(row[0]), `Removed C1 must not be shipped: ${row[0]}`);
      continue;
    }
    assert.equal(byWord.get(row[0])[12].id, `ox-${String(index + 1).padStart(4, '0')}`);
  }
  assert.equal(new Set(raw.map(row => row[12].id)).size, raw.length);
});

test('adds 160 B1 and 160 B2 items, each with two bilingual examples and usage guidance', () => {
  const additions = raw.filter(row => /^(edu|supp)-/.test(row[12].id));
  for (const level of ['B1', 'B2']) assert.equal(additions.filter(row => row[3] === level).length, 160);
  for (const row of additions) {
    assert.equal(row[12].examples.length, 2);
    assert(row[12].usageNote.length > 10);
    for (const example of row[12].examples) {
      assert(example.en.split(/\s+/).length >= 5);
      assert(example.vi.length > 10);
      assert(!/We observed|It is an honor|soemthing|tkae|charater|\bthe word\b/.test(example.en));
    }
  }
});

test('active curriculum physically removes non-core C1 and keeps a metadata-only removal record', () => {
  const app = runtime();
  assert.equal(app.evaluate("VOCAB.filter(word => word.level === 'B1').length"), 951);
  assert.equal(app.evaluate("VOCAB.filter(word => word.level === 'B2').length"), 1546);
  assert.equal(app.evaluate("VOCAB.filter(word => word.level === 'C1').length"), 185);
  const archive = JSON.parse(fs.readFileSync(`${__dirname}/removed-c1.json`, 'utf8'));
  assert.equal(archive.length, 1117);
  assert.equal(archive.length + app.evaluate("VOCAB.filter(word => word.level === 'C1').length"), 1302);
  assert(archive.every(row => !('original' in row) && !('example' in row) && !('meaningVi' in row)));
  assert(!fs.existsSync(`${__dirname}/vocabulary-c1-archive.json`));
});

test('all editable content tables have unique entries and valid translations', () => {
  const corrections = fs.readFileSync(`${__dirname}/content-corrections.tsv`, 'utf8').trim().split(/\r?\n/).slice(1).map(line => line.split('|'));
  assert.equal(corrections.length, 140);
  assert.equal(new Set(corrections.map(row => row[0])).size, corrections.length);
  for (const row of corrections) assert.equal(row.length, 5);
  for (const [filename, width, count, keyColumn] of [
    ['content-repairs.tsv', 6, 829, 0], ['content-glosses.tsv', 2, 512, 0],
    ['content-expansion.tsv', 11, 160, 1], ['content-additions.tsv', 11, 160, 1]
  ]) {
    const rows = fs.readFileSync(`${__dirname}/${filename}`, 'utf8').trim().split(/\r?\n/).slice(1).map(line => line.split('|'));
    assert.equal(rows.length, count, filename);
    assert.equal(new Set(rows.map(row => row[keyColumn])).size, count, filename);
    assert(rows.every(row => row.length === width && row.every(value => value.trim())), filename);
  }
});

test('default lessons use reviewed B1 content, respect selected level and never fall through to C1', () => {
  const app = runtime();
  assert(app.evaluate("SRSEngine.getNewWords(10).every(word => word.reviewed && word.level === 'B1')"));
  app.evaluate("AppState.user.studyLevel = 'B2'");
  assert(app.evaluate("SRSEngine.getNewWords(10).every(word => word.reviewed && word.level === 'B2')"));
  app.evaluate("AppState.user.studyLevel = 'C1'");
  assert(app.evaluate('SRSEngine.getNewWords(10).length > 0 && SRSEngine.getNewWords(10).length <= 10'));
  assert.equal(app.evaluate('new Set(SRSEngine.getNewWords(10).map(word => word.topic)).size'), 1);
  app.evaluate("for (const word of AppState.vocabList.filter(word => word.level === 'B2')) AppState.wordProgress[word.id] = {box: 5}; AppState.user.studyLevel = 'B2';");
  assert.equal(app.evaluate('SRSEngine.getNewWords(10).length'), 0);
});

test('quality holds are excluded even when unreviewed legacy content is enabled', () => {
  const app = runtime();
  app.evaluate('AppState.user.reviewedOnly = false');
  app.evaluate("AppState.vocabList.push({ ...VOCAB[0], id: 'custom-held', reviewed: true, qualityIssues: ['template-or-incomplete-example'] })");
  assert.equal(app.evaluate("isStudyReady(AppState.vocabList.find(word => word.id === 'custom-held'))"), false);
  assert(app.evaluate('AppState.vocabList.filter(word => word.qualityIssues.length).every(word => !isStudyReady(word))'));
  assert(app.evaluate('SRSEngine.getNewWords(2000).every(word => !word.qualityIssues.length)'));
});

test('target matching handles phrases, inflections and irregular verbs without broad prefix matches', () => {
  const app = runtime();
  assert.equal(app.evaluate("findTargetSpan('I look after my sister.', 'look after').text"), 'look after');
  assert.equal(app.evaluate("findTargetSpan('Prices have risen again.', 'rise').text"), 'risen');
  assert.equal(app.evaluate("findTargetSpan('We are making progress.', 'make').text"), 'making');
  assert.equal(app.evaluate("findTargetSpan('The principal arrived.', 'principle')"), null);
  assert.equal(app.evaluate("findTargetSpan('We took care of her.', 'take care of').text"), 'took care of');
  assert.equal(app.evaluate("findTargetSpan('The (test) is easy.', '(test)').text"), '(test)');
  assert.equal(app.evaluate("findTargetSpan('They begged us to stay.', 'beg').text"), 'begged');
  assert.equal(app.evaluate("findTargetSpan('It was inferred from the results.', 'infer').text"), 'inferred');
  assert.equal(app.evaluate("findTargetSpan('They were forbidden to enter.', 'forbid').text"), 'forbidden');
  assert.equal(app.evaluate("findTargetSpan('She forbade it.', 'forbid').text"), 'forbade');
  assert.equal(app.evaluate("findTargetSpan('These are natural phenomena.', 'phenomenon').text"), 'phenomena');
  assert.equal(app.evaluate("findTargetSpan('We sell overseas.', 'oversee')"), null);
});

test('matching only uses already learned distractors and falls back if there are not enough', () => {
  const app = runtime();
  app.evaluate("globalThis.currentWord = VOCAB.find(word => word.reviewed); SessionEngine.renderMatchingQuestion(currentWord, document.getElementById('session-stage-root'))");
  assert(!app.elements.get('session-stage-root').innerHTML.includes('data-en-id'));
  app.evaluate("for (const word of VOCAB.filter(word => word.reviewed).slice(1, 8)) AppState.wordProgress[word.id] = {box: 1};");
  assert(app.evaluate("getDistractors(currentWord, 'meaningVi', 3, true).every(word => SRSEngine.getWordProgress(word.id).box > 0)"));
});

test('highlighting and inline audio arguments preserve apostrophes and escape HTML', () => {
  const app = runtime();
  app.context.payload = `She said "don't" <img src=x onerror=alert(1)>`;
  const escaped = app.evaluate("highlightTargetWord(payload, 'said')");
  assert(!escaped.includes('<img'));
  const argument = decodeHtml(app.evaluate('inlineString(payload)'));
  assert.equal(JSON.parse(argument), app.context.payload);
  assert.equal(app.evaluate("normalizeAnswer('  Don’t   give up  ')"), "don't give up");
  assert.equal(app.evaluate("normalizeSearch('ĐIỆN THOẠI')"), 'dien thoai');
});

test('distractors are finite, unique, reviewed and not taken from quality-held rows', () => {
  const app = runtime();
  assert(app.evaluate("VOCAB.filter(word => word.reviewed).every(word => { const items = getDistractors(word, 'meaningVi'); return items.length === 3 && new Set(items.map(item => item.meaningVi)).size === 3 && items.every(item => item.meaningVi !== word.meaningVi && isStudyReady(item)); })"));
  assert(app.evaluate("getDistractors(VOCAB.find(word => word.word === 'look after'), 'word', 2000).every(word => word.word !== 'take care of')"));
  app.evaluate('AppState.vocabList = [VOCAB.find(word => word.reviewed)]');
  assert.equal(app.evaluate("getDistractors(AppState.vocabList[0], 'word').length"), 0);
});

test('word introduction renders bilingual examples and all generated audio handlers compile', () => {
  const app = runtime();
  app.evaluate("SessionState.active = true; SessionEngine.renderFlashcardIntro(VOCAB.find(word => word.word === 'look forward to'), document.getElementById('session-stage-root'))");
  const rendered = app.elements.get('session-stage-root').innerHTML;
  assert(rendered.includes('Cách dùng:'));
  assert(rendered.includes('summer holidays'));
  for (const match of rendered.matchAll(/onclick="([^"]*)"/g)) new vm.Script(decodeHtml(match[1]));
});

test('cloze uses the inflected answer and falls back rather than showing an unmasked sentence', () => {
  const app = runtime();
  app.evaluate("SessionEngine.renderFillBlankQuestion({ ...VOCAB.find(word => word.word === 'rise'), example: 'Prices have risen again.' }, document.getElementById('session-stage-root'))");
  const rendered = app.elements.get('session-stage-root').innerHTML;
  assert(rendered.includes('Prices have ________ again.'));
  assert(/data-correct="true"[\s\S]*?>risen<\//.test(rendered));
  app.evaluate("SessionEngine.renderFillBlankQuestion({ ...VOCAB.find(word => word.word === 'rise'), example: 'Costs are high.' }, document.getElementById('session-stage-root'))");
  assert(!app.elements.get('session-stage-root').innerHTML.includes('Cloze test'));
});

test('search spans all levels, is accent-insensitive, escapes queries and supports load more', () => {
  const app = runtime();
  app.evaluate("currentCefrTab = 'C1'; searchQuery = 'look after'; renderLibrary()");
  assert(app.elements.get('library-topic-grid').innerHTML.includes('look after'));
  app.evaluate("searchQuery = 'cham soc'; renderLibrary()");
  assert(app.elements.get('library-topic-grid').innerHTML.includes('look after'));
  app.evaluate("searchQuery = '<img src=x onerror=alert(1)>'; renderLibrary()");
  assert(!app.elements.get('library-topic-grid').innerHTML.includes('<img'));
  app.evaluate("searchQuery = 'a'; renderLibrary()");
  assert(app.elements.get('library-topic-grid').innerHTML.includes('Xem thêm 60'));
  app.elements.get('library-show-more').onclick();
  assert.equal(app.evaluate('librarySearchLimit'), 120);
});

test('saving progress does not cache the entire dictionary', () => {
  const app = runtime();
  app.evaluate('saveState()');
  assert(!app.storage.has('lexiup_vocab_data'));
  assert(app.storage.has('lexiup_word_progress'));
});

test('bootstrap, adding a custom phrase and duplicate prevention complete without errors', () => {
  const app = runtime();
  app.boot();
  const values = { 'custom-word-input': "learner's notebook", 'custom-meaning-input': 'sổ của người học <img src=x>', 'custom-ipa-input': '', 'custom-pos-input': 'phrase', 'custom-level-input': 'B1', 'custom-example-input': "This is a learner's notebook.", 'custom-example-vi-input': 'Đây là sổ của người học.', 'custom-colloc-input': 'a useful notebook' };
  for (const [id, value] of Object.entries(values)) app.elements.get(id).value = value;
  const form = app.elements.get('form-add-custom-word');
  form.listeners.submit[0]({ preventDefault() {} });
  assert.equal(app.evaluate('AppState.vocabList.filter(word => word.isCustom).length'), 1);
  form.listeners.submit[0]({ preventDefault() {} });
  assert.equal(app.evaluate('AppState.vocabList.filter(word => word.isCustom).length'), 1);
  app.evaluate("searchQuery = 'notebook'; renderLibrary()");
  const result = app.elements.get('library-topic-grid').innerHTML;
  assert(!result.includes('<img'));
  for (const match of result.matchAll(/onclick="([^"]*)"/g)) new vm.Script(decodeHtml(match[1]));
});

test('invalid backups leave state unchanged and archived IDs survive valid restore', () => {
  const app = runtime();
  const before = app.evaluate('JSON.stringify(AppState)');
  app.evaluate(`restoreFullBackup(JSON.stringify({ app: 'LexiUp', user: { xp: 900 }, customWords: [null] }))`);
  assert.equal(app.evaluate('JSON.stringify(AppState)'), before);
  assert.equal(app.alerts.length, 1);
  app.evaluate(`restoreFullBackup(JSON.stringify({ app: 'LexiUp', user: { xp: 80, theme: 'dark', studyLevel: 'B2' }, wordProgress: { 'ox-3479': { box: 4, nextReview: 2000, lastReview: 1000, correctStreak: 3 } }, history: [], customWords: [] }))`);
  assert.equal(app.evaluate('AppState.wordProgress["ox-3479"].box'), 4);
  assert.equal(app.evaluate('AppState.user.xp'), 80);
  assert.equal(app.evaluate('AppState.user.studyLevel'), 'B2');
});

test('settings from storage cannot inject HTML or invalid enum values', () => {
  const app = runtime();
  assert.equal(app.evaluate("normalizeUser({ placementLevel: '<img>', theme: 'bad', dailyGoal: -1 }).placementLevel"), null);
  assert.equal(app.evaluate("normalizeCustomWord({ word: '<svg>', meaningVi: 'test', level: 'B1' })"), null);
  assert.equal(app.evaluate("Object.keys(normalizeProgress({ '__proto__': {box: 1}, bad: {box: 99} })).length"), 0);
});

test('correct feedback does not advance automatically, double grading is ignored and practice does not promote SRS', () => {
  const app = runtime();
  app.evaluate("globalThis.currentWord = { ...VOCAB.find(word => word.reviewed) }; SessionState.active = true; SessionState.isAnswered = false; SessionEngine.renderMultipleChoiceVi(currentWord, document.getElementById('session-stage-root')); SessionEngine.handleAnswerResult(true, currentWord, currentWord.word)");
  assert.equal(app.evaluate('SessionState.xpEarned'), 10);
  assert.equal(app.evaluate('SRSEngine.getWordProgress(currentWord.id).box'), 1);
  app.evaluate('SessionEngine.handleAnswerResult(true, currentWord, currentWord.word)');
  assert.equal(app.evaluate('SessionState.xpEarned'), 10);
  assert(![...app.timers.values()].some(timer => timer.delay === 1400));
  app.evaluate("SessionState.mode = 'practice'; SessionState.isAnswered = false; SessionEngine.handleAnswerResult(true, currentWord, currentWord.word)");
  assert.equal(app.evaluate('SRSEngine.getWordProgress(currentWord.id).box'), 1);
});

test('an immediate retry cannot erase a failed first attempt or promote the memory box', () => {
  const app = runtime();
  app.evaluate("globalThis.currentWord = { ...VOCAB.find(word => word.reviewed) }; SessionState.active = true; SessionState.isAnswered = false; SessionEngine.renderMultipleChoiceVi(currentWord, document.getElementById('session-stage-root')); SessionEngine.handleAnswerResult(false, currentWord, currentWord.word); SessionState.isAnswered = false; SessionEngine.handleAnswerResult(true, currentWord, currentWord.word)");
  assert.equal(app.evaluate('SRSEngine.getWordProgress(currentWord.id).box'), 1);
  assert.equal(app.evaluate('SessionState.correctFirstTry'), 0);
});

test('new sessions reset attempt flags without mutating the shared dictionary', () => {
  const app = runtime();
  app.evaluate("globalThis.currentWord = VOCAB.find(word => word.reviewed); SessionEngine.startSession([currentWord]); SessionState.queue[0]._hasMissedOnce = true;");
  assert.equal(app.evaluate('currentWord._hasMissedOnce'), undefined);
  app.evaluate('SessionEngine.startSession([currentWord])');
  assert.equal(app.evaluate('SessionState.queue[0]._hasMissedOnce'), false);
});

test('local date keys use the learner date rather than UTC date slicing', () => {
  const app = runtime();
  assert.equal(app.evaluate('localDateKey(new Date(2026, 10, 1, 0, 10))'), '2026-11-01');
  assert.equal(app.evaluate('localDateKey(new Date(2026, 10, 1, 23, 55))'), '2026-11-01');
});

test('summary next-session respects the selected level when no new words remain', () => {
  const app = runtime();
  app.boot();
  app.evaluate("AppState.user.studyLevel = 'B2'; for (const word of VOCAB.filter(item => item.level === 'B2')) AppState.wordProgress[word.id] = { box: 1, nextReview: 9999999999999, lastReview: 1, correctStreak: 1 }");
  app.elements.get('btn-summary-next-session').click();
  assert.equal(app.evaluate('SessionState.active'), false);
  app.evaluate("delete AppState.wordProgress[VOCAB.find(word => word.level === 'B2').id]");
  app.elements.get('btn-summary-next-session').click();
  assert.equal(app.evaluate('SessionState.active'), true);
  assert.equal(app.evaluate("SessionState.queue.length === 1 && SessionState.queue.every(word => word.level === 'B2')"), true);
});

test('keyboard shortcuts do not hijack native button keys, modifiers or held keys', () => {
  const app = runtime();
  app.boot();
  app.evaluate('SessionEngine.startSession([VOCAB[0]])');
  const dispatch = (key, target, extra = {}) => {
    const event = { key, target, preventDefault() {}, ...extra };
    app.callbacks.keydown.forEach(handler => handler(event));
  };
  dispatch('Enter', app.elements.get('btn-flashcard-continue'));
  assert.equal(app.evaluate('SessionState.currentIntroWord.id'), raw[0][12].id);
  const before = app.utterances.length;
  dispatch(' ', app.elements.get('btn-flashcard-continue'));
  dispatch('r', app.document.body, { ctrlKey: true });
  assert.equal(app.utterances.length, before);
  dispatch('Enter', app.document.body, { repeat: true });
  assert.equal(app.evaluate('SessionState.currentIntroWord.id'), raw[0][12].id);
  let repeatedDefaultPrevented = false;
  dispatch('Enter', app.elements.get('btn-flashcard-continue'), { repeat: true, preventDefault() { repeatedDefaultPrevented = true; } });
  assert.equal(repeatedDefaultPrevented, true);
  dispatch('Enter', app.document.body);
  assert.equal(app.evaluate('SessionState.currentIntroWord'), null);
});

test('typing Enter grades once, waits for feedback, then allows continuing', () => {
  const app = runtime();
  app.evaluate("AppState.user.reducedMotion = true; SessionEngine.startSession([VOCAB[0]]); SessionEngine.renderTypingQuestion(SessionState.queue[0], document.getElementById('session-stage-root'))");
  const input = app.elements.get('quiz-typing-input');
  input.value = raw[0][0];
  const enter = extra => input.listeners.keydown[0]({ key: 'Enter', preventDefault() {}, stopPropagation() {}, ...extra });
  enter({ repeat: true });
  assert.equal(app.evaluate('SessionState.isAnswered'), false);
  enter();
  assert.equal(app.evaluate('SessionState.isAnswered'), true);
  assert.equal(app.evaluate('SessionState.active'), true);
  assert.equal(app.evaluate('SessionState.xpEarned'), 10);
  enter();
  assert.equal(app.evaluate('SessionState.active'), false);
  assert.equal(app.evaluate('AppState.user.xp'), 10);
});

test('restoring an old backup resets stale daily counts and saves the normalized user', () => {
  const app = runtime();
  app.evaluate("const oldDate = new Date(); oldDate.setDate(oldDate.getDate() - 3); restoreFullBackup(JSON.stringify({ app: 'LexiUp', user: { xp: 50, streak: 7, todayLearnedCount: 9, lastStudyDate: localDateKey(oldDate) }, wordProgress: {}, history: [] }))");
  assert.equal(app.alerts.length, 0);
  assert.equal(app.evaluate('AppState.user.todayLearnedCount'), 0);
  assert.equal(app.evaluate('AppState.user.streak'), 0);
  assert.equal(app.evaluate('AppState.user.xp'), 50);
  assert.equal(JSON.parse(app.storage.get('lexiup_user_state')).todayLearnedCount, 0);
});

test('resetting progress allows a new study streak to begin on the same day', () => {
  const app = runtime();
  app.boot();
  app.evaluate('recordActivity(10, 1, 1)');
  app.elements.get('btn-reset-progress-modal').click();
  app.elements.get('btn-execute-reset').click();
  assert.equal(app.evaluate('AppState.user.streak'), 0);
  app.evaluate('recordActivity(10, 1, 1)');
  assert.equal(app.evaluate('AppState.user.streak'), 1);
  assert.equal(app.evaluate('AppState.user.todayLearnedCount'), 1);
});

test('session completion saves results even when canvas is unavailable', () => {
  const app = runtime({ canvasUnavailable: true });
  app.evaluate('SessionState.active = true; SessionState.totalCount = 1; SessionState.correctFirstTry = 1; SessionState.xpEarned = 10; SessionState.newWordCount = 1; SessionEngine.finishSession()');
  assert.equal(app.evaluate('AppState.user.xp'), 10);
  assert.equal(app.elements.get('sum-xp-earned').textContent, '+10 XP');
});

test('late answer callbacks cannot change progress after the session is closed', () => {
  const app = runtime();
  app.evaluate("SessionEngine.renderMultipleChoiceVi(VOCAB[0], document.getElementById('session-stage-root')); SessionState.active = false; SessionState.isAnswered = false; SessionEngine.handleAnswerResult(true, VOCAB[0], VOCAB[0].word)");
  assert.equal(app.evaluate('SessionState.xpEarned'), 0);
  assert.equal(app.evaluate('Object.keys(AppState.wordProgress).length'), 0);
});

test('finishing a session twice cannot award duplicate XP or learning history', () => {
  const app = runtime();
  app.evaluate("AppState.user.reducedMotion = true; SessionState.active = true; SessionState.totalCount = 2; SessionState.correctFirstTry = 2; SessionState.xpEarned = 20; SessionState.newWordCount = 2; SessionEngine.finishSession()");
  assert.equal(app.evaluate('AppState.user.xp'), 20);
  app.evaluate('SessionEngine.finishSession()');
  assert.equal(app.evaluate('AppState.user.xp'), 20);
  assert.equal(app.evaluate('AppState.user.todayLearnedCount'), 2);
  assert.equal(app.evaluate('AppState.history[0].wordsCount'), 2);
});

test('an open tab rolls over daily progress and resets a broken streak before recording study', () => {
  const app = runtime();
  app.evaluate("const previousDay = new Date(); previousDay.setDate(previousDay.getDate() - 3); AppState.user.lastStudyDate = localDateKey(previousDay); AppState.user.todayLearnedCount = 9; AppState.user.streak = 8; recordActivity(10, 1, 1)");
  assert.equal(app.evaluate('AppState.user.todayLearnedCount'), 1);
  assert.equal(app.evaluate('AppState.user.streak'), 1);
  assert.equal(app.evaluate('AppState.user.lastStudyDate'), app.evaluate('localDateKey()'));
  app.evaluate('recordActivity(10, 1, 1)');
  assert.equal(app.evaluate('AppState.user.todayLearnedCount'), 2);
  assert.equal(app.evaluate('AppState.user.streak'), 1);
});

test('semantic review fields and bilingual metadata are preserved in every reviewed entry', () => {
  const reviews = JSON.parse(fs.readFileSync(`${__dirname}/content-semantic-review.json`, 'utf8'));
  const fields = { pos: 2, meaningVi: 5, definitionEn: 6, example: 7, exampleVi: 8, collocations: 10, wordFamily: 11 };
  assert.equal(new Set(reviews.map(review => review.word)).size, reviews.length);
  for (const review of reviews) {
    const row = raw.find(item => item[0] === review.word);
    assert(row?.[12].semanticReviewed, review.word);
    for (const [field, index] of Object.entries(fields)) {
      if (field in review) assert.deepEqual(row[index], review[field], `${review.word}: ${field}`);
    }
    assert.deepEqual(row[12].examples[0], { en: row[7], vi: row[8] }, review.word);
    if (review.usageNote) assert.equal(row[12].usageNote, review.usageNote, review.word);
  }
  assert.equal(raw.filter(row => !row[12].reviewed).length, 0);
  assert.match(raw.find(row => row[0] === 'clip')[5], /đoạn phim/);
  assert.match(raw.find(row => row[0] === 'compliance')[5], /tuân thủ/);
  assert.match(raw.find(row => row[0] === 'flag')[5], /cờ/);
});

test('review activity does not count as newly learned vocabulary', () => {
  const app = runtime();
  app.evaluate('recordActivity(20, 2, 0)');
  assert.equal(app.evaluate('AppState.user.todayLearnedCount'), 0);
  assert.equal(app.evaluate('AppState.history[0].wordsCount'), 2);
  app.evaluate('recordActivity(10, 1, 1)');
  assert.equal(app.evaluate('AppState.user.todayLearnedCount'), 1);
});

test('native voices honor UK and rate settings; manual listening works when autoplay is disabled', () => {
  const app = runtime();
  app.evaluate("AudioManager.init(); AppState.user.speechEnabled = false; AudioManager.speak('appointment', 'uk', 0.8)");
  assert.equal(app.utterances.length, 1);
  assert.equal(app.utterances[0].lang, 'en-GB');
  assert.equal(app.utterances[0].rate, 0.8);
  assert.equal(app.utterances[0].voice.lang, 'en-GB');
  app.evaluate("AudioManager.speak('automatic', null, null, true)");
  assert.equal(app.utterances.length, 1);
});

test('native failure falls back exactly once, and cancelled speech never restarts stale audio', () => {
  const app = runtime();
  app.evaluate("AudioManager.speak('test')");
  const utterance = app.utterances[0];
  utterance.onerror({ error: 'network' });
  utterance.onerror({ error: 'network' });
  assert.equal(app.media.length, 1);
  app.evaluate('AudioManager.stop()');
  utterance.onerror({ error: 'network' });
  assert.equal(app.media.length, 1);
  assert(app.media[0].paused);
});

test('offline speech uses an installed English voice without mislabelling its accent', () => {
  const app = runtime({ online: false, voices: [
    { name: 'UK network', lang: 'en-GB', localService: false },
    { name: 'US installed', lang: 'en_US', localService: true },
    { name: 'Vietnamese', lang: 'vi-VN', localService: true }
  ] });
  app.evaluate("AudioManager.speak('appointment', 'uk')");
  assert.equal(app.utterances.length, 1);
  assert.equal(app.utterances[0].voice.name, 'US installed');
  assert.equal(app.utterances[0].lang, 'en-US');
  app.utterances[0].onstart();
  assert(app.elements.get('audio-status').textContent.includes('en-US (thay cho UK'));
  assert.equal(app.media.length, 0);
});

test('online speech keeps the requested accent and prefers a local voice for that accent', () => {
  const app = runtime({ voices: [
    { name: 'UK network', lang: 'en-GB', localService: false },
    { name: 'UK installed', lang: 'en_GB', localService: true }
  ] });
  app.evaluate("AudioManager.speak('appointment', 'uk')");
  assert.equal(app.utterances[0].voice.name, 'UK installed');
  assert.equal(app.utterances[0].lang, 'en-GB');
  app.utterances[0].onstart();
  assert(!app.elements.get('audio-status').textContent.includes('thay cho'));
  const otherAccent = runtime({ voices: [{ name: 'US installed', lang: 'en-US', localService: true }] });
  otherAccent.evaluate("AudioManager.speak('appointment', 'uk')");
  assert.equal(otherAccent.utterances.length, 0);
  assert.equal(otherAccent.media.length, 1);
});

test('a synchronous remote playback error clears media callbacks and cannot report false success', () => {
  const app = runtime({ native: false, throwAudioPlay: true });
  app.evaluate("AudioManager.speak('appointment')");
  assert.equal(app.media.length, 1);
  assert(app.media[0].paused);
  assert.equal(app.media[0].onplaying, null);
  assert.equal(app.media[0].onended, null);
  assert.equal(app.evaluate('currentActiveAudio'), null);
  assert.equal(app.elements.get('audio-status').dataset.failed, 'true');
});

test('silent native startup has a bounded watchdog and remote timeout gives actionable feedback', () => {
  const app = runtime();
  app.evaluate("AudioManager.speak('test')");
  const watchdog = [...app.timers.values()].find(timer => timer.delay === 2500);
  assert(watchdog);
  watchdog.handler();
  assert.equal(app.media.length, 1);
  const remoteTimeout = [...app.timers.values()].find(timer => timer.delay === 7000);
  assert(remoteTimeout);
  remoteTimeout.handler();
  assert.equal(app.elements.get('audio-status').dataset.failed, 'true');
  assert(app.elements.get('audio-status').textContent.includes('thử lại'));
});

test('offline with no speech support reports unavailability instead of silently failing', () => {
  const app = runtime({ native: false, online: false });
  assert.equal(app.evaluate('AudioManager.isAvailable()'), false);
  app.evaluate("AudioManager.speak('test')");
  assert.equal(app.media.length, 0);
  assert.equal(app.elements.get('audio-status').dataset.failed, 'true');
});

test('stale media cannot override a newer playback request', () => {
  const app = runtime({ native: false });
  app.evaluate("AudioManager.speak('first')");
  const first = app.media[0];
  const oldPlaying = first.onplaying;
  app.evaluate("AudioManager.speak('second')");
  app.media[1].onplaying();
  const status = app.elements.get('audio-status').textContent;
  oldPlaying();
  assert.equal(app.elements.get('audio-status').textContent, status);
  assert(first.paused);
});

test('repairs cover every previously flagged B1 and B2 entry without reusing sentence templates', () => {
  const repairs = fs.readFileSync(`${__dirname}/content-repairs.tsv`, 'utf8').trim().split(/\r?\n/).slice(1).map(line => line.split('|'));
  assert.equal(repairs.length, 829);
  assert.equal(new Set(repairs.map(row => row[0])).size, repairs.length);
  const prohibited = /We observed|They decided to|It is important to|It is an honor|soemthing|tkae|[\[\]\/]/i;
  for (const [word, pos, meaning, example, translation, collocation] of repairs) {
    const row = raw.find(item => item[0] === word);
    assert(row && row[12].reviewed, word);
    assert.equal(row[2], pos);
    assert.equal(row[5], meaning);
    assert.equal(row[7], example);
    assert.equal(row[8], translation);
    assert.equal(row[10][0], collocation);
    assert(!prohibited.test(example), word);
    assert(!row[12].qualityIssues.length, word);
  }
  const examples = raw.flatMap(row => row[12].examples || [{ en: row[7], vi: row[8] }]);
  assert.equal(new Set(examples.map(example => example.en.toLowerCase())).size, examples.length);
});

test('every edited primary example has a target span, including inflected phrases', () => {
  const app = runtime();
  assert.deepEqual(JSON.parse(app.evaluate('JSON.stringify(VOCAB.filter(word => word.reviewed && !findTargetSpan(word.example, word.word)).map(word => word.word))')), []);
  assert.equal(app.evaluate("findTargetSpan('We are committed to helping.', 'be committed to').text"), 'are committed to');
  assert.equal(app.evaluate("findTargetSpan('She tipped the waiter.', 'tip').text"), 'tipped');
  assert.equal(app.evaluate("findTargetSpan('The programmer arrived.', 'program')"), null);
  assert.equal(app.evaluate("findTargetSpan('The supervisor oversaw the work.', 'oversee').text"), 'oversaw');
  assert.equal(app.evaluate("findTargetSpan('The work was overseen by a supervisor.', 'oversee').text"), 'overseen');
  assert.equal(app.evaluate("findTargetSpan('The overseas office opened.', 'oversee')"), null);
  assert.equal(app.evaluate("findTargetSpan('She scanned the timetable.', 'scan').text"), 'scanned');
  assert.equal(app.evaluate("findTargetSpan('We put up two shelves.', 'shelf').text"), 'shelves');
  assert.equal(app.evaluate("getDistractors(VOCAB[0], 'word', 0).length"), 0);
});

test('hyphenated nouns do not overwrite phrasal verbs or their saved progress', () => {
  const app = runtime();
  for (const [verb, noun] of [['check in', 'check-in'], ['check out', 'check-out']]) {
    const verbRow = raw.find(row => row[0] === verb);
    const nounRow = raw.find(row => row[0] === noun);
    assert(verbRow && nounRow);
    assert.notEqual(verbRow[12].id, nounRow[12].id);
    assert.equal(nounRow[2], 'noun');
    app.context.testId = nounRow[12].id;
    assert.equal(app.evaluate('Object.keys(normalizeProgress({[testId]: {box: 2, lastReview: 10, nextReview: 20}})).length'), 1);
    app.evaluate('AppState.wordProgress[testId] = {box: 2, lastReview: 10, nextReview: 20}; saveState(); AppState.wordProgress = {}; initAppState();');
    assert.equal(app.evaluate('AppState.wordProgress[testId].box'), 2);
  }
});

test('failed progress saves roll back persisted settings and display a persistent warning', () => {
  const options = { failStorageKey: 'lexiup_word_progress' };
  const app = runtime(options);
  app.storage.set('lexiup_user_state', '{"xp":7}');
  assert.equal(app.evaluate('AppState.user.xp = 900; saveState()'), false);
  assert.equal(app.storage.get('lexiup_user_state'), '{"xp":7}');
  assert(app.elements.get('storage-status').textContent.includes('Chưa lưu'));
  delete options.failStorageKey;
  assert.equal(app.evaluate('saveState()'), true);
  assert.equal(app.elements.get('storage-status').textContent, '');
});

test('failed restore rolls back storage and leaves the current in-memory learner untouched', () => {
  const app = runtime({ failStorageKey: 'lexiup_word_progress' });
  app.storage.set('lexiup_user_state', '{"xp":7}');
  app.storage.set('lexiup_custom_words', '[]');
  const stateBefore = app.evaluate('JSON.stringify(AppState)');
  const storageBefore = JSON.stringify([...app.storage]);
  app.evaluate("restoreFullBackup(JSON.stringify({app:'LexiUp', user:{xp:900}, wordProgress:{'ox-0001':{box:1,lastReview:10,nextReview:20}}, customWords:[], history:[]}))");
  assert.equal(app.evaluate('JSON.stringify(AppState)'), stateBefore);
  assert.equal(JSON.stringify([...app.storage]), storageBefore);
  assert(app.alerts[0].includes('Chưa khôi phục'));
});

test('removed C1 progress remains recoverable but does not inflate active memory boxes', () => {
  const app = runtime();
  const removed = JSON.parse(fs.readFileSync(`${__dirname}/removed-c1.json`, 'utf8'));
  app.context.removedId = removed[0].id;
  app.evaluate('AppState.wordProgress[removedId] = {box: 5, lastReview: 10, nextReview: 20}; renderProgressView();');
  assert.equal(Number(app.elements.get('prog-total-mastered').textContent), 0);
  assert.equal(Number(app.elements.get('box-count-5').textContent), 0);
  assert.equal(app.evaluate('AppState.wordProgress[removedId].box'), 5);
});

test('content build is deterministic and never resurrects pruned C1 entries', () => {
  const crypto = require('node:crypto');
  const digest = filename => crypto.createHash('sha256').update(fs.readFileSync(`${__dirname}/${filename}`)).digest('hex');
  const filenames = ['index.html', 'removed-c1.json', 'content-audit.json', 'content-review-ledger.json', 'backups/index.before-education-2026-11-01.html'];
  const before = filenames.map(digest);
  require('node:child_process').execFileSync(process.execPath, [`${__dirname}/build-curriculum.js`], { cwd: __dirname });
  assert.deepEqual(filenames.map(digest), before);
  const report = JSON.parse(fs.readFileSync(`${__dirname}/content-audit.json`, 'utf8'));
  const ledger = JSON.parse(fs.readFileSync(`${__dirname}/content-review-ledger.json`, 'utf8'));
  assert.equal(ledger.length, original.length + 320);
  assert.equal(report.semanticPending.length, raw.filter(row => !row[12].reviewed).length);
  const reviews = JSON.parse(fs.readFileSync(`${__dirname}/content-semantic-review.json`, 'utf8'));
  assert.equal(report.semanticReviewedEntries, reviews.length);
  const previouslyEdited = new Set(['content-corrections.tsv', 'content-repairs.tsv'].flatMap(filename =>
    fs.readFileSync(`${__dirname}/${filename}`, 'utf8').trim().split(/\r?\n/).slice(1).map(line => line.split('|')[0])));
  assert.equal(report.semanticPending.length, 1393 - reviews.filter(review => !previouslyEdited.has(review.word)).length);
  assert.equal(report.baselineStructuralIssues.length, 0);
  assert.equal(report.structurallyScreenedOriginalEntries, original.length);
  assert.equal(ledger.filter(row => /full-review-outstanding/.test(row.status)).length, report.semanticPending.length);
});

test('a further C1 removal stays removed on rebuild while unknown edit names still fail', context => {
  const path = require('node:path');
  const os = require('node:os');
  const childProcess = require('node:child_process');
  const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'lexiup-curriculum-'));
  context.after(() => {
    assert.equal(path.dirname(path.resolve(fixture)), path.resolve(os.tmpdir()));
    assert(path.basename(fixture).startsWith('lexiup-curriculum-'));
    fs.rmSync(fixture, { recursive: true, force: true });
  });
  for (const filename of ['index.html', 'build-curriculum.js', 'curriculum-policy.json', 'content-corrections.tsv', 'content-repairs.tsv', 'content-glosses.tsv', 'content-semantic-review.json', 'content-expansion.tsv', 'content-additions.tsv']) {
    fs.copyFileSync(path.join(__dirname, filename), path.join(fixture, filename));
  }
  fs.mkdirSync(path.join(fixture, 'backups'));
  fs.copyFileSync(path.join(__dirname, 'backups/index.before-education-2026-11-01.html'), path.join(fixture, 'backups/index.before-education-2026-11-01.html'));
  const policyPath = path.join(fixture, 'curriculum-policy.json');
  const policy = JSON.parse(fs.readFileSync(policyPath, 'utf8'));
  assert(policy.c1Core.includes('compliance'));
  policy.c1Core = policy.c1Core.filter(word => word !== 'compliance');
  fs.writeFileSync(policyPath, JSON.stringify(policy));
  const build = () => childProcess.execFileSync(process.execPath, [path.join(fixture, 'build-curriculum.js')], { cwd: fixture, stdio: 'pipe' });
  build();
  const first = fs.readFileSync(path.join(fixture, 'index.html'), 'utf8');
  build();
  assert.equal(fs.readFileSync(path.join(fixture, 'index.html'), 'utf8'), first);
  assert(!JSON.parse(first.match(/const RAW_VOCAB = (\[[\s\S]*?\]);/)[1]).some(row => row[0] === 'compliance'));
  const reviewPath = path.join(fixture, 'content-semantic-review.json');
  const reviews = JSON.parse(fs.readFileSync(reviewPath, 'utf8'));
  reviews.push({ word: 'compliance-typo' });
  fs.writeFileSync(reviewPath, JSON.stringify(reviews));
  assert.throws(build, error => String(error.stderr).includes('Unknown editable headword: compliance-typo'));
});
