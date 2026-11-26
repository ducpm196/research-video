# Lab DVO L02 — Phân tích & sắp xếp phiên bản ngữ nghĩa SemVer

Đọc `stdin` `vers=<v1,v2,v3>`. So sánh bộ số của phần tử đầu và cuối, kiểm tra phép so chuỗi sai và sắp giảm dần theo SemVer.

In đúng 3 dòng: `semver_1_10_gt_1_9=<0|1>`, `str_cmp_bug=<0|1>`, `sorted_desc=<v1,v2,v3>`.
Chấm tự động: `bash labs/cham.sh DVO L02 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
