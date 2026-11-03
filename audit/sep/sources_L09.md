# Nguồn đã đọc nguyên văn cho SEP L09 (ước lượng, cam kết và nói “chưa được”)

Đọc ngày 2026-11-02 (bản PDF chính thức trên acm.org, trích chữ bằng pdftotext; câu dưới đây chép nguyên văn).
Công thức ước lượng ba điểm E = (O + 4M + B)/6 và s = (B − O)/6 được dạy như một phương pháp toán (“cách ước lượng ba điểm hay dùng
trong quản lý dự án”), KHÔNG gán cho tác giả hay tài liệu nào — nguồn gốc chưa đọc nguyên văn (NOT_VERIFIED). Mọi số ngày là SỐ MINH
HOẠ; tính lại ở `checks` và `audit/sep/verify_parts/L09.py` (phân số chính xác, mô phỏng phân bố beta–PERT có trung bình đúng bằng E).

## [ACM18] ACM Code of Ethics and Professional Conduct (2018)
Tải: https://www.acm.org/binaries/content/assets/about/acm-code-of-ethics-and-professional-conduct.pdf
- 1.3: “Computing professionals should be honest about their qualifications, and about any limitations in their competence to complete a
  task. … Furthermore, commitments should be honored.”
- 2.6: “If at any time before or during the work assignment the professional identifies a lack of a necessary expertise, they must
  disclose this to the employer or client. The client or employer may decide to pursue the assignment with the professional after
  additional time to acquire the necessary competencies, to pursue the assignment with someone else who has the required expertise, or
  to forgo the assignment.”

## Điều KHÔNG dạy
- Không nói khoảng E ± 2s chứa kết quả với một xác suất nào (cần giả định phân bố; bài chỉ dùng nó như cách báo độ chắc).
- Không gán phương pháp ba điểm cho một chương trình hay năm cụ thể.
- “Ước lượng không phải đàm phán” là lập luận của bài (giáo án `fix`), không trích từ nguồn.
- Cộng độ lệch theo căn tổng bình phương chỉ đúng khi các việc độc lập — bài nói rõ điều kiện này.
