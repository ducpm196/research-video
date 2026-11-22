# Báo cáo kiểm định độc lập WP-AF4-5 Stage 9 — Khóa `RLN` (`L00–L13`, 14 bài)

**Kết luận tổng thể: `NO-GO`**  
Toàn bộ phần toán học học tăng cường, mô phỏng, kiểm chứng độc lập (`verify_rln.py` 94/94 PASS), YAML `checks` (297/297 PASS), biên dịch video (`build_report.json` 14/14 khớp `spec_sha256` & `tts_sha256`), phụ đề (`L*.srt == say` 14/14), ASR (`0` câu chưa xem xét), thực thi lab (`14/14` khớp `mong_doi.txt`) và toàn bộ **18/18 SVG** đều sạch 100%.  
Tuy nhiên, khóa `RLN` **chưa đạt ngưỡng xuất xưởng Stage 9** do các lỗi **`MUST`** hệ thống: (1) **14/14 bài** lộ nguyên văn `loi_giai.py` ở `practice#1` và đáp án ở `practice#2` **trước** `practice#3` (`pause: 30`) — vi phạm **`P8`**; (2) **14/14 `de.md`** thiếu đặc tả định dạng chuỗi đầu ra bắt buộc và dùng thuật ngữ/viết tắt tiếng Anh chưa chú thích (`P1`); (3) **14/14 `practice#0`** dùng bảng boilerplate sai/thiếu token cú pháp thực tế (`P1`); (4) **14/14 `covers:`** gắn cứng mẫu tự động nên trỏ sai cảnh dạy thật của mục tiêu; (5) **0/14 bài** có mục `Hai mức quy mô` trong `recap` (`P9`), và 3 bài (`L05, L07, L10`) thân bài mới đạt `P9=1`.

---

## 1. Tổng hợp cổng kỹ thuật & nhất quán dữ liệu (`OBSERVED`)

| Hạng mục | Kết quả | Chi tiết quan sát |
|---|---|---|
| `audit/rln/verify_rln.py` | **94/94 PASS** | Đối chiếu độc lập `L00–L13` bằng phân số chính xác, SymPy, NumPy Monte Carlo, liệt kê xác suất |
| `tools/lv.py lint` (`L00..L13`) | **14/14 PASS** | `0 FAIL, 0 WARN` trên cả 14 đặc tả (gồm KaTeX parse) |
| Biểu thức `checks:` trong 14 YAML | **297/297 PASS** | 0 FAIL |
| `curriculum/rln.yaml` ↔ YAML | **14/14 khớp nội dung** | `title` và `objectives` khớp 14/14; **SHOULD**: `curriculum/rln.yaml` dòng 13 vẫn ghi `status: planned` |
| `build_report.json` (`spec_sha256`, `tts_sha256`) | **14/14 khớp 100%** | Dựng lúc `2026-11-20T00:31Z–00:59Z`, 1 giọng `vi-VN-NamMinhNeural` (`edge`/`edge?`), đủ 1,461/1,461 PNG |
| `out/RLN/L*/L*.srt == say` | **14/14 khớp 100%** | `0` sai khác trên toàn bộ 1,461 câu/khung |
| `out/RLN/L*/asr_report.md` | **14/14 sạch** | `thiếu audio: 0`, `chưa xem xét: 0` trên cả 14 bài (các câu gắn cờ đã đánh dấu `NOT_VERIFIED bằng tai người` theo đúng sổ lexicon) |
| `labs/RLN/L*/loi_giai.py` vs `mong_doi.txt` | **14/14 khớp stdout** | Chạy trực tiếp `.venv/Scripts/python.exe` ra đúng 100% `mong_doi.txt` |
| `audit/layout_RLN.tsv` | **STALE (SHOULD)** | Tệp rỗng 2 byte (`2026-11-19T02:46:02Z`), sinh trước lần dựng mới ngày `2026-11-20` |
| `audit/review/screen_code/RLN.yaml` | **SHOULD/INFO** | Gắn nhãn toàn bộ `practice 1 0` là `kind: other, lang: text` thay vì `kind: run, lang: python` |
| Khung hình PNG đã kiểm (`33` PNG) | **33/33 sạch** | 0 đè chữ, 0 tràn khung trên toàn bộ 18 SVG + 14 `practice#0` + 1 `practice#1` (`L00/00101.png` xác nhận trực quan lỗi lộ code trước `pause`) |

---

## 2. Kiểm tra câu `"càng ..."` và tiếng Việt trong `say`

