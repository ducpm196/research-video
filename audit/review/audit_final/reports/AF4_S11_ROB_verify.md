# Báo cáo kiểm định độc lập khoá ROB (Robot tự hành) — Stage 11 (`WP-AF4-5`)

- **Phạm vi**: Đọc độc lập toàn bộ 14 bài `L00..L13` (`curriculum/rob.yaml`, `lessons/rob/L00..L13.yaml`, `labs/ROB/L00..L13/{de.md, loi_giai.py, mong_doi.txt}`, `audit/rob/sources_L13.md`, `audit/rob/verify_rob.py`, `audit/review/screen_code/ROB.yaml`, `audit/layout_ROB.tsv`, `out/ROB/L00..L13/{build_report.json, L*.srt, asr_report.md}`, và xem trực tiếp **45 ảnh PNG** trong `out/ROB/L*/frames/*.png`).
- **Quy tắc**: Chỉ đọc, không sửa tệp nào trong kho; tự tính lại và chạy kiểm chứng độc lập toàn bộ mã/lab/checks.
- **Verdict tổng thể**: **`NO-GO`** (chưa đạt chuẩn AF2/AF4 để chốt khoá).

---

## 1. Bảng tóm tắt chỉ số (theo `BRIEF_R4.md` & `ADDENDUM.md`)

| Chỉ số | Kết quả đo | Ngưỡng AF2/AF4 | Trạng thái |
|---|---|---|---|
| Số bài `MUST = 0` | **0 / 14** (0%) — mọi bài đều dính ít nhất lỗi `E51` (`covers:`), `P8` lộ lời giải trước `pause`, `L07` & `L13` sai toán/dữ kiện lab | 14 / 14 (100%) | **FAIL** |
| Số bài `P1 = 2` (chuẩn chặt) | **0 / 14** (0%) — `L06, L12` đạt `P1 = 1`; 12 bài còn lại `P1 = 0` (chủ yếu do bảng `practice#0` sai lệch và `practice#1/#3`) | ≥ 13 / 14 (≥ 90%) | **FAIL** |
| Số bài `P8 = 2` (Thực nghiệm) | **0 / 14** (0%) — 14/14 bài đặt code `loi_giai.py` (`practice#1`) + stdout (`practice#2`) TRƯỚC `pause: 30` (`practice#3`); 14/14 `de.md` thiếu định dạng stdout | 14 / 14 (100%) | **FAIL** |
| Số bài `P9 = 2` (Quy mô/thời gian) | **5 / 14** có ≥ 2 mức quy mô trong thân bài (`L06, L08, L11, L12, L13`); **0 / 14** có mục `"Hai mức quy mô"` trong `recap` | ≥ 12 / 14 (≥ 80%) | **FAIL** |
| Số bài `spec_sha256` khớp `lv.spec_digest` | **14 / 14** (100%, `STALE = 0`) | 14 / 14 | **PASS** |
| Số bài `L*.srt` khớp `say` | **14 / 14** (100%, 0 câu thiếu/sai số) | 14 / 14 | **PASS** |
| Số bài `asr_report.md` sạch (`chưa xem xét = 0`) | **14 / 14** (100%; lưu ý mọi mục gắn cờ ghi `NOT_VERIFIED bằng tai người`) | 14 / 14 | **PASS** |
| Số bài `checks:` & `verify_rob.py` PASS | **14 / 14** (`verify_rob.py`: `14/14 PASS`, mọi `checks:` trong YAML PASS) | 14 / 14 | **PASS** |
| Số bài lab chạy `loi_giai.py` khớp `mong_doi.txt` | **14 / 14** (chạy trực tiếp bằng `.venv/Scripts/python`; lưu ý lỗi toán ở `L07` & `L13` và lỗi thiếu dữ liệu ở `L09` `de.md`) | 14 / 14 | **PASS kỹ thuật / FAIL nội dung (L07, L13)** |
| `screen_code/ROB.yaml` khớp SHA16 | **42 / 42** khối (`practice` 1, 2, 4 × 14 bài) | 42 / 42 | **PASS** |
| `lv.lint` & `SPELL_CANON` & toán thô trong `say` | **0** lỗi `lint`, **0** lỗi `SPELL_CANON`, **0** ký hiệu toán thô trong `say` | 0 | **PASS** |
| Khung hình PNG kiểm bằng mắt | **45 / 45 PNG** (đủ 15/15 khung SVG + 28/28 `practice#0/#1` + 3 `practice#3`): **0** đè chữ, **0** cắt công thức, **0** mất tương phản | 0 lỗi hiển thị | **PASS** |
| Tổng số `SHOULD` / `INFO` | **32 SHOULD** (trùng số ví dụ lab 13 bài, `layout_ROB.tsv` stale, `P9` thiếu, thời lượng < 9 phút ở `L00, L02`, câu `"càng "`, `introduces` lệch nhẹ…) | — | — |

---

## 2. Những phát hiện hệ thống xuyên suốt cả 14 bài (`L00–L13`)

### 2.1. Lỗi hệ thống ở cảnh `practice` & thư mục `labs/ROB/` (`MUST` — chặn P8 & P1)
1. **Lộ toàn bộ lời giải TRƯỚC `pause` (`P8 = 0` ở 14/14 bài — `MUST`)**: Trong cả 14 bài `L00..L13`, cảnh `practice` được ghép cố định 5 bước:
   - `practice#0`: bảng `"viết trong mã | đọc và hiểu là"`
   - `practice#1`: **in nguyên văn toàn bộ code `loi_giai.py`** (`Cài đặt kiểm chứng ROB:Lxx bằng Python`)
   - `practice#2`: **in nguyên văn `mong_doi.txt`** (`Đầu ra chạy thật (1 dòng)`)
   - `practice#3`: mới tới bảng đề bài + `pause: 30` (*"Hãy bấm tạm dừng và tự làm trước."*)
   - `practice#4`: in lại `Kết quả mong đợi cần khớp 100%`
   → Người học nhìn thấy trọn vẹn code lời giải và đáp án ngay trước khi được yêu cầu tạm dừng làm bài (trái hoàn toàn `BRIEF_AF2.md` §2: Step 1 đề + `pause`, sau `pause` mới hiện kết quả mong đợi/gợi ý).
