# CHUYÊN ĐỀ 3: HỆ THỐNG PHÂN TÁN, KAFKA, SAGA & TỐI ƯU HÓA ORACLE 19C

> **Mục tiêu**: Nâng cấp tư duy kiến trúc và làm chủ toàn bộ bài toán phân tán cao tải, tối ưu hóa cơ sở dữ liệu chuyên sâu cấp Senior / Tech Lead.  
> **Căn cứ học phần**: T1 & T3 trong khung chuẩn UIT AI (`curriculum/dsy.yaml`, `den.yaml`, `evt.yaml`, `dbs.yaml`, `par.yaml`) và bằng chứng thực tế tại `hub-system-graph.md`.

---

## 1. GIAO DỊCH PHÂN TÁN (DISTRIBUTED TRANSACTIONS) & MÔ HÌNH SAGA

### 1.1. Vì sao 2PC (Two-Phase Commit) thất bại ở quy mô Ngân hàng?
- **Giao thức 2PC**:
  1. *Prepare Phase*: Coordinator hỏi tất cả các Node "Có thể commit không?". Các Node khóa tài nguyên và trả lời YES/NO.
  2. *Commit Phase*: Nếu tất cả YES $\to$ Coordinator ra lệnh Commit.
- **Điểm yếu chí tử**:
  - **Khóa chặn đồng bộ (Synchronous Blocking)**: Các dòng dữ liệu tham gia giao dịch (ví dụ dòng số dư tài khoản) bị giữ khóa từ pha Prepare cho đến khi pha Commit hoàn tất. Nếu một node bị lag mạng, các giao dịch khác chạm vào cùng dòng đó phải chờ, thread và connection pool có thể cạn kiệt.
  - **Single Point of Failure**: Nếu Coordinator sập giữa 2 pha, các resource managers đã Prepare không biết commit hay rollback, tài nguyên bị giữ khóa cho tới khi Coordinator phục hồi hoặc DBA ra quyết định thủ công (In-doubt / heuristic decision).
  - Khó áp dụng với các đối tác bên thứ ba (NAPAS, EVN, Telco) vì giao tiếp với họ thường qua API/bản tin riêng, không tham gia XA/2PC chung với ngân hàng.

### 1.2. Mô hình SAGA (SAGA Pattern) trong Payment Hub
Saga phân tách một giao dịch lớn thành một chuỗi các **Giao dịch Cục bộ (Local Transactions)** độc lập. Mỗi giao dịch cục bộ cập nhật DB riêng của microservice đó và phát ra sự kiện để kích hoạt bước tiếp theo.

```
Luồng Thành Công:
[T1: Trích nợ Khách hàng] ---> [T2: Gọi đối tác EVN] ---> [T3: Ghi nhận Hóa đơn hoàn tất]

Luồng Bồi Hoàn khi EVN lỗi:
[T1: Trích nợ Khách hàng] ---> [T2: Gọi đối tác EVN (FAIL!)]
          ^                                  |
          | (Kích hoạt Giao dịch bồi hoàn)   v
[C1: Hoàn tiền tài khoản] <------------------+
```

- **Hai hình thức triển khai Saga**:
  1. **Choreography (Tự phối hợp qua Event)**: Các dịch vụ tự lắng nghe Kafka topic của nhau để kích hoạt bước kế tiếp. Nhược điểm: Khó kiểm soát luồng khi có 10+ bước, dễ rơi vào bẫy "vòng lặp sự kiện" (Cyclic dependencies).
  2. **Orchestration (Điều phối tập trung — Khuyên dùng cho Ngân hàng)**: Sử dụng một Coordinator chuyên biệt (như dịch vụ `Billing Orchestration Engine` trong hệ thống tích hợp ngân hàng).
     - Lưu trạng thái máy trạng thái vào bảng `billing_saga_state`: `INITIALIZED` $\to$ `DEBITED` $\to$ `PROVIDER_PROCESSING` $\to$ `SUCCESS` hoặc `REVERTED`.
     - Nếu bước $T_i$ thất bại, Orchestrator chủ động gửi lệnh gọi các giao dịch bồi hoàn $C_{i-1}, \dots, C_1$ theo chiều ngược lại.

