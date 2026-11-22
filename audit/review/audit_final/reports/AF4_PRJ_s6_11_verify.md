# Independent AF4 Verification Report — `PRJ:L05–L10`

**Verifier:** `f94fd97f` (`WP-AF4 PRJ L05-L10 Verifier`, read-only)

## 1. Automated & Artifact Consistency

All checks below were run read-only against `lessons/prj/L05..L10*.yaml`, `curriculum/prj.yaml`, `labs/PRJ/L05..L10/`, `audit/review/screen_code/PRJ.yaml`, `audit/layout_PRJ.tsv`, and `out/PRJ/L05..L10/`.

| Lesson | Frames | Timeline / MP4 Duration | Streams (`1920x1080`, `h264`, `aac`) | `spec_sha256` & `tts_sha256` (`lv.cmd_verify`) | SRT vs YAML `say` | `asr_report.md` | `screen_code/PRJ.yaml` SHAs |
|---|---|---|---|---|---|---|---|
| **L05** | 50 | `351.733s` / `351.73s` | PASS (`edge`: 50, `vi-VN-NamMinhNeural`) | PASS (`d8bc1177...` / `5df838d4...`) | 50/50 exact match | `câu: 50, thiếu audio: 0, gắn cờ: 8, chưa xem xét: 0` | 5/5 match |
| **L06** | 48 | `349.733s` / `349.73s` | PASS (`edge`: 48, `vi-VN-NamMinhNeural`) | PASS (`ad6926bc...` / `d8e6610b...`) | 48/48 exact match | `câu: 48, thiếu audio: 0, gắn cờ: 11, chưa xem xét: 0` | 5/5 match |
| **L07** | 46 | `330.867s` / `330.87s` | PASS (`edge`: 46, `vi-VN-NamMinhNeural`) | PASS (`5c87ed70...` / `6100f361...`) | 46/46 exact match | `câu: 46, thiếu audio: 0, gắn cờ: 6, chưa xem xét: 0` | 5/5 match |
| **L08** | 47 | `334.733s` / `334.73s` | PASS (`edge`: 47, `vi-VN-NamMinhNeural`) | PASS (`ce561281...` / `bfe564e8...`) | 47/47 exact match | `câu: 47, thiếu audio: 0, gắn cờ: 2, chưa xem xét: 0` | 5/5 match |
| **L09** | 47 | `341.467s` / `341.47s` | PASS (`edge`: 47, `vi-VN-NamMinhNeural`) | PASS (`b90d53da...` / `09acc687...`) | 47/47 exact match | `câu: 47, thiếu audio: 0, gắn cờ: 10, chưa xem xét: 0` | 5/5 match |
| **L10** | 46 | `332.933s` / `332.93s` | PASS (`edge`: 46, `vi-VN-NamMinhNeural`) | PASS (`26189468...` / `cba376b2...`) | 46/46 exact match | `câu: 46, thiếu audio: 0, gắn cờ: 7, chưa xem xét: 0` | 5/5 match |

- **`audit/layout_PRJ.tsv`**: 2 bytes (`\r\n`, empty) → **0 layout errors** across `L05..L10`.
- **Visual PNG Inspection** (29 rendered `1920x1080` PNGs inspected directly across `L05..L10`, covering `hook`, `prereq`, `intuition` SVG, `example` code + output, `check` output, `quymo` tables, `pitfalls`, `quiz`, `practice`):
  - L05: `00000`, `00005`, `00013`, `00022`, `00025`, `00031`, `00035`, `00039`, `00047`
  - L06: `00000`, `00012`, `00020`, `00023`, `00029`, `00036`
  - L07: `00000`, `00012`, `00018`, `00021`, `00027`, `00034`
  - L08: `00000`, `00012`, `00020`, `00022`, `00028`, `00035`
  - L09: `00000`, `00012`, `00019`, `00022`, `00028`, `00035`
  - L10: `00000`, `00012`, `00019`, `00021`, `00025`, `00027`, `00034`
  - All SVGs (`viewBox="0 0 960 170"`), tables, code blocks, and quiz frames render without clipping, overlap, or misaligned arrows. One minor HTML formatting defect observed in `out/PRJ/L10/frames/00000.png` (literal backticks rendered in `hook`).

---

## 2. Content & Lab Fidelity Scores

| Criterion | Score | Target | Breakdown (`L05–L10`) |
|---|---|---|---|
| **P1** (Self-contained inline glossing) | **5/6 (83.3%)** | `>=80%` | **PASS**: L05, L06, L07, L08, L09 · **FAIL**: L10 (`hook` writes `P1=(10,3), P2=(20,5)` without specifying `(T_i, C_i)` order until inferred in `formula`; `prereq` cites `u = Kp*e + Ki*integral + Kd*de` without defining `e, Ki, Kd`) |
| **P8** (Exact alignment & genuine lab solution) | **3/6 (50.0%)** | `100%` | **PASS**: L05, L06, L08 · **FAIL**: L07, L09, L10 (details in MUST blockers below) |
| **P9** (Visual layout clarity & `clear: true`) | **6/6 (100%)** | `>=80%` | **PASS**: L05, L06, L07, L08, L09, L10 (`audit/layout_PRJ.tsv` = 0 errors; every step has `clear: true`; no clipping/overlap in inspected PNGs) |

---

## 3. MUST Blockers (3)

