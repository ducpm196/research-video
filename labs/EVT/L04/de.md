# Lab EVT L04 — Gấp chuỗi sự kiện (Event Sourcing) và ảnh chụp định kỳ

Gấp danh sách biến động số dư `[+250, -80, +120, -40]` từ `0` để ra số dư hiện tại. Sau đó với kho `200 000` sự kiện chụp ảnh mỗi `500` sự kiện, tính tổng số ảnh chụp và số sự kiện tối đa cần phát lại khi phục hồi.

Định dạng đầu ra (3 dòng):
`balance=<số nguyên>`
`snapshots=<số nguyên>`
`max_replay=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh EVT L04 duong_dan/bai_cua_ban.py
```