2. **`de.md` thiếu định dạng `stdout` ở 14/14 bài (`MUST` ở `L09`, `SHOULD/MUST` ở 13 bài còn lại)**:
   - Không có `de.md` nào trong `L00..L13` ghi mẫu dòng `stdout` cần in (tên khoá như `budget_ms=...`, `v=...m/s omega=...`, số chữ số thập phân `:.3f`, dấu cách). Người học chỉ mở `labs/ROB/Lxx/de.md` sẽ không thể vượt qua `cham.sh` nếu không chép từ video hoặc mở `mong_doi.txt`.
   - Đặc biệt **`L09/de.md`**: chỉ ghi *"Tính điểm ba ứng viên và chọn cặp có điểm tổng hợp cao nhất"* mà **không hề ghi 3 ứng viên đầu vào** `((0.5, 0.0), 0.7, 0.6, 0.5), ((0.3, 0.5), 0.9, 0.8, 0.3), ((0.1, -0.5), 0.4, 0.9, 0.1)` (lại khác số ví dụ trong bài!).
3. **Số liệu lab trùng hệt ví dụ trong bài ở 13/14 bài (`L00..L08, L10..L13` — `SHOULD`, vi phạm `BRIEF_AF2.md` §2)**: Chỉ riêng `L09` đổi số đầu vào so với thân bài.
4. **Bảng `practice#0` sai lệch token thật của `loi_giai.py` ở 13/14 bài (trừ `L06`) — kéo `P1` xuống 0**:
   - Mẫu `practice#0` bị dán cứng (`f"{val:.3f}"`, `math.log / exp / sqrt`, `for x in ds:`, `sum / len / max / min`, `print(...)`) không khớp với token thật trong `practice#1`:
     - `L00, L11`: code dùng `:.0f`, bảng ghi `:.3f`.
     - `L01, L10, L12, L13`: code dùng gán nhiều biến (`vl, vr, L = ...`, `L, e = ...`, `v, a, td = ...`) và `:.1f` / `:.2f`, bảng không giải thích mà ghi `:.3f`.
     - `L02`: code dùng `math.pi`, `math.sin`, `math.radians`, nhưng bảng lại giải thích `math.log / exp / sqrt`.
     - `L03`: code dùng tham số mặc định `lambda z, mu=2.0, s=0.1:`, toán tử `**`, `math.pi`, gán nhiều biến `d1, d3 = ...`, `:.2f`, `:.1f`, nhưng bảng chỉ có `lambda x: ...`, `:.3f`, `log/exp/sqrt` (thiếu cả `print(...)`).
     - `L04`: code dùng tập hợp `{1, 4, 7}`, biểu thức điều kiện `if ... in ... else ...`, `range(10)`, chỉ số `bel[1]`, `:.1f` — không có trong `practice#0`.
     - `L05`: code dùng `math.sin`, `math.cos`, `vh, th = 1.0, 0.0`, `:.1f`, nhưng bảng lại giải thích `math.log / exp / sqrt` và `:.3f`.
     - `L07`: code dùng `;` ngăn cách hai câu lệnh, chỉ số âm `raw[-1]`, `range(4)`, `round(..., 2)` — không có trong bảng, trong khi bảng lại ghi `:.3f` không dùng tới.
     - `L08`: code dùng `**` và định dạng khoa học `:.0e`, bảng lại ghi `:.3f`.
     - `L09`: code dùng tuple lồng nhau `((0.5, 0.0), ...)` và giải nén 4 biến `for vw, h, c, s in cands`, `round(..., 2)`, `max(scored)` trên tuple — không có trong bảng, trong khi bảng ghi `:.3f` không dùng tới.
     - `L13`: code dùng `**`, `:.1f`, `:.2f`, bảng ghi `:.3f`.
   - Ngoài ra, **14/14 bài** đều hiển thị lệnh `bash labs/cham.sh ROB Lxx duong_dan/bai_cua_ban.py` ở `practice#3` mà chưa giảng một dòng về `bash` / đường dẫn / cơ chế lệnh chấm tại chỗ (theo `BRIEF_FIX_R4.md` §3). Và **6/14 bài** ở `practice#3` dùng thuật ngữ/ký hiệu viết tắt chưa từng xuất hiện trong thân bài (`L02`: `encoder`; `L05`: `EKF`; `L07`: `SLAM`, `1D`; `L09`: `DWA`; `L10`: `Pure Pursuit`, `e_lat`, `m^-1`; `L11`: `fx`, `cx`; `L13`: `lidar`).

### 2.2. Lỗi `covers:` (`E51` — `MUST` ở 14/14 bài)
Cả 14 bài có `objectives` khớp 100% giữa `curriculum/rob.yaml` và `lessons/rob/L*.yaml`, nhưng trường `covers:` bị gán máy móc:
- `L00..L09, L11..L12` (12 bài): đều gán `1 -> example, 2 -> check, 3 -> practice`, làm sai lệch hầu hết mục tiêu (ví dụ `L00` mục tiêu 1 *"Mô tả các khối và luồng dữ liệu"* nằm ở `sym`, mục tiêu 3 *"Hiểu kiểu xuất bản–đăng ký"* nằm ở `sym`, nhưng `covers` trỏ `example` và `practice` — cả hai cảnh này chỉ tính ngân sách `20 ms`). Tương tự ở `L01..L09, L11..L12`, mục tiêu 3 luôn trỏ `practice` dù `practice` không dạy các phần đó (như ràng buộc không trượt ngang `L01`, cảm biến ngoài `L02`, phân biệt mật độ/xác suất `L03`, lấy mẫu lại/ESS `L04`, khi nào tuyến tính hoá thất bại `L05`, vì sao phải chặn giá trị `L06`, tác hại đóng vòng sai `L07`, ước lượng số mẫu lối hẹp `L08`, ảnh hưởng trọng số `L09`, độ sâu hai camera & sai số `L11`, mô phỏng–thực tế `L12`).
- `L10`: `covers` trỏ `2 -> lookahead, 3 -> practice`, trong khi mục tiêu 2 (*"Đổi độ cong thành vận tốc góc"*) dạy ở `example`, còn mục tiêu 3 (*"Chọn khoảng nhìn trước theo tốc độ"*) dạy ở `lookahead`.
- `L13`: `covers` trỏ `1 -> stage1, 2 -> stage2, 3 -> practice`, trong khi mục tiêu 1 trải từ `stage1..stage5`, mục tiêu 2 trải từ `stage2..stage5`, và mục tiêu 3 (*"Quyết định tốc độ, cảm biến và lúc bỏ người đi kèm..."*) dạy ở `quiz`, không phải `practice`.

