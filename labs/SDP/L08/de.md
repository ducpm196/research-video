# Lab SDP L08 — Mẫu khởi tạo: Minh họa bẫy trạng thái chung ở Singleton vs Instance mới

Viết bộ đếm `Singleton` dùng chung và `Counter()` độc lập: nếu bài kiểm thử A tăng 1 rồi bài B tăng 1, Singleton cho kết quả lệch `2` (phụ thuộc thứ tự), còn tạo mới luôn cho `1`, in đúng 3 dòng:
1. `singleton_a_then_b=1,2`
2. `isolated_a_then_b=1,1`
3. `order_leak=1`

Chấm tự động:
```bash
bash labs/cham.sh SDP L08 duong_dan/bai_cua_ban.py
```
