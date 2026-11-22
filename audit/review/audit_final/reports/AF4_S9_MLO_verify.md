# Báo cáo Kiểm định Độc lập WP-AF4-5 Stage 9 — Khoá `MLO` (`L00–L14`, 15 bài)

**Kết luận tổng thể: `NO-GO`** (kỹ thuật dựng & toán học đạt 100%, nhưng rớt các cổng sư phạm AF2/AF4-5: `covers:` lệch hàng loạt, `practice#1` lộ nguyên văn `loi_giai.py` trước `pause`, `de.md` thiếu đặc tả định dạng đầu ra & chứa thuật ngữ Anh chưa giải thích, `practice#0` sai/thiếu cú pháp, `recap` thiếu `"Hai mức quy mô"`).

---

## 1. Tóm tắt chỉ số toàn khoá (`L00–L14`)

| Hạng mục kiểm tra | Kết quả | Chi tiết |
|---|---|---|
| **Toán học & Mô phỏng (`verify_mlo.py`)** | **20/20 PASS** | Khớp độc lập toàn bộ `L00–L14` + `sources_L14.md` |
| **Biểu thức `checks:` trong YAML** | **191/191 PASS** | 100% biểu thức kiểm trong 15 tệp YAML đều đúng |
| **Build (`build_report.json`)** | **15/15 PASS** | `spec_sha256` & `tts_sha256` khớp 100%; 1 giọng `vi-VN-NamMinhNeural`; đủ khung PNG & MP4 |
| **Phụ đề (`L*.srt == say`)** | **15/15 PASS** | Khớp từng câu trên 1.259/1.259 câu |
| **ASR (`asr_report.md`)** | **15/15 PASS** | `thiếu audio: 0`, `chưa xem xét: 0`, `gone: 0` (lưu ý `L02` 16 cờ, `L11` 14 cờ đều ghi `NOT_VERIFIED bằng tai người`) |
| **Mã màn hình (`screen_code/MLO.yaml`)** | **44/44 PASS** | `0 missing`, `0 orphan`, `0 stale` |
| **Lab (`loi_giai.py == mong_doi.txt`)** | **15/15 chạy khớp** | Chạy trực tiếp `.venv/Scripts/python.exe` khớp 15/15 (lưu ý: `bash.exe` gọi `cham.sh` lỗi DLL `0xC0000142` trong môi trường sandbox này) |
| **Khung hình PNG đã xem** | **35/35 sạch** | ≥ 1 SVG + 1 bảng/`practice#0` mỗi bài: 0 đè chữ, 0 tràn khung |
| **`audit/layout_MLO.tsv`** | **STALE (SHOULD)** | Tệp rỗng (2 byte) ghi lúc `2026-11-19T02:39Z`, trước khi sửa YAML (`10:32Z`) và dựng mới (`22:40Z`) |
| **Tỷ lệ `P1 = 2` (chuẩn chặt)** | **0/15 (0%)** | `P1=2`: 0 · `P1=1`: 5 (`L00, L04, L05, L09, L12`) · `P1=0`: 10 (`L01..L03, L06..L08, L10, L11, L13, L14`) |
| **Tỷ lệ `P8 = 2`** | **15/15 có lab, 0/15 đạt chuẩn tự làm độc lập** | Có `de.md` + `loi_giai.py` + `mong_doi.txt`, nhưng **14/15** lộ trọn `loi_giai.py` ở `practice#1` trước `pause`, **15/15** `de.md` thiếu mẫu chuỗi đầu ra, **8/15** trùng số ví dụ |
| **Tỷ lệ `P9 = 2`** | **Thân bài: 13/15 (86,7%) · `recap Hai mức quy mô`: 0/15 (0%)** | Thân bài `L05` và `L01` chưa có 2 mức quy mô/thời gian (`P9=1`); **0/15** bài có mục `Hai mức quy mô` trong `recap` |
| **8 câu `"càng ..."` trong `say` (+1 tiêu đề)** | **8/8 đúng đơn điệu, 1 `SHOULD` diễn đạt** | `L04 quiz#2` (`500 lần chọn kéo điểm lên càng nhiều`) thiếu vế `"càng"` đứng trước |
| **Số bài `MUST = 0`** | **0/15 (0%)** | Mọi bài đều có ít nhất 1 lỗi `MUST` (chủ yếu ở `covers:` sai, `practice` lộ lời giải + `de.md` thiếu format, `P1` cú pháp/thuật ngữ, thiếu `Hai mức quy mô`) |

---

## 2. Kiểm tra 8 câu `"càng ..."` trong `say` (và tiêu đề)

