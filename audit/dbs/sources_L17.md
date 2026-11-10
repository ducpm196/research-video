# Nguồn đã đọc nguyên văn cho DBS L17 (bài hành trình: tiến hoá lược đồ ở quy mô lớn)

Đọc ngày 2026-11-02 (curl + trích văn bản, hoặc WebFetch khi trang chặn curl). Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác
trong bài là phép tính lại (VER, `checks` của bài và `audit/dbs/verify_dbs.py` L17) hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá nhân
trong lời đọc; tên tác giả chỉ ở `source:`.

Đổi so với ROADMAP §8.1 mục 3 (Dynamo 2007 → DynamoDB 2022): người điều phối chỉ định theo ví dụ của người dùng — “thêm một cột khi đã có
vài triệu người dùng thì làm sao nhanh, hiệu quả, không lỗi dữ liệu cũ”. Dynamo/DynamoDB KHÔNG được đọc trong phiên này.

## [PT11] Percona Toolkit, *pt-online-schema-change* (tài liệu POD trong mã nguồn chính thức)
Tải: raw.githubusercontent.com/percona/percona-toolkit/3.x/bin/pt-online-schema-change (bản 3.7.2). Trang docs.percona.com trả 403
(Cloudflare) với curl → đọc cùng văn bản tài liệu ngay trong tệp mã nguồn của Percona.
- DESCRIPTION: “pt-online-schema-change emulates the way that MySQL alters tables internally, but it works on a copy of the table you wish to
  alter. This means that the original table is not locked, and clients may continue to read and change data in it.”
- DESCRIPTION: “works by creating an empty copy of the table to alter, modifying it as desired, and then copying rows from the original table
  into the new table. When the copy is complete, it moves away the original table and replaces it with the new one.”
- DESCRIPTION: “The data copy process is performed in small chunks of data, which are varied to attempt to make them execute in a specific
  amount of time … Any modifications to data in the original tables during the copy will be reflected in the new table, because the tool
  creates triggers on the original table to update the corresponding rows in the new table.”
- DESCRIPTION: “it uses an atomic RENAME TABLE operation to simultaneously rename the original and new tables.”
- DESCRIPTION (an toàn): “The tool pauses the data copy operation if it observes any replicas that are delayed in replication.” “The tool
  pauses or aborts its operation if it detects too much load on the server.” “In most cases the tool will refuse to operate unless a PRIMARY
  KEY or UNIQUE INDEX is present in the table.”
- `--chunk-time`: “type: float; default: 0.5 — Adjust the chunk size dynamically so each data-copy query takes this long to execute.”
- `--chunk-size`: “type: size; default: 1000 — Number of rows to select for each chunk copied.” (giá trị khởi đầu khi tự chỉnh theo chunk-time)
- `--max-load`: “default: Threads_running=25 — Examine SHOW GLOBAL STATUS after every chunk, and pause if any status variables are higher than
  their thresholds.”
- Bổ sung đợt C 2026-11-09 (curl raw.githubusercontent.com/percona/percona-toolkit/3.x/bin/pt-online-schema-change, VERSION “pt-online-schema-change
  3.7.2”): DESCRIPTION “The use of triggers means that the tool will not work if any triggers are already defined on the table.”;
  `--preserve-triggers`: “As of MySQL 5.7.2, it is possible to define multiple triggers for a given table that have the same trigger event and
  action time. This allows us to add the triggers needed for pt-online-schema-change even if the table already has its own triggers.” → bài ghi
  “theo tài liệu, bảng chưa có bộ kích hoạt nào (bản mới có tuỳ chọn nới điều kiện này)”; điều kiện khoá chính ghi “hầu như luôn” theo “In most cases”.
- ABOUT PERCONA TOOLKIT: “Percona Toolkit was forked from two projects in June, 2011: Maatkit and Aspersa.” COPYRIGHT: “This program is
  copyright 2011-2026 Percona LLC and/or its affiliates.”

## [GH16] GitHub Blog, *gh-ost: GitHub’s online schema migration tool for MySQL*, 2016-08-01
Tải: github.blog/news-insights/company-news/gh-ost-github-s-online-migration-tool-for-mysql/ (curl, 184 977 byte).
- “MySQL table migration is a well known problem, and has been addressed by online schema change tools since 2009. Growing, fast-paced products
  often require changes to database structure. Adding/changing/removing columns and indexes etc., are blocking operations with the default
  MySQL behavior. We conduct such schema changes multiple times per day and wish to minimize user facing impact.”
- “MySQL’s Online DDL for InnoDB is only “online” on the server on which it is invoked. Replication stream serializes the alter which causes
  replication lag. … The DDL is uninterruptible … it cannot throttle or pause on high load.”
