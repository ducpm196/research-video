# CHUYÊN ĐỀ 1: NỀN TẢNG KHOA HỌC MÁY TÍNH, JAVA HIỆN ĐẠI & MẠNG MÁY TÍNH

> **Mục tiêu**: Xây dựng lại nền tảng vững chắc từ con số 0 cho người mới hoặc người mất gốc kiến thức.  
> **Căn cứ học phần**: T0 & T1 trong khung chuẩn UIT AI (`curriculum/cs112.yaml`, `cs115.yaml`, `csa.yaml`, `osy.yaml`, `net.yaml`, `par.yaml`).

---

## 1. BẢN CHẤT KIẾN TRÚC MÁY TÍNH & BỘ NHỚ JVM

### 1.1. Mô hình bộ nhớ máy tính & CPU Cache
- CPU hoạt động ở tốc độ nano-giây, trong khi RAM chính (DRAM) chậm hơn khoảng 100 lần.
- **Hệ thống phân cấp bộ nhớ** (số liệu xấp xỉ, minh họa; thay đổi tùy đời CPU):
  $$\text{Registers (0.5 ns)} \to \text{L1 Cache (1 ns)} \to \text{L2 Cache (3–10 ns)} \to \text{L3 Cache (20–40 ns)} \to \text{Main Memory (100 ns)}$$
- **Cache Line & False Sharing**: Dữ liệu nạp từ RAM lên CPU Cache theo từng khối 64 bytes gọi là *Cache Line*. Khi hai luồng trên hai CPU core khác nhau ghi vào hai biến độc lập nhưng nằm chung một Cache Line 64-byte, CPU phải vô hiệu hóa cache liên tục (Cache Invalidation qua giao thức MESI), làm sụt giảm nghiêm trọng hiệu năng đa luồng. Trong hệ thống thanh toán tốc độ cao (như LMAX Disruptor), kỹ thuật *Cache Line Padding* được áp dụng để chèn byte rỗng, ngăn cách các biến quan trọng. Annotation `@Contended` của JDK là API nội bộ (`jdk.internal.vm.annotation.Contended`), code ứng dụng chỉ dùng được khi chạy với cờ `-XX:-RestrictContended`; vì vậy thư viện như Disruptor tự padding bằng các field thừa.

### 1.2. Mô hình bộ nhớ JVM (JVM Memory Layout)
Bộ nhớ của Java Virtual Machine được phân tách rạch ròi:

```
+-----------------------------------------------------------------------+
|                             JVM HEAP                                  |
|  +--------------------------------+  +-----------------------------+  |
|  |        Young Generation        |  |       Old Generation        |  |
|  |  +----------+ +----+ +----+    |  |  (Tenured Space)            |  |
|  |  | Eden     | | S0 | | S1 |    |  |  Đối tượng tồn tại lâu năm  |  |
|  |  | Tạo mới  | |Surv| |Surv|    |  |  (Cấu hình Cache, Pool)     |  |
|  |  +----------+ +----+ +----+    |  |                             |  |
|  +--------------------------------+  +-----------------------------+  |
+-----------------------------------------------------------------------+
|  Metaspace (Off-Heap)              | Thread Stack (Per-thread)        |
|  Class Metadata, Method Tables    | Stack Frames, Local Primitives  |
+------------------------------------+----------------------------------+
```

1. **Heap Memory**: Nơi chứa toàn bộ các Object (`new Order()`, `new Account()`). Được chia thành:
   - **Young Generation**: Bao gồm vùng *Eden* và hai vùng *Survivor (S0, S1)*. Hầu hết các đối tượng ngắn hạn (như DTO request/response, chuỗi tạm) sinh ra trong Eden và chết đi nhanh chóng trong đợt *Minor GC*.
   - **Old Generation (Tenured)**: Chứa các đối tượng sống sót qua nhiều chu kỳ GC (ngưỡng tuổi do JVM tự điều chỉnh, tối đa `MaxTenuringThreshold` = 15 mặc định), ví dụ: Connection Pools, Spring Singleton Beans, In-memory Caches. Với G1, các region Old được thu dọn dần trong *Mixed GC*; *Full GC* chỉ là phương án cuối khi không kịp giải phóng.
2. **Thread Stack**: Mỗi thread sở hữu một Stack riêng biệt (mặc định 1MB, cấu hình qua `-Xss`). Chứa các Stack Frame khi gọi hàm, bao gồm: biến nguyên thủy cục bộ (`int`, `long`, `boolean`), biến con trỏ tham chiếu (reference pointer trỏ vào Heap), và địa chỉ trả về của hàm. Khi hàm kết thúc, stack frame tự động giải phóng tức thì mà không cần GC. Nếu gọi đệ quy vô hạn hoặc stack quá sâu $\to$ Lỗi `StackOverflowError`.
3. **Metaspace**: Nằm ở bộ nhớ ngoài Native Memory (từ Java 8 thay thế PermGen). Chứa siêu dữ liệu cấu trúc Class (Class Metadata), Bytecode, Constant Pool. Nếu ứng dụng nạp quá nhiều thư viện động (CGLIB proxies, reflection) mà không cấu hình giới hạn `-XX:MaxMetaspaceSize`, hệ thống có thể chiếm hết RAM của server gây OOM OS-level.

