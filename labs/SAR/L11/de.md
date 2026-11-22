# Lab SAR L11 — Khoá tài khoản báo cáo ở chế độ chỉ đọc trên SQLite

Mở cơ sở dữ liệu `sqlite3` tạo một bảng hoá đơn chứa số tiền `950`, sau đó bật chế độ chỉ đọc (`PRAGMA query_only = ON`) của SQLite. Kiểm chứng xem lệnh đọc có lấy ra đúng số tiền `950` không (`read_allowed`), lệnh xoá có bị chặn và ném ngoại lệ lỗi vận hành không (`write_blocked`), và qua đó xác định phạm vi thiệt hại đã được khoanh vùng hay chưa (`blast_contained`).

Định dạng đầu ra (3 dòng):
`read_allowed=<0|1>`
`write_blocked=<0|1>`
`blast_contained=<0|1>`

Chấm tự động:
```bash
bash labs/cham.sh SAR L11 duong_dan/bai_cua_ban.py
```
