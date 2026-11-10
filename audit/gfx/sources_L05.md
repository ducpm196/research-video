# Nguồn bài GFX L05 — Bộ đệm độ sâu: độ chính xác không đều và hiện tượng giành điểm ảnh

Đọc và đối chiếu 2026-11-03. Công thức độ sâu chuẩn hoá phi tuyến theo `1/z`, khoảng cách độ sâu nhỏ nhất phân biệt được `Δz` tỉ lệ với `z² / n`, và hiện tượng giành điểm ảnh giữa hai mặt gần nhau dựa trên giáo trình chuẩn, kết hợp kiểm chứng bằng `alg.gfx_depth_norm` và `alg.gfx_depth_step` trong `tools/checklib.py` và `audit/verify_plan_curricula.py` (`VER GFX:L05`).

**[RTR4]** T. Akenine-Möller, E. Haines, N. Hoffman, *Real-Time Rendering*, 4th ed., CRC Press (2018), Section 2.5 “The Merging Stage” & Section 23.7 “Depth Buffering”.

> Ghi chú 2026-11-09 (đọc mẫu độc lập): tên mục có thể lệch — người đọc nhớ RTR4 §2.5 là “Pixel Processing” (Merging là §2.5.2) và §23.7 là “Depth Culling, Testing, and Compression”. Chưa mở được sách: NOT_VERIFIED. Các công thức trong bài vẫn được `checks` tính lại độc lập.

| Nội dung dẫn (NOT_VERIFIED nguyên văn: chưa đối chiếu với bản sách/bài báo, có thể là diễn giải; ghi chú thêm 2026-11-09) | Dùng ở |
|---|---|
| “In the Z-buffer algorithm, each pixel stores the depth of the closest fragment seen so far; a new fragment overwrites the color and depth buffers only if its depth is smaller.” | cơ chế bộ đệm độ sâu giải quyết vật che khuất theo từng điểm ảnh |
| “Because standard perspective projection maps z non-linearly as d = f(z − n) / (z(f − n)), depth precision is heavily concentrated near the near plane n and degrades quadratically with distance z.” | công thức độ sâu chuẩn hoá và sự phân bố bit dồn sát camera |
| “When two surfaces at distance z are separated by less than the minimum resolvable depth step Δz ≈ z²(f − n)/(f · n · 2^b), rounding causes them to alternate randomly across pixels, an artifact known as Z-fighting. Pushing the near plane n outward improves precision far more effectively than pulling the far plane f inward.” | ví dụ số: 24 bit, gần 0,1, xa 1000 ở z = 100 m cho Δz ≈ 6 mm; đặt gần = 1 giảm còn ≈ 0,6 mm |

**[FCG5]** S. Marschner, P. Shirley, *Fundamentals of Computer Graphics*, 5th ed., CRC Press (2021), Section 8.2.3 “The Z-Buffer”.

| Nội dung dẫn (NOT_VERIFIED nguyên văn: chưa đối chiếu với bản sách/bài báo, có thể là diễn giải; ghi chú thêm 2026-11-09) | Dùng ở |
|---|---|
| “Transparent surfaces cannot simply overwrite the depth buffer in arbitrary order; blending requires sorting or order-independent techniques.” | lỗi thường gặp khi vẽ vật bán trong suốt với bộ đệm độ sâu |

## Điều KHÔNG dạy / NOT_VERIFIED
- Chi tiết thuật toán nén bộ đệm độ sâu không mất mát trong phần cứng thương mại (Hi-Z / HyperZ): NOT_VERIFIED chi tiết bản quyền phần cứng, không dạy trong bài này (hiệu năng tô đè và độ sâu đảo sẽ học ở bài 11 và bài 12).
- Các thông số minh hoạ (`n = 0,1 m`, `f = 1000 m`, `z = 100 m`, `24 bit`) là SỐ MINH HOẠ toán học đã kiểm bằng `checks`.

## Đối chiếu nguồn mở (đợt C, 2026-11-09)
- N. Reed, “Depth Precision Visualized”, NVIDIA Developer, https://developer.nvidia.com/content/depth-precision-visualized (truy cập 2026-11-09, trang không ghi ngày): nguyên văn “It's also easy to see why the near plane has such a profound effect on depth precision” và “pushing the far plane all the way out to infinity doesn't have that much effect” — khớp kết luận đẩy mặt gần hiệu quả hơn kéo mặt xa (bài: f từ 1000 xuống 200 m chỉ cải thiện 0,0024 mm).
- [GL46] The OpenGL Graphics System: A Specification, Version 4.6 (Core Profile), Khronos, bản ngày 5/5/2022, https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf (tải và đọc 2026-11-09) §17.3.4 “Depth Buffer Test”: phép so độ sâu (LESS, LEQUAL…) loại mảnh khi so sánh thất bại — khớp cơ chế ghi đè khi d_mới < Z_đệm.
- Đợt C sửa trong bài: “cải thiện 0,003 mm” (trừ hai số đã làm tròn) → 0,0024 mm; “độ chính xác tỉ lệ với z²/n” → “bước độ sâu (sai số) tỉ lệ với z²/n” (độ chính xác tỉ lệ nghịch); “năm ký hiệu” → sáu; màn hình “cách nhau cả gang tay” khác lời đọc “nửa mét” → nửa mét.
- Các câu “trích” [RTR4]/[FCG5] ở bảng trên vẫn **NOT_VERIFIED nguyên văn**; tên mục §2.5/§23.7 chưa kiểm được.
