# Lab MLO L07 — Phát hành chạy bóng: ghi nhật ký độ lệch mà không ảnh hưởng người dùng

Trong chế độ chạy bóng song song, cho dự đoán mô hình cũ `old_p = [0.2, 0.8, 0.6, 0.3, 0.9]` và mới `new_p = [0.3, 0.7, 0.4, 0.3, 0.8]` (ngưỡng `0.5`). Trả kết quả cho người dùng từ bản cũ và ghi nhật ký số yêu cầu lệch nhãn.

Định dạng đầu ra:
`served=old disagree=<số>/5`

Chấm tự động:
```bash
bash labs/cham.sh MLO L07 duong_dan/bai_cua_ban.py
```