### 2.3. Kiểm tra `"càng "`, toán thô trong `say`, `SPELL_CANON`, `P9` (`Hai mức quy mô`), và `layout_ROB.tsv`
- **Các câu có `"càng "` trong `say`/`show`** (tổng 5 chỗ ở 5 bài, ngoài ra `L08` `intuition.title` có `"Càng rải nhiều điểm, càng dễ gặp lối hẹp"`):
  1. `L03` `prereq.0` (`show` & `say`): `"gần 2 m thì hay gặp, càng xa càng hiếm"`
  2. `L04` `intuition.0` (`say`): `"cột càng cao thì robot càng tin mình đang ở đó."`
  3. `L06` `sym.0` (`show` & `say`): `"$p$ càng gần 1 thì $l$ càng lớn không giới hạn."` / `"p càng gần 1 thì l càng lớn không giới hạn."`
  4. `L10` `lookahead.1` (`show` & `say`): `"xe càng nhanh càng nhìn xa, nên lệnh quay càng nhẹ."` / `"Xe càng nhanh thì lệnh quay càng nhẹ, nên không bị giật."`
  5. `L13` `stage5.1` (`show` & `say`): `"sự cố càng hiếm thì càng cần nhiều dặm mới kết luận được."`
- **Ký hiệu toán thô trong `say`**: **0/14 bài** (sạch 100%).
- **Lỗi `SPELL_CANON` và `term_canon.yaml`**: **0/14 bài** (`lv.lint` đạt 0 FAIL, 0 WARN trên cả 14 bài).
- **`P9` ("Hai mức quy mô" trong thân bài + `recap`)**: **0/14 bài** có hộp/ý `"Hai mức quy mô"` ở `recap`. Trong thân bài: 5 bài có ≥ 2 mức quy mô có số đo và đánh đổi (`L06` 5 cm vs 2 cm; `L08` 2D/3D/6D & 100/300 mẫu; `L11` 4 m vs 8 m & 1280×720 vs 640×360; `L12` 1,5 vs 3 m/s; `L13` 5 chặng quy mô); 5 bài chỉ ở mức 1 (`L00, L02, L03, L05, L10`); 4 bài ở mức 0 (`L01, L04, L07, L09`).
- **`audit/layout_ROB.tsv`**: Có kích thước 2 byte (1 dòng trống, biểu thị 0 lỗi khi quét), nhưng dấu thời gian là `2026-11-19 09:55:38`, **CŨ HƠN** lần sửa YAML thêm `practice` (`2026-11-19 16:07`) và lần dựng video (`2026-11-20 05:38Z–06:12Z`) → **STALE** (cần chạy lại `layout_scan.py ROB`).
- **`cham.sh` trên môi trường Windows mặc định**: `bash` trong `PATH` trỏ tới `C:\WINDOWS\system32\bash.exe` (WSL) nên lệnh `bash labs/cham.sh ...` thoát mã 1 nếu không gọi qua Git Bash hoặc Python trực tiếp.

---

## 3. Bảng tổng hợp từng bài `L00–L13`

| Bài | sha16 YAML | Phút | `spec` khớp | `SRT` khớp | `verify_rob` & `checks` | Lab chạy (`python`) | `P1` (chặt) | `P2` | `P3` | `P4` | `P5` | `P6` | `P7` | Tổng P1–P7 | `P8` | `P9` | `MUST` | `SHOULD` |
|---|---|---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|---:|
| `L00` | `637dcdebc032005e` | 8.15 | ✓ | ✓ (74/74) | PASS | PASS | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 1 | 2 | 3 |
| `L01` | `ca9da88550dcb13f` | 11.23 | ✓ | ✓ (93/93) | PASS | PASS | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 0 | 2 | 2 |
| `L02` | `c4572a9a48042087` | 8.90 | ✓ | ✓ (77/77) | PASS | PASS | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 1 | 2 | 3 |
| `L03` | `1c2a0c1c19d2bcd7` | 11.01 | ✓ | ✓ (96/96) | PASS | PASS | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 1 | 2 | 2 |
| `L04` | `f68e36cdc415f652` | 11.15 | ✓ | ✓ (96/96) | PASS | PASS | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 0 | 2 | 2 |
| `L05` | `df04f86d2a8be557` | 11.93 | ✓ | ✓ (96/96) | PASS | PASS | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 1 | 2 | 2 |
| `L06` | `2094ae67b1eeb313` | 10.11 | ✓ | ✓ (79/79) | PASS | PASS | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | 0 | 2 | 2 | 2 |
| `L07` | `ac9c9320fad19558` | 9.94 | ✓ | ✓ (86/86) | PASS | PASS (SAI TOÁN) | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 0 | 3 | 2 |
| `L08` | `5db251c8d1f355f5` | 10.00 | ✓ | ✓ (86/86) | PASS | PASS | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 2 | 2 | 2 |
| `L09` | `3c0ad55bc6876bc9` | 10.04 | ✓ | ✓ (84/84) | PASS | PASS | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 0 | 3 | 1 |
| `L10` | `8ab3d868a2059e66` | 11.25 | ✓ | ✓ (96/96) | PASS | PASS | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 1 | 2 | 2 |
| `L11` | `546bd12ca19184aa` | 9.77 | ✓ | ✓ (78/78) | PASS | PASS | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 2 | 2 | 2 |
| `L12` | `0a8540d5af6ee850` | 10.55 | ✓ | ✓ (86/86) | PASS | PASS | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | 0 | 2 | 2 | 2 |
| `L13` | `c8d74aa72c0d86d4` | 16.98 | ✓ | ✓ (151/151) | PASS | PASS (SAI DỮ KIỆN) | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | 0 | 2 | 3 | 2 |