- **Từ ngoại & ký hiệu trong `say`**: Sau khi áp dụng `lexicon_vi.yaml` + `lexicon_vi.RLN.yaml`, còn **0 từ ngoại ngoài sổ** và **0 ký hiệu LaTeX/toán thô** trong `say` ở cả 14 bài.
- **14 câu chứa `"càng"` trong `say` (`14/14` ĐẠT — đúng đơn điệu, tự nhiên, không ngược chiều)**:
  1. `L00 pitfalls#3`: *"Ở nhiệm vụ có lượt chơi kết thúc, đường càng dài càng nhận thêm nhiều lần cộng 2."*
  2. `L00 quiz#2`: *"Gam-ma càng gần 1 thì nhìn càng xa, nhưng phải tính nhiều vòng hơn."*
  3. `L03 sym#1`: *"Chữ c là hệ số khám phá của công thức cận trên tin cậy, c càng lớn thì càng chịu thử tay chưa chắc."*
  4. `L03 formula#2`: *"Tay càng ít thử thì Q càng có thể lệch xa giá trị thật, nên ta cộng một phần thưởng giảm theo N, và tăng chậm theo t."*
  5. `L03 example#3`: *"Cận trên tin cậy khám phá có lý do, rồi khám phá ngày càng thưa khi đã đủ chắc, nhưng chưa bao giờ dừng hẳn, vì lôgarit của t vẫn tăng chậm."*
  6. `L03 recap#0`: *"Cận trên tin cậy cộng điểm cho tay chưa chắc, rồi khám phá ngày càng thưa."*
  7. `L09 prereq#1`: *"Gam-ma là hệ số chiết khấu, một số từ 0 tới 1, làm phần thưởng càng ở xa càng được tính nhẹ đi."*
  8. `L10 prereq#1`: *"Xác suất càng gần 1 thì âm lôgarit càng gần 0."*
  9. `L10 pitfalls#1`: *"Nó chỉ học từ các câu người đã chấm, nên chính sách được tối ưu càng mạnh càng dễ viết những câu lạ mà mô hình cho điểm cao nhầm."*
  10. `L11 concept#0`: *"Thứ ba là vòng phản hồi tự khuếch đại, quảng cáo phổ biến được in to hơn nên càng phổ biến hơn."*
  11. `L11 example#2`: *"Quay vòng thì cộng 200 số hạng bị chiết khấu ngày càng mạnh, chỉ được khoảng 19 phẩy 6, nên lần này về đích thắng."*
  12. `L12 pitfalls#0`: *"Bài học sai thứ nhất, nhật ký càng lớn càng đủ, trong khi phải có ngẫu nhiên hoá."* (trích ngộ nhận để bác bỏ ngay).
  13. `L13 hook#0`: *"Hôm nay ta đi qua năm chặng đó, xem mỗi chặng vướng ở đâu, xử lý ra sao, và vì sao càng về sau, vấn đề lớn nhất lại là đo cho đúng."*
  14. `L13 recap#1`: *"Điều cần mang theo, càng lớn thì cái khó càng chuyển từ làm cho nó học được sang đo cho đúng."*

---

## 3. Tỷ lệ `P1`, `P8`, `P9` toàn khóa (`L00–L13`)

| Chỉ số | Tỷ lệ đạt chuẩn | Phân bố chi tiết |
|---|---|---|
| **`P1 = 2`** (chuẩn chặt tính cả `practice#0` & `de.md`) | **0/14 (0%)** *(thân bài chính: **14/14 = 100%** đạt `P1=2`)* | `P1=2`: **0** · `P1=1`: **6** (`L00, L01, L04, L05, L06, L11`) · `P1=0`: **8** (`L02, L03, L07, L08, L09, L10, L12, L13`) |
| **`P8 = 2`** (thực nghiệm tự làm độc lập, không lộ giải) | **0/14 (0%)** *(có lab chạy thật: **14/14 = 100%**)* | **14/14** đạt `P8=1*`: có đủ lab chạy khớp, nhưng **14/14** lộ trọn `loi_giai.py` ở `practice#1` và `mong_doi.txt` ở `practice#2` trước `pause: 30`, **14/14** `de.md` thiếu mẫu chuỗi đầu ra (`key=value`), và **13/14** lab (trừ `L10` nhánh KL) trùng y hệt số liệu đã tính trong bài |
| **`P9 = 2`** | Thân bài: **11/14 (78,6%)** · `recap Hai mức quy mô`: **0/14 (0%)** · SVG sạch: **14/14 (100%)** | Thân bài `P9=2`: `L00–L04, L06, L08, L09, L11–L13` · Thân bài `P9=1`: `L05, L07, L10` · `recap` thiếu thẻ `Hai mức quy mô`: `14/14` |
| **`MUST = 0`** | **0/14 (0%)** | Cả 14 bài đều vướng ít nhất 3 lỗi `MUST` hệ thống (`P8` lộ `loi_giai` + `de.md` thiếu format, `covers:` sai cảnh dạy, `recap` thiếu `Hai mức quy mô`) |

### Bảng tổng hợp điểm từng bài (`L00–L13`)

