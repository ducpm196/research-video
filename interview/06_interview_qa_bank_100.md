# CHUYÊN ĐỀ 6: BỘ 100 CÂU HỎI - ĐÁP PHỎNG VẤN THỰC CHIẾN DEV TÍCH HỢP SENIOR ACB

> **Mục tiêu**: Cung cấp phản xạ tự nhiên trước mọi câu hỏi hóc búa nhất của Hội đồng Kỹ thuật và Lãnh đạo Khối CNTT ACB, bảo vệ vững chắc mức lương 50,000,000 VND Gross.  
> **Cấu trúc 5 phần**:
> - Phần 1: Khoa học máy tính lõi, Java 21, JVM & Đa luồng (Câu 1 – 20)
> - Phần 2: Kỹ nghệ Microservices, Spring Boot, REST & Redis (Câu 21 – 40)
> - Phần 3: Hệ phân tán, Apache Kafka & Tối ưu hóa Oracle 19c (Câu 41 – 65)
> - Phần 4: Nghiệp vụ Ngân hàng, Temenos T24, NAPAS ISO 8583 & SAGA (Câu 66 – 90)
> - Phần 5: Ứng dụng AI, Thiết kế Hệ thống & Bản lĩnh Đàm phán Lương (Câu 91 – 100)

---

## PHẦN 1: KHOA HỌC MÁY TÍNH LÕI, JAVA 21, JVM & ĐA LUỒNG (CÂU 1 – 20)

### Câu 1: Trình bày sự khác biệt giữa String, StringBuilder và StringBuffer trong Java. Khi nào nên dùng loại nào?
- **Trả lời**: `String` là bất biến (immutable), mỗi thao tác nối chuỗi tạo ra một đối tượng mới trên Heap. `StringBuffer` là khả biến (mutable) và an toàn đa luồng (thread-safe) nhờ các method được bọc `synchronized` (chậm hơn). `StringBuilder` là khả biến nhưng không thread-safe (nhanh nhất). Trong xử lý bản tin ngân hàng đơn luồng, luôn dùng `StringBuilder` để ghép chuỗi nhằm tránh tạo rác trên Heap.

### Câu 2: Cơ chế Garbage Collection (GC) hoạt động như thế nào? Nêu sự khác biệt giữa Minor GC, Major GC và Full GC?
- **Trả lời**: GC dọn dẹp các vùng nhớ không còn con trỏ tham chiếu từ GC Roots (Local variables, Static fields, JNI pointers).
  - *Minor GC*: Thu dọn vùng Young Gen (Eden/Survivor); cũng là Stop-the-World nhưng thường ngắn vì chỉ sao chép các đối tượng còn sống (thời gian thực tế phụ thuộc lượng đối tượng sống, cần đo bằng log GC).
  - *Major GC*: Thu dọn vùng Old Gen.
  - *Full GC*: Thu dọn toàn bộ Heap (cả Young, Old) và Metaspace. Full GC gây hiện tượng Stop-the-World (STW) đóng băng toàn bộ ứng dụng, là nguyên nhân hàng đầu gây timeout API ngân hàng.

### Câu 3: Làm thế nào để điều tra nguyên nhân một ứng dụng Java bị lỗi `OutOfMemoryError: Java heap space`?
- **Trả lời**:
  1. Cấu hình JVM bật `-XX:+HeapDumpOnOutOfMemoryError` và `-XX:HeapDumpPath=/log/dump.hprof`.
  2. Dùng công cụ **Eclipse Memory Analyzer (MAT)** mở file `.hprof`, chạy báo cáo *Leak Suspects Report*.
  3. Kiểm tra các đối tượng chiếm Retained Heap lớn nhất: Thường là các mảng tĩnh (Static List), Cache không có chính sách hết hạn (Eviction policy), hoặc câu lệnh SQL đọc toàn bộ bảng hàng triệu dòng vào RAM mà không phân trang (Paging).

### Câu 4: Từ khóa `volatile` trong Java có tác dụng gì? Nó có thay thế được `synchronized` không?
- **Trả lời**: `volatile` đảm bảo **Tính khả kiến (Visibility)** theo Java Memory Model (JLS §17.4): lần ghi vào biến `volatile` *happens-before* mọi lần đọc biến đó xảy ra sau, nên thread khác luôn thấy giá trị mới (và cả các ghi trước đó của thread ghi). JVM hiện thực bằng memory barrier; không phải "ghi thẳng xuống RAM" vì cache CPU vốn được giữ nhất quán bằng giao thức coherence. Nó cũng ngăn trình biên dịch và CPU sắp xếp lại lệnh vượt qua điểm truy cập volatile. Tuy nhiên, `volatile` **KHÔNG ĐẢM BẢO TÍNH NGUYÊN TỬ (Atomicity)** (ví dụ phép `count++` gồm 3 thao tác read-modify-write). Để đảm bảo tính nguyên tử, phải dùng `AtomicInteger` (sử dụng cơ chế CAS) hoặc khối `synchronized`.

### Câu 5: Phân biệt `CompletableFuture`, `ExecutorService` và Virtual Threads (Java 21).
- **Trả lời**:
  - `ExecutorService`: Giao diện thực thi tác vụ; các pool kiểu `newFixedThreadPool` dùng Platform Threads (OS threads) nên số luồng bị giới hạn (vài trăm là phổ biến, tùy cấu hình). Java 21 có thêm `Executors.newVirtualThreadPerTaskExecutor()`.
  - `CompletableFuture`: Cho phép viết code bất đồng bộ theo phong cách hàm (Functional/Promise style), kết hợp nhiều tác vụ chạy song song (`allOf`, `thenApplyAsync`).
  - `Virtual Threads` (JEP 444): luồng nhẹ do JVM quản lý (có thể tới hàng triệu luồng), thường tự unmount khi gặp blocking I/O, giúp viết code đồng bộ tuần tự mà vẫn phục vụ được rất nhiều tác vụ chờ I/O. Bẫy ở Java 21: chặn I/O bên trong `synchronized` hoặc native code sẽ **ghim (pin)** luồng ảo vào carrier; thay bằng `ReentrantLock` và theo dõi bằng `-Djdk.tracePinnedThreads` (JDK 24, JEP 491, đã gỡ bỏ ghim do `synchronized`). Luồng ảo không làm CPU nhanh hơn với tác vụ tính toán nặng.

### Câu 6: Java Memory Model (JMM) định nghĩa nguyên tắc "Happens-Before" như thế nào?
- **Trả lời**: Nguyên tắc *Happens-Before* đảm bảo hành động $A$ được nhìn thấy bởi hành động $B$:
  - Mở khóa (Unlock) một monitor xảy ra trước khi Khóa (Lock) monitor đó.
  - Ghi vào một biến `volatile` xảy ra trước mọi lần đọc biến đó sau này.
  - Gọi `Thread.start()` xảy ra trước bất kỳ hành động nào trong luồng con.
  - Luồng con kết thúc (`Thread.join()`) xảy ra trước khi hàm `join()` trả về.

### Câu 7: Tại sao nên tránh dùng `finalize()` trong Java và thay thế bằng gì?
- **Trả lời**: `finalize()` không đảm bảo thời điểm thực thi, làm trì hoãn việc giải phóng bộ nhớ của GC và có thể gây nghẽn hàng đợi Finalizer. Từ Java 9, `finalize()` đã bị deprecated. Thay thế bằng giao diện `AutoCloseable` kết hợp khối lệnh `try-with-resources` hoặc dùng `java.lang.ref.Cleaner`.

### Câu 8: Phân biệt Shallow Copy và Deep Copy. Trong banking DTO làm sao để Deep Copy an toàn?
- **Trả lời**: Shallow Copy chỉ copy giá trị biến nguyên thủy và sao chép con trỏ tham chiếu đối tượng (thay đổi đối tượng con ở bản copy sẽ ảnh hưởng bản gốc). Deep Copy tạo mới toàn bộ cây đối tượng con độc lập. Để Deep Copy an toàn: Dùng cơ chế Serialization/Deserialization (qua Jackson ObjectMapper / Protobuf) hoặc tự viết hàm Copy Constructor tường minh.

### Câu 9: Giải thích cấu trúc Cây B-Tree và lý do tại sao các Database như Oracle/Postgres dùng B-Tree làm Index thay vì Cây Nhị phân?
- **Trả lời**: Cây nhị phân có hệ số phân nhánh nhỏ (2 con), làm tăng chiều cao của cây ($H = \log_2 N$). Mỗi lần duyệt qua 1 node trên đĩa cứng tương đương 1 lần Disk I/O. Cây B-Tree (và B+Tree) có hệ số phân nhánh rất lớn (hàng trăm đến hàng ngàn con mỗi node), chiều cao cây chỉ từ 3 đến 4 tầng đối với hàng chục triệu bản ghi. Do đó, chỉ cần tối đa 3–4 lần Disk I/O là tìm thấy bản ghi dữ liệu.

### Câu 10: Cơ chế ForkJoinPool hoạt động theo nguyên lý nào? Ứng dụng trong việc xử lý dữ liệu ngân hàng?
- **Trả lời**: Dựa trên thuật toán **Chia để trị (Divide and Conquer)** và cơ chế **Đánh cắp công việc (Work-Stealing)**. Mỗi Worker Thread có một hàng đợi Deque (Double-ended queue) riêng. Khi một thread xử lý xong công việc của mình, nó sẽ "đánh cắp" tác vụ từ đuôi hàng đợi của các thread đang bận rộn khác. Dùng để tính toán song song lãi suất, sao kê và đối soát cho hàng triệu khách hàng cuối ngày.

### Câu 11: ClassLoader trong Java hoạt động theo mô hình nào? Vì sao có cơ chế "Parent Delegation" và khi nào người ta phá nó?
- **Trả lời**: Có 3 ClassLoader dựng sẵn: *Bootstrap* (nạp `java.base`, viết bằng native), *Platform* (Java 9+, thay cho Extension) và *Application* (nạp classpath của ứng dụng). Khi cần một class, mỗi loader **hỏi loader cha trước**, cha không có mới tự nạp.
  - *Lý do*: bảo đảm lớp lõi như `java.lang.String` chỉ do JDK nạp, không ai "đóng giả" được bằng một file `String.class` trong thư mục ứng dụng; đồng thời mỗi class chỉ có một bản trong một cây loader.
  - *Phá có chủ đích*: Tomcat nạp class của webapp **trước** class của container để mỗi ứng dụng dùng thư viện riêng; OSGi (nền của Adobe Experience Manager) cho mỗi bundle một loader riêng.
  - *Hậu quả thực tế*: redeploy nhiều lần mà còn tham chiếu giữ loader cũ (ví dụ `ThreadLocal`, driver JDBC đăng ký tĩnh) sẽ gây rò rỉ Metaspace → `OutOfMemoryError: Metaspace`.

### Câu 12: Vì sao `ThreadLocal` có thể gây rò rỉ bộ nhớ trong ứng dụng dùng Thread Pool? Cách dùng an toàn?
- **Trả lời**: Dữ liệu `ThreadLocal` nằm trong `ThreadLocalMap` của chính đối tượng `Thread`. **Khóa** của map là tham chiếu yếu (weak) nhưng **giá trị** là tham chiếu mạnh. Thread trong pool sống rất lâu nên giá trị không được dọn nếu quên gỡ, và còn "dính" sang request kế tiếp dùng lại thread đó (lộ dữ liệu giữa hai khách hàng).
  - Luôn gọi `remove()` trong khối `finally` (hoặc trong `Filter` ở cuối request). Dùng cho `traceId` của MDC, `SecurityContext`, nhưng **không** lưu đối tượng lớn.
  - Với Virtual Threads (Java 21) mỗi luồng ảo cũng có `ThreadLocal` riêng; hàng triệu luồng nghĩa là hàng triệu bản sao, nên cân nhắc truyền tham số tường minh hoặc `ScopedValue` (bản preview ở Java 21).

### Câu 13: Type Erasure của Java Generics là gì? Nó gây ra những hạn chế nào?
- **Trả lời**: Trình biên dịch kiểm tra kiểu generic rồi **xóa** thông tin kiểu tham số, chỉ giữ cận trên (thường là `Object`). Tại thời điểm chạy, `List<String>` và `List<Integer>` cùng là `List`.
  - Hạn chế: không viết được `new T()`, `new T[10]`, `x instanceof List<String>`; không overload hai method chỉ khác kiểu tham số generic; có thể xảy ra *heap pollution* (một `List<String>` chứa `Integer` nếu đi qua raw type).
  - Trình biên dịch sinh *bridge method* để giữ tính đa hình sau khi xóa kiểu.
  - Ứng dụng: khi Jackson cần giải mã `List<TransferRequest>`, phải truyền `TypeReference<List<TransferRequest>>` vì thông tin kiểu không còn ở runtime.

### Câu 14: Java NIO (Channel, Buffer, Selector) khác I/O truyền thống thế nào? Ý nghĩa với hệ thống nhiều kết nối socket?
- **Trả lời**: I/O truyền thống gán **một luồng cho một kết nối** và luồng bị chặn khi chờ dữ liệu. NIO cho phép đặt channel ở chế độ non-blocking và dùng một `Selector` (trên Linux dựa vào `epoll`) để **một luồng theo dõi hàng ngàn kết nối**, chỉ xử lý kết nối nào đã có dữ liệu sẵn sàng.
  - Dữ liệu đi qua `ByteBuffer` (có `position`, `limit`, `capacity`; gọi `flip()` để chuyển từ ghi sang đọc). `DirectByteBuffer` nằm ngoài heap, tránh một lần copy khi gửi qua mạng nhưng tốn chi phí cấp phát.
  - Netty và Vert.x xây trên mô hình này (Event Loop). Quy tắc sống còn: **không bao giờ chặn Event Loop** (không gọi JDBC, `Thread.sleep`, tính toán nặng trên đó), nếu không toàn bộ kết nối bị đứng.
  - Java 21 cho cách thứ hai: giữ code đồng bộ dễ đọc nhưng chạy trên Virtual Threads.

### Câu 15: Java Reflection tốn chi phí ở đâu và làm sao giảm?
- **Trả lời**: Chi phí đến từ việc tra cứu method/field theo tên, kiểm tra quyền truy cập, đóng gói tham số (boxing, mảng `Object[]`) và JIT khó inline lời gọi. Spring, Hibernate, Jackson dùng reflection rất nhiều nhưng chủ yếu **một lần lúc khởi động**.
  - Giảm chi phí: cache đối tượng `Method`/`Field` đã tra cứu; gọi `setAccessible(true)` một lần; dùng `MethodHandle` lưu trong biến `static final` để JIT tối ưu được.
  - Từ Java 18 (JEP 416) reflection nội bộ được cài đặt lại bằng method handle nên khoảng cách hẹp hơn.
  - Hướng khác: sinh mã lúc biên dịch (MapStruct thay cho mapper dùng reflection; Micronaut/Quarkus xử lý DI lúc build). Với GraalVM Native Image, phần reflection phải khai báo trước vì không tra cứu động được.

### Câu 16: Khi tinh chỉnh JVM cho dịch vụ giao dịch, em bắt đầu từ cờ nào và theo nguyên tắc nào?
- **Trả lời**: Nguyên tắc: **đo trước, chỉnh sau**; bật log GC (`-Xlog:gc*`) và xem tần suất, thời gian pause, mức heap sau Full GC.
  - `-Xms` bằng `-Xmx` để heap không co giãn gây pause. Trong container dùng `-XX:MaxRAMPercentage=75` thay vì số cứng, chừa chỗ cho Metaspace, thread stack, direct buffer.
  - Bộ gom rác: **G1** (mặc định từ Java 9) với mục tiêu `-XX:MaxGCPauseMillis` (mặc định 200ms); khi heap lớn và cần pause rất ngắn, thử **ZGC** (`-XX:+UseZGC`; ở Java 21 bật chế độ generational bằng `-XX:+ZGenerational`, từ JDK 23 generational là mặc định (JEP 474) và từ JDK 24 cờ này đã lỗi thời (JEP 490)).
  - Bật `-XX:+HeapDumpOnOutOfMemoryError` luôn luôn ở production (xem Câu 3).
  - Sai lầm hay gặp: tăng heap để "chữa" rò rỉ bộ nhớ, hoặc chỉnh nhiều cờ cùng lúc nên không biết cờ nào có tác dụng.

### Câu 17: `HashMap` hoạt động bên trong thế nào, và `ConcurrentHashMap` an toàn đa luồng bằng cách nào?
- **Trả lời**: `HashMap` là mảng các bucket; chỉ số = `hash(key) & (n-1)`. Khi hai khóa rơi cùng bucket thì nối thành danh sách; từ Java 8, khi thêm phần tử vào một bucket đã có 8 phần tử (`TREEIFY_THRESHOLD = 8`) và mảng đủ lớn (≥ 64; nếu nhỏ hơn thì resize thay vì chuyển cây) thì chuyển thành **cây đỏ-đen** để tra cứu $O(\log n)$ thay vì $O(n)$. Khi số phần tử vượt `capacity × 0.75` mảng được nhân đôi (resize).
  - `HashMap` **không** an toàn đa luồng: ghi đồng thời có thể mất dữ liệu (ở Java 7 còn gây vòng lặp vô hạn khi resize).
  - `ConcurrentHashMap` (Java 8+): bucket rỗng thì ghi bằng CAS; bucket có dữ liệu thì khóa `synchronized` **chỉ trên nút đầu của bucket đó**, nên nhiều luồng ghi các bucket khác nhau không chặn nhau. Không cho phép khóa hoặc giá trị `null`.
  - Dùng các phép nguyên tử `computeIfAbsent`, `merge` thay cho "kiểm tra rồi ghi" (check-then-act) vốn dễ sai.

