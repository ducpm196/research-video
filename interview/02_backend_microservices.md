# CHUYÊN ĐỀ 2: KỸ NGHỆ MICROSERVICES & SPRING BOOT DOANH NGHIỆP

> **Mục tiêu**: Nâng cấp kỹ năng lập trình từ cơ bản lên chuẩn Kỹ sư Backend Doanh nghiệp (Enterprise Backend Engineer).  
> **Căn cứ học phần**: T2 & T5 trong khung chuẩn UIT (`curriculum/swf.yaml`, `sdp.yaml`, `cld.yaml`, `dvo.yaml`).

---

## 1. NỘI TẠI SPRING BOOT & TRANSACTION MANAGEMENT

### 1.1. Cơ chế Dynamic Proxy & Lỗi "Self-Invocation" kinh điển
- Hầu hết các tính năng kỳ diệu của Spring (`@Transactional`, `@Async`, `@Cacheable`, `@Secured`) đều dựa trên **AOP (Aspect-Oriented Programming)** và kỹ thuật **Dynamic Proxy**:
  - **CGLIB Proxy**: Tạo class con kế thừa trực tiếp từ target class (sinh bytecode lúc chạy). Spring Boot 2.0+ **mặc định dùng CGLIB** (`spring.aop.proxy-target-class=true`) kể cả khi bean có interface.
  - **JDK Dynamic Proxy** (`java.lang.reflect.Proxy`): chỉ dùng khi đặt `spring.aop.proxy-target-class=false` và bean có cài đặt Interface (đây là mặc định của Spring Framework thuần, không phải Spring Boot).
- **Lỗi tự gọi hàm nội bộ (Self-Invocation Bug)**:
  ```java
  @Service
  public class PaymentService {
      public void processOrder(Order order) {
          // GỌI NỘI BỘ TRONG CÙNG CLASS: SẼ KHÔNG CÓ TRANSACTION!
          this.deductBalance(order);
      }

      @Transactional
      public void deductBalance(Order order) {
          // Cập nhật số dư...
      }
  }
  ```
  - **Bản chất lỗi**: Khi một method trong cùng class gọi trực tiếp method khác qua con trỏ `this`, lời gọi không đi qua Spring Proxy bọc ngoài, dẫn đến việc `@Transactional` bị bỏ qua hoàn toàn. Dữ liệu ghi vào DB không được commit trong transaction và không thể rollback khi có lỗi!
  - **Cách khắc phục**:
    1. Tách method sang một `@Service` riêng biệt rồi inject vào.
    2. Tự inject chính bean đó vào class (qua `@Lazy` hoặc `ApplicationContext.getBean()`).
    3. Sử dụng AspectJ compile-time / load-time weaving thay vì Spring AOP proxy.

### 1.2. Lan truyền Giao dịch (Transaction Propagation) & Quy tắc Rollback
- Các mức Propagation cần nắm vững trong Ngân hàng:
  - **`REQUIRED`** (Mặc định): Nếu đã có transaction cha đang chạy, tham gia vào transaction đó. Nếu chưa có, tạo mới.
  - **`REQUIRES_NEW`**: Luôn luôn tạm dừng (suspend) transaction hiện tại và mở ra một transaction vật lý hoàn toàn độc lập. Cực kỳ quan trọng trong ngân hàng: Dùng để **ghi Log kiểm toán (Audit Log)** hoặc ghi nhận trạng thái lỗi, đảm bảo dù giao dịch chuyển tiền chính bị rollback thì bản ghi log thất bại vẫn được lưu thành công vào cơ sở dữ liệu.
  - **`MANDATORY`**: Bắt buộc phải có transaction cha đang chạy; nếu không có sẽ ném ra ngoại lệ `IllegalTransactionStateException`.
  - **`SUPPORTS`**: Nếu có transaction thì chạy trong transaction; nếu không có thì chạy non-transactional.
