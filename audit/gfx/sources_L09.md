# Nguồn bài GFX L09 — Dò tia: giao tia với cầu, bóng đổ và phản xạ

Đọc và đối chiếu 2026-11-03. Nhãn dùng trong `source` của bài `lessons/gfx/L09_do_tia.yaml`.

## [WH80] T. Whitted, “An Improved Illumination Model for Shaded Display”, Communications of the ACM, Vol. 23, No. 6, pp. 343–349 (1980)
- Trích nguyên văn về cây tia (*tree of rays*):
  > “To accurately render a two-dimensional image of a three-dimensional scene, global illumination information that affects the intensity of each pixel of the image must be known at the time the intensity is calculated. In a simplified form, this information is stored in a tree of "rays" extending from the viewer to the first surface encountered and from there to other surfaces and to the light sources.”
- Trích nguyên văn về bóng đổ, phản xạ và khúc xạ:
  > “Consideration of all of these factors allows the shader to accurately simulate true reflection, shadows, and refraction, as well as the effects simulated by conventional shaders.”
  > “A point on a surface lies in shadow if it is visible to the viewer but not visible to the light source.”
- Hướng tia phản xạ gương $\mathbf{r}$ từ tia tới đơn vị $\mathbf{d}$ và pháp tuyến đơn vị $\mathbf{n}$:
  $$\mathbf{r} = \mathbf{d} - 2(\mathbf{d} \cdot \mathbf{n})\mathbf{n}$$

## [MS21] S. Marschner, P. Shirley, “Fundamentals of Computer Graphics” (5th ed., 2021), chương 4 (Ray Tracing)
- Phương trình tia xuất phát từ gốc $\mathbf{o}$ theo hướng đơn vị $\mathbf{d}$ với tham số khoảng cách $t \ge 0$: $\mathbf{p}(t) = \mathbf{o} + t\mathbf{d}$.
- Thay vào phương trình mặt cầu tâm $\mathbf{c}$ bán kính $r$: $\|\mathbf{o} + t\mathbf{d} - \mathbf{c}\|^2 = r^2$. Đặt $\mathbf{m} = \mathbf{o} - \mathbf{c}$ và vì $\|\mathbf{d}\|^2 = 1$, thu được phương trình bậc hai:
  $$t^2 + 2(\mathbf{m} \cdot \mathbf{d})t + (\|\mathbf{m}\|^2 - r^2) = 0$$
  Biệt thức $\Delta = b^2 - 4ac$ quyết định số giao điểm: $\Delta \lt 0$ (không giao), $\Delta = 0$ (tiếp xúc), $\Delta \gt 0$ (hai giao điểm $t_1 \lt t_2$, chọn nghiệm dương nhỏ nhất).
- Hiện tượng tự che bóng (*shadow acne* / mụn bóng): do sai số dấu phẩy động, điểm giao tính được có thể nằm hơi chìm dưới bề mặt một lượng rất nhỏ; nếu bắn tia bóng đổ ngay từ $t = 0$, tia sẽ tự cắt chính bề mặt đó ở $t \approx 10^{-6}$. Cách khắc phục chuẩn là dời gốc tia một khoảng nhỏ $\varepsilon \gt 0$ (hoặc chỉ nhận giao ở $t \gt \varepsilon$) theo hướng pháp tuyến.

## Điều KHÔNG dạy / NOT_VERIFIED
- Không dạy thuật toán giao tia–tam giác Möller–Trumbore (1997) và cấu trúc cây hộp bao phân cấp (*BVH*) ở mức cài đặt chi tiết — chỉ nêu ý tưởng hộp bao ở phần mở rộng / câu hỏi quyết định để người học hiểu vì sao dò tia thực tế không thử hết mọi vật.
- Toạ độ mặt cầu tâm $(0, 0, 5)$ bán kính $1$ và nguồn sáng là SỐ MINH HOẠ để giải phương trình bậc hai chẵn số.