### Câu 18: Vì sao tiền không được lưu bằng `double`? Quy tắc khi dùng `BigDecimal` và hợp đồng `equals`/`hashCode`?
- **Trả lời**: `double` là số nhị phân dấu chấm động nên không biểu diễn chính xác nhiều số thập phân (`0.1 + 0.2 = 0.30000000000000004`); sai số tích lũy qua hàng triệu giao dịch là không chấp nhận được.
  - Dùng `BigDecimal` tạo từ **chuỗi** (`new BigDecimal("0.1")`), không từ `double`. Luôn chỉ định `scale` và `RoundingMode` tường minh khi chia (`divide(x, 2, RoundingMode.HALF_UP)`), nếu không sẽ ném `ArithmeticException` với phép chia vô hạn tuần hoàn.
  - Bẫy: `new BigDecimal("2.0").equals(new BigDecimal("2.00"))` là `false` (khác scale); so sánh giá trị phải dùng `compareTo(...) == 0`. Vì vậy dùng `BigDecimal` làm khóa `HashMap` cũng nguy hiểm, nên chuẩn hóa bằng `stripTrailingZeros()`.
  - Hợp đồng: hai đối tượng `equals` thì phải có cùng `hashCode`; ghi đè một trong hai mà bỏ quên cái kia làm `HashMap`/`HashSet` tra cứu sai.
  - Phía DB dùng kiểu `NUMBER(p, s)`; một số hệ thống lưu theo đơn vị nhỏ nhất bằng `long` để tránh hẳn số thập phân.

### Câu 19: Deadlock trong Java xảy ra khi nào, phát hiện và phòng tránh ra sao?
- **Trả lời**: Cần đủ 4 điều kiện Coffman: loại trừ tương hỗ, giữ-và-chờ, không bị tước đoạt, chờ vòng tròn. Ví dụ luồng A giữ khóa tài khoản X chờ Y, luồng B giữ Y chờ X (chuyển tiền chéo hai chiều).
  - *Phát hiện*: `jstack <pid>` (hoặc `jcmd <pid> Thread.print`) in ra mục `Found one Java-level deadlock` kèm luồng nào giữ/chờ khóa nào.
  - *Phòng tránh*: luôn lấy khóa theo **thứ tự cố định** (ví dụ sắp tăng dần theo số tài khoản); dùng `tryLock(timeout)` rồi lùi lại; thu hẹp phạm vi khóa; tránh gọi code lạ trong khi đang giữ khóa.
  - Cùng nguyên tắc "thứ tự khóa xác định" này áp dụng cho deadlock ở Oracle (xem Câu 63 và Câu 75).

### Câu 20: Java 17 và Java 21 có những tính năng nào đáng dùng trong code nghiệp vụ?
- **Trả lời**: Các bản LTS gần đây: 8, 11, 17, 21.
  - *Java 17*: `record` (DTO bất biến gọn), `sealed class/interface` (giới hạn tập kiểu con, tiện mô hình hóa kết quả giao dịch), `text block` (SQL/JSON nhiều dòng), `switch` expression.
  - *Java 21*: **Virtual Threads** (chính thức), *pattern matching cho `switch`* và *record patterns* (chính thức), `SequencedCollection` (có `getFirst/getLast/reversed`). *Structured Concurrency* và *Scoped Values* ở Java 21 vẫn là bản preview, chưa nên dùng cho production.
  - Lưu ý khi nâng cấp: kiểm tra thư viện (Spring Boot 3 yêu cầu tối thiểu Java 17), cờ JVM đã bị xóa, và kiểm thử tải trước khi lên production.

---

## PHẦN 2: KỸ NGHỆ MICROSERVICES, SPRING BOOT & REDIS (CÂU 21 – 40)

### Câu 21: Nêu vòng đời của một Spring Bean (Bean Lifecycle).
- **Trả lời**:
  1. Nạp Bean Definition $\to$ 2. Khởi tạo đối tượng (Constructor) $\to$ 3. Tiêm phụ thuộc (Dependency Injection - Setters/Fields) $\to$ 4. Gọi các Aware interfaces (`BeanNameAware`, `ApplicationContextAware`) $\to$ 5. `BeanPostProcessor.postProcessBeforeInitialization` $\to$ 6. `@PostConstruct` / `InitializingBean.afterPropertiesSet` $\to$ 7. `BeanPostProcessor.postProcessAfterInitialization` (Tại đây Spring bọc Proxy CGLIB/JDK cho `@Transactional`) $\to$ 8. Bean sẵn sàng phục vụ $\to$ 9. `@PreDestroy` / `DisposableBean.destroy` khi ứng dụng tắt.

### Câu 22: Điều gì xảy ra nếu hai Spring Beans bị phụ thuộc vòng (Circular Dependency)? Spring xử lý như thế nào?
- **Trả lời**: Nếu dùng Constructor Injection, Spring ném lỗi `BeanCurrentlyInCreationException` và không khởi động được ứng dụng. Từ Spring Boot 2.6, phụ thuộc vòng **bị cấm mặc định** cho mọi kiểu injection (`spring.main.allow-circular-references=false`); cách đúng là tách thiết kế để bỏ vòng. Nếu bật lại cờ này và dùng Setter/Field Injection, Spring giải quyết được thông qua **Bộ nhớ đệm 3 tầng (Three-level Cache)** của `DefaultSingletonBeanRegistry`:
  - `singletonObjects` (Cache 1): Chứa các Bean đã khởi tạo hoàn chỉnh.
  - `earlySingletonObjects` (Cache 2): Chứa Bean thô sớm (Early reference) để giải quyết phụ thuộc vòng.
  - `singletonFactories` (Cache 3): Chứa ObjectFactory để tạo Early Proxy.

### Câu 23: Làm thế nào để đảm bảo một API Spring Boot tuân thủ nguyên tắc Idempotent?
- **Trả lời**:
  1. Client gửi kèm header `Idempotency-Key` (tên theo bản nháp IETF; hệ thống cũ hay dùng `X-Idempotency-Key`) hoặc `requestId` duy nhất sinh từ UUID.
  2. Tầng API Gateway / Interceptor kiểm tra key trong Redis: `SET key "PROCESSING" NX EX 120`.
  3. Nếu key đã tồn tại:
     - Nếu value là `"PROCESSING"`: Trả về mã HTTP `409 Conflict` (Giao dịch đang được xử lý).
     - Nếu value là kết quả giao dịch đã hoàn tất: Trả về ngay kết quả đã lưu trong cache mà không gọi xuống Core Banking lần 2.
  4. Nếu key chưa tồn tại: Cho phép đi tiếp vào controller hạch toán, sau khi hạch toán xong thì cập nhật kết quả vào Redis.

### Câu 24: Khi nào nên dùng `@Qualifier` và `@Primary` trong Spring?
- **Trả lời**: Khi có từ hai Bean trở lên cùng triển khai một Interface (ví dụ: `T24Adapter` và `CoreMockAdapter` cùng implement `CoreBankingAdapter`). `@Primary` đánh dấu Bean mặc định được chọn nếu không có chỉ định cụ thể. `@Qualifier("beanName")` chỉ định đích danh Bean cần inject tại vị trí tiêm phụ thuộc.

### Câu 25: Giải thích hiện tượng Thủng Cache (Cache Penetration) và cách xử lý bằng Bloom Filter.
- **Trả lời**: Thủng Cache xảy ra khi hacker liên tục gửi các request tra cứu ID không tồn tại trong hệ thống (ví dụ `cif_id = -999999`). Cache bị miss liên tục, khiến 100% request chọc thẳng vào Database làm sập DB.
  - *Giải pháp*: Triển khai **Bloom Filter** trước tầng Cache. Bloom Filter sử dụng mảng bit và nhiều hàm băm để kiểm tra sự tồn tại của ID với độ phức tạp $O(1)$. Nếu Bloom Filter trả về FALSE $\to$ Chắc chắn ID không tồn tại, từ chối request ngay lập tức mà không cần truy vấn DB hay Redis.

### Câu 26: Phân biệt Filter, Interceptor và AOP Aspect trong Spring Boot.
- **Trả lời**:
  - `Filter` (Servlet level): Chạy trong chuỗi filter của Web Container (Tomcat), **trước** `DispatcherServlet`; trong Spring Boot filter thường vẫn là một Spring bean (đăng ký qua `FilterRegistrationBean`/`DelegatingFilterProxy`, Spring Security là một chuỗi filter). Dùng cho CORS, xác thực, ánh xạ chứng thư client mTLS thành danh tính (bắt tay TLS do connector của Tomcat thực hiện), ghi log request raw, nén.
  - `Interceptor` (Spring MVC level): Chạy bên trong `DispatcherServlet`, trước và sau khi request vào Controller (biết handler nào sẽ xử lý). Dùng để kiểm tra Authentication token, validate header `Idempotency-Key`.
  - `AOP Aspect`: Áp dụng tại bất kỳ tầng nào (Service, Repository, Controller) thông qua bọc quanh method execution. Dùng cho Audit Log, đo thời gian thực thi (@Timed), Transaction management.

### Câu 27: Làm sao cấu hình Connection Pool (HikariCP) tối ưu trong Spring Boot cho hệ thống ngân hàng?
- **Trả lời**:
  - `maximum-pool-size`: Không nên đặt quá lớn. Điểm khởi đầu được HikariCP ("About Pool Sizing") dẫn lại từ wiki PostgreSQL:
    $$\text{Connections} = (\text{CPU Cores} \times 2) + \text{Effective Spindle Count}$$
    Trong đó CPU Cores là số nhân của **máy chủ cơ sở dữ liệu**, và tổng kết nối thực tế = pool size × số instance ứng dụng. Đây là điểm xuất phát để đo tải rồi tinh chỉnh, không phải con số tối ưu cố định; pool quá lớn (hàng trăm) thường làm DB tranh chấp CPU/khóa và tăng độ trễ.
  - `connection-timeout`: 2000–3000ms (nếu quá thời gian này không lấy được kết nối thì báo lỗi ngay, tránh treo request).
  - `idle-timeout`: 600,000ms (10 phút).
  - `max-lifetime`: 1,800,000ms (30 phút, phải ngắn hơn timeout của tường lửa hoặc database để tránh stale connection).

### Câu 28: JWT là gì, vì sao nó "stateless", và làm sao thu hồi (logout, khóa tài khoản) khi token chưa hết hạn?
- **Trả lời**: JWT gồm header, payload (claims) và chữ ký; server chỉ cần kiểm tra chữ ký, `iss`, `aud`, `exp` mà không tra DB nên "stateless". Payload chỉ được mã hóa Base64, **không bí mật**, nên không đặt dữ liệu nhạy cảm vào đó. Dùng RS256/ES256 (khóa bất đối xứng) để các dịch vụ chỉ cần khóa công khai.
  - Vì stateless nên không thu hồi trực tiếp được. Cách làm: access token **sống ngắn** (5–15 phút) cộng refresh token có xoay vòng (rotation); khi logout hoặc khóa tài khoản, lưu `jti` của token vào **blacklist trong Redis với TTL = thời gian còn lại của token**, nên bộ nhớ tự dọn.
  - Gateway/Filter kiểm tra `jti` có trong blacklist không trước khi cho vào. Trong Spring Security 6 dùng `http.oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))` (kiểu `oauth2ResourceServer().jwt()` đã deprecated từ 6.1).

### Câu 29: Redis Cluster chia dữ liệu thế nào? Những giới hạn khi dùng lệnh nhiều khóa và khi failover?
- **Trả lời**: Không gian khóa chia thành **16384 hash slot**; slot của khóa = `CRC16(key) mod 16384`, mỗi master giữ một dải slot. Client nhận `MOVED` (slot đã chuyển hẳn) hoặc `ASK` (đang di chuyển) rồi hỏi đúng node.
  - Lệnh nhiều khóa, Lua script, giao dịch `MULTI` chỉ chạy được khi mọi khóa **cùng slot**, nếu không báo `CROSSSLOT`. Dùng *hash tag* `{account:123}` để ép các khóa liên quan vào cùng slot.
  - Sao chép master→replica là **bất đồng bộ**: master có thể xác nhận ghi rồi chết trước khi replica nhận được, nên một số ghi đã "thành công" bị mất sau failover. Vì vậy Redis không phải nguồn sự thật cho số dư; dữ liệu tiền phải nằm ở DB giao dịch (xem Câu 35).

### Câu 30: Circuit Breaker (Resilience4j) hoạt động thế nào và cấu hình ra sao cho lời gọi sang Core Banking?
- **Trả lời**: Ba trạng thái: **CLOSED** (cho qua, đếm lỗi trong cửa sổ trượt), **OPEN** (vượt `failureRateThreshold`, từ chối ngay không gọi xuống dịch vụ lỗi, tránh dồn thêm tải), **HALF_OPEN** (sau `waitDurationInOpenState` cho vài lời gọi thử, thành công thì đóng lại).
  - Kết hợp: *Timeout* (luôn đặt thời gian chờ), *Retry* với exponential backoff + jitter, *Bulkhead* (giới hạn số lời gọi đồng thời để một đối tác chậm không ăn hết thread pool).
  - **Cẩn trọng với tiền**: chỉ retry thao tác idempotent hoặc có idempotency key. Khi lệnh ghi nợ bị timeout, kết quả là *chưa biết*, không phải *thất bại*; fallback đúng là trả trạng thái "đang xử lý" rồi đối soát/bù trừ, tuyệt đối không giả lập "thành công".

### Câu 31: Distributed Tracing với OpenTelemetry giúp gì khi một giao dịch đi qua nhiều dịch vụ?
- **Trả lời**: Mỗi yêu cầu có một `trace id` xuyên suốt, mỗi bước là một `span` (có thời gian bắt đầu/kết thúc, thuộc tính, quan hệ cha-con). Giữa các dịch vụ HTTP, ngữ cảnh truyền qua header chuẩn W3C `traceparent` (`00-<trace-id 32 hex>-<span-id 16 hex>-<flags>`).
  - Với bất đồng bộ phải tự truyền ngữ cảnh: đặt vào **header của bản tin Kafka** hoặc thuộc tính bản tin MQ, nếu không chuỗi trace bị đứt tại hàng đợi.
  - Ghi `traceId` vào log (qua MDC) để từ một mã giao dịch lọc ra mọi log liên quan. Dùng *sampling* (lấy mẫu) để kiểm soát chi phí, nhưng luôn giữ trace có lỗi hoặc chậm.
  - Giá trị: trả lời nhanh câu hỏi "giao dịch chậm ở bước nào: cổng, Core hay NAPAS?".

### Câu 32: Những biện pháp bảo mật container (Docker) cơ bản cho dịch vụ ngân hàng?
- **Trả lời**:
  - Chạy bằng **user không phải root** (`USER app`), hệ thống file chỉ đọc (`readOnlyRootFilesystem`), bỏ các Linux capability không cần (`drop: ["ALL"]`), không dùng `--privileged`.
  - Ảnh nền tối giản (distroless/alpine) để giảm bề mặt tấn công; quét lỗ hổng ảnh trong pipeline CI; ghim phiên bản (digest), không dùng `latest`.
  - **Không nhét bí mật vào ảnh hoặc biến môi trường trong Dockerfile**; lấy từ Secret của Kubernetes hoặc Vault lúc chạy.
  - Giới hạn CPU/memory để một container lỗi không làm đói cả node; dùng NetworkPolicy chỉ mở các luồng cần thiết.

### Câu 33: Liveness, Readiness và Startup probe trên Kubernetes khác nhau thế nào? Sai lầm phổ biến?
- **Trả lời**: *Liveness*: tiến trình còn sống không, nếu fail thì **khởi động lại** container. *Readiness*: sẵn sàng nhận lưu lượng chưa, nếu fail thì **gỡ khỏi Service** nhưng không restart. *Startup*: cho ứng dụng khởi động chậm thêm thời gian trước khi áp liveness.
  - Sai lầm: đưa kiểm tra DB/Kafka vào **liveness**; khi DB chậm, toàn bộ pod bị restart hàng loạt làm sự cố nặng thêm. Kiểm tra phụ thuộc ngoài thuộc về readiness.
  - Tắt êm: bật `server.shutdown=graceful` trong Spring Boot, đặt `terminationGracePeriodSeconds` đủ dài và `preStop` để pod ngừng nhận request mới nhưng hoàn tất các giao dịch đang chạy.

