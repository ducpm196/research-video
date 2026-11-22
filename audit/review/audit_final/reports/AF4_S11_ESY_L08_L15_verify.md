# Báo cáo kiểm định độc lập WP-AF4-5 Stage 11 — ESY (L08–L15)

**Verdict: `NO-GO`**

Kiểm định độc lập 8 bài `L08..L15` của khoá `ESY` (`lessons/esy/L08_*.yaml` .. `L15_*.yaml`, `curriculum/esy.yaml`, `labs/ESY/L08..L15/`, `out/ESY/L08..L15/`, `audit/esy/verify_esy.py`, `audit/esy/sources_L15.md`, `audit/layout_ESY.tsv`, `audit/review/screen_code/ESY.yaml`) theo chuẩn AF2/AF4 (`BRIEF_R4.md`, `BRIEF_AF2.md`, `ADDENDUM.md`). Thực hiện hoàn toàn ở chế độ **CHỈ ĐỌC**, không sửa bất kỳ tệp nào.

---

## 1. Bảng tổng hợp toàn đợt (L08–L15)

| Chỉ số | Kết quả | Ghi chú |
|---|---:|---|
| Tổng số bài kiểm định | **8 / 8** (`L08..L15`) | Đọc đủ YAML, curriculum, lab, SRT, ASR, PNG |
| Số bài `MUST = 0` | **0 / 8** | Cả 8 bài đều có lỗi `MUST` (tập trung ở `covers:`, `practice` lộ lời giải trước `pause`, `de.md` thiếu định dạng `stdout` & sai lệch với `loi_giai.py`) |
| Số bài `P1 = 2` (chuẩn chặt `BRIEF_R4.md`) | **0 / 8** (`0%`) | `L13` đạt `P1 = 1` (thân bài 0 lỗi, kẹt ở bảng `practice#0` vs `practice#1`); 7 bài còn lại `P1 = 0` (nếu chỉ tính thân bài không tính khối `practice#1`: 1 bài `P1=2`, 6 bài `P1=1`, 1 bài `P1=0`) |
| Số bài `P8 = 2` (Thực nghiệm) | **0 / 8** (`0%`) | `L11` đạt `P8 = 1` (không lộ lời giải nhưng `de.md` thiếu định dạng `stdout`); 7 bài còn lại `P8 = 0` (lộ nguyên `loi_giai.py` + `mong_doi.txt` ở `practice#1/#2` TRƯỚC `pause: 30` ở `practice#3`) |
| Số bài `P9 = 2` (Quy mô / thời gian) | **6 / 8** (`75%`) | `L08, L10, L12, L13, L14, L15` đạt `P9 = 2`; `L09, L11` đạt `P9 = 1`. Không bài nào (0/8) có khung chữ `"Hai mức quy mô"` tường minh trong `recap` (trừ `L15` có 5 chặng xuyên suốt và `L12` nhắc "ngày thứ một trăm") |
| Số bài `spec_sha256` khớp `lv.spec_digest` | **8 / 8** (`100%`) | Khớp tuyệt đối 64 ký tự hex ở cả 8 `build_report.json` |
| Số bài `SRT` khớp `say` | **8 / 8** (`100%`) | Khớp 100% từng câu, không thiếu câu, không sai số |
| Số bài `checks:` & `verify_esy.py` PASS | **8 / 8** (`100%`) | Tổng `137/137` biểu thức `checks:` trong YAML + `72/72 PASS` trong `audit/esy/verify_esy.py` |
| Số bài `lv.lint` (0 err, 0 warn) | **8 / 8** (`100%`) | Lint tự động pass 0 err / 0 warn, nhưng không bắt được lỗi ngữ nghĩa của `covers:` và lỗi P8 lộ code trước `pause` |
| Số bài `lab` chạy thật khớp `mong_doi.txt` | **8 / 8** (`100%`) | Cả 8 `loi_giai.py` chạy exit 0 và stdout khớp 100% `mong_doi.txt` |
| Số phát hiện `SHOULD` | **18 mục** | Gồm thiếu định nghĩa P1 rải rác trong thân bài, thiếu `Hai mức quy mô` trong `recap`, số lab trùng ví dụ (`L09, L10, L13, L15`), câu `L15` vượt trần 16 phút (`17.69 phút`, hợp lệ với bài `journey`) |

### Bảng tổng hợp từng bài

| Bài | `sha16` YAML | Phút | Khớp `spec_sha256` | Khớp `SRT` | `checks:` | Lab chạy | `P1` (chặt / thân bài) | `P8` | `P9` | `MUST` | `SHOULD` |
|---|---|---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|---:|
| **L08** | `ab43f744373351d4` | 11.17 | ✓ (`5babc823...`) | ✓ (91/91) | 16/16 | ✓ | 0 / 1 | 0 | 2 | 3 | 2 |
| **L09** | `fe29c1416e12f1be` | 11.61 | ✓ (`7d38c305...`) | ✓ (100/100) | 16/16 | ✓ | 0 / 1 | 0 | 1 | 3 | 3 |
| **L10** | `56b4ddc090622fb2` | 11.49 | ✓ (`e0029231...`) | ✓ (103/103) | 15/15 | ✓ | 0 / 1 | 0 | 2 | 3 | 3 |
| **L11** | `3a79e7b29ccc4b01` | 9.42 | ✓ (`ea36b44c...`) | ✓ (81/81) | 12/12 | ✓ | 0 / 0 | 1 | 1 | 2 | 2 |
| **L12** | `c5a5970968ce4b9a` | 9.24 | ✓ (`a05c2c43...`) | ✓ (82/82) | 14/14 | ✓ | 0 / 1 | 0 | 2 | 3 | 2 |
| **L13** | `57371e0c20ef38bc` | 9.40 | ✓ (`0d56270e...`) | ✓ (79/79) | 20/20 | ✓ | 1 / 2 | 0 | 2 | 3 | 2 |
| **L14** | `ba3bcfb11d1cdf41` | 9.79 | ✓ (`392bea2e...`) | ✓ (85/85) | 14/14 | ✓ | 0 / 1 | 0 | 2 | 3 | 2 |
| **L15** | `7f6c0624d6edc971` | 17.69 | ✓ (`7fa4e9d2...`) | ✓ (147/147) | 32/32 | ✓ | 0 / 1 | 0 | 2 | 3 | 2 |

