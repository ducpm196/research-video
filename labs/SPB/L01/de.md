# Lab SPB L01 — `@RestController`, DTO `record`, Validation & Problem Details (RFC 9457)

Mở rộng dịch vụ `vn.nganhang.chuyenkhoan`:
1. Tạo `TransferRequest(fromAccount, toAccount, amount)` dùng Java `record`, kiểm `@NotBlank` trên 2 tài khoản và `@Positive` trên `amount`.
2. `POST /api/v1/transfers` nhận `@Valid @RequestBody`, hợp lệ trả `201 Created` với `TransferResponse(txId, "ACCEPTED", amount)`.
3. Thêm `@RestControllerAdvice` (`ApiExceptionHandler`) trả `ProblemDetail` chuẩn RFC 9457 (`application/problem+json`, HTTP `400`, `title = "Validation Error"`, danh sách trường lỗi trong thuộc tính `errors`).
4. Khai báo thêm phụ thuộc `spring-boot-starter-validation` trong `pom.xml` để kích hoạt kiểm tra hợp lệ bean.

Chấm tự động:
```bash
bash labs/cham.sh SPB L01 duong_dan/du_an_cua_ban
```
