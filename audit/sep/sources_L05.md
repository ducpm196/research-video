# Nguồn đã đọc nguyên văn cho SEP L05 (rủi ro, kỳ vọng thiệt hại, khi nào phải dừng)

Đọc ngày 2026-11-02. Mọi lỗi A, B, C, R1–R3, xác suất, thiệt hại, số máy là SỐ MINH HOẠ; phép tính kỳ vọng p × D và
1 − (1 − p)^n là toán của bài, tính lại trong `checks` và `audit/sep/verify_parts/L05.py`.

## [ACM18] ACM Code of Ethics and Professional Conduct (2018)
Tải: https://www.acm.org/binaries/content/assets/about/acm-code-of-ethics-and-professional-conduct.pdf (200)
- 1.2: “A computing professional has an additional obligation to report any signs of system risks that might result in harm.”
  … “Before reporting risks, a computing professional should carefully assess relevant aspects of the situation.”
- 2.5: “Extraordinary care should be taken to identify and mitigate potential risks in machine learning systems. A system for which future
  risks cannot be reliably predicted requires frequent reassessment of risk as the system evolves in use, or it should not be deployed.
  Any issues that might result in major risk must be reported to appropriate parties.”
- 2.9: “In cases where misuse or harm are predictable or unavoidable, the best option may be to not implement the system.”

## Sửa giáo án (ghi lại)
- `fix` cũ của L05 viện dẫn CAS L01, L02 như các sự kiện “không thể xảy ra” — chưa có nguồn đọc nguyên văn cho cách nói đó; bài
  không viện dẫn CAS. Thay bằng phát biểu tính được: 0,001 mỗi năm trên 1000 hệ thống → 1 − 0,999^1000 ≈ 0,632 (VER SEP:L05).

## Điều KHÔNG dạy (nguồn không ghi)
- Không dạy chuẩn an toàn chức năng theo ngành (mức toàn vẹn an toàn…) — chưa đọc văn bản chuẩn.
- “Ngưỡng riêng cho hậu quả không đảo ngược được” và các lớp chặn (sao lưu đã thử khôi phục, xác nhận trước khi xoá, giới hạn số bản
  ghi) là thực hành đề xuất của bài, không gán cho bộ quy tắc; bộ quy tắc chỉ được trích ở câu 2.9 nói trên.
- Không dẫn sự cố có thật nào trong bài này.