---

## 2. Kiểm tra chéo toàn cục các tiêu chí bắt buộc

1. **Toán học, công thức, `checks:`, giá trị số**:
   - Toàn bộ `137/137` `checks:` và `72/72` kiểm tra trong `audit/esy/verify_esy.py` đều PASS.
   - Mọi số liệu trong `L15` khớp nguyên văn `audit/esy/sources_L15.md` (`[GR97]`, `[MJ97]`, `[RN05]`, `[JPL14a]`, `[JPL14b]`, `[JPL15]`, `[FP]`), phân biệt rõ `(số minh hoạ)` và cận trên mẫu `≈ 49,3 lần mỗi sol` (dùng `1480 phút` theo NASA NSSDCA thay vì `24h 37m` ngày sao), không nêu tên cá nhân trong `say`.
2. **Mọi câu có `"càng "` trong `say`/`show`/`title`**:
   - **L08**: `prereq#2` (`"Dây càng dài, điện dung càng lớn"`), `intuition` title (`"Điện trở càng lớn, dây lên mức 1 càng chậm"`), `example#0` (`"càng gần đầy càng chậm"`), `example#2` (`"điện trở càng nhỏ thì dòng càng lớn"`). Đều đúng vật lý/toán học.
   - **L09**: `sym#0` (`"chu kỳ càng ngắn, ưu tiên càng cao"`). Đúng định nghĩa Rate Monotonic.
   - **L13**: `intuition` title (`"Thức càng ít, phần ngủ càng nặng"`). Đúng đơn điệu.
   - **L10, L11, L12, L14, L15**: Không xuất hiện `"càng "`. **0 lỗi.**
3. **Ký hiệu toán thô trong `say`**: **0 lỗi** across 8 bài (chỉ có tên chuẩn `I²C` trong L08 `hook#0`, `sym#0`, `example#0`, `pitfalls#0`, `recap#0` — đã xử lý phát âm chuẩn).
4. **Lỗi `SPELL_CANON` và `term_canon`**: **0 lỗi** across 8 bài (dùng nhất quán `tỉ`, `lũy`, `tuỳ`, `lô-ga-rít`, `tệp`, `khoá`).
5. **`audit/layout_ESY.tsv` và `audit/review/screen_code/ESY.yaml`**:
   - `audit/layout_ESY.tsv` rỗng (2 byte `\r\n`, không ghi nhận tràn khung).
   - `audit/review/screen_code/ESY.yaml` khớp cấu trúc khối code của L08–L15 (có `practice 1 0`, `practice 2 0`, `practice 4 0` cho L08–L10, L12–L15; và chỉ `practice 1 0` cho L11).
6. **Tổng hợp các lỗi hệ thống trên cả 8 bài**:
   - **Lỗi hệ thống 1 (`covers:` sai ánh xạ ở 8/8 bài)**: Mọi bài đều gán cứng `objective 1 -> example` (hoặc `stage1`), `objective 2 -> check` (hoặc `stage2`), `objective 3 -> practice`, bất chấp nội dung thực sự của mục tiêu và cảnh!
   - **Lỗi hệ thống 2 (`practice` lộ lời giải trước `pause` ở 7/8 bài: L08–L10, L12–L15)**: `practice#1` in nguyên văn toàn bộ mã `loi_giai.py` (`Cài đặt kiểm chứng ESY:Lxx bằng Python`) và `practice#2` in nguyên văn `mong_doi.txt` (`Đầu ra chạy thật (1 dòng)`) **trước** khi `practice#3` yêu cầu học viên bấm `pause: 30` để tự làm! (Riêng `L11` không có `practice#1/#2` nên không bị lộ).
   - **Lỗi hệ thống 3 (`de.md` thiếu đặc tả `stdout` & không khớp bài/lời giải ở 8/8 bài)**: Không một `de.md` nào trong `L08..L15` ghi rõ định dạng dòng in ra (`key=value`, số chữ số thập phân, dấu nháy, thứ tự), khiến người học chỉ đọc `de.md` không thể viết đúng để qua `labs/cham.sh`. Ngoài ra `L09, L10, L13, L15` dùng trùng số của ví dụ trong bài; `L12, L14` hardcode kết quả (`static_alloc_safe=1`, `b_sig_ok = False`) không đúng mô tả trong `de.md`.
   - **Lỗi hệ thống 4 (bảng `practice#0` sai lệch token thật của `loi_giai.py` ở 8/8 bài)**: Bảng `practice#0` ở 7 bài `L08–L10, L12–L15` dùng mẫu chung `f"{val:.3f}"` và `print(...)` bất chấp `loi_giai.py` thực tế dùng `:.1f`, `:.4f`, `:.0f`, `range()`, `math.ceil()`, `[:2]`, `1e6`, `400_000`, `int(...)`, `not`, `if...else`, `;`, `# comment`, v.v.; riêng `L09` còn ghi thừa `math.log / exp / sqrt` dù không dùng; `L11` thiếu hẳn bảng `practice#0`.

---

## 3. Báo cáo chi tiết từng bài (L08–L15)

