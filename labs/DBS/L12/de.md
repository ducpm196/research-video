# Lab DBS L12 — SQLite: tìm chu trình trên đồ thị ưu tiên bằng WITH RECURSIVE

Cơ sở dữ liệu có sẵn bảng `Edges(u INT, v INT)`. Đếm số cạnh và dùng CTE đệ quy (`WITH RECURSIVE r(s,t,d) AS (SELECT u,v,1 FROM Edges UNION ALL SELECT r.s, e.v, r.d+1 FROM r JOIN Edges e ON r.t=e.u WHERE r.d < 8)`) kèm `EXISTS (SELECT 1 FROM r WHERE s=t)` để phát hiện chu trình và kết luận lịch có khả tuần tự xung đột hay không.

In đúng 3 dòng: `edges=<d>`, `cycle_found=<0|1>`, `conflict_serializable=<0|1>`.
Chấm tự động: `bash labs/cham.sh DBS L12 duong_dan/bai_cua_ban.sql`
