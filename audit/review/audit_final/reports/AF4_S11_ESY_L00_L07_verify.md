# Báo cáo Kiểm định Độc lập Stage 11 — Khoá ESY (L00–L07) [AF4]

**Verdict: `NO-GO`**

Kiểm định độc lập 8 bài `L00`–`L07` khoá `ESY` (đối chiếu `curriculum/esy.yaml`, `lessons/esy/L00..L07*.yaml`, `labs/ESY/L00..L07/{de.md, loi_giai.py, mong_doi.txt}`, `out/ESY/L00..L07/{build_report.json, L*.srt, asr_report.md, frames/*.png}`, `audit/layout_ESY.tsv`, `audit/review/screen_code/ESY.yaml`, `audit/esy/verify_esy.py`) theo chuẩn AF2/AF4 (`BRIEF_R4.md`, `BRIEF_AF2.md`, `ADDENDUM.md`). Toàn bộ quá trình chỉ đọc, không sửa bất kỳ tệp nào trong kho.

---

## 1. Tỷ lệ đạt & Bảng tóm tắt chỉ số (L00–L07)

| Chỉ số | Kết quả | Tỷ lệ |
|---|---|---|
| Bài `MUST = 0` | **0 / 8** | **0,0%** |
| Bài `P1 = 2` (chuẩn P1 CHẶT) | **0 / 8** (L01 đạt P1=1; 7 bài đạt P1=0) | **0,0%** |
| Bài `P8 = 2` (thực nghiệm không lộ đáp án trước pause, đủ stdout, khác số ví dụ) | **0 / 8** (L01, L02 đạt P8=1; 6 bài đạt P8=0) | **0,0%** |
| Bài `P9 = 2` (Hai mức quy mô trong thân bài + `recap`) | **0 / 8** (L00 đạt P9=1; 7 bài đạt P9=0) | **0,0%** |
| Bài `spec_sha256` khớp `lv.spec_digest` | **8 / 8** | **100,0%** |
| Bài `L*.srt` khớp 100% `say` | **8 / 8** (0 câu lệch/thiếu) | **100,0%** |
| Bài `checks:` YAML & `verify_esy.py` PASS | **8 / 8** (145/145 checks; 72/72 `verify_esy.py`) | **100,0%** |
| Bài lab `loi_giai.py` chạy thật khớp `mong_doi.txt` | **8 / 8** | **100,0%** |
| Tổng số phát hiện `MUST` / `SHOULD` / `INFO` | **34 MUST** / **21 SHOULD** / **10 INFO** | — |

---

## 2. Bảng tổng hợp từng bài (L00–L07)

| Bài | sha16 YAML | Phút (từ) | Spec khớp | SRT khớp | Lab chạy | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng P1–P7 | Mất gốc | P8 | P9 | Bảng cách đọc phủ hết mã? | Cần biết trước / Mục kẹt chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **L00** | `94cf438432c7681a` | 9,4 (1589) | ✓ | ✓ (78/78) | ✓ | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 1 | **Không** (thiếu `=`, `int()`, `<=`, `ms` ghép f-string; thừa `.3f`) | `RAM`, `ADC`, `flash`, `\cdot`, `int()`, `<=` |
| **L01** | `72f9b634bd05028c` | 9,7 (1547) | ✓ | ✓ (82/82) | ✓ | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | GẦN | 1 | 0 | **Không** (không có bảng ở `practice`; `ops` thiếu giảng `//`, `;`) | `//`, `;` trong khối C `ops`; định dạng stdout lab |
| **L02** | `444c0bb812cf889a` | 9,3 (1532) | ✓ | ✓ (78/78) | ✓ | 0 | 2 | 1 | 2 | 2 | 2 | 1 | 10 | GẦN | 1 | 0 | **Không** (không có bảng cho C ở `isr`; không có bảng ở `practice`) | `cli()`, `sei()`, `//`, `;`, `uint16_t` cú pháp C; `raw_glitches` |
| **L03** | `307617335f8ae09e` | 8,5 (1402) | ✓ | ✓ (70/70) | ✓ | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 0 | **Không** (thiếu `_` trong `16_000_000`, `:.0f`, `:.1f`, `=`; thừa `.3f`) | `PWM`, `f_{clk}`, `16_000_000`, `:.0f`, `:.1f` |
| **L04** | `0dfbea214ff13464` | 9,3 (1447) | ✓ | ✓ (75/75) | ✓ | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 0 | **Không** (thiếu `:.2f`, `=`; thừa `.3f`) | `V_{ref}`, `lsb_mv` (`LSB`), `:.2f` |
| **L05** | `756fdeac71d3d62d` | 11,5 (1991) | ✓ | ✓ (92/92) | ✓ | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 0 | **Không** (bảng ghi `for x in ds:` & `.3f`, mã dùng `for _ in range(10):`, `+=`, `**`, `.4f`) | `←` (`assign`), `+=`, `_`, `range()`, `**`, `:.4f`, `closed_form` |
| **L06** | `75e8e9db1fa77abe` | 10,2 (1469) | ✓ | ✓ (76/76) | ✓ | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 0 | **Không** (thiếu `a, b = ...`, `int()`, `>>`) | `Q8.8` (ý nghĩa `Q` và `8.8`), `a, b = ...`, `int()`, `>>` |
| **L07** | `6152090a957b492d` | 9,8 (1614) | ✓ | ✓ (82/82) | ✓ | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 0 | **Không** (thiếu `a, b = ...`, `115_200`, `//`; thừa `.3f`) | `baud, bits_per_byte = ...`, `115_200`, `//` |

