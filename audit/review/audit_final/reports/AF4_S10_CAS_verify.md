# Kiểm định độc lập Stage 10 — Khoá `CAS` (`L00–L11`, 12/12 bài)

**Kết luận tổng thể: `NO-GO`**

Khoá `CAS` có nền tảng nội dung thân bài, nguồn trích dẫn (`sources_L*.md`), kiểm chứng số học (`verify_cas.py` 93/93 PASS), hiển thị khung hình (0 lỗi bố cục) và đồng bộ bản dựng (`spec_sha256`, `tts_sha256`, `SRT`) rất tốt. Tuy nhiên, phần **`practice` / `labs/CAS/L*`**, **chuẩn P1/P8/P9** và siêu dữ liệu **`covers:`** còn lỗi hệ thống và một số lỗi sai kiến thức/logic ở bài thực hành khiến khoá **chưa đạt ngưỡng Stage 10**.

---

## 1. Bảng tóm tắt cấp khoá

| Hạng mục kiểm | Kết quả | Ghi chú |
|---|---|---|
| Số bài đã kiểm | **12/12** (`L00–L11`) | Chỉ đọc, không sửa tệp |
| `lv.py lint` | **12/12 PASS** (0 FAIL, 0 WARN) | Đã chạy trực tiếp trên từng YAML |
| `audit/cas/verify_cas.py` | **93/93 PASS** | Đã chạy trực tiếp |
| `build_report.json` (`spec` & `tts` digest) | **12/12 khớp** | `spec_sha256 == lv.spec_digest`, `tts_sha256 == lv.tts_digest` |
| `out/CAS/L*/L*.srt == say` | **12/12 khớp 100%** | Không thiếu câu, không lệch số |
| `out/CAS/L*/asr_report.md` | **12/12** `thiếu audio: 0`, `chưa xem xét: 0` | `L01(2), L04(1), L06(1), L08(8), L09(24), L11(2)` câu gắn cờ (đã vào `asr_reviewed`, còn `NOT_VERIFIED bằng tai người`) |
| `labs/CAS/L*/loi_giai.py` vs `mong_doi.txt` | **12/12 chạy PASS** | Chạy bằng `.venv/Scripts/python.exe` (không dùng `bash.exe`) |
| `audit/layout_CAS.tsv` | **0 lỗi bố cục** (tệp 2 byte `\r\n`) | Xác nhận trực quan qua 37 PNG |
| `audit/review/screen_code/CAS.yaml` | **34/34 khớp SHA** (`MISSING=0, ORPHAN=0, STALE=0`) | Nhưng 10 khối `practice 1 0` (mã Python) gắn nhãn nhầm `kind: other` ("Đầu ra mong đợi...") |
| Số bài **MUST = 0** (tính cả P1/P8/P9) | **0/12** | Nếu chỉ tính sai chuẩn xác/logic trong bài & lab: **7/12** sạch (`L01, L05, L07, L09, L10` có MUST ở `practice`/`lab`) |
| Số bài **SHOULD > 0** | **12/12** | Cả 12 bài đều có lệch `covers:` + 10 bài sai nhãn `screen_code` + ASR/tính nhất quán |
| Số bài **P1 = 2** (chấm chặt) | **0/12** (`12/12` đạt `0`) | Toàn bộ dùng Python/Bash chưa giảng trong khoá; nhiều thuật ngữ thân bài/`de.md` chưa giảng |
| Số bài **P8 = 2** | **0/12** (`8` bài `1`, `4` bài `0`) | 10/12 lộ `loi_giai`+`mong_doi` trước `pause`; 12/12 `de.md` không có format stdout; 4 bài sai logic đề↔code |
| Số bài **P9 = 2** | **0/12** (`11` bài `1`, `L00` đạt `0`) | 12/12 thiếu `<p class="note"><b>Hai mức quy mô:</b> ...` và SVG quy mô trong `recap` |

---

## 2. Phát hiện phân tách `MUST` / `SHOULD` / `INFO`

### MUST (Phải sửa trước khi GO)

