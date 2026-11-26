# Lab BEP L09 — Bộ quét Code Review OWASP & Kiểm định Postmortem RCA

Đọc từ `stdin` 3 dòng:
- Dòng 1: `flags=<flag1,flag2,...>` (`SQLI_CONCAT`, `TIMING_EQ`, `NO_IDEM`, `CLEAN`)
- Dòng 2: `actions=<action1,action2,...>` (công việc sau sự cố; hành động tự động bắt đầu bằng `AUTO:`, hành động nhắc nhở bắt đầu bằng `MANUAL:`)
- Dòng 3: `dod_missing=<int>` (số tiêu chí Definition of Done còn thiếu)

Yêu cầu:
1. Đếm `security_defects` = số cờ khác `CLEAN` trong `flags`.
2. Đếm `auto_fix_count` = số hành động bắt đầu bằng `AUTO:` trong `actions`.
3. Xác định `release_decision`: `APPROVED` chỉ khi `security_defects == 0`, `dod_missing == 0` và `auto_fix_count >= 1`; ngược lại `CHANGES_REQUESTED`.

In đúng 3 dòng: `security_defects=<int>`, `auto_fix_count=<int>`, `release_decision=<APPROVED|CHANGES_REQUESTED>`.

Chấm tự động: `bash labs/cham.sh BEP L09 duong_dan/bai_cua_ban.py`
