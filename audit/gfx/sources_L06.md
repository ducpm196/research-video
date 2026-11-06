# Nguồn bài GFX L06 — Chiếu sáng cục bộ: khuếch tán Lambert và phản xạ Blinn–Phong

Đọc và đối chiếu 2026-11-03. Mô hình chiếu sáng cục bộ gồm thành phần môi trường, khuếch tán tỉ lệ với cô-sin góc tới và phản xạ bóng sáng dùng vector nửa đường dựa trên hai bài báo kinh điển của Bùi Tường Phong (1975) và James F. Blinn (1977) cùng giáo trình chuẩn, kết hợp kiểm chứng bằng `alg.gfx_lambert` và `alg.gfx_blinn_spec` trong `tools/checklib.py` và `audit/verify_plan_curricula.py` (`VER GFX:L06`).

**[PHO75]** Bui Tuong Phong, “Illumination for Computer Generated Pictures”, *Communications of the ACM*, Vol. 18, No. 6, pp. 311–317 (June 1975).

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “The shading of a point on a surface is computed as the sum of an ambient term, a diffuse reflection term proportional to the cosine of the angle of incidence, and a specular reflection term raised to a power n representing the glossiness of the surface.” | ba thành phần của mô hình chiếu sáng cục bộ và vai trò số mũ độ bóng s |
| “By interpolating the surface normal vector across the polygon and evaluating the shading equation at each picture element, smooth highlights are obtained on curved surfaces approximated by polygons.” | nội suy pháp tuyến qua tam giác và lỗi quên chuẩn hoá lại sau khi nội suy |

**[BLI77]** J. F. Blinn, “Models of Light Reflection for Computer Synthesized Pictures”, *Computer Graphics (Proceedings of SIGGRAPH ’77)*, Vol. 11, No. 2, pp. 192–198 (July 1977).

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “Define the unit vector H = (L + V) / |L + V| halfway between the light direction L and the viewer direction V. The specular intensity is computed from (N · H)^s, avoiding the per-pixel reflection vector computation.” | định nghĩa vector nửa đường h và công thức bóng sáng max(0, n · h)^s |

**[FCG5]** S. Marschner, P. Shirley, *Fundamentals of Computer Graphics*, 5th ed., CRC Press (2021), Chapter 10 “Surface Shading”.

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “Diffuse reflection follows Lambert’s cosine law: the irradiance on a surface element is proportional to max(0, n · l), where n and l are unit vectors.” | công thức khuếch tán max(0, n · l) và ví dụ n = (0, 0, 1), l = (0; 0,6; 0,8) → 0,8 |

## Điều KHÔNG dạy / NOT_VERIFIED
- Chi tiết hàm phân bố vi bề mặt Torrance–Sparrow đầy đủ trong bài báo của Blinn 1977: bài 6 chỉ dạy dạng luỹ thừa `(n · h)^s` dùng trong đường ống thời gian thực; mô hình dựa trên vật lý và bảo toàn năng lượng sẽ dạy ở bài 10 và bài 13.
- Quy tắc phát âm: tên tiếng Việt **Bùi Tường Phong** đọc tự nhiên; các tên `Lambert`, `Blinn`, `SIGGRAPH` chỉ hiện trên màn hình, lời đọc (`say:`) dùng tiếng Việt “khuếch tán đều theo cô-sin góc tới” và “mô hình vector nửa đường” theo `lexicon_vi.GFX.yaml`.
