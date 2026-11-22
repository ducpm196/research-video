# Báo cáo Kiểm định Stage 9 Độc lập — Khóa `CVI` (`L00–L12`, 13 bài)

**Kết luận tổng thể: `NO-GO`** (chặn phát hành ở các hạng mục `MUST`: **P8** rò rỉ lời giải trong `practice#1..2` ở 12/13 bài + thiếu định dạng `stdout` ở 13/13 `de.md` + trùng số ví dụ 13/13 + sai lệch toán/mô tả ở nhiều lab; **P1** thiếu bảng đọc mã đúng mã thật & dùng thuật ngữ Anh chưa dạy trong `de.md`/`check#1`; **P9** thiếu khối `Hai mức quy mô` trong thân bài & `recap` ở 13/13 bài; **`covers:`** ánh xạ khuôn mẫu sai cảnh dạy ở 13/13 bài).

---

## 1. Tóm tắt số liệu toàn khóa & độ nhất quán máy kiểm

| Hạng mục kiểm tra | Kết quả | Ghi chú xác minh |
|---|---|---|
| `verify_cvi.py` | **112/112 PASS** | `.venv\Scripts\python.exe audit\cvi\verify_cvi.py` (exit 0) |
| `lv.py curriculum curriculum/cvi.yaml` | **13 bài, 13 đặc tả, 0 lỗi** | Không lỗi cấu trúc; nhưng `L00..L11` curriculum ghi 2 mục tiêu, YAML ghi 4 mục tiêu |
| `lv.py lint` (`L00–L12`) | **13/13 PASS** (`0 FAIL, 0 WARN`) | 25–41 PASS/bài; toàn bộ 319 phép kiểm tra số học PASS |
| `lv.py verify` (`L00–L12`) | **13/13 PASS** (`streams=True`) | Khớp `spec_sha256` & `tts_sha256`, độ dài `614.53s` (`L11`) – `1010.63s` (`L12`) |
| `L*.srt == say` | **13/13 khớp** | Kiểm trực tiếp trên 13 bản dựng `out/CVI/L*` |
| `loi_giai.py == mong_doi.txt` | **13/13 khớp khi chạy Python** | Lưu ý: `lab_gate.py CVI` qua `bash.exe` bị treo trong sandbox Windows |
| `build_report.json` | **13/13 hợp lệ & mới hơn YAML** | YAML sửa `2026-11-19 15:22–15:24`; build `2026-11-20 08:01–08:28`; giọng `vi-VN-NamMinhNeural` (`edge` + 2–3 `edge?` cache cũ ở L00–L11; L12 129/129 `edge`) |
| `out/CVI/L*/asr_report.md` | **13/13 `chưa xem xét = 0`, `thiếu audio = 0`** | Tổng **67 câu gắn cờ ASR** across L00–L12 (`L00`: 29, `L05`: 5, `L01/L07/L08/L12`: 4, `L03/L06/L09`: 3, `L02/L10/L11`: 2, `L04`: 1) — máy khớp chữ viết nhưng phát âm thực của từ ngoại/chữ cái vẫn `NOT_VERIFIED` bằng tai người |
| `screen_code.py check --course CVI` | **38 khối — PASS 38 · FAIL 0** | `run/python`: 1 (`L00 check#1`), `other/text`: 37 (`practice` các bài), `unverified_claims`: 0 |
| `audit/layout_CVI.tsv` | **STALE & RỖNG (`SHOULD`)** | Kích thước 2 byte (`\r\n`), sửa lần cuối `2026-11-19 09:47:19` (trước sửa YAML và build) |
| Khung hình PNG (`out/CVI/L*/frames/`) | **34/34 PNG đã xem SẠCH** | Không đè chữ, không tràn khung, không cắt nhãn (`L04/00017.png` sát viền dưới một chút nhưng đọc rõ) |
| **Tỷ lệ `P1 = 2`** | **0/13 (0%)** | Thân bài giải thích thuật ngữ khá tốt, nhưng 12/13 lỗi bảng `practice#0` + `de.md`, `L00` lỗi `check#1` thiếu bảng đọc mã `numpy` + `de.md` |
| **Tỷ lệ `P8 = 2`** | **0/13 (0%)** | 12/13 (`L01–L12`) lộ `loi_giai.py` + stdout trước `pause`; 13/13 `de.md` thiếu định dạng `stdout` & trùng số ví dụ; 6–7 bài lệch `de.md ↔ loi_giai.py` |
| **Tỷ lệ `P9` (thân bài)** | **11/13 (84,6%)** | 11 bài có 2 mức quy mô/điều kiện + bảng `được/mất/đánh đổi` rõ; `L01`, `L03` còn mỏng ở cấu trúc hai mức quy mô trong `quiz#2` |
| **Tỷ lệ `P9` (`Hai mức quy mô` ở thân bài & `recap`)** | **0/13 (0%)** | Không bài nào có thẻ `<p class="note"><b>Hai mức quy mô:</b> ...` trong thân bài hoặc `recap` |
| **Tỷ lệ `MUST = 0`** | **0/13 (0%)** | Mọi bài `L00–L12` đều còn tối thiểu 3 lỗi `MUST` |