### Câu 34: Nguyên tắc thiết kế REST API cho nghiệp vụ tài chính?
- **Trả lời**:
  - Tài nguyên là danh từ (`/accounts/{id}/transfers`); dùng đúng phương thức: `GET` an toàn, `PUT`/`DELETE` idempotent, `POST` tạo mới (không idempotent nếu không có idempotency key), `PATCH` cập nhật một phần.
  - Mã trạng thái có ý nghĩa: `400` sai cú pháp, `401/403` xác thực/phân quyền, `404`, `409` xung đột (giao dịch đang xử lý, phiên bản cũ), `422` sai nghiệp vụ, `429` kèm `Retry-After`. Lỗi trả theo khuôn thống nhất (RFC 9457 Problem Details, thay thế RFC 7807, `application/problem+json`).
  - Tiền trong JSON truyền dạng **chuỗi hoặc số nguyên đơn vị nhỏ nhất**, không dùng số thực. Phân trang theo *cursor* thay vì `offset` khi dữ liệu lớn và thay đổi liên tục.
  - Quản lý phiên bản API (`/v1`), mô tả bằng OpenAPI/Swagger và giữ tương thích ngược.

### Câu 35: Khóa phân tán bằng Redis (`SET NX`) đúng cách ra sao, và nó có đủ để bảo đảm không giải ngân hai lần không?
- **Trả lời**: Cách làm đúng: `SET lock:{id} <token ngẫu nhiên> NX PX 300000` (cấp khóa nguyên tử có hạn), và **mở khóa bằng Lua** so sánh token rồi mới xóa, để không xóa nhầm khóa của luồng khác sau khi khóa mình đã hết hạn. Có thể dùng "watchdog" (Redisson) để gia hạn khi tác vụ còn chạy.
  - **Giới hạn**: TTL hết hạn trong lúc luồng bị dừng (GC pause, mạng chậm) làm hai bên cùng tin mình giữ khóa; sao chép bất đồng bộ có thể làm mất khóa khi failover. Tranh luận Redlock (Kleppmann và tác giả Redis) cho thấy khóa Redis là cơ chế **giảm xung đột/tối ưu**, không phải bảo đảm tuyệt đối.
  - Vì vậy phải có **tuyến phòng thủ cuối ở DB**: ràng buộc UNIQUE trên mã giải ngân/`requestId`, hoặc cập nhật có điều kiện `WHERE status = 'APPROVED'` (hoặc cột version), kèm *fencing token* nếu cần. Mutex Redis chặn phần lớn trùng lặp; ràng buộc DB mới bảo đảm tính đúng.

### Câu 36: Các chiến lược cache và 3 sự cố kinh điển: Penetration, Breakdown, Avalanche?
- **Trả lời**: Mẫu phổ biến là *Cache-Aside*: đọc cache, miss thì đọc DB rồi ghi cache; khi cập nhật thì ghi DB rồi **xóa** cache.
  - *Penetration* (truy vấn khóa không tồn tại): Bloom Filter hoặc cache giá trị rỗng với TTL ngắn (xem Câu 25).
  - *Breakdown* (một khóa nóng hết hạn, hàng ngàn request cùng lao xuống DB): khóa mutex khi dựng lại cache (chỉ một luồng nạp, số còn lại chờ hoặc dùng dữ liệu cũ), hoặc "hết hạn logic" và làm mới nền.
  - *Avalanche* (nhiều khóa hết hạn cùng lúc hoặc Redis sập): **TTL cộng ngẫu nhiên (jitter)**, nhiều tầng cache, giới hạn tốc độ và circuit breaker bảo vệ DB.
  - Nhất quán: có khoảng trễ giữa ghi DB và xóa cache; chấp nhận nhất quán cuối cùng cho dữ liệu hiển thị, **không** dùng cache làm nguồn cho số dư khi hạch toán.

### Câu 37: Những cạm bẫy của `@Transactional` trong Spring mà em từng thấy?
- **Trả lời**:
  - **Gọi nội bộ (self-invocation)**: method `@Transactional` gọi từ method khác cùng class sẽ không đi qua proxy nên không có transaction. Tách sang bean khác.
  - Mặc định chỉ **rollback với `RuntimeException`/`Error`**; checked exception không rollback trừ khi đặt `rollbackFor`.
  - `@Transactional` trên method `private`/`final` hoặc class không do Spring quản lý thì vô hiệu.
  - `Propagation.REQUIRES_NEW` mở transaction độc lập, dùng cho ghi log kiểm toán nhưng cần thận trọng vì dùng thêm một connection (có thể cạn pool khi lồng nhiều).
  - **Không giữ transaction qua lời gọi mạng chậm** (gọi Core/NAPAS) vì giữ khóa và connection DB lâu; tách phần ghi DB và phần gọi ngoài, dùng Outbox hoặc SAGA.
  - Nhớ rằng gọi `@Transactional` rồi bắn Kafka trong cùng method vẫn là dual-write (xem Câu 42).

### Câu 38: Khi nào chọn gRPC thay vì REST cho giao tiếp giữa các dịch vụ?
- **Trả lời**: gRPC chạy trên HTTP/2 (ghép kênh, một kết nối nhiều luồng), dùng Protobuf nhị phân (nhỏ, nhanh), có hợp đồng `.proto` sinh code hai phía, hỗ trợ streaming và **deadline** lan truyền qua chuỗi lời gọi. Phù hợp giao tiếp nội bộ, độ trễ thấp, nhiều lời gọi.
  - REST/JSON phù hợp API công khai cho đối tác và kênh mobile/web: dễ gỡ lỗi, trình duyệt gọi trực tiếp, hệ sinh thái rộng.
  - Tương thích Protobuf: **không đổi số thứ tự field, không tái sử dụng số đã xóa**, chỉ thêm field mới; đây là luật vàng để triển khai từng dịch vụ mà không phá vỡ nhau.
  - Dù chọn gì cũng phải đặt timeout, retry có kiểm soát và idempotency cho thao tác ghi.

### Câu 39: Dữ liệu trong microservices: vì sao "mỗi dịch vụ một database", và SAGA Choreography khác Orchestration thế nào?
- **Trả lời**: Mỗi dịch vụ sở hữu dữ liệu của mình để thay đổi và mở rộng độc lập; hệ quả là **không có JOIN hoặc transaction ACID xuyên dịch vụ**. Truy vấn tổng hợp dùng *API Composition* hoặc *CQRS* (một read model dựng từ sự kiện).
  - *Choreography*: các dịch vụ phản ứng với sự kiện của nhau, không có điều phối viên. Ưu: ít điểm tập trung. Nhược: luồng nghiệp vụ nằm rải rác, khó theo dõi và dễ vòng lặp sự kiện.
  - *Orchestration*: một bộ điều phối giữ **máy trạng thái** và ra lệnh từng bước, gọi bù trừ khi lỗi. Ưu: luồng rõ, dễ quan sát, dễ thêm bước. Nhược: bộ điều phối thành thành phần quan trọng cần nhân bản và bền vững (lưu trạng thái trong DB).
  - Với giải ngân, thanh toán nhiều bước có tiền, thường chọn Orchestration vì cần truy vết và kiểm toán từng bước.

### Câu 40: Cấu hình, bí mật và triển khai an toàn: em xử lý thế nào từ 12-Factor đến đổi schema DB?
- **Trả lời**:
  - Cấu hình tách khỏi mã (12-Factor): `application.yml` theo profile, ConfigMap/Spring Cloud Config; **bí mật** (mật khẩu DB, khóa ký) lấy từ Kubernetes Secret/Vault, xoay vòng định kỳ, không commit vào Git.
  - Triển khai: *Rolling update* mặc định; *Blue/Green* chuyển nhanh và quay lui nhanh; *Canary* cho một phần nhỏ lưu lượng trước. GitOps (Argo CD/Flux) coi Git là nguồn sự thật của trạng thái triển khai.
  - Đổi schema không dừng hệ thống: công cụ migration (Flyway/Liquibase) và mẫu **Expand → Migrate → Contract**: thêm cột mới (tương thích bản cũ), chạy hai phiên bản song song, chuyển dữ liệu, rồi mới xóa cột cũ ở bản sau. Không bao giờ đổi tên/xóa cột trong cùng bản phát hành với code dùng nó.
  - Mọi thay đổi có kế hoạch quay lui đã được thử.

---

## PHẦN 3: HỆ PHÂN TÁN, APACHE KAFKA & TỐI ƯU ORACLE 19C (CÂU 41 – 65)

### Câu 41: Định lý CAP phát biểu gì? Một hệ thống ngân hàng Core hạch toán tiền bạc thuộc nhóm nào (CP hay AP)?
- **Trả lời**: Định lý CAP khẳng định trong một hệ thống phân tán khi xảy ra Phân mảnh mạng (Network Partition - P), ta chỉ có thể chọn tính Nhất quán (Consistency - C) hoặc tính Sẵn sàng (Availability - A).
  - Hệ thống hạch toán tiền bạc, số dư tài khoản của Ngân hàng **BẮT BUỘC PHẢI THUỘC NHÓM CP**. Khi đứt mạng giữa các node dữ liệu, ngân hàng thà từ chối giao dịch (mất Availability) chứ tuyệt đối không bao giờ cho phép 2 node ghi nợ số dư lệch nhau (mất Consistency gây thất thoát tài sản).
  - Các hệ thống phụ trợ (như Lịch sử thông báo biến động số dư, hiển thị tin tức khuyến mãi) có thể chấp nhận nhóm **AP** (Eventual Consistency).

### Câu 42: Transactional Outbox Pattern giải quyết bài toán gì? So sánh 2 cách đọc bảng Outbox: Polling Publisher và CDC (Change Data Capture).
- **Trả lời**: Giải quyết bài toán Dual-Write (ghi DB và bắn Kafka đồng thời mà không dùng 2PC).
  - *Polling Publisher*: Dùng một tiến trình chạy nền định kỳ `SELECT * FROM outbox WHERE status = 'PENDING' FOR UPDATE SKIP LOCKED` rồi gửi Kafka. Ưu điểm: Đơn giản, dễ viết. Nhược điểm: Gây tải định kỳ lên DB, có độ trễ (latency vài giây).
  - *CDC (Debezium)*: Đọc Redo Log/WAL của Database engine. Ưu điểm: độ trễ thấp (thường dưới một giây khi hệ thống khỏe), không phải chạy truy vấn polling, bắt được mọi thay đổi đã commit có trong log. Đánh đổi: vẫn có tải (với Oracle, LogMiner cần ARCHIVELOG và supplemental logging), vận hành phức tạp hơn, và giao nhận là at-least-once nên consumer phải idempotent.
  - Lưu ý với Polling: nếu chạy nhiều poller với `SKIP LOCKED` thì thứ tự gửi theo cùng một khóa nghiệp vụ không còn được bảo đảm.

### Câu 43: Làm thế nào để đảm bảo thứ tự của các sự kiện giao dịch (Order Preservation) trong Apache Kafka?
- **Trả lời**:
  1. Trong Kafka, **thứ tự chỉ được đảm bảo trong phạm vi MỘT Partition**, không đảm bảo trên toàn bộ Topic.
  2. Khi Producer gửi message, bắt buộc phải truyền **Message Key** (ví dụ: `key = account_no`). Kafka sẽ dùng hàm băm `MurmurHash2(key) % num_partitions` để đảm bảo toàn bộ giao dịch của cùng một số tài khoản luôn luôn đi vào đúng một Partition duy nhất.
  3. Phía Producer phải cấu hình `max.in.flight.requests.per.connection=1` (hoặc bật `enable.idempotence=true` trên Kafka 1.0+) để tránh việc bản tin gửi lại do retry mạng làm đảo lộn thứ tự.

### Câu 44: Giải thích cơ chế Consumer Rebalance trong Kafka. Làm sao giảm thiểu tác động của Rebalance?
- **Trả lời**: Rebalance xảy ra khi có Consumer mới gia nhập nhóm, rời nhóm, crash (không gửi heartbeat trong `session.timeout.ms`), hoặc xử lý quá lâu không gọi `poll()` trong `max.poll.interval.ms`, khiến Group Coordinator phải phân chia lại Partition cho các Consumers.
  - *Eager Protocol* truyền thống: Dừng toàn bộ Consumers trong nhóm, hủy gán toàn bộ Partitions rồi gán lại từ đầu $\to$ Gây gián đoạn hệ thống (Stop-the-World).
  - *Cooperative Sticky Protocol* (Khuyên dùng): Chỉ tạm dừng và chuyển đổi các Partition cần dịch chuyển, các Partition không bị ảnh hưởng vẫn tiếp tục tiêu thụ bình thường.
  - *Tối ưu hóa*: Tăng `max.poll.interval.ms` hoặc giảm `max.poll.records` nếu tác vụ xử lý DB tốn nhiều thời gian, đảm bảo gọi `consumer.poll()` đúng hạn. Dùng *static membership* (`group.instance.id`, KIP-345) để khởi động lại pod không gây rebalance. Từ Kafka 4.0, giao thức nhóm mới (KIP-848, `group.protocol=consumer`) chuyển việc gán partition về broker và rebalance theo từng phần.

### Câu 45: Tại sao bảng con không đánh Index trên cột Foreign Key lại gây ra Deadlock trong Oracle?
- **Trả lời**: Trong Oracle (Database Concepts 19c, mục "Locks and Foreign Keys"), nếu bảng con có Foreign Key trỏ về Primary Key bảng cha mà cột Foreign Key không có Index: Khi một session `DELETE` dòng cha hoặc `UPDATE` **cột khóa chính** của bảng cha (hoặc `MERGE` vào bảng cha), Oracle lấy khóa mức bảng trên bảng con (**TM lock mode 4 – Share**) trong lúc câu lệnh đó chạy. Câu lệnh phải chờ mọi DML đang dở trên bảng con, và trong lúc giữ khóa thì chặn DML của session khác trên bảng con. Các phiên chờ chéo nhau như vậy rất dễ dẫn tới `ORA-00060 Deadlock`. (UPDATE các cột không phải khóa chính ở bảng cha không gây khóa này.) Đánh B-Tree index trên mọi cột Foreign Key là quy chuẩn bắt buộc trong thiết kế DB ngân hàng!

### Câu 46: Trình bày sự khác biệt giữa `FOR UPDATE NOWAIT`, `FOR UPDATE WAIT 5` và `FOR UPDATE SKIP LOCKED` trong Oracle.
- **Trả lời**:
  - `FOR UPDATE`: Khóa các dòng thỏa mãn điều kiện. Nếu dòng đó đang bị khóa bởi session khác, chờ vô hạn đến khi session kia nhả khóa $\to$ Nguy cơ treo thread nếu session kia bị nghẽn.
  - `FOR UPDATE NOWAIT`: Nếu dòng đang bị khóa, trả lỗi `ORA-00054: resource busy` ngay lập tức mà không chờ.
  - `FOR UPDATE WAIT n`: Chờ tối đa $n$ giây; nếu hết thời gian chưa lấy được khóa thì trả lỗi `ORA-30006`.
  - `FOR UPDATE SKIP LOCKED`: Bỏ qua các dòng đang bị khóa và chỉ lấy các dòng chưa bị khóa. Rất hợp để xây Job Worker/hàng đợi chạy song song trên Oracle mà các worker không phải chờ khóa của nhau; đổi lại không còn thứ tự xử lý chặt chẽ giữa các worker.

### Câu 47: Exactly-Once Semantics (EOS) của Kafka thực sự bảo đảm điều gì và không bảo đảm điều gì?
- **Trả lời**: EOS gồm hai phần. *Idempotent producer* (`enable.idempotence=true`, mặc định từ Kafka 3.0): broker gán Producer ID và số thứ tự cho mỗi bản tin theo partition nên retry không sinh bản tin trùng. *Transaction*: `transactional.id` + Transaction Coordinator cho phép ghi nguyên tử vào nhiều partition/topic và commit cả offset đã tiêu thụ (`sendOffsetsToTransaction`); consumer đặt `isolation.level=read_committed` để chỉ thấy dữ liệu đã commit (broker ghi *commit/abort marker*).
  - Mô hình *consume → xử lý → produce* trong **nội bộ Kafka** (Kafka Streams `exactly_once_v2`) được bảo đảm đúng một lần.
  - **Không bảo đảm** tác dụng phụ ngoài Kafka (ghi DB, gọi API Core). Với chúng vẫn cần *Idempotent Consumer* (lưu `messageId` đã xử lý, ràng buộc UNIQUE) hoặc Transactional Outbox. Nói "Kafka đảm bảo exactly-once" mà không nêu giới hạn này là sai.

### Câu 48: Log Compaction của Kafka là gì và dùng khi nào?
- **Trả lời**: Với `cleanup.policy=compact`, Kafka giữ **bản ghi mới nhất của mỗi khóa** thay vì xóa theo thời gian. Bản tin có giá trị `null` (tombstone) đánh dấu xóa khóa và bị dọn sau `delete.retention.ms`.
  - Dùng cho dữ liệu dạng "trạng thái hiện tại theo khóa": bảng tham chiếu, snapshot số dư, topic changelog của Kafka Streams/ksqlDB. Consumer mới có thể dựng lại toàn bộ trạng thái bằng cách đọc topic từ đầu.
  - Lưu ý: segment đang ghi (active) không bị compact; compaction chạy nền theo `min.cleanable.dirty.ratio` nên consumer vẫn có thể thấy nhiều phiên bản cũ của một khóa; **thứ tự offset vẫn được giữ**.
  - Không dùng để lưu lịch sử giao dịch cần kiểm toán đầy đủ (dùng retention theo thời gian hoặc đẩy sang kho lưu trữ).

