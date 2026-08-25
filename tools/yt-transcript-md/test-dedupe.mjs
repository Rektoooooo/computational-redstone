/**
 * Loads the REAL background.js (with a chrome stub) and exercises the pure
 * transcript functions. Run: node test-dedupe.mjs
 */
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const SOURCE = '/Users/WorkSebas/Downloads/yt-transcript-md/background.js';

const noop = () => {};
const sandbox = {
  chrome: {
    runtime: { onMessage: { addListener: noop } },
    commands: { onCommand: { addListener: noop } },
    tabs: {}, storage: {}, downloads: {}, scripting: {}
  },
  console
};
vm.createContext(sandbox);
vm.runInContext(readFileSync(SOURCE, 'utf8'), sandbox);

const { dropRepeatedPass, groupSegments, buildMarkdown } = sandbox;

let failures = 0;
function check(name, condition, detail) {
  if (condition) {
    console.log(`  PASS  ${name}`);
  } else {
    failures++;
    console.log(`  FAIL  ${name}${detail ? ' -> ' + detail : ''}`);
  }
}

/* Build a plausible transcript: one segment every 3 seconds. */
function makeTranscript(count) {
  const segments = [];
  for (let i = 0; i < count; i++) {
    segments.push({ start: i * 3, text: `line number ${i}` });
  }
  return segments;
}

console.log('\ndropRepeatedPass');

const single = makeTranscript(200);
const doubled = single.concat(single.map((s) => ({ ...s })));

check('doubled input is halved', dropRepeatedPass(doubled).length === single.length,
  `got ${dropRepeatedPass(doubled).length}, want ${single.length}`);

check('doubled input keeps the FIRST pass',
  JSON.stringify(dropRepeatedPass(doubled)) === JSON.stringify(single));

check('clean input is untouched',
  JSON.stringify(dropRepeatedPass(single)) === JSON.stringify(single));

check('empty input is safe', dropRepeatedPass([]).length === 0);
check('single segment is safe', dropRepeatedPass([{ start: 0, text: 'x' }]).length === 1);

/* A caption arriving slightly out of order must NOT truncate the file. */
const jittered = makeTranscript(100);
jittered[50] = { start: jittered[49].start - 2, text: 'late caption' };
check('2s jitter does not truncate', dropRepeatedPass(jittered).length === 100,
  `got ${dropRepeatedPass(jittered).length}`);

/* Tripled input: the first backward jump wins, so we still keep exactly one pass. */
const tripled = single.concat(single, single);
check('tripled input still yields one pass', dropRepeatedPass(tripled).length === single.length);

console.log('\ngroupSegments seam handling');

/* Even if a duplicate slipped past, the chunker must not glue the seam together. */
const seam = [
  { start: 1000, text: 'the very end of the video' },
  { start: 0, text: 'hi guys and welcome back' }
];
const seamChunks = groupSegments(seam);
check('backward jump starts a new chunk', seamChunks.length === 2,
  `got ${seamChunks.length} chunk(s): ${JSON.stringify(seamChunks)}`);

console.log('\nend to end (buildMarkdown)');

const info = {
  title: 'Test Video', author: 'Someone', pageUrl: 'https://youtu.be/x',
  lengthSeconds: 600, videoId: 'x'
};
const md = buildMarkdown(info, 'English (auto-generated)', dropRepeatedPass(doubled), true);

const stamps = [...md.matchAll(/\*\*\[([\d:]+)\]\*\*/g)].map((m) => {
  const parts = m[1].split(':').map(Number);
  return parts.reduce((acc, p) => acc * 60 + p, 0);
});
const goesBackwards = stamps.some((t, i) => i > 0 && t < stamps[i - 1]);
check('no backward timestamp in output', !goesBackwards);

const firstLineHits = (md.match(/line number 0\b/g) || []).length;
check('first caption appears exactly once', firstLineHits === 1, `appeared ${firstLineHits}x`);

const lastLineHits = (md.match(/line number 199\b/g) || []).length;
check('last caption appears exactly once', lastLineHits === 1, `appeared ${lastLineHits}x`);

console.log(failures === 0 ? '\nAll checks passed.\n' : `\n${failures} check(s) FAILED.\n`);
process.exit(failures === 0 ? 0 : 1);
