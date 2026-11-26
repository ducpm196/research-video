# Lab WEB L04 — Node.js: đo thời gian chờ tuần tự vs Promise.all

Đọc `stdin` `times=<t1,t2,...>`. Tính tổng thời gian khi chờ tuần tự từng tác vụ so với thời gian lớn nhất khi chạy đồng thời qua `Promise.all` và hệ số tăng tốc.

In đúng 3 dòng: `seq_ms=<d>`, `parallel_ms=<d>`, `speedup=<.1f>x`.
Chấm tự động: `bash labs/cham.sh WEB L04 duong_dan/bai_cua_ban.js`