| Bài | `sha16` | Thời lượng (từ / khung) | ASR cờ | `P1` (thân / chặt) | `P8` | `P9` (thân / recap / SVG) | `MUST` | `SHOULD` | `INFO` |
|---|---|---:|---:|---|---|---|---|---|---|
| `L00` | `d8c08bb707e16434` | 13,1p (2206 / 115) | 4 | 2 / **1** | **1\*** | 2 / **0** / 2 | 3 | 3 | 1 |
| `L01` | `bdddaec024e0abda` | 12,8p (2243 / 107) | 12 | 2 / **1** | **1\*** | 2 / **0** / 2 | 3 | 2 | 1 |
| `L02` | `fc830c1727581586` | 13,2p (2224 / 107) | 2 | 2 / **0** | **1\*** | 2 / **0** / 2 | 4 | 2 | 1 |
| `L03` | `4a2b2e3a83cbece7` | 12,8p (2181 / 111) | 4 | 2 / **0** | **1\*** | 2 / **0** / 2 | 4 | 2 | 1 |
| `L04` | `11f00bef89cf581f` | 11,9p (2028 / 106) | 5 | 2 / **1** | **1\*** | 2 / **0** / 2 | 3 | 3 | 1 |
| `L05` | `621050606be420f1` | 10,6p (1824 / 89) | 3 | 2 / **1** | **1\*** | **1** / **0** / 2 | 4 | 2 | 1 |
| `L06` | `65031c10e1acad20` | 12,5p (2160 / 107) | 7 | 2 / **1** | **1\*** | 2 / **0** / 2 | 4 | 2 | 1 |
| `L07` | `0f928fec575dc21d` | 12,9p (2207 / 108) | 14 | 2 / **0** | **1\*** | **1** / **0** / 2 | 4 | 2 | 1 |
| `L08` | `ba2e7d296d039cc3` | 10,3p (1752 / 86) | 10 | 2 / **0** | **1\*** | 2 / **0** / 2 | 4 | 2 | 1 |
| `L09` | `c6e68e4881386fe8` | 12,2p (2208 / 102) | 1 | 2 / **0** | **1\*** | 2 / **0** / 2 | 4 | 2 | 1 |
| `L10` | `2c720e21c4bc5d2f` | 12,9p (2108 / 107) | 17 | 2 / **0** | **1\*** | **1** / **0** / 2 | 4 | 2 | 1 |
| `L11` | `83b1afcd85987e91` | 10,6p (1768 / 92) | 1 | 2 / **1** | **1\*** | 2 / **0** / 2 | 3 | 3 | 1 |
| `L12` | `51020f73157cc4ce` | 11,0p (1963 / 92) | 0 | 2 / **0** | **1\*** | 2 / **0** / 2 | 4 | 2 | 1 |
| `L13` | `752df04470d4e62b` | 16,1p (2741 / 131) | 0 | 2 / **0** | **1\*** | 2 / **0** / 2 | 4 | 3 | 1 |

---

## 4. Chi tiết kiểm định từng bài (`L00..L13`)

### Các lỗi hệ thống lặp lại ở 14/14 bài
- **`MUST-SYS-1` (`P8`)**: `practice#1` chiếu nguyên văn `loi_giai.py` và `practice#2` chiếu `mong_doi.txt` **trước** `practice#3` (`pause: 30` *"Hãy bấm tạm dừng và tự làm trước"*).
- **`MUST-SYS-2` (`P8`)**: Toàn bộ 14 tệp `labs/RLN/L*/de.md` không nêu định dạng chuỗi đầu ra bắt buộc (`key=value ...`), nên người học không thể tự làm qua `cham.sh` nếu không nhìn trộm `practice#1/#2`.
- **`MUST-SYS-3` (`P9`)**: `0/14` bài có thẻ `<p class="note"><b>Hai mức quy mô:</b> ...` trong `recap` (và 3 bài `L05, L07, L10` thân bài chưa đủ 2 mức quy mô).
- **`SHOULD-SYS-1` (`P1`)**: `practice#0` dùng bảng mẫu chung không khớp `practice#1` (`f"{val:.3f}"` có mặt ở cả 14 bài dù 10/14 bài dùng `:.1f`, `:.2f` hoặc không dùng `.3f`; chưa giải thích `bash labs/cham.sh`).
- **`SHOULD-SYS-2`**: `audit/layout_RLN.tsv` STALE từ `2026-11-19`; `curriculum/rln.yaml` vẫn để `status: planned`; `audit/review/screen_code/RLN.yaml` gán `kind: other, lang: text` cho khối mã `practice#1`.

---

### `L00` — `Bài 0 — Bài toán học tăng cường: trạng thái, hành động, phần thưởng và lợi nhuận chiết khấu`
- **Toán & nhất quán**: Khớp `curriculum`, `verify_rln.py` (`L00a–h`), `checks` 22/22 PASS, `loi_giai.py` khớp `mong_doi.txt` (`G_inf=10.0 G_0_0_10=8.1`).
- **MUST**:
  1. `MUST-SYS-1`, `MUST-SYS-2` (`practice#1` khung `00101.png` lộ nguyên code trước `practice#3` `pause: 30`; `de.md` thiếu format `G_inf=... G_0_0_10=...`).
  2. `covers:` sai cảnh dạy: `obj 1` (vòng lặp tác tử–môi trường) trỏ `example` (lẽ ra `intuition#0` + `sym#0`); `obj 3` (suy ra `1/(1-γ)` và khi nào không hội tụ) trỏ `check` (lẽ ra `formula#2-3` + `concept#0` + `pitfalls#0`); `obj 4` (chọn `γ` để chờ và cộng hằng số đổi quyết định) trỏ `practice` (lẽ ra `quiz` + `pitfalls#3`).
  3. `MUST-SYS-3`: `recap` thiếu `Hai mức quy mô`.
- **SHOULD**:
  1. `P1=1`: `practice#0` ghi `f"{val:.3f}"` (mã dùng `:.1f`) và thiếu `**`; `de.md` viết `G = sum(gamma^t * r)` nhưng chưa nêu `t` đếm từ `0` và dùng `gamma=0.9` không chú thích `γ`.
  2. Lab trùng y số liệu thân bài (`gamma=0.9`, `[0, 0, 10]`).
  3. `SHOULD-SYS-2`.
- **INFO**: `spec_sha256`, `tts_sha256`, `SRT == say` (`115/115`), `ASR` (`4` cờ, `0` chưa xem xét), 2 câu `"càng"` (`pitfalls#3`, `quiz#2`) chuẩn.
- **PNG đã xem**: `out/RLN/L00/frames/00035.png`, `00039.png`, `00100.png`, `00101.png` (sạch trực quan; `00101.png` xác nhận lộ `loi_giai`).