---

## 3. Kiểm tra xuyên suốt toàn cụm L00–L07

1. **Lỗi hệ thống P8 (Lộ lời giải trước `pause` & `practice#0` sai token thật — 6/8 bài `L00, L03, L04, L05, L06, L07`)**:
   - `practice#1` hiện **nguyên văn toàn bộ `loi_giai.py`** (dưới tiêu đề *"Cài đặt kiểm chứng ESY:Lxx bằng Python"*) và `practice#2` hiện **nguyên văn toàn bộ `mong_doi.txt`** (*"Đầu ra chạy thật (1 dòng)"*) **TRƯỚC** `practice#3` (bảng giao đề và `pause: 30`). Người học thấy sạch code giải và đáp án trước khi bấm dừng làm bài.
   - `practice#0` của cả 6 bài đều dán cứng một bảng mẫu có dòng ``f"{val:.3f}"`` (*Định dạng chuỗi làm tròn 3 chữ số thập phân*) và `print(...)`, trong khi 5/6 bài (`L00, L03, L04, L05, L07`) không hề dùng `.3f`, đồng thời bỏ sót hàng loạt cú pháp thật có trong `loi_giai.py` (`int()`, `<=`, `_`, `:.0f`, `:.1f`, `:.2f`, `:.4f`, `range()`, `+=`, `**`, `>>`, `//`, gán cặp `a, b = ...`).
2. **Lỗi hệ thống `de.md` thiếu định dạng `stdout` (8/8 bài)**:
   - Không một tệp `labs/ESY/L00..L07/de.md` nào nêu quy cách chuỗi `stdout` phải in (tên các khoá `key=value`, khoảng trắng, đơn vị gắn liền `ms`/`V`/`dB`/`%`, số chữ số thập phân, định dạng hex `0x...`). Người học tự viết bài (đặc biệt ở L01, L02 không lộ code trước pause) không thể viết đúng 100% để `bash labs/cham.sh` chấm PASS.
3. **Lỗi hệ thống `covers:` sai thực chất (8/8 bài)**:
   - Cả 8 bài đều ánh xạ máy móc `1 -> example (hoặc pwm ở L03), 2 -> check, 3 -> practice`, bất kể cảnh đó có thực sự dạy mục tiêu tương ứng hay không (chi tiết ở từng bài dưới đây). Tuy `lv.lint` (kiểm E51) cho qua vì chỉ kiểm động từ + `kind` cảnh, về nội dung giáo án thì sai cảnh dạy.
4. **Lỗi hệ thống `P9` ("Hai mức quy mô" trong thân bài + `recap` — 0/8 bài đạt)**:
   - Không bài nào có cảnh/mục `Hai mức quy mô` (so sánh bài toán ở ≥ 2 mức quy mô như ×1 vs ×100 vs ×10 000, chỉ ra chỗ gãy và đánh đổi, rồi chốt lại trong `recap`). Chỉ có `L00` có bảng 1 giây vs 1 giờ (`example#3`, tính tuyến tính số lần trễ 1 vs 3600) nhưng không nhắc trong `recap` và không phân tích sự thay đổi giải pháp/đánh đổi theo quy mô.
5. **Kiểm `SPELL_CANON`, `"càng "`, và ký hiệu toán thô trong `say`**:
   - **`SPELL_CANON`** (`luỹ/tùy/hủy/khỏe/logarit/tỷ/vectơ` và `khóa` vs `khoá`): **0 lỗi** trong `show`/`say` của cả 8 bài (chỉ có 1 chuỗi ghi chú lịch sử sửa trong metadata `asr_reviewed` ở `L07`, không lên video).
   - **Câu có `"càng "`**: Có đúng **1 câu** ở `L05` (`prereq#1`, `say`): *"Tiếp theo, lũy thừa của một số nhỏ hơn 1 thì càng nhân càng nhỏ."* — thiếu điều kiện số dương ($0 < x < 1$).
   - **Ký hiệu toán thô trong `say`**: **0 lỗi** trên cả 8 bài.
6. **Kiểm `audit/layout_ESY.tsv`, `audit/review/screen_code/ESY.yaml`, `out/ESY/L0x/asr_report.md`**:
   - `audit/layout_ESY.tsv`: rỗng (1 dòng trống `\r\n`).
   - `audit/review/screen_code/ESY.yaml`: ghi nhận `L01 ops 0 0` (khớp logic qua bản Python đối chiếu `L01_bits`), `L02 isr 0 0` (khớp mô phỏng `L02_torn`), và các khối `practice 1/2/4` khớp đúng `mong_doi.txt` & `loi_giai.py`; tuy nhiên thiếu mục cho bảng `practice#0` và chưa ghi nhận lỗi chú thích `sei()` ở `L02 isr`.
   - `asr_report.md`: cả 8 bài có 0 câu thiếu audio, 0 câu gắn cờ chưa xem xét (`unreviewed: 0`). Các câu gắn cờ đều là lệch ASR chuẩn đã biết (`byte` -> bay/bai, `bit` -> biết/bích, `mê-ga-héc` -> MHz, `mi li giây` -> mili giây/dây) hoặc nhầm thanh tiếng Việt của Whisper.

---

## 4. Chi tiết kiểm định từng bài (MUST / SHOULD / INFO)

