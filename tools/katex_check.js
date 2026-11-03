// Đọc JSON [{id, tex, display}] từ stdin, parse bằng KaTeX (throwOnError), in JSON [{id, error}] các lỗi.
const katex = require('./vendor/node_modules/katex');
const macros = require('./katex_macros.json');
let buf = '';
process.stdin.on('data', d => (buf += d));
process.stdin.on('end', () => {
  const items = JSON.parse(buf);
  const errors = [];
  for (const it of items) {
    try {
      katex.renderToString(it.tex, { displayMode: !!it.display, throwOnError: true, strict: 'ignore', macros: { ...macros } });
    } catch (e) {
      errors.push({ id: it.id, tex: it.tex, error: String(e.message || e) });
    }
  }
  process.stdout.write(JSON.stringify(errors));
});
