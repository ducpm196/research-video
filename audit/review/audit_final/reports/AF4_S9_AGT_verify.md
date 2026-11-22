# Báo cáo kiểm định độc lập WP-AF4-5 Stage 9 — Khoá AGT (`L00–L12`, 13/13 bài)

**Kết luận tổng thể: `NO-GO`** (chặn bởi nhiều lỗi `MUST` ở cảnh `practice` [lộ `loi_giai.py` trước `pause`], `de.md` [thiếu định dạng đầu ra/đầu vào và thuật ngữ tiếng Anh chưa chú thích], `practice#0` [thiếu hoặc lệch với `loi_giai.py`], lab `L02`/`L04` đi đường tắt, và thiếu `Hai mức quy mô` trong `recap`).

---

## 1. Tóm tắt số đo toàn khoá (`OBSERVED`)

| Hạng mục | Kết quả đo | Ghi chú |
|---|---|---|
| Số bài đã đọc & kiểm | **13/13** (`L00–L12`) | Khớp `curriculum/agt.yaml`, `lessons/agt/L*.yaml`, `labs/AGT/L*/` |
| `audit/agt/verify_agt.py` | **15 PASS · 0 FAIL** | Tự chạy kiểm độc lập (Monte Carlo, JSON thật, Bellman–Ford, tổ hợp, nguồn `L12`) |
| `tools/lv.py lint` | **13/13 PASS** (`0 FAIL, 0 WARN`) | Tổng **148** biểu thức `checks` trong 13 YAML (cộng `verify_agt.py` = khớp 100%) |
| `build_report.json` (`STALE`) | **0/13 STALE** | Toàn bộ 13 bài dựng `2026-11-20T00:06..00:28Z`, `spec_sha256 == lv.spec_digest`, 1 giọng `vi-VN-NamMinhNeural` (`edge` + `edge?` cùng họ `ms`) |
| `L*.srt == say` | **13/13 khớp 100%** | Khớp từng ký tự khi ghép các đoạn phụ đề của từng bài |
| `asr_report.md` | **0 thiếu audio, 0 chưa xem xét** | Tổng **14** câu gắn cờ trong `asr_reviewed` ở `L01,L02,L03,L04(3),L05,L06(4),L08,L09,L11` đều ghi `NOT_VERIFIED bằng tai người` |
| `labs/AGT/L*/loi_giai.py` vs `mong_doi.txt` | **13/13 chạy khớp đầu ra** | Nhưng về sư phạm: **13/13 `de.md` thiếu định dạng đầu ra**, `L04` & `L02` **đi đường tắt** |
| `audit/layout_AGT.tsv` | **0 dòng lỗi (`b'\r\n'`) — STALE** | Tệp ghi lúc `2026-11-19T02:44:56Z` (trước sửa YAML `08:19Z` và dựng `2026-11-20`); kiểm bằng mắt **32 PNG** bản dựng mới nhất: **0 lỗi đè chữ/tràn khung** |
| **Tỷ lệ `P1`** (`practice#0` + `de.md` đủ thuật ngữ/ký hiệu) | **0/13 (0%) đạt mức 2** | 5 bài mức 1 (`L00,L03,L06,L07,L11`), 8 bài mức 0 (`L01,L02,L04,L05,L08,L09,L10,L12`) |
| **Tỷ lệ `P8`** (không lộ `loi_giai` trước `pause` & lab thực chất) | **1/13 (7,7%) không lộ trước `pause` (`L04`); 0/13 (0%) sạch trọn vẹn** | **12/13 bài (`L00–L03, L05–L12`) lộ nguyên văn `loi_giai.py` ở `practice#1` và `mong_doi.txt` ở `practice#2` trước `pause: 30` ở `practice#3`**; riêng `L04` không lộ nhưng lab `L04` hardcode `matched_quote=1` |
| **Tỷ lệ `P9`** (thân bài + `recap` `Hai mức quy mô`, SVG) | **0/13 (0%) đạt trọn cả thân bài & `recap`** | Thân bài có ≥ 2 mức quy mô + đánh đổi: **9/13 (69,2%)** (`L00,L02,L03,L05,L06,L07,L08,L11,L12`); `recap` `Hai mức quy mô`: **0/13 (0%)**; SVG sạch: **13/13 (100%)** |