- “We’ve been using pt-online-schema-change for years. However as we grew in volume and traffic, we hit more and more problems, to the point of
  considering many migrations as “risky operations”. Some migrations would only be able to run during off-peak hours or through weekends;
  others would consistently cause MySQL outage.”
- “they create a ghost table, in the likeness of your original table, migrate that table while empty, slowly and incrementally copy data from
  your original table to the ghost table, meanwhile propagating ongoing changes … When the tool is satisfied the tables are in sync, it
  replaces your original table with the ghost table.”
- “Triggers … are interpreted code. … they add the overhead of a parser and interpreter to each query acting on your migrated table.”
- “Locks: … Lock contention is directly related to write concurrency on the master. We have experienced near or complete lock downs in
  production, to the effect of rendering the table or the entire database inaccessible due to lock contention.”
- “We’ve seen stalls to the extent of many seconds to a minute while attempting to remove triggers from a busy table at the end of a migration”.
- “Non pausability: … While it may suspend the row-copy operation, it cannot suspend the triggers. Removal of the triggers results in data loss.
  … On busy servers, we have seen that even as the online operation throttles, the master is brought down by the load of the triggers.”
- Triggerless: “gh-ost does not use triggers. It intercepts changes to table data by tailing the binary logs. It therefore works in an
  asynchronous approach, applying the changes to the ghost table some time after they’ve been committed.”
- Lightweight: “the master only observes a single connection that is sequentially writing to the ghost table.”
- Pauseable: “gh-ost is able to suspend all writes to the master when throttling. Throttling implies no row-copy on the master and no row
  updates.” Ví dụ điều tiết theo truy vấn: “Consider SELECT HOUR(NOW()) BETWEEN 8 and 17.” “Flag file: touch a file and gh-ost begins
  throttling. Remove the file and it resumes work.”
- Dynamically controllable: “chunk-size=1500, max-lag-millis=2000, max-load=Thread_running=30 are examples to instructions gh-ost accepts”.
- Testable: “Each of our production tables, as small as empty and as large as many hundreds of GB, is being migrated via a trivial statement
  that does not really modify its structure (engine=innodb). … We take complete checksum of entire table data from both the original table and
  ghost table and expect them to be identical.”
- Trustable: “we’ve completed thousands of successful migrations before trying it out on masters for the first time.” “You can instruct
  gh-ost to postpone the cut-over using a flag file. gh-ost will complete the row-copy but will not flip the tables. Instead, it will keep
  applying ongoing changes”.
- “gh-ost is now powering all of our production migrations. We’re running it daily … sometimes multiple times a day.”

## [ST17] Stripe Blog, *Online migrations at scale*, 2017-02-02
Tải: stripe.com/blog/online-migrations (curl).
- “In this post, we’ll explain how we safely did one large migration of our hundreds of millions of Subscriptions objects.”
- Scale: “Imagine that it takes one second to migrate each subscription object: in sequential fashion, it would take over three years to
  migrate one hundred million objects.”
- Uptime: “We perform all infrastructure upgrades online, rather than relying on planned maintenance windows.”
- “There’s a common 4 step dual writing pattern … Dual writing to the existing and new tables to keep them in sync. Changing all read paths in
  our codebase to read from the new table. Changing all write paths in our codebase to only write to the new table. Removing old data that
  relies on the outdated data model.”
- “We can mitigate performance concerns by slowly ramping up the percentage of objects that get duplicated, while keeping a careful eye on
  operational metrics.”
- “whenever objects are updated, they will automatically be copied over to the new table … Finally, we’ll backfill any remaining Customer
  subscriptions into the new Subscriptions table.”
- “The most expensive part of backfilling the new table on the live database is simply finding all the objects that need migration. …
  we were able to offload this to an offline process that had no impact on our production databases. We make snapshots of our databases
  available to our Hadoop cluster, which lets us use MapReduce”.
- “Run a large, multi-threaded migration to duplicate these subscriptions with a fleet of processes … in parallel. Once the migration is
  complete, run the Scalding job once again to make sure there are no existing subscriptions missing”.
- Reads: “Use Scientist to read from both the Subscriptions table and the Customers table. If the results don’t match, raise an error”.
- Conclusion: “All the changes we made were incremental. We never attempted to change more than a few hundred lines of code at one time.”

## [MY18] MySQL Server Blog, *MySQL 8.0: InnoDB now supports Instant ADD COLUMN*, 2018-05-09; MySQL 8.0.12 Release Notes, 2018-07-27
Tải: dev.mysql.com/blog-archive/mysql-8-0-innodb-now-supports-instant-add-column/ và dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-12.html
(curl bị 403 → WebFetch, yêu cầu trích nguyên văn).
- Blog: “Prior to MySQL 5.6 the only way to do DDL was to COPY the rows one by one.” “Up until 8.0 …, InnoDB used to add columns to a table by
  rebuilding the table even for the INPLACE DDL algorithm.” “For large tables it can take a long time especially in a Replication setup.”
  “Disk space requirements will be more than double, roughly the same size as the existing table.”
