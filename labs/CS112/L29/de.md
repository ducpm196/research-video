# Lab CS112 L29 — Mô phỏng ngăn xếp đoạn chờ của Timsort: minrun, bất biến cũ và bản sửa

Cần: Python 3.11 trở lên (không cần thư viện). Tạo `timsort_mo_phong.py` (số liệu minh hoạ, khác ví dụ trong bài).

**Phần 1 — minrun**: hàm `minrun(n)`: đặt `r = 0`; khi `n >= 64`: `r = r | (n & 1)` rồi `n = n >> 1`; trả về `n + r`. Với mỗi `n` trong `1000, 4097, 5000`: tính `minrun`, số đoạn `= ceil(n / minrun)` (dùng `math.ceil`) và xem số đoạn có là lũy thừa của 2 không (số `k` là lũy thừa của 2 khi `k & (k - 1) == 0`). In `n = <n>: minrun <số>, <số đoạn> doan, luy thua cua 2: CO/KHONG`.

**Phần 2 — ngăn xếp đoạn chờ**: dãy độ dài đoạn lần lượt được đẩy vào ngăn xếp (danh sách, đỉnh ở cuối): `62, 109, 119, 37, 22, 55`. Sau mỗi lần đẩy, chạy vòng gộp: khi ngăn xếp có hơn 1 phần tử, đặt `n = len - 2` (chỉ số đoạn B; A là `n - 1`, C là `n + 1`):

- nếu `(n > 0 và s[n-1] <= s[n] + s[n+1])` hoặc (CHỈ ở bản sửa) `(n > 1 và s[n-2] <= s[n-1] + s[n])`: nếu `s[n-1] < s[n+1]` thì `n = n - 1`; rồi gộp `s[n]` và `s[n+1]` thành một phần tử (tổng);
- ngược lại nếu `s[n] <= s[n+1]`: gộp `s[n]` và `s[n+1]`;
- ngược lại: dừng.

Viết hàm nhận cờ `ban_sua` (False là bản cũ, chỉ xét 3 đoạn trên cùng; True là thêm điều kiện thứ hai, xét 4 đoạn). Sau khi đẩy hết, kiểm bất biến trên toàn ngăn xếp: mọi `s[i] > s[i+1] + s[i+2]` và mọi `s[i] > s[i+1]`. In `Ban cu: ngan xep cuoi <danh sách>, bat bien DUNG/HONG` rồi dòng tương tự cho `Ban sua`.

Phải in đúng năm dòng:

```
n = 1000: minrun ..., ... doan, luy thua cua 2: ...
n = 4097: ...
n = 5000: ...
Ban cu: ngan xep cuoi [...], bat bien ...
Ban sua: ngan xep cuoi [...], bat bien ...
```

Chạy: `python timsort_mo_phong.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L29 timsort_mo_phong.py`.