### Bài L08 — Bus I²C và SPI (`L08_i2c_spi.yaml`)
- **Thông số dựng**: `sha16=ab43f744373351d4`, `spec_sha256=5babc8238ea06e09...` (khớp), `91` khung, `11.17` phút, `1808` từ, `SRT` khớp `91/91`, `asr_report.md`: 28 câu gắn cờ đều đã `asr_reviewed`, `checks: 16/16 PASS`, `loi_giai.py` chạy ra `spi_4B_us=80.0 i2c_4B_us=112.5` khớp `mong_doi.txt`.
- **Phát hiện**:
  - **[MUST] P8 — `practice#1/#2` lộ lời giải trước `pause`**: `practice#1` (`00079.png`) hiển thị nguyên văn `loi_giai.py` và `practice#2` (`00080.png`) hiển thị `spi_4B_us=80.0 i2c_4B_us=112.5` trước `pause: 30` ở `practice#3` (`00081.png`).
  - **[MUST] Lab `L08/de.md` thiếu định dạng `stdout` và mơ hồ về khung I²C**: `de.md` chỉ ghi *"Tính độ rộng thời gian truyền 32 bit ở xung nhịp `400 kHz` (SPI) và overhead byte địa chỉ I2C"*, hoàn toàn không ghi định dạng `spi_4B_us=... i2c_4B_us=...` (1 chữ số thập phân), không nói truyền ghi 4 byte dữ liệu = 1 byte địa chỉ + 4 byte dữ liệu = 5 byte = 45 nhịp (không tính Start/Stop), trong khi thân bài `i2c#1` dạy đọc thanh ghi 5 byte = 2 byte địa chỉ + 1 số thanh ghi + 2 dữ liệu = 45 nhịp.
  - **[MUST] `covers:` ánh xạ sai toàn bộ 3 mục tiêu**:
    - `objective 1` ("So sánh I²C và SPI...") $\to$ trỏ `example` (Chọn điện trở kéo lên — phải là `sym` hoặc cảnh so sánh).
    - `objective 2` ("Ghép byte địa chỉ I²C") $\to$ trỏ `check` (Chạy mô phỏng điện áp RC từng ns — thực tế dạy ở `i2c` và `quiz` Q1).
    - `objective 3` ("Chọn điện trở kéo lên cho I²C") $\to$ trỏ `practice` (Thời gian truyền khung 4 byte — thực tế dạy ở `example` và `quiz` Q2–Q3).
  - **[SHOULD] P1 (chặt) & bảng `practice#0` lệch `loi_giai.py`**:
    - Thân bài `sym#0` (`show`): dùng `SDA`, `SCL` (`dữ liệu SDA, xung nhịp SCL`) nhưng không giải thích chữ viết tắt SDA/SCL (bảng cách đọc có phủ không: **không**).
    - `practice#0` (`00078.png`) giải thích `f"{val:.3f}"` (3 chữ số) và `print(...)`, nhưng `practice#1` (`00079.png`) dùng `:.1f`, `400_000`, `1e6`, `# addr+4B with ACK bits` (bảng cách đọc có phủ không: **không**).
  - **[SHOULD] P9**: Có 2 mức điện dung (`200 pF` vs `100 pF`) và 2 tốc độ (`400 kHz` vs `100 kHz`) kèm đánh đổi 2 biên ($R_{\min}–R_{\max}$), đạt `P9 = 2`, nhưng `recap` chưa nêu tường minh sự thay đổi theo quy mô (dây dài hơn/tốc độ cao hơn siết hẹp khoảng $R$).
  - **[INFO]**: Hình ảnh SVG (`00032.png`) và HTML sạch, không đè chữ, không cắt công thức.
- **Điểm chuẩn**: `P1 = 0` (chặt: 5 mục; thân bài: 1 mục), `P8 = 0`, `P9 = 2`.

---

### Bài L09 — Lập lịch đơn điệu theo tần số và phân tích thời gian đáp ứng (`L09_lap_lich_rm.yaml`)
- **Thông số dựng**: `sha16=fe29c1416e12f1be`, `spec_sha256=7d38c3052b8184c0...` (khớp), `100` khung, `11.61` phút, `1964` từ, `SRT` khớp `100/100`, `asr_report.md`: 7 câu gắn cờ đã `asr_reviewed`, `checks: 16/16 PASS`, `loi_giai.py` chạy ra `U=0.833 LL_bound=0.7798 exact_R3=10` khớp `mong_doi.txt`.
- **Phát hiện**:
  - **[MUST] P8 — `practice#1/#2` lộ lời giải trước `pause`**: `practice#1` (`00089.png`) in nguyên văn `loi_giai.py`, `practice#2` in `U=0.833 LL_bound=0.7798 exact_R3=10` trước `pause: 30` ở `practice#3`.
  - **[MUST] Lab `L09/de.md` thiếu định dạng `stdout`**: `de.md` không nêu `U={u:.3f} LL_bound={ll:.4f} exact_R3={r}` (3 và 4 chữ số thập phân, tên khoá).
  - **[MUST] `covers:` ánh xạ sai mục tiêu 2 và 3**:
    - `objective 2` ("Tính thời gian đáp ứng xấu nhất bằng phép lặp") $\to$ trỏ `check` (cảnh `check` *cố ý không dùng phép lặp* mà đếm tổng việc $\le t$; phép lặp dạy ở `rta` và `example`).
    - `objective 3` ("Biết cận chỉ là điều kiện đủ") $\to$ trỏ `practice` (`practice` chỉ in 3 số cho `(1,4),(2,6),(3,12)`, không minh hoạ/giải thích điều kiện đủ; thực tế dạy ở `rta`, `pitfalls#0` và `quiz`).
  - **[SHOULD] Trùng số liệu giữa lab và ví dụ (`BRIEF_AF2` §2)**: Lab `L09` dùng đúng bộ `(1,4),(2,6),(3,12)` của ví dụ trong bài.
  - **[SHOULD] P1 (chặt) & bảng `practice#0` lệch `loi_giai.py`**:
    - Thân bài `sym#0` (`show`): viết $n\,(2^{1/n} - 1)$ nhưng chưa định nghĩa tường minh `n` là số tác vụ trước/ngay tại công thức (chỉ suy ra ở câu sau *"Với n = 3"*).
    - Thân bài `pitfalls#3`: dùng *"Hàm xử lý ngắt"* trong khi `L09` chỉ `requires: [L00]` (không qua `L02`), nên ngắt chưa được giảng trong chuỗi tiên quyết của `L09` (bảng cách đọc: **không**).
    - `practice#0` (`00088.png`) giải thích `math.log / exp / sqrt` (không dùng trong `loi_giai.py`!) và `f"{val:.3f}"`, nhưng thiếu `range(10)`, `_`, `tasks[:2]`, `math.ceil`, `**`, generator `sum(c / p for ...)`, `:.4f` trong `practice#1` (`00089.png`).
  - **[SHOULD] P9 yếu (`P9 = 1`)**: Chỉ đổi $C_3$ từ 2 lên 3 ở `quiz` và $U=0.833$ vs $1$ ở `pitfalls`, chưa cho thấy vấn đề thay đổi ở $\ge 2$ mức quy mô số lượng tác vụ (ví dụ $n=2$ vs $n=100$) hoặc siêu chu kỳ, và `recap` không nhắc quy mô.
  - **[INFO]**: 2 khung SVG (`00036.png`, `00056.png`) hiển thị rõ nét, căn lề chuẩn.
