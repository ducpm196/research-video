# Nguồn đã đọc nguyên văn cho CAS L11 (năm 2038: một sự cố biết trước)

Đọc ngày 2026-11-02 (urllib + trích văn bản HTML; PDF bằng pdftotext; bản tải để ở thư mục nháp của phiên, không đưa vào kho). Chỉ trích
các câu bài giảng dựa vào (CITED). Ngày giờ của 2³¹ − 1, −2³¹, 2³² − 1 giây là phép tính lại (VER: `checks` của bài,
`audit/cas/ver/L11.py`, `audit/verify_plan_curricula.py` CAS:L11). Số minh hoạ ghi rõ trên màn hình. Không nêu tên cá nhân.

## [LWN19] J. Corbet, *Approaching the kernel year-2038 end game*, LWN.net, 11/1/2019
Tải: lwn.net/Articles/776435/ (HTTP 200, 59 958 byte).
- “In January 2038, the 32-bit time_t value used on many Unix-like systems will run out of bits and be unable to represent the current time.”
- “The fact that systems being deployed now will still be operating in 2038 adds urgency to the issue as well.”
- “Timekeeping within the kernel has been reworked to use 64-bit values throughout, even on 32-bit systems”
- “The only remaining problem, of course, is that user space is still using 32-bit times, so things will still explode on schedule in 2038.”
- “For many applications, all that will be needed at this point is a rebuild and they will be prepared to survive the 2038 transition.
  Others, of course, will require more work.”
- “Problems will remain, mostly in filesystem timestamps and time values that are passed to ioctl() calls”

## [GL] GNU C Library, tệp NEWS (nhánh master, bản sao GitHub bminor/glibc)
Tải: raw.githubusercontent.com/bminor/glibc/master/NEWS (HTTP 200, 403 603 byte). Trang gốc sourceware.org trả trang chặn máy (“Anubis”)
→ đọc bản sao chỉ-đọc trên GitHub (suy ra là bản chép của kho chính thức; nội dung là tệp NEWS do dự án viết).
- Mục “Version 2.34”: “Add support for 64-bit time_t on configurations like x86 where time_t is traditionally 32-bit. Although time_t still
  defaults to 32-bit on these configurations, this default may change in future versions. This is enabled with the _TIME_BITS preprocessor
  macro set to 64 and is only supported when LFS (_FILE_OFFSET_BITS=64) is also enabled. It is only enabled for Linux and the full support
  requires a minimum kernel version of 5.1.”
- Mục “Version 2.40”: “Architectures which use a 32-bit seconds-since-epoch field in struct lastlog, struct utmp, struct utmpx (such as i386,
  powerpc64le, rv32, rv64, x86-64) switched from a signed to an unsigned type for that field. This allows these fields to store timestamps
  beyond the year 2038, until the year 2106. Please note that applications are still expected to migrate off the interfaces declared in
  <utmp.h> and <utmpx.h> …”

## [EXT4] The Linux Kernel documentation, *ext4 Data Structures and Algorithms — 4.1.3 Inode Timestamps*
Tải: docs.kernel.org/filesystems/ext4/inodes.html (HTTP 200, 40 072 byte).
- “Four timestamps are recorded in the lower 128 bytes of the inode structure … The four fields are 32-bit signed integers that represent
  seconds since the Unix epoch (1970-01-01 00:00:00 GMT), which means that the fields will overflow in January 2038.”
- “If the inode structure size sb->s_inode_size is larger than 128 bytes … the ctime, atime, and mtime inode fields are widened to 64 bits.
  Within this “extra” 32-bit field, the lower two bits are used to extend the 32-bit seconds field to be 34 bit wide … Therefore, timestamps
  should not overflow until May 2446.” “dtime was not widened.”
- Bảng: “0x000000000 - 0x07fffffff 1970-01-01 to 2038-01-19”; dòng cuối “2378-04-22 to 2446-05-10”.

