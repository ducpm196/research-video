# Báo cáo kiểm định WP-AF4-5 Stage 11 — RBM L10–L17 (CHỈ ĐỌC 100%)

## 1. Kết luận: **NO-GO**
Tất cả 8/8 bài (`L10–L17`) đều khớp toàn vẹn kỹ thuật dựng (`spec_sha256` khớp 8/8, `L*.srt == say` khớp 8/8, `checks` tự động 212/212 PASS, `loi_giai.py == mong_doi.txt` 8/8, nội dung toán học thân bài chính xác và L17 tuân thủ `sources_L17.md`), **NHƯNG cả 8/8 bài đều trượt ở tiêu chí AF4**: (1) `practice` lộ toàn bộ mã lời giải + đầu ra mong đợi **trước** `pause: 30` (P8 = 0/1); (2) `labs/RBM/L10..L17/de.md` không tự đứng được, riêng L10 mâu thuẫn mô hình/kết quả với lời giải; (3) `P1` trong `practice`/`de.md` dùng hàng loạt cú pháp Python/CLI chưa từng giảng ở khoá RBM và bảng "viết trong mã → đọc và hiểu là" cũng không phủ hết; (4) `covers:` ở cả 8/8 bài trỏ sai cảnh dạy mục tiêu; (5) P9 thiếu 2 mức quy mô/thời gian trong `recap` ở `L10–L16`.

## 2. Bảng tóm tắt toàn bộ chỉ số (RBM L10–L17)
| Chỉ số | Kết quả | Chi tiết |
|---|---|---|
| Số bài đã kiểm | **8 / 8** | `L10–L17` |
| Số bài **MUST = 0** | **0 / 8** | 8/8 bài có ≥ 3 lỗi MUST (lộ `practice` trước `pause`, `de.md` không tự đứng, `covers:` trỏ sai cảnh, P1 `practice`/`de.md`) |
| Số bài **P1 = 2** (chuẩn CHẶT, gồm `practice` & `de.md`) | **0 / 8** | Thân bài chính sạch, nhưng `practice` + `de.md` đều có ≥ 3 cú pháp Python/CLI chưa giảng |
| Số bài **P8 = 2** | **0 / 8** | Cả 8 bài P8 = 0 hoặc 1 do lộ lời giải + đáp án trước `pause: 30` và `de.md` thiếu thông số + định dạng xuất |
| Số bài **P9 = 2** (2 mức quy mô thân bài & `recap`) | **1 / 8** | Chỉ `L17` đạt P9 = 2; `L10–L13, L15–L16` đạt 1 (thiếu trong `recap`); `L14` đạt 0 |
| Số bài **`spec_sha256` khớp** (`build_report.json` vs `lv.spec_digest`) | **8 / 8** | Khớp 100% ở tất cả `L10–L17` |
| Số bài **`L*.srt == say` khớp** | **8 / 8** | Khớp từng câu (`94, 101, 100, 91, 105, 93, 106, 156` câu), `asr_report.md` thiếu audio = 0, chưa xem xét = 0 |
| Số bài **checks nội tại** tự tính lại | **212 / 212** | `L10`: 23/23, `L11`: 30/30, `L12`: 25/25, `L13`: 24/24, `L14`: 25/25, `L15`: 23/23, `L16`: 27/27, `L17`: 35/35 |
| Số bài **lab chạy thật** (`loi_giai.py` vs `mong_doi.txt`) | **8 / 8** | Chạy bằng `.venv/Scripts/python.exe` khớp 100% `mong_doi.txt` (lưu ý `bash labs/cham.sh` lỗi môi trường shell Windows: `Bash/E_ACCESSDENIED` / Git Bash `-1073741502`) |
| Số phát hiện **SHOULD** | **13** | 7 bài `L10–L16` thiếu P9 trong `recap`; 5 lần `"càng "` trong `say` (`L10, L12×2, L16, L17`); 1 đè chữ nhẹ SVG (`L16` `00041.png`) |
| Tổng số PNG đã mở xem | **41 PNG** | 5–6 khung/bài cho cả 8/8 bài |

---

