# Lab CLD L14 — Bù trừ nhả tài nguyên trong Saga đặt vé

Rạp có `15` ghế trống ban đầu (`available = 15`). Bước 1 giữ `2` ghế (`reserve`), nhưng bước 2 thanh toán thất bại nên phải kích hoạt hàm bù trừ nhả lại `2` ghế (`release`). In trạng thái tồn kho qua từng bước.

Định dạng đầu ra (2 dòng):
`after_reserve=<số nguyên>`
`after_compensate=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh CLD L14 duong_dan/bai_cua_ban.py
```