---

## 2. Kiểm tra riêng các quy tắc sư phạm cốt lõi

1. **Lỗi lộ `loi_giai` ở `practice#1` trước `pause` (`P8` — `MUST`)**:
   - Ở **12/13 bài** (`L00, L01, L02, L03, L05, L06, L07, L08, L09, L10, L11, L12`), cảnh `practice` có cấu trúc: `practice#0` (bảng ký hiệu) → `practice#1` (`Cài đặt kiểm chứng AGT:Lxx bằng Python` in nguyên văn toàn bộ `loi_giai.py`) → `practice#2` (`Đầu ra chạy thật` in nguyên văn `mong_doi.txt`) → `practice#3` (`pause: 30`, *"Hãy bấm tạm dừng và tự làm trước"*) → `practice#4` (`Kết quả mong đợi`).
   - Như vậy `practice#1` và `practice#2` đã lộ trọn lời giải và đáp án trước khi học viên dừng video tự làm.
   - Riêng `L04` chỉ có 2 step (`practice#0` hướng dẫn + `pause: 30` → `practice#1` kết quả mong đợi) nên không lộ trước `pause`, nhưng lại thiếu bảng giải thích ký hiệu và `loi_giai.py` đi đường tắt.

2. **Thuật ngữ/viết tắt tiếng Anh chưa chú thích ở `practice#0` và `de.md` (`P1` — `MUST`)**:
   - **13/13 `de.md`** không ghi đặc tả chuỗi đầu ra (`mong_doi.txt`) nên người học chỉ đọc `de.md` không thể viết đúng `print(...)` để qua `cham.sh`.
   - Thuật ngữ/viết tắt tiếng Anh chưa chú thích trong thân bài hoặc `de.md`: `vs` (`L00,L06,L07,L11`), `amt` (`L01`), **`DAG`** (`L02` — không hề có trong bài học), `system` / `k` (`L03`), **`TPR`, `FPR`, `base`** (`L05` — không hề có trong bài học), **`cache`**, **`token`** (`L08`), **`prompt injection`** (`L09`), **`trace`**, **`Pareto`** (`L10` — `Pareto` không hề xuất hiện trong bài), **`Workflow`** (`L11`), **`benchmark`**, **`SWE-bench Verified`** (`L12`).
   - `practice#0` ở `L00–L03, L05–L12` dùng template tĩnh với tên giữ chỗ `val`, `ham`, `ds`, `xs`, `f(x)` không khớp toán tử/hàm dùng trong `loi_giai.py` (thiếu `**`, `//`, `isinstance`, `.isdigit()`, `enumerate`, `*c`, `range`, `dict`, `.get()`, `.values()`, `round`); `L04` bỏ trống hoàn toàn bước `practice#0`.

3. **Câu `"càng ..."` và lời đọc tiếng Việt (`say`)**:
   - Toàn khoá chỉ có 3 lượt dùng `"càng"` ở 2 bài: `L05` `pitfalls#1` (*"Bài càng khó, bộ kiểm chứng càng phải chặt"*) và `L08` `hook#0` (*"lịch sử thì ngày càng dài"*), `recap#1` (*"chạy càng lâu càng gần tỉ lệ với bình phương số bước"*). Cả 3 đều đúng logic/toán học (Bayes theo tỉ lệ nền; tổng $nS + G\frac{n(n-1)}{2}$ tiệm cận $\frac{G}{2}n^2$).
   - Lời đọc `say` giữ nguyên tắc toàn tiếng Việt (tên kỹ thuật tiếng Anh chỉ đặt ở `show`; `L05` dùng `Bayes` được từ điển đọc `Bay-ét`). Tuy nhiên `asr_reviewed` còn **14 câu `NOT_VERIFIED bằng tai người`** (đặc biệt `L06` chữ `"Đ"` bị ASR nghe thành `đe/đê/đây`; `L04` `S 1/S 2` nghe thành `F1/F2`; `L08` `S + G*i` nghe thành `S + Ve*Y`; `L05` `Bayes` nghe thành `bay S`).

