# Lab BNX L23 — Điểm bất thường, nhãn và số điểm bị gắn (Python thuần, không cần cài thư viện học máy)

Số liệu là số minh hoạ, khác ví dụ trong bài. Một rừng cô lập huấn luyện mỗi cây trên `n = 128` điểm. Viết `mau.py` (chỉ dùng `import math`) để tính:

1. **Mức tham chiếu** `c(n) = 2·(ln(n−1) + γ) − 2·(n−1)/n` với `γ = 0.5772156649` (`math.log` là lôgarit tự nhiên). In `c(128) = <số làm tròn 4 chữ số>`.
2. Hai điểm A và B có **độ sâu trung bình** `h` lần lượt là 2 và 9. Điểm bất thường `s = −2^(−h / c)` (dấu âm như thư viện). Ngưỡng `offset = −0.6`; **điểm quyết định** = `s − offset`; nhãn là `−1` nếu điểm quyết định âm, ngược lại `1`.
3. Tập có `N = 3000` giao dịch, tỉ lệ nhiễm `p = 0.03`. Theo quy tắc đếm của bài (đúng khi các điểm khác nhau), số điểm bị gắn `−1` là `p·(N−1)` làm tròn lên (`math.ceil`). Thật sự lạ chỉ có 25 điểm: tính số điểm thường bị gắn oan.

In đúng bốn dòng (làm tròn bằng `round(x, 4)`):

```
c(128) = <số>
A diem <số> quyet dinh <số> nhan <1 hoặc -1>
B diem <số> quyet dinh <số> nhan <1 hoặc -1>
bi gan -1: <số> | gan oan: <số>
```

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L23 mau.py`.