1. **`L00 prereq#1` (`show` & `say`)**: *"nhiều số đo tụ quanh một tâm, càng xa tâm càng hiếm."* → **ĐẠT** (mật độ phân phối chuẩn giảm ngặt theo $|x-\mu|$).
2. **`L00 example#0` (`show` & `say`)**: *"điểm rác x, là con số mô hình tính từ nội dung thư, càng lớn càng giống rác"* → **ĐẠT** (đúng quy ước thang điểm $x > 0$ là rác, $-1$ thường vs $+1$ rác).
3. **`L04 prereq#1` (`say`)**: *"Mẫu càng nhiều thì điểm đo được càng ít dao động."* → **ĐẠT** ($\sigma = \sqrt{p(1-p)/n}$ giảm ngặt khi $n$ tăng).
4. **`L04 example#3` (`show` & `say`)**: *"Tập càng nhỏ và thử càng nhiều thì càng lệch... thử càng nhiều lần thì càng chắc có một lần may."* → **ĐẠT** ($\sigma \propto 1/\sqrt{n}$ và $1-(1-q)^k$ tăng theo $k$).
5. **`L04 quiz#2` (`show` & `say`)**: *"Vì 500 lần chọn kéo điểm lên càng nhiều..."* → **`SHOULD`**: câu cụt một vế `"càng"` (đọc nghe hơi gượng; nên viết *"vì chọn càng nhiều lần — ở đây 500 lần — thì điểm bị kéo lên càng nhiều"*).
6. **`L07 intuition.title` (`show` tiêu đề)**: *"Khác biệt càng nhỏ, cần càng nhiều khách"* → **ĐẠT** ($n \propto 1/\Delta^2$).
7. **`L09 hook#0` (`show` & `say`)**: *"...và lần huấn luyện sau, chúng càng được gợi ý nhiều hơn."* → **ĐẠT** (tỉ lệ hiển thị tăng 57% → 88% qua 10 vòng).
8. **`L10 prereq#0` (`show` & `say`)**: *"hiệu càng xa, phạt càng nhanh"* / *"hiệu càng xa thì phạt càng tăng nhanh."* → **ĐẠT** ($(p-y)^2$ tăng bậc hai theo $|p-y|$).
9. **`L10 sym#0` (`show` & `say`)**: *"Điểm càng nhỏ càng tốt, và 0 là hoàn hảo."* → **ĐẠT** (Brier $\ge 0$, hoàn hảo tại 0).

---

## 3. Bảng tổng hợp điểm từng bài (`L00–L14`)

| Bài | `sha16` | Thời lượng (từ) | `P1` | `P8` | `P9` (thân / recap) | `MUST` | `SHOULD` | `INFO` | PNG đã xem |
|---|---|---:|---:|---:|---|---:|---:|---:|---|
| `L00` | `95222f62875b8c15` | 9,2p (1532) | 1 | 1* | 2 / 0 (`recap` thiếu) | 3 | 1 | 1 | `00020`, `00067`, `00071`, `00072` |
| `L01` | `7795291bc2f16446` | 9,6p (1531) | 0 | 1* | 1 / 0 (`recap` thiếu) | 4 | 0 | 1 | `00025`, `00074` |
| `L02` | `be4902df6fb2f5e1` | 8,7p (1440) | 0 | 1* | 2 / 0 (`recap` thiếu) | 4 | 2 | 1 | `00019`, `00064` |
| `L03` | `a6c7bed87eefb495` | 7,8p (1254) | 0 | 1* | 2 / 0 (`recap` thiếu) | 5 | 1 | 1 | `00017`, `00062` |
| `L04` | `965803db4147ac50` | 9,2p (1545) | 1 | 1* | 2 / 0 (`recap` thiếu) | 3 | 1 | 1 | `00024`, `00069` |
| `L05` | `e4b5a44623ff016b` | 8,2p (1374) | 1 | 1* | 1 / 0 (cả thân & recap) | 4 | 1 | 1 | `00020`, `00063` |
| `L06` | `c2d63f283c89dba2` | 8,9p (1462) | 0 | 1* | 2 / 0 (`recap` thiếu) | 3 | 1 | 1 | `00005`, `00019`, `00064` |
| `L07` | `f323504488f85d67` | 9,9p (1675) | 0 | 1* | 2 / 0 (`recap` thiếu) | 3 | 0 | 1 | `00020`, `00074` |
| `L08` | `d50ea9716fd70112` | 9,3p (1457) | 0 | 1* | 2 / 0 (`recap` thiếu) | 3 | 0 | 2 | `00020`, `00070` |
| `L09` | `aa51568d61ee197e` | 8,9p (1464) | 1 | 1* | 2 / 0 (`recap` thiếu) | 3 | 1 | 1 | `00020`, `00070` |
| `L10` | `7820b19acd887b74` | 8,8p (1452) | 0 | 1* | 2 / 0 (`recap` thiếu) | 3 | 1 | 1 | `00017`, `00068` |
| `L11` | `0cb56794b96a4b70` | 8,5p (1305) | 0 | 1* | 2 / 0 (`recap` thiếu) | 3 | 2 | 1 | `00021`, `00061` |
| `L12` | `bd9d2bd7caf49058` | 9,3p (1513) | 1 | 1* | 2 / 0 (`recap` thiếu) | 3 | 0 | 2 | `00026`, `00068` |
| `L13` | `31239d986cfdcfbf` | 8,0p (1350) | 0 | 1* | 2 / 0 (`recap` thiếu) | 3 | 1 | 1 | `00015`, `00055` |
| `L14` | `58059ef90c7a6fee` | 17,3p (2998) | 0 | 1* | 2 / 0 (4 chặng, không có thẻ `Hai mức quy mô`) | 3 | 1 | 2 | `00017`, `00035`, `00052`, `00126` |

