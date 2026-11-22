# WP-AF4-5 Stage 9 IRS Verifier v2

- **Khoá học**: `IRS` (`L00–L13`, 14 bài)
- **Phán quyết**: **NO-GO**
- **Tóm tắt kiểm tra tự động & điểm đã đạt**:
  - `lv.py lint`: `14/14 PASS` (`14.4–25.1p`)
  - `verify_irs.py`: `150/150 PASS`
  - `screen_code`: `28/28 PASS`
  - `loi_giai.py == mong_doi.txt`: `14/14 PASS`
  - `layout_IRS.tsv`: `0` dòng lỗi bố cục
  - `P9`: `14/14`; `"càng "`: `0` lỗi; công thức `L02` & `L12` đã sửa chuẩn.

## Lỗi MUST cần sửa

1. **P8 — Trùng nguyên số bài giảng trong `de.md` (`13/14` bài)**:
   - Các bài `L00, L01, L02, L04..L13` (trừ `L03`) lặp nguyên bộ số ví dụ từ thân bài vào đề lab.
   - `L07/de.md`: thiếu quy định làm tròn mấy chữ số thập phân.
   - `L06/de.md`: tiêu đề khó hiểu `"tránh gộp số 0 chưa chấm"`.

2. **`covers:` lệch scene trên 9 bài**:
   - `L00 obj3 -> quiz`
   - `L02 obj3 -> pitfalls`
   - `L04 obj3 -> pitfalls`
   - `L05 obj2 -> example`, `obj3 -> listwise`
   - `L07 obj2 -> formula`, `obj3 -> pitfalls/quiz`
   - `L08 obj1 -> formula`, `obj3 -> formula/example`
   - `L10 obj2 -> formula`, `obj3 -> online`
   - `L12 obj3 -> check`, `obj4 -> quiz`
   - `L13 obj3 -> quiz`

3. **P1 — Thuật ngữ & bảng đọc Python**:
   - Thiếu thuật ngữ: `TF-IDF` (`L02` + sửa cách gọi `"tần suất văn bản df"` cho chính xác là số văn bản chứa từ / document frequency), `IVF` (`L03`), `O(n²)` (`L05`), `SGD/dot` (`L07`), `ε` (`L09`), `IPS` (`L10`), `MMR` (`L11`).
   - Bảng đọc Python: false positive `dict` trên `13/14` bài (xử lý qua `ast_p1.py`), thiếu `is None`, `.split()`, `.count()`, `*a`, v.v.
