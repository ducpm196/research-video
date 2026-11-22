# Báo cáo Kiểm định Độc lập WP-AF4-5 Stage 8 — Khóa `SAR` (`L00–L13`, 14 bài, v2)

**Vai trò:** WP-AF4-5 Stage 8 SAR Verifier v2 (độc lập, read-only)  
**Phán quyết tổng thể:** **`NO-GO`**

---

## 1. Tóm tắt kiểm tra tự động (chạy thực tế trong sandbox)
- `lv.py curriculum curriculum/sar.yaml`: **14/14 bài có đặc tả, 0 lỗi** (`rc=0`).
- `lv.py lint lessons/sar/L*.yaml`: **14/14 PASS (`0 FAIL, 0 WARN`)**.
- `audit/sar/verify_sar.py`: **15/15 PASS (`0 FAIL`)**.
- `labs/sar/L*/loi_giai.py` chạy trực tiếp vs `mong_doi.txt`: **14/14 PASS**.
- `audit/review/screen_code.py check --course SAR`: **15 khối — PASS 16 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0** (`1 NOT_VERIFIED` hợp lệ cho số liệu minh họa ở `L01 example 0 0`).
- `audit/review/arith_scan.py SAR`: **31 phép tính kiểm được, 0 FAIL**.
- `audit/layout_SAR.tsv`: **0 lỗi** (`preview.html` và `layout_SAR.tsv` mới hơn thời điểm sửa YAML).
- `L*.srt == say`: **14/14 khớp 100%**; `out/sar/L*/asr_report.md`: **14/14 `chưa xem xét: 0`, `thiếu audio: 0`**.
- **Ngưỡng chính tả / câu / SVG**: `"càng "` chỉ có 1 câu ở `L02:212,224` (kèm bảng số $1/(1-b)$ rõ ràng, không gây hiểu nhầm); `SPELL_CANON` & `E55` sạch ở cả YAML và `de.md`; 15/15 `<svg>` có `oob=[]`, 0 `$...$` trong SVG, kiểm tra trực tiếp 9 khung PNG (`audit/sar/snap/*.png` & `out/sar/*/frames/*.png`) sạch đẹp; `L13` tuân thủ `audit/sar/sources_L13.md` (không lọt tên riêng, có nhãn `(số minh hoạ)`).
- **`lv.py verify` (MP4/build):** **14/14 FAIL — `video STALE: file đặc tả đã đổi sau lần build`** (`spec_sha256` lệch vì đã thêm `Hai mức quy mô` và sửa `covers:` sau bản build `2026-11-19`, trong khi `tts_sha256` vẫn khớp).

---

## 2. Danh sách `MUST fix` (chặn `GO`)

### M1. Trạng thái MP4 STALE (`14/14`) & Thời lượng MP4 thực tế `< 9.0` phút (`5/14` bài)
- `L00–L13` đều FAIL `lv.py verify` (`video STALE`) vì YAML sửa sau bản dựng `2026-11-19`.
- 5 bài có `timeline_seconds` thực tế `< 540s` (`< 9.0` phút) trong `out/sar/L*/build_report.json`:
  - `L00`: `531.667s` (**8.86 phút**, 1407 từ)
  - `L01`: `522.600s` (**8.71 phút**, 1440 từ)
  - `L08`: `518.933s` (**8.65 phút**, 1377 từ)
  - `L10`: `511.100s` (**8.52 phút**, 1393 từ)
  - `L11`: `488.767s` (**8.15 phút**, 1362 từ)
- Cần bổ sung lời giảng (bao gồm đọc `Hai mức quy mô`, bảng đọc mã/thuật ngữ và phần mở rộng ngắn ở 5 bài trên) để đạt `>= 540s` (`>= 9.0` phút), chạy lại `layout_scan.py SAR`, dựng lại `MP4` và chạy `lv.py verify` + `asr` cho cả 14/14 bài.

