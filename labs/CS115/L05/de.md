# Lab CS115 L05 — Trị riêng và vector riêng của ma trận 2 × 2

Cần: Python 3 (không cần thư viện ngoài). Tạo tệp `rieng.py`. Ma trận `M = [[5, 2], [2, 2]]` (số minh hoạ, khác ví dụ trong bài); ký hiệu `[[a, b], [c, d]]`.

1. In `dinh thuc: <a*d - b*c>` và `vet: <a + d>` (vết = tổng hai số trên đường chéo).
2. Trị riêng là nghiệm của `lambda^2 - vet*lambda + dinh thuc = 0`. Tính `delta = vet^2 - 4*dinh thuc`, nếu `delta` là số chính phương (bình phương của một số nguyên, ví dụ 25 = 5²) thì hai trị riêng là `(vet - căn delta)/2` và `(vet + căn delta)/2`. In `tri rieng: [<nhỏ>, <lớn>]` (số nguyên).
3. Với mỗi trị riêng `lam` (nhỏ trước), in HAI dòng liên tiếp. Dòng một: `vector rieng cho <lam>: [x, y]`, vector riêng là `[b, lam - a]` chia cả hai số cho ước chung lớn nhất của chúng (`math.gcd`). Dòng hai: `M.v = lambda.v (lambda=<lam>): True` nếu `M` nhân `v` đúng bằng `lam` nhân `v`.
4. Với `R = [[0, -2], [2, 0]]` (xoay) tính `delta`; vì `delta < 0` nên in `ma tran xoay: khong co tri rieng thuc`.

Chạy: `python rieng.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L05 rieng.py`.
