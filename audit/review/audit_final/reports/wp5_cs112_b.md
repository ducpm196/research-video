# WP5 — CS112 nửa B (L15–L29) lên chuẩn AF2

## Tiến độ
- XONG 15/15 bài: **L15–L29** (phiên 1: L15–L26; phiên 2: L27–L29). Mỗi bài: `af2: true` + `covers`, quy mô đo thật (cảnh `scale`, hoặc cảnh đã có sẵn trong bài ở L26, L27, L29), cảnh `practice` + lab chạy thật qua `labs/cham.sh`, P1 tại chỗ, lint 0 FAIL 0 WARN, render 0 vấn đề, sổ screen_code có khối kết quả practice + nguồn `Lxx_lab`, `verify_cs112_af2b.py` PASS.
- Lời đọc (số từ `say`): L15 1871 · L16 1757 · L17 1833 · L18 1798 · L19 ~1990 · L20 1958 · L21 1951 · L22 2083 · L23 2298 · L24 2272 · L25 1795 · L26 2237 · L27 1790 · L28 ~2230 · L29 2273 (đều ≤ 2 300).

## Công cụ riêng của nửa B (không đụng nửa A)
- `audit/cs112/af2b_calc.py`: hàm đếm/đo tất định cho cảnh quy mô (LCG cố định, không đo giờ); `checks:` của bài gọi bằng `__import__('runpy').run_path('audit/cs112/af2b_calc.py')[...]`.
- `audit/cs112/gen_labs_b.py`: sinh `labs/CS112/L15…L26` qua `audit/labkit.write_lab`; `mong_doi.txt` = đầu ra THẬT khi chạy lời giải.
- `audit/cs112/verify_cs112_af2b.py`: tính lại độc lập số của cảnh quy mô và đầu ra từng lab bằng cách KHÁC (vét cạn, đệ quy, sympy, Floyd–Warshall, định lý ma trận–cây Kirchhoff, quy hoạch động…); không đụng `verify_cs112.py`.
- Bài sinh từ mẫu (L17, L18, L21, L23–L26): sửa MẪU `audit/cs112/src/Lxx_*.tpl.yaml`, điền lại bài bằng script riêng (hình đã rút ra từ bài hiện có, round-trip khớp byte trước khi sửa; `asr_reviewed` nằm trong mẫu). Bài không có mẫu (L15, L16, L19, L20, L22): sửa trực tiếp YAML.
- Sổ `audit/review/screen_code/CS112.yaml`: chỉ THÊM khối `CS112 Lxx practice n 0` (kind output, of `src:CS112:Lxx_lab`) và nguồn `Lxx_lab`; không sửa mục nào có sẵn. Bài mới không thêm khối mã Python trên màn hình ngoài khối kết quả lab. Không sửa `symbols.CS112.yaml`, `lexicon_vi.CS112.yaml`, `curriculum/cs112.yaml` (lộ trình L15–L26 không khai `objectives:`; không cần đồng bộ).

