# Lab WEB L03 — Node.js: kiểm chứng thứ tự trên V8 Event Loop

Đọc `stdin` `sync1=<n> macro=<n> micro=<n> sync2=<n>`. Chạy hàm đồng bộ, `Promise.resolve().then(...)` (microtask) và `setTimeout(..., 0)` (macrotask) để xuất thứ tự thực thi thực tế.

In đúng 3 dòng: `sync_done=<0|1>`, `event_loop_order=<a,b,c,d>`, `micro_before_macro=<0|1>`.
Chấm tự động: `bash labs/cham.sh WEB L03 duong_dan/bai_cua_ban.js`
