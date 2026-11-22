# Báo cáo kiểm định độc lập Stage 9 — Khóa `IRS` (`L00–L13`, 14 bài)

**Vai trò:** WP-AF4-5 Stage 9 IRS Verifier độc lập (read-only).  
**Kết luận tổng thể:** **`NO-GO`** (phát hiện **2 lỗi `MUST`** làm sai công thức/lệch đề thực hành giữa thân bài, `de.md`, `loi_giai.py` và `mong_doi.txt` tại `L02` và `L12`; kèm các lỗi `SHOULD` về gán cứng ở `L00, L06`, thiếu đơn vị `MiB` ở `L13`, lỗ hổng P1 do phần AF2 `practice#0/#3` + `de.md` dùng thuật ngữ/viết tắt tiếng Anh chưa giảng trong thân bài, và `L01, L04` thiếu 2 mức quy mô).

---

## 1. Tổng hợp số liệu & tỷ lệ đạt chuẩn (`OBSERVED`)

| Hạng mục kiểm tra | Kết quả | Ghi chú |
|---|---|---|
| `curriculum/irs.yaml` ↔ `lessons/irs/L*.yaml` (`L00..L13`) | **14/14 khớp** | Đủ 14 bài; `covers:` ánh xạ đủ `objectives` sang `scene` hợp lệ (`14/14`) |
| `audit/irs/verify_irs.py` | **150/150 PASS** | Chỉ kiểm thân bài `hook..quiz`; chưa kiểm `practice` & `labs/IRS/` |
| `lv.lint` (`L00..L13`) | **0 FAIL / 0 WARN** | 14/14 sạch |
| `build_report.json` (`spec_sha256`, `tts_sha256`, `voices`) | **14/14 PASS** | `STALE = 0` cả spec và TTS; 100% 1 giọng `vi-VN-NamMinhNeural` |
| `out/IRS/L*/L*.srt == say` | **14/14 khớp 100%** | Không thiếu câu, không sai chữ |
| `out/IRS/L*/asr_report.md` | **14/14 `chưa xem xét: 0`** | `thiếu audio: 0` ở cả 14 bài |
| `audit/layout_IRS.tsv` | **0 lỗi bố cục** | Tệp 2 byte trống |
| Khung hình PNG đã xem (`out/IRS/L*/frames/*.png`) | **28/28 PNG sạch** | 1 SVG/biểu đồ + 1 `practice#0` mỗi bài; không đè chữ, không tràn khung |
| Các câu chứa `"càng "` trong `say` | **26 step / 28 câu sạch (28/28)** | Không có câu tối nghĩa hay ngược chiều kiểu `FND L00` |
| Chạy thực tế `labs/IRS/L*/loi_giai.py == mong_doi.txt` | **14/14 exit 0** | **Cảnh báo:** `L02` tính sai công thức so với lý thuyết; `L12` dùng `0.07` khác `de.md` (`0.05ms`); `L00, L06` gán cứng |
| **Tỷ lệ `P1` (thuật ngữ tại chỗ — tính cả `say`, `practice#0/#3`, `de.md`)** | **`2`: 0/14 (0%) · `1`: 14/14 (100%) · `0`: 0/14** | Thân bài (`hook..quiz`) sạch ~100%; toàn bộ điểm `1` đến từ AF2 `practice#0/#3` và `de.md` |
| **Tỷ lệ `P8` (thực nghiệm tự đối chiếu được)** | **`2`: 12/14 (85,7%) · `0`: 2/14 (`L02, L12`)** | `L02` và `L12` học viên làm đúng đề/lý thuyết sẽ FAIL `cham.sh` |
| **Tỷ lệ `P9` (hai mức quy mô + đánh đổi)** | **`2`: 12/14 (85,7%) · `1`: 1/14 (`L04`) · `0`: 1/14 (`L01`)** | `L00..L12` không có mục `Hai mức quy mô` riêng trong `recap` (chỉ có trong thân bài) |

---

## 2. Chi tiết kiểm định từng bài (`L00..L13`)

