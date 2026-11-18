# Lab CS112 L26 — Tập độc lập và phủ đỉnh, kiểm chứng chỉ, cái túi 0/1 giả đa thức

Cần: Python 3.11 trở lên. Tạo `np_khoi.py` (số liệu minh hoạ, khác ví dụ trong bài).

**Phần 1 — quy dẫn**: đồ thị 7 đỉnh `0…6`, 9 cạnh: `(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,0), (1,5), (2,6)`.
- Vét cạn mọi tập con đỉnh (`itertools.combinations`) để tìm kích thước LỚN NHẤT của một tập độc lập (không cạnh nào có cả hai đầu trong tập) và NHỎ NHẤT của một phủ đỉnh (mọi cạnh có ít nhất một đầu trong tập).
- Kiểm chứng chỉ: lấy một tập độc lập lớn nhất `S` (tập đầu tiên tìm được khi duyệt kích thước giảm dần, trong mỗi kích thước theo thứ tự của `combinations`) và duyệt đúng một lần mọi cạnh để kiểm không cạnh nào có cả hai đầu trong `S`; đếm số cạnh đã duyệt.

**Phần 2 — cái túi 0/1** (quy hoạch động bảng `n` hàng, `W + 1` cột): các món `(nặng, giá trị)` = `(3, 8), (5, 10), (4, 7), (6, 13), (2, 3), (7, 12)`. Chạy với `W = 14` và với `W = 14000`; mỗi lần in giá trị lớn nhất, số ô của bảng (`n * (W + 1)`) và số bit để ghi `W` (`W.bit_length()`). Với `W` lớn, được dùng cách tối ưu bộ nhớ, nhưng số ô tính theo công thức vẫn là `n * (W + 1)`.

In đúng bốn dòng:

```
Tap doc lap lon nhat: <a>, phu dinh nho nhat: <b>, tong = <a + b>
Kiem chung chi: duyet <số cạnh> canh, hop le: CO
Cai tui 0/1 W = 14: toi uu <giá trị>, so o bang <số>, so bit cua W: <số>
Cai tui 0/1 W = 14000: toi uu <giá trị>, so o bang <số>, so bit cua W: <số>
```

Chạy: `python np_khoi.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L26 np_khoi.py`.
