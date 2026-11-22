# Lab EVT L01 — Tiến hoá lược đồ tương thích xuôi và ngược

Cho hai bản ghi sự kiện `v1 = {'order_id': 10, 'amount': 200}` và `v2 = {'order_id': 11, 'amount': 350, 'tier': 'vip'}`. Người nhận cũ bỏ qua trường lạ `tier` và chỉ cần đọc `order_id`, người nhận mới đọc `amount` với giá trị mặc định `'std'` nếu thiếu `tier` (tương thích hai chiều).

Định dạng đầu ra (2 dòng):
`old_reads_v2=<order_id nguyên>`
`new_reads_v1=<tier mặc định>`

Chấm tự động:
```bash
bash labs/cham.sh EVT L01 duong_dan/bai_cua_ban.py
```
