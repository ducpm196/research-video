# Nguồn bài HCI L00 — Lỗi do thiết kế, không do người dùng: hộp xác nhận giống hệt nhau

Đọc nguyên văn ngày 2026-11-03. Các phép trừ mốc thời gian được kiểm tự động bằng `checks` (`alg.hci_minutes_diff`) và `audit/verify_plan_curricula.py` (`HCI:L00`).

## [FCC18] Federal Communications Commission, Public Safety and Homeland Security Bureau — *Report and Recommendations: Hawaii Emergency Management Agency January 13, 2018 False Alert* (tháng 4/2018).
URL: https://docs.fcc.gov/public/attachments/DOC-350119A1.pdf

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “At 8:07 a.m. HST on Saturday, January 13, 2018, the Hawaii Emergency Management Agency (HI-EMA) inadvertently transmitted a false Emergency Alert System (EAS) and Wireless Emergency Alert (WEA) message indicating that a ballistic missile threat was inbound to Hawaii.” | `hook`, `example`: mốc 8:07 sáng phát cảnh báo giả trên toàn bang |
| “BALLISTIC MISSILE THREAT INBOUND TO HAWAII. SEEK IMMEDIATE SHELTER. THIS IS NOT A DRILL.” | `hook`, `intuition`: thông điệp cảnh báo thật gửi tới điện thoại người dân |
| “Are you sure that you want to send this Alert?” | `hook`, `intuition`, `example`: hộp xác nhận chung cho cả tập trận và cảnh báo thật, không hiện nội dung sắp phát |
| “At 8:45 a.m. HST, 38 minutes after the false alert was issued, HI-EMA transmitted a second EAS and WEA message cancelling the first alert.” | `hook`, `example`, `check`: mốc 8:45 sáng phát thông điệp đính chính qua hệ thống cảnh báo, tổng cộng 38 phút |
| “The false alert was the result of a combination of human error and inadequate safeguards.” | `pitfalls` (lỗi 1): báo cáo kết luận do cả lỗi con người và thiếu cơ chế an toàn, không dừng ở kết luận “nhân viên bấm nhầm” |

## [NO13] Donald A. Norman — *The Design of Everyday Things: Revised and Expanded Edition*. Basic Books, 2013, chương 5 (*Human Error? No, Bad Design*).

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “Human error is defined as any deviance from ‘appropriate’ behavior. … Most industrial accidents are caused by human error: estimates range between 75 and 95 percent. How is it that so many people are so incompetent? Answer: They aren’t. It’s a design problem.” | `concept`, `recap`: góc nhìn xem lỗi của người vận hành là triệu chứng của thiết kế thiếu hàng rào bảo vệ |
| “Slips occur when the goal is correct, but the required actions are not done properly: the execution is flawed. Mistakes occur when the goal or plan is wrong.” | `prereq`, `sym`, `concept`, `example`: phân biệt lỗi trượt (ý định đúng, tay làm lệch) và lỗi nhầm (hiểu sai tình huống nên lập kế hoạch sai) |

## Điều KHÔNG dạy / NOT_VERIFIED
- Không nêu tên cá nhân ca trực hoặc người giám sát trong sự cố ngày 13/1/2018.
- Các ví dụ phụ trong phần ôn nền, tự làm và lỗi thường gặp (cửa hàng xoá nhầm kho hàng, gửi thư nhầm cho 50 000 khách, hai nút đặt sát nhau) là SỐ MINH HOẠ để rèn phân loại lỗi trượt — lỗi nhầm và tính thời gian khắc phục.
- Tên riêng và chữ viết tắt (`Hawaii`, `FCC`, `Norman`) chỉ hiện trên màn hình; lời đọc dùng tiếng Việt tự nhiên (“một bang hải đảo của Mỹ”, “báo cáo điều tra của cơ quan viễn thông Mỹ”, “nhà nghiên cứu thiết kế”).