### `L00` — Đo chất lượng truy hồi: độ chuẩn xác, độ phủ và hạng nghịch đảo trung bình
- **Kỹ thuật:** `116` frames (`841.633s`), `asr_report`: `gắn cờ 3, chưa xem xét 0`, `SRT == say`, `spec_ok=True, tts_ok=True`, `covers: [1->example, 2->check, 3->practice]`.
- **PNG đã xem:** `out/IRS/L00/frames/00024.png` (SVG cửa sổ `k=5`), `out/IRS/L00/frames/00094.png` (`practice#0`). Không đè chữ/tràn khung.
- **Điểm `P1 = 1` · `P8 = 2` (vận hành) · `P9 = 2`** (`recall_base` so kho `T=5` với `TREC-7` `528 000` văn bản / `26,4 triệu` cặp vs `50 000` cặp; `recap` nhắc hỏi nguồn gốc `T`, chưa có mục `Hai mức quy mô` riêng).
- **Phát hiện:**
  - **`SHOULD` (gán cứng / đi đường tắt):** `labs/IRS/L00/loi_giai.py` và `L00` `practice#1` gán cứng đáp số `p5 = 2 / 5; r5 = 2 / 5; r10 = 3 / 5; p3_B = 0 / 3; mrr = (1.0 + 1.0/3.0 + 0.0) / 3.0`, không cài đặt hàm tính `P@k, R@k, MRR` từ danh sách hạng `[1, 3, 6]`, `[4, 5, 6]` như `de.md` nêu.
  - **`SHOULD` (`P1`):** `de.md` và `practice#3` dùng cụm tiếng Anh `Mean Reciprocal Rank` (thân bài chỉ nói `hạng nghịch đảo trung bình` và `M R R`); `practice#0` chỉ giải thích `:.3f`, không giải cú pháp `f"..."` và `:.1f`, `:.4f` dùng trong `practice#1`.
  - **`INFO` (`"càng "`):** 1 câu (`formula#3`: "Vị trí càng xa thì người dùng càng phải đọc qua nhiều dòng sai...") — chính xác.

### `L01` — Độ lợi tích lũy có chiết khấu và chuẩn hoá (nDCG)
- **Kỹ thuật:** `104` frames (`878.267s`), `asr_report`: `gắn cờ 8, chưa xem xét 0`, `SRT == say`, `spec_ok=True, tts_ok=True`, `covers: [1->example, 2->check, 3->practice]`.
- **PNG đã xem:** `out/IRS/L01/frames/00022.png` (SVG cột mức liên quan vs sau chiết khấu), `out/IRS/L01/frames/00090.png` (`practice#0`). Sạch.
- **Điểm `P1 = 1` · `P8 = 2` · `P9 = 0`** (bài chỉ so vị trí `1..1024`, 4 vs 5 văn bản chấm và công thức 2002 vs 2005; thiếu so sánh ≥ 2 mức quy mô hệ thống; `recap` không có `Hai mức quy mô`).
- **Phát hiện:**
  - **`SHOULD` (`P1` / chỉ số `i`):** `labs/IRS/L01/de.md` ghi chiết khấu `1/log2(i+1)` (quy ước `i` đếm từ `1` như thân bài), nhưng `loi_giai.py` dùng `enumerate(rels)` (`i` đếm từ `0`) nên viết `math.log2(i + 2)` mà không giải thích sự lệch chỉ số này; `practice#0` dùng từ `"mô-đun"` chưa giải nghĩa và thiếu `enumerate`, `sum`.
  - **`SHOULD` (`P9`):** Thiếu so sánh ở hai mức quy mô (ví dụ chấm trên câu hỏi nhỏ vs kho triệu văn bản / chỉ mục tìm kiếm thực tế) trong thân bài và `recap`.
  - **`INFO` (`"càng "`):** 2 câu (`sym#0`, `intuition#0`) — chính xác.

