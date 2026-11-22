# Báo cáo kiểm định độc lập AF4 v2 — Stage 10 Khoá TOC (`L00–L14`, 15 bài)

**Kết luận tổng thể: `NO-GO`**

- `lv.py curriculum curriculum/toc.yaml`: **15/15** (`0 lỗi`).
- `lv.py lint` (`L00..L14`): **15/15 PASS** (`0 FAIL, 0 WARN`). Thời lượng: 14/15 ≥ 9p (`9.5–20.9p`); **`L09` = `8.9p` (< 9.0p)**.
- `verify_toc.py`: **102/102 PASS**; `loi_giai.py == mong_doi.txt`: **15/15 MATCH**; `screen_code`: **32/32 PASS**; `layout_TOC.tsv`: **0 dòng**; `"càng "`: **0 câu**.
- MP4 `out/TOC/L00..L14`: **15/15 STALE (chờ rebuild)**.

## Việc cần sửa để chuyển `GO`
1. **`L11/de.md`**: Bổ sung bảng `rows = [[1, 0, 1], [0, 0, 1], [1, 1, 0]]` vào `de.md` & sửa `"Kiểm tra từng trường hợp trong toàn bộ..."`.
2. **`L06/de.md` & `L06 practice#0`**: Xoá đáp án `= 14` khỏi tiêu đề và `Nhiệm vụ`; đổi độ dài `8` (trùng `quiz`) sang `10` (`C_5 = 42`).
3. **`L09`**: Tăng nhẹ lời đọc để `>= 9.2 phút` (hiện `8.9p`), sửa tiêu đề `de.md` & `practice#0` (bỏ `"từ trái sang phải /"`).
4. **P1 bảng `practice`**: Dùng phân tích AST để bỏ `{a,b}/set()` thừa ở `L00, L01, L03, L04, L06..L09, L11..L14`, bổ sung token thật cho `L01, L02 (frozenset, .union, *(...), .get, .pop, .add, not), L03, L04, L05, L06, L07, L08, L09, L11, L12, L13`; giải thích `{n}` ở `L14/de.md`, `O(n)` / `O(n log n)` / `C_4`.
5. **P9 thân bài** (`L03, L04, L06, L07, L08, L10, L11, L12`) & **`covers:`** (`L01, L02, L05, L06, L09, L10, L11`) & `L08/de.md` bỏ `'000111'` trùng `quiz` & `L13/de.md` diễn đạt rõ hơn.
