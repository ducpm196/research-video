# Báo cáo đọc độc lập — Sample I-a (10 bài Lớp A ngẫu nhiên)

- Ngày kiểm tra: `2026-11-24`
- Phạm vi: kiểm tra độc lập 10 bài Lớp A (`BNX L23`, `BNX L04`, `CS112 L12`, `DMS L12`, `JVA L09`, `CS115 L46`, `BNX L24`, `CS112 L29`, `JV2 L02`, `BNX L08`) tập trung tiêu chí S1–4 (chuẩn xác kiến thức/phép tính/mã màn hình, giải thích thuật ngữ cho người mất gốc, `covers` khớp `objectives`, khung hình PNG, thời lượng không `pause`/tổng `pause`, ASR `chưa xem xét: 0`, `spec_sha256`/mtime).
- Giới hạn môi trường sandbox khi đọc:
  - **Java (`JVA L09`, `JV2 L02`)**: ĐÃ biên dịch và chạy thật (`javac`/`java` OpenJDK 22.0.2) cả `loi_giai.java` lẫn các đoạn mã Java trong bài — khớp 100%.
  - **Toán & mô phỏng thuật toán**: ĐÃ tính/mô phỏng độc lập lại toàn bộ bằng PowerShell / `.NET` / C# (`Add-Type`) trong `%TEMP%` (không chạm mã kho) — khớp 100%.
  - **Python (`python.exe`)**: `CHƯA KIỂM thực thi Python trực tiếp` (sandbox chặn quyền truy cập `C:\Python311` và `C:\Python313`), do đó mọi câu liên quan tới thực thi Python (`sklearn/onnx`, `sqlite3`, `tools/lv.py spec_digest`) được ghi rõ `CHƯA KIỂM` ở phần runtime Python, còn số liệu/logic đã đối chiếu độc lập bằng C#/.NET.
  - **Hibernate/H2 (`BNX L24`)**: `CHƯA KIỂM thực thi Hibernate/H2` (cần thư viện ngoài/Maven; chỉ kiểm độc lập logic và phép đếm SQL).

---

## Bảng tổng hợp 10 bài

