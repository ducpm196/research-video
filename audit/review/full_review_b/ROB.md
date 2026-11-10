# ROB — đã đọc 14/14 bài

Đọc kiểm 2026-11-08: mọi cảnh, mọi `show`/`say`/`checks`, đề và đáp án quiz của 14 bài `lessons/rob/`. ROB không có mẫu `audit/rob/src/*.tpl.yaml` (không cần chạy `sync_tpl_from_lesson.py`). Tổng: 8 bài đã sửa, 2 mục MUST, 12 mục SHOULD.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | đã sửa | example: MUST — bảng ngân sách ghi định vị 9 ms là “trễ tệ nhất”, trong khi hình `intuition` và Lỗi 1 nói lúc khó nhất định vị mất 25 ms (tự mâu thuẫn); đổi thành “lúc chạy bình thường”, thêm dòng Bước 4: lúc khó nhất 4 + 25 + 2 + 1 = 32 ms vượt hạn 20 ms, phải tính theo trễ tệ nhất (thêm `checks`). quiz câu 2: SHOULD — đáp án nói vòng định vị 40 Hz “dư nhiều” mà quên lúc khó nhất 25 ms vừa khít chu kỳ 25 ms; vị trí cũ “tới 25 ms” sửa thành tới khoảng 50 ms (một chu kỳ chờ + thời gian tính). Giáo án L00 `example` thêm vế lúc khó nhất | Siegwart–Nourbakhsh–Scaramuzza (2011) ch. 1; nguyên tắc thời hạn thời gian thực dùng trễ tệ nhất (ESY bài 9, chính bài này Lỗi 1) | lint: 0 FAIL, 0 WARN, 21 PASS; render: 67 khung (0 vấn đề) |
| L01 | không phát hiện lỗi | — | — | — |
| L02 | đã sửa | sym: SHOULD — “sai số không bao giờ được sửa — chỉ cộng thêm” tuyệt đối; viết lại: chỉ dùng bánh xe thì không có gì sửa sai số, nó cộng dồn nên khoảng sai có thể có lớn dần theo quãng | Siegwart–Nourbakhsh–Scaramuzza (2011) mục 5.2.4; Borenstein & Feng, IEEE TRA 12(6) 1996 | lint: 0 FAIL, 0 WARN, 24 PASS; render: 69 khung (0 vấn đề) |
| L03 | không phát hiện lỗi | — | — | — |
| L04 | không phát hiện lỗi | — | — | — |
| L05 | đã sửa | example Bước 3–4: SHOULD — gọi ô ngoài đường chéo 0,01 của F P Fᵀ là “tương quan”; đó là hiệp phương sai (hệ số tương quan ở đây là 0,01/√(0,02·0,01) ≈ 0,71); đổi thuật ngữ ở màn hình và lời đọc; xoá 1 mục `asr_reviewed` cũ | Thrun–Burgard–Fox, Probabilistic Robotics (2005) mục 3.3 (ma trận hiệp phương sai) | lint: 0 FAIL, 0 WARN, 22 PASS; render: 64 khung (0 vấn đề) |
| L06 | đã sửa | pitfalls Lỗi 1: SHOULD — “bản đồ không bao giờ sửa” sai: không chặn thì vẫn sửa, nhưng rất chậm — sau 20 lần “chiếm”, phải 42 lần “trống” mới về dưới 0,5 (thêm `checks` bằng alg.occ_sequence); intuition: “đóng băng” → “gần như đóng băng” | Thrun–Burgard–Fox (2005) ch. 9; tính lại: 20·ln(7/3)/ln(1,5) ≈ 41,8 | lint: 0 FAIL, 0 WARN, 25 PASS; render: 68 khung (0 vấn đề) |
| L07 | đã sửa | prereq: SHOULD — “sai số cộng dồn chứ không tự triệt tiêu” tuyệt đối (sai số ngẫu nhiên có thể bù một phần); viết lại “chỉ bánh xe thì không có gì kéo nó về” | Thrun–Burgard–Fox (2005) mục 5.4 (mô hình chuyển động theo đo quãng đường) | lint: 0 FAIL, 0 WARN, 24 PASS; render: 77 khung (0 vấn đề) |
| L08 | đã sửa | sym: SHOULD — mô tả cây mở rộng nhanh là “kéo nút gần nhất của cây về phía điểm ngẫu nhiên” dễ hiểu thành dời nút cũ; đúng là mọc thêm một nút MỚI từ nút gần nhất, cách một đoạn ngắn về phía điểm đó (tách câu dài, sửa `focus`) | S. LaValle, Rapidly-Exploring Random Trees, TR 98-11 (1998); Planning Algorithms (2006) mục 5.5 | lint: 0 FAIL, 0 WARN, 24 PASS; render: 72 khung (0 vấn đề) |
| L09 | đã sửa | hook: SHOULD — “lập kế hoạch lại cả đường mất cả giây” là con số không nguồn nói như sự thật; đổi thành “có thể mất cả giây” | — (viết mềm lại, không có nguồn) | lint: 0 FAIL, 0 WARN, 24 PASS; render: 74 khung (0 vấn đề) |
| L10 | không phát hiện lỗi | — | — | — |
| L11 | không phát hiện lỗi | — | — | — |
| L12 | không phát hiện lỗi | — | — | — |
| L13 | đã sửa | stage4 (màn hình, lời đọc, trường `stage.scale`): MUST — ghi “năm 2019, có người ngồi kèm: hơn 6,1 triệu dặm” cộng riêng 65 000 dặm không người lái; nguồn nói hơn 6,1 triệu dặm là TỔNG, gồm phần có người kèm 2019 và 65 000 dặm không người lái. stage4: SHOULD — “mô phỏng phản thực vài giây sau đó” (“vài giây” không có trong nguồn) → “diễn biến sau đó”; “thử mọi bản phần mềm sau” → “các bản” (nguồn: “future software can be tested”). stage3: SHOULD — “lọc Kalman” → “một biến thể của lọc Kalman (UKF)” (nguồn ghi unscented Kalman filter, bài 5 dạy bản mở rộng); “sai số cỡ xen-ti-mét” → “thường cỡ” (nguồn: “usually”); câu ra-đa viết lại cho rõ là trình điều khiển USB của máy nhận dữ liệu gây trục trặc. stage2: SHOULD — “chỉnh tham số bằng cách thử lần lượt” (không có trong trích nguồn) → “học các tham số từ dữ liệu đã ghi”. stage5: SHOULD — “muốn chứng minh giảm 90% cần 56,3 triệu dặm” đọc thành chứng minh mức giảm 90%; nguồn nói một xe có tỉ lệ bằng 10% mốc cần 56,3 triệu dặm mới kết luận được là có giảm — viết lại | audit/rob/sources_L13.md: [ST06] Thrun và cộng sự, JFR 23(9) 2006, §4, §5, §10.1; [WM20] arXiv:2011.00038 Abstract, §1.2; [KU25] arXiv:2505.01515v1 Introduction | lint: 0 FAIL, 0 WARN, 41 PASS; render: 144 khung (0 vấn đề) |

