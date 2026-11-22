# Independent Re-Verification Report — AF4 LNX (`L00–L09`) v3

**Verifier:** `WP-AF4-2 LNX Verifier v3` (`df5f451a`, read-only)  
**Verdict:** **GO** (`0` MUST defects; `P1` = 100%, `P8` = 100%, `P9` = 100%; all 10 lessons `L00–L09` current and verified)

---

## 1. Summary Scores
- **MUST count:** **0** (target `0`; prior residual `MUST` on `L05` resolved)
- **P1 (self-contained inline glossing):** **10/10 (100%)** (`>= 80%` PASS; `lv.py lint` 0 FAIL / 0 WARN across `L00–L09`)
- **P8 (exact `say`/`show`/`lab` alignment & curriculum sync):** **10/10 (100%)** (`L05` `example#1` fixed + `curriculum/lnx.yaml` line 71 synced; `labs/LNX/L00–L09/mong_doi.txt` 10/10 exact match with `practice#1`)
- **P9 (visual clarity & `clear: true`):** **10/10 (100%)** (`>= 80%` PASS; 0 overlaps/clipping in inspected `1920x1080` frames)
- **Pipeline & Gate Checks (`L00–L09`):**
  - `tools/lv.py verify` → **10/10 PASS** (`spec_sha256` & `tts_sha256` match, `streams=True`, duration matches `timeline_seconds`).
  - `tools/lv.py lint` → **10/10 PASS** (`0 FAIL, 0 WARN`).
  - `tools/lv.py curriculum curriculum/lnx.yaml` → **PASS** (`10 bài, 10 đã có đặc tả, 0 lỗi`).
  - `out/LNX/L00–L09/Lxx.srt` vs YAML `say` → **10/10 exact match**.
  - `out/LNX/L00–L09/asr_report.md` → **10/10 clean**: `thiếu audio: 0`, `chưa xem xét: 0`.
  - `audit/review/screen_code/LNX.yaml` → **50/50 exact SHA match** (`STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0`).
  - `audit/review/check_xref.py --course LNX` → **0 hits**.

---

## 2. Residual Defect Closure (`L05` + `curriculum/lnx.yaml`)
1. **`L05` `example#1` (`out/LNX/L05/frames/00016.png`–`00018.png`) — RESOLVED:** Visually verified exact match between `p1` (`grep /etc/hosts` + `ip -4 -o addr show`) and spoken `say`, plus `00039.png` matches `labs/LNX/L05/mong_doi.txt`.
2. **`curriculum/lnx.yaml` line 71 (`L05.objectives[1]`) — RESOLVED:** Exact 1:1 match with `lessons/lnx/L05_mang_linux_cong_dns.yaml` line 24.
3. **Non-regression (`L00–L04, L06–L09`):** Retained verified builds (`spec_digest_match=True`, `tts_digest_match=True`, `lv.py verify` PASS) with zero regressions.

**Final Verdict: GO**
