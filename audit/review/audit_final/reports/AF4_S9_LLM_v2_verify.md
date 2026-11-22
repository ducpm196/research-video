# WP-AF4-5 Stage 9 LLM Verifier v2

- **Khoá học**: `LLM` (`L00–L14`, 15 bài)
- **Phán quyết**: **NO-GO**
- **Tóm tắt kiểm tra tự động & điểm đã đạt**:
  - `lv.py lint`: `15/15 PASS`
  - `verify_llm.py`: `18/18 PASS`
  - `loi_giai.py == mong_doi.txt`: `15/15 PASS`
  - `screen_code`: `30/30 PASS`
  - `layout_LLM.tsv`: `0` dòng lỗi bố cục
  - `P9`: `15/15`, tất cả `15/15` ẩn trước `pause: 30`
  - Đã sửa tốt: `L02` BPE, `L01/de.md`, `L14/de.md`, `L00/07/12` bỏ hardcode.

## Lỗi MUST cần sửa

1. **P8 — Trùng nguyên số ví dụ bài giảng trong `de.md` (`14/15` bài)**:
   - Tất cả các bài (trừ `L04` mới đạt một phần) đều lặp nguyên bộ số ví dụ từ thân bài sang `de.md`. Cần đổi sang bộ dữ liệu mới độc lập.

2. **Lỗi gõ chữ / chính tả code — `L02 practice#0`**:
   - Lỗi `merge1=...s freq=...`.

3. **P1 — Bảng đọc Python & thuật ngữ thân bài**:
   - False positive `dict`/`set` trên `13/15` bài (sửa bằng `ast_p1.py`).
   - `L10`: ký hiệu `%` đang giải thích sai là phép chia lấy dư (cần phân biệt chuỗi định dạng / đơn vị).
   - `L02`: thiếu `",".join`, và một số bài thiếu `*u`, `7e9`, v.v.
   - Thiếu thuật ngữ/khái niệm nền trong thân bài: `perplexity` (`L01`), `BPE` (`L02`), `KV cache/fp16/16 bit` (`L05`), `nhị thức` (`L11`), `recall` (`L12`), `Fraction` (`L00`), `exp()` (`L06`).

4. **`covers:` lệch scene trên 5 bài**:
   - `L01 obj3 -> pitfalls`
   - `L03 obj1 -> sym`
   - `L04 obj3 -> pitfalls/sym`
   - `L07 obj3 -> pitfalls`
   - `L11 obj1 -> hook/pitfalls`
   - `L00 obj2 -> example`

5. **Thời lượng `< 9.0 phút`**:
   - Các bài `L00..L03, L07, L09..L12` dưới `9.0 phút`. Cần bổ sung khoảng `150–250` từ thuyết minh/giảng giải thực chất cho mỗi bài đạt `>= 9.0p` (`>= 9.2p` an toàn).