## Chi tiết từng bài (cảnh quy mô: số đo thật, ghi "số minh hoạ" khi giả định tốc độ)
- **L15 nhánh cận TSP**: cây đầy đủ 13 700 / 1,1·10^8 / 3,6·10^12 / 3,3·10^17 nút (8/12/16/20 thành phố) so với 38–90 / 121–394 / 1 603–5 930 / 308–6 016 nút nhánh cận (ba ma trận giả lập mỗi cỡ); giá phải trả: phụ thuộc dữ liệu, UB/LB khi hết giờ. Lab: 4 thành phố, LB 22 < tối ưu 27. P1: "chu trình", "vét cạn".
- **L16 tham lam cái túi**: số so sánh n(n−1)/2 · sắp xếp trộn (đếm thật) · n! ở n = 10 / 1 000 / 100 000 (45 / 21 / 3 628 800; 499 500 / 8 728; 5·10^9 / 1 536 555); đánh đổi: đống khi chỉ lấy k món. Lab: phân số chính xác, 0/1 tham lam 59 < tối ưu 72. P1: "n!", "cái túi 0/1", "vét cạn".
- **L17 xếp lịch**: 2^n tập con (2 048 … 1,2·10^18) vs so sánh sắp xếp trộn đo thật (26 … 18 673 837); phản ví dụ có giá thuê (2 vs 100): đổi mục tiêu phải đổi thuật toán. Lab: ba tiêu chí + vét cạn trên 9 sự kiện (4 / 3 / 2 / 4). P1: "tập con", "phản ví dụ", "vét cạn".
- **L18 quy hoạch động**: lời gọi F(n): 2 692 537 / 331 160 281 / 4,1·10^10 / 7,6·10^16 so với 59…159 (ghi nhớ) và n−1 phép cộng; đổi tiền 1,3,4: 229 970 lời gọi so 71; giới hạn ngăn xếp (RecursionError ở F(2000), đo thật) và bộ nhớ bảng. Lab: đổi tiền 1,4,6, các a mà tham lam sai (8, 9, 14, 15, 20), 3 053 / 53 lời gọi.
- **L19 QHĐ theo đoạn**: lần thử chỗ cắt (n³−n)/6 đếm thật (20 … 166 666 500) vs Catalan (14 … 1,0·10^15); n ×10 → thời gian ×1 000, bộ nhớ ×100. Lab: 6 ma trận → 570 phép nhân, ngoặc ((A1 ((A2 A3) (A4 A5))) A6), 42 cách. P1: "truy vết", "vét cạn".
- **L20 LIS/LCS**: 2^n dãy con vs n(n−1)/2 so sánh (28 … 499 500; 5·10^9 ở 10^5); LCS 10^6 / 10^8 / 10^10 ô (4 triệu … 40 tỉ byte) và hướng giảm bộ nhớ (hai hàng; chia đôi kiểu Hirschberg, kiểm bằng cài đặt thật trong verify). Lab: LIS 5 qua 4 7 8 11 12, LCS THUAT.
- **L21 QHTT hai biến**: 6 giao điểm của xưởng bánh (4 hợp lệ + 2 giả); C(2n, n) giao điểm (6 … 1,2·10^17) và thời gian 0,2 giây / 13 ngày / 10^5 năm; giới hạn: cần cách đi từng bước. Lab: 13 cặp, 5 đỉnh, tối ưu 45/2, chứng chỉ y1 = 3/2, y2 = 1/2. Mục tiêu 1, 2 đổi lời ("Mô tả…", "Nhìn…") cho khớp cảnh dạy (E51).
- **L22 đơn hình**: lần xoay đo thật trên LP ngẫu nhiên (2–2 … 6–10) so với 252 … 1,2·10^17 giao điểm; khối Klee–Minty: Dantzig 15 / 31 / 1 023 = 2^n − 1 lần xoay (đo), chỉ-số-nhỏ 9 / 15 / 177; giá phải trả: tệ nhất vẫn mũ. Lab: 2 lần xoay, z = 21 tại (3, 3/2); Klee–Minty n = 4. Tên Klee/Minty chỉ hiện trên màn hình (lint cảnh báo phát âm; chưa dò ASR).
- **L23 sắp xếp nhanh**: so sánh đo thật mảng ngẫu nhiên / đã sắp / cận dưới ở n = 1 000, 2 000, 100 000 (11 015 / 499 500 / 8 530 … 2 017 091 / 5·10^9 / 1 516 705); đã sắp đệ quy sâu n−1 tầng → RecursionError từ n = 2 000 (đo thật), ngẫu nhiên n = 10^5 chỉ sâu 39 tầng. Lab: phân hoạch 7 so sánh, 13 (sâu 3) và 28 (sâu 7), cận dưới 16, sắp xếp đếm.
- **L24 đường đi ngắn nhất**: lần nới cạnh đo thật: ngẫu nhiên 1 000/5 000 → 4 967 (Dijkstra) vs 50 000 (Bellman–Ford dừng sớm); chuỗi 1 000 đỉnh cạnh ngược → 999 vs 998 001; 10^5 đỉnh → 10^10 (công thức). Lab: đồ thị cạnh âm (Dijkstra d[A] = 2, Bellman–Ford 1), chu trình âm. Tên Dijkstra/Bellman/Ford vẫn nói như bài cũ (không thêm tên mới vào lời đọc).
- **L25 cây khung nhỏ nhất**: số cây khung n^(n−2) (10^8 / số 197 chữ số / 739 chữ số) vs so sánh sắp cạnh đo thật (196 / 54 624 / 637 269) và bước hợp–tìm (7 / 547 / 1 444); hợp–tìm trên chuỗi xấu nhất: không mẹo n(n−1)/2 (499 500) vs 998 (gắn nhỏ vào lớn); ghi rõ nén đường chưa thêm lợi ở phép thử này. Lab: 130 cây khung, nhỏ nhất 20. Tên Kruskal/Prim/Cayley chỉ hiện trên màn hình.
- **L26 P/NP**: giữ cảnh quy mô cũ (19! ≈ 4 năm; bảng số bit của W), thêm lab: |tập độc lập| + |phủ đỉnh| = 7, kiểm chứng chỉ duyệt 9 cạnh, cái túi 0/1 W = 14 và 14 000 (90 → 84 006 ô trong khi số bit 4 → 14).