### `L01` — `Bài 1 — Hàm giá trị và phương trình Bellman kỳ vọng`
- **Toán & nhất quán**: Khớp `curriculum`, `verify_rln.py` (`L01a–i`), `checks` 15/15 PASS, `loi_giai.py` khớp `mong_doi.txt` (`V_A=5.263 V_B=4.737`).
- **MUST**:
  1. `MUST-SYS-1`, `MUST-SYS-2` (`de.md` thiếu format `V_A=... V_B=...`).
  2. `covers:` sai cảnh dạy: `obj 1` (định nghĩa `V, Q`) trỏ `example` (lẽ ra `sym#1`); `obj 2` (suy ra Bellman) trỏ `check` (lẽ ra `formula#0-2`); `obj 4` (dùng `Q(s,a)` quyết định đổi hành động) trỏ `practice` (lẽ ra `quiz#2`; `practice` chỉ tính `V_A, V_B`, không tính `Q`).
  3. `MUST-SYS-3`: `recap` thiếu `Hai mức quy mô` (thân bài có 2 trạng thái vs 10.000 trạng thái ở `pitfalls#3`).
- **SHOULD**:
  1. `P1=1`: `practice#0` đúng `:.3f`, nhưng chưa giảng `bash labs/cham.sh`; lab trùng y số liệu `example`.
  2. `SHOULD-SYS-2`.
- **INFO**: `spec/tts/SRT(107/107)/ASR(12 cờ, 0 chưa xem xét)` khớp.
- **PNG đã xem**: `out/RLN/L01/frames/00023.png`, `00027.png`, `00092.png` (sạch).

### `L02` — `Bài 2 — Lặp chính sách và tốc độ hội tụ của lặp giá trị`
- **Toán & nhất quán**: Khớp `curriculum`, `verify_rln.py` (`L02a–i`), `checks` 19/19 PASS, `loi_giai.py` khớp `mong_doi.txt` (`iters_g09=66 iters_g099=688`).
- **MUST**:
  1. `MUST-SYS-1`, `MUST-SYS-2` (`de.md` thiếu format `iters_g09=... iters_g099=...`).
  2. `covers:` sai: `obj 2` (suy ra tính co) trỏ `check` (lẽ ra `formula#0-1`); `obj 4` (đọc đúng điều kiện dừng) trỏ `practice` (lẽ ra `pitfalls#3`; `practice` chỉ tính `k90, k99`).
  3. `P1=0`: `practice#0` thiếu **`math.ceil(...)`** (dù code `practice#1` gọi `math.ceil`) và ghi thừa `f"{val:.3f}"`, `exp / sqrt`; `de.md` dùng `ln(eps)/ln(gamma)`, `gamma`, `eps` không chú thích `ε, γ`.
  4. `MUST-SYS-3`: `recap` thiếu `Hai mức quy mô` (thân bài có `γ=0.9` 66 vòng vs `0.99` 688 vòng vs `0.999` 6905 vòng).
- **SHOULD**: Lab trùng số liệu `hook`; `SHOULD-SYS-2`.
- **INFO**: `spec/tts/SRT(107/107)/ASR(2 cờ, 0 chưa xem xét)` khớp.
- **PNG đã xem**: `out/RLN/L02/frames/00023.png`, `00026.png`, `00093.png` (sạch).

### `L03` — `Bài 3 — Khám phá và khai thác: kẻ cướp nhiều tay, ε-tham lam, UCB`
- **Toán & nhất quán**: Khớp `curriculum`, `verify_rln.py` (`L03a–i`), `checks` 17/17 PASS, `loi_giai.py` khớp `mong_doi.txt` (`p_best=0.91 p_other=0.01 q1=1.0`).
- **MUST**:
  1. `MUST-SYS-1`, `MUST-SYS-2` (`de.md` thiếu format `p_best=... p_other=... q1=...`).
  2. `covers:` sai cả 4 mục tiêu: `obj 1` (xác suất ε-tham lam) trỏ `example` (lẽ ra `formula#0-1` + `check` — `example` giảng UCB!); `obj 2` (trung bình cộng dồn + bước cố định) trỏ `check` (lẽ ra `prereq#0` + `pitfalls#3`); `obj 3` (tính điểm UCB) trỏ `check` (lẽ ra `formula#2-3` + `example`); `obj 4` (so sánh mất mát) trỏ `practice` (lẽ ra `pitfalls#1` + `quiz#2`).
  3. `P1=0`: `practice#0` thiếu gán nhiều biến `k, eps = 10, 0.1`, ghi thừa `f"{val:.3f}"` (mã dùng `:.2f`, `:.1f`); `de.md` dùng `eps=0.1` chưa chú thích.
  4. `MUST-SYS-3`: `recap` thiếu `Hai mức quy mô`.
- **SHOULD**: Lab trùng số liệu `formula#1`/`prereq#0`; `SHOULD-SYS-2`.
- **INFO**: `spec/tts/SRT(111/111)/ASR(4 cờ, 0 chưa xem xét)` khớp; 4 câu `"càng"` chuẩn.
- **PNG đã xem**: `out/RLN/L03/frames/00030.png`, `00033.png`, `00095.png` (sạch).

