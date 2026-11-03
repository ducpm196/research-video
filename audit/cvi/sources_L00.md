# Nguồn bài CVI L00 — ảnh số

Đọc 2026-11-03 (curl từ kho mã nguồn chính thức trên GitHub; bản tải ở scratchpad `cvi_work/src/`).

**[OCV]** OpenCV 4.x, `modules/imgcodecs/include/opencv2/imgcodecs.hpp`,
https://raw.githubusercontent.com/opencv/opencv/4.x/modules/imgcodecs/include/opencv2/imgcodecs.hpp

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “IMREAD_COLOR_BGR = 1, //!< If set, always convert image to the 3 channel BGR color image.” | lỗi 3: có thư viện đọc ảnh màu theo thứ tự lam, lục, đỏ |
| “IMREAD_COLOR = 1, //!< Same as IMREAD_COLOR_BGR.” | lỗi 3 (chế độ mặc định) |

**[W3C]** W3C CSS Color Module Level 4, mã chuyển đổi mẫu `css-color-4/conversions.js` (kho chính thức w3c/csswg-drafts),
https://raw.githubusercontent.com/w3c/csswg-drafts/main/css-color-4/conversions.js — trang w3.org/TR/css-color-4 trả trang chặn
“Just a moment…” cho curl nên đọc tệp mã trong kho chính thức của nhóm soạn chuẩn.

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “convert an array of sRGB values where in-gamut values are in the range [0 - 1] to linear light (un-companded) form.” … “if (abs <= 0.04045) { return val / 12.92; } return sign * (Math.pow((abs + 0.055) / 1.055, 2.4));” | lỗi 4: 128 → 0,216 |
| “return sign * (1.055 * Math.pow(abs, 1/2.4) - 0.055);” | lỗi 4: nửa ánh sáng → giá trị lưu ≈ 188 |

## Điều KHÔNG dạy (nguồn không ghi / số minh hoạ)
- Camera giám sát 1920 × 1080, ổ 1 TB, camera 4K, “nén nhỏ đi hàng chục lần” là SỐ MINH HOẠ / nhận xét chung; không nêu tỉ lệ nén cụ thể của chuẩn nào.
- Tên thư viện chỉ trên màn hình; lời đọc nói “có thư viện xử lý ảnh nổi tiếng”.
