# Nguồn bài GFX L00 — Đường ống kết xuất: từ đỉnh tới điểm ảnh, và ngân sách một khung hình

Đọc và đối chiếu 2026-11-03. Các định nghĩa tầng đường ống kết xuất, tốc độ điểm ảnh và ngân sách thời gian khung hình dựa trên giáo trình chuẩn về đồ hoạ thời gian thực, kết hợp kiểm chứng độc lập bằng `alg.gfx_frame_budget_ms` và `alg.gfx_pixels_per_sec` trong `tools/checklib.py` và `audit/verify_plan_curricula.py` (`VER GFX:L00`).

**[RTR4]** T. Akenine-Möller, E. Haines, N. Hoffman, *Real-Time Rendering*, 4th ed., CRC Press (2018), Chapter 2 “The Graphics Rendering Pipeline” & Chapter 18 “Pipeline Optimization”.

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “The main function of the pipeline is to generate, or render, a two-dimensional image, given a virtual camera, three-dimensional objects, light sources, and more.” | mở đầu & định nghĩa đường ống kết xuất |
| “The geometry stage (which contains Vertex Shading, Projection, Clipping, and Screen Mapping) … The rasterizer stage (Triangle Setup, Triangle Traversal) … The pixel stage (Pixel Shading, Merging).” | 5 bước trên màn hình: xử lý đỉnh, ghép nguyên thuỷ, raster hoá, tô mảnh, ghép ảnh |
| “Average frame rate is a coarse metric; a single long frame causes a noticeable hitch or stutter even when the average frames per second remains high. Frame time (in milliseconds per frame) is a linear and much more reliable measure for real-time rendering.” | lỗi 1 & lỗi người đi làm: khung hình trễ một lần (17 ms → 34 ms) gây giật dù trung bình vẫn 60 khung/giây |

**[FCG5]** S. Marschner, P. Shirley, *Fundamentals of Computer Graphics*, 5th ed., CRC Press (2021), Chapter 8 “The Graphics Pipeline”.

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “In a pipeline, each stage processes a stream of data elements and passes the results on to the next stage. The total throughput is determined by the slowest stage.” | trực giác dây chuyền và nút cổ chai của đường ống |

## Điều KHÔNG dạy / NOT_VERIFIED
- Chi tiết kiến trúc phần cứng cụ thể của từng hãng (số nhân xử lý, bộ lập lịch phần cứng trên thẻ đồ hoạ thương mại): NOT_VERIFIED từ tài liệu vi kiến trúc đóng, không dạy trong bài.
- Các con số cụ thể trong bài (màn hình 1920 × 1080 ở 60 và 120 khung mỗi giây, kính thực tế ảo 2160 × 2160 mỗi mắt ở 90 khung mỗi giây, 59 khung 16 ms + 1 khung 56 ms) là SỐ MINH HOẠ toán học được kiểm tự động bằng `checks`.
- Tên riêng các giao diện lập trình (`OpenGL`, `DirectX`, `Vulkan`) chỉ hiện trên màn hình ở phần ghi chú nếu cần; lời đọc hoàn toàn dùng tiếng Việt tự nhiên.
