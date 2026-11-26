# Lab SDP L14 — Phiên bản ngữ nghĩa SemVer: phân loại nâng cấp và sắp thứ tự

Đọc `stdin` `base=<M.m.p> v1=<M.m.p> v2=<M.m.p>`. Tăng phiên bản theo 3 mức `patch`, `minor`, `major` từ `base`, và đối chiếu phép so bộ số với so chuỗi giữa `v1`, `v2`.

In đúng 3 dòng: `patch=<v> minor=<v> major=<v>`, `tuple_cmp_1_10_gt_1_9=<0|1>`, `str_cmp_wrong=<0|1>`.
Chấm tự động: `bash labs/cham.sh SDP L14 duong_dan/bai_cua_ban.py`
