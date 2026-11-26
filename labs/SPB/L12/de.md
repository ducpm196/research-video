# Lab SPB L12 — Tình huống chuyên gia: `Dockerfile` nhiều tầng, JVM container & đường ống CI

Hoàn thiện cấu hình đóng gói sản xuất cho dịch vụ chuyển khoản:
1. Viết `Dockerfile` nhiều tầng (`>= 2` `FROM`): tầng dựng dùng JDK 21 + `./mvnw -B package -DskipTests`, tầng chạy dùng `eclipse-temurin:21-jre-alpine`, tạo `USER` không phải root và khởi chạy với `-XX:MaxRAMPercentage=75.0`.
2. Viết `.github/workflows/ci.yml` chạy `./mvnw -B verify` trên JDK 21.
3. Mở `GET /api/v1/runtime` trả về cấu hình heap (`maxHeapMiB512_75pct` = `384` MiB ở ngưỡng 512 MiB × 75%) và cài hàm tĩnh `RuntimeProfileController.maxHeapMiB(long, double)`.

Chấm tự động:
```bash
bash labs/cham.sh SPB L12 duong_dan/du_an_cua_ban
```
