# Lab TOC L08 — Kiểm chuẩn ôtômat đẩy xuống (PDA) trên toàn bộ chuỗi nhị phân dài 0..10

Cài ôtômat đẩy xuống (đẩy `'0'` vào ngăn xếp ở pha đầu, chuyển pha và lấy `'0'` ra khi gặp `'1'`, từ chối ký tự lạ hoặc `'0'` đứng sau `'1'`). Đối chiếu kết quả của hàm với ngôn ngữ `0^n 1^n` trên toàn bộ `2047` chuỗi nhị phân độ dài `0..10`, cùng hai mẫu `'00001111'` và `'01010101'`.

Định dạng đầu ra (1 dòng):
`tested=<số> all_match=<0 hoặc 1> ex_00001111=<0 hoặc 1> ex_01010101=<0 hoặc 1>`

Chấm tự động:
```bash
bash labs/cham.sh TOC L08 duong_dan/bai_cua_ban.py
```
