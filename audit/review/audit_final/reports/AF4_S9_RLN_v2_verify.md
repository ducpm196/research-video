# Báo cáo kiểm định độc lập AF4 v2 — Stage 9 Khoá `RLN` (`L00–L13`, 14 bài)

**Kết luận tổng thể: `NO-GO`**

So với vòng AF4 v1 (`audit/review/audit_final/reports/AF4_S9_RLN_verify.md`), bản sửa ngày `2026-11-20` đã khắc phục triệt để **3 lỗi lớn**:
1. **0/14 bài còn lộ code/đáp án trước `pause: 30`** (`practice#0` giao đề + khuôn stdout + `bash labs/cham.sh`, rồi `pause: 30`, sau đó mới hiện `mong_doi.txt`, bảng đọc mã và `loi_giai.py`).
2. **14/14 `labs/rln/L*/de.md`** đã có mục `Định dạng đầu ra (1 dòng):` và bỏ được `off-policy`/`on-policy` khỏi `L05/de.md`.
3. **14/14 đạt `P9 = 2`** (đủ `Hai mức quy mô:` trong `recap` cả 14/14 bài và trong thân bài ở `L05, L07, L10`), `audit/layout_RLN.tsv` đã quét lại sau `preview.html` (**0 dòng lỗi bố cục**), `screen_code` (**28/28 PASS**), `verify_rln.py` (**94/94 PASS**), `lv.py lint` (**14/14 PASS**, `0 FAIL, 0 WARN`).

Tuy nhiên, khoá `RLN` **vẫn `NO-GO`** vì còn **4 nhóm vấn đề `MUST` chưa xử lý xong**:
1. **`P8` trùng số liệu thân bài (14/14)** và `de.md` thiếu tự đứng được (`L03, L04, L05, L07`): **12/14 bài** (`L00–L09, L11, L13`) dùng nguyên si số liệu và đáp số đã tính trên màn hình trong bài giảng; **2/14 bài** (`L10, L12`) trùng một phần (`prob/loss` ở `L10`, `w10=1024` ở `L12`).
2. **`covers:` E51 trỏ sai cảnh dạy ở 8/14 bài (`L00, L02, L03, L04, L06, L11, L12, L13`)** (`lv.py lint` không kiểm ngữ nghĩa cảnh nên lọt).
3. **`P1` chưa sạch (0/14 đạt `P1 = 2`)**:
   - **14/14 bảng đọc mã `practice`** vẫn còn dòng boilerplate thừa (`{k: v} / dict(...)`, `d[k]` hoặc `{a, b} / set() / .add()`, `<=` không có trong `loi_giai.py`), và **6 bài thiếu token thật** (`L03` thiếu `k, eps = 10, 0.1`; `L04, L07, L12` thiếu danh sách `[...]`; `L07` thiếu generator `(bt for x in xs)`; `L09` thiếu tham số mặc định `e=0.2`; `L13` thiếu dấu gạch dưới `200_000_000`).
   - **Thuật ngữ/ký hiệu chưa giảng trong thân bài & `de.md`**: nổi bật là **`L10 check#0`** chèn `K = 4`, `β`, `(KL)`, `π_ref` (viết thô ngoài `$...$`) **trước** khi bài giảng `β` (`penalty#0`) và `K` (`pitfalls#2`), trong khi `KL` và `π_ref` chưa từng xuất hiện trong `L10`; **`L07 check#0`** dùng `V(s)` dù `L07` chỉ `requires: [L00]` (chưa học `L01`); **`L06`** dùng `DQN`, **`L08`** dùng `Actor–Critic`, **`L12`** dùng `ESS`, **`L13`** dùng `60 Hz`/`1 GPU`/`Atari` mà chưa mở nghĩa; **`L01 recap#1`** dùng `O(n³)`.
4. **MP4/SRT/ASR chưa dựng lại (`14/14 STALE`)**: toàn bộ `out/RLN/L00..L13/build_report.json` là bản dựng cũ, lệch `spec_sha256` so với YAML mới.

## 1. Tổng hợp cổng kỹ thuật & trạng thái dựng

| Hạng mục | Kết quả | Chi tiết quan sát |
|---|---|---|
| `tools/lv.py lint` (`L00..L13`) | **14/14 PASS** | `0 FAIL, 0 WARN`; toàn bộ `checks:` và KaTeX parse PASS |
| Thời lượng ước tính (`words / 150` + `pause`) | **14/14 ≥ 9 phút** | Nhỏ nhất `L08`: `11,81p`; lớn nhất `L13`: `18,42p` |
| `audit/rln/verify_rln.py` | **94/94 PASS** | Đối chiếu độc lập `L00–L13` |
| `labs/rln/L00..L13/loi_giai.py` vs `mong_doi.txt` | **14/14 MATCH** | Khớp stdout 100% |
| `audit/review/screen_code/rln.yaml` | **28/28 PASS** | `PASS 28 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0` |
| `audit/layout_RLN.tsv` | **0 dòng (PASS)** | `0` khung lỗi bố cục |
| Câu chứa `"càng "` (`show`/`say`) | **14/14 ĐẠT** | Đều đơn điệu rõ chiều, đúng ngữ cảnh |
| `curriculum/rln.yaml` ↔ YAML | **14/14 khớp nội dung** | `status: planned` |
| `out/RLN/L*/build_report.json` & `.mp4` | **14/14 STALE** | Chờ rebuild toàn khoá |

## 2. Bảng tổng hợp `L00–L13` (`MUST` / `P1` / `P8` / `P9`)

