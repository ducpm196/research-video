# Independent AF4 Verification Report — SEC `L00–L14` (15 lessons)

**Verifier:** `54372f6d` (`WP-AF4-3 Stage 7 SEC Verifier`, read-only)
**Verdict: `NO-GO`**
*(Due to 5 MUST P8 blockers in `L01, L06, L07, L10, L11` — P8 = 10/15 < 100% target — and P1 unglossed terms in 13/15 newly added AF2 `practice`/`de.md` blocks.)*

---

### 1. Build / SRT / ASR / Layout / Gate Sync (Observed Evidence)
- **`spec_sha256` & `tts_sha256` (`out/SEC/L00..L14/build_report.json`)**: **15/15 match** current `lessons/sec/L00..L14*.yaml` (`spec_digest` and `tts_digest` via `tools/lv.py`).
- **SRT vs `say` (`out/SEC/L00..L14/L*.srt`)**: **15/15 exact 1-to-1 match** between SRT entry texts, `build_frames` captions, and `lv.sentences(step['say'])` across all frames (L00:73, L01:69, L02:69, L03:81, L04:79, L05:79, L06:74, L07:76, L08:73, L09:77, L10:83, L11:88, L12:74, L13:67, L14:77).
- **`asr_report.md`**: **15/15** have `thiếu audio: 0` and `chưa xem xét: 0` (flagged counts: L00:1, L01:0, L02:1, L03:5, L04:2, L05:2, L06:1, L07:10, L08:2, L09:1, L10:2, L11:11, L12:2, L13:1, L14:1 — all reviewed).
- **`lv.lint`**: **15/15 PASS** (`0 FAIL, 0 WARN`).
- **`audit/layout_SEC.tsv`**: **0 layout errors** (file contains only an empty line).
- **`audit/sec/verify_sec.py`**: **26 PASS · 0 FAIL**.
- **Scene `checks:` (`L00..L14` YAMLs)**: **0 failures** across all scenes.
- **`audit/review/screen_code/SEC.yaml`**: **0 MISSING, 0 STALE** for all `.code` blocks in `L00..L14` (verified SHA256 directly in Python).
- **`labs/SEC/L00..L14/loi_giai.py` vs `mong_doi.txt`**: **15/15 stdout exact match** when executed directly with `.venv\Scripts\python.exe -B`. *(Read-only sandbox blocked Git Bash init on `lab_gate.py`; coordinator already verified outside sandbox.)*
- **Visual PNG inspection (`read_file`)**: Sampled **64 PNGs** (`>= 4` per lesson covering `intuition` SVG, tables, code blocks in `L06`/`L12`, stacked `prereq`/`check` tables in `L03`/`L05`/`L09`, and both `practice` steps in all 15 lessons). All 64 PNGs rendered crisply at 1920x1080 with zero clipping, overlap, or overflow.

---

### 2. P1 (Self-contained inline glossing for new AF2 blocks/labs & whole lesson)
- **Whole core lesson (`hook..recap`)**: **15/15** well-glossed in plain Vietnamese.
- **New AF2 `practice` & `labs/SEC/L00..L14/de.md`**: **2/15 (13.3%)** fully self-contained (`L08`, `L14`, aside from minor `PY` abbreviation). **13/15** introduce unglossed English terms/acronyms not defined in the lesson body (target `>=80%`):
  - `L00`: `de.md` & `practice` use `Information Disclosure`, `Tampering`, `Spoofing`, `Confidentiality`, `Integrity`, `Authentication` (lesson only teaches Vietnamese terms + `(STRIDE)`).
  - `L01`: `de.md` uses `salt`, `pbkdf2_hex_len` (`hex` is not introduced until L07).
  - `L02`: `de.md` uses `Diceware` (lesson calls it "danh sách 7776 từ").
  - `L03`: `practice` & `de.md` use `OTP` (lesson only says "mã một lần").
  - `L04`: `practice` & `de.md` use `RBAC` (lesson only says "phân quyền theo vai trò").
  - `L05`: `practice` uses `CSRF` (lesson only says "giả mạo yêu cầu chéo trang").
  - `L06`: `practice` & `de.md` use `HTML`, `XSS`, `SQL`, `SQLite`, `payload` (none defined in L06 except one mention of "nội dung HTML").
  - `L07`: `practice` & `de.md` use `CBC`, `CTR`, `IV` (lesson only teaches `ECB`, "chế độ bộ đếm", and "số dùng một lần").
  - `L09`: `practice` & `de.md` use `CA` (never appears in L09 YAML; lesson says "tổ chức cấp") and `TLS` (only in title).
  - `L10`: `de.md` uses `ratio_vs_32bit_hash` without defining what it compares.
  - `L11`: `practice` & `de.md` use `ASLR`, `entropy` (`ASLR` never appears in L11 YAML; lesson says "ngẫu nhiên hoá địa chỉ").
  - `L12`: `practice` & `de.md` use `first-match`, `ALLOW`, `DENY` (lesson uses "luật khớp đầu tiên", "cho", "chặn").
  - `L13`: `practice` uses `Bayes PPV` (`PPV` never appears in L13 YAML; lesson calls it "tỉ lệ cảnh báo là thật").
  - All `L00–L14` `practice` tables say `cài đặt bằng PY` without glossing `PY` = Python.

---

