# Nguồn bài CVI L03 — mô hình camera, ma trận nội, méo ống kính, hiệu chuẩn

Đọc 2026-11-03. Trang docs.opencv.org trả HTTP 403 cho công cụ (cả WebFetch lẫn curl: trang chặn “Just a moment…”), nên đọc tệp nguồn
của chính trang hướng dẫn đó trong kho mã chính thức của OpenCV trên GitHub (cùng nội dung, không qua dịch vụ trung gian).

**[OCVC]** OpenCV 4.x, hướng dẫn “Camera Calibration”,
https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_calib3d/py_calibration/py_calibration.markdown

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “Radial distortion causes straight lines to appear curved. Radial distortion becomes larger the farther points are from the center of the image.” | hình méo hướng tâm; “tâm không lệch, góc lệch nhiều” |
| “x_distorted = x(1 + k_1 r^2 + k_2 r^4 + k_3 r^6), y_distorted = y(1 + k_1 r^2 + k_2 r^4 + k_3 r^6)” | công thức méo (bài chỉ dùng k1, ghi ở quy ước) |
| “Intrinsic parameters are specific to a camera. They include information like focal length (f_x, f_y) and optical centers (c_x, c_y).” … “It is expressed as a 3x3 matrix: camera matrix = [f_x 0 c_x; 0 f_y c_y; 0 0 1]” | ký hiệu, ma trận nội K |
| “The camera matrix is unique to a specific camera, so once calculated, it can be reused on other images taken by the same camera.” | (nền cho lỗi 2–3: chỉ dùng lại khi tiêu cự, độ phân giải không đổi — điều kiện là suy luận của bài) |
| “We know the coordinates of these points in real world space and we know the coordinates in the image, so we can solve for the distortion coefficients. For better results, we need at least 10 test patterns.” | lỗi 4, câu tự làm 3: “ít nhất khoảng 10 ảnh bàn cờ” |
| “Re-projection error gives a good estimation of just how exact the found parameters are. The closer the re-projection error is to zero, the more accurate the parameters we found are.” | tự kiểm: sai số chiếu lại |

## Điều KHÔNG dạy (nguồn không ghi / số minh hoạ)
- “Sai số chiếu lại nhỏ mà mép ảnh vẫn sai khi bàn cờ chỉ nằm giữa” là SUY LUẬN của bài, kiểm bằng số (méo 0,16 điểm ảnh ở giữa,
  20 ở góc; sai số chuẩn của k1 gấp ~60 lần khi chỉ có điểm giữa ảnh — verify_parts/L03.py L03j), không phải câu của OpenCV.
  OpenCV chỉ ghi “càng gần 0 càng chính xác”; bài không phản bác câu đó mà nêu điều kiện: chỉ đúng ở vùng có điểm mẫu.
- Nhóm đo linh kiện, ảnh 640 × 480, f = 800, k1 = −0,2 / −0,1, ống kính 4 mm, điểm cảm biến 0,005 mm, tiêu cự trôi 5% là SỐ MINH HOẠ.
- Bài Zhang (2000) về hiệu chuẩn bằng mặt phẳng: trang Microsoft Research trả trang HTML thay vì PDF → NOT_VERIFIED, không trích.
