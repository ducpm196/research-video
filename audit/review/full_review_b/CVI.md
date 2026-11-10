# CVI — đã đọc 13/13 bài

Đọc toàn bộ `show`, `say`, `checks`, quiz và đáp án của 13 bài `lessons/cvi/`, đối chiếu các bài có sự kiện thật (L04, L05, L07, L08, L10, L11, L12) với `audit/cvi/sources_L*.md`. Khoá không có mẫu `*.tpl.yaml` nên không cần đồng bộ mẫu. Tổng: 6 bài sửa, 0 mục MUST, 7 mục SHOULD.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | đã sửa | recap tư duy: SHOULD — “phần lớn lỗi ảnh là lỗi dữ liệu” không có nguồn; đổi thành “rất nhiều lỗi ảnh…, như ba lỗi đầu ở trên”; quiz đáp án 3: SHOULD — “nén video nhỏ đi hàng chục lần” nói thấp hơn thực tế; đổi thành “hàng chục tới hàng trăm lần, tuỳ mức nén” (4K30 thô ≈ 6 Gbit/s, luồng nén thường vài chục Mbit/s) | tính lại: 24 883 200 byte · 30 · 8 ≈ 5,97·10⁹ bit/s; ITU-T H.264/H.265 (mức nén tuỳ cấu hình) | lint: 0 FAIL, 0 WARN, 34 PASS; render: 93 khung (0 vấn đề) |
| L01 | đã sửa | hook: SHOULD — “bộ tìm cạnh nổi tiếng nhất” là xếp hạng không kiểm được; đổi thành “một bộ tìm cạnh kinh điển” | Gonzalez & Woods, Digital Image Processing, 4th ed., §10.2 (Sobel là một trong các toán tử gradient cổ điển) | lint: 0 FAIL, 0 WARN, 36 PASS; render: 89 khung (0 vấn đề) |
| L02 | không phát hiện lỗi | — | — | — |
| L03 | không phát hiện lỗi | — | — | — |
| L04 | đã sửa | hook: SHOULD — đem nguyên tỉ lệ “bỏ 90% sai, mất dưới 5% đúng” của Lowe 2004 áp cho tường gạch như sự thật; thêm “trên bộ ảnh thử của Lowe (2004). Giả sử tỉ lệ đó cũng đúng ở đây” | Lowe, IJCV 60(2) 2004, §7.1 (đo trên bộ ảnh của chính bài báo) | lint: 0 FAIL, 0 WARN, 30 PASS; render: 81 khung (0 vấn đề) |
| L05 | không phát hiện lỗi | — | — | — |
| L06 | đã sửa | pitfalls bước 1: SHOULD — “Camera có máy chiếu chấm sáng lên tường” nghe như mọi camera đều có; đổi thành “Một số camera đo độ sâu có máy chiếu…” (stereo chủ động) | Intel RealSense D400 Series Datasheet (máy chiếu hồng ngoại tạo vân; truy cập 2026-11-08, no revision given) | lint: 0 FAIL, 0 WARN, 35 PASS; render: 90 khung (0 vấn đề) |
| L07 | không phát hiện lỗi | — | — | — |
| L08 | không phát hiện lỗi | — | — | — |
| L09 | không phát hiện lỗi | — | — | — |
| L10 | đã sửa | real bước 2: SHOULD — “độ chính xác tụt 11% tới 14%” dễ hiểu nhầm thành mức giảm tương đối, trong khi bài vừa dạy “tăng bao nhiêu phần trăm”; nguồn là điểm phần trăm tuyệt đối (83% → 72% là “11% drop”). Đổi thành “11 tới 14 điểm phần trăm” | Recht và cộng sự, ICML 2019, arXiv:1902.10811 (“the best model … sees an 11% drop from 83% to 72%”, `sources_L12.md`) | lint: 0 FAIL, 0 WARN, 31 PASS; render: 86 khung (0 vấn đề) |
| L11 | đã sửa | (người điều phối sửa sau báo cáo) SHOULD — nguyên tắc Morgan nêu lần đầu năm 1894 (An Introduction to Comparative Psychology), bản sửa 1903; bài ghi “từ năm 1903” → sửa màn hình và lời đọc | New World Encyclopedia “C. Lloyd Morgan” (truy cập 2026-11-08, no revision given) | lint: 0 FAIL, 0 WARN, 24 PASS / render: 79 khung (0 vấn đề) |
| L12 | đã sửa | stage6 (màn hình, lời đọc, trường `stage.scale`): SHOULD — giống L10, “tụt 11% tới 14%” đổi thành “11 tới 14 điểm phần trăm”, khớp “tụt 11 điểm” ở hook và ở tự kiểm | như trên, [RE19] | lint: 0 FAIL, 0 WARN, 38 PASS; render: 121 khung (0 vấn đề) |

## Không sửa và vì sao
- L07 bước 2: lớp 3 × 3 × 512 × 512 của mạng có lối tắt được đếm “+ 512” hệ số tự do. Bản cài đặt thường bỏ hệ số tự do vì có chuẩn hoá theo lô, khi đó còn 2 359 296; tỉ số với đầu phân loại vẫn ≈ 460. Bài nói rõ là đếm theo công thức lớp tích chập đã học, và [H15] không ghi chuyện bỏ hệ số tự do, nên không sửa.
- L11: “phỏng theo một nguyên tắc … từ năm 1903 (Morgan)” khớp [G20] (“as early as 1903”). Theo hiểu biết của tôi, “Morgan's Canon” xuất hiện lần đầu năm 1894, còn 1903 là bản in lại; tôi chưa mở được sách gốc để kiểm nên giữ theo nguồn đã ghi. Ghi chú: chưa kiểm được nguồn gốc 1894.
- L12 chặng 5: “bộ thử 100 000 ảnh giữ nguyên từ 2012” có trong [RU15] cho tới 2014. Kết quả tìm kiếm cho thấy trang tải ILSVRC 2017 (image-net.org/challenges/LSVRC/2017/2017-downloads) ghi dữ liệu không đổi từ 2012, nhưng tôi chưa mở trực tiếp được trang đó (truy cập 2026-11-08). Giữ nguyên, ghi “chưa kiểm được nguồn trực tiếp”.
- L12 chặng 1, bước 2: con số 5 lỗi trên 1500 ảnh là của bộ thử 2012–2014, đặt ở chặng 2010. Câu không ghi năm, nên không sai, chỉ hơi lẫn chặng.
- L02 cân bằng biểu đồ: dùng công thức sách giáo khoa (L−1)·tích lũy/N, khác `equalizeHist` của OpenCV (trừ tích lũy nhỏ nhất). Bài đã ghi quy ước ở đầu tệp, nên không sai.
- L01 bước 4: “hướng cạnh nghiêng 45 độ” đọc theo hướng gradient hay theo đường biên đều ra 45° (hoặc 135°). Giữ.
- `rec()` của `audit/verify_plan_curricula.py` cho CVI không cần đổi: không bài nào đổi số.

## Kết quả bộ kiểm
- `audit/cvi/verify_cvi.py`: `verify_cvi: 112/112 PASS`
- `tools/lv.py curriculum curriculum/cvi.yaml`: `curriculum: 13 bài, 13 đã có đặc tả, 0 lỗi`
- `audit/review/scan_ctrl.py`: không có lượt nào ở `lessons/cvi/`.
