# Independent Re-Verification Report — AF4 LNX (`L00–L09`) v2

**Verifier:** `0e49343e` (`WP-AF4-2 LNX Verifier v2`, read-only)  
**Verdict:** **NO-GO** (`1` residual `MUST` / `P8` = `90% < 100%` on `L05`; all 5 other prior MUST defects and all `L00–L04, L06–L09` lessons are clean)

---

## 1. Summary Scores
- **MUST count:** **1** (target `0`)
- **P1 (self-contained inline glossing):** **10/10 (100%)** (`>= 80%` PASS)
- **P8 (exact `say`/`show`/`lab` alignment):** **9/10 (90%)** (`< 100%` — `L05` `example#1` `say` vs `show` mismatch & `curriculum/lnx.yaml` objective drift)
- **P9 (visual clarity & `clear: true`):** **10/10 (100%)** (`>= 80%` PASS; `18/20` = 90% in `L00`, `17/19` = 89% in `L01–L09`; 0 overlaps/clipping in inspected `1920x1080` PNGs)
- **Technical pipeline (`lv.py verify`, SHA256, SRT, ASR, `screen_code`, `check_xref`):**
  - `tools/lv.py verify` → **10/10 PASS** (`streams=True`, duration matches `timeline_seconds`).
  - `spec_sha256` & `tts_sha256` in `out/LNX/L00–L09/build_report.json` → **10/10 exact match**.
  - `out/LNX/L00–L09/Lxx.srt` vs YAML `say` sentences → **10/10 exact match**.
  - `out/LNX/L00–L09/asr_report.md` → **10/10 clean**: `thiếu audio: 0`, `chưa xem xét: 0` across all 10 lessons.
  - `out/LNX/L00–L09/Lxx.mp4` → all 10 present (`8.93 MB`–`10.91 MB`).
  - `audit/review/screen_code/LNX.yaml` SHA check → **50/50 exact SHA match** (`missing=[]`, `extra=[]`, `stale=[]`).
  - `check_xref` logic across `lessons/lnx/L00–L09` + `curriculum/lnx.yaml` → **0 hits**.

---

## 2. Prior 6 MUST Defects Re-Verification
1. **MUST-1 (`L00` `ln -s`):** **RESOLVED.** `labs/LNX/L00/mong_doi.txt` & `out/LNX/L00/frames/00047.png` both show `hard_content=SAFE_DATA`, `hard_links=1`, `sym_failed=1`.
2. **MUST-2 (`L05` `/etc/hosts` `#` & socket bind):** **RESOLVED.** `labs/LNX/L05/mong_doi.txt` & `out/LNX/L05/frames/00039.png` both show `loopback_only=127.0.0.1`, `all_ifaces=0.0.0.0`, `hosts_before_dns=1`.
3. **MUST-3 (`check_xref` FND/NET refs):** **RESOLVED.** 0 hits.
4. **MUST-4 (`svg_arrow` directions & `L09` box overlap):** **RESOLVED.** Visually verified in `L00/00016.png`, `L08/00010.png`, `L09/00010.png`.
5. **MUST-5 (`L04` `data_kb=4` vs `0 KB`):** **RESOLVED.** Visually verified in `L04/00021.png` & `00022.png`.
6. **MUST-6 (`L05` `curl`/`ss` alignment):** **PARTIALLY RESOLVED → 1 Residual MUST:**
   - In `lessons/lnx/L05_mang_linux_cong_dns.yaml` `example#1` (`out/LNX/L05/frames/00017.png`), `say` still states `"Ta chạy trực tiếp một công-tai-nơ Li-núc thật để đọc cấu hình tệp ánh xạ cục bộ, bảng định tuyến máy chủ tên miền và so sánh kết nối tới cổng dịch vụ thật."` whereas `show` (`p1`) ONLY runs `grep ... /etc/hosts` and `ip -4 -o addr show`.
   - `curriculum/lnx.yaml` line 71 (`L05.objectives[1]`) was NOT updated and still says `"Đọc kết quả cổng đang mở, kiểm tra nối TCP và phản hồi HTTP bằng curl"`.

---

## 3. Per-Lesson Scores (`L00–L09`)

| Lesson | MP4 (MB) | Frames | SRT/SHA | ASR (`thiếu`/`chưa`) | P1 | P8 | P9 |
|---|---|---|---|---|---|---|---|
| `L00` | 10.91 | 53 | Match | 0 / 0 | Pass | Pass | Pass |
| `L01` | 8.93 | 44 | Match | 0 / 0 | Pass | Pass | Pass |
| `L02` | 9.12 | 45 | Match | 0 / 0 | Pass | Pass | Pass |
| `L03` | 9.08 | 45 | Match | 0 / 0 | Pass | Pass | Pass |
| `L04` | 9.15 | 47 | Match | 0 / 0 | Pass | Pass | Pass |
| `L05` | 9.68 | 45 | Match | 0 / 0 | Pass | **Fail** | Pass |
| `L06` | 9.24 | 44 | Match | 0 / 0 | Pass | Pass | Pass |
| `L07` | 9.22 | 44 | Match | 0 / 0 | Pass | Pass | Pass |
| `L08` | 9.78 | 44 | Match | 0 / 0 | Pass | Pass | Pass |
| `L09` | 9.51 | 44 | Match | 0 / 0 | Pass | Pass | Pass |

---

## 4. Required Fix for `GO`
1. Fix `L05` `example#1` `say` in `audit/lnx/data_b.py` (line 109) & rebuild `L05` so `say` matches `p1` (`/etc/hosts` + `ip -4 -o addr show`).
2. Sync `curriculum/lnx.yaml` line 71 (`L05.objectives[1]`) with `lessons/lnx/L05_mang_linux_cong_dns.yaml`.
