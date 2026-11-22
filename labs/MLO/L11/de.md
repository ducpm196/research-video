# Lab MLO L11 — Lượng tử hoá đối xứng số nguyên 8 bit (int8) và nén bộ nhớ trong (RAM)

Lượng tử hoá giá trị `-0.9` về số nguyên 8 bit đối xứng (`int8`) trên khoảng `[-2, 2]` (giá trị nguyên lớn nhất `q_max = 127`), tính sai số khôi phục và so bộ nhớ trong (`RAM`) cho mô hình `13 tỉ` tham số giữa dạng số thực dấu phẩy động 32 bit (`fp32`, `4 byte/tham số`) và số nguyên 8 bit (`int8`, `1 byte/tham số`).

Định dạng đầu ra (2 dòng):
`q=<số nguyên> deq=<4 chữ số> err=<4 chữ số>`
`fp32_gb=<số nguyên> int8_gb=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh MLO L11 duong_dan/bai_cua_ban.py
```
