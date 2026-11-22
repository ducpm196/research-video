# Lab SDP L05 — SOLID 1: Đơn trách nhiệm và Đóng–Mở với chuỗi quy tắc tính tiền

Viết hàm `calc_total(base, rules)` nhận danh sách hàm/quy tắc: quy tắc thuế `+10%` áp trên `200 000` ra `220 000`, sau đó ghép thêm quy tắc giảm `-5%` thành `209 000` mà không sửa hàm cũ, in đúng 3 dòng:
1. `with_tax_only=220000`
2. `with_tax_and_discount=209000`
3. `core_modified=0`

Chấm tự động:
```bash
bash labs/cham.sh SDP L05 duong_dan/bai_cua_ban.py
```
