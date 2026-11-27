# Lab SPB L08 — Spring Security: JWT HS256, phân quyền RBAC & chặn truy cập chéo đối tượng (BOLA)

Cài đặt bảo mật phi trạng thái dùng Spring Security:
1. Trong gói `vn.nganhang.chuyenkhoan`, cài `JwtService` gồm `sign(String sub, String role, long expEpochSec)` (tạo JWT phần tải JSON `{"sub":"...","role":"...","exp":...}`) và `verify(String token)` kiểm chữ ký `HmacSHA256` kèm hạn `exp` (so sánh cố định thời gian an toàn); kèm bộ lọc `JwtAuthFilter` (`OncePerRequestFilter`) gắn quyền `"ROLE_" + role` vào `SecurityContextHolder` (sai thì `clearContext()`).
2. `SecurityConfig` đặt `SessionCreationPolicy.STATELESS`, chỉ cho phép vai trò `ROLE_TELLER` gọi `POST /api/v1/transfers` (`VIEWER` trả `403`, thiếu/hỏng/hết hạn JWT trả `401`).
3. `SecureTransferController` kiểm quyền sở hữu chủ tài khoản nguồn (an sở hữu `TK-AN`, binh sở hữu `TK-BINH`): gọi chéo sang tài khoản người khác trả `403` (chống BOLA).

Chấm tự động:
```bash
bash labs/cham.sh SPB L08 duong_dan/du_an_cua_ban
```
