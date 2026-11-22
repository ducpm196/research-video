# WP-AF4-3 Stage 6 Verification Report — Course `OSY` (`L00–L15`)

**Verifier:** `737a6bfe` (`WP-AF4-3 Stage 6 OSY Verifier`, read-only)  
**Verdict: `GO`** (`MUST: 0`, `P1: ~94%`, `P8: 100%`, `P9: 100%`)

---

## 1. Automated & Read-Only Checks (`L00–L15`, 16 lessons)
- **`lv.py curriculum curriculum/osy.yaml`**: `16 bài, 16 đã có đặc tả, 0 lỗi` (`16/16` title + objectives match).
- **`lv.py lint` & `lv.py verify` (`L00–L15`)**: **16/16 PASS** (`0 FAIL, 0 WARN, 441 PASS`; `h264`+`aac`, `1920x1080`, `spec_sha256` & `tts_sha256` match).
- **`screen_code.py check --course OSY`**: `28 khối — PASS 33 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0`.
- **`layout_OSY.tsv`**: `0` layout errors; **`check_xref --course OSY`**: `0` hits; **`SRT == say`**: **16/16**; **`ASR`**: **16/16** `thiếu audio: 0`, `chưa xem xét: 0`.
- **Direct lab execution (`gcc -std=c11 -Wall -Wextra -Werror` L00 + `.venv/python` L01–L15)**: **16/16** `rc=0`, exact `mong_doi.txt` & `practice` match; `L02`/`L08` `de.md` contradictions fixed; `L01, L04, L06, L15` genuinely computed.
- **Visual PNG inspection (26 `1920x1080` PNGs via `read_file`)**: Crisp rendering across `L00–L15` (SVGs, code blocks, `C (C11)`/`Python` practice tables), zero clipping or overlap.

## 2. Minor Non-Blocking SHOULD Notes
- `labs/OSY/L07/de.md` references standard `Alloc`/`Max` 5×3 matrices from `L07 example` without repeating them inline; `L01/de.md` (`pid`) and `L09/de.md` (`TLB/EAT/RAM` body) omit inline Vietnamese parenthetical glosses in body text.