### 1.3. Khắc phục bài toán "Ghi kép" (Dual-Write Problem) bằng Transactional Outbox Pattern
- **Hiểm họa Dual-Write**: Một service vừa phải ghi dữ liệu vào Database, vừa phải gửi Message vào Kafka. Nếu ghi DB thành công nhưng Kafka broker bị sập (hoặc mạng đứt), message bị mất $\to$ Hệ thống mất tính nhất quán! Nếu gửi Kafka trước nhưng DB commit lỗi $\to$ Các service khác đã xử lý dựa trên dữ liệu ảo!
- **Giải pháp Transactional Outbox Pattern**:
  ```
  [Microservice Application]
             |
             v (Giao dịch cục bộ ACID duy nhất)
  +-------------------------------------------------------+
  | Database (PostgreSQL / Oracle)                        |
  |  +-----------------------+  +-----------------------+ |
  |  | Bảng Nghiệp vụ        |  | Bảng OUTBOX_EVENT     | |
  |  | (INSERT transaction)  |  | (INSERT event payload)| |
  |  +-----------------------+  +-----------------------+ |
  +-------------------------------------------------------+
             |
             | (Đọc log bằng Debezium / Kafka Connect CDC)
             v
      [Apache Kafka Broker]
  ```
  - Bước 1: Ứng dụng ghi đồng thời dữ liệu nghiệp vụ và bản tin sự kiện vào bảng `OUTBOX_EVENT` trong **CÙNG MỘT TRANSACTION DATABASE (ACID 100%)**.
  - Bước 2: Một công cụ CDC (Change Data Capture như Debezium) đọc trực tiếp từ Write-Ahead Log (WAL của Postgres hoặc Redo Log của Oracle) và đẩy message vào Kafka mà không cần can thiệp code ứng dụng. Ngữ nghĩa là **At-least-once Delivery**: message có thể bị gửi trùng (ví dụ khi connector khởi động lại), nên consumer phải idempotent. Với Oracle, Debezium dùng LogMiner (cần ARCHIVELOG và supplemental logging) và vẫn tạo một phần tải lên DB.

---

## 2. APACHE KAFKA CHUYÊN SÂU CẤP SENIOR (HIGH-THROUGHPUT STREAMING)

### 2.1. Cấu trúc lưu trữ & Cơ chế Zero-Copy
- **Topic & Partition**: Partition là một append-only commit log tuần tự ghi xuống đĩa cứng. Dữ liệu được chia thành các file phân đoạn (Segment files: `.log` và `.index`).
- **Ghi đĩa tuần tự (Sequential I/O)**: Trên cùng một thiết bị, ghi tuần tự nhanh hơn nhiều so với ghi ngẫu nhiên (tài liệu Kafka "Design: Persistence" dẫn ví dụ một mảng RAID-5 6 đĩa 7200rpm: ghi tuần tự khoảng 600 MB/s so với ghi ngẫu nhiên khoảng 100 KB/s). Kafka tận dụng ghi tuần tự và OS Page Cache thay vì tự cache trong heap JVM.
- **Zero-Copy qua `sendfile`**: Khi Consumer kéo dữ liệu, Kafka sử dụng system call `sendfile()` của Linux kernel, chuyển trực tiếp dữ liệu từ OS Page Cache ra Network Socket Buffer mà không cần copy qua JVM Application Memory, giảm CPU cycles và áp lực GC. Lưu ý: khi bật TLS giữa client và broker (thường bắt buộc trong ngân hàng), dữ liệu phải mã hóa trong JVM nên **không còn zero-copy**.

### 2.2. Đảm bảo tính nhất quán và không mất tin (Zero Message Loss)
- **Cấu hình Producer chuẩn Ngân hàng** (từ Kafka 3.0, `acks=all` và `enable.idempotence=true` đã là mặc định — KIP-679):
  ```properties
  acks=all
  retries=2147483647
  max.in.flight.requests.per.connection=5 # <= 5 khi enable.idempotence=true vẫn giữ thứ tự
  enable.idempotence=true
  ```