*(Lưu ý: `P7 = 1` đồng loạt vì `objectives` khớp nội dung bài nhưng `covers:` trỏ sai cảnh. Thân bài `L00–L13` giảng cơ chế/tính tay/tự kiểm/lỗi nghề nghiệp rất vững nên `P2=P3=P4=P5=P6=2` trên toàn bộ 14 bài.)*

---

## 4. Chi tiết `MUST / SHOULD / INFO` từng bài (`L00–L13`)

### `L00` (`lessons/rob/L00_kien_truc_robot.yaml`, `labs/ROB/L00`)
- **MUST**:
  1. `practice.1–3` (`L00_kien_truc_robot.yaml:251–264`): Lộ toàn bộ code lời giải (`budget = 1000 / 50 ...`) và stdout (`budget_ms=20 used_ms=16 margin_ms=4`) TRƯỚC `pause: 30` (`P8 = 0`).
  2. `covers` (`L00_kien_truc_robot.yaml:287–293`): Mục tiêu 1 (*"Mô tả các khối và luồng dữ liệu"*) trỏ `example` (ngân sách 20 ms) thay vì `sym`; mục tiêu 3 (*"Hiểu kiểu xuất bản–đăng ký"*) trỏ `practice` thay vì `sym` (`E51`).
- **SHOULD**:
  1. `P1`: `practice#0` ghi `f"{val:.3f}"` trong khi `practice#1` dùng `:.0f`, gán `=` không giảng, `practice#3` dùng `bash labs/cham.sh ...` chưa giảng (`P1 = 0`).
  2. `labs/ROB/L00/de.md`: Không ghi định dạng stdout `budget_ms=20 used_ms=16 margin_ms=4` và dùng trùng y nguyên số ví dụ (`4+9+2+1`, `50 Hz`).
  3. Thời lượng `8.15 phút` < ngưỡng 9 phút (`BRIEF_AF2.md` §10) và `recap` thiếu `"Hai mức quy mô"` (`P9 = 1`).
- **INFO**: `check.0` khai `introduces: [geq]` trong khi HTML viết `\le 20` (nên là `leq`). `asr_report.md`: 74 câu, 8 gắn cờ, 0 chưa xem xét.

### `L01` (`lessons/rob/L01_xe_vi_sai.yaml`, `labs/ROB/L01`)
- **MUST**:
  1. `practice.1–3` (`L01_xe_vi_sai.yaml:331–344`): Lộ code `loi_giai.py` và stdout `v=0.5m/s omega=0.4rad/s R=1.25m` trước `pause: 30` (`P8 = 0`).
  2. `covers` (`L01_xe_vi_sai.yaml:367–373`): Mục tiêu 2 (*"Tính bán kính quay"*) trỏ `check` (thử quãng đường); mục tiêu 3 (*"Hiểu ràng buộc không trượt ngang"*) trỏ `practice` thay vì `sym`/`pitfalls` (`E51`).
- **SHOULD**:
  1. `P1`: `practice#1` dùng `vl, vr, L = 0.4, 0.6, 0.5`, `:.1f`, `:.2f` trong khi `practice#0` chỉ ghi `:.3f`; `practice#3` dùng `bash labs/cham.sh ...` chưa giảng (`P1 = 0`).
  2. `labs/ROB/L01/de.md`: Thiếu định dạng stdout; trùng số ví dụ (`0.4, 0.6, 0.5`). Thiếu cảnh so sánh ≥ 2 mức quy mô trong thân bài và `recap` (`P9 = 0`).
- **INFO**: `asr_report.md`: 93 câu, 23 gắn cờ, 0 chưa xem xét.

### `L02` (`lessons/rob/L02_do_quang_duong.yaml`, `labs/ROB/L02`)
- **MUST**:
  1. `practice.1–3` (`L02_do_quang_duong.yaml:265–278`): Lộ code `loi_giai.py` và stdout `mm_per_tick=0.314 lateral_err_10m=0.175m` trước `pause: 30` (`P8 = 0`).
  2. `covers` (`L02_do_quang_duong.yaml:301–307`): Mục tiêu 2 (*"Giải thích vì sao sai số hướng làm sai số vị trí lớn nhanh"*) trỏ `check`; mục tiêu 3 (*"Biết vì sao cần cảm biến bên ngoài"*) trỏ `practice` thay vì `pitfalls` (`E51`).
- **SHOULD**:
  1. `P1`: `practice#0` liệt kê `math.log / exp / sqrt` nhưng `practice#1` dùng `math.pi`, `math.sin`, `math.radians`; `practice#3` dùng từ `"encoder"` chưa định nghĩa trong bài; `bash labs/cham.sh ...` chưa giảng (`P1 = 0`).
  2. `labs/ROB/L02/de.md`: Thiếu định dạng stdout; trùng số ví dụ (`0.1 m, 1000 xung, 1°, 10 m`).
  3. Thời lượng `8.90 phút` < 9 phút; `recap` thiếu `"Hai mức quy mô"` (`P9 = 1`).
- **INFO**: `pitfalls.2` `show` viết `"con quay hồi chuyển"` (trong `say` giải thích là `"cảm biến đo góc quay"`). `asr_report.md`: 77 câu, 6 gắn cờ, 0 chưa xem xét.