*\*Ghi chú `P8 = 1*`: Đã có đủ thư mục `labs/MLO/Lxx` (`de.md`, `loi_giai.py`, `mong_doi.txt`) chạy thật khớp 100%; bị trừ từ 2 xuống 1 vì `practice#1` in nguyên lời giải trước `pause` (14/15 bài) và `de.md` thiếu đặc tả chuỗi đầu ra (15/15 bài).*

---

## 4. Chi tiết kiểm định từng bài (`L00..L14`)

### `L00` — Vòng đời mô hình trong sản xuất và nợ kỹ thuật của hệ học máy
- **Khớp giáo án & kiểm số**: Khớp `curriculum/mlo.yaml` (`84,1% -> 67,1%`, 4 tuần 84,1→78,0%, 100k/5k dòng); `checks` 10/10 PASS; `verify_mlo` L00a PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` sai cả 3 mục tiêu: Obj 1 (*Mô tả vòng dữ liệu…*) trỏ `example` (lẽ ra `sym`); Obj 2 (*mã mô hình chỉ là phần nhỏ*) trỏ `check` (lẽ ra `sym`/`practice`); Obj 3 (*mô hình tốt lúc học có thể kém dần*) trỏ `practice` (lẽ ra `example`/`check`).
  2. `practice#1` in nguyên văn `loi_giai.py` và `practice#2` in `mong_doi.txt` trước `practice#3` (`pause: 30`); `de.md` không ghi định dạng chuỗi phải in (`ml_pct=... glue_lines=... glue_pct=...`).
  3. `recap` thiếu mục `"Hai mức quy mô"` (`P9`).
- **SHOULD**:
  1. `practice#0` ghi `f"{val:.3f}"` (3 chữ số) trong khi `practice#1` dùng `:.1f` và dấu gạch dưới số lớn `100_000`, `5_000` chưa giải thích; `de.md` dùng `ML`, `vs` chưa chú thích (`P1=1`).
- **INFO**:
  1. `spec_sha256`, `tts_sha256`, `SRT == say` (79/79), `ASR unrev=0`, PNG (`00020`, `00067`, `00071`, `00072`) sạch.

### `L01` — Tái lập: hạt giống, mã, dữ liệu, môi trường
- **Khớp giáo án & kiểm số**: Khớp `curriculum` (`seed 42 -> {0,1,4}`, `43 -> {0,2,4}`, `14 seeds -> 76,7%..96,7%`); `checks` 15/15 PASS; `verify_mlo` L01a–c PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` sai cả 3 mục tiêu: Obj 1 (*Liệt kê mọi thứ cần ghi lại*) trỏ `example` (lẽ ra `sym`); Obj 2 (*Dùng hạt giống đúng cách*) trỏ `check` (lẽ ra `example`/`pitfalls`/`practice`); Obj 3 (*Tính song song không tất định*) trỏ `practice` (lẽ ra `pitfalls`).
  2. `practice#1` lộ nguyên `loi_giai.py` trước `pause`; `de.md` thiếu mẫu đầu ra (`same_seed=... diff_seed=... s42=...`).
  3. `P1 = 0`: `practice#0` ghi thừa `f"{val:.3f}"` (mã không dùng số thực!) và bỏ sót `list(range(10))`, `random.Random(...).sample(...)`, `!=`, `==`, `int(...)`; `de.md` dùng `seed` và `random.Random(42).sample` chưa giảng.
  4. `P9`: Thân bài chỉ có 14 hạt giống trên cùng 30 mẫu (`P9=1`), `recap` thiếu `"Hai mức quy mô"`.
- **INFO**: `spec/tts/SRT(86/86)/ASR(unrev=0)` khớp; PNG (`00025`, `00074`) sạch.