### `L02` — Mô hình không gian vector: TF-IDF và độ tương tự cosin
- **Kỹ thuật:** `108` frames (`859.367s`), `asr_report`: `gắn cờ 29, chưa xem xét 0`, `SRT == say`, `spec_ok=True, tts_ok=True`, `covers: [1->example, 2->check, 3->practice]`.
- **PNG đã xem:** `out/IRS/L02/frames/00024.png` (SVG không gian từ `pin`/`màn`), `out/IRS/L02/frames/00094.png` (`practice#0`). Sạch.
- **Điểm `P1 = 1` · `P8 = 0` (HỎNG) · `P9 = 2`** (`pitfalls#2`: kho 3 văn bản vs 10 văn bản; `quiz#2`: kho triệu văn bản cần chuẩn hoá sẵn và tính lại khi kho đổi).
- **Phát hiện:**
  - **`MUST` (Sai công thức `idf` & mâu thuẫn số liệu giữa thân bài/giáo án với `practice`/`loi_giai.py`/`mong_doi.txt`):**
    - Trong `curriculum/irs.yaml` L02 và thân bài `L02_tf_idf.yaml` (`example#0..#2`, `verify_parts/L02.py`): với 3 văn bản `d1="máy ổ máy"`, `d2="máy pin"`, `d3="máy pin màn"`, từ `"pin"` có `df = 2`, nên **`idf(pin) = ln(3 / 2) = ln(1,5) ≈ 0,405`** và **`cos(q, d3) ≈ 0,346`**.
    - Thế nhưng `labs/IRS/L02/loi_giai.py` và `L02` `practice#1/#2/#4` (dòng 447–462) viết **`idf_pin = math.log(3 / 1.5)`** (lấy `3 / 1.5 = 2` → `ln(2) = 0,693`!), đồng thời gán nhầm **`v_d3 = (0.0, idf_pin, idf_o)`** (dùng `idf_o` cho từ `"man"`) và gán cứng **`cos_d2 = 1.0`**. Đầu ra `mong_doi.txt` là `idf_may=0.0 idf_pin=0.693 cos_d2=1.0 cos_d3=0.534` — **sai hoàn toàn** so với bài giảng (`0.405` và `0.346`). Học viên cài đúng `idf = ln(N/df)` theo `de.md` và bài giảng sẽ bị `cham.sh` chấm **FAIL**.
  - **`SHOULD` (`P1`):** `TF-IDF` xuất hiện ở `title`, `practice#3`, `de.md` nhưng trong `say` và thân bài không nói tên gọi `TF-IDF`; `practice#0` thiếu giải thích `math.hypot` và dùng `"mô-đun"`.
  - **`INFO` (`"càng "`):** 3 câu (`prereq#0`, `prereq#2`, `sym#0`) — chính xác.

### `L03` — Truy hồi dày và tìm láng giềng gần đúng
- **Kỹ thuật:** `107` frames (`856.367s`), `asr_report`: `gắn cờ 7, chưa xem xét 0`, `SRT == say`, `spec_ok=True, tts_ok=True`, `covers: [1->example, 2->check, 3->practice]`.
- **PNG đã xem:** `out/IRS/L03/frames/00032.png` (SVG 3 cụm A, B, C), `out/IRS/L03/frames/00094.png` (`practice#0`). Sạch (chú ý nhãn `láng giềng thật (3,5; 1) ở cụm B` sát viền dưới hộp cam nhưng không chạm/tràn).
- **Điểm `P1 = 1` · `P8 = 2` · `P9 = 2`** (12 điểm vs 5000 điểm vs 1 triệu vs 4 triệu; thêm 200 000 sản phẩm làm cụm phình `11 000 -> 211 000` chậm `19x`; `recap` chưa có mục `Hai mức quy mô` riêng).
- **Phát hiện:**
  - **`SHOULD` (`P1`):** `labs/IRS/L03/de.md` và `practice#3` dùng viết tắt **`IVF`** (*"IVF tìm láng giềng gần đúng"*) nhưng trong toàn bộ thân bài `L03` (cả `show` lẫn `say`) chưa từng xuất hiện hay giải thích chữ viết tắt `IVF` (chỉ gọi là "chỉ mục chia cụm" / "tệp ngược"); `practice#1` dùng `1_000_000` (dấu `_` ngăn cách số) chưa giảng trong `practice#0`.
  - **`INFO` (`"càng "`):** 0 câu.

