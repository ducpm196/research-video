# Lab DVO L11 — Tính toán dung lượng lưu trữ nhật ký theo lưu lượng req/s

Đọc `stdin` `rps=<int> rec_B=<int> days=<int> sample_pct=<float>`. Tính dung lượng thập phân một ngày (GB), tổng `days` ngày (TB) và dung lượng khi lấy mẫu `sample_pct`.

In đúng 3 dòng: `gb_per_day=<.1f>`, `tb_30_days=<.2f>`, `sampling_10pct_tb=<.2f>`.
Chấm tự động: `bash labs/cham.sh DVO L11 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
