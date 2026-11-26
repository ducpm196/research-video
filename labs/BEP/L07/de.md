# Lab BEP L07 — Bộ phân tích Span OpenTelemetry & API Gateway Circuit Breaker

Đọc từ `stdin` 3 dòng:
- Dòng 1: `spans=<sid:pid:dur,...>` (`pid` bằng `NONE` nếu là nhịp gốc)
- Dòng 2: `events=<OK|FAIL,...>` (chuỗi kết quả qua Gateway)
- Dòng 3: `quota=<int> cb_thresh=<int>` (hạn mức tối đa số yêu cầu được nhận và ngưỡng lỗi mở cầu dao)

Yêu cầu:
1. Tính `self_ms = dur - sum(direct_children_dur)` cho từng span, tìm `top_span` có `self_ms` lớn nhất (nếu hoà lấy tên nhỏ hơn theo từ điển).
2. Mô phỏng API Gateway xử lý tối đa `quota` yêu cầu đầu trong `events` (nếu qua `quota` coi như bị chặn `429`); trước lúc vượt `quota`, nếu cầu dao chưa `OPEN` và gặp `FAIL`, tăng bộ đếm lỗi, chạm `cb_thresh` thì mở `OPEN` (các yêu cầu sau đó bị chặn `503`); gặp `OK` reset bộ đếm lỗi về `0`. Đếm số yêu cầu đi lọt `passed` (`OK`).
3. In đúng 3 dòng: `top_self_span=<str>`, `top_self_ms=<int>`, `gw_passed=<int> cb_state=<CLOSED|OPEN>`.

Chấm tự động: `bash labs/cham.sh BEP L07 duong_dan/bai_cua_ban.py`
