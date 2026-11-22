# Independent Read-Only Verification Report: Course `MLP` (`L00–L13`)

**Role:** `WP-AF4-4 MLP Verifier` (read-only; zero workspace modifications)  
**Verdict:** **`NO-GO`** (`MUST = 2`, target `0`; `P8 = 85.7%` [12/14 lessons], target `100%`)

---

## 1. Summary Metrics

| Metric | Target | Observed | Status |
|---|---|---|---|
| `MUST` count | `0` | **`2`** (`L03.example`, `L12.check` `say`/`show` contradictions) | **FAIL** |
| `P1` inline glossing rate | `>= 80%` | **~91%** (all 14 `sym` + `formula` scenes cover core APIs/formulas) | **PASS** |
| `P8` exact `say`/`show`/`lab` alignment | `100%` | **85.7%** (12/14 lessons; 14/14 labs match `mong_doi.txt`, 2 `say`/`show` contradictions in `L03`, `L12`) | **FAIL** |
| `P9` visual clarity & `clear: true` | `>= 80%` | **`clear: true` 100%** (all steps); **~92% frames clean** (3 minor `.code` right-border overflows in `L04`, `L09`, `L12`) | **PASS (with SHOULD)** |

---

## 2. Course-Level Checks Observed
- **`D:\research-video\curriculum\mlp.yaml`**: `14 bài, 14 đã có đặc tả, 0 lỗi` via `tools/lv.py curriculum curriculum/mlp.yaml`.
- **`D:\research-video\audit\layout_MLP.tsv`**: Empty (0 layout violations).
- **`tools/lv.py lint` & `tools/lv.py verify` (`L00–L13`)**: **14/14 PASS**.
- **Lab execution (`labs/MLP/L00..L13/loi_giai.py`)**: 14/14 pass cleanly via `labs/.venv-ml/Scripts/python.exe` matching `mong_doi.txt`.

---

## 3. Blocking `MUST` Findings (2)
1. **`MUST-1` (`P8`, `L03` `example` step 2 `say` vs `show`):** `lessons/mlp/L03_phan_loai_nguong_pr.yaml` lines 139–145 (`out/MLP/L03/frames/00021.png`): `show` prints identical `P=1.000 R=0.933 F1=0.966` for `t=0.50` and `t=0.30`, whereas `say` claims Recall jumped and Precision fell.
2. **`MUST-2` (`P8`, `L12` `check` step 2 `say` vs `show`):** `lessons/mlp/L12_dong_goi_suy_luan_cpu.yaml` lines 178–180 (`out/MLP/L12/frames/00025.png`): `show` displays `json_bytes=69`, whereas `say` speaks `"tám mươi chín bai"` (`89`).

## 4. Non-Blocking `SHOULD` Findings
- **`.code` right-border overflow**: `L04` (`00018.png`), `L09` (`00018.png`), `L12` (`00018.png`).
- **Truncated `hook` titles** (`L01–L04, L06, L08, L09, L11–L13`), minor `L05` `hook` `98%` vs `95%`, `L04` `"across K folds"`, minor secondary term glosses.
