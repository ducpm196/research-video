# Lab SDP L14 — Phiên bản ngữ nghĩa SemVer: phân loại nâng cấp và sắp thứ tự

Viết hàm `bump_ver(ver, kind)` cho `ver = (1, 4, 2)` theo 3 loại `'patch'`, `'minor'`, `'major'`, và kiểm chứng so sánh tuple `(1, 10, 0) > (1, 9, 3)` thay vì so chuỗi, in đúng 3 dòng:
1. `patch=1.4.3 minor=1.5.0 major=2.0.0`
2. `tuple_cmp_1_10_gt_1_9=1`
3. `str_cmp_wrong=1`

Chấm tự động:
```bash
bash labs/cham.sh SDP L14 duong_dan/bai_cua_ban.py
```
