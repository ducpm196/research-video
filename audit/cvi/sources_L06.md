# Nguồn bài CVI L06 — độ sâu từ chênh lệch ảnh

Bài không nêu sự kiện hay con số của nguồn ngoài. Phần ôn nền Z = f·B/d và ý “sai số tăng gần theo Z²” là nội dung đã dạy ở
ROB bài 11 (`lessons/rob/L11_camera_lo_kim.yaml`); bài này tự suy ra công thức sai số δZ ≈ Z²·δd/(f·B) từ phép trừ hai phân số
(kiểm bằng sympy ở `verify_parts/L06.py`). Số f = 700, B = 0,12 m, d = 42 lấy từ giáo án (VER CVI:L06).

## Điều KHÔNG dạy (chưa đọc nguồn / số minh hoạ)
- Hàng điểm ảnh 10, 20, 90, 40…, robot, tường trắng, dải tìm 0…168, ảnh 640 × 480 là SỐ MINH HOẠ.
- “Camera có máy chiếu chấm sáng lên tường để tạo vân” không nêu tên sản phẩm nào; là nhận xét chung, không trích nguồn.
- Không dạy tên “đường cực / hình học cực” và thuật toán nắn ảnh cụ thể (Hartley–Zisserman chưa đọc trong đợt này).