### Câu 49: Cấu hình nào của Kafka bảo đảm không mất bản tin khi một broker hỏng?
- **Trả lời**: Bộ ba cổ điển: `replication.factor=3`, `min.insync.replicas=2`, producer `acks=all`. Producer chỉ nhận xác nhận khi ít nhất 2 bản sao trong ISR (In-Sync Replicas) đã ghi, nên mất một broker vẫn không mất dữ liệu đã xác nhận.
  - Đặt `unclean.leader.election.enable=false` để không bầu một replica tụt hậu làm leader (sẽ mất bản tin nhưng giữ khả dụng).
  - Nếu ISR còn dưới `min.insync.replicas`, producer nhận lỗi `NotEnoughReplicas`, tức Kafka **chọn tính nhất quán thay vì sẵn sàng**, đúng tinh thần CP của hệ thống tài chính (Câu 41).
  - Producer phải xử lý lỗi gửi (callback/retry có idempotence), không "gửi rồi quên". Giá phải trả: độ trễ ghi cao hơn so với `acks=1`.

### Câu 50: Kafka consumer nên commit offset khi nào để đạt at-least-once, và xử lý "bản tin độc" (poison message) ra sao?
- **Trả lời**: Tắt `enable.auto.commit`, **xử lý xong rồi mới commit** offset (hoặc `commitSync` sau mỗi lô). Nếu crash giữa chừng, bản tin được đọc lại, nên consumer phải **idempotent** (kiểm tra `messageId` đã xử lý). Commit trước khi xử lý cho ngữ nghĩa at-most-once (có thể mất bản tin) và hiếm khi hợp lý với tiền.
  - *Poison message* (lỗi giải mã, dữ liệu sai) nếu cứ ném lỗi sẽ khiến consumer kẹt mãi ở một offset. Chuẩn: retry vài lần với backoff, rồi đẩy sang **Dead Letter Topic** kèm lý do và metadata, commit để đi tiếp, và cảnh báo để người xử lý sau.
  - Phân biệt lỗi tạm thời (DB chậm: retry) với lỗi vĩnh viễn (dữ liệu sai: DLQ ngay).
  - Dùng *retry topic* theo mức trễ (1 phút, 10 phút…) để không chặn các bản tin khỏe phía sau; đổi lại mất thứ tự theo key, nên luồng cần thứ tự (cùng tài khoản) phải dùng retry chặn có giới hạn hoặc kiểm tra phiên bản trước khi áp dụng.

### Câu 51: Chọn số partition cho topic thế nào và vì sao "hot partition" nguy hiểm?
- **Trả lời**: Số partition quyết định mức song song tối đa: **một partition chỉ được một consumer trong cùng nhóm đọc**, nên số consumer hữu ích ≤ số partition. Ước lượng: partition ≥ thông lượng mục tiêu ÷ thông lượng một consumer xử lý được, cộng dư địa tăng trưởng.
  - Chỉ có thể **tăng**, không giảm số partition; khi tăng, ánh xạ `hash(key) % n` đổi nên các khóa mới có thể rơi sang partition khác, làm đảo thứ tự theo khóa. Cần tính trước.
  - *Hot partition*: một khóa chiếm tỷ trọng lớn (ví dụ tài khoản của một công ty trả lương hàng loạt) làm một partition quá tải trong khi các partition khác rảnh. Giải pháp: chọn khóa phân phối đều hơn, hoặc thêm hậu tố cho khóa nếu không cần thứ tự toàn cục.
  - Theo dõi *consumer lag* (`kafka-consumer-groups --describe`) làm chỉ báo sức khỏe quan trọng nhất.

### Câu 52: Kafka khác hàng đợi truyền thống như IBM MQ thế nào, và vì sao ngân hàng thường dùng cả hai?
- **Trả lời**: *IBM MQ/JMS* là hàng đợi: bản tin bị xóa sau khi tiêu thụ, hỗ trợ giao tiếp request/reply (`JMSCorrelationID`), bản tin bền vững, giao dịch XA, truyền **đúng một lần** giữa hai điểm; rất hợp tích hợp với Core Banking (như T24) cần độ tin cậy từng bản tin.
  - *Kafka* là **log phân vùng bền vững**: bản tin được giữ theo thời gian/dung lượng, nhiều nhóm consumer đọc độc lập và có thể **replay**, thông lượng rất cao, thứ tự trong partition. Hợp phân phối sự kiện, streaming, xây read model.
  - Vì vậy kiến trúc ngân hàng thường: lệnh nghiệp vụ đi qua MQ tới Core; sự kiện sau hạch toán đi qua Kafka tới thông báo, phân tích, đối soát.
  - Tiêu chí chọn: cần replay/nhiều bên đọc → Kafka; cần request/reply, bản tin đơn lẻ có đảm bảo giao nhận và XA → MQ.

### Câu 53: Trong ksqlDB, các loại JOIN khác nhau thế nào và điều kiện co-partitioning là gì?
- **Trả lời**: *Stream* là chuỗi sự kiện bất biến; *Table* là trạng thái mới nhất theo khóa (suy ra từ changelog).
  - *Stream–Table join*: làm giàu sự kiện (ví dụ gắn thông tin khách hàng vào giao dịch), tra bảng tại thời điểm sự kiện đến.
  - *Stream–Stream join*: bắt buộc có cửa sổ thời gian `WITHIN` (ví dụ ghép lệnh với phản hồi trong 5 phút) vì cả hai vế là vô hạn.
  - *Table–Table join*: kết quả là một bảng được cập nhật khi một trong hai vế đổi.
  - **Co-partitioning**: hai vế phải có **cùng số partition và cùng khóa phân vùng** để các bản tin cùng khóa nằm cùng task; nếu không phải repartition trước.
  - Phân biệt *push query* (đăng ký nhận kết quả liên tục) và *pull query* (hỏi trạng thái hiện tại); UDF/UDAF viết bằng Java để thêm hàm tính toán riêng.

### Câu 54: Schema Registry và tương thích Avro: thay đổi schema thế nào cho an toàn?
- **Trả lời**: Schema Registry lưu các phiên bản schema theo *subject*; mỗi bản tin chỉ mang `schema id`, nên nhỏ gọn và producer/consumer luôn biết cách giải mã.
  - **BACKWARD** (mặc định): schema mới đọc được dữ liệu cũ → nâng cấp **consumer trước**. **FORWARD**: schema cũ đọc được dữ liệu mới → nâng cấp **producer trước**. **FULL**: cả hai.
  - Thay đổi an toàn: thêm field **có giá trị mặc định**, xóa field có giá trị mặc định. Nguy hiểm: xóa/đổi tên field bắt buộc, đổi kiểu dữ liệu.
  - Đặt chế độ tương thích ở registry để CI từ chối schema phá vỡ ngay từ khi merge, thay vì để phát hiện lúc production.
  - Với tiền dùng logical type `decimal` (hoặc chuỗi), không dùng `double`.

### Câu 55: Kafka Streams quản lý trạng thái (state) thế nào để chịu lỗi?
- **Trả lời**: Các phép toán có trạng thái (aggregate, join, windowing) lưu trong *state store* cục bộ (mặc định RocksDB) để truy cập nhanh. Mọi thay đổi đồng thời được ghi vào **changelog topic** trong Kafka nên khi instance chết, instance khác dựng lại store từ changelog.
  - Dựng lại có thể lâu nên dùng `num.standby.replicas` (bản sao nóng) để chuyển nhanh khi failover.
  - Khi rebalance, các task di chuyển cùng state; dùng cooperative rebalancing để giảm gián đoạn.
  - `processing.guarantee=exactly_once_v2` cho mô hình đọc-xử lý-ghi nguyên tử trong Kafka.
  - Mẫu "chia để trị" cho sao kê (Câu 75): chia khoảng thời gian thành các phần xử lý song song rồi gộp, mỗi phần là một tác vụ độc lập có thể chạy lại.

### Câu 56: Oracle Partitioning mang lại gì? Partition Exchange hoạt động ra sao?
- **Trả lời**: Chia bảng lớn thành các partition theo *range/interval* (ngày giao dịch), *list* hay *hash*. Lợi ích: **partition pruning** (truy vấn có điều kiện ngày chỉ quét partition liên quan), bảo trì từng phần (rebuild index, nén), và xóa dữ liệu cũ bằng `DROP/TRUNCATE PARTITION` gần như tức thời thay vì `DELETE` hàng triệu dòng.
  - *Interval partitioning* tự tạo partition mới khi có dữ liệu mới.
  - **Partition Exchange**: `ALTER TABLE ... EXCHANGE PARTITION ... WITH TABLE ...` hoán đổi hai segment bằng cách đổi con trỏ trong từ điển dữ liệu, nên là thao tác siêu dữ liệu, gần như tức thời bất kể kích thước. Dùng để nạp dữ liệu lô lớn vào bảng staging rồi "gắn" vào bảng chính, hoặc lưu trữ ra ngoài.
  - Index *local* (theo partition) dễ bảo trì hơn *global*; global index có thể bị `UNUSABLE` sau thao tác partition nếu không cập nhật kèm (`UPDATE INDEXES`).

### Câu 57: Em đọc execution plan của Oracle thế nào để tìm nguyên nhân câu SQL chậm?
- **Trả lời**: Bước 1: lấy **plan thực tế**, không chỉ plan ước lượng: chạy với hint `/*+ gather_plan_statistics */` rồi `SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(format => 'ALLSTATS LAST'))`.
  - Bước 2: so sánh **E-Rows** (optimizer ước lượng) với **A-Rows** (thực tế). Lệch hàng chục lần là dấu hiệu thống kê cũ/thiếu, dữ liệu lệch phân bố hoặc điều kiện khó ước lượng.
  - Bước 3: tìm bước tốn I/O (`Buffers`, `Reads`, `A-Time`) và loại truy cập: `TABLE ACCESS FULL` có hợp lý không, `INDEX RANGE SCAN` có theo đúng cột dẫn đầu không, thứ tự và phương pháp join (Nested Loops/Hash) có hợp lý với kích thước dữ liệu không.
  - Cách xử lý: cập nhật thống kê (`DBMS_STATS`), thêm hoặc sửa index (kể cả composite), viết lại truy vấn, cố định plan tốt bằng SQL Plan Baseline. **Thêm index tạo ra chi phí ghi**, luôn đo lại sau khi đổi.

### Câu 58: Index Range Scan, Index Skip Scan và vì sao `WHERE TRUNC(ngay) = ...` làm index mất tác dụng?
- **Trả lời**: *Range scan* đi theo cây B-Tree đến khoảng khóa thỏa điều kiện. Với index composite `(a, b)`, điều kiện chỉ trên `b` thường không dùng được range scan hiệu quả; Oracle có thể dùng **Skip Scan** (coi như nhiều range scan nhỏ theo từng giá trị của `a`) nhưng chỉ hiệu quả khi `a` có **ít giá trị phân biệt**.
  - Quy tắc: đặt cột dùng điều kiện bằng và có tính chọn lọc cao ở đầu index composite, tùy truy vấn thực tế.
  - Bọc hàm lên cột đã đánh index (`TRUNC(ngay)`, `UPPER(ten)`, ép kiểu ngầm) khiến optimizer không dùng được index thường. Sửa bằng điều kiện khoảng `ngay >= :d AND ngay < :d + 1`, hoặc tạo *function-based index* đúng biểu thức.
  - *Covering index* chứa đủ cột truy vấn cần, tránh bước truy cập bảng; nhưng index càng nhiều thì INSERT/UPDATE càng chậm.

### Câu 59: Bind variable quan trọng thế nào với Oracle? Còn "bind peeking" thì sao?
- **Trả lời**: Câu lệnh có giá trị nối thẳng vào chuỗi SQL (`WHERE id = 1001`, `1002`…) khiến mỗi lần là một câu khác nhau → **hard parse** tốn CPU, tranh chấp shared pool/library cache, và mở đường **SQL injection**. Dùng bind variable (`:id`, hoặc `?` trong JDBC `PreparedStatement`) để tái dùng plan (*soft parse*) và an toàn hơn.
  - *Bind peeking*: lần phân tích đầu Oracle "nhìn" giá trị bind để chọn plan; nếu dữ liệu lệch (một giá trị chiếm 90% dòng) plan tối ưu cho giá trị này có thể rất tệ cho giá trị kia. Từ 11g có **Adaptive Cursor Sharing** tạo nhiều plan theo độ lệch.
  - Cờ `cursor_sharing=FORCE` chỉ nên là giải pháp tình thế cho code cũ; cách đúng là sửa ứng dụng dùng bind.

### Câu 60: Mức cô lập giao dịch của Oracle khác gì? Làm sao tránh "lost update"?
- **Trả lời**: Oracle mặc định **READ COMMITTED** với *đa phiên bản* dựa trên undo: mỗi câu lệnh thấy ảnh chụp dữ liệu nhất quán tại thời điểm bắt đầu câu lệnh, **người đọc không chặn người ghi** và ngược lại. Không có dirty read. Có thêm `SERIALIZABLE` (lỗi `ORA-08177: can't serialize access`) và `READ ONLY`.
  - `ORA-01555: snapshot too old`: truy vấn dài cần dữ liệu undo đã bị ghi đè; xử lý bằng undo retention đủ lớn và tối ưu truy vấn.
  - **Lost update** (hai phiên cùng đọc số dư rồi cùng ghi): dùng khóa bi quan `SELECT ... FOR UPDATE`, hoặc khóa lạc quan với cột `version` (`UPDATE ... SET version = version + 1 WHERE id = :id AND version = :v`, kiểm tra số dòng bị cập nhật phải bằng 1), hoặc cập nhật tương đối `SET balance = balance - :amt WHERE balance >= :amt`.
  - Chọn bi quan khi tranh chấp cao (số dư nóng), lạc quan khi tranh chấp thấp (sàn chuyển nhượng, Câu 69).

### Câu 61: Vì sao PL/SQL dùng `BULK COLLECT` và `FORALL`? Autonomous Transaction dùng khi nào?
- **Trả lời**: Xử lý từng dòng trong vòng lặp tạo ra rất nhiều **chuyển ngữ cảnh (context switch)** giữa engine PL/SQL và engine SQL. `BULK COLLECT INTO` lấy cả lô dòng vào mảng một lần; `FORALL` gửi cả lô DML trong một lần chuyển. Dùng mệnh đề `LIMIT 1000` để không nạp quá nhiều vào bộ nhớ, và `SAVE EXCEPTIONS` để một dòng lỗi không làm hỏng cả lô.
  - Nguyên tắc: nếu làm được bằng một câu SQL thuần theo tập hợp (set-based) thì ưu tiên hơn cả vòng lặp bulk.
  - `PRAGMA AUTONOMOUS_TRANSACTION` chạy một transaction độc lập, commit/rollback không ảnh hưởng transaction gọi. Chỉ hợp lý cho **ghi log lỗi/kiểm toán** cần giữ lại cả khi giao dịch chính rollback. Không dùng cho nghiệp vụ tiền vì làm mất tính nguyên tử và dễ tự gây deadlock với transaction cha.

### Câu 62: Oracle Sharding, In-Memory, Advanced Queuing và JSON dùng cho việc gì? (các điểm JD nhắc tới)
- **Trả lời** (mức hiểu biết, nêu rõ phạm vi kinh nghiệm thực tế khi được hỏi):
  - *Oracle Database In-Memory*: thêm **dạng cột trong bộ nhớ** bên cạnh dạng hàng, tăng tốc truy vấn phân tích/tổng hợp trên dữ liệu OLTP; không thay thế index cho truy vấn điểm.
  - *Oracle Sharding*: chia ngang dữ liệu qua nhiều database độc lập theo *sharding key* (ví dụ mã khách hàng) để mở rộng ghi và cô lập lỗi; đổi lại truy vấn xuyên shard phức tạp hơn.
  - *Advanced Queuing (AQ)*: hàng đợi bản tin **nằm trong DB**, nên có thể enqueue trong cùng transaction với thao tác dữ liệu, một dạng Outbox sẵn có.
  - *JSON*: lưu JSON trong cột (kèm ràng buộc `IS JSON`), truy xuất bằng `JSON_VALUE`, `JSON_TABLE`; hợp cho dữ liệu bán cấu trúc, không bỏ được mô hình quan hệ cho dữ liệu lõi.
  - Khi được hỏi sâu, nói thật mình đã dùng đến đâu và đã đọc/thử đến đâu.

