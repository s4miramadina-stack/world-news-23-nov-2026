// Writes the front page for Monday 23 November 2026 (entry.png, drawn by draw.py)
// to the output directory. Standard library only; the bytes are copied unchanged,
// so every run produces an identical file.
import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';

if (!existsSync(source)) {
  console.error('entry.png is missing next to main.ts; run draw.py first');
  process.exit(1);
}
if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true });

copyFileSync(source, join(outDir, 'entry.png'));
console.log(`wrote ${join(outDir, 'entry.png')}`);
