# Lab SPB L00 — Dự án Spring Boot 4.1.3 nền tảng với Maven Wrapper

Dựng dự án Maven Wrapper (`spring-boot-starter-parent:4.1.3`, `java.version=21`, gói `vn.nganhang.chuyenkhoan`) dùng starter web mô-đun của Boot 4 (`spring-boot-starter-webmvc`).

Yêu cầu:
1. Lớp chính `ChuyenKhoanApplication` đánh dấu `@SpringBootApplication`.
2. Bộ điều khiển `HealthController` mở `GET /api/v1/health` trả JSON gồm `"status": "UP"`, `"service": "chuyen-khoan"`, `"boot": "4.1.3"`.
3. Đường dẫn không tồn tại trả HTTP 404.
4. Nếu máy chưa cài sẵn `mvn` toàn cục, chép `mvnw`, `mvnw.cmd` và thư mục `.mvn/` từ thư mục mẫu `labs/SPB/L00/loi_giai` (xem `labs/SPB/VERSIONS.md`).

Chấm tự động bằng dự án mẫu hoặc thư mục của bạn:
```bash
bash labs/cham.sh SPB L00 duong_dan/du_an_cua_ban
```
