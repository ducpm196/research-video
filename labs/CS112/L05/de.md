# Lab CS112 L05 — Dựng cây tìm kiếm nhị phân, duyệt, đo chiều cao

Cần: Python 3.11 trở lên (kiểm: `python --version` trong Git Bash). Không cần cài thêm thư viện.

Cách tạo tệp: mở một **trình soạn thảo chữ thuần** (Notepad, VS Code; không dùng Word), gõ nội dung, lưu với tên `cay_nhi_phan.py` (đuôi `.py`, mã hoá UTF-8) vào **thư mục gốc của bộ khoá** (thư mục chứa `labs`), rồi mở Git Bash tại đó.

Gõ lớp nút (một nút có khoá và hai con; `None` nghĩa là không có con), số liệu minh hoạ, **khác ví dụ trong bài**:

```python
class Nut:
    def __init__(self, khoa, trai=None, phai=None):
        self.khoa = khoa
        self.trai = trai
        self.phai = phai
```

Viết các hàm đệ quy (cây rỗng là `None`):
1. `them(goc, khoa)`: nếu `goc` là `None` thì trả nút mới; nếu `khoa < goc.khoa` thì `goc.trai = them(goc.trai, khoa)`, ngược lại `goc.phai = them(goc.phai, khoa)`; cuối cùng trả `goc`.
2. `duyet_giua(nut)` (trái, nút, phải) và `duyet_truoc(nut)` (nút, trái, phải): trả danh sách các khoá; cây rỗng trả `[]`.
3. `chieu_cao(nut)`: cây rỗng cao `-1`, ngược lại `1 + max(chiều cao hai con)`.
4. `la_cay_tim_kiem(nut)`: `True` khi danh sách `duyet_giua(nut)` tăng ngặt từng cặp liền nhau.

Rồi chạy và in đúng chữ không dấu, theo thứ tự:
- Dựng cây bằng cách chèn lần lượt `50, 30, 70, 20, 40, 60, 80, 10, 45` vào cây rỗng; in `giua: <các khoá cách nhau một dấu cách>`, `truoc: <...>`, `chieu cao: <số>`, và `he so goc: <chiều cao con trái - chiều cao con phải của gốc>`.
- Chèn lần lượt `1, 2, 3, 4, 5, 6, 7` vào cây rỗng khác; in `chen 1..7 theo thu tu: chieu cao <số>`.
- Cây `Nut(8, Nut(3, Nut(1), Nut(9)), Nut(10))`: in `cay hong: dung` nếu `la_cay_tim_kiem` trả `True`, ngược lại `cay hong: sai`. Cây dựng ở đầu: in `cay tot: dung` hoặc `cay tot: sai` theo cùng cách.

Chạy: `python cay_nhi_phan.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh CS112 L05 cay_nhi_phan.py`.
