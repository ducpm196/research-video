# IRS — đã đọc 14/14 bài

Đọc kiểm đợt B, 2026-11-08. Đọc từng bài từ đầu đến cuối (mọi cảnh, `show`/`say`/`checks`, quiz, đáp án), đối chiếu `audit/irs/sources_L*.md`;
tải lại hai PDF để kiểm số (arXiv 1812.02353, Covington và cộng sự 2016) và ghi câu trích vào sources_L09.md, sources_L13.md.
Khoá không có mẫu `audit/irs/src/*.tpl.yaml` → không cần đồng bộ mẫu. Tổng: 4 bài sửa, 1 MUST, 5 SHOULD.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | không phát hiện lỗi | — | sources_L00.md (Järvelin, Kekäläinen 2002: TREC-7 528 000 văn bản, 50 câu hỏi, 1000 kết quả) | — |
| L01 | không phát hiện lỗi | — | sources_L01.md | — |
| L02 | đã sửa | pitfalls lỗi 4: SHOULD — “công thức xếp hạng có bão hoà … ra đời để chặn việc này (nhồi từ khoá)” sai: bão hoà chỉ giới hạn lợi ích của việc lặp từ, văn bản nhồi từ khoá vẫn được điểm cao; sửa màn hình, lời đọc và `fix` của giáo án L02 | S. Robertson, H. Zaragoza, The Probabilistic Relevance Framework: BM25 and Beyond, Foundations and Trends in IR 3(4), 2009 (bão hoà tần suất); DEN bài 7 | lint: 0 FAIL, 0 WARN, 30 PASS; render: 87 khung (0 vấn đề) |
| L03 | đã sửa | pitfalls lỗi 2 (lời đọc): SHOULD — “vùng đông người” trong khi màn hình nói vùng đông điểm dữ liệu; sửa “vùng có nhiều điểm” cho khớp màn hình | — (khớp màn hình) | lint: 0 FAIL, 0 WARN, 32 PASS; render: 82 khung (0 vấn đề) |
| L04 | không phát hiện lỗi | — | sources_L04.md (Cormack và cộng sự 2009: k = 60, 4–5% trung bình) | — |
| L05 | không phát hiện lỗi | — | sources_L05.md | — |
| L06 | đã sửa | quiz câu 3: MUST — đề “thay W bằng X” nhưng đáp án lấy trung bình món ốp lưng (4 + 5 + 2)/3 ≈ 3,667, còn tính điểm 5 của W đã bị thay; đúng là (4 + 2)/2 = 3 (nếu giữ W thì W lại có 2 món chung với U và đáp án “không ai dùng được” sai). Sửa đề (nói rõ bảng chỉ còn U, V, X), tiêu đề, đáp án, `checks`, và `audit/irs/verify_parts/L06.py` (L06f, có chú thích lý do). formula bước 1 (lời đọc): SHOULD — “cosin không phụ thuộc một người chấm nhiều hay ít món” sai (số món đã chấm đổi vector, đổi cosin); sửa thành “nhân cả hàng điểm với cùng một số thì độ giống không đổi” | toán, kiểm bằng checks và verify_parts/L06.py | lint: 0 FAIL, 0 WARN, 32 PASS; render: 84 khung (0 vấn đề) |
| L07 | không phát hiện lỗi | — | sources_L07.md (480 189 / 17 770 / 100 480 507; 20–100 chiều; 3,7 + 0,5 − 0,3) | — |
| L08 | không phát hiện lỗi | — | sources_L08.md (Hu và cộng sự 2008 hệ số 40, dưới nửa chương trình; Mikolov 2013 mũ 3/4; Yi 2019 p = 0,02) | — |
| L09 | đã sửa | example.1: SHOULD — (người điều phối sửa sau báo cáo) tính tay thì xếp theo trung bình đã khoá tai nghe mới sau 18 lần không bấm (1/20 = 0,05 < 51/1002 ≈ 0,0509 < 1/19); thêm câu giải thích vì sao mô phỏng hạt giống 0 cho 19 lần (trung bình tai nghe cũ có lúc tụt dưới 0,05), thêm `checks`; lint 0 FAIL 0 WARN, render 0 vấn đề, verify_irs 123/123 | sources_L09.md; kiểm lại arXiv 1812.02353: “we split users … into three buckets: 90%, 5%, 5%” (ghi bổ sung vào sources_L09.md) | — |
| L10 | không phát hiện lỗi | — | sources_L10.md (Joachims 2017 hoán đổi 1–21, 7 ngày; Zhao 2019 −0,07% / +0,24%) | — |
| L11 | không phát hiện lỗi | — | sources_L11.md (Carbonell, Goldstein 1998: λ = 1 / λ = 0) | — |
| L12 | không phát hiện lỗi | — | sources_L12.md (khung Covington 2016; mọi số thời gian là minh hoạ) | — |
| L13 | đã sửa | stage2 bước 2: SHOULD — “mất mát tăng 4,1%: từ 34,6% lên khoảng 34,6 · 1,041 ≈ 36,0%” là suy diễn không nguồn: bài báo chỉ ghi “increased … by a dramatic 4.1%”, không nói tương đối hay điểm phần trăm; bỏ con số 36,0, giữ “tăng 4,1%, gọi là đáng kể” và so với mức chênh giữa các cấu hình mạng ở Bảng 1. Sửa `checks`, `verify_parts/L13.py` (L13e, có chú thích), ghi câu trích vào sources_L13.md | Covington, Adams, Sargin, RecSys 2016, mục 6 và Bảng 1 (PDF tải lại 2026-11-08) | lint: 0 FAIL, 0 WARN, 37 PASS; render: 125 khung (0 vấn đề) |

## Không sửa và vì sao
- L09: tính tay, xếp theo trung bình thì tai nghe mới đã thua từ sau 18 lần không bấm (1/20 = 0,05 < 0,0509), còn hook và ví dụ kể “19 lần”: con số 19 là kết quả mô phỏng (`irs_bandit_run`, hạt giống 0), lần hiện thứ 19 xảy ra khi trung bình của tai nghe cũ dao động xuống dưới 0,05. Bài không khẳng định luật “dừng sau đúng 19 lần”; “0,92¹⁹ ≈ 0,205, khoảng 1 trong 5” là ước lượng gần đúng, mô phỏng ra 25/100. Không sai kiến thức nên giữ. Người điều phối có thể cân nhắc thêm một câu giải thích.
- L12: hook dùng danh mục 10 000 sản phẩm, còn hình phễu dùng kho 10 triệu: hai ví dụ minh hoạ riêng, đều ghi “số minh hoạ” → giữ.
- L04 (IRS): bài báo năm 2009 ghi hợp nhất thứ hạng “consistently yields better results”, còn bài giảng (lỗi 3) dạy “không phải mọi câu hỏi”. Đây là cảnh báo đúng (dựng ví dụ có số), có dẫn “4–5% trung bình” → giữ.

## Kết quả cuối
- `audit/irs/verify_irs.py`: verify_irs: 123/123 PASS
- `tools/lv.py curriculum curriculum/irs.yaml`: curriculum: 14 bài, 14 đã có đặc tả, 0 lỗi
- `audit/review/scan_ctrl.py`: không có lượt nào ở lessons/irs (8 lượt còn lại thuộc lessons/jva, không phải khoá này)
- `rec()` của IRS trong `audit/verify_plan_curricula.py` không dùng số đã đổi (IRS:L06 chỉ kiểm cosin 0,606; IRS:L13 không có 36,0) → không cần sửa.