- **Điểm chuẩn**: `P1 = 0` (chặt: ≥8 mục; thân bài: 2 mục), `P8 = 0`, `P9 = 1`.

---

### Bài L10 — Lập lịch theo hạn sớm nhất và đảo ngược ưu tiên (`L10_edf_dao_uu_tien.yaml`)
- **Thông số dựng**: `sha16=56b4ddc090622fb2`, `spec_sha256=e00292311cdb28fb...` (khớp), `103` khung, `11.49` phút, `2011` từ, `SRT` khớp `103/103`, `asr_report.md`: 1 câu gắn cờ đã `asr_reviewed`, `checks: 15/15 PASS`, `loi_giai.py` chạy ra `U=1.0 fixed_prio_miss_t6=1 edf_feasible=1` khớp `mong_doi.txt`.
- **Phát hiện**:
  - **[MUST] P8 — `practice#1/#2` lộ lời giải trước `pause`**: `practice#1` (`00092.png`) in nguyên văn `loi_giai.py` và `practice#2` in `U=1.0 fixed_prio_miss_t6=1 edf_feasible=1` trước `pause: 30` ở `practice#3`.
  - **[MUST] Lab `L10/de.md` thiếu định dạng `stdout` & `loi_giai.py` gán cứng**: `de.md` không nêu định dạng `U=... fixed_prio_miss_t6=... edf_feasible=...`; đồng thời `loi_giai.py` gán cứng `fixed_prio_miss_t6=1` trong comment chứ không mô phỏng lịch RM/EDF.
  - **[MUST] `covers:` ánh xạ sai mục tiêu 2 và 3**:
    - `objective 2` ("Biết hành vi khi quá tải") $\to$ trỏ `check` (`check` kiểm bộ `(2,4),(3,6)` khi $U=1$, không phải quá tải! Quá tải dạy ở cảnh `overload`).
    - `objective 3` ("Nhận ra đảo ngược ưu tiên và cách kế thừa ưu tiên sửa nó") $\to$ trỏ `practice` (`practice` không hề có khoá hay đảo ngược ưu tiên; dạy ở `inversion` và `quiz` Q2).
  - **[SHOULD] Trùng số liệu ví dụ**: Lab `L10` dùng lại y nguyên `(2,4),(3,6)` của ví dụ trong bài.
  - **[SHOULD] P1 (chặt) & bảng `practice#0` lệch `loi_giai.py`**:
    - Thân bài: `sym#0` dùng viết tắt `EDF` không giải nghĩa chữ tiếng Anh gốc; `pitfalls#0` dùng *"một ngắt dồn dập"* trong khi `L10` chỉ `requires: [L09]->[L00]` (chưa học ngắt).
    - `practice#0` (`00091.png`) chỉ có `.3f` và `print(...)`, thiếu `:.1f`, `int(u <= 1.0)`, `# Fixed priority...` ở `practice#1` (`00092.png`).
  - **[SHOULD] `recap` thiếu tóm tắt số 2 mức quy mô**: Đạt `P9 = 2` ở thân bài nhờ so $U=1.0$ (kịp) và quá tải $U=1.2$ (trễ dây chuyền) + đánh đổi với RM, nhưng `recap` không nêu lại số liệu 2 mức.
  - **[INFO]**: 3 khung SVG (`00025.png`, `00031.png`, `00045.png`) sạch, trực quan, chữ đỏ `"trễ hạn"` nổi bật đúng chỗ.
- **Điểm chuẩn**: `P1 = 0` (chặt: 5 mục; thân bài: 2 mục), `P8 = 0`, `P9 = 2`.

---