*(Ghi chú phạm vi môn học: `curriculum/cvi.yaml` gồm 13 bài `L00–L12` từ ảnh số đến hành trình ImageNet, không có bài khuếch tán; mọi phép tính tích chập, Sobel, Otsu, camera lỗ kim, khớp đặc trưng, RANSAC, độ sâu hai camera, học chuyển giao, phát hiện/IoU/mAP, phân đoạn/Dice, dịch chuyển miền, lối tắt, ImageNet đã được đối chiếu toàn bộ.)*

---

## 2. Kiểm tra tất cả câu `"càng ..."` trong `say` (và `show`)

Quét toàn bộ `L00–L12` tìm được **6 lần xuất hiện** (đều đúng quy luật toán/vật lý nhân quả, tiếng Việt tự nhiên, không mắc lỗi suy diễn đường tắt):
1. `L02 intuition#0` (`say` + `show` SVG): *"hai trung bình càng xa thì hai lớp càng tách bạch"* — đúng (khoảng cách trung bình tăng làm $\sigma_B^2$ tăng).
2. `L03 formula#2` (`say` + `show`): *"Tiêu cự càng lớn thì góc nhìn càng hẹp, như ống kính chụp xa"* — đúng ($\tan(\text{FOV}/2) = (W/2)/f_x$).
3. `L03 distort#1` (`say`): *"Ở tâm, vòng và chấm trùng nhau, càng ra góc thì chấm càng bị kéo vào trong"* — đúng với méo thùng $k_1 < 0$.
4. `L04 prereq#2` (`say`): *"Tỉ số càng gần 1 nghĩa là hai số càng gần bằng nhau"* — đúng với $d_1/d_2 \to 1$.
5. `L06 prereq#0` (`say` + `show`): *"điểm càng gần thì d càng lớn"* — đúng ($d = fB/Z$).
6. `L12 hook#0` (`say` + `show`): *"vì sao càng về sau, câu hỏi lớn nhất lại là đo cho đúng"* — chuyển ý tự nhiên.

---

## 3. Báo cáo chi tiết từng bài (`L00–L12`)

### `L00` — Ảnh số: điểm ảnh, kênh màu, độ sâu bit và dung lượng
- **Số liệu & máy kiểm:** `106` frame (`783.767s`, `1980` từ), `lint 37 PASS / 0 FAIL`, `verify PASS`, `ASR flagged=29, chưa xem xét=0`.
- **PNG đã xem:** `out/CVI/L00/frames/00031.png` (SVG tensor/mảng 3D ảnh), `00035.png` (biểu đồ bit & dải mức), `00095.png` (`practice#0` Tự làm). Đều sạch, không đè chữ.
- **`MUST`:**
  1. **P1 (`check#1` + `de.md`):** `check#1` đưa đoạn mã Python `import numpy as np; khung = np.zeros((1080, 1920, 3), dtype=np.uint8); khung.nbytes` nhưng **không có bảng đọc mã** giải thích `np`, `zeros`, `dtype`, `uint8`, `nbytes`. Ngoài ra `labs/CVI/L00/de.md` dùng `GiB` và `gamma` nhưng bài chưa dạy/chú thích hai từ này.
  2. **P8 (toán `de.md` ↔ `loi_giai.py`, trùng ví dụ, thiếu định dạng stdout):** `de.md` yêu cầu *"Tính số byte/khung, **GiB** mỗi khung 1080p..."* nhưng `loi_giai.py` lại tính `mib = b_frame / (1024**2)` và in `MiB=5.93` (khớp `mong_doi.txt`: `bytes=6220800 MiB=5.93 linear_128=0.216`) — **sai lệch đơn vị GiB vs MiB**; `de.md` không ghi định dạng chuỗi `stdout` (`bytes=... MiB=... linear_128=...`) và dùng lại y nguyên số ví dụ (`1920×1080`, `128`). *(Lưu ý: `L00` không lộ `loi_giai.py` vì `practice` chỉ có 2 bước với `pause: 30` ở bước 0.)*
  3. **P9 (`recap` & thân bài):** Thiếu `<p class="note"><b>Hai mức quy mô:</b> ...` trong thân bài và `recap`. (Thân bài `quiz#0/#2` có so sánh ảnh `224×224` vs `1080p` vs 1 giờ `4K` `2,69 TB` + bảng được/mất — **P9 thân bài đạt, `recap` trượt**.)
  4. **`covers:`:** Khai báo khuôn mẫu `[(1, 'example'), (2, 'check'), (3, 'check'), (4, 'practice')]` — không ánh xạ đúng các cảnh dạy thực tế (`sym`, `intuition`, `formula`, `pitfalls`).
- **`SHOULD`:** `curriculum` chỉ ghi 2 mục tiêu trong khi YAML có 4; `ASR` gắn cờ 29 câu (`L00` cao nhất khóa) cần nghe kiểm lại thực tế; `layout_CVI.tsv` stale.
- **`INFO`:** Các thuật ngữ trong thân bài (`TB`, `MiB`, `OpenCV`, `BGR`, `sRGB`) đều được chú thích tiếng Việt tại chỗ. `L00 check#1` là khối `run/python` duy nhất được `screen_code` đánh dấu chạy mã thực.
- **Điểm đánh giá:** `P1=1`, `P8=0`, `P9_body=đạt`, `P9_recap=0`.

