# Báo cáo kiểm định độc lập AF4 v2 Stage 10 — Khóa `PLC` (`L00–L13`, 14 bài)

**Kết luận tổng thể: `NO-GO`**

- `lv.py lint` (`L00..L13`): **14/14 PASS** (`0 FAIL, 0 WARN`); 13/14 >= 9p, riêng **`L06` = `8.9p` (< 9.0p)**.
- `verify_plc.py`: **72/72 PASS**; `screen_code`: **63 khối PASS**; `loi_giai.py == mong_doi.txt`: **14/14 MATCH**; `layout_PLC.tsv`: **0 lỗi**; 0/14 lộ code/output trước `pause: 30`.
- MP4 `out/PLC/L00..L13`: **14/14 STALE (chờ rebuild)**.

## Việc cần sửa để chuyển `GO`
1. **[MUST] `L13` (`de.md`, `loi_giai.py`, `mong_doi.txt`, `practice`)**: Đổi nhãn/nội dung từ `"tỉ lệ an toàn Chrome 96.2%"` / `safe_new_pct` (bị đảo ngược) sang đúng nguồn `[CR19]` (`125/130 = 96.2%` là tỉ lệ lỗi nghiêm trọng DO hỏng bộ nhớ, tốt hơn đổi bộ số không trùng `130, 5, 76, 24`).
2. **P8 spoilers & lệch đề**: `L03` (bỏ `= 4`), `L10` (bỏ `= 4`), `L12` (bỏ `(10, 20, 30, 40)` và `xs2 = xs1 + (40,)`), `L07/de.md` (bỏ `([15, 20])` & `(13)`), `L11/de.md` (bỏ `('+', 20, 'x')` & đổi `('*' ,4, 5)` khác quiz), `L02/de.md` (không ép tên `term` khi `loi_giai` dùng `fold`), `L04` (`tầm vực` → `phạm vi`), `L08/de.md` (đổi đỉnh khỏi `R, X, Y`).
3. **P1 (`practice` & thân bài)**: Thay bảng đọc bằng `ast_p1` (bỏ `set()`/`dict()`/`%` sai ở 11 bài; bổ sung token thật cho `L00–L13`), giải thích thuật ngữ/ký hiệu còn thiếu (`while..in`, `//`, `**`, `1.0f`, `0x`, `x: int`, `bool`, `with`, `try..finally`, `void`, `deepcopy`, `∘`, `@lru_cache`, `tranh chấp`).
4. **Thời lượng `L06` (`>= 9.2p`) & `covers:` (`L02, L05, L12, L13`)**.