### M2. Lỗi toán học & mâu thuẫn dữ liệu ở `L00 recap#1` và `L07 de.md`
1. **`lessons/sar/L00_thuoc_tinh_chat_luong.yaml:262` (`recap#1`, khối `Hai mức quy mô`)**:
   - Đang viết: `"một dịch vụ đạt sẵn sàng 99,5% chỉ ngừng nhẹ, nhưng ghép chuỗi 10 dịch vụ tụt xuống 95,4% (chỉ dùng 5 dịch vụ đạt 62,4% nếu thiếu độc lập)"`.
   - **Sai hoàn toàn về toán và đại lượng**: Thân bài `L00 pitfalls#3` (`L00:182-183`) tính **độ trễ SLO** với mỗi dịch vụ đạt **95,4%** (`0,954^5 = 79,0%`, `0,954^10 = 62,4%`), không phải sẵn sàng `99,5%` (`0,995^10 ≈ 95,1%`). Câu này vừa nhầm `99,5%` với `95,4%`, vừa đảo ngược kết quả `10 dịch vụ -> 95,4%` và `5 dịch vụ -> 62,4%`, và nói ngược về giả thiết độc lập. Phải viết lại khớp đúng `L00:182-183` (`1 dịch vụ 95,4% -> 5 dịch vụ 79,0% -> 10 dịch vụ 62,4%`).
2. **`labs/sar/L07/de.md:3` & `labs/sar/L07/loi_giai.py:2`**:
   - Đang viết: `"trong khoảng 4.9 giây (tổng 5 000 yêu cầu req ở mức 1 000 yêu cầu/s), tổng số token khả dụng bằng 20 + int(4.9 * 10) = 69"`.
   - **Mâu thuẫn toán học**: Ở tốc độ `1 000 yêu cầu/s`, `4.9` giây chỉ có `4 900` yêu cầu (`t = 0..4.999 s` mới có `5 000` yêu cầu, như `L07:99` dùng `4.999 s`!).
   - Ngoài ra, `loi_giai.py:2` chỉ dùng biểu thức đóng `acc = cap + int(4.9 * rate)`, không cài vòng lặp mô phỏng thùng token theo từng yêu cầu dù `obj1` là `"Cài thùng token"`.

### M3. `covers:` trỏ sai cảnh dạy thực chất (`L04, L10` sai nặng; `L01, L13` lệch `practice`)
- **`lessons/sar/L04_bo_nho_dem.yaml:284-286`**: `objective: 2` (`"Chọn chiến lược ghi và thời gian sống"`) đang trỏ `scene: check`, nhưng `L04 check` (`L04:144-164`) chỉ kiểm lại độ trễ `1,49 / 25,5 / 5,9 ms` và jitter `368 khoá`, **không hề nhắc tới chiến lược ghi hay thời gian sống** (nội dung này nằm ở `sym` dòng `71-90` và `pitfalls` Lỗi 1 dòng `172-174`). *(Lưu ý: `E51` đòi động từ `"Chọn"` trỏ vào `example/check/practice/formula`, nên cần đưa bước chọn chiến lược ghi + TTL vào `example`/`check` hoặc đổi đầu mục tiêu/cảnh cho khớp.)*
- **`lessons/sar/L10_nhat_quan_da_vung.yaml:266-268`**: `objective: 2` (`"Chọn mức nhất quán theo từng loại dữ liệu"`) đang trỏ `scene: check`, nhưng `L10 check` (`L10:134-164`) chỉ liệt kê các cặp vùng & tình huống chết vùng, **không hề nhắc loại dữ liệu** (nội dung này nằm ở `pitfalls` Lỗi 1 dòng `170-171` và `quiz` câu 3 dòng `219-227`).
- **`lessons/sar/L01_ghi_quyet_dinh.yaml:270-275`**: `objective: 1` (`"Viết bản ghi quyết định: bối cảnh, lựa chọn, hệ quả"`) trỏ `practice`, trong khi `labs/sar/L01/de.md` chỉ chấm điểm trọng số `RDBMS` vs `NoSQL` chứ không viết ADR 4 mục (nên trỏ `obj1 -> example` vốn có Quyết định 007 đầy đủ bối cảnh/lựa chọn/hệ quả).
- **`lessons/sar/L13_hanh_trinh_twitter.yaml:507-509`**: `objective: 3` (`"Chọn giữa thêm máy và tách dịch vụ ở quy mô của chính mình, kèm điều kiện đổi lựa chọn"`) trỏ `practice`, nhưng `labs/sar/L13/de.md` chỉ tính `100 GB/ngày`, `5787 tweet/s`, `36.5 TB/năm` cho Twitter (`obj2`); nội dung `obj3` nằm ở `stage3` / `quiz`.

