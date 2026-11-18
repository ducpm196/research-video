# Lab BNX L02 — Mã hoá tay một bản tin ba trường

Một bản tin ghi nhận lần rút tiền ATM (số minh hoạ) có ba trường:

| số hiệu | kiểu dây | giá trị |
|---|---|---|
| 1 | 0 (số nguyên biến độ dài) | 20 |
| 6 | 0 (số nguyên biến độ dài) | 70000 |
| 7 | 2 (độ dài rồi byte) | chuỗi `ATM01` (5 ký tự) |

Viết `mau.py` (Python) gồm hàm `varint(n)` và hàm `field(num, wire, payload)` như trong bài (khoá trường = `num << 3 | wire`), rồi ghép ba trường theo thứ tự trên thành một dãy byte `m` và in đúng hai dòng:

1. `m.hex(" ")` — các byte thập lục phân cách nhau bằng dấu cách;
2. `<số byte> byte` — độ dài của `m`.

Gợi ý tính tay trước: khoá của trường 6 là 6 × 8 + 0 = 48 = `30`; 70000 chia thành các nhóm 7 bit thấp trước. Chuỗi `ATM01` mã hoá là `3a 05` rồi 5 byte chữ.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L02 mau.py`.
