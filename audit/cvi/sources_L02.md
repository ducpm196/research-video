# Nguồn bài CVI L02 — biểu đồ tần suất, cân bằng, ngưỡng Otsu

Đọc 2026-11-03 (bản tải ở scratchpad `cvi_work/src/`).

**[OT79]** N. Otsu, “A Threshold Selection Method from Gray-Level Histograms”, IEEE Transactions on Systems, Man, and Cybernetics 9(1),
tr. 62–66, 1/1979, DOI 10.1109/TSMC.1979.4310076. Trang IEEE Xplore trả trang rỗng cho công cụ; đã đọc **siêu dữ liệu Crossref**
(https://api.crossref.org/works/10.1109/TSMC.1979.4310076): “title”: “A Threshold Selection Method from Gray-Level Histograms”,
“author”: Nobuyuki Otsu, “published-print”: 1979-1, “page”: “62-66”, “volume”: “9”. Toàn văn: NOT_VERIFIED → bài chỉ dùng tên phương pháp,
không trích câu nào của bài báo, không nêu “thước đo tách” của tác giả; tỉ số σ_B²/σ² ở lỗi 2 là phép tính của bài, không gán cho tác giả.

**[OCVT]** OpenCV 4.x, hướng dẫn “Image Thresholding”,
https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.markdown

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “In global thresholding, we used an arbitrary chosen value as a threshold. In contrast, Otsu's method avoids having to choose a value and determines it automatically.” | khái niệm: máy tự chọn ngưỡng |
| “Consider an image with only two distinct image values (*bimodal image*), where the histogram would only consist of two peaks. A good threshold would be in the middle of those two values.” | hình biểu đồ hai đỉnh |
| “Otsu's algorithm tries to find a threshold value (t) which minimizes the **weighted within-class variance** given by the relation: σ_w²(t) = q₁(t)σ₁²(t) + q₂(t)σ₂²(t)” | bước 1 của phần suy ra; tự kiểm (tính thẳng phương sai trong lớp) |
| “But this might not be good in all cases, e.g. if an image has different lighting conditions in different areas. In that case, adaptive thresholding can help. Here, the algorithm determines the threshold for a pixel based on a small region around it.” | lỗi 1: ngưỡng cục bộ |
| “In the third case, the image is first filtered with a 5x5 gaussian kernel to remove the noise, then Otsu thresholding is applied.” | lỗi 3: làm mờ trước |

## Điều KHÔNG dạy (nguồn không ghi / số minh hoạ)
- Hệ thức “phương sai cả ảnh = trong lớp + giữa lớp” và dạng w₀w₁(μ₀ − μ₁)² là phép biến đổi đại số, được kiểm bằng phân số chính xác
  (verify_parts/L02.py), không trích từ bài báo gốc.
- Ảnh hoá đơn, bóng tay, các giá trị 200/120/110/30, nền 100…105, ảnh 3 bit là SỐ MINH HOẠ.
- Cân bằng biểu đồ dùng công thức làm tròn((L − 1)·tỉ lệ tích lũy) — công thức chuẩn trong sách giáo khoa, không gắn tên tác giả.
