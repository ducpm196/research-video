# Lab AIP L05 — Tự động kiểm API/UI Contract, Bộ lọc PII & Kiểm định AI Governance

Đọc từ `stdin` 2 dòng:
- Dòng 1: `status=<int> lat_ms=<int> max_lat=<int> selector=<str> log_line=<chuỗi_văn_bản>`
- Dòng 2: `rate_priv=<float> rate_unpriv=<float>`

Yêu cầu:
1. Kiểm thử API/UI: `qa_pass = int(status == 200 and lat_ms <= max_lat and 'data-testid' in selector)`.
2. Đếm và che toàn bộ mẫu PII xuất hiện trong `log_line` (khớp email `[\w.+-]+@[\w-]+\.[\w.-]+` và số điện thoại Việt Nam bắt đầu bằng `0` dài 10 chữ số `\b0\d{9}\b`) thành `[REDACTED]`, ghi lại số phần tử PII phát hiện được (`pii_count`) và kiểm `pii_clean = 1`.
3. Tính `di = rate_unpriv / rate_priv` (làm tròn 3 chữ số) và kiểm định chuẩn công bằng 4/5 (`gov_ok = int(di >= 0.80)`), rồi quyết định `ship_ready = int(qa_pass == 1 and gov_ok == 1)`.

In đúng 3 dòng: `qa_pass=<0|1> pii_redacted=<int>`, `disparate_impact=<.3f> gov_ok=<0|1>`, `ship_ready=<0|1>`.

Chấm tự động: `bash labs/cham.sh AIP L05 duong_dan/bai_cua_ban.py`
