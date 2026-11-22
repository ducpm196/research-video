# Lab TOC L04 — Kiểm tra đầy đủ điều kiện tách bơm x, y, z cho p=5 trên 0^5 1^5

Với độ dài bơm `p = 5`, chuỗi `s = '0000011111'` và phép tách `x = '00'`, `y = '00'`, `z = '011111'`: viết chương trình kiểm tra đồng thời các điều kiện `x + y + z == s`, `len(x + y) <= p`, `len(y) >= 1`, sau đó bơm lặp `y` thành `i = 2` (`x + y*2 + z`) và kiểm tra chuỗi mới có phá vỡ tính bằng nhau số chữ `'0'` và `'1'` hay không.

Định dạng đầu ra (1 dòng):
`split_ok=<0 hoặc 1> pumped_len=<số nguyên> valid=<0 hoặc 1>`

Chấm tự động:
```bash
bash labs/cham.sh TOC L04 duong_dan/bai_cua_ban.py
```