## 3. Bảng từng bài P1–P9
| Bài | sha16 lúc đọc | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | Mất gốc | P8 | P9 | Cần biết trước (thuật ngữ/kỹ năng bài DÙNG mà KHÔNG giảng tại chỗ) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| `L10` | `43681b3433c620a2` | 10,44 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 1 | Python (`=`, `for _ in range`, `+=`, `;`, `abs`, `:.2f/.4f`), bash CLI; `dt` trong `∫e dt` |
| `L11` | `5d40236190165933` | 12,13 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 1 | Python (`lambda`, `**`, `f"{:.2f/.1f/.5f}"`), bash CLI |
| `L12` | `a0d0ae70ae59b2eb` | 11,61 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 1 | Python (gán tuple nhiều biến, `/`, `*`, `:.1f`), bash CLI |
| `L13` | `dfb5a64c73221e4b` | 10,65 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 1 | Python (`list` 2D `P[0][0]`, `#` comment, `:.1f`), bash CLI |
| `L14` | `66b43a0ef08e0017` | 11,55 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 0 | Python (gán nhiều biến, `abs`, `:.0f`), bash CLI, thuật ngữ `alias` trong `de.md` |
| `L15` | `30e75139056883cf` | 10,56 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 1 | Python (`import heapq`, `set`, `dict.get`, `while`, `heappop/heappush`, `break`, `and`, `not in`, `0 <= v[0] < 3`), bash CLI |
| `L16` | `5fd91803eaeb9211` | 12,06 | 0 | 2 | 1 | 2 | 2 | 2 | 1 | 10 | GẦN | 0 | 1 | Python (list tuple, generator expression `x for x, _ in pts`, `**2`, `:.2f`), bash CLI |
| `L17` | `75a802309fd576f0` | 19,67 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 0 | 2 | Python (gán nhiều biến, `for _ in range(99)`, `:.2f`), bash CLI; ký hiệu `32K` (bộ nhớ) trong thân bài |

*(Ghi chú: P7 = 1 cho cả 8 bài vì `covers:` trỏ sai cảnh dạy mục tiêu và mục tiêu 3 đều trỏ vào `practice` không đạt yêu cầu tự đứng; riêng thân bài toán học của L10–L17 nếu tách riêng khỏi `practice`/`de.md` có P1–P6 rất tốt.)*

---

## 4. Chi tiết phát hiện MUST / SHOULD / INFO

### A. Lỗi MUST
1. **[MUST — 8/8 bài `L10–L17`] `practice` lộ toàn bộ mã lời giải và đầu ra mong đợi TRƯỚC `pause: 30` (P8 hỏng)**
   - **Vị trí & trích chữ**:
     - `L10` (`43681b3433c620a2`, d. 298–314): step 1 in nguyên `loi_giai.py` (`k = 4.0 ... print(f"P_steady_err=...")`), step 2 in `P_steady_err=0.20 PI_final_err=0.2338`, rồi mới tới step 3 `pause: 30`.
     - `L11` (`5d40236190165933`, d. 358–374): step 1 in nguyên `loi_giai.py`, step 2 in `g_025=-1.50 x10_div=57.7 x10_conv=0.00098` trước step 3 `pause: 30`.
     - `L12` (`a0d0ae70ae59b2eb`, d. 318–334): step 1 in nguyên `loi_giai.py`, step 2 in `K=0.5 x_est=0.5 P_est=0.5` trước step 3 `pause: 30`.
     - `L13` (`dfb5a64c73221e4b`, d. 315–331): step 1 in nguyên `loi_giai.py`, step 2 in `pred_var_pos=2.0 cross_cov_pos_vel=1.0` trước step 3 `pause: 30`.
     - `L14` (`66b43a0ef08e0017`, d. 401–417): step 1 in nguyên `loi_giai.py`, step 2 in `need_fs_gt=14Hz observed_alias=3Hz` trước step 3 `pause: 30`.
     - `L15` (`30e75139056883cf`, d. 328–344): step 1 in nguyên `loi_giai.py`, step 2 in `astar_steps=5 h_start=3` trước step 3 `pause: 30`.
     - `L16` (`5fd91803eaeb9211`, d. 341–357): step 1 in nguyên `loi_giai.py`, step 2 in `slope=1.98 intercept=1.03` trước step 3 `pause: 30`.
     - `L17` (`75a802309fd576f0`, d. 537–553): step 1 in nguyên `loi_giai.py`, step 2 in `P_after_99_Q0=0.01` trước step 3 `pause: 30`.
   - **Đối chiếu `audit/review/screen_code/RBM.yaml`**: Khối `RBM L10..L17 practice 1 0` và `practice 2 0` (d. 183–326) đều nằm trước `pause: 30` (step 3).

