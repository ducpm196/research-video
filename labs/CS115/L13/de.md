# Lab CS115 L13 — Bayes bằng cách đếm, và kỳ vọng, phương sai

Cần: Python 3 (không cần thư viện ngoài). Tạo tệp `bayes.py`. Số liệu (số minh hoạ, khác ví dụ trong bài): một bệnh có tỉ lệ `2%`; máy bắt đúng `95%` người bệnh và báo nhầm `5%` người khoẻ.

1. Đếm trên `10000` người (dùng phép chia nguyên `//` hoặc số nguyên): số người bệnh, số người bệnh được báo đúng, số người khoẻ bị báo nhầm. In `dem 10000 nguoi: benh <a>, bao dung <b>, bao nham <c>`.
2. Xác suất thật khi dương tính, bằng cách đếm: `b / (b + c)`, làm tròn 4 chữ số thập phân. In `xac suat that khi duong tinh (dem): <số>`.
3. Cùng xác suất bằng công thức Bayes `P(dương | bệnh) * P(bệnh) / P(dương)`, với `P(dương) = P(dương | bệnh) * P(bệnh) + P(dương | khoẻ) * P(khoẻ)`. In `xac suat that khi duong tinh (Bayes): <số>` (làm tròn 4 chữ số).
4. Với tiên nghiệm `0.2%` (hiếm hơn mười lần), in `tien nghiem 0.2%: <số>` (làm tròn 4 chữ số).
5. Biến ngẫu nhiên `X` nhận `0, 1, 2` với xác suất `0.2, 0.5, 0.3`. In `ky vong: <E[X]>`, `phuong sai: <E[X^2] - E[X]^2>`, `do lech chuan: <căn phương sai>`, mỗi số làm tròn 4 chữ số rồi in bằng `print` của Python (ví dụ `1.1`).

Chạy: `python bayes.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L13 bayes.py`.