1. **`[L07]` Mâu thuẫn toán học `O(n²)` vs `O(n³)` giữa thân bài và `practice`/lab**
   - **Cảnh/tệp:** `L07_cloudflare_regex.yaml` (`practice#1, #3`), `labs/CAS/L07/{de.md, loi_giai.py}`.
   - **Trích nguyên chữ:** Thân bài (`example#2`, `check#0`, `recap#0`) dạy mẫu `.*.*=.*` tìm ở mọi vị trí trên chuỗi `n` chữ `x` tăng bậc **`n mũ 3`** (`n=10 → 638`, `n=20 → 3773`, `n=100 → 358 853`, `n=200 → 2 767 703`, tỉ số `7,7`). Ngược lại `practice#3` và `de.md` ghi `"ReDoS mẫu '.*.*=.*' tăng bậc hai O(n^2)"` và `loi_giai.py` tính `n * (n + 1) // 2` (`125250`, công thức cho **1** vị trí bắt đầu).
   - **Đề xuất sửa:** Sửa đề và lời giải lab tính đúng tổng số bước quay lui ở mọi vị trí (bậc `O(n³)`) khớp cơ chế thân bài, hoặc nêu rõ mô phỏng một vị trí bắt đầu và giải thích không dùng thuật ngữ `O(n^2)`/`ReDoS` chưa giảng.

2. **`[L09]` Lab `practice`/lab kiểm sai điều kiện biên RFC 6520 và sai số byte lộ**
   - **Cảnh/tệp:** `L09_heartbleed.yaml` (`practice#1, #3`), `labs/CAS/L09/{de.md, loi_giai.py}`.
   - **Trích nguyên chữ:** Thân bài (`formula#0`, `example#0`, `sources_L09.md`) khẳng định điều kiện đúng của RFC 6520 §4 và bản vá OpenSSL 1.0.1g là **`1 + 2 + n + 16 <= L`** (phải gồm 1 byte loại + 2 byte độ dài + ≥ 16 byte đệm; với `L=20, n=65535` thì lộ ngoài bản ghi `65 518` byte). Nhưng `loi_giai.py` viết `claimed_len, actual_len = 65535, 1; overread_blocked = (claimed_len > actual_len); leak_bytes_prevented = claimed_len - actual_len` (`65534`), kiểm trên biến `actual_len=1` (mà máy chủ không biết tách khỏi `L`) và bỏ quên 3 byte đầu + 16 byte đệm.
   - **Đề xuất sửa:** Viết lại lab kiểm đúng `1 + 2 + claimed_len + 16 <= record_len` trên `record_len` (L) thực nhận và tính đúng phần đọc vượt ngoài bản ghi (`claimed_len - (record_len - 3)` hoặc theo điều kiện RFC).

3. **`[L05]` Đề lab lệch logic lời giải và sai số liệu nguồn SEC (`465M` vs `>460M`)**
   - **Cảnh/tệp:** `labs/CAS/L05/{de.md, loi_giai.py}`, `L05_knight_capital.yaml` (`practice#1`).
   - **Trích nguyên chữ:** `de.md` yêu cầu: `"Tính xác suất hỏng triển khai khi cập nhật tay 7/8 nút và tổng lỗ 465M / 45 phút"`. Nhưng `loi_giai.py` **không tính xác suất** nào (chỉ in `missing_nodes=1 loss_per_min_M=10.3`) và dùng **`465.0 / 45.0`** (`10.3`), trái với lệnh SEC 34-70694 và thân bài (`"hơn 460 triệu"` → `460 / 45 > 10,2`). Đồng thời `sources_L05.md` lưu ý nguồn SEC không nói `"bằng tay"` (`manual`), nhưng `de.md` và `curriculum/cas.yaml` Obj 3 vẫn ghi `"cập nhật tay"` / `"triển khai bằng tay"`.
   - **Đề xuất sửa:** Đồng bộ `de.md` và `loi_giai.py` tính cả xác suất sót máy (ví dụ `1 - (1 - p)**n`) lẫn tốc độ lỗ từ mốc `460` triệu/45 phút (`10.2`), bỏ chữ "bằng tay" ở phần mô tả sự cố thật.

4. **`[L01]` Mâu thuẫn số học `0.3434` vs `0,3433` và thuật ngữ `24-bit` trong lab**
   - **Cảnh/tệp:** `L01_patriot.yaml` (`practice#1–#4`), `labs/CAS/L01/{de.md, loi_giai.py}`.
   - **Trích nguyên chữ:** Thân bài (`example#0`, `recap#0`) và báo cáo GAO ghi sai số 100 giờ là **`0,3433` giây** (`3 600 000 * (0.1 - 838860 / 2**23) = 0.34332275...`). Nhưng `loi_giai.py` dùng `err_tick = 9.54e-8` (đã làm tròn) nhân `3 600 000` ra **`drift_s=0.3434`**. Ngoài ra `de.md` viết `"hệ nhị phân 24-bit"` thay vì 23 bit phần lẻ (thanh ghi 24 bit).
   - **Đề xuất sửa:** Dùng phép tính chính xác `0.8 / 2**23` (hoặc `0.1 - 838860 / 2**23`) để ra đúng `0.3433`, và sửa `de.md` nêu rõ 23 bit phần lẻ / thanh ghi 24 bit.

