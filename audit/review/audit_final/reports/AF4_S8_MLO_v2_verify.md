# Báo cáo Kiểm định Độc lập WP-AF4-5 Stage 8 — Khoá `MLO` (`L00–L14`, 15 bài) [Verifier v2]

**Phán quyết tổng thể: `NO-GO`**

## 1. Tóm tắt kiểm tra tự động
- `audit/mlo/verify_mlo.py`: **20/20 PASS**
- `tools/lv.py lint` (`L00–L14`): **15/15 PASS** (`0 FAIL, 0 WARN`, 191/191 `checks`)
- `loi_giai.py` vs `mong_doi.txt`: **15/15 PASS**
- Chính tả `SPELL_CANON` / `"càng "` (9 câu) / lặp ngoặc / 18 `<svg>`: **Sạch**
- `tools/lv.py verify`: **15/15 FAIL (STALE)** (`build_report.json` thuộc `2026-11-19`)
- `audit/layout_MLO.tsv`: trống (chờ chạy lại sau sửa)

## 2. Danh sách MUST fix

1. **Rebuild toàn bộ 15 bài (`L00–L14`) + `layout_scan.py MLO` + ASR** (cùng bổ sung lời cho 8 bài `< 9,0p`: `L02, L03, L05, L06, L09, L10, L11, L13`).
2. **Lỗi toán `L07 recap#1`**: `5% → 6%` ghi nhầm `14 751` (đúng là **`8158`**; `14 751` là cho `10% → 11%`).
3. **`[P1]` Bảng đọc mã `practice` lỗi 14/15 bài**: Chạy lại với `ast_p1.py` (bỏ `{...}` dict/set thừa ở 14 bài và `%` chia dư giả ở `L00, L12, L13`; bổ sung `.sample`, `==`, `!=`, `in`, `>=`, `.values()`, `<`, `.random()`, `0.1 <= psi < 0.25`, `key=/reverse=`).
4. **`covers:` sai ở 9/15 bài (`L00, L01, L03, L06, L07, L08, L12, L13, L14`)**:
   - `L00` obj2→`sym`; `L01` obj3→`pitfalls`; `L03` obj1→`sym/quiz`; `L06` obj1→`sym/pitfalls`; `L07` obj1→`sym/pitfalls/practice`; `L08` obj2→`sym/pitfalls`; `L12` obj1→`sym/pitfalls/quiz`; `L13` obj3→`pitfalls`; `L14` obj1→`stage1..4`, obj3→`quiz`.
5. **`[P8]` Lỗi `de.md`**: `L13/de.md:1` lộ `99%` ở tiêu đề; `L00, L04` lặp số thân bài; `L09` thiếu quy ước phá hoà chỉ số nhỏ hơn; `L06` thiếu quy ước làm tròn nguyên (`1067`); `L10` lộ `(p - y)^2`, `L14` lộ `4 * 3 * 2`, `L01` lộ `random.Random(seed).sample(...)`.
6. **`[P1]` Thuật ngữ mới chưa giảng trong `recap#1` & `de.md`**: `GPU` (`L01`), `TB/petabyte` (`L02`), `CI/ms` (`L03`), `req/s` (`L06`), `top-2` (`L09`), `RAM/băng thông` (`L11`), `API` (`L13`), `fp32/RAM/q_max` (`L11/de.md`), `float/int` (`L11 example#3`), đồng bộ tên `PSI`/`Brier`.

## 3. SHOULD fix
- Đưa 8 bài `< 9,0p` (`L03, L13, L05, L11` ưu tiên cao) lên `>= 9,0p` thực tế.
- Cập nhật `curriculum/mlo.yaml` (`status: active`) khi hoàn tất.
- Sửa diễn đạt nhỏ: `L09 recap#1` (`40% → 57% → 88%`), `L12` chú thích `Clopper–Pearson`, `&lt;` trong HTML (`L03, L11, L13`), `L11` tránh mốc làm tròn `.5` (`-57.15`).
