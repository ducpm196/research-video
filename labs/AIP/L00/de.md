# Lab AIP L00 — Feature Store Point-in-Time As-Of Join & Parity Audit

Đọc từ `stdin` 3 dòng:
- Dòng 1: `events=<e_id:ts:online_val,...>`
- Dòng 2: `features=<e_id:ts:val,...>`
- Dòng 3: `parity_tol=<float>`

Yêu cầu:
1. Với mỗi sự kiện `(e_id, ev_ts, on_val)`, tìm giá trị đặc trưng hợp lệ của cùng `e_id` có `feat_ts` lớn nhất thoả mãn `feat_ts <= ev_ts`. Đếm `joined_count` (số sự kiện tìm được ít nhất 1 đặc trưng quá khứ) và `missing_count`.
2. Trên các sự kiện ghép thành công, tính sai lệch lớn nhất `max_skew = max(|feat_val - online_val|)` (nếu không ghép được sự kiện nào lấy `0.0`).
3. Xác định `parity_ok` (`1` nếu `missing_count == 0` và `max_skew <= parity_tol`, ngược lại `0`).

In đúng 3 dòng: `joined_count=<int> missing_count=<int>`, `max_skew=<.6f>`, `parity_ok=<0|1>`.

Chấm tự động: `bash labs/cham.sh AIP L00 duong_dan/bai_cua_ban.py`