5. **`[L10]` Đề lab yêu cầu "độ sai tương đối" nhưng lời giải tính tỉ số `2.1x` với số lạ**
   - **Cảnh/tệp:** `labs/CAS/L10/{de.md, loi_giai.py}`, `L10_google_flu_trends.yaml` (`practice#1–#4`).
   - **Trích nguyên chữ:** `de.md` hỏi `"Tính độ sai tương đối khi dự báo cao hơn CDC gấp 2.1× (vượt >100%)"`, nhưng `loi_giai.py` dùng `cdc_pct, gft_pct = 5.0, 10.5` (không có trong `de.md` hay thân bài vốn dùng `2%` và `4,2%`) và in `gft_over_cdc=2.1x` (tỉ số, không phải sai số phần trăm `(10.5 - 5.0) / 5.0 * 100 = 110%`).
   - **Đề xuất sửa:** Ghi rõ đầu vào trong `de.md` và tính đúng sai số tương đối `%` theo công thức đã dạy ở `prereq#0`.

6. **`[P8 — Toàn khoá]` Lộ lời giải trước `pause` (10/12 bài) và `de.md` không tự đứng được (12/12 bài)**
   - **Lộ trước `pause`:** Trong 10/12 bài (`L00, L01, L02, L04, L06, L07, L08, L09, L10, L11`), `practice#1` hiện trọn bộ `loi_giai.py` và `practice#2` hiện trọn bộ `mong_doi.txt` **trước** `practice#3 (pause: 30)`.
   - **`de.md` không tự đứng được (12/12):** Không một tệp `labs/CAS/L*/de.md` nào ghi định dạng `stdout` bắt buộc (`indep_pct=...`, `ticks=...`, v.v.); nhiều bài thiếu hẳn giá trị đầu vào (`L00, L03, L06, L08, L10`); 5 bài (`L00, L01, L02, L04, L11`) dùng trùng nguyên số ví dụ trong bài.
   - **Đề xuất sửa:** Di chuyển `loi_giai` + `mong_doi` ra **sau** `pause: 30`; bổ sung đủ đầu vào, yêu cầu bài toán và định dạng `stdout` chính xác vào mọi `de.md`; đổi số liệu lab khác ví dụ thân bài.

7. **`[P1 — Toàn khoá]` 12/12 bài đạt `P1 = 0` theo chuẩn chặt**
   - Khoá `CAS` không có điều kiện tiên quyết Python/Bash (`assumes` chỉ là toán phổ thông), nhưng 12/12 bài yêu cầu viết/đọc mã Python và chạy `bash labs/cham.sh ...`.
   - Bảng đọc mã `practice#0` thiếu ở `L03, L05`, và ở 10 bài còn lại chỉ phủ `f"{val:.3f}"`, `print(...)` (cộng `import thu_vien` ở `L11`), bỏ sót hàng loạt cú pháp (`**`, `<<`, `//`, `:.4f`, `:.2f`, `:.1f`, `e-8`, `int()`, `set()`, dict comprehension, `class`, `def`, `__init__`, `self`, `return`, `datetime`, `timedelta`, `strftime`, `bash`) và nhiều thuật ngữ/ký hiệu chưa giảng trong thân bài & `de.md` (chi tiết từng mục ở Bảng mục 4).

8. **`[P9 — Toàn khoá]` 12/12 bài thiếu `<p class="note"><b>Hai mức quy mô:</b> ...` và SVG quy mô trong `recap`**
   - Dù 11/12 bài (`L01–L11`) có ví dụ số ở ≥ 2 mức quy mô/thời gian + đánh đổi trong thân bài/quiz, không có bài nào có `<p class="note"><b>Hai mức quy mô:</b> ...` hay SVG hai mức quy mô trong `recap` (riêng `L00` thiếu 2 mức quy mô ngay cả trong thân bài).

---

### SHOULD (Nên sửa để hoàn thiện chuẩn chất lượng)

