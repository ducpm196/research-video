# Nguồn bài HCI L10 — Thiết kế chống lỗi: ngăn, phát hiện, hoàn tác

Đọc và tra cứu 2026-11-03. Nhãn dùng trong `source:` của bài.

## [N13] D. A. Norman, *The Design of Everyday Things: Revised and Expanded Edition*, Basic Books, 2013, Chương 5 (“Human Error? No, Bad Design”)
| Nguyên lý thiết kế chống lỗi | Dùng ở |
|---|---|
| Phân biệt lỗi trượt (*slips* — định làm đúng nhưng thao tác sai do thói quen/mất tập trung) và lỗi nhầm (*mistakes* — mục tiêu hoặc mô hình tâm trí không phù hợp) (đã học ở HCI L00) | cảnh ôn nền |
| Các cơ chế phòng chống theo thứ tự hiệu quả: (1) **Ràng buộc** (*constraints* / *forcing functions*) làm hành động sai không thể thực hiện; (2) **Hoàn tác** (*undo*) cho phép đảo ngược hành động dễ dàng; (3) **Xác nhận có nội dung** (*confirmation* nêu rõ đối tượng và hậu quả, tránh hộp xác nhận lặp lại gây bấm theo thói quen) — *đối chiếu 2026-11-09*: ba cơ chế có trong mục *Design Lessons from the Study of Errors* (tr. 202–203) theo thứ tự tiêu đề “Adding Constraints to Block Errors”, “Undo”, “Confirmation and Error Messages”, nhưng sách **không xếp hạng “theo thứ tự hiệu quả”**; câu gốc về hoàn tác, nguyên văn: “Perhaps the most powerful tool to minimize the impact of errors is the Undo command in modern electronic systems, reversing the operations performed by the previous command, wherever possible.” (tr. 203); về xác nhận: “But these requests are usually ill-timed because after requesting an operation, people are usually certain they want it done.” (tr. 203). Nên bỏ chữ “theo thứ tự hiệu quả” hoặc ghi là cách xếp của bài | cảnh ký hiệu, khái niệm, lỗi thường gặp |

## [R00] J. Reason, “Human error: models and management”, *BMJ* (British Medical Journal), 320(7237), trang 768–770, 2000 (và *Human Error*, Cambridge University Press, 1990)
| Câu trích / Mô hình phô mai Thuỵ Sĩ (*Swiss cheese model*) | Dùng ở |
|---|---|
| Hệ thống an toàn cao có nhiều lớp phòng vệ (*defensive layers*), mỗi lớp như một lát phô mai có các lỗ hổng (*holes*); tai nạn chỉ xảy ra khi lỗ hổng ở mọi lớp thẳng hàng cùng lúc — **VERIFIED 2026-11-09** (mục *The Swiss cheese model of system accidents*, BMJ 320:768–770), các cụm nguyên văn: “High technology systems have many defensive layers”; “they are more like slices of Swiss cheese, having many holes”; “the holes in many layers momentarily line up to permit a trajectory of accident opportunity”. Lưu ý: Reason viết “many layers … momentarily”, không nói “mọi lớp” theo nghĩa tuyệt đối | cảnh hình dung (SVG các lớp chắn độc lập), suy ra công thức |
| Khi các lớp phòng vệ **độc lập**, xác suất lỗi lọt qua cả hệ thống bằng tích xác suất lọt của từng lớp ($\prod p_i$); khi hai lớp phụ thuộc nhau (ví dụ người duyệt thứ hai bấm đồng ý theo thói quen), lỗ hổng thẳng hàng sẵn nên xác suất lọt gần như không giảm — *đối chiếu 2026-11-09*: **không có trong [R00]**; bài báo chỉ mô tả định tính, không có công thức tích xác suất. Đây là suy luận xác suất của bài, không được gán cho Reason | cảnh suy ra công thức, ví dụ $1/1000 \times 1/100 = 1/100\,000$, lỗi thường gặp |

## Điều KHÔNG dạy / NOT_VERIFIED
- Con số tỉ lệ lỗi trượt $1/1000$, tỉ lệ lọt qua người duyệt độc lập $1\%$ ($0{,}01$) dẫn tới xác suất lọt $1/100\,000$ là **SỐ MINH HOẠ** (đã ghi rõ trong `curriculum/hci.yaml` L10 và trong bài), kiểm bằng `alg.hci_swiss_cheese_leak`.
- Không đọc `Norman`, `Reason`, `BMJ` trong `say:`.

## Đối chiếu nguồn mở 2026-11-09 (BN-0040)
- [R00]: bản mở trên PubMed Central, https://pmc.ncbi.nlm.nih.gov/articles/PMC1117770/ (đọc qua công cụ tải trang; trang PMC không ghi số trang in 768/769/770 cạnh từng mục, nên chỉ ghi tên mục). Europe PMC xác nhận BMJ 320(7237):768–770, 2000. Ba cụm từ mô hình phô mai Thuỵ Sĩ VERIFIED; công thức $\prod p_i$ không có trong bài (là suy luận của bài học).
- [N13]: bản toàn văn do người dùng tải lên archive.org (không phải bản NXB), https://archive.org/details/the-design-of-everyday-things_202512. Mục *Design Lessons from the Study of Errors*: tr. 202–203; mô hình Swiss cheese cũng được Norman nhắc ở tr. 208 (Hình 5.3). Phát hiện: sách không xếp ba cơ chế “theo thứ tự hiệu quả” → đã ghi chú trong bảng.
- Bảng [N13] và [R00] là diễn giải nguyên lý (không gắn nhãn “nguyên văn”); các câu trong ngoặc kép thêm ngày 2026-11-09 là nguyên văn đã đọc.