### `L03` (`lessons/rob/L03_mo_hinh_cam_bien.yaml`, `labs/ROB/L03`)
- **MUST**:
  1. `practice.1–3` (`L03_mo_hinh_cam_bien.yaml:294–307`): Lộ code `loi_giai.py` và stdout `pdf_21=2.42 pdf_23=0.044 ratio=54.6x` trước `pause: 30` (`P8 = 0`).
  2. `covers` (`L03_mo_hinh_cam_bien.yaml:330–336`): Mục tiêu 2 (*"Hiểu vì sao cần thành phần đo hỏng"*) trỏ `check`; mục tiêu 3 (*"Phân biệt mật độ và xác suất"*) trỏ `practice` thay vì `prereq`/`check` (`E51`).
- **SHOULD**:
  1. `P1`: `practice#0` thiếu tham số mặc định `lambda z, mu=2.0, s=0.1:`, toán tử `**`, `math.pi`, `d1, d3 = ...`, `:.2f`, `:.1f`, `print(...)`, và `bash labs/cham.sh ...` (`P1 = 0`).
  2. `labs/ROB/L03/de.md`: Thiếu định dạng stdout; trùng số ví dụ (`2.0, 0.1, 2.1, 2.3`). `P9 = 1` (`pitfalls.1` chỉ có 1 mức 10 tia → 1024 lần, chưa có mức thứ 2 & chưa vào `recap`).
- **INFO**: `prereq.0` có câu `"gần 2 m thì hay gặp, càng xa càng hiếm"`. `asr_report.md`: 96 câu, 5 gắn cờ, 0 chưa xem xét.

### `L04` (`lessons/rob/L04_dinh_vi_loc_bayes.yaml`, `labs/ROB/L04`)
- **MUST**:
  1. `practice.1–3` (`L04_dinh_vi_loc_bayes.yaml:318–331`): Lộ code `loi_giai.py` và stdout `p_door1=0.258 p_wall0=0.032 sum=1.0` trước `pause: 30` (`P8 = 0`).
  2. `covers` (`L04_dinh_vi_loc_bayes.yaml:354–360`): Mục tiêu 2 trỏ `check`; mục tiêu 3 (*"Giải thích lấy mẫu lại và kích thước mẫu hiệu dụng"*) trỏ `practice` thay vì `sym`/`pitfalls` (`E51`).
- **SHOULD**:
  1. `P1`: `practice#0` thiếu `{1, 4, 7}`, `... if ... in ... else ...`, `range(10)`, `bel[1]`, `:.1f`, `bash labs/cham.sh ...` (`P1 = 0`).
  2. `labs/ROB/L04/de.md`: Thiếu định dạng stdout; trùng số ví dụ (`{1,4,7}`, `0.8`, `0.1`). Thiếu so sánh ≥ 2 mức quy mô (`P9 = 0`).
- **INFO**: `intuition.0` `say` có `"cột càng cao thì robot càng tin mình đang ở đó."`. `asr_report.md`: 96 câu, 8 gắn cờ, 0 chưa xem xét.

### `L05` (`lessons/rob/L05_kalman_mo_rong.yaml`, `labs/ROB/L05`)
- **MUST**:
  1. `practice.1–3` (`L05_kalman_mo_rong.yaml:314–327`): Lộ code `loi_giai.py` và stdout `jac_theta=(-0.0, 1.0)` trước `pause: 30` (`P8 = 0`).
  2. `covers` (`L05_kalman_mo_rong.yaml:350–356`): Mục tiêu 2 trỏ `check`; mục tiêu 3 (*"Biết khi nào tuyến tính hoá thất bại"*) trỏ `practice` thay vì `intuition`/`pitfalls` (`E51`).
- **SHOULD**:
  1. `P1`: `practice#0` ghi `math.log / exp / sqrt` và `:.3f` nhưng `practice#1` dùng `math.sin`, `math.cos`, `vh, th = 1.0, 0.0`, `:.1f`; `practice#3` dùng `EKF` chưa giảng trong thân bài; `example.1` dùng `\operatorname{diag}` chưa giải thích ký hiệu trên màn hình; `bash labs/cham.sh ...` chưa giảng (`P1 = 0`).
  2. `labs/ROB/L05/de.md`: Thiếu định dạng stdout; trùng số ví dụ (`vh=1, th=0`). `recap` thiếu `"Hai mức quy mô"` (`P9 = 1`).
- **INFO**: `asr_report.md`: 96 câu, 11 gắn cờ, 0 chưa xem xét.

### `L06` (`lessons/rob/L06_ban_do_luoi.yaml`, `labs/ROB/L06`)
- **MUST**:
  1. `practice.1–3` (`L06_ban_do_luoi.yaml:277–290`): Lộ code `loi_giai.py` và stdout `log_odds_3=2.542 prob=0.927` trước `pause: 30` (`P8 = 0`).
  2. `covers` (`L06_ban_do_luoi.yaml:313–319`): Mục tiêu 2 trỏ `check`; mục tiêu 3 (*"Biết vì sao phải chặn giá trị"*) trỏ `practice` thay vì `intuition`/`pitfalls` (`E51`).
- **SHOULD**:
  1. `P1 = 1`: `practice#0` khớp tốt nhất khoá (`import`, `math.log`, `math.exp`, `:.3f`, `print`), chỉ còn `bash labs/cham.sh ...` chưa giảng và `MB` (`pitfalls.3`) viết tắt chưa giải thích tại chỗ.
  2. `labs/ROB/L06/de.md`: Thiếu định dạng stdout; trùng số ví dụ (`3 lần 0.7`). Thân bài có 2 mức quy mô rất tốt (`pitfalls.3`: ô 5 cm vs 2 cm), nhưng thiếu tóm tắt `"Hai mức quy mô"` trong `recap`.