### Câu 63: Gặp `ORA-00060: deadlock detected` ở production, em điều tra và xử lý từng bước thế nào?
- **Trả lời**:
  1. Oracle phát hiện vòng chờ, chọn một phiên làm nạn nhân và **rollback câu lệnh bị lỗi (chỉ câu lệnh, không phải cả transaction)**; ứng dụng phải bắt lỗi và rollback/retry cả giao dịch.
  2. Alert log ghi đường dẫn tới **file trace `.trc`** trong thư mục diagnostic; file có phần `Deadlock graph` với tài nguyên (`TX` khóa dòng, `TM` khóa bảng), chế độ khóa, phiên giữ và phiên chờ, kèm câu SQL và `Rows waited on`.
  3. Từ trace xác định hai giao dịch nào khóa các dòng theo thứ tự ngược nhau. Nguyên nhân thường gặp: cập nhật nhiều dòng theo **thứ tự khác nhau**, khóa bảng con do **thiếu index foreign key** (Câu 45), hoặc `SELECT FOR UPDATE` ở các bước không nhất quán.
  4. Sửa gốc: khóa dòng theo **thứ tự xác định** bằng từng câu lệnh riêng (`SELECT ... WHERE account_no = :acc FOR UPDATE` cho tài khoản nhỏ trước, lớn sau); không dựa vào `SELECT ... ORDER BY ... FOR UPDATE` vì Oracle không bảo đảm khóa dòng theo thứ tự `ORDER BY`. Kèm theo: tạo index FK, rút ngắn transaction, dùng `NOWAIT`/`WAIT n` khi phù hợp.
  5. Kiểm chứng bằng test đồng thời lặp lại và theo dõi tần suất lỗi sau khi sửa. Đừng nói "triệt tiêu 100%" nếu chưa có số liệu đo.

### Câu 64: Sinh khóa chính: Oracle SEQUENCE, UUID và Snowflake khác nhau thế nào?
- **Trả lời**:
  - *SEQUENCE*: tăng dần, nhỏ gọn; `CACHE n` giúp nhanh nhưng khi khởi động lại có thể **nhảy số (gap)**, không dùng để bảo đảm liên tục (không dùng cho số chứng từ kế toán cần liền mạch). Trên RAC cần cân nhắc `ORDER`. Chèn giá trị tăng dần dồn vào cạnh phải của index gây *hot block*; có thể dùng reverse key index hoặc hash partition.
  - *UUID v4*: ngẫu nhiên, sinh được ở bất kỳ nơi nào không cần phối hợp, nhưng chèn ngẫu nhiên làm **phân mảnh index** và lớn (16 byte). UUID v7/ULID có tiền tố thời gian nên thân thiện với index hơn.
  - *Snowflake*: số 64-bit gồm thời gian + mã máy + số thứ tự, tăng dần theo thời gian, sinh phân tán; cần quản lý mã máy và đồng hồ không chạy lùi.
  - Với **idempotency key** (do client sinh) dùng UUID; với khóa nội bộ cần hiệu năng index thì chọn khóa tăng dần theo thời gian.

### Câu 65: Thiết kế sổ cái (ledger) ghi nợ - ghi có kép để vừa đúng vừa kiểm toán được?
- **Trả lời**:
  - *Bút toán kép*: mỗi giao dịch gồm các dòng ghi nợ và ghi có có **tổng bằng nhau**; số dư là kết quả của các bút toán (hoặc bảng số dư cập nhật trong **cùng transaction** với bút toán).
  - *Chỉ thêm, không sửa* (append-only): sai sót được sửa bằng **bút toán đảo (reversal)**, không `UPDATE/DELETE` dòng cũ; lịch sử luôn truy vết được.
  - *Idempotency*: cột `request_id` có ràng buộc `UNIQUE` để một yêu cầu gửi lại không ghi hai lần.
  - Cập nhật số dư an toàn: khóa theo thứ tự tài khoản cố định hoặc `UPDATE ... WHERE balance >= :amt` kiểm tra số dòng ảnh hưởng.
  - *Đối soát*: định kỳ so tổng bút toán với số dư và với sao kê đối tác (xem Câu 70 và Câu 78); mọi chênh lệch phải có người xử lý, không "tự cân".
  - Đây là mô hình tư duy chung; nên giải thích bằng hệ thống mình thực sự đã làm thay vì tuyên bố đã tự xây ledger của ngân hàng.

---

## PHẦN 4: NGHIỆP VỤ NGÂN HÀNG, TEMENOS T24, NAPAS ISO 8583 & SAGA (CÂU 66 – 90)

### Câu 66: Mô tả luồng bản tin kỹ thuật khi khách hàng dùng ACB One chuyển khoản 247 sang ngân hàng khác qua NAPAS.
- **Trả lời**:
  1. App gọi API Gateway ACB $\to$ Gateway kiểm tra xác thực phiên/thiết bị; với giao dịch trên 10 triệu đồng hoặc làm tổng trong ngày vượt 20 triệu đồng thì bắt buộc xác thực sinh trắc học theo QĐ 2345/QĐ-NHNN.
  2. Service Chuyển tiền gọi core banking trích nợ tài khoản khách hàng (giữ trạng thái `HOLD` tiền hoặc trích nợ thành công). JD của ACB không nêu ACB dùng core nào; khi kể ví dụ, nói rõ T24 là hệ đã làm ở OCB.
  3. Adapter chuyển tiền đóng gói bản tin theo đặc tả kết nối NAPAS 247 (gốc ISO 8583, ví dụ **MTI 0200**; đặc tả hiện hành cần kiểm với tài liệu NAPAS) gửi qua TCP Socket sang NAPAS Switch.
  4. NAPAS Switch định tuyến bản tin sang Ngân hàng thụ hưởng (Beneficiary Bank).
  5. Ngân hàng thụ hưởng ghi có tiền vào tài khoản người nhận và trả bản tin **MTI 0210** với `Field 39 = 00` về NAPAS.
  6. NAPAS chuyển tiếp bản tin `0210` về Gateway ACB.
  7. Gateway ACB giải mã bản tin, cập nhật trạng thái lệnh thành `COMPLETED`, chuyển khoản hold thành trích nợ chính thức trên core banking (nếu bước 2 mới giữ hold) và bắn push notification cho khách hàng qua Kafka.

### Câu 67: Nếu gửi bản tin MTI 0200 sang NAPAS nhưng bị timeout mạng không nhận được phản hồi 0210, hệ thống phải xử lý như thế nào?
- **Trả lời**:
  1. Tuyệt đối **không được báo giao dịch thất bại và hoàn tiền ngay cho khách**, vì có thể NAPAS đã xử lý xong và tiền đã vào tài khoản người nhận.
  2. Chuyển trạng thái giao dịch sang `PENDING_RECONCILIATION / TIMEOUT`.
  3. Gửi bản tin **MTI 0420 (Reversal Advice — thông báo đảo giao dịch, theo ISO 8583:1987; 0400 mới là Reversal Request)** sang NAPAS, gửi lặp `0421` nếu chưa nhận phản hồi; hoặc truy vấn trạng thái/tra soát theo quy trình NAPAS (cơ chế cụ thể của NAPAS 247 cần kiểm với tài liệu NAPAS).
  4. Nếu NAPAS xác nhận đảo thành công (bản tin `0430` với `Field 39 = 00`) $\to$ Thực hiện hoàn tiền cho khách hàng.
  5. Nếu bản tin đảo thất bại hoặc không nhận được phản hồi $\to$ Giữ nguyên trạng thái để chạy tiến trình đối soát file EOD liên ngân hàng vào sáng hôm sau.

### Câu 68: Trong tích hợp Temenos T24 qua IBM MQ, tại sao phải dùng `JMSCorrelationID` thay vì mở kết nối đồng bộ?
- **Trả lời**: Temenos T24 xử lý giao dịch qua hàng đợi bất đồng bộ. Nếu dùng kết nối đồng bộ (HTTP Blocking hoặc MQ synchronous receive), thread Java của microservice sẽ bị treo để đợi Core phản hồi. Trong giờ cao điểm khi T24 xử lý chậm (ví dụ minh họa: vài giây/lệnh), hàng trăm thread sẽ chiếm sạch Connection Pool làm sập Microservice. Dùng `JMSCorrelationID`: Message gửi vào queue có một ID duy nhất; thread gửi xong giải phóng ngay lập tức. Khi T24 xử lý xong và đẩy vào queue OUT với đúng Correlation ID đó, một listener bất đồng bộ sẽ bắt message và hoàn tất callback.

### Câu 69: Trình bày quy trình Chuyển nhượng Sổ tiết kiệm trực tuyến (Online Deposit Contract Marketplace) trong hệ thống ngân hàng.
- **Trả lời**:
  1. Người bán tạo lệnh chuyển nhượng trên Mobile App $\to$ Dịch vụ kiểm tra hợp đồng tiết kiệm có tồn tại trên T24 và chưa có lệnh chuyển nhượng nào đang mở $\to$ Tạo lệnh ở trạng thái `ORDER`.
  2. Người mua tìm kiếm danh sách sổ chuyển nhượng qua API `recommendations` (sắp xếp theo mức chênh lệch lãi suất `amount_diff`).
  3. Người mua nhấn Mua $\to$ Hệ thống kích hoạt Khóa lạc quan (`last_access`), chuyển trạng thái sang `PROCESSING`.
  4. Dịch vụ gọi `t24DepositContractCaller.UpdateCif` thực thi 2 bản tin OFS: `ACCOUNT_T24_DEPOSIT_OFS` và `AZ_ACCOUNT_T24_OFS_AMD` để đổi thông tin CIF người sở hữu trên Core T24.
  5. Nếu T24 trả về thành công $\to$ Cập nhật trạng thái `DONE`, phát sự kiện `NOTIFICATION_WITH_DATA_REQUEST_STREAM` qua Kafka để thông báo sổ tiết kiệm mới cho người mua.
  6. Nếu T24 trả về mã lỗi nghi ngờ (Timeout mạng, Core treo, Tài khoản phong tỏa) $\to$ Chuyển trạng thái `HOLD`, kích hoạt luồng đối soát tự động, không để mất tiền người mua.

### Câu 70: Làm thế nào để đối soát tự động hàng triệu giao dịch thanh toán hóa đơn đối tác cuối ngày?
- **Trả lời**: Áp dụng mô hình **Đối soát 3 bên (Three-Way Reconciliation)**:
  - Tải file sao kê của đối tác (SFTP) và export sổ cái Core T24 vào các bảng Staging.
  - Sử dụng câu lệnh SQL `FULL OUTER JOIN` trên `(transaction_id, amount, date)`:
    ```sql
    SELECT NVL(b.trans_id, p.trans_id) AS trans_id,
           CASE 
               WHEN b.trans_id IS NOT NULL AND p.trans_id IS NOT NULL THEN 'MATCHED'
               WHEN b.trans_id IS NOT NULL AND p.trans_id IS NULL THEN 'BANK_SUCCESS_PARTNER_MISSING'
               WHEN b.trans_id IS NULL AND p.trans_id IS NOT NULL THEN 'PARTNER_SUCCESS_BANK_MISSING'
           END AS recon_status
    FROM bank_transactions b
    FULL OUTER JOIN partner_transactions p ON b.trans_id = p.trans_id AND b.amount = p.amount;
    ```
  - Tự động sinh danh sách lệch sổ và đẩy vào quy trình hoàn tiền (Refund) hoặc truy thu tự động.

### Câu 71: Tại Mirae Asset Finance (Grooo International), bạn đã xử lý bài toán Giải ngân Khoản vay Tự động (Automated Loan Disbursement) như thế nào để ngăn chặn lỗi giải ngân 2 lần?
- **Trả lời**: *(Nói rõ phần nào mình trực tiếp code, phần nào do team/đội khác làm. [chỉ giữ nếu có bằng chứng])*
  1. Bài toán: Sau khi hồ sơ vay được duyệt trên hệ thống LOS, hệ thống LMS kích hoạt lệnh giải ngân tiền qua tài khoản ngân hàng của khách hàng (hoặc ví điện tử). Nếu mạng chập chờn hoặc gateway trả về timeout, việc bấm retry có thể dẫn đến việc giải ngân tiền 2 lần (Double Disbursement), gây thất thoát tài chính không thể thu hồi.
  2. Giải pháp kỹ thuật:
     - Áp dụng **Distributed State Machine kết hợp Idempotency Key**: Mã hồ sơ vay `application_id` được dùng làm khóa duy nhất. Trước khi gọi cổng chuyển tiền, hệ thống thực thi lệnh cập nhật trạng thái trong PostgreSQL:
       ```sql
       UPDATE loan_contract SET disbursement_status = 'DISBURSING', updated_at = NOW()
       WHERE application_id = $1 AND disbursement_status = 'APPROVED';
       ```
     - Nếu `rows_affected == 0` (hồ sơ đang được giải ngân hoặc đã giải ngân rồi) $\to$ Từ chối mọi request tiếp theo ngay lập tức.
     - Sử dụng mô hình **Saga Orchestrator**: Trừ hạn mức tín dụng $\to$ Gọi cổng chuyển tiền liên ngân hàng kèm mã `transId = "DISB_" + application_id`.
     - Nếu cổng chuyển tiền timeout $\to$ Tuyệt đối không hoàn tiền hay retry, mà chuyển sang trạng thái `DISBURSEMENT_IN_DOUBT`, kích hoạt Worker tự động gọi API truy vấn trạng thái giao dịch (Query Transaction Status) sang đối tác định kỳ (1 phút, 5 phút, 15 phút). Chỉ khi đối tác xác nhận giao dịch thất bại thì mới nhả trạng thái cho phép thực hiện lại.

### Câu 72: Tại Sutrix Group, bạn đã làm việc với Adobe Experience Manager (AEM) và Java Core như thế nào? Kiến thức AEM giúp ích gì cho một Senior Backend/Integration Engineer tại Ngân hàng?
- **Trả lời**:
  1. Tại Sutrix Group, tôi trực tiếp phát triển các dự án cho khách hàng viễn thông quốc tế (Globe Telecom) trên nền tảng **Adobe Experience Manager (AEM 6.4/6.5)** kết hợp Java Core:
     - Viết các **OSGi Services / Bundles** theo kiến trúc module hóa động, nạp và cấu hình dịch vụ linh hoạt trong runtime qua Apache Felix.
     - Xây dựng **Sling Models** để bóc tách dữ liệu từ cây phân cấp JCR (Java Content Repository) và binding an toàn sang HTML qua template HTL (Sightly).
     - Phối hợp với đội hạ tầng trên môi trường AWS (EC2, S3, RDS) và tinh chỉnh bộ nhớ đệm tại tầng AEM Dispatcher (Apache HTTP Server). [chỉ giữ nếu có bằng chứng]
     - Chứng chỉ **Adobe Certified Expert - AEM Sites Developer**. [chỉ giữ nếu có bằng chứng — chứng chỉ phải tra cứu được]
  2. Giá trị chuyển giao cho vị trí Senior Backend Ngân hàng:
     - Tư duy kiến trúc đa tầng (Multi-tier Architecture): Hiểu rõ cách các kênh số (Digital Channels / CMS / Front-end) giao tiếp với hệ thống Backend Microservices phía sau thông qua API Gateway, từ đó thiết kế các API có độ trễ thấp và thân thiện với việc cache tại tầng Edge/CDN/Dispatcher.
     - Nền tảng Java Core và OSGi giúp tôi nắm vững cơ chế ClassLoader, quản lý vòng đời component, và tối ưu hóa bộ nhớ JVM từ những năm đầu sự nghiệp.

### Câu 73: Bạn có quá trình học vấn bắt đầu từ FPT Polytechnic và hiện đang học liên thông Cử nhân AI tại UIT (ĐHQG TP.HCM). Lộ trình này định hình năng lực kỹ thuật của bạn ra sao?
- **Trả lời**:
  - Giai đoạn nền tảng tại FPT Polytechnic (chuyên ngành Lập trình máy tính & thiết bị di động, 2016 – 2019) đã rèn luyện cho tôi kỹ năng lập trình thực chiến vững vàng, kỷ luật viết code sạch (Clean Code), làm chủ Java Core, cấu trúc dữ liệu và khả năng thích ứng nhanh với các framework doanh nghiệp.
  - Sau nhiều năm cọ xát với các hệ thống lớn tại Sutrix, Grooo (Mirae Asset) và OCB, tôi nhận thấy để trở thành một Kỹ sư Cấp cao (Senior/Lead) thực thụ, mình cần một nền tảng toán học hàn lâm, tư duy giải thuật tối ưu và làm chủ các công nghệ đón đầu tương lai.
  - Đó là lý do tôi quyết định học liên thông: hiện tôi **đang học Cử nhân AI tại UIT, dự kiến tốt nghiệp 11/2026** (Đại học Công nghệ Thông tin – ĐHQG TP.HCM).
  - Sự kết hợp này giúp tôi: **vừa có kinh nghiệm làm việc trên các hệ thống tích hợp Core Banking / Fintech, vừa đang bổ sung nền tảng toán học và AI** (dự án AI là dự án học tập/cá nhân tại UIT, không phải hệ thống production).

