# Lab SPB L07 — OpenAPI 3 (`springdoc 3.2.1`), phân trang con trỏ & phiên bản v1/v2

Mở tài liệu hợp đồng API chuẩn OpenAPI 3 và phân trang con trỏ:
1. Gắn `springdoc-openapi-starter-webmvc-ui:3.2.1` để `GET /v3/api-docs` xuất lược đồ cho `/api/v1/transfers` và `/api/v2/transfers`.
2. `GET /api/v1/transfers?cursor=5&limit=3` lọc `id > cursor` (không `>=`, không `OFFSET`) và trả `nextCursor = 8`, `hasMore = true`.
3. `POST /api/v2/transfers` chấp nhận yêu cầu không gửi trường `channel` (mặc định `"MOBILE"`) để giữ tương thích ngược.

Chấm tự động:
```bash
bash labs/cham.sh SPB L07 duong_dan/du_an_cua_ban
```