### Bài L00 — `L00_he_nhung.yaml` (`sha16: 94cf438432c7681a`)
- **Thông số**: 561,2 s (9,4 phút), 78 khung, 1589 từ; `spec_sha256` khớp; `checks` 14/14 PASS; SRT 78/78 khớp; `loi_giai.py` chạy thật ra `used_ms=16 deadline_met=1 slack=4ms` khớp `mong_doi.txt`.
- **MUST**:
  1. **P8 — Lộ lời giải và đáp án trước `pause`** (`practice#1`, `#2` vs `#3`): `practice#1` chiếu nguyên văn 3 dòng code của `loi_giai.py` và `practice#2` chiếu nguyên văn `used_ms=16 deadline_met=1 slack=4ms` trước khi `practice#3` giao đề và `pause: 30`. Đề xuất: bỏ `practice#1` & `#2` (hoặc chuyển thành gợi ý/mẫu sau `pause`).
  2. **P8 — `practice#0` lệch token thật `loi_giai.py`** (`practice#0` `show`): Bảng ghi `f"{val:.3f}"` và `print(...)`, trong khi `loi_giai.py` không có `.3f` mà dùng `used = ...`, `int(used <= budget)`, `{budget-used}ms`.
  3. **P8 — `de.md` thiếu định dạng `stdout` & lệch số lượng tác vụ** (`labs/ESY/L00/de.md` dòng 1–3): Tiêu đề ghi *"3 tác vụ trong chu kỳ 20 ms"*, nhưng thân đề tính `(4 + 9 + 2 + 1 = 16 ms <= 20 ms)` có **4 số hạng**, không giải thích `1` là gì; đồng thời `de.md` không nêu định dạng `used_ms=... deadline_met=... slack=...ms`.
  4. **P1 — 4 mục chưa giảng tại chỗ** (`sym#0`, `prereq#1`, `practice#1`):
     - `sym#0` (`show`): viết tắt **`RAM`**, **`ADC`**, và **`flash`** chưa được giảng nghĩa viết tắt/chức năng tại chỗ (lời đọc nói "bộ nhớ dữ liệu" và "bộ chuyển đổi tương tự số" nhưng không gắn với tên viết tắt trên màn hình; `flash` không giải thích là bộ nhớ chương trình không mất khi tắt nguồn).
     - `prereq#1` (`show`): dùng ký hiệu `$\cdot$` (`16\,000 \cdot 10`) trong khi `assumes: ['cdot']` không hợp lệ vì L00 là bài đầu tiên (`requires: []`), chưa có bài ESY nào đứng trước giảng `\cdot`.
     - `practice#1` (`show`): dùng `int(...)`, `<=`, gán biến `=` chưa giảng trong bài hay bảng `practice#0`.
  5. **`covers:` ánh xạ sai cảnh** (`L00_he_nhung.yaml` dòng 286–292): `objective 1` ("Phân biệt vi điều khiển và máy tính đa dụng") trỏ tới `example` (thực chất là `sym`); `objective 2` ("Phân biệt thời gian thực cứng và mềm") trỏ tới `check` (thực chất là `realtime`); `objective 3` ("Hiểu thời gian thực là đúng hạn có bảo đảm...") trỏ tới `practice` (lab chỉ cộng `4+9+2+1=16<=20`, không kiểm tra trung bình vs xấu nhất; thực chất là `example`).
- **SHOULD**:
  1. **P9**: Thiếu cảnh/mục `Hai mức quy mô` trong thân bài và phần tổng kết trong `recap` (hiện chỉ có bảng 1 giây vs 1 giờ ở `example#3` để minh hoạ tích luỹ sự cố 1%, chưa phân tích quy mô thay đổi giải pháp/đánh đổi).
  2. `example#0` (`show`/`say`): dùng cụm `"bộ nhớ đệm nhanh"` (cache) chưa giải thích sơ cơ chế.
- **INFO**:
  1. Giá trị số toàn bài chính xác (`16 GB / 2 KB = 8 388 608`, `mean=1.29 ms`, `max=30 ms`, `10/1.29 ≈ 7.8`, quiz `mean=3 ms`, `max=12 ms`).

---

### Bài L01 — `L01_thanh_ghi_bit.yaml` (`sha16: 72f9b634bd05028c`)
- **Thông số**: 581,7 s (9,7 phút), 82 khung, 1547 từ; `spec_sha256` khớp; `checks` 21/21 PASS; SRT 82/82 khớp; `loi_giai.py` chạy thật ra `set=0x24 clr=0x4 tog=0xc` khớp `mong_doi.txt`.
- **MUST**:
  1. **`de.md` thiếu định dạng `stdout` & chưa nêu rõ tính nối tiếp** (`labs/ESY/L01/de.md` dòng 3): Không nêu định dạng `set=0x... clr=0x... tog=0x...` (và `hex()` Python bỏ số 0 dẫn đầu thành `0x4` thay vì `0x04`), cũng không nêu rõ 3 phép gán thực hiện **nối tiếp trên cùng biến `reg`** rồi in giá trị trung gian sau từng bước. (Vì `L01` không chiếu code hay `mong_doi.txt` trước `pause`, người học tự làm theo `de.md` chắc chắn trượt `cham.sh`!).
  2. **`covers:` ánh xạ sai cảnh** (`L01_thanh_ghi_bit.yaml` dòng 293–299): `objective 1` ("Hiểu thanh ghi ngoại vi: mỗi bit điều khiển một chân") trỏ tới `example` (cảnh dạy chính là `sym`/`intuition`); `objective 2` ("Bật, tắt, đảo, đọc một bit...") trỏ tới `check` (chỉ kiểm bật & tắt, thiếu đảo & đọc; cảnh dạy đủ 4 phép là `ops`); `objective 3` ("Tránh lỗi ghi đè cả thanh ghi") trỏ tới `practice` (cảnh dạy chính là `example` / `pitfalls`).