### Bài L11 — Hệ điều hành thời gian thực: tác vụ, hàng đợi, đồng bộ (`L11_rtos.yaml`)
- **Thông số dựng**: `sha16=3a79e7b29ccc4b01`, `spec_sha256=ea36b44cbf3c613f...` (khớp), `81` khung, `9.42` phút, `1596` từ, `SRT` khớp `81/81`, `asr_report.md`: 27 câu gắn cờ đã `asr_reviewed`, `checks: 12/12 PASS`, `loi_giai.py` chạy ra `queued=3 decoded='OK\n'` khớp `mong_doi.txt`.
- **Phát hiện**:
  - **[MUST] Lab `L11/de.md` thiếu định dạng `stdout` và sai lệch nội dung với `loi_giai.py`**: `de.md` mô tả *"Mô phỏng hàng đợi giữa ISR nhanh (20 µs) và tác vụ giải mã nền để không mất byte UART"*, nhưng không hề cho dữ liệu đầu vào `b'OK\n'`, cỡ hàng đợi `maxlen=8`, hay định dạng in `queued=3 decoded='OK\n'`; `loi_giai.py` cũng không mô phỏng `20 µs`.
  - **[MUST] `covers:` ánh xạ sai cả 3 mục tiêu**:
    - `objective 1` ("Chia chương trình thành các tác vụ có ưu tiên") $\to$ trỏ `example` (tính cỡ hàng đợi UART 116 $\to$ 128 chỗ, không phải chia tác vụ — dạy ở `sym` và `queue`).
    - `objective 2` ("Truyền dữ liệu từ ngắt sang tác vụ bằng hàng đợi") $\to$ trỏ `check` (tính thời gian đầy hàng đợi 9,98 ms vs 10,07 ms; truyền ISR$\to$hàng đợi$\to$tác vụ dạy ở `queue` và `practice`).
    - `objective 3` ("Biết hàm nào được gọi trong ngắt") $\to$ trỏ `practice` (Python `deque`, không dạy/kiểm tra hàm không chờ trong ngắt — dạy ở `queue`, `pitfalls#0`, `quiz` Q2).
  - **[SHOULD] P1 (chặt) — Mã C trong thân bài (`queue#0`) và thiếu bảng `practice#0`**:
    - Trong `queue#0` (`show`): dùng `uint8_t`, `UDR0`, `for (;;)`, `&b`, `WAIT_FOREVER` mà không giải thích tại chỗ (dù `L11` `requires: [L10]->[L09]->[L00]`; ngay cả `L02` cũng chưa dạy `for (;;)` hay `&b`).
    - `practice` (`00072.png`) không có bước `practice#0` giải thích token Python, dù `practice#1` không lộ mã Python (nên `L11` là bài duy nhất **không lộ lời giải trước `pause`**!).
  - **[SHOULD] P9 yếu (`P9 = 1`)**: Có 2 bài toán cỡ khác nhau (`115 200 baud / 10 ms` ở `example` và `9600 baud / 20 ms` ở `quiz`) + đánh đổi RAM (`12 byte`) lấy biên an toàn, nhưng chưa phân tích trên cùng hệ khi tốc độ/tải tăng gấp 10–100 lần và `recap` không có mục hai mức quy mô.
  - **[INFO]**: `L11` là bài duy nhất giữ đúng trật tự `P8` (không lộ `loi_giai.py` hay `mong_doi.txt` trước `pause: 30`). Hai khung SVG (`00028.png`, `00031.png`) rất rõ ràng.
- **Điểm chuẩn**: `P1 = 0` (chặt: 4 mục C trong `queue#0`), `P8 = 1` (không lộ nhưng `de.md` thiếu spec stdout), `P9 = 1`.

---

### Bài L12 — Độ tin cậy: bộ giám sát, tràn ngăn xếp, cấp phát động (`L12_do_tin_cay.yaml`)
- **Thông số dựng**: `sha16=c5a5970968ce4b9a`, `spec_sha256=a05c2c43223774a6...` (khớp), `82` khung, `9.24` phút, `1503` từ, `SRT` khớp `82/82`, `asr_report.md`: 21 câu gắn cờ đã `asr_reviewed`, `checks: 14/14 PASS`, `loi_giai.py` chạy ra `wdt_fed_ok=1 static_alloc_safe=1` khớp `mong_doi.txt`.
- **Phát hiện**:
  - **[MUST] P8 — `practice#1/#2` lộ lời giải trước `pause`**: `practice#1` (`00069.png`) in nguyên văn `loi_giai.py` và `practice#2` in `wdt_fed_ok=1 static_alloc_safe=1` trước `pause: 30` ở `practice#3`.
  - **[MUST] Lab `L12/de.md` thiếu định dạng `stdout` & `loi_giai.py` gán cứng**: `de.md` không nêu chuỗi `wdt_fed_ok=1 static_alloc_safe=1` và nói *"mức đỉnh ngăn xếp trong giới hạn"*, nhưng `loi_giai.py` chỉ gán cứng `static_alloc_safe=1` và không tính/kiểm ngăn xếp chút nào.
  - **[MUST] `covers:` ánh xạ sai mục tiêu 1 và 3**:
    - `objective 1` ("Dùng bộ giám sát đúng cách") $\to$ trỏ `example` (`example` dạy **ước lượng ngăn xếp**, không phải bộ giám sát! Bộ giám sát dạy ở `sym`, `where`, `intuition#0`, `pitfalls#0,#3`, `quiz` Q2).
    - `objective 3` ("Hiểu vì sao tránh cấp phát động khi chạy") $\to$ trỏ `practice` (`practice` chỉ gán cứng `static_alloc_safe=1`; lý do phân mảnh dạy ở `heap`).
  - **[SHOULD] P1 (chặt) & bảng `practice#0` lệch `loi_giai.py`**:
    - Thân bài `example#3` (`show`): dùng `0xA5` (tiền tố `0x` chưa dạy trong chuỗi tiên quyết `L12->L11->L10->L09->L00`, `say` tránh đọc mà nói *"một mẫu cố định"*).
    - `practice#0` (`00068.png`) giải thích `:.3f` và `print(...)`, nhưng `practice#1` (`00069.png`) không dùng `.3f` mà dùng gán bộ đôi `wdt_ms, loop_ms = 100, 80`, phép so sánh `>`, `not`, `int(...)`.
  - **[SHOULD] P9**: Có trục thời gian ("ngày thử nghiệm" vs "ba tháng / ngày thứ một trăm" ở `hook`, `heap`, `recap#1`) và 3 mức hạn watchdog (`50 / 100 / 1000 ms`) kèm đánh đổi (`P9 = 2`), nhưng ví dụ phân mảnh mới dừng ở 1 ảnh chụp 5 khối chứ chưa có bảng 2 mốc thời gian cụ thể.
  - **[INFO]**: Hai khung SVG (`00021.png` răng cưa watchdog, `00025.png` cột ngăn xếp) sạch, chính xác về tỉ lệ và con số.
