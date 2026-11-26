# Lab CPR L02 — Kiểm chứng truyền tham trị và cộng dồn khung ngăn xếp qua stdin

Viết chương trình C chuẩn C11 đọc 5 số nguyên từ `stdin`: `v sum_n f1 f2 f3`.
Cài hàm `double_val(int x)` nhân đôi trên bản sao, hàm đệ quy `sum_to(int n)` tính `1 + ... + n` (trả `0` nếu `n <= 0`), và in đúng 2 dòng:
1. `after_call=<v sau khi gọi double_val(v)>`
2. `sum=<sum_to(sum_n)> stack_frames=<f1 + f2 + f3>`

Chấm tự động:
```bash
bash labs/cham.sh CPR L02 duong_dan/bai_cua_ban.c
```

> Gợi ý đọc `stdin`: `int v, n, f1, f2, f3; if (scanf("%d %d %d %d %d", &v, &n, &f1, &f2, &f3) != 5) return 1;` (dấu `&` lấy địa chỉ ô nhớ để `scanf` nạp đủ 5 số từ `stdin`).
