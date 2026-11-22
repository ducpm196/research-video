# Báo cáo Kiểm chứng Độc lập WP-AF4-5 Stage 9 — Khoá CVI (L00–L12)

## 1. Tóm tắt kiểm tra tự động
- `audit/cvi/verify_cvi.py`: `112/112 PASS`
- `tools/lv.py curriculum curriculum/cvi.yaml`: `13 bài, 0 lỗi`
- `tools/lv.py lint lessons/cvi/L*.yaml`: `13/13 PASS` (`0 FAIL, 0 WARN`)
- `loi_giai.py` vs `mong_doi.txt`: `13/13 khớp 100%`
- `audit/review/screen_code.py check --course CVI`: `27/27 PASS`
- `audit/layout_CVI.tsv`: `0` lỗi bố cục; 19/19 `<svg>` sạch
- Thời lượng: `11.7–19.0` phút (tất cả `>= 9.0` phút)

## 2. Phán quyết: **NO-GO**

## 3. Danh sách lỗi MUST fix

### A. `[P1]` Bảng đọc mã Python & thuật ngữ
- 13/13 bài dính false positive `{...}` -> `dict`/`set`, `%`, `for/slice` từ `_legacy_build_read_rows` + thiếu `= / + / - / * / /`, `lambda`, `[x] * N`, `M[i][j]`, `a, b = ...`. (Lưu ý bổ sung `"ceil"` vào `ast_p1.py` cho `L05`; đồng bộ `up_s9_llm_rl_cv.py` ở `L08, L09, L12` với `labs/cvi/`).
- `L00`: dùng `gamma` ở `practice#0`/`de.md` nhưng thân bài chỉ nói "đường cong".
- `L04`: dùng `(như SIFT)` ở `practice#0`/`de.md` nhưng thân bài không giới thiệu `SIFT`.

### B. `[P8]` Lộ đáp số / công thức & trùng số thân bài trong `de.md`
- Lộ đáp số / công thức trong `de.md`:
  - `L01/de.md:3`: lộ `-40` và `0`.
  - `L02/de.md:3`: lộ `t = 12`.
  - `L06/de.md:1,3`: tiêu đề lộ `Z = fB/d`, nội dung lộ `42, 10.5` và công thức `f*B/(d - 1) - Z`.
  - `L07/de.md:3`: lộ `(h_flip_2, rot180_6)` (= `broken_augs=2`).
  - `L00/de.md:3`: chép nguyên biểu thức `((128/255 + 0.055)/1.055)^2.4`.
- Lặp bộ số bài giảng: `12/13` bài `L00–L11` (và `L12` nên chọn sự kiện khác trong bài như 2010–2011 / 2019–2020 để tránh lặp y nguyên kết quả `4.2x, 12.5x, 2251`).

### C. `covers:` sai cảnh dạy (`12/13` bài `L00–L06, L08–L12`)
- `L00` obj1→`sym/intuition`, obj2→`prereq/intuition`, obj3→`example`
- `L01` obj3→`blur`
- `L02` obj1→`sym/intuition`, obj2→`example`
- `L03` obj2 bổ sung `sym`
- `L04` obj4→`pitfalls`
- `L05` obj1→`hook/pitfalls`, obj2→`concept`, obj4→`pitfalls`
- `L06` obj1→`row`, obj4→`quiz/pitfalls`
- `L08` obj2→`nms`
- `L09` obj3→`rare`
- `L10` obj3→`example`, obj4→`real/pitfalls`
- `L11` obj2→`counterfactual`, obj4→`counterfactual/pitfalls`
- `L12` obj1→`stage1..stage6`

## 4. Danh sách SHOULD fix
- `L00 recap.1`: sửa lệch đơn vị `MiB` ↔ `MB` và mở nghĩa `1080p`, `4K` (lẫn `L01` `4K = 3840 × 2160`).
- `L04 recap.1`: viết `&lt; 0,8` thay `< 0,8`.
- `L07 recap.1`: đổi `500 ảnh` → `300 ảnh` cho khớp thân bài.
- `L10 recap.1`: sửa lời đọc `"nửa đêm"` thành `"một nửa ban đêm"`.
- `L12 recap.1`: bỏ hoặc mở nghĩa `AlexNet` và `GPU` trên `show` khớp `say`.
- `L11/de.md:1`, `L12/de.md:1`: bỏ `(shortcut learning)` và `top-5` không có trong bài.
- `labs/cvi/L09/loi_giai.py:6`: đổi tên biến `iou_bg` → `iou_obj_all_bg` cho rõ nghĩa.