| Bài | `sha16` YAML | Từ / Không pause / Tổng `pause` | ASR chưa xem xét | `out` mới hơn YAML (`spec_sha256`) | MUST | SHOULD | P1–P7 (Tổng) | P8 / P9 | Mất gốc | L1–L5 | `covers` | Kết luận |
|---|---|---:|---:|---|---:|---:|---|---|---|---|---|---|
| `BNX L23` | `2bd25e5c6f589c98` | 2 296 từ / 12,08 phút / 145 s | 0 | `out` mới hơn (`7d6dc2a521f02226`*)| 0 | 2 | 2,2,2,2,2,2,2 (14) | 2 / 2 | ĐỦ | 2,2,2,2,1† | 5/6 (mục 1 lệch cảnh) | ĐẠT (sửa SHOULD) |
| `BNX L04` | `8b520ac0c685cfbe` | 2 293 từ / 12,03 phút / 145 s | 0 | `out` mới hơn (`571f60a4528ccd52`*) | 0 | 0 | 2,2,2,2,2,2,2 (14) | 2 / 2 | ĐỦ | 2,2,2,2,1† | 6/6 | ĐẠT |
| `CS112 L12` | `aba0c6976b8228d9` | 2 287 từ / 13,53 phút / **608 s** | 0 | **YAML mới hơn** (`e2616fc85c929ed9`*, khớp lúc ghi `asr_reviewed`) | 0 | 3 | 2,2,2,2,2,2,2 (14) | 2 / 2 | ĐỦ | 2,2,2,2,1† | 4/5 (mục 3 thiếu `pitfalls`) | ĐẠT (sửa SHOULD) |
| `DMS L12` | `5b60566eac4dd858` | 2 297 từ / 13,00 phút / **450 s** | 0 | `out` mới hơn (`95a106c8cbde2147`*) | 0 | 2 | 2,2,2,2,2,2,2 (14) | 2 / 2 | ĐỦ | 2,2,2,2,1† | 4/5 (mục 1 thiếu `three`) | ĐẠT (sửa SHOULD) |
| `JVA L09` | `718c6a9a2eb706e4` | 2 201 từ / 12,26 phút / 80 s | 0 | `out` mới hơn (`7da674a984a5b124`*) | 0 | 1 | 2,2,2,2,2,2,2 (14) | 2 / 2 | ĐỦ | 2,2,2,2,1† | 7/8 (mục 1 nên thêm `sym`) | ĐẠT (sửa SHOULD) |
| `CS115 L46` | `e76ce54e6a2367ea` | 1 769 từ / 10,30 phút / 300 s | 0 | `out` mới hơn (`ccf212a7d0610914`*) | 0 | 0 | 2,2,2,2,2,2,2 (14) | 1 / 2 | GẦN | 2,2,2,2,1† | 4/4 | ĐẠT (`P8=1`) |
| `BNX L24` | `0d9b26f0277cc074` | 2 260 từ / 12,18 phút / 150 s | 0 | **YAML mới hơn** (`a33e2aee8ad37a5e`*, khớp lúc ghi `asr_reviewed`) | 0 | 2 | 2,2,2,2,2,2,2 (14) | 2 / 2 | ĐỦ | 2,2,2,2,1† | 6/7 (mục 1 thiếu `formula`) | ĐẠT (sửa SHOULD) |
| `CS112 L29` | `bbb82be4c2f57a47` | 2 303 từ (`journey`) / 13,35 phút / 300 s | 0 | `out` mới hơn (`3c025cf1c765b490`*) | 0 | 0 | 2,2,2,2,2,2,2 (14) | 1 / 2 | GẦN | 2,2,2,2,1† | 4/4 | ĐẠT (`P8=1`) |
| `JV2 L02` | `6fa1cb92d67a525e` | 2 253 từ / 13,00 phút / 175 s | 0 | **YAML mới hơn** (`45be8ca8dce495b0`*, khớp lúc ghi `asr_reviewed`) | 0 | 3 | 2,2,2,2,2,2,2 (14) | 2 / 2 | ĐỦ | 2,2,2,2,1† | 4/6 (mục 2 thiếu `formula`, mục 5 thiếu `pitfalls`) | ĐẠT (sửa SHOULD) |
| `BNX L08` | `530cceca67ee4020` | **2 304 từ** / 12,80 phút / 145 s | 0 | **YAML mới hơn** (`cf70eb03ff4736ce`*, khớp lúc ghi `asr_reviewed`) | 0 | 3 | 2,2,2,2,2,2,2 (14) | 2 / 2 | ĐỦ | 2,2,2,2,1† | 4/5 (mục 1 nên thêm `intuition`) | ĐẠT (sửa SHOULD) |

- **Ghi chú (\*) về `spec_sha256`**: `tools/lv.py` (`spec_digest`) băm JSON chuẩn hoá của YAML **đã bỏ trường `asr_reviewed`**, nên khác SHA-256 thô của tệp. Trong sandbox không chạy được `python.exe` nên chưa tái tính `spec_digest` trực tiếp; ở cả 4 bài có `mtime YAML > mtime build_report.json` (`CS112 L12`, `BNX L24`, `JV2 L02`, `BNX L08`), dấu thời gian sửa YAML trùng sát giờ `checked_at` trong `asr_report.md` (ghi chú `asr_reviewed` sau khi dựng video). Cần chạy xác nhận `lv.py verify` ngoài sandbox cho 4 bài này.
- **Ghi chú (†) về `L5`**: Cả 10 bài đều ghi `ca_them: 'mien: lop_A_da_dat', ca_an: false` trong `labs/CONTRACT.yaml`, nên không có `ca_an/` là hợp lệ theo hợp đồng Lớp A.
- **Boilerplate & `checks` & Khung hình PNG**: 0/10 bài dính chuỗi trong `boiler_deny.txt`; 0/10 bài có `checks` hằng đẳng thức rỗng; 40/40 khung hình PNG đã mở sạch, không chồng chữ, không cắt cụt.

**Kết luận chung Sample I-a:** **MUST = 0** trên cả 10 bài (không có lỗi chặn kiến thức, công thức, lab hay thời lượng tối thiểu); có **16 mục SHOULD** rải ở 7/10 bài (chủ yếu là thiếu cảnh phụ trong `covers`, 2 bài có tổng `pause > 300 s`, 1 bài vượt trần 2 300 từ đúng 4 từ, 4 bài có `mtime YAML > mtime build_report.json` do cập nhật `asr_reviewed`).

---

## Chi tiết từng bài