### `L01` — Lọc ảnh bằng tích chập: làm mờ, phát hiện cạnh Sobel
- **Số liệu & máy kiểm:** `99` frame (`741.567s`, `2076` từ), `lint 37 PASS / 0 FAIL`, `verify PASS`, `ASR flagged=4, chưa xem xét=0`.
- **PNG đã xem:** `out/CVI/L01/frames/00023.png` (SVG lưới tích chập/tương quan), `00054.png` (SVG tín hiệu & làm mờ trước khi lấy cạnh), `00084.png` (`practice#0` bảng đọc mã). Đều sạch.
- **`MUST`:**
  1. **P8 (lộ lời giải + sai khái niệm tích chập vs tương quan chéo + gán cứng + trùng ví dụ):** `practice#1` và `practice#2` lộ nguyên `loi_giai.py` và `sobel_edge_x=40 flat_region=0` trước `practice#3` (`pause: 30`). Nghiêm trọng hơn về mặt CV: `de.md` ghi *"Tích chập Sobel `S_x`"* nhưng `loi_giai.py` tính `sum(kx[r][c] * img[r][c] ...)` **không lật 180°** (tức tương quan chéo ra `+40`), trái ngược trực tiếp với `pitfalls#0` của chính `L01` đã chứng minh *tích chập phải lật bộ lọc nên ra `-40`*! Đồng thời `loi_giai.py` gán cứng `flat_region=0` không tính trên vùng phẳng; `de.md` thiếu định dạng `stdout` và trùng đúng ma trận ví dụ (`cột phải 10`).
  2. **P1 (`practice#0` lệch mã):** Bảng `practice#0` dạy `f"{val:.3f}"`, `len`, `max`, `min` (không dùng trong `loi_giai.py`), nhưng lại thiếu `range(...)` và `sum(... for r in ... for c in ...)` được dùng thật.
  3. **P9:** Thiếu `Hai mức quy mô` trong thân bài & `recap`; thân bài `quiz#2` so sánh sáng (cạnh 40) vs chiều (cạnh 20) nhưng chưa thể hiện rõ hai mức quy mô dữ liệu/không gian như các bài sau.
  4. **`covers:`:** Khuôn mẫu `example/check/check/practice`, bỏ sót `sym`, `formula`, `blur`, `pitfalls`.
- **`SHOULD`:** `curriculum` 2 mục tiêu vs YAML 4; `probes/p1` ghi `Sobel` (2/8) & `Gauss` (0/8) ASR nghe kém; `layout_CVI.tsv` stale.
- **Điểm đánh giá:** `P1=1`, `P8=0`, `P9_body=thiếu/mỏng`, `P9_recap=0`.

### `L02` — Biểu đồ tần suất, cân bằng và ngưỡng Otsu
- **Số liệu & máy kiểm:** `100` frame (`771.3s`, `2120` từ), `lint 37 PASS / 0 FAIL`, `verify PASS`, `ASR flagged=2, chưa xem xét=0`.
- **PNG đã xem:** `out/CVI/L02/frames/00018.png` (SVG hai đỉnh tối/sáng & ngưỡng `t=12`), `00055.png` (SVG cân bằng biểu đồ), `00085.png` (`practice#0` bảng đọc mã). Đều sạch.
- **`MUST`:**
  1. **P8 (lộ lời giải + lệch ngưỡng `49` vs `12` + trùng ví dụ + thiếu định dạng `stdout`):** `practice#1..2` lộ `loi_giai.py` và `best_thr=49 between_var=434.0` trước `pause: 30`. Với `[10, 10, 12, 50, 52, 55]`, mọi $t \in [12, 49]$ đều cho $\sigma_B^2 = 434{,}0$; nhưng trong bài YAML (`example#3`, SVG `00018.png`) chọn `t = 12` (đầu tiên), còn `loi_giai.py` dùng `max((var, t) for t in range(11, 55) ...)` nên trả về `best_thr=49` mà không giải thích sự khác biệt. `de.md` thiếu định dạng `stdout` và trùng y nguyên 6 số ví dụ.
  2. **P1 (`practice#0` lệch mã):** Dạy `f"{val:.3f}"` và `min` (không dùng; lời giải dùng `:.1f`), thiếu `if ...` lọc trong list comprehension, `range()`, `**`.
  3. **P9:** Thiếu `Hai mức quy mô` ở thân bài & `recap` (thân bài `quiz#2` có so sánh ngưỡng toàn ảnh vs cục bộ vùng nhỏ/vừa + bảng được/mất — thân bài đạt).
  4. **`covers:`:** Khuôn mẫu `example/check/check/practice`, không phản ánh `intuition`, `formula`, `equalize`, `pitfalls`.
- **`SHOULD`:** `curriculum` 2 mục tiêu vs YAML 4; `Otsu` ASR 0/8 (`probes/p1`); `layout_CVI.tsv` stale.
- **Điểm đánh giá:** `P1=1`, `P8=0`, `P9_body=đạt`, `P9_recap=0`.

