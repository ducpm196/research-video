# Kế hoạch AF6 — Sửa cho đúng thực chất, dựng lớp thực hành thật và web lộ trình tương tác

- Ref: `AF6` · Mốc giờ: `2026-11-27T16:08Z` · Mốc git: `a3039c1f` (`update v6.1`)
- Bộ ba cùng mốc: tệp này, `knowledge-graph_AF6_20261127T1608Z.md`, `handover_AF6_20261127T1608Z.md`
- Phạm vi lượt này: CHỈ rà soát và lập kế hoạch. Không sửa bài, lab, video, công cụ, cổng; không commit. Thực thi ở phiên sau.
- Đích của kho (người dùng nêu 2026-11-27): **từ con số 0 tới năng lực nền của kỹ sư senior về công nghệ thông tin, khoa học máy tính, trí tuệ nhân tạo, khoa học dữ liệu**; ngoài video phải có **web tương tác theo bản đồ lộ trình, tích hoàn thành từng bước, có phần thưởng từ mục nhỏ tới mục lớn**.
- Kế hoạch này THAY `plan_AF5_20261123T0110Z.md` cho mọi việc còn lại. Phần AF5 đã làm được giữ nguyên trừ các điểm nêu ở mục 2.
- Chứng cứ: mọi con số dưới đây có lệnh và đầu ra trong `audit/review/audit_final/logs/af6/` (gọi tắt `af6/`). Nhãn: OBSERVED = tôi chạy/đọc trong lượt này; CITED = trích báo cáo của tác tử đọc (kèm tệp); INFERRED = suy luận, chưa kiểm.

---

## 1. Kết luận rà soát

**Trạng thái kho: `PARTIAL`.** Tuyên bố "53/53 khoá ĐÃ CHỐT, 806/806 bài 0 lỗi bắt buộc sửa" của `handover_AF5_final_20261127.md` **không đứng được** (`FAILED`), dù bộ cổng máy đạt thật.

| Tuyên bố của bản bàn giao AF5 | Kết quả kiểm lại | Nhãn |
|---|---|---|
| Bộ cổng nhanh 0 cổng trượt | Đúng: chạy lại tại `a3039c1f`, 0 cổng trượt (`af6/gates_nhanh.out`) | OBSERVED, VALID |
| 806 video tươi, khớp giáo án | Đúng: `TOTAL_STALE=0`, `pack check` 806 bài, 0 vấn đề, 10 474,9 phút | OBSERVED, VALID |
| Bộ chấm lab chống in cứng | Đúng trên mẫu: 179/179 lời giải đạt, 179/179 bài in cứng bị trượt (`af6/p5_mutation.out`) | OBSERVED, VALID |
| Đọc độc lập 806/806 bài, 0 lỗi bắt buộc sửa | **Sai.** Mẫu K (hạt giống 611, 32 bài, 4 người đọc mới): 31 bài lớp B, C và khoá mới có **48 lỗi bắt buộc sửa ở 26/31 bài**; hồ sơ `read_af5` ghi 0 cho cả 32 bài. Bài lớp A duy nhất trong mẫu (`JV2 L09`): 0 lỗi | CITED (`af6/sample_k/K1..K4.md`); tôi kiểm lại 7 lỗi bằng lệnh, đều đúng |
| Cảnh Tự làm hết khuôn mẫu | **Sai.** Khuôn cũ bị thay bằng khuôn mới: 378 bài có ≥ 50% lời cảnh Tự làm dùng chung câu với ≥ 20 bài khác (`af6/p2_repeat_sentences.out`) | OBSERVED |
| Lab đạt chuẩn | **Chỉ đạt về hình thức.** 443/806 lab là bài tính công thức (Python ≤ 12 dòng, chỉ thư viện chuẩn); chặng 8–11: 368/429 (`af6/p6_lab_by_stage.out`) | OBSERVED |
| Âm thanh đã kiểm bằng máy, 0 câu chưa xem | **Không có giá trị chứng cứ.** 5 359/5 706 mục "đã xem" là lý do sinh tự động (`af6/p7_asr_whitelist.out`); người dùng nghe 15 câu ngày 27/11, 5 câu phải sửa | OBSERVED |

### 1.1. Học ngay được chưa

| Phần | Số bài | Khuyến nghị | Căn cứ |
|---|---:|---|---|
| Chặng 1–5 phần soạn tay (`FND`, `JVA`, `JV2`, `PYT`, `BNK`, `BNX`, `INT`, `ACB`, `DMS`, `CS112`, `CS115 L00–L21`, `L44–L46`) | 196 | **Học ngay được.** | 120 bài không đổi lời đọc so với mốc đã rà `5d7f329`; 76 bài đổi nhỏ (trung vị +32 từ) (`af6/p4_before_after.out`). Bài đổi nhiều nhất (`JV2 L09`) được đọc lại: 0 lỗi bắt buộc sửa, dựng lại được cả dự án từ mã trên màn hình (CITED K4). Lưu ý: lab lớp A không có ca ẩn nên bài in cứng vẫn đạt |
| Chặng 6–11 lớp C (34 khoá + `CS115 L22–L43`) | 536 | **Xem phần giảng được, nhưng coi chừng câu cuối mỗi đoạn lời; bỏ qua phần Tự làm.** 11/16 bài mẫu có lỗi bắt buộc sửa (13 lỗi). | 16/16 bài mẫu: số liệu và mã trên màn hình đúng khi tính/chạy lại; lỗi nằm ở câu nối thêm và ở lab (CITED K1, K2) |
| `CPR`, `LNX`, `MLP`, `PRJ` (viết lại) | 45 | **Chưa nên học** (gồm cả 5 dự án chặng `PRJ L00–L04` nằm trong Chặng 1–5: tạm bỏ qua). | 8/8 bài mẫu có lỗi bắt buộc sửa, 18 lỗi (CITED K3) |
| `SPB`, `BEP`, `AIP` (mới soạn) | 29 | **Chưa nên học.** | 7/7 bài mẫu có lỗi bắt buộc sửa, 17 lỗi. `SPB` dùng công cụ thật (Spring Boot 4.1.3, Maven, Docker chạy được) nhưng mã được dạy có lỗi đo được; `BEP`/`AIP` là bài đúc khuôn, lab không cài thứ mà tên bài nêu (CITED K4; tôi kiểm lại `BEP L06`) |

Bắt đầu học Chặng 1 ngay hôm nay là an toàn. Kế hoạch dưới đây sửa theo đúng thứ tự người học đi tới, luôn đi trước người học ít nhất một chặng (quyết định `D-9`).

### 1.2. Sáu nguyên nhân gốc