- **Điểm chuẩn**: `P1 = 0` (chặt: 5 mục; thân bài: 1 mục), `P8 = 0`, `P9 = 2`.

---

### Bài L13 — Năng lượng: chế độ ngủ và tuổi thọ pin (`L13_nang_luong.yaml`)
- **Thông số dựng**: `sha16=57371e0c20ef38bc`, `spec_sha256=0d56270ea34965b8...` (khớp), `79` khung, `9.40` phút, `1405` từ, `SRT` khớp `79/79`, `asr_report.md`: 14 câu gắn cờ đã `asr_reviewed`, `checks: 20/20 PASS`, `loi_giai.py` chạy ra `avg_ma=0.1099 battery_days=379` khớp `mong_doi.txt`.
- **Phát hiện**:
  - **[MUST] P8 — `practice#1/#2` lộ lời giải trước `pause`**: `practice#1` (`00066.png`) in nguyên văn `loi_giai.py` và `practice#2` in `avg_ma=0.1099 battery_days=379` trước `pause: 30` ở `practice#3`.
  - **[MUST] Lab `L13/de.md` thiếu định dạng `stdout`**: `de.md` không nêu chuỗi `avg_ma=... battery_days=...` (4 chữ số thập phân cho `avg_ma`, làm tròn nguyên `.0f` cho `battery_days`).
  - **[MUST] `covers:` ánh xạ sai mục tiêu 3**: `objective 3` ("Biết phần nào đang quyết định tuổi thọ") $\to$ trỏ `practice`, nhưng `practice` chỉ tính 1 cặp `avg_ma` và `battery_days`, không tính tỉ trọng hay xác định phần quyết định (dạy ở `intuition`, `example`, `quiz` Q3).
  - **[SHOULD] Trùng số liệu ví dụ (`BRIEF_AF2` §2)**: Lab `L13` lấy y nguyên bộ `1% × 10 mA + 99% × 10 µA, 1000 mAh -> 379 ngày` của ví dụ trong bài.
  - **[SHOULD] P1 (chặt) & P9 ở `recap`**:
    - Thân bài `L13` rất xuất sắc (**0 mục P1 chưa giảng**). Chỉ vướng bảng `practice#0` (`00065.png`) ghi `f"{val:.3f}"` trong khi `practice#1` (`00066.png`) dùng `:.4f` và `:.0f` (2 mục $\to P1 = 1$).
    - P9 thân bài rất tốt (4 mức `10%, 1%, 0.1%, 0.01%` ở `intuition` + đảo chiều phần quyết định ở `example`), nhưng `recap` chưa nhắc lại số liệu 2 mức quy mô.
  - **[INFO]**: Hai khung SVG (`00010.png`, `00018.png`) rất rõ ràng, cân đối.
- **Điểm chuẩn**: `P1 = 1` (thân bài: **2**; chặt gồm `practice#1`: 2 mục `.4f`, `.0f`), `P8 = 0`, `P9 = 2`.

---

### Bài L14 — Cập nhật phần sụn an toàn và khởi động tin cậy (`L14_cap_nhat_an_toan.yaml`)
- **Thông số dựng**: `sha16=ba3bcfb11d1cdf41`, `spec_sha256=392bea2e217046d6...` (khớp), `85` khung, `9.79` phút, `1609` từ, `SRT` khớp `85/85`, `asr_report.md`: 8 câu gắn cờ đã `asr_reviewed`, `checks: 14/14 PASS`, `loi_giai.py` chạy ra `rollback_to=A` khớp `mong_doi.txt`.
- **Phát hiện**:
  - **[MUST] P8 — `practice#1/#2` lộ lời giải trước `pause`**: `practice#1` (`00074.png`) in nguyên văn `loi_giai.py` và `practice#2` in `rollback_to=A` trước `pause: 30` ở `practice#3`.
  - **[MUST] Lab `L14/de.md` thiếu định dạng `stdout` & không khớp bài toán băm**: `de.md` không cho biết đầu vào (`active='A'`, `b_sig_ok=False`, `boot_ok=True`) hay định dạng `rollback_to=A`, và tiêu đề ghi *"có xác thực băm"* nhưng `loi_giai.py` không hề băm dữ liệu.
  - **[MUST] `covers:` ánh xạ sai mục tiêu 1 và 2**:
    - `objective 1` ("Phân biệt mã kiểm tổng và chữ ký số") $\to$ trỏ `example` (`example` dạy cập nhật A/B; phân biệt CRC vs chữ ký số dạy ở `prereq` và `sym`).
    - `objective 2` ("Giải thích khởi động tin cậy") $\to$ trỏ `check` (`check` kiểm mất điện khi cập nhật A/B; chuỗi khởi động tin cậy từ ROM dạy ở `boot`).
  - **[SHOULD] P1 (chặt) & bảng `practice#0` lệch `loi_giai.py`**:
    - Thân bài `sym#0` (`show`): dùng `CRC-32` chưa giải thích viết tắt `CRC`.
    - `practice#0` (`00073.png`) giải thích `:.3f` và `print(...)`, nhưng `practice#1` (`00074.png`) không dùng `.3f` mà dùng `;`, `False`/`True`, `and`, biểu thức ba ngôi `'B' if ... else active`.
  - **[SHOULD] P9**: Có quy mô đội 10 000 thiết bị (`hook`) vs 1 thiết bị lộ khoá (`pitfalls#3`) và 2 mức cỡ phần sụn (`400 KB` vừa vs `600 KB` tràn flash 1024 KB) kèm đánh đổi (`P9 = 2`), nhưng `recap` chưa nêu lại 2 mức quy mô.
  - **[INFO]**: Khung SVG bố trí bộ nhớ (`00029.png`) sạch, rõ ràng, không đè chữ.