---

## 2. JAVA CORE HIỆN ĐẠI (TỪ JAVA 8 ĐẾN JAVA 21)

### 2.1. Lập trình Hàm & Stream API
- **Lambda Expressions & Functional Interfaces**: `@FunctionalInterface` chỉ có duy nhất một hàm trừu tượng (`Function<T,R>`, `Predicate<T>`, `Consumer<T>`, `Supplier<T>`).
- **Stream API**: Xử lý dữ liệu dạng pipeline khai báo (declarative):
  ```java
  // Lọc và tính tổng giá trị các giao dịch chuyển tiền thành công
  BigDecimal totalSuccessfulAmount = transactions.stream()
      .filter(tx -> "SUCCESS".equals(tx.getStatus()))
      .map(Transaction::getAmount)
      .reduce(BigDecimal.ZERO, BigDecimal::add);
  ```
- **Lưu ý với kiểu tiền tệ trong Ngân hàng**: Tuyệt đối **KHÔNG BAO GIỜ** dùng `float` hoặc `double` để lưu trữ số tiền vì lỗi làm tròn số học nhị phân dấu phẩy động (IEEE 754). Luôn luôn sử dụng `BigDecimal` với phép toán làm tròn tường minh:
  ```java
  // Đúng chuẩn ngân hàng
  BigDecimal balance = new BigDecimal("1000000.50");
  BigDecimal interest = balance.multiply(new BigDecimal("0.055"))
                               .setScale(2, RoundingMode.HALF_UP);
  ```

### 2.2. Records & Pattern Matching (Java 17 / 21)
- `record` giúp định nghĩa các DTO bất biến **nông** (shallowly immutable): các field là `final`, nhưng nếu thành phần là đối tượng khả biến (ví dụ `List`) thì phải sao chép phòng thủ (`List.copyOf`) mới an toàn khi chia sẻ giữa nhiều luồng:
  ```java
  public record TransferRequest(
      String transId,
      String sourceAccount,
      String destAccount,
      BigDecimal amount,
      String currency
  ) {
      public TransferRequest {
          Objects.requireNonNull(transId, "transId must not be null");
          if (amount.compareTo(BigDecimal.ZERO) <= 0) {
              throw new IllegalArgumentException("Amount must be strictly positive");
          }
      }
  }
  ```

### 2.3. Virtual Threads (Project Loom — Java 21)
- **Vấn đề của Platform Thread (OS Thread)**: Mỗi Thread truyền thống trong Java ánh xạ 1:1 với một Kernel Thread của hệ điều hành. Mỗi luồng dự trữ tới ~1MB không gian địa chỉ cho ngăn xếp (bộ nhớ thật chỉ được cấp dần khi dùng), và chi phí Context Switching của OS đắt đỏ khi phục vụ hàng chục ngàn kết nối chặn I/O đồng thời.
- **Virtual Thread** (JEP 444): Là các luồng nhẹ do JVM quản lý; ngăn xếp lưu trên heap và co giãn theo độ sâu lời gọi (từ vài trăm byte đến vài KB, không có con số cố định). Khi một Virtual Thread thực hiện tác vụ I/O chặn (như đọc DB, gọi REST, đợi IBM MQ), JVM thường tháo dỡ (unmount) nó khỏi Carrier Thread (OS Thread thực tế) và gán Carrier Thread đó cho luồng khác chạy. Khi tác vụ I/O có kết quả, Virtual Thread được gắn lại (mount) để chạy tiếp.
- **Bẫy ghim luồng (pinning) ở Java 21**: nếu chặn I/O khi đang ở trong khối `synchronized` hoặc trong native code, luồng ảo bị ghim vào carrier và không unmount được; vài luồng như vậy có thể chiếm hết carrier. Cách xử lý: thay `synchronized` quanh I/O bằng `ReentrantLock`, theo dõi bằng `-Djdk.tracePinnedThreads=full` hoặc sự kiện JFR `jdk.VirtualThreadPinned`. Từ JDK 24 (JEP 491) `synchronized` không còn gây ghim.
- **Cấu hình với Spring Boot 3.2+**:
  ```properties
  spring.threads.virtual.enabled=true
  ```

---

## 3. CẤU TRÚC DỮ LIỆU & THUẬT TOÁN CỐT LÕI

