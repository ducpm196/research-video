# Báo cáo kiểm định độc lập WP-AF4-5 Stage 9 — Khoá AGT (`L00–L12`, v2)

**Phán quyết tổng thể: `NO-GO`**

Đã đọc và kiểm toàn diện `curriculum/agt.yaml`, 13/13 bài `lessons/agt/L00..L12.yaml`, 13/13 bộ lab `labs/AGT/L00..L12/{de.md, loi_giai.py, mong_doi.txt}`, `audit/agt/verify_agt.py`, `audit/agt/sources_L12.md`, `audit/review/screen_code/AGT.yaml`, `audit/layout_AGT.tsv`, `audit/s9_11/{common.py, ast_p1.py, up_s9_llm_rl_cv.py}`, `tools/{lv.py, checklib.py}`.

## 1. Tóm tắt kiểm tra tự động

| Hạng mục kiểm tra | Kết quả | Chi tiết |
|---|---|---|
| `audit/agt/verify_agt.py` | **15 PASS · 0 FAIL** | Khớp 100% nguồn L12 và kiểm toán học |
| `tools/lv.py curriculum curriculum/agt.yaml` | **PASS (0 lỗi)** | 13 bài |
| `tools/lv.py lint lessons/agt/L*.yaml` | **13/13 PASS** | `0 FAIL, 0 WARN` |
| `loi_giai.py` vs `mong_doi.txt` | **13/13 PASS** | `rc=0`, khớp stdout 100% |
| `audit/review/screen_code/AGT.yaml` | **28/28 khớp SHA** | 0 thiếu, 0 thừa, 0 lệch SHA |
| Thời lượng bài (`>= 9.0` phút) | **13/13 ĐẠT** | `10.1–19.8` phút (+ pause `11.1–21.1` phút) |
| Lỗi lặp ngoặc đơn / `"càng "` / SVG | **0 lỗi** | 3 câu `"càng "` đều chuẩn logic |
| Trạng thái MP4 & `layout_AGT.tsv` | **STALE 13/13** | Cần chạy `layout_scan` + rebuild MP4 |

## 2. Lỗi MUST fix

### M1. `[P1]` Bảng đọc mã `practice` lệch 13/13 & thiếu thuật ngữ
- False positive `{...}` -> `dict`/`set`, `%` modulo, comprehension sai (xử lý qua `ast_p1.py`).
- Thiếu token thực tế: `L01` (`isinstance`, `not isinstance(..., bool)`, `.isdigit()`, `*c`, `and not`, `0 < amt <= 10_000_000`), `L02` (generator `...`, `default=0`, `.values()`), `L04` (`in`), `L05` (`tp, fp = ...`), `L08` (`toks[-1]`, `range(...)`), `L09` (`policy.get(a)`, `==`), `L10` (`.values()`).
- Thiếu giải thích thuật ngữ: `L01` (`bool`, `isinstance`, `.isdigit()`), `L10` (`quy luật Pareto` chưa được định nghĩa trước `de.md`/`practice#0`).

### M2. `[P8]` `de.md` trùng bộ số bài giảng (11/12 bài thường) & lộ đáp số (`L06`, `L12`)
- `L06/de.md:3`: lộ công thức `n*(n-1)` và `2*(n-1)`.
- `L12/de.md:3`: lộ đáp số `45`.
- `L00, L02..L11`: lặp bộ số ví dụ từ `example`.
- `L01`: thiếu ca biên `bool` (`True`) trong `calls`.

### M3. `covers:` sai 8/13 bài
- `L01` obj 1 → `sym`
- `L02` obj 3 → `sym` / `pitfalls`
- `L03` obj 2 → `sym`
- `L04` obj 3 → `example` / `pitfalls`
- `L05` obj 2 → `sym` / `pitfalls` / `quiz`
- `L07` obj 3 → `sym` / `pitfalls`
- `L11` obj 2 → `sym`/`quiz`, obj 3 → `sym`/`pitfalls`
- `L12` obj 3 → `quiz`, obj 1 → phủ `stage1..stage5`

### M4. Rebuild MP4 & `layout_scan.py AGT`

## 3. SHOULD fix
- `L05:64,83`: diễn đạt `TPR/FPR/base` rõ hơn trong bảng.
- `[P9]` đồng bộ số `recap` khớp thân bài (`L00, L03, L07, L08`) và bổ sung số lớn định lượng (`L01, L04, L09, L10`).
- Đổi `"vs"` → `"so với"` (`L06, L07, L11`), gọi rõ `SWE-bench Verified` ở `L12 stage5`.
- `covers:` phụ trợ: `L00` obj 3, `L08` obj 2.