### `L02` — Phiên bản hoá dữ liệu và dòng dõi
- **Khớp giáo án & kiểm số**: Khớp `curriculum` (`2e4f5668f65e` vs `6def19a1c342`, 11/12 ký tự đổi); `checks` 14/14 PASS; `verify_mlo` L02a PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` sai Obj 2 (*Truy ngược mô hình…*) trỏ `check` (lẽ ra `sym`/`quiz`) và Obj 3 (*Phân biệt tên tệp với phiên bản*) trỏ `practice` (lẽ ra `example`/`pitfalls`; lab không hề đổi tên tệp).
  2. `practice#1` lộ nguyên `loi_giai.py` trước `pause`; `de.md` thiếu mẫu đầu ra (`h1=... h2=... changed=...`).
  3. `P1 = 0`: Thân bài `pitfalls#2,#3` dùng `GB`, `MB` (`5 GB`, `50 MB`) nhưng chưa từng giảng `1 GB ≈ 1000 MB` hay `1 GB = 1 tỉ byte` (tới tận `L11` mới giảng `GB`); `practice#0` ghi thừa `f"{val:.3f}"` và thiếu `.encode()`, `.hexdigest()[:12]`, `!=`, `\n`.
  4. `recap` thiếu `"Hai mức quy mô"`.
- **SHOULD**:
  1. Thời lượng `523,1s` (**8,7 phút < 9 phút** chuẩn AF2).
  2. `ASR` gắn cờ **16 câu** vì từ `byte` đọc thô thành `"bay/bai/vai"` (`NOT_VERIFIED bằng tai người`).
- **INFO**: `spec/tts/SRT(76/76)/ASR(unrev=0)` khớp; PNG (`00019`, `00064`) sạch.

### `L03` — Kiểm thử cho hệ học máy: dữ liệu, mô hình, hành vi
- **Khớp giáo án & kiểm số**: Khớp `curriculum` (`An, Hùng, Lan`); `checks` 13/13 PASS; `verify_mlo` L03a PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` sai Obj 1 (*Viết kiểm thử lược đồ và phân bố dữ liệu*) trỏ `example` (cảnh `example` dạy kiểm thử bất biến, lược đồ chỉ ở `sym` và `quiz#2`).
  2. `practice` **thiếu hẳn 3 bước chuẩn AF2**: không có `practice#0` (bảng `"viết trong mã → đọc và hiểu là"`), không có khối mã chạy thật và đầu ra chạy thật; `de.md` thiếu mẫu đầu ra (`inv_pass=... min_slice_pass=...`).
  3. `P1 = 0`: `example#0` đưa khối mã Python (`def`, `.format()`, `{... for t in ...}`, `assert`, `f"..."`) lên màn hình mà không có bảng giải thích cú pháp cho người mất gốc; `de.md` dùng từ `test` chưa chú thích.
  4. `recap` thiếu `"Hai mức quy mô"`.
  5. Mức độ tự làm ở `de.md`: không nói rõ hàm cần viết, tên `'An','Hung','Lan'`, ngưỡng `0.80` hay giá trị `0.96, 0.72` — người học không thể tự viết ra `mong_doi.txt` nếu chỉ đọc `de.md`.
- **SHOULD**:
  1. Thời lượng `467,5s` (**7,8 phút < 9 phút**) và `1.254 từ` (< 1.300 từ).
- **INFO**: `spec/tts/SRT(72/72)/ASR(unrev=0)` khớp; PNG (`00017`, `00062`) sạch.

### `L04` — Theo dõi thí nghiệm và chọn mô hình không quá khớp tập kiểm định
- **Khớp giáo án & kiểm số**: Khớp `curriculum` (`200` mô hình trên `100` mẫu -> `0,61`); `checks` 12/12 PASS; `verify_mlo` L04a PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` sai Obj 1 (*Ghi lại mọi lần chạy…*) trỏ `example` (lẽ ra `sym`/`pitfalls`) và Obj 3 (*Giữ một tập kiểm tra chỉ dùng một lần*) trỏ `practice` (lẽ ra `sym`/`pitfalls`; lab chỉ mô phỏng 200 lần trên tập kiểm định).
  2. `practice#1` lộ nguyên `loi_giai.py` trước `pause`; `de.md` thiếu mẫu đầu ra (`true_skill=0.50 best_lucky_val=...`).
  3. `recap` thiếu `"Hai mức quy mô"`.
- **SHOULD**:
  1. `P1 = 1`: `practice#0` ghi `f"{val:.3f}"` (mã dùng `:.2f`) và dư `len / min`, trong khi thiếu `random.Random(42)`, `rng.random() < 0.5`, biểu thức sinh lặp (`for _ in range(...)`), `print(...)`.
  2. `quiz#2` câu `"càng"`: *"Vì 500 lần chọn kéo điểm lên càng nhiều"* thiếu vế `"càng"` mở đầu.
- **INFO**: `spec/tts/SRT(81/81)/ASR(unrev=0)` khớp; PNG (`00024`, `00069`) sạch.