### Câu 74: Tại OCB, bạn đã làm việc với hệ thống streaming sự kiện qua ksqlDB và Notification Hub cho SMS/OTT/Email như thế nào để xử lý lưu lượng thông báo lớn?
- **Trả lời**: *(Phân biệt rõ: cụm Kafka/ksqlDB do đội Nền tảng Dữ liệu quản trị — mình phối hợp sử dụng; chỉ nhận "thiết kế" phần mình trực tiếp làm. Lưu lượng thật chỉ nêu nếu có số đo [chỉ giữ nếu có bằng chứng].)*
  1. *Luồng dữ liệu (Event Streaming)*:
     - Mọi biến động số dư từ Core T24 và SAGA Engine được đẩy vào Kafka topic `core.balance.events` theo mô hình CDC.
     - Sử dụng **ksqlDB** để thực hiện Stream-Table Join theo thời gian thực giữa luồng biến động số dư với bảng cấu hình người dùng `crm.customer.preferences`.
     - Phân luồng động: Nếu người dùng đã cài Mobile Banking App $\to$ Định tuyến sang OTT Push (tiết kiệm chi phí viễn thông). Nếu chưa cài App và số tiền $\ge$ ngưỡng cấu hình (ví dụ minh họa: 50.000đ) $\to$ Định tuyến sang SMS Brandname. Các biến động nhỏ hoặc sao kê định kỳ $\to$ Định tuyến sang Email Digest.
  2. *Notification Hub Resilience*:
     - Thiết lập Priority Queue: OTP và Cảnh báo tài khoản ưu tiên số 1 (mục tiêu thiết kế, ví dụ minh họa: < 500ms); Biến động số dư ưu tiên số 2; Thông báo quảng bá ưu tiên số 3.
     - Kiểm soát nghẽn mạng đối tác: Áp dụng Token Bucket Rate Limiter và Circuit Breaker tự động chuyển đổi giữa các cổng SMS/nhà mạng (Viettel, VinaPhone, MobiFone) khi đối tác gặp sự cố hoặc trả về mã lỗi 429/503.
     - Khử trùng lặp qua Redis Key (`noti:sent:{event_id}`) có TTL 24h, giảm thiểu việc gửi lặp tin nhắn biến động số dư (Kafka giao ít nhất một lần nên không cam kết tuyệt đối).
     - Cơ chế Dead Letter Queue (DLQ) lưu vết bản tin lỗi sau 3 lần retry exponential backoff để đội ngũ vận hành đối soát và phát lại.

### Câu 75: Trình bày kiến trúc Xử lý Sao kê Tài khoản khối lượng lớn (Statement Hub) và Chi lương theo lô (Corporate Batch Payroll) áp dụng Kafka Streams Divide-and-Conquer và Transactional Outbox.
- **Trả lời**:
  1. *Kiến trúc Sao kê Tài khoản cao tải (Statement Hub)*:
     - Thách thức: Khách hàng doanh nghiệp yêu cầu xuất sao kê hàng triệu giao dịch trong tháng. Nếu truy vấn trực tiếp vào Core T24 DB sẽ làm treo Core.
     - Giải pháp: Xây dựng đường ống đồng bộ CDC từ Core sang cơ sở dữ liệu read-only phân tán. Sử dụng **Kafka Streams theo mẫu thiết kế Divide-and-Conquer (`kstream-statement-divide-conquer`)**: Chia nhỏ khoảng thời gian truy vấn thành các phân đoạn (chunks) song song, xử lý trên nhiều Kafka partitions và tổng hợp kết quả (aggregation) để sinh file sao kê định dạng PDF/Excel trả về client (thời gian thực tế phải đo, không hứa trước).
  2. *Kiến trúc Chi lương theo lô Doanh nghiệp (Batch Payroll Transfer Engine)*:
     - Áp dụng **Transactional Outbox Pattern**: Lệnh chi lương 10,000 nhân viên được lưu vào bảng `batch_trans_details` và bảng Outbox trong cùng một transaction cơ sở dữ liệu.
     - Debezium CDC bắt các bản ghi và đẩy vào Kafka topic `po.batch.transfer`.
     - Router Worker phân loại luồng: Tài khoản nội bộ đi thẳng vào Core T24 adapter; tài khoản liên ngân hàng đi qua Cổng chuyển mạch NAPAS (247 hoặc kênh xử lý theo lô, tùy sản phẩm).
     - Cơ chế Idempotent Worker và Batch Completion Consumer đối soát trạng thái từng lệnh, cập nhật tiến độ theo thời gian thực về Dashboard doanh nghiệp.

### Câu 76: Nếu ACB tiến hành liên hệ tham chiếu (Reference Check) với anh Phan Anh Tuấn (Phó phòng Ứng dụng Tích Hợp tại OCB - sếp trực tiếp) và anh Quan Quốc Bảo (Giám đốc Quản lý Ứng dụng tại ACB - người quen qua mạng lưới chuyên môn), họ sẽ nhận xét như thế nào về chuyên môn và thái độ làm việc của bạn?
- **Trả lời**: *(Nguyên tắc: ứng viên chỉ nói mình đã xin phép người tham chiếu; không bao giờ nói thay họ sẽ nhận xét gì.)*
  - **Với anh Phan Anh Tuấn (Phó phòng Ứng dụng Tích Hợp tại OCB - Quản lý trực tiếp / Sếp của tôi)**:
    - Tôi đã xin phép anh Tuấn (quản lý trực tiếp của tôi tại OCB) làm người tham chiếu. Anh có thể xác nhận vai trò và phạm vi công việc thực tế của tôi trong Squad Lending. Tôi không suy đoán thay anh về nội dung nhận xét.
    - Về phần việc của mình, tôi chỉ tự trình bày những gì tôi trực tiếp làm, và tách riêng phần phối hợp với các đội hạ tầng dùng chung (Core T24 qua IBM MQ, NAPAS 247, cụm Kafka/ksqlDB). Việc đánh giá là của người tham chiếu.
  - **Với anh Quan Quốc Bảo**:
    - [Chỉ nêu nếu anh Bảo đã đồng ý làm người tham chiếu.] Tôi đã xin phép anh Bảo; anh biết tôi qua trao đổi chuyên môn, không phải qua quan hệ công việc trực tiếp. Tôi không suy đoán nội dung anh sẽ nhận xét.

### Câu 77: Trình bày kiến trúc Hệ thống Thu hộ Tự động qua Tài khoản Định danh (Virtual Account - VA) và cơ chế Webhook Idempotency khi đối tác gửi yêu cầu gạch nợ.
- **Trả lời**:
  1. *Nguyên lý Tài khoản Định danh (Virtual Account)*:
     - Khách hàng doanh nghiệp (ví dụ: sàn thương mại điện tử, ví điện tử, công ty bảo hiểm) được cấp một dải đầu số VA (ví dụ: `8888 + mã_khách_hàng`). Khi người tiêu dùng chuyển tiền 24/7 từ bất kỳ ngân hàng nào vào số VA này qua NAPAS, cổng NAPAS sẽ gửi bản tin ghi có về ACB (ví dụ MTI 0200 theo đặc tả gốc ISO 8583; cần kiểm với tài liệu NAPAS).
     - Cổng VA phân tích tiền tố (Prefix) để ánh xạ: `VA Number` $\to$ `Master Account` (Tài khoản thực của Doanh nghiệp) + `Partner Identifier`.
     - Core T24 thực hiện ghi Có vào Tài khoản thực của Doanh nghiệp theo thời gian thực.
  2. *Cơ chế Bắn Webhook Gạch nợ Tức thời & Idempotency*:
     - Ngay khi Core ghi Có thành công, sự kiện được đẩy vào Kafka topic `va.credit.success`.
     - Microservice Webhook Dispatcher bọc payload kèm chữ ký số HMAC-SHA256 (hoặc chữ ký RSA Private Key của ACB) và header `X-ACB-Event-ID`.
     - Phía đối tác xác thực chữ ký và kiểm tra `Event-ID`. Nếu đã nhận rồi $\to$ Trả về ngay `200 OK` (chống gạch nợ 2 lần).
     - Nếu đối tác trả về `5xx` hoặc timeout $\to$ Hệ thống kích hoạt cơ chế Retry theo thuật toán Exponential Backoff kết hợp Dead Letter Queue (DLQ) để đối soát EOD.

### Câu 78: Trình bày quy trình và giải thuật Đối soát 3 Bên Cuối ngày (End-of-Day 3-Way Reconciliation: Core Banking vs Cổng NAPAS vs Đối tác Doanh nghiệp). Làm thế nào đối soát hàng triệu giao dịch trong thời gian ngắn?
- **Trả lời**:
  1. *Quy trình Đối soát 3 Bên*:
     - **File 1 (Core Ledger)**: Danh sách giao dịch ghi Có/Nợ thực tế trong ngày từ Core T24.
     - **File 2 (NAPAS Clearing File)**: File thanh quyết toán điện tử do NAPAS gửi theo lịch quy định (giờ cụ thể cần kiểm với tài liệu NAPAS).
     - **File 3 (Partner Transaction Log)**: File sao kê giao dịch từ hệ thống ERP của đối tác thu hộ.
     - **Xử lý 4 kịch bản sai lệch (Discrepancy Matrix)**:
       - *Kịch bản 1 (Cả 3 bên đều có và khớp số tiền)*: Giao dịch thành công hoàn hảo (Matched).
       - *Kịch bản 2 (Core có, NAPAS có, Đối tác không có)*: Đối tác bị rớt webhook $\to$ Kích hoạt API đồng bộ tự động gạch nợ bù cho đối tác.
       - *Kịch bản 3 (Core có, NAPAS không có)*: Lỗi nội bộ $\to$ Treo tiền vào tài khoản chờ xử lý và chuyển đội Vận hành tra soát hoàn tiền (Reversal).
       - *Kịch bản 4 (NAPAS có, Core không có)*: Lệnh thanh toán NAPAS thành công nhưng ghi Có Core bị timeout $\to$ Kiểm tra lại sổ cái Core theo mã tham chiếu, rồi sinh giao dịch ghi Có bổ sung cho khách hàng (có bước kiểm soát/duyệt).
  2. *Tối ưu hóa Thuật toán Đối soát*:
     - Không dùng lặp lồng $O(N \times M)$ hoặc câu lệnh `JOIN` trực tiếp trên bảng DB hàng chục triệu dòng.
     - Sử dụng giải thuật **Two-Pointer trên tập dữ liệu đã sắp xếp (Sorted Two-Pointer Merge)**: Sắp xếp các tập giao dịch theo `transaction_reference_id` ($O(N \log N)$), sau đó dùng 2 hoặc 3 con trỏ chạy tịnh tiến song song một lượt duy nhất ($O(N)$). Thời gian thực tế phụ thuộc phần cứng và khối lượng, phải đo; không nêu con số nếu không có số đo.

### Câu 79: Khi tích hợp xác thực sinh trắc học theo Quyết định 2345/QĐ-NHNN, làm sao xử lý sự cố sập kết nối mTLS sang hệ thống xác thực của Bộ Công an (C06/VNeID) mà không làm tắc nghẽn giao dịch?
- **Trả lời**:
  1. *Hiểu đúng luồng chính*: Theo QĐ 2345, ngân hàng so khớp sinh trắc học của khách với dữ liệu đã thu thập và kiểm tra khớp với chip CCCD (hoặc qua VNeID) lúc đăng ký. Vì vậy mỗi giao dịch thường so khớp với mẫu đã lưu tại ngân hàng; kết nối C06 chủ yếu cần ở bước đăng ký/đối chiếu.
  2. *Thiết kế Fallback & Circuit Breaker cho bước đăng ký*:
     - Tích hợp Circuit Breaker (Resilience4j) với ngưỡng timeout và tỷ lệ lỗi cấu hình được (ví dụ minh họa: 2000ms, 50% lỗi trong 10 giây) $\to$ Chuyển sang `OPEN`, cho khách đăng ký lại sau, không chặn các giao dịch đã có mẫu hợp lệ.
  3. *Quy trình Dự phòng*:
     - Khách đã đăng ký sinh trắc học: so khớp 1:1 với mẫu đã lưu (mã hóa, khóa quản lý bằng HSM) — luồng này không phụ thuộc C06.
     - Khách chưa đăng ký sinh trắc học: không được chuyển trên 10 triệu/lần hoặc làm tổng trong ngày vượt 20 triệu cho đến khi đăng ký (NFC trên app hoặc tại quầy). **Không hướng dẫn khách chia nhỏ giao dịch để lách ngưỡng.**

### Câu 80: Giải thích cơ chế bảo mật khóa phần cứng HSM (Hardware Security Module) trong giao dịch thẻ và thanh toán liên ngân hàng: Master Key (ZMK), Zone PIN Key (ZPK) và PIN Translation.
- **Trả lời**:
  - Mã PIN của khách hàng là dữ liệu tối mật cấp 1, **tuyệt đối không bao giờ được xuất hiện dưới dạng văn bản rõ (Clear Text) trong bộ nhớ RAM của máy chủ ứng dụng**.
  - *Zone Master Key (ZMK)*: Khóa trao đổi mã hóa giữa 2 trung tâm dữ liệu (ví dụ giữa ACB và NAPAS), được chia thành các thành phần (Key Components) do hai người độc lập giữ và nạp trực tiếp vào HSM.
  - *Zone PIN Key (ZPK)*: Khóa dùng để mã hóa khối mã PIN (PIN Block) trên đường truyền liên ngân hàng, được trao đổi và thay định kỳ dưới sự bảo vệ của ZMK. ZMK là khóa mã hóa khóa (key-encrypting key), không dùng để mã hóa PIN.
  - *Cơ chế PIN Translation tại HSM*:
    - Khi tin nhắn thanh toán từ ATM/POS gửi về, khối PIN Block được mã hóa bằng khóa nội bộ của thiết bị (Terminal PIN Key - TPK).
    - API Gateway chuyển gói tin vào thiết bị HSM.
    - HSM dịch mã (translate) PIN Block từ TPK sang ZPK của NAPAS (lệnh payShield `CA`; ZPK→ZPK là `CC`; kiểm tra PIN dưới LMK dùng `JC` cho TPK, `JE` cho ZPK) **ngay trong phần cứng chống can thiệp vật lý (Tamper-resistant Hardware)**; PIN rõ không bao giờ ra khỏi HSM.
    - Bản tin bọc PIN Block mới được gửi sang NAPAS. Cơ chế này giảm mạnh nguy cơ rò rỉ mã PIN ngay cả khi máy chủ ứng dụng bị xâm nhập.

### Câu 81: Tại OCB, bạn tham gia Squad Lending và trực tiếp tích hợp hệ thống Cổng Thông tin Tín dụng Quốc gia (CIC) như thế nào? Quy trình tra cứu tự động, phân loại nhóm nợ và giải ngân hạn mức diễn ra ra sao?
- **Trả lời**:
  1. *Kiến trúc Tích hợp Cổng CIC B2B API*:
     - Tại OCB, trong Squad Lending tôi trực tiếp làm phần tích hợp giữa Hệ thống Khởi tạo Khoản vay (LOS) với Trung tâm Thông tin Tín dụng Quốc gia (CIC - Ngân hàng Nhà nước); kênh kết nối và hạ tầng bảo mật do đội hạ tầng quản lý. [chỉ giữ nếu có bằng chứng]
     - Thiết lập kết nối qua đường truyền kênh thuê riêng VPN Site-to-Site, bảo mật hai chiều bằng mTLS và ký số điện tử bản tin theo chuẩn bảo mật NHNN.
     - Khi khách hàng nộp hồ sơ vay vốn, mở thẻ tín dụng hoặc thấu chi, LOS tự động đẩy lệnh tra cứu sang Kafka topic `lending.cic.request`.
  2. *Bóc tách dữ liệu & Phân loại Nhóm nợ*:
     - Worker tiêu thụ bản tin, gọi sang B2B API của CIC để tải dữ liệu lịch sử tín dụng (khoảng thời gian theo sản phẩm báo cáo CIC đã đăng ký).
     - Tự động bóc tách 5 nhóm nợ theo Thông tư 31/2024/TT-NHNN (thay Thông tư 11/2021):
       - *Nhóm 1 (Nợ đủ tiêu chuẩn)*: Quá hạn dưới 10 ngày.
       - *Nhóm 2 (Nợ cần chú ý)*: Quá hạn từ 10 đến 90 ngày.
       - *Nhóm 3 (91–180 ngày), Nhóm 4 (181–360 ngày), Nhóm 5 (trên 360 ngày)*: Nợ xấu (nguồn thứ cấp: cafef.vn 21/07/2026, hethongphapluat.com, truy cập 2026-11-10, chưa đối chiếu được nguyên văn Điều 10). Nợ cơ cấu lại được phân nhóm theo quy định riêng, không mặc nhiên là nợ xấu.
     - Đẩy các chỉ số (Tổng dư nợ tín chấp/thế chấp, số lượng TCTD đang có quan hệ, điểm xếp hạng tín dụng CIC) vào Credit Decision Engine để tự động tính toán hạn mức phê duyệt (Underwriting Approval). Ví dụ quy tắc chính sách (minh họa): nếu có nợ nhóm 2 trở lên trong 12 tháng gần nhất $\to$ dừng phê duyệt tự động và chuyển thẩm định thủ công hoặc từ chối theo chính sách tín dụng.
  3. *Quy trình Giải ngân Tự động Idempotent*:
     - Sau khi khách hàng ký hợp đồng điện tử qua OTP/FaceID, hệ thống điều phối phát bản tin tạo khế ước vay trên Core Banking Temenos T24 (phân hệ Arrangement & Lending) và gọi Cổng NAPAS 247 chuyển tiền sang tài khoản người thụ hưởng.
     - Áp dụng khóa phân tán Redis Mutex (`disbursement:lock:{application_id}`) với TTL (ví dụ minh họa: 300 giây), kết hợp ràng buộc trạng thái trong DB, idempotency key và cơ chế bù trừ SAGA để ngăn giải ngân trùng khi gặp timeout mạng.

