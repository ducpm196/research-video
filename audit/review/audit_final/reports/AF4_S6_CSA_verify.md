# Independent AF4 Verification Report — CSA `L00–L14` (15 lessons)

**Verifier:** `f692865b` (`WP-AF4-3 Stage 6 CSA Verifier`, read-only)
**Verdict: `NO-GO`**
- **P1 (Self-contained inline glossing):** **10 / 15 (66.7%)** *(target >= 80% — FAIL)*
- **P8 (Exact alignment + genuine solution, no hardcoding):** **12 / 15 (80.0%)** *(target 100% — FAIL; 3 MUST blockers: L04, L07, L11)*
- **P9 (Visual layout clarity & `clear: true` before big blocks):** **15 / 15 (100%)** *(target >= 80% — PASS)*

---

## 1. Build / SHA / SRT / ASR / Layout / Visual Sync (15/15 PASS)

All 15 lessons (`L00–L14`) were built `2026-11-19T00:55:01Z`–`01:28:02Z` and verified against `tools/lv.py` (`spec_digest`, `tts_digest`, `build_frames`):
- **`spec_sha256` & `tts_sha256`:** `15/15` exact match (`build_report.json` matches `lv.spec_digest(spec)` and `lv.tts_digest(lv.build_frames(spec))` for `L00–L14`).
- **SRT vs `say` (`caption`):** `15/15` exact sentence-by-sentence match (`L00`: 86, `L01`: 86, `L02`: 84, `L03`: 90, `L04`: 76, `L05`: 90, `L06`: 87, `L07`: 93, `L08`: 71, `L09`: 76, `L10`: 81, `L11`: 75, `L12`: 80, `L13`: 72, `L14`: 77 cues).
- **`asr_report.md`:** `15/15` have `thiếu audio: 0` and `chưa xem xét: 0` (`checked_at`: `2026-11-19T00:55:05Z`–`01:28:02Z`; flagged counts 0–23, all reviewed).
- **`audit/layout_CSA.tsv`:** Empty (2 bytes `\r\n`), `0` layout errors reported.
- **`checks` in `lessons/csa/L00..L14*.yaml`:** Executed all `276` Python check expressions across `L00–L14` — `0` failures.
- **Visual PNG inspection (`read_file`):** Inspected **45+ PNGs** across all 15 lessons (>= 3 per lesson covering SVGs, code blocks, `L03/code_read`, all 15 `practice` table & expected-output frames, plus worst-case multi-table stacked frames `L00/00053`, `L01/00051`, `L06/00042`, `L10/00047`, `L11/00029`, `L12/00028`, `L12/00068`). All inspected frames are crisp and legible with **zero** clipping, overlap, or overflow.

---

## 2. P1 — Self-Contained Inline Glossing (`10 / 15`, 66.7%)

Lesson body `sym` scenes and `assumes` are well-structured, **but 5 lessons have unglossed terms/symbols in the newly added AF2 `practice` scenes and/or `labs/CSA/*/de.md`:**
- **L04:** `mong_doi.txt` / `practice` outputs `eps_f32_lt_1e6=1` (`FLT_EPSILON`), which is never glossed in `de.md` or `L04` (`L04` `sym` only defines 64-bit `ε = 2^-52`, not 32-bit `FLT_EPSILON`).
- **L07:** `labs/CSA/L07/de.md` introduces `BLT` (`ADD, ADDI, BLT = 3 lệnh`) without glossing `BLT` (lesson `sym` taught `ble`, not `BLT`).
- **L08:** `practice` (`Phương trình hiệu năng CPU = IC × CPI / f`) and `de.md` (`IC = 1e9 lệnh`) use `IC` without glossing it (`Instruction Count` / số lệnh); the lesson body (`sym`) used `N`.
- **L10:** `practice` (`Phân cấp bộ nhớ và AMAT`) uses `AMAT` without inline glossing in the video (`L10` `amat` scene only said `"Thời gian truy cập trung bình"`, never `"AMAT"`; `de.md` does write `"thời gian truy cập trung bình AMAT"`).
- **L11:** `de.md` uses English `Tag/Index/Offset`, `idx`, `off`, and `conflict_at_0x80` without mapping to the lesson's Vietnamese terms (`thẻ, chỉ số, độ dời`) or explaining what `conflict_at_0x80` counts.
- **L14:** `practice` (`Dịch địa chỉ ảo, bảng trang và TLB EAT`) and `de.md` (`VPN 0x05`, `tính EAT`) use **`EAT`** and **`VPN`** without ever glossing them in either the video or `de.md` (`L14` body only said `"Thời gian hiệu dụng"` and `"số trang"`).
- *(Note on L03 & L01: `L03` has `code_read` glossing `uint8_t / int8_t`, `(x >> k) & 1U`, `memcpy(&u, &f, 4)` — `uint8_t / int8_t` isn't used in L03's lab (`uint32_t` is), whereas `L01/de.md` uses `uint8_t` and `int8_t` without `code_read`, though `L01/de.md` gives `(255)` and `(-1)` inline.)*

*(Counting L04, L07, L08, L11, L14 as P1 fails -> `10/15`; even if L04 is counted under P8 only, `11/15` = 73.3% is still < 80%.)*

---

## 3. P8 — Exact Numerical / Code / Output Alignment (`12 / 15`, 80.0%)

Compiled/executed all 15 `labs/CSA/L00..L14/loi_giai.*` (`gcc -std=c11 -Wall -Wextra -Werror -lm` for `L00–L05`; `python` for `L06–L14`): all 15 exit 0 and match `mong_doi.txt` and `practice` step 2 (`<div>...</div>`) 100%. **However, 3 lessons have MUST-level P8 defects:**

