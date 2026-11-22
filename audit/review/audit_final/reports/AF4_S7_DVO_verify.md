# WP-AF4-3 Stage 7 Independent Verification Report — Course `DVO` (`L00–L13`)

**Verifier:** `63e85ddc` (`WP-AF4-3 Stage 7 DVO Verifier`, read-only)  
**Verdict: `NO-GO`** (`MUST = 1`: `L09` `9.2h` vs `8.8` on-screen arithmetic contradiction; `P1` = 92.9% core / 42.9% incl. `practice#0`; `P8` = 100%; `P9` = 92.9%)

---

## 1. Automated & Read-Only Checks (`L00–L13`, 14 lessons)
- `lv.py curriculum`, `lv.py lint` (`14/14` 0F/0W), `lv.py verify` (`14/14`), `layout_DVO.tsv` (`0`), `screen_code` (`14/14`), `verify_dvo.py` (`18/18`), direct Python lab run (`14/14`), `SRT == say` (`14/14`), `ASR` (`0 thiếu, 0 chưa xem xét`), `27/27 PNGs` crisp & legible.
- **[MUST-1] `L09` arithmetic mismatch:** `lessons/dvo/L09_bon_chi_so.yaml:261` (`upgrade_dvo.py:129`, `out/DVO/L09/frames/00076.png`) prints `trung bình lệch (9.2h)` instead of `8.8h`, contradicting `lead_mean_h=8.8` (`mong_doi.txt`, `00079.png`, `pitfalls#2`).
- **[P1] `practice#0` glosses:** Unglossed tags in `L00` (`git bisect`), `L02` (`SemVer`), `L03/L12` (`CI`), `L05` (`IaC`), `L08` (`Expand-Contract`), `L11` (`req/s/log/TB` + `CPU`), `L12` (`prod`), `L13` (`DORA Elite/Low`, `~208` vs `209x`).
- **[SHOULD]:** Align `L08` `dt` simulation + `L03`/`L04`/`L06` `de.md` details with `loi_giai.py`.