### `L03` — Hiệu chuẩn camera: mô hình lỗ kim, ma trận K và méo ống kính
- **Số liệu & máy kiểm:** `101` frame (`788.767s`, `2167` từ), `lint 35 PASS / 0 FAIL`, `verify PASS`, `ASR flagged=3, chưa xem xét=0`.
- **PNG đã xem:** `out/CVI/L03/frames/00026.png` (SVG camera lỗ kim & tia chiếu), `00043.png` (SVG lưới méo ống kính), `00086.png` (`practice#0` bảng đọc mã). Đều sạch.
- **`MUST`:**
  1. **P8 (lộ lời giải + trùng ví dụ + thiếu định dạng `stdout`):** `practice#1..2` lộ `loi_giai.py` và `pixel_u=520 pixel_v=340` trước `pause: 30`; `de.md` dùng lại y nguyên `f=800, (320,240), (0.5, 0.25, 2.0)` của `example#0`, thiếu định dạng `stdout`.
  2. **P1 (`practice#0` lệch mã):** Dạy `f"{val:.3f}"` không dùng (lời giải dùng `:.0f` và gán nhiều biến `f, cx, cy = ...`).
  3. **P9:** Thiếu `Hai mức quy mô` ở thân bài & `recap`; thân bài `quiz#2` liệt kê quy trình hiệu chuẩn (10 ảnh bàn cờ, khóa nét, kiểm mỗi ca) nhưng không có bảng so sánh hai mức quy mô + đánh đổi như đa số bài khác (mới có đối chiếu tâm vs góc ở `distort#1`/`pitfalls#3`).
  4. **`covers:`:** Khuôn mẫu `example/check/check/practice`, thiếu `sym`, `formula`, `distort`, `pitfalls`.
- **`SHOULD`:** `sym#0` dùng ký hiệu `mm` không mở ngoặc `mi-li-mét`; `curriculum` 2 mục tiêu vs YAML 4; `layout_CVI.tsv` stale.
- **Điểm đánh giá:** `P1=1`, `P8=0`, `P9_body=thiếu/mỏng`, `P9_recap=0`.

### `L04` — Khớp đặc trưng giữa hai ảnh: điểm khoá, mô tả và phép thử tỉ số
- **Số liệu & máy kiểm:** `88` frame (`669.167s`, `1953` từ), `lint 31 PASS / 0 FAIL`, `verify PASS`, `ASR flagged=1, chưa xem xét=0`.
- **PNG đã xem:** `out/CVI/L04/frames/00017.png` (SVG biến đổi độ sáng/xoay/tỉ lệ), `00033.png` (SVG khớp đúng vs mơ hồ trong không gian mô tả), `00072.png` (`practice#0` bảng đọc mã). Sạch (lưu ý nhỏ ở `00017.png`: chú thích `"ảnh 11 × 11: góc dưới phải sáng 10, còn lại 0"` nằm hơi sát cạnh dưới khung cam nhưng vẫn đọc rõ).
- **`MUST`:**
  1. **P8 (lộ lời giải + trùng ví dụ + thiếu định dạng `stdout`):** `practice#1..2` lộ `loi_giai.py` và `keep_good=1 keep_ambiguous=0` trước `pause: 30`; `de.md` thiếu định dạng `stdout` và trùng đúng `(0.3, 0.5)` và `(0.45, 0.50)`.
  2. **P1 (`de.md`/`practice#3` dùng thuật ngữ chưa dạy + `practice#0` lệch mã):** Thân bài YAML cố ý tránh từ `SIFT` (chỉ nói *"bài báo năm 2004 về đặc trưng bất biến theo tỉ lệ"*), nhưng `de.md` và `practice#3` dùng trực tiếp **`SIFT`** chưa hề giải thích trong bài; `practice#0` dạy `f"{val:.3f}"` không dùng nhưng thiếu `int(...)` và phép so sánh `< 0.8`.
  3. **P9:** Thiếu `Hai mức quy mô` ở thân bài & `recap` (thân bài `quiz#2` có bảng chọn ngưỡng/cặp + được/mất — thân bài đạt).
  4. **`covers:`:** Khuôn mẫu `example/check/check/practice`.
- **`SHOULD`:** `curriculum` 2 mục tiêu vs YAML 4; `layout_CVI.tsv` stale.
- **Điểm đánh giá:** `P1=0`, `P8=0`, `P9_body=đạt`, `P9_recap=0`.

### `L05` — Tìm mô hình khi nhiều điểm sai: đồng thuận mẫu ngẫu nhiên
- **Số liệu & máy kiểm:** `101` frame (`774.433s`, `2179` từ), `lint 38 PASS / 0 FAIL`, `verify PASS`, `ASR flagged=5, chưa xem xét=0`.
- **PNG đã xem:** `out/CVI/L05/frames/00023.png` (SVG khớp đúng & khớp sai quanh đường thẳng), `00086.png` (`practice#0` bảng đọc mã). Đều sạch.
- **`MUST`:**
  1. **P8 (lộ lời giải + trùng ví dụ + thiếu định dạng `stdout`):** `practice#1..2` lộ `loi_giai.py` và `n_w50=72 n_w30=567` trước `pause: 30`; `de.md` thiếu định dạng `stdout` và dùng lại đúng `w=0.5, w=0.3, s=4, p=0.99`.
  2. **P1 (`de.md`/`practice#3` + `practice#0`):** YAML dịch hoàn toàn sang tiếng Việt (*"đồng thuận mẫu ngẫu nhiên"*), không hề giới thiệu chữ **`RANSAC`**, nhưng `de.md` & `practice#3` gọi `RANSAC`, `ceil`, `ln` chưa giải thích; `practice#0` dạy `f"{val:.3f}"` và `math.log / exp / sqrt` (không dùng `exp`/`sqrt`) nhưng thiếu `math.ceil(...)`, `**`, gán tham số mặc định `s=4, p=0.99`.
  3. **P9:** Thiếu `Hai mức quy mô` ở thân bài & `recap` (thân bài `quiz#2` so sánh $w$ & số lần thử + được/mất — thân bài đạt).
  4. **`covers:`:** Khuôn mẫu `example/check/check/practice`.