- **Quy tắc Rollback mặc định của Spring**:
  - Spring chỉ mặc định rollback khi gặp **`RuntimeException`** (Unchecked Exception) hoặc **`Error`**.
  - Nếu method ném ra **`Checked Exception`** (như `IOException`, `SQLException`, hoặc custom checked exception), Spring **MẶC ĐỊNH SẼ KHÔNG ROLLBACK**!
  - **Quy chuẩn bắt buộc trong Ngân hàng**: Luôn khai báo tường minh:
    ```java
    @Transactional(rollbackFor = Exception.class)
    public void executeFundTransfer(...) { ... }
    ```

---

## 2. THIẾT KẾ RESTFUL API CHUẨN OPENAPI 3.0 (SWAGGER)

ACB yêu cầu khắt khe về việc đặc tả API bằng Swagger/OpenAPI để phục vụ kết nối Open Banking và hệ thống phân tán.

### 2.1. Ngữ nghĩa HTTP & Tính lũy đẳng (Idempotency)
- **Tính Idempotent**: Một request được gọi một lần hay nhiều lần liên tiếp đều tạo ra cùng một trạng thái hệ thống cuối cùng.
  - `GET`, `PUT`, `DELETE`: Có tính Idempotent.
  - `POST`: **Không có tính Idempotent** (mỗi lần gọi có thể tạo mới một giao dịch). Do đó, các API chuyển tiền (`POST /transfers`) bắt buộc phải bổ sung header `Idempotency-Key` (tên theo bản nháp IETF `draft-ietf-httpapi-idempotency-key-header`; nhiều hệ thống cũ dùng `X-Idempotency-Key`) hoặc `order_id` để hệ thống kiểm tra chống trùng lặp.
- **Mã phản hồi HTTP chuẩn mực trong Ngân hàng**:
  - `200 OK`: Truy vấn hoặc xử lý đồng bộ thành công.
  - `201 Created`: Tạo mới thành công tài nguyên (mở sổ tiết kiệm, tạo lệnh chuyển khoản).
  - `202 Accepted`: Lệnh đã được tiếp nhận và đưa vào hàng đợi xử lý bất đồng bộ (chưa hạch toán xong).
  - `400 Bad Request`: Sai format dữ liệu đầu vào.
  - `401 Unauthorized`: Chưa đăng nhập hoặc Token hết hạn.
  - `403 Forbidden`: Đã đăng nhập nhưng không có quyền thực thi tác vụ.
  - `409 Conflict`: Xung đột phiên bản dữ liệu (Optimistic Lock failure) hoặc giao dịch đang được xử lý bởi phiên khác.
  - `422 Unprocessable Content` (RFC 9110; tên cũ "Unprocessable Entity"): Dữ liệu đúng cú pháp nhưng vi phạm quy tắc nghiệp vụ (ví dụ: Số dư tài khoản không đủ để trích nợ).
  - `504 Gateway Timeout`: Phía Core T24 hoặc NAPAS không phản hồi kịp thời (cần kiểm tra trạng thái lệnh, không được tự ý báo fail cho người dùng).

### 2.2. Định dạng lỗi chuẩn RFC 9457 (Problem Details, thay thế RFC 7807)
Mọi API ngân hàng phải trả về cấu trúc lỗi đồng nhất, `Content-Type: application/problem+json` (Spring 6 có sẵn lớp `ProblemDetail`); `errorCode`, `timestamp` là trường mở rộng hợp lệ:
```json
{
  "type": "https://api.acb.com.vn/errors/insufficient-funds",
  "title": "Insufficient Account Balance",
  "status": 422,
  "detail": "Account 12345678 has balance of 100,000 VND, which is insufficient for transfer amount 500,000 VND",
  "instance": "/api/v1/transfers/tx-987654321",
  "errorCode": "ACC_0042",
  "timestamp": "2026-11-06T15:30:00Z"
}
```

---

## 3. BỘ NHỚ ĐỆM PHÂN TÁN VỚI REDIS (HIGH-PERFORMANCE CACHING)

