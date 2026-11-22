# Lab PLC L00 — Phân biệt lỗi pha cú pháp (pha 2) và pha ngữ nghĩa (pha 3) trên danh sách từ tố

Cài hàm kiểm tra cho danh sách từ tố (token): pha cú pháp (pha 2) duyệt ngăn xếp/độ sâu ngoặc kiểm tra đóng mở cân bằng và không âm dọc chuỗi `['(', '1', '+', '2']`; pha ngữ nghĩa (pha 3) tra bảng biến đã khai báo `{'x': 1}` với biến `'y'`.

Định dạng đầu ra (1 dòng):
`syn_err=<0 hoặc 1> sem_err=<0 hoặc 1>`

Chấm tự động:
```bash
bash labs/cham.sh PLC L00 duong_dan/bai_cua_ban.py
```
