# Lab WEB L02 — Node.js: CSS Box Model và điểm ưu tiên bộ chọn

Đọc `stdin` `w=<n> pad=<n> bd=<n> id_a=<n> id_b=<n>` (Node: `const fs = require('fs'); const kv = Object.fromEntries(fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(s => s.split('=')));`). Tính bề rộng hiển thị thực tế theo `content-box`, `border-box` và so độ ưu tiên thành phần ID.

In đúng 3 dòng: `content_box_w=<d>`, `border_box_w=<d>`, `id_beats_2class=<0|1>`.
Chấm tự động: `bash labs/cham.sh WEB L02 duong_dan/bai_cua_ban.js`
