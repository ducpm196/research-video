# Lab CAS L07 — Cloudflare ReDoS bậc ba O(n^3) của mẫu quay lui

Đọc `stdin` `n=<int>`. Dùng mô hình bậc ba tối giản đếm tổng số bước quay lui tích lũy trên mọi vị trí đầu chuỗi độ dài `n`: tại mỗi phần đuôi độ dài `m = n - s` (với `s = 0..n-1`), số bước quay lui là `m * (m + 1) // 2`, tức tổng `sum((n - s) * (n - s + 1) // 2 for s in range(n))` (`= n*(n+1)*(n+2)//6`), và bội số làm tròn so với tuyến tính `n`. (Lưu ý đây là công thức đa thức bậc 3 tối giản của mẫu, khác với số bước thô của trình khớp `bt_match` ở bài giảng.)

In đúng 1 dòng: `n=<d> cubic_steps=<d> ratio=<d>x`.
Chấm tự động: `bash labs/cham.sh CAS L07 duong_dan/bai_cua_ban.py`