- **INFO**: `sym.0` có `"$p$ càng gần 1 thì $l$ càng lớn không giới hạn."`. `asr_report.md`: 79 câu, 9 gắn cờ, 0 chưa xem xét.

### `L07` (`lessons/rob/L07_do_thi_tu_the.yaml`, `labs/ROB/L07`) — **CÓ LỖI TOÁN HỌC NGHIÊM TRỌNG Ở LAB**
- **MUST**:
  1. **Sai toán học ở `labs/ROB/L07/{de.md, loi_giai.py, mong_doi.txt}` & `practice#1..4` (`L07_do_thi_tu_the.yaml:266–281`)**: `de.md` yêu cầu bài toán tối thiểu bình phương với 3 đoạn `+1 m` và đo vòng khép kín `2.7 m`, nhưng lại viết *"phân bổ lượng chỉnh `-0.1 m/đoạn` tối thiểu bình phương"* và `loi_giai.py` tính `err / 3.0` ra `[0.0, 0.9, 1.8, 2.7]`. **SAI!** Theo đúng thân bài `L07` (`example`, `check`, `verify_rob.py`), bài toán có **4 cạnh** (3 cạnh quãng đường + 1 cạnh đóng vòng), nghiệm bình phương tối thiểu chia đều sai lệch cho **4 cạnh** (`-0.3 / 4 = -0.075 m/cạnh`), cho `[0.0, 0.925, 1.85, 2.775]` (tổng bình phương sai lệch `0.0225`). Chính cảnh `check` của `L07` (dòng 159) đã chứng minh `[0.0, 0.9, 1.8, 2.7]` là phương án *sai* ("tin hẳn đóng vòng", tổng bình phương `0.03 > 0.0225`).
  2. `practice.1–3`: Lộ code và stdout trước `pause: 30` (`P8 = 0`).
  3. `covers` (`L07_do_thi_tu_the.yaml:302–308`): Mục tiêu 1 trỏ `example`, mục tiêu 2 trỏ `check`, mục tiêu 3 (*"Hiểu tác hại của đóng vòng sai"*) trỏ `practice` thay vì `pitfalls` (`E51`).
- **SHOULD**:
  1. `P1`: `practice#0` ghi `:.3f` (không dùng), thiếu `;`, `raw[-1]`, `range(4)`, `round(..., 2)`, `SLAM`, `1D` (`practice#3`), `bash labs/cham.sh ...` (`P1 = 0`).
  2. `labs/ROB/L07/de.md`: Thiếu định dạng stdout; trùng số ví dụ (`1, 1, 1` và `2.7`). Thiếu so sánh ≥ 2 mức quy mô trong thân bài và `recap` (`P9 = 0`).
- **INFO**: `asr_report.md`: 86 câu, 3 gắn cờ, 0 chưa xem xét.

### `L08` (`lessons/rob/L08_lap_ke_hoach_theo_mau.yaml`, `labs/ROB/L08`)
- **MUST**:
  1. `practice.1–3` (`L08_lap_ke_hoach_theo_mau.yaml:274–287`): Lộ code `loi_giai.py` và stdout `grid_6dof=1e+12 needs_sampling=1` trước `pause: 30` (`P8 = 0`).
  2. `covers` (`L08_lap_ke_hoach_theo_mau.yaml:310–316`): Mục tiêu 2 (*"Mô tả bản đồ ngẫu nhiên và cây mở rộng nhanh"*) trỏ `check`; mục tiêu 3 (*"Ước lượng số mẫu cần cho lối hẹp"*) trỏ `practice` thay vì `example`/`quiz` (`E51`).
- **SHOULD**:
  1. `P1`: `practice#0` thiếu `**`, ghi `:.3f` nhưng code dùng `:.0e`; thiếu giảng `bash labs/cham.sh ...` (`P1 = 0`).
  2. `labs/ROB/L08/de.md`: Thiếu định dạng stdout; trùng số ví dụ (`100^6`). Thân bài có ≥ 2 mức quy mô (2D/3D/6D; 100/300 mẫu) nhưng thiếu tóm tắt `"Hai mức quy mô"` ở `recap`.
- **INFO**: `intuition.title` có `"Càng rải nhiều điểm..."`. `asr_report.md`: 86 câu, 4 gắn cờ, 0 chưa xem xét.

### `L09` (`lessons/rob/L09_cua_so_dong.yaml`, `labs/ROB/L09`)
- **MUST**:
  1. **`labs/ROB/L09/de.md` thiếu hoàn toàn dữ liệu đầu vào của bài toán** (`cands = [((0.5, 0.0), 0.7, 0.6, 0.5), ((0.3, 0.5), 0.9, 0.8, 0.3), ((0.1, -0.5), 0.4, 0.9, 0.1)]`): đề chỉ viết *"Tính điểm ba ứng viên và chọn cặp có điểm tổng hợp cao nhất"* dù số liệu khác ví dụ trong bài → người học không thể tự làm từ `de.md`!
  2. `practice.1–3` (`L09_cua_so_dong.yaml:275–288`): Lộ code `loi_giai.py` và stdout trước `pause: 30` (`P8 = 0`).
  3. `covers` (`L09_cua_so_dong.yaml:311–317`): Mục tiêu 2 (*"Loại vận tốc không dừng kịp"*) trỏ `check`; mục tiêu 3 (*"Chấm điểm và thấy ảnh hưởng của trọng số"*) trỏ `practice` thay vì `example`/`quiz` (`E51`).
- **SHOULD**:
  1. `P1`: `practice#0` ghi `:.3f` (không dùng), thiếu tuple lồng nhau, giải nén 4 phần tử, `round(..., 2)`, `max(scored)` trên tuple, `DWA` (`practice#3`), `bash labs/cham.sh ...` (`P1 = 0`). Thiếu định dạng stdout trong `de.md`; thiếu so sánh ≥ 2 mức quy mô (`P9 = 0`).
- **INFO**: `asr_report.md`: 84 câu, 5 gắn cờ, 0 chưa xem xét.

