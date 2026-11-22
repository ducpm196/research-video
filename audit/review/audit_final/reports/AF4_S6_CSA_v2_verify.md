# Independent AF4 Re-Verification Report — CSA `L00–L14` (+ `L15–L16` Add-on)

**Verifier:** `a6ba53a5` (`WP-AF4-3 Stage 6 CSA Verifier v2`, read-only)  
**Verdict: `GO`**
- **MUST blockers:** **`0`** *(all 4 prior MUST items in L04, L07, L11, and L08/L10/L14 are resolved & rebuilt)*
- **P1 (Self-contained inline glossing):** **`15 / 15` (`100%`, or `13–14 / 15` = `86.7%–93.3%` under strictest reading of L11/L14 `practice` table cells)** *(target `>= 80%` — **PASS**)*
- **P8 (Exact `say`/`show`/`lab` alignment + genuine solution, no hardcoding):** **`15 / 15` (`100%`)** *(target `100%` — **PASS**)*
- **P9 (Visual layout clarity & `clear: true` before big blocks):** **`15 / 15` (`100%`)** *(target `>= 80%` — **PASS**)*

---

## 1. Build / SHA / SRT / ASR / Layout / Checks Summary (`15/15` PASS; `L15–L16` `2/2` PASS)

All 17 CSA lessons (`L00–L16`) were rebuilt on `2026-11-19T13:09:13Z`–`13:40:53Z` (`out/CSA/Lxx/Lxx.mp4` present) and verified read-only against `D:\research-video\tools\lv.py` & `checklib.py`:
- **`spec_sha256` & `tts_sha256`:** `15/15` (`L00–L14`) and `2/2` (`L15–L16`) exact match.
- **SRT vs `say`/`caption`:** `15/15` (`L00–L14`) and `2/2` (`L15–L16`) exact sentence-by-sentence match.
- **`asr_report.md`:** `17/17` (`L00–L16`) report **`thiếu audio: 0`** and **`chưa xem xét: 0`**.
- **`audit/layout_CSA.tsv`:** Empty (2 bytes `\r\n`, `0` layout defects).
- **YAML `checks`:** Executed all `310` check expressions across `L00–L16` (`276` in `L00–L14`, `34` in `L15–L16`) with `checklib` as `alg` — **`0` failures**.
- **`practice` language labels:** `L00–L05` use `"C (C11)"`; `L06–L16` use `"Python"`. All `practice` steps (and `L03/code_read`) have `clear: true`.

---

## 2. Verification of Prior MUST & P1 Blockers (`4/4` FIXED)
1. **`L04` (`P8` + `P1` — FIXED):** `labs/CSA/L04/de.md`, `loi_giai.c`, `mong_doi.txt`, and `L04` `practice` match 100% (`FLT_EPSILON` glossed inline; genuine non-associativity + `<float.h>`).
2. **`L07` (`P8` + `P1` — FIXED):** `labs/CSA/L07/loi_giai.py` counts `iters += 1` inside `while r2 <= 10:`; `de.md` aligns with `BLE (nhảy nếu ≤)`.
3. **`L11` (`P8` + `P1` — FIXED):** `labs/CSA/L11/de.md` glosses `Tag/Index/Offset` alongside `thẻ/chỉ số/độ dời` and aligns `conflict_at_0x80=2` with `mong_doi.txt`, `loi_giai.py`, and `L11 practice`.
4. **`L08`, `L10`, `L14` (`P1` — FIXED):** `IC`, `AMAT`, `VPN`, `EAT` glossed inline.

---

## 3. Add-on Spot-Check: `L15–L16` (`2/2` PASS) & Visual PNG Inspection (`24` frames)
- `L15` & `L16` pass SHA, SRT, ASR (`0` missing / `0` unreviewed), checks (`11/11` & `23/23`), and lab match.
- Visually inspected **24 `1920x1080` PNGs** across `L03, L04, L07, L08, L10, L11, L14, L15, L16` — all crisp, zero clipping/overlap/overflow.
