# Báo cáo kiểm định độc lập v2 khoá ROB (Robot tự hành) — Stage 11 (`AF4 v2`)

- **Phạm vi đọc & kiểm chứng độc lập**: Đọc toàn bộ 14 bài `lessons/rob/L00_*.yaml`..`L13_*.yaml`, 14 bộ lab `labs/rob/L00..L13/{de.md, loi_giai.py, mong_doi.txt}`, `curriculum/rob.yaml`, `audit/rob/{verify_rob.py, sources_L13.md}`, `audit/review/screen_code/ROB.yaml`, `audit/layout_ROB.tsv`, `out/ROB/L00..L13/{build_report.json, L*.srt, asr_report.md}`. Chạy độc lập bằng `.venv\Scripts\python.exe` (chỉ đọc, không sửa tệp nào).
- **Verdict tổng thể**: **`NO-GO`** (đã sửa được rò rỉ P8 trước `pause` và P9 `recap`, nhưng vẫn còn lỗi **`MUST`** ở `L07`, `L09`, `L13`, `covers:` 7 bài, và hỏng khuôn stdout `practice.0` ở `L01`, `L09`; đồng thời 14/14 MP4/SRT/ASR hiện đang **STALE** so với YAML sau lần sửa `15:27–15:29`).

---

## 1. Bảng tổng hợp kết quả chạy công cụ & chỉ số

| Hạng mục kiểm tra | Kết quả đo | Trạng thái | Ghi chú |
|---|---|---|---|
| `lv.py lint` (14 bài `L00..L13`) | **14 / 14 PASS** (`0 FAIL, 0 WARN`) | **PASS kỹ thuật** | `L00` thực tế ước tính ~8.60 phút (< 9 phút) |
| `verify_rob.py` | **14 / 14 PASS** | **PASS** | Mọi kiểm chứng toán/mô phỏng thân bài đều đúng |
| `screen_code.py check --course ROB` | **28 / 28 khối PASS** (`0 FAIL/STALE/MISSING/ORPHAN/WARN`) | **PASS** | — |
| `lab_gate.py ROB` | Trong sandbox bị `bash.exe` exit `-1073741502`; chạy trực tiếp Python khớp `mong_doi.txt` **14/14** | **Khớp Python 14/14** | — |
| `audit/layout_ROB.tsv` | **0 dòng lỗi** (2 byte) | **PASS** | — |
| `P8` không lộ code/stdout trước `pause: 30` | **14 / 14 bài** | **PASS phần thứ tự** | Còn lỗi nghiêm trọng về tự đủ (`L09`), sai toán/spoiler (`L07`), sai dữ kiện/công thức (`L13`), khuôn sai (`L01`, `L09`) |
| `P9` (`Hai mức quy mô` trong thân bài + `recap`) | `recap`: **14 / 14**; thân bài: **13 / 14** (`L03` còn thiếu bảng/ví dụ 2 mức tường minh) | **PASS 13/14 (≥80%)** | — |
| `covers:` khớp đúng cảnh dạy thật | **7 / 14** (hoặc 6/14 nếu tính `L01` `check` phụ) | **FAIL** | `L00, L03, L04, L06, L08, L12, L13` trỏ sai cảnh |
| `out/ROB/L00..L13` MP4/SRT/ASR khớp YAML hiện tại | **0 / 14** (`STALE = 14/14`) | **STALE — CHƯA REBUILD** | Chờ sửa xong rồi dựng lại |

---

## 2. Phát hiện hệ thống xuyên suốt

1. **Lỗi P1 ở bảng giải thích mã Python (`practice.2`)**:
   - **13/14 bài (`L00–L08, L10–L13`)** chèn dòng ma `{k: v} / dict(...)` do nhận nhầm `{...}` trong f-string; **`L09`** chèn dòng ma `{a, b} / set() / .add()`.
   - Thiếu giải thích token thật: gán nhiều biến `a, b = ...` (`L01, L03, L05, L09, L10, L12`), tập hợp `{2, 5}` và `in` (`L04`), tham số mặc định `lambda z, mu=3.0, s=0.2:` (`L03`), `raw[-1]` (`L07`), tuple `(v, w)` và giải nén `for v, w in cands:` (`L09`).
   - `L01` `practice.0` bị lỗi khuôn đầu ra: `v=...s omega=...s R=...m` (thiếu `m/` và `rad/`); `L09` `practice.0` dư ngoặc: `best=...)`.
