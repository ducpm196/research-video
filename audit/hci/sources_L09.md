# Nguồn bài HCI L09 — Truy cập cho mọi người: kích thước đích, bàn phím, trình đọc màn hình

Đọc và tra cứu 2026-11-03. Nhãn dùng trong `source:` của bài.

## [WCAG22] W3C Recommendation, *Web Content Accessibility Guidelines (WCAG) 2.2*, 5 October 2023 — https://www.w3.org/TR/WCAG22/
| Tiêu chí & Câu trích nguyên văn | Dùng ở |
|---|---|
| **Success Criterion 2.5.8 Target Size (Minimum) (Level AA):** “The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except where: Spacing: Undersized targets (those less than 24 by 24 CSS pixels) are positioned so that if a 24 CSS pixel diameter circle is centered on the bounding box of each, the circles do not intersect another target or the circle for another undersized target…” — **VERIFIED 2026-11-09** đúng nguyên văn bản Khuyến nghị 5/10/2023 (mã nguồn W3C, thẻ `WCAG22-20231005`). Lưu ý: bản cập nhật 12/12/2024 (thẻ `WCAG22-20241212`, hiện là bản tại w3.org/TR/WCAG22/) đổi “except where:” thành “**except when:**”; ngoại lệ Spacing giữ nguyên chữ. Các ngoại lệ còn lại bị lược: Equivalent, Inline, User agent control, Essential | cảnh ký hiệu, suy ra, ví dụ, lỗi thường gặp |
| **Success Criterion 2.5.5 Target Size (Enhanced) (Level AAA)** (có từ WCAG 2.1, giữ ở 2.2): “The size of the target for pointer inputs is at least 44 by 44 CSS pixels…” — **VERIFIED 2026-11-09** (câu đầy đủ: “… at least 44 by 44 CSS pixels except when:” rồi bốn ngoại lệ). Ở WCAG 2.1 tiêu chí này tên là “**Target Size**” (AAA); hậu tố “(Enhanced)” mới có từ WCAG 2.2 | cảnh ví dụ so sánh đích 24 px và 44 px theo định luật thời gian trỏ |
| **Guideline 2.1 Keyboard Accessible (2.1.1 Keyboard, 2.1.2 No Keyboard Trap)** và **2.4.7 Focus Visible** — *đã sửa 2026-11-09*: 2.4.7 thuộc **Guideline 2.4 Navigable**, không thuộc 2.1 (bản cũ xếp nhầm vào ngoặc của 2.1). Diễn giải, không phải câu trích nguyên văn: mọi chức năng vận hành được qua giao diện bàn phím mà không bị kẹt tiêu điểm; **4.1.2 Name, Role, Value:** thành phần giao diện có tên và vai trò xác định được bằng chương trình cho trình đọc màn hình | cảnh khái niệm, lỗi thường gặp |

## [MK92] I. S. MacKenzie, “Fitts’ Law as a Research and Design Tool in Human-Computer Interaction”, *Human-Computer Interaction*, 1992 (đã học ở HCI L02)
| Công thức | Dùng ở |
|---|---|
| $T = a + b \cdot \log_2(D / W + 1)$: với $D = 200\text{ px}, a = 0{,}1\text{ s}, b = 0{,}15\text{ s/bit}$, mở rộng đích từ $W = 24\text{ px}$ lên $W = 44\text{ px}$ giảm thời gian trỏ từ $\approx 0{,}583\text{ s}$ xuống $\approx 0{,}471\text{ s}$ | cảnh ví dụ, tự kiểm (`alg.hci_fitts_time`) |

## Điều KHÔNG dạy / NOT_VERIFIED
- Không dạy danh sách đầy đủ mọi thuộc tính `aria-*` của WAI-ARIA 1.2 (đã có phần kỹ thuật web ở WEB L11; bài này tập trung vào đo lường khả năng truy cập bằng định luật thời gian trỏ và kiểm thử thao tác).
- Không đọc `WCAG`, `W3C`, `Fitts`, `CSS`, `HTML`, `ARIA`, `px` trong `say:` — lời đọc nói “bộ chuẩn tiếp cận web”, “định luật thời gian trỏ”, “điểm ảnh”.

## Đối chiếu nguồn mở 2026-11-09 (BN-0040)
- w3.org/TR/WCAG22/ trả trang kiểm tra Cloudflare (“Just a moment…”, HTTP 403 với trình tải) ngày 2026-11-09. Đã đọc mã nguồn chính thức của W3C trên GitHub, theo thẻ phát hành:
  - https://raw.githubusercontent.com/w3c/wcag/WCAG22-20231005/guidelines/sc/22/target-size-minimum.html — 2.5.8 “… except where:” + ngoại lệ Spacing khớp nguyên văn.
  - https://raw.githubusercontent.com/w3c/wcag/WCAG22-20241212/guidelines/sc/22/target-size-minimum.html — bản cập nhật 12/12/2024: “… except when:”.
  - https://raw.githubusercontent.com/w3c/wcag/WCAG22-20231005/guidelines/sc/21/target-size-enhanced.html và …/WCAG21-20230921/guidelines/sc/21/target-size.html — 2.5.5 “… at least 44 by 44 CSS pixels except when:”; tên ở 2.1 là “Target Size”.
  - https://raw.githubusercontent.com/w3c/wcag/WCAG22-20231005/guidelines/index.html — tiêu đề nhóm: “Keyboard Accessible” (2.1), “Navigable” (2.4).
- Kết quả: 2.5.8 và 2.5.5 VERIFIED; đã sửa việc xếp 2.4.7 vào Guideline 2.1. Phép tính Fitts $D = 200$, $W = 24 \to 44$: $0{,}1 + 0{,}15\log_2(200/24+1) \approx 0{,}583$ s và $0{,}1 + 0{,}15\log_2(200/44+1) \approx 0{,}471$ s — đúng.
