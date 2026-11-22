# Lab PLC L08 — Đánh dấu-quét theo chiều rộng (BFS) thu hồi vòng rác trên đồ thị vùng đống

Cài thuật toán đánh dấu-quét dùng hàng đợi tìm theo chiều rộng (`pop(0)`) từ gốc `'R'` trên đồ thị đối tượng `{'R': ['A'], 'A': ['B'], 'B': [], 'C': ['D'], 'D': ['C'], 'E': []}` để giữ lại các nút sống và liệt kê danh sách nút rác bị thu hồi theo thứ tự tăng dần.

Định dạng đầu ra (1 dòng):
`alive=<danh sách sắp xếp> reclaimed=<danh sách sắp xếp>`

Chấm tự động:
```bash
bash labs/cham.sh PLC L08 duong_dan/bai_cua_ban.py
```