- **SHOULD**:
  1. **P1 (2 mục — P1=1)**: Trong khối mã C ở `ops#0`, chưa giảng ký hiệu chú thích **`//`** và dấu kết thúc lệnh **`;`** cho người mất gốc lần đầu nhìn mã C.
  2. **P9**: Hoàn toàn thiếu `Hai mức quy mô` trong thân bài và `recap` (`P9 = 0`).
- **INFO**:
  1. Không lộ code hay kết quả `mong_doi.txt` trước `pause` (`practice#0` là đề + `pause: 30`, `practice#1` mới là `mong_doi.txt`); số liệu lab (`0x04`) khác ví dụ (`145`).
  2. Các phép bit C ở `ops#0` đã kiểm chứng lại bằng mô phỏng Python: `145 -> 177 -> 145 -> 153 -> bit4=1`, hoàn toàn chính xác.

---

### Bài L02 — `L02_ngat_chong_doi.yaml` (`sha16: 444c0bb812cf889a`)
- **Thông số**: 557,6 s (9,3 phút), 78 khung, 1532 từ; `spec_sha256` khớp; `checks` 14/14 PASS; SRT 78/78 khớp; `loi_giai.py` chạy thật ra `accepted_at_ms=7 raw_glitches=1` khớp `mong_doi.txt`.
- **MUST**:
  1. **Sai kiến thức kỹ thuật về `sei()` trong khối mã C** (`isr#0` `show`, dòng 146): Viết `cli(); uint16_t x = dem; sei(); // tắt ngắt, đọc, bật lại nếu trước đó đang bật`. Thực tế trên AVR (`<avr/interrupt.h>`), `sei()` **luôn** bật bit ngắt toàn cục `I` trong `SREG`, **không** kiểm tra "nếu trước đó đang bật" (muốn giữ trạng thái trước đó phải lưu `SREG` trước `cli()` rồi phục hồi `SREG`). Đề xuất: sửa chú thích thành `// tắt ngắt, đọc, rồi bật lại ngắt` hoặc giới thiệu `SREG`.
  2. **Mâu thuẫn logic & thiếu đặc tả ở `labs/ESY/L02/{de.md, loi_giai.py, mong_doi.txt}`**:
     - `de.md` không nêu định dạng `stdout` (`accepted_at_ms=... raw_glitches=...`) và **hoàn toàn không nhắc tới `raw_glitches` là gì, đếm thế nào**.
     - `loi_giai.py` **hardcode** `raw_glitches=1` trong `print(...)` thay vì tính từ `samples`, đồng thời đếm `streak` chỉ cho `v == 1` (khác với thuật toán `alg.debounce` trong thân bài đếm `x == prev` cho cả mức 0 lẫn 1).
  3. **P1 — ≥ 3 mục chưa giảng tại chỗ** (`isr#0`, `pitfalls#0`):
     - `isr#0`: dùng `cli()`, `sei()`, `uint16_t`, `;`, `//` — chưa giảng cú pháp gọi hàm `()`, ý nghĩa tên viết tắt `cli`/`sei` (clear/set global interrupt) hay khai báo biến C (`volatile uint16_t dem;`, `uint16_t x = dem;`).
     - `pitfalls#0`: nhắc `"In ra cổng nối tiếp"` nhưng cổng nối tiếp chưa từng được giảng trước L07.
  4. **`covers:` ánh xạ sai cảnh** (`L02_ngat_chong_doi.yaml` dòng 308–314): `objective 1` ("So sánh ngắt và vòng thăm dò") trỏ `example` (cảnh dạy chính là `sym`); `objective 2` ("Viết hàm xử lý ngắt ngắn, dùng biến dùng chung an toàn") trỏ `check` (cảnh dạy chính là `isr`); `objective 3` ("Chống dội phím bằng lấy mẫu") trỏ `practice` (cảnh dạy chính là `example`).
- **SHOULD**:
  1. **Lỗi hiển thị SVG (`P3 = 1`)** trên `out/ESY/L02/frames/00035.png` và `00036.png`: Chữ số `4` trên trục mẫu (`0 1 2 3 4 5 ... 13`) hiển thị màu trắng/mờ gần như mất tương phản trên nền kem (đến `00037.png` mới rõ lại).
  2. **P9**: Thiếu `Hai mức quy mô` trong thân bài và `recap` (`P9 = 0`).
  3. `isr#0`: chú thích `uint16_t` ghi `"số nguyên không âm 16 bit"` — nên gọi chính xác là `"số nguyên không dấu 16 bit"`.
- **INFO**:
  1. Không lộ code hay đáp án trước `pause`, số liệu lab khác ví dụ trong bài.

---

