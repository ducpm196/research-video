# Independent Read-Only AF4 Verification Report — `NET` `L00–L14` (15 lessons)

**Verifier:** `132cef26` (`WP-AF4-3 Stage 6 NET Verifier`, read-only)

## 1. Build / SRT / ASR / Layout / Screen-Code Sync (Observed)
- **`spec_sha256` & `tts_sha256` (`tools/lv.py`)**: **15/15 PASS** (`spec_ok=True`, `tts_ok=True`, `lv.cmd_verify` PASS for `L00–L14`, `1920x1080` `h264`+`aac`, `duration` within `<=0.01s` of `timeline_seconds`, single voice `vi-VN-NamMinhNeural`, `built_at` `2026-11-19T02:18..02:49Z`).
- **`lv.lint` (`tools/lv.py`)**: **15/15 PASS** (`0 FAIL, 0 WARN` across `L00–L14`; all KaTeX formulas and YAML `checks:` pass).
- **`SRT` vs `say`**: **15/15 MATCH** — concatenated `say` strings across `scenes[].steps[]` match concatenated `out/NET/Lxx/Lxx.srt` text 100% (`joined_match=True` for all 15 lessons; frame counts `75–105`).
- **`asr_report.md`**: **15/15 `thiếu audio: 0`, `chưa xem xét: 0`** (flagged counts range `0–29`, all annotated in `asr_reviewed` with `NOT_VERIFIED bằng tai người`).
- **`audit/layout_NET.tsv`**: Size `2` bytes (`\r`, **0 layout issues** logged).
- **`audit/review/screen_code/NET.yaml`**: All 25 `L00–L14` block `sha16` hashes in `screen_code.py inventory --course NET` match `NET.yaml` 100%.
- **Visual PNG inspection (`read_file`, 38 PNGs across `L00–L14`, >=2–3/lesson)**:
  - All 38 PNGs are visually sharp, legible, and free of clipping, overlapping text, or overflow. **However**, `L08/frames/00079.png` visually displays the wrong expected output (`rounds_to_reach_16=14`, `final_vals=15,16`).

---

## 2. Rubric Scores (Observed)

- **P1 (Self-contained inline glossing for new AF2 blocks/labs & whole lesson): `8 / 15` (53.3% — BELOW 80% target)**
  - Whole-lesson body (`hook..quiz`, `recap`) consistently glosses terms inline (`sym` + inline notes).
  - **AF2 `practice` & `labs/NET/Lxx/de.md` gaps (7 lessons fail P1)**:
    - `L02`: `de.md` uses `RTT = 50 ms` without glossing `RTT` (first defined in `L10`), while `L02` `example` uses "trễ một chiều".
    - `L04`: `de.md` uses `Switch MAC` without glossing `Switch = bộ chuyển mạch` (`L04` lesson only uses "bộ chuyển mạch").
    - `L09`: `de.md` uses `TCP socket loopback`, `socket.AF_INET`, `SOCK_STREAM`, `PING ↔ PONG` without teaching/glossing `socket`, `loopback`, `AF_INET`, or `SOCK_STREAM`.
    - `L10`: `practice` step 1 uses `BDP/gói` and `de.md` uses `BDP` / `bdp_packets` without glossing `BDP = tích băng thông–trễ` (`L10` lesson never uses the `BDP` acronym).
    - `L11`: `practice` step 1 uses `AIMD` and `de.md` uses `cwnd`, `ssthresh`, `AIMD`, `timeout` — none of these 4 terms appear in `L11` lesson or have inline glosses in `de.md`.
    - `L12`: `practice` step 1 uses `HTTP/1.1 keep-alive` and `de.md` uses `RTT` without inline glosses (`keep-alive = kết nối bền`, `RTT = lượt đi về`).
    - `L14`: `de.md` introduces `RSA` and `64 hex` (`hex = hệ 16`) without inline glosses (`L14` lesson calls it "hệ khoá công khai đồ chơi" and "hệ 16").
  - *(Minor across all 15)*: `practice` step 1 writes `cài đặt bằng PY` without glossing `PY = Python` on screen; `L01` (`tx_us`, `prop_ms`) and `L05` (`bcast`) use abbreviated output keys without inline expansion.

- **P8 (Exact numerical/code/output alignment & genuine `loi_giai.*` solution): `12 / 15` (80.0% — BELOW 100% target)**
  - `L00–L06`, `L10–L14` (12 lessons): `loi_giai.py` executes cleanly (`rc=0`), matches `mong_doi.txt`, aligns with `de.md`, `practice`, and lesson `checks:`.
  - **3 Failures**:
    1. **`L08` (Direct contradiction)**: `labs/NET/L08/de.md` specifies `rounds_to_reach_16=15` and `final_vals=16,16` (matching `L08` `hook` "15 vòng", `example` table round 15 `(16, 16)`, `verify` "từ vòng 15 cả hai cùng ghi 16", and `checks:` `alg.count_to_infinity(20)[15] == (16, 16)`). However, `labs/NET/L08/loi_giai.py` uses `while max(b, c) < 16:`, stopping at round 14 (`b=15, c=16`), so `loi_giai.py`, `mong_doi.txt`, `L08_vecto_khoang_cach.yaml` `practice` step 2, and rendered `out/NET/L08/frames/00079.png` all show `rounds_to_reach_16=14` and `final_vals=15,16`.
    2. **`L07` (Hardcoding in `loi_giai.py`)**: `labs/NET/L07/loi_giai.py` line 12 literally hardcodes `print('next_hop_all=B')` instead of tracking parent / first-hop pointers during Dijkstra (unlike `audit/review/screen_code/NET.yaml` `L07_ls`, which computes `par` and `hops`).
    3. **`L09` (Socket failure & process hang in environment)**: Executing `labs/NET/L09/loi_giai.py` in this environment raised `PermissionError: [WinError 10013]` on `socket.create_connection(('127.0.0.1', p))` and **hung indefinitely** because `srv` is a non-daemon `threading.Thread` blocked on `s.accept()`.