1. **`[covers: — 12/12 bài]` Khai báo `covers:` bị lệch khỏi cảnh dạy thật:**
   - 11/12 bài (`L00–L04, L06–L11`) dùng mẫu rập khuôn `1->example, 2->check, 3->check, 4->practice`; `L05` dùng `1->example, 2->timeline, 3->check, 4->practice`.
   - Hệ quả: `objective: 4` ở **12/12 bài** (chọn biện pháp hệ thống / thiết kế giao diện / xếp thứ tự di chuyển) trỏ nhầm vào `practice` (chỉ in 1 dòng số học) thay vì `pitfalls` / `quiz` / `design` (`L03`). Nhiều mục tiêu 1–3 cũng trỏ sai:
     - `L00` Obj 2 (nguyên nhân góp phần) → trỏ `check` (chỉ kiểm 66 phút, 0,1%, 10%) thay vì `concept`/`example`.
     - `L01` Obj 1 (dòng thời gian) → trỏ `example` thay vì `timeline`; Obj 2 (đổi 0,1 sang nhị phân) → trỏ `check` thay vì `formula`.
     - `L02` Obj 2 (dòng thời gian & căn chỉnh 40s) → trỏ `check` thay vì `timeline`; Obj 3 (so 3 cách xử lý tràn) → trỏ `check` thay vì `formula`.
     - `L03` Obj 3 (tính lại 170 km = 226 − 57) → trỏ `check` (không nhắc 226 hay 57) thay vì `example`.
     - `L04` Obj 3 (vì sao lỗi hiện dưới tải cao & ghi vết cứu tàu) → trỏ `check` thay vì `example`/`fix`.
     - `L05` Obj 3 (tốc độ lỗ, khớp lệnh, xác suất sót máy) → trỏ `check` (chỉ kiểm mã băm) thay vì `example`/`quiz`.
     - `L06` Obj 2 (vì sao khởi động lại & lâu hơn dự kiến) → trỏ `check` thay vì `intuition`/`example`.
     - `L07` Obj 3 (đẩy quy tắc toàn cầu trong vài giây) → trỏ `check` thay vì `intuition`/`pitfalls`.
     - `L08` Obj 2 (4 cách sao lưu) → trỏ `check` thay vì `intuition`/`pitfalls`.
     - `L09` Obj 3 (lộ bộ nhớ kề & thay khoá) → trỏ `check` thay vì `intuition`/`pitfalls`/`quiz`.
     - `L10` Obj 1 (sai số % & "cao hơn gấp đôi") → trỏ `example` (chỉ dùng MAE) thay vì `prereq`.
     - `L11` Obj 2 (hạn không dấu, 34 bit, 64 bit) → trỏ `check` thay vì `example`; Obj 3 (kiểm kê) → trỏ `check` thay vì `inventory`.

2. **`[screen_code/CAS.yaml]` Gắn nhãn sai bản chất 10 khối mã Python `practice 1 0`:**
   - Ở 10 bài (`L00, L01, L02, L04, L06, L07, L08, L09, L10, L11`), khối `practice 1 0` là **mã nguồn Python** (`Cài đặt kiểm chứng CAS:Lxx bằng Python`), nhưng `screen_code/CAS.yaml` lại đăng ký `kind: other, lang: text, reason: "Đầu ra mong đợi chính xác của lab..."` thay vì `kind: run, lang: python`. (Riêng `L03 design 0 0` và `L05 check 0 0` đã là `kind: run` và chạy PASS).

3. **`[ASR / Phát âm tiếng Việt]`:**
   - `L09` có **24/91 câu bị gắn cờ** (chủ yếu do đọc thô `"byte"` thành `"bay/bai/vai"`, hoặc chữ cái đơn `n, p, L`); `L08` có **8/94 câu** (`MB/GB/tỉ/nhầm`); `L01` (2), `L04` (1 — chữ `"r"` đọc thành `"error"`), `L06` (1 — `"Amazon"` thành `"Amarron"`), `L11` (2 — `"n bit"`, `"32 bit"`). Toàn bộ các mục `asr_reviewed` đều ghi `NOT_VERIFIED bằng tai người` — nên nghe kiểm tra hoặc Việt hoá từ `"byte"` (`bai`) / tránh chữ cái đơn đứng một mình trong `say`.

4. **`[Nhất quán chi tiết lab & bài học]`:**
   - `L06/de.md`: lỗi chính tả `"máy phép gỡ"` (nên là "máy cho phép gỡ"); ngưỡng `10%` và `60%` không khớp ví dụ thân bài (`100` máy, tối thiểu `70` → tối đa `30%`).
   - `L08/loi_giai.py`: `aborted_on_primary = int(not ((host == expected_rm_target) and restore_tested))` vẫn trả `aborted_on_primary=1` ngay cả khi `host == 'db-secondary'` mà `restore_tested == False`.
   - `L03/de.md` & `loi_giai.py`: thân bài `design` dùng `4.448222`, `prereq`/`formula` dùng `4.448` và `4.45`, còn `loi_giai.py` dùng `4.44822`.