- **`SHOULD`:** `curriculum` 2 mục tiêu vs YAML 4; `RANSAC` ASR 1/8 (`probes/p1`); `layout_CVI.tsv` stale.
- **Điểm đánh giá:** `P1=0`, `P8=0`, `P9_body=đạt`, `P9_recap=0`.

### `L06` — Độ sâu từ hai camera: thị sai, khớp khối và sai số tăng theo bình phương khoảng cách
- **Số liệu & máy kiểm:** `100` frame (`760.8s`, `2118` từ), `lint 36 PASS / 0 FAIL`, `verify PASS`, `ASR flagged=3, chưa xem xét=0`.
- **PNG đã xem:** `out/CVI/L06/frames/00025.png` (SVG tam giác đồng dạng hai camera), `00085.png` (`practice#0` bảng đọc mã). Đều sạch.
- **`MUST`:**
  1. **P8 (lộ lời giải + trùng ví dụ + thiếu định dạng `stdout` + `de.md` bỏ qua bước suy $d=10.5$):** `practice#1..2` lộ `loi_giai.py` và `Z2=2.0 err2=0.05m Z8=8.0 err8=0.84m` trước `pause: 30`; `de.md` thiếu định dạng `stdout`, trùng số `f=700, B=0.12, d=42, Z=2m, Z=8m` của ví dụ, và hỏi sai số khi $d$ lệch `-1` tại $Z=8\text{ m}$ mà không nêu rõ cần suy lại $d = fB/8 = 10.5$ trước.
  2. **P1 (`de.md` + `practice#0`):** `de.md` dùng `pixel`, `vs` (bài dùng `điểm ảnh`); `practice#0` dạy `f"{val:.3f}"` (lời giải dùng `:.1f` và `:.2f`).
  3. **P9:** Thiếu `Hai mức quy mô` ở thân bài & `recap` (thân bài `quiz#2` so sánh hai cỡ $B=0{,}12\text{ m}$ vs $0{,}46\text{ m}$ ở gần $0{,}5\text{ m}$ và xa $8\text{ m}$ + bảng được/mất — thân bài đạt).
  4. **`covers:`:** Khuôn mẫu `example/check/check/practice`.
- **`SHOULD`:** `hook#0` dùng `cm` không chú thích `xăng-ti-mét`; `curriculum` 2 mục tiêu vs YAML 4; `layout_CVI.tsv` stale.
- **Điểm đánh giá:** `P1=0`, `P8=0`, `P9_body=đạt`, `P9_recap=0`.

### `L07` — Học chuyển giao và tăng cường dữ liệu: khi nào tăng cường làm hỏng nhãn
- **Số liệu & máy kiểm:** `103` frame (`748.2s`, `2146` từ), `lint 34 PASS / 0 FAIL`, `verify PASS`, `ASR flagged=4, chưa xem xét=0`.
- **PNG đã xem:** `out/CVI/L07/frames/00028.png` (SVG mạng đông cứng + lớp tuyến tính cuối & trường tiếp nhận), `00043.png` (SVG biến đổi làm đổi nhãn chữ số 7 đoạn `2↔5`, `6↔9`), `00088.png` (`practice#0` bảng đọc mã). Đều sạch.
- **`MUST`:**
  1. **P8 (lộ lời giải + thiếu phần bảo toàn nhãn + trùng ví dụ + thiếu định dạng `stdout`):** `practice#1..2` lộ `loi_giai.py` và `head_params=5130` trước `pause: 30`; tiêu đề `de.md` ghi `"& bảo toàn nhãn"` nhưng thân `de.md` và `loi_giai.py` **chỉ tính `512 * 10 + 10 = 5130`**, hoàn toàn không kiểm tra bảo toàn nhãn; thiếu định dạng `stdout` và trùng đúng `512 -> 10` của ví dụ.
  2. **P1 (`practice#0`):** Dạy `f"{val:.3f}"` không dùng trong `loi_giai.py`.
  3. **P9:** Thiếu `Hai mức quy mô` ở thân bài & `recap` (thân bài `quiz#2` so sánh đóng băng lớp cuối vs tinh chỉnh khối cuối vs học cả mạng trên 2000 ảnh + bảng được/mất — thân bài đạt).
  4. **`covers:`:** Khuôn mẫu `example/check/check/practice`.
- **`SHOULD`:** `curriculum` 2 mục tiêu vs YAML 4; `ResNet` ASR 4/8 (`probes/p1`); `layout_CVI.tsv` stale.
- **Điểm đánh giá:** `P1=1`, `P8=0`, `P9_body=đạt`, `P9_recap=0`.