4. **Khớp `curriculum ↔ YAML ↔ de.md ↔ loi_giai.py`, `covers:`, và `recap` `Hai mức quy mô` (`P9`)**:
   - Mọi số liệu thân bài (`checks` & `verify_agt.py`) khớp hoàn toàn giữa `curriculum/agt.yaml`, `lessons/agt/*.yaml`, và `audit/agt/sources_L12.md` (`L12`).
   - **Đi đường tắt ở lab**: `L04/loi_giai.py` in cứng `matched_quote=1` mà không kiểm chuỗi trích dẫn thật; `L02/loi_giai.py` cộng cứng `2 + max(3, 4) + 2 + 1` mà không dựng cấu trúc/duyệt DAG; `L01/loi_giai.py` đổi bộ 4 lời gọi khác `L01.yaml`/`curriculum` và dùng `isinstance(amt, int)` (không loại `bool` như `verify_agt.py` L01a).
   - **`covers:`**: cả 13 bài gán máy móc `[1: example, 2: check, 3: practice]` (`L12`: `[1: stage1, 2: stage2, 3: practice]`), lệch cảnh dạy thật của mục tiêu (vd: `objective: 3` thường nằm ở `pitfalls`/`quiz`, còn `practice` chỉ là một phép tính đơn).
   - **`recap` `Hai mức quy mô`**: **0/13 bài** có bảng/mục đối chiếu `Hai mức quy mô` ở `recap`.

---

## 3. Báo cáo chi tiết từng bài (`L00–L12`)

### `L00` — `L00_vong_lap_tac_tu.yaml` (`sha16: 5eff826e25677d62`, 11.1 phút, 92 khung, 11 checks)
- **Chỉ số**: `P1 = 1` · `P8 = 0` · `P9 = 1` (thân bài 2, `recap` thiếu `Hai mức quy mô`)
- **MUST**:
  - `[P8]` `practice#1` (`00081.png`) lộ toàn bộ mã `loi_giai.py` (`p95 = 0.95 ** 20 * 100 ...`) và `practice#2` (`00082.png`) lộ đầu ra trước `pause: 30` ở `practice#3`.
  - `[Lab]` `de.md` không nêu định dạng đầu ra `task20_at95=...% task20_at99=...%`.
- **SHOULD**:
  - `[P1]` `de.md` dùng `vs` không chú thích; `practice#0` (`00080.png`) thiếu giải thích toán tử luỹ thừa `**`.
  - `[P9]` `recap` thiếu mục `Hai mức quy mô` (dù thân bài có 10 vs 20 bước và 1/2/3 lần thử).
  - `[covers]` `objective: 1` (vòng lặp, điều kiện dừng) trỏ `example` thay vì `sym`; `objective: 3` (thử lại) trỏ `practice` (lab không có thử lại).
- **INFO**: `say == srt` khớp 100%; `asr_report`: 0 gắn cờ; 2 SVG (`00024.png`, `00028.png`) & `recap` (`00087.png`) hiển thị sạch.
- **PNG đã xem**: `out/AGT/L00/frames/00024.png`, `00028.png`, `00080.png`, `00081.png`, `00087.png`.

### `L01` — `L01_goi_cong_cu.yaml` (`sha16: 0b1024142696eb1f`, 9.3 phút, 85 khung, 9 checks)
- **Chỉ số**: `P1 = 0` · `P8 = 0` · `P9 = 0` (thân bài 0, `recap` thiếu `Hai mức quy mô`)
- **MUST**:
  - `[P8]` `practice#1` (`00073.png`) lộ toàn bộ `loi_giai.py` và `practice#2` lộ đầu ra trước `pause: 30` ở `practice#3`.
  - `[Lab/P1]` `de.md` dùng viết tắt `amt` chưa chú thích, không liệt kê 4 lời gọi đầu vào `[(500_000, '0123456789'), (-50, ...), (100, '123'), (20_000_000, ...)]`, và thiếu định dạng đầu ra `total_calls=... valid_count=... idx=...`.
  - `[Lab]` 4 lời gọi trong `loi_giai.py` khác với 4 lời gọi của `curriculum` & `L01.yaml` `example` (`(-200)`, `'1000'`, `'98765'`, `ghi_chu='x'`), đồng thời `isinstance(amt, int)` không loại `bool` như `verify_agt.py` L01a.