---

### INFO (Ghi nhận thêm, không chặn)

1. **`say` không chứa ký hiệu toán thô:** Đã quét toàn bộ 12 bài — **0 câu** chứa ký hiệu toán thô (`+ = * / < > ^ % _ { } [ ] \ | ~ $ · × ÷ − ≤ ≥ ≈ → ← ↔`).
2. **Câu chứa `"càng "` trong `say`:** Tìm thấy **4 câu** across 12 bài, đều đi kèm định lượng/ngữ cảnh rõ và không bị ASR gắn cờ:
   - `L01 [intuition#0]`: `"Chạy càng lâu, n càng lớn, nên sai số tăng đều theo giờ chạy..."`
   - `L04 [formula#1]`: `"Vì vậy tải càng cao thì tác vụ cao chờ càng lâu."`
   - `L10 [example#1]`: `"Càng nhiều ứng viên, càng chắc tìm được một chuỗi trùng hợp với quá khứ mà chẳng liên quan gì tới cúm."`
   - `L10 [pitfalls#0]`: `"Bài học sai thứ nhất là nghĩ dữ liệu càng lớn thì dự báo càng đúng."` (trích lời ngộ nhận để phản bác).
3. **`sources_L*.md` ("Điều KHÔNG dạy"):** Thân bài cả 12 bài tuân thủ nghiêm ngặt các mục "Điều KHÔNG dạy" và phân biệt rõ `(CITED)` vs `(số minh hoạ)` vs `(VER)` (chỉ có `L05/de.md` ghi `465M` & "cập nhật tay" và `L01/de.md` ghi `24-bit` là lệch từ nguồn).
4. **Tiêu đề `curriculum/cas.yaml` vs `lessons/cas/L*.yaml`:** Chỉ khác tiền tố chuẩn `'Bài X — '` (12/12 `objectives` khớp nguyên văn).
5. **Chạy thử mã trên màn hình thân bài:** `L03 design 0 0` (`tu_pao_luc_giay(10) = 44.48222`, tổng `54.48222`) và `L05 check 0 0` (`True`, `False`, `b995c3ca82ef`) đều chạy thật bằng Python cho kết quả khớp 100%.

---

## 3. Bảng tổng hợp từng bài (`L00–L11`)

