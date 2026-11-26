# Lab SPB L03 — PostgreSQL 17 thật + Flyway + Bắt & Sửa lỗi 1+N (`JOIN FETCH`)

Dùng `spring.jpa.hibernate.ddl-auto=validate` và tệp di trú Flyway `V1__init.sql` tạo hai bảng `accounts` và `journal_entries` trên **PostgreSQL 17** thật (Testcontainers ghim digest `postgres:17-alpine@sha256:d3244e8ce3f165ee3c93d9c4a4b1d0fe48b3a89e2287b717fdcbbde92d405065`):
1. `AccountRepository` phải khai báo `findAllWithEntries()` dùng `@Query("SELECT DISTINCT a FROM Account a LEFT JOIN FETCH a.entries ORDER BY a.id")`.
2. Trên 20 tài khoản mỗi tài khoản có 1 bút toán, `findAll()` rồi đọc `entries` phát sinh `>= 21` câu SQL (1+N), còn `findAllWithEntries()` chỉ phát sinh đúng `1` câu SQL.
3. Khai báo đầy đủ cặp thực thể quan hệ (`Account`, `JournalEntry`), `JournalEntryRepository` và kế thừa `PostgresBaseTest` như cấu trúc mẫu trong `labs/SPB/L03/loi_giai`.

Chấm tự động (cần Docker):
```bash
bash labs/cham.sh SPB L03 duong_dan/du_an_cua_ban
```
