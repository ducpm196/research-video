# Lab EVT L03 — Bảo toàn phiên bản đơn điệu khi gói tin đến lệch thứ tự

Cho chuỗi cập nhật địa chỉ đến lệch thứ tự `[(2, 'HN'), (5, 'DN'), (3, 'HCM')]` theo cặp `(version, city)`. Chỉ áp dụng bản cập nhật có `version` lớn hơn phiên bản hiện đang giữ (trả về phiên bản và thành phố cuối).

Định dạng đầu ra (2 dòng):
`final_ver=<số nguyên>`
`final_city=<tên>`

Chấm tự động:
```bash
bash labs/cham.sh EVT L03 duong_dan/bai_cua_ban.py
```
