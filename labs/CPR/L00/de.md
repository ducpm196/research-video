# Lab CPR L00 — Đo kích thước kiểu cơ bản và mảng động theo stdin trên GCC

Viết chương trình C chuẩn C11 đọc hai số nguyên `arr_len` và `scale_n` từ `stdin` rồi in đúng 3 dòng (mỗi kích thước đo trực tiếp bằng `sizeof`):
1. `char=<sizeof(char)> int=<sizeof(int)> ll=<sizeof(long long)> ptr=<sizeof(void *)>`
2. `arr_bytes=<arr_len * sizeof(int)>`
3. `total_bytes=<scale_n * sizeof(int)>` (tính bằng `size_t`, đủ lớn cho hàng triệu phần tử)

Máy chấm chạy thêm ca ẩn quy mô trong `ca_an/` nên không in cứng đáp án tĩnh.

Chấm tự động bằng Git Bash:
```bash
bash labs/cham.sh CPR L00 duong_dan/bai_cua_ban.c
```

> Gợi ý đọc `stdin`: `unsigned long long arr_len = 0, scale_n = 0; if (scanf("%llu %llu", &arr_len, &scale_n) != 2) return 1;` (`&` lấy địa chỉ biến cho `scanf` ghi giá trị vào).