### Bài L03 — `L03_dinh_thoi_pwm.yaml` (`sha16: 307617335f8ae09e`)
- **Thông số**: 512,0 s (**8,5 phút**), 70 khung, 1402 từ; `spec_sha256` khớp; `checks` 19/19 PASS; SRT 70/70 khớp; `loi_giai.py` chạy thật ra `pwm_hz=1000 duty_pct=25.6%` khớp `mong_doi.txt`.
- **MUST**:
  1. **Mâu thuẫn công thức độ rộng xung giữa `de.md`, thân bài và `loi_giai.py`/`mong_doi.txt`** (`labs/ESY/L03/de.md`, `pwm#1`, `pitfalls#2`):
     - `curriculum/esy.yaml` và tiêu đề `de.md` (cũng như bảng `practice#3`) ghi **`độ rộng 25%`** (`63 / 250 = 25,2%`, làm tròn gần 25%).
     - Thân bài `pwm#1` dạy công thức chính: $\dfrac{\text{CMP}}{\text{TOP}+1} = \dfrac{63}{250} = 25{,}2\%$.
     - Nhưng `loi_giai.py` và `mong_doi.txt` lại tính **`(63 + 1) / (249 + 1) * 100 = 25.6%`** (theo lưu ý chế độ Fast PWM của ATmega328P ở Lỗi 3), trong khi `de.md` không hề nói dùng công thức Fast PWM `(OCR + 1) / (TOP + 1)` và thậm chí không ghi định dạng `pwm_hz=... duty_pct=...%`!
  2. **P8 — Lộ lời giải và đáp án trước `pause`** (`practice#1`, `#2` vs `#3`): `practice#1` chiếu nguyên văn `loi_giai.py`, `practice#2` chiếu nguyên văn `pwm_hz=1000 duty_pct=25.6%` trước `pause: 30` ở `practice#3`. Đồng thời số liệu lab (`16 MHz, 64, TOP=249, CMP/OCR=63`) **trùng y hệt** ví dụ chính trong bài!
  3. **P8 — `practice#0` lệch token thật `loi_giai.py`**: Bảng ghi `f"{val:.3f}"` và `print(...)`, trong khi `loi_giai.py` dùng `16_000_000`, `:.0f`, `:.1f` (không dùng `.3f`).
  4. **P1 — ≥ 3 mục chưa giảng tại chỗ** (`sym#0`, `pitfalls#2,#3`, `practice#1`):
     - `PWM`: Xuất hiện trong mục tiêu và `pitfalls#2`, `#3` (`tần số PWM`, `chế độ PWM nhanh`), nhưng phần giới thiệu ở `hook#0` và `pwm` chỉ viết tiếng Việt *"điều chế độ rộng xung"* mà chưa từng gắn chữ viết tắt `(PWM)`.
     - `$f_{\text{clk}}$` (`sym#0`): Không giải thích chữ viết tắt `clk` (clock).
     - `practice#1`: dùng `16_000_000` (dấu `_` phân tách chữ số), `:.0f`, `:.1f`, phép gán `=` chưa được giảng.
  5. **`covers:` ánh xạ sai cảnh** (`L03_dinh_thoi_pwm.yaml` dòng 256–262): `objective 1` ("Tính tần số bộ định thời...") trỏ tới `pwm` (cảnh dạy tính tần số là `sym`, còn `pwm` tính độ rộng xung); `objective 3` ("Dùng PWM điều khiển độ sáng, tốc độ động cơ") trỏ tới `practice` (chỉ tính số, không đề cập động cơ/độ sáng; cảnh nói về độ sáng/động cơ là `pwm#4`).
- **SHOULD**:
  1. **Thời lượng ngắn hơn chuẩn AF2**: 512,0 s = **8,5 phút** (< 9 phút tối thiểu theo `BRIEF_AF2`).
  2. **P9**: Thiếu `Hai mức quy mô` trong thân bài và `recap` (`P9 = 0`).
  3. `de.md` dùng tên biến `OCR` (`OCR=63`) và `presc` trong khi thân bài dùng `CMP` và `N` mà không giải thích ánh xạ tên thanh ghi `OCR` với `CMP`.
- **INFO**:
  1. Các hình SVG (`00016.png`, `00020.png`) rất rõ ràng, không đè chữ, phản ánh chính xác mô hình đếm `0..TOP`.

---

### Bài L04 — `L04_adc.yaml` (`sha16: 0dfbea214ff13464`)
- **Thông số**: 555,5 s (9,3 phút), 75 khung, 1447 từ; `spec_sha256` khớp; `checks` 19/19 PASS; SRT 75/75 khớp; `loi_giai.py` chạy thật ra `lsb_mv=3.22 V512=1.65V SNR=61.96dB` khớp `mong_doi.txt`.
- **MUST**:
  1. **P8 — Lộ lời giải và đáp án trước `pause`** (`practice#1`, `#2` vs `#3`): Chiếu trọn `loi_giai.py` và `lsb_mv=3.22 V512=1.65V SNR=61.96dB` trước `pause: 30` ở `practice#3`; số liệu lab (`10-bit, 3.3 V, mã 512`) **trùng y hệt** ví dụ trong `sym#1` và `snr#0`.
  2. **P8 — `practice#0` lệch token thật & `de.md` thiếu định dạng `stdout`**: `practice#0` ghi `.3f`, trong khi `loi_giai.py` dùng `:.2f` (`{step_mv:.2f}`, `{v512:.2f}`, `{snr_db:.2f}`). `de.md` không nêu định dạng `lsb_mv=... V512=...V SNR=...dB`.
  3. **P1 — 3 mục chưa giảng tại chỗ** (`sym#0`, `practice#1`):
     - `$V_{\text{ref}}$` (`sym#0`): Dùng ký hiệu `V_ref` trên màn hình mà không ghi chú `ref` / `V_ref = điện áp tham chiếu` trong chữ trên màn hình.
     - `lsb_mv` (`practice#1`, `#2`, `#4`): Dùng viết tắt **`lsb`** (Least Significant Bit / bậc lượng tử nhỏ nhất) chưa từng được nhắc hoặc giảng ở bất kỳ đâu trong bài hay các bài trước!
     - `:.2f` và phép gán biến `=` trong `practice#1` không có trong bảng `practice#0`.
  4. **`covers:` ánh xạ sai cảnh** (`L04_adc.yaml` dòng 286–292): `objective 1` ("Đổi mã ADC ra điện áp và ngược lại") trỏ `example` (thực chất là `sym`); `objective 2` ("Tính bước lượng tử và tỉ số tín hiệu trên nhiễu...") trỏ `check` (không tính SNR; thực chất là `sym` + `snr`); `objective 3` ("Biết thêm bit không thêm độ chính xác khi nhiễu tương tự lớn") trỏ `practice` (không có nhiễu tương tự; thực chất là `example`).
