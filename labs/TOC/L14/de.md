# Lab TOC L14 — So sánh bùng nổ nhánh quay lui 2^n và số tập vị trí n + 1 trên mẫu dài n=25

Với mẫu `(a?){n}a{n}` ở `n = 25` (chuỗi `'a'*25`): tính số nhánh quay lui tệ nhất `2^n`, kích thước tập vị trí chạy song song của máy Thompson `n + 1`, và tổng số bước kiểm tra trên toàn chuỗi dài `n` (`n * (n + 1)`).

Định dạng đầu ra (1 dòng):
`backtrack=<số nguyên> subset_pos=<số nguyên> linear_checks=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh TOC L14 duong_dan/bai_cua_ban.py
```
