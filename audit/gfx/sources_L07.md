# Nguồn bài GFX L07 — Kết cấu và lấy mẫu: nội suy song tuyến, mipmap, răng cưa

Đọc và đối chiếu 2026-11-03. Nhãn dùng trong `source` của bài `lessons/gfx/L07_ket_cau.yaml`.

## [WI83] L. Williams, “Pyramidal Parametrics”, Computer Graphics (SIGGRAPH '83 Proceedings), Vol. 17, No. 3, pp. 1–11 (1983)
- Khái niệm *mipmap* (*multum in parvo* — “nhiều thứ trong một chỗ nhỏ”): chuỗi ảnh kết cấu được lọc trước ở các độ phân giải giảm nửa liên tiếp ($N \times N$, $\frac{N}{2} \times \frac{N}{2}$, …, $1 \times 1$), tổng cộng $\log_2 N + 1$ mức cho kết cấu vuông kích thước lũy thừa của 2.
- Chi phí bộ nhớ tăng thêm theo cấp số nhân công bội $\frac{1}{4}$:
  $$\sum_{k=1}^{\log_2 N} \left(\frac{1}{4}\right)^k \lt \frac{1/4}{1 - 1/4} = \frac{1}{3}$$
  Mức $1024 \times 1024$ có $11$ mức ($1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1$), tổng số điểm kết cấu là $1\,398\,101$, tăng thêm $\frac{349\,525}{1\,048\,576} \approx 0{,}33333 \approx \frac{1}{3}$ so với mức gốc.

## [MS21] S. Marschner, P. Shirley, “Fundamentals of Computer Graphics” (5th ed., CRC Press, 2021), chương 11 (Texture Mapping)
- Nội suy song tuyến (*bilinear interpolation*) từ bốn điểm kết cấu góc ô $v_{00}, v_{10}, v_{01}, v_{11}$ với toạ độ lẻ $(u, v) \in [0, 1]^2$:
  $$v(u, v) = (1 - u)(1 - v)v_{00} + u(1 - v)v_{10} + (1 - u)v\,v_{01} + u\,v\,v_{11}$$
  Cũng bằng nội suy tuyến tính một chiều theo $u$ trên hai hàng trước, rồi nội suy theo $v$ giữa hai kết quả.
- Khi phóng đại (*magnification*, một điểm kết cấu phủ nhiều điểm ảnh), lấy mẫu điểm gần nhất tạo ô vuông bậc thang, còn nội suy song tuyến làm mượt chuyển tiếp giữa các điểm kết cấu.
- Khi thu nhỏ (*minification*, một điểm ảnh phủ nhiều điểm kết cấu), lấy mẫu một điểm duy nhất vi phạm định lý lấy mẫu Nyquist (tần số kết cấu trên màn hình vượt quá nửa tần số điểm ảnh), gây hiện tượng răng cưa và sọc lấp lánh (*shimmering / moiré*) khi camera di chuyển; giải pháp là lọc trước bằng tháp ảnh thu nhỏ sẵn (*mipmap*).

## Điều KHÔNG dạy / NOT_VERIFIED
- Không đi sâu công thức elip của lọc dị hướng (*anisotropic filtering* / EWA của Heckbert 1989) — chỉ nêu nguyên lý khi nhìn nghiêng một ô điểm ảnh chiếu lên kết cấu thành hình kéo dài chứ không vuông, để người học biết khi nào cần bật lọc theo hướng nhìn.
- Các giá trị điểm kết cấu (10, 20, 30, 40; bàn cờ đen trắng 0 và 200) là SỐ MINH HOẠ để tính tay và kiểm chứng bằng `alg.gfx_bilinear` và `alg.gfx_mipmap_stats`.
