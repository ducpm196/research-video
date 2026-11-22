# Independent AF4 v2 Verification Report — `DBS` (`L00–L14` + `L15–L17` spot-check)

**Verifier:** `5758ecfe` (`WP-AF4-3 Stage 7 DBS Verifier v2`, read-only)  
**Verdict: `GO`** (`MUST: 0`, `P1: 15/15 = 100%`, `P8: 15/15 = 100%`, `P9: 13/15 = 86.7%`, `+L15–L17 3/3 PASS`)

---

## 1. Build / Hash / SRT / ASR / Curriculum Sync (`L00–L17`)
- `lv.py curriculum curriculum/dbs.yaml`: **18/18 PASS** (`0` errors).
- `lv.py lint` & `lv.py verify` on `L00–L17`: **18/18 PASS**, Scene `checks`: **361/361 PASS**.
- `spec_sha256` & `tts_sha256`: **18/18 match** (`L00–L17` rebuilt `2026-11-19 21:18–21:55` local).
- `SRT` vs `say`: **18/18 exact match**. `asr_report.md`: **18/18** `thiếu audio: 0`, `chưa xem xét: 0`.
- `audit/layout_DBS.tsv`: Empty (`0` layout overflow errors).
- SQLite Lab Execution (`labs/DBS/L00..L17/loi_giai.sql` vs `mong_doi.txt` & `practice`): **18/18 exact match**.

## 2. Prior Blockers, SVG & P1 Re-Verification
- **`L05` P8 (`5` vs `6`):** **FIXED** (`labs/DBS/L05/de.md` = `bad_join_rows=6`, confirmed in `out/DBS/L05/frames/00084.png`).
- **`L11` truncation & lab alignment:** **FIXED** (`out/DBS/L11/frames/00085.png` = `"bảo đảm tính nguyên tử (ACID)"`; `de.md` and `loi_giai.sql` aligned).
- **P1 inline glosses (`L00, L01, L06, L07, L08, L11, L12, L14`) + `SQL (SQLite)`:** **FIXED** (all 18 `practice` tables use `SQL (SQLite)`; `PRAGMA`, `PK/FK`, `CROSS/INNER JOIN`, `EXPLAIN QUERY PLAN`, `SCAN`, `B-Tree`, `CTE đệ quy`, `WAL`, `checkpoint`, `REDO/UNDO`, `COMMIT` glossed inline).
- **Visual PNG inspection (29 PNGs via `read_file`):** 27/29 crisp; non-blocking P9 SHOULD: `L09/00024.png` SVG arrow overlaps `"ngăn 3"` and `L11/00026.png` dashed red arc crosses red caption (likely overwritten when `upgrade_dbs.py` re-ran).

## 3. Scores
- `MUST`: **0** · `P1`: **15/15 (100%)** · `P8`: **15/15 (100%)** · `P9`: **13/15 (86.7%)** · `L15–L17` spot-check: **3/3 PASS** → **`GO`**.