### 3. P8 (Exact alignment across `say`, `show`, `checks`, `de.md`, `loi_giai.*`, `mong_doi.txt`, non-hardcoded `loi_giai.*`)
- **Score: 10/15 (66.7%)** — below the **100%** target. Passing: `L00, L02, L03, L04, L05, L08, L09, L12, L13, L14` (with minor SHOULD notes below). Failing (**5 lessons**):
  1. **L01**: `labs/SEC/L01/de.md` line 5 has `2. slow_crack_days=24170` (100x too high), directly contradicting `mong_doi.txt` (`242`), `loi_giai.py` (`round((26**8)/(1e4*86400))` = `242`), `practice` (`242`), and `L01` `example`/`check`/`pitfalls` (`242 ngày`).
  2. **L06**: `labs/SEC/L06/de.md` line 5 has `2. escaped_len=38`, directly contradicting `mong_doi.txt` (`37`), `loi_giai.py` (`len(html.escape('<script>alert(1)</script>'))` = `37`), `practice` (`37`), and `L06` `check` (`25 + 4*3 = 37`).
  3. **L07**: `labs/SEC/L07/loi_giai.py` line 9 hardcodes `print('ecb_leaks_pattern=1')` instead of deriving it from `ecb0 == ecb1` (and `practice` claims `CBC/CTR` though L07 never covers CBC).
  4. **L10**: `labs/SEC/L10/loi_giai.py` line 5 hardcodes `print('ratio_vs_32bit_hash=1')`, `labs/SEC/L10/de.md` omits any definition of `ratio_vs_32bit_hash`, and `L10` `practice` step 0 mislabels the formula evaluation as `(Mô phỏng định lượng)`.
  5. **L11**: `labs/SEC/L11/de.md` line 3 states `kỳ vọng số lần đoán trung bình (2^16)/2 khi chương trình khởi động lại mỗi lần đoán sai` — omitting `"nhưng giữ nguyên bố trí địa chỉ"`. As `L11_an_toan_bo_nho.yaml` (`check` step 1) explicitly contrasts, restarting with re-randomization requires `2^16 = 65 536` guesses, whereas `(2^16)/2 = 32 768` only holds when layout is preserved. Also `L11/de.md` prose omits `28 bit` entirely despite requiring `3. slots_28bit=268435456`.

---

### 4. P9 (Visual layout clarity & `clear: true` before big blocks)
- **Score: 12/15 (80%)** on strict `clear: true` discipline (**15/15** on visual legibility & `layout_SEC.tsv` = 0 errors).
- All `intuition` SVGs, `pitfalls` steps 2–3, `example` mid-scene resets, and all `practice` steps 0–1 have `clear: true` and render cleanly.
- Minor non-overflowing cases where a second table follows a large table/text block without `clear: true`: `L03 check 1` (`00044.png`), `L05 prereq 1` (`00014.png`), `L09 prereq 1` (`00014.png`).

---

### 5. MUST Blockers & SHOULD Improvements

#### MUST Blockers (5 items)
1. **`labs/SEC/L01/de.md`**: Fix `slow_crack_days=24170` → `slow_crack_days=242` to match `26^8 / (1e4 * 86400)`, `mong_doi.txt`, `loi_giai.py`, `practice`, and lesson body.
2. **`labs/SEC/L06/de.md`**: Fix `escaped_len=38` → `escaped_len=37` to match `len(html.escape('<script>alert(1)</script>'))`, `mong_doi.txt`, `loi_giai.py`, `practice`, and `L06` `check`.
3. **`labs/SEC/L07/loi_giai.py`**: Replace hardcoded `print('ecb_leaks_pattern=1')` with computed `int(ecb0 == ecb1)` (and slice `msg = b'BLOCK_A_' * 2` into `b0, b1 = msg[:8], msg[8:]`).
4. **`labs/SEC/L10/loi_giai.py`, `de.md`, `L10_ham_bam_ngay_sinh.yaml` (`practice`)**: Define `ratio_vs_32bit_hash` explicitly in `de.md`, compute it in `loi_giai.py` instead of hardcoding `'ratio_vs_32bit_hash=1'`, and remove `(Mô phỏng định lượng)` from `L10` `practice` step 0 (or make the lab an actual Monte Carlo simulation).
5. **`labs/SEC/L11/de.md`**: Clarify `"khởi động lại nhưng giữ nguyên bố trí địa chỉ"` for `(2^16)/2 = 32 768`, and explicitly mention `28 bit` in the problem statement before `slots_28bit=268435456`.

#### SHOULD Improvements
1. **P1 inline glossing in AF2 `practice` & `de.md` (`L00–L14`)**: Gloss/map unintroduced English terms & acronyms back to lesson vocabulary and expand `PY` → `Python` in `practice` tables.
2. **`L02/de.md` wording**: Replace `"chênh lệch độ mạnh bội số không gian mẫu"` with `"kiểm tra 4 từ có mạnh hơn 8 chữ thường không (1 = có, 0 = không)"`.
3. **Function-name & lab alignment (`L05`, `L12`, `L14`)**: Align `loi_giai.py` function names with `de.md` (`cookie_sent` in `L05`, `decide` in `L12`), and consider aligning `L14/de.md` with the 4-condition ransomware-hardened `3-2-1 + immutable` model taught in `L14`.
4. **Generic `covers:` metadata (`L00–L14`)**.
5. **P9 `clear: true` polish**: Add `clear: true` on `L03 check 1`, `L05 prereq 1`, `L09 prereq 1` before their second tables.
6. **Rebuild affected videos** when YAML `practice` text changes.