### `L04` — `Bài 4 — Học từ kinh nghiệm: Monte Carlo và sai phân thời gian TD(0)`
- **Toán & nhất quán**: Khớp `curriculum`, `verify_rln.py` (`L04a–e`), `checks` 15/15 PASS, `loi_giai.py` khớp `mong_doi.txt` (`MC=6.0 TD0=8.0`).
- **MUST**:
  1. `MUST-SYS-1`, `MUST-SYS-2` (`de.md` thiếu format `MC=... TD0=...`).
  2. `covers:` sai: `obj 3` (Ví dụ 6.4 hai đáp số khác nhau) trỏ `check` (`check` là bước ngẫu nhiên Ví dụ 6.2; Ví dụ 6.4 nằm ở `example`!); `obj 4` (chọn tốc độ học và phương pháp) trỏ `practice` (lẽ ra `pitfalls#3` + `quiz#2`).
  3. `MUST-SYS-3`: `recap` thiếu `Hai mức quy mô`.
- **SHOULD**:
  1. `P1=1`: `practice#0` ghi `f"{val:.3f}"` (mã dùng `:.1f`), dư `len / max / min`, thiếu giải thích danh sách `[4.0, 6.0, 8.0]`; `de.md` dùng `Monte Carlo`, `TD(0)`, `vs`, `gamma=0.9` không chú thích (trong `say`, bài cố tình tránh đọc `Monte Carlo` và `TD(0)`).
  2. Lab trùng số liệu `prereq#0` & `formula#3`; `SHOULD-SYS-2`.
- **INFO**: `spec/tts/SRT(106/106)/ASR(5 cờ, 0 chưa xem xét)` khớp.
- **PNG đã xem**: `out/RLN/L04/frames/00024.png`, `00091.png` (sạch).

### `L05` — `Bài 5 — Q-learning và SARSA: học ngoài chính sách và theo chính sách`
- **Toán & nhất quán**: Khớp `curriculum`, `verify_rln.py` (`L05a–e`), `checks` 15/15 PASS, `loi_giai.py` khớp `mong_doi.txt` (`q_learning=2.2 sarsa=1.8`).
- **MUST**:
  1. `MUST-SYS-1`, `MUST-SYS-2` (`de.md` thiếu format `q_learning=... sarsa=...`).
  2. `covers:` sai: `obj 1` (viết cập nhật Q-learning & SARSA) trỏ `example` (lẽ ra `formula#1-3` + `quiz#0-1` — `example` tính xác suất rơi vách); `obj 3` (phân biệt giá trị học được `-13` với điểm chạy thật `-47`) trỏ `practice` (lẽ ra `pitfalls#0,3` — `practice` chỉ tính một bước `2.2` vs `1.8`).
  3. `P1`: `de.md` dùng **`off-policy`, `on-policy`, `Q-learning`, `SARSA`, `Q_next`, `gamma=1, alpha=0.1`** — riêng `off-policy`, `on-policy` **chưa từng xuất hiện** trong bài `L05` YAML (chỉ dùng "học ngoài chính sách" / "học theo chính sách") và `SARSA` không có trong `say`.
  4. `MUST-SYS-3`: `recap` thiếu `Hai mức quy mô`, và thân bài mới chỉ so sánh đường 13 bước vs 17 bước / 100 lượt (`P9=1`, chưa có hai mức quy mô bài toán/thời gian).
- **SHOULD**: `practice#0` ghi `f"{val:.3f}"` (mã dùng `:.1f`); lab trùng số liệu `formula#3`; `SHOULD-SYS-2`.
- **INFO**: `spec/tts/SRT(89/89)/ASR(3 cờ, 0 chưa xem xét)` khớp.
- **PNG đã xem**: `out/RLN/L05/frames/00016.png`, `00076.png` (sạch).

### `L06` — `Bài 6 — Xấp xỉ hàm và mạng Q sâu: bộ nhớ phát lại, mạng mục tiêu`
- **Toán & nhất quán**: Khớp `curriculum`, `verify_rln.py` (`L06a–f`), `checks` 15/15 PASS, `loi_giai.py` khớp `mong_doi.txt` (`dqn_target=10.9 terminal_target=1.0`).
- **MUST**:
  1. `MUST-SYS-1`, `MUST-SYS-2` (`de.md` thiếu format `dqn_target=... terminal_target=...`).
  2. `covers:` sai: `obj 3` (không có mạng mục tiêu → đuổi đích di động) trỏ `check` (lẽ ra `formula#2` + `pitfalls#0`, vì `check` là đếm cặp liền nhau); `obj 4` (bộ ba nguy hiểm & đánh giá quá cao) trỏ `practice` (lẽ ra `pitfalls#2-3`).
  3. `P1`: `de.md` dùng **`DQN`, `max Q_target`, `step`, `terminal_target`, `gamma=0.99`** không chú thích (`DQN` không có trong lời đọc `L06` YAML).
  4. `MUST-SYS-3`: `recap` thiếu `Hai mức quy mô` (thân bài `P9=2`: 48 ô vs Atari `2^100`, bộ nhớ 1 triệu vs 50.000 bước).
- **SHOULD**: `practice#0` ghi `f"{val:.3f}"` (mã dùng `:.1f`); lab trùng số liệu `sym#0`/`example#0`; `SHOULD-SYS-2`.
- **INFO**: `spec/tts/SRT(107/107)/ASR(7 cờ, 0 chưa xem xét)` khớp.
- **PNG đã xem**: `out/RLN/L06/frames/00031.png`, `00094.png` (sạch).

