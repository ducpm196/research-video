# Nguồn đã đọc nguyên văn cho CAS L08 (GitLab.com, sự cố cơ sở dữ liệu 31/1/2017)

Đọc ngày 2026-11-02 (urllib + trích văn bản HTML; bản tải ở thư mục nháp của phiên). Chỉ trích các câu bài giảng dựa vào (CITED). Khoảng
thời gian, tỉ số, ước lượng 486 GB là phép tính lại (VER: `checks`, `audit/cas/ver/L08.py`, `audit/verify_plan_curricula.py` CAS:L08).

## [GL17] GitLab, *Postmortem of database outage of January 31* (“Published on: February 10, 2017”)
URL: https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/ (HTTP 200, 226 278 byte). Bài hậu kiểm chính thức.
- “The outage was caused by an accidental removal of data from our primary database server.”
- “we lost modifications to database data such as projects, comments, user accounts, issues and snippets, that took place between 17:20 and
  00:00 UTC on January 31. Our best estimate is that it affected roughly 5,000 projects, 5,000 comments and 700 new user accounts. Code
  repositories or wikis hosted on GitLab.com were unavailable during the outage, but were not affected by the data loss.”
  Mục “Data loss impact” ghi khác: “created between January 31st 17:20 UTC and 23:30 UTC has been lost” → bài dùng 23:30, nói “khoảng”.
- “± 17:20 UTC: prior to starting this work, our engineer took an LVM snapshot of the production database and loaded this into the staging
  environment. … This procedure normally happens automatically once every 24 hours (at 01:00 UTC)”.
- “± 19:00 UTC: GitLab.com starts experiencing an increase in database load due to what we suspect was spam.” “part of the load was caused by a
  background job trying to remove a GitLab employee and their associated data. This was the result of their account being flagged for abuse and
  accidentally scheduled for removal.”
- “± 23:00 UTC: Due to the increased load, our PostgreSQL secondary's replication process started to lag behind. The replication failed as WAL
  segments needed by the secondary were already removed from the primary. As GitLab.com was not using WAL archiving, the secondary had to be
  re-synchronised manually.”
- “pg_basebackup would hang, producing no meaningful output”. “± 23:30 UTC: one of the engineers thinks that perhaps pg_basebackup created some
  files in the PostgreSQL data directory of the secondary during the previous attempts”. “Unfortunately this was not clearly documented in our
  engineering runbooks nor in the official pg_basebackup document.”
- “an engineer proceeds to wipe the PostgreSQL database directory, errantly thinking they were doing so on the secondary. Unfortunately this
  process was executed on the primary instead. The engineer terminated the process a second or two after noticing their mistake, but at this
  point around 300 GB of data had already been removed.”
- “Unfortunately the process of both finding and using backups failed completely.”
- Bốn cách: “Every 24 hours a backup is generated using pg_dump , this backup is uploaded to Amazon S3.” “Every 24 hours we generate an LVM
  snapshot of the disk storing the production database data. This snapshot is then loaded into the staging environment”. “For various servers
  (e.g. the NFS servers storing Git data) we use Azure disk snapshots. These snapshots are taken once per 24 hours.” “Replication between
  PostgreSQL hosts, primarily used for failover purposes and not for disaster recovery.”
- “The S3 bucket was empty”. “the backup procedure was using pg_dump 9.2, while our database is running PostgreSQL 9.6 … A difference in major
  versions results in pg_dump producing an error, terminating the backup procedure.” “Unfortunately DMARC was not enabled for the cronjob
  emails, resulting in them being rejected by the receiver. This means we were never aware of the backups failing, until it was too late.”
- “While enabled for the NFS servers, these snapshots were not enabled for any of the database servers as we assumed that our other backup
  procedures were sufficient.”
- “the produced snapshots are not really meant to be used for disaster recovery. At the time of the outage we had two snapshots available: A
  snapshot created for our staging environment every 24 hours, almost 24 hours before the outage happened. A snapshot created manually by one of
  the engineers roughly 6 hours before the outage.” “To recover GitLab.com we decided to use the LVM snapshot created 6 hours before … (the
  alternative was to lose almost 24 hours of data).”
- “Copying the data from the staging to the production host took around 18 hours. These disks are network disks and are throttled to a really
  low number (around 60Mbps)”.
- “On February 1st at 17:00 UTC we managed to restore the GitLab.com database without webhooks.” “Around 18:00 UTC we finished the final
  restoration procedures”.
- “The document in question was initially private … and contained name of the engineer who accidentally removed the data. … we will redact
  names in future cases”.
- 5 Whys: “Problem 1: GitLab.com was down for about 18 hours.” … “Restoring this required manual work as this was not automated, nor was it
  documented properly.” “Problem 2: restoring GitLab.com took over 18 hours.” “Why was the backup procedure not tested on a regular basis? -
  Because there was no ownership, as a result nobody was responsible for testing this procedure.”
- Việc cần làm: “Update PS1 across all hosts to more clearly differentiate between hosts and environments”, “Prometheus monitoring for backups”,
  “Hourly LVM snapshots of the production databases”, “Automated testing of recovering PostgreSQL database backups”, “Assign an owner for data
  durability”. “one could alias rm to something safer but in doing so would only protect themselves against accidentally running rm -rf
  /important-data , not against disk corruption or any of the many other ways you can lose data.” “An ideal environment is one in which you can
  make mistakes but easily and quickly recover from them with minimal to no impact.” “LVM snapshots are now taken every hour instead of once
  per 24 hours.”

## Phép tính của bài (VER)
- 17:20 → 23:30 = 370 phút = 6 giờ 10; 01:00 → 23:30 = 1350 phút = 22 giờ 30; tỉ số ≈ 3,6; 23:30 → 18:00 hôm sau = 18 giờ 30.
- 60 Mbit/s = 7,5 MB/s; × 18 giờ ≈ 486 GB — ƯỚC LƯỢNG của bài (nguồn không ghi cỡ dữ liệu đã chép), ghi rõ trên màn hình.
- Quiz 200 GB: 7,4 giờ ở 60 Mbit/s; 1600 s ≈ 26,7 phút ở 1 Gbit/s (số minh hoạ).

## Sai sót giáo án đã sửa
- Tên bài cũ “… năm cách sao lưu không dùng được”: bài hậu kiểm chính thức liệt kê **bốn** cách (pg_dump, LVM, Azure, sao chép), ba cách không
  dùng được, cách thứ tư (ảnh LVM cho môi trường thử) cứu được dữ liệu. Câu “5 cách” chỉ có trong tài liệu theo dõi trực tiếp (Google Docs) mà
  phiên này không đọc → đổi tên bài và `example` (VER CAS:L08 cập nhật). Bản đồ khoá ở L00 cần sửa câu “năm cách sao lưu” (báo người điều phối).

## Điều KHÔNG dạy
- Tên kỹ sư; tên các máy (db1/db2); lệnh cụ thể. Không gọi là “lỗi của một người”.
- “5 trên 5 cách sao lưu không chạy”: không có trong bài hậu kiểm chính thức → không dạy.
- Cỡ cơ sở dữ liệu: nguồn chỉ ghi “around 300 GB … removed” → không khẳng định tổng cỡ.
