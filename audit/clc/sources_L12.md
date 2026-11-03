# Nguồn đã đọc nguyên văn cho CLC L12 (bài hành trình: kho lưu trữ đối tượng S3, 2006 → 2022)

Đọc ngày 2026-11-02 bằng curl (tác nhân trình duyệt) rồi trích văn bản (bỏ thẻ HTML), mọi trang trả 200; không trang nào bị chặn.
Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác là phép tính lại (VER: `checks` của bài, `audit/clc/verify_clc.py` L12,
`audit/verify_plan_curricula.py` CLC:L12) hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá nhân trong lời đọc và trên màn hình; bài tổng kết
sự cố 2017 không nêu tên ai, chỉ ghi “an authorized S3 team member”. Tên tác giả blog chỉ ghi ở đây.

## [PR06] Amazon, thông cáo báo chí “Amazon Web Services Launches”, 2006-03-14
URL: https://press.aboutamazon.com/2006/3/amazon-web-services-launches (curl 200, 153 779 byte).
- Tiêu đề phụ: “S3 Provides Application Programming Interface for Highly Scalable Reliable, Low-Latency Storage at Very Low Costs”.
- “SEATTLE--(BUSINESS WIRE)--March 14, 2006-- Amazon Web Services today announced "Amazon S3(TM)," a simple storage service that offers
  software developers a highly scalable, reliable, and low-latency data storage infrastructure at very low costs.”
- “Amazon S3 is storage for the Internet. It's designed to make web-scale computing easier for developers.”
- “Amazon S3 is intentionally built with a minimal feature set. The focus is on simplicity and robustness.”
- “Write, read, and delete objects containing from 1 byte to 5 gigabytes of data each. The number of objects that can be stored is unlimited.”
  “Each object is stored and retrieved via a unique developer-assigned key.”
- Design requirements: “Scalable: … adding nodes to the system increases, not decreases, its availability, speed, throughput, capacity, and
  robustness.” “Reliable: Store data durably, with 99.99% availability. There can be no single points of failure.” “Fast: … Any performance
  bottlenecks can be fixed by simply adding nodes to the system.” “Inexpensive: Amazon S3 is built from inexpensive commodity hardware
  components. As a result, frequent node failure is the norm and must not affect the overall system.”
- Design principles: “Decentralization: Use fully decentralized techniques to remove scaling bottlenecks and single points of failure.”
  “Failure tolerant: The system considers the failure of components to be a normal mode of operation”. “Symmetry: Nodes in the system are
  identical in terms of functionality”. “Simplicity: The system should be made as simple as possible, but no simpler.”
- Giá: “Developers pay just $0.15 per gigabyte of storage per month and $0.20 per gigabyte of data transferred.” “no minimum fee”.
- Ứng dụng sớm: nhóm Stardust@Home (UC Berkeley) dùng S3 “to store and deliver the 60 million images … to 100,000 volunteers”.

## [B13] AWS News Blog, “Amazon S3 – Two Trillion Objects, 1.1 Million Requests / Second”, 2013-04-18
URL: https://aws.amazon.com/blogs/aws/amazon-s3-two-trillion-objects-11-million-requests-second/ (curl 200; `datetime="2013-04-18…"`).
- “Last June I blogged about the first trillion objects stored in Amazon S3. On the first day of re:Invent I updated that number to 1.3 trillion.”
- “there are now more than 2 trillion (2 x 10 12 ) objects stored in Amazon S3 and that the service is regularly peaking at over 1.1 million
  requests per second.”
- “It took us six years to grow to one trillion stored objects, and less than a year to double that number.”

## [S17] AWS, “Summary of the Amazon S3 Service Disruption in the Northern Virginia (US-EAST-1) Region” (sự cố 2017-02-28)
URL: https://aws.amazon.com/message/41926/ (curl 200, 307 243 byte).
- “At 9:37AM PST, an authorized S3 team member using an established playbook executed a command which was intended to remove a small number of
  servers for one of the S3 subsystems that is used by the S3 billing process. Unfortunately, one of the inputs to the command was entered
  incorrectly and a larger set of servers was removed than intended.”
