# Nguồn bài HCI L10 — Thiết kế chống lỗi: ngăn, phát hiện, hoàn tác

Đọc và tra cứu 2026-11-03. Nhãn dùng trong `source:` của bài.

## [N13] D. A. Norman, *The Design of Everyday Things: Revised and Expanded Edition*, Basic Books, 2013, Chương 5 (“Human Error? No, Bad Design”)
| Nguyên lý thiết kế chống lỗi | Dùng ở |
|---|---|
| Phân biệt lỗi trượt (*slips* — định làm đúng nhưng thao tác sai do thói quen/mất tập trung) và lỗi nhầm (*mistakes* — mục tiêu hoặc mô hình tâm trí không phù hợp) (đã học ở HCI L00) | cảnh ôn nền |
| Các cơ chế phòng chống theo thứ tự hiệu quả: (1) **Ràng buộc** (*constraints* / *forcing functions*) làm hành động sai không thể thực hiện; (2) **Hoàn tác** (*undo*) cho phép đảo ngược hành động dễ dàng; (3) **Xác nhận có nội dung** (*confirmation* nêu rõ đối tượng và hậu quả, tránh hộp xác nhận lặp lại gây bấm theo thói quen) | cảnh ký hiệu, khái niệm, lỗi thường gặp |

## [R00] J. Reason, “Human error: models and management”, *BMJ* (British Medical Journal), 320(7237), trang 768–770, 2000 (và *Human Error*, Cambridge University Press, 1990)
| Câu trích / Mô hình phô mai Thuỵ Sĩ (*Swiss cheese model*) | Dùng ở |
|---|---|
| Hệ thống an toàn cao có nhiều lớp phòng vệ (*defensive layers*), mỗi lớp như một lát phô mai có các lỗ hổng (*holes*); tai nạn chỉ xảy ra khi lỗ hổng ở mọi lớp thẳng hàng cùng lúc | cảnh hình dung (SVG các lớp chắn độc lập), suy ra công thức |
| Khi các lớp phòng vệ **độc lập**, xác suất lỗi lọt qua cả hệ thống bằng tích xác suất lọt của từng lớp ($\prod p_i$); khi hai lớp phụ thuộc nhau (ví dụ người duyệt thứ hai bấm đồng ý theo thói quen), lỗ hổng thẳng hàng sẵn nên xác suất lọt gần như không giảm | cảnh suy ra công thức, ví dụ $1/1000 \times 1/100 = 1/100\,000$, lỗi thường gặp |

## Điều KHÔNG dạy / NOT_VERIFIED
- Con số tỉ lệ lỗi trượt $1/1000$, tỉ lệ lọt qua người duyệt độc lập $1\%$ ($0{,}01$) dẫn tới xác suất lọt $1/100\,000$ là **SỐ MINH HOẠ** (đã ghi rõ trong `curriculum/hci.yaml` L10 và trong bài), kiểm bằng `alg.hci_swiss_cheese_leak`.
- Không đọc `Norman`, `Reason`, `BMJ` trong `say:`.
