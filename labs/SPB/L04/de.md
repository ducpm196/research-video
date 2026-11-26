# Lab SPB L04 — Sổ cái bút toán kép, khoá bi quan theo thứ tự & bảng `Idempotency-Key`

Cài đặt `LedgerTransferService` trên **PostgreSQL 17** thật (`V1__ledger.sql` có cột `version` cho khoá lạc quan và bảng `idempotency_keys` khoá chính `idem_key`):
1. Kiểm tra `idempotency_keys` trước; trùng `idemKey` thì trả ngay `txId` đã chốt, không trừ tiền lại.
2. Khoá 2 tài khoản bằng `@Lock(LockModeType.PESSIMISTIC_WRITE)` luôn theo **thứ tự mã tăng dần** (`fromId.compareTo(toId) <= 0`) để triệt tiêu bế tắc khi chạy ngược chiều đồng thời.
3. Ghi 2 dòng `JournalEntry` (`-amount` ở nguồn, `+amount` ở đích) sao cho `SUM(amount) = 0`.
4. Cài đủ các lớp phụ trợ (`IdempotencyRecord`, `JournalRepo.netSum()`, `PostgresBaseTest`) và cột `@Version` kiểu `long` trên `Account` theo mẫu `labs/SPB/L04/loi_giai`.

Chấm tự động (cần Docker):
```bash
bash labs/cham.sh SPB L04 duong_dan/du_an_cua_ban
```