### 1. `BNX L23` — sha16: `2bd25e5c6f589c98`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (`lessons/bnx/L23_scikit_learn_onnx_rung_co_lap.yaml` + `labs/BNX/L23/` + 4 frames `00016, 00033, 00068, 00097`)
- Thời lượng / từ lời đọc: `14:30` (`12,08` phút không `pause`, `pause = 145 s`) / `2 296` từ. ASR: `109` câu, `0` chưa xem xét. `out_newer: True`.

#### A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | `covers` (mục tiêu 1) | `- objective: 1` -> `scene: example` | Mục tiêu 1 yêu cầu "Giải thích vì sao điểm lạ bị cô lập sau ít lần cắt hơn điểm thường"; cảnh `example` chỉ quy đổi điểm ra độ sâu (`2,49` và `11,88`), còn phần giải thích cơ chế nằm ở `intuition` (xác suất cắt vào khoảng trống `~94%`) và `formula` bước 2. | Thêm `intuition` (và/hoặc `formula`) vào `covers` cho `objective: 1`. | ĐÃ ĐỌC ĐỦ |
| SHOULD | `formula` step 6 | `say`: "...điểm lạ chỉ năm phẩy không bảy lần." (`show`: `49881 5.075`) | `5.075` nếu làm tròn 2 chữ số là `5,08` (hoặc 1 chữ số như `intuition` là `5,1`), đọc `năm phẩy không bảy` là cắt cụt chữ số cuối. | Đọc `năm phẩy không tám` hoặc `năm phẩy một`. | ĐÃ KIỂM (.NET Math) |

#### B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 (Tổng=14) | P8=2 P9=2` -> Mất gốc: `ĐỦ`
- Lab: `L1=2 L2=2 L3=2 L4=2 L5=1 (miễn Lớp A)`
- `covers` đúng: `5/6`
- Số đã tính lại / mã đã chạy: `c(256)=10.2448`, `s(c/2,256)=-0.7071`, `s(1,256)=-0.9346`, `depth(-0.8448)=2.4927`, `depth(-0.4475)=11.8843`, `gap prob=0.9353`; lab `c(128)=8.8584`, `A: -0.8551 / -0.2551 / -1`, `B: -0.4945 / 0.1055 / 1`, `ceil(0.03*2999)=90`, `oan=65` (khớp 100% `mong_doi.txt`). Thực thi Python/`sklearn`/`onnxruntime`: `CHƯA KIỂM (sandbox chặn python.exe)`.
- Khung hình đã xem: `00016.png`, `00033.png`, `00068.png`, `00097.png` — bố cục sạch, SVG và công thức rõ.

---

### 2. `BNX L04` — sha16: `8b520ac0c685cfbe`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (`lessons/bnx/L04_oauth2_openid_connect.yaml` + `labs/BNX/L04/` + 4 frames `00018, 00032, 00056, 00075`)
- Thời lượng / từ lời đọc: `14:27` (`12,03` phút không `pause`, `pause = 145 s`) / `2 293` từ. ASR: `108` câu, `0` chưa xem xét. `out_newer: True`.

#### A. Chuẩn xác
Không phát hiện lỗi MUST/SHOULD.

#### B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 (Tổng=14) | P8=2 P9=2` -> Mất gốc: `ĐỦ`
- Lab: `L1=2 L2=2 L3=2 L4=2 L5=1 (miễn Lớp A)`
- `covers` đúng: `6/6`
- Số đã tính lại / mã đã chạy: PKCE SHA-256 `E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM`, Base64 Basic `s6BhdRkqt3:gX1fBat3bV`, mô phỏng `xin_ma(10, 1000, 100000) = 140, 13360, 1333390`; lab `1 API=36`, `4 API=144`, `giây cuối=149` (khớp 100% `mong_doi.txt`). Thực thi Python: `CHƯA KIỂM (sandbox chặn python.exe)`.
- Khung hình đã xem: `00018.png`, `00032.png`, `00056.png`, `00075.png` — sạch, rõ.

---

### 3. `CS112 L12` — sha16: `aba0c6976b8228d9`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (`lessons/cs112/L12_chia_de_tri_dinh_ly_tho.yaml` + `labs/CS112/L12/` + 4 frames `00033, 00059, 00079, 00111`)
- Thời lượng / từ lời đọc: `23:40` (`13,53` phút không `pause`, `pause = 608 s`) / `2 287` từ. ASR: `119` câu, `0` chưa xem xét. `out_newer: False`.

