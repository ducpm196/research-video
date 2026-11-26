# Lab SPB L11 — Quan sát hệ thống: nhật ký cấu trúc ECS JSON, `X-Correlation-Id`, OpenTelemetry & Prometheus

Cài đặt quan sát chuẩn sản xuất trên Boot 4:
1. `CorrelationFilter` giữ hoặc tự sinh tiêu đề `X-Correlation-Id`, đặt vào `MDC` để log cấu trúc (`logging.structured.format.console=ecs`) có đủ mã tương quan, và luôn dọn `MDC` trong `finally`.
2. `ObsTransferController` ghi nhận bộ đếm `bank_transfers` trên `MeterRegistry` chỉ gắn nhãn thấp `status` (không gắn ID giao dịch hay mã tương quan vào nhãn Prometheus).
3. Mở `/actuator/prometheus` để thu thập chỉ số `bank_transfers_total`.

Chấm tự động:
```bash
bash labs/cham.sh SPB L11 duong_dan/du_an_cua_ban
```
