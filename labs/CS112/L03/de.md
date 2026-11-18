# Lab CS112 L03 — Đếm số lần chép của mảng động và chèn đầu danh sách liên kết

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện.

Cách tạo tệp: mở một **trình soạn thảo chữ thuần** (Notepad, VS Code; không dùng Word), gõ nội dung, lưu với tên `mang_dong.py` (đuôi `.py`, mã hoá UTF-8) vào **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó.

**Phần 1 — đếm số lần chép.** Mảng động bắt đầu với sức chứa 1. Thêm lần lượt `n` phần tử; khi thêm phần tử thứ `dang_co + 1` mà `dang_co == suc_chua` (mảng đầy) thì phải chép `dang_co` phần tử sang vùng mới, rồi sức chứa mới là `tang(suc_chua)`. Viết hàm `chep(n, tang)` trả về **tổng số lần chép** (thêm `dang_co` vào biến đếm mỗi lần đầy). `tang` là một hàm truyền vào: `lambda s: s * 2` nhận sức chứa `s` và trả `s * 2` (gấp đôi), `lambda s: s + 10` trả `s + 10` (xin thêm 10 ô).

**Phần 2 — danh sách liên kết.** Gõ lớp nút sau (số liệu minh hoạ, **khác ví dụ trong bài**):

```python
class Nut:
    def __init__(self, gia_tri, tiep=None):
        self.gia_tri = gia_tri
        self.tiep = tiep
```

Viết `chen_dau(dau, gia_tri)`: tạo nút mới chứa `gia_tri`, cho nó trỏ (`tiep`) vào nút đầu cũ `dau`, rồi **trả về nút mới** (đó là đầu danh sách mới). Viết `duyet(dau)`: đi từ `dau` theo `tiep` tới khi gặp `None`, trả về danh sách Python các `gia_tri` theo thứ tự đi qua.

**In đúng chữ không dấu**, theo thứ tự:
1. Với `n` trong `(1000, 5000)`, hai dòng: `n = <n> gap doi: <số> lan chep` rồi `n = <n> them 10 o: <số> lan chep`.
2. Dựng danh sách `1 -> 2` (`Nut(1, Nut(2))`), chèn lần lượt 5, 6, 7 vào đầu, rồi in `sau khi chen 5, 6, 7 vao dau: ` tiếp theo là các giá trị nối bằng ` -> ` (dùng `" -> ".join(str(x) for x in duyet(dau))`).

Chạy: `python mang_dong.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L03 mang_dong.py`.
