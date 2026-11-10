# LLM — đã đọc 15/15 bài

Người đọc: tác tử đợt B, 2026-11-08. Đọc mọi cảnh (`show`, `say`, `checks`, quiz, đáp án) qua bản trích chữ của từng tệp; L14 đối chiếu từng con số với `audit/llm/sources_L14.md`. Bài không sinh từ mẫu (`audit/llm/src/` không tồn tại), nên không cần `sync_tpl_from_lesson.py`.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | đã sửa | pitfalls: SHOULD — “câu dài **luôn** có xác suất nhỏ hơn” sai khi so hai câu khác nhau (chỉ đúng với câu kéo dài từ câu ngắn) → “thường” | Jurafsky–Martin, SLP bản 3 (nháp 2024), §3.2 (chuẩn hoá theo độ dài, độ hỗn loạn) | lint: 0 FAIL, 0 WARN, 18 PASS; render: 53 khung (0 vấn đề) |
| L01 | không phát hiện lỗi | — (đã tính lại: 1,225; 1/504; 4,738; 1/64; 2,828; 1,732; 6) | — | — |
| L02 | đã sửa | hook: SHOULD — “**hầu hết** mô hình ngôn ngữ lớn dùng” BPE: không kiểm được, nhiều mô hình dùng WordPiece/Unigram → “nhiều mô hình”; xoá mục `asr_reviewed` cũ của câu này | Sennrich và cộng sự 2016 (BPE); Kudo 2018, *Subword Regularization* (Unigram); Devlin và cộng sự 2019 (BERT, WordPiece) | lint: 0 FAIL, 0 WARN, 21 PASS; render: 54 khung (0 vấn đề) |
| L03 | không phát hiện lỗi | — (đã tính lại 0,956; 0,99; 0,263; 0,707) | — | — |
| L04 | đã sửa | pitfalls lỗi 2: SHOULD — “không có vị trí thì phép chú ý cho cùng kết quả ở mỗi từ” chỉ đúng khi KHÔNG có mặt nạ; với mặt nạ nhân quả, thứ tự lộ gián tiếp → thêm điều kiện; lỗi 3: SHOULD — “muốn mô hình suy nghĩ **phải** viết bước trung gian” quá tuyệt đối → “thường giúp làm đúng hơn” | Haviv và cộng sự 2022, *Transformer Language Models without Positional Encodings Still Learn Positional Information* (arXiv 2203.16634); Wei và cộng sự 2022, *Chain-of-Thought Prompting* (arXiv 2201.11903) | lint: 0 FAIL, 0 WARN, 17 PASS; render: 53 khung (0 vấn đề) |
| L05 | đã sửa | pitfalls lỗi 3 (`say`): SHOULD — “Các mô hình **mới** chia sẻ khoá” mang tính thời điểm, lại lệch màn hình → “Nhiều mô hình” | Ainslie và cộng sự 2023, GQA (arXiv 2305.13245) | lint: 0 FAIL, 0 WARN, 31 PASS; render: 84 khung (0 vấn đề) |
| L06 | đã sửa | tiêu đề hook: SHOULD — “quyết định **hàng triệu đô**” không nguồn, và không khớp ví dụ 681 ngày-thẻ → “quyết định ngân sách huấn luyện”; pitfalls lỗi 2: SHOULD — “chi phí phục vụ **mỗi ngày** lớn hơn chi phí huấn luyện” sai/không nguồn → “tổng chi phí phục vụ suốt thời gian dùng có thể vượt” | Sardana, Frankle 2023, *Beyond Chinchilla-Optimal: Accounting for Inference* (arXiv 2401.00448) | lint: 0 FAIL, 0 WARN, 17 PASS; render: 55 khung (0 vấn đề) |
| L07 | không phát hiện lỗi | — (đã tính lại phân phối ở T = 0,5/1/2, top-p) | — | — |
| L08 | đã sửa | quiz câu 2: SHOULD — “khởi tạo ngẫu nhiên thì **làm hỏng** mô hình” quá tuyệt đối; LoRA khởi tạo A ngẫu nhiên, B = 0 → “nếu cả hai ma trận đều ngẫu nhiên, mô hình lệch khỏi trọng số ban đầu trước khi học được gì” | Hu và cộng sự 2022, LoRA, §4.1 (A Gauss, B = 0) | lint: 0 FAIL, 0 WARN, 17 PASS; render: 48 khung (0 vấn đề) |
| L09 | không phát hiện lỗi | — | — | — |
| L10 | đã sửa | pitfalls lỗi 1: **MUST** — “cùng chênh 2 điểm” với bất đồng 70/30 trên bộ 500 câu là sai số (70 − 30 = 40 câu = 8 điểm); sửa thành bộ 2000 câu (40/2000 = 2 điểm), thêm `checks` `(70 - 30) / 2000 == 0.02`; “khác biệt thật” → “gần như chắc là khác biệt thật” | tính lại; McNemar 1947 / kiểm định dấu | lint: 0 FAIL, 0 WARN, 18 PASS; render: 52 khung (0 vấn đề) |
| L11 | đã sửa | pitfalls lỗi 2: **MUST** — “lợi ích giảm **hơn** một nửa” sai: 0,5·0,6 + 0,5·0,683 cho đúng một nửa lợi ích → “chỉ còn một nửa”, thêm `checks`; example bước 3, lỗi 1, recap: SHOULD — “đa số đúng khi ≥ 3/5 đúng” và “biểu quyết chỉ có ích khi trên 50%” chỉ đúng khi mọi lần sai ra CÙNG một đáp án; tự nhất quán lấy đáp án nhiều nhất (đa số tương đối) → thêm điều kiện “trường hợp xấu nhất” | Wang và cộng sự 2023, *Self-Consistency*, §2 (lấy đáp án xuất hiện nhiều nhất) | lint: 0 FAIL, 0 WARN, 19 PASS; render: 57 khung (0 vấn đề) |
| L12 | đã sửa | example bước 4: **MUST** — “câu 3 không bao giờ tìm thấy đoạn đúng, **dù tăng k**” mâu thuẫn với đáp án quiz (“tăng k có thể lấy được”) → “không có đoạn đúng trong cả 3 đoạn được lấy”; prereq: SHOULD — “cô-sin càng gần 1 càng cùng nghĩa” mâu thuẫn bài 3 (gần ≠ đồng nghĩa) → “càng cùng hướng, thường là càng gần nghĩa” | Manning, Raghavan, Schütze, *Introduction to Information Retrieval* (2008), ch. 8 (độ phủ theo k); LLM bài 3 | lint: 0 FAIL, 0 WARN, 16 PASS; render: 59 khung (0 vấn đề) |
| L13 | không phát hiện lỗi | — (đã kiểm công thức Leviathan và cộng sự 2023 (1 − α^(k+1))/(1 − α), 3,36; 2,3; 64; 256) | — | — |
| L14 | không phát hiện lỗi | — (đối chiếu từng con số với sources_L14.md: 12 giờ / 3,5 ngày, 2,3·10¹⁹, 8^0,74, 5 × 2, 174,6 tỉ, 3,14·10²³, 3640 PF-ngày, 1,3%, 5,76·10²³, 20,2/21,1, 67,5 − 60,0, 21,2 nghìn tỉ) | audit/llm/sources_L14.md | — |