## [MDB] MariaDB Documentation, *TIMESTAMP*
Tải: mariadb.com/docs/server/reference/data-types/date-and-time-data-types/timestamp (HTTP 200). Trang MySQL (dev.mysql.com) trả **403**,
web.archive.org trả **429** → không dạy chi tiết của MySQL.
- “From MariaDB 11.5: … the TIMESTAMP data type can hold values between '1970-01-01 00:00:01' ( UTC ) and '2106-02-07 06:28:15 UTC'.”
- “Before MariaDB 11.5: … the TIMESTAMP data type can hold values between '1970-01-01 00:00:01' ( UTC ) and '2038-01-19 03:14:07' ( UTC ).”

## [FAA15] FAA, Airworthiness Directive 2015-09-07 (Docket FAA-2015-0936), Federal Register 80 FR 24789, 1/5/2015 — Boeing 787
Trang federalregister.gov chặn tải tự động (“Request Access”); đọc qua **API chính thức** federalregister.gov/api/v1/documents/2015-10066.json
(HTTP 200, phần tóm tắt) và **bản PDF chính thức của GPO** govinfo.gov/content/pkg/FR-2015-05-01/pdf/2015-10066.pdf (HTTP 200, 233 795 byte).
- “a Model 787 airplane that has been powered continuously for 248 days can lose all alternating current (AC) electrical power due to the
  generator control units (GCUs) simultaneously going into failsafe mode. This condition is caused by a software counter internal to the
  GCUs that will overflow after 248 days of continuous power.”
- “We have been advised by Boeing of an issue identified during laboratory testing.” “If the four main GCUs (associated with the engine
  mounted generators) were powered up at the same time, after 248 days of continuous power, all four GCUs will go into failsafe mode at the
  same time, resulting in a loss of all AC electrical power regardless of flight phase.”
- “This AD requires a repetitive maintenance task for electrical power deactivation.” “We consider this AD interim action. The manufacturer
  is currently developing a GCU software upgrade”. Khoảng cách: “intervals not to exceed 120 days”.

## [PY] Python 3 documentation, *time — Time access and conversions*
Tải: docs.python.org/3/library/time.html (HTTP 200) — chỉ để đối chiếu, không dạy riêng:
- “… for 32-bit systems, it is typically in 2038.”

## Phép tính của bài (VER, không có trong nguồn)
- 2³¹ − 1 = 2 147 483 647 giây = 24 855 ngày dư 11 647 giây = 03:14:07; 1970–2037: 68 năm, 17 năm nhuận → 24 837 ngày; 24 855 − 24 837 = 18
  → 19/1/2038 (khớp [MDB] “2038-01-19 03:14:07” và [EXT4] “2038-01-19”). Giờ Việt Nam (UTC+7): 10:14:07.
- −2³¹ giây → 13/12/1901 20:45:52 UTC (khớp [EXT4] “1901-12-13”). 2³² − 1 → 2106-02-07 06:28:15 UTC (khớp [MDB] 11.5, [GL] 2.40 “2106”).
- 34 bit với gốc có dấu: 2³⁴ − 2³¹ − 1 giây → 2446-05-10 (khớp [EXT4] “May 2446”). 2⁶³ giây ≈ 292 tỉ năm.
- [FAA15] không ghi bộ đếm đếm đơn vị gì. Bài thử GIẢ THUYẾT “32 bit có dấu, mỗi 1/100 giây”: 2³¹ / 100 / 86 400 ≈ 248,55 ngày — trùng
  248 ngày, nhưng chỉ là giả thuyết, bài nói rõ “nguồn không ghi” (minh hoạ cách tách dữ kiện khỏi suy đoán của bài 0).

## Điều KHÔNG dạy (nguồn không ghi hoặc không đọc được)
- Đơn vị của bộ đếm trong GCU của 787: FAA không ghi → không khẳng định.
- MySQL TIMESTAMP: trang 403 → không dạy; chỉ dạy MariaDB theo trang đã đọc.
- Phiên bản nhân Linux đầu tiên “an toàn 2038” trọn vẹn: không có câu nào trong nguồn đã đọc khẳng định → không dạy; chỉ nói theo [LWN19]
  (nhân đã chuyển sang 64 bit bên trong; phần người dùng còn 32 bit) và [GL] (2.34 cần nhân tối thiểu 5.1).
- Số thiết bị nhúng còn dùng 32 bit trên thế giới: không có nguồn → không nêu số.