- Blog: “only metadata changes are made in the data dictionary … we don’t touch the data of the table.” “After an instant ADD COLUMN is
  issued, any update to the table will write rows in the new format along. The default values if any are looked up from the data dictionary.”
- Blog, giới hạn: “Only support adding columns in one statement, that is if there are other non-INSTANT operations in the same statement, it
  can’t be done instantly”; “Only support adding columns at last, not in the middle of existing columns”.
- Blog: “This INSTANT ADD COLUMN patch was contributed by the Tencent Games DBA Team.”
- 8.0.12: “InnoDB now supports ALGORITHM=INSTANT for … Adding a column. … Operations that support ALGORITHM=INSTANT only modify metadata in the
  data dictionary. … table data is unaffected, making the operations instantaneous. If not specified explicitly, ALGORITHM=INSTANT is used by
  default by operations that support it. If ALGORITHM=INSTANT is specified but not supported, the operation fails immediately with an error.”

## [PG18] PostgreSQL 11 Release Notes (Release date: 2018-10-18); thông cáo “PostgreSQL 11 Released!”, 2018-10-18
Tải: www.postgresql.org/docs/release/11.0/ và www.postgresql.org/about/news/postgresql-11-released-1894/ (curl).
- E.23.3.3 Utility Commands: “Allow ALTER TABLE to add a column with a non-null default without doing a table rewrite … This is enabled when
  the default value is a constant.”
- Thông cáo: “Removing the need for ALTER TABLE .. ADD COLUMN .. DEFAULT .. with a not NULL default to rewrite the whole table on execution,
  which provides a significant performance boost when running this command.”
- Bổ sung 2026-11-08 (đọc kiểm): PostgreSQL 10 Documentation, ALTER TABLE, mục Notes (www.postgresql.org/docs/10/sql-altertable.html, WebFetch):
  “If there is no DEFAULT clause, this is merely a metadata change and does not require any immediate update of the table's data; the added
  NULL values are supplied on readout, instead.” → bài ghi “cột để rỗng, không mặc định, thì từ trước đã chỉ sửa siêu dữ liệu”, và câu
  “trước 2018 thêm cột là dựng lại cả bảng” chỉ áp cho MySQL (nguồn [MY18]: “Up until 8.0 …, InnoDB used to add columns … by rebuilding”).

## [MY22] MySQL 8.0.29 Release Notes, 2022-04-26
Tải: dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-29.html (WebFetch).
- “InnoDB now supports ALTER TABLE ... DROP COLUMN operations using ALGORITHM=INSTANT.”
- “Prior to MySQL 8.0.29, an instantly added column could only be added as the last column of the table. From MySQL 8.0.29, an instantly added
  column can be added to any position in the table.”
- “Instantly added or dropped columns create a new row version. Up to 64 row versions are permitted. A new TOTAL_ROW_VERSIONS column was added
  to the INFORMATION_SCHEMA.INNODB_TABLES table to track the number of row versions.”

## Điều KHÔNG dạy (nguồn không ghi)
- Năm ra đời riêng của pt-online-schema-change: [PT11] chỉ ghi bộ công cụ tách ra tháng 6/2011 và bản quyền từ 2011; [GH16] ghi công cụ loại
  này có “since 2009”. Bài nói “từ 2009, và trong bộ công cụ năm 2011”, không nói tên công cụ đầu tiên hay tác giả.
- Số dòng, kích thước bảng, thời gian thật của một lần đổi lược đồ ở GitHub hay Stripe: không có. Bảng 5 triệu dòng (cỡ ≈ 0,4 GB tính lại từ 50 000 trang 8 KB; đợt C thay “200 GB” cũ vốn mâu thuẫn với 100 dòng mỗi trang), 28 giờ chép,
  1000 tiến trình, 2 cột mỗi tháng là SỐ MINH HOẠ, ghi rõ trên màn hình.
- Khi chạm giới hạn 64 phiên bản dòng thì MySQL làm gì: [MY22] không ghi → không dạy; chỉ dạy “theo dõi cột đếm”.
- Phiên bản 8.0.x cụ thể của bài blog [MY18]: blog không ghi; lấy từ release notes 8.0.12.
- Cơ chế bên trong của PostgreSQL 11 (lưu giá trị mặc định ở đâu): release notes không ghi → chỉ dạy “không viết lại bảng, khi mặc định là hằng”.
- Dynamo 2007 / DynamoDB 2022 (ứng viên cũ của ROADMAP): không đọc, không dạy.