2. **Thuật ngữ/ký hiệu/từ viết tắt chưa giải thích trước khi dùng**:
   - `L02`: `lidar`, `encoder`, `con quay hồi chuyển`; `L03`: `Gauss`; `L05`: `\operatorname{diag}`, `EKF` ở `hook.0` `show`; `L06`: `MB`; `L07`: `1D`; `L08`: `2D`, `5 bậc tự do`; `L09`: `DWA`, `CPU`; `L10`: `Pure Pursuit`, `e_lat`; `L11`: `lidar`, `px`.
3. **Cụm `"càng "` mơ hồ** (6 chỗ): `L03` `prereq.0`, `L04` `intuition.0`, `L06` `sym.0`, `L08` `intuition.title`, `L10` `lookahead.1`, `L13` `stage5.1`.

---

## 3. Chi tiết MUST / P1 / P8 / P9 / `covers:` từng bài (`L00..L13`)

| Bài | Thời lượng ước | `covers:` | `P1` | `P8` | `P9` | `MUST` | Chi tiết lỗi chính |
|---|---|---:|:---:|:---:|:---:|---:|---|
| `L00` | **~8.60m** (<9m) | **FAIL** (obj 3 → `check`, phải là `sym`) | 1 | 2 | 2 | **1** | **MUST**: `covers` obj 3. **SHOULD**: Thời lượng <9p; `dict(...)` ma; `check.0` `introduces: [geq]` vs `\le` |
| `L01` | ~11.53m | PASS nhẹ | 0 | 2 | 2 | **1** | **MUST**: `practice.0` `v=...s omega=...s` thiếu `m/` và `rad/` |
| `L02` | ~9.33m | PASS | 0 | 2 | 2 | **0** | **SHOULD**: `dict(...)` ma; `encoder`/`lidar`/`con quay hồi chuyển` |
| `L03` | ~11.18m | **FAIL** (obj 2 → `check`) | 0 | 2 | 1 | **1** | **MUST**: `covers` obj 2. **SHOULD**: `de.md` thiếu làm tròn; `càng `; thân bài thiếu 2 mức quy mô |
| `L04` | ~11.59m | **FAIL** (obj 3 → `check`) | 0 | 2 | 2 | **1** | **MUST**: `covers` obj 3. **SHOULD**: `set`/`in` vs `dict`; `"càng "` |
| `L05` | ~12.02m | PASS | 0 | 2 | 2 | **0** | **SHOULD**: `(EKF)` ở `hook.0`, `\operatorname{diag}`, `dict(...)` |
| `L06` | ~10.35m | **FAIL** (obj 3 → `check`) | 1 | 2 | 2 | **1** | **MUST**: `covers` obj 3. **SHOULD**: `MB`; `"càng "` |
| `L07` | ~10.37m | PASS | 0 | **0** | 2 | **2** | **MUST 1 (SAI TOÁN)**: 4 cạnh (`-0.075`) vs 5 cạnh có cạnh đóng vòng (`-0.06`, nghiệm `[0.94, 1.88, 2.82, 3.76]`). **MUST 2 (SPOILER `de.md`)**: `de.md` ghi sẵn `-0.3 m` và `-0.075 m` |
| `L08` | ~10.05m | **FAIL** (obj 2 → `intuition`, phải là `sym`) | 0 | 1 | 2 | **1** | **MUST**: `covers` obj 2. **SHOULD**: `de.md` thiếu `:.0e`; `"càng "` |
| `L09` | ~10.44m | PASS | 0 | **0** | 2 | **2** | **MUST 1 (`de.md` KHÔNG TỰ ĐỦ)**: thiếu công thức lăn 1 bước, `head`, `clr`, chuẩn hoá tốc độ, làm tròn 3 chữ số. **MUST 2**: `practice.0` dư ngoặc `best=...)` |
| `L10` | ~11.37m | PASS | 0 | 2 | 2 | **0** | **SHOULD**: `dict(...)`, `Pure Pursuit`, `e_lat`, `"càng "` |
| `L11` | ~10.12m | PASS | 0 | 1 | 2 | **0** | **SHOULD**: `de.md` thiếu `:.0f`; `fx`, `cx`, `lidar`, `px` |
| `L12` | ~10.82m | **FAIL** (obj 2→`check`, obj 3→`practice` thay vì `pitfalls`) | 1 | 2 | 2 | **1** | **MUST**: `covers` obj 2 & obj 3 |
| `L13` | ~17.04m | **FAIL** (obj 3 → `stage5` thay vì `quiz`) | 0 | **0** | 2 | **3** | **MUST 1 (SAI DỮ KIỆN)**: `2004->2007` & `60 dặm` không có trong bài/`sources_L13.md`. **MUST 2 (SAI CÔNG THỨC)**: `stop_ratio = (35/25)^2 = 1.96x` bỏ qua phản ứng (bài tính `33.7/17.8 = 1.89x`). **MUST 3**: `covers` obj 3 |
