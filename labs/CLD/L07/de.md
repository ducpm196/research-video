# Lab CLD L07 — Công thức tự co giãn ngang (HPA) kèm dung sai

Đọc `stdin` `cur=<int> tgt=<int> tol=<float> cpu1=<int> cpu2=<int>`. Áp dụng quy tắc HPA giữ nguyên khi `|cpu/tgt - 1| <= tol`, ngược lại tính `ceil(cur * cpu / tgt)` (giữ nguyên hai tên khoá `replicas_at_84` cho `cpu1` và `replicas_at_64` cho `cpu2` trên mọi bộ dữ liệu).

In 2 dòng: `replicas_at_84=<d>`, `replicas_at_64=<d>`.
Chấm tự động: `bash labs/cham.sh CLD L07 duong_dan/bai_cua_ban.py`