### `L04` — Truy hồi lai và hợp nhất thứ hạng
- **Kỹ thuật:** `108` frames (`836.533s`), `asr_report`: `gắn cờ 14, chưa xem xét 0`, `SRT == say`, `spec_ok=True, tts_ok=True`, `covers: [1->example, 2->check, 3->practice]`.
- **PNG đã xem:** `out/IRS/L04/frames/00035.png` (SVG ghép danh sách từ khoá + vector), `out/IRS/L04/frames/00095.png` (`practice#0`). Sạch.
- **Điểm `P1 = 1` · `P8 = 2` · `P9 = 1`** (chỉ có ngưỡng cắt danh sách 4 vs 100 dòng ở `pitfalls#3` và năm 2009, chưa có số liệu ở ≥ 2 mức quy mô kho/tải; `recap` không có `Hai mức quy mô`).
- **Phát hiện:**
  - **`SHOULD` (`P1`):** `labs/IRS/L04/de.md` và `practice#3` dùng **`Reciprocal Rank Fusion`** và **`RRF`**, nhưng thân bài `L04` chỉ dùng tiếng Việt *"hợp nhất thứ hạng"* và chưa từng giới thiệu `RRF`/`Reciprocal Rank Fusion`; `practice#0` giải `lambda x: ...` nhưng `practice#1` dùng `lambda r1, r2, k=60:` và toán tử ba ngôi `'B' if sb > sa else 'A'`.
  - **`SHOULD` (`P9`):** Thiếu đối chiếu ở ≥ 2 mức quy mô hệ thống trong thân bài và `recap`.
  - **`INFO` (`"càng "`):** 3 câu (`prereq#0`, `prereq#2`, `formula#0`) — chính xác.

### `L05` — Học để xếp hạng: theo điểm, theo cặp, theo danh sách
- **Kỹ thuật:** `107` frames (`878.5s`), `asr_report`: `gắn cờ 3, chưa xem xét 0`, `SRT == say`, `spec_ok=True, tts_ok=True`, `covers: [1->example, 2->check, 3->practice]`.
- **PNG đã xem:** `out/IRS/L05/frames/00034.png` (SVG đường mất mát theo cặp), `out/IRS/L05/frames/00094.png` (`practice#0`). Sạch.
- **Điểm `P1 = 1` · `P8 = 2` · `P9 = 2`** (`pitfalls#3`: 1 cặp vs câu hỏi 1000 văn bản → `499 500` cặp phải lấy mẫu).
- **Phát hiện:**
  - **`SHOULD` (`P1`):** `de.md` và `practice#3` dùng **`RankNet pairwise loss`** — `RankNet` chỉ xuất hiện trong HTML `formula#0` (không có trong `say`), còn `pairwise loss` chưa từng giảng trong thân bài (chỉ gọi là "mất mát theo cặp"); `practice#0` dùng `"mô-đun"` và thiếu `math.log1p`.
  - **`INFO` (`"càng "`):** 4 câu (`prereq#3`, `intuition#0` ×2, `formula#1`) — chính xác.

### `L06` — Lọc cộng tác theo láng giềng
- **Kỹ thuật:** `94` frames (`747.633s`), `asr_report`: `gắn cờ 22, chưa xem xét 0`, `SRT == say`, `spec_ok=True, tts_ok=True`, `covers: [1->example, 2->check, 3->practice]`.
- **PNG đã xem:** `out/IRS/L06/frames/00018.png` (SVG đồ thị U-V-W), `out/IRS/L06/frames/00081.png` (`practice#0`). Sạch.
- **Điểm `P1 = 1` · `P8 = 2` (vận hành) · `P9 = 2`** (`item_based`: 1 triệu người dùng → `~5·10^11` cặp đổi liên tục vs bảng cùng xem theo sản phẩm ít đổi hơn).
- **Phát hiện:**
  - **`SHOULD` (gán cứng / đi đường tắt):** `labs/IRS/L06/loi_giai.py` và `practice#1` gán cứng tích vô hướng `20.0`, `11.0` và bình phương độ dài `34`, `32`, `30` thay vì tính từ `U=(5,3,0), V=(4,0,4), W=(1,2,5)` và bỏ qua số 0 chưa chấm khi đánh giá.
  - **`SHOULD` (`P1`):** `practice#0` dùng `"mô-đun"` chưa giải nghĩa; thân bài (`hook..quiz`) sạch 100%.
  - **`INFO` (`"càng "`):** 1 câu (`prereq#0`) — chính xác.

