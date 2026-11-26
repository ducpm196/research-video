# Lab PRJ L04 (Đạt / Chưa đạt theo `labs/PRJ/SPEC.md`) — Bộ giải Đồ thị luồng tiền & Hồi quy tuyến tính

Viết chương trình Python đọc dữ liệu động từ chuẩn vào (`stdin`, bỏ qua dòng trống hoặc `#`) theo đúng khuôn 5 loại bản ghi:
- `QUERY <src> <dst>`: cặp nút nguồn và đích cần tìm chi phí thấp nhất.
- `DIRECT <chi_phi>`: chi phí tuyến đi thẳng tham khảo để tính tỉ lệ phần trăm tiết kiệm `(direct - min_cost) / direct * 100`. Nếu `direct <= 0` thì `saved_pct=0.0%`.
- `EDGE <u> <v> <w>`: cạnh có hướng của đồ thị chính (nếu gặp `w < 0` ở đồ thị thử riêng thì chặn). Dùng `heapq` đạt độ phức tạp `O((V + E) log V)` cho đồ thị thưa hàng nghìn nút.
- `PROBE <u> <v> <w>`: tập cạnh kiểm tra riêng quy tắc từ chối cạnh âm (`neg_rejected=1` nếu tồn tại bất kỳ cạnh `PROBE` có `w < 0`, ngược lại `neg_rejected=0`).
- `POINT <x> <y>`: điểm dữ liệu dùng cho hồi quy tuyến tính công thức đóng `y = w*x + b` (cực tiểu hoá `MSE`). Nếu mẫu số phương sai `sum((x - mx)^2) == 0`, đặt an toàn `ols_w=0.0`, `ols_b=round(my, 1)`.

Đọc `labs/PRJ/L04/du_lieu.txt` qua `stdin` và in đúng 3 dòng định dạng:
```
min_cost=<nguyen> saved_pct=<x.x%>
neg_rejected=<0|1>
ols_w=<w.w> ols_b=<b.b> mse=<m.mm>
```

Lưu ý: máy chấm chạy thêm các ca ẩn (biên mẫu số 0, không có cạnh âm, đồ thị hàng nghìn nút) trong `ca_an/`.

Chấm tự động:
```bash
bash labs/cham.sh PRJ L04 duong_dan/bai_cua_ban.py
```
