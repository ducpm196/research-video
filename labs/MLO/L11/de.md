# Lab MLO L11 — Lượng tử hoá int8 và nén bộ nhớ mô hình

Đọc `stdin` `val=<float> rmax=<float> params_b=<int>`. Lượng tử hóa đối xứng 8-bit (`qmax = 127`) trên `[-rmax, rmax]`, tính sai số khôi phục và so RAM của `fp32` vs `int8`.

In 2 dòng: `q=<d> deq=<.4f> err=<.4f>`, `fp32_gb=<d> int8_gb=<d>`.
Chấm tự động: `bash labs/cham.sh MLO L11 duong_dan/bai_cua_ban.py`
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
