# Lab DVO L02 — Phân tích & sắp xếp phiên bản ngữ nghĩa (SemVer — Chính.Phụ.Vá) đúng (tránh bẫy so chuỗi)

Viết hàm `parse_ver(s)` tách `'1.10.0'` và `'1.9.3'` thành bộ số nguyên để so sánh, kiểm tra so chuỗi cho kết quả ngược và sắp danh sách `['1.10.0', '1.2.0', '1.9.3']`, in đúng 3 dòng:
1. `semver_1_10_gt_1_9=1`
2. `str_cmp_bug=1`
3. `sorted_desc=1.10.0,1.9.3,1.2.0`

Chấm tự động:
```bash
bash labs/cham.sh DVO L02 duong_dan/bai_cua_ban.py
```