### `L05` — Kho đặc trưng và lệch huấn luyện–phục vụ
- **Khớp giáo án & kiểm số**: Khớp `curriculum` (`70` → `2,0` và `1,0`); `checks` 10/10 PASS; `verify_mlo` L05a PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` sai Obj 3 (*Tránh dùng thông tin tương lai…*) trỏ `practice` (cảnh `practice` chỉ tính `z_train` và `z_serve_skew`, không có rò rỉ tương lai; thông tin tương lai chỉ có 1 hộp ở `pitfalls#1`).
  2. `practice#1` lộ nguyên `loi_giai.py` trước `pause`, đồng thời **lab trùng y hệt số liệu ví dụ** (`x=70, mean=50/60, std=10`); `de.md` thiếu mẫu đầu ra (`z_train=... z_serve_skew=...`).
  3. `P1` (`de.md` & `practice#0`): `de.md` dùng `mean=50`, `mean=60` (tiếng Anh chưa giải thích, bài dùng `trung bình`); `practice#0` ghi `f"{val:.3f}"` trong khi `practice#1` dùng `:.1f`.
  4. `P9`: Thân bài **không có phép đo ở 2 mức quy mô/thời gian** (`P9 = 1`) và `recap` thiếu `"Hai mức quy mô"`.
- **SHOULD**:
  1. Thời lượng `492,6s` (**8,2 phút < 9 phút**).
- **INFO**: `spec/tts/SRT(74/74)/ASR(unrev=0)` khớp; PNG (`00020`, `00063`) sạch.

### `L06` — Phục vụ mô hình: theo lô, trực tuyến, độ trễ và thông lượng
- **Khớp giáo án & kiểm số**: Khớp `curriculum` (`310 ms`, `1600/s` vs `200/s`); `checks` 12/12 PASS; `verify_mlo` L06a PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` sai Obj 1 (*Chọn dự đoán theo lô hay trực tuyến*) trỏ `example` (lẽ ra `sym`/`pitfalls`) và Obj 3 (*Đặt giới hạn thời gian chờ khi gộp lô*) trỏ `practice` (lẽ ra `example#3`/`pitfalls#3`; lab không có timeout).
  2. `practice#1` lộ nguyên `loi_giai.py` trước `pause`, đồng thời **lab trùng y hệt số liệu ví dụ** (`100 req/s`, `batch=32`, `20 ms`, `5 ms`); `de.md` thiếu mẫu đầu ra (`first_wait_ms=... single_rps=... batch_rps=...`).
  3. `P1 = 0`: `de.md` dùng `batch`, `req/s`, `vs`, `ms` chưa chú thích; `prereq#0` trên màn hình viết `1000 ms` không ghi chú `ms = mi li giây` (`say` đọc thành lời); `practice#0` ghi `f"{val:.3f}"` trong khi mã dùng `:.0f`.
  4. `recap` thiếu `"Hai mức quy mô"`.
- **SHOULD**:
  1. Thời lượng `536,6s` (**8,9 phút < 9 phút**).
- **INFO**: `spec/tts/SRT(76/76)/ASR(unrev=0)` khớp; PNG (`00005`, `00019`, `00064`) sạch.

### `L07` — Phát hành mô hình an toàn: chạy bóng, canary, thử nghiệm A/B
- **Khớp giáo án & kiểm số**: Khớp `curriculum` (`31 234`, `8158`, `14 751`); `checks` 12/12 PASS; `verify_mlo` L07a PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` sai cả 3 mục tiêu: Obj 1 (*Chạy mô hình mới song song…*) trỏ `example` (lẽ ra `sym`/`pitfalls#2`/`practice`); Obj 2 (*Đo hiệu quả kinh doanh bằng thử nghiệm hai nhóm*) trỏ `check` (lẽ ra `example`); Obj 3 (*Biết điểm ngoại tuyến tốt hơn chưa chắc tốt hơn khi chạy thật*) trỏ `practice` (lẽ ra `hook`/`pitfalls#0`).
  2. `practice#1` lộ nguyên `loi_giai.py` trước `pause`; `de.md` thiếu mẫu đầu ra (`served=old disagree=.../5`).
  3. `P1 = 0`: `de.md` dùng 3 thuật ngữ Anh chưa chú thích (`shadow mode`, `log`, `user`); `practice#0` dư `f"{val:.3f}"`, `len / max / min` và thiếu `zip(...)`, `>=`, `!=`, `int(...)`.
  4. `recap` thiếu `"Hai mức quy mô"`.
- **INFO**: `spec/tts/SRT(86/86)/ASR(unrev=0)` khớp; PNG (`00020`, `00074`) sạch.

