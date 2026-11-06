# Nguồn bài HCI L12 — Hành trình: chuẩn tiếp cận web từ 14 hướng dẫn năm 1999 tới tiêu chí đo được năm 2008–2023

Đọc và tra cứu 2026-11-03 từ các khuyến nghị chính thức của W3C. Nhãn dùng trong `stage.source` và `source:` của bài.

## [W99] W3C Recommendation, *Web Content Accessibility Guidelines 1.0*, 5 May 1999 — https://www.w3.org/TR/WCAG10/
| Câu trích / Con số | Dùng ở |
|---|---|
| Ban hành ngày 5/5/1999; gồm **14 hướng dẫn** (*guidelines*) và **65 điểm kiểm** (*checkpoints*) chia làm 3 mức ưu tiên: **Priority 1** (16 điểm kiểm), **Priority 2** (30 điểm kiểm), **Priority 3** (19 điểm kiểm) → $16 + 30 + 19 = 65$ | chặng 1 (1999), tự kiểm |
| Điểm nghẽn: nhiều điểm kiểm gắn chặt vào công nghệ HTML thời kỳ đầu (ví dụ “Until user agents allow users to…”) và diễn đạt định tính nên khó kiểm thử nhất quán khi web chuyển sang ứng dụng động | chặng 1 điểm nghẽn |

## [W08] W3C Recommendation, *Web Content Accessibility Guidelines (WCAG) 2.0*, 11 December 2008 — https://www.w3.org/TR/WCAG20/
| Câu trích / Con số | Dùng ở |
|---|---|
| Ban hành ngày 11/12/2008; tổ chức theo **4 nguyên tắc** (*Perceivable, Operable, Understandable, Robust* — cảm nhận được, vận hành được, hiểu được, vững chắc), **12 hướng dẫn**, và **61 tiêu chí thành công kiểm chứng được** (*testable success criteria*) chia theo 3 mức A, AA, AAA | chặng 2 (2008) |
| Công thức tỉ lệ tương phản (*contrast ratio*): $(L_1 + 0{,}05) / (L_2 + 0{,}05)$ với $L_1 \ge L_2 \in [0, 1]$. Giữa trắng ($L_1 = 1$) và đen ($L_2 = 0$): $(1 + 0{,}05)/(0 + 0{,}05) = 1{,}05 / 0{,}05 = 21:1$. Tiêu chí **1.4.3 Contrast (Minimum) (Level AA)** yêu cầu tối thiểu **4,5:1** cho chữ thường (3:1 cho chữ lớn) | chặng 2 phép tính, tự kiểm |

## [W18] W3C Recommendation, *Web Content Accessibility Guidelines (WCAG) 2.1*, 5 June 2018 — https://www.w3.org/TR/WCAG21/
| Câu trích / Con số | Dùng ở |
|---|---|
| Ban hành ngày 5/6/2018; giữ nguyên 61 tiêu chí của 2.0 và **thêm 17 tiêu chí mới** ($61 + 17 = 78$ tiêu chí) nhằm giải quyết điểm nghẽn trên thiết bị di động màn hình cảm ứng, người nhìn kém (*low vision*) và nhận thức | chặng 3 (2018) |
| **1.4.10 Reflow (Level AA):** nội dung dòng lại ở chiều rộng tương đương **320 CSS pixels** mà không phải cuộn hai chiều — tương ứng khung nhìn máy tính **1280 CSS px** khi phóng đại **400%** ($1280 / 4 = 320\text{ px}$) | chặng 3 phép tính, tự kiểm |
| **2.5.5 Target Size (Level AAA):** đích con trỏ tối thiểu $44 \times 44\text{ CSS pixels}$ (diện tích $44 \times 44 = 1936\text{ px}^2$) | chặng 3 phép tính |

## [W23] W3C Recommendation, *Web Content Accessibility Guidelines (WCAG) 2.2*, 5 October 2023 — https://www.w3.org/TR/WCAG22/
| Câu trích / Con số | Dùng ở |
|---|---|
| Ban hành ngày 5/10/2023; đánh dấu tiêu chí **4.1.1 Parsing** là “obsolete and removed” (trình duyệt hiện đại đã chuẩn hoá cách xử lý thẻ lỗi) và **thêm 9 tiêu chí mới**: tổng số tiêu chí hiệu lực là $78 - 1 + 9 = 86$ | chặng 4 (2023), bài học sai 2 (`fix`) |
| **2.5.8 Target Size (Minimum) (Level AA):** đích con trỏ tối thiểu $24 \times 24\text{ CSS pixels}$ (diện tích $24 \times 24 = 576\text{ px}^2$; so với mức AAA $1936\text{ px}^2$ thì $1936 / 576 \approx 3{,}36$ lần diện tích) | chặng 4 phép tính, tự kiểm |
| **3.3.8 Accessible Authentication (Minimum) (Level AA):** không bắt người dùng vượt qua bài kiểm tra chức năng nhận thức (như gõ lại mật khẩu phức tạp mà chặn dán hoặc giải câu đố nhận dạng) khi đăng nhập, trừ khi có cơ chế hỗ trợ (cho phép dán / trình quản lý mật khẩu) | chặng 4 quy mô & thực hành |

## Điều KHÔNG dạy / NOT_VERIFIED
- Không dạy lộ trình hay thời điểm ban hành của dự thảo WCAG 3.0 (*W3C Accessibility Guidelines 3.0 Working Draft*) vì chưa phải khuyến nghị chính thức (NOT_VERIFIED ngày hoàn tất).
- Không đồng nhất “vượt công cụ quét tự động” với “người khuyết tật dùng được” (`fix` của giáo án).
- Kịch bản đội sản phẩm có 40 màn hình, 3 lập trình viên ở phần tự làm là **SỐ MINH HOẠ**.
- Không đọc `W3C`, `WCAG`, `HTML`, `CSS`, `ARIA`, `AA`, `AAA` trong `say:` — lời đọc nói “tổ chức chuẩn web quốc tế”, “bộ chuẩn tiếp cận web”, “mức một / mức hai / mức ba”, “điểm ảnh”.