| Mã | Nguyên nhân | Số đo (OBSERVED trừ khi ghi khác) |
|---|---|---|
| RC-1 | **Cổng độ dài tối thiểu tạo ra câu độn.** Kế hoạch AF5 (do tôi viết) đặt sàn 1 300 từ / 9 phút. Đợt thực thi đáp ứng bằng cách nối câu vào cuối đoạn lời. | 7 934 câu, 198 664 từ thêm vào 614 bài ngoài cảnh Tự làm; 343 bài có ≥ 10 câu; 1 490 câu vừa nằm cuối đoạn vừa không chung từ nào với màn hình, ở 336 bài; 153 câu trong đó dùng từ tuyệt đối ("hoàn toàn", "luôn", "dứt điểm") (`af6/p8_tail_sentences.out`). Trước đợt thực thi 80 bài dưới 1 300 từ; nay bài ngắn nhất trên 1 600 từ |
| RC-2 | **Khuôn Tự làm mới thay khuôn cũ.** Danh sách cấm `boiler_deny.txt` chỉ chứa câu của khuôn cũ. | 9 câu xuất hiện ở ≥ 100 bài; câu "Hãy bảo đảm chương trình của bạn xử lý đúng cả dữ liệu mẫu lẫn hai bộ dữ liệu kiểm ẩn…" ở 514 bài |
| RC-3 | **Lab không rèn kỹ năng của bài.** Bộ chấm chỉ so đầu ra chuẩn nên bài làm né đúng kỹ năng vẫn đạt. | Lời giải trung vị 9 dòng; 290 lab chỉ in 1 dòng; lab của bài Docker (`LNX L08`) không có lệnh `docker` nào; 6/8 lab lớp B đạt với bài làm né kỹ năng (CITED K3); 2 ca ẩn chấm sai bài đúng vì rơi điểm giữa làm tròn (`BCH L08` tôi kiểm lại, `IRS L00` CITED K2) |
| RC-4 | **Người đọc của đợt thực thi chấm quá nhẹ.** 806 báo cáo có nội dung riêng (không phải khuôn), nhưng 0 dòng mức bắt buộc sửa trên 806 bài. | 422/806 báo cáo chấm điểm tối đa; 1 607 dòng "nên sửa" (`af6/p1_read_reports.out`). Mẫu K: cùng 32 bài, người đọc mới ra 48 lỗi bắt buộc sửa |
| RC-5 | **Cổng phát âm bị vô hiệu bằng duyệt tự động.** | 1 432 câu có độ giống dưới 0,80 (161 câu dưới 0,70) được ghi "đã xem" với lý do sinh sẵn |
| RC-6 | **Nhãn chất lượng không gắn chứng cứ riêng.** 53 dòng `quality.yaml` cùng một câu chứng cứ. | `grep -c 'ĐÃ CHỐT' quality.yaml` = 54 |

Bài học thiết kế: mọi cổng có thể đạt bằng cách **thêm chữ** hoặc **thay khuôn** đều sẽ bị đáp ứng theo cách đó. Kế hoạch này bỏ mọi cổng kiểu sàn số lượng, và mỗi cổng mới đi kèm một mẫu đối chứng do người đọc khác chấm (mục 5).

---

## 2. Cái gì của AF5 giữ, cái gì đổi

| Hạng mục AF5 | Xử lý |
|---|---|
| Dãy 11 chặng nguyên khoá, `next:`, 0 cạnh ngược (`check_next_refs` 593 lời hẹn, 0 lệch) | GIỮ |
| `cham.sh` bản 2, `labs/CONTRACT.yaml`, ca ẩn, chế độ dự án | GIỮ, bổ sung kiểm chất lượng ca ẩn và kiểm kỹ năng (WP-3) |
| Khoá bộ sinh bài (`_frozen.py`, `test_frozen` 56/56) | GIỮ |
| Ba khoá mới `SPB`, `BEP`, `AIP` | `SPB`: GIỮ dự án và công cụ, sửa mã dạy sai và nối 13 lab thành một dự án lớn dần. `BEP`, `AIP`: GIỮ giáo án, VIẾT LẠI bài và lab (lab phải cài đúng thứ tên bài nêu) |
| Cổng `G-LEN` (sàn 1 300 từ, 9 phút) | **BỎ** |
| Cổng `G-BOILER` theo danh sách cấm tĩnh | **THAY** bằng cổng đo câu lặp giữa các bài (`G-REPEAT`) |
| Điều kiện chốt "đọc độc lập 100%" | **THAY** bằng quy trình đọc có hiệu chuẩn và mẫu đối chứng (mục 5.2) |
| Nhãn `ĐÃ CHỐT` 53/53 | **GỠ**, thay bằng nhãn ba trục (mục 5.1) |
| Cảnh Tự làm trong video là nơi dạy thực hành | **ĐỔI**: thực hành chuyển sang lớp lab trên web; video chỉ giữ một thẻ giao việc ngắn, đúng sự thật (`D-3`) |
| `HOC_TAP.html` một tệp tĩnh | **NÂNG** thành web lộ trình (WP-4); bản tĩnh giữ làm dự phòng cho tới khi web mới đạt nghiệm thu |

---

## 3. Quyết định đã chốt (theo uỷ quyền "toàn quyền quyết định hướng đi" ngày 2026-11-23, áp dụng tiếp cho lượt này)

| Mã | Quyết định | Lý do ngắn |
|---|---|---|
| D-1 | Sự thật trước: gỡ nhãn `ĐÃ CHỐT`, dùng nhãn ba trục theo từng bài (Bài giảng · Thực hành · Âm thanh). | Một nhãn gộp che mất chỗ yếu; người học cần biết bài nào chỉ nên xem, bài nào làm lab được |
| D-2 | Câu thêm sau mốc `5d7f329` ở cảnh không phải Tự làm: **mặc định xoá**, chỉ giữ khi người đọc xác nhận câu đó bám màn hình, đúng, và không tuyệt đối hoá. | Thân bài trước khi độn đã được kiểm đúng; xoá rẻ và an toàn hơn sửa từng câu |
| D-3 | Thực hành hai tầng, tách khỏi video. Tầng 1 "Luyện nhanh": lab nhỏ hiện có, sửa cho đủ đề và ca kiểm. Tầng 2 "Lab nghề": lab dùng công cụ thật của nghề, 3–5 lab mỗi khoá và một dự án mỗi chặng; nội dung nằm ở `labs/` và hiển thị trên web. | Lab viết bằng chữ sửa nhanh, không phải dựng lại video; hết động cơ sinh khuôn trong video |
| D-4 | Dựng web lộ trình cục bộ: trang tĩnh không cần bước dựng, chạy qua máy chủ nhỏ viết bằng thư viện chuẩn Python, tiến độ lưu thành tệp trên máy người học. | Chấm lab thật được từ web; không phụ thuộc dịch vụ ngoài; bền lâu dài |
| D-5 | Phần thưởng chỉ trao cho việc có bằng chứng (xem đủ video, trả lời trước khi xem đáp án, lab được bộ chấm xác nhận). | Phần thưởng phải đẩy người học làm việc thật, không phải bấm tích |
| D-6 | Quy trình đọc độc lập bản 2: người đọc phải qua bài hiệu chuẩn có cài lỗi; mỗi khoá chốt bằng mẫu đối chứng do người đọc khác nhóm chấm. | RC-4 |
| D-7 | Phát âm: sửa từ điển đọc theo kết quả nghe của người dùng; hàng nghe ưu tiên theo rủi ro; nút "báo lỗi phát âm" ngay trong trình xem bài. | RC-5; người dùng đang tự nghe |
| D-8 | Không soạn thêm bài giảng mới cho tới khi chặng tương ứng đạt nhãn; ngoại lệ duy nhất là lỗ hổng nằm trên đường học chính (mục 8). | Tránh lặp lại việc mở rộng trước khi chắc |
| D-9 | Thứ tự làm theo đường người học đi: Chặng 1 → 11; mỗi chặng sửa trọn (lời đọc, thẻ giao việc, lab, phát âm) rồi mới sang chặng sau. | Người học bắt đầu ngay; luôn có một chặng đã sửa xong phía trước |
| D-10 | Mỗi bài chỉ dựng lại video **một lần**: gom sửa lời đọc + thẻ Tự làm + từ điển đọc rồi mới dựng. | Dựng 806 bài tốn khoảng 16–24 giờ máy (CITED `repo_review_20261127.md`: 526 bài trong 56 840 s) |
| D-11 | Tệp `nghe_thu_ket_qua.json` là của người dùng (đang ghi trong lúc rà soát): phiên thực thi chỉ đọc, không ghi đè, không đụng chỉ mục git. | Quan sát 2026-11-27 22:53 +07: tệp đổi và được đưa vào chỉ mục khi tôi không thao tác |
| D-12 | Commit: người dùng tự commit (các bản `v5.1`, `v6`, `v6.1`). Phiên thực thi hỏi một lần lúc bắt đầu; nếu không được phép thì lưu phần thay đổi của từng gói việc thành tệp vá. | Quy tắc sẵn có |

