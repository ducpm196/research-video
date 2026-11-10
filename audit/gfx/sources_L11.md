# Nguồn bài GFX L11 — Hiệu năng thời gian thực: tô đè, số lệnh vẽ và mức chi tiết

Đọc và đối chiếu 2026-11-03. Nhãn dùng trong `source` của bài `lessons/gfx/L11_hieu_nang.yaml`.

## [AM18] T. Akenine-Möller, E. Haines, N. Hoffman, A. Pesce, M. Iwanicki, S. Hillaire, “Real-Time Rendering” (4th ed., A K Peters/CRC Press, 2018), chương 18 (Pipeline Optimization) & chương 19 (Acceleration Algorithms)
- **Tô đè (*overdraw*) và kiểm độ sâu sớm (*Early-Z*):**
  - Nếu một điểm ảnh trên màn hình $W \times H$ bị trung bình $k$ tam giác phủ lên và được vẽ từ xa tới gần (sau ra trước), cả $k$ mảnh đều vượt qua phép kiểm độ sâu tại thời điểm vẽ nên bộ tô mảnh phải chạy đủ $k \cdot W \cdot H$ lần (ở $1920 \times 1080$ với $k = 3$: $3 \cdot 2\,073\,600 = 6\,220\,800$ mảnh).
  - Phần cứng hiện đại hỗ trợ kiểm độ sâu sớm (*early depth test*) trước khi chạy bộ tô mảnh cho các vật đục không tự sửa độ sâu trong bộ tô mảnh. Khi sắp xếp các vật đục vẽ từ gần ra xa (trước ra sau), vật gần nhất ghi độ sâu trước nên các mảnh bị che phía sau bị loại ngay từ đầu, đưa số mảnh phải tô về gần $1 \cdot W \cdot H = 2\,073\,600$.
- **Nút cổ chai đường ống (*pipeline bottlenecks*) và số lệnh vẽ (*draw calls*):**
  - Đường ống kết xuất là chuỗi nối tiếp giữa bộ xử lý trung tâm (chuẩn bị trạng thái, gửi lệnh vẽ), tầng xử lý đỉnh, tầng tô mảnh và băng thông bộ nhớ; tốc độ khung hình bị quyết định bởi tầng chậm nhất.
  - Gửi hàng nghìn lệnh vẽ nhỏ lẻ mỗi khung hình làm bộ xử lý trung tâm tốn chi phí chuyển trạng thái và giao tiếp trình điều khiển dù bộ xử lý đồ hoạ đang rảnh; giải pháp là gộp lưới tĩnh hoặc vẽ nhiều bản sao trong một lệnh (*batching / instancing*).
- **Mức chi tiết (*Level of Detail — LOD*):**
  - Một mô hình nhiều tam giác khi ở xa chỉ phủ vài chục điểm ảnh trên màn hình: nhiều tam giác rơi vào cùng một điểm ảnh vừa tốn xử lý đỉnh vừa gây răng cưa hình học và giảm hiệu quả xử lý theo ô $2 \times 2$ của bộ tô mảnh. Thay bằng các phiên bản ít tam giác hơn theo diện tích chiếu hoặc khoảng cách giữ nguyên hình dáng nhìn thấy mà giảm mạnh chi phí đỉnh.

## Điều KHÔNG dạy / NOT_VERIFIED
- Không dạy chi tiết thuật toán tạo lưới thu gọn tự động bằng sai số bậc hai (Garland & Heckbert 1997, QEM) hay hệ thống cụm tam giác ảo hoá (*meshlets / Nanite*).
- Các con số thời gian xử lý từng tầng (ví dụ: bộ xử lý trung tâm 14 ms, xử lý đỉnh 4 ms, tô mảnh 6 ms) là SỐ MINH HOẠ để thực hành chẩn đoán nút cổ chai.

## Đối chiếu (đợt C, 2026-11-09)
- Đợt C viết lại phần “định luật điểm nghẽn” (trước đây dẫn tên khoá khác): ví dụ ba công đoạn 4, 2, 6 ms, công đoạn sau chờ công đoạn trước → khung xong lúc 12, 18, 24 ms, cách nhau 6 ms = max; giảm công đoạn 2 ms không đổi gì, giảm công đoạn 6 → 4 ms thì khung ra mỗi 4 ms (có `checks`). Lập luận là mô hình dây chuyền cơ bản, tính tay được, không cần nguồn ngoài.
