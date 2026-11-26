# Lab DAN L11 — Méo tỉ lệ trục tung cắt ngọn trên biểu đồ cột

Đọc `stdin` `a=<float> b=<float> base=<float>`. Tính chênh lệch phần trăm thực từ `a` lên `b` và độ phóng đại thị giác khi cắt đáy trục ở `base`.

In 1 dòng: `real_diff_pct=<.1f>% visual_ratio=<.1f>x`.
Chấm tự động: `bash labs/cham.sh DAN L11 duong_dan/bai_cua_ban.py`

> Gợi ý đọc `stdin`: `kv = {k: float(v) for k, v in (t.split("=") for t in sys.stdin.read().split())}`.