### `L08` — Giám sát trôi dữ liệu
- **Khớp giáo án & kiểm số**: Khớp `curriculum` (`PSI ≈ 0,228`); `checks` 13/13 PASS; `verify_mlo` L08a PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` sai Obj 2 (*Chọn đặc trưng và ngưỡng cần theo dõi*) trỏ `check` (lẽ ra `sym`/`pitfalls#2,#3`) và Obj 3 (*Biết trôi đầu vào chưa chắc làm mô hình kém đi*) trỏ `practice` (lẽ ra `pitfalls#0`).
  2. `practice#1` lộ nguyên `loi_giai.py` trước `pause`, đồng thời **lab trùng y hệt số liệu ví dụ** (`[0.25]*4` vs `[0.1, 0.2, 0.3, 0.4]`); `de.md` thiếu mẫu đầu ra (`psi=... alert_moderate=...`).
  3. `P1 = 0`: `sym#0` viết công thức `\text{PSI} = ...` nhưng cả màn hình và `say` đều không giải thích `PSI` là viết tắt của gì (`say` bỏ qua hẳn chữ `PSI`); `de.md` dùng `PSI = sum((cur - exp) * ln(cur / exp))` toàn tên biến/hàm tiếng Anh chưa chú thích; `practice#0` dư `exp / sqrt`, `len / max / min`, thiếu `zip(...)`, `0.1 <= psi < 0.25`, `print(...)`.
  4. `recap` thiếu `"Hai mức quy mô"`.
- **INFO**: `spec/tts/SRT(82/82)/ASR(unrev=0)` khớp; PNG (`00020`, `00070`) sạch; trong `L08`, `f"{val:.3f}"` khớp với `psi:.3f`.

### `L09` — Trôi khái niệm, vòng phản hồi và huấn luyện lại
- **Khớp giáo án & kiểm số**: Khớp `curriculum` (`88%` sau 10 vòng, `60/60/10/10/10` sau 5 vòng); `checks` 11/11 PASS; `verify_mlo` L09a PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` sai Obj 1 (*Phân biệt trôi dữ liệu và trôi khái niệm*) trỏ `example` (cảnh `example` dạy vòng phản hồi; trôi dữ liệu vs khái niệm nằm ở `sym` và `quiz#2`) và Obj 3 (*Huấn luyện lại có kiểm tra trước khi thay*) trỏ `practice` (lẽ ra `pitfalls#0`).
  2. `practice#1` lộ nguyên `loi_giai.py` trước `pause`; `de.md` thiếu mẫu đầu ra (`clicks=... top2_share=...%`).
  3. `recap` thiếu `"Hai mức quy mô"`.
- **SHOULD**:
  1. `P1 = 1`: `de.md` dùng `top-2` chưa chú thích; `practice#0` ghi `f"{val:.3f}"` (mã dùng `:.1f`), dư `len / max / min`, thiếu `range(10)`, `sorted(..., key=..., reverse=True)[:2]`, `print(...)`.
  2. Thời lượng `535,0s` (**8,9 phút < 9 phút**).
- **INFO**: `spec/tts/SRT(83/83)/ASR(unrev=0)` khớp; PNG (`00020`, `00070`) sạch.

### `L10` — Hiệu chuẩn xác suất
- **Khớp giáo án & kiểm số**: Khớp `curriculum` (`Brier = 0,125`); `checks` 12/12 PASS; `verify_mlo` L10a PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` sai Obj 1 (*Hiểu hiệu chuẩn là gì*) trỏ `example` (lẽ ra `sym`/`intuition`), Obj 2 (*Tính điểm Brier*) trỏ `check` (lẽ ra `example`/`check`/`practice`), Obj 3 (*Độ chính xác không đo hiệu chuẩn*) trỏ `practice` (lẽ ra `pitfalls#0`).
  2. `practice#1` lộ nguyên `loi_giai.py` trước `pause`, đồng thời **lab trùng y hệt số liệu ví dụ** (`0.9, 0.8, 0.3, 0.6` và `1, 1, 0, 0`); `de.md` thiếu mẫu đầu ra (`brier=...`).
  3. `P1 = 0`: `de.md` dùng `mean((p - y)^2)` (`mean` chưa chú thích); `practice#0` ghi `f"{val:.3f}"` (mã dùng `:.4f`), dư `max / min`, thiếu `**2`, `zip(probs, y)`.
  4. `recap` thiếu `"Hai mức quy mô"`.
- **SHOULD**:
  1. Thời lượng `526,3s` (**8,8 phút < 9 phút**).
- **INFO**: `spec/tts/SRT(80/80)/ASR(unrev=0)` khớp; PNG (`00017`, `00068`) sạch.