2. **[MUST — 8/8 bài `L10–L17`] `labs/RBM/L10..L17/de.md` KHÔNG tự đứng được; riêng `L10` mâu thuẫn kiến thức với `loi_giai.py`**
   - **`L10/de.md`** (d. 1–8): `"So sánh đáp ứng phản hồi P thuần vs PI rút sai số xác lập về 0."` — Không nêu mô hình `y += (0.8 * e + 0.5 * integ) * 0.1`, không nêu số bước `40`, bước `0.1`, không nêu định dạng `P_steady_err=... PI_final_err=...`. **Nghiêm trọng hơn**: bài giảng dạy đối tượng `x' = -x + u` (`sym` d. 95), còn `L10/loi_giai.py` dùng `y += (0.8 * e + 0.5 * integ) * 0.1` (thiếu `-y`) và chỉ chạy 40 bước nên `PI_final_err=0.2338 > P_steady_err=0.20`, trái với tuyên bố `"tích phân về 0"` ở tiêu đề `de.md`!
   - **`L11/de.md`** (d. 1–8): `"Chạy 10 bước x_{k+1} = (1 - 10*h)*x_k ở h=0.25 và h=0.05."` — Thiếu giá trị đầu `x_0 = 1.0` và định dạng in `g_025=... x10_div=... x10_conv=...` (làm tròn 2, 1, 5 chữ số).
   - **`L12/de.md`** (d. 1–8): Thiếu định dạng in `K=... x_est=... P_est=...` (1 chữ số thập phân).
   - **`L13/de.md`** (d. 1–8): Thiếu `P = I_2` ban đầu và định dạng in `pred_var_pos=... cross_cov_pos_vel=...`.
   - **`L14/de.md`** (d. 1–8): Thiếu định dạng in `need_fs_gt=...Hz observed_alias=...Hz`, dùng từ tiếng Anh `alias` chưa có ở đề.
   - **`L15/de.md`** (d. 1–8): Không ghi kích thước lưới trong thân đề, đổi tường từ `(1,1),(1,2)` (bài giảng) thành `(0,2),(1,2)` (lab) mà không giải thích, thiếu yêu cầu in `h_start=3` và định dạng `astar_steps=... h_start=...`.
   - **`L16/de.md`** (d. 1–8): Thiếu định dạng in `slope=... intercept=...` (làm tròn 2 chữ số).
   - **`L17/de.md`** (d. 1–8): Thiếu định dạng in `P_after_99_Q0=...` (làm tròn 2 chữ số).

3. **[MUST — 8/8 bài `L10–L17`] `covers:` trỏ sai cảnh dạy mục tiêu**
   - `L10` (d. 334–340): `obj 1` ("Giải thích vai trò của P, I, D") → `ponly` (chỉ có P; phải là `sym`/`addi`/`addd`); `obj 2` ("Tính sai số xác lập... 1/(1 + K)") → `check` (phải là `ponly`); `obj 3` ("Thấy hệ số P lớn có thể gây dao động và mất ổn định") → `practice` (không dạy dao động/mất ổn định; phải là `addd`).
   - `L11` (d. 394–400): `obj 2` ("Với hệ nhiều chiều...") → `check` (chỉ kiểm 1D; phải là `system`); `obj 3` ("tốc độ học của Gradient Descent") → `practice` (không có GD; phải là `gd`).
   - `L12` (d. 354–360): `obj 2` ("trọng số tối ưu") → `check` (suy ra K ở `formula`); `obj 3` ("Chạy vòng dự đoán – cập nhật") → `practice` (chỉ có bước đo; phải là `cycle`).
   - `L13` (d. 351–357): `obj 1` ("Viết mô hình... bằng ma trận F và H") → `example` (định nghĩa ở `sym`); `obj 3` ("hiệp phương sai làm phép đo vị trí sửa được cả vận tốc") → `practice` (chỉ tính `F P F^T`; phải là `intuition`/`example`).
   - `L14` (d. 437–443): `obj 1` ("định lý lấy mẫu") → `example` (định lý ở `nyquist`); `obj 3` ("Đọc biểu đồ |X_k| của biến đổi Fourier rời rạc") → `practice` (không có DFT; phải là `dft`).
   - `L15` (d. 364–370): `obj 2` ("ước lượng không vượt quá giá thật") → `check` (điều kiện ở `admissible`); `obj 3` ("A* mở ít ô hơn Dijkstra") → `practice` (không chạy Dijkstra; phải là `example`).
   - `L16` (d. 377–383): `obj 2` ("Dùng mô hình để sửa số đọc") → `check` (sửa số đọc ở `example` step 4); `obj 3` ("khoảng tin cậy... không nên dùng ngoài khoảng đã đo") → `practice` (chỉ khớp đường; phải là `confidence`/`extrapolate`).
   - `L17` (d. 572–578): `obj 2` (gồm 4 phép tính ở chặng 1, 2, 4) → chỉ trỏ `stage2`; `obj 3` ("Chọn công thức... cho robot của mình, kèm điều kiện đổi lựa chọn") → `practice` (chỉ chạy Q=0; bài toán chọn cho robot là `quiz`).