- **Cấu hình Topic/Broker đi kèm** (không phải cấu hình producer, producer bỏ qua nếu đặt ở phía nó):
  ```properties
  replication.factor=3
  min.insync.replicas=2
  unclean.leader.election.enable=false
  ```
  - `enable.idempotence=true`: Mỗi Producer được gán một Producer ID (PID), và mỗi message có một Sequence Number tăng dần theo từng partition. Broker bỏ qua bản ghi trùng Sequence Number $\to$ khử trùng lặp do **retry nội bộ của producer trong cùng một phiên**. Không khử được trùng khi ứng dụng tự gửi lại, hoặc khi producer khởi động lại với PID mới (trừ khi dùng `transactional.id`).
- **Cấu hình Consumer**:
  - Tắt tự động commit: `enable.auto.commit=false`.
  - Chỉ commit offset thủ công (`Acknowledgment.acknowledge()`) sau khi đã xử lý xong nghiệp vụ và ghi DB thành công.
- **Xử lý bản tin lỗi độc hại (Poison Pill) bằng Non-blocking Retry Topics**:
  - Không để Consumer bị tắc nghẽn vô hạn khi gặp 1 message hỏng.
  - Chuyển tiếp message lỗi sang chuỗi topic retry trễ dần: `payment.order.retry-10s` $\to$ `payment.order.retry-1m` $\to$ `payment.order.dlq` (Dead Letter Queue để cảnh báo cho đội Vận hành).
  - Đánh đổi: retry không chặn làm **mất thứ tự theo key** (bản tin sau của cùng tài khoản có thể được xử lý trước bản tin đang retry). Với luồng cần thứ tự, dùng retry chặn (blocking) có giới hạn hoặc kiểm tra phiên bản/trạng thái trước khi áp dụng.

---

## 3. TỐI ƯU HÓA CƠ SỞ DỮ LIỆU ORACLE 19C & XỬ LÝ DEADLOCK

ACB đặc biệt coi trọng kinh nghiệm làm việc với Stored Procedure và khả năng tối ưu hóa Oracle SQL (yêu cầu $\ge 3$ năm).

### 3.1. Đọc và Phân tích Kế hoạch Thực thi (Execution Plan)
- Sử dụng lệnh:
  ```sql
  EXPLAIN PLAN FOR SELECT * FROM transactions WHERE account_no = '123456' AND created_date >= TRUNC(SYSDATE);
  SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
  ```
- **Các dấu hiệu nhận biết hiệu năng**:
  - `TABLE ACCESS FULL`: Quét toàn bộ bảng. Hợp lý với bảng nhỏ hoặc khi truy vấn lấy một tỷ lệ lớn số dòng; là dấu hiệu cần xem xét khi truy vấn điểm trên bảng giao dịch rất lớn.
  - `INDEX UNIQUE SCAN`: Tối ưu nhất ($O(\log N)$), truy vấn trên Primary Key hoặc Unique Index.
  - `INDEX RANGE SCAN`: Tối ưu khi truy vấn theo dải ngày hoặc giá trị lặp lại có chỉ mục.
  - `TABLE ACCESS BY INDEX ROWID BATCHED`: Đọc index lấy con trỏ `ROWID`, sau đó gom nhóm để đọc block dữ liệu trên đĩa.
  - **Quy tắc Index tổ hợp (Composite Index Column Order)**: Nếu tạo index trên `(status, created_date)`, câu truy vấn có điều kiện `WHERE created_date = ...` (không có `status`) không dùng được Index Range Scan thông thường. Tuy nhiên vì `status` có ít giá trị phân biệt, Oracle có thể dùng **Index Skip Scan** khá hiệu quả (Oracle SQL Tuning Guide: skip scan có lợi khi cột đầu có ít giá trị phân biệt). Quy tắc chung: đặt trước các cột luôn xuất hiện với điều kiện bằng trong các truy vấn quan trọng, cột dùng điều kiện khoảng (ngày) đặt sau; thiết kế theo tập truy vấn thực tế.