### `L07` — `Bài 7 — Gradient chính sách REINFORCE và đường cơ sở giảm phương sai`
- **Toán & nhất quán**: Khớp `curriculum`, `verify_rln.py` (`L07a–f`), `checks` 20/20 PASS, `loi_giai.py` khớp `mong_doi.txt` (`mean=-0.50 raw_var=30.25 bas_var=0.00`).
- **MUST**:
  1. `MUST-SYS-1`, `MUST-SYS-2` (`de.md` thiếu format `mean=... raw_var=... bas_var=...`).
  2. `covers:` sai: `obj 2` (chứng minh trừ đường cơ sở không đổi kỳ vọng & tính phương sai) trỏ `check` (lẽ ra `formula#3` + `example#2-3`); `obj 3` (đường cơ sở phụ thuộc hành động làm lệch gradient) trỏ `practice` (lẽ ra `pitfalls#1` — `practice` dùng `b=11` cố định).
  3. `P1=0`: `practice#0` **thiếu `print(...)`**, **thiếu `**2`** và generator expression `(x - ... for x in xs)`, ghi `f"{val:.3f}"` (mã dùng `:.2f`) và dư `max / min`; `de.md` dùng `REINFORCE`, `baseline` chưa chú thích.
  4. `MUST-SYS-3`: `recap` thiếu `Hai mức quy mô`, thân bài chưa đối chiếu 2 mức quy mô bài toán (`P9=1`).
- **SHOULD**: Lab trùng số liệu `example`; `SHOULD-SYS-2`.
- **INFO**: `spec/tts/SRT(108/108)/ASR(14 cờ, 0 chưa xem xét)` khớp.
- **PNG đã xem**: `out/RLN/L07/frames/00027.png`, `00094.png` (sạch).

### `L08` — `Bài 8 — Diễn viên–nhà phê bình và hàm lợi thế`
- **Toán & nhất quán**: Khớp `curriculum`, `verify_rln.py` (`L08a–e`), `checks` 15/15 PASS, `loi_giai.py` khớp `mong_doi.txt` (`advantage=1.5 increase_prob=1`).
- **MUST**:
  1. `MUST-SYS-1`, `MUST-SYS-2` (`de.md` thiếu format `advantage=... increase_prob=...`).
  2. `covers:` sai: `obj 2` (chạy một bước cho cả diễn viên và nhà phê bình) trỏ `check` (lẽ ra `example#1-2` + `quiz#1`); `obj 3` (nhà phê bình sai làm diễn viên học sai kể cả lệch đều) trỏ `practice` (lẽ ra `pitfalls#0,3` — `practice` chỉ tính `adv=1.5`).
  3. `P1=0`: `practice#0` thiếu **`int(adv > 0)`** (ép kiểu boolean thành 0/1) và ghi `f"{val:.3f}"` (mã dùng `:.1f`); `de.md` dùng **`Actor-Critic`** (không có trong `L08` YAML) và `gamma=0.9` chưa chú thích.
  4. `MUST-SYS-3`: `recap` thiếu `Hai mức quy mô` (thân bài `P9=2`: lượt 10.000 bước vs lượt ngắn).
- **SHOULD**: Lab trùng số liệu `example#0`; `SHOULD-SYS-2`.
- **INFO**: `spec/tts/SRT(86/86)/ASR(10 cờ, 0 chưa xem xét)` khớp.
- **PNG đã xem**: `out/RLN/L08/frames/00016.png`, `00074.png` (sạch).

### `L09` — `Bài 9 — Tối ưu chính sách gần kề (PPO): cắt tỉ số để bước cập nhật an toàn`
- **Toán & nhất quán**: Khớp `curriculum`, `verify_rln.py` (`L09a–f`), `checks` 19/19 PASS, `loi_giai.py` khớp `mong_doi.txt` (`pos_clipped=2.4 neg_unclipped=-1.6`).
- **MUST**:
  1. `MUST-SYS-1`, `MUST-SYS-2` (`de.md` thiếu format `pos_clipped=... neg_unclipped=...`).
  2. `covers:` sai: `obj 2` (vì sao trung bình `ρ·A` ước lượng lợi thế dưới chính sách mới) trỏ `check` (lẽ ra `formula#0-1`); `obj 4` (quyết định biên cắt & số lượt tối ưu + theo dõi) trỏ `practice` (lẽ ra `pitfalls#3` + `quiz#2`).
  3. `P1=0`: `practice#0` ghi `f"{val:.3f}"` (mã dùng `:.1f`), dư `sum / len`, thiếu tham số mặc định `e=0.2` trong `lambda`; `de.md` dùng `clip(...)`, `rho`, `eps=0.2` chưa chú thích.
  4. `MUST-SYS-3`: `recap` thiếu `Hai mức quy mô` (thân bài `P9=2`: 10 lượt 320 bước vs 30 lượt 960 bước trên lô 2048).
- **SHOULD**: Lab trùng số liệu `example#0-1`; `SHOULD-SYS-2`.
- **INFO**: `spec/tts/SRT(102/102)/ASR(1 cờ, 0 chưa xem xét)` khớp; 1 câu `"càng"` chuẩn.
- **PNG đã xem**: `out/RLN/L09/frames/00028.png`, `00089.png` (sạch).

