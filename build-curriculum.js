const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');

const root = __dirname;
const htmlPath = path.join(root, 'index.html');
let html = fs.readFileSync(htmlPath, 'utf8');
const match = html.match(/const RAW_VOCAB = (\[[\s\S]*?\]);/);
assert(match, 'Missing embedded vocabulary');
let rows = JSON.parse(match[1]);
const backupDir = path.join(root, 'backups');
fs.mkdirSync(backupDir, { recursive: true });
const backupPath = path.join(backupDir, 'index.before-education-2026-11-01.html');
if (!fs.existsSync(backupPath)) fs.writeFileSync(backupPath, html);
const originalRows = JSON.parse(fs.readFileSync(backupPath, 'utf8').match(/const RAW_VOCAB = (\[[\s\S]*?\]);/)[1]);
const policyPath = path.join(root, 'curriculum-policy.json');
const policy = JSON.parse(fs.readFileSync(policyPath, 'utf8'));
const c1Core = policy.c1Core;
assert(Array.isArray(c1Core) && new Set(c1Core).size === c1Core.length, 'Invalid C1 policy');
const coreSet = new Set(c1Core);
const originalByWord = new Map(originalRows.map(row => [row[0], row]));
function editableRow(word) {
  const row = rows.find(item => item[0] === word);
  if (row) return row;
  const original = originalByWord.get(word);
  if (original?.[3] === 'C1' && !coreSet.has(word)) return null;
  assert.fail(`Unknown editable headword: ${word}`);
}
function structuralIssues(row) {
  const issues = [];
  if (!Array.isArray(row) || row.length < 12) return ['invalid-row-schema'];
  for (const [index, name] of [[0, 'word'], [2, 'pos'], [4, 'topic'], [5, 'meaning'], [6, 'definition'], [7, 'example'], [8, 'translation']]) {
    if (typeof row[index] !== 'string' || !row[index].trim()) issues.push(`missing-${name}`);
  }
  if (!['B1', 'B2', 'C1'].includes(row[3])) issues.push('invalid-level');
  if (!Array.isArray(row[10])) issues.push('invalid-collocations');
  return issues;
}
const baselineIssues = originalRows.flatMap((row, index) => {
  const issues = structuralIssues(row);
  return issues.length ? [{ id: `ox-${String(index + 1).padStart(4, '0')}`, word: row[0], issues }] : [];
});

function readTable(filename, width) {
  return fs.readFileSync(path.join(root, filename), 'utf8').trim().split(/\r?\n/).slice(1).map((line, index) => {
    const fields = line.split('|').map(value => value.trim());
    assert.equal(fields.length, width, `${filename}:${index + 2}: invalid columns`);
    assert(fields.every(Boolean), `${filename}:${index + 2}: empty field`);
    return fields;
  });
}