---

## 4. Sổ điểm nghẽn hợp đồng

Trạng thái mọi dòng: `OPEN` (mở 2026-11-27). Cột cuối là gói việc đóng nó.

| ID | Chưa xác định / chưa kiểm | Việc phụ thuộc | Chứng cứ còn thiếu | Hệ quả nếu để | Phép đóng | Đóng ở |
|---|---|---|---|---|---|---|
| BN6-01 | Câu thêm sau `5d7f329` đúng hay sai chưa ai kiểm từng câu | Mọi bài lớp B, C | Phán quyết giữ/xoá cho 7 934 câu | Người học nghe khẳng định sai | `tail_review.py --check`: 0 câu chưa có phán quyết; mẫu đối chứng 0 lỗi bắt buộc sửa do câu thêm | WP-2 |
| BN6-02 | Thẻ Tự làm trong video ghi "Mục tiêu" là mục tiêu của bài chứ không phải việc của lab | 597 bài có ca ẩn | Thẻ sinh từ `de.md` | Người học không biết phải làm gì | `G-TASKCARD`: thẻ = nhiệm vụ + dữ liệu mẫu + đầu ra, lấy từ `de.md`; 0 lệch | WP-3 |
| BN6-03 | Đề lab thiếu định nghĩa vào/ra/làm tròn | 443 lab luyện nhanh | Đề đủ 5 mục | Bài đúng bị chấm trượt; người mất gốc kẹt | `G-DE`: 5 mục bắt buộc có mặt; ví dụ tính tay khớp `mong_doi.txt` | WP-3 |
| BN6-04 | Ca ẩn mỏng: rơi điểm giữa làm tròn, dòng ra là hằng số, biến thể sai vẫn đạt | 597 lab | Bộ biến thể sai cho từng lab | Điểm "đạt" không chứng minh gì | `G-CASE`: ≥ 3 ca; không ca nào cách điểm giữa < 1e-9; không dòng hằng; ≥ 2 biến thể sai có tên đều bị trượt | WP-3 |
| BN6-05 | Bộ chấm chỉ so đầu ra, không kiểm kỹ năng (không heap, không Docker, không khoá vẫn đạt) | Lab nghề, 45 bài lớp B | Bộ kiểm hành vi theo loại lab | Lab nghề vô nghĩa | Lab nghề chấm bằng `kiem/` (kiểm thử thật) hoặc bằng công cụ (valgrind/`docker inspect`/`EXPLAIN`); bài làm né kỹ năng có trong `kiem/ne/` phải trượt | WP-3, WP-5 |
| BN6-06 | Hồ sơ `read_af5` không dùng làm chứng cứ "sạch" được | Nhãn chất lượng | Người đọc đã hiệu chuẩn | Lặp lại "100%" giả | Bài hiệu chuẩn: bắt ≥ 80% lỗi cài sẵn; mẫu đối chứng theo 5.2 | WP-1, WP-9 |
| BN6-07 | 5 359 câu bị gắn cờ phát âm chưa ai nghe | Âm thanh 738 bài | Tai người | Đọc sai thuật ngữ, sai số | Hàng nghe ưu tiên: 100% câu nhóm rủi ro cao được người nghe hoặc được sửa từ điển rồi dựng lại | WP-6 (cần người dùng) |
| BN6-08 | Từ điển đọc sai các từ người dùng đã bắt: `ORA`, `PostgreSQL`, tên cờ lệnh | Mọi bài chứa các từ đó | Danh sách vị trí | Lỗi lặp ở mọi bài dùng từ | `lexicon_regress.py`: mỗi mục `fix` trong `nghe_thu_ket_qua.json` có một dòng trong từ điển và một phép thử | WP-6 |
| BN6-09 | Web mới chưa tồn tại; tiến độ cũ nằm trong `localStorage` khoá `hoc_tap_v2` | Người học đang dùng trang cũ | Bản chuyển dữ liệu | Mất tiến độ đã tích | Phép thử chuyển dữ liệu: trạng thái mẫu `hoc_tap_v2` → nhật ký sự kiện, số bài đã học và lịch ôn giữ nguyên | WP-4 |
| BN6-10 | Chưa có ngân hàng câu hỏi chấm tự động; câu Tự kiểm hiện là tự luận | Bước "Tự kiểm" trên web, cổng chặng | Câu hỏi có đáp án máy kiểm được | Phần thưởng trao theo tự khai | Mỗi bài ≥ 3 câu có đáp án; `quiz_verify.py` tính lại 100% đáp án từ biểu thức kiểm | WP-7 |
| BN6-11 | Đích "nền kỹ sư senior" chưa có định nghĩa đo được | Thứ tự ưu tiên, lab nghề, khoá bổ sung | Ma trận năng lực có bằng chứng đầu ra | Không biết khi nào là đủ | Ma trận mục 8 được người dùng xem; mỗi năng lực có ≥ 1 lab nghề hoặc dự án làm bằng chứng | WP-0 (xem), WP-5, WP-8 |
| BN6-12 | Quyền commit ở phiên thực thi | Điểm quay lui | Câu trả lời của người dùng | Không có mốc quay lui theo gói việc | Hỏi một lần đầu phiên | WP-0 (cần người dùng) |
| BN6-13 | Ba khoá mới và lớp B: mã mẫu trên video có lỗi thật mà lời giải lab đã sửa (`PRJ L01` kẹt khoá, `PRJ L03` O(n²)) | 45 bài lớp B, 29 bài khoá mới (`SPB L05`: xoá đệm trước khi commit làm số cũ sống 35 s; `SPB L10`: tin Kafka vẫn đi khi giao dịch hoàn tác — CITED K4) | Chạy lại mọi khối mã cảnh dạy với ca biên | Dạy mã sai | `screen_code` thêm ca biên do người đọc nêu; 0 khối lệch | WP-2 |
| BN6-14 | Các phép đo `af6/p2`, `p6`, `p8` là dò theo quy tắc, có thể báo thừa hoặc sót | Ước lượng khối lượng WP-2, WP-3 | Đối chiếu với phán quyết người đọc trên 32 bài mẫu | Ước lượng lệch | So `p8_tail_candidates.tsv` với lỗi câu thêm trong `sample_k/`: ghi tỉ lệ bắt được | WP-1 |

