# Nguồn bài GFX L08 — Màu và gamma: vì sao trung bình hai màu phải tính trong không gian tuyến tính

Đọc và đối chiếu 2026-11-03. Nhãn dùng trong `source` của bài `lessons/gfx/L08_gamma.yaml`.

## [IEC99] IEC 61966-2-1:1999, “Multimedia systems and equipment — Colour measurement and management — Part 2-1: Colour management — Default RGB colour space — sRGB”
- Hàm truyền đổi từ giá trị chuẩn hoá $c \in [0, 1]$ của không gian sRGB sang cường độ sáng tuyến tính $x \in [0, 1]$:
  $$x = \begin{cases} \dfrac{c}{12{,}92} & \text{nếu } c \le 0{,}04045 \\[6pt] \left(\dfrac{c + 0{,}055}{1{,}055}\right)^{2{,}4} & \text{nếu } c \gt 0{,}04045 \end{cases}$$
- Hàm truyền ngược đổi từ cường độ sáng tuyến tính $x \in [0, 1]$ sang giá trị sRGB $c \in [0, 1]$:
  $$c = \begin{cases} 12{,}92\,x & \text{nếu } x \le 0{,}0031308 \\[6pt] 1{,}055\,x^{1/2{,}4} - 0{,}055 & \text{nếu } x \gt 0{,}0031308 \end{cases}$$
- Hệ quả số học (kiểm bằng `alg.gfx_srgb_to_linear`, `alg.gfx_linear_to_srgb`, `alg.gfx_srgb_blend_byte`):
  - Điểm giữa tuyến tính $x = 0{,}5$ đổi sang sRGB cho $c \approx 0{,}735357 \Rightarrow \text{round}(255 \cdot c) = 188$ (byte 188 trên 255).
  - Byte 128 trên 255 ($c = 128/255 \approx 0{,}50196$) đổi sang tuyến tính chỉ đạt $x \approx 0{,}21586$, tức chỉ khoảng $21{,}6\%$ cường độ sáng của màu trắng hoàn toàn — quá tối so với mức $50\%$ năng lượng ánh sáng.

## [MS21] S. Marschner, P. Shirley, “Fundamentals of Computer Graphics” (5th ed., 2021) & [AM18] T. Akenine-Möller và cộng sự, “Real-Time Rendering” (4th ed., 2018), mục 5.6 (Gamma Correction)
- Mắt người nhạy với thay đổi độ sáng ở vùng tối hơn vùng sáng; mã hoá phi tuyến sRGB dành nhiều mức lượng tử 8 bit cho vùng tối để tránh vệt bậc thang (*banding*).
- Cộng ánh sáng từ nhiều đèn, trộn màu bán trong suốt, nội suy màu và lọc kết cấu đều là phép cộng năng lượng photon vật lý nên bắt buộc thực hiện trong không gian tuyến tính; chỉ mã hoá lại sang sRGB ở bước cuối cùng khi ghi ra bộ đệm khung hình hiển thị.

## Điều KHÔNG dạy / NOT_VERIFIED
- Không dạy các đường cong truyền của dải động cao (PQ SMPTE ST 2084 hay HLG) và không gian màu rộng (Display P3, Rec. 2020) — bài tập trung vào nguyên lý cốt lõi giữa không gian tuyến tính và mã hoá gamma chuẩn 8 bit.
- Các ví dụ trộn hai đèn và hai điểm ảnh là SỐ MINH HOẠ để tính trực tiếp trên công thức chuẩn IEC 61966-2-1.

## Đối chiếu nguồn mở (đợt C, 2026-11-09)
- Bản chuẩn IEC 61966-2-1 không mở miễn phí. Đối chiếu bằng [GL46] OpenGL 4.6 Core Profile (Khronos, 5/5/2022, https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf, đọc 2026-11-09): §8.24 “sRGB Texture Color Conversion”, phương trình (8.17): cl = cs/12,92 khi cs ≤ 0,04045, cl = ((cs + 0,055)/1,055)^2,4 khi cs > 0,04045; §17.3.7 “sRGB Conversion”, phương trình (17.1): cs = 12,92·cl khi 0 < cl < 0,0031308, cs = 1,055·cl^0,41666 − 0,055 khi 0,0031308 ≤ cl < 1 — trùng hằng số bài dùng (0,41666 ≈ 1/2,4).
- Cùng §8.24, nguyên văn: “Ideally, implementations should perform this color conversion on each sample prior to filtering … (though this post-filtering approach is inferior to converting from sRGB prior to filtering)” — ủng hộ lỗi 1 của bài (lọc và tạo mức thu nhỏ phải làm trên giá trị tuyến tính).
- Đợt C sửa: ghi chú đoạn thẳng 12,92 nói “độ dốc hữu hạn tại c = 0” (mơ hồ) → hàm ngược (mã hoá) có độ dốc hữu hạn tại 0; thêm định nghĩa bản đồ pháp tuyến (toạ độ = 2c − 1) và bản đồ độ nhám.