### `L11` — Tối ưu mô hình để triển khai: lượng tử hoá, chưng cất
- **Khớp giáo án & kiểm số**: Khớp `curriculum` (`1,3 -> 83 -> 1,3071`, `28/14/7 GB`); `checks` 16/16 PASS; `verify_mlo` L11a PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` sai Obj 3 (*Biết vì sao phải đánh giá lại sau khi tối ưu*) trỏ `practice` (lẽ ra `pitfalls#0,#3`; lab chỉ tính lại số học lượng tử hoá và GB bộ nhớ).
  2. `practice#1` lộ nguyên `loi_giai.py` trước `pause`, đồng thời **lab trùng y hệt số liệu ví dụ** (`1.3`, `int8`, `7 tỉ`); `de.md` thiếu mẫu đầu ra (`q=... deq=... err=...`, `fp32_gb=... int8_gb=...`).
  3. `P1 = 0`: `example#3` dùng `float32`, `float16`, `int8` không giải nghĩa `float`/`int`; `de.md` dùng `int8`, `RAM`, `q_max=127` (`RAM` và `q_max` không có trong bài); `practice#0` ghi `f"{val:.3f}"` (mã dùng `:.4f`) và thiếu `round(...)`, `abs(...)`.
  4. `recap` thiếu `"Hai mức quy mô"`.
- **SHOULD**:
  1. Thời lượng `507,9s` (**8,5 phút < 9 phút**).
  2. `ASR` gắn cờ **14 câu** vì `bit`/`byte` đọc thô (`biết/bịch`, `bay/vai`) — `NOT_VERIFIED bằng tai người`.
- **INFO**: `spec/tts/SRT(74/74)/ASR(unrev=0)` khớp; PNG (`00021`, `00061`) sạch.

### `L12` — Thẻ mô hình, công bằng và khả năng giải thích
- **Khớp giáo án & kiểm số**: Khớp `curriculum` (`94%`, `75%`, `92,1%`); `checks` 11/11 PASS; `verify_mlo` L12a PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` sai Obj 1 (*Viết thẻ mô hình*) trỏ `example` (lẽ ra `sym`/`quiz#2`) và Obj 3 (*Bỏ cột nhạy cảm không làm mô hình công bằng*) trỏ `practice` (lẽ ra `pitfalls#0`).
  2. `practice#1` lộ nguyên `loi_giai.py` trước `pause`, đồng thời **lab trùng y hệt số liệu ví dụ** (`846/900`, `75/100`); `de.md` thiếu mẫu đầu ra (`overall=...% maj=...% min=...%`).
  3. `recap` thiếu `"Hai mức quy mô"`.
- **INFO / `P1 = 1`**:
  1. `pitfalls#3` nêu tên `Clopper–Pearson` không giải thích; `de.md` dùng `vs`; `practice#0` ghi `f"{val:.3f}"` (mã dùng `:.1f`).
  2. `spec/tts/SRT(80/80)/ASR(unrev=0)` khớp; PNG (`00026`, `00068`) sạch.

### `L13` — Bảo mật hệ học máy: đầu độc dữ liệu, rò rỉ dữ liệu huấn luyện, đầu vào đối kháng
- **Khớp giáo án & kiểm số**: Khớp `curriculum` (`99%` sạch, `75%` kích hoạt); `checks` 9/9 PASS; `verify_mlo` L13a PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` sai Obj 1 (*Liệt kê bề mặt tấn công…*) trỏ `example` (lẽ ra `sym`) và Obj 3 (*Áp dụng kiểm soát nguồn, giới hạn truy vấn, mã băm, chữ ký*) trỏ `practice` (lẽ ra `pitfalls#0..3`).
  2. `practice#1` lộ nguyên `loi_giai.py` trước `pause`, đồng thời **lab trùng y hệt số liệu ví dụ** (`396/400 = 99%`, `15/20 = 75%`); `de.md` thiếu mẫu đầu ra (`clean_acc=...% trigger_hijack=...%`).
  3. `P1 = 0`: `de.md` dùng `trigger` (`mẫu gắn trigger`, `từ khoá trigger`) và `vs` (trong bài gọi là `dấu hiệu`, chưa từng dùng/giải thích `trigger`); `practice#0` ghi `f"{val:.3f}"` (mã dùng `:.1f`).
  4. `recap` thiếu `"Hai mức quy mô"` (chữ `"ở từng quy mô"` ở `recap#2` là nhắc bài 14 sắp tới).
- **SHOULD**:
  1. Thời lượng `477,9s` (**8,0 phút < 9 phút**).
- **INFO**: `spec/tts/SRT(67/67)/ASR(unrev=0)` khớp; PNG (`00015`, `00055`) sạch.