Tổng: 9 bài sửa; 3 mục MUST, 11 mục SHOULD.

Giáo án `curriculum/llm.yaml` sửa cho khớp bài: L04 `fix` (thêm “và không có mặt nạ”), L06 `fix` (bỏ “hiện nay” mang tính thời điểm), L11 `example` (thêm “coi các lần sai cùng một đáp án”). `rec()` LLM:L04/L06/L11 của `verify_plan_curricula.py` không cần đổi (số không đổi).

## Không sửa và vì sao
- L08 hook: “16 byte mỗi tham số … chỉ cho trọng số và trạng thái” — theo ZeRO, 16 byte gồm cả đạo hàm (2 + 2 + 12); “trạng thái” đủ rộng để hiểu, không sai số liệu.
- L13 lỗi 2: “nửa byte thường làm mô hình kém đi ở một số việc (toán, mã)” — có chữ “thường … một số”, hợp với các báo cáo lượng tử hoá, không có con số cụ thể nên giữ.
- L03 lỗi 2: “vector của từ hay gặp thường dài hơn” — có chữ “thường”; quan hệ độ dài–tần số không đơn điệu ở mọi mô hình, nhưng câu không tuyệt đối.
- L09 lỗi 3: “câu tự tin thường được chấm cao hơn câu thận trọng, kể cả khi sai” — có nghiên cứu ủng hộ (Hosking và cộng sự 2024, *Human Feedback is not Gold Standard*), giữ nguyên.
- L07 hook: “hỏi hai lần, nhận hai câu trả lời khác nhau” — đúng khi lấy mẫu; chính bài giải thích điều kiện ngay sau đó.

## Kết quả bộ kiểm
- `audit/llm/verify_llm.py`: TỔNG: 18 PASS · 0 FAIL
- `tools/lv.py curriculum curriculum/llm.yaml`: curriculum: 15 bài, 15 đã có đặc tả, 0 lỗi
- `audit/verify_plan_curricula.py`: TỔNG: 521 PASS · 0 FAIL
- `audit/review/scan_ctrl.py`: không có lượt nào ở `lessons/llm`
