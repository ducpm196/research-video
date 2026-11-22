# Independent AF4 Verification Report v2 — SEC `L00–L14` (+ `L15` spot-check)

**Verifier:** `1d88086d` (`WP-AF4-3 Stage 7 SEC Verifier v2`, read-only)  
**Verdict: `GO`** (`MUST: 0`, `P1: 15/15 = 100%`, `P8: 15/15 = 100%`, `P9: 15/15 = 100% visual / 80% strict clear: true`, `+L15 PASS`)

---

### 1. Prior 5 MUST Blockers & P1 Fixes — All Resolved
1. **`L01` (`labs/SEC/L01/de.md`)**: `2. slow_crack_days=242` aligned with `mong_doi.txt`, `practice`, and lesson body; `hex` & `salt` inline-glossed.
2. **`L06` (`labs/SEC/L06/de.md`)**: `2. escaped_len=37` aligned with `mong_doi.txt`, `practice`, and `L06 check`; `HTML/XSS/SQL/SQLite/payload` inline-glossed.
3. **`L07` (`labs/SEC/L07/{loi_giai.py, de.md}` & `practice`)**: Computes `same_ecb = int(ecb0 == ecb1)` genuinely (no hardcoding); `ECB` vs `CTR/IV/nonce` aligned.
4. **`L10` (`labs/SEC/L10/{loi_giai.py, de.md}` & `practice`)**: Genuinely computes `round(k / (2 ** bits_sec))`; `(Mô phỏng định lượng)` removed.
5. **`L11` (`labs/SEC/L11/{de.md, loi_giai.py}` & `practice`)**: Mentions `28 bit` (`2^28 = 268 435 456`) and `"giữ nguyên bố trí địa chỉ"`; `ASLR`/`entropy` inline-glossed.
6. **P1 across `L00–L14`**: All `practice` tables use `Python`; STRIDE, `Diceware`, `OTP`, `RBAC`, `CSRF`, `CA/TLS`, `first-match/ALLOW/DENY`, `Bayes PPV` all glossed inline.

### 2. Sync, Lint, Labs & Visual Inspection (`L00–L14` + `L15`)
- `spec_sha256` & `tts_sha256`: **16/16 match** (`rebuilt 2026-11-19T14:57..15:26Z`).
- `SRT == say`: **16/16 exact match**. `asr_report.md`: **16/16** `thiếu audio: 0`, `chưa xem xét: 0`.
- `lv.lint`: **16/16 `0 FAIL, 0 WARN`**. `audit/sec/verify_sec.py`: **26 PASS · 0 FAIL**. Scene `checks`: **190/190 PASS**. `screen_code/SEC.yaml`: **19/19** verified. `loi_giai.py == mong_doi.txt`: **16/16**.
- Visually inspected **27 rendered `1920x1080` PNGs** across `L01, L03, L05, L06, L07, L09, L10, L11, L12, L13, L15` — crisp, zero clipping/overlap/overflow.
