# Nguồn bài HCI L07 — Đo cảm nhận: thang khả dụng hệ thống SUS

Đọc và tra cứu 2026-11-03. Nhãn dùng trong `source:` của bài.

## [B96] J. Brooke, “SUS: A ‘Quick and Dirty’ Usability Scale”, trong *Usability Evaluation in Industry*, P. W. Jordan, B. Thomas, B. A. Weerdmeester, I. L. McClelland (chủ biên), Taylor & Francis, trang 189–194, 1996
| Câu trích nguyên văn / quy tắc | Dùng ở |
|---|---|
| Bảng hỏi gồm 10 phát biểu, thang 5 mức từ 1 (“Strongly disagree” — rất không đồng ý) tới 5 (“Strongly agree” — rất đồng ý), xen kẽ câu khen (lẻ: 1, 3, 5, 7, 9) và câu chê (chẵn: 2, 4, 6, 8, 10) để tránh người trả lời đánh máy móc một cột | cảnh ký hiệu, hình dung, suy ra công thức |
| “For items 1, 3, 5, 7, and 9 the score contribution is the scale position minus 1. For items 2, 4, 6, 8, and 10, the contribution is 5 minus the scale position. Multiply the sum of the scores by 2.5 to obtain the overall value of SU.” | cảnh suy ra công thức, ví dụ tính điểm từ 10 câu trả lời `[4, 2, 4, 1, 5, 2, 4, 2, 4, 1]` → $(16 + 17) \cdot 2{,}5 = 82{,}5$ |
| “SUS scores have a range of 0 to 100.” — tuy nằm trên thang 0–100 nhưng không phải tỉ lệ phần trăm | cảnh lỗi thường gặp (`fix` của giáo án) |

## [BKM08] A. Bangor, P. T. Kortum, J. T. Miller, “An Empirical Evaluation of the System Usability Scale”, *International Journal of Human-Computer Interaction*, 24(6), trang 574–594, 2008 (và tổng hợp ngành xoay quanh mốc 68)
| Kết quả | Dùng ở |
|---|---|
| Khảo sát 2324 phiếu qua 206 nghiên cứu cho trung bình theo nghiên cứu 69,69 (trung bình theo phiếu 70,14); mốc chuẩn ngành thường lấy quanh 68 là mức trung bình (trung vị / bách phân vị 50) | cảnh lỗi thường gặp: điểm 68 là quanh mức trung bình của nhiều nghiên cứu, không phải “68% người dùng hài lòng” |

## Điều KHÔNG dạy / NOT_VERIFIED
- Không dạy cấu trúc hai nhân tố (“Usability” 8 câu và “Learnability” câu 4, 10) của các nghiên cứu phân tích nhân tố về sau (NOT_VERIFIED chi tiết hệ số tải nhân tố).
- Bộ 10 câu trả lời `[4, 2, 4, 1, 5, 2, 4, 2, 4, 1]` và các bộ câu trả lời ở phần tự kiểm / tự làm là **SỐ MINH HOẠ** được kiểm bằng `alg.hci_sus_score`.
- Không đọc `SUS`, `Brooke`, `Bangor`, `Kortum`, `Miller` trong `say:` — lời đọc nói “thang khả dụng hệ thống mười câu”.
