# Phiên bản công cụ đã kiểm chứng cho khoá SPB (chốt ngày 2026-11-24 theo quy tắc D-11 / BN-14)

Mọi phiên bản dưới đây được kiểm chạy thật trên máy chuẩn (`audit/review/audit_final/logs/af5_exec/spb_step0_verify.log`) vào ngày **2026-11-24**:

| Thành phần | Phiên bản / Giá trị đã ghim | Lý do chọn & Ghi chú |
|---|---|---|
| **Java (JDK)** | `21.0.13` (Eclipse Adoptium LTS, `C:\tools\jdk-21`) | Theo `labs/ENV.md` (JDK 21+) |
| **Spring Boot** | `4.1.3` (`spring-boot-starter-parent:4.1.3`) | Theo quy tắc `D-11`: nhánh `4.1.x` có hỗ trợ mã nguồn mở tới `2027-07-31` và đã có bản vá `4.1.3` (ra ngày `2026-11-19`); nhánh `4.2.0` mới ra `2026-11-19` chưa có bản vá `.1` |
| **Maven Wrapper** | Apache Maven `3.10.1` (`mvnw` / `mvnw.cmd`, `sha` trong `mvnw` chuẩn của `start.spring.io`) | Máy không cài `mvn` toàn cục (`O-0024`), mọi bài `SPB` dùng `./mvnw -B verify` |
| **springdoc-openapi** | `3.2.1` (`org.springdoc:springdoc-openapi-starter-webmvc-ui:3.2.1`) | Bản `3.x` tương thích Spring Boot `4.1.x` (kiểm tồn tại trên Maven Central ngày `2026-11-24`) |
| **Docker Engine** | `28.3.2` (`build 578ccf6`) | Docker Desktop (`>= 24.0`, máy người học tối thiểu 8 GB RAM) |
| **Ảnh `hello-world`** | `hello-world:latest` @ `sha256:1e4c05b897a751332ce85c7e9449da2d93514ea2dea6dbb0e2753c9e949b2bfa` | Thử Docker ở `SPB L00` |
| **Ảnh `postgres`** | `postgres:17-alpine` @ `sha256:d3244e8ce3f165ee3c93d9c4a4b1d0fe48b3a89e2287b717fdcbbde92d405065` | Dùng từ `SPB L03` (JPA + Flyway) & `SPB L10` (Testcontainers) |
| **Ảnh `redis`** | `redis:8` (`8.10.3`) @ `sha256:1f88291b4c57bdf249f02eb085a8669889b2d2954e91d4de5118a5da6b78dd53` | Dùng ở `SPB L05` & `SPB L10` |
| **Ảnh `apache/kafka`** | `apache/kafka:3.9.0` @ `sha256:fbc7d7c428e3755cf36518d4976596002477e4c052d1f80b5b9eafd06d0fff2f` | Dùng ở `SPB L06` & `SPB L10` (KRaft, không cần ZooKeeper) |
| **Ảnh Oracle (`WP-3C`)** | `gvenzl/oracle-free:23-slim` @ `sha256:6d61d267a3b978c24c5ac1790e62e927416a0aec446bd86e4b3a1527562757bd` | Container `bnx-ora` (Oracle AI Database 26ai Free 23.26.3) cho 5 nhánh lab tuỳ chọn `WP-3C` |

## Ghi chú nâng cấp Spring Boot 4.1.x (khác 2.x / 3.x)
- Spring Boot 4 tách gọn starter theo mô-đun: web dùng `spring-boot-starter-webmvc` (thay cho `-web`), kiểm thử MVC dùng `spring-boot-starter-webmvc-test`, Flyway dùng `spring-boot-starter-flyway`, Security OAuth2 Resource Server dùng `spring-boot-starter-security-oauth2-resource-server`.
- Các ví dụ `RestTemplate` / `TestRestTemplate` đã đánh dấu lỗi thời từ 4.x; khoá dùng `RestClient` / `MockMvc`.
- `apache/kafka:3.9.0` chạy với Testcontainers `2.0.5` cần `.withEnv("KAFKA_LISTENERS", "PLAINTEXT://:9092,BROKER://:9093,CONTROLLER://:9094")` để tránh lỗi kiểm tra `0.0.0.0` trong `advertised.listeners` của `KafkaDockerWrapper` (đã kiểm chạy thật cùng PostgreSQL 17 và Redis 8).