- **Điểm chuẩn**: `P1 = 0` (chặt: 5 mục; thân bài: 1 mục), `P8 = 0`, `P9 = 2`.

---

### Bài L15 — Tình huống chuyên gia theo dòng thời gian: phần mềm trên robot thăm dò sao Hoả (`L15_hanh_trinh_sao_hoa.yaml`)
- **Thông số dựng**: `sha16=7f6c0624d6edc971`, `spec_sha256=7fa4e9d23276093b...` (khớp), `147` khung, `17.69` phút, `2996` từ (bài `case: journey` hợp lệ dài hơn 16 phút theo `BRIEF_AF2`), `SRT` khớp `147/147`, `asr_report.md`: 17 câu gắn cờ đã `asr_reviewed`, `checks: 32/32 PASS`, `loi_giai.py` chạy ra `period_ms=125.0 used_ms=117 overload=1` khớp `mong_doi.txt`.
- **Phát hiện**:
  - **[MUST] P8 — `practice#1/#2` lộ lời giải trước `pause`**: `practice#1` (`00131.png`) in nguyên văn `loi_giai.py` và `practice#2` (`00132.png`) in `period_ms=125.0 used_ms=117 overload=1` trước `pause: 30` ở `practice#3` (`00133.png`).
  - **[MUST] Lab `L15/de.md` thiếu định dạng `stdout` & trùng số `stage1`**: `de.md` không nêu định dạng `period_ms=... used_ms=... overload=...`, và lấy đúng số minh hoạ `40+60+2+15=117 > 110` của `stage1#1`.
  - **[MUST] `covers:` ánh xạ sai/thiếu ở cả 3 mục tiêu**:
    - `objective 1` ("...qua năm chặng từ 1997 tới nay...") $\to$ chỉ trỏ `stage1` (1/5 chặng!).
    - `objective 2` ("Tính lại hạn chót 8 Hz..., số lần cấp thêm..., nhịp đặt lại trễ và tuổi thọ vượt thiết kế") $\to$ chỉ trỏ `stage2` (trong khi 8 Hz ở `stage1`, 42× ở `stage4`, và cả 4 được kiểm lại ở `check`).
    - `objective 3` ("Chọn giữa khởi động lại định kỳ, giới hạn vùng nhớ cố định và giám sát ngưỡng... kèm điều kiện đổi lựa chọn") $\to$ trỏ `practice` (`practice` là phép cộng Pathfinder 1997! Tình huống trạm đo thời tiết chọn 3 phương án và điều kiện đổi ở `quiz`).
  - **[SHOULD] P1 (chặt) & bảng `practice#0` lệch `loi_giai.py`**:
    - Thân bài `stage1#0` (`show`): dùng `"bus 1553"` chưa giải nghĩa `bus` (dạy ở L08, không nằm trong `requires: [L10, L12, L14]`) và chuẩn `1553` (`say` nói *"Phần cứng nối thiết bị"*).
    - `practice#0` (`00130.png`) giải thích `:.3f` và `print(...)`, nhưng `practice#1` (`00131.png`) dùng `:.1f` và `int(cycle_used > 110)`.
  - **[SHOULD] Chuỗi `covers` chưa phản ánh 5 chặng**: Mặc dù thân bài + `recap` trình bày xuất sắc cả 5 chặng quy mô/thời gian (`P9 = 2`), `covers` không trỏ đủ.
  - **[INFO]**: Đối chiếu `audit/esy/sources_L15.md` đạt chuẩn cao (tránh chi tiết sai của `[MJ97]`, giải thích rõ số minh hoạ, cận trên 49,3 lần/sol, sol ≈ 1480 phút). Hai khung SVG (`00021.png`, `00026.png`) và `quiz`/`recap` (`00116.png`, `00137.png`) hiển thị hoàn hảo.
- **Điểm chuẩn**: `P1 = 0` (chặt: 3 mục; thân bài: 1 mục), `P8 = 0`, `P9 = 2`.

---

## 4. Danh sách toàn bộ 38 khung hình PNG đã mở xem trực tiếp (`read_file`)