### `L07` — Phân rã ma trận cho gợi ý
- **Kỹ thuật:** `123` frames (`931.367s`), `asr_report`: `gắn cờ 6, chưa xem xét 0`, `SRT == say`, `spec_ok=True, tts_ok=True`, `covers: [1->example, 2->check, 3->practice]`.
- **PNG đã xem:** `out/IRS/L07/frames/00040.png` (SVG phân rã ma trận `P × Q`), `out/IRS/L07/frames/00109.png` (`practice#0`). Sạch.
- **Điểm `P1 = 1` · `P8 = 2` · `P9 = 2`** (`480 189 × 17 770 = 8,53 tỉ` ô → `24,9 triệu` tham số; người mới 1 lượt chấm vs nhiều lượt chấm cần chỉnh `λ`).
- **Phát hiện:**
  - **`SHOULD` (`P1`):** `de.md` và `practice#3` dùng viết tắt **`SGD`** (*"Phân rã ma trận SGD"*), nhưng thân bài `L07` chỉ gọi *"đi xuống dốc"* và chưa từng giảng hay nhắc chữ `SGD`; `practice#0` chưa giải `zip(p, q)` và `round(..., 4)` trong `practice#1`.
  - **`INFO` (`"càng "`):** 2 câu (`prereq#2`, `prereq#4`) — chính xác.

### `L08` — Phản hồi ngầm, lấy mẫu âm và thiên lệch phổ biến
- **Kỹ thuật:** `126` frames (`949.7s`), `asr_report`: `gắn cờ 4, chưa xem xét 0`, `SRT == say`, `spec_ok=True, tts_ok=True`, `covers: [1->example, 2->check, 3->practice]`.
- **PNG đã xem:** `out/IRS/L08/frames/00040.png` (SVG 3 cách chia mẫu âm), `out/IRS/L08/frames/00113.png` (`practice#0`). Sạch.
- **Điểm `P1 = 1` · `P8 = 2` · `P9 = 2`** (`pitfalls#3`: 1 người cực tích cực 1000 lượt + 99 người 10 lượt → `50,3%` mất mát vs cố định 10 mẫu → `1%`; tiến trình 2008 → 2013 → 2016 → 2019).
- **Phát hiện:**
  - **`SHOULD` (`P1` / ký hiệu):** `de.md` và `practice#3` viết *"bù tần suất log(p)"* dễ nhầm với `log10(p)` và thiếu dấu trừ (`loi_giai.py` dùng `-math.log(0.02)` đúng như `ln` ở thân bài); `practice#0` dùng `"mô-đun"`.
  - **`INFO` (`"càng "`):** 2 câu (`hook#1`, `prereq#3`) — chính xác.

### `L09` — Khởi động lạnh và khám phá trong gợi ý
- **Kỹ thuật:** `123` frames (`950.2s`), `asr_report`: `gắn cờ 1, chưa xem xét 0`, `SRT == say`, `spec_ok=True, tts_ok=True`, `covers: [1->example, 2->check, 3->practice]`.
- **PNG đã xem:** `out/IRS/L09/frames/00040.png` (SVG phân phối `Beta(1,1)` vs `Beta(51,951)`), `out/IRS/L09/frames/00108.png` (`practice#0`). Sạch.
- **Điểm `P1 = 1` · `P8 = 2` · `P9 = 2`** (`0` lượt vs `19` vs `40/60` vs `1000` lượt; kho `10 000` sản phẩm với `ε-greedy` chỉ `0,00001` mỗi món nên thực tế 2019 bỏ; người mới vs xem nhiều).
- **Phát hiện:**
  - **`SHOULD` (`P1`):** `practice#0` dùng `"mô-đun"`, chưa giải `lambda` 2 tham số trả tuple; `Thompson sampling` có trong HTML `formula#2` nhưng không đọc trong `say`.
  - **`INFO` (`"càng "`):** 2 câu (`sym#0`, `sym#1`) — chính xác.

### `L10` — Thiên lệch vị trí: đánh giá ngoại tuyến bằng trọng số nghịch đảo xu hướng
- **Kỹ thuật:** `110` frames (`887.167s`), `asr_report`: `gắn cờ 3, chưa xem xét 0`, `SRT == say`, `spec_ok=True, tts_ok=True`, `covers: [1->example, 2->check, 3->practice]`.
- **PNG đã xem:** `out/IRS/L10/frames/00025.png` (SVG cột xác suất nhìn thấy vị trí 1..5), `out/IRS/L10/frames/00095.png` (`practice#0`). Sạch.
- **Điểm `P1 = 1` · `P8 = 2` · `P9 = 2`** (nhật ký nhỏ `1000` lần ở `p=0,02` độ lệch chuẩn `0,05` phải cắt vs `100 000` lần; ngoại tuyến vs thử nghiệm trực tuyến 2016/2017/2019).
- **Phát hiện:**
  - **`SHOULD` (`P1`):** `de.md` và `practice#3` dùng hai viết tắt tiếng Anh **`CTR`** và **`IPS`** (*"chuẩn hoá CTR"*, *"trọng số nghịch đảo xu hướng IPS"*), nhưng thân bài `L10` chỉ dùng tiếng Việt *"tỉ lệ bấm"* và *"trọng số nghịch đảo xu hướng"*, chưa từng giải thích `CTR` hay `IPS`.
  - **`INFO` (`"càng "`):** 2 câu (`check#1`, `recap#2`) — chính xác.