### 3.1. Các mô hình Caching
1. **Cache-Aside (Lazy Loading)**: Ứng dụng đọc từ Cache trước; nếu Miss thì đọc từ DB rồi ghi ngược vào Cache; khi Update dữ liệu thì xóa Cache (hoặc cập nhật DB rồi invalidate Cache).
2. **Write-Through**: Ứng dụng ghi vào Cache, Cache tự động ghi đồng bộ xuống DB.
3. **Write-Behind (Write-Back)**: Ứng dụng ghi vào Cache và phản hồi ngay; Cache gom nhóm các bản ghi để ghi bất đồng bộ xuống DB (thường dùng cho lưu trữ lượt view hoặc số liệu thống kê, hiếm khi dùng cho số dư tài khoản).

### 3.2. Ba hiểm họa kinh điển của Cache & Giải pháp giảm thiểu

```
1. Cache Penetration (Thủng Cache):
   Request -> ID không tồn tại -> Cache Miss -> DB Query -> DB Miss -> Server chịu tải!
   => Giải pháp: Lưu Null Object vào Cache (TTL 60s) hoặc dùng Bloom Filter.

2. Cache Breakdown (Sập Cache theo Điểm):
   Key "Hot" (ví dụ: Tỷ giá vàng/USD) hết hạn đột ngột -> 10,000 concurrent requests cùng chọc vào DB!
   => Giải pháp: Mutex Lock (D-Lock) hoặc Logical Expiration (tự refresh ngầm).

3. Cache Avalanche (Tuyết lở Cache):
   Hàng triệu Keys cùng hết hạn tại đúng 00:00:00 -> Toàn bộ request dồn xuống DB -> Sập DB!
   => Giải pháp: Thêm Jitter (TTL ngẫu nhiên: 3600s + rand(0, 300s)).
```

### 3.3. Khóa phân tán với Redis (Distributed Lock)
- Để **giảm** khả năng hai instance cùng xử lý một tài khoản tại một thời điểm (khóa Redis có hạn TTL không bảo đảm loại trừ tuyệt đối khi có GC pause dài hoặc failover; tính đúng cuối cùng phải dựa vào ràng buộc UNIQUE/cập nhật có điều kiện ở DB hoặc fencing token, xem tài liệu "Distributed Locks with Redis"):
  ```java
  // Lệnh SET nguyên tử (Atomic) với NX (Not Exists) và PX (Milliseconds Expiration) — Jedis 3.x+
  String result = jedis.set("lock:account:" + accountNo, requestId,
                            SetParams.setParams().nx().px(10000));
  if ("OK".equals(result)) {
      try {
          // Thực thi trừ tiền tài khoản an toàn...
      } finally {
          // Giải phóng khóa bằng LUA SCRIPT để đảm bảo chỉ xóa đúng khóa do chính mình tạo
          String luaScript = 
              "if redis.call('get', KEYS[1]) == ARGV[1] then " +
              "   return redis.call('del', KEYS[1]) " +
              "else " +
              "   return 0 " +
              "end";
          jedis.eval(luaScript, Collections.singletonList("lock:account:" + accountNo), 
                                Collections.singletonList(requestId));
      }
  }
  ```

---

## 4. CONTAINER HÓA VỚI DOCKER & TỐI ƯU HÓA CHO JAVA