### M4. `[P8]` Lộ đáp số/công thức trước `pause:`, trùng bộ số ví dụ, thiếu định nghĩa & quy ước làm tròn
1. **Lộ đáp số và/hoặc công thức trước `pause: 30` trong `14/14` `labs/sar/L*/de.md` và `practice#0`**:
   - **Tất cả 14/14 tệp `labs/sar/L*/de.md`** đều in sẵn nguyên 3 dòng đáp số cuối (`1. ... 2. ... 3. ...`) ngay trong đề bài (người học chỉ cần chép 3 lệnh `print` là qua `cham.sh`). Phải thay bằng khuôn mẫu placeholder (`p95_ms=<giá_trị>`) và chỉ hiện đáp số thật ở `practice#1` sau `pause: 30`.
   - **Lộ công thức/code/kết quả trong mô tả đề & `practice#0`**:
     - `L02/de.md:3` & `L02:291`: lộ `avg_qps=2315`, `peak_qps=6944`.
     - `L03:257`: lộ `chỉ giao diện → nghiệp vụ → dữ liệu (UI->App->Data), cấm gọi ngược`.
     - `L04/de.md:3` & `L04:248`: lộ công thức `h * 1 + (1 - h) * 50` và kết quả `90% -> 5.90 ms`, `99% -> 1.49 ms`.
     - `L05:252`: lộ `cần 10 phân mảnh (shard) x 3 = 30 nút`.
     - `L06/de.md:3` & `L06:245`: lộ công thức `1 - (1-a)^2`, `a^2` và kết quả `99,99%`, `98,01%`.
     - `L07/de.md:3` & `L07:245`: lộ công thức code `20 + int(4.9 * 10) = 69`.
     - `L08:228`: lộ `tích lũy 20/s → sau 1 giờ tồn 72 000 tin`.
     - `L09/de.md:3` & `L09:239`: lộ `INSERT INTO idem` và đáp số `150`.
     - `L10/de.md:3` & `L10:233`: lộ `RTT = 2 * one_way = 80 ms` và `>= 80 ms`.
     - `L11/de.md:3`: lộ thẳng lệnh SQLite `PRAGMA query_only = ON`.
     - `L12/de.md:3` & `L12:266`: lộ `10^8 / 2 592 000 s`, `38,6 ghi/giây`, `11 574/giây`.
     - `L13/de.md:3` & `L13:469`: lộ `500 triệu x 200 byte = 100 GB`, `36.5 TB`, `~5 787 tweet/giây`.
2. **Trùng nguyên bộ số ví dụ từ thân bài giảng (`8/14` bài lặp y hệt, `2/14` lặp phần lớn)**:
   - Trùng nguyên bộ số `example`/`stage1`: **`L02`** (`10M DAU x 20 req, 3x -> 2315, 6944`), **`L04`** (`1 ms, 50 ms, 90% -> 5.90, 99% -> 1.49`), **`L05`** (`5 TB, 500 GB/nút, RF=3 -> 10, 30`), **`L06`** (`2 nút 99% -> 99.99%, 98.01%`), **`L07`** (`rate=10, cap=20, 5000 req -> 69`), **`L08`** (`120/s, 100/s, 1h -> 72000`), **`L12`** (`100M/tháng, 500 B, 5 năm -> 38.6, 11574, 3.0 TB`), **`L13`** (`500M/ngày x 200 B = 100 GB/ngày, 5787`). Nên đổi sang bộ số mới độc lập cho tất cả các lab này (vẫn giữ `L00, L01, L11` là bộ số/tình huống riêng tốt; `L03, L09, L10` nên đổi bộ số/tên lớp mới để tránh trùng hoàn toàn).