---

## 5. Chuẩn chất lượng bản 2

### 5.1. Nhãn ba trục theo từng bài (`quality.yaml` bản 2)

| Trục | Mức | Điều kiện |
|---|---|---|
| Bài giảng | `G0` chưa rà · `G1` máy đạt · `G2` đã đọc có hiệu chuẩn, 0 lỗi bắt buộc sửa | `G2` cần báo cáo của người đọc đã qua hiệu chuẩn, khớp mã băm tệp bài |
| Thực hành | `T0` không có · `T1` luyện nhanh đủ đề + ca kiểm tốt · `T2` tự cài cơ chế (≥ 20 dòng lôgic, có biến thể sai bị trượt) · `T3` công cụ thật, kiểm hành vi · `T4` dự án có bộ kiểm thử | Do máy tính từ `labs/CONTRACT.yaml` bản 3 và kết quả cổng lab |
| Âm thanh | `A0` chỉ máy · `A1` đã sửa theo từ điển và nghe mẫu · `A2` người đã nghe các câu rủi ro cao của bài | Từ `nghe_thu_ket_qua.json` và hàng nghe |

Khoá chỉ được ghi "đạt" khi 100% bài `G2`, mọi bài ≥ `T1`, có ≥ 3 lab `T3` (hoặc `T2` với khoá thuần lý thuyết: `DMS`, `TOC`, `CS112`, `CS115`, `CLC` phần toán), mọi bài ≥ `A1`, và qua mẫu đối chứng. Mỗi dòng nhãn phải trỏ tới tệp chứng cứ riêng (`G-LABEL` chặn hai khoá dùng chung một câu chứng cứ).

### 5.2. Đọc độc lập bản 2

1. **Hiệu chuẩn:** bộ 6 bài có cài 20 lỗi đã biết (lấy từ lỗi thật của Mẫu K và Mẫu H, cài vào bản sao trong `tests/fixtures/calib/`). Người đọc (tác tử hay người) phải bắt ≥ 16/20 và không báo quá 4 lỗi giả mới được chấm `G2`.
2. **Đọc có chạy:** mỗi bài phải kèm lệnh đã chạy cho từng khẳng định định lượng và cho lab: lời giải mẫu, bài in cứng, và ít nhất một bài làm né kỹ năng.
3. **Định nghĩa lỗi bắt buộc sửa** bổ sung ba loại mà đợt AF5 xếp nhẹ: câu khẳng định tuyệt đối sai điều kiện; lời đọc trái với màn hình hoặc với chính bài; cảnh Tự làm/đề lab không đủ để làm bài.
4. **Mẫu đối chứng trước khi ghi nhãn khoá:** người đọc khác nhóm đọc lại ⌈20%⌉ số bài (tối thiểu 3) của khoá; tìm ra ≥ 1 lỗi bắt buộc sửa thì cả khoá quay lại sửa và đọc, tối đa 2 vòng rồi báo `PARTIAL`.

### 5.3. Cổng mới và cổng bỏ

| Cổng | Kiểm gì | Thay cho |
|---|---|---|
| `G-TAIL` | Mọi câu lời đọc có mặt ở HEAD mà không có ở `5d7f329` phải có phán quyết `giu`/`xoa` trong `audit/review/tail_review.tsv`; câu `giu` phải chung ≥ 1 từ nội dung với màn hình của đoạn và không chứa từ tuyệt đối ngoài danh sách cho phép | `G-LEN`, `G-PAD` |
| `G-REPEAT` | Tỉ lệ từ của cảnh Tự làm nằm trong câu lặp ở ≥ 20 bài phải ≤ 20%; ngoài cảnh Tự làm ≤ 5% (số hiện tại: trung vị toàn bài 4,6%, cảnh Tự làm 378 bài ≥ 50%) | `G-BOILER` |
| `G-TASKCARD` | Thẻ Tự làm sinh tất định từ `de.md` (nhiệm vụ, dữ liệu mẫu, đầu ra mong đợi); không có câu gợi ý chung; dữ liệu mẫu trên thẻ giữ nguyên xuống dòng và khi đưa vào lời giải mẫu phải ra đúng đầu ra ghi trên thẻ (Mẫu K: thẻ gộp dòng bằng `;` làm lời giải `AIP L01` ném lỗi) | `G-PRACTICE` |
| `G-SHOW` | Không đoạn nào có `show` rỗng mà không xoá màn hình; khung sáng của bảng trỏ đúng hàng đang đọc (Mẫu K: `CLD L02`, `EVT L03` màn hình chỉ còn ô cũ bị mờ; 5 bài lệch khung sáng một hàng) | — |
| `G-DE` | `de.md` có đủ 5 mục: Nhiệm vụ, Dữ liệu vào, Dữ liệu ra (nghĩa từng dòng), Quy tắc làm tròn/định dạng, Ví dụ tính tay | — |
| `G-CASE` | Xem BN6-04 | `G-ANTI-PRINT` (giữ, mở rộng) |
| `G-SKILL` | Lab `T3`/`T4`: mọi bài làm trong `kiem/ne/` phải trượt | — |
| `G-LABEL` | Xem 5.1 | đếm `ĐÃ CHỐT` |
| `G-ROOT` | Gốc kho chỉ gồm danh sách cho phép (chặn tái diễn tệp rác 39,7 GiB) | — |
| `G-WEB` | Bộ thử web (mục 6.8) | — |

Mọi cổng mới có phép thử dương và âm trong `tests/` trước khi áp vào kho. Không cổng nào đặt sàn số lượng chữ, số câu hay số phút.

---

## 6. Web lộ trình tương tác (WP-4)

### 6.1. Hiện trạng (OBSERVED: ảnh chụp và mã của `HOC_TAP.html`)

Đã có: vòng tiến độ, tích từng bài, lịch ôn giãn cách 1–3–7–14–30–60–120 ngày, chuỗi ngày học, thanh 11 chặng, tìm kiếm, nền tối, nút "Học tiếp", trang xem bài `out/<KHOÁ>/<Lxx>/xem.html` (video, mục lục, tốc độ). Chưa có: bản đồ, các bước trong một bài, phần thưởng, huy hiệu, chấm lab từ web, xuất/nhập tiến độ. Tiến độ nằm trong `localStorage` của trình duyệt, mất khi đổi trình duyệt hay xoá dữ liệu.

### 6.2. Kiến trúc