- **SHOULD**:
  - `[P1]` `practice#0` (`00072.png`) liệt kê thừa `sum / len / max / min` nhưng thiếu `isinstance`, `.isdigit()`, `enumerate`, `*c`.
  - `[P9]` Cả thân bài lẫn `recap` chưa đối chiếu số liệu ở ≥ 2 mức quy mô.
  - `[covers]` `objective: 1` (viết lược đồ) trỏ `example` thay vì `sym`; `objective: 3` (thử lại an toàn) trỏ `practice` (lab không có thử lại/khoá luỹ đẳng).
- **INFO**: `say == srt` khớp 100%; `asr_reviewed`: 1 câu (`chuỗi/chủ`, `NOT_VERIFIED` bằng tai); SVG `00018.png` sạch.
- **PNG đã xem**: `out/AGT/L01/frames/00018.png`, `00072.png`, `00073.png`.

### `L02` — `L02_lap_ke_hoach.yaml` (`sha16: 8ba2b3c2983ea53c`, 9.2 phút, 85 khung, 10 checks)
- **Chỉ số**: `P1 = 0` · `P8 = 0` · `P9 = 1` (thân bài 2, `recap` thiếu `Hai mức quy mô`)
- **MUST**:
  - `[P8]` `practice#1` lộ nguyên văn `loi_giai.py` trước `pause: 30` ở `practice#3`.
  - `[P1/Lab]` `de.md` dùng chữ viết tắt tiếng Anh **`DAG`** không hề được định nghĩa trong thân bài L02 hay trong đề; thiếu cạnh phụ thuộc của 5 bước và thiếu định dạng đầu ra `sequential=...s critical_path=...s saved=...s`.
  - `[Lab]` `loi_giai.py` đi đường tắt: viết thẳng `2 + max(3, 4) + 2 + 1` thay vì biểu diễn đồ thị phụ thuộc và tính thời điểm hoàn thành theo phụ thuộc.
- **SHOULD**:
  - `[P1]` `practice#0` (`00073.png`) liệt kê thừa `f"{val:.3f}"`, `sum / len / min` không dùng trong `loi_giai.py`.
  - `[P9]` `recap` thiếu `Hai mức quy mô`; `covers` trỏ `objective: 3` (so sánh lập kế hoạch trước vs từng bước) vào `practice` (không dạy phần này).
- **INFO**: `say == srt` khớp 100%; `asr_reviewed`: 1 câu (`của A`, `NOT_VERIFIED` bằng tai); SVG `00018.png` sạch.
- **PNG đã xem**: `out/AGT/L02/frames/00018.png`, `00073.png`.

### `L03` — `L03_bo_nho.yaml` (`sha16: 5a9a4633da2f3f30`, 9.3 phút, 78 khung, 8 checks)
- **Chỉ số**: `P1 = 1` · `P8 = 0` · `P9 = 1` (thân bài 2, `recap` thiếu `Hai mức quy mô`)
- **MUST**:
  - `[P8]` `practice#1` lộ nguyên văn `loi_giai.py` trước `pause: 30` ở `practice#3`.
  - `[Lab]` `de.md` thiếu định dạng đầu ra `max_turns=... full_after=...`.
- **SHOULD**:
  - `[P1]` `de.md` dùng `system` và `k` (`128k`, `8k`, `2k`) chưa chú thích; `practice#0` (`00066.png`) thiếu phép chia nguyên `//` và thừa `f"{val:.3f}"`.
  - `[P9]` `recap` thiếu `Hai mức quy mô` (thân bài đã có 128k vs 32k và cắt gọn 30k vs 2k); `covers` trỏ `objective: 2, 3` sai cảnh (`sym`, `pitfalls`).
- **INFO**: `say == srt` khớp 100%; `asr_reviewed`: 1 câu (`Chia/Chìa`, `NOT_VERIFIED` bằng tai); SVG `00020.png` sạch.
- **PNG đã xem**: `out/AGT/L03/frames/00020.png`, `00066.png`.