3. **Thiếu định nghĩa/quy ước trong `de.md` (không tự đủ để giải đúng định dạng)**:
   - **`L06/de.md:3`**: **THIẾU định nghĩa `downtime_ratio`** (không nói lấy `(1 - series_pct) / (1 - parallel_pct)` hay làm tròn số nguyên + `x`).
   - **`L02/de.md:3`**: thiếu quy ước `1 KB = 1000 B`, `1 MB = 10^6 B`, làm tròn số nguyên (`avg_qps`, `peak_qps`) và `1` chữ số thập phân (`peak_mb_per_s`), và chưa nêu rõ `peak_mb_per_s` đo bằng `MB/s` (không nhân 8) khác với `megabit/s` ở thân bài.
   - **`L04/de.md:3`**: thiếu định nghĩa `speedup_99_vs_no_cache` (`50 / lat_99pct_ms`) và quy ước làm tròn (`:.2f`, `:.1f` + `x`).
   - **`L01, L07, L08, L12, L13` `de.md`**: thiếu quy ước làm tròn (`:.2f` ở `L01`, `:.2f` + `%` ở `L07`, `:.1f` ở `L08`, `1 tháng = 30 ngày` & `round`/`1 TB = 10^12 B` ở `L12`, `1 năm = 365 ngày` & `round`/`1 GB = 10^9 B` ở `L13`), riêng `L01/de.md` cần nêu rõ thứ tự trọng số `(0.5, 0.3, 0.2)` ứng với `(acid, join, scale_write)`.

### M5. `[P1]` Thuật ngữ tiếng Anh & token thực hành chưa giảng tại chỗ (`14/14` bài)
- **Thiếu bảng đọc mã/token thực hành** (`"viết trong mã → đọc là"`) cho `practice`/`de.md`/`loi_giai.py` ở cả `14/14` bài (đặc biệt các từ khoá SQLite ở `L09, L11`: `sqlite3`, `CREATE TABLE`, `PRIMARY KEY`, `INSERT INTO`, `UPDATE`, `SELECT`, `DELETE`, `PRAGMA query_only = ON`, `IntegrityError`, `OperationalError`, và các tên biến/hàm `sorted`, `zip`, `math.ceil`, `:.2f`).
- **Thuật ngữ chuyên môn tiếng Anh lọt vào `practice#0` và `de.md` nhưng CHƯA được giảng/liệt kê trong thân bài (`hook..quiz`)**:
  - `L00` (`L00:239`, `L00/de.md`): `P95`, `P99`, `SLO`.
  - `L01` (`L01:238`, `L01/de.md`): `ADR`, `RDBMS`, `NoSQL`, `ACID`, `Sharding`, `join`, `scale_write`, `vs`.
  - `L02` (`L02/de.md`): `QPS`, `DAU`, `req`.
  - `L03` (`L03:257`, `L03/de.md`): `UI`, `App`, `Data`, `RANK`, `caller`, `callee` (và `UI-&gt;App-&gt;Data` dùng `->` thay `→`).
  - `L04` (`L04:248`, `L04/de.md`): `Cache`, `DB`, `hit`, `Cache Hit Rate`, `speedup`.
  - `L05` (`L05:252`, `L05/de.md`): `RF`, `Replication Factor`, `shard`.
  - `L06` (`L06:245`, `L06/de.md`): `vs`, `parallel`, `series`, `downtime`.
  - `L07` (`L07:245`, `L07/de.md`): `burst`, `cap`, `rate`, `req`, `accepted`, `rejected`.
  - `L08` (`L08/de.md`): `backlog`, `drain`, `msg/s`.
  - `L09` (`L09/de.md`): `SQLite`, `sqlite3`, `ledger`, `idem`, `bal`, `INSERT INTO`, `PRIMARY KEY`, `IntegrityError`, `tx_attempts`, `applied_once`.
  - `L10` (`L10/de.md`): `RTT`, `one_way`, `sync`, `async`, `cross_region`.
  - `L11` (`L11:234`, `L11/de.md`): `SQLite`, `PRAGMA query_only = ON`, `SELECT`, `DELETE`, `INSERT`, `OperationalError`, `blast_radius`.
  - `L12` (`L12:266`, `L12/de.md`): `URL Shortener`, `link`, `QPS`.
  - `L13` (`L13/de.md`): `QPS`, `500M` (thân bài dùng `TPS` và `500 triệu`).

