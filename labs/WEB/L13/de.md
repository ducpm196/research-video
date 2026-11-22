# Lab WEB L13 — Node.js thật: kiểm chứng hợp nhất không mất dữ liệu ở chế độ ngoại tuyến

Viết tập lệnh Node.js mô phỏng hai máy ngoại tuyến cùng thêm `'mua sua'` và `'goi me'` vào tập hợp gốc `{'lam bai'}`: kiểm tra hợp nhất hai chiều `merge(A, B)` và `merge(B, A)` đều cho kết quả y hệt (`3` mục), in đúng 3 dòng:
1. `merged_len=3`
2. `commutative=1`
3. `idempotent=1`

Chấm tự động:
```bash
bash labs/cham.sh WEB L13 duong_dan/bai_cua_ban.js
```