### `L04` — `L04_tim_thong_tin.yaml` (`sha16: 11f6cd6f874b7274`, 10.1 phút, 94 khung, 12 checks)
- **Chỉ số**: `P1 = 0` · `P8 = 1` (không lộ trước `pause`, nhưng lab đi đường tắt) · `P9 = 1` (thân bài 1, `recap` 0)
- **MUST**:
  - `[Lab]` `loi_giai.py` **đi đường tắt**: tiêu đề `de.md` là *"Truy vấn lặp & kiểm trích dẫn tự động"*, nhưng `loi_giai.py` chỉ tính độ phủ và **in cứng chuỗi `matched_quote=1`**, không hề thực hiện kiểm trích dẫn chuỗi trong nguồn! `de.md` cũng không cung cấp dữ liệu câu nguồn/câu trích và thiếu định dạng đầu ra.
  - `[P1]` Cảnh `practice` thiếu hoàn toàn `practice#0` (bảng giải thích ký hiệu mã Python), nhảy thẳng vào bảng hướng dẫn làm bài (`00085.png`).
- **SHOULD**:
  - `[P9]` Thân bài chưa có 2 mức quy mô (chỉ có 10 văn bản và ngưỡng dừng); `recap` thiếu `Hai mức quy mô`; `covers` trỏ `objective: 2, 3` chưa khớp nội dung cảnh.
- **INFO**: `say == srt` khớp 100%; `asr_reviewed`: 3 câu (`ôn/ông`, `S 1/F1`, `S 2/F2`, `NOT_VERIFIED` bằng tai); SVG `00017.png` & bảng `00009.png` sạch.
- **PNG đã xem**: `out/AGT/L04/frames/00009.png`, `00017.png`, `00085.png`.

### `L05` — `L05_tu_kiem_tra.yaml` (`sha16: c245835da9134bbf`, 10.3 phút, 92 khung, 12 checks)
- **Chỉ số**: `P1 = 0` · `P8 = 0` · `P9 = 1` (thân bài 2, `recap` thiếu `Hai mức quy mô`)
- **MUST**:
  - `[P8]` `practice#1` lộ nguyên văn `loi_giai.py` trước `pause: 30` ở `practice#3`.
  - `[P1/Lab]` `de.md` (và bảng `practice#3`) dùng 3 thuật ngữ/viết tắt tiếng Anh **`TPR`, `FPR`, `base`** không hề xuất hiện trong thân bài; thiếu định dạng đầu ra `accepted_true_pct=...%`.
- **SHOULD**:
  - `[P1]` `practice#0` (`00080.png`) có `f"{val:.3f}"` trong khi bài dùng `:.1f`.
  - `[P9]` `recap` thiếu `Hai mức quy mô`; `covers` trỏ `objective: 2, 3` vào `check` và `practice` trong khi bài giảng nằm ở `sym`/`pitfalls`/`quiz`.
- **INFO**: Câu `"Bài càng khó, bộ kiểm chứng càng phải chặt"` ở `pitfalls#1` chuẩn toán học; `say == srt` khớp 100%; `asr_reviewed`: 1 câu (`Bayes→Bay-ét`, `NOT_VERIFIED` bằng tai); SVG `00025.png` & bảng `00004.png` sạch.
- **PNG đã xem**: `out/AGT/L05/frames/00004.png`, `00025.png`, `00080.png`.

### `L06` — `L06_nhieu_tac_tu.yaml` (`sha16: 967491eaee8b8d99`, 9.0 phút, 80 khung, 11 checks)
- **Chỉ số**: `P1 = 1` · `P8 = 0` · `P9 = 1` (thân bài 2, `recap` thiếu `Hai mức quy mô`)
- **MUST**:
  - `[P8]` `practice#1` lộ nguyên văn `loi_giai.py` trước `pause: 30` ở `practice#3`.
  - `[Lab]` `de.md` thiếu định dạng đầu ra `mesh_channels=... hub_channels=...`.
- **SHOULD**:
  - `[P1]` `de.md` dùng `vs` chưa chú thích; `practice#0` (`00067.png`) ghi thừa `f"{val:.3f}"` không dùng trong `loi_giai.py`.
  - `[P9]` `recap` thiếu `Hai mức quy mô` (thân bài đã có 3/6/10 tác tử); `covers` trỏ `objective: 3` (mất mát chuyển giao) vào `practice` (chỉ đếm kênh).
