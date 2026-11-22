# Lab WEB L03 — Node.js thật: kiểm chứng thứ tự 1, 4, 3, 2 trên V8 Event Loop

Viết tập lệnh Node.js thực thi đồng bộ (`1`, `4`), `Promise.resolve().then(...)` (`3`) và `setTimeout(..., 0)` (`2`) vào mảng `order` để chứng minh microtask luôn chạy trước macrotask, in đúng 3 dòng:
1. `sync_done=1`
2. `event_loop_order=1,4,3,2`
3. `micro_before_macro=1`

Chấm tự động:
```bash
bash labs/cham.sh WEB L03 duong_dan/bai_cua_ban.js
```