## Cổng cuối phần (chạy trên cả khoá CS112, gồm nửa A của tác tử khác)
Xem mục "Kết quả cổng" ở cuối (điền sau khi chạy).

## Phiên 2: L27, L28, L29
- **L27 bài tập lớn**: giữ cảnh `intuition`/`measure` (số đo thật của báo cáo BTL) làm quy mô; thêm `covers` (mục tiêu 4 đổi "Viết nhật ký" → "Ghi nhật ký" cho khớp cảnh dạy), mục tiêu 5 và lab `mini_btl`: bốn chiến lược (bảng, ghi nhớ, vét cạn, tham lam) trên 7 ma trận p = (22, 9, 18, 24, 20, 16, 27, 13): 20 709 phép nhân, 56 lần thử, 113 và 729 lời gọi, tham lam lệch 30,6%, vét cạn n = 9 gọi 6 561 lần. P1: "giao diện", "trung vị" giảng tại chỗ. Lab không ghi sẵn công thức 3^(n−1).
- **L28 tổng ôn**: thêm cảnh `scale` (hàm ví dụ n·log₂ n đếm thật 10 240 / 229 376 / 2 228 224 so với vòng lặp đôi mọi cặp n(n−1)/2: 523 776 đếm thật; 1,3·10^8 và 8,6·10^9 theo công thức; 2 mili giây so với 8,6 giây, số minh hoạ) và lab `tong_on`: ba hệ thức truy hồi (3T(n/2)+n, 2T(n/2)+n², T(n/2)+1) kiểm bằng tỉ số với hàm chuẩn người học tự chọn từ định lý thợ (đề không ghi g), và bẫy tham lam đổi 12 với 1, 6, 10 (3 đồng so với 2). Mục tiêu 3 đổi "Đọc thuộc lòng" → "Nhớ" (E51: không phải kỹ năng LÀM).
- **L29 Timsort**: CẮT 3 125 → 2 273 từ lời đọc: bỏ câu thừa, giữ mọi con số trên màn hình (kiểm bằng `checks` sẵn có). Các điểm cắt (lời đọc, màn hình vẫn hiện): hook (câu "lỗi có mặt cả ở ngôn ngữ gốc"), ôn bài 13 ví dụ log₂ 3!, ví dụ bất biến 30-20-10 ở bảng thuật ngữ, câu mở đầu của intuition/mechanism, 2 câu số đo ngẫu nhiên ở chặng 1 (19 458 756 / 19 606 028), ví dụ bit của minrun 2112, ngưỡng đoạn nhỏ 64→32 và ghi chú tương thích ở chặng 2, ba bước tính ngăn xếp ở chặng 2, hai câu về chú thích mã và công cụ chứng minh ở chặng 3, các bước 2–3 của "sức chỗ nối" và hai bước cuối của ví dụ 315 phần tử ở chặng 4–5, bài học sai số 3 và 5 (đã xoá hai hàng khỏi bảng, đánh số lại 1–3), một nửa lời giải câu hỏi quyết định, phần lặp của recap. Không tách bài, không đánh số lại. Thêm `covers` và lab `timsort_mo_phong` (minrun 1000 / 4097 / 5000 → 63 / 33 / 40, số đoạn 16 / 125 / 125, bản cũ hỏng bất biến [171, 119, 59, 55], bản sửa gộp [404]). Mục tiêu 3 đổi "Chọn giữa…" → "Cân nhắc giữa…", thêm mục tiêu 4; đồng bộ `curriculum/cs112.yaml` (Edit nhỏ trên dòng `objectives` của L29).
- Sửa theo bài học của người đọc CS112 A (reports/R_WP5_CS112_A.md): các cảnh mới không có mã trên màn hình (không rủi ro mã sai luật); lab L27/L28 không ghi công thức đóng; tiêu đề cảnh `scale` L19 khớp hàng bảng (5, 10, 20, 30, 1 000); số trong `say` không dùng nhóm có dấu cách (quét tự động L15–L29: 0 chỗ); L19 giải thích công thức (n³−n)/6; L28 giải thích "vòng lặp đôi".

