# Lab MLO L03 — Kiểm thử bất biến hành vi và lát nhóm

Đọc `stdin` `names=<n1,n2,...> kw=<str> slices=<k:v,...> thr=<float>` (tuỳ chọn `bias=<sub_bi_le>`). Kiểm tra mọi câu `name is <kw>` đều dự đoán `1` (không chứa `bias`) và mọi nhóm lát đạt `>= thr`.

In 1 dòng: `inv_pass=<0|1> min_slice_pass=<0|1>`.
Chấm tự động: `bash labs/cham.sh MLO L03 duong_dan/bai_cua_ban.py`
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Tham số tuỳ chọn `bias=<chuỗi>` (nếu có): bất kỳ tên nào chứa chuỗi con `bias` đều bị dự đoán sai `0` (khiến `inv_pass=0`).
