# WP-AF4-2 Independent Read-Only Verification Report (v2) — Course CPR (`L00–L09`)

**Verifier:** `4131ffa7` (`WP-AF4-2 CPR Verifier v2`, read-only)  
**Target:** Course `CPR` (`L00–L09`, 10 lessons) after fixes & rebuilds.

---

## 1. Automated & Structural Checks (Directly Observed)
- **`audit/cpr/verify_cpr.py`**: **37/37 PASS** (all 19 `example`/`check` C11 programs + all 10 `labs/CPR/L00..L09/loi_giai.c` compiled & executed via GCC vs `mong_doi.txt` + 8 `checklib` cross-checks).
- **`tools/lv.py lint` (`L00–L09`)**: **0 FAIL, 0 WARN** across all 10 specs:
  - `L00`: 21 PASS (1,027 words, ~6.8 min)
  - `L01`: 21 PASS (1,020 words, ~6.8 min)
  - `L02`: 19 PASS (993 words, ~6.6 min)
  - `L03`: 20 PASS (910 words, ~6.1 min)
  - `L04`: 19 PASS (921 words, ~6.1 min)
  - `L05`: 20 PASS (964 words, ~6.4 min)
  - `L06`: 20 PASS (912 words, ~6.1 min)
  - `L07`: 19 PASS (904 words, ~6.0 min)
  - `L08`: 22 PASS (921 words, ~6.1 min)
  - `L09`: 19 PASS (981 words, ~6.5 min)
- **`tools/lv.py curriculum curriculum/cpr.yaml`**: **10 bài, 10 đã có đặc tả, 0 lỗi**.
- **`audit/review/screen_code.py check --course CPR`**: **48/48 PASS** (`run/c 19, output/- 19, other/text 10`; `FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0`; `unverified_claims: 0`).
- **`tools/lv.py verify` (`L00–L09`)**: **10/10 PASS** (`spec_sha256` & `tts_sha256` match, `h264` 1920x1080 + `aac`, duration == `timeline_seconds`, single voice `vi-VN-NamMinhNeural` via `edge`).
- **`Lxx.srt` vs YAML `say` (`L00–L09`)**: **10/10 exact match** (`0 diffs`, cue count == frame count on all 10 lessons).
- **`out/CPR/Lxx/asr_report.md` (`L00–L09`)**: **10/10 PASS** (`thiếu audio: 0`, `chưa xem xét: 0` on all 10 lessons).
- **`audit/layout_CPR.tsv`**: Observed as empty (1 blank line), so visual verification relied directly on rendered `1920x1080` PNGs in `out/CPR/L00..L09/frames/`.

---

## 2. Build, Stream, SHA & ASR Details (`L00–L09`)

| Lesson | Frames / SRT | Duration / Timeline | `spec_sha256` (prefix) | `tts_sha256` (prefix) | ASR (`thiếu` / `gắn cờ` / `chưa xem xét`) | `lv.py verify` |
|---|---|---|---|---|---|---|
| `L00` | 52 / 52 | 363.73s / 363.733s | `a5d69098dfaba45b` | `9f9fcaddf1e3305a` | 0 / 4 / 0 | PASS |
| `L01` | 51 / 51 | 352.4s / 352.4s | `995d08ac15828d71` | `35db711ac45d5cb4` | 0 / 2 / 0 | PASS |
| `L02` | 49 / 49 | 351.1s / 351.1s | `7824bb990aaac9ce` | `fc382a6373e1c324` | 0 / 1 / 0 | PASS |
| `L03` | 47 / 47 | 328.47s / 328.467s | `582057b816c363df` | `d7c514f585e10482` | 0 / 1 / 0 | PASS |
| `L04` | 48 / 48 | 332.27s / 332.267s | `d695cb8e2fbbb16d` | `7b091a0da71d1294` | 0 / 2 / 0 | PASS |
| `L05` | 49 / 49 | 341.4s / 341.4s | `61930dc0e0183fc1` | `398f764e5a6fb47c` | 0 / 4 / 0 | PASS |
| `L06` | 48 / 48 | 332.2s / 332.2s | `2283c00e314892d1` | `f58dc88ac582a977` | 0 / 4 / 0 | PASS |
| `L07` | 45 / 45 | 322.7s / 322.7s | `2d2b9563e2ca74fd` | `225fd10a2a094844` | 0 / 2 / 0 | PASS |
| `L08` | 45 / 45 | 323.83s / 323.833s | `b5d5d9349a3a58ad` | `b74deed982ad17aa` | 0 / 1 / 0 | PASS |
| `L09` | 47 / 47 | 341.97s / 341.967s | `171d504b85e56fc8` | `0bed67b551202c5d` | 0 / 3 / 0 | PASS |

