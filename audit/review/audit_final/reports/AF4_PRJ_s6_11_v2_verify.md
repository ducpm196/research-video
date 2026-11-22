# Independent AF4 Re-Verification Report — `PRJ:L05–L10` (v2)

**Verifier:** `11a7d91a` (`WP-AF4 PRJ L05-L10 Verifier v2`, read-only)  
**Verdict:** **GO**

---

## 1. Resolution of Prior MUST Blockers & P1/SHOULD Items

All 3 prior MUST blockers and the targeted `P1`/formatting defects from `D:\research-video\audit\review\audit_final\reports\AF4_PRJ_s6_11_verify.md` have been **fixed and rebuilt** into the current specs, labs, and MP4s:

1. **`L07` Hardcoded `loi_giai.py` (MUST → FIXED):**
   - `D:\research-video\labs\PRJ\L07\loi_giai.py` lines 12–19 implement genuine Circuit Breaker state and failure tracking (`state, fails = 'CLOSED', 0`, iterating `(False, False, False)`, transitioning `if fails >= 3: state = 'OPEN'`, and printing `f'cb_after_3fails={state}'`).
   - `D:\research-video\audit\prj\verify_prj.py` (`28/28 PASS`) explicitly verifies both output match against `mong_doi.txt` and non-hardcoded state logic.
   - `L07` `quymo` table (`lessons/prj/L07_du_an_chang_8_duong_ong_outbox_cb.yaml` line 207, visually confirmed in `out/PRJ/L07/frames/00027.png`) aligns to `~80% dời khi thêm nút 5`.

2. **`L09` Fake DFA Verification & `hook`/`intuition` Mismatch (MUST → FIXED):**
   - `D:\research-video\lessons\prj\L09_du_an_chang_10_kiem_chung_hinh_thuc.yaml` lines 200–213 (`check` scene) defines `dfa(s)` (validating `ch in ('a', 'b')`), tests `cases = ['', 'ab', 'aab', 'b', 'ba', 'abb']`, and runs `all(dfa(w) == int(w.endswith('ab')) for w in cases)`; `say` accurately describes all 6 cases and calls `dfa(w)`. Visually confirmed in `out/PRJ/L09/frames/00024.png` and `00026.png`.
   - `hook` (`0,34 s` after `100 giờ`) and `intuition` SVG (`Tích lũy 0,1 s × 3 600 000`) agree (`100 h × 3600 s/h × 10 ticks/s = 3,600,000`). Visually confirmed in `out/PRJ/L09/frames/00000.png` and `00012.png`.
   - `D:\research-video\labs\PRJ\L09\de.md` & `loi_giai.py` match on `"aaab"` and `"aba"` with `{a, b}` validation.

3. **`L10` `say` vs `show` Numerical Contradiction + `P1`/Formatting Fixes (MUST + P1 → FIXED):**
   - `D:\research-video\lessons\prj\L10_du_an_chang_11_pid_merkle.yaml` lines 193–196 (`check` step 1): `show` prints `after_5steps=9.688 err=0.312`, and `say` / `L10.srt` speak `"Kết quả đạt chín phẩy sáu tám tám với sai số không phẩy ba một hai"` (plus explanation of round-half-to-even from `9.6875` and `0.3125`). Visually confirmed in `out/PRJ/L10/frames/00025.png` and ASR transcript (`"Kết quả đạt 9,688 với sai số 0,312."` in `out/PRJ/L10/asr_report.md`).
   - `L10 hook` line 65 (`out/PRJ/L10/frames/00000.png`): literal markdown backticks replaced with `<code>P1=(10,3), P2=(20,5)</code>` and inline gloss `(chu kỳ T, thời lượng C)`.
   - `L10 prereq` line 79 (`out/PRJ/L10/frames/00004.png`): defines `Kp` and `e = target - x` (`rút gọn từ PID`), removing undefined `Ki, Kd`.
   - `L10 example` line 164: updated `say` to `"hai tác vụ chia sẻ một bộ xử lý"`.

---

## 2. Per-Lesson Artifact & Build Verification (`L05–L10`)