### `L08` — Phát hiện vật thể: Giao trên hợp, độ chính xác trung bình và ngưỡng đánh giá
- **Số liệu & máy kiểm:** `109` frame (`760.333s`, `2112` từ), `lint 41 PASS / 0 FAIL`, `verify PASS`, `ASR flagged=4, chưa xem xét=0`.
- **PNG đã xem:** `out/CVI/L08/frames/00021.png` (SVG hai hộp & đường cong chuẩn xác – độ phủ), `00052.png` (SVG AP theo nhiều ngưỡng IoU `0,5..0,95`), `00094.png` (`practice#0` bảng đọc mã). Đều sạch.
- **`MUST`:**
  1. **P8 (lộ lời giải + trùng ví dụ + thiếu định dạng `stdout`):** `practice#1..2` lộ `loi_giai.py` và `iou_diff=0.143 iou_nms=0.818` trước `pause: 30`; `de.md` thiếu định dạng `stdout` và dùng lại y nguyên 3 hộp ví dụ `(0,0,10,10), (5,5,15,15), (1,0,11,10)`.
  2. **P1 (`de.md`/`practice#3` + `practice#0`):** YAML dạy `"loại bỏ không cực đại"`, chưa từng đưa tên viết tắt **`NMS`**, nhưng `de.md` và `practice#3` dùng ngay `NMS` không chú thích; `practice#0` dạy `sum / len` (không dùng trong `loi_giai.py`) và thiếu chỉ mục tuple `a[0], a[2]`.
  3. **P9:** Thiếu `Hai mức quy mô` ở thân bài & `recap` (thân bài `quiz#2` so sánh đếm người vs robot gắp + ngưỡng 0,5 vs 0,75 + bảng đánh đổi — thân bài đạt).
  4. **`covers:`:** `[(1, 'example'), (2, 'threshold'), (3, 'check'), (4, 'practice')]` — vẫn thiếu cảnh `sym`, `pitfalls`.
- **`SHOULD`:** `curriculum` 2 mục tiêu vs YAML 4; `IoU` ASR 1/8 (`probes/p1`); `layout_CVI.tsv` stale.
- **Điểm đánh giá:** `P1=0`, `P8=0`, `P9_body=đạt`, `P9_recap=0`.

### `L09` — Phân đoạn ảnh: Giao trên hợp, hệ số chồng lấp và lớp nhỏ bị lấn át
- **Số liệu & máy kiểm:** `101` frame (`690.6s`, `1908` từ), `lint 33 PASS / 0 FAIL`, `verify PASS`, `ASR flagged=3, chưa xem xét=0`.
- **PNG đã xem:** `out/CVI/L09/frames/00022.png` (SVG mặt nạ phân đoạn `TP/FP/FN/TN`), `00085.png` (`practice#0` bảng đọc mã). Đều sạch.
- **`MUST`:**
  1. **P8 (lộ lời giải + `loi_giai.py` thiếu phép tính `de.md` yêu cầu + trùng ví dụ + thiếu định dạng `stdout`):** `practice#1..2` lộ `loi_giai.py` và `iou=0.667 dice=0.8 dice_ge_iou=1` trước `pause: 30`; `de.md` yêu cầu *"Tính IoU, Dice **và độ chính xác điểm ảnh đánh lừa khi vật chỉ chiếm 1% ảnh**"* nhưng `loi_giai.py` **không hề tính độ chính xác điểm ảnh khi vật 1%** (`mong_doi.txt` chỉ có `iou`, `dice`, `dice_ge_iou`); trùng số `TP=40, FP=10, FN=10` của ví dụ; thiếu định dạng `stdout`.
  2. **P1 (`de.md` + `practice#0`):** `de.md` dùng `vs`; `practice#0` thiếu `int(...)` và `:.1f` (chỉ giải thích `:.3f`).
  3. **P9:** Thiếu `Hai mức quy mô` ở thân bài & `recap` (thân bài `rare#0` + `quiz#2` có hai quy mô 1% vật vs 99% nền và bảng được/mất — thân bài đạt).
  4. **`covers:`:** Khuôn mẫu `example/check/check/practice`.
- **`SHOULD`:** `curriculum` 2 mục tiêu vs YAML 4; `layout_CVI.tsv` stale.
- **Điểm đánh giá:** `P1=1`, `P8=0`, `P9_body=đạt`, `P9_recap=0`.

### `L10` — Dịch chuyển miền: đo độ chính xác theo lát dữ liệu và lập kế hoạch thu mẫu
- **Số liệu & máy kiểm:** `101` frame (`740.433s`, `2117` từ), `lint 34 PASS / 0 FAIL`, `verify PASS`, `ASR flagged=2, chưa xem xét=0`.
- **PNG đã xem:** `out/CVI/L10/frames/00028.png` (SVG phân bố ngày/đêm tập thử vs triển khai), `00088.png` (`practice#0` bảng đọc mã). Đều sạch.
- **`MUST`:**
  1. **P8 (lộ lời giải + trùng ví dụ + thiếu định dạng `stdout`):** `practice#1..2` lộ `loi_giai.py` và `test_overall=90.5% deploy_real=72.5%` trước `pause: 30`; `de.md` thiếu định dạng `stdout` và trùng đúng `90%/10%, 50%/50%, 0.95/0.50` của ví dụ.
  2. **P1 (`de.md` + `practice#0`):** `de.md` dùng `vs`; `practice#0` dạy `f"{val:.3f}"` không dùng (lời giải dùng `:.1f`).
  3. **P9:** Thiếu `Hai mức quy mô` ở thân bài & `recap` (thân bài `quiz#2` so sánh đánh giá gộp vs theo từng lát và thành phố mới + bảng được/mất — thân bài đạt).
  4. **`covers:`:** Khuôn mẫu `example/check/check/practice`, thiếu `real`.
