# Lab SEP L08 — Luật 3 bước chọn phương án đa bên: ràng buộc không âm, tổng điểm, và ưu tiên bên yếu thế

Cho điểm tác động trên thang `[-2, 2]` tới 4 bên `[công_ty, khách, nhà_hàng, tài_xế]` của ba phương án: `'P1': [2, 2, 1, -1]`, `'P2': [1, 1, 2, 0]`, `'P3': [0, 1, 1, 2]`. Áp dụng đúng luật trong bài: (1) chỉ giữ phương án có điểm nhỏ nhất `>= 0`; (2) xếp theo `(tổng điểm, điểm của bên yếu thế nhất [tài_xế])`.

Định dạng đầu ra (1 dòng):
`filtered=<danh sách tên> fair_pick=<tên phương án>`

Chấm tự động:
```bash
bash labs/cham.sh SEP L08 duong_dan/bai_cua_ban.py
```
