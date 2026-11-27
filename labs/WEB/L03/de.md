# Lab WEB L03 — Node.js: kiểm chứng thứ tự trên V8 Event Loop

Đọc `stdin` `sync1=<n> macro=<n> micro=<n> sync2=<n>` (Node: `const fs = require('fs'); const kv = Object.fromEntries(fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(s => s.split('=')));`, dùng hàm mũi tên `() => ...`). Chạy hàm đồng bộ, `Promise.resolve().then(...)` (tác vụ vi mô / micro) và `setTimeout(..., 0)` (tác vụ hẹn giờ / macro) để xuất thứ tự thực thi thực tế.

In đúng 3 dòng: `sync_done=<0|1>`, `event_loop_order=<a,b,c,d>`, `micro_before_macro=<0|1>`.
Chấm tự động: `bash labs/cham.sh WEB L03 duong_dan/bai_cua_ban.js`
