# Nguồn bài GFX L10 — Kết xuất dựa trên vật lý: bảo toàn năng lượng và hiệu ứng Fresnel

Đọc và đối chiếu 2026-11-03. Nhãn dùng trong `source` của bài `lessons/gfx/L10_ket_xuat_vat_ly.yaml`.

## [SC94] C. Schlick, “An Inexpensive BRDF Model for Physically-based Rendering”, Computer Graphics Forum, Vol. 13, No. 3, pp. 233–246 (1994)
- Xấp xỉ luỹ thừa bậc năm cho hệ số phản xạ theo góc tới $\theta$ (với $\cos\theta = \mathbf{n} \cdot \mathbf{v}$ hoặc $\mathbf{h} \cdot \mathbf{v}$):
  $$F(\theta) = F_0 + (1 - F_0)(1 - \cos\theta)^5$$
- Trong đó $F_0$ là hệ số phản xạ khi nhìn thẳng góc ($\theta = 0^\circ \Rightarrow \cos\theta = 1$, suy ra $F(0^\circ) = F_0$). Khi nhìn sượt sát mép ($\theta = 90^\circ \Rightarrow \cos\theta = 0$), mọi bề mặt phẳng nhẵn đều tiến tới phản xạ toàn phần $F(90^\circ) = F_0 + (1 - F_0) \cdot 1 = 1$.
- Hệ số phản xạ thẳng góc $F_0$ liên hệ với chiết suất $n$ của vật liệu (trong không khí $n_{\text{kk}} \approx 1$):
  $$F_0 = \left(\frac{n - 1}{n + 1}\right)^2$$
  Với thuỷ tinh hoặc nhựa thông thường có $n = 1{,}5$: $F_0 = \left(\frac{0{,}5}{2{,}5}\right)^2 = 0{,}2^2 = 0{,}04$ (tức $4\%$).

## [PJH23] M. Pharr, W. Jakob, G. Humphreys, “Physically Based Rendering: From Theory to Implementation” (4th ed., MIT Press, 2023) & [AM18] T. Akenine-Möller và cộng sự, “Real-Time Rendering” (4th ed., 2018), chương 9 (Physically Based Shading)
- Nguyên lý bảo toàn năng lượng (*energy conservation*): tổng năng lượng ánh sáng phản xạ gương (tức thời ở bề mặt) và phần ánh sáng đi vào vật liệu để tán xạ khuếch tán không được vượt quá năng lượng ánh sáng chiếu tới.
- Nếu phần phản xạ bề mặt đã lấy đi tỉ lệ $F(\theta)$, thì phần năng lượng còn lại đi vào trong vật liệu chỉ tối đa là $1 - F(\theta)$. Do đó thành phần khuếch tán của chất điện môi (phi kim: nhựa, gỗ, đá, nước) phải nhân với $(1 - F(\theta))$:
  $$L_{\text{ra}} = F(\theta)\,L_{\text{gương}} + (1 - F(\theta))\,L_{\text{khuếch tán}}$$
- Với kim loại dẫn điện (*conductors*): ánh sáng đi vào bên trong bị hấp thụ ngay thành nhiệt nên thành phần khuếch tán bằng $0$, còn hệ số phản xạ thẳng góc $F_0$ cao (khoảng $0{,}5$ tới $0{,}95$) và mang màu riêng của kim loại (như vàng, đồng).

## Điều KHÔNG dạy / NOT_VERIFIED
- Không đi sâu chứng minh tích phân bán cầu của hàm phân bố vi diện (*microfacet normal distribution function* GGX/Trowbridge–Reitz và hàm che khuất hình học Smith) — bài tập trung vào hai trụ cột dễ kiểm chứng bằng số: công thức phản xạ theo góc nhìn và phép chia năng lượng $F$ với $(1 - F)$.