- “the index subsystem, manages the metadata and location information of all S3 objects in the region. This subsystem is necessary to serve
  all GET, LIST, PUT, and DELETE requests. The second subsystem, the placement subsystem, manages allocation of new storage and requires the
  index subsystem to be functioning properly”.
- “Removing a significant portion of the capacity caused each of these systems to require a full restart. While these subsystems were being
  restarted, S3 was unable to service requests.”
- “S3 subsystems are designed to support the removal or failure of significant capacity with little or no customer impact. … we have not
  completely restarted the index subsystem or the placement subsystem in our larger regions for many years. S3 has experienced massive growth
  over the last several years and the process of restarting these services and running the necessary safety checks to validate the integrity
  of the metadata took longer than expected.”
- “By 12:26PM PST, the index subsystem had activated enough capacity to begin servicing S3 GET, LIST, and DELETE requests. By 1:18PM PST, the
  index subsystem was fully recovered … The placement subsystem … finished recovery at 1:54PM PST. At this point, S3 was operating normally.”
- “the tool used allowed too much capacity to be removed too quickly. We have modified this tool to remove capacity more slowly and added
  safeguards to prevent capacity from being removed when it will take any subsystem below its minimum required capacity level. … We are also
  auditing our other operational tools to ensure we have similar safety checks.”
- “breaking services into small partitions which we call cells. By factoring services into cells, engineering teams can assess and thoroughly
  test recovery processes … As S3 has scaled, the team has done considerable work to refactor parts of the service into smaller cells to
  reduce blast radius and improve recovery. … We are reprioritizing that work to begin immediately.”
- “From the beginning of this event until 11:37AM PST, we were unable to update the individual services’ status on the AWS Service Health
  Dashboard (SHD) because of a dependency the SHD administration console has on Amazon S3. … we have changed the SHD administration console
  to run across multiple AWS regions.”

## [W20] AWS What's New, “Amazon S3 now delivers strong read-after-write consistency automatically for all applications”, “Posted on: Dec 1, 2020”
URL: https://aws.amazon.com/about-aws/whats-new/2020/12/amazon-s3-now-delivers-strong-read-after-write-consistency-automatically-for-all-applications/ (curl 200).
- “Amazon S3 delivers strong read-after-write consistency for any storage request, without changes to performance or availability, without
  sacrificing regional isolation for applications, and at no additional cost.”
- “Amazon S3 pioneered object storage in the cloud with high availability, performance, and virtually unlimited scalability, with eventual
  consistency.” “Without strong consistency, you would insert custom code into these applications, or provision databases to keep objects
  consistent with any changes in Amazon S3 across millions or billions of objects.”
- “After a successful write of a new object or an overwrite of an existing object, any subsequent read request immediately receives the latest
  version of the object. S3 also provides strong consistency for list operations”.
- “All Amazon S3 customers automatically receive strong consistency in all AWS Regions”.

## [B20] AWS News Blog, “Amazon S3 Update – Strong Read-After-Write Consistency”, 2020-12-01
URL: https://aws.amazon.com/blogs/aws/amazon-s3-update-strong-read-after-write-consistency/ (curl 200; `datetime="2020-12-01…"`).
- “When we launched S3 back in 2006, … it was designed to provide 99.99% availability … (at last count) over 10,000 data lakes.”
- “eventual consistency. In a nutshell, after a call to an S3 API function such as PUT that stores or modifies data, there’s a small time window
  where the data has been accepted and durably stored, but not yet visible to all GET or LIST requests.”
- “Amazon EMR built EMRFS Consistent View and open source Hadoop developers built S3Guard, which provided a layer of strong consistency”.
- “Effective immediately, all S3 GET, PUT, and LIST operations, as well as operations that change object tags, ACLs, or metadata, are now
  strongly consistent. … This applies to all existing and new S3 objects, works in all regions, and is available to you at no extra charge!
  There’s no impact on performance, you can update an object hundreds of times per second if you’d like, and there are no global dependencies.”
