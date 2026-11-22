# Kiểm định độc lập AF4 v2 — Stage 10 Khoá `PAR` (`L00–L13`: 14/14 bài)

## Kết luận: **NO-GO**

- `lv.py lint`: **14/14 PASS** (`0 FAIL, 0 WARN`, `11.09–20.17` phút).
- `verify_par.py`: **96/96 PASS**; `screen_code`: **28/28 PASS**; `loi_giai.py == mong_doi.txt`: **14/14 MATCH**; `layout_PAR.tsv`: **0 lỗi**; `Hai mức quy mô:` ở `recap`: **14/14**; 0 lỗi `"càng "` mơ hồ.
- MP4 `out/PAR/L00..L13`: **14/14 STALE (chờ rebuild)**.

## Việc cần sửa để chuyển `GO`
1. **[MUST] Toán `L12 recap.1`**: Sửa `"nâng 16 thẻ đạt ngay 5,93×"` → `1 / (0.05 + 0.95 / 16) = 9,14×` (hoặc ghi rõ 8 thẻ `5,93×`, tốt nhất khớp 2% thân bài: 8 thẻ `7,02×` / 16 thẻ `12,31×`). Sửa `L10 recap.1` `"1,97D GB"` → `"1,97D"`.
2. **[MUST] `L04 practice.0` & `de.md`**: Bỏ spoiler `"từ 30 xuống 20"` và gợi ý `sorted(jobs, reverse=True)`.
3. **P1 bảng `practice`**: Dùng `ast_p1` (bỏ `dict`/`set` thừa ở 14 bài và `%` modulo sai ở L11; bổ sung đủ token thật), giải thích đơn vị/ký hiệu (`s=giây` L00/01, `bit` L03/06/10, `ms` L04/10/11, `byte` L05 hook, `RAM` L05/06, `GB/MB` L10/11, `LPT/makespan` L04, `TF/s/TB/s/FLOP/byte/AI/Roofline` L07, `GFLOP/s` L13, `False Sharing`/`512-bit`/`T_inf`/`^` ở `de.md`).
4. **`covers:`** (`L01, L04..L11, L13`).
