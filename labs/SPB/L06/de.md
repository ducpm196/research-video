# Lab SPB L06 — Kafka 3.9.0 thật: Outbox giao dịch, thử lại 3 lần & hàng thư chết `-dlt`

Xây luồng phát sự kiện an toàn trên **Apache Kafka 3.9.0** (KRaft, Testcontainers ghim digest + `KAFKA_LISTENERS` không dùng `0.0.0.0`):
1. `OrderOutboxService.createTransferOrder(...)` lưu `OutboxEvent(PENDING)` trong cùng `@Transactional`; khi giao dịch hoàn tác, hàng Outbox cũng mất theo.
2. `publishPending()` phát từng bản ghi lên chủ đề `transfer.events` và chuyển trạng thái `SENT`.
3. `TransferEventConsumer` đánh dấu `@RetryableTopic(attempts = "3", backOff = @BackOff(delay = 100), dltTopicSuffix = "-dlt")`: bản tin bắt đầu bằng `"POISON:"` ném lỗi đủ 3 lần sẽ rơi vào `@DltHandler` (`transfer.events-dlt`).
4. Cung cấp đầy đủ `OutboxEvent`, `OutboxRepo`, `KafkaBaseTest` cùng hai getter kiểm thử `getProcessed()` và `getDltReceived()` (tham khảo `labs/SPB/L06/loi_giai`).

Chấm tự động (cần Docker):
```bash
bash labs/cham.sh SPB L06 duong_dan/du_an_cua_ban
```
