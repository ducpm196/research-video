# Lab AIP L03 — Dynamic Batching Simulator & Edge INT8 Fit Check

Đọc từ `stdin` 2 dòng:
- Dòng 1: `n_reqs=<int> max_batch=<int> fixed_ms=<float> per_item_ms=<float> wait_ms=<float>`
- Dòng 2: `params_millions=<float> bits=<int> edge_ram_mb=<float>`

Yêu cầu:
1. Chia `n_reqs` yêu cầu thành các lô tối đa `max_batch` phần tử: tính tổng số lô `batches = ceil(n_reqs / max_batch)` (nếu chia hết lấy trọn, phần dư nằm ở lô cuối). Tổng thời gian xử lý toàn bộ qua các lô bằng `sum(fixed_ms + sz * per_item_ms)` với mỗi lô kích thước `sz`. Tính `qps = n_reqs * 1000.0 / total_exec_ms`. (Giả định kích thước từng lô đóng sẵn trong cửa sổ; `worst_case_ms = wait_ms + fixed_ms + max_batch * per_item_ms`).
2. Tính dung lượng mô hình `model_mb = params_millions * (bits / 8.0)` và kiểm tra `fits_edge = int(model_mb <= edge_ram_mb)`.

In đúng 3 dòng: `batches=<int> qps=<.1f>`, `worst_case_ms=<.1f>`, `model_mb=<.1f> fits_edge=<0|1>`.

Chấm tự động: `bash labs/cham.sh AIP L03 duong_dan/bai_cua_ban.py`
