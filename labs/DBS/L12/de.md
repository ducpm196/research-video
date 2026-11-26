# Lab DBS L12 — SQLite: tìm chu trình trên đồ thị ưu tiên bằng WITH RECURSIVE

Cơ sở dữ liệu có sẵn bảng `Edges(u INT, v INT)`. Đếm số cạnh và dùng CTE đệ quy `WITH RECURSIVE` tìm đường đi quay lại chính đỉnh xuất phát để kết luận lịch có khả tuần tự xung đột hay không.

In đúng 3 dòng: `edges=<d>`, `cycle_found=<0|1>`, `conflict_serializable=<0|1>`.
Chấm tự động: `bash labs/cham.sh DBS L12 duong_dan/bai_cua_ban.sql`