### `L10` (`lessons/rob/L10_bam_quy_dao.yaml`, `labs/ROB/L10`)
- **MUST**:
  1. `practice.1–3` (`L10_bam_quy_dao.yaml:326–339`): Lộ code `loi_giai.py` và stdout `curvature=0.25 radius=4.0m` trước `pause: 30` (`P8 = 0`).
  2. `covers` (`L10_bam_quy_dao.yaml:362–368`): Mục tiêu 2 (*"Đổi độ cong thành vận tốc góc"*) trỏ `lookahead` thay vì `example`; mục tiêu 3 (*"Chọn khoảng nhìn trước theo tốc độ"*) trỏ `practice` thay vì `lookahead` (`E51`).
- **SHOULD**:
  1. `P1`: `practice#0` ghi `:.3f` nhưng code dùng `:.2f`, `:.1f` và `L, e = 2.0, 0.5`; `practice#3` dùng `"Pure Pursuit"`, `"e_lat"`, `"m^-1"` chưa định nghĩa trong bài; thiếu giảng `bash labs/cham.sh ...` (`P1 = 0`).
  2. `labs/ROB/L10/de.md`: Thiếu định dạng stdout; trùng số ví dụ (`L=2, e=0.5`). `recap` thiếu `"Hai mức quy mô"` (`P9 = 1`).
- **INFO**: `lookahead.1` có `"xe càng nhanh càng nhìn xa, nên lệnh quay càng nhẹ."`. `asr_report.md`: 96 câu, 9 gắn cờ, 0 chưa xem xét.

### `L11` (`lessons/rob/L11_camera_lo_kim.yaml`, `labs/ROB/L11`)
- **MUST**:
  1. `practice.1–3` (`L11_camera_lo_kim.yaml:253–266`): Lộ code `loi_giai.py` và stdout `u_px=740` trước `pause: 30` (`P8 = 0`).
  2. `covers` (`L11_camera_lo_kim.yaml:289–295`): Mục tiêu 2 (*"Hiểu vì sao một camera không đo được độ sâu"*) trỏ `check`; mục tiêu 3 (*"Tính độ sâu từ hai camera và sai số của nó"*) trỏ `practice` thay vì `example`/`pitfalls` (`E51`).
- **SHOULD**:
  1. `P1`: `practice#0` ghi `:.3f` nhưng code dùng `:.0f`; `practice#3` ghi `fx`, `cx` (thân bài dùng `f`, `c_x`); thiếu giảng `bash labs/cham.sh ...` (`P1 = 0`).
  2. `labs/ROB/L11/de.md`: Thiếu định dạng stdout; trùng số ví dụ (`800, 640, 0.5, 4`). Thân bài có 2 mức quy mô tốt (4 m vs 8 m; 1280×720 vs 640×360), nhưng `recap` thiếu `"Hai mức quy mô"`.
- **INFO**: `asr_report.md`: 78 câu, 3 gắn cờ, 0 chưa xem xét.

### `L12` (`lessons/rob/L12_an_toan_kiem_thu.yaml`, `labs/ROB/L12`)
- **MUST**:
  1. `practice.1–3` (`L12_an_toan_kiem_thu.yaml:279–292`): Lộ code `loi_giai.py` và stdout `stop_dist_m=1.425` trước `pause: 30` (`P8 = 0`).
  2. `covers` (`L12_an_toan_kiem_thu.yaml:315–321`): Mục tiêu 2 (*"Tính tốc độ tối đa theo tầm phát hiện"*) trỏ `check`; mục tiêu 3 (*"Giải thích khoảng cách giữa mô phỏng và thực tế"*) trỏ `practice` thay vì `pitfalls` (`E51`).
- **SHOULD**:
  1. `P1 = 1`: `practice#1` dùng gán nhiều biến `v, a, td = 1.5, 1.0, 0.2` và `practice#3` dùng `bash labs/cham.sh ...` chưa giảng.
  2. `labs/ROB/L12/de.md`: Thiếu định dạng stdout; trùng số ví dụ (`1.5, 1.0, 0.2`). Thân bài có 2 mức quy mô (`1.5` vs `3 m/s` → `1.425` vs `5.1 m`), nhưng `recap` thiếu `"Hai mức quy mô"`.
- **INFO**: `asr_report.md`: 86 câu, 3 gắn cờ, 0 chưa xem xét.

### `L13` (`lessons/rob/L13_hanh_trinh_xe_tu_lai.yaml`, `labs/ROB/L13`) — **CÓ LỖI DỮ KIỆN & CÔNG THỨC Ở LAB**
- **MUST**:
  1. **Sai dữ kiện và công thức ở `labs/ROB/L13/{de.md, loi_giai.py, mong_doi.txt}` & `practice#1..4` (`L13_hanh_trinh_xe_tu_lai.yaml:520–535`)**:
     - Tiêu đề `de.md` & `practice#3` ghi `"2004->2007"`, trong khi bài L13 dạy 5 chặng `2004 → 2005 → 2009–2020 → 2023–2025` (không hề có năm 2007).
     - `loi_giai.py` tính `ratio_dist = (35.0 / 25.0) ** 2` (`1.96x`) và đặt tên là `stop_dist_ratio`, trong khi công thức quãng dừng của chính bài (`v*t + v^2/(2a)`) cho `17.8 m` tại `25 mph` và `33.7 m` tại `35 mph`, tức tỉ số quãng dừng thật là `33.7 / 17.8 = 1.89x` (`1.96x` chỉ là tỉ số phần phanh thuần tuý, bỏ qua quãng phản ứng `v*t`).
  2. `practice.1–3`: Lộ code và stdout trước `pause: 30` (`P8 = 0`).
  3. `covers` (`L13_hanh_trinh_xe_tu_lai.yaml:556–562`): Mục tiêu 3 (*"Quyết định tốc độ, cảm biến và lúc bỏ người đi kèm..."*) trỏ `practice` thay vì `quiz` (`E51`).
