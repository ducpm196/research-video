# Lab LNX L04 — Đếm i-nốt thực tế và quy mô thư mục nhiều tệp nhỏ qua stdin

Viết kịch bản Bash đọc `<n_files> <scale_n>` từ `stdin`, tạo thư mục tạm chứa đúng `n_files` tệp 0 byte, đếm số tệp (`files`), tổng đối tượng gồm cả thư mục (`objects`), và tính tổng i-nốt quy mô `inodes_scale = scale_n + 1`.

Chấm tự động:
```bash
bash labs/cham.sh LNX L04 duong_dan/bai_cua_ban.sh
```