| Bài | sha16 lúc đọc | Phút | Spec / TTS / SRT / Lab | ASR (cờ / chưa XX / thiếu) | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng P1–7 | Mất gốc | P8 | P9 | Cần biết trước (trích chính) | Chỗ thiếu chính |
|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **L00** | `159446f848db55b8` | 12.5 | Khớp / Khớp / Khớp / PASS | 0 / 0 / 0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 0 | `rò rỉ tài nguyên`, `chỉ mục`, `cụm máy`, `quay lui`, Python `**`, `:.2f`, `bash` | P1 mã & thuật ngữ; P8 lộ giải + `de.md` thiếu format; P9 thiếu 2 quy mô + recap; `covers` |
| **L01** | `9cef7f7d0c8ea945` | 13.5 | Khớp / Khớp / Khớp / PASS | 2 / 0 / 0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | Python `9.54e-8`, `:.4f`, `=`, `*`, `bash` | MUST lab `0.3434` vs `0.3433`; P1 mã; P8 lộ giải + `de.md` thiếu format; P9 thiếu recap; `covers` |
| **L02** | `5410cae1f8c31183` | 13.1 | Khớp / Khớp / Khớp / PASS | 0 / 0 / 0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | Python `<<`, `not ... <= ...`, `int()`, tuple unpack, `bash` | P1 mã; P8 lộ giải + `de.md` thiếu format; P9 thiếu recap; `covers` |
| **L03** | `4e1589607be3141e` | 12.2 | Khớp / Khớp / Khớp / PASS | 0 / 0 / 0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | Python OOP (`class`, `def`, `__init__`, `self`, `return`, `#`), `lbf`, `N`, `bash` | P1 OOP ở `design` (không có bảng đọc); P8 `de.md` thiếu format & input; P9 thiếu recap; `covers` |
| **L04** | `ea2010447a959978` | 12.4 | Khớp / Khớp / Khớp / PASS | 1 / 0 / 0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | Python `=`, `+`, `f"...ms"`, `priority inheritance`, `bash` | P1 mã; P8 lộ giải + `de.md` thiếu format; P9 thiếu recap; `covers` |
| **L05** | `54e7e189e1d56a63` | 11.5 | Khớp / Khớp / Khớp / PASS | 0 / 0 / 0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 1 | Python `import hashlib`, `def`, `.encode()`, `.hexdigest()`, `[:12]`, `set()`, `465M`, `bash` | MUST lab thiếu xác suất + `465M` vs `>460M`; P1 mã `check#0`; P8 `de.md` lệch code; P9 recap; `covers` |
| **L06** | `38bdc7ff91bcf393` | 11.7 | Khớp / Khớp / Khớp / PASS | 1 / 0 / 0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | `AWS` (chưa giải nghĩa), Python `>`, `int()`, `bash` | P1 mã; P8 lộ giải + `de.md` thiếu format & lệch ngưỡng `10%/60%`; P9 thiếu recap; `covers` |
| **L07** | `30f3ee7d037f2422` | 12.2 | Khớp / Khớp / Khớp / PASS | 0 / 0 / 0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | Python `//`, `ReDoS`, `O(n^2)`, `bash` | MUST lab `O(n^2)` vs bài `O(n^3)`; P1 mã/ký hiệu; P8 lộ giải + sai logic; P9 recap; `covers` |
| **L08** | `2eaa340d450087df` | 11.5 | Khớp / Khớp / Khớp / PASS | 8 / 0 / 0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | `GB` (1000 MB), Python `;`, `==`, `and`, `not`, `rm -rf`, `hostname`, `restore`, `bash` | P1 mã/Linux; P8 lộ giải + `de.md` thiếu format + logic `secondary`; P9 recap; `covers` |
| **L09** | `20d9aed0166d8ebf` | 11.6 | Khớp / Khớp / Khớp / PASS | 24 / 0 / 0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 1 | `KB`, `RFC`, `bounds`, `payload`, `1B`, `65535B`, Python `>`, `int()`, `bash` | MUST lab sai kiểm biên RFC + `65534`; P1 mã/thuật ngữ; P8 lộ giải; P9 recap; ASR `byte`; `covers` |
| **L10** | `57a0104d2a6e8e52` | 11.2 | Khớp / Khớp / Khớp / PASS | 0 / 0 / 0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 1 | Python `:.1f`, `=`, `ngoại suy`, `2.1×`, `bash` | MUST lab tính tỉ số thay vì độ sai tương đối; P1 mã; P8 lộ giải; P9 recap; `covers` |
| **L11** | `f9977eeef8af64cf` | 13.8 | Khớp / Khớp / Khớp / PASS | 2 / 0 / 0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | `x86`, `TIMESTAMP`, `import as`, `dt.datetime`, `tzinfo`, `timedelta`, `<<`, `strftime`, `UTC`, `bash` | P1 Python/cú pháp; P8 lộ giải + `de.md` thiếu format; P9 thiếu recap; `covers` |

*(Ghi chú: trong bảng trên, `L09` có `P8 = 0` vì sai kiểm biên RFC 6520; tính chính xác: 4 bài `P8 = 0` là `L05, L07, L09, L10`, 8 bài `P8 = 1` là `L00, L01, L02, L03, L04, L06, L08, L11` — đã ghi ở bảng tóm tắt mục 1).*

---

## 4. Liệt kê chi tiết các mục `P1` chưa giảng (từng bài, cảnh/step, trích chữ, độ phủ bảng cách đọc)