- **SHOULD**:
  1. `P1`: `practice#0` thiếu `**`, ghi `:.3f` nhưng code dùng `:.1f`, `:.2f`; `practice#3` dùng từ `"lidar"` chưa xuất hiện trong bài (bài dùng `"máy quét laser"` / `"máy quét tia sáng"`); thiếu giảng `bash labs/cham.sh ...` (`P1 = 0`).
  2. `labs/ROB/L13/de.md`: Thiếu định dạng stdout; trùng số bài (`5% × 142`, `25 -> 35 mph`). `recap` thiếu tóm tắt 2 mức quy mô cụ thể (ví dụ `7,14` vs `56,7 triệu dặm`).
- **INFO**: Mọi sự kiện/con số trích từ `[ST06]`, `[WM20]`, `[WS20]`, `[KU24]`, `[KU25]` trong thân bài đều khớp hoàn toàn `audit/rob/sources_L13.md`. Có câu `"sự cố càng hiếm thì càng cần nhiều dặm"` ở `stage5.1`. `asr_report.md`: 151 câu, 2 gắn cờ, 0 chưa xem xét.

---

## 5. Người học mất gốc kẹt ở đâu?

- **Trong phần lý thuyết (`hook`..`quiz`)**: Người học mất gốc **theo được rất tốt** ở cả 14 bài vì từng bài đều có `prereq` ôn toán tại chỗ, `sym` giải mã ký hiệu, `intuition` vẽ SVG, `example` + `check` làm tay từng bước, và `quiz` dừng kiểm tra hiểu. Điểm kẹt nhỏ lẻ trong thân bài chỉ là `\operatorname{diag}` (`L05` `example.1`), `"con quay hồi chuyển"` trên chữ màn hình (`L02` `pitfalls.2`), và `"MB"` (`L06` `pitfalls.3`).
- **Khi tới phần Tự làm (`practice` + `labs/ROB/Lxx/`)**: Người học kẹt hàng loạt vì:
  1. `practice#0` giải thích **sai bộ ký hiệu** so với code ở `practice#1` (`L00–L05, L07–L13`: đọc bảng `:.3f` hay `math.log/exp/sqrt` xong nhìn xuống lại thấy `:.0f`, `math.sin`, `lambda z, mu=2.0`, `{1,4,7}`, `raw[-1]`, `:.0e`, tuple lồng nhau…).
  2. `practice#1/#2` cho xem luôn lời giải và đáp án trước khi dừng (`practice#3`), nhưng nếu người học tự mở `labs/ROB/Lxx/de.md` để tự viết từ đầu thì **kẹt ngay vì `de.md` không ghi định dạng `stdout`**, riêng `L09/de.md` không ghi cả số đầu vào của 3 ứng viên, còn `L07/de.md` và `L13/de.md` lại ra công thức/đáp số mâu thuẫn với chính bài giảng vừa nghe.
  3. Trên Windows mặc định, gõ `bash labs/cham.sh ...` không kèm giải thích môi trường có thể gọi nhầm `C:\WINDOWS\system32\bash.exe`.

---

## 6. Danh sách toàn bộ 45 ảnh PNG đã xem trực tiếp (`read_file`)

Tất cả 45 khung hình dưới đây đã được mở và kiểm tra trực tiếp bằng `read_file`: **không đè chữ, không cắt công thức KaTeX/SVG, tương phản đạt chuẩn**.

- **`L00`**: `out/ROB/L00/frames/00019.png` (`intuition#0` SVG), `00062.png` (`practice#0`), `00063.png` (`practice#1`), `00065.png` (`practice#3`)
- **`L01`**: `out/ROB/L01/frames/00024.png` (`intuition#0` SVG), `00081.png` (`practice#0`), `00082.png` (`practice#1`)
- **`L02`**: `out/ROB/L02/frames/00019.png` (`intuition#0` SVG), `00065.png` (`practice#0`), `00066.png` (`practice#1`)
- **`L03`**: `out/ROB/L03/frames/00028.png` (`intuition#0` SVG), `00083.png` (`practice#0`), `00084.png` (`practice#1`)
- **`L04`**: `out/ROB/L04/frames/00031.png` (`intuition#0` SVG), `00084.png` (`practice#0`), `00085.png` (`practice#1`)
- **`L05`**: `out/ROB/L05/frames/00040.png` (`intuition#0` SVG), `00083.png` (`practice#0`), `00084.png` (`practice#1`)
- **`L06`**: `out/ROB/L06/frames/00021.png` (`intuition#0` SVG), `00024.png` (`intuition#1` SVG), `00067.png` (`practice#0`), `00068.png` (`practice#1`)
- **`L07`**: `out/ROB/L07/frames/00020.png` (`intuition#0` SVG), `00074.png` (`practice#0`), `00075.png` (`practice#1`), `00077.png` (`practice#3`)
- **`L08`**: `out/ROB/L08/frames/00024.png` (`intuition#0` SVG), `00074.png` (`practice#0`), `00075.png` (`practice#1`)
- **`L09`**: `out/ROB/L09/frames/00019.png` (`intuition#0` SVG), `00072.png` (`practice#0`), `00073.png` (`practice#1`)
- **`L10`**: `out/ROB/L10/frames/00019.png` (`intuition#0` SVG), `00084.png` (`practice#0`), `00085.png` (`practice#1`)
- **`L11`**: `out/ROB/L11/frames/00019.png` (`intuition#0` SVG), `00065.png` (`practice#0`), `00066.png` (`practice#1`)
- **`L12`**: `out/ROB/L12/frames/00018.png` (`intuition#0` SVG), `00072.png` (`practice#0`), `00073.png` (`practice#1`)
- **`L13`**: `out/ROB/L13/frames/00018.png` (`timeline#0` SVG), `00024.png` (`range_mech#0` SVG), `00133.png` (`practice#0`), `00134.png` (`practice#1`), `00136.png` (`practice#3`)
