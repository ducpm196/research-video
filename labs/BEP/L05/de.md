# Lab BEP L05 — Bộ điều phối Saga Compensations & Backoff-to-DLQ

Đọc từ `stdin` 2 dòng:
- Dòng 1: `steps=<name:status,name:status,...>` (`status` là `OK` hoặc `FAIL`)
- Dòng 2: `base_ms=<int> cap_ms=<int> max_retries=<int>`

Yêu cầu:
1. Chạy các bước tuần tự; ngay khi gặp bước đầu tiên `status=FAIL`, dừng lại và tạo chuỗi bù trừ đảo ngược dạng `undo_<step>` cho toàn bộ bước đã `OK` trước đó (nếu mọi bước đều `OK` thì ghi `NONE`).
2. Tính tổng thời gian chờ của `max_retries` lượt thử lại lũy thừa bị giới hạn trần: `sum(min(cap_ms, base_ms * 2**k) for k in range(max_retries))` nếu có bước `FAIL`; nếu mọi bước đều `OK` thì `backoff_total_ms=0`.
3. Xác định `routed_dlq` (`1` nếu có bước `FAIL`, ngược lại `0`).

In đúng 3 dòng: `compensations=<u2,u1 hoặc NONE>`, `backoff_total_ms=<int>`, `routed_dlq=<0|1>`.

Chấm tự động: `bash labs/cham.sh BEP L05 duong_dan/bai_cua_ban.py`
