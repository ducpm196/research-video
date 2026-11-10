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
| “Most industrial accidents are caused by human error: estimates range between 75 and 95 percent. How is it that so many people are so incompetent? Answer: They aren’t. It’s a design problem.” (tr. 162, đoạn mở đầu chương 5) … “Human error is defined as any deviance from ‘appropriate’ behavior.” (tr. 170, mục *Definitions: Errors, Slips, and Mistakes*) — **VERIFIED 2026-11-09, đã sửa theo bản gốc**: từng câu đúng nguyên văn nhưng bản cũ đảo thứ tự (định nghĩa ở tr. 170 đứng sau đoạn mở đầu tr. 162); nay xếp theo thứ tự trong sách | `concept`, `recap`: góc nhìn xem lỗi của người vận hành là triệu chứng của thiết kế thiếu hàng rào bảo vệ |
| “Slips occur when the goal is correct, but the required actions are not done properly: the execution is flawed. Mistakes occur when the goal or plan is wrong.” — **VERIFIED 2026-11-09**: nguyên văn chú thích *Figure 5.1. Classification of Errors*, tr. 170 | `prereq`, `sym`, `concept`, `example`: phân biệt lỗi trượt (ý định đúng, tay làm lệch) và lỗi nhầm (hiểu sai tình huống nên lập kế hoạch sai) |

## Điều KHÔNG dạy / NOT_VERIFIED
- Không nêu tên cá nhân ca trực hoặc người giám sát trong sự cố ngày 13/1/2018.
- Các ví dụ phụ trong phần ôn nền, tự làm và lỗi thường gặp (cửa hàng xoá nhầm kho hàng, gửi thư nhầm cho 50 000 khách, hai nút đặt sát nhau) là SỐ MINH HOẠ để rèn phân loại lỗi trượt — lỗi nhầm và tính thời gian khắc phục.
- Tên riêng và chữ viết tắt (`Hawaii`, `FCC`, `Norman`) chỉ hiện trên màn hình; lời đọc dùng tiếng Việt tự nhiên (“một bang hải đảo của Mỹ”, “báo cáo điều tra của cơ quan viễn thông Mỹ”, “nhà nghiên cứu thiết kế”).

## Bổ sung khi đọc kiểm 2026-11-08 (đọc lại [FCC18], bản PDF docs.fcc.gov DOC-350119A1, trích bằng pdftotext, tr. 11–14, 23–24)
| Câu trích nguyên văn | Dùng ở |
|---|---|
| “HI-EMA cancels further transmission of the false alert, but does not issue an "all clear" message.” (8:12 a.m.); chú thích 59: “It also does not "recall" messages that have already been transmitted and displayed.” | `example` bước 2–3: lệnh ngừng phát lại không thu hồi tin đã hiện |
| 8:24–8:27 a.m.: “HI-EMA staff meets to discuss options for a second, corrective EAS and WEA message.” 8:30 a.m.: “HI-EMA calls a representative of the FEMA IPAWS Program Management Office … but the call is not answered.” Chú thích 65: “FEMA did not need to authorize HI-EMA to send the correction as a CEM, and HI-EMA knew that at the time that they called.” | `example` bước 3 (sửa: bỏ ý “xin phép cơ quan liên bang”) |
| 8:31–8:44 a.m.: “HI-EMA calls another representative of the FEMA IPAWS Program Management Office … After 45 seconds, they agree …”; “The Deputy Chief … logs into HI-EMA's alert origination software and creates false alert correction messages for EAS and WEA.” 8:45 a.m.: “HI-EMA issues a CEM to correct the false alert 38 minutes after initial transmission.” | `example` bước 3 |
| “Prior to the January 13, 2018, false alert, HI-EMA did not have protocols or training in place with respect to how to issue a correction to an alert”; “HI-EMA has created templates for EAS and WEA messages that officers may use to correct a false alarm.” | `example` bước 3–4, `pitfalls` lỗi 4 |
| “the employee who triggered the false alert believed that the missile threat was real.” | `concept` bước 2 (lỗi nhầm là trường hợp thật) |
- Đã bỏ khỏi lời đọc: “hàng triệu người dân”, “giao thông đình trệ” (không có trong câu đã trích).

## Đối chiếu nguồn mở 2026-11-09 (BN-0040)
- Chỉ đối chiếu hai câu [NO13]; phần [FCC18] đã kiểm ngày 2026-11-08, không đọc lại.
- [NO13] — bản toàn văn *The Design of Everyday Things: Revised and Expanded Edition* (2013) do người dùng tải lên archive.org (identifier `the-design-of-everyday-things_202512`, tệp PDF 369 trang và `_djvu.txt`; không phải bản phát hành của NXB; số trang lấy theo số trang in trong bản quét, PDF tr. 181 = sách tr. 162). Truy cập 2026-11-09: https://archive.org/details/the-design-of-everyday-things_202512
  - Câu “Most industrial accidents … It’s a design problem.”: nguyên văn, tr. 162 (mở đầu chương 5).
  - Câu “Human error is defined as any deviance from ‘appropriate’ behavior.”: nguyên văn, tr. 170. Bản cũ ghép hai câu theo thứ tự ngược → đã xếp lại theo thứ tự trong sách.
  - Câu “Slips occur when … Mistakes occur when the goal or plan is wrong.”: nguyên văn, chú thích Hình 5.1, tr. 170.
