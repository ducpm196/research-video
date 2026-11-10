# SEP — đã đọc 12/12 bài

Đọc kiểm 2026-11-08: mọi cảnh, `show`/`say`/`checks`, quiz và đáp án; đối chiếu điều luật (tên, số hiệu, ngày ban hành, ngày hiệu lực) và câu
trích với `audit/sep/sources_L*.md` (Luật 91/2025/QH15 thông qua 26/6/2025, hiệu lực 1/1/2026; Nghị định 13/2023/NĐ-CP ban hành 17/4/2023, hiệu
lực 1/7/2023; Nghị định 356/2025/NĐ-CP ngày 31/12/2025, hiệu lực 1/1/2026; ACM Code 22/6/2018; GPL-3.0 29/6/2007; Apache 2.0; MIT; Project Zero
90+30; npm blog 23/3 và 29/3/2016). Số hiệu và ngày của mọi văn bản đều khớp. Không bài nào sinh từ mẫu. Tổng: **0 MUST, 7 SHOULD** trên 5 bài.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 trách nhiệm nghề nghiệp | không phát hiện lỗi | — (0,99¹⁰⁰ ≈ 0,366; n = 299; ACM 1.1, 1.2, 1.3, 2.5) | ACM Code 2018 (PDF acm.org) | — |
| L01 dữ liệu cá nhân | không phát hiện lỗi | — (Luật 91/2025/QH15 Đ2, Đ3, Đ9, Đ12; Sweeney 87%; 58 400 tổ hợp → 0,843) | [L91], [S00], [ACM18] 1.6 | — |
| L02 công bằng | không phát hiện lỗi | — (phương trình 2.6 Chouldechova kiểm bằng số; 0,025; 0,052) | [C17], [K16] | — |
| L03 giải thích được | không phát hiện lỗi | — | [W17], ACM 1.3, 1.4 | — |
| L04 giấy phép | không phát hiện lỗi | — (MIT, Apache 2.0 §3–§4, GPL-3.0 §0, §5c, §6, “aggregate”) | [MIT], [AP2], [GPL3], [GH] | — |
| L05 rủi ro | không phát hiện lỗi | — (1 − 0,999¹⁰⁰⁰ ≈ 0,632; R3 0,181; ACM 1.2, 2.5, 2.9) | ACM Code 2018 | — |
| L06 môi trường | đã sửa | check.1: SHOULD — “trung bình Mỹ **2020**: 0,429” — câu trích của Patterson 2021 không ghi năm cho 0,429 → “trung bình lưới điện Mỹ (bài báo ghi)”, lời đọc cùng nghĩa, chú thích đầu tệp sửa theo; serving.0: SHOULD — “đo ở Google trong ba năm 2019–2021” → “mỗi năm một tuần tháng 4, từ 2019 tới 2021” đúng phạm vi đo của bài báo | [P21] §2.4; [P22] (“one week of April in 2019, 2020, and 2021”) | lint: 0 FAIL, 0 WARN, 29 PASS; render: 87 khung (0 vấn đề) |
| L07 công bố lỗ hổng | đã sửa | quiz.2: SHOULD — đáp án đếm hạn 7 ngày từ ngày báo (10/3 → 17/3) như điều chắc chắn, trong khi trang chính sách không ghi mốc đếm khi bằng chứng khai thác đến sau → thêm ghi chú “trang chính sách không ghi rõ … bài đếm từ ngày 0; ghi rõ ngày hạn trong thư” (show + say + focus) | Project Zero, Vulnerability Disclosure Policy (đọc 2026-11-02) | lint: 0 FAIL, 0 WARN, 26 PASS; render: 82 khung (0 vấn đề) |
| L08 xung đột lợi ích | đã sửa | objectives: SHOULD — “Áp luật hai bước” trong khi bài dạy ba bước (ràng buộc → tổng → bên yếu thế) → “luật ba bước” | bài tự lập luận từ ACM 1.1, 1.2 | lint: 0 FAIL, 0 WARN, 24 PASS; render: 76 khung (0 vấn đề) |
| L09 ước lượng, cam kết | đã sửa | pitfalls.3: SHOULD — “Im lặng khi biết mình sẽ trễ … (trái nguyên tắc 2.6)”: 2.6 chỉ nói về thiếu chuyên môn; giữ lời hứa và trung thực về giới hạn là 1.3 → “trái nguyên tắc 1.3 và 2.6” | ACM Code 2018 1.3 (“commitments should be honored”), 2.6 | lint: 0 FAIL, 0 WARN, 26 PASS; render: 92 khung (0 vấn đề) |
| L10 left-pad | không phát hiện lỗi | — (22/3/2016 14:30, 273 gói, 0.0.3, 16:05–16:55, 2,5 giờ; chính sách 24 h (2016) và 72 h / 300 lượt / 1 người (hiện hành)) | [N16a], [N16b], [N26] | — |
| L11 hành trình dữ liệu cá nhân | đã sửa | stage5.0: SHOULD — “hồ sơ đánh giá đã nộp vẫn dùng được” gán cho Luật 91 Đ39 nhưng không có trong câu đã trích (chỉ khoản 1 về đồng ý) → bỏ; SHOULD — Đ38.2 / NĐ 356 Đ41 cho DN nhỏ chọn thực hiện “Điều 21, Điều 22 và khoản 2 Điều 33”, bài ghi gọn thành “đánh giá tác động” → ghi đủ phạm vi “(trong đó có đánh giá tác động)” ở show, “một số nghĩa vụ, trong đó có đánh giá tác động” ở lời đọc | Luật 91/2025/QH15 Đ38 k2, Đ39 k1; NĐ 356/2025/NĐ-CP Đ41 k1 | lint: 0 FAIL, 0 WARN, 39 PASS; render: 127 khung (0 vấn đề) |

## Không sửa và vì sao
- L07 hook: “Nhóm phát hiện ghi: tìm ra ngày 3/4/2014” đúng câu của heartbleed.com (nhóm đó tìm ra ngày 3/4); lỗi đã được người khác tìm độc lập trước (bài có nêu “người khác công bố độc lập”). Không nêu thêm ngày của nhóm kia vì chưa có nguồn đã đọc.
- L02: câu “các tiêu chí này không thể cùng thoả” gộp cả cân bằng tỉ lệ chọn; ba điều kiện của Kleinberg không trùng hệt ba tiêu chí của bài, nhưng với tỉ lệ nền khác nhau và bộ lọc không hoàn hảo thì cân bằng lỗi kéo theo tỉ lệ chọn khác nhau (trừ TPR = FPR) — kết luận vẫn đúng; giữ.
- L04 quiz: phát hành qua chợ ứng dụng với gói GPL-3.0 còn vướng điều khoản của chợ ứng dụng — ngoài văn bản đã đọc; bài đã khuyên hỏi chuyên môn pháp lý.
- L11: không đối chiếu được lại PDF ký số trong phiên (ảnh quét); dựa vào câu đã chép nguyên văn ngày 2026-11-02 trong `audit/sep/sources_L11.md`.
- `rec()` của SEP trong `audit/verify_plan_curricula.py` không cần đổi (không đổi số nào).

## Kết quả bộ kiểm
- `audit/sep/verify_sep.py`: **verify_sep: 66/66 PASS**
- `tools/lv.py curriculum curriculum/sep.yaml`: **curriculum: 12 bài, 12 đã có đặc tả, 0 lỗi**
- `audit/review/scan_ctrl.py`: không có lượt nào ở `lessons/sep/`.