### 4.1. Multi-Stage Dockerfile chuẩn bảo mật & gọn nhẹ
```dockerfile
# Giai đoạn 1: Build source code bằng Maven
FROM maven:3.9-eclipse-temurin-21-alpine AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src
RUN mvn clean package -DskipTests

# Giai đoạn 2: Runtime Image siêu nhẹ
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Tạo non-root user để tăng cường bảo mật
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

COPY --from=builder /app/target/*.jar app.jar

# Tinh chỉnh JVM thích ứng với giới hạn RAM của Kubernetes Container
ENV JAVA_OPTS="-XX:InitialRAMPercentage=50.0 -XX:MaxRAMPercentage=75.0 -XX:+UseG1GC -XX:+ExitOnOutOfMemoryError"

EXPOSE 8080
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

- **Giải thích cờ JVM Container Awareness**:
  - JVM nhận biết giới hạn RAM của container nhờ `-XX:+UseContainerSupport` (bật mặc định từ JDK 10 / 8u191); hai cờ phần trăm bên dưới chỉ quyết định kích thước heap dựa trên giới hạn đó.
  - `InitialRAMPercentage=50.0`: JVM khởi tạo Heap bằng 50% giới hạn RAM của Container.
  - `MaxRAMPercentage=75.0`: Giới hạn trần Heap là 75% RAM Container, chừa lại 25% cho Metaspace, Thread Stacks, Native Memory và I/O buffers, giúp giảm nguy cơ Container bị Linux OOM-Killer tắt cưỡng bức (`Exit Code 137`). Không bảo đảm tuyệt đối: native memory (direct buffer, Metaspace không giới hạn, nhiều thread) vẫn có thể vượt phần 25%, nên cần đo bằng Native Memory Tracking và đặt `-XX:MaxMetaspaceSize`.

---

## 5. TÍCH HỢP HỆ THỐNG DOANH NGHIỆP: AEM & JAVA CORE (SUTRIX DOMAIN)

Trong các tổ chức quy mô lớn như Ngân hàng và Tập đoàn Viễn thông (ví dụ Globe Telecom), hệ thống phân tách rạch ròi giữa **Kênh giao diện trải nghiệm số (Experience Platform - Adobe Experience Manager / AEM)** và **Hạ tầng Dịch vụ Tích hợp (Core Services / Microservices)**:

1. **Kiến trúc Adobe Experience Manager (AEM Sites)**:
   - **Mô hình kiến trúc phân tầng**:
     $$\text{AEM Author / Publisher} \to \text{AEM Dispatcher (Apache HTTP Server Cache)} \to \text{End Users}$$
   - **Apache Sling & JCR (Java Content Repository - Apache Jackrabbit Oak)**: Mọi nội dung, trang web, assets được lưu trữ dưới dạng cây Node phân cấp (Hierarchical Node Tree). Truy vấn JCR bằng XPath, SQL-2 hoặc QueryBuilder API.
   - **OSGi (Open Services Gateway initiative - Apache Felix)**: Nền tảng module hóa động của Java. Cho phép nạp (install), dừng (stop), cập nhật (update) các gói dịch vụ (OSGi Bundles / Services) trong runtime mà không cần khởi động lại máy chủ JVM.
   - **Sling Models & HTL (HTML Template Language)**: Phân tách hoàn toàn logic xử lý nghiệp vụ Java khỏi tầng hiển thị (Presentation Layer), đảm bảo tính an toàn chống lỗi XSS tự động.

2. **Mô hình Tích hợp AEM với Backend Microservices (Headless / Hybrid Integration)**:
   - Khi AEM cần hiển thị dữ liệu thời gian thực (ví dụ: Biểu lãi suất tiết kiệm, Tỷ giá ngoại tệ ACB, Form đăng ký mở thẻ/khoản vay):
     - **Sai lầm sơ cấp**: Để component trên AEM gọi trực tiếp API backend mỗi khi render HTML $\to$ Làm sập hệ thống backend khi có hàng chục ngàn người truy cập đồng thời.
     - **Giải pháp Senior**:
       - *Chiến lược 1 (Client-side AJAX / SPA component)*: AEM chỉ render khung HTML/React tĩnh; trình duyệt người dùng gọi trực tiếp qua API Gateway (có Rate Limiting và Redis Caching).
       - *Chiến lược 2 (Dispatcher Caching & Invalidation)*: AEM Dispatcher lưu cache kết quả HTML/JSON. Khi backend có thay đổi (ví dụ cập nhật tỷ giá), backend phát sự kiện qua Kafka $\to$ Trigger lệnh *Dispatcher Flush (Replication Agent)* xóa cache tức thời.
