# Lab SDP L00 — Đo độ phức tạp vòng McCabe bằng cây cú pháp AST thật

Viết chương trình Python dùng thư viện chuẩn `ast` đếm số nút rẽ nhánh (`If, For, While, BoolOp`) của hàm chứa 2 `if`, 1 `for`, 1 `and`, tính `M = 1 + nhánh = 5`, in đúng 3 dòng:
1. `decision_points=4`
2. `mccabe_complexity=5`
3. `max_recommended_le10=1`

Chấm tự động:
```bash
bash labs/cham.sh SDP L00 duong_dan/bai_cua_ban.py
```