| Bài | Cảnh / step hoặc tệp | Trích chữ chưa giảng | Bảng cách đọc `practice#0` có phủ không? |
|---|---|---|---|
| **L00** | `example#0` | `rò rỉ tài nguyên` | không (thân bài) |
| **L00** | `example#1` | `chỉ mục`, `cụm máy` | không (thân bài) |
| **L00** | `quiz#0` | `quay lui` (`quay lui cấu hình`) | không (thân bài) |
| **L00** | `practice#1` | `=`, `**`, `*`, `:.2f`, `:.1f` (bảng chỉ ghi `:.3f`) | không (chỉ phủ `f"{val:.3f}"`, `print`) |
| **L00** | `practice#3`, `de.md` | `bash labs/cham.sh ...` (`bash`) | không |
| **L01** | `practice#1` | `9.54e-8`, `=`, `*`, `:.4f` | không (bảng chỉ phủ `f"{val:.3f}"`, `print`) |
| **L01** | `practice#3`, `de.md` | `bash`, cụm `hệ nhị phân 24-bit` (bài dùng 23 bit phần lẻ) | không |
| **L02** | `practice#1` | `lo, hi = -(1 << 15), (1 << 15) - 1` (`<<`, gán cặp), `int(not lo <= bh_val <= hi)` | không (bảng chỉ phủ `f"{val:.3f}"`, `print`) |
| **L02** | `practice#3`, `de.md` | `bash` | không |
| **L03** | `design#0`, `design#1` | `class`, `def`, `__init__`, `self`, `return`, `#`, `.niuton_giay()` | không (`L03` không có `practice#0`) |
| **L03** | `practice#0`, `de.md` | `lbf-giây`, `N-giây`, `4.448×`, `bash` | không |
| **L04** | `practice#1` | `=`, `+`, `f"wait_no_inherit={no_inherit}ms..."` | không (chỉ phủ `f"{val:.3f}"`, `print`) |
| **L04** | `practice#3`, `de.md` | `bash`, `priority inheritance` | không |
| **L05** | `check#0` | `import hashlib`, `def`, `.encode()`, `.hexdigest()`, `[:12]`, `{ten: ... for ...}`, `len(set(...)) == 1`, `return` | không (`L05` không có `practice#0`) |
| **L05** | `practice#0`, `de.md` | `465M`, `bash` | không |
| **L06** | `pitfalls#0`, `quiz#2` | `AWS` (không giải nghĩa viết tắt của Amazon Web Services) | không (thân bài) |
| **L06** | `practice#1` | `=`, `>`, `int(blocked)` | không (chỉ phủ `f"{val:.3f}"`, `print`) |
| **L06** | `practice#3`, `de.md` | `bash` | không |
| **L07** | `practice#1` | `=`, `*`, `+`, `//` | không (chỉ phủ `f"{val:.3f}"`, `print`) |
| **L07** | `practice#3`, `de.md` | `ReDoS`, `O(n^2)`, `bash` | không |
| **L08** | `example#2`, `check#0`, `quiz#0` | `GB` (không định nghĩa 1 GB = 1000 MB trước khi dùng) | không (thân bài) |
| **L08** | `practice#1` | `;`, `True`, `==`, `and`, `not`, `int(...)` | không (chỉ phủ `f"{val:.3f}"`, `print`) |
| **L08** | `practice#3`, `de.md` | `rm -rf`, `hostname`, `restore`, `bash` | không |
| **L09** | `sym#0` | `RFC` (`RFC 6520`) | không (thân bài) |
| **L09** | `example#2`, `pitfalls#0` | `KB` (không giải nghĩa ký hiệu KB) | không (thân bài) |
| **L09** | `practice#1` | `claimed_len, actual_len = 65535, 1`, `>`, `int(...)` | không (chỉ phủ `f"{val:.3f}"`, `print`) |
| **L09** | `practice#3`, `de.md` | `bounds`, `payload`, `1B`, `65535B`, `bash` | không |
| **L10** | `practice#1` | `cdc_pct, gft_pct = 5.0, 10.5`, `/`, `:.1f` | không (chỉ phủ `f"{val:.3f}"`, `print`) |
| **L10** | `practice#3`, `de.md` | `ngoại suy`, `2.1×`, `bash` | không |
| **L11** | `example#1`, `inventory#0`, `quiz#0` | `x86`, `TIMESTAMP` (kiểu dữ liệu chưa giải thích cấu trúc) | không (thân bài) |
| **L11** | `practice#1` | `import ... as dt`, `dt.datetime(...)`, `tzinfo=dt.timezone.utc`, `dt.timedelta(...)`, `1 << 31`, `.strftime('%Y-%m-%d %H:%M:%S')` | không (bảng chỉ phủ `import thu_vien`, `f"{val:.3f}"`, `print`) |
| **L11** | `practice#3`, `de.md` | `UTC`, `2**31-1`, `bash` | không |

---

## 5. Người học kẹt ở đâu (1 dòng/bài cho người mất gốc từ con số 0)

