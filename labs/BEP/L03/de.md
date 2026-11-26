# Lab BEP L03 — Serverless Cold-Start Estimator & Kiểm soát OWASP BOLA

Đọc từ `stdin` 3 dòng:
- Dòng 1: `warm_ms=<int> cold_penalty=<int> cold_rate=<float>`
- Dòng 2: `owners=<id1:user1,id2:user2,...>`
- Dòng 3: `reqs=<req_user:doc_id,req_user:doc_id,...>`

Yêu cầu:
1. Tính độ trễ trung bình Serverless `avg_ms = warm_ms + cold_rate * cold_penalty`.
2. Đánh giá từng yêu cầu trong `reqs`: chỉ cho phép (`200`) nếu `doc_id` tồn tại và `owners[doc_id] == req_user`; ngược lại từ chối (`403`), đếm số ca hợp lệ (`allowed`) và số ca bị chặn BOLA (`blocked`).
3. In đúng 3 dòng: `avg_latency_ms=<.1f>`, `allowed=<int>`, `bola_blocked=<int>`.

Chấm tự động: `bash labs/cham.sh BEP L03 duong_dan/bai_cua_ban.py`
