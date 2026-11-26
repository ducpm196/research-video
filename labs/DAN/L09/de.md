# Lab DAN L09 — Phát hiện bất thường bền vững theo MAD

Đọc `stdin` `xs=<v1,v2,...> target=<float>`. Tính điểm z cổ điển (chia độ lệch chuẩn tổng thể) và điểm z bền vững dùng trung vị cùng `1.4826 * MAD` cho `target`.

In 1 dòng: `z_classical=<.2f> z_robust=<.1f>`.
Chấm tự động: `bash labs/cham.sh DAN L09 duong_dan/bai_cua_ban.py`

> Gợi ý đọc `stdin`: `kv = dict(t.split("=") for t in sys.stdin.read().split())`; sắp danh sách `sorted(...)` tìm trung vị và MAD rồi nhân `1.4826`.