| Lesson | Spec & Lab Paths | Frames / MP4 Size / Duration | `lv.cmd_verify` (`spec_sha256` & `tts_sha256` & streams) | SRT vs YAML `say` | `asr_report.md` | `screen_code/PRJ.yaml` | Code Exec & Lab `loi_giai.py == mong_doi.txt` |
|---|---|---|---|---|---|---|---|
| **L05** | `lessons/prj/L05_du_an_chang_6_bo_giai_khung_lap_lich.yaml`<br>`labs/PRJ/L05/{de.md,loi_giai.py,mong_doi.txt}` | 50 PNGs / `9,711,494 B` / `351.73s` (`tl=351.733s`) | **PASS** (`rc=0`, `h264 1920x1080`, `aac`, `edge: 50`, `tts=5df838d4...`) | 50 cues, exact match | `câu: 50, thiếu audio: 0, gắn cờ: 8, chưa xem xét: 0` | 5/5 SHAs match | `example`, `check`, `loi_giai.py` **PASS** |
| **L06** | `lessons/prj/L06_du_an_chang_7_nhat_ky_hmac_sqlite.yaml`<br>`labs/PRJ/L06/{de.md,loi_giai.py,mong_doi.txt}` | 48 PNGs / `9,838,264 B` / `349.73s` (`tl=349.733s`) | **PASS** (`rc=0`, `h264 1920x1080`, `aac`, `edge: 48`, `tts=d8e6610b...`) | 48 cues, exact match | `câu: 48, thiếu audio: 0, gắn cờ: 11, chưa xem xét: 0` | 5/5 SHAs match | `example`, `check`, `loi_giai.py` **PASS** |
| **L07** | `lessons/prj/L07_du_an_chang_8_duong_ong_outbox_cb.yaml`<br>`labs/PRJ/L07/{de.md,loi_giai.py,mong_doi.txt}` | 46 PNGs / `9,423,207 B` / `330.87s` (`tl=330.867s`) | **PASS** (`rc=0`, `h264 1920x1080`, `aac`, `edge: 46`, `spec=381494b1...`, `tts=6100f361...`) | 46 cues, exact match | `câu: 46, thiếu audio: 0, gắn cờ: 6, chưa xem xét: 0` | 5/5 SHAs match | `example`, `check`, `loi_giai.py` (real state) **PASS** |
| **L08** | `lessons/prj/L08_du_an_chang_9_phan_loai_do_do.yaml`<br>`labs/PRJ/L08/{de.md,loi_giai.py,mong_doi.txt}` | 47 PNGs / `8,729,050 B` / `334.73s` (`tl=334.733s`) | **PASS** (`rc=0`, `h264 1920x1080`, `aac`, `edge: 47`, `tts=bfe564e8...`) | 47 cues, exact match | `câu: 47, thiếu audio: 0, gắn cờ: 2, chưa xem xét: 0` | 5/5 SHAs match | `example`, `check`, `loi_giai.py` **PASS** |
| **L09** | `lessons/prj/L09_du_an_chang_10_kiem_chung_hinh_thuc.yaml`<br>`labs/PRJ/L09/{de.md,loi_giai.py,mong_doi.txt}` | 47 PNGs / `9,391,438 B` / `343.20s` (`tl=343.2s`) | **PASS** (`rc=0`, `h264 1920x1080`, `aac`, `edge: 47`, `spec=936621b9...`, `tts=bf4f322a...`) | 47 cues, exact match | `câu: 47, thiếu audio: 0, gắn cờ: 10, chưa xem xét: 0` | 5/5 SHAs match | `example`, `check`, `loi_giai.py` **PASS** |
| **L10** | `lessons/prj/L10_du_an_chang_11_pid_merkle.yaml`<br>`labs/PRJ/L10/{de.md,loi_giai.py,mong_doi.txt}` | 47 PNGs / `9,214,135 B` / `338.77s` (`tl=338.767s`) | **PASS** (`rc=0`, `h264 1920x1080`, `aac`, `edge: 47`, `spec=b031e483...`, `tts=4bb482ba...`) | 47 cues, exact match | `câu: 47, thiếu audio: 0, gắn cờ: 8, chưa xem xét: 0` | 5/5 SHAs match | `example`, `check`, `loi_giai.py` **PASS** |

- `D:\research-video\audit\layout_PRJ.tsv`: `2 bytes` (`\r\n` only) → **0 layout errors**.
- `clear: true`: present on every step across `L05–L10` (`clear_missing=[]`).
- `D:\research-video\audit\prj\verify_prj.py`: **28/28 PASS**.

---

## 3. Rendered `1920x1080` PNG Visual Inspection

Directly inspected **29 PNG frames** via `read_file`:
- **L05**: `out/PRJ/L05/frames/{00000, 00013, 00044}.png` (`hook`, `intuition` SVG, `practice` table)
- **L06**: `out/PRJ/L06/frames/{00000, 00012, 00042}.png` (`hook`, `intuition` SVG, `practice` table)
- **L07**: `out/PRJ/L07/frames/{00000, 00012, 00018, 00021, 00027, 00040}.png` (`hook`, `intuition` SVG, `example` code/output, `quymo` `~80%`, `practice` table)
- **L08**: `out/PRJ/L08/frames/{00000, 00012, 00041}.png` (`hook`, `intuition` SVG, `practice` table)
- **L09**: `out/PRJ/L09/frames/{00000, 00012, 00019, 00024, 00026, 00041}.png` (`hook`, `intuition` SVG `3 600 000`, `example` code, `check` real `dfa(s)` + `6` cases & output `dfa_matches_spec=1 inf_limit=10.0`, `practice` table)
- **L10**: `out/PRJ/L10/frames/{00000, 00004, 00012, 00019, 00022, 00023, 00025, 00042}.png` (`hook` clean `<code>` + `(chu kỳ T, thời lượng C)`, `prereq` `Kp` & `e = target - x`, `intuition` SVG, `example` code/output, `check` code & `after_5steps=9.688 err=0.312` matching spoken `0,312`, `practice` table)

All `practice` tables correctly display `"Mở labs/PRJ/Lxx/de.md và cài đặt Python"` (no `PY` shorthand). No clipping, overlap, raw HTML/backtick leaks, or SVG misalignment observed.

---

## 4. Final Scores & Verdict

| Metric | Score | Target | Details |
|---|---|---|---|
| **MUST count** | **0** | `0` | All 3 prior MUST blockers (`L07`, `L09`, `L10`) resolved and rebuilt |
| **P1** (Self-contained inline glossing) | **6/6 (100%)** | `>= 80%` | PASS: `L05`, `L06`, `L07`, `L08`, `L09`, `L10` |
| **P8** (Exact `say`/`show`/`lab` alignment) | **6/6 (100%)** | `100%` | PASS: `L05`, `L06`, `L07`, `L08`, `L09`, `L10` |
| **P9** (Visual clarity & `clear: true`) | **6/6 (100%)** | `>= 80%` | PASS: `L05`, `L06`, `L07`, `L08`, `L09`, `L10` |

### Remaining Non-Blocking SHOULD Notes
- Minor `P1` polish (optional): `FCFS` in `L05` `hook` and `TN` in `L08` `hook` could be expanded inline on screen, and `audit/review/screen_code/PRJ.yaml` labels `L05..L10` `example 1 0` / `check 1 0` as `kind: other` instead of `kind: output` (hashes all match 5/5). None block release.

**Verdict: GO**
