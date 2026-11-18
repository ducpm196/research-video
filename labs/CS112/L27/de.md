# Lab CS112 L27 — Mini bài tập lớn: ba cách nhân chuỗi ma trận và một quy tắc tham lam

Cần: Python 3.11 trở lên. Tạo `mini_btl.py` (số liệu minh hoạ, khác ví dụ trong bài). Bảy ma trận `A1 … A7`, `A_i` cỡ `p[i-1] x p[i]` với `p = (22, 9, 18, 24, 20, 16, 27, 13)` (chỉ số từ 1; `n = 7`). Cài bốn chiến lược cho cùng một việc "số phép nhân số ít nhất của đoạn `i..j`", mỗi chiến lược một hàm nhận `(i, j)`:

1. **bảng** (từ dưới lên): `m[i][j] = min` qua chỗ cắt `k` của `m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j]`, điền theo độ dài đoạn; đếm số lần tính biểu thức trong `min`;
2. **ghi nhớ** (từ trên xuống, từ điển): đệ quy có nhớ; đếm số lần hàm được gọi (kể cả lần tra bảng ra ngay);
3. **vét cạn** (đệ quy không nhớ): đếm số lần hàm được gọi (kể cả lần ở đoạn một ma trận, trả 0);
4. **tham lam**: chọn chỗ cắt `k` có `p[k]` nhỏ nhất trong đoạn (hoà thì `k` nhỏ nhất), rồi làm tiếp hai nửa theo cùng quy tắc; trả về tổng số phép nhân của cách đặt ngoặc đó.

Rồi in đúng sáu dòng, các giá trị tính từ chương trình (không gõ sẵn):

```
Bang: <số phép nhân>, <số lần tính> lan thu cat
Ghi nho: <số phép nhân>, <số lần gọi> loi goi
Vet can: <số phép nhân>, <số lần gọi> loi goi
Tham lam: <số phép nhân>, lech <phần trăm làm tròn 1 chữ số> % so voi toi uu
Ba cach dung bang nhau: CO
Vet can khi n = 9: <số lần gọi> loi goi
```

(Dòng cuối chạy vét cạn thêm một lần với chuỗi `n = 9` ma trận có `p = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12)` và chỉ in số lần gọi; các dòng khác dùng `p` của đề.)

Chạy: `python mini_btl.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L27 mini_btl.py`.
