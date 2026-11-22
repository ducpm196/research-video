# Kiểm định độc lập AF4 v2 — Stage 10 Khoá `HCI` (`L00–L12`, 13/13 bài)

## Kết luận tổng thể: **NO-GO**

- `lv.py lint`: **13/13 PASS** (0 FAIL, 0 WARN); `verify_hci.py`: **27/27 PASS**; `loi_giai.py == mong_doi.txt`: **13/13 MATCH**; `screen_code`: **26/26 PASS**; `layout_HCI.tsv`: **0 dòng**; `P9 = 2`: **13/13**; `L09, L10` SVG tương phản đã sửa tốt!
- MP4 `out/HCI/L00..L12`: **13/13 STALE (chờ rebuild)**.

## Việc cần sửa để chuyển `GO`
1. **Lỗi lặp 4 lần (`L12 pitfalls#1`)**: `(ngôn ngữ đánh dấu trang mạng)` lặp 4 lần → giữ 1 lần.
2. **`covers:` (7 bài)**: `L02, L04, L06, L08, L09, L11, L12`.
3. **P8 spoilers & số liệu (`L00, L01, L04, L05, L06, L08, L11, L12`)**: Bỏ đáp số khỏi tiêu đề `de.md` & `practice#0` (`27 phút`, `5!=120`, `4 cụm`, `4.35s / 2.55s`, `4 lớp / 38 phút`, `65 / 21:1`); sửa `L05/de.md` `B 0.2` → `BB 0.2`; đổi bộ số khỏi trùng `quiz`/bài (`L01, L06, L08, L11, L12`); sửa `L06/de.md` `p` nhất quán với $p_{\text{sót}}$; ghi rõ `area_24` (`L12`), `p2=1.0` (`L10`), `perms_total` tính thật (`L08`).
4. **P1 (`practice` + thân bài)**: Thay bảng đọc bằng `ast_p1` (bổ sung cho `L02, L04, L06, L07, L08, L09, L11`, bỏ `set`/`dict` thừa 13 bài); mở nghĩa `px` (`L02, L09`), `O(n)` (`L03 recap#1`), `$10^{-5}$` (`L10 recap#1`), `thẻ văn bản`/`HTML` (`L09`).
5. **Thời lượng `L11`** (8.72p thuần lời đọc → thêm ~70 từ lên ≥ 9.2p) & SVG `L08 intuition#0` đậm hơn (`#0369a1`/`#15803d`), `L01` `Phải-Dưới`.