- **INFO**: `say == srt` khớp 100%; `asr_reviewed`: 4 câu (`Đ` nghe thành `đe/đê/đây`, `NOT_VERIFIED` bằng tai); SVG `00017.png` sạch.
- **PNG đã xem**: `out/AGT/L06/frames/00017.png`, `00067.png`.

### `L07` — `L07_danh_gia_tac_tu.yaml` (`sha16: 01dc6d5edf1df882`, 10.2 phút, 86 khung, 13 checks)
- **Chỉ số**: `P1 = 1` · `P8 = 0` · `P9 = 1` (thân bài 2, `recap` thiếu `Hai mức quy mô`)
- **MUST**:
  - `[P8]` `practice#1` lộ nguyên văn `loi_giai.py` trước `pause: 30` ở `practice#3`.
  - `[Lab]` `de.md` thiếu định dạng đầu ra `pass_at_3=...% pass_pow_3=...%`.
- **SHOULD**:
  - `[P1]` `de.md` dùng `vs` không chú thích; `practice#0` (`00074.png`) thiếu toán tử `**` và dùng `:.3f` thay cho `:.1f`.
  - `[P9]` `recap` thiếu `Hai mức quy mô` (thân bài đã có $k=1..5$ và $n=100$ vs $400$); `covers` trỏ `objective: 3` vào `practice` (chỉ tính `pass@3`/`pass^3`).
- **INFO**: `say == srt` khớp 100%; `asr_report`: 0 gắn cờ; SVG `00020.png` sạch.
- **PNG đã xem**: `out/AGT/L07/frames/00020.png`, `00074.png`.

### `L08` — `L08_chi_phi_do_tre.yaml` (`sha16: 750fc54f824d07b8`, 9.8 phút, 85 khung, 11 checks)
- **Chỉ số**: `P1 = 0` · `P8 = 0` · `P9 = 1` (thân bài 2, `recap` thiếu `Hai mức quy mô`)
- **MUST**:
  - `[P8]` `practice#1` lộ nguyên văn `loi_giai.py` trước `pause: 30` ở `practice#3`.
  - `[P1/Lab]` `de.md` dùng tiếng Anh **`cache`**, **`token`** không giải thích đối chiếu với *"bộ nhớ đệm"*, *"từ tố"* của bài; thiếu định dạng đầu ra `final_ctx=... total_input=... mult=...x`.
- **SHOULD**:
  - `[P1]` `practice#0` (`00072.png`) dùng biến giả `ds`, `xs` và thiếu `range(...)`, chỉ số âm `[-1]`, `:.2f`.
  - `[P9]` `recap` thiếu `Hai mức quy mô` (thân bài có 10 vs 20 bước); `covers` trỏ `objective: 2, 3` sai cảnh (`example`, `pitfalls`).
- **INFO**: Các câu `"càng ..."` ở `hook#0` và `recap#1` chính xác toán học; `say == srt` khớp 100%; `asr_reviewed`: 1 câu (`i/Y`, `G/Ve`, `NOT_VERIFIED` bằng tai); SVG `00021.png` sạch.
- **PNG đã xem**: `out/AGT/L08/frames/00021.png`, `00072.png`.

### `L09` — `L09_an_toan_tac_tu.yaml` (`sha16: 1a1f05ad92c56d7f`, 9.5 phút, 86 khung, 8 checks)
- **Chỉ số**: `P1 = 0` · `P8 = 0` · `P9 = 0` (thân bài 1, `recap` 0)
- **MUST**:
  - `[P8]` `practice#1` lộ nguyên văn `loi_giai.py` trước `pause: 30` ở `practice#3`.
  - `[P1/Lab]` `de.md` (và `practice#3`) dùng cụm **`prompt injection`** chưa có trong bài; không nêu 4 tên hành động tiếng Anh (`read_doc`, `send_mail`, `transfer`, `drop_db`) và nhãn chính sách (`allow`, `confirm`, `deny`) mà `loi_giai.py` dùng, cũng thiếu định dạng đầu ra `auto_executed=... blocked=...`.