#### A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | `practice` step 1 | `pause: 600` (cộng `quiz` `pause: 8` = **608 s**) | Vi phạm quy ước `BRIEF_AF5.md` §2.D: "Tổng `pause` hợp lý (≤ 300 s)". | Hạ `practice` `pause` xuống ≤ `290 s`. | ĐÃ ĐỌC ĐỦ |
| SHOULD | `covers` (mục tiêu 3) | `- {objective: 3, scene: examples}` | Mục tiêu 3 có hai vế: "Kiểm điều kiện đều đặn ở trường hợp 3 và nhận ra hệ thức rơi vào khe hở"; `examples` chỉ kiểm đều đặn TH3, còn khe hở `2T(n/2) + n log n` được dạy ở `pitfalls` (Lỗi 1). | Thêm `{objective: 3, scene: pitfalls}` vào `covers`. | ĐÃ ĐỌC ĐỦ |
| SHOULD | tệp YAML vs `build_report.json` | `ym=2026-11-24T09:46:02 > bm=2026-11-24T04:57:09` | Mtime YAML mới hơn `build_report.json` (trùng sát giờ `asr checked_at=03:00:17Z`, khả năng chỉ thêm `asr_reviewed`). | Chạy `lv.py verify CS112 L12` ngoài sandbox để xác nhận `spec_sha256` khớp. | CHƯA KIỂM (`lv.py` cần `python.exe`) |

#### B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 (Tổng=14) | P8=2 P9=2` -> Mất gốc: `ĐỦ`
- Lab: `L1=2 L2=2 L3=2 L4=2 L5=1 (miễn Lớp A)`
- `covers` đúng: `4/5`
- Số đã tính lại / mã đã chạy: chạy C# `MergeSort` thật cho `n=1000 -> 8415` và `n=100000 -> 1493143` phép so sánh; tỉ số `8T(n/2)+n^2` cho `1.5, 1.75, 1.875, 1.999`; lab `4T(n/2)+n^2 -> 1.100`, `9T(n/3)+n -> 1.500`, `T(n/2)+n -> 1.999` (khớp 100% `mong_doi.txt`). Python: `CHƯA KIỂM (sandbox)`.
- Khung hình đã xem: `00033.png`, `00059.png`, `00079.png`, `00111.png` — đồ thị SVG, công thức và mã rõ nét.

---

### 4. `DMS L12` — sha16: `5b60566eac4dd858`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (`lessons/dms/L12_bao_ham_loai_tru.yaml` + `labs/DMS/L12/` + 4 frames `00030, 00046, 00075, 00110`)
- Thời lượng / từ lời đọc: `20:30` (`13,00` phút không `pause`, `pause = 450 s`) / `2 297` từ. ASR: `124` câu, `0` chưa xem xét. `out_newer: True`.

#### A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | `practice` step 1 | `pause: 420` (cộng `quiz` `pause: 30` = **450 s**) | Vượt ngưỡng `BRIEF_AF5.md` §2.D: "Tổng `pause` hợp lý (≤ 300 s)". | Hạ `practice` `pause` xuống ≤ `270 s`. | ĐÃ ĐỌC ĐỦ |
| SHOULD | `covers` (mục tiêu 1) | `- {objective: 1, scene: example}` | Mục tiêu 1 là "Áp dụng bao hàm–loại trừ cho ba tập và nhiều tập"; phần 3 tập nằm ở `three` (và `intuition`), còn `example` áp dụng cho 4 tập ($D_4$). | Thêm `{objective: 1, scene: three}` vào `covers`. | ĐÃ ĐỌC ĐỦ |

#### B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 (Tổng=14) | P8=2 P9=2` -> Mất gốc: `ĐỦ`
- Lab: `L1=2 L2=2 L3=2 L4=2 L5=1 (miễn Lớp A)`
- `covers` đúng: `4/5`
- Số đã tính lại / mã đã chạy: tính độc lập bằng PowerShell `D3=2, D4=9, D5=44, D6=265, D7=1854, D8=14833, D9=133496, D20=895014631192902121`; lab `1..1000` không chia hết 3,5,7 = `457`, toàn ánh `5->3` = `150`, nguyên tố cùng nhau `360` = `96` (khớp 100% `mong_doi.txt`). Python: `CHƯA KIỂM (sandbox)`.
- Khung hình đã xem: `00030.png`, `00046.png`, `00075.png`, `00110.png` — biểu đồ Venn và bảng rõ.

