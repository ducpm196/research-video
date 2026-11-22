# Lab IRS L05 — Học để xếp hạng: mất mát theo cặp và trọng số vị trí đầu

Tính mất mát theo cặp `ln(1 + exp(-(s_a - s_b)))` khi hai điểm đúng thứ tự `(s_a=2.5, s_b=1.2)` so với đảo ngược `(1.2, 2.5)`. Sau đó tính độ giảm DCG khi tráo cặp vị trí `(1, 2)` (mức `4` và `2`) so với cặp `(3, 4)` (mức `1` và `0`) trong dãy `[4, 2, 1, 0]`.

Định dạng đầu ra (2 dòng):
`loss_ok=<3 chữ số> loss_swap=<3 chữ số>`
`dcg_drop_12=<3 chữ số> dcg_drop_34=<3 chữ số>`