### 3.1. Phân tích độ phức tạp thời gian & không gian (Big-O)
- $O(1)$: Truy xuất mảng theo chỉ số, lấy giá trị từ Hash Table (trường hợp lý tưởng).
- $O(\log N)$: Tìm kiếm nhị phân, thao tác trên cây B-Tree / Red-Black Tree.
- $O(N)$: Duyệt danh sách tuần tự (Full Table Scan).
- $O(N \log N)$: Các thuật toán sắp xếp tối ưu (Merge Sort, TimSort trong Java).
- $O(N^2)$: Vòng lặp lồng nhau (Nested loops join không có index).

### 3.2. Cơ chế bên trong của `HashMap` và `ConcurrentHashMap`
- **`HashMap`**:
  - Cấu trúc: Mảng các Buckets (mặc định kích thước 16, hệ số tải `loadFactor = 0.75`).
  - Hàm băm: `int index = (n - 1) & hash(key)`.
  - Xung đột băm (Hash Collision): Xảy ra khi hai key khác nhau cho ra cùng một chỉ số index.
  - Tiến hóa cấu trúc (Java 8+): Ban đầu các node xung đột được liên kết dạng Danh sách liên kết đơn (Singly Linked List, tìm kiếm $O(K)$). Khi số phần tử trong 1 bucket vượt ngưỡng `TREEIFY_THRESHOLD = 8` và kích thước mảng $\ge 64$, danh sách tự động chuyển thành **Cây Đỏ-Đen (Red-Black Tree)** với độ phức tạp tìm kiếm giảm xuống $O(\log K)$, chống tấn công từ chối dịch vụ HashDoS.
  - **Cảnh báo đa luồng**: `HashMap` không an toàn trong môi trường đa luồng (Non-thread-safe). Nếu nhiều thread cùng `put()` đồng thời có thể mất dữ liệu hoặc hỏng cấu trúc bên trong; ở Java 7 trở về trước, resize đồng thời còn có thể tạo vòng lặp vô hạn (CPU 100%).
- **`ConcurrentHashMap`**:
  - Không sử dụng khóa toàn bảng (Table-level lock như `Hashtable`).
  - Sử dụng cơ chế **CAS (Compare-And-Swap)** không khóa khi ghi node đầu tiên của bucket.
  - Sử dụng khóa mịn `synchronized` trên chính Node đầu tiên của Bucket khi có xung đột, cho phép hàng ngàn luồng đọc và ghi đồng thời trên các buckets khác nhau mà không hề xung đột khóa.

---

## 4. MẠNG MÁY TÍNH & GIAO THỨC TÍCH HỢP NGÂN HÀNG

### 4.1. Mô hình OSI & Chồng giao thức TCP/IP
- **Tầng Giao vận (Transport Layer - TCP)**:
  - **Quá trình bắt tay 3 bước (TCP 3-Way Handshake)**:
    1. Client gửi cờ `SYN` (kèm số thứ tự khởi tạo $Seq = X$).
    2. Server phản hồi cờ `SYN-ACK` (kèm $Seq = Y$, $Ack = X + 1$).
    3. Client gửi cờ `ACK` ($Seq = X + 1$, $Ack = Y + 1$). Kết nối sẵn sàng.
  - **Cơ chế đảm bảo tin cậy**: TCP tự động đánh số gói tin (Sequence Number), xác nhận đã nhận (ACK), tự động truyền lại gói tin bị mất (Retransmission) và kiểm soát tắc nghẽn (Congestion Control).
- **Tầng Ứng dụng**: HTTP/1.1, HTTP/2 (Multiplexing), gRPC (HTTP/2 + Protobuf nhị phân), ISO 8583 (bản tin nhị phân/ASCII thuần qua raw TCP socket).

### 4.2. Bảo mật truyền dẫn: SSL/TLS & Mutual TLS (mTLS)
- **Bắt tay TLS 1.3 (TLS Handshake)**:
  - Client gửi `ClientHello` (danh sách Cipher Suites hỗ trợ, Client Random, và `key_share` ECDHE).
  - Server gửi `ServerHello` (Cipher Suite được chọn, `key_share` của server). Từ đây hai bên đã tính được khóa bắt tay bằng ECDHE.
  - Sau `ServerHello`, server gửi `EncryptedExtensions`, `Certificate`, `CertificateVerify`, `Finished` **đã được mã hóa** (RFC 8446). Khóa phiên đối xứng (AES-GCM hoặc ChaCha20-Poly1305) được dẫn xuất qua HKDF, không bao giờ truyền qua mạng.
- **Mutual TLS (mTLS) trong Tích hợp Ngân hàng**:
  - Không chỉ Client xác thực Server, mà **Server cũng yêu cầu Client phải gửi Chứng chỉ số cá nhân (Client Certificate)** để xác minh danh tính.
  - mTLS là lựa chọn phổ biến cho kết nối API giữa ngân hàng và đối tác. Yêu cầu cụ thể của từng kênh (ví dụ NAPAS) phụ thuộc đặc tả kết nối của đối tác (kênh thuê riêng, VPN, MAC/HSM cho ISO 8583…), cần kiểm tra theo tài liệu tích hợp thực tế chứ không mặc định.
