# Lab BEP L08 — Trình kiểm SLA/OLA Budget & L3 Escalation Audit

Đọc từ `stdin` 3 dòng:
- Dòng 1: `sla_pct=<float> downtime_min=<float>`
- Dòng 2: `ola_l2_limit=<int> elapsed_min=<int> has_trace=<0|1>`
- Dòng 3: `edge_vals=<v1,v2,...>` (các mẫu số thử nghiệm; kiểm xem `0` hay số âm có được guard trả `0.0` hay không: đếm các số `<= 0` được chặn an toàn)

Yêu cầu:
1. Tính ngân sách lỗi SLA tháng 30 ngày (`budget_min = (1.0 - sla_pct / 100.0) * 43200.0`) và xác định `sla_breached` (`1` nếu `downtime_min > budget_min`, ngược lại `0`).
2. Quyết định chuyển tuyến L3: `l3_action = ESCALATE_L3` nếu `elapsed_min > ola_l2_limit` và `has_trace == 1`; nếu `elapsed_min > ola_l2_limit` mà thiếu trace ghi `NEED_TRACE`, ngược lại `KEEP_L2`. Trạng thái `l3_action` nhận `ESCALATE_L3`, `NEED_TRACE`, hoặc `KEEP_L2`.
3. Đếm số giá trị không dương trong `edge_vals` cần bộ bảo vệ chia (`guarded_cases = sum(x <= 0)`).

In đúng 3 dòng: `budget_min=<.2f> sla_breached=<0|1>`, `l3_action=<STR>`, `guarded_cases=<int>`.

Chấm tự động: `bash labs/cham.sh BEP L08 duong_dan/bai_cua_ban.py`
