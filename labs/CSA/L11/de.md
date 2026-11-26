# Lab CSA L11 — Mô phỏng Cache ánh xạ trực tiếp: Tag, Index, Offset và xung đột

Đọc `stdin` `lines=<int> idx_bits=<int> off_bits=<int> probe=<hex> seq=<hex,...>`. Phân tích `probe`, rồi mô phỏng tuần tự `seq` để đếm hit, miss và số lần ghi đè xung đột.

In đúng 3 dòng: `split_0x84=tag:<d>,idx:<d>,off:<d>`, `hits=<d> misses=<d>`, `conflict_at_0x80=<d>`.
Chấm tự động: `bash labs/cham.sh CSA L11 duong_dan/bai_cua_ban.py`
