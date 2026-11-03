# Nguồn đã đọc nguyên văn cho SEP L08 (ra quyết định khi các bên xung đột lợi ích)

Đọc ngày 2026-11-02 (bản PDF chính thức trên acm.org, trích chữ bằng pdftotext; câu dưới đây chép nguyên văn).
Mọi điểm ảnh hưởng (ứng dụng giao đồ ăn: X, Y, Z; trường học: A, B, C, D) là SỐ MINH HOẠ — chấm điểm là ý kiến của con người.
Luật chọn ba bước (ràng buộc → tổng → bên yếu thế) là công cụ của bài, dựng từ câu 1.1 và 1.2 dưới đây; không gán cho ACM như một
“thuật toán” (chính bộ quy tắc nói nó không phải thuật toán). Tính lại ở `checks` và `audit/sep/verify_parts/L08.py`.

## [ACM18] ACM Code of Ethics and Professional Conduct (2018)
Tải: https://www.acm.org/binaries/content/assets/about/acm-code-of-ethics-and-professional-conduct.pdf
- 1.1: “When the interests of multiple groups conflict, the needs of those less advantaged should be given increased attention and priority.”
- 1.2: “Avoiding harm begins with careful consideration of potential impacts on all those affected by decisions. … In either case, ensure
  that all harm is minimized.”
- Lời mở đầu: “The entire computing profession benefits when the ethical decision-making process is accountable to and transparent to all
  stakeholders.”
- Lời mở đầu: “The Code is not an algorithm for solving ethical problems; rather it serves as a basis for ethical decision-making.”

## Sai sót trong giáo án (đã báo người điều phối)
- `curriculum/sep.yaml` L08 example: “3 phương án × 4 bên, chấm −2 đến 2” nhưng X = [2, 2, 3, −2] (VER SEP:L08 cùng số) — điểm 3 nằm
  ngoài thang −2…2. Với thang −2…2 và một bên −2, tổng lớn nhất có thể là 2 + 2 + 2 − 2 = 4, nên “tổng 5” không xảy ra được. Bài dùng
  X = [2, 2, 2, −2], tổng 4 (vẫn cao nhất; Y = [1, 1, 1, 0], Z = [0, 1, 1, 1] tổng 3). Cần sửa example + VER SEP:L08.

## Điều KHÔNG dạy
- Không nêu tên công ty giao đồ ăn hay trường học thật; tình huống là minh hoạ.
- Không nói luật ba bước là chuẩn của ngành hay của ACM.
