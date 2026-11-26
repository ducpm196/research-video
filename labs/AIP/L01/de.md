# Lab AIP L01 — Bộ chọn Model Registry đa tiêu chí & Kiểm định A/B Z-test

Đọc từ `stdin` 3 dòng:
- Dòng 1: `runs=<id:f1:lat_ms,...>`
- Dòng 2: `min_f1=<float> max_lat=<float>`
- Dòng 3: `na=<int> ca=<int> nb=<int> cb=<int> z_thresh=<float>` (số mẫu và số chuyển đổi của bản A và bản B)

Yêu cầu:
1. Từ `runs`, lọc ứng viên thoả đồng thời `f1 >= min_f1` và `lat_ms <= max_lat`, chọn `best_run` có `f1` cao nhất (nếu hoà ưu tiên `lat_ms` nhỏ hơn; không có trả `NONE`).
2. Tính kiểm định hai tỉ lệ gộp `z = (pb - pa) / sqrt(pp * (1 - pp) * (1/na + 1/nb))` (nếu mẫu số bằng 0 đặt `z = 0.0`).
3. Chỉ đặt `deploy_prod = 1` nếu `best_run != "NONE"` và `z >= z_thresh`.

In đúng 3 dòng: `promoted_run=<str>`, `ab_z=<.3f>`, `deploy_prod=<0|1>`.

Chấm tự động: `bash labs/cham.sh AIP L01 duong_dan/bai_cua_ban.py`
