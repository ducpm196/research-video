# Lab SWF L01 — Kiểm chứng bất biến vòng lặp s = i*(i-1)//2

Đọc `stdin` `n=<int>`. Chạy vòng lặp `i = 0..n-1` cộng dồn `s += i`, tại mỗi bước và sau khi thoát vòng lặp kiểm khẳng định bất biến `s == i * (i - 1) // 2`.

In đúng 3 dòng: `invariant_holds_all=<0|1>`, `final_i=<d>`, `final_sum=<d>`.
Chấm tự động: `bash labs/cham.sh SWF L01 duong_dan/bai_cua_ban.py`