### Câu 82: Trong Squad Lending tại OCB, khi xử lý bài toán thu hồi nợ tự động (Auto-Debit & Collection) vào ngày đến hạn thanh toán, hệ thống thiết kế cơ chế quét số dư CASA, trích nợ từng phần (Partial Debit), và đồng bộ trạng thái hợp đồng vay trên T24 như thế nào?
- **Trả lời**:
  1. *Lập lịch quét theo lô phân đoạn (Chunked Batch Scheduler)*:
     - Hàng ngày vào các mốc giờ cấu hình (ví dụ minh họa: 06:00, 12:00, 18:00), hệ thống LMS (Loan Management System) tự động quét danh sách các hợp đồng vay đến hạn thanh toán trong ngày hoặc đang quá hạn.
     - Phân bổ danh sách nợ thành các Batch nhỏ (500 – 1,000 hợp đồng/lô) đẩy vào Kafka topic `lending.collection.batch` để các worker xử lý song song, tránh việc quét toàn bảng làm quá tải database Core T24.
  2. *Cơ chế Trích nợ từng phần (Partial Debit)*:
     - Worker truy vấn số dư khả dụng trên tài khoản CASA của khách hàng.
     - Nếu số dư $\ge$ nghĩa vụ thanh toán kỳ này (Gốc + Lãi + Phí): Phát lệnh trích nợ đủ 100%, hạch toán bản tin OFS sang Core T24 ghi Có vào hợp đồng vay, cập nhật trạng thái kỳ trả nợ sang `PAID`.
     - Nếu số dư không đủ: Áp dụng cơ chế *Partial Debit* — trích toàn bộ số dư khả dụng hiện có (thứ tự thu gốc/lãi theo thỏa thuận trong hợp đồng và quy định cho vay của NHNN; thứ tự cụ thể cần kiểm theo chính sách ngân hàng), ghi nhận số tiền còn thiếu vào bảng theo dõi dư nợ quá hạn và kích hoạt lịch quét lại vào khung giờ tiếp theo. Lưu ý: phần còn thiếu vẫn bị tính ngày quá hạn để phân nhóm nợ.
  3. *Xử lý chuyển nhóm nợ tự động (Debt Reclassification)*:
     - Nếu sau 23:59 của ngày đến hạn mà khoản vay vẫn chưa được thanh toán đủ, hệ thống chuyển sang tính số ngày quá hạn (Days Past Due - DPD).
     - Khi DPD vượt qua các mốc 10 ngày (chuyển sang Nhóm 2), 90 ngày (chuyển sang Nhóm 3 - Nợ xấu) theo Thông tư 31/2024/TT-NHNN, hệ thống tự động sinh bản tin điều chỉnh nhóm nợ trên T24, đồng thời gửi bản tin báo cáo biến động dư nợ sang Cổng CIC quốc gia theo định kỳ quy định.

### Câu 83: Phân tích kiến trúc kỹ thuật sản phẩm Thấu chi Cầm cố Sổ tiết kiệm (Term Deposit Overdraft) và Thấu chi Lương tín chấp (Payroll Overdraft) mà bạn trực tiếp tích hợp trong Squad Lending. Làm sao bảo đảm tính toàn vẹn số dư và tự động giải chấp trên Core T24?
- **Trả lời**: *(Mọi tỷ lệ, lãi suất, thời gian dưới đây là ví dụ minh họa; số thật theo chính sách ngân hàng.)*
  1. *Thấu chi Cầm cố Sổ tiết kiệm (Deposit Overdraft / Collateral Pledge)*:
     - *Bản chất*: Khách hàng dùng số dư tiền gửi có kỳ hạn (Term Deposit T24) làm tài sản bảo đảm để vay thấu chi tức thời vào tài khoản thanh toán CASA với hạn mức theo tỷ lệ LTV do chính sách ngân hàng quy định mà không phải tất toán sổ trước hạn.
     - *Cơ chế 2 pha trên Core T24*:
       - Pha 1 (Phong tỏa tài sản): Microservice phát bản tin OFS sang hàng đợi sự kiện phong tỏa tiền gửi (`collateral-hold-events`) để khóa số tiền bảo đảm trên sổ tiết kiệm, không cho phép khách hàng rút tiền tiết kiệm khi đang có dư nợ thấu chi.
       - Pha 2 (Cấp hạn mức): Gọi service hạn mức Core T24 thiết lập hạn mức thấu chi trên tài khoản CASA.
     - *Tính lãi Spread* (số liệu minh họa): Lãi suất thấu chi $=$ Lãi suất tiền gửi $+$ 2.5%/năm. Hệ thống chỉ tính lãi trên số dư âm thực tế của CASA theo phương pháp tích lũy ngày.
     - *Tự động giải chấp*: Khi khách hàng tất toán dư nợ thấu chi hoặc khi sổ tiết kiệm đáo hạn, hệ thống kích hoạt SAGA để tự động cấn trừ nợ và phát lệnh gỡ bỏ phong tỏa (`Unlock Event`), giải phóng số dư còn lại về CASA.
  2. *Thấu chi Lương Tín chấp (Unsecured Payroll Overdraft)*:
     - Tích hợp với hệ thống chi lương doanh nghiệp theo lô: Thuật toán tự động phân tích dòng tiền nhận lương vài tháng gần nhất để cấp hạn mức thấu chi tín chấp theo bội số lương (ví dụ minh họa: 2–3 lần) theo danh sách whitelist phê duyệt trước.
  3. *Ký số Hợp đồng Tín dụng Đám mây (Cloud CA E-Sign)*:
     - Tích hợp cổng ký số từ xa của nhà cung cấp dịch vụ chứng thực chữ ký số (theo Luật Giao dịch điện tử 2023 và Nghị định 23/2025/NĐ-CP), kết hợp xác thực khuôn mặt và OTP theo chính sách xác thực người ký của ngân hàng, giúp khách hàng ký hợp đồng tín dụng điện tử mà không cần token USB hay đến quầy giao dịch.

### Câu 84: Phân tích kiến trúc sản phẩm Vay trên Hạn mức Thẻ Tín dụng (Loan on Credit Card / Line of Credit - LoC) và Mở thẻ ảo tức thì. Làm sao tích hợp giữa OMNI-BFF, Card Management System (CMS) và Core T24 để quản lý hạn mức, tính toán phương án trả góp và phòng chống rủi ro?
- **Trả lời**:
  1. *Bản chất nghiệp vụ*: Cho phép chủ thẻ tín dụng hiện hữu chuyển đổi hạn mức thẻ khả dụng thành tiền mặt giải ngân trực tiếp vào tài khoản CASA trả góp theo kỳ hạn (3, 6, 12, 24 tháng), hoặc phát hành thẻ tín dụng ảo (Virtual Credit Card) gần như tức thời để chi tiêu online.
  2. *Quy trình Tích hợp Kỹ thuật trên OMNI-BFF (Retail Lending Integration Gateway)*:
     - *Mô phỏng trả nợ*: Khách hàng chọn số tiền vay và kỳ hạn. Hệ thống truy vấn ma trận lãi suất và biểu phí chuyển đổi để tính toán lịch trả nợ gốc lãi hàng tháng theo phương pháp dư nợ giảm dần.
     - *Thẩm định hạn mức*: Gọi dịch vụ thẻ và CMS để kiểm tra trạng thái thẻ (thẻ đang hoạt động, không bị khóa, không quá hạn), kiểm tra hạn mức khả dụng $\ge$ số tiền đăng ký vay.
     - *Đăng ký & Ký hợp đồng điện tử*: Khách hàng xác nhận qua xác thực khuôn mặt và OTP theo chính sách ngân hàng. Tạo bản ghi hợp đồng vay trên thẻ.
     - *Phong tỏa hạn mức thẻ & Hạch toán*: Gọi CMS phong tỏa số tiền tương ứng trên thẻ tín dụng (Block Card Limit) để đảm bảo khách hàng không quẹt thẻ vượt trần. Đồng thời phát lệnh giải ngân ghi Có vào tài khoản CASA trên Core T24.
  3. *Mở thẻ ảo tức thì*:
     - Tích hợp Loan Origination System (LOS) Adapter: Tự động khởi tạo hồ sơ phát hành thẻ ảo, đồng bộ thông tin CIF sang hệ thống CMS; CMS cấp số thẻ ảo (PAN) và ngày hết hạn, HSM tính mã CVV2 từ khóa CVK.

### Câu 85: Cơ chế Cầm cố Sổ tiết kiệm Đồng sở hữu / Bên thứ ba bảo lãnh (Pledge Savings with Related Parties) và Xử lý Tất toán trước hạn (Early Settlement Overdraft) trong hệ thống Tích hợp Tín dụng. Làm sao bảo đảm tính pháp lý và toàn vẹn dữ liệu?
- **Trả lời**:
  1. *Cầm cố Sổ tiết kiệm có Bên liên quan / Đồng sở hữu*:
     - *Thực tế ngân hàng*: Sổ tiết kiệm có thể đứng tên đồng sở hữu (hai vợ chồng) hoặc khách hàng vay vốn được bảo đảm bằng sổ tiết kiệm của bên thứ ba (ví dụ bố mẹ).
     - *Kiến trúc dữ liệu*: Quản lý qua các bảng dữ liệu đăng ký tài sản bảo đảm (cầm cố), chi tiết tài sản tiền gửi và các bên liên quan.
     - *Luồng ký số tuần tự (Multi-Party Sequential E-Signing)*: Hệ thống không cho phép giải ngân ngay sau khi người vay ký. Microservice khởi tạo phiên ký số đám mây cho từng đồng chủ sở hữu/người bảo lãnh. Mỗi bên liên quan nhận thông báo OTT/SMS, đăng nhập OMNI App, xác thực khuôn mặt theo chính sách xác thực người ký và ký số Cloud CA đồng thuận cầm cố tài sản. Chỉ khi 100% bên liên quan hoàn tất ký số, hệ thống mới phát lệnh phong tỏa sổ trên T24 và mở hạn mức thấu chi.
  2. *Xử lý Tất toán trước hạn (Early Settlement Overdraft)*:
     - Khách hàng có thể chủ động tất toán dư nợ thấu chi trước hạn bất kỳ lúc nào trên ứng dụng ngân hàng số.
     - Hệ thống tính toán chính xác số ngày sử dụng thực tế, lãi tích lũy đến ngày hiện tại, và phí trả nợ trước hạn (nếu có).
     - Khi trích nợ tất toán thành công từ CASA, hệ thống gọi quy trình đổi hướng đáo hạn và giải chấp trên Core T24, giải tỏa phong tỏa toàn bộ số dư sổ tiết kiệm về trạng thái bình thường.

### Câu 86: Thiết kế và vận hành Cổng Ký số Hợp đồng Tín dụng Đám mây (Cloud CA) tích hợp Sinh trắc học Quyết định 2345/QĐ-NHNN và Kho lưu trữ Văn bản Số Doanh nghiệp (ECM). Làm sao bảo đảm tính toàn vẹn, chống chối bỏ (Non-repudiation) và đạt SLA thời gian ký?
- **Trả lời**:
  1. *Kiến trúc Tích hợp Ký số Từ xa (Remote Signing Architecture)*:
     - Khách hàng không cần dùng USB Token vật lý. Khi hồ sơ vay được duyệt, Retail Lending Integration Gateway gọi cổng ký số Cloud CA để tạo yêu cầu cấp chứng thư số cá nhân theo chuẩn chữ ký số công cộng.
     - Sinh file PDF hợp đồng tín dụng chuẩn hóa từ template, nhúng các trường siêu dữ liệu (Metadata) và vị trí con dấu số (Signature Placeholder).
  2. *Bảo mật kép và căn cứ pháp lý*:
     - Căn cứ: Luật Giao dịch điện tử 2023 và Nghị định 23/2025/NĐ-CP về chữ ký điện tử và dịch vụ tin cậy (thay Nghị định 130/2018, hiệu lực 10/04/2025). QĐ 2345/QĐ-NHNN điều chỉnh giao dịch thanh toán trực tuyến, không phải căn cứ cho việc ký hợp đồng.
     - Hệ thống xác thực người ký bằng Face Match với dữ liệu sinh trắc học đã đăng ký (đã đối chiếu chip CCCD) và Liveness Detection, theo chính sách ngân hàng.
     - Sau đó hệ thống gửi OTP để khách ủy quyền ký. Khóa bí mật trong HSM của nhà cung cấp dịch vụ ký số từ xa được kích hoạt để ký hợp đồng; dấu thời gian do dịch vụ cấp dấu thời gian (TSA) cấp, không phải do OTP. [chuẩn dấu thời gian cụ thể: chỉ giữ nếu có bằng chứng]
  3. *Đồng bộ lưu trữ kho ECM*:
     - Hợp đồng PDF đã ký số hoàn chỉnh được tự động đẩy vào Hệ thống Quản trị Tài liệu Doanh nghiệp số (ECM), sinh mã định danh tài liệu duy nhất và mã hash SHA-256 để kiểm toán nội bộ và tra cứu lịch sử phục vụ thanh tra NHNN.

### Câu 87: Với quy mô là một OMNI-BFF kết nối tới nhiều APIC endpoint và microservice nghiệp vụ (số lượng cụ thể chỉ nêu nếu có nguồn), làm thế nào dịch vụ Retail Lending Integration Gateway duy trì tính sẵn sàng cao (High Availability), kiểm soát lỗi phân tán (Fault Tolerance) và chống tràn bộ nhớ/nghẽn luồng (Thread Starvation)?
- **Trả lời**:
  1. *Mô hình I/O Bất đồng bộ & Non-blocking*:
     - Triển khai trên nền tảng Java Spring WebFlux / Vert.x kết hợp Netty event loop, giúp mỗi worker xử lý hàng nghìn kết nối đồng thời với lượng RAM tối thiểu, không bị giới hạn bởi số lượng OS Thread truyền thống.
  2. *Kiểm soát Lỗi bằng Resilience4j Circuit Breaker & Bulkhead*:
     - Mỗi kết nối downstream (Core T24, CIC, Cards, Cổng Ký số Đám mây Cloud CA) được cô lập bằng một Bulkhead riêng biệt để sự cố chậm phản hồi của một bên thứ ba không làm cạn kiệt Connection Pool của toàn bộ service.
     - Cấu hình Circuit Breaker với ngưỡng trượt (Sliding Window; ví dụ minh họa): Nếu tỷ lệ lỗi gọi CIC hoặc Cổng Ký số Cloud CA vượt quá 50% trong 20 request gần nhất, Circuit Breaker tự động bật trạng thái `OPEN`, lập tức trả về phản hồi fallback thân thiện cho khách hàng (ví dụ: lưu trạng thái hồ sơ sang dạng nháp Draft để hệ thống tự động retry sau qua Kafka), bảo vệ Gateway không bị nghẽn 504 Gateway Timeout.
  3. *Thiết lập Ma trận Timeout Phân tầng (ví dụ minh họa, số thật theo cấu hình hệ thống)*:
     - Dịch vụ nội bộ ngân hàng (Core T24, CASA, CMS Thẻ): Timeout nghiêm ngặt $\le 3,000$ms.
     - Dịch vụ đối tác ngoại vi (Cổng CIC NHNN, Cổng Ký số Cloud CA): Timeout $\le 8,000$ms kết hợp cơ chế Callback Webhook bất đồng bộ.
  4. *Distributed Tracing toàn diện qua OpenTelemetry*:
     - Truyền `X-Correlation-ID` và `X-Trace-ID` xuyên suốt qua toàn bộ các APIC endpoint và lời gọi microservice. Log được đẩy tập trung vào cụm Elasticsearch/Kibana, giúp kỹ sư phát hiện tức thời vị trí trễ cổ chai trong luồng duyệt vay số.

### Câu 88: Quy trình Xác nhận Khoản vay Trực tuyến (Online Loan Confirmation) và Bộ động cơ Quản lý Lý do Từ chối (Rejection Reasons Engine) trong Squad Lending được xây dựng ra sao?
- **Trả lời**:
  1. *Hệ quản trị xác nhận khoản vay (`loan-confirmation`)*:
     - Dữ liệu quản lý qua các bảng `loan_confirmation_online`, `loans_confirmation`, `rejection_reason_config` và `reject_reason` trên database `lending_integration` (truy xuất qua `LoanConfirmationOnlineRepository` và `LoansConfirmationRepository`).
     - Cho phép khách hàng tra cứu chi tiết đề nghị vay (`/loan-confirmation/get-detail`), lịch sử các lần xác nhận (`/loan-confirmation/get-histories`), và dư nợ chờ xác thực (`/loan-confirmation/get-outstanding`).
  2. *Bộ phân loại lý do từ chối tự động (Auto-Rejection Engine)*:
     - Khi một hồ sơ vay hoặc thấu chi không đạt tiêu chuẩn (do DTI vượt ngưỡng, nợ CIC nhóm 2, tài sản bảo đảm bị phong tỏa bởi tòa án, hoặc chữ ký số không hợp lệ), hệ thống gọi `/loan-confirmation/get-reject-reasons` và `/loan-confirmation/send-rejection`.
     - Phân loại mã lý do chuẩn hóa (ví dụ: `REJ_CIC_BAD_DEBT`, `REJ_DTI_OVER_LIMIT`, `REJ_INSUFFICIENT_INCOME`), lưu log kiểm toán vào `loc_eligible_log` và gửi thông báo đa kênh (OTT Push, SMS Brandname qua `mcs-notification`) với nội dung hướng dẫn khách hàng cải thiện hồ sơ mà không để lộ các thông số bảo mật nhạy cảm.

