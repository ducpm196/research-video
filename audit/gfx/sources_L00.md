# Nguồn bài GFX L00 — Đường ống kết xuất: từ đỉnh tới điểm ảnh, và ngân sách một khung hình

Đọc và đối chiếu 2026-11-03. Các định nghĩa tầng đường ống kết xuất, tốc độ điểm ảnh và ngân sách thời gian khung hình dựa trên giáo trình chuẩn về đồ hoạ thời gian thực, kết hợp kiểm chứng độc lập bằng `alg.gfx_frame_budget_ms` và `alg.gfx_pixels_per_sec` trong `tools/checklib.py` và `audit/verify_plan_curricula.py` (`VER GFX:L00`).

**[RTR4]** T. Akenine-Möller, E. Haines, N. Hoffman, *Real-Time Rendering*, 4th ed., CRC Press (2018), Chapter 2 “The Graphics Rendering Pipeline” & Chapter 18 “Pipeline Optimization”.

| Nội dung dẫn (NOT_VERIFIED nguyên văn: chưa đối chiếu với bản sách/bài báo, có thể là diễn giải; ghi chú thêm 2026-11-09) | Dùng ở |
|---|---|
| “The main function of the pipeline is to generate, or render, a two-dimensional image, given a virtual camera, three-dimensional objects, light sources, and more.” | mở đầu & định nghĩa đường ống kết xuất |
| “The geometry stage (which contains Vertex Shading, Projection, Clipping, and Screen Mapping) … The rasterizer stage (Triangle Setup, Triangle Traversal) … The pixel stage (Pixel Shading, Merging).” | 5 bước trên màn hình: xử lý đỉnh, ghép nguyên thuỷ, raster hoá, tô mảnh, ghép ảnh |
| “Average frame rate is a coarse metric; a single long frame causes a noticeable hitch or stutter even when the average frames per second remains high. Frame time (in milliseconds per frame) is a linear and much more reliable measure for real-time rendering.” | lỗi 1 & lỗi người đi làm: khung hình trễ một lần (17 ms → 33,33 ms, ghi chú cũ ghi 34 ms) gây giật dù trung bình vẫn 60 khung/giây |

**[FCG5]** S. Marschner, P. Shirley, *Fundamentals of Computer Graphics*, 5th ed., CRC Press (2021), Chapter 8 “The Graphics Pipeline”.

| Nội dung dẫn (NOT_VERIFIED nguyên văn: chưa đối chiếu với bản sách/bài báo, có thể là diễn giải; ghi chú thêm 2026-11-09) | Dùng ở |
|---|---|
| “In a pipeline, each stage processes a stream of data elements and passes the results on to the next stage. The total throughput is determined by the slowest stage.” | trực giác dây chuyền và nút cổ chai của đường ống |

## Điều KHÔNG dạy / NOT_VERIFIED
- Chi tiết kiến trúc phần cứng cụ thể của từng hãng (số nhân xử lý, bộ lập lịch phần cứng trên thẻ đồ hoạ thương mại): NOT_VERIFIED từ tài liệu vi kiến trúc đóng, không dạy trong bài.
- Các con số cụ thể trong bài (màn hình 1920 × 1080 ở 60 và 120 khung mỗi giây, kính thực tế ảo 2160 × 2160 mỗi mắt ở 90 khung mỗi giây, 59 khung 16 ms + 1 khung 56 ms) là SỐ MINH HOẠ toán học được kiểm tự động bằng `checks`.
- Tên riêng các giao diện lập trình (`OpenGL`, `DirectX`, `Vulkan`) chỉ hiện trên màn hình ở phần ghi chú nếu cần; lời đọc hoàn toàn dùng tiếng Việt tự nhiên.

## Đối chiếu nguồn mở (đợt C, 2026-11-09)
- Không mở được bản [RTR4] / [FCG5]: bốn câu “trích” ở bảng trên vẫn **NOT_VERIFIED nguyên văn** (coi là diễn giải). Bài không còn dựa vào câu [FCG5] “throughput is determined by the slowest stage”: cảnh ôn nền nay tự chứng minh bằng bảng thời gian ba khung qua ba tầng 2, 5, 3 ms (khung xong lúc 10, 15, 20 ms → cách nhau 5 ms = max), có `checks`.
- Cột “Dùng ở” dòng 3 ghi “17 ms → 34 ms”: bài thật dùng 33,33 ms (2 × 16,67), giữ nguyên bài; sửa ghi chú này.
- [GL46] The OpenGL Graphics System: A Specification, Version 4.6 (Core Profile), Khronos, bản ngày 5/5/2022, https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf (tải và đọc 2026-11-09), mục lục chương: 11 “Programmable Vertex Processing”, 13 “Fixed-Function Vertex Post-Processing” (13.7 cắt, 13.8 chia phối cảnh và khung nhìn), 14 “Fixed-Function Primitive Assembly and Rasterization”, 15 “Programmable Fragment Processing”, 17 “Writing Fragments and Samples to the Framebuffer” (17.3.4 kiểm độ sâu, 17.3.6 trộn màu) — thứ tự khớp năm tầng trên màn hình (xử lý đỉnh → ghép nguyên thuỷ và cắt → raster hoá → tô mảnh → ghép ảnh). Đây là đối chiếu cấu trúc, không phải câu trích.