const glosses = readTable('content-glosses.tsv', 2);
assert.equal(new Set(glosses.map(fields => fields[0])).size, glosses.length, 'Duplicate gloss');
for (const [word, meaningVi] of glosses) {
  const row = editableRow(word);
  if (!row) continue;
  row[5] = meaningVi;
  row[12] = { ...row[12], glossEdited: true };
}
const corrections = readTable('content-corrections.tsv', 5);
assert.equal(new Set(corrections.map(fields => fields[0])).size, corrections.length, 'Duplicate correction');
const collocationCorrections = {
  appointment: ['make an appointment', 'a dental appointment'], assignment: ['complete an assignment', 'submit an assignment'],
  account: ['open a bank account', 'a savings account'], charge: ['an extra charge', 'a delivery charge'],
  staff: ['hotel staff', 'a member of staff'], kind: ['kind to someone', 'a kind gesture'],
  benefit: ['benefit from feedback', 'benefit the community'], board: ['board a plane', 'board a train'],
  approach: ['a practical approach', 'adopt a different approach', 'an approach to a problem'],
  concern: ['express concern', 'concern about safety'], claim: ['support a claim', 'a claim about a product'],
  resolve: ['resolve an issue', 'resolve a dispute'], sustain: ['sustain progress', 'sustain economic growth'],
  allocate: ['allocate resources', 'allocate time', 'allocate a budget'],
  collaborate: ['collaborate closely', 'collaborate on a project'],
  facilitate: ['facilitate learning', 'facilitate a smooth transition'],
  patient: ['patient with beginners', 'remain patient'], principal: ['the principal reason', 'the principal aim'],
  principle: ['a basic principle', 'in principle'], credit: ['credit someone with success', 'credit success to teamwork']
};
const senseNotes = {
  account: 'Ở mục này học nghĩa tài khoản ngân hàng; account còn có nghĩa bản tường thuật trong ngữ cảnh khác.',
  charge: 'Ở đây là danh từ khoản phí, không phải động từ sạc điện hay buộc tội.',
  kind: 'Ở đây là tính từ tử tế. Danh từ kind có nghĩa là loại.',
  board: 'Ở đây là động từ lên phương tiện. Danh từ board có thể là tấm bảng hoặc hội đồng.',
  relative: 'Ở đây là tính từ tương đối; danh từ a relative có nghĩa là người họ hàng.',
  view: 'Đang học động từ nhìn nhận: view something as something. Danh từ a view có thể là quan điểm hoặc quang cảnh.',
  feature: 'Đang học động từ có sự góp mặt/có một phần quan trọng; danh từ feature là đặc điểm hoặc tính năng.',
  award: 'Động từ: award someone a prize hoặc award a prize to someone. Danh từ an award là giải thưởng.',
  average: 'Đang học động từ đạt mức trung bình, không phải danh từ mức trung bình.',
  count: 'Ở đây là danh từ chỉ lần đếm hoặc tổng số; động từ count có nghĩa là đếm.',
  credit: 'Credit someone with something: ghi nhận công lao. Danh từ credit có thể là tín dụng hoặc sự công nhận.',
  principal: 'Ở đây là tính từ chính/chủ yếu. Danh từ principal là hiệu trưởng; principle viết khác và nghĩa là nguyên tắc.',
  patient: 'Ở đây là tính từ kiên nhẫn. Danh từ a patient có nghĩa là bệnh nhân.',
  staff: 'Nghĩa đang học là đội ngũ nhân viên, không phải nghĩa cây gậy.',
  tonne: 'Một tonne bằng 1.000 kg; ton có thể chỉ đơn vị khác tùy quốc gia.',
  comply: 'Comply with + quy định hoặc yêu cầu; không bỏ giới từ with.'
};
for (const [word, meaningVi, definitionEn, example, exampleVi] of corrections) {
  const row = editableRow(word);
  if (!row) continue;
  [row[5], row[6], row[7], row[8]] = [meaningVi, definitionEn, example, exampleVi];
  row[12] = { ...row[12], reviewed: true, source: 'LexiUp editorial 2026-11-01' };
  if (collocationCorrections[word]) row[10] = collocationCorrections[word];
  if (senseNotes[word]) row[12].usageNote = senseNotes[word];
}

const repairs = readTable('content-repairs.tsv', 6);
assert.equal(new Set(repairs.map(fields => fields[0])).size, repairs.length, 'Duplicate repair');
for (const [word, pos, meaningVi, example, exampleVi, collocation] of repairs) {
  const row = editableRow(word);
  if (!row) continue;
  [row[2], row[5], row[7], row[8], row[10], row[11]] = [pos, meaningVi, example, exampleVi, [collocation], null];
  row[12] = { ...row[12], reviewed: true, source: 'LexiUp editorial repair 2026-11-01',
    examples: [{ en: example, vi: exampleVi }] };
  if (word === 'next') row[6] = 'after this or after that; at the following time or stage';
}
const definitionRepairs = {
  centre: 'to make something the main subject or focus; to have something as the main focus',
  key: 'to enter information using a keyboard',
  experiment: 'to try a method or idea to learn what happens or find out what works',
  better: 'an improvement or something that is more satisfactory',
  tear: 'a drop of liquid that comes from your eye when you cry',
  capture: 'the act of catching a person or animal, or of recording images or information',
  catch: 'an act of catching, something caught, or a hidden disadvantage in an offer',
  negative: 'a disadvantage, a refusal, or a photographic image with reversed light and dark areas',
  positive: 'an advantage or a good feature of a situation',
  rail: 'a bar used as a support or barrier, or one of the steel bars that trains run on',
  touch: 'the sense of feeling through the skin, or an act of making light contact',
  respect: 'admiration for good qualities, or considerate treatment of another person',
  relation: 'a connection between people, things, or ideas',
  release: 'the act of making a product available or setting a person or animal free',
  master: 'a person with great skill, or a person with control over others',
  confidence: 'belief in your own abilities or trust in another person or thing',
  row: 'a line of people or things standing or arranged next to each other',
  devote: 'to give an amount of time or attention to something',
  process: 'to perform a series of operations on data or documents in order to handle them',
  pension: 'a regular sum paid by a government or employer to someone who has retired',
  sight: 'the ability to see; something seen, especially a view or scene that attracts attention'
};
for (const [word, definition] of Object.entries(definitionRepairs)) rows.find(row => row[0] === word)[6] = definition;
rows.find(row => row[0] === 'tear')[1] = '/tɪə(r)/';
rows.find(row => row[0] === 'subject')[1] = '/səbˈdʒekt/';

