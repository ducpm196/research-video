# Independent AF4 Verification Report — `DBS` `L00–L14` (15 lessons)

**Verifier:** `7e0dcc84` (`WP-AF4-3 Stage 7 DBS Verifier`, read-only)
**Scope verified (read-only):** `lessons/dbs/L00..L14*.yaml`, `labs/DBS/L00..L14/{de.md,loi_giai.sql,mong_doi.txt}`, `audit/review/screen_code/DBS.yaml`, `audit/layout_DBS.tsv`, `out/DBS/L00..L14/{build_report.json,L*.srt,asr_report.md,L*.mp4}`, and 51 rendered `frames/*.png` visually inspected via `read_file` (≥3 PNGs/lesson covering SVG, tables, code, dense stacks, and AF2 `practice`).

---

## 1. Build / SRT / ASR / Layout Sync & Visual Inspection

- **Build & Hash Sync (`lv.spec_digest`, `lv.tts_digest`, `lv.cmd_verify`):** **15/15 PASS** (`rc=0`). Every `out/DBS/L00..L14/build_report.json` matches current YAML `spec_sha256` and `tts_sha256`; all 15 MP4s have `h264` + `aac`, `1920x1080`, and duration within `0.01s` of `timeline_seconds`.
- **SRT vs `say`:** **15/15 exact match.** Normalized concatenation of all step `say` fields equals concatenated `L*.srt` cues, and cue count == `frames` in `build_report.json` for all 15 lessons (82–110 cues/frames per lesson).
- **`asr_report.md`:** **15/15** have `thiếu audio: 0` and `chưa xem xét: 0`. (`gắn cờ` counts: L00:5, L01:0, L02:4, L03:1, L04:7, L05:7, L06:3, L07:13, L08:1, L09:0, L10:5, L11:3, L12:7, L13:2, L14:5; note many reviewed rows still carry `NOT_VERIFIED bằng tai người` comments).
- **`audit/layout_DBS.tsv`:** **2 bytes** (empty; 0 layout overflow errors).
- **Visual `frames/*.png` inspection (51 PNGs via `read_file`):**
  - Clean rendering (zero clipping/viewport overflow) across code, tables, subtitles, dense 3-block frames (`L04/00012.png`, `L07/00075.png`, `L10/00013.png`, `L11/00012.png`), and `practice` expected-output blocks.
  - **Observed visual defects:**
    1. `out/DBS/L11/frames/00085.png` (`practice` step 0 `Kiểm chứng` cell): mid-word truncation `"bảo đảm nguyên tử A"` (cut off `"ACID"`).
    2. `out/DBS/L09/frames/00024.png` (SVG): blue vertical pointer arrow tip overlaps `"n"` of `"ngăn 3"`.
    3. `out/DBS/L11/frames/00026.png` (SVG): dashed red return arc cuts directly across the red label `"lỗi → huỷ cả nhóm → quay về đúng trạng thái đầu, tổng vẫn 150"`.

---

## 2. P1 — Self-Contained Inline Glossing: **7/15 (46.7%)** *(Target: ≥80% — FAIL)*

- **Whole-lesson bodies (excluding AF2 `practice` & `de.md`):** **15/15** well self-contained in Vietnamese; technical/SQL concepts and symbols are consistently glossed inline.
- **AF2 `practice` + `labs/DBS/Lxx/de.md` gaps (8 lessons introduce unglossed terms):**
  - **L00:** `PRAGMA foreign_keys=ON` (`practice` + `de.md`; `PRAGMA` never appears in L00 body), `PK`, `FK`, `INSERT OR IGNORE` unglossed in `de.md`.
  - **L01:** `CROSS JOIN`, `INNER JOIN` unglossed in `practice`/`de.md` (L01 body only teaches relational algebra `×`, `⋈`, and plain `JOIN`).
  - **L06:** `INSERT OR IGNORE` unglossed in `de.md`.
  - **L07:** `CTE đệ quy` (`de.md`), `EXPLAIN QUERY PLAN` (`de.md`), `SCAN` (`practice`/`de.md`) appear without inline glossing (taught later in L09/L10/L16).
  - **L08:** `B-Tree` (`practice`/`de.md`; lesson teaches `cây B+`), `SCAN`, `SEARCH USING INDEX` (`practice`), `CREATE INDEX`, `BETWEEN` (`de.md`) unglossed.
  - **L11:** `SAVEPOINT` in `de.md` (not taught until L15) + truncated `ACID` -> `A` in `practice`.
  - **L12:** `CTE đệ quy` unglossed in `de.md`.
  - **L14:** `WAL`, `checkpoint`, `REDO`, `UNDO`, `COMMIT` used raw in `practice`/`de.md` without inline Vietnamese glosses (L14 body uses `"ghi nhật ký trước"`, `"điểm kiểm tra"`, `"pha làm lại"`, `"pha huỷ"`, `"ghi nhận"`).
- **Pass P1 cleanly (7/15):** L02, L03, L04, L05, L09 (minor `BETWEEN` in `de.md`), L10, L13 (minor `Wait-For` in `de.md`; `2PL` is glossed in `practice`).

---

## 3. P8 — Exact Numerical/Code/Output Alignment & Genuine Lab Solutions: **13/15 (86.7%)** *(Target: 100% — FAIL)*