### 3.2. Chiến lược Phân vùng Bảng (Table Partitioning)
Trong hệ thống ngân hàng, bảng `TRANSACTION` tăng trưởng hàng triệu bản ghi mỗi ngày.
- **Range Partitioning theo Ngày giao dịch (`trans_date`)**:
  ```sql
  CREATE TABLE transaction_history (
      trans_id VARCHAR2(36) NOT NULL,
      account_no VARCHAR2(20) NOT NULL,
      amount NUMBER(18, 2),
      trans_date DATE NOT NULL
  )
  PARTITION BY RANGE (trans_date) (
      PARTITION p_2026_10 VALUES LESS THAN (TO_DATE('2026-11-01', 'YYYY-MM-DD')),
      PARTITION p_2026_11 VALUES LESS THAN (TO_DATE('2026-12-01', 'YYYY-MM-DD')),
      PARTITION p_max VALUES LESS THAN (MAXVALUE)
  );
  ```
  - **Lợi ích**: Khi truy vấn giao dịch trong tháng 11, Oracle áp dụng cơ chế **Partition Pruning (Cắt tỉa phân vùng)**, chỉ quét đúng phân vùng `p_2026_11` và bỏ qua hàng trăm GB dữ liệu của các năm cũ. Khi cần xóa dữ liệu lịch sử quá hạn lưu trữ, `ALTER TABLE ... DROP PARTITION` là thao tác DDL gần như tức thời (chỉ ghi ít redo cho thay đổi từ điển dữ liệu, không tạo undo/redo cho từng dòng như `DELETE`). Thêm `UPDATE INDEXES` (từ 12c, global index được bảo trì bất đồng bộ) để global index không bị chuyển sang `UNUSABLE`.

### 3.3. Phòng ngừa Deadlock ORA-00060 trong Stored Procedure
- **Thuật toán Deterministic Row Locking** (khóa từng dòng bằng câu lệnh riêng theo thứ tự đã sắp; không dựa vào `ORDER BY ... FOR UPDATE` vì Oracle không bảo đảm thứ tự khóa dòng theo `ORDER BY`):
  ```sql
  CREATE OR REPLACE PROCEDURE transfer_balance(
      p_from_acc IN VARCHAR2,
      p_to_acc   IN VARCHAR2,
      p_amount   IN NUMBER
  ) AS
      v_acc1  VARCHAR2(20);
      v_acc2  VARCHAR2(20);
      v_dummy VARCHAR2(20);
  BEGIN
      IF p_from_acc = p_to_acc THEN
          RAISE_APPLICATION_ERROR(-20001, 'Source and destination must differ');
      END IF;

      -- Sắp xếp thứ tự tài khoản theo Alphabet/Số để đảm bảo khóa xác định
      IF p_from_acc < p_to_acc THEN
          v_acc1 := p_from_acc;
          v_acc2 := p_to_acc;
      ELSE
          v_acc1 := p_to_acc;
          v_acc2 := p_from_acc;
      END IF;

      -- Khóa tuần tự tài khoản nhỏ trước, tài khoản lớn sau
      -- (PL/SQL bắt buộc có INTO; thiếu INTO sẽ lỗi biên dịch PLS-00428)
      SELECT account_no INTO v_dummy FROM accounts WHERE account_no = v_acc1 FOR UPDATE;
      SELECT account_no INTO v_dummy FROM accounts WHERE account_no = v_acc2 FOR UPDATE;

      -- Thực hiện trích nợ (có kiểm tra số dư) và ghi có
      UPDATE accounts SET balance = balance - p_amount
       WHERE account_no = p_from_acc AND balance >= p_amount;
      IF SQL%ROWCOUNT = 0 THEN
          RAISE_APPLICATION_ERROR(-20002, 'Insufficient funds');
      END IF;
      UPDATE accounts SET balance = balance + p_amount WHERE account_no = p_to_acc;

      -- Không COMMIT trong thủ tục: để tầng gọi (ứng dụng/Spring) quản lý ranh giới transaction
  END;
  /
  ```
  - Giới hạn: thứ tự khóa xác định chỉ ngăn deadlock giữa các luồng code **cùng tuân theo** thứ tự đó. ORA-00060 vẫn có thể xảy ra từ luồng khác (batch, hệ thống khác), FK thiếu index, tranh chấp ITL hoặc bitmap index; cần đọc trace file để xác định.