### M6. `[P9]` Khối `Hai mức quy mô` trong `recap` chưa đọc thành lời & bị `focus` làm mờ (`L04, L06, L13`); thân bài `L03, L09` lệch `show`/`say`
- Ở **14/14 bài (`L00–L13`)**, `<p class="note"><b>Hai mức quy mô:</b> ...` trong `recap#1` chỉ nằm trong `show:`, **không có trong `say:`** (người chỉ nghe/xem không được giảng phần này).
- Đặc biệt ở `L04:272-274`, `L06:269-271`, `L13:494-496`, `focus: [1, 1]` chỉ tô sáng khối `Tư duy` (phần tử 1) và **làm mờ (dim) toàn bộ đoạn `Hai mức quy mô:`** (phần tử 2) suốt khung hình!
- Ở **`L03:190-191`** (`pitfalls` Lỗi 3) và **`L09:176-184`** (`pitfalls` Lỗi 4), câu đối chiếu 2 quy mô mới chỉ thêm vào `show:`, **chưa được đọc trong `say:`**.

---

## 3. Danh sách `SHOULD fix`

1. **Chính xác hóa số liệu `L01:261` (`recap#1`)**: ghi rõ `"ngưỡng xem lại 2 500/s ở tháng 21 và chạm trần 5 000/s ở tháng 36"` thay vì `"trần dự kiến 2 600/s ở tháng thứ 21–36"` (tránh lẫn số quiz `2 600/s`).
2. **Định nghĩa tường minh `"mô-đun"` / `"mô-đun hoá"` trong thân bài `L03 sym`** (`L03:56-74`): hiện từ này chỉ nằm ở tiêu đề `L03` và nhắc tên ở `L02:320`, chưa được giải thích trực tiếp cạnh `lớp` và `ranh giới`. Ngoài ra nên nhắc giải thích ngắn `"giao diện lập trình (API)"` ngay tại `L07:31` khi dùng lần đầu (hiện tới `L13:194` mới mở ngoặc).
3. **Làm rõ so sánh `L11:257` (`recap#1`)**: viết `"xác suất lọt từ 10% (0,1) xuống 0,1% (0,001 — giảm 100 lần)"` để người mới dễ theo dõi phép chia `0,1 / 0,001 = 100` (tránh nhầm với `1000` lần so với `0` lớp).
4. **Giảm mật độ ngoặc đơn dày đặc trong `labs/sar/L*/de.md`** (`L00, L02, L03, L06, L07, L08, L10, L11/de.md:3`): tách thành gạch đầu dòng (Dữ liệu đầu vào / Yêu cầu / Quy ước làm tròn / Khuôn mẫu đầu ra).
5. **Độ dài bài hành trình `L13`**: hiện `2732` từ (`991.9s` ≈ `16.53` phút), vượt nhẹ trần quy ước `2300` từ trong `BRIEF_WP4.md` (có thể gọt bớt câu trùng lặp ở `check`/`quiz` hoặc ghi nhận ngoại lệ bài hành trình 5 chặng).
6. **Đồng bộ `audit/sar/af2/upgrade_sar.py`**: cập nhật bộ sinh nguồn khớp với mọi sửa đổi `de.md`, `loi_giai.py`, `practice#0`, `covers`, `Hai mức quy mô` và chạy lại `screen_code.py` nếu thay đổi khối mã/văn bản khối.
