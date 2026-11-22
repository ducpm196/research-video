# Lab SDP L06 — SOLID 2: Phát hiện vi phạm nguyên lý thay thế Liskov (Rectangle vs Square)

Viết hàm `check_rect(r)` gán `r.w = 5; r.h = 4` rồi kỳ vọng `r.area() == 20`: kiểm chứng `Rectangle` đạt `20`, còn `Square` (ép `w=h`) trả `16` gây phá hậu điều kiện, in đúng 3 dòng:
1. `rect_area=20`
2. `square_area=16`
3. `lsp_violated=1`

Chấm tự động:
```bash
bash labs/cham.sh SDP L06 duong_dan/bai_cua_ban.py
```