4. **[MUST — 8/8 bài `L10–L17`] Liệt kê từng mục P1 CHẶT chưa giảng (theo `BRIEF_R4.md`)**
   *Lưu ý: Cú pháp Python chưa từng được giảng ở `L00–L09` (chỉ có bảng đọc mã ở `practice` step 0).*
   | Bài | Cảnh/step | Mục chưa giảng (trích chữ) | Bảng cách đọc có phủ không? |
   |---|---|---|---|
   | `L10` | `practice` st1,3 & `de.md` | `k = 4.0`, `y, integ = 0.0, 0.0` (gán biến/tuple), `for _ in range(40):` (`_`, `range`), `+=`, `;`, `abs(...)`, `:.2f` / `:.4f`, `bash labs/cham.sh ...`, `PI` (`de.md`) | **Không** (bảng chỉ có `for x in ds:`, `f"{val:.3f}"`, `print(...)`) |
   | `L10` | `sym` st0 (d. 96) | `dt` trong `$\int e\,dt$` (giải thích ý nghĩa tích phân, không giảng riêng ký hiệu `dt`) | Không có bảng |
   | `L11` | `practice` st1,3 & `de.md` | `run = lambda h: ...` (gán hàm), `** 10` (luỹ thừa `**`), `:.2f` / `:.1f` / `:.5f`, `bash labs/cham.sh ...` | **Không** đối với `**`, `=`, `:.1f/.2f/.5f`, `bash` (bảng chỉ có `lambda x: ...`, `f"{val:.3f}"`, `print(...)`) |
   | `L12` | `practice` st1,3 & `de.md` | `x, P, z, R = 0.0, 1.0, 1.0, 1.0`, `/`, `*`, `:.1f`, `bash labs/cham.sh ...` | **Không** (bảng chỉ có `f"{val:.3f}"`, `print(...)`) |
   | `L13` | `practice` st1,3 & `de.md` | `P = [[1.0, 0.0], [0.0, 1.0]]`, `# P_new = ...`, `P[0][0]`, `:.1f`, `bash labs/cham.sh ...` | **Không** (bảng chỉ có `f"{val:.3f}"`, `print(...)`) |
   | `L14` | `practice` st1,3 & `de.md` | `f_sig, fs = 7.0, 10.0`, `abs(...)`, `:.0f`, `bash labs/cham.sh ...`, `alias` (`de.md` d. 3) | **Không** (bảng chỉ có `f"{val:.3f}"`, `print(...)`) |
   | `L15` | `practice` st1,3 & `de.md` | `import heapq`, `walls = {(0, 2), (1, 2)}` (`set`, `tuple`), `;`, `pq = [...]`, `dist = {start: 0}` (`dict`), `while pq:`, `_, g, u = heapq.heappop(pq)`, `==`, `print(...)`, `break`, `for dr, dc in ...`, `0 <= v[0] < 3`, `and`, `not in`, `dist.get(v, 99)`, `heapq.heappush(...)`, `bash` | **Không** (bảng chỉ có `import thu_vien`, `if dieu_kien:`, `lambda x: ...`, `f"{val:.3f}"`) |
   | `L16` | `practice` st1,3 & `de.md` | `pts = [(0, 1.0), ...]`, `x for x, _ in pts` (generator), `;`, `**2`, `:.2f`, `bash` | **Không** với tuple, generator, `**2`, `:.2f`, `bash` (bảng chỉ có `f"{val:.3f}"`, `sum/len/max/min`, `print(...)`) |
   | `L17` | `practice` st1,3 & `de.md` | `P, R = 1.0, 1.0`, `for _ in range(99):`, `:.2f`, `bash` | **Không** (bảng chỉ có `for x in ds:`, `f"{val:.3f}"`, `print(...)`) |
   | `L17` | `stage3` st3 (d. 367) | `32K` (`K` = nghìn đơn vị nhớ) | Không có bảng |

