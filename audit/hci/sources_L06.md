# Nguồn bài HCI L06 — Kiểm thử khả dụng: bao nhiêu người thử là đủ

Đọc và tra cứu 2026-11-03. Nhãn dùng trong `source:` của bài.

## [NL93] J. Nielsen, T. K. Landauer, “A mathematical model of the finding of usability problems”, INTERCHI ’93 (Proceedings of the INTERACT ’93 and CHI ’93 Conference on Human Factors in Computing Systems), trang 206–213, 1993
| Câu trích nguyên văn / kết quả | Dùng ở |
|---|---|
| “$\text{Found}(i) = N(1 - (1 - \lambda)^i)$” — trong đó $i$ (hoặc $n$) là số người thử độc lập, $\lambda$ là xác suất trung bình một người thử gặp và bộc lộ một vấn đề khả dụng | cảnh suy ra công thức, ví dụ, tự kiểm |
| Giá trị trung bình $\lambda \approx 0{,}31$ (31%) qua các dự án kiểm thử người dùng mà hai tác giả khảo sát | hook, ví dụ 5 người ($1 - 0{,}69^5 \approx 84{,}4\%$) và 15 người ($1 - 0{,}69^{15} \approx 99{,}6\%$) |
| Lợi ích kinh tế giảm dần khi tăng số người thử trong cùng một vòng; chia ngân sách thành nhiều vòng thử nhỏ sau mỗi đợt sửa lỗi tìm được nhiều vấn đề thật sự hơn | ví dụ so sánh 1 vòng 15 người với 3 vòng 5 người |
| Giá trị $\lambda$ khác nhau đáng kể giữa các dự án (phụ thuộc độ phức tạp hệ thống và độ đồng nhất của nhóm người dùng) | cảnh lỗi thường gặp (`fix` của giáo án) |

## Điều KHÔNG dạy / NOT_VERIFIED
- Không dạy công thức chi phí – lợi ích đầy đủ có tham số chi phí cố định và chi phí biến đổi trên mỗi người thử của [NL93] (không cần cho mục tiêu bài).
- Các con số tổng số lỗi cụ thể trên một sản phẩm giả định (ví dụ 20 lỗi ở vòng 1, sửa xong lộ thêm 10 lỗi ở vòng 2, và trường hợp lỗi khó có $\lambda = 0{,}10$) là **SỐ MINH HOẠ** được kiểm chứng bằng `alg.hci_nielsen_found` trong `checks`.
- Không đọc tên riêng `Nielsen`, `Landauer`, `INTERCHI` trong `say:` — chỉ hiển thị trên màn hình; lời đọc nói “hai nhà nghiên cứu năm 1993”.
