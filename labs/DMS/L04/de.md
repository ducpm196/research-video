# Lab DMS L04 — Quy nạp: kiểm hai bước cho công thức tổng bình phương

Viết `quynap.py` (Python 3.11 trở lên); chạy: `python quynap.py`.

Khẳng định cần chứng minh bằng quy nạp: tổng các bình phương 1² + 2² + ... + n² bằng n(n+1)(2n+1)/6. Đặt `tong(n)` là tổng cộng trực tiếp bằng vòng lặp, `ct(n) = n*(n+1)*(2*n+1)//6`.

In đúng bảy dòng:
1. `co so: <tong(1)> <ct(1)>`
2. bốn dòng, với n = 1, 2, 3, 4: `quy nap <n>-><n+1>: <tong(n)> + <(n+1)^2> = <tong(n) + (n+1)^2>, cong thuc <ct(n+1)>`
3. `kiem 1..1000: dung` nếu `tong(n) == ct(n)` với mọi n từ 1 đến 1000, ngược lại `kiem 1..1000: sai`
4. Một công thức SAI: `sai(n) = n*(n+1)*(n+2)//6`. Tìm n đầu tiên mà `tong(n) != sai(n)`, rồi in `cong thuc sai: co so dung, sai dau tien o n=<n>` (ở n = 1 công thức sai vẫn đúng: đó là lý do bước cơ sở đơn độc không đủ).

Gợi ý: `str(...)` đổi số thành chữ để ghép bằng dấu `+`; dùng vòng `while` cho phần 4.

Chấm: `bash labs/cham.sh DMS L04 quynap.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