## Sửa theo reader (reports/R_WP5_CS112_B.md; đọc 15/15 bài: MUST 1, P1 = 2 ở 11/15, SHOULD 9)
Đã sửa TOÀN BỘ MUST, mọi bài P1 = 1 và mọi SHOULD có thể sửa:
- **MUST L26** (practice, lời đọc): "tăng đúng 1000 lần" → "gần 1000 lần, khoảng 933 lần" (84 006 / 90 = 933,4). Sửa ở mẫu L26.
- **L15**: hai bước mới trong cảnh `branch` hiện ma trận con của nút 1→4 (không rút gọn thêm, cận 25) và nút 1→3 (cột 1 trừ 11, R[1][3] = 30 − 10 − 3 = 17, cận 53); lab thêm mục 5 và hai dòng `Nut con 1->2: 22`, `Nut con 1->3: 28` (tính từ ma trận 4 thành phố của lab), `verify_cs112_af2b` L15f/L15g kiểm bằng `tsp_bb.child` và vét cạn đường đi qua nút con. Mục tiêu 5 thêm "cận của hai nút con". Sổ screen_code đã làm mới khối practice L15 (ledger_refresh).
- **L20**: `de.md` ghi rõ vét cạn dùng tập con KHÁC RỖNG (kích thước 1..n, số tập con đã thử 2^n − 1 = 1023); pitfalls lỗi 2 có ví dụ dãy 1, 2, 3, 0 (L = 1, 2, 3, 1; đáp số 3) cả trên màn hình và lời đọc, kèm `checks`.
- **L18, L27, L28**: đọc "(n cộng một)" thành cụm rõ: "F của chỉ số n cộng một", "T của chỉ số n cộng một", "2 mũ với số mũ là n cộng một", "n nhân tổng n cộng một" (L27 `intuition`); L23 cũng đổi "2 nhân tổng n cộng một, nhân H n".
- **L22**: bỏ tên Dantzig khỏi lời đọc, "được đề xuất năm 1947" (tên còn trên màn hình); sửa cả mục `asr_reviewed` tương ứng.
- **L25**: "vài chục đến vài nghìn bước" → "từ 7 bước tới khoảng một nghìn bốn trăm bước" (bảng 7 / 547 / 1 444).
- **L23 (P1)**: giảng "hoán vị" (một thứ tự của n số, trung bình trên mọi hoán vị), "kỳ vọng" (trung bình qua nhiều lần chọn chốt ngẫu nhiên), và nói rõ công thức C(n) = 2(n + 1)H_n − 4n KHÔNG suy ra ở đây (cần hệ thức truy hồi riêng, máy kiểm n ≤ 7). Bù lời đọc: bỏ ví dụ Θ ở prereq (và mục asr_reviewed), câu cuối của `idea`, câu "toàn số bằng nhau" ở `cost` (màn hình vẫn hiện).
- **L27 (P1)**: prereq thêm bước ôn ba thuật ngữ: tham lam (bài 16), ghi nhớ từ trên xuống (bài 18, F(40): hơn 331 triệu lời gọi còn 79), vét cạn (bài 15, 17; 2^11 = 2048), kèm `checks`.
- **L28 (P1)**: prereq thêm bước ôn bốn từ của bài 8–14 (thế ngược, quy nạp và phần dư R(n), khe hở, quay lui) kèm ví dụ số và `checks` (R(n) = n − c·n kiểm bằng số); thêm `factorial` vào `assumes`. Bù lời đọc: gọn đoạn mô tả cây ở `intuition`, bỏ một câu ở `verify`.
- **L29 (P1)**: prereq thêm hàng "hệ hai": bit, `n >> 1` = n chia 2 bỏ phần dư, `n & 1` = số dư, 2112 = 100001000000 = 2048 + 64, kèm `checks`; lời đọc thêm hai câu (không đọc ký hiệu). Bù: bỏ câu mốc 2015/2021 ở `intuition` và câu "ngăn xếp chỉ giữ một bất biến" ở chặng 4.
- Lời đọc sau sửa: L15 2004 · L18 1801 · L20 1975 · L22 2082 · L23 2260 · L25 1799 · L26 2240 · L27 1870 · L28 2278 · L29 2269 (đều ≤ 2 300).
- Không sửa: hai mục "chưa kiểm được nguồn" của reader (số đo trích từ báo cáo BTL ở L27; "300 dãy, 300 cặp xâu" ở L20) — số đã được `verify_cs112_p2.py`/báo cáo BTL kiểm; video MP4/SRT cũ (phải dựng lại, ngoài phạm vi).