- **L00:** Kẹt từ `example#0` (`"rò rỉ tài nguyên"`), `example#1` (`"chỉ mục"`, `"cụm máy"`), `quiz#0` (`"quay lui"`) và kẹt nặng ở `practice#1–#3` / `de.md` (chưa từng học Python `**`, `:.2f`, `bash`, `de.md` không có định dạng stdout).
- **L01:** Theo trôi chảy phần toán, nhưng kẹt ở `practice#1–#3` / `de.md` (cú pháp Python `9.54e-8`, `:.4f`, `bash`, `de.md` thiếu format stdout và ra `0.3434` khác `0,3433` vừa học).
- **L02:** Theo trôi chảy phần bù 2 và dòng thời gian, kẹt ở `practice#1–#3` / `de.md` (toán tử dịch bit `<<`, `int(not ...)`, `bash`, `de.md` thiếu format stdout).
- **L03:** Kẹt ở `design#0` (`class XungLuc:`, `def __init__`, `self`, `return` không giảng cú pháp OOP) và `practice#0` / `de.md` (`lbf-giây`, `N-giây`, thiếu format stdout và thiếu input `100.0`).
- **L04:** Theo trôi chảy phần lập lịch, kẹt ở `practice#1–#3` / `de.md` (Python `f"...ms"`, `bash`, thuật ngữ tiếng Anh `priority inheritance`, `de.md` thiếu format stdout).
- **L05:** Kẹt ở `check#0` (đọc mã Python `import hashlib`, `hexdigest()[:12]`, dict comprehension, `set()`) và `practice#0` / `de.md` (đề đòi tính xác suất với `465M` nhưng đáp án không tính xác suất và thiếu format stdout).
- **L06:** Kẹt nhẹ ở `pitfalls#0` (`AWS`), và kẹt nặng ở `practice#1–#3` / `de.md` (Python `>`, `int()`, `bash`, `de.md` thiếu input `10`, `60` và format stdout).
- **L07:** Kẹt ở `practice#1–#3` / `de.md` (chia nguyên `//`, ký hiệu chưa giảng `ReDoS`, `O(n^2)` và mâu thuẫn với `n mũ 3` vừa học ở `example#2`).
- **L08:** Kẹt ở `example#2`/`quiz#0` (quy đổi `GB` sang `megabyte` không giảng trước) và kẹt nặng ở `practice#1–#3` / `de.md` (Python `;`, `and`, `not`, lệnh `rm -rf`, `hostname`, `restore`, thiếu format stdout).
- **L09:** Kẹt nhẹ ở `sym#0` (`RFC`), `example#2` (`KB`), và kẹt nặng ở `practice#1–#3` / `de.md` (`bounds`, `payload`, `1B`, `65535B`, và công thức `claimed_len > actual_len` trái với `1 + 2 + n + 16 <= L` vừa học).
- **L10:** Theo trôi chảy phần mô phỏng và MAE, kẹt ở `practice#1–#3` / `de.md` (`ngoại suy`, thiếu input `5.0`/`10.5`, đề hỏi độ sai tương đối nhưng đáp án in `2.1x`).
- **L11:** Kẹt nhẹ ở `example#1` (`x86`, `TIMESTAMP`), và kẹt nặng ở `practice#1–#3` / `de.md` (`datetime`, `timezone.utc`, `timedelta`, `1 << 31`, `strftime`, `bash`, thiếu format stdout).

---

## 6. Danh sách khung hình PNG đã mở xem trực tiếp (37 PNG)

- **L00:** `out/CAS/L00/frames/00027.png` (intuition SVG), `00070.png` (quiz), `00082.png` (practice#1)
- **L01:** `out/CAS/L01/frames/00023.png` (intuition SVG), `00041.png` (example), `00095.png` (practice#1)
- **L02:** `out/CAS/L02/frames/00021.png` (intuition SVG), `00074.png` (quiz), `00089.png` (practice#1)
- **L03:** `out/CAS/L03/frames/00018.png` (intuition SVG), `00060.png` (pitfalls), `00063.png` (design OOP), `00084.png` (practice#0)
- **L04:** `out/CAS/L04/frames/00021.png` (intuition SVG), `00072.png` (quiz), `00088.png` (practice#1)
- **L05:** `out/CAS/L05/frames/00021.png` (intuition SVG), `00055.png` (check Python), `00081.png` (practice#0)
- **L06:** `out/CAS/L06/frames/00027.png` (intuition SVG), `00069.png` (quiz), `00083.png` (practice#1)
- **L07:** `out/CAS/L07/frames/00023.png` (intuition SVG), `00043.png` (example), `00085.png` (practice#1)
- **L08:** `out/CAS/L08/frames/00026.png` (intuition SVG), `00064.png` (quiz), `00080.png` (practice#1)
- **L09:** `out/CAS/L09/frames/00024.png` (intuition SVG), `00063.png` (quiz), `00079.png` (practice#1)
- **L10:** `out/CAS/L10/frames/00022.png` (intuition SVG), `00057.png` (quiz), `00075.png` (practice#1)
- **L11:** `out/CAS/L11/frames/00020.png` (intuition SVG), `00038.png` (example), `00085.png` (practice#1)

*(Nhận xét chung về hiển thị: 37/37 PNG đều sắc nét, không đè chữ, không cắt khung, không tràn viền, KaTeX và SVG hiển thị sạch, khớp `layout_CAS.tsv` rỗng.)*