- **P9 (Visual layout clarity & `clear: true` before big blocks): `13 / 15` (86.7% — MEETS >=80% target)**
  - All 15 `practice` scenes set `clear: true` on both steps; major SVGs/tables/pitfall blocks have `clear: true`; 0 render/layout errors; all 38 inspected PNGs are clean.
  - Deducted for `L03` (6 steps with `<table>`/`<div class="code">` lacking `clear: true`) and `L04` (5 stacked `<table>` steps without `clear: true`, resulting in 3 stacked tables on `L04/frames/00083.png`).

---

## 3. Blockers & Improvements

### **MUST Blockers (Fix before GO)**
1. **Fix `NET L08` lab/lesson alignment & rebuild `L08`**:
   - Change `labs/NET/L08/loi_giai.py` termination condition (`while min(b, c) < 16:`, or simultaneous round loop until both reach `16`) so it outputs `rounds_to_reach_16=15` and `final_vals=16,16` matching `de.md`, `hook`, `example`, `verify`, and `checks:`.
   - Update `labs/NET/L08/mong_doi.txt`, `lessons/net/L08_vecto_khoang_cach.yaml` (`practice` step 2), `curriculum/net.yaml`, and `audit/review/screen_code/NET.yaml` (`NET L08 practice 1 0`), then rebuild `out/NET/L08`.
2. **Fix `NET L07` hardcoding in `labs/NET/L07/loi_giai.py`**:
   - Track parent/first-hop pointers in Dijkstra and derive `next_hop_all` (and `sa_direct_vs_sb_ba`) from the graph/paths rather than hardcoding `print('next_hop_all=B')`.
3. **Fix `NET L09` socket thread hang & verify execution**:
   - Make the server thread `daemon=True` (and/or add socket timeouts / `try..finally` cleanup) in `labs/NET/L09/loi_giai.py` so connection failure never hangs the grader, and verify `L09` passes `cham.sh` in an environment allowing loopback TCP sockets.
4. **Fix P1 inline glossing in AF2 blocks & `de.md` (to >=80%, i.e. >=12/15)**:
   - Add inline Vietnamese glosses in `labs/NET/Lxx/de.md` and `practice` `Kiểm chứng` for: `L02` (`RTT`), `L04` (`Switch = bộ chuyển mạch`), `L09` (`socket`, `loopback`, `AF_INET`, `SOCK_STREAM`), `L10` (`BDP = tích băng thông–trễ`), `L11` (`cwnd = cửa sổ tắc nghẽn`, `ssthresh = ngưỡng`, `AIMD = tăng cộng – giảm nhân`, `timeout = hết giờ chờ`), `L12` (`keep-alive = kết nối bền`, `RTT`), `L14` (`RSA`, `hex = hệ 16`). (Rebuild affected lessons if `practice` slide text changes.)

### **SHOULD Improvements**
1. **`L02/de.md` terminology**: Align `RTT = 50 ms` with `L02` lesson's `trễ một chiều = 50 ms` (or clarify why `R * 50 ms` is used).
2. **`L10/de.md` clarity**: Explicitly distinguish `bdp_packets = 3750` (BDP in packets) from the lesson's exact full-utilization window `W = 3751`, and mention `W = 1000` in the `de.md` prose before `w1000_eff=26.7%`.
3. **`L04/de.md` phrasing**: Change "qua 2 khung" to "qua 3 khung (2 địa chỉ MAC khác nhau)" to match `loi_giai.py`.
4. **`L03` & `L04` visual breathing room (`P9`)**: Add `clear: true` before stacked tables in `L04 quiz` (`00083.png`) and `L03 verify#2 / quiz#1,#3`.
5. **Global minor `practice` gloss**: Expand `PY` -> `Python (PY)` in `practice` step 1, and gloss `tx_us`/`prop_ms` (`L01`) and `bcast` (`L05`) in `de.md`.

---

## Verdict: **`NO-GO`**
`NET L00–L14` fails **P8** (`12/15`, target `100%`) due to the `L08` expected-output contradiction baked into the rendered video, `L07` hardcoding in `loi_giai.py`, and `L09` socket `WinError 10013` / non-daemon thread hang, and fails **P1** (`8/15`, target `>=80%`) on AF2 `practice`/`de.md` inline glossing.
