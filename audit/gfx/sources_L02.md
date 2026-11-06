# Nguồn bài GFX L02 — Phép chiếu phối cảnh và phép chia cho w

Đọc và đối chiếu 2026-11-03. Phép chiếu phối cảnh bằng tam giác đồng dạng, ma trận chiếu đặt độ sâu vào thành phần `w`, và nội suy có hiệu chỉnh phối cảnh dựa trên giáo trình chuẩn, kết hợp kiểm chứng bằng `alg.gfx_persp_project` và `alg.gfx_persp_interp` trong `tools/checklib.py` và `audit/verify_plan_curricula.py` (`VER GFX:L02`).

**[FCG5]** S. Marschner, P. Shirley, *Fundamentals of Computer Graphics*, 5th ed., CRC Press (2021), Chapter 7 “Viewing” & Section 8.1.3 “Perspective Correct Interpolation”.

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “By similar triangles, a point (x, y, z) projects onto the image plane at distance f to x′ = f · x / z and y′ = f · y / z. Objects twice as far appear half as large.” | công thức chiếu phối cảnh và ví dụ số z = 4 so với z = 8 |
| “Because division by z is non-linear, a 4 × 4 matrix places z into the homogeneous coordinate w, deferring the perspective divide until after matrix multiplication.” | cơ chế đặt z vào w rồi thực hiện phép chia cho w |
| “Linear interpolation in screen space does not correspond to linear interpolation in 3D world space under perspective projection. Instead, 1/z and u/z vary linearly in screen space.” | lỗi người đi làm: nội suy tuyến tính trên màn hình làm méo kết cấu/thuộc tính; phải nội suy theo 1/z |

**[RTR4]** T. Akenine-Möller, E. Haines, N. Hoffman, *Real-Time Rendering*, 4th ed., CRC Press (2018), Section 4.7 “Projections” & Section 23.1.

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “Parallel lines in three-dimensional space that are not parallel to the image plane converge to a vanishing point as z approaches infinity.” | trực giác đường ray xe lửa hội tụ khi z tăng |

## Điều KHÔNG dạy / NOT_VERIFIED
- Lịch sử phần cứng thế hệ cũ những năm 1990 không có chia phối cảnh trên từng điểm ảnh: NOT_VERIFIED nguyên văn tài liệu kỹ thuật phần cứng máy chơi điện tử cụ thể, nên chỉ giải thích lỗi toán học và hiện tượng hình ảnh bị gãy đường chéo, không nêu tên máy thương mại.
- Các điểm minh hoạ `(2, 1, 4)`, `(2, 1, 8)`, đoạn thẳng có `z0 = 2`, `z1 = 6` là SỐ MINH HOẠ toán học đã kiểm bằng `checks`.