---

## 3. Resolution of Prior MUST, P9 SVG & P1/SHOULD Items

1. **Prior MUST (`L09 example.2` / step 3, `lessons/cpr/L09_tinh_huong_phan_tich_nhat_ky.yaml:167-170`) — RESOLVED:**
   - `say` now accurately explains `clean=1`: *"Biến sạch bằng một chứng tỏ con trỏ dữ liệu đã được đưa an toàn về rỗng sau khi giải phóng."* Matches `v.d == NULL` (`line 159`).
2. **Prior P9 SVG Clipping/Overflow (`L00`, `L02`, `L09`) — RESOLVED (Visual PNG Inspection):**
   - `L00 intuition` (`out/CPR/L00/frames/00016.png`, `L00_chuong_trinh_c_sizeof.yaml:111-124`): Widened 110px gaps + shortened labels `"GCC dịch"`, `"Nạp RAM"`. Clean, zero clipping.
   - `L02 intuition` (`out/CPR/L02/frames/00009.png`, `L02_ham_ngan_xep.yaml:81-94`): Widened 120px gaps + shortened labels `"Chép 10, 25"`, `"return → xoá"`. Clean, zero clipping.
   - `L09 intuition` (`out/CPR/L09/frames/00010.png`, `L09_tinh_huong_phan_tich_nhat_ky.yaml:89-104`): Widened orange Box 2 (`width="255"`) fits `"2. Đầy → Kiểm & Nhân đôi"` cleanly inside border.
   - Representative SVG, table, code, pitfall, and practice PNGs visually inspected across `L00–L09` (`L00/00024.png`, `L00/00027.png`, `L01/00010.png`, `L01/00023.png`, `L02/00028.png`, `L03/00009.png`, `L03/00018.png`, `L04/00010.png`, `L04/00017.png`, `L05/00010.png`, `L05/00020.png`, `L06/00010.png`, `L06/00021.png`, `L07/00009.png`, `L07/00018.png`, `L07/00026.png`, `L08/00008.png`, `L08/00019.png`, `L09/00016.png`, `L09/00020.png`, `L09/00030.png`, `L09/00042.png`): zero clipping, overlap, or truncation.
3. **Prior P1 Inline Glosses & SHOULD Alignments (`L00–L09`) — RESOLVED:**
   - `L00` (`L00_chuong_trinh_c_sizeof.yaml:157-164`): All 4 rows of `example.0` table narrated and aligned.
   - `L01` (`L01_bien_vong_lap_tran_so.yaml:129-142`): Unused `<limits.h>` replaced by `<stdint.h>` (`INT32_MAX`, `INT32_MIN`), `%u`/`%d`, `static`, `&&`, `(uint8_t)` cast all glossed inline before use. *(Minor remaining SHOULD: ternary `?:` in `L01 check.0` line 172 `ok1 ? (a + b1) : 0` and `L09 example.1` line 154 `v->cap ? v->cap * 2 : 2` is not explicitly in a syntax-gloss row, though clear in context.)*
   - `L02` (`L02_ham_ngan_xep.yaml:126-137`): `static` helper, `%d`, and `if (n <= 0) return 0;` cleanly glossed; unused `?:` row removed.
   - `L03` (`L03_mang_chuoi_c.yaml:124-136`): `const char s[]`, `snprintf`, and `(void)need;` (`-Werror` unused-var silence) explicitly glossed.
   - `L04` (`L04_con_tro_dia_chi.yaml:103,131-144`): Hex `0x7000` read cleanly (`"hệ thập lục phân bảy nghìn"`), `||` and `if (q)` (`q != NULL`) glossed in `example.0`.
   - `L05` (`L05_so_hoc_con_tro.yaml:133-145`): `<stddef.h>`, `ptrdiff_t`, `%td`, and `const int *a, size_t n` glossed in `example.0`.
   - `L06` (`L06_cap_phat_dong_heap.yaml:145-159`): `if (!p)` / `if (!tmp)` explicitly glossed as `p == NULL`.
   - `L07` (`L07_struct_padding_linked_list.yaml:126-139,190-201`): `while (h)` (`h != NULL`), `<stddef.h>` / `offsetof(S, field)` glossed in `example.0`; `quymo.0` `say` aligned to `"một trăm nghìn bản ghi"` (`0,4 MB`) and `"một triệu bản ghi"` (`4 MB`).
   - `L08` (`L08_tep_nhi_phan_bit.yaml:123-137`): `FILE *f`, `fclose(f)`, `<< 12`, `|`, and `0xFFF` glossed in `example.0`.
   - `L09` (`L09_tinh_huong_phan_tich_nhat_ky.yaml:133-149,227`): `example.0` aligned with 4 rows including 2-arg `_Static_assert(sizeof(Rec) == 16, "...")`, `(Rec){...}`, `(unsigned long long)sum` + `%llu`; `pitfalls.0` fixed to 2-arg `_Static_assert`.
