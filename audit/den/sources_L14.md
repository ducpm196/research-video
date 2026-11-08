# Nguồn đã đọc nguyên văn cho DEN L14 (bài hành trình: từ ánh xạ rồi rút gọn tới mô hình luồng dữ liệu)

Đọc ngày 2026-11-02: tải PDF bằng curl, trích văn bản bằng `pdftotext` (có và không có `-layout`), đọc các mục được trích dưới đây.
Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác trong bài là phép tính lại (VER, `checks` của bài và
`audit/den/verify_den.py` L14) hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:`.

Ba nguồn ứng viên của ROADMAP §8.1 mục 3 (OSDI 2004, NSDI 2012, VLDB 2015) đều đọc được và khớp nội dung. Thêm một nguồn cho chặng cuối
“ổn định và tiếp tục phát triển”: bài CACM 2016 của chính nhóm làm Spark [SP16] — lý do: ba bài kia là bài công bố ý tưởng; chỉ [SP16] ghi
lại hệ đã ra sao sau nhiều năm có rất nhiều người dùng (người đóng góp, số tổ chức, cụm lớn nhất, thư viện chuẩn). Bài CACM 2008 về
MapReduce (có số liệu năm 2007) KHÔNG đọc được (cacm.acm.org trả trang chặn của Cloudflare) → không dùng, không dạy số liệu năm 2007.

## [MR04] J. Dean, S. Ghemawat, *MapReduce: Simplified Data Processing on Large Clusters*, OSDI 2004
Tải: static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf (13 trang, 190 711 byte).
- Abstract: “a typical MapReduce computation processes many terabytes of data on thousands of machines. … hundreds of MapReduce programs
  have been implemented and upwards of one thousand MapReduce jobs are executed on Google's clusters every day.”
- §1: “Over the past five years, the authors and many others at Google have implemented hundreds of special-purpose computations that
  process large amounts of raw data”. “we designed a new abstraction that allows us to express the simple computations we were trying to
  perform but hides the messy details of parallelization, fault-tolerance, data distribution and load balancing in a library.”
  “to use re-execution as the primary mechanism for fault tolerance.”
- §3.3: “Completed map tasks are re-executed on a failure because their output is stored on the local disk(s) of the failed machine and is
  therefore inaccessible. Completed reduce tasks do not need to be re-executed since their output is stored in a global file system.”
  “network maintenance on a running cluster was causing groups of 80 machines at a time to become unreachable for several minutes. The
  MapReduce master simply re-executed the work done by the unreachable worker machines”.
- §3.5: “we tend to choose M so that each individual task is roughly 16 MB to 64 MB of input data … We often perform MapReduce computations
  with M = 200,000 and R = 5,000, using 2,000 worker machines.”
- §3.6 Backup Tasks: “a "straggler": a machine that takes an unusually long time to complete one of the last few map or reduce tasks”.
  “a machine with a bad disk may experience frequent correctable errors that slow its read performance from 30 MB/s to 1 MB/s.”
  “When a MapReduce operation is close to completion, the master schedules backup executions of the remaining in-progress tasks.”
  “typically increases the computational resources used by the operation by no more than a few percent.”
- §5.1: “a cluster that consisted of approximately 1800 machines.” §5.3: “The sort program sorts 10^10 100-byte records (approximately
  1 terabyte of data).” “the input data is split into 64MB pieces (M = 15000).” “Including startup overhead, the entire computation takes
  891 seconds.”
- §5.4: “with backup tasks disabled … The entire computation takes 1283 seconds, an increase of 44% in elapsed time.”
- §5.5: “we intentionally killed 200 out of 1746 worker processes several minutes into the computation. … The entire computation finishes in
  933 seconds including startup overhead (just an increase of 5% over the normal execution time).”
- §6: “We wrote the first version of the MapReduce library in February of 2003, and made significant enhancements to it in August of 2003,
  including the locality optimization, dynamic load balancing of task execution across worker machines, etc.”
  “from 0 in early 2003 to almost 900 separate instances as of late September 2004.” “it makes it possible to write a simple program and run
  it efficiently on a thousand machines in the course of half an hour”.
- Table 1 “MapReduce jobs run in August 2004”: Number of jobs 29,423; Average job completion time 634 secs; Machine days used 79,186 days;
  Input data read 3,288 TB; Intermediate data produced 758 TB; Output data written 193 TB; Average worker machines per job 157; Average worker
  deaths per job 1.2; Average map tasks per job 3,351; Average reduce tasks per job 55. (Bảng trích bằng `pdftotext`, nhãn và số theo cùng thứ tự.)
- §6.1: “the size of one phase of the computation dropped from approximately 3800 lines of C++ code to approximately 700 lines when expressed
  using MapReduce.” “one change that took a few months to make in our old indexing system took only a few days to implement in the new system.”
- §8: “Second, network bandwidth is a scarce resource. … the locality optimization allows us to read data from local disks, and writing a
  single copy of the intermediate data to local disk saves network bandwidth. Third, redundant execution can be used to reduce the impact of
  slow machines, and to handle machine failures and data loss.” “restricting the programming model makes it easy to parallelize and
  distribute computations and to make such computations fault-tolerant.”

## [RDD12] M. Zaharia và cộng sự, *Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing*, NSDI 2012
Tải: www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf (886 315 byte).
- Abstract: “RDDs are motivated by two types of applications that current computing frameworks handle inefficiently: iterative algorithms
  and interactive data mining tools. In both cases, keeping data in memory can improve performance by an order of magnitude.”
- §1: “in most current frameworks, the only way to reuse data between computations (e.g., between two MapReduce jobs) is to write it to an
  external stable storage system, e.g., a distributed file system. This incurs substantial overheads due to data replication, disk I/O, and
  serialization, which can dominate application execution times.”
- §1: “the only ways to provide fault tolerance are to replicate the data across machines or to log updates across machines. Both approaches
  are expensive for data-intensive workloads”. “RDDs provide an interface based on coarse-grained transformations (e.g., map, filter and
  join) … This allows them to efficiently provide fault tolerance by logging the transformations used to build a dataset (its lineage)
  rather than the actual data.”
- §1: “Spark is up to 20× faster than Hadoop for iterative applications, speeds up a real-world data analytics report by 40×, and can be used
  interactively to scan a 1 TB dataset with 5–7s latency.”
- §2.1: “an RDD is a read-only, partitioned collection of records.” §2.3: “only the lost partitions of an RDD need to be recomputed upon
  failure, and they can be recomputed in parallel on different nodes, without having to roll back the whole program.”
- §2.4: “RDDs would be less suitable for applications that make asynchronous fine-grained updates to shared state, such as a storage system
  for a web application or an incremental web crawler.”
- §4 (phụ thuộc hẹp/rộng): “in a lineage graph with wide dependencies, a single failed node might cause the loss of some partition from all the
  ancestors of an RDD, requiring a complete re-execution.” §5.4: “it can be helpful to checkpoint some RDDs to stable storage.”
- §5: “Spark can read data from any Hadoop input source (e.g., HDFS or HBase) using Hadoop's existing input plugin APIs”.
- §6.1: “We ran both algorithms for 10 iterations on 100 GB datasets using 25–100 machines.” “For logistic regression, Spark 25.3× and 20.7×
  faster than Hadoop and HadoopBinMem respectively on 100 machines.” Hình 7 (nhãn số trên cột, logistic regression, 100 máy): Hadoop
  lượt đầu 80 s, các lượt sau 76 s; HadoopBinMem 139 s, 62 s; Spark 46 s, 3 s. (76 / 3 ≈ 25,3 và 62 / 3 ≈ 20,7 khớp câu chữ của §6.1.)
- §6.1: “we ran no-op Hadoop jobs, and saw that these at incurred least 25s of overhead”.
- §6.3: “Figure 11 compares the running times for 10 iterations of k-means on a 75-node cluster … each iteration consisted of 400 tasks working
  on 100 GB of data. Until the end of the 5th iteration, the iteration times were about 58 seconds. In the 6th iteration, one of the machines
  was killed … which increased the iteration time to 80s. Once the lost RDD partitions were reconstructed, the iteration time went back down
  to 58s.”
- §6.6: “Even at 1 TB of data, queries on Spark took 5–7 seconds. … querying the 1 TB file from disk took 170s.”

## [DF15] T. Akidau và cộng sự, *The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing*, PVLDB 8(12), 2015 (VLDB 2015)
Tải: www.vldb.org/pvldb/vol8/p1792-Akidau.pdf (365 591 byte).
- Abstract: “Unbounded, unordered, global-scale datasets are increasingly common in day-to-day business (e.g. Web logs, mobile usage
  statistics, and sensor networks).” “one can never fully optimize along all dimensions of correctness, latency, and cost”. “We as a field
  must stop trying to groom unbounded datasets into finite pools of information that eventually become complete, and instead live and
  breathe under the assumption that we will never know if or when we have seen all of our data”.
- §1: “Batch systems such as MapReduce (and its Hadoop variants, including Pig and Hive), FlumeJava, and Spark suffer from the latency
  problems inherent with collecting all input data into a batch before processing it.”
- §1: bốn câu hỏi “What results are being computed. Where in event time they are being computed. When in processing time they are
  materialized. How earlier results relate to later refinements.”
- §1.2: “Fixed windows (sometimes called tumbling windows) are defined by a static window size, e.g. hourly windows or daily windows.”
  “Sessions are windows that capture some period of activity over a subset of the data, in this case per key. Typically they are defined by a
  timeout gap.”
- §1.3: “Event Time, which is the time at which the event itself actually occurred”. “Processing Time, which is the time at which an event is
  observed at any given point during processing within the pipeline”.
- §2.2.1 / Hình 3: “windowing a dataset by sliding windows of two-minute width and one-minute period” → mỗi phần tử nằm trong 2 cửa sổ
  (ví dụ (k, v1, 12:00) vào [11:59, 12:01) và [12:00, 12:02)).
- §2.2.2 / Hình 4: “windowed by session, with a 30-minute session timeout”; dữ liệu (k1, 13:02), (k2, 13:14), (k1, 13:57), (k1, 13:20);
  “The sessions implementation of AssignWindows puts each element into a single window that extends 30 minutes beyond its own timestamp”;
  “the windows for v1 and v4 overlap, so the sessions windowing strategy merges them into a single new, larger session”.
- §2.3 (mốc nước): “They are sometimes too fast, meaning there may be late data that arrives behind the watermark.” “They are sometimes too
  slow. … the watermark can be held back for the entire pipeline by a single slow datum.” “we postulate that watermarks alone are insufficient.”
  Lambda Architecture: “it simply provides the best low-latency estimate of a result that the streaming pipeline can provide, with the promise of
  eventual consistency and correctness once the batch pipeline runs”.
- §2.3: ba chế độ. Discarding: “Upon triggering, window contents are discarded, and later results bear no relation to previous results. This mode
  is useful in cases where the downstream consumer … expects the values from various trigger fires to be independent (e.g. when injecting into a
  system that generates a sum of the values injected).” Accumulating: “This is useful when the downstream consumer expects to overwrite old values
  with new ones when receiving multiple results for the same window”. Accumulating & Retracting: “When the window triggers again in the future, a
  retraction for the previous value will be emitted first, followed by the new value”; “Retractions are necessary in pipelines with multiple serial
  GroupByKeyAndWindow operations, since the multiple results generated by a single window over subsequent trigger fires may end up on separate keys
  when grouped downstream.”
- §3.3.4: “Given the high level of accuracy we achieve with watermarks for structured input sources like log files, such customers find watermarks
  very effective in triggering a single, highly-accurate aggregate per window.”
- §3.3.5: một đường ống gợi ý dùng kích hoạt theo thời gian xử lý vì “having regularly updated, partial views on the data was much more valuable
  than waiting until mostly complete views were ready”.
- §3.2 Design Principles: “Never rely on any notion of completeness.”
- §3.3.1: “One particularly large log join pipeline runs in streaming mode on MillWheel by default, but has a separate FlumeJava batch
  implementation used for large scale backfills. A much nicer setup would be to have a single implementation written in a unified model”.
  “one MillWheel customer ran their streaming pipeline in weak consistency mode, with a nightly MapReduce to generate truth. They found that
  customers stopped trusting the weakly consistent results over time”.
- §3.3.3: “Lacking a principled system for updates and retractions, a team that processed resource utilization statistics ended up leaving our
  platform to build a custom solution”. “Another billing team had significant issues with watermark lags caused by stragglers in their input.”
- §3.3.4: “For them, 100% accuracy is not required, but having a largely complete view of their data in a reasonable amount of time is.”
- §4: “The future of data processing is unbounded data.”

## [SP16] M. Zaharia và cộng sự, *Apache Spark: A Unified Engine for Big Data Processing*, Communications of the ACM 59(11), 11/2016
Tải: people.eecs.berkeley.edu/~matei/papers/2016/cacm_apache_spark.pdf (DOI 10.1145/2934664).
- “In 2009, our group at the University of California, Berkeley, started the Apache Spark project to design a unified engine for distributed
  data processing.” “In six years, Apache Spark has grown to 1,000 contributors and thousands of deployments.”
- “Since its release in 2010, Spark has grown to be the most active open source project or big data processing, with more than 1,000
  contributors. The project is in use in more than 1,000 organizations … The largest publicly announced deployment has more than 8,000 nodes.”
- “whereas prior systems required writing the data to storage to pass it to another engine, Spark can run diverse functions over the same
  data, often in memory.”
- Spark Streaming: “we split the input data into small batches (such as every 200 milliseconds) that we regularly combine with state stored
  inside RDDs to produce new results.”
- “In 2014, … Spark sorted 100TB of data 3× faster than the previous record holder based on Hadoop MapReduce using 10× fewer machines. This
  benchmark was not executed in memory but rather on (solidstate) disks.”
- “One benefit of doing these optimizations in a general engine is that they simultaneously affect all of Spark's libraries”.
- “with over 60% of organizations using at least three of Spark's APIs” (khảo sát 7/2015, 1,400 người trả lời). “In our July 2015 survey,
  60% of respondents reported using them [DataFrames].”

## Điều KHÔNG dạy (nguồn không ghi)
- Số liệu MapReduce năm 2007–2008 (bài CACM 2008): không đọc được → không dạy.
- Tốc độ của Spark so với ánh xạ rồi rút gọn ở MỌI loại việc: [RDD12] chỉ ghi “up to 20×” cho việc lặp; k-means chỉ 1,9×–3,2×; lượt đầu
  “moderately faster”. Bài không nói “Spark nhanh gấp 100 lần” (con số hay được kể lại, không có trong hai bài đã đọc).
- Thời gian ra đời, số máy, số người dùng của chính hệ Cloud Dataflow: [DF15] chỉ ghi “an external reimplementation for Cloud Dataflow is
  largely complete at the time of writing” → không dạy quy mô của Cloud Dataflow; không nói gì về Apache Beam (chưa đọc nguồn).
- Nhóm rời nền tảng: [DF15] §3.3.3 ghi đó là “a team that processed resource utilization statistics” (nhóm xử lý thống kê sử dụng tài
  nguyên), KHÔNG phải nhóm thanh toán; nhóm thanh toán (“another billing team”) là nhóm gặp mốc nước trễ do tác vụ chậm. Nguồn không ghi tên
  nhóm, thời gian, quy mô → chỉ dạy “một nhóm xử lý thống kê sử dụng tài nguyên … rời nền tảng để tự làm” (sửa 2026-11-08: bản trước gọi nhầm
  là nhóm thanh toán).
- Ai nghĩ ra “kiến trúc Lambda”: [DF15] không ghi → không dạy.
- Tổng thời gian 10 lượt lặp (764 s, 73 s), thời gian thêm do mất máy (22 s), số phiên, số cửa sổ: là PHÉP TÍNH LẠI từ số của nguồn, ghi VER.
  Tổng 7 rồi 10 của một cửa sổ, đội 3 người, 100 GB, 20 lượt (dùng số đo Hình 7 của [RDD12] làm giả định), cửa sổ 5 phút, trễ 10 phút ở phần
  quiz là SỐ MINH HOẠ.
- Số bản chép khi ghi giữa hai việc: [RDD12] chỉ ghi “data replication”, không ghi số bản → hình vẽ ghi “nhiều bản”.
- “Dữ liệu tới sau mốc nước bị bỏ”: [DF15] không nói như vậy (chỉ nói mốc nước có thể quá nhanh) → bài nói “không có trong kết quả đã xuất”.
