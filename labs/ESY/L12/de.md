# Lab ESY L12 — Watchdog timer và đỉnh ngăn xếp 0xA5

Đọc `wdt_ms stack_B depth|c0,c1,...` từ stdin (ví dụ `90 16 11|50,75,110,60`). Đếm số chu kỳ vượt `wdt_ms` và số byte ngăn xếp bị ghi đè.
In đúng 1 dòng `wdt_resets=<int> stack_used_B=<int>`.
