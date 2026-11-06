# Nguồn bài HCI L11 — Tình huống chuyên gia: thiết kế lại giao diện gửi cảnh báo khẩn cấp

Đọc và tra cứu 2026-11-03. Nhãn dùng trong `source:` của bài. Không nêu tên cá nhân vận hành hay quản lý trong bài.

## [FCC18] Federal Communications Commission (FCC), Public Safety and Homeland Security Bureau, *Report and Recommendations: Hawaii Emergency Management Agency January 13, 2018 False Ballistic Missile Alert*, tháng 4/2018
| Mốc thời gian / Câu trích nguyên văn từ báo cáo | Dùng ở |
|---|---|
| **8:05 AM HST:** cuộc gọi bắt đầu bài tập chuyển ca không báo trước cho nhân viên trực cảnh báo | cảnh mở đầu, dòng thời gian, tái hiện cơ chế |
| **8:07 AM HST:** nhân viên trực chọn mục gửi cảnh báo thật từ danh sách thả xuống và bấm “Yes” ở hộp xác nhận `“Are you sure that you want to send this Alert?”` — cảnh báo tên lửa đạn đạo giả được phát đi toàn bang qua WEA và EAS | mở đầu, tái hiện cơ chế, tính khoảng thời gian |
| Giao diện dùng **cùng một màn hình và cùng một hộp xác nhận** `“Are you sure that you want to send this Alert?”` cho cả cảnh báo thật (*live alert*) lẫn tập trận (*drill*), không có màn hình xem trước nội dung bản tin sẽ phát, không yêu cầu người thứ hai duyệt (*two-person rule*) | tái hiện cơ chế, thiết kế lại các lớp phòng vệ |
| **8:31 AM – 8:44 AM HST (13 phút):** vì hệ thống **không có sẵn mẫu bản tin huỷ / đính chính** (*false alarm cancellation template*), cấp quản lý và nhân viên phải đăng nhập và tự soạn thảo bản tin đính chính từ 8:31 tới 8:44 | tái hiện cơ chế, tính $44 - 31 = 13$ phút |
| **8:45 AM HST:** bản tin đính chính chính thức (*“There is no missile threat or danger to the State of Hawaii. Repeat. False Alarm.”*) được phát đi qua WEA/EAS — **38 phút** kể từ 8:07 AM | mở đầu, tái hiện cơ chế, tính $45 - 7 = 38$ phút (`alg.hci_minutes_diff(8, 7, 8, 45) == 38`) |
| Kết luận và khuyến nghị của báo cáo: sự cố do kết hợp lỗi con người và thiếu các cơ chế bảo vệ kỹ thuật – quy trình; khuyến nghị tách không gian tập trận khỏi hệ thống phát thật, xem trước toàn văn, hai người xác nhận độc lập, có sẵn mẫu huỷ cảnh báo một chạm, và diễn tập định kỳ có kịch bản lỗi | cảnh bài học sai (`fix`), tự làm, tổng kết |

## Điều KHÔNG dạy / NOT_VERIFIED
- Không dạy tin đồn phổ biến trên báo chí rằng “nhân viên chỉ đơn thuần trượt tay bấm nhầm dòng trong khi biết đó là tập trận” như nguyên nhân duy nhất — báo cáo [FCC18] ghi nhận cả việc nhân viên nghe nhầm cuộc gọi tập trận là tình huống thật lẫn việc giao diện không phân biệt tập trận với cảnh báo thật và thiếu cơ chế xem trước / hai người duyệt.
- Không nêu tên cá nhân nhân viên hay giám đốc cơ quan.
- Các con số ước lượng thời gian thao tác khi thiết kế lại (ví dụ phát bản tin đính chính soạn sẵn trong dưới 2 phút, hoặc xác suất lọt qua 3 lớp độc lập) là **SỐ MINH HOẠ** tính từ mô hình đã học ở bài 5, 8, 10.
- Không đọc `Hawaii`, `FCC`, `WEA`, `EAS` trong `say:` — lời đọc nói “một bang hải đảo của Mỹ”, “cơ quan viễn thông Mỹ”, “hệ thống cảnh báo khẩn cấp”.