const semanticReviews = JSON.parse(fs.readFileSync(path.join(root, 'content-semantic-review.json'), 'utf8'));
assert.equal(new Set(semanticReviews.map(review => review.word)).size, semanticReviews.length, 'Duplicate semantic review');
const semanticFields = { pos: 2, meaningVi: 5, definitionEn: 6, example: 7, exampleVi: 8, collocations: 10, wordFamily: 11 };
for (const review of semanticReviews) {
  assert(typeof review.word === 'string' && review.word.trim(), 'Missing semantic review headword');
  for (const [field, value] of Object.entries(review)) {
    assert(['word', 'usageNote', ...Object.keys(semanticFields)].includes(field), `Unknown semantic field: ${field}`);
    if (field === 'collocations') assert(Array.isArray(value) && value.every(item => typeof item === 'string' && item.trim()), `Invalid collocations: ${review.word}`);
    else if (field === 'wordFamily') assert(value === null || (typeof value === 'object' && !Array.isArray(value) && Object.values(value).every(item => typeof item === 'string' && item.trim())), `Invalid word family: ${review.word}`);
    else assert(typeof value === 'string' && value.trim(), `Invalid ${field}: ${review.word}`);
  }
  const row = editableRow(review.word);
  if (!row) continue;
  for (const [field, index] of Object.entries(semanticFields)) if (field in review) row[index] = review[field];
  row[12] = { ...row[12], reviewed: true, semanticReviewed: true, source: 'LexiUp bilingual editorial review 2026-11-01',
    examples: [{ en: row[7], vi: row[8] }] };
  if (review.usageNote) row[12].usageNote = review.usageNote;
}

const topicNames = {
  money: 'Mua sắm & Tiền bạc', digital: 'Công nghệ & Đời sống', study: 'Học tập & Kỹ năng',
  daily: 'Gia đình & Đời sống', work: 'Công việc & Hợp tác', travel: 'Du lịch & Đi lại',
  health: 'Sức khỏe & Thói quen', environment: 'Môi trường & Cộng đồng', qualities: 'Cảm xúc, Tính cách & Thái độ'
};
const supplemental = readTable('content-additions.tsv', 11);
const supplementalNames = new Set(supplemental.map(fields => fields[1]));
const additions = [...readTable('content-expansion.tsv', 11), ...supplemental];
assert.equal(new Set(additions.map(fields => fields[1].toLowerCase())).size, additions.length, 'Duplicate addition');
for (const [level, word, pos, topic, meaningVi, definitionEn, example, exampleVi, example2, exampleVi2, usageNote] of additions) {
  let identifier = `${supplementalNames.has(word) ? 'supp' : 'edu'}-${level.toLowerCase()}-${word.replace(/[^a-z0-9]+/g, '-')}`;
  let row = supplementalNames.has(word) ? rows.find(item => item[0] === word) : rows.find(item => item[12]?.id === identifier);
  if (row && supplementalNames.has(word)) identifier = row[12].id;
  if (!row) {
    assert(!rows.some(item => item[0].toLowerCase() === word.toLowerCase()), `Duplicate headword: ${word}`);
    row = [];
    rows.push(row);
  }
  Object.assign(row, [word, '', pos, level, topicNames[topic] || topic, meaningVi, definitionEn, example, exampleVi,
    '[Ứng dụng thực tế]', [word], null, {
      id: identifier, reviewed: true, priority: 1, usageNote,
      examples: [{ en: example, vi: exampleVi }, { en: example2, vi: exampleVi2 }],
      source: 'LexiUp original examples 2026-11-01', levelBasis: 'editorial-estimate'
    }]);
}


const suspectPattern = /We observed\b|They decided to\b|It is an honor\b|It is important to\b|You must be\b|\bthe issue\b|\bthe word\b|\bsomeone\b|\bsomething\b|soemthing|tkae|\bcharater\b|\bcount ing\b|[\[\]()/]/i;
const unfinishedPattern = /\b(of|to|by|for|with|into|their|a|an|the)\s*[.!?]$/i;
for (const [index, row] of rows.entries()) {
  const metadata = row[12] || {};
  const issues = [];
  if (!metadata.reviewed && (suspectPattern.test(row[7]) || unfinishedPattern.test(row[7]))) issues.push('template-or-incomplete-example');
  if (!row[5] || row[5].toLowerCase() === row[0].toLowerCase()) issues.push('missing-translation');
  if (!row[7] || !row[8]) issues.push('missing-bilingual-example');
  row[12] = { ...metadata, id: metadata.id || `ox-${String(index + 1).padStart(4, '0')}`, qualityIssues: issues };
}
assert(c1Core.every(word => rows.some(row => row[0] === word && row[3] === 'C1')), 'Missing retained C1 word');
const active = rows.filter(row => row[3] !== 'C1' || coreSet.has(row[0]));
const archived = rows.filter(row => row[3] === 'C1' && !coreSet.has(row[0]));
rows = active;
const countLevels = list => list.reduce((counts, row) => ({ ...counts, [row[3]]: (counts[row[3]] || 0) + 1 }), {});
for (const row of rows) assert.deepEqual(structuralIssues(row), [], `Invalid active entry: ${row[0]}`);
assert.equal(new Set(rows.map(row => row[12].id)).size, rows.length, 'Duplicate stable ID');
assert.equal(new Set(rows.map(row => row[0].toLowerCase())).size, rows.length, 'Duplicate headword');

