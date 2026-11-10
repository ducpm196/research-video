# Nguồn bài HCI L08 — Thí nghiệm giao diện: trong chủ thể, giữa chủ thể và cân bằng thứ tự

Đọc và tra cứu 2026-11-03. Nhãn dùng trong `source:` của bài.

## [MK13] I. S. MacKenzie, *Human-Computer Interaction: An Empirical Research Perspective*, Morgan Kaufmann, 2013, Chương 5 (“Designing HCI Experiments”, mục 5.10 “Within-subjects and between-subjects” và mục 5.11 “Order effects, counterbalancing, and latin squares”) — số mục và tên mục **VERIFIED 2026-11-09** theo mục lục của NXB (tên mục 5.10 đã sửa: bản gốc là “and”, không phải “vs.”)
| Nội dung / nguyên lý | Dùng ở |
|---|---|
| Thiết kế **trong chủ thể** (*within-subjects*): mỗi người tham gia thử tất cả $k$ điều kiện (giao diện). Ưu điểm: cần ít người hơn và khử được khác biệt cá nhân vì mỗi người tự làm đối chứng cho chính mình. Nhược điểm: chịu hiệu ứng thứ tự (*order effects* — quen tay do học hoặc mỏi mệt) | cảnh khái niệm, hình dung |
| Thiết kế **giữa chủ thể** (*between-subjects*): mỗi người tham gia chỉ thử đúng 1 điều kiện. Ưu điểm: không có hiệu ứng truyền sang giữa các điều kiện. Nhược điểm: cần nhiều người hơn và phương sai giữa các cá nhân lớn có thể che lấp hiệu ứng của giao diện | cảnh khái niệm, lỗi thường gặp |
| Cân bằng thứ tự hoàn toàn với $k$ giao diện cần $k!$ thứ tự ($3! = 6$, $4! = 24$, $5! = 120$). **Hình vuông Latin** (*Latin square*) cỡ $k \times k$ xếp $k$ nhóm sao cho mỗi giao diện xuất hiện ở mỗi vị trí thứ tự (thứ nhất, thứ hai, …, thứ $k$) đúng 1 lần và mỗi hàng chứa đủ $k$ giao diện | cảnh suy ra công thức, ví dụ $3 \times 3$ (`ABC`, `BCA`, `CAB`), tự kiểm |

## Điều KHÔNG dạy / NOT_VERIFIED
- Không đi sâu vào công thức kiểm định phương sai lặp lại (ANOVA hai chiều / Friedman test) — chỉ dừng ở việc khử độ lệch thứ tự bằng trung bình trên hình vuông Latin.
- Các con số thời gian hoàn thành nhiệm vụ cụ thể (ví dụ hiệu ứng quen tay giảm 4 giây ở lượt hai và 8 giây ở lượt ba, hay người nhanh / người chậm chênh nhau 20 giây) là **SỐ MINH HOẠ** để người học thấy cơ chế khử lệch thứ tự và khác biệt cá nhân.
- Trong `say:`, từ `Latin` được phép đọc (theo `lexicon_vi.HCI.yaml` đọc là `La-tinh`); không đọc `MacKenzie` trong `say:`.

## Đối chiếu nguồn mở 2026-11-09 (BN-0040)
- Mục lục [MK13] trên trang NXB Elsevier: https://www.educate.elsevier.com/book/details/9780124058651 — “Chapter 5. Designing HCI Experiments”: 5.9 Questionnaire design; **5.10 Within-subjects and between-subjects**; **5.11 Order effects, counterbalancing, and latin squares**; 5.12 Group effects and asymmetric skill transfer; 5.13 Longitudinal studies. Số mục 5.10/5.11 đúng; tên 5.10 đã sửa theo mục lục.
- Ghi chú nghiên cứu của tác giả https://www.yorku.ca/mack/RN-Counterbalancing.html (cập nhật 29/3/2013, “appears in greater detail … in Chapter 5”): xác nhận cân bằng thứ tự bằng nhóm và hình vuông Latin, có ví dụ 2 × 2, 3 × 3, 4 × 4, 5 × 5.
- Bảng trên là tóm tắt nguyên lý, không phải câu trích; không đọc được nội dung chương 5 (sách không mở) nên các diễn giải ưu/nhược điểm chỉ đối chiếu ở mức ghi chú nghiên cứu. Không thấy mâu thuẫn số liệu ($k!$ thứ tự là phép đếm của bài).
