# Kiểm định độc lập AF4 v2 Stage 10 `SEP` (`L00–L11`, 12 bài) — KẾT LUẬN: **NO-GO**

- `lv.py lint` (`L00–L11`): **12/12 PASS** (0 FAIL, 0 WARN; `11.20–19.45` phút); `verify_sep.py`: **71/71 PASS**; `screen_code`: **24/24 PASS**; `loi_giai.py == mong_doi.txt`: **12/12 PASS**; `layout_SEP.tsv`: **0 dòng**; `P9 = 2`: **12/12**.
- MP4 `out/SEP/L00..L11`: **12/12 STALE (chờ rebuild)**.

## Việc cần sửa để chuyển `GO`
1. **`L07` (`practice#0`, `de.md`, `loi_giai.py`, `formula#1`)**: Bỏ `"gia hạn 30 ngày"` và `d120` (trái `sources_L07.md`); đổi sang hạn 90 ngày, ngày công bố khi có vá sớm ở ngày `v` (`v+30` khi `v<=90`), và hạn 7 ngày đang khai thác; thêm điều kiện `v <= 90` ở `L07 formula#1`.
2. **`L08` (`practice#0,#4`, `de.md`, `loi_giai.py`)**: Đưa điểm lab về thang `-2..2`, lọc `min(v) >= 0`, chọn theo `(sum(v), v[3])` sao cho thử đúng bước 3 ưu tiên bên yếu thế.
3. **`L09` (`practice#0`, `de.md`)**: Bỏ chữ `PERT` (trái `sources_L09.md`), đổi khỏi `(O=3, M=5, B=13)` trùng `quiz` (vd `(O=2, M=5, B=14)`), dùng ký hiệu `s` hoặc giải thích `SD`.
4. **`L11` (`de.md`, `loi_giai.py`, `practice`)**: Bỏ `GDPR 4%`, `EUR`, `Sweeney` (trái `sources_L11.md`), thay bằng Luật 91/2025/QH15 hoặc ví dụ nội dung bài; sửa công thức khớp `exp(-(N-1)/c)`.
5. **`covers:` (`L00–L06`)** & **P1 bảng `practice` (`ast_p1`)** (và đổi số `L01/L03 de.md` khỏi trùng `quiz`).