- “you no longer need to use EMRFS Consistent View or S3Guard, further reducing the cost”.

## [B21] AWS News Blog, “Amazon S3’s 15th Birthday – It is Still Day 1 after 5,475 Days & 100 Trillion Objects”, 2021-03-14
URL: https://aws.amazon.com/blogs/aws/amazon-s3s-15th-birthday-it-is-still-day-1-after-5475-days-100-trillion-objects/ (curl 200).
- “S3 now stores over 100 trillion (10 14 …) objects, and regularly peaks at tens of millions of requests per second.”
- “We started with a simple conceptual model: Uniquely named buckets that could hold any number of objects, each identified by a string key.
  The initial API was equally simple: create a bucket, list all buckets, put an object, get an object, and put an access control list. This
  simplicity helped us to avoid any one-way doors … All of those decisions remain valid and code written on launch day will still work just
  fine today.”
- “we have reduced the price per GB-month of S3 many times, and have also introduced storage classes”.
- “S3 is designed to provide “11 9’s” (99.999999999%) of durability. … we automatically make use of multiple storage arrays, racks, cells, and
  Availability Zones (77 and counting).”
- “S3 … gets better “beneath your feet” over time, with no API changes and no downtime for upgrades. As a simple example, we recently
  established a way to dramatically reduce latency for … 0.01% of the PUT requests made to S3. … it avoided a situation where customer
  requests would time out and retry.”

## [PI22] AWS News Blog, “Welcome to AWS Pi Day 2022”, 2022-03-14
URL: https://aws.amazon.com/blogs/aws/welcome-to-aws-pi-day-2022/ (curl 200; `datetime="2022-03-14…"`).
- “Amazon S3 now holds more than 200 trillion (2 x 10 14 ) objects. … Counting at one object per second, it would take 6.342 million years to
  reach this number!”
- “Shortly after the 2006 launch of S3, I was happy to announce the then-impressive metric of 800 million stored objects, so the object count
  has grown by a factor of 250,000 in less than 16 years.”
- “Request Rate – Amazon S3 now averages over 100 million requests per second.”

## Điều KHÔNG dạy (nguồn không ghi)
- Độ dài của “cửa sổ thời gian nhỏ” của nhất quán cuối cùng trước 2020: [B20] không ghi số → không dạy con số; tỉ lệ 1% đọc thấy bản cũ
  trong bài là SỐ MINH HOẠ.
- Cách S3 làm được nhất quán mạnh bên trong (giao thức, bộ nhớ đệm): [W20], [B20] không ghi → không dạy.
- Hai người cùng ghi một khoá thì ai thắng: không có trong các câu đã đọc → không dạy.
- Số máy bị gỡ, số máy tối thiểu của mỗi hệ con, số ô (cell) của hệ con chỉ mục năm 2017: [S17] không ghi. 100 máy, tối thiểu 80, 10 ô
  là SỐ MINH HOẠ.
- Số máy chủ của S3, số yêu cầu một máy phục vụ được: không nguồn nào ghi; 1000 yêu cầu mỗi giây mỗi máy là SỐ MINH HOẠ.
- Mốc “ô, giảm bán kính ảnh hưởng” bắt đầu năm nào: [S17] chỉ ghi “As S3 has scaled” → bài nói “trong những năm tăng trưởng, theo bài
  tổng kết 2017”, không gán năm.
- Mốc 800 triệu đối tượng là “ngay sau khi ra mắt năm 2006” theo [PI22]; ngày chính xác không ghi → bài không gán ngày.
- Lý do người vận hành gõ sai, danh tính người vận hành: [S17] không ghi, bài không nêu.
- Tên khách hàng (Stardust@Home, Dropbox) không dùng trong lời đọc; con số 34 PB của [B20] không dùng.
