# Lab SPB L02 — Tầng dịch vụ, tiêm phụ thuộc & `@Transactional` (`REQUIRES_NEW`, `rollbackFor`)

Cài đặt `TransferService` và `AuditLogService` (tiêm phụ thuộc qua constructor):
1. `InsufficientFundsException` là checked exception (`extends Exception`).
2. `TransferService.transfer(fromId, toId, amount)` đánh dấu `@Transactional(rollbackFor = InsufficientFundsException.class)`: nếu `fromId.equals(toId)` hoặc `amount <= 0` thì ném `IllegalArgumentException`; trừ tạm số dư nguồn, gọi `audit.record(...)`, nếu số dư nguồn `< 0` thì ném `InsufficientFundsException` để hoàn tác số dư.
3. `AuditLogService.record(msg)` dùng `@Transactional(propagation = Propagation.REQUIRES_NEW)` để nhật ký tra soát vẫn được lưu ngay cả khi giao dịch chính bị hoàn tác.
4. Tham khảo hợp đồng các thực thể và kho đi kèm (`Account`, `AccountRepo`, `AuditEntry`, `AuditEntryRepo`) trong thư mục mẫu `labs/SPB/L02/loi_giai`.

Chấm tự động:
```bash
bash labs/cham.sh SPB L02 duong_dan/du_an_cua_ban
```