- **`SHOULD`:** `curriculum` 2 mục tiêu vs YAML 4; `layout_CVI.tsv` stale.
- **Điểm đánh giá:** `P1=1`, `P8=0`, `P9_body=đạt`, `P9_recap=0`.

### `L11` — Tình huống: khi mô hình đúng vì lý do sai
- **Số liệu & máy kiểm:** `86` frame (`614.533s`, `1712` từ), `lint 25 PASS / 0 FAIL`, `verify PASS`, `ASR flagged=2, chưa xem xét=0`.
- **PNG đã xem:** `out/CVI/L11/frames/00018.png` (SVG bò trên cỏ vs bãi biển & lối tắt), `00070.png` (`practice#0` bảng đọc mã). Đều sạch.
- **`MUST`:**
  1. **P8 (lộ lời giải + không mô phỏng như đề bài + trùng ví dụ + thiếu định dạng `stdout`):** `practice#1..2` lộ `loi_giai.py` và `spur_train=95% counterexample_beach=0%` trước `pause: 30`; `de.md` yêu cầu *"Mô phỏng mô hình dùng luật nền cỏ: đúng `95%` trên tập huấn luyện nhưng `0%` khi bò đứng trên bãi biển"*, nhưng `loi_giai.py` **không mô phỏng**, chỉ viết `train_shortcut = 0.95 * 100; beach_cows = 0.0`! Thiếu định dạng `stdout` và trùng đúng số `95%/0%` ví dụ.
  2. **P1 (`de.md`/`practice#3` + `practice#0`):** `de.md` và `practice#3` dùng **`shortcut learning`** và **`vs`** (bài dạy `"học lối tắt"`, không dạy cụm tiếng Anh `shortcut learning`); `practice#0` dạy `f"{val:.3f}"` (lời giải dùng `:.0f`).
  3. **P9:** Thiếu `Hai mức quy mô` ở thân bài & `recap` (thân bài `quiz#0..2` so sánh 3 bãi cũ vs 1 bãi mới + chọn mô hình A/B & bảng được/mất — thân bài đạt).
  4. **`covers:`:** Khuôn mẫu `example/check/check/practice`, thiếu `counterfactual`, `pitfalls`.
- **`SHOULD`:** `curriculum` 2 mục tiêu vs YAML 4; `layout_CVI.tsv` stale.
- **Điểm đánh giá:** `P1=0`, `P8=0`, `P9_body=đạt`, `P9_recap=0`.

### `L12` — Hành trình: nhận dạng ảnh trên một triệu ảnh, từ 28% lỗi năm 2010 tới 2,3% năm 2017 và sau đó
- **Số liệu & máy kiểm:** `129` frame (`1010.633s`, `2833` từ, `case: journey`), `lint 39 PASS / 0 FAIL`, `verify PASS`, `ASR flagged=4, chưa xem xét=0`.
- **PNG đã xem:** `out/CVI/L12/frames/00016.png` (SVG trục thời gian lỗi ImageNet 2010–2017), `00040.png` (SVG so sánh 3 lớp `3×3` vs 1 lớp `7×7`), `00112.png` (`practice#0` bảng đọc mã). Đều sạch.
- **`MUST`:**
  1. **P8 (lộ lời giải + thiếu bước giảm 2014→2017 / 2010→2017 + trùng ví dụ + thiếu định dạng `stdout`):** `practice#1..2` lộ `loi_giai.py` và `drop_factor=4.2x err2014=6700 err2017=2251` trước `pause: 30`; `de.md` hỏi *"Tính hệ số giảm lỗi từ `28.2% -> 6.7% -> 2.251%`"* nhưng `loi_giai.py` chỉ tính `28.2 / 6.7` (`4.2x`), bỏ sót chặng `-> 2.251%` (`12.5x` hoặc `3.0x`); thiếu định dạng `stdout` và trùng y nguyên số liệu bài học.
  2. **P1 (`de.md`/`practice#3` + `practice#0`):** `de.md` và `practice#3` dùng **`top-5`** chưa từng xuất hiện trong thân bài (bài dạy `"lỗi năm đáp án"`); `practice#0` dạy `f"{val:.3f}"` (lời giải dùng `:.1f`) và thiếu `int(round(...))`.
  3. **P9:** Thiếu `<p class="note"><b>Hai mức quy mô:</b> ...` trong thân bài và `recap` (dù thân bài `stage1..6` & `quiz#2` làm rất tốt việc so sánh quy mô ImageNet 1 triệu ảnh với bài toán 3000 ảnh + đánh đổi — thân bài đạt).
  4. **`covers:`:** `[(1, 'stage1'), (2, 'stage2'), (3, 'practice')]` — mục tiêu 1 là *kể sáu chặng 2010–2020* và mục tiêu 2 là *tính lại 4 đại lượng (`4,2 lần`, `2048`, `27C² vs 49C²`, `83% → 72%`)* nhưng chỉ trỏ tới `stage1`, `stage2` (bỏ sót `stage3..stage6`, `check`).
