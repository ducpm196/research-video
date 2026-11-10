# Nguồn bài GFX L01 — Biến đổi mô hình và góc nhìn bằng toạ độ thuần nhất

Đọc và đối chiếu 2026-11-03. Phép biến đổi thuần nhất, thứ tự nhân ma trận không giao hoán và quy tắc biến đổi pháp tuyến bằng nghịch đảo chuyển vị dựa trên giáo trình chuẩn, kết hợp kiểm chứng bằng `alg.gfx_rot2d`, `alg.gfx_trans2d`, `alg.gfx_apply2d` trong `tools/checklib.py` và `audit/verify_plan_curricula.py` (`VER GFX:L01`).

**[FCG5]** S. Marschner, P. Shirley, *Fundamentals of Computer Graphics*, 5th ed., CRC Press (2021), Chapter 6 “Transformation Matrices” & Section 6.2.2 “Transforming Normal Vectors”.

| Nội dung dẫn (NOT_VERIFIED nguyên văn: chưa đối chiếu với bản sách/bài báo, có thể là diễn giải; ghi chú thêm 2026-11-09) | Dùng ở |
|---|---|
| “Homogeneous coordinates append an extra coordinate w (1 for points, 0 for direction vectors) so that translation and linear transformations can be represented uniformly by matrix multiplication.” | ôn nền & giải mã ký hiệu toạ độ thuần nhất (x, y, 1) và vector hướng (x, y, 0) |
| “Matrix multiplication is not commutative: rotating then translating a point produces a different result from translating then rotating.” | ví dụ số: điểm (1, 0) quay 90° rồi tịnh tiến (2, 0) ra (2, 1); tịnh tiến rồi quay ra (0, 3) |
| “Surface normal vectors do not transform by the same matrix M as points when non-uniform scaling or shearing is present. Because t · n = 0 must hold after transformation, normals transform by the inverse transpose (M⁻¹)ᵀ.” | lỗi người đi làm & câu tự làm: biến đổi pháp tuyến bằng nghịch đảo chuyển vị khi co giãn không đều |

**[RTR4]** T. Akenine-Möller, E. Haines, N. Hoffman, *Real-Time Rendering*, 4th ed., CRC Press (2018), Section 4.1 “Basic Transforms” & Section 4.1.7 “Normal Transform”.

| Nội dung dẫn (NOT_VERIFIED nguyên văn: chưa đối chiếu với bản sách/bài báo, có thể là diễn giải; ghi chú thêm 2026-11-09) | Dùng ở |
|---|---|
| “The view transform places the camera at the origin and aims it along a canonical axis; equivalently, it applies the inverse of the camera’s world transform to the scene.” | khái niệm biến đổi góc nhìn là nghịch đảo của biến đổi đặt camera |

## Điều KHÔNG dạy / NOT_VERIFIED
- Quy ước lưu ma trận theo cột hay theo hàng trong từng thư viện phần mềm cụ thể: chỉ nhắc quy ước toán học nhất quán trong bài (nhân vector cột ở bên phải, tác động từ phải sang trái), không đi sâu vào lịch sử từng thư viện (NOT_VERIFIED chi tiết lịch sử thiết kế API).
- Các toạ độ minh hoạ trong bài (điểm (1, 0), tịnh tiến (2, 0), co giãn ngang gấp 2) là SỐ MINH HOẠ toán học đã kiểm bằng `checks`.

## Đối chiếu nguồn mở (đợt C, 2026-11-09)
- [PBR4] M. Pharr, W. Jakob, G. Humphreys, Physically Based Rendering 4e, bản trực tuyến https://pbr-book.org/4ed/Geometry_and_Transformations/Applying_Transformations (truy cập 2026-11-09, no revision given), §3.10.3 “Normals”: đọc được nguyên văn “we see that normals must be transformed by the inverse transpose of the transformation matrix”; phần dẫn dắt mở đầu bằng “Because the normal vector n and any tangent vector t on the surface are orthogonal by construction” rồi suy ra SᵀM = I, S = (M⁻¹)ᵀ. Khớp cảnh mới “Vì sao lại là nghịch đảo chuyển vị?” của bài (đợt C thêm).
- §3.10.2 (vector): “the multiplication of the matrix and the column vector is simplified since the implicit homogeneous w coordinate is zero” — khớp quy ước w = 0 cho vector hướng.
- Các câu “trích” [FCG5]/[RTR4] ở bảng trên vẫn **NOT_VERIFIED nguyên văn** (không mở được sách).
