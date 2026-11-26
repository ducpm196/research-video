# Lab BEP L02 — Bộ kiểm đồ thị kiến trúc C4/UML & Đường găng

Đọc từ `stdin` 2 dòng:
- Dòng 1: `nodes=<name:ms,name:ms,...>`
- Dòng 2: `edges=<u->v,u->v,...>`

Yêu cầu:
1. Dùng thuật toán Kahn (sắp xếp tô pô) kiểm tra đồ thị phụ thuộc có hướng không chu trình (`has_cycle = 0` hoặc `1`).
2. Nếu không có chu trình (`has_cycle=0`), tính độ trễ đường găng `critical_ms` qua quy hoạch động tô pô `dp[v] = nodes[v] + max(dp[u])`; nếu có chu trình ghi `critical_ms=-1`.
3. In đúng 3 dòng: `node_count=<int>`, `has_cycle=<0_hoặc_1>`, `critical_ms=<int>`.

Chấm tự động: `bash labs/cham.sh BEP L02 duong_dan/bai_cua_ban.py`
