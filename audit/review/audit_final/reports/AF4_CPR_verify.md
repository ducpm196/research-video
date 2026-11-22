# WP-AF4-2 Independent Read-Only Verification Report — Course CPR (`L00–L09`)

**Verifier:** `f4a51c55` (`WP-AF4-2 CPR Verifier`, read-only)

## 1. Automated & Structural Checks (Directly Observed)
- **`audit/cpr/verify_cpr.py`**: **37/37 PASS** (all 19 `example`/`check` C11 programs + all 10 `labs/CPR/L00..L09/loi_giai.c` compiled & run via GCC vs `mong_doi.txt` + 8 `checklib` cross-checks).
- **`tools/lv.py lint` (L00–L09)**: **0 FAIL, 0 WARN** across all 10 specs (word counts 903–1,015, all ≤ 2,300; E39/E51/E53 PASS).
- **`tools/lv.py curriculum curriculum/cpr.yaml`**: **10 bài, 10 đã có đặc tả, 0 lỗi**.
- **`audit/review/screen_code.py check --course CPR`**: **48/48 PASS** (`run/c` 19, `output/-` 19, `other/text` 10; `0 FAIL, 0 STALE, 0 MISSING, 0 ORPHAN`).
- **`build_report.json` / `SRT` / `ASR` (L00–L09)**: **10/10 PASS** (`spec_sha256` & `tts_sha256` match 10/10; `caption == Lxx.srt` 0 diffs across all 10 lessons; `asr_report.md` `thiếu audio: 0`, `chưa xem xét: 0` on all 10).
- **`lab_gate.py CPR`**: Coordinator already ran outside sandbox (`10 PASS · 0 FAIL`).

## 2. Totals & Summary Rates (Before Fix)
- **MUST total**: **1** (`L09 example.3` `say` calls `clean=1` "tổng kích thước dữ liệu cuối bằng không" instead of `v.d == NULL` pointer nullified)
- **SHOULD list**: **14 items**
- **P1=2 rate**: **1/10 (10%)** (`L00`=2; `L02–L09`=1; `L01`=0) -> NEEDS FIX to >=80%
- **P8=2 rate**: **10/10 (100%)**
- **P9=2 rate**: **7/10 (70%)** (`L00`, `L02`, `L09` have SVG box/arrow clipping/overflow)
- **Verdict**: **NO-GO / NEEDS FIXES** -> fixing MUST + 3 SVG boxes + P1 "tại chỗ" C syntax glosses across `L00–L09`.

## 3. Detailed Issues to Fix
1. **L09 `example.3` (MUST)**: `clean=1` comes from `v.d == NULL`, fix `say` to state pointer `v.d` is already `NULL` (`clean=1`) after free (not total size = 0).
2. **SVG clipping/overflow (L00, L02, L09)**:
   - `L00 intuition.1`: widen gaps or shorten arrow labels (`"GCC biên dịch"`, `"Nạp vào RAM"`).
   - `L02 intuition.1`: widen gaps or shorten arrow labels (`"Sao chép 10, 25"`, `"return → xoá khung"`).
   - `L09 intuition.1`: widen orange Box 2 (`"2. Đầy → Kiểm & Nhân đôi"`) so text stays inside border.
3. **P1 C11 syntax "tại chỗ" & SHOULD alignment**:
   - `L00 example.1`: narrate all 4 rows in table or match table rows to `say`/`focus`.
   - `L01`: explain `<stdint.h>` (`INT32_MAX`/`INT32_MIN`), `%u`, `%d`, `static`, `&&`, `?:` cleanly before/at use (`example.1` currently says `<limits.h>` which is unused).
   - `L02`: explain `static` helper function and `%d`; remove unused `?:` row or show it cleanly.
   - `L03`: briefly gloss `const` (read-only array param) and `(void)need;` (`-Werror` unused-param silence).
   - `L04`: clarify `0x7000` (hex address), `||`, `if (q)` (`q != NULL`); make `say` say `"không ích bảy nghìn"` cleanly or `"địa chỉ thập lục phân bảy nghìn"`.
   - `L05`: define `ptrdiff_t`, `<stddef.h>`, `%td` cleanly in `example.1`.
   - `L06`: note `!p` means `p == NULL` in `example.1` / `intuition`.
   - `L07`: align `quymo.1` `say` with the `1 000 / 100 000 / 1 000 000` table (say `"một trăm nghìn bản ghi"`), define `offsetof` macro (`<stddef.h>`) and `while (h)` (`h != NULL`).
   - `L08`: gloss `<<`, `|`, `0xFFF`, `FILE *`, `fclose` in `sym` / `example.1`.
   - `L09`: align `example.1` rows & `say`, fix `pitfalls.1` to 2-arg `_Static_assert(sizeof(Rec) == 16, "...")`, gloss `(Rec){...}` and `(unsigned long long)sum` + `%llu`.