Tất cả 38 khung hình đều hiển thị sắc nét, không đè chữ, không tràn lề, không cắt công thức, độ tương phản tốt:
- **L08 (6 ảnh)**: `out/ESY/L08/frames/00000.png` (hook#0), `00032.png` (intuition#0 SVG), `00078.png` (practice#0), `00079.png` (practice#1 — lộ code), `00080.png` (practice#2 — lộ stdout), `00081.png` (practice#3 — pause).
- **L09 (4 ảnh)**: `out/ESY/L09/frames/00036.png` (intuition#0 SVG), `00056.png` (example#4 SVG), `00088.png` (practice#0), `00089.png` (practice#1 — lộ code).
- **L10 (5 ảnh)**: `out/ESY/L10/frames/00025.png` (intuition#0 SVG), `00031.png` (example#1 SVG), `00045.png` (example#4 SVG), `00091.png` (practice#0), `00092.png` (practice#1 — lộ code).
- **L11 (4 ảnh)**: `out/ESY/L11/frames/00028.png` (intuition#0 SVG), `00031.png` (intuition#1 SVG), `00072.png` (practice#0 — hướng dẫn + pause), `00075.png` (practice#1 — kết quả mong đợi sau pause).
- **L12 (4 ảnh)**: `out/ESY/L12/frames/00021.png` (intuition#0 SVG), `00025.png` (intuition#1 SVG), `00068.png` (practice#0), `00069.png` (practice#1 — lộ code).
- **L13 (4 ảnh)**: `out/ESY/L13/frames/00010.png` (sym#0 SVG), `00018.png` (intuition#0 SVG), `00065.png` (practice#0), `00066.png` (practice#1 — lộ code).
- **L14 (3 ảnh)**: `out/ESY/L14/frames/00029.png` (intuition#0 SVG), `00073.png` (practice#0), `00074.png` (practice#1 — lộ code).
- **L15 (8 ảnh)**: `out/ESY/L15/frames/00021.png` (timeline#0 SVG), `00026.png` (mech#0 SVG), `00116.png` (quiz#0), `00130.png` (practice#0), `00131.png` (practice#1 — lộ code), `00132.png` (practice#2 — lộ stdout), `00133.png` (practice#3 — pause), `00137.png` (recap#0).

---

## 5. Người học kẹt ở đâu (góc nhìn người mất gốc, theo `ADDENDUM.md` & `BRIEF_R4.md`)

- **L08**: Kẹt nhẹ ở `sym#0` (`show`: `"dữ liệu SDA, xung nhịp SCL"` không giải nghĩa SDA/SCL) và kẹt nặng ở `practice` (bảng `practice#0` dạy `.3f` trong khi `practice#1` dùng `.1f`, `1e6`, `400_000`; mở `de.md` không biết phải in `spi_4B_us=80.0 i2c_4B_us=112.5` hay I²C tính mấy byte).
- **L09**: Kẹt nhẹ ở `sym#0` (chữ `n` trong $n(2^{1/n}-1)$ chưa giới thiệu trước), `pitfalls#3` (`"Hàm xử lý ngắt"` chưa học vì L09 chỉ đòi L00), và kẹt nặng ở `practice` (`practice#0` dạy `math.log/exp/sqrt` không dùng tới, còn `practice#1` dùng `range`, `[:2]`, `math.ceil`, `**`, `.4f` chưa giảng; `de.md` không ghi format stdout).
- **L10**: Kẹt nhẹ ở `sym#0` (`EDF`), `pitfalls#0` (`"ngắt"`), và kẹt ở `practice` (`practice#1` dùng `.1f`, `int(u <= 1.0)` chưa có trong bảng `practice#0`; `de.md` không ghi format stdout).
- **L11**: Kẹt ở `queue#0` (mã C `uint8_t`, `UDR0`, `for (;;)`, `&b` không được giải thích từng ký hiệu) và kẹt hoàn toàn khi làm lab vì `labs/ESY/L11/de.md` không cho chuỗi đầu vào `b'OK\n'`, cỡ `maxlen=8` hay định dạng in `queued=3 decoded='OK\n'`.
- **L12**: Kẹt nhẹ ở `example#3` (`0xA5` — hệ 16 chưa học trong chuỗi `L00->L09->L10->L11->L12`), và kẹt ở `practice` (`practice#1` dùng gán nhiều biến, `>`, `not`, `int(...)` chưa có trong `practice#0`; `de.md` đòi kiểm ngăn xếp nhưng không có format stdout và lời giải thật chỉ gán cứng `static_alloc_safe=1`).
- **L13**: Thân bài **không kẹt**; chỉ kẹt ở `practice` vì `practice#0` dạy `.3f` trong khi `practice#1` dùng `.4f` và `.0f`, và `de.md` không ghi format stdout `avg_ma=... battery_days=...`.
- **L14**: Kẹt nhẹ ở `sym#0` (`CRC-32`), và kẹt ở `practice` (`practice#1` dùng `;`, `False`, `and`, `'B' if ... else active` chưa có trong `practice#0`; `de.md` không ghi `active='A', b_sig_ok=False, boot_ok=True` và format `rollback_to=A`).
- **L15**: Kẹt nhẹ ở `stage1#0` (`"bus 1553"` không giải nghĩa), và kẹt ở `practice` (`practice#1` dùng `.1f`, `int(cycle_used > 110)` chưa có trong `practice#0`; `de.md` không ghi format `period_ms=... used_ms=... overload=...`).

---

## 6. Kiến nghị khắc phục để đạt `GO`

1. **Sửa `practice` (P8 + P1)**: Bỏ việc hiển thị `loi_giai.py` và `mong_doi.txt` trước `pause: 30` ở 7 bài `L08–L10, L12–L15` (chỉ đưa bảng hướng dẫn + `pause` trước, rồi mới hiện `mong_doi.txt` và/hoặc giải thích sau `pause`, giống cấu trúc không lộ đáp án của `L11`); đồng thời cập nhật bảng `practice#0` (hoặc gỡ mã giải ra sau `pause`) cho khớp 100% token Python thật dùng trong từng bài.
2. **Viết lại `labs/ESY/L08..L15/de.md` (+ đổi số liệu lab ở `L09, L10, L13, L15`, sửa logic `L10, L11, L12, L14`)**: Ghi rõ dữ liệu đầu vào, công thức/quy ước (ví dụ `L08` 1 addr + 4 data byte không tính Start/Stop; `L11` chuỗi `b'OK\n'`), và **nguyên văn mẫu `stdout`** (tên khoá, số chữ số thập phân); dùng số liệu khác ví dụ thân bài để tránh chép lại.
3. **Sửa `covers:` ở 8/8 bài**: Ánh xạ đúng mỗi `objective` tới cảnh thực sự dạy/làm kỹ năng đó (ví dụ `L08` obj 2 $\to$ `i2c`/`quiz`; `L15` obj 1 $\to$ `stage1..stage5` hoặc `check`, obj 3 $\to$ `quiz`; nếu `sym`/`boot`/`heap`/`inversion`/`overload` là cảnh dạy chính thì chuyển `kind` hoặc bổ sung bước thực hành/kiểm chứng tương ứng).
4. **Bổ sung định nghĩa P1 rải rác trong thân bài & tóm tắt P9 ở `recap`**: Giải nghĩa `SDA`/`SCL` (`L08`), `n` và `ngắt` (`L09`), `EDF`/`ngắt` (`L10`), `uint8_t`/`UDR0`/`for(;;)`/`&` (`L11`), `0x` (`L12`), `CRC` (`L14`), `bus 1553` (`L15`); bổ sung đối chiếu 2 mức quy mô cho `L09`, `L11` và câu chốt quy mô/đánh đổi trong `recap`.
