# Lab EVT L06 — Bù trừ ngược thứ tự trong giao dịch dài (Saga)

Đọc `stdin` `steps=<s1,s2,...> fail=<step>`. Chạy tuần tự tới khi gặp bước `fail` thì sinh danh sách bù trừ `'undo_<bước>'` theo thứ tự đảo ngược.

In 2 dòng: `failed_at=<step>`, `compensations=<list>`.
Chấm tự động: `bash labs/cham.sh EVT L06 duong_dan/bai_cua_ban.py`