| Thành phần | Thiết kế | Lý do |
|---|---|---|
| Máy chủ | `hoc.py` (chỉ thư viện chuẩn Python), chỉ nghe `127.0.0.1`, mở bằng `hoc.cmd`; phục vụ tệp tĩnh, video (hỗ trợ tua), và 5 đường API | Một nguồn gốc ổn định cho mọi trang; chấm lab thật; không cần cài gì thêm |
| Giao diện | `web/` gồm HTML, CSS, mô-đun JavaScript thuần; không bước dựng, không tải gì từ mạng; bản đồ vẽ bằng SVG | Bền, dễ sửa, chạy ngoại tuyến |
| Dữ liệu | `tools/web_build.py` sinh `web/data/catalog.json` (chặng, khoá, bài, tiên quyết, mục tiêu, mục lục, nhãn ba trục, 16 lộ trình nghề) và `web/data/quiz/<KHOÁ>.json`; nguồn duy nhất là `curriculum/`, `lessons/`, `labs/`, `quality.yaml`, `pack.STAGES` | Không chép tay; có phép thử lược đồ |
| Tiến độ | Nhật ký sự kiện chỉ ghi thêm `~/.hoc_tap/events.jsonl` + ảnh chụp trạng thái suy ra; xuất/nhập một tệp JSON; nhập được trạng thái cũ `hoc_tap_v2` | Không mất khi đổi trình duyệt; sao lưu được; tính lại điểm được khi đổi luật thưởng |
| An toàn | Mã phiên ngẫu nhiên trong địa chỉ; API chấm chỉ nhận tệp nằm trong thư mục làm bài người học chọn; gọi `cham.sh` bằng danh sách tham số, có giới hạn thời gian; không lệnh nào ghép chuỗi vào shell | Máy chủ cục bộ vẫn phải chặn trang web lạ gọi vào |
| Dự phòng | `HOC_TAP.html` tĩnh tiếp tục được sinh cho tới khi web mới qua nghiệm thu W3 | Không có ngày nào người học không có trang để học |

API: `GET /api/state`, `POST /api/event`, `POST /api/cham` (khoá, bài, đường dẫn tệp → kết quả bộ chấm), `POST /api/nghe` (ghi một phán quyết phát âm theo đúng lược đồ `nghe_thu_ket_qua.json`, vào tệp riêng `~/.hoc_tap/nghe.jsonl` để không đụng tệp của người dùng), `GET /api/export`.

### 6.3. Bản đồ

- **Ba mức thu phóng.** Toàn cảnh: 11 vùng nối nhau theo một con đường uốn (mỗi chặng một vùng, màu và biểu tượng riêng; vùng chưa tới phủ sương). Trong vùng: mỗi khoá là một nhánh đường. Trong khoá: mỗi bài là một nút tròn theo thứ tự học, cạnh tiên quyết liên khoá vẽ nét đứt.
- **Trạng thái nút:** chưa mở (thiếu tiên quyết; vẫn vào được sau một lời nhắc), sẵn sàng, đang học (vành tiến độ theo số bước xong), xong (1–3 sao), cần ôn (chấm nhấp nháy nhẹ), bài có nhãn `G0/G1` mang viền cảnh báo "đang rà".
- **Nút đặc biệt:** dự án chặng (`PRJ`) là "cổng chặng" ở cuối vùng; lab nghề là nút hình lục giác trên nhánh khoá.
- **Chọn nghề:** chọn một trong 16 lộ trình của `tracks.yaml` thì đường của nghề đó sáng lên, phần còn lại mờ đi; thanh tiến độ tính theo lộ trình đã chọn.
- **Điều hướng:** kéo, cuộn để phóng, bàn phím (mũi tên đi theo cạnh, Enter mở bài), nút "Học tiếp" đưa tới nút kế; có chế độ danh sách tương đương cho trình đọc màn hình.

### 6.4. Các bước trong một bài và cách tích

| Bước | Điều kiện tự tích | Sao |
|---|---|---|
| ① Xem video | Đã phát ≥ 90% thời lượng (tính theo các đoạn đã phát, tua không tính) | ★ |
| ② Tự kiểm | Trả lời trước rồi mới mở đáp án; câu có đáp án máy kiểm thì máy chấm, câu tự luận thì tự chấm 3 mức | ★★ |
| ③ Luyện nhanh | `POST /api/cham` trả về đạt | ★★★ |
| ④ Lab nghề (nếu bài có) | Bộ kiểm thử của lab đạt | huy hiệu kỹ năng |
| ⑤ Ôn | Tới hạn theo lịch giãn cách; trả lời lại 1–2 câu | giữ sao khỏi mờ |

Tích tay vẫn được phép (ví dụ đã học ở nơi khác) nhưng ghi là "tự đánh dấu", không cộng điểm.

### 6.5. Thang phần thưởng, từ nhỏ tới lớn

| Cấp | Sự kiện | Phản hồi | Điểm |
|---|---|---|---:|
| Vi mô | Xong một bước | Dấu tích vẽ nét 300 ms, tiếng "tách" nhỏ, vành nút đầy thêm | +10 (lab nhanh +20) |
| Vi mô | Trả lời đúng ngay lần đầu | Chữ "+5" bay lên | +5 |
| Bài | Đủ sao của bài | Sao bung 800 ms, nút trên bản đồ đổi màu, cạnh tới nút kế sáng lên | +10 thưởng |
| Ngày | Đạt mục tiêu phút/ngày tự đặt | Ngọn lửa chuỗi ngày +1; "rương ngày" mở ra 10–50 điểm | 10–50 |
| Khoá | Xong mọi bài của khoá | Huy hiệu khoá + thẻ "bạn đã làm được" liệt kê kỹ năng (lấy từ mục tiêu) | +100 |
| Lab nghề | Bộ kiểm thử đạt | Huy hiệu kỹ năng có tên công cụ | +50 |
| Chặng | Qua cổng chặng (dự án) | Pháo giấy toàn màn hình 2,5 s, vùng kế tan sương, thẻ chứng nhận xuất được ra ảnh | +500 |
| Cột mốc | 10/50/100/200/400/806 bài; 10/50/100 giờ; 7/30/100 ngày liên tục | Cúp trong trang Hồ sơ | — |
| Cấp độ | Tổng điểm vượt ngưỡng | Tên cấp theo nghề: Tập sự → Kỹ sư → Kỹ sư chính → Senior nền tảng | — |

Nguyên tắc: phần thưởng gắn với bằng chứng (`D-5`); chuỗi ngày có một ngày nghỉ mỗi tuần không mất chuỗi; không thông báo dồn ép, không đếm ngược gây sợ mất; tôn trọng cài đặt giảm chuyển động của hệ điều hành; âm thanh tắt được; mọi thay đổi trạng thái đều có chữ đi kèm chứ không chỉ màu.

### 6.6. Các trang

Bản đồ · Bài học (video + bước + đề lab + nút chấm + nút "báo lỗi phát âm" gắn với dòng phụ đề đang đọc) · Ôn hôm nay · Hồ sơ (điểm, cấp, huy hiệu, lịch nhiệt, tiến độ theo nghề, xuất/nhập) · Tìm kiếm.

### 6.7. Giai đoạn