### `L11` — Đa dạng, công bằng và vòng phản hồi của hệ gợi ý
- **Kỹ thuật:** `108` frames (`833.133s`), `asr_report`: `gắn cờ 7, chưa xem xét 0`, `SRT == say`, `spec_ok=True, tts_ok=True`, `covers: [1->example, 2->check, 3->practice]`.
- **PNG đã xem:** `out/IRS/L11/frames/00021.png` (SVG bản đồ ứng viên A, X, Y, Z), `out/IRS/L11/frames/00093.png` (`practice#0`). Sạch.
- **Điểm `P1 = 1` · `P8 = 2` · `P9 = 2`** (`loop`: tiến triển qua ngày 1..4; `pitfalls#3`: hệ sản xuất 2016/2019 phải lấy mọi lượt xem và dữ liệu khám phá).
- **Phát hiện:**
  - **`SHOULD` (`P1`):** `de.md` và `practice#3` dùng viết tắt **`MMR`** (*"MMR cân bằng liên quan với đa dạng"*, `MMR = lam*rel - (1-lam)*sim`), nhưng thân bài `L11` chưa từng nhắc hay giải thích `MMR`; `practice#1` dùng toán tử ba ngôi `'Y' if sy > sx else 'X'` chưa giải ở `practice#0`.
  - **`INFO` (`"càng "`):** 3 câu (`prereq#1` ×2, `intuition#0`) — chính xác.

### `L12` — Tình huống chuyên gia: thiết kế hệ gợi ý hai tầng trong ngân sách 100 ms
- **Kỹ thuật:** `96` frames (`754.367s`), `asr_report`: `gắn cờ 2, chưa xem xét 0`, `SRT == say`, `spec_ok=True, tts_ok=True`, `covers: [1->example, 2->check, 3->check, 4->practice]`.
- **PNG đã xem:** `out/IRS/L12/frames/00029.png` (SVG cái phễu + thanh ngân sách 100 ms), `out/IRS/L12/frames/00081.png` (`practice#0`). Sạch.
- **Điểm `P1 = 1` · `P8 = 0` (HỎNG) · `P9 = 2`** (`10 triệu` sản phẩm chấm thẳng 500s → 10 000 = 500ms → 1000 = 80ms TB / 115ms p99 → 600 = 87ms p99; 1 vs 10 vs 100 mảnh).
- **Phát hiện:**
  - **`MUST` (Lệch tham số giữa `de.md` và `loi_giai.py`/`mong_doi.txt`/`practice#1`):**
    - `labs/IRS/L12/de.md` ghi: *"Cắt ứng viên `1000 -> 600` (`0.05ms` rank + `15ms` gen + `30ms` net)"*.
    - Nhưng `loi_giai.py` và `L12` `practice#1` dùng chi phí p99 là **`0.07` ms/ứng viên** (`15 + 1000 * 0.07 + 30 = 115ms`, `15 + 600 * 0.07 + 30 = 87ms`). Nếu học viên làm theo đúng con số `0.05ms` trong `de.md`, kết quả là `p99_before=95ms p99_after=75ms` và **FAIL `cham.sh`**.
  - **`SHOULD` (`P1`):** `de.md` dùng viết tắt tiếng Anh `rank`, `gen`, `net` chưa xuất hiện trong bài.
  - **`INFO` (`"càng "`):** 1 câu (`pitfalls#2`) — chính xác.

