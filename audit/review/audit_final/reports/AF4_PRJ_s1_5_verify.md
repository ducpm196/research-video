# WP-AF4-2 Independent Verification Report — `PRJ` `L00–L04` (`S01–S05`)

**Scope Verified (read-only, verifier `66c769b3`):**
- Curriculum & Lab Spec: `D:\research-video\curriculum\prj.yaml`, `D:\research-video\labs\PRJ\SPEC.md`
- Lesson YAML specs: `D:\research-video\lessons\prj\L00_*.yaml` .. `L04_*.yaml`
- Labs: `D:\research-video\labs\PRJ\L00\` .. `L04\` (`de.md`, `loi_giai.py`, `mong_doi.txt`)
- Rendered outputs: `D:\research-video\out\PRJ\L00\` .. `L04\` (`build_report.json`, `asr_report.md`, `L0x.srt`, `_frames.txt`, 63 sampled `frames/*.png`)

## Global Tooling & Automated Checks (OBSERVED)
| Check | Observed Result | Status |
|---|---|---|
| Lint (`L00–L04`) | `L00`: 18 PASS; `L01–L04`: 17 PASS each. **0 FAIL, 0 WARN** across all 5 | **PASS** |
| Curriculum (`prj.yaml`) | `11 bài, 11 đã có đặc tả, 0 lỗi` | **PASS** |
| Spec digest & SRT==`say` | **5/5** `spec_sha256` match `build_report.json`; **5/5** `srt_match_exact=True`; single voice `vi-VN-NamMinhNeural` | **PASS** |
| Reference verifier (`verify_prj.py`) | `verify_prj: 20/20 PASS` | **PASS** |
| Screen code ledger (`PRJ`) | `55 khối — PASS 55 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0` | **PASS** |
| On-screen Python snippets | **10/10** `rc=0`; stdout matches on-screen output steps verbatim | **PASS** |
| Lab `loi_giai.py` vs `mong_doi.txt` | **5/5** `rc=0`, stdout matches `mong_doi.txt` & `practice` expected output 100% | **PASS** |
| `lab_gate.py PRJ` (`cham.sh` via Git Bash) | Run in unrestricted shell by coordinator: `11 PASS · 0 FAIL` (covering `L00–L10`) | **PASS** |

## Summary Verdict

| Lesson | MUST | SHOULD | P1 (Capstone / Strict R4) | P8 (Quiz & Lab) | P9 (Scale & Layout) | Spec/SRT/ASR |
|---|---:|---:|---|---|---|---|
| `L00` | 0 | 2 | Capstone OK / Strict notes (Python/SQL syntax) | PASS | PASS | PASS (48/48) |
| `L01` | 0 | 2 | Capstone OK / Strict notes (SQL/Python syntax) | PASS | PASS | PASS (44/44) |
| `L02` | 0 | 2 | Capstone OK / Strict notes (`JWT`/`b'...'`/SQL) | PASS | PASS | PASS (48/48) |
| `L03` | 0 | 1 | Capstone OK / Strict notes (`set`/`sorted`/comp) | PASS | PASS | PASS (43/43) |
| `L04` | 0 | 2 | Capstone OK / Strict notes (`OLS`/`setdefault`/gen) | PASS | PASS | PASS (44/44) |

**Overall Verdict:** **`ALLOW_WITH_CONDITIONS` -> PASS (0 MUST defects)**
- **Zero MUST defects** across all 5 lessons (`L00–L04`): `lv.py lint` 0 FAIL / 0 WARN, `verify_prj.py` 20/20 PASS, `screen_code` 55/55 PASS, `spec_sha256` 5/5 match, `SRT == say` 5/5 exact, `asr_report.md` 0 unreviewed, 63/63 sampled rendered PNGs clean with high contrast and no overflow, and all 5 `loi_giai.py` + 10 on-screen Python snippets verified exact.
- **Minor SHOULD notes** (`L00` `<= 0` vs `isdigit()`, `L01` `ORDER BY sorted(...)`, `L02` `exp` check & `OFFSET 99 980`, `L03` `hook.checks` 3 vs 4 items, `L04` `SS_xx` naming & early `if d >` explanation): polish optional, zero factual/code breakage.
