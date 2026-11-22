# WP-AF4-3 Stage 7 Verification Report — Course `WEB` (`L00–L15`)

**Verifier:** `b2c82dcd` (`WP-AF4-3 Stage 7 WEB Verifier`, read-only)  
**Verdict: `GO`** (`MUST: 0`, `P1: 88% >= 80%`, `P8: 100%`, `P9: 94% >= 80%`)

---

## 1. Observed Checks (`L00–L15`, 16 lessons)
- `lv.py curriculum`: `16 bài, 16 đã có đặc tả, 0 lỗi`; `lv.py lint` & `lv.py verify`: `16/16 PASS`.
- `spec_sha256` & `tts_sha256`: `16/16 match` (rebuilt `2026-11-20 00:13–00:49` local).
- `SRT == say`: `16/16`; `ASR`: `16/16` (`thiếu audio: 0`, `chưa xem xét: 0`); `layout_WEB.tsv`: `0`.
- `screen_code`: `23/23 PASS`; `verify_web.py`: `15/15` non-`asyncio` checks PASS (`L04` async covered by `Node.js` + `ThreadPoolExecutor` in `L04` checks); `node labs/WEB/L00..L15/loi_giai.js == mong_doi.txt`: **`16/16 PASS`**, zero hardcoded `console.log`/`print`; all `16/16` `practice#0` tables show **`Node.js`**.
- **Visual PNG inspection:** `40` `1920x1080` PNGs across `L00–L15` inspected via `read_file` — crisp, zero clipping or overlap.

## 2. Minor Non-Blocking Notes
- Optional P1 glosses in `L02/L03/L07/L09/L10/L15` (`practice#0`/`de.md`), `L04/de.md` `async` prose, `L11` `WCAG 2.1` vs `2.2` label.
