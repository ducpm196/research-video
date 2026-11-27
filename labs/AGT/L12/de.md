# Lab AGT L12 — Tiến bộ giải bài tập mã nguồn SWE-bench 2022-2025

Đọc `stdin` `old_pct=<f> full_n=<int> new_ok=<int> ver_pct=<f> ver_n=<int>`. Tính số bài giải ban đầu, bội số tăng tiến và số bài đạt được trên SWE-bench Verified.

In 1 dòng: `full_old=<d> full_gain=<.1f>x verified_solved=<d>`.
Chấm tự động: `bash labs/cham.sh AGT L12 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: `kv = dict(t.split('=') for t in sys.stdin.read().split())` rồi ép `float`/`int` và dùng `round(...)`, `f"{val:.1f}x"`.