---

### B. Phát hiện SHOULD
1. **[SHOULD — 7/8 bài `L10–L16`] Thiếu P9 hai mức quy mô/thời gian trong `recap` (và thiếu số liệu 2 mức quy mô ở `L14`)**: `recap` của `L10–L16` chỉ tóm tắt chuỗi logic khái niệm mà không có số liệu/đánh đổi ở ≥ 2 mức quy mô hoặc mốc thời gian. Riêng `L14` trong cả thân bài cũng chưa so sánh 2 mức quy mô N hay tần số lấy mẫu kèm đánh đổi chi phí.
2. **[SHOULD — 4 bài] Dùng `"càng "` trong `say`** (kiểm theo yêu cầu AF4):
   - `L10` `ponly` st4 (d. 162): `"...đồng thời trị riêng, bằng âm của 1 cộng K, càng âm hơn, nên hệ về nhanh hơn."`
   - `L12` `sym` st0 (d. 115): `"...P càng lớn thì càng không chắc. ...càng xa đỉnh càng hiếm gặp..."`
   - `L12` `pitfalls` st1 (d. 264): `"...Bộ lọc ngày càng tin dự đoán và gần như bỏ qua phép đo mới..."`
   - `L16` `confidence` st1 (d. 247): `"...giống hình chuông nhưng đuôi dày hơn, càng ít dữ liệu càng dày."`
   - `L17` `stage1` st1 (d. 197): `"Khoảng chờ càng dài thì phép đo đến muộn càng được tin nhiều, tự động..."`
3. **[SHOULD — `L16`] Nhãn đồ thị đè nhẹ lên điểm dữ liệu** (`L16` `example` st4, `out/RBM/L16/frames/00041.png`): nhãn `y = 1,98x + 1,03` cắt ngang chấm cam tại `(3; 6,9)` (vẫn đọc được, nhưng cần dịch vị trí nhãn).

---

