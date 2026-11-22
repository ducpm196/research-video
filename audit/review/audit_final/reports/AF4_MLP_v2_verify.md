# Independent Read-Only Verification Report v2: Course `MLP` (`L00–L13`)

**Role:** `WP-AF4-4 MLP Verifier v2` (read-only; zero workspace modifications)  
**Verdict:** **`NO-GO`** (`MUST = 2` in `L13`, target `0`; `P8 = 92.9%` [13/14 lessons], target `100%`)

All prior v1 blockers and visual `SHOULD`s in `L03`, `L04`, `L09`, and `L12` are **FIXED and cleanly rebuilt**. However, a post-build YAML edit to `L13` (`lessons/mlp/L13_tinh_huong_phat_hien_gian_lan.yaml`, modified when `gen_mlp.py` re-ran wall-clock timing for `L12`) left `L13` stale and introduced `elapsed_s=2.98` vs `"chưa tới một giây"` / `< 1 s`.

---

## 1. Summary Metrics
- **`MUST` count:** **`2`** (both in `L13`: stale build `spec_sha256` mismatch + `elapsed_s=2.98` vs `"chưa tới một giây"` / `< 1 s`)
- **`P1` inline glossing:** **~91%** (`>= 80%` PASS)
- **`P8` exact `say`/`show`/`lab`/build alignment:** **92.9%** (`13/14` lessons `L00–L12` pass; `14/14` labs match `mong_doi.txt`; `L13` fails)
- **`P9` visual clarity & `clear: true`:** **`clear: true` 100%** (252/252 steps); **8/8 inspected v2 PNGs clean** (`L03`, `L04`, `L09`, `L12` `.code` wraps clean, `L13/00021.png` stale)

## 2. Action Needed for `GO`
1. Eliminate wall-clock `elapsed_s` drift or align `L13` wording (`<= 5 s` / `"chỉ vài giây"`) in `audit/mlp/data_mlp_b.py`, rebuild `L13` (`lv.py build` + `lv.py asr` + `asr_flags.py MLP`), and re-verify `L13`.