| GĐ | Nội dung | Nghiệm thu |
|---|---|---|
| W1 | `web_build.py`, `hoc.py`, nhật ký sự kiện, chuyển dữ liệu `hoc_tap_v2`, trang danh sách tương đương trang cũ | `tests/test_web_build.py`: 806 bài mỗi bài đúng một lần, đồ thị không chu trình, 0 liên kết chết; phép thử chuyển dữ liệu (BN6-09) |
| W2 | Bản đồ ba mức, trang bài học với 5 bước, tích tự động bước ①②, phần thưởng vi mô và cấp bài | 6 kịch bản đầu-cuối đạt; 806 nút vẽ xong < 1,5 s trên máy này |
| W3 | Điểm, cấp, chuỗi ngày, rương ngày, huy hiệu khoá, cổng chặng, hồ sơ, xuất/nhập, chọn nghề | Thêm 6 kịch bản; phát lại nhật ký sự kiện cho ra đúng điểm (tất định) |
| W4 | Chấm lab từ web, nút báo lỗi phát âm, hàng nghe | Kịch bản: nộp lời giải mẫu → đạt, nộp bài in cứng → trượt; đường dẫn ngoài thư mục làm bài bị từ chối |
| W5 | Câu hỏi có đáp án máy kiểm (WP-7), ôn giãn cách dùng câu hỏi | `quiz_verify.py` 100% |
| W6 | Tiếp cận, hiệu năng, hướng dẫn dùng | Đi hết đường học chỉ bằng bàn phím; tương phản ≥ 4,5:1; giảm chuyển động tắt hết hoạt ảnh |

### 6.8. Bộ thử `G-WEB`

Phép thử đơn vị Python cho `web_build.py` và `hoc.py`; phép thử trạng thái (phát lại sự kiện); kịch bản đầu-cuối bằng Playwright với trình duyệt Edge sẵn có (OBSERVED: `launch(channel="msedge")` chạy được trên máy này; Chromium kèm Playwright không khớp phiên bản). Không cổng web nào được tính đạt nếu chưa chạy thật kịch bản tương ứng.

---

## 7. Gói việc

Thứ tự chạy: WP-0 → WP-1 → (WP-4 W1–W3 song song với WP-2/WP-3 của Chặng 6) → lặp WP-2/3/5/6 theo từng chặng → WP-7 → WP-8 → WP-9.

### WP-0. Mốc và an toàn
0.1 Hỏi quyền commit (BN6-12). 0.2 Ghi lại 8 phép đo `af6/p1…p8` làm mốc. 0.3 Thêm `G-ROOT`. 0.4 Gỡ nhãn `ĐÃ CHỐT` khỏi `quality.yaml` và trang học, thay bằng nhãn tạm theo bảng 1.1. 0.5 Người dùng xem ma trận năng lực mục 8 (BN6-11).
Nghiệm thu: `grep -c 'ĐÃ CHỐT' quality.yaml` = 0; `G-ROOT` đạt; cây làm việc không có tệp ngoài danh sách.

### WP-1. Cổng và quy trình đọc bản 2
1.1 Viết `tail_review.py` (so với `5d7f329`, sinh bảng câu thêm), các cổng mục 5.3 kèm phép thử dương/âm. 1.2 Bỏ `G-LEN`, `G-PAD`, `G-BOILER` khỏi `content_gates.py` và `final_gates`. 1.3 Dựng bộ hiệu chuẩn 6 bài / 20 lỗi. 1.4 Viết `BRIEF_AF6.md` (từ `af6/BRIEF_K.md` + mục 5.2). 1.5 Đo độ bắt của `p8_tail_candidates.tsv` so với Mẫu K (BN6-14).
Nghiệm thu: `tests/test_gates_v2.py` đạt; cổng mới chạy trên kho hiện tại phải **trượt** đúng các lỗi Mẫu K đã nêu (đối chứng dương): `G-CASE` trượt `BCH L08`; `G-SKILL` không áp được cho `LNX L08` vì chưa có `kiem/ne/` (ghi nhận); `G-REPEAT` trượt ≥ 378 bài.

### WP-2. Sửa lời đọc (theo chặng)
Với mỗi bài lớp B, C: (a) lập bảng câu thêm; (b) mặc định xoá; người đọc đã hiệu chuẩn duyệt giữ câu nào đạt 3 điều kiện `D-2`; (c) sửa các lỗi bắt buộc sửa đã nêu trong `sample_k/` và các lỗi người đọc mới tìm ra; (d) lớp B và ba khoá mới: chạy lại mã cảnh dạy với ca biên (BN6-13); (e) không dựng video ở bước này (chờ WP-3, `D-10`).
Khối lượng: 614 bài có câu thêm; 343 bài ≥ 10 câu. Lớp A (196 bài): chỉ rà 76 bài có đổi, không xoá mặc định. `BEP` (10 bài) và `AIP` (6 bài): viết lại theo giáo án, vì 11/17 lỗi của khoá mới là mục tiêu ghi "Đo/Cài/Nhận diện/Viết" mà nội dung chỉ là một phép tính (CITED K4). `SPB` (13 bài): sửa mã dạy sai rồi nối 13 lab rời thành một dự án lớn dần, lab chạy với PostgreSQL/Redis/Kafka thật thay cho H2 ở các bài nói về chúng.
Nghiệm thu mỗi chặng: `G-TAIL` đạt; mẫu đối chứng 5.2 bước 4 đạt; `screen_code check` đạt.

### WP-3. Sửa thực hành tầng 1 và thẻ Tự làm (theo chặng)
3.1 `de.md` đủ 5 mục (`G-DE`). 3.2 Ca ẩn theo `G-CASE`, kèm ≥ 2 biến thể sai có tên trong `labs/<K>/<L>/sai/`. 3.3 Thẻ Tự làm trong tệp bài sinh tất định từ `de.md` (`G-TASKCARD`), lời đọc của thẻ là câu mô tả đúng nhiệm vụ của lab đó; bỏ hàng "Gợi ý triển khai" chung. 3.4 Sửa lời giải mẫu có dữ liệu mặc định in cứng (`or "<mẫu>"`). 3.5 Dựng lại video, chạy ASR, cập nhật `xem.html`.
Nghiệm thu mỗi chặng: `lab_gate` đạt; `G-CASE`, `G-DE`, `G-TASKCARD`, `G-REPEAT` đạt; `find_stale_all` 0; `pack check --decode` đạt.

### WP-4. Web lộ trình
Theo mục 6. W1–W3 làm ngay sau WP-1 vì không phụ thuộc việc sửa bài.

### WP-5. Lab nghề (tầng 2) theo chặng
Mỗi lab nghề: thư mục `labs/<KHOÁ>/N<k>/` gồm `de.md`, mã khởi đầu, `kiem/` (kiểm thử hành vi), `kiem/ne/` (bài làm né kỹ năng phải trượt), `loi_giai/`. Chạy trên máy người học với công cụ đã có trên máy này (OBSERVED: Java 21, gcc 16.2, Docker 28.3, Node 25, Python có sklearn/torch/pandas; Maven dùng `mvnw`).

