# Lab PLC L08 — Thu gom rác đánh dấu-quét (duyệt theo chiều rộng BFS)

Đọc `root|adj` từ `stdin` (ví dụ `R|R:A;A:B;B:;C:D;D:C;E:`).
Duyệt theo chiều rộng từ `root` để tách tập nút còn sống (`alive`) và tập nút rác không đi tới được (`reclaimed`). Sắp xếp cả hai danh sách tăng dần theo thứ tự chữ cái (`sorted(...)`).

In đúng 1 dòng `alive=[...] reclaimed=[...]`.
Chấm tự động: `bash labs/cham.sh PLC L08 duong_dan/bai_cua_ban.py`
