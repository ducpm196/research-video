# Lab CS115 L17 — MLE, MAP và tiên nghiệm

Cần: Python 3 (chỉ `import math`), `from fractions import Fraction`. Tạo tệp `mle.py` (số minh hoạ, khác ví dụ trong bài).

1. Đồng xu: 9 ngửa trong 12 lần. In `MLE dong xu: <k/n>` (phân số tối giản của `Fraction`), `MAP (+1 ngua, +1 sap): <(k+1)/(n+2)>` và `MAP (+2 ngua, +2 sap): <(k+2)/(n+4)>`.
2. Lôgarit khả năng của dữ liệu đó là `k * ln(theta) + (n - k) * ln(1 - theta)`. In `ln kha nang: theta=0.75 -> <số>, theta=0.5 -> <số>` (mỗi số làm tròn 4 chữ số thập phân bằng `round(..., 4)`), rồi dòng `MLE tot hon: True` nếu giá trị tại `0.75` lớn hơn.
3. Dữ liệu chiều cao `[150, 160, 170, 180]` giả sử từ phân phối chuẩn. MLE của `mu` là trung bình cộng, MLE của phương sai là trung bình bình phương độ lệch (chia `n`). In `MLE mu, sigma^2: <mu> <phuong sai>`.
4. Phân loại 4 lớp, số đếm `[6, 3, 2, 1]`. MLE là `đếm / tổng`; in `phan loai MLE: [..]`. Với tiên nghiệm cộng thêm 1 lần đếm cho mỗi lớp: `(đếm + 1) / (tổng + 4)`; in `phan loai co +1 moi lop: [..]`. Phân số in bằng `str` của `Fraction`, ngăn bằng dấu phẩy và một khoảng trắng.

Chạy: `python mle.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L17 mle.py`.