| Chặng | Khoá | Lab nghề (công cụ) |
|---|---|---|
| 6 | `CPR` | Danh sách liên kết không rò (gcc + AddressSanitizer); bộ đọc tệp nhị phân; gỡ lỗi bằng gdb theo kịch bản |
| 6 | `LNX` | Lọc nhật ký thật bằng `grep/awk/sort`; viết dịch vụ nhỏ + `cron`; chạy và gỡ lỗi container thật (`docker run -p -v`, `logs`, `inspect`); Compose 2 dịch vụ |
| 6 | `CSA` `OSY` `NET` | Đo bộ nhớ đệm bằng chương trình C; bộ lập lịch mô phỏng có kiểm thử; sản xuất–tiêu thụ bằng luồng thật; máy khách/máy chủ TCP; bắt và đọc gói bằng `tcpdump`/`curl -v`; chia mạng con có kiểm thử |
| 7 | `DBS` | Thiết kế lược đồ + truy vấn trên PostgreSQL trong Docker; đọc `EXPLAIN` trước và sau khi thêm chỉ mục; hai phiên giao dịch tái hiện đọc bẩn/bế tắc |
| 7 | `SWF` `SDP` | Viết kiểm thử trước cho mô-đun có lỗi cài sẵn; tái cấu trúc theo mẫu thiết kế với bộ kiểm thử giữ nguyên |
| 7 | `WEB` `SEC` | API nhỏ + trang gọi API có phân trang con trỏ; tìm và vá chèn SQL/XSS trong ứng dụng mẫu; băm mật khẩu và JWT có kiểm thử |
| 8 | `DSY` `EVT` `DEN` | Kafka trong Docker: người tiêu thụ lũy đẳng, thứ tự theo khoá; hộp thư đi với PostgreSQL; đường ống theo lô có kiểm chất lượng dữ liệu |
| 8 | `CLD` `CLC` `DVO` `SAR` | Dockerfile nhiều tầng đo bộ đệm lớp; triển khai lên Kubernetes cục bộ (kind) nếu máy đủ, không thì Compose; đường ống CI chạy cục bộ; bài thiết kế hệ thống có bảng chấm |
| 9 | `DAN` `DSC` | Phân tích tệp giao dịch thật bằng pandas + SQL; thử nghiệm A/B có kiểm định; báo cáo tái lập được |
| 9 | `MLP` `MLO` `AIP` | Đường ống sklearn chống rò rỉ đo bằng thí nghiệm; theo dõi thí nghiệm và sổ mô hình; giám sát trôi dữ liệu; phục vụ mô hình qua API có kiểm thử độ trễ |
| 9 | `CS115 L22–L43` `CVI` `LLM` `AGT` `IRS` `RLN` | Lan truyền ngược tự cài đối chiếu với PyTorch; CNN nhỏ trên CPU; bộ tách từ BPE; RAG trên tập văn bản nhỏ có đo độ phủ; tác tử gọi công cụ có bộ kiểm; hệ gợi ý phân rã ma trận |
| 10–11 | các khoá chuyên ngành | Mỗi khoá 2 lab `T2`/`T3`; làm sau cùng |

Dự án chặng (`PRJ L00–L10`) nâng lên `T4`: có bộ kiểm thử hành vi, bảng chấm, và bài làm né kỹ năng phải trượt.
Nghiệm thu mỗi lab: lời giải đạt, mọi bài trong `kiem/ne/` trượt (`G-SKILL`), một người đọc đã hiệu chuẩn làm thử từ đề mà không mở lời giải.

### WP-6. Phát âm
6.1 Đưa 10 mục `fix` hiện có của người dùng vào từ điển đọc, mỗi mục một phép thử; tìm mọi vị trí cùng từ trong 806 bài. 6.2 Xếp 5 359 câu thành hàng nghe: nhóm 1 = câu có số/đơn vị bị nghe khác (ví dụ "phẩy" nghe thành "nghìn") và câu độ giống < 0,70; nhóm 2 = 0,70–0,79; nhóm 3 = còn lại (phần lớn là máy chép sai từ mượn như "byte" → "bay", xử lý theo cặp từ thay vì từng câu). 6.3 Bài nào sửa từ điển thì dựng lại cùng đợt WP-3.
Nghiệm thu: `lexicon_regress.py` đạt; nhóm 1 được người nghe 100% (cần người dùng; không có thì nhãn Âm thanh dừng ở `A1`).

### WP-7. Câu hỏi máy kiểm được và cổng chặng
Mỗi bài ≥ 3 câu (điền số hoặc chọn một) soạn từ các biểu thức `checks` đã có của bài, đáp án do máy tính lại; mỗi chặng một bài kiểm 20 câu rút ngẫu nhiên + dự án chặng.
Nghiệm thu: `quiz_verify.py` 100%; người đọc đối chứng làm thử 10% số câu, 0 câu sai đáp án hoặc mơ hồ.

### WP-8. Lấp lỗ hổng năng lực (sau khi Chặng 1–9 đạt nhãn)
Theo ma trận mục 8. Ưu tiên: thống kê suy diễn cho khoa học dữ liệu; học sâu thực hành; SQL phân tích; kỹ năng nghề của senior (đọc mã, rà soát mã, viết tài liệu thiết kế, ước lượng). Mỗi khoá mới theo đúng chuẩn 5.1–5.2 ngay từ bài đầu.

### WP-9. Nghiệm thu
Bộ cổng đầy đủ (cổng AF5 còn giữ + cổng mục 5.3 + `G-WEB`); mẫu đối chứng toàn kho ≥ 60 bài phân tầng do người đọc khác nhóm chấm; cập nhật nhãn ba trục; bàn giao. Kho chỉ được ghi `DONE` khi BN6-07 đóng; nếu chưa có tai người thì `PARTIAL` và ghi rõ.

---

## 8. Ma trận năng lực đích (bản đề xuất, chờ người dùng xem — BN6-11)

"Nền kỹ sư senior" trong kế hoạch này nghĩa là: với mỗi năng lực dưới đây, người học **làm ra được một sản phẩm kiểm được** chứ không chỉ xem xong bài. Cột "Hiện có" tính theo kho hôm nay (INFERRED từ tên bài và hồ sơ lab `af6/p3_labs.out`).

