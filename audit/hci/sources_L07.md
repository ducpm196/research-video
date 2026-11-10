# Nguồn bài HCI L07 — Đo cảm nhận: thang khả dụng hệ thống SUS

Đọc và tra cứu 2026-11-03. Nhãn dùng trong `source:` của bài.

## [B96] J. Brooke, “SUS: A ‘Quick and Dirty’ Usability Scale”, trong *Usability Evaluation in Industry*, P. W. Jordan, B. Thomas, B. A. Weerdmeester, I. L. McClelland (chủ biên), Taylor & Francis, trang 189–194, 1996
| Câu trích nguyên văn / quy tắc (đối chiếu 2026-11-09 với bản thảo tác giả, mục *Scoring SUS*) | Dùng ở |
|---|---|
| Bảng hỏi gồm 10 phát biểu, thang 5 mức từ 1 (“Strongly disagree” — rất không đồng ý) tới 5 (“Strongly agree” — rất đồng ý), xen kẽ câu khen (lẻ: 1, 3, 5, 7, 9) và câu chê (chẵn: 2, 4, 6, 8, 10) để tránh người trả lời đánh máy móc một cột — **VERIFIED 2026-11-09** (diễn giải đúng): “a simple, ten-item scale”; bảng hỏi ghi nhãn “Strongly disagree … Strongly agree”, mức 1–5; “by alternating positive and negative items, the respondent has to read each statement and make an effort to think whether they agree or disagree with it.” | cảnh ký hiệu, hình dung, suy ra công thức |
| “For items 1,3,5,7,and 9 the score contribution is the scale position minus 1. For items 2,4,6,8 and 10, the contribution is 5 minus the scale position. Multiply the sum of the scores by 2.5 to obtain the overall value of SU.” — **VERIFIED 2026-11-09**, mục *Scoring SUS* (đã chép đúng dấu câu của bản gốc: “1,3,5,7,and 9”, “2,4,6,8 and 10”) | cảnh suy ra công thức, ví dụ tính điểm từ 10 câu trả lời `[4, 2, 4, 1, 5, 2, 4, 2, 4, 1]` → $(16 + 17) \cdot 2{,}5 = 82{,}5$ |
| “SUS scores have a range of 0 to 100.” — **VERIFIED 2026-11-09**, mục *Scoring SUS*; tuy nằm trên thang 0–100 nhưng không phải tỉ lệ phần trăm | cảnh lỗi thường gặp (`fix` của giáo án) |

## [BKM08] A. Bangor, P. T. Kortum, J. T. Miller, “An Empirical Evaluation of the System Usability Scale”, *International Journal of Human-Computer Interaction*, 24(6), trang 574–594, 2008 (và tổng hợp ngành xoay quanh mốc 68)
| Kết quả (trạng thái đối chiếu 2026-11-09) | Dùng ở |
|---|---|
| **NOT_VERIFIED (không mở được nguồn)**: Khảo sát 2324 phiếu qua 206 nghiên cứu cho trung bình theo nghiên cứu 69,69 (trung bình theo phiếu 70,14); mốc chuẩn ngành thường lấy quanh 68 là mức trung bình (trung vị / bách phân vị 50) — chưa đọc được bài [BKM08] hay bài tổng hợp nào nêu các số 2324 / 206 / 69,69 / 70,14 / 68 | cảnh lỗi thường gặp: điểm 68 là quanh mức trung bình của nhiều nghiên cứu, không phải “68% người dùng hài lòng” |

## Điều KHÔNG dạy / NOT_VERIFIED
- Không dạy cấu trúc hai nhân tố (“Usability” 8 câu và “Learnability” câu 4, 10) của các nghiên cứu phân tích nhân tố về sau (NOT_VERIFIED chi tiết hệ số tải nhân tố).
- Bộ 10 câu trả lời `[4, 2, 4, 1, 5, 2, 4, 2, 4, 1]` và các bộ câu trả lời ở phần tự kiểm / tự làm là **SỐ MINH HOẠ** được kiểm bằng `alg.hci_sus_score`.
- Không đọc `SUS`, `Brooke`, `Bangor`, `Kortum`, `Miller` trong `say:` — lời đọc nói “thang khả dụng hệ thống mười câu”.

## Đối chiếu nguồn mở 2026-11-09 (BN-0040)
- [B96]: bản thảo của tác giả (John Brooke, Redhatch Consulting; trang bìa ResearchGate publication 228593520, “uploaded by John Brooke on 31 July 2020”), tệp chép lại tại https://code.metalisp.dev/marcuskammer/emacs.d/raw/commit/9a28c3b0351b5a630e02f042822da2e81be7b52a/ux/SUSCHAPT.pdf (8 trang, có lớp chữ). Đây là bản thảo, **không có số trang sách 189–194**; trích dẫn ghi theo tên mục (*SUS - the System Usability Scale*, *Scoring SUS*). Ba dòng [B96] VERIFIED. Ví dụ trong bản thảo: tổng 22 → 22 × 2,5 = 55.
- [BKM08]: không mở được. uxpajournal.org (Bangor 2009, Lewis 2018) trả HTML/404 cho tệp PDF; không có bản mở của IJHCI 24(6). Cả dòng số liệu để NOT_VERIFIED; cần đọc bài gốc trước khi giữ 69,69 / 70,14 / 206 trong bài học.
- Brooke 2013 “SUS: A Retrospective” (JUS 8(2)) chưa mở được (cùng lỗi tên miền uxpajournal.org).