1. **L04 (`labs/CSA/L04/de.md` vs `loi_giai.c` & `mong_doi.txt`):**
   - `de.md` explicitly asks to `"đối chiếu tổng Kahan vs cộng thẳng cho [1e16, 1.0, -1e16]"` and does **not** mention `FLT_EPSILON < 1e-6`.
   - `loi_giai.c` does **not** implement Kahan summation at all; instead it prints `eps_f32_lt_1e6=1` (`FLT_EPSILON < 1e-6f ? 1 : 0`), matching `mong_doi.txt` and `practice`. Thus `loi_giai.c` does not solve the Kahan task in `de.md`, and `de.md` misstates the 3rd computation.
2. **L07 (`labs/CSA/L07/loi_giai.py` & `de.md`):**
   - **Hardcoding:** `loi_giai.py` line 7 hardcodes `print('loop_iters=10')` instead of counting loop iterations in the simulation (`iters += 1`).
   - **Instruction mismatch:** `de.md` specifies `BLT` (`ADD, ADDI, BLT = 3 lệnh`) from `R2=1` to `N=10`, whereas `loi_giai.py` executes `while r2 <= 10:` (matching `ble` in `L07` lesson YAML, not `BLT` `<`).
3. **L11 (`labs/CSA/L11/de.md` vs `mong_doi.txt`, `loi_giai.py`, `L11` `practice`):**
   - `de.md` line 5 specifies expected output `3. conflict_at_0x80=1`.
   - `mong_doi.txt` line 3, `loi_giai.py` stdout, and `L11` `practice` step 2 all have `conflict_at_0x80=2` (because `[0x00, 0x04, 0x80, 0x08]` causes 2 conflict misses at index 0: `0x80` evicts `0x00`, then `0x08` evicts `0x80`, and `loi_giai.py` counts total conflicts `conf = 2` under the misleading key `conflict_at_0x80`). Anyone following `de.md` (`=1`) will fail `cham.sh`.

*(Minor SHOULD P8 completeness notes: `L01/de.md`, `L05/de.md`, and `L06/de.md` omit describing their 3rd output test case in the prose sentence — `u8_wrap_127_plus_1`, `fa_101`, `add_200_100` — though the expected format lines themselves list them and `loi_giai.*` computes them genuinely.)*

---

## 4. P9 — Visual Layout Clarity & `clear: true` (`15 / 15`, 100%)

- All 15 AF2 `practice` scenes and `L03/code_read` have `clear: true` on every step.
- All `intuition` (SVG) scenes start fresh scenes; all `pitfalls` scenes clear before step 2.
- All 45+ visually inspected PNGs (including stacked multi-table `verify`/`example`/`quiz` steps in `L00`, `L01`, `L06`, `L10`, `L11`, `L12`) render cleanly without clipping, overlap, or subtitle overflow.

---

## 5. Blockers & Improvements

### MUST Blockers (must fix & rebuild before `PASS`)
1. **`L04` (P8/P1):** Align `labs/CSA/L04/de.md`, `loi_giai.c`, `mong_doi.txt`, and `L04` `practice` — either implement Kahan vs naive sum in `loi_giai.c` & update `mong_doi.txt`/`practice`, OR update `de.md` to ask for `FLT_EPSILON < 1e-6` (with inline gloss of `FLT_EPSILON`) and drop the unimplemented Kahan prompt.
2. **`L07` (P8/P1):** Remove hardcoded `print('loop_iters=10')` in `labs/CSA/L07/loi_giai.py` (track `iters += 1` inside the `while` loop), and change `BLT` to `BLE` (glossed inline as `nhảy nếu ≤`) in `labs/CSA/L07/de.md` to match `while r2 <= 10:` and the lesson's `ble`.
3. **`L11` (P8/P1):** Fix the contradiction in `labs/CSA/L11/de.md` (`conflict_at_0x80=1` vs `mong_doi.txt` & `practice` `conflict_at_0x80=2`): either update `de.md` (and clarify whether it counts total conflict misses = `2`, or rename key consistently across `de.md`/`mong_doi.txt`/`loi_giai.py`/`practice` and rebuild `L11`), and gloss `Tag/Index/Offset` alongside `thẻ/chỉ số/độ dời`.
4. **`L08`, `L10`, `L14` (P1):** Add inline glossing for `IC` (`số lệnh`, `L08` `practice` & `de.md`), `AMAT` (`thời gian truy cập trung bình`, `L10` `practice`), and `VPN` (`số trang ảo`) + `EAT` (`thời gian truy cập hiệu dụng`, `L14` `practice` & `de.md`) so the course meets `P1 >= 80%`.

### SHOULD Improvements
1. **`L01` / `L03` (`code_read`):** Move/copy the `uint8_t / int8_t` gloss into `L01` (where `L01/de.md` uses `uint8_t`/`int8_t`) and tailor `L03/code_read` to `uint32_t` / `float` / `memcpy(&u, &f, 4)` used in `L03`.
2. **`L01`, `L05`, `L06` `de.md`:** Explicitly mention the 3rd test case in the prose instruction (`127 + 1` in `uint8_t`, `(a=1, b=0, cin=1)`, and `200 + 100`) so prose and numbered output lines match 1-to-1.
3. **`L06` `practice`:** Note the mapping `C → CF` and `V → OV` in `L06` `practice` or `sym`.
4. **`P9` hygiene:** Consider adding `clear: true` before stacked `<table`/`code` steps (`step > 0`) in `verify`/`quiz`/`example` scenes (e.g., `L00–L12, L14`) when refactoring, though current rendering has zero visual overlap/overflow.
