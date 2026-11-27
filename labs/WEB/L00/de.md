# Lab WEB L00 — Node.js: tính TTFB qua TCP + TLS + HTTP với RTT

Đọc `stdin` `rtt_near=<n> rtt_far=<n> apis=<n>` (Node: `const fs = require('fs'); const kv = Object.fromEntries(fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(s => s.split('=')));`). Tính TTFB (3 vòng RTT cho TCP, TLS, HTTP GET) tại `rtt_near`, tổng thời gian của `rtt_far` cộng `apis` lượt gọi API tuần tự, và số chặng bắt tay.

In đúng 3 dòng: `ttfb_50ms=<d>`, `remote_200ms_4api=<d>`, `roundtrips_handshake=3`.
Chấm tự động: `bash labs/cham.sh WEB L00 duong_dan/bai_cua_ban.js`