---

### 5. `JVA L09` — sha16: `718c6a9a2eb706e4`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (`lessons/jva/L09_danh_sach_va_ban_do.yaml` + `labs/JVA/L09/` + 4 frames `00031, 00067, 00090, 00117`)
- Thời lượng / từ lời đọc: `13:35` (`12,26` phút không `pause`, `pause = 80 s`) / `2 201` từ. ASR: `129` câu, `0` chưa xem xét. `out_newer: True`.

#### A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | `covers` (mục tiêu 1) | `- objective: 1` -> `scene: check` | `sym` dạy `ArrayList<Long>`, `add`, `get(0)`, `size()`, `for (long x : gd)` trước, còn `check` cộng theo chỉ số `i`. | Thêm `sym` vào `covers` cho `objective: 1`. | ĐÃ ĐỌC ĐỦ |

#### B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 (Tổng=14) | P8=2 P9=2` -> Mất gốc: `ĐỦ`
- Lab: `L1=2 L2=2 L3=2 L4=2 L5=1 (miễn Lớp A)`
- `covers` đúng: `7/8`
- Số đã tính lại / mã đã chạy: ĐÃ biên dịch & chạy thật bằng OpenJDK 22 (`javac`/`java`): `ThongKe.java` (`labs/JVA/L09/loi_giai.java`) ra đúng 5 dòng khớp `mong_doi.txt`; các đoạn mã trong bài (`lambda`, `sort`, `127/128 == vs equals`, `ConcurrentModificationException`) đều chạy thật khớp 100%.
- Khung hình đã xem: `00031.png`, `00067.png`, `00090.png`, `00117.png` — sạch, rõ.

---

### 6. `CS115 L46` — sha16: `e76ce54e6a2367ea`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (`lessons/cs115/L46_nghich_dao_ma_tran.yaml` + `labs/CS115/L46/` + 4 frames `00020, 00043, 00072, 00083`)
- Thời lượng / từ lời đọc: `15:18` (`10,30` phút không `pause`, `pause = 300 s`) / `1 769` từ. ASR: `103` câu, `0` chưa xem xét. `out_newer: True`.

#### A. Chuẩn xác
Không phát hiện lỗi MUST/SHOULD.

#### B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 (Tổng=14) | P8=1 P9=2` -> Mất gốc: `GẦN` (chỉ vì các cảnh giảng minh hoạ bằng bảng số và công thức toán, không kèm khối mã chạy thật trên màn hình; lab Python có đầy đủ).
- Lab: `L1=2 L2=2 L3=2 L4=2 L5=1 (miễn Lớp A)`
- `covers` đúng: `4/4`
- Số đã tính lại / mã đã chạy: tính lại toàn bộ ví dụ nhà (`M=[[2,1],[1,1]]`, `w=(2,1)`), `quymo` (`t=0.1, 0.01, 0.0001 -> max=11, 101, 10001`), quiz (`det=2, w=(1,1)`), và 8 dòng lab (`det=1`, `M^-1=[[3,-2],[-7,5]]`, `w=[1,2]`, `t=1/100 -> [-1/10, 1/10]`, `t=1/10000 -> [-10, 10]`, hồi quy `[2/3, 1]`, `det(X2^T X2)=0`) — khớp 100% `mong_doi.txt`. Python: `CHƯA KIỂM (sandbox)`.
- Khung hình đã xem: `00020.png`, `00043.png`, `00072.png`, `00083.png` — SVG hình bình hành và công thức ma trận sắc nét.

---

### 7. `BNX L24` — sha16: `0d9b26f0277cc074`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (`lessons/bnx/L24_jpa_hibernate_spring_data.yaml` + `labs/BNX/L24/` + 4 frames `00015, 00049, 00071, 00101`)
- Thời lượng / từ lời đọc: `14:41` (`12,18` phút không `pause`, `pause = 150 s`) / `2 260` từ. ASR: `115` câu, `0` chưa xem xét. `out_newer: False`.

