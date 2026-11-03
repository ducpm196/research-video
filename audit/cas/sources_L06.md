# Nguồn đã đọc nguyên văn cho CAS L06 (Amazon S3, vùng Bắc Virginia, 28/2/2017)

Đọc ngày 2026-11-02 (urllib + trích văn bản HTML; bản tải ở thư mục nháp của phiên, không đưa vào kho). Chỉ trích các câu bài giảng dựa
vào (CITED). Khoảng thời gian là phép tính lại (VER: `checks` của bài, `audit/cas/ver/L06.py`, `audit/verify_plan_curricula.py` CAS:L06).
Số máy (100, tối thiểu 70, gỡ 4 / 40, 5 máy mỗi 10 phút, 200 / 150 / 60, 12 ô) là SỐ MINH HOẠ: bài tổng kết không cho số máy nào.
Đã đối chiếu với CLC L12 (audit/clc/sources_L12.md [S17], cùng URL): cùng mốc 4 giờ 17 phút, cùng thuật ngữ “hệ con chỉ mục / cấp chỗ”.

## [S17] AWS, *Summary of the Amazon S3 Service Disruption in the Northern Virginia (US-EAST-1) Region*
URL: https://aws.amazon.com/message/41926/ (HTTP 200, 307 243 byte, 2026-11-02). Bài tổng kết chính thức của công ty; không nêu tên người.
- “the service disruption that occurred in the Northern Virginia (US-EAST-1) Region on the morning of February 28th, 2017.”
- “At 9:37AM PST, an authorized S3 team member using an established playbook executed a command which was intended to remove a small number
  of servers for one of the S3 subsystems that is used by the S3 billing process. Unfortunately, one of the inputs to the command was entered
  incorrectly and a larger set of servers was removed than intended.”
- “The servers that were inadvertently removed supported two other S3 subsystems. One of these subsystems, the index subsystem, manages the
  metadata and location information of all S3 objects in the region. This subsystem is necessary to serve all GET, LIST, PUT, and DELETE
  requests. The second subsystem, the placement subsystem, manages allocation of new storage and requires the index subsystem to be functioning
  properly to correctly operate.”
- “Removing a significant portion of the capacity caused each of these systems to require a full restart. While these subsystems were being
  restarted, S3 was unable to service requests.”
- Dịch vụ khác: “including the S3 console, Amazon Elastic Compute Cloud (EC2) new instance launches, Amazon Elastic Block Store (EBS) volumes
  (when data was needed from a S3 snapshot), and AWS Lambda were also impacted”.
- “S3 subsystems are designed to support the removal or failure of significant capacity with little or no customer impact.”
- “we have not completely restarted the index subsystem or the placement subsystem in our larger regions for many years. S3 has experienced
  massive growth over the last several years and the process of restarting these services and running the necessary safety checks to validate
  the integrity of the metadata took longer than expected.”
- “By 12:26PM PST, the index subsystem had activated enough capacity to begin servicing S3 GET, LIST, and DELETE requests. By 1:18PM PST, the
  index subsystem was fully recovered and GET, LIST, and DELETE APIs were functioning normally. … The placement subsystem began recovery when
  the index subsystem was functional and finished recovery at 1:54PM PST. At this point, S3 was operating normally.”
- “the tool used allowed too much capacity to be removed too quickly. We have modified this tool to remove capacity more slowly and added
  safeguards to prevent capacity from being removed when it will take any subsystem below its minimum required capacity level. … We are also
  auditing our other operational tools to ensure we have similar safety checks.”
- “breaking services into small partitions which we call cells. By factoring services into cells, engineering teams can assess and thoroughly
  test recovery processes … to reduce blast radius and improve recovery.” “The S3 team had planned further partitioning of the index subsystem
  later this year. We are reprioritizing that work to begin immediately.”
- “From the beginning of this event until 11:37AM PST, we were unable to update the individual services’ status on the AWS Service Health
  Dashboard (SHD) because of a dependency the SHD administration console has on Amazon S3. Instead, we used the AWS Twitter feed (@AWSCloud) and
  SHD banner text … we have changed the SHD administration console to run across multiple AWS regions.”

## Phép tính của bài (VER)
- 9:37 → 12:26 = 169 phút (2 giờ 49); → 13:18 = 221 (3 giờ 41); → 13:54 = 257 (4 giờ 17); 13:18 → 13:54 = 36; 9:37 → 11:37 = 120.
- Công cụ chặn mức tối thiểu và gỡ chậm: chỉ là số minh hoạ cho hai biện pháp AWS ghi; ô 1/12 ≈ 8,3% là số minh hoạ.

## Điều KHÔNG dạy (nguồn không ghi)
- Số máy bị gỡ, tham số cụ thể bị gõ sai, tốc độ gỡ mới, mức tối thiểu thật: bài tổng kết không ghi → chỉ dùng số minh hoạ, ghi rõ.
- Thiệt hại tiền của khách hàng, số trang web bị ảnh hưởng (hay được báo chí kể): không có trong bài tổng kết → không dạy.
- Không gọi người chạy lệnh là “người gõ sai”/không nêu tên: nguồn chỉ viết “an authorized S3 team member”.
- Gỡ chậm “đủ lâu để cảnh báo kịp kêu” là suy luận của bài (INFERRED) từ ý “remove capacity more slowly”, không phải câu của nguồn.
