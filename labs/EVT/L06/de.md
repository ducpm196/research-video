# Lab EVT L06 — Bù trừ ngược thứ tự trong giao dịch dài (Saga)

Chạy tuần tự 3 bước `['reserve_stock', 'charge_card', 'ship_order']`. Khi bước `'ship_order'` thất bại, hoàn tác các bước đã chạy thành công theo thứ tự đảo ngược thành danh sách `'undo_<bước>'`.

Định dạng đầu ra (2 dòng):
`failed_at=<tên bước>`
`compensations=<danh sách>`

Chấm tự động:
```bash
bash labs/cham.sh EVT L06 duong_dan/bai_cua_ban.py
```