### `L14` — Tình huống chuyên gia theo dòng thời gian: từ nợ kỹ thuật tới nền tảng học máy
- **Khớp giáo án & kiểm số**: Khớp `curriculum` & `sources_L14.md` (`[SC15]`, `[TX17]`, `[TH20]`); giữ đúng chữ *"có vẻ"* (*"apparently"*); số minh hoạ gắn nhãn rõ; `checks` 21/21 PASS; `verify_mlo` L14a–d PASS; `loi_giai.py` khớp `mong_doi.txt`.
- **MUST**:
  1. `covers:` lệch Obj 2 (chỉ trỏ `stage2`, trong khi độ trễ nằm ở `stage3`, 18 cấu hình ở `stage4`, tổng hợp ở `check`) và Obj 3 (*Chọn mức đầu tư hạ tầng hợp với quy mô đội…*) trỏ `practice` (lẽ ra `quiz`).
  2. `practice#1` lộ nguyên `loi_giai.py` trước `pause`, đồng thời **lab trùng y hệt số liệu bài** (`1500/150`, `3*3*2=18`, `5000/100000`); `de.md` thiếu mẫu đầu ra (`p999_speedup=... configs=... ml_code=...%`).
  3. `P1 = 0`: `de.md` dùng `ML`, `p99.9` (`p99.9` trong bài viết là `phân vị 99,9`, chưa giới thiệu ký hiệu `p99.9`); `practice#0` ghi `f"{val:.3f}"` (mã dùng `:.0f` và `:.1f`).
- **SHOULD**:
  1. `say` ở 6 bước (`intuition#0, stage1#1, stage2#1, stage3#2, check#0, recap#0`) viết ký hiệu `%` (`5%`, `70%`, `2%`…) thay vì `phần trăm` như `L00–L13` (TTS vẫn đọc đúng nhưng không đồng nhất quy ước `say`).
  2. `recap` tổng hợp theo 4 chặng thời gian (hợp bài hành trình), nhưng chưa có thẻ chốt dạng `"Hai mức quy mô"`.
- **INFO**: `spec/tts/SRT(143/143)/ASR(unrev=0)` khớp; PNG (`00017`, `00035`, `00052`, `00126`) sạch.

---

## 5. Danh sách ảnh PNG đã kiểm bằng mắt (35 tệp)

- `out/MLO/L00/frames/`: `00020.png`, `00067.png`, `00071.png`, `00072.png`
- `out/MLO/L01/frames/`: `00025.png`, `00074.png`
- `out/MLO/L02/frames/`: `00019.png`, `00064.png`
- `out/MLO/L03/frames/`: `00017.png`, `00062.png`
- `out/MLO/L04/frames/`: `00024.png`, `00069.png`
- `out/MLO/L05/frames/`: `00020.png`, `00063.png`
- `out/MLO/L06/frames/`: `00005.png`, `00019.png`, `00064.png`
- `out/MLO/L07/frames/`: `00020.png`, `00074.png`
- `out/MLO/L08/frames/`: `00020.png`, `00070.png`
- `out/MLO/L09/frames/`: `00020.png`, `00070.png`
- `out/MLO/L10/frames/`: `00017.png`, `00068.png`
- `out/MLO/L11/frames/`: `00021.png`, `00061.png`
- `out/MLO/L12/frames/`: `00026.png`, `00068.png`
- `out/MLO/L13/frames/`: `00015.png`, `00055.png`
- `out/MLO/L14/frames/`: `00017.png`, `00035.png`, `00052.png`, `00126.png`

---

## 6. Kết luận cuối cùng: **`NO-GO`**

Để đạt **`GO`**, cần xử lý các điểm chặn sau rồi chạy lại `layout_scan.py MLO`, `lab_gate.py MLO`, dựng lại video & ASR:
1. Sửa **`covers:`** ở `L00–L14` trỏ đúng cảnh dạy từng mục tiêu.
2. Sửa cảnh **`practice`** và **`labs/MLO/L*/de.md`**: bỏ việc lộ nguyên `loi_giai.py` ở `practice#1` trước `pause` (đổi sang kiểm chứng số liệu khác với bài lab), đổi số liệu lab ở 8 bài đang trùng ví dụ (`L05, L06, L08, L10–L14`), bổ sung đầy đủ 3 bước chuẩn AF2 cho `L03`, và ghi rõ **định dạng chuỗi đầu ra** vào mọi `de.md`.
3. Sửa **`P1`** ở `practice#0` (khớp đúng cú pháp dùng trong `practice#1`, bỏ `f"{val:.3f}"` thừa ở 13 bài, bổ sung bảng giải mã cho khối mã Python ở `L03 example#0`) và chú thích/Việt hoá toàn bộ thuật ngữ Anh ở `de.md` (`ML, seed, test, mean, batch, req/s, shadow mode, log, user, PSI, top-2, int8, RAM, q_max, trigger, p99.9`) + `GB/MB` (`L02`), `PSI` (`L08`), `float32/float16/int8` (`L11`).
4. Bổ sung mục **`Hai mức quy mô`** trong thân bài (`L05`, `L01`) và trong `recap` (`L00–L13`), đồng thời nâng độ dài các bài `< 9 phút` (`L02, L03, L05, L06, L09, L10, L11, L13`), chỉnh câu `"càng"` ở `L04 quiz#2`, và cập nhật `curriculum/mlo.yaml` (`status`) cùng `audit/layout_MLO.tsv`.