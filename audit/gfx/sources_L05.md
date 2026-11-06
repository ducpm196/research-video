# Nguồn bài GFX L05 — Bộ đệm độ sâu: độ chính xác không đều và hiện tượng giành điểm ảnh

Đọc và đối chiếu 2026-11-03. Công thức độ sâu chuẩn hoá phi tuyến theo `1/z`, khoảng cách độ sâu nhỏ nhất phân biệt được `Δz` tỉ lệ với `z² / n`, và hiện tượng giành điểm ảnh giữa hai mặt gần nhau dựa trên giáo trình chuẩn, kết hợp kiểm chứng bằng `alg.gfx_depth_norm` và `alg.gfx_depth_step` trong `tools/checklib.py` và `audit/verify_plan_curricula.py` (`VER GFX:L05`).

**[RTR4]** T. Akenine-Möller, E. Haines, N. Hoffman, *Real-Time Rendering*, 4th ed., CRC Press (2018), Section 2.5 “The Merging Stage” & Section 23.7 “Depth Buffering”.

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “In the Z-buffer algorithm, each pixel stores the depth of the closest fragment seen so far; a new fragment overwrites the color and depth buffers only if its depth is smaller.” | cơ chế bộ đệm độ sâu giải quyết vật che khuất theo từng điểm ảnh |
| “Because standard perspective projection maps z non-linearly as d = f(z − n) / (z(f − n)), depth precision is heavily concentrated near the near plane n and degrades quadratically with distance z.” | công thức độ sâu chuẩn hoá và sự phân bố bit dồn sát camera |
| “When two surfaces at distance z are separated by less than the minimum resolvable depth step Δz ≈ z²(f − n)/(f · n · 2^b), rounding causes them to alternate randomly across pixels, an artifact known as Z-fighting. Pushing the near plane n outward improves precision far more effectively than pulling the far plane f inward.” | ví dụ số: 24 bit, gần 0,1, xa 1000 ở z = 100 m cho Δz ≈ 6 mm; đặt gần = 1 giảm còn ≈ 0,6 mm |

**[FCG5]** S. Marschner, P. Shirley, *Fundamentals of Computer Graphics*, 5th ed., CRC Press (2021), Section 8.2.3 “The Z-Buffer”.

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “Transparent surfaces cannot simply overwrite the depth buffer in arbitrary order; blending requires sorting or order-independent techniques.” | lỗi thường gặp khi vẽ vật bán trong suốt với bộ đệm độ sâu |

## Điều KHÔNG dạy / NOT_VERIFIED
- Chi tiết thuật toán nén bộ đệm độ sâu không mất mát trong phần cứng thương mại (Hi-Z / HyperZ): NOT_VERIFIED chi tiết bản quyền phần cứng, không dạy trong bài này (hiệu năng tô đè và độ sâu đảo sẽ học ở bài 11 và bài 12).
- Các thông số minh hoạ (`n = 0,1 m`, `f = 1000 m`, `z = 100 m`, `24 bit`) là SỐ MINH HOẠ toán học đã kiểm bằng `checks`.
