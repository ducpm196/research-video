# Lab SPB L09 — Kiểm thử đơn vị (JUnit 5 + Mockito) và tầng web (`@WebMvcTest` + `@MockitoBean`)

Cài đặt `UnitTransferService` và `UnitTransferController`:
1. Kiểm số dư trước khi trừ; nếu thiếu ném `IllegalStateException` và **tuyệt đối không** gọi `debit`/`credit`/`alerts.sent`.
2. Thứ tự gọi bắt buộc: `balanceOf` → `debit` → `credit` → `alerts.sent`.
3. `UnitTransferController` kiểm hợp lệ `@Valid` trả `201` hoặc `400` chạy gọn qua lát cắt `@WebMvcTest` + `@MockitoBean`.

Chấm tự động:
```bash
bash labs/cham.sh SPB L09 duong_dan/du_an_cua_ban
```
