# Lab SPB L10 — Kiểm thử tích hợp toàn luồng với PostgreSQL 17, Redis 8 & Kafka 3.9 qua Testcontainers

Kết nối cả ba container thật dùng chung via `@ServiceConnection`:
1. `FullStackBaseTest` khởi động singleton `postgres:17-alpine`, `redis:8`, `apache/kafka:3.9.0` đúng digest trong `VERSIONS.md`.
2. `POST /api/v1/full-transfers` cập nhật số dư + ghi 2 dòng bút toán PostgreSQL (`SUM = 0`), xoá khoá đệm Redis (`bal:<id>`), và phát sự kiện tới `bank.full.events` để listener nhận được.
3. Khai báo đúng các thành phần được kiểm thử gọi trực tiếp: `FullStackBaseTest` (trường `PG`, `REDIS`, `KAFKA`), `FullStackService.cachedBalance(...)` và `getEvents()`, cùng `AccountRepo`, `JournalRepo.net()` (xem `labs/SPB/L10/loi_giai`).

Chấm tự động (cần Docker):
```bash
bash labs/cham.sh SPB L10 duong_dan/du_an_cua_ban
```