- **SHOULD**:
  1. **P9**: Thiếu `Hai mức quy mô` trong thân bài và `recap` (`P9 = 0`).
  2. `quiz#2` (`show`): ghi `SNR ≈ 6,02 · 12 + 1,76 = 72,24 + 1,76 = 74 dB` (chính xác là `74,00 dB`, viết `74` ở đây đúng bằng `74,0` nhưng thiếu chữ số thập phân `.0` hoặc dấu `≈`).
- **INFO**:
  1. Đồ thị bậc ADC (`00010.png`) và sơ đồ ngăn lượng tử (`00018.png`) trực quan, không lỗi hiển thị.

---

### Bài L05 — `L05_loc_so.yaml` (`sha16: 756fdeac71d3d62d`)
- **Thông số**: 688,2 s (11,5 phút), 92 khung, 1991 từ; `spec_sha256` khớp; `checks` 19/19 PASS; SRT 92/92 khớp; `loi_giai.py` chạy thật ra `y10=0.8926 closed_form=0.8926` khớp `mong_doi.txt`.
- **MUST**:
  1. **P8 — Lộ lời giải và đáp án trước `pause`** (`practice#1`, `#2` vs `#3`): Chiếu trọn `loi_giai.py` và `y10=0.8926 closed_form=0.8926` trước `pause: 30` ở `practice#3`; số liệu lab (`alpha=0.2, y=0, x=1, 10 mẫu`) **trùng y hệt** cảnh `example`.
  2. **P8 — `practice#0` lệch token thật & `de.md` thiếu định dạng `stdout`**:
     - `practice#0` ghi `for x in ds:` và `f"{val:.3f}"`, nhưng `loi_giai.py` dùng `for _ in range(10):`, `+=`, `**`, `:.4f`, và chuỗi `closed_form=`.
     - `de.md` không nêu định dạng `y10=... closed_form=...` hay yêu cầu làm tròn 4 chữ số thập phân.
  3. **P1 — ≥ 3 mục chưa giảng tại chỗ** (`filters#2`, `pitfalls#1`, `practice#1`):
     - `←` (`assign` trong `filters#2`): khai báo trong `assumes: [assign, dots]` nhưng **không có bài ESY nào trước L05 giảng `←` hay `dots`**.
     - `+=` trong mã C ở `pitfalls#1` (`y += (x - y) / 4`) và mã Python `practice#1`: chưa giảng toán tử `+=` trong L05 (và trước đó L01 chỉ có `|=`, `&=`, `^=`).
     - `_`, `range(10)`, `**`, `:.4f`, `closed_form` trong `practice#1`: không được giảng ở bài hay bảng `practice#0`.
  4. **`covers:` ánh xạ sai cảnh** (`L05_loc_so.yaml` dòng 329–335): `objective 1` ("Chọn tần số lấy mẫu và đặt lọc tương tự trước ADC") trỏ `example` (thực chất là `sampling`); `objective 2` ("Cài lọc trung bình trượt và lọc thông thấp bậc nhất") trỏ `check` (chỉ kiểm lọc bậc nhất, không có trung bình trượt; thực chất là `filters`); `objective 3` ("Hiểu đánh đổi giữa giảm nhiễu và độ trễ") trỏ `practice` (chỉ tính bước nhảy 10 mẫu không nhiễu; thực chất là `filters`/`pitfalls`/`quiz`).
- **SHOULD**:
  1. **Câu chứa `"càng "` thiếu điều kiện** (`prereq#1`, `say`): `"Tiếp theo, lũy thừa của một số nhỏ hơn 1 thì càng nhân càng nhỏ."` — chỉ đúng với số **dương** ($0 < x < 1$), nếu số âm (vd `-2 < 1`) hoặc `0` thì mệnh đề sai. Cần bổ sung `"dương nhỏ hơn 1"`.
  2. **P9**: Thiếu `Hai mức quy mô` trong thân bài và `recap` (`P9 = 0`).
- **INFO**:
  1. Tính toán aliasing (`1 Hz` vs `3 Hz` ở `4 Hz` -> `[1, 0, -1, 0, 1]`), giảm nhiễu $\sqrt{4} = 2$, `0.8^10`, lọc nguyên bị kẹt ở `25` đều chuẩn xác.

---