### `L10` — `Bài 10 — Học phần thưởng từ sở thích của người: mô hình Bradley–Terry và phạt độ lệch`
- **Toán & nhất quán**: Khớp `curriculum`, `verify_rln.py` (`L10a–f`), `checks` 22/22 PASS, `loi_giai.py` khớp `mong_doi.txt` (`prob=0.731 loss=0.313 kl_adj_r=1.861`; riêng `0.8/0.2` là số mới khác `0.5/0.05` trong bài).
- **MUST**:
  1. `MUST-SYS-1`, `MUST-SYS-2` (`de.md` thiếu format `prob=... loss=... kl_adj_r=...`).
  2. `covers:` sai 3 mục tiêu: `obj 2` (đạo hàm `1-σ(d)` và học từng bước) trỏ `penalty` (lẽ ra `formula` + `example` — `penalty` giảng phạt độ lệch!); `obj 3` (tính `r - β ln(π/π_gốc)` & `β` đổi chọn) trỏ `check` (lẽ ra `penalty` + `quiz#2`); `obj 4` (lỗi trộn cặp cùng câu hỏi & bỏ phạt) trỏ `practice` (lẽ ra `pitfalls#2-3`).
  3. `P1=0`: `de.md` dùng **`KL`, `pi_ref`, `loss`, `sigmoid(1)`, `Bradley-Terry`, `beta=0.1, pi=0.8, ref=0.2`** — trong đó `KL`, `pi_ref`, `loss` **chưa từng xuất hiện** trong `L10` YAML (chỉ dùng "phạt độ lệch", `π_gốc`, "mất mát"), còn `Bradley-Terry` không có trong `say`. `practice#0` ghi thừa `sqrt`.
  4. `MUST-SYS-3`: `recap` thiếu `Hai mức quy mô`, và thân bài chỉ có `K=4` (6 cặp) vs `K=9` (36 cặp) chưa gắn thời gian/quy mô huấn luyện (`P9=1`).
- **SHOULD**: Số liệu `sigmoid(1)` trùng thân bài (nhưng `kl_adj_r` đổi mới `0.8/0.2`); `SHOULD-SYS-2`.
- **INFO**: `spec/tts/SRT(107/107)/ASR(17 cờ, 0 chưa xem xét)` khớp; 2 câu `"càng"` chuẩn.
- **PNG đã xem**: `out/RLN/L10/frames/00026.png`, `00093.png` (sạch).

### `L11` — `Bài 11 — Khai thác phần thưởng: khi tác tử làm đúng điều ta viết, không phải điều ta muốn`
- **Toán & nhất quán**: Khớp `curriculum`, `verify_rln.py` (`L11a–f`), `checks` 15/15 PASS, `loi_giai.py` khớp `mong_doi.txt` (`intended=100 reward_hacked=200 broken=1`).
- **MUST**:
  1. `MUST-SYS-1`, `MUST-SYS-2` (`de.md` thiếu format `intended=... reward_hacked=... broken=...`).
  2. `covers:` sai: `obj 3` (4 nguồn khai thác) trỏ `check` (lẽ ra `concept#0`); `obj 4` (thiết kế phần thưởng theo kết quả + kiểm định tính) trỏ `practice` (lẽ ra `pitfalls` + `quiz#2`).
  3. `MUST-SYS-3`: `recap` thiếu `Hai mức quy mô` (thân bài `P9=2`: 20 vs 1000 bước, đánh đổi ở `quiz#2`).
- **SHOULD**:
  1. `P1=1`: `practice#0` ghi `f"{val:.3f}"` (mã chỉ in số nguyên, không dùng `.3f`), thiếu **`//`** (chia lấy nguyên) và **`int(exploit_loop > finish)`**.
  2. Lab trùng số liệu `example#0-1`; `SHOULD-SYS-2`.
- **INFO**: `spec/tts/SRT(92/92)/ASR(1 cờ, 0 chưa xem xét)` khớp; 2 câu `"càng"` chuẩn.
- **PNG đã xem**: `out/RLN/L11/frames/00024.png`, `00078.png` (sạch).

### `L12` — `Bài 12 — Tình huống chuyên gia: đánh giá chính sách mới từ nhật ký cũ — trọng số quan trọng và phương sai bùng nổ`
- **Toán & nhất quán**: Khớp `curriculum`, `verify_rln.py` (`L12a–f`), `checks` 18/18 PASS, `loi_giai.py` khớp `mong_doi.txt` (`w10=1024 ESS=1.006`).
- **MUST**:
  1. `MUST-SYS-1`, `MUST-SYS-2` (`de.md` thiếu format `w10=... ESS=...`).
  2. `covers:` sai: `obj 3` (trọng số nhân qua nhiều bước làm phương sai bùng nổ) trỏ `check` (lẽ ra `example#2-3` + `quiz#1`); `obj 4` (quyết định khi nào cần thử nghiệm trực tuyến có kiểm soát) trỏ `practice` (lẽ ra `pitfalls#3` + `quiz#2`).
  3. `P1=0`: `de.md` dùng **`Effective Sample Size`** (tiếng Anh chưa từng xuất hiện trong `L12` YAML, vốn dùng "số mẫu hiệu dụng" và không dùng viết tắt `ESS`); `practice#0` thiếu **`**`** (`2**10`) và generator `sum(x*x for x in w)`, dư `len / max / min`.
  4. `MUST-SYS-3`: `recap` thiếu `Hai mức quy mô` (thân bài `P9=2`: 10 lượt vs 1000 lượt vs 22 triệu trang trong 5 tuần).
