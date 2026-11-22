# Lab CLD L13 — Rò rỉ bí mật trong các lớp ảnh bất biến

Mô phỏng 3 lớp ảnh cộng gộp: lớp 1 tạo `{'app.py', 'key.env'}`, lớp 2 sao chép thêm `'cfg.yml'`, lớp 3 xoá `'key.env'` khỏi giao diện cuối (`visible`). Kiểm tra xem tệp nhìn thấy cuối cùng có còn `'key.env'` không và lịch sử toàn bộ các lớp ảnh có vẫn còn giữ `'key.env'` không.

Định dạng đầu ra (2 dòng):
`in_final_view=<1 hoặc 0>`
`leaked_in_layers=<1 hoặc 0>`

Chấm tự động:
```bash
bash labs/cham.sh CLD L13 duong_dan/bai_cua_ban.py
```