#### A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | `covers` (mục tiêu 1) | `- objective: 1` -> `scene: intuition` | Mục tiêu 1 gồm "Khai báo một thực thể và kể bốn trạng thái..."; `intuition` chỉ giảng 4 trạng thái, còn khai báo `@Entity`, `@Id`, `@OneToMany`, `@ManyToOne` nằm ở `formula` bước 1. | Thêm `formula` vào `covers` cho `objective: 1`. | ĐÃ ĐỌC ĐỦ |
| SHOULD | tệp YAML vs `build_report.json` | `ym=2026-11-22T14:53:50 > bm=2026-11-22T13:23:04` | Mtime YAML mới hơn `build_report.json` (trùng sát giờ `asr checked_at=07:53:59Z`). | Chạy `lv.py verify BNX L24` ngoài sandbox để xác nhận `spec_sha256` khớp. | CHƯA KIỂM (`lv.py` cần `python.exe`) |

#### B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 (Tổng=14) | P8=2 P9=2` -> Mất gốc: `ĐỦ`
- Lab: `L1=2 L2=2 L3=2 L4=2 L5=1 (miễn Lớp A)`
- `covers` đúng: `6/7`
- Số đã tính lại / mã đã chạy: phép đếm `1+N` (`5, 50, 500, 50000 -> 6, 51, 501, 50001`), dòng trả về (`10, 1000, 100000`), thực thể giữ trong ngữ cảnh (`500 + 500*2 = 1500`, `20 + 20*2 = 60`), lab (`1 + 12 = 13 cau`, `36 the`). Thực thi Hibernate/H2 và Python `sqlite3`: `CHƯA KIỂM (cần Maven/Hibernate JAR ngoài và Python bị chặn trong sandbox)`.
- Khung hình đã xem: `00015.png`, `00049.png`, `00071.png`, `00101.png` — sạch, rõ.

---

### 8. `CS112 L29` — sha16: `bbb82be4c2f57a47`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (`lessons/cs112/L29_hanh_trinh_timsort.yaml` + `labs/CS112/L29/` + 4 frames `00018, 00043, 00057, 00090`)
- Thời lượng / từ lời đọc: `18:21` (`13,35` phút không `pause`, `pause = 300 s`) / `2 303` từ (`case: journey`, được phép vượt 2 300 từ). ASR: `106` câu, `0` chưa xem xét. `out_newer: True`.

#### A. Chuẩn xác
Không phát hiện lỗi MUST/SHOULD.

#### B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 (Tổng=14) | P8=1 P9=2` -> Mất gốc: `GẦN` (trong các cảnh giảng chỉ dùng bảng số liệu lịch sử từ `[LS02]`, `[CAV15]` và phép tính tay, không chạy đoạn mã trên màn hình; lab Python đầy đủ).
- Lab: `L1=2 L2=2 L3=2 L4=2 L5=1 (miễn Lớp A)`
- `covers` đúng: `4/4`
- Số đã tính lại / mã đã chạy: chạy C# kiểm toàn bộ `minrun(2112)=33 (64 đoạn)`, `minrun(315)=40`, chuỗi `b[0..5] = 0,16,17,34,52,87`, ngưỡng ngăn xếp `4,9,18,39`, phân bố `315 -> [39,39,40,39,39,40,39,40]`, `log2(2^20!) = 19458756` (`+0.76%`); lab `minrun(1000)=63 (16 đoạn, CO)`, `4097->33 (125, KHONG)`, `5000->40 (125, KHONG)`, `Ban cu: [171, 119, 59, 55] HONG`, `Ban sua: [404] DUNG` (khớp 100% `mong_doi.txt`). Python: `CHƯA KIỂM (sandbox)`.
- Khung hình đã xem: `00018.png`, `00043.png`, `00057.png`, `00090.png` — trục thời gian SVG và bảng sắc nét.

---

### 9. `JV2 L02` — sha16: `6fa1cb92d67a525e`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (`lessons/jv2/L02_kieu_tong_quat_so_sanh.yaml` + `labs/JV2/L02/` + 4 frames `00017, 00061, 00087, 00134`)
- Thời lượng / từ lời đọc: `15:55` (`13,00` phút không `pause`, `pause = 175 s`) / `2 253` từ. ASR: `152` câu, `0` chưa xem xét. `out_newer: False`.