### Bài L06 — `L06_dau_phay_tinh.yaml` (`sha16: 75e8e9db1fa77abe`)
- **Thông số**: 611,3 s (10,2 phút), 76 khung, 1469 từ; `spec_sha256` khớp; `checks` 19/19 PASS; SRT 76/76 khớp; `loi_giai.py` chạy thật ra `q88_a=384 q88_prod=864 val=3.375` khớp `mong_doi.txt`.
- **MUST**:
  1. **P8 — Lộ lời giải và đáp án trước `pause`** (`practice#1`, `#2` vs `#3`): Chiếu trọn `loi_giai.py` và `q88_a=384 q88_prod=864 val=3.375` trước `pause: 30` ở `practice#3`; số liệu lab (`1.5 * 2.25` Q8.8) **trùng y hệt** ví dụ `example` trong bài (và `de.md` cũng lộ sẵn số `384`, `576`, `864 = 3.375`).
  2. **P8 — `practice#0` thiếu token thật & `de.md` thiếu định dạng `stdout`**: `practice#0` chỉ có `f"{val:.3f}"` và `print(...)`, thiếu `a, b = ...`, `int(...)`, `>>`. `de.md` không nêu định dạng `q88_a=... q88_prod=... val=...`.
  3. **P1 — ≥ 3 mục chưa giảng tại chỗ** (`sym#0`, `practice#1`):
     - `Q8.8` (`sym#0`): giải thích là số 16 bit với 8 bit cuối là phần lẻ, nhưng chưa giải thích ý nghĩa ký hiệu `Q` và con số `8` đứng trước (8 bit nguyên gồm 1 bit dấu + 7 bit độ lớn, nên mới từ `-128` tới `127,996` thay vì `255`).
     - `practice#1`: dùng `a, b = ...`, `int(...)`, toán tử `>>` (trong thân bài L06 chỉ viết chữ *"dịch phải 8"*, không viết hay nhắc lại ký hiệu `>>` từ L01).
  4. **`covers:` ánh xạ sai cảnh** (`L06_dau_phay_tinh.yaml` dòng 277–283): `objective 3` ("Phân biệt tràn quay vòng và bão hoà") trỏ `practice` (lab chỉ nhân `1.5 * 2.25`, không hề có tràn hay bão hoà; cảnh dạy chính là `overflow`).
- **SHOULD**:
  1. **P9**: Thiếu `Hai mức quy mô` trong thân bài và `recap` (`P9 = 0`).
  2. Khoảng cách hiển thị nhẹ ở `quiz#0` (`00055.png`): `Lệnh động cơ $= 1{,}5 \cdot$ sai số` hiển thị dấu chấm `\cdot` dính sát chữ `sai số` (`= 1,5· sai số` thiếu khoảng trắng trước `sai số`).
- **INFO**:
  1. `source` dòng 8 ghi `"CSA bài 4 (số bù hai)"`, nhưng nội dung `prereq#1` đã tự giảng lại bù hai từ đầu (không vi phạm tham chiếu chéo cho người học).

---

### Bài L07 — `L07_uart.yaml` (`sha16: 6152090a957b492d`)
- **Thông số**: 586,6 s (9,8 phút), 82 khung, 1614 từ; `spec_sha256` khớp; `checks` 20/20 PASS; SRT 82/82 khớp; `loi_giai.py` chạy thật ra `uart_bytes_per_sec=11520` khớp `mong_doi.txt`.
- **MUST**:
  1. **P8 — Lộ lời giải và đáp án trước `pause`** (`practice#1`, `#2` vs `#3`): Chiếu trọn `loi_giai.py` và `uart_bytes_per_sec=11520` trước `pause: 30` ở `practice#3`; số liệu lab (`115 200 baud, 8N1`) **trùng y hệt** câu 1 phần `quiz` (và đáp án `11 520 byte/giây` lộ ngay ở tiêu đề `de.md`).
  2. **P8 — `practice#0` lệch token thật & `de.md` thiếu định dạng `stdout`**: `practice#0` ghi `f"{val:.3f}"` dù `loi_giai.py` chỉ in số nguyên `bps` không dùng `.3f`, đồng thời thiếu `baud, bits_per_byte = 115_200, 10` và toán tử chia nguyên `//`. `de.md` không nêu định dạng `uart_bytes_per_sec=...`.
  3. **P1 — 3 mục chưa giảng tại chỗ** (`practice#1`): Gán cặp biến `baud, bits_per_byte = ...`, dấu `_` phân tách số `115_200`, toán tử chia nguyên Python `//` (chỉ có ở `practice#1`, không giảng trong bài hay `practice#0`).
  4. **`covers:` ánh xạ sai cảnh** (`L07_uart.yaml` dòng 327–333): `objective 1` ("Đọc một khung UART 8N1") trỏ `example` (dạy sai lệch tốc độ UBRR; cảnh dạy khung 8N1 là `sym`); `objective 2` ("Tính thời gian truyền và tốc độ byte") trỏ `check` (kiểm UBRR lân cận; cảnh dạy tốc độ là `speed`); `objective 3` ("Kiểm sai lệch tốc độ do xung nhịp") trỏ `practice` (chỉ chia `115200 // 10`, không kiểm sai lệch xung nhịp; cảnh dạy là `example` / `check`).
- **SHOULD**:
  1. **P9**: Thiếu `Hai mức quy mô` trong thân bài và `recap` (`P9 = 0`).
  2. `sym#0` (`show`): ký hiệu `8N1` giải thích *"8 bit dữ liệu, không bit chẵn lẻ, 1 bit dừng"* nhưng chưa nói `N` viết tắt của `None` (không), và hàng `b0..b7` chưa ghi chú `b` = bit.