### `L13` — Hành trình: gợi ý video từ đồ thị cùng xem tới hệ thống hai tầng
- **Kỹ thuật:** `153` frames (`1239.567s`), `asr_report`: `gắn cờ 4, chưa xem xét 0`, `SRT == say`, `spec_ok=True, tts_ok=True`, `covers: [1->stage1, 2->stage2, 3->practice]`.
- **PNG đã xem:** `out/IRS/L13/frames/00028.png` (SVG dòng thời gian 5 chặng 2008–2019), `out/IRS/L13/frames/00135.png` (`practice#0`). Sạch.
- **Điểm `P1 = 1` · `P8 = 2` (hoặc `1` nếu chỉ đọc `de.md`) · `P9 = 2`** (5 chặng 2008 → 2016 → 2019 + quiz 20 000 vs 2 triệu sản phẩm; `recap` tóm tắt quy mô theo từng chặng).
- **Phát hiện:**
  - **`SHOULD` (`P1` / nhất quán đơn vị `MiB`):** `de.md` yêu cầu *"Tính bộ nhớ bảng nhúng 1 triệu × 256 số float32"*, `loi_giai.py` chia `1024**2` ra **`emb_mib=976.6`**, trong khi thân bài `L13` (`stage2#0` và `check#0`) chỉ tính **`1 024 000 000 byte ≈ 1 tỉ byte`** và **chưa từng giảng `float32` hay `MiB = 1024² byte`** (chỉ `practice#2/#4` lộ tên biến `emb_mib=976.6`).
  - **`INFO` (`"càng "`):** 2 câu (`stage2#0`, `stage5#1`) — chính xác.

---

## 3. Danh sách ảnh PNG đã kiểm tra (28/28 khung)

- `L00`: `00024.png` (SVG), `00094.png` (`practice#0`)
- `L01`: `00022.png` (SVG), `00090.png` (`practice#0`)
- `L02`: `00024.png` (SVG), `00094.png` (`practice#0`)
- `L03`: `00032.png` (SVG), `00094.png` (`practice#0`)
- `L04`: `00035.png` (SVG), `00095.png` (`practice#0`)
- `L05`: `00034.png` (SVG), `00094.png` (`practice#0`)
- `L06`: `00018.png` (SVG), `00081.png` (`practice#0`)
- `L07`: `00040.png` (SVG), `00109.png` (`practice#0`)
- `L08`: `00040.png` (SVG), `00113.png` (`practice#0`)
- `L09`: `00040.png` (SVG), `00108.png` (`practice#0`)
- `L10`: `00025.png` (SVG), `00095.png` (`practice#0`)
- `L11`: `00021.png` (SVG), `00093.png` (`practice#0`)
- `L12`: `00029.png` (SVG), `00081.png` (`practice#0`)
- `L13`: `00028.png` (SVG), `00135.png` (`practice#0`)

---

## 4. Kết luận & Khuyến nghị khắc phục (để chuyển sang `GO`)

**Kết luận:** **`NO-GO`**

1. **Sửa `MUST` ở `L02`:** Thay `math.log(3 / 1.5)` bằng `math.log(3 / 2)` (tính đúng `df` từ 3 văn bản `'may o may'`, `'may pin'`, `'may pin man'`, dùng `idf_man`, không gán cứng `cos_d2 = 1.0`), cập nhật `labs/IRS/L02/loi_giai.py`, `mong_doi.txt`, `L02_tf_idf.yaml` (`practice#1/#2/#4`) và dựng lại video `L02` (để `idf_pin=0.405`, `cos_d3=0.346` khớp thân bài).
2. **Sửa `MUST` ở `L12`:** Sửa `labs/IRS/L12/de.md` từ `0.05ms rank` thành `0.07ms rank ở phân vị 99 (70ms/1000)` để khớp `loi_giai.py` và `mong_doi.txt` (`115ms` và `87ms`).
3. **Xử lý `SHOULD` ở `L00, L06, L13` và `P1`/`P9`:**
   - Bỏ gán cứng trong `L00` và `L06` `loi_giai.py` / `practice#1` (viết hàm tính từ vector/danh sách hạng).
   - Đồng bộ thuật ngữ tiếng Anh/viết tắt trong `de.md` và `practice#3` (`IVF`, `RRF`/`Reciprocal Rank Fusion`, `RankNet pairwise loss`, `SGD`, `CTR`, `IPS`, `MMR`, `Mean Reciprocal Rank`, `TF-IDF`, `gen`/`net`/`rank`, `float32`/`MiB`) bằng tiếng Việt đã dạy hoặc giải nghĩa tại chỗ; bổ sung giải nghĩa `"mô-đun"` và các hàm Python xuất hiện trong `practice#1`.
   - Bổ sung 2 mức quy mô cho `L01, L04` và phần tổng kết `Hai mức quy mô` trong `recap` nếu áp dụng chuẩn `P9` chặt cho toàn khóa.