Cổng chạy lại sau "Sửa theo reader" (cả khoá CS112): `lv.py lint` 0 FAIL 0 WARN cho L15, L18, L20–L29; `lv.py render` 0 vấn đề cho 10 bài đổi (L15, L18, L20, L22, L23, L25–L29); `lv.py curriculum` 30 bài 0 lỗi; `check_curricula_graph` 0 lỗi; `test_e52` 0 FAIL; `lab_gate CS112` 30 PASS · 0 FAIL; `screen_code check --course CS112` 94 khối, PASS 141, 0 FAIL/STALE/MISSING/ORPHAN; `arith_scan` 243 phép 0 FAIL; `verify_cs112_af2b` PASS (thêm L15f, L15g).

## Còn lại / đề xuất
- Không còn bài chưa nâng trong L15–L29. Đề xuất cho người điều phối: dựng lại cả khoá (câu `say` mới/đổi; mọi video CS112 L15–L29 sẽ STALE), rồi chạy ASR; tên riêng Klee/Minty (L22), Kruskal/Prim/Cayley (L25) chỉ hiện trên màn hình vì chưa dò ASR.
- Chưa có người đọc độc lập cho L15–L29; `asr_reviewed` cho câu mới chưa có; chưa thêm mục `term:` E52 (test không đòi).
- L29 còn sát trần (2 273/2 300): nếu thêm nội dung phải cắt tiếp; điểm cắt kế tiếp đề xuất: một trong năm chặng (chặng 4 hoặc 5) chuyển thành bài mở rộng riêng ĐẶT CUỐI khoá nếu cần (không tự tách).

## Kết quả cổng cuối phần (phiên 2, 2026-11-14, cả khoá CS112 gồm nửa A)
- `tools/lv.py curriculum curriculum/cs112.yaml`: 30 bài, 30 có đặc tả, 0 lỗi.
- `audit/check_curricula_graph.py`: tham chiếu hỏng 0, chu trình 0, VER không PASS 0, ví dụ chữ số thiếu VER 0.
- `python tests/test_e52.py`: 0 FAIL.
- `audit/review/lab_gate.py CS112`: 30 PASS · 0 FAIL (L00–L29).
- `audit/review/screen_code.py check --course CS112`: 94 khối, PASS 141 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0.
- `audit/review/arith_scan.py`: 243 phép tính, 0 FAIL.
- `audit/cs112/verify_cs112_af2b.py`: PASS (L15a–L29b, 0 lỗi).
- Mỗi bài L15–L29: `lv.py lint` 0 FAIL 0 WARN, `lv.py render` 0 vấn đề (L19, L28 dựng lại sau khi sửa lời). Xem PNG tay: L15, L16, L17, L22, L25 (phiên 1); L27–L29 chỉ qua render máy.
- Bẫy kỹ thuật: heredoc Bash của công cụ đổi hai dấu gạch ngược thành một (từng làm lệnh to thành ký tự TAB và lệnh frac thành formfeed ở L16; đã sửa, quét ký tự điều khiển sạch). Soạn tệp có LaTeX bằng Write/Edit.
