# Lab SEP L04 — Kiểm tra chuỗi phụ thuộc giấy phép MIT/Apache vs GPL-3.0 trên danh sách gói

Duyệt danh sách phụ thuộc `[('auth', 'MIT'), ('fmt', 'Apache-2.0'), ('csv_fast', 'GPL-3.0'), ('http', 'BSD-3-Clause')]`, lọc tên các gói dùng giấy phép buộc mở mã (`GPL...`) khi phân phối phần mềm đóng.

Định dạng đầu ra (1 dòng):
`total_deps=<số nguyên> closed_app_conflict=<danh sách tên gói>`

Chấm tự động:
```bash
bash labs/cham.sh SEP L04 duong_dan/bai_cua_ban.py
```