1. **`L07` — Hardcoded lab solution (`P8` failure)**
   - **File**: `labs/PRJ/L07/loi_giai.py` line 14 vs `labs/PRJ/L07/de.md` line 3.
   - **Observed**: `de.md` requires `(3) mở ngắt mạch OPEN sau 3 lỗi` (`cb_after_3fails=OPEN`), but `loi_giai.py` line 14 literally hardcodes `print('cb_after_3fails=OPEN')` with zero Circuit Breaker state variable, failure counter, or `CLOSED -> OPEN` transition logic.

2. **`L09` — Fake DFA check in `check` scene & `say`/`show` + `hook`/`intuition` factual contradictions (`P8` failure)**
   - **File**: `lessons/prj/L09_du_an_chang_10_kiem_chung_hinh_thuc.yaml` lines 158–163 (`check` scene) & lines 44, 102 (`hook` vs `intuition`).
   - **Observed**:
     - `check` step 0 `show` runs `ok = all((w.endswith('ab')) == (1 if w in ('ab','aab') else 0) for w in cases)` on `cases = ['ab', 'aab', 'b', 'ba', 'abb']`. It neither defines nor calls `dfa(w)`, instead comparing `endswith('ab')` against a hardcoded tuple `('ab', 'aab')`.
     - `check` step 0 `say` contradicts `show` by claiming `"Ở nhánh kiểm chứng, ta quét năm trường hợp biên gồm chuỗi rỗng đuôi..."` (no empty string exists in `cases`) and `"So sánh từng kết quả của DFA với đặc tả kết thúc bằng a b"`.
     - `hook` `show` (line 44) states `"sai số cộng lặp 24 bit sau 100 giờ gây lệch 0,34 s"`, whereas `intuition` SVG (line 102) writes `"Tích lũy 0,1 s × 36000"` (`36,000 × 0.1 s = 3,600 s = 1 giờ`, not 100 hours = `3,600,000` ticks).

3. **`L10` — `say` vs `show` numerical contradiction in `check` scene (`P8` failure)**
   - **File**: `lessons/prj/L10_du_an_chang_11_pid_merkle.yaml` lines 166–168 (`check` scene step 1).
   - **Observed**: `show` prints `after_5steps=9.688 err=0.312` (Python round-half-to-even of `9.6875` and `0.3125`, matching `out/PRJ/L10/frames/00025.png`), while `say` (and `L10.srt` cue 26) speaks `"Kết quả đạt chín phẩy sáu tám tám với sai số không phẩy ba một ba"` (`0.313`, which also fails to sum with `9.688` to `10.000`).

---

## 4. SHOULD Polish Suggestions

1. **`L10` `hook` literal markdown backticks** (`lessons/prj/L10_du_an_chang_11_pid_merkle.yaml` line 39, visible in `out/PRJ/L10/frames/00000.png`): Replace `` `P1=(10,3), P2=(20,5)` `` inside `<p>` with `<code>P1=(10,3), P2=(20,5)</code>` and briefly state `(T_i, C_i)` = `(chu kỳ, thời gian chạy)` inline.
2. **`L10` `example` `say` wording & `prereq` PID mismatch**:
   - Line 137–138 `say` says `"vì hai tác vụ chạy song song"` when Liu–Layland RMS bound (`0.828`) applies to uniprocessor preemptive scheduling.
   - `prereq` / `curriculum/prj.yaml` refer to PID (`Ki*integral + Kd*de`), whereas `example`/`check`/`de.md` only implement a proportional (`P`-only) controller (`Kp`).
3. **`L07` `quymo` table vs `hook`/`formula` percentage**: `quymo` (line 184) states `Băm mod: ~75% dời khi thêm nút 5` while `hook` and `formula` state `80%` (`1 - 1/5 = 80%`). Align to `80%` (or explain why).
4. **`L09` `labs/PRJ/L09/de.md` vs `loi_giai.py`**: `de.md` asks to test on `['aaab', 'aba', 'b']`, whereas `loi_giai.py` only evaluates `dfa("aaab")` and `dfa("aba")` (and `dfa` treats any character `!= 'a'` as `'b'` without validating `{a, b}`).
5. **`L05` & `L08` minor inline glossing (`P1` polish)**:
   - `L05`: `FCFS` appears unexpanded on screen in `hook`/`formula` (only spoken as "đến trước phục vụ trước" in `check`).
   - `L08`: `TP, FP, FN, TN` appear in `hook`/`sym`/`intuition` without explicit expansion (`TN` is never explained).
   - `L09`: `0 ReDoS` in `sym` could include a brief gloss (`ReDoS = Regular Expression Denial of Service`).
6. **`audit/prj/verify_prj.py` coverage & `audit/review/screen_code/PRJ.yaml` metadata**: `verify_prj.py` currently only checks `L00–L04`; extending it to `L05–L10` (with non-hardcoded behavioral assertions) would catch issues like L07/L09 automatically. Also `screen_code/PRJ.yaml` records `L05..L10` `example 1 0` / `check 1 0` as `kind: other` instead of `kind: output` (`L00..L04`).

---

## Verdict

**NO-GO**

- **Blocking reasons**: 3 **MUST** defects (`L07` hardcoded `loi_giai.py`, `L09` fake DFA verification in `check` + `say`/`show` & `hook`/`intuition` mismatches, `L10` `say` `0,313` vs `show` `0.312` contradiction); **P8 = 3/6 (50.0%)**, below the mandatory `100%` target.
- **Required before re-verification**: Fix the 3 MUST items in `labs/PRJ/L07/loi_giai.py`, `lessons/prj/L09_*.yaml`, and `lessons/prj/L10_*.yaml`, then rebuild `L09` and `L10` (audio/video/SRT/ASR) so `spec_sha256`, `tts_sha256`, and `asr_report.md` remain in sync.