- `lv.lint`: 15/15 `0 errors, 0 warnings`.
- Scene `checks`: **318/318 PASS** across L00–L14.
- `audit/review/screen_code/DBS.yaml`: covers screen SQL/pseudo blocks.
- `practice` step 1 `<div>` lines vs `mong_doi.txt`: **15/15** exact match.
- `loi_giai.sql` vs `mong_doi.txt` (executed in SQLite 3.49.1 `:memory:` autocommit matching `sqlite3`/`sqlrun.py`): **15/15** output match; solutions compute via SQL queries/constraints rather than hardcoding constants.
- **P8 Failures (2/15):**
  1. **L05:** `labs/DBS/L05/de.md` states `3. bad_join_rows=5`, directly contradicting `labs/DBS/L05/mong_doi.txt`, `labs/DBS/L05/loi_giai.sql` (2×3 = 6 rows), and `lessons/dbs/L05_chuan_hoa.yaml` (`practice` step 1 + `00084.png`), which all expect **`bad_join_rows=6`**.
  2. **L11:** `lessons/dbs/L11_giao_dich_acid.yaml` `practice` step 0 (`00085.png`) truncates `"nguyên tử ACID"` to `"nguyên tử A"`. Furthermore, `labs/DBS/L11/de.md` asks for `TaiKhoan(id, so_du)` and `"thử giao dịch trừ 80 rồi ROLLBACK"` (which would hit `CHECK(so_du >= 0)` on `60 - 80 = -20`) plus mentions `SAVEPOINT`, whereas `labs/DBS/L11/loi_giai.sql` uses `TK(id, sd)` and runs `UPDATE TK SET sd=sd-20 ...; ROLLBACK;` (never testing `-80` or `SAVEPOINT`).
- **Minor alignment notes (still pass SQL computation):**
  - **L00:** `de.md` specifies `(1,'Trung','K1')` and `INSERT OR IGNORE ... (2,'Em','K9')`; `loi_giai.sql` uses `(1,'Bi','K1')` and `INSERT INTO SV SELECT 2,'Em','K9' WHERE EXISTS(...)`.
  - **L07:** `de.md` asks to verify `EXPLAIN QUERY PLAN ...` outputs `SCAN Logs`; `loi_giai.sql` checks `1 - EXISTS(SELECT 1 FROM sqlite_master WHERE type='index' ...)`.

---

## 4. P9 — Visual Layout Clarity & `clear: true`: **13/15 (86.7%)** *(Target: ≥80% — PASS)*

- `audit/layout_DBS.tsv` has 0 errors; all 15 `practice` scenes set `clear: true` on both steps.
- All 51 inspected frames fit inside 1920×1080 without overflow.
- **Deductions (2/15):**
  - **L09:** SVG pointer arrow overlaps `"ngăn 3"` in `00024.png`.
  - **L11:** Truncated `"nguyên tử A"` in `00085.png` + SVG dashed arc crosses red caption text in `00026.png`.
- Note: Several non-practice scenes append big tables/code blocks without `clear: true` (reaching 3 stacked blocks in `L04 prereq.2`, `L07 quiz.2`, `L10 prereq.2`, `L11 prereq.2`), though rendered frames still fit cleanly.

---

## 5. Blockers, Improvements & Verdict

### MUST Blockers
1. **Fix L05 P8 mismatch:** Update `labs/DBS/L05/de.md` line `3. bad_join_rows=5` → `bad_join_rows=6` to match `mong_doi.txt`, `loi_giai.sql`, and `L05_chuan_hoa.yaml`.
2. **Fix L11 truncation & lab alignment:**
   - Fix truncated `"bảo đảm nguyên tử A"` in `lessons/dbs/L11_giao_dich_acid.yaml` `practice` step 0 (restore `ACID` or concise phrasing) and rebuild L11.
   - Align `labs/DBS/L11/de.md` and `labs/DBS/L11/loi_giai.sql` (table/column names, `-80` vs `-20`, remove `SAVEPOINT` from L11 or align with L15).
3. **Fix P1 glossing in AF2 `practice` & `de.md` (currently 7/15 < 80%):** Add inline Vietnamese glosses for unglossed terms in `L00` (`PRAGMA foreign_keys=ON`, `PK`, `FK`, `INSERT OR IGNORE`), `L01` (`CROSS JOIN`, `INNER JOIN`), `L06` (`INSERT OR IGNORE`), `L07` (`CTE đệ quy`, `EXPLAIN QUERY PLAN`, `SCAN`), `L08` (`B-Tree`/`cây B+`, `SEARCH USING INDEX`, `CREATE INDEX`, `BETWEEN`), `L11` (`SAVEPOINT`), `L12` (`CTE đệ quy`), and `L14` (`WAL`, `checkpoint`, `REDO`, `UNDO`, `COMMIT`), rebuilding any modified lesson YAMLs.

### SHOULD Improvements
1. **SVG polish:** Adjust arrow/label coordinates in `L09` (`ngăn 3`, frame `00024.png`) and `L11` (dashed return arc vs caption, frame `00026.png`).
2. **Lab fidelity (`L00`, `L07`, `L09`, `L13`):** Align `L00` `loi_giai.sql` with `de.md` (`'Trung'` and `INSERT OR IGNORE` for `'K9'`); clarify `sqlite_master` check in `L07/de.md`; gloss `BETWEEN` (`L09`) and `đồ thị chờ (Wait-For)` (`L13`).
3. **`clear: true` hygiene:** Consider `clear: true` before 3-block stacks (`L04 prereq.2`, `L07 quiz.2`, `L10 prereq.2`, `L11 prereq.2`).
4. **ASR spot-listening:** Optionally human-verify flagged lines marked `NOT_VERIFIED bằng tai người` (notably L07:12, L00:5, L05:5, L10:5).

### **Verdict: `NO-GO`**
*(Fails P8 100% target due to `L05 de.md` `5` vs `6` contradiction and `L11` screen text truncation/lab divergence, and fails P1 ≥80% target due to unglossed AF2 terms in 8/15 lessons.)*