- **SHOULD**: Lab dùng cùng `w=2^10=1024` như `example#2`; `SHOULD-SYS-2`.
- **INFO**: `spec/tts/SRT(92/92)/ASR(0 cờ, 0 chưa xem xét)` khớp; 1 câu `"càng"` chuẩn.
- **PNG đã xem**: `out/RLN/L12/frames/00022.png`, `00077.png` (sạch).

### `L13` — `Bài 13 — Tình huống chuyên gia theo dòng thời gian: học chơi trò Atari từ 7 trò năm 2013 tới cả 57 trò năm 2020`
- **Toán & nhất quán**: Khớp `curriculum`, `sources_L13.md`, `verify_rln.py` (`L13a–h`), `checks` 31/31 PASS, `loi_giai.py` khớp `mong_doi.txt` (`days=38.6 skiing_norm=108.3%`).
- **MUST**:
  1. `MUST-SYS-1`, `MUST-SYS-2` (`de.md` thiếu format `days=... skiing_norm=...%`).
  2. `covers:` sai cả 3 mục tiêu: `obj 1` (5 chặng 2013–2020) chỉ trỏ `stage1` (1/5 chặng; lẽ ra `intuition` + `stage1..stage5`); `obj 2` (số ngày, 29/49, lịch `ε`, điểm Skiing) chỉ trỏ `stage2` (lẽ ra `stage1` + `stage2` + `stage4` + `stage5` + `check`); `obj 3` (chọn quy trình đánh giá 1 GPU / 1 tuần) trỏ `practice` (lẽ ra `quiz`).
  3. `P1=0`: `de.md` dùng **`Atari`, `60Hz`, `fps`, `Skiing`, `Agent57`** không chú thích (`sources_L13.md` ghi rõ bài cố tình không đọc `Skiing` và `Agent57` trong `say`); `practice#0` ghi `f"{val:.3f}"` (mã dùng `:.1f`) và thiếu dấu gạch dưới trong số lớn `200_000_000`.
  4. `MUST-SYS-3`: `recap` thiếu thẻ chuẩn `Hai mức quy mô` (dù bài hành trình có đủ 5 chặng quy mô + bài toán 1 GPU / 1 tuần).
- **SHOULD**:
  1. Thời lượng `967,5s` / `2.741 từ` (> 2.300 từ — chấp nhận được với bài hành trình 5 chặng `case: journey`, nhưng cần ghi nhận).
  2. Lab trùng y số liệu `stage4`/`stage5`; `SHOULD-SYS-2`.
- **INFO**: `spec/tts/SRT(131/131)/ASR(0 cờ, 0 chưa xem xét)` khớp; 2 câu `"càng"` chuẩn.
- **PNG đã xem**: `out/RLN/L13/frames/00019.png`, `00024.png`, `00112.png` (sạch).

---

## 5. Danh sách đầy đủ 33 ảnh PNG đã xem

- `out/RLN/L00/frames/`: `00035.png`, `00039.png`, `00100.png`, `00101.png`
- `out/RLN/L01/frames/`: `00023.png`, `00027.png`, `00092.png`
- `out/RLN/L02/frames/`: `00023.png`, `00026.png`, `00093.png`
- `out/RLN/L03/frames/`: `00030.png`, `00033.png`, `00095.png`
- `out/RLN/L04/frames/`: `00024.png`, `00091.png`
- `out/RLN/L05/frames/`: `00016.png`, `00076.png`
- `out/RLN/L06/frames/`: `00031.png`, `00094.png`
- `out/RLN/L07/frames/`: `00027.png`, `00094.png`
- `out/RLN/L08/frames/`: `00016.png`, `00074.png`
- `out/RLN/L09/frames/`: `00028.png`, `00089.png`
- `out/RLN/L10/frames/`: `00026.png`, `00093.png`
- `out/RLN/L11/frames/`: `00024.png`, `00078.png`
- `out/RLN/L12/frames/`: `00022.png`, `00077.png`
- `out/RLN/L13/frames/`: `00019.png`, `00024.png`, `00112.png`

---

## 6. Kết luận & Việc cần làm để chuyển sang `GO`

**Kết luận: `NO-GO`**

1. **Sửa `practice` & `labs/RLN/L*/de.md` (`L00–L13`)**: Bỏ lộ `loi_giai.py` ở `practice#1` và `mong_doi.txt` ở `practice#2` trước `pause: 30` (đổi sang kiểm chứng ví dụ số khác hoặc giao đề + định dạng đầu ra trước `pause`); cập nhật `practice#0` khớp 100% token Python thật sự dùng trong bài + `bash labs/cham.sh`; ghi rõ định dạng stdout bắt buộc và Việt hoá/chú thích mọi từ Anh/viết tắt trong 14 `de.md`.
2. **Sửa `covers:` (`L00–L13`)**: Ánh xạ lại từng mục tiêu về đúng cảnh dạy thật sự trong bài.
3. **Bổ sung `Hai mức quy mô` (`L00–L13`)**: Thêm `<p class="note"><b>Hai mức quy mô:</b> ...` trong thân bài (`L05, L07, L10`) và trong `recap` (`L00–L13`).
4. **Cập nhật sổ & dựng lại**: Chạy lại `layout_scan.py RLN`, cập nhật `audit/review/screen_code/RLN.yaml` (`kind: run, lang: python`), `curriculum/rln.yaml` (`status`), rồi dựng lại video + kiểm `spec_sha256` / `ASR`.