| Bài | Phút | `lint` | `covers:` | `P1` | `P8` | `P9` | `MUST` | Lỗi `MUST` chính còn lại |
|---|---|---:|---|---:|---:|---:|---:|---|
| `L00` | 14,8 / 15,7 | PASS | **FAIL** (obj 1, 4) | **1** | **1** | **2** | 2 | `covers` obj 1 (`concept`→`intuition`+`sym`), obj 4 (`check`→`quiz`+`pitfalls`); `de.md` trùng số (`0.9`, `[0,0,10]`); `practice` thừa `dict` |
| `L01` | 15,1 / 15,9 | PASS | PASS | **1** | **1** | **2** | 1 | `de.md` trùng số (`V_A=5.263`); `recap#1` có `O(n³)` chưa giảng; `practice` thừa `dict` |
| `L02` | 15,0 / 15,8 | PASS | **FAIL** (obj 3, 4) | **1** | **1** | **2** | 2 | `covers` obj 3 (`check`→`formula`+`quiz`), obj 4 (`check`→`pitfalls`); `de.md` trùng số (`66`, `688`) & chưa chú thích `eps, gamma`; `practice` thừa `set(), <=` |
| `L03` | 14,7 / 15,5 | PASS | **FAIL** (obj 2, 4) | **0** | **1** | **2** | 3 | `covers` obj 2 (`example`→`prereq`+`pitfalls`), obj 4 (`check`→`pitfalls`+`quiz`); `practice` thiếu `k, eps = 10, 0.1` + thừa `dict`; `de.md` thiếu công thức cộng dồn & trùng số |
| `L04` | 13,6 / 14,5 | PASS | **FAIL** (obj 4) | **1** | **1** | **2** | 2 | `covers` obj 4 (`check`→`quiz`+`pitfalls`; obj 2 nên `formula`+`quiz`); `practice` thiếu `[...]` + thừa `dict`; `de.md` thiếu công thức `TD(0)` & trùng số |
| `L05` | 12,6 / 13,4 | PASS | PASS | **1** | **1** | **2** | 1 | `de.md` trùng số (`2.2`, `1.8`) & thiếu công thức cập nhật tường minh; `practice` thừa `dict` |
| `L06` | 14,5 / 15,4 | PASS | **FAIL** (obj 3) | **0** | **1** | **2** | 3 | `covers` obj 3 (`example`→`formula`+`pitfalls`); `de.md` & `practice#0` dùng `DQN`, `Q_target` chưa mở nghĩa + trùng `10.9`; `practice` thừa `dict` |
| `L07` | 15,3 / 16,2 | PASS | PASS | **0** | **1** | **2** | 2 | `check#0` dùng `V(s)` dù chỉ `requires: [L00]`; `de.md` viết `dấu gradient`, thiếu công thức mẫu & quy ước phương sai chia `N` (`len`), trùng số (`-0.50`, `30.25`); `practice` thiếu `[...]`, generator, thừa `dict` |
| `L08` | 11,8 / 12,7 | PASS | PASS | **0** | **1** | **2** | 2 | `de.md` dùng `Actor–Critic` chưa có trong YAML + trùng số (`1.5`); `practice` thừa `dict` |
| `L09` | 14,9 / 15,7 | PASS | PASS | **0** | **1** | **2** | 2 | `practice` thiếu tham số mặc định `e=0.2` trong `lambda` + thừa `dict`; `de.md` trùng số (`2.4`, `-1.6`) |
| `L10` | 14,5 / 15,4 | PASS | PASS | **0** | **1** | **2** | 2 | `check#0` dùng `K, β, KL, π_ref` trước khi giảng `β`/`K` và không giải thích `KL`, `π_ref`; `de.md` & `practice#0` dùng `KL`, `pi_ref`, trùng `0.731`/`0.313`; `practice` thừa `dict` |
| `L11` | 11,9 / 12,8 | PASS | **FAIL** (obj 2, 4) | **1** | **1** | **2** | 2 | `covers` obj 2 (`check`→`example`), obj 4 (`check`→`pitfalls`+`quiz`); `de.md` trùng số (`100`, `200`); `practice` thừa `set(), <=` |
| `L12` | 13,4 / 14,2 | PASS | **FAIL** (obj 3) | **0** | **1** | **2** | 3 | `covers` obj 3 (`check`→`example`+`quiz`); `de.md` & `practice#0` dùng `ESS` chưa giảng nghĩa + trùng `w10=1024`; `practice` thiếu `[...]` + thừa `dict` |
| `L13` | 18,4 / 19,3 | PASS | **FAIL** (obj 3) | **0** | **1** | **2** | 3 | `covers` obj 3 (`stage5`→`quiz`; obj 2 nên gồm `stage1`); `recap#1`/`practice#0`/`de.md` dùng `Hz`, `GPU`, `Atari`, `skiing_norm` chưa mở nghĩa; `practice` thiếu `_` trong `200_000_000` + thừa `dict`; `de.md` trùng `38.6`, `108.3%` |

## 3. Chi tiết các khoảng trống cần sửa để chuyển sang `GO`
1. Sửa bảng đọc mã `practice` (`ast_p1.py` + bổ sung token thật cho `L03, L04, L07, L09, L12, L13`).
2. Sửa thuật ngữ/ký hiệu chưa giảng trong thân bài & `de.md` (`L01, L06, L07, L08, L10, L12, L13`).
3. Sửa `P8` — đổi bộ số lab tách khỏi ví dụ thân bài & bổ sung công thức tường minh ở `L03, L04, L05, L07`.
4. Sửa `covers:` ở 8/14 bài (`L00, L02, L03, L04, L06, L11, L12, L13`).
5. Cập nhật `screen_code/rln.yaml` + `layout_scan` + `curriculum/rln.yaml` + dựng lại video.