### Câu 89: Cơ chế Tính toán DTI (Debt-to-Income), LTV (Loan-to-Value) và Đánh giá Khả năng Trả nợ Tự động trong Squad Lending được vận hành như thế nào?
- **Trả lời**:
  1. *Thu thập và chuẩn hóa dữ liệu thu nhập (`/loan/income`)*:
     - Tích hợp `IncomeRepository` và phân hệ chi lương doanh nghiệp `chi lương doanh nghiệp theo lô (Corporate Batch Payroll Gateway)`. Trích xuất dòng tiền thực nhận (Net Income) định kỳ 3–6 tháng gần nhất của CIF.
  2. *Tính toán chỉ số DTI (Debt-to-Income Ratio)*:
     - Công thức: $\text{DTI} = \frac{\sum \text{Nghĩa vụ trả nợ hàng tháng}}{\text{Tổng thu nhập ròng hàng tháng}} \times 100\%$.
     - Nghĩa vụ trả nợ bao gồm: Khoản trả nợ tại OCB + Tất cả các khoản trả góp/thẻ tín dụng tại các TCTD khác được bóc tách từ báo cáo CIC (mã sản phẩm báo cáo cụ thể: chỉ giữ nếu có bằng chứng).
     - Quy tắc phê duyệt (ví dụ minh họa; ngưỡng thật theo chính sách từng ngân hàng): khống chế $\text{DTI} \le 45\%$ đối với thấu chi tín chấp. Nếu vượt ngưỡng $45\%$, hệ thống tự động giảm hạn mức đề xuất hoặc từ chối phê duyệt thẳng.
  3. *Tính toán chỉ số LTV (Loan-to-Value Ratio) cho Sổ tiết kiệm*:
     - Công thức: $\text{LTV} = \frac{\text{Hạn mức thấu chi đề xuất}}{\text{Số dư gốc sổ tiết kiệm}} \times 100\%$.
     - Khống chế trần (ví dụ minh họa, tỷ lệ thật theo chính sách ngân hàng): Đối với sổ tiết kiệm VND, LTV tối đa ví dụ $85\% \text{--} 90\%$. Khoảng đệm $10\% \text{--} 15\%$ nhằm dự phòng cho rủi ro phát sinh lãi vay thấu chi tích lũy nếu khách hàng không thanh toán lãi đúng hạn.

### Câu 90: Kiến trúc Máy trạng thái Hợp đồng Vay (Loan Lifecycle State Machine) và Cơ chế Bù trừ SAGA phân tán trong Squad Lending được triển khai ra sao?
- **Trả lời**:
  1. *Máy trạng thái tuần tự khép kín (Finite State Machine - FSM)*:
     - Trạng thái hợp đồng vay/thấu chi được kiểm soát nghiêm ngặt theo chuỗi:
       $$\text{INITIATED} \to \text{ELIGIBILITY\_CHECKED} \to \text{CIC\_CLEARED} \to \text{COLLATERAL\_LOCKED} \to \text{CONTRACT\_SIGNED} \to \text{LIMIT\_GRANTED} \to \text{DISBURSED} \to \text{ACTIVE} \to \text{SETTLED}$$
     - Mọi bước chuyển trạng thái (State Transition) đều được ghi nhận có dấu thời gian (Timestamp), định danh phiên làm việc và bảo vệ bằng Optimistic Locking trên bảng `od_registration` / `overdraft-loan-contract`.
  2. *Cơ chế Bù trừ SAGA phân tán (Distributed SAGA Compensation)*:
     - Giả sử hệ thống đã phong tỏa sổ tiết kiệm thành công trên Core T24 (trạng thái phong tỏa = LOCKED), nhưng bước gọi service hạn mức Core T24 bị lỗi mạng timeout.
     - SAGA Orchestrator lập tức kích hoạt nhánh bù trừ ngược (Compensating Flow): Phát bản tin giải tỏa phong tỏa sổ tiết kiệm trên Core T24, khôi phục tài sản về trạng thái nguyên vẹn, cập nhật trạng thái hồ sơ sang `ROLLBACK_COMPLETED` và gửi thông báo lỗi chi tiết cho khách hàng. Nhờ đó, hạn chế tình trạng tài sản của khách hàng bị phong tỏa "oan" khi chưa được giải ngân vốn (nếu lệnh giải tỏa cũng lỗi thì đưa vào hàng đợi retry/đối soát).

---

## PHẦN 5: ỨNG DỤNG AI, THIẾT KẾ HỆ THỐNG & ĐÀM PHÁN LƯƠNG 50M (CÂU 91 – 100)

### Câu 91: Bạn thiết kế một Payment Hub phục vụ tải cao (mục tiêu thiết kế ví dụ: 10,000 TPS) cho ACB như thế nào?
- **Trả lời**: (Vẽ sơ đồ kiến trúc 4 tầng):
  1. *Ingress*: Cụm API Gateway (Kong / Spring Cloud Gateway) chạy sau Cloudflare/F5 Load Balancer, xác thực mTLS và Rate Limiting.
  2. *Orchestration Layer*: Cụm Microservices stateless chạy trên Kubernetes, sử dụng Java 21 Virtual Threads hoặc Go Fiber. Triển khai mô hình SAGA Orchestration lưu trạng thái vào PostgreSQL/Oracle.
  3. *Messaging & Streaming Backbone*: Cụm Apache Kafka đa cụm (Multi-cluster active-active) với phân vùng tối ưu theo `account_no`. Triển khai Transactional Outbox Pattern qua Debezium CDC.
  4. *Integration Adapters*: Tách riêng cụm Adapter kết nối Core T24 qua IBM MQ bất đồng bộ và Cổng NAPAS qua TCP Socket nhị phân với Redis Deduplication. Toàn bộ hệ thống có distributed tracing qua OpenTelemetry và giám sát Prometheus/Grafana.

### Câu 92: Làm thế nào để áp dụng mô hình Machine Learning phát hiện gian lận trong luồng giao dịch mà không làm tăng độ trễ hệ thống?
- **Trả lời**: Áp dụng mô hình **Dual-Path Architecture (Đường dẫn kép)**:
  - *Fast Path (Đồng bộ; mục tiêu thiết kế, ví dụ minh họa: < 5ms)*: Sử dụng mô hình nhẹ Isolation Forest đã được lượng tử hóa (Quantization) chạy qua ONNX Runtime trực tiếp trong bộ nhớ của Gateway. Chỉ kiểm tra các đặc trưng tức thời (Z-score số tiền, Geovelocity địa lý, giờ giao dịch). Nếu điểm rủi ro quá cao $\to$ Chặn ngay.
  - *Slow Path (Bất đồng bộ)*: Toàn bộ dữ liệu giao dịch đẩy vào Kafka topic `payment.events`. Cụm worker AI chạy mô hình học sâu (Deep Learning / Graph Neural Networks) phân tích toàn bộ mạng lưới quan hệ giữa các tài khoản người nhận, phát hiện các đường dây rửa tiền phức tạp và cập nhật Blacklist vào Redis cho Fast Path sử dụng.

### Câu 93: Sự cố kỹ thuật lớn nhất bạn từng trực tiếp xử lý tại OCB là gì và bài học rút ra?
- **Trả lời**: *(Đây là **khung kể chuyện minh họa** theo mô hình STAR. Hãy thay bằng sự cố thật của chính mình và chỉ nêu số đo mà mình có bằng chứng; người phỏng vấn sẽ hỏi "đo bằng cách nào?")*. Ví dụ với sự cố deadlock vào ngày thanh toán lương:
  - *Bối cảnh*: Vào ngày chi lương, lưu lượng chuyển khoản và thanh toán hóa đơn tăng vọt. Bảng giao dịch Oracle báo lỗi `ORA-00060 Deadlock detected`, nhiều connection bị treo khiến API Gateway nghẽn 504.
  - *Nguyên nhân*: Hai tiến trình chuyển tiền đồng thời cập nhật tài khoản nguồn và đích theo thứ tự đảo ngược nhau, kết hợp với việc bảng con lịch sử thiếu index trên cột khóa ngoại.
  - *Hành động khắc phục*: Tôi trực tiếp thực hiện lệnh Trace Deadlock qua file `.trc`, xác định chính xác 2 câu lệnh SQL xung đột. Lập tức thêm Index còn thiếu trên cột khóa ngoại (chạy `ONLINE` không lock bảng). Viết lại Stored Procedure áp dụng thuật toán *Deterministic Locking Order* (luôn khóa tài khoản nhỏ trước, lớn sau).
  - *Kết quả*: Nêu số đo thật trước và sau khi sửa (tần suất lỗi `ORA-00060`, thời gian phản hồi API) lấy từ hệ thống giám sát; nếu không có số đo thì nói rõ kết quả định tính và không bịa con số.
  - *Bài học*: Luôn khóa theo thứ tự xác định, đánh index khóa ngoại, và có kịch bản kiểm thử đồng thời trước khi lên production.

### Câu 94: Làm thế nào bạn cân bằng giữa yêu cầu bảo mật khắt khe của ngân hàng và trải nghiệm mượt mà của người dùng?
- **Trả lời**: Áp dụng nguyên tắc **Risk-Based Authentication (Xác thực theo mức độ rủi ro)**. Với các giao dịch giá trị nhỏ (< 10 triệu) đến người nhận quen thuộc và vị trí địa lý quen thuộc, hệ thống cho phép xác thực mượt qua mã PIN hoặc FaceID nhẹ. Ngoài ra, xác thực sinh trắc học là **bắt buộc theo QĐ 2345** (không phụ thuộc điểm AI) khi chuyển trên 10 triệu/lần, khi tổng trong ngày vượt 20 triệu, và khi đăng nhập/giao dịch lần đầu trên thiết bị mới; điểm rủi ro cao (IP lạ, giờ bất thường) có thể kích hoạt thêm bước xác thực. Sinh trắc học được so khớp với mẫu đã đăng ký (đã đối chiếu chip CCCD/VNeID).

### Câu 95: Nếu kiến trúc sư của ACB đề xuất dùng Microservices nhưng bạn thấy bài toán đó chỉ cần Modular Monolith, bạn sẽ phản biện ra sao?
- **Trả lời**: Tôi sẽ phản biện dựa trên phân tích chi phí - lợi ích (Trade-off Analysis):
  - Microservices mang lại sự độc lập triển khai nhưng phải trả giá bằng: Chi phí hạ tầng Kubernetes, mạng lưới phân tán phức tạp, độ trễ mạng (Network Latency), bài toán nhất quán dữ liệu phân tán (phải dùng Saga thay cho ACID DB), và khó khăn trong giám sát phân tán.
  - Nếu module đó có tần suất thay đổi thấp, lưu lượng vừa phải và phụ thuộc chặt chẽ vào dữ liệu Core Banking, tôi đề xuất thiết kế theo mô hình **Modular Monolith** với ranh giới Domain-Driven Design (DDD) rõ ràng. Khi lưu lượng vượt ngưỡng hoặc team mở rộng quy mô, ta có thể tách module đó thành Microservice độc lập mà không tốn công viết lại từ đầu.

### Câu 96: Tại sao bạn ứng tuyển vào ACB mà không tiếp tục ở lại OCB?
- **Trả lời**: 3 năm tại OCB là quãng thời gian quý giá giúp tôi phát triển từ một kỹ sư backend thành Chuyên viên chính, trực tiếp làm các luồng tích hợp tín dụng của Squad Lending và phối hợp với các đội vận hành Core T24, NAPAS, Payment Hub. Tôi chọn ACB vì ACB là ngân hàng thương mại cổ phần bán lẻ hàng đầu Việt Nam với văn hóa quản trị rủi ro chặt chẽ và đang dẫn đầu trong làn sóng chuyển đổi số số hóa toàn diện. Đây là môi trường lý tưởng để tôi đóng góp năng lực tích hợp hệ thống phân tán và áp dụng kiến thức AI tôi đang học (đang học Cử nhân AI tại UIT, dự kiến tốt nghiệp 11/2026) vào các bài toán quy mô lớn hơn.

### Câu 97: Bạn có 3 năm làm việc ở OCB và đang học Cử nhân AI tại UIT (dự kiến tốt nghiệp 11/2026). Khung lương 3 năm thường chỉ ở mức Middle (35–40M). Tại sao ACB nên trả cho bạn 50M Gross?
- **Trả lời**: (Sử dụng kịch bản đàm phán 3 trụ cột):
  > *"Em hiểu khung chức danh theo số năm kinh nghiệm là chuẩn mực quản trị chung. Tuy nhiên, giá trị mà ACB nhận được từ em không được đo bằng số tháng ngồi tại văn phòng, mà bằng **tốc độ giải quyết vấn đề và năng lực tạo ra giá trị ngay từ ngày đầu tiên**:"*
  > 1. *Tại OCB, chức danh của em là **Chuyên viên chính (Senior Integration Application Specialist)** trong Squad Lending, trực tiếp làm các luồng tích hợp nghiệp vụ: Thấu chi cầm cố sổ tiết kiệm phong tỏa 2 pha trên Core T24, Thấu chi lương, Tích hợp ký số Cloud CA kết hợp xác thực khuôn mặt, và cổng CIC B2B [chỉ giữ nếu có bằng chứng]. Đồng thời, em phối hợp với các đội hạ tầng của phòng (đội sở hữu kết nối Core T24 qua IBM MQ và chuyển mạch NAPAS 247) khi xử lý các bài toán hạch toán phân tán và deadlock Oracle.*
  > 2. *Em đang học Cử nhân AI tại UIT, dự kiến tốt nghiệp 11/2026, song song với công việc. Chương trình bổ sung cho em tư duy giải thuật và nền tảng về phát hiện bất thường; dự án AI của em là dự án học tập/cá nhân, không phải hệ thống production.*
  > 3. *Với mức lương 50M Gross, ACB có ngay một Kỹ sư Tích hợp cấp Senior có thể độc lập gánh vác các dự án trọng điểm mà không tốn thời gian hay chi phí đào tạo lại. Em tin rằng đây là khoản đầu tư mang lại ROI cao và an toàn cho ngân hàng.*

### Câu 98: Nếu được nhận vào ACB, kế hoạch 90 ngày đầu tiên của bạn là gì?
- **Trả lời**:
  - **30 ngày đầu**: Tìm hiểu toàn diện kiến trúc hiện tại của ACB, tài liệu tích hợp API, môi trường CI/CD, chuẩn mực mã nguồn và các quy định bảo mật PCI-DSS/QĐ 2345. Nắm rõ quy trình phối hợp giữa Khối CNTT và các Khối Nghiệp vụ.
  - **60 ngày tiếp theo**: Trực tiếp nhận bàn giao và tham gia phát triển một module tích hợp cụ thể (ví dụ kết nối đối tác mới hoặc tối ưu hóa adapter Core). Đưa ra các cải tiến về hiệu năng (tối ưu hóa index Oracle hoặc tinh chỉnh Kafka consumer).
  - **90 ngày**: Độc lập dẫn dắt thiết kế kỹ thuật cho các tính năng tích hợp mới, chia sẻ kinh nghiệm xử lý sự cố T24/NAPAS và tổ chức workshop nội bộ về ứng dụng AI trong tối ưu hóa luồng thanh toán cho các đồng nghiệp.

### Câu 99: Định nghĩa của bạn về một "Senior Engineer thực thụ" trong ngành Ngân hàng?
- **Trả lời**: Trong ngành Ngân hàng, một Senior Engineer thực thụ không phải là người viết được những đoạn code phức tạp nhất, mà là người:
  1. Luôn đặt **Tính an toàn và Bảo toàn dòng tiền của khách hàng** lên vị trí số 1.
  2. Viết code rõ ràng, có khả năng tự phục hồi (Self-healing), có logging truy vết đầy đủ và dễ bảo trì.
  3. Dự báo trước được các điểm lỗi tiềm ẩn (Failure modes: nghẽn MQ, timeout mạng, deadlock DB) trước khi chúng kịp xảy ra trên môi trường Production.
  4. Có khả năng kết nối mượt mà giữa Ngôn ngữ Nghiệp vụ của Giám đốc Khối Kinh doanh với Ngôn ngữ Kỹ thuật của hệ thống máy tính.

### Câu 100: Bạn cam kết gì với ACB nếu đạt được mức đãi ngộ 50 triệu gross kỳ vọng?
- **Trả lời**: Em cam kết cống hiến 100% tâm huyết và năng lực kỹ thuật:
  - Đáp ứng SLA/SLO được giao cho các phân hệ tích hợp em phụ trách (mức cụ thể theo cam kết của ngân hàng, không tự đặt con số).
  - Thiết kế có kiểm soát (idempotency, đối soát, kiểm thử đồng thời) để giảm thiểu rủi ro thất thoát tài chính và trừ tiền kép, và xử lý minh bạch khi có sự cố.
  - Sẵn sàng đồng hành cùng Khối CNTT ACB trong mọi giai đoạn cao điểm (trực hệ thống Tết, Golive dự án lớn) và tiên phong nghiên cứu, chuyển giao các giải pháp AI-Banking tiên tiến nhất cho ngân hàng.