### 3.4. Tối ưu hóa PL/SQL với BULK COLLECT và FORALL
Khi xử lý batch đối soát hoặc tính lãi hàng triệu tài khoản:
```sql
DECLARE
    CURSOR c_acc IS SELECT * FROM accounts WHERE status = 'ACTIVE';
    TYPE t_account_list IS TABLE OF accounts%ROWTYPE;
    v_accounts t_account_list;
BEGIN
    OPEN c_acc;
    LOOP
        -- LIMIT để không nạp hàng triệu dòng vào PGA một lần (tránh ORA-04030)
        FETCH c_acc BULK COLLECT INTO v_accounts LIMIT 1000;
        EXIT WHEN v_accounts.COUNT = 0;

        -- Xử lý mảng trong bộ nhớ...

        -- Cập nhật đồng loạt: mỗi lô chỉ một lần chuyển ngữ cảnh PL/SQL -> SQL
        FORALL i IN 1..v_accounts.COUNT
            UPDATE accounts SET interest = v_accounts(i).interest
            WHERE account_no = v_accounts(i).account_no;
    END LOOP;
    CLOSE c_acc;
    COMMIT;
END;
/
```
Lợi ích đến từ việc giảm số lần chuyển ngữ cảnh giữa SQL Engine và PL/SQL Engine (từ một lần mỗi dòng xuống một lần mỗi lô). Mức cải thiện cụ thể phải đo trên dữ liệu thật; nếu làm được bằng một câu SQL theo tập hợp (set-based) thì thường còn tốt hơn.

---

## 4. TUNING HIỆU NĂNG BỘ NHỚ JVM & GARBAGE COLLECTION

- **Garbage-First Collector (G1GC)**:
  - Chia bộ nhớ Heap thành nhiều phân vùng nhỏ (Regions) có kích thước bằng nhau, là lũy thừa của 2 (JVM tự chọn trong khoảng 1MB–32MB, nhắm khoảng 2048 region; từ JDK 18 có thể đặt `-XX:G1HeapRegionSize` tới 512MB).
  - G1GC liên tục đo lường và ưu tiên thu dọn các Region chứa nhiều rác nhất trước ("Garbage-First"), đảm bảo thời gian tạm dừng ứng dụng nằm trong ngưỡng kỳ vọng.
- **Các cờ JVM tối ưu hóa cho hệ thống ngân hàng tải cao**:
  ```bash
  -server
  -Xms8g -Xmx8g
  -XX:+UseG1GC
  -XX:MaxGCPauseMillis=100
  -XX:InitiatingHeapOccupancyPercent=45
  -XX:G1ReservePercent=15
  -XX:+ParallelRefProcEnabled
  -XX:+HeapDumpOnOutOfMemoryError
  -XX:HeapDumpPath=/var/log/dumps/oom_dump.hprof
  ```
  - Cố định `-Xms = -Xmx` để ngăn chặn JVM phải co giãn bộ nhớ liên tục trong lúc đang chịu tải giao dịch.
  - `-XX:MaxGCPauseMillis=100`: **Mục tiêu mềm** (soft goal, theo HotSpot GC Tuning Guide): G1 cố gắng giữ pause STW dưới 100ms nhưng không bảo đảm; đặt quá thấp có thể làm giảm thông lượng.
  - `-XX:+HeapDumpOnOutOfMemoryError`: Tự động xuất file dump bộ nhớ ngay tại thời điểm bị OOM để dùng Eclipse Memory Analyzer Tool (MAT) phân tích chính xác vị trí rò rỉ bộ nhớ (Memory Leak).
