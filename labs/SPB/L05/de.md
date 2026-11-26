# Lab SPB L05 — Redis 8 thật: Cache-Aside, TTL kèm jitter, vô hiệu đệm & chống dồn tải (`SET NX EX`)

Cài đặt `BalanceCacheService` làm việc với **Redis 8** thật (`redis:8@sha256:1f88291b4c57bdf249f02eb085a8669889b2d2954e91d4de5118a5da6b78dd53`):
1. `getBalance(accId)` đọc khoá `"bal:" + accId`; khi trượt đệm dùng `SET lock:bal:<id> <token> NX EX 5` để chỉ 1 luồng truy vấn DB và ghi lại đệm với TTL 30–35 giây.
2. `deposit(accId, delta)` cập nhật số dư DB và **xoá ngay khoá đệm** `"bal:" + accId` tránh đọc số cũ.
3. Cung cấp thêm hai phương thức đếm lượt đọc DB phục vụ kiểm thử: `getDbReads()` (trả số lần truy vấn DB) và `resetDbReads()` (đặt lại bộ đếm về 0).
4. Cài đủ lớp thực thể và nền kiểm thử đi kèm (`Account`, `AccountRepo`, `RedisBaseTest`) như trong `labs/SPB/L05/loi_giai`.

Chấm tự động (cần Docker):
```bash
bash labs/cham.sh SPB L05 duong_dan/du_an_cua_ban
```
