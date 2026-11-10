# Nguồn bài GFX L04 — Raster hoá tam giác: hàm cạnh và toạ độ trọng tâm

Đọc và đối chiếu 2026-11-03. Phương pháp raster hoá song song bằng hàm cạnh của Pineda (1988), toạ độ trọng tâm theo tỉ lệ diện tích có dấu, và quy tắc cạnh trên–trái dựa trên bài báo gốc và giáo trình chuẩn, kết hợp kiểm chứng bằng `alg.gfx_barycentric` trong `tools/checklib.py` và `audit/verify_plan_curricula.py` (`VER GFX:L04`).

**[PIN88]** J. Pineda, “A Parallel Algorithm for Polygon Rasterization”, *Computer Graphics (Proceedings of SIGGRAPH ’88)*, Vol. 22, No. 4, pp. 17–20 (1988).

| Nội dung dẫn (NOT_VERIFIED nguyên văn: chưa đối chiếu với bản sách/bài báo, có thể là diễn giải; ghi chú thêm 2026-11-09) | Dùng ở |
|---|---|
| “An edge function E(x, y) = (x − X0) dY − (y − Y0) dX is linear in x and y, and divides the plane into three regions: points to the left, points to the right, and points exactly on the line.” | suy ra công thức hàm cạnh và tính chất cộng thêm bước hằng số khi dịch 1 điểm ảnh |
| “A point lies inside a convex polygon if and only if the edge functions for all oriented edges have the same non-negative sign, allowing many pixels to be tested in parallel.” | kiểm điểm nằm trong tam giác bằng dấu của ba hàm cạnh |

**[FCG5]** S. Marschner, P. Shirley, *Fundamentals of Computer Graphics*, 5th ed., CRC Press (2021), Section 2.7 “Triangles” & Section 8.1.2 “Triangle Rasterization”.

| Nội dung dẫn (NOT_VERIFIED nguyên văn: chưa đối chiếu với bản sách/bài báo, có thể là diễn giải; ghi chú thêm 2026-11-09) | Dùng ở |
|---|---|
| “Barycentric coordinates (α, β, γ) express any point p in the plane of triangle (a, b, c) as p = α a + β b + γ c with α + β + γ = 1, and equal the signed area ratios of the subtriangles.” | định nghĩa toạ độ trọng tâm, kiểm tổng bằng 1, nội suy thuộc tính và ví dụ tam giác (0, 0), (4, 0), (0, 4) |
| “To avoid drawing pixels on a shared edge twice or leaving gaps between adjacent triangles, a tie-breaking rule such as the top-left rule assigns ownership of boundary pixels to exactly one triangle.” | lỗi người đi làm: điểm ảnh nằm trên cạnh chung của hai tam giác và quy tắc trên–trái |

## Điều KHÔNG dạy / NOT_VERIFIED
- Kích thước ô gạch phần cứng cụ thể (ví dụ 8 × 8 hay 16 × 16 điểm ảnh trên từng dòng chip thương mại): NOT_VERIFIED từ tài liệu phần cứng đóng, chỉ dạy nguyên lý hộp bao và hàm cạnh tuyến tính.
- Tên riêng `Pineda` và `SIGGRAPH` chỉ hiện ở phần ghi chú nguồn trên màn hình nếu có; lời đọc (`say:`) hoàn toàn dùng thuật ngữ tiếng Việt “hàm cạnh” và “toạ độ trọng tâm” theo `lexicon_vi.GFX.yaml`.

## Đối chiếu nguồn mở (đợt C, 2026-11-09)
- [GL46] The OpenGL Graphics System: A Specification, Version 4.6 (Core Profile), Khronos, bản ngày 5/5/2022, https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf (tải và đọc 2026-11-09) §14.6.1 “Basic Polygon Rasterization”: (a) mặt trước/sau xác định theo dấu diện tích có dấu trong toạ độ cửa sổ, mặc định CCW là mặt trước; nguyên văn “Initially, culling is disabled” → lỗi 2 của bài đã sửa thành “khi bật chế độ loại mặt sau” (trước đó nói như luôn bị bỏ); (b) nguyên văn “if two polygons lie on either side of a common edge … on which a fragment center lies, then exactly one of the polygons results in the production of the fragment”; (c) toạ độ trọng tâm a + b + c = 1; (d) phương trình (14.10): độ sâu nội suy tuyến tính z = a·za + b·zb + c·zc trên màn hình — khớp ghi chú “trọng số trên màn hình dùng thẳng cho độ sâu chuẩn hoá”.
- Microsoft Learn, “Rasterization Rules” (Direct3D 11), https://learn.microsoft.com/en-us/windows/win32/direct3d11/d3d10-graphics-programming-guide-rasterizer-stage-rules (cập nhật 2026-09-08): nguyên văn “A top edge, is an edge that is exactly horizontal and is above the other edges … A left edge, is an edge that is not exactly horizontal and is on the left side of the triangle” và “The top-left rule ensures that adjacent triangles are drawn once.” Bảng quy tắc trên–trái của bài (trục y hướng lên, đỉnh ngược chiều kim đồng hồ: cạnh trái là cạnh đi xuống) tương đương.
- Các câu “trích” [PIN88]/[FCG5] ở bảng trên vẫn **NOT_VERIFIED nguyên văn**.
