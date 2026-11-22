# Independent Read-Only AF4 v2 Verification Report — `NET` `L00–L15` (16 lessons)

**Verifier:** `f5468e90` (`WP-AF4-3 Stage 6 NET Verifier v2`, strictly read-only)
**Baseline:** `D:\research-video\audit\review\audit_final\reports\AF4_S6_NET_verify.md`

---

## 1. Build / Lint / SRT / ASR / Layout / Screen-Code Sync (Observed)

- **`tools/lv.py verify` & `build_report.json` (`L00–L15`)**: **16/16 PASS** (`spec_ok=True`, `tts_ok=True`, `verify_rc=0`; `1920x1080` `h264`+`aac`; MP4 `duration` within `<=0.01s` of `timeline_seconds`; single voice `vi-VN-NamMinhNeural`; rebuilt `2026-11-19T13:42:48Z..14:16:31Z`).
- **`tools/lv.py lint` (`L00–L15`)**: **16/16 PASS** (`0 FAIL, 0 WARN`).
- **`tools/lv.py curriculum curriculum/net.yaml`**: **PASS** (`16 bài, 16 đã có đặc tả, 0 lỗi`, `rc=0`).
- **`SRT` vs `say` (`out/NET/Lxx/Lxx.srt`)**: **16/16 MATCH** (`say==srt=True` on all 16 lessons).
- **`out/NET/Lxx/asr_report.md` (`L00–L15`)**: **16/16 `thiếu audio: 0`, `chưa xem xét: 0`**.
- **`audit/layout_NET.tsv`**: Size `2` bytes (`\r`, **0 layout issues**).
- **`audit/review/screen_code/NET.yaml`**: **26/26 MATCH**.

---

## 2. Prior Blocker & Visual PNG Verification

1. **`L08` expected-output contradiction — FIXED & VERIFIED**: `labs/NET/L08/loi_giai.py` iterates `while min(b, c) < 16:`, outputting `rounds_to_reach_16=15`, `final_vals=16,16` matching `de.md`, `mong_doi.txt`, lesson YAML, `curriculum/net.yaml`, and `out/NET/L08/frames/00079.png`.
2. **`L07` hardcoding — FIXED & VERIFIED**: `labs/NET/L07/loi_giai.py` dynamically computes first-hop pointers in Dijkstra (`rc=0`, matches `mong_doi.txt` & `out/NET/L07/frames/00078.png`).
3. **`L09` non-daemon server thread hang — FIXED**: `labs/NET/L09/loi_giai.py` uses `settimeout(3.0)`, `try..finally: s.close()`, `daemon=True`, `t.join(timeout=3.0)` (exits immediately without hang; note loopback socket connect outside sandbox already verified via `lab_gate NET` PASS).
4. **P1 inline glossing & `"Python"` in `practice` — FIXED & VERIFIED**: All 16 lessons display `Python`; `RTT`, `Switch`, `socket/loopback/AF_INET/SOCK_STREAM`, `BDP`, `cwnd/ssthresh/AIMD/timeout`, `keep-alive`, `RSA/hex` glossed inline.
5. **Visual PNG inspection**: 25 `1920x1080` PNGs inspected via `read_file` across `L02, L03, L04, L07, L08, L09, L10, L11, L12, L14, L15` — all crisp, zero clipping/overlap/overflow.

---

## 3. Rubric Scores & Final Verdict

- **MUST blockers:** **`0`**
- **P1 (Inline glossing):** **`15 / 16` (93.8%)** (`15/15 = 100%` on `L00–L14`) — **PASS (`>=80%`)**
- **P8 (Alignment & genuine solution):** **`16 / 16` (100%)** — **PASS (`100%`)**
- **P9 (Visual clarity & `clear: true`):** **`14 / 16` (87.5%)** (`13/15 = 86.7%` on `L00–L14`) — **PASS (`>=80%`)**

**Final Verdict: `GO`**