4. **Labs (`labs/CPR/L00..L09/{de.md, loi_giai.c, mong_doi.txt}`) — 100% ALIGNED:**
   - Every `practice.1` expected output block in `L00–L09` YAML matches `labs/CPR/Lxx/mong_doi.txt` character-for-character and matches `de.md` & `loi_giai.c`.

---

## 4. Per-Lesson Scores & Overall Verdict

| Lesson | MUST | P1 (Inline Glossing) | P8 (`say`/`show`/`lab`) | P9 (Visual Clarity) | Notes |
|---|---|---|---|---|---|
| `L00` | 0 | 2 | 2 | 2 | SVG fixed (`00016.png`), 4-row `example.0` aligned |
| `L01` | 0 | 1 | 2 | 2 | `<stdint.h>`, `%u`/`%d`, `static`, `&&` fixed; minor SHOULD: ternary `?:` in `check.0` |
| `L02` | 0 | 2 | 2 | 2 | SVG fixed (`00009.png`), `example.0` clean |
| `L03` | 0 | 2 | 2 | 2 | `const`, `(void)need;` glossed |
| `L04` | 0 | 2 | 2 | 2 | `||`, `if (q)`, `0x7000` clean |
| `L05` | 0 | 2 | 2 | 2 | `ptrdiff_t`, `<stddef.h>`, `%td` glossed |
| `L06` | 0 | 2 | 2 | 2 | `!p` glossed as `p == NULL` |
| `L07` | 0 | 2 | 2 | 2 | `offsetof`, `while (h)`, `quymo.0` `say` aligned |
| `L08` | 0 | 2 | 2 | 2 | `<<`, `|`, `0xFFF`, `FILE *`, `fclose` glossed |
| `L09` | 0 | 2 | 2 | 2 | MUST `clean=1` (`v.d == NULL`) fixed, SVG fixed (`00010.png`), 2-arg `_Static_assert` fixed |

### Summary Metrics
- **`MUST` total:** **0** (target `0`)
- **`P1=2` rate:** **9/10 (90%)** (target `>= 80%`) — 1 minor non-blocking SHOULD (`?:` operator gloss in `L01 check.0` / `L09 example.1`)
- **`P8=2` rate:** **10/10 (100%)** (target `100%`)
- **`P9=2` rate:** **10/10 (100%)** (target `>= 80%`)

### Final Verdict: **GO**
All prior MUST, P9 SVG overflow/clipping, and P1/SHOULD blockers are resolved, all automated gates (`verify_cpr.py` 37/37, `lv.py lint` 0 FAIL/0 WARN, `lv.py curriculum` 0 errors, `screen_code.py` 48/48, `lv.py verify` 10/10, SRT exact match 10/10, ASR 0 missing/0 unreviewed) pass, and visual PNG checks are clean.
