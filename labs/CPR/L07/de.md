# Lab CPR L07 — Đo căn lề struct và cộng/giải phóng danh sách liên kết qua stdin

Viết chương trình C chuẩn C11 định nghĩa `struct S1 { char a; int b; char c; };` và `struct S2 { int b; char a; char c; };`, đọc `n` rồi đọc `n` số nguyên từ `stdin`, dựng danh sách liên kết đơn `n` nút, tính tổng và giải phóng hết từng nút, in đúng 2 dòng:
1. `s1=<sizeof S1> s2=<sizeof S2>`
2. `list_sum=<tổng nút> freed=<số nút đã giải phóng>`

Chấm tự động:
```bash
bash labs/cham.sh CPR L07 duong_dan/bai_cua_ban.c
```