#### A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | `covers` (mục tiêu 2) | `- objective: 2` -> `scene: intuition` | Mục tiêu 2 gồm "khai báo hộp tổng quát... và hàm có ràng buộc so sánh được"; hộp `Hop<T>` ở `intuition`, còn `<T extends Comparable<T>> T lon(T a, T b)` ở `formula` bước 1. | Thêm `formula` vào `covers` cho `objective: 2`. | ĐÃ ĐỌC ĐỦ |
| SHOULD | `covers` (mục tiêu 5) | `- objective: 5` -> `scene: scale` | Mục tiêu 5 gồm `n log n` (`scale`) và "bẫy phép trừ làm tràn" (`formula` bước 4 và `pitfalls` Lỗi 3). | Thêm `pitfalls` vào `covers` cho `objective: 5`. | ĐÃ ĐỌC ĐỦ |
| SHOULD | tệp YAML vs `build_report.json` | `ym=2026-11-14T12:36:55 > bm=2026-11-14T05:15:39` | Mtime YAML mới hơn `build_report.json` (trùng sát giờ `asr checked_at=05:36:59Z`). | Chạy `lv.py verify JV2 L02` ngoài sandbox để xác nhận `spec_sha256` khớp. | CHƯA KIỂM (`lv.py` cần `python.exe`) |

#### B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 (Tổng=14) | P8=2 P9=2` -> Mất gốc: `ĐỦ`
- Lab: `L1=2 L2=2 L3=2 L4=2 L5=1 (miễn Lớp A)`
- `covers` đúng: `4/6`
- Số đã tính lại / mã đã chạy: ĐÃ biên dịch & chạy thật bằng OpenJDK 22 (`javac`/`java`): `SapXepGiaoDich.java` (`labs/JV2/L02/loi_giai.java`) khớp 100% `mong_doi.txt`; `LonNhat` (`7`, `abd`, `-11 0 4`), `SapXep` (`4,2,5,6,1,3`), `DemSoSanh` với `Random(42)` (`1000->8683`, `100000->1534624`, `1000000->18640873`, đã xếp `999, 99999, 999999`), và `(int)(3000000000L - 1L) = -1294967297` đều khớp 100%.
- Khung hình đã xem: `00017.png`, `00061.png`, `00087.png`, `00134.png` — sạch, rõ.

---

### 10. `BNX L08` — sha16: `530cceca67ee4020`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (`lessons/bnx/L08_elasticsearch_manh_ban_sao.yaml` + `labs/BNX/L08/` + 4 frames `00024, 00043, 00097, 00130`)
- Thời lượng / từ lời đọc: `15:13` (`12,80` phút không `pause`, `pause = 145 s`) / `2 304` từ. ASR: `142` câu, `0` chưa xem xét. `out_newer: False`.

#### A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| SHOULD | toàn bài (`say`) | tổng `2 304` từ | Vượt trần hợp đồng `1 300 – 2 300` từ của `BRIEF_AF5.md` §2.D đúng 4 từ (không vi phạm ngưỡng MUST `< 1 300`). | Rút gọn 5–10 từ ở câu nối dài. | ĐÃ ĐỌC ĐỦ |
| SHOULD | `covers` (mục tiêu 1) | `- objective: 1` -> `scene: practice` | `intuition` bước 1–4 cũng dựng chỉ mục ngược mẫu kèm mã Python chạy thật cho 4 giao dịch. | Thêm `intuition` vào `covers` cho `objective: 1`. | ĐÃ ĐỌC ĐỦ |
| SHOULD | tệp YAML vs `build_report.json` | `ym=2026-11-24T12:06:55 > bm=2026-11-24T11:31:49` | Mtime YAML mới hơn `build_report.json` (trùng sát giờ `asr checked_at=05:07:31Z`). | Chạy `lv.py verify BNX L08` ngoài sandbox để xác nhận `spec_sha256` khớp. | CHƯA KIỂM (`lv.py` cần `python.exe`) |

#### B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 (Tổng=14) | P8=2 P9=2` -> Mất gốc: `ĐỦ`
- Lab: `L1=2 L2=2 L3=2 L4=2 L5=1 (miễn Lớp A)`
- `covers` đúng: `4/5`
- Số đã tính lại / mã đã chạy: chạy C# tính `zlib.crc32` thật trên `tx1..tx1200` (`315/1200 = 0.263`, `split 3->6 True`), và trên `1200, 120000, 1200000` (`doi=885, 89991, 899480`, `postings=2, 120, 1200`); lab `29,41,50 mod 5 = 4 1 0`, `doi 4->6: giu manh 4 / 12` (khớp 100% `mong_doi.txt`). Python: `CHƯA KIỂM (sandbox)`.
- Khung hình đã xem: `00024.png`, `00043.png`, `00097.png`, `00130.png` — sạch, rõ.