- **`SHOULD`:** Độ dài `2833` từ (~`18.9` phút > 2300 từ, nhưng hợp lệ theo ngoại lệ `case: journey`); đối chiếu `curriculum` (`2010–2017` ở `cvi.yaml` vs `2010–2020` ở YAML); `layout_CVI.tsv` stale.
- **Điểm đánh giá:** `P1=0`, `P8=0`, `P9_body=đạt`, `P9_recap=0`.

---

## 4. Danh sách 34 PNG đã mở xem trực tiếp

- **L00:** `out/CVI/L00/frames/00031.png`, `00035.png`, `00095.png`
- **L01:** `out/CVI/L01/frames/00023.png`, `00054.png`, `00084.png`
- **L02:** `out/CVI/L02/frames/00018.png`, `00055.png`, `00085.png`
- **L03:** `out/CVI/L03/frames/00026.png`, `00043.png`, `00086.png`
- **L04:** `out/CVI/L04/frames/00017.png`, `00033.png`, `00072.png`
- **L05:** `out/CVI/L05/frames/00023.png`, `00086.png`
- **L06:** `out/CVI/L06/frames/00025.png`, `00085.png`
- **L07:** `out/CVI/L07/frames/00028.png`, `00043.png`, `00088.png`
- **L08:** `out/CVI/L08/frames/00021.png`, `00052.png`, `00094.png`
- **L09:** `out/CVI/L09/frames/00022.png`, `00085.png`
- **L10:** `out/CVI/L10/frames/00028.png`, `00088.png`
- **L11:** `out/CVI/L11/frames/00018.png`, `00070.png`
- **L12:** `out/CVI/L12/frames/00016.png`, `00040.png`, `00112.png`

---

## 5. Việc cần sửa trước khi tái kiểm định (`NO-GO` → `GO`)

1. **Sửa `P8` toàn khóa (`L00–L12`):**
   - Gỡ bỏ `practice#1` (`loi_giai.py`) và `practice#2` (`mong_doi.txt`) khỏi **trước** `pause: 30` ở `L01–L12` (chỉ gợi ý đề + đặt `pause` rồi mới hiện kiểm chứng/đầu ra, hoặc đối chiếu kiểu `L00`).
   - Chuẩn hóa lại 13 cặp `de.md` + `loi_giai.py` + `mong_doi.txt`: ghi rõ định dạng `stdout`, dùng **số liệu mới khác ví dụ trong bài**, và vá dứt điểm các lỗi logic (`L00` GiB→MiB & giải thích gamma; `L01` đổi đề sang tương quan chéo hoặc lật bộ lọc 180° thành `-40` & tính thật vùng phẳng; `L02` đồng bộ `t=12` hay `t=49`; `L06` ghi đủ `d=10.5` hoặc hướng dẫn suy; `L07` bổ sung kiểm tra bảo toàn nhãn hoặc bỏ khỏi tiêu đề; `L09` bổ sung tính độ chính xác điểm ảnh khi vật 1%; `L11` chạy mô phỏng mảng/tập mẫu thật thay vì gán hằng số; `L12` bổ sung hệ số giảm `2.251%`).
2. **Sửa `P1` toàn khóa (`L00–L12`):**
   - Bổ sung bảng đọc mã giải thích `np`, `zeros`, `dtype`, `uint8`, `nbytes` cho `L00 check#1`.
   - Đồng bộ bảng `practice#0` (`L01–L12`) khớp 100% cú pháp Python thực tế có trong lời giải (bỏ `:.3f`, `len/max/min` thừa; thêm `range()`, `int()`, `round()`, `**`, `math.ceil()`, chỉ số tuple...).
   - Thống nhất/chú thích mọi từ khóa tiếng Anh xuất hiện trong `de.md`/`practice#3` (`GiB`, `gamma`, `SIFT`, `RANSAC`, `ceil`, `ln`, `pixel`, `vs`, `NMS`, `shortcut learning`, `top-5`).
3. **Sửa `P9` toàn khóa (`L00–L12`):** Thêm `<p class="note"><b>Hai mức quy mô:</b> ...` vào cả thân bài (tăng cường 2 mức quy mô cho `L01`, `L03`) và cảnh `recap` của 13/13 bài.
4. **Sửa `covers:` & đồng bộ `curriculum`:** Ánh xạ từng mục tiêu của `L00–L12` tới đúng cảnh dạy thực sự (`sym`, `formula`, `blur`, `equalize`, `distort`, `pitfalls`, `real`, `counterfactual`, `stage3..stage6`), đồng bộ số lượng mục tiêu giữa `curriculum/cvi.yaml` và `L*.yaml`.
5. **Chạy lại layout check & rebuild:** Cập nhật `audit/layout_CVI.tsv`, sửa/rebuild và re-verify toàn khóa.