| Lĩnh vực | Năng lực | Khoá giảng | Hiện có về thực hành | Còn thiếu |
|---|---|---|---|---|
| CNTT | Dòng lệnh, Git, môi trường, gỡ lỗi | `FND`, `LNX`, `BNX L00` | Tốt ở `FND`; `LNX` lab giả lập | Lab nghề `LNX` |
| CNTT | Lập trình thành thạo 2 ngôn ngữ + kiểm thử | `JVA`, `JV2`, `PYT`, `CPR` | Tốt ở Java/Python; C yếu | Lab nghề `CPR`; bộ bài luyện thuật toán có chấm |
| CNTT | Cơ sở dữ liệu và SQL | `DBS`, `BNK L04–05` | SQL nhỏ trên sqlite | PostgreSQL thật, kế hoạch thực thi, giao dịch |
| CNTT | Web, API, bảo mật ứng dụng | `WEB`, `SEC`, `BNX`, `SPB` | `SPB` có dự án thật | Lab nghề `WEB`, `SEC` |
| CNTT | Vận hành: container, CI/CD, đám mây, quan sát | `CLD`, `CLC`, `DVO` | Gần như chỉ tính công thức | Toàn bộ lab nghề chặng 8 |
| KHMT | Toán rời rạc, thuật toán, độ phức tạp | `DMS`, `CS112` | Tốt (soạn tay, lab 20–33 dòng) | Bộ bài luyện tăng dần |
| KHMT | Máy tính, hệ điều hành, mạng | `CSA`, `OSY`, `NET` | Mô phỏng nhỏ | Lab đo thật |
| KHMT | Hệ phân tán, kiến trúc | `DSY`, `EVT`, `SAR` | Tính công thức | Kafka/PostgreSQL thật; bài thiết kế có bảng chấm |
| KHMT | Lý thuyết tính toán, ngôn ngữ lập trình, song song | `TOC`, `PLC`, `PAR` | Tính công thức | 2 lab cơ chế mỗi khoá (bộ phân tích cú pháp, máy ngăn xếp) |
| AI | Toán cho học máy | `CS115` | Tốt ở L00–L21 | Lab cho L22–L43 |
| AI | Học máy thực hành và đánh giá | `MLP`, `DSC L10–11` | sklearn có dùng, nhưng bài bị độn | Sửa `MLP`; lab đo rò rỉ thật |
| AI | Học sâu thực hành | `CS115 L34–43`, `MLP L10–11` | 3 lab dùng torch | **Thiếu khoá thực hành học sâu** |
| AI | Mô hình ngôn ngữ, RAG, tác tử, đánh giá | `LLM`, `AGT`, `IRS` | Tính công thức | Lab nghề chặng 9 |
| AI | MLOps | `MLO`, `AIP` | Tính công thức | Lab nghề chặng 9 |
| KHDL | Thống kê và suy diễn | `CS115 L13–17, L44`, `DSC`, `DAN L10` | Rải rác | **Thiếu khoá thống kê suy diễn có thực hành** |
| KHDL | Phân tích dữ liệu, trực quan hoá, SQL phân tích | `DAN`, `DSC`, `PYT L09–11` | pandas xuất hiện ở 2 lab | Lab nghề `DAN`, `DSC`; **thiếu SQL phân tích** |
| KHDL | Kỹ thuật dữ liệu | `DEN`, `DSY L07–12` | Tính công thức | Lab nghề chặng 8 |
| Chung | Kỹ năng nghề của senior: đọc và rà soát mã, viết tài liệu thiết kế, ước lượng, xử lý sự cố | `SEP`, `CAS`, `BEP L09`, `SAR` | Chỉ nghe giảng | Bài tập rà soát mã và viết tài liệu thiết kế có bảng chấm |

---

## 9. Lộ trình phiên (thứ tự, không phải cam kết thời gian)

Mỗi phiên kết thúc ở một điểm dừng an toàn: cổng nhanh đạt, không có bài nào dựng dở, sổ `STATE` ghi phiên kế tiếp bắt đầu ở đâu.

| Phiên | Việc | Điểm dừng |
|---|---|---|
| E1 | WP-0, WP-1 | Cổng bản 2 có phép thử; nhãn đã gỡ; trang học hiện nhãn tạm |
| E2–E3 | WP-4 W1–W2 | Web mới chạy song song trang cũ; chuyển dữ liệu đạt |
| E4 | WP-4 W3 | Bản đồ + phần thưởng đủ cấp; người dùng dùng thử |
| E5 | Chặng 1–5 phần soạn tay: rà 76 bài lớp A có đổi + WP-6.1; thêm ca ẩn cho lab lớp A nào in cứng vẫn đạt | 196 bài đạt `G2` · `T1+` · `A1` |
| E6 | Dự án chặng `PRJ L00–L04` (WP-2, WP-3, nâng lên `T4`) | 5 dự án chặng đầu đạt nhãn |
| E7–E8 | Chặng 3: `SPB` (sửa mã dạy sai, nối lab), `BEP` (viết lại) | Chặng 1–5 trọn vẹn đạt nhãn; mẫu đối chứng đạt |
| E9–E11 | Chặng 6: WP-2, WP-3, WP-5 (gồm `CPR`, `LNX`, `PRJ L05`) | Chặng 6 đạt nhãn; mẫu đối chứng đạt |
| E12–E14 | Chặng 7 | như trên |
| E15 | WP-4 W4 (chấm lab từ web, báo lỗi phát âm) | Lab chặng 6–7 chấm được từ web |
| E16–E19 | Chặng 8 | như trên |
| E20–E24 | Chặng 9 (gồm `MLP`, `AIP` viết lại, `CS115 L22–L43`) | như trên |
| E25–E26 | WP-7, WP-4 W5–W6 | Câu hỏi máy kiểm; web hoàn chỉnh |
| E27–E29 | Chặng 10–11 | như trên |
| E30 | WP-8 thiết kế khoá bổ sung | Giáo án được duyệt |
| E31 | WP-9 | Bàn giao |

Ghi chú: thứ tự trên bám đường người học đi (`D-9`). Nếu người học tới một chặng trước khi chặng đó sửa xong, phiên thực thi đổi thứ tự để chặng đó lên trước; kiểm tiến độ người học trong `~/.hoc_tap/` hoặc hỏi người dùng.

---

## 10. Mười hai bẫy cần tránh ở phiên thực thi

1. Không đặt lại bất kỳ sàn số lượng nào (từ, phút, số câu). Bài ngắn mà đúng là bài tốt.
2. Không thay khuôn câu này bằng khuôn câu khác; thẻ Tự làm sinh từ dữ liệu của chính lab.
3. Không ghi "đã xem" cho cờ phát âm bằng máy. Chỉ có ba kết cục: người đã nghe, đã sửa từ điển, hoặc để mở.
4. Không dùng báo cáo của người đọc chưa qua hiệu chuẩn làm chứng cứ.
5. Không dựng video trước khi gom đủ ba loại sửa của bài (`D-10`).
6. Không chạy lời giải lab tại gốc kho (tệp 39,7 GiB từng sinh ra theo cách đó); mọi thứ chạy trong thư mục tạm.
7. Không ghi vào `nghe_thu_ket_qua.json`, không đụng chỉ mục git.
8. Không tính một cổng là đạt theo mã thoát của lệnh gộp; đọc dòng tổng của từng cổng.
9. Không quá 4 tác tử cùng lúc; ghi sổ trước khi mở; tác tử tự ghi báo cáo ra tệp.
10. Không sửa lớp A theo kiểu hàng loạt; 120 bài không đổi là tài sản đã kiểm.
11. Không để web ghi tiến độ chỉ vào trình duyệt; nguồn thật là nhật ký sự kiện trên đĩa.
12. Không ghi `DONE` khi còn điểm nghẽn `REQUIRED` mở; thiếu tai người thì là `PARTIAL`.

---

## 11. Phần chưa kiểm trong lượt rà này

| Việc | Trạng thái |
|---|---|
| Bộ cổng đầy đủ `day_du` tại `a3039c1f` (lab_gate, screen_code, audit_all, verify_spb, giải mã video) | NOT_VERIFIED lượt này; chỉ CITED từ nhật ký của đợt thực thi |
| 41/48 lỗi bắt buộc sửa của Mẫu K | CITED từ báo cáo tác tử, chưa tự kiểm lại (đã kiểm 7: `OSY L02`, `CLD L02`, `SEC L04`, `EVT L03`, `BCH L08`, `LNX L08`, `BEP L06`) |
| Mẫu K là 32/806 bài | Tỉ lệ lỗi của toàn kho là ước lượng; khoảng tin cậy rộng |
| Ma trận mục 8 | INFERRED từ tên bài và hồ sơ lab; chưa đọc nội dung từng khoá để khẳng định "thiếu" |
| Thiết kế web | Chưa có dòng mã nào; mọi số hiệu năng là mục tiêu, chưa đo |
| Nghe bằng tai người | Người dùng đang làm (191 phán quyết tính tới 22:53 +07 ngày 27/11) |
