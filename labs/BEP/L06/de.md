# Lab BEP L06 — Singleflight Coalescer & Audit Trail Hash-Chain

Đọc từ `stdin` 3 dòng:
- Dòng 1: `miss_keys=<k1,k2,...>` (các yêu cầu đọc bị hụt cache đến trong cùng 1 khung thời gian)
- Dòng 2: `events=<e1,e2,...>` (chuỗi sự kiện audit cần nối băm)
- Dòng 3: `tamper_idx=<int>` (vị trí thay bằng gắn thêm `'*'`)

Yêu cầu:
1. Đếm số lượt gọi xuống DB khi có Singleflight cho cụm hụt đồng thời (`db_reads_sf = len(set(miss_keys))`).
2. Tính chuỗi băm `Audit Trail` bắt đầu từ `h = '0' * 64`, cập nhật `h = sha256(f"{h}|{ev}")` cho từng sự kiện và xuất 12 ký tự đầu của băm cuối (`tail_hash12`).
3. Thử sửa `events[tamper_idx]` thêm `'*'` ở cuối rồi tính lại chuỗi băm, kiểm tra phát hiện sai lệch (`tamper_detected=1` hoặc `0`).

In đúng 3 dòng: `db_reads_sf=<int>`, `tail_hash12=<str>`, `tamper_detected=<0|1>`.

Chấm tự động: `bash labs/cham.sh BEP L06 duong_dan/bai_cua_ban.py`
