# Nguồn bài GFX L03 — Cắt, toạ độ thiết bị chuẩn hoá và phép biến đổi khung nhìn

Đọc và đối chiếu 2026-11-03. Quy trình cắt nguyên thuỷ trong không gian thuần nhất trước khi chia cho `w`, hệ toạ độ thiết bị chuẩn hoá `[-1, 1]` và phép biến đổi khung nhìn sang điểm ảnh dựa trên giáo trình chuẩn, kết hợp kiểm chứng bằng `alg.gfx_ndc_to_pixel` trong `tools/checklib.py` và `audit/verify_plan_curricula.py` (`VER GFX:L03`).

**[FCG5]** S. Marschner, P. Shirley, *Fundamentals of Computer Graphics*, 5th ed., CRC Press (2021), Section 8.1.4 “Clipping” & Section 7.1 “Viewport Transformation”.

| Nội dung dẫn (NOT_VERIFIED nguyên văn: chưa đối chiếu với bản sách/bài báo, có thể là diễn giải; ghi chú thêm 2026-11-09) | Dùng ở |
|---|---|
| “Clipping must be performed in homogeneous coordinates before the perspective divide by w. If a line segment or triangle straddles the eye plane w = 0, points behind the camera have w < 0 and dividing by w flips their signs, inverting the primitive across the screen.” | lỗi người đi làm & câu hỏi trọng tâm: vì sao phải cắt trước khi chia cho w |
| “In homogeneous clip coordinates, a point is inside the canonical view volume when −w ≤ x ≤ w, −w ≤ y ≤ w, and −w ≤ z ≤ w.” | điều kiện cắt trong không gian thuần nhất trước khi chia |
| “The viewport transformation maps normalized device coordinates in [−1, 1] to pixel coordinates in [0, width] × [0, height] via x_pixel = (x_ndc + 1)/2 · width.” | công thức đổi toạ độ chuẩn hoá sang chỉ số điểm ảnh và ví dụ x = 0,5 → 1440 |

**[RTR4]** T. Akenine-Möller, E. Haines, N. Hoffman, *Real-Time Rendering*, 4th ed., CRC Press (2018), Section 2.3.3 “Clipping” & Section 2.3.4 “Screen Mapping”.

| Nội dung dẫn (NOT_VERIFIED nguyên văn: chưa đối chiếu với bản sách/bài báo, có thể là diễn giải; ghi chú thêm 2026-11-09) | Dùng ở |
|---|---|
| “Primitives partially inside the view volume require clipping, generating new vertices at the boundary intersection by linear interpolation in clip space.” | công thức tìm giao điểm cắt biên theo tham số nội suy t |

## Điều KHÔNG dạy / NOT_VERIFIED
- Khác biệt chi tiết giữa miền độ sâu chuẩn hoá `[-1, 1]` và `[0, 1]` của từng giao diện lập trình: chỉ nêu quy ước chuẩn `[-1, 1]` cho toạ độ ngang/dọc theo giáo án `curriculum/gfx.yaml`, không đọc chữ viết tắt `NDC`, `OpenGL`, `DirectX`, `Vulkan` trong lời giảng (`say:`).
- Các số minh hoạ khung hình `1920`, `1280`, điểm trước/sau camera là SỐ MINH HOẠ toán học đã kiểm bằng `checks`.

## Đối chiếu nguồn mở (đợt C, 2026-11-09)
- [GL46] The OpenGL Graphics System: A Specification, Version 4.6 (Core Profile), Khronos, bản ngày 5/5/2022, https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf (tải và đọc 2026-11-09) §13.7 “Primitive Clipping”: nguyên văn “In clip coordinates, the view volume is defined by −wc ≤ xc ≤ wc, −wc ≤ yc ≤ wc, zmin ≤ zc ≤ wc”, với zmin = −wc (chế độ NEGATIVE_ONE_TO_ONE) hoặc 0 (ZERO_TO_ONE). Bài chỉ dạy điều kiện cho x, y và mặt gần dạng w = w_gần (với ma trận của bài w = z) — đúng, nhưng câu [FCG5] “−w ≤ z ≤ w” ở bảng trên chỉ đúng cho quy ước [−1, 1].
- §13.8.1 “Controlling the Viewport”: xw = (px/2)·xd + ox, với px là bề rộng và ox là tâm khung nhìn; khi khung nhìn bắt đầu ở 0 thì ox = px/2, cho xw = (xd + 1)/2 · px — đúng công thức bài (1440 với xd = 0,5, px = 1920).
- Đợt C thêm ghi chú: 0 và 1920 là toạ độ hai mép; cột điểm ảnh đánh số 0…1919, tâm ở i + 0,5 (cùng §14.6.1: “data associated with a fragment must be sampled at the fragment's center”).
- Các câu “trích” [FCG5]/[RTR4] ở bảng trên vẫn **NOT_VERIFIED nguyên văn**.