### C. Thông tin kiểm tra thêm (INFO)
- **Không ký hiệu toán thô trong `say`**: 8/8 bài sạch (0 ký hiệu `+`, `*`, `/`, `=`, `<`, `>`, `^`, `_`, `$`, `\`, chữ Hy Lạp thô trong `say`; chỉ có dấu gạch nối tiếng Việt hợp lệ như `ki-lô-gam`, `ra-đa`, `xăng-ti-mét`).
- **`audit/layout_RBM.tsv`**: Tệp rỗng (chỉ 1 dòng trống, chưa có bản ghi kiểm bố cục cho RBM).
- **`audit/review/screen_code/RBM.yaml`**: Có 3 khối/bài (`practice 1 0`, `practice 2 0`, `practice 4 0`) cho `L00–L17`; cấu trúc khớp tệp YAML nhưng phản ánh đúng lỗi lộ `practice 1 0` & `practice 2 0` trước `pause`.
- **`curriculum/rbm.yaml` & `audit/rbm/sources_L17.md`**: Bài hành trình `L17` tuân thủ chặt nguồn `[MS85]`: đúng 4 chặng (1960–1961, 1961–1964, 1966–1972, 1973–1985), không đọc tên cá nhân trong `say`, không dạy số liệu bị cấm (số bit phần định trị máy mô phỏng, chi tiết phần cứng tàu Apollo, số trạng thái C-5A/RAINPAL), mọi số minh hoạ đều ghi rõ `(số minh hoạ)` và quy tắc `2^24` ghi rõ là quy tắc thô tự suy ra.
- **`L15` `00037.png`**: Đường nét đứt cam hơi chạm mép trên chữ `S` và `Đ` nhưng vẫn rõ chữ.

---

## 5. Danh sách PNG đã xem (41 PNG)
- **L10** (`out/RBM/L10/frames/`): `00000.png` (hook), `00022.png` (SVG vòng phản hồi), `00045.png` (SVG P vs P+I), `00080.png` (practice code), `00087.png` (recap).
- **L11** (`out/RBM/L11/frames/`): `00020.png` (SVG trục số ổn định), `00033.png` (SVG phân kỳ vs hội tụ), `00075.png` (quiz), `00088.png` (practice code), `00095.png` (recap).
- **L12** (`out/RBM/L12/frames/`): `00037.png` (SVG thanh độ không chắc), `00042.png` (SVG phân phối chuẩn), `00077.png` (quiz), `00087.png` (practice code), `00094.png` (recap).
- **L13** (`out/RBM/L13/frames/`): `00028.png` (SVG elip hiệp phương sai), `00045.png` (check quy về 1D), `00069.png` (quiz), `00079.png` (practice code), `00086.png` (recap).
- **L14** (`out/RBM/L14/frames/`): `00001.png` (hook), `00025.png` (SVG bánh xe quay ngược), `00030.png` (SVG chồng phổ 7Hz/3Hz), `00063.png` (SVG phổ DFT), `00091.png` (practice code), `00098.png` (recap).
- **L15** (`out/RBM/L15/frames/`): `00001.png` (hook lưới SVG), `00025.png` (SVG cột chồng g+h), `00037.png` (SVG đường đi A*), `00082.png` (practice code), `00089.png` (recap).
- **L16** (`out/RBM/L16/frames/`): `00026.png` (SVG ô vuông bình phương phần dư), `00041.png` (SVG đường khớp 4 điểm — nhãn `y=1,98x+1,03` chạm chấm cam), `00093.png` (practice code), `00095.png` (practice bảng hướng dẫn), `00100.png` (recap).
- **L17** (`out/RBM/L17/frames/`): `00019.png` (SVG trục thời gian 4 chặng), `00024.png` (SVG cơ chế vòng 2 bước & 2 cách hỏng), `00125.png` (quiz robot 32 bit), `00139.png` (practice code), `00146.png` (recap).

---

## 6. Người học kẹt ở đâu
- **L10**: Kẹt ở `practice` st1–3 & `labs/RBM/L10/de.md` (`"So sánh đáp ứng phản hồi P thuần vs PI rút sai số xác lập về 0"` — thiếu mô hình/tham số/định dạng in, lại tự thấy `PI_final_err=0.2338 > 0.20` và cú pháp `for _ in range(40)`, `+=`, `:.4f` chưa giảng).
- **L11**: Kẹt ở `practice` st1–3 & `labs/RBM/L11/de.md` (`"run = lambda h: (1.0 - 10.0 * h) ** 10"` — không có trong `de.md` giá trị `x_0=1`, định dạng xuất, và toán tử `**` chưa giảng trong bảng step 0).
- **L12**: Kẹt ở `practice` st1–3 & `labs/RBM/L12/de.md` (`"x, P, z, R = 0.0, 1.0, 1.0, 1.0"` — bảng step 0 không giảng gán nhiều biến, toán tử `/`, `*`, `:.1f`; `de.md` không nêu định dạng chuỗi xuất).
- **L13**: Kẹt ở `practice` st1–3 & `labs/RBM/L13/de.md` (`"p00 = P[0][0] + 2*P[0][1] + P[1][1]"` — chưa giảng mảng 2 chiều, chỉ số `[][]`, `#`, `:.1f`; `de.md` không cho `P = I_2` và định dạng xuất).
- **L14**: Kẹt ở `practice` st1–3 & `labs/RBM/L14/de.md` (`"Tính tần số alias |f - k*fs|..."` — `de.md` dùng từ `alias` và thiếu định dạng xuất `need_fs_gt=...Hz`; `practice` st1 dùng gán nhiều biến, `abs`, `:.0f` chưa giảng).
- **L15**: Kẹt ở `practice` st1–3 & `labs/RBM/L15/de.md` (`"import heapq ... while pq: ... heappop ... dist.get(v, 99)"` — quá nhiều cú pháp Python trung cấp chưa giảng trong bảng step 0; tường trong `de.md` đổi vị trí so với bài giảng và thiếu định dạng xuất `h_start=3`).
- **L16**: Kẹt ở `practice` st1–3 & `labs/RBM/L16/de.md` (`"mx = sum(x for x, _ in pts)/4"` — generator expression, tuple unpacking, `**2`, `:.2f` chưa giảng; `de.md` thiếu định dạng xuất; ngoài ra `00041.png` nhãn chữ chạm nhẹ chấm dữ liệu `(3; 6,9)`).
- **L17**: Kẹt ở `stage3` st3 (`"bộ nhớ 32K"` — chưa giải thích `K`) và `practice` st1–3 & `labs/RBM/L17/de.md` (`"for _ in range(99): ... :.2f"` chưa giảng và `de.md` thiếu định dạng xuất `P_after_99_Q0=...`).