## Không sửa và vì sao
- L13: mọi sự kiện/năm/con số đã đối chiếu với các câu trích nguyên văn trong `audit/rob/sources_L13.md` (đọc 2026-11-02); lần này KHÔNG tải lại PDF nguồn. Câu “phần lớn có người được huấn luyện ngồi sau vô lăng” (20 triệu dặm) là suy ra từ 74 000 dặm không người lái / hơn 20 triệu dặm của [WS20], không phải câu trích — giữ vì phép so đủ chặt. Bước 2 chặng 4 (29/47 ≈ 62% “phần người kèm đã ngăn”) khớp câu của [KU25] về [WM20], giữ nguyên.
- L13 chặng 3: 19,1 dặm/giờ × 6,9 giờ ≈ 131,8 dặm là phép tính lại, không phải độ dài đường đua do nguồn ghi — bài đã trình bày đúng là “tính lại”, giữ.
- L00 Lỗi 2 (“tin vị trí quá 100 ms thì giảm tốc hoặc dừng”), L09 Lỗi 4, L10 Lỗi 4, L12 Lỗi 4: ngưỡng là số minh hoạ trong bối cảnh bài, không trình bày như quy chuẩn — giữ.
- L09 quiz: lời đọc “điểm cao không bao giờ vượt qua được bộ lọc” — đúng theo cấu trúc thuật toán (lọc trước rồi mới chấm điểm, Fox–Burgard–Thrun 1997), giữ.
- L10 recap “mọi bộ điều khiển đều mặc cả giữa hai điều này” và L12 recap “thiết kế cho lúc mọi thứ khác đều hỏng”: câu tư duy, không phải khẳng định kỹ thuật đo được — giữ.
- L04 Lỗi 3 nói lấy mẫu lại sau mỗi phép đo làm mất đa dạng: định vị Monte Carlo chuẩn vẫn lấy mẫu lại mỗi bước; bài nói về “quá thường xuyên” khi trọng số chưa suy biến (khớp Thrun–Burgard–Fox 2005 mục 4.3.4), giữ.
- `audit/verify_plan_curricula.py`: không cần đổi `rec()` của ROB — không con số cũ nào đổi (chỉ thêm `checks` mới ở L00, L06).
- `scan_ctrl.py`: 8 lượt, tất cả ở `lessons/jva/` (không thuộc ROB, không chạm).

## Kết quả bộ kiểm
- `audit/rob/verify_rob.py`: verify_rob: 14/14 PASS
- `tools/lv.py curriculum curriculum/rob.yaml`: curriculum: 14 bài, 14 đã có đặc tả, 0 lỗi
- `audit/verify_plan_curricula.py` (dòng ROB): ROB:L00 … ROB:L13 đều PASS
- lint toàn bộ 14 bài ROB: 0 FAIL, 0 WARN
