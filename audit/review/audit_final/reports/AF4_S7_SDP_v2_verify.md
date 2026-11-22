# WP-AF4-3 Stage 7 Verification Report v2 — Course `SDP` (`L00–L15` + `L16–L17` currency)

**Verifier:** `e3df1abf` (`WP-AF4-3 Stage 7 SDP Verifier v2`, read-only)  
**Verdict: `GO`** (`MUST: 0`, `P1: 16/16 = 100%`, `P8: 16/16 = 100%`, `P9: 16/16 = 100%`, `L16–L17: 2/2 PASS`)

---

## 1. Prior `MUST-1` (`SDP L13`) — Verified Fixed
- Lab & `L13` `practice` now teach **Mùi mã và tái cấu trúc an toàn** (`fee_old` vs `fee_new` across 10,000 `random.Random(1)` pairs + `fee_bug` missing `max(0, k - 5)` + `(500000, 3)`). Zero hardcoding.
- Executed `labs/SDP/L13/loi_giai.py`: `new_mismatches=0`, `bug_mismatches=817`, `edge_500k_3km=550000` (exact match with `mong_doi.txt` & `practice`).
- Inspected `out/SDP/L13/frames/{00021,00072,00073,00074,00075,00076,00077}.png` via `read_file`: crisp, zero overlap/clipping.

## 2. Whole-Course Verification (`L00–L17`)
- `lv.py curriculum`: `18/18` 0 errors; `screen_code`: `56 khối — PASS 57 · FAIL 0`; `verify_sdp.py`: `36 PASS · 0 FAIL`; `layout_SDP.tsv`: `0`; `lv.py lint` & `lv.py verify`: `18/18 PASS`; `checks`: `206/206 PASS`; `SRT == say`: `18/18`; `ASR`: `18/18` `0 thiếu / 0 chưa xem xét`.
- **Verdict: `GO`**.
