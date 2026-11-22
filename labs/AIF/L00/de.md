# Lab AIF L00 — Tác tử phản xạ ba ô và đếm không gian trạng thái

Liệt kê mọi trạng thái của phòng 3 ô (vị trí `pos` là `0`, `1` hoặc `2`; độ bẩn 3 ô `dirty_0`, `dirty_1`, `dirty_2` mỗi ô là `0` hoặc `1`). Khởi đầu máy ở ô `0` với trạng thái bụi `[1, 0, 1]`, chạy mô phỏng tác tử phản xạ: hút nếu ô hiện tại bẩn, ngược lại đi sang ô kế tiếp bên phải tới khi cả 3 ô sạch.

Định dạng đầu ra cần in đúng 1 dòng:
`total_states=<số nguyên> clean=<danh sách> steps=<số bước>`

Chấm tự động:
```bash
bash labs/cham.sh AIF L00 duong_dan/bai_cua_ban.py
```
