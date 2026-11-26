# Lab WEB L12 — Node.js: ngân sách thời gian khung hình 60Hz và 120Hz

Đọc `stdin` `hz1=<n> hz2=<n> task_ms=<n>`. Tính ngân sách `1000 / Hz` và kiểm tra tác vụ `task_ms` có vượt ngân sách gây rớt khung ở mỗi tần số hay không.

In đúng 3 dòng: `budget_60hz_ms=<.1f>`, `budget_120hz_ms=<.1f>`, `task12ms_jank_at_60_120=<0|1>,<0|1>`.
Chấm tự động: `bash labs/cham.sh WEB L12 duong_dan/bai_cua_ban.js`