- **INFO**:
  1. Sơ đồ dạng sóng UART (`00024.png`) sạch đẹp, 3 mức lệch `0%`, `3,55%`, `6%` căn đúng ranh giới 9,5 bit và vượt khung 10 bit ở `6%`.

---

## 5. Danh sách toàn bộ PNG đã xem trực tiếp (`read_file`)

- **L00** (6 ảnh): `out/ESY/L00/frames/00023.png` (SVG intuition), `00056.png` (quiz pause), `00066.png` (`practice#0`), `00067.png` (`practice#1` lộ code), `00068.png` (`practice#2` lộ stdout), `00073.png` (recap).
- **L01** (5 ảnh): `out/ESY/L01/frames/00027.png` (SVG intuition), `00031.png` (`ops` mã C), `00065.png` (quiz pause), `00072.png` (`practice#0`), `00075.png` (`practice#1`).
- **L02** (8 ảnh): `out/ESY/L02/frames/00020.png` (SVG intuition), `00024.png` (`isr` mã C), `00035.png` (SVG example — chữ `4` trục x mờ/trắng mất tương phản), `00036.png` (SVG example — chữ `4` vẫn mờ), `00037.png` (SVG example — chữ `4` rõ lại), `00061.png` (quiz pause), `00068.png` (`practice#0`), `00071.png` (`practice#1`).
- **L03** (6 ảnh): `out/ESY/L03/frames/00016.png` (SVG intuition), `00020.png` (SVG pwm), `00051.png` (quiz pause), `00057.png` (`practice#0`), `00058.png` (`practice#1` lộ code), `00059.png` (`practice#2` lộ stdout).
- **L04** (5 ảnh): `out/ESY/L04/frames/00010.png` (SVG sym), `00018.png` (SVG intuition), `00062.png` (`practice#0`), `00063.png` (`practice#1` lộ code), `00064.png` (`practice#2` lộ stdout).
- **L05** (5 ảnh): `out/ESY/L05/frames/00038.png` (SVG intuition), `00041.png` (SVG example), `00079.png` (`practice#0`), `00080.png` (`practice#1` lộ code), `00081.png` (`practice#2` lộ stdout).
- **L06** (5 ảnh): `out/ESY/L06/frames/00017.png` (SVG intuition), `00055.png` (quiz pause — khoảng cách `\cdot` sát `sai số`), `00063.png` (`practice#0`), `00064.png` (`practice#1` lộ code), `00065.png` (`practice#2` lộ stdout).
- **L07** (5 ảnh): `out/ESY/L07/frames/00024.png` (SVG intuition), `00061.png` (quiz pause), `00070.png` (`practice#0`), `00071.png` (`practice#1` lộ code), `00072.png` (`practice#2` lộ stdout).

Tổng: **45 khung PNG** đã mở và kiểm tra trực tiếp bằng mắt. Không có khung nào bị đè chữ hay cắt công thức KaTeX; chỉ có 1 lỗi tương phản nhỏ ở chữ số `4` trục x của `L02/00035.png–00036.png`.

---

## 6. Người học kẹt ở đâu (1 dòng / bài)

- **L00**: `sym#0` (`RAM`, `ADC`, `flash`) viết tắt không giải thích tại chỗ và `prereq#1` dùng `\cdot` khi chưa có bài trước giảng; sang `practice#1` gặp `int(used <= budget)` chưa giảng và đã bị lộ đáp án trước `pause`.
- **L01**: `ops#0` gặp ký hiệu `//` và `;` của C chưa giảng; khi tự làm lab (`de.md`), không biết phải in đúng chuỗi `set=0x24 clr=0x4 tog=0xc` (dạng hex chữ thường bỏ số 0 đầu).
- **L02**: `isr#0` kẹt ở cú pháp C `volatile uint16_t dem; cli(); uint16_t x = dem; sei();` (và hiểu nhầm `sei()` kiểm tra trạng thái trước đó); khi làm lab, không biết `raw_glitches=1` lấy từ đâu vì `de.md` không định nghĩa.
- **L03**: `pitfalls#2` gặp `PWM` không nối với tên tiếng Việt đã học; sang `practice#1` gặp `16_000_000`, `:.0f`, `:.1f` chưa giảng, và khi làm lab bị rối giữa `25%` (`de.md`), `25,2%` (thân bài) và `25.6%` (`mong_doi.txt`).
- **L04**: `sym#0` gặp `$V_{\text{ref}}$` chưa gắn chú thích viết tắt; sang `practice#1` gặp `lsb_mv` (`LSB` chưa từng giảng) và `:.2f` không khớp bảng `practice#0`.
- **L05**: `filters#2` gặp ký hiệu `←` (`assign`) lần đầu trong khoá ESY dù chưa từng giảng; sang `practice#1` kẹt hàng loạt token Python chưa giảng (`_`, `range()`, `+=`, `**`, `:.4f`, `closed_form`).
- **L06**: `sym#0` chưa rõ vì sao gọi là `Q8.8` lại có cực đại `127,996` (không giải thích 1 bit dấu trong 8 bit nguyên); sang `practice#1` gặp `a, b = ...`, `int()`, `>>` chưa giảng trong bảng `practice#0`.
- **L07**: `practice#1` gặp gán cặp `baud, bits_per_byte = 115_200, 10` và phép chia nguyên `//` chưa giảng trong bảng `practice#0`; nếu tự làm từ `de.md` thì không biết định dạng `uart_bytes_per_sec=...`.
