# Báo cáo kiểm định độc lập AF4 v2 — Stage 11 RBM (`L10–L17`, CHỈ ĐỌC 100%)

## 1. Kết luận: **NO-GO**
Toàn bộ **8/8** bài `L10–L17` đã khắc phục xong các lỗi lớn trước đó: 0/8 lộ code/output trước `pause: 30`, `L10 PI_final_err=0.0001` khớp đúng `y'=-y+u`, `L15` tường `4×5` rõ ràng, `L16` `fit.svg` hết đè chữ, `L17 32K` giải thích rõ trong `say`, và **P9 = 2 đạt 8/8**.

Còn 4 nhóm vấn đề cần vá:
1. **`covers:` trỏ sai cảnh dạy mục tiêu ở 7/8 bài** (`L10, L12, L13, L14, L15, L16, L17`).
2. **P1 bảng `practice`**: `common.py` bắt nhầm `{...:.2f}` trong f-string thành `dict(...)` ở 7/8 bài (`L10–L14, L16–L17`); thiếu nhiều cú pháp thật (`L15`: `{a,b}`, `(a,b)`, `heapq.heappop/heappush`, `not in`, `.get()`, `and`, `0 <= v[0] < 4`, `_`; `L13`: list comp lồng; `L10, L12, L14, L16, L17`: gán nhiều biến / tuple / `_`).
3. **`de.md` thiếu chi tiết ở 2/8 bài (`P8 = 1`)**: `L10/de.md` thiếu `y(0)=0, integ(0)=0` & quy tắc Euler; `L11/de.md` thiếu định nghĩa & quy cách làm tròn `.2f/.2f/.5f` của `g_030, x10_div, x10_conv`.
4. **MP4 `out/rbm/L10..L17` chưa dựng lại** + **5 chỗ `"càng "` (`L10, L12×2, L16, L17`)** + `L17 stage3#3` ghi chú `32K` trên `show`.

---

## 2. Bảng tóm tắt chỉ số (`RBM L10–L17`)
| Chỉ số | Kết quả | Ghi chú |
|---|---|---|
| `tools/lv.py lint` (`L10–L17`) | **8 / 8 PASS** (`0 FAIL, 0 WARN`) | `12.3–14.1p` (`L10–L16`), `23.1p` (`L17`) |
| `audit/rbm/verify_rbm.py` | **92 / 92 PASS** | — |
| `screen_code` RBM | **36 / 36 PASS** | — |
| `loi_giai.py == mong_doi.txt` | **8 / 8 KHỚP** | (`lab_gate.py` cần chạy ngoài sandbox để tránh lỗi `bash.exe` `-1073741502`) |
| `audit/layout_RBM.tsv` | **0 dòng lỗi** | — |
| P8 không lộ trước `pause: 30` | **8 / 8** (6/8 đạt P8=2; `L10, L11` P8=1) | — |
| P9 (`Hai mức quy mô`) | **8 / 8** | — |

---

## 3. Bảng chi tiết từng bài (`L10–L17`)
| Bài | Phút | MUST | P1 | P8 | P9 | Lỗi chính |
|---|---:|---:|---:|---:|---:|---|
| `L10` | 12.3 | 3 | 1 | 1 | 2 | `covers` obj1/obj2; `de.md` thiếu `y(0)=0, integ(0)=0` & Euler; `P1` `y, integ, dt =`, `_`, `dict` ma; `"càng "` `ponly#4` |
| `L11` | 14.1 | 1 | 2 | 1 | 2 | `de.md` thiếu định nghĩa & `.2f/.2f/.5f` cho `g_030, x10_div, x10_conv`; `dict` ma |
| `L12` | 13.4 | 2 | 1 | 2 | 2 | `covers` obj3 (`cycle`); `P1` `x, P, z, R =`, `dict` ma; `"càng "` `sym#0`, `pitfalls#1` |
| `L13` | 12.1 | 3 | 1 | 2 | 2 | `covers` obj1 (`sym`) & obj3 (`intuition`/`example`); `P1` list comp lồng & `dict` ma; `recap#0` `"xe thật 15 biến"` |
| `L14` | 13.6 | 2 | 1 | 2 | 2 | `covers` obj3 (`dft`); `P1` `f_sig, fs =` & `dict` ma |
| `L15` | 12.5 | 3 | 0 | 2 | 2 | `covers` obj2 (`admissible`) & obj3 (`example`); `P1` thiếu `set/tuple/heapq/not in/.get/and/chaining/_` |
| `L16` | 13.9 | 2 | 1 | 2 | 2 | `covers` obj2 (`example`); `P1` tuple/`x, _` & `dict` ma; `"càng "` `confidence#1` |
| `L17` | 23.1 | 2 | 1 | 2 | 2 | `covers` obj2 (`stage2`/`stage4`) & obj3 (`quiz`); `P1` `P, R =`, `_`, `dict` ma; `"càng "` `stage1#1`; `32K` trên `show` |
