# Lab DBS L12 — SQLite thật: tìm chu trình trên đồ thị ưu tiên bằng CTE đệ quy (WITH RECURSIVE)

Viết tập lệnh SQLite biểu diễn cạnh xung đột `Edges(u INT, v INT)` cho lịch `R1(A) W2(A) R2(B) W1(B)`: cạnh `(1,2)` và `(2,1)`. Dùng CTE đệ quy (`WITH RECURSIVE`, truy vấn gọi lại chính nó) kiểm tra có đường đi từ `u` quay lại chính `u` (`cycle_found=1`), in đúng 3 dòng:
1. `edges=2`
2. `cycle_found=1`
3. `conflict_serializable=0`

Chấm tự động:
```bash
bash labs/cham.sh DBS L12 duong_dan/bai_cua_ban.sql
```
