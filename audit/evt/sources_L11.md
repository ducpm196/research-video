# Nguồn đã đọc nguyên văn cho EVT L11 (bài hành trình: nhật ký sự kiện của LinkedIn → bỏ ZooKeeper)

Đọc ngày 2026-11-02 (tải bằng curl/WebFetch, trích văn bản bằng pdftotext hoặc bóc thẻ HTML; bản tải ở thư mục nháp của phiên).
Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác trong bài là phép tính lại (VER, `checks` của bài và
`audit/evt/verify_evt.py` L11) hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:`.

## [K11] J. Kreps, N. Narkhede, J. Rao. *Kafka: a Distributed Messaging System for Log Processing.* NetDB’11, 12/6/2011, Athens
Tải: https://www.microsoft.com/en-us/research/wp-content/uploads/2017/09/Kafka.pdf (7 trang, đọc được trọn vẹn).
- Tóm tắt: “We have been using Kafka in production for some time and it is processing hundreds of gigabytes of new data each day.”
- §1: “At LinkedIn (a social network site), we found that in addition to traditional offline analytics, we needed to support most of the real-time applications mentioned above with delays of no more than a few seconds.”
- §1: “Kafka has been open sourced and used successfully in production at LinkedIn for more than 6 months. It greatly simplifies our infrastructure, since we can exploit a single piece of software for both online and offline consumption of the log data of all types.”
- §2: “JMS has no API to allow the producer to explicitly batch multiple messages into a single request. This means each message requires a full TCP/IP roundtrip, which is not feasible for the throughput requirements of our domain.”
- §2: “many messaging systems assume near immediate consumption of messages … Their performance degrades significantly if messages are allowed to accumulate, as is the case for offline consumers such as data warehousing applications that do periodic large loads”
- §2: “At LinkedIn, we find the "pull" model more suitable for our applications since each consumer can retrieve the messages at the maximum rate it can sustain and avoid being flooded by messages pushed faster than it can handle.”
- §3.1: “Each partition of a topic corresponds to a logical log. Physically, a log is implemented as a set of segment files of approximately the same size (e.g., 1GB). Every time a producer publishes a message to a partition, the broker simply appends the message to the last segment file.”
- §3.1: “a message stored in Kafka doesn't have an explicit message id. Instead, each message is addressed by its logical offset in the log.”
- §3.1 (Stateless broker): “the information about how much each consumer has consumed is not maintained by the broker, but by the consumer itself … A message is automatically deleted if it has been retained in the broker longer than a certain period, typically 7 days.”
- §3.1: “A consumer can deliberately rewind back to an old offset and re-consume data. … when there is an error in application logic in the consumer, the application can re-play certain messages after the error is fixed.”
- §3.2: “we employ a highly available consensus service Zookeeper” — dùng cho “(1) detecting the addition and the removal of brokers and consumers, (2) triggering a rebalance process in each consumer …, and (3) maintaining the consumption relationship and keeping track of the consumed offset of each partition.”
- §3.3: “In general, Kafka only guarantees at-least-once delivery.” “Kafka guarantees that messages from a single partition are delivered to a consumer in order. However, there is no guarantee on the ordering of messages coming from different partitions.”
- §3.3: “If a broker goes down, any message stored on it not yet consumed becomes unavailable. If the storage system on a broker is permanently damaged, any unconsumed message is lost forever. In the future, we plan to add built-in replication”
- §4: “Without too much tuning, the end-to-end latency for the complete pipeline is about 10 seconds on average”
- §4: “Currently, Kafka accumulates hundreds of gigabytes of data and close to a billion messages per day”
- §4 (kiểm đếm): “each producer … periodically generates a monitoring event, which records the number of messages published by that producer for each topic within a fixed time window … The consumers can then count the number of messages that they have received from a given topic and validate those counts”
- §5: “we ran a single producer to publish a total of 10 million messages, each of 200 bytes. We configured the Kafka producer to send messages in batches of size 1 and 50.” “On average, Kafka can publish messages at the rate of 50,000 and 400,000 messages per second for batch size of 1 and 50, respectively.”
- §5: “With a batch size of 50, a single Kafka producer almost saturated the 1Gb link between the producer and the broker.” “the Kafka producer currently doesn't wait for acknowledgements from the broker … there is no guarantee that every published message is actually received by the broker.”
- §5: “In Kafka, a batch size of 50 messages improved the throughput by almost an order of magnitude.”

## [V15] G. Wang, J. Koshy, S. Subramanian, K. Paramasivam, M. Zadeh, N. Narkhede, J. Rao, J. Kreps, J. Stein. *Building a Replicated Logging System with Apache Kafka.* PVLDB 8(12), 2015 (VLDB 2015)
Tải: https://www.vldb.org/pvldb/vol8/p1654-wang.pdf (2 trang, đọc được trọn vẹn).
- §1: “in 2010 we implemented Kafka as LinkedIn's centralized online data pipelining system.” “Since Oct. 2012, Kafka has become a top-level Apache open source software and be widely adopted outside LinkedIn as well”
- §1: “today LinkedIn generates billions of log entries and events that capture its over-300 million members' activities every day”
- §2: “In primarybackup replication, the leader waits until the append is completed on all the replicas before acknowledging the client, whereas in quorum-based replication it only waits until the append is completed on a majority of the replicas. As a result, the primary-backup approach could employ fewer replicas (F + 1) to tolerate the same number of failures (F ) than the quorum approach (2F + 1)”
- §2: “Since Kafka is typically deployed in the same data center where the variance of network latency is low, the benefit of using less replicas outweighs the potential slight increase in latency. We designed and implemented Kafka message log replication in Kafka 0.8.0, with the key idea of separating the key elements of a consensus protocol such as leader election and membership changes from log replication itself.”
- §2: “We rely on the quorum-based Apache Zookeeper service [4] for making consensus decisions such as leader election and storing critical partition metadata such as replica lists, while using a primary-backup approach for replicating logs from leader to followers.” “(e.g., in Kafka we can choose a replication factor of two for the log while using an ensemble of five Zookeeper nodes)”
- §2: “consumer clients only fetch messages that have been replicated to all in-sync replicas.”
- §2: “We introduced a key-based log compaction mechanism in Kafka 0.8.1 … purge old events if there is a newer message with the same key”

## [LI15] LinkedIn Engineering blog, *Running Kafka At Scale*, 20/3/2015 (engineering.linkedin.com/kafka/running-kafka-scale)
Tải được (HTTP 200), đọc trọn bài.
- “When combined, the Kafka ecosystem at LinkedIn is sent over 800 billion messages per day which amounts to over 175 terabytes of data. Over 650 terabytes of messages are then consumed daily … At the busiest times of day, we are receiving over 13 million messages per second, or 2.75 gigabytes of data per second. To handle all these messages, LinkedIn runs over 1100 Kafka brokers organized into more than 60 clusters.”
- “LinkedIn goes one step further, and defines four categories of messages: queuing, metrics, logs and tracking data that each live in their own cluster.” “We now keep logging data separate simply because of how much there is.”
- “For each message category, LinkedIn has a cluster named local containing messages created in the datacenter. There is also an aggregate cluster, which combines messages from all local clusters … We use the Kafka mirror maker application to copy messages forward, from local into aggregate.”
- “This tiered infrastructure solves many problems, but it greatly complicates monitoring … creates myriad points of failure where messages can disappear.”
- “As an individual producer sends messages into Kafka, it keeps a count of how many messages it has sent during the current time interval. Periodically, it transmits that count as a message to a special auditing topic.” “By comparing these counts to the producer counts, we are able to determine that all of the messages produced actually got to Kafka.”

## [KIP500] C. McCabe, *KIP-500: Replace ZooKeeper with a Self-Managed Metadata Quorum*, Apache Kafka wiki (trạng thái “Accepted”; sửa lần cuối 9/7/2020). Mốc tạo: phiếu KAFKA-9119 “KIP-500: Replace ZooKeeper with a Metadata Quorum”, created 2019-10-30, fixVersion 2.8.0 (releaseDate 2021-04-18) — đọc qua REST của issues.apache.org
Tải: https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Self-Managed+Metadata+Quorum (đọc trọn).
- Motivation: “Currently, Kafka uses ZooKeeper to store its metadata about partitions and brokers, and to elect a broker to be the Kafka Controller. We would like to remove this dependency on ZooKeeper. This will enable us to manage metadata in a more scalable and robust way, enabling support for more partitions. It will also simplify the deployment and configuration of Kafka.”
- Metadata as an Event Log: “A single number, the offset, describes a consumer's position in the stream. Multiple consumers can quickly catch up to the latest state simply by replaying all the events newer than their current offset.” “However, although our users enjoy these benefits, Kafka itself has been left out.”
- “When the controller pushes out state change notifications … it is possible for brokers to get some of the changes, but not all. Although the controller retries several times, it eventually give up. This can leave brokers in a divergent state.”
- “although ZooKeeper is the store of record, the state in ZooKeeper often doesn't match the state that is held in memory in the controller … In some cases, restarting the controller is the only way to resolve the discrepancy.”
- “Rather than pushing out notifications to brokers, brokers should simply consume metadata events from the event log. This ensures that metadata changes will always arrive in the same order. … When they start up, they will only need to read what has changed from the controller, not the full state.”
- Simpler Deployment: “ZooKeeper is a separate system, with its own configuration file syntax, management tools, and deployment patterns. This means that system administrators need to learn how to manage and deploy two separate distributed systems in order to deploy Kafka.” “administrators may set up SASL on Kafka, and incorrectly think that they have secured all of the data travelling over the network.”
- Overview: “We have pictured 4 broker nodes and 3 ZooKeeper nodes in this diagram. This is a typical size for a small cluster.” “In the proposed architecture, three controller nodes substitute for the three ZooKeeper nodes.”
- Controller Quorum: “The controller nodes comprise a Raft quorum which manages the metadata log.” “Because the controllers will now all track the latest state, controller failover will not require a lengthy reloading period” “Just like ZooKeeper, Raft requires a majority of nodes to be running in order to continue running. Therefore, a three-node controller cluster can survive one failure. A five-node controller cluster can survive two failures, and so on.”
- “Periodically, the controllers will write out a snapshot of the metadata to disk.”
- Broker Metadata: “the broker will track the offset of the last updates it fetched, and only request newer updates from the active controller.” “This will allow the broker to start up very quickly, even if there are hundreds of thousands or even millions of partitions.” “if the broker is too far behind the active controller, or if the broker has no cached metadata at all, the controller will send a full metadata image rather than a series of deltas.”
- Broker states: “The broker will be in the fenced state when starting up and attempting to fetch the newest metadata. It will re-enter the fenced state if it can't contact the active controller.”
- Bridge Release: “When upgrading from an earlier release to a post-ZK release, the upgrade must be done in two steps: first, you must upgrade to the bridge release, and then you must upgrade to the post-ZK release.”
- Rejected Alternatives (Pluggable Consensus): “Supporting multiple metadata storage options would inevitably decrease the amount of testing we could give to each configuration.”

- Bổ sung đợt C (2026-11-09): KIP-500 đã được thảo luận công khai TRƯỚC tháng 10/2019 — tập podcast Confluent “KIP-500: Apache Kafka Without ZooKeeper ft. Colin McCabe and Jason Gustafson”, ngày đăng “September 18, 2019” (buzzsprout.com/186154/1720903, truy cập 2026-11-09, no revision given). Vì vậy bài chỉ ghi “đề xuất số 500, năm 2019”; mốc 30/10/2019 là ngày tạo **phiếu KAFKA-9119**, và phép tính 1966 ngày ghi rõ “từ ngày mở phiếu công việc của đề xuất”. Ngày tạo trang KIP trên wiki: chưa kiểm được nguồn.

## [K011] Apache Kafka 0.11.0 — ghi lũy đẳng, giao dịch (bài học sai 1 của L11)
- Trang tải về chính thức kafka.apache.org/community/downloads (truy cập 2026-11-09, no revision given): mục 0.11.0.0 “Released June 28, 2017”; mục 1.0.0: “Since release 0.11.0, the idempotent producer …”.
- KIP-98 *Exactly Once Delivery and Transactional Messaging* (cwiki, truy cập 2026-11-09): “Current state: Adopted”; “Note that idempotence must be enabled in order to use transactions.” Trang KIP không ghi số bản phát hành của giao dịch → bản 0.11 cho giao dịch: chưa kiểm được trực tiếp trong ghi chú phát hành (giữ vì khớp mốc ghi lũy đẳng 0.11.0 và kiến thức chung).

## [B28] Apache Kafka blog (lưu trữ), *What’s New in Apache Kafka 2.8.0*, 19/4/2021 (blogsarchive.apache.org/kafka/entry/what-s-new-in-apache5)
- “This release offers an early access version of KIP-500, which allows you to run Kafka brokers without Apache ZooKeeper, instead depending on an internal Raft implementation.”
- “The implementation is not yet feature complete and should not be used in production, but it is possible to start new clusters without ZooKeeper and go through basic produce and consume use cases.”
- “moving topic metadata and configurations out of ZooKeeper and into a new internal topic named @metadata. This topic is managed by an internal Raft quorum of "controllers" and is replicated to all brokers in the cluster.”

## [B33] Apache Kafka blog (lưu trữ), *What’s New in Apache Kafka 3.3*, 3/10/2022 (blogsarchive.apache.org/kafka/entry/what-rsquo-s-new-in)
- “This new mode, called KRaft mode, improves partition scalability and resiliency while simplifying deployments of Apache Kafka. It also eliminates the need to run an Apache ZooKeeper™ cluster alongside every Apache Kafka cluster.”
- “The 3.3 release now marks KRaft mode as production ready for new clusters only. There are some features that are currently supported by Apache ZooKeeper (ZK) mode that are not yet supported by KRaft mode.”
- “KIP-778 allows the upgrade of KRaft clusters without the need for the infamous “double roll”.”

## [BK] Apache Kafka blog (kafka.apache.org/blog/_print/, trang gộp mọi bài từ 2023): 3.5.0 (15/6/2023), 3.6.0 (10/10/2023), 3.9.0 (6/11/2024)
- 3.5.0: “Note: ZooKeeper is now marked deprecated in this release. ZooKeeper is planned to be removed in Apache Kafka 4.0.”
- 3.6.0: “The 3.6.0 release marked the first production ready release for the migration of Kafka clusters from a ZooKeeper metadata system to a KRaft metadata system.”
- 3.9.0: “This is a major release, the final one in the 3.x line. This will also be the final major release to feature the deprecated Apache ZooKeeper mode.”
- 3.9.0: “As we migrated thousands of clusters (big and small), we found and fixed many bugs.” “if you wanted to upgrade from Kafka 3.0 to Kafka 4.0, you might do the following: Upgrade to Kafka 3.9. Perform ZK migration. Upgrade to Kafka 4.0.”
- 3.9.0 (KIP-853): “Previously, controller quorums were specified by a static configuration … This made changing the hostnames of controllers, or adding or removing them, very difficult to do without downtime.”

## [B40] Apache Kafka blog, *Apache Kafka 4.0.0 Release Announcement*, 18/3/2025 (kafka.apache.org/blog/2025/03/18/apache-kafka-4.0.0-release-announcement/)
- “Apache Kafka 4.0 is a significant milestone, marking the first major release to operate entirely without Apache ZooKeeper®. By running in KRaft mode by default, Kafka simplifies deployment and management, eliminating the complexity of maintaining a separate ZooKeeper ensemble.”
- “ZooKeeper was the backbone of Kafka for more than 10 years, and it did serve Kafka very well.”
- “Kafka’s major releases, such as version 4.0, remove APIs deprecated for at least 12 months”

## Không đọc được / không dùng
- Bài thông báo 3.3.1 trên kafka.apache.org/blog/2022/… : 404 (blog mới chỉ còn bài từ 2023) → dùng bản lưu trữ [B33].
- J. Kreps, “The Log” (2013): không cần cho bài, không đọc → không dạy.

## Điều KHÔNG dạy (nguồn không ghi)
- Ngày phát hành bản 0.8.0 và 0.8.1: [V15] chỉ ghi tên bản, không ghi năm → bài ghi chặng “2012 → 2015” (mốc tháng 10/2012 và bài tóm tắt 2015), không nói năm phát hành bản sao chép.
- Thời gian chuyển bộ điều khiển (giây) trước/sau KIP-500: [KIP500] chỉ ghi “lengthy reloading period”, không có con số → không dạy con số.
- Số phân vùng tối đa của chế độ cũ: không có trong nguồn → chỉ dạy câu “hundreds of thousands or even millions of partitions” của [KIP500] về khởi động nhanh.
- Lý do bỏ đề xuất thay ZooKeeper bằng kho khác (etcd, Consul): chỉ dạy đúng lý do kiểm thử và “event log” ghi trong [KIP500].
- Kích thước tin trung bình 2015: nguồn không ghi; bài TÍNH LẠI từ 175 TB / 800 tỉ tin và 2,75 GB/s / 13 triệu tin/s (≈ 210–220 byte), ghi là phép chia, không phải số đo.
- “70% more space” của [K11] §5 không khớp phép chia đơn giản (200 + 144)/(200 + 9) ≈ 1,65 → không dạy con số này.
