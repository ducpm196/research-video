# Lab PLC L06 — Giải ràng buộc kiểu bằng thuật toán hợp nhất thay thế lặp

Cho danh sách ràng buộc kiểu giữa các biến chưa biết và kiểu cụ thể `constraints = [('ret', 't_x'), ('t_x', 't_y'), ('t_y', 'int')]`. Chạy vòng lặp hợp nhất thế dần cho tới khi cả `'t_x'` và `'ret'` đều được suy ra kiểu `'int'`.

Định dạng đầu ra (1 dòng):
`inferred_tx=<kiểu> ret=<kiểu>`

Chấm tự động:
```bash
bash labs/cham.sh PLC L06 duong_dan/bai_cua_ban.py
```
