# Nguồn bài HCI L09 — Truy cập cho mọi người: kích thước đích, bàn phím, trình đọc màn hình

Đọc và tra cứu 2026-11-03. Nhãn dùng trong `source:` của bài.

## [WCAG22] W3C Recommendation, *Web Content Accessibility Guidelines (WCAG) 2.2*, 5 October 2023 — https://www.w3.org/TR/WCAG22/
| Tiêu chí & Câu trích nguyên văn | Dùng ở |
|---|---|
| **Success Criterion 2.5.8 Target Size (Minimum) (Level AA):** “The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except where: Spacing: Undersized targets (those less than 24 by 24 CSS pixels) are positioned so that if a 24 CSS pixel diameter circle is centered on the bounding box of each, the circles do not intersect another target or the circle for another undersized target…” | cảnh ký hiệu, suy ra, ví dụ, lỗi thường gặp |
| **Success Criterion 2.5.5 Target Size (Enhanced) (Level AAA)** (có từ WCAG 2.1, giữ ở 2.2): “The size of the target for pointer inputs is at least 44 by 44 CSS pixels…” | cảnh ví dụ so sánh đích 24 px và 44 px theo định luật thời gian trỏ |
| **Guideline 2.1 Keyboard Accessible (2.1.1 Keyboard, 2.1.2 No Keyboard Trap, 2.4.7 Focus Visible):** mọi chức năng vận hành được qua giao diện bàn phím mà không bị kẹt tiêu điểm; **4.1.2 Name, Role, Value:** thành phần giao diện có tên và vai trò xác định được bằng chương trình cho trình đọc màn hình | cảnh khái niệm, lỗi thường gặp |

## [MK92] I. S. MacKenzie, “Fitts’ Law as a Research and Design Tool in Human-Computer Interaction”, *Human-Computer Interaction*, 1992 (đã học ở HCI L02)
| Công thức | Dùng ở |
|---|---|
| $T = a + b \cdot \log_2(D / W + 1)$: với $D = 200\text{ px}, a = 0{,}1\text{ s}, b = 0{,}15\text{ s/bit}$, mở rộng đích từ $W = 24\text{ px}$ lên $W = 44\text{ px}$ giảm thời gian trỏ từ $\approx 0{,}583\text{ s}$ xuống $\approx 0{,}471\text{ s}$ | cảnh ví dụ, tự kiểm (`alg.hci_fitts_time`) |

## Điều KHÔNG dạy / NOT_VERIFIED
- Không dạy danh sách đầy đủ mọi thuộc tính `aria-*` của WAI-ARIA 1.2 (đã có phần kỹ thuật web ở WEB L11; bài này tập trung vào đo lường khả năng truy cập bằng định luật thời gian trỏ và kiểm thử thao tác).
- Không đọc `WCAG`, `W3C`, `Fitts`, `CSS`, `HTML`, `ARIA`, `px` trong `say:` — lời đọc nói “bộ chuẩn tiếp cận web”, “định luật thời gian trỏ”, “điểm ảnh”.