- **SHOULD**:
  - `[P1]` `practice#0` (`00074.png`) thiếu cú pháp từ điển `{k: v}` và `.get(...)`, lại ghi thừa `f"{val:.3f}"`.
  - `[P9]` Thân bài và `recap` chưa có số liệu ở ≥ 2 mức quy mô; `covers` trỏ `objective: 3` (tổ hợp quyền nguy hiểm) vào `practice` (không dạy tổ hợp 3 điều kiện).
- **INFO**: `say == srt` khớp 100%; `asr_reviewed`: 1 câu (`tác/tát`, `đọc/độc`, `NOT_VERIFIED` bằng tai); SVG `00023.png` sạch.
- **PNG đã xem**: `out/AGT/L09/frames/00023.png`, `00074.png`.

### `L10` — `L10_quan_sat_go_loi.yaml` (`sha16: 9d62579bc5e9888b`, 9.5 phút, 83 khung, 12 checks)
- **Chỉ số**: `P1 = 0` · `P8 = 0` · `P9 = 0` (thân bài 1, `recap` 0)
- **MUST**:
  - `[P8]` `practice#1` lộ nguyên văn `loi_giai.py` trước `pause: 30` ở `practice#3`.
  - `[P1/Lab]` `de.md` (và `practice#3`) dùng **`trace`** và **`Pareto`** — riêng **`Pareto`** hoàn toàn không được giảng hay nhắc tới ở bất kỳ đâu trong bài L10; `de.md` thiếu tên các nhóm lỗi/giá trị `(22, 15, 9, 4)` và định dạng đầu ra `top_cause_pct=...% total=...`.
- **SHOULD**:
  - `[P1]` `practice#0` (`00071.png`) thiếu từ điển `{...}` và `.values()`, ghi thừa `max / min / len` và `:.3f`.
  - `[P9]` Thân bài và `recap` chưa có 2 mức quy mô; `covers` trỏ `objective: 3` (phát lại) vào `practice` (chỉ tính `22/50`).
- **INFO**: `say == srt` khớp 100%; `asr_report`: 0 gắn cờ; 2 SVG (`00018.png`, `00022.png`) sạch.
- **PNG đã xem**: `out/AGT/L10/frames/00018.png`, `00022.png`, `00071.png`.

### `L11` — `L11_tong_hop.yaml` (`sha16: bccf2de7c06c3014`, 11.1 phút, 86 khung, 11 checks)
- **Chỉ số**: `P1 = 1` · `P8 = 0` · `P9 = 1` (thân bài 2, `recap` thiếu `Hai mức quy mô`)
- **MUST**:
  - `[P8]` `practice#1` lộ nguyên văn `loi_giai.py` trước `pause: 30` ở `practice#3`.
  - `[Lab]` `de.md` thiếu định dạng đầu ra `fixed_workflow=...% autonomous_agent=...%`.
- **SHOULD**:
  - `[P1]` `de.md` (và `practice#3`) dùng **`Workflow`** (tiếng Anh viết hoa) và `vs`; `practice#0` (`00073.png`) thiếu toán tử `**` và dùng `:.3f` thay cho `:.1f`.
  - `[P9]` `recap` thiếu `Hai mức quy mô`; `covers` trỏ `objective: 3` (giới hạn, điểm dừng, người giám sát) vào `practice` (chỉ tính `0.98^4` vs `0.95^6`).
- **INFO**: `say == srt` khớp 100%; `asr_reviewed`: 1 câu (`Bảng/Bản`, `NOT_VERIFIED` bằng tai); SVG `00019.png` sạch.
- **PNG đã xem**: `out/AGT/L11/frames/00019.png`, `00073.png`.

### `L12` — `L12_hanh_trinh_tac_tu_cong_cu.yaml` (`sha16: eab6826a1c7eb27b`, 17.3 phút, 137 khung, 24 checks)
- **Chỉ số**: `P1 = 0` · `P8 = 0` · `P9 = 1` (thân bài 2, `recap` thiếu `Hai mức quy mô`)
- **MUST**:
  - `[P8]` `practice#1` (`00120.png`) lộ nguyên văn `loi_giai.py` trước `pause: 30` ở `practice#3`.
  - `[P1/Lab]` `de.md` dùng **`benchmark`** và **`SWE-bench Verified`** chưa chú thích trong `de.md`, không nêu số `286` (hoặc cách làm tròn `45`), và thiếu định dạng đầu ra `full_old=... full_gain=...x verified_solved=...`.