html = html.replace(match[0], `const RAW_VOCAB = ${JSON.stringify(rows).replace(/</g, '\\u003c')};`);
const coreDeclaration = `const C1_CORE = new Set(${JSON.stringify(c1Core)});`;
if (/const C1_CORE = new Set\([^\n]+\);/.test(html)) {
  html = html.replace(/const C1_CORE = new Set\([^\n]+\);/, coreDeclaration);
} else {
  html = html.replace('    const VOCAB = RAW_VOCAB.map', `    ${coreDeclaration}\n    const VOCAB = RAW_VOCAB.map`);
}
fs.writeFileSync(`${htmlPath}.curriculum.tmp`, html);
fs.renameSync(`${htmlPath}.curriculum.tmp`, htmlPath);
const removalPath = path.join(root, 'removed-c1.json');
const previousRemovals = fs.existsSync(removalPath) ? JSON.parse(fs.readFileSync(removalPath, 'utf8')) : [];
const removals = [...new Map([...previousRemovals, ...archived.map(row => ({
  id: row[12].id, word: row[0], reason: 'outside-editorial-core'
}))].map(item => [item.id, item])).values()];
fs.writeFileSync(removalPath, JSON.stringify(removals, null, 2) + '\n');
const report = {
  date: '2026-11-01', baseline: { B1: 791, B2: 1386, C1: 1302 },
  additions: countLevels(additions.map(fields => [null, null, null, fields[0]])),
  correctedEntries: corrections.length, repairedEntries: repairs.length, glossEditedEntries: glosses.length,
  semanticReviewedEntries: semanticReviews.length,
  structurallyScreenedOriginalEntries: policy.originalEntryCount,
  active: countLevels(active), removedC1: removals.length,
  reviewed: active.filter(row => row[12].reviewed).length,
  reviewedByLevel: countLevels(active.filter(row => row[12].reviewed)),
  unreviewed: active.filter(row => !row[12].reviewed).length,
  baselineStructuralIssues: baselineIssues,
  semanticPending: active.filter(row => !row[12].reviewed).map(row => ({
    id: row[12].id, word: row[0], level: row[3], glossEdited: !!row[12].glossEdited,
    reason: 'full-definition-example-translation-review-outstanding'
  })),
  pending: active.filter(row => row[12].qualityIssues.length).map(row => ({ id: row[12].id, word: row[0], level: row[3], issues: row[12].qualityIssues })),
  limitations: ['Editorial review is not independent linguistic certification.', 'Removed C1 entries were structurally screened and excluded, not all semantically rewritten.', 'Supplemental levels are teaching targets estimated by the editor, not official lexical CEFR certification.', 'C1 core is an editorial selection, not a corpus frequency ranking.', 'Browser layout and physical audio playback have not been verified.']
};
const editFields = { meaning: 5, definition: 6, example: 7, exampleTranslation: 8, pos: 2, ipa: 1, collocations: 10 };
report.editsAgainstOriginal = Object.fromEntries(Object.entries(editFields).map(([field, index]) => [field,
  active.filter(row => originalByWord.has(row[0]) && JSON.stringify(row[index]) !== JSON.stringify(originalByWord.get(row[0])[index])).length
]));
const removedIds = new Set(removals.map(row => row.id));
const activeByWord = new Map(active.map(row => [row[0], row]));
const ledger = originalRows.map((row, index) => {
  const id = `ox-${String(index + 1).padStart(4, '0')}`;
  const current = activeByWord.get(row[0]);
  return { id, word: row[0], level: row[3], status: removedIds.has(id) ? 'removed-from-curriculum' : current?.[12].semanticReviewed ? 'editorially-reviewed' : current?.[12].reviewed ? 'editorially-edited' : current?.[12].glossEdited ? 'gloss-edited-full-review-outstanding' : 'full-review-outstanding' };
});
ledger.push(...active.filter(row => !originalByWord.has(row[0])).map(row => ({ id: row[12].id, word: row[0], level: row[3], status: 'supplement-editorially-authored', levelBasis: row[12].levelBasis })));
fs.writeFileSync(path.join(root, 'content-review-ledger.json'), JSON.stringify(ledger, null, 2) + '\n');
fs.writeFileSync(path.join(root, 'content-audit.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({ ...report, pending: report.pending.length, semanticPending: report.semanticPending.length }, null, 2));
