# Lab CAS L03 — Lỗi đơn vị lực đẩy lbf-giây sang N-giây

Đọc `stdin` `cmd=<float> lbf_to_n=<float>`. Tính xung lượng thực tế theo đơn vị N-giây khi phần mềm xuất theo `lbf-s`.

In đúng 1 dòng: `reported=<.1f> actual=<.2f> factor=<.2f>`.
Gợi ý Python: `import sys; kv = dict(t.split('=') for t in sys.stdin.read().split())`; dùng `float(...)`, in `f"{val:.1f}"` / `f"{val:.2f}"`.
Chấm tự động: `bash labs/cham.sh CAS L03 duong_dan/bai_cua_ban.py`