- **SHOULD**:
  - `[P1]` `practice#0` (`00119.png`) thiếu `round(...)` và dùng `:.3f` thay cho `:.1f`.
  - `[P9]` `recap` thiếu `Hai mức quy mô` (thân bài hành trình đã có đủ 5 chặng quy mô + bài toán đội 40 lỗi); `covers` trỏ `objective: 1` chỉ tới `stage1` (thiếu `stage2..5`), `objective: 2` chỉ tới `stage2`, `objective: 3` tới `practice` (thực tế nằm ở `quiz`).
- **INFO**: Toàn bộ số liệu và trích dẫn khớp 100% `audit/agt/sources_L12.md` (`[RE23]`, `[TF23]`, `[GR23]`, `[SB24]`, `[SA24]`, `[SBV]`); `say == srt` khớp 100%; `asr_report`: 0 gắn cờ; 2 SVG (`00026.png`, `00030.png`), bảng `00005.png`, `recap` `00126.png` đều sạch.
- **PNG đã xem**: `out/AGT/L12/frames/00005.png`, `00026.png`, `00030.png`, `00119.png`, `00120.png`, `00126.png`.

---

## 4. Tổng hợp danh sách PNG đã xem (32 khung)

- `L00`: `00024.png`, `00028.png`, `00080.png`, `00081.png`, `00087.png`
- `L01`: `00018.png`, `00072.png`, `00073.png`
- `L02`: `00018.png`, `00073.png`
- `L03`: `00020.png`, `00066.png`
- `L04`: `00009.png`, `00017.png`, `00085.png`
- `L05`: `00004.png`, `00025.png`, `00080.png`
- `L06`: `00017.png`, `00067.png`
- `L07`: `00020.png`, `00074.png`
- `L08`: `00021.png`, `00072.png`
- `L09`: `00023.png`, `00074.png`
- `L10`: `00018.png`, `00022.png`, `00071.png`
- `L11`: `00019.png`, `00073.png`
- `L12`: `00005.png`, `00026.png`, `00030.png`, `00119.png`, `00120.png`, `00126.png`

---

## 5. Kết luận & điều kiện để chuyển sang `GO`

**Kết luận: `NO-GO`**

Để đạt **`GO`**, cần sửa các điểm chặn sau (sau đó chạy lại `layout_scan.py AGT`, dựng lại video bài sửa và kiểm tra lại):
1. **Sửa cảnh `practice` (tất cả 13 bài)**: gỡ `loi_giai.py` và đầu ra chạy thật ra khỏi vị trí trước `pause` (chỉ đặt hướng dẫn + `practice#0` giải thích đúng các ký hiệu Python thực dùng trước `pause: 30`; chỉ hiển thị `mong_doi.txt` sau `pause`), đồng thời bổ sung `practice#0` cho `L04`.
2. **Sửa `labs/AGT/L00..L12/de.md` & `loi_giai.py`**:
   - Ghi rõ đầu vào + định dạng dòng kết quả mong đợi ở mọi `de.md` để người học tự viết không cần nhìn lời giải.
   - Chú thích tiếng Việt hoặc thay thế mọi từ/viết tắt tiếng Anh chưa giảng (`DAG`, `TPR`, `FPR`, `base`, `Pareto`, `cache`, `token`, `amt`, `system`, `prompt injection`, `trace`, `Workflow`, `benchmark`, `vs`).
   - Sửa `L04/loi_giai.py` kiểm trích dẫn chuỗi thật trên dữ liệu nguồn (không hardcode `matched_quote=1`), sửa `L02/loi_giai.py` tính đường găng từ biểu diễn đồ thị phụ thuộc, và đồng bộ `L01/loi_giai.py` (loại `bool`, khớp dữ liệu bài).
3. **Bổ sung `Hai mức quy mô` vào `recap`** (và bổ sung 2 mức quy mô cho thân bài `L01, L04, L09, L10`), sửa `covers:` trỏ đúng cảnh dạy từng mục tiêu, và làm tươi `audit/layout_AGT.tsv`.