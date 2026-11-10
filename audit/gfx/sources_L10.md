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

## BN-0038 — điểm chuẩn F0 (đợt C, 2026-11-09)
- [BU12] B. Burley, “Physically-Based Shading at Disney”, SIGGRAPH 2012 course notes, https://media.disneyanimation.com/uploads/production/publication_asset/48/asset/s2012_pbs_disney_brdf_notes_v3.pdf (tải và đọc 2026-11-09), §5.4: nguyên văn “our specular parameter determines the incident specular amount. The normalized range of this parameter is remapped linearly to the incident specular range [0.0, 0.08]. This corresponds to IOR values in the range [1.0, 1.8], encompassing most common materials. Notably, the middle of the parameter range corresponds to an IOR of 1.5, a very typical value, and is also our default.” → mặc định 0,04 ứng với n = 1,5.
- [KA13] B. Karis, “Real Shading in Unreal Engine 4”, SIGGRAPH 2013 course notes, https://cdn2.unrealengine.com/Resources/files/2013SiggraphPresentationsNotes-26915738.pdf (tải và đọc 2026-11-09): nguyên văn “its actual default was Burley's 0.5 (corresponding to 4% reflectance)” và “F0 of nonmetals is now a constant 0.04.”
- [PBR4] https://pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission (truy cập 2026-11-09, no revision given), §9.3.2 “The Index of Refraction”, Bảng 9.1: thuỷ tinh 1,5–1,6, nước (20 °C) 1,333; văn bản: “an air–glass surface with a difference around 1.5”. Thay vào F0 = ((n − 1)/(n + 1))²: n = 1,5 → 0,04; n = 1,333 → 0,0204; n từ 1,3 đến 1,7 → 0,017 đến 0,067 (bài ghi “0,02..0,07”). Trang PBR4 này không ghi trực tiếp con số 4%.
- Kết luận BN-0038: mọi chỗ F0 trong GFX (L10: 0,04 điện môi, nước 0,02, khoảng 0,02..0,07; L13: n = 1,5 → 0,04, phi kim 0,04) khớp nguồn. Ô SVG L10 “F₀ ≈ 2–5%” là tóm tắt khoảng thường gặp (nước 2%, nhựa và thuỷ tinh 4–5%), không có nguồn mở ghi đúng cận 5%; ngọc, kim cương cao hơn — để nguyên, ghi ở báo cáo.
- Câu “kim loại F0 khoảng 0,5 tới 0,95” ở trên chưa kiểm được trong nguồn mở đợt này (bảng của RTR4 không mở được): NOT_VERIFIED; bài chỉ nói “phần lớn kênh màu trên 50%” và câu tự làm dùng 0,80 có nhãn số minh hoạ.
- Đợt C sửa trong bài: định nghĩa chiết suất và khúc xạ; tiêu đề cảnh ôn nền ghi “phản xạ bài 9” trong khi nội dung là chiết suất → sửa; lời đọc “phương trình sóng” → “công thức quang học chính xác”.
