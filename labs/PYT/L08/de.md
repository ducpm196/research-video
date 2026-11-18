# Lab PYT L08 — Tạo môi trường ảo, cài từ danh sách, in phiên bản

**cần: mạng (bước cài), Python 3.11 trở lên.** Làm trong Git Bash, tại thư mục gốc của bộ khoá (nơi có thư mục `labs`: gõ `pwd` rồi `ls` để kiểm; chưa đúng thì `cd` tới đó, hoặc mở lại bằng *Open Git Bash here*, như bài 0). Lưu ý: `python -m venv .venv-hoc` **tạo thư mục mới `.venv-hoc`** ngay trong thư mục bạn đang đứng (xoá thư mục này là xoá môi trường, không hại gì khác); `pip install` **tải thư viện từ mạng** (PyPI), mất vài phút và có thể in nhiều dòng; không có mạng thì lệnh này báo lỗi, hãy nối mạng rồi chạy lại. Lệnh `-m` chạy một mô-đun có sẵn theo tên (`venv` là mô-đun tạo môi trường ảo):

```bash
python -m venv .venv-hoc
source .venv-hoc/Scripts/activate          # macOS/Linux: source .venv-hoc/bin/activate
pip install -r labs/requirements-py.txt
```

Tạo `in_phien_ban.py`: nạp `matplotlib`, `numpy`, `pandas`, `pytest` và in **bốn dòng** `<tên> <số chính>` (số đứng trước dấu chấm đầu của `<tên>.__version__`), theo thứ tự chữ cái. Chạy `python in_phien_ban.py` trong môi trường vừa tạo và **đối chiếu** từng dòng với các dòng `==` của `labs/requirements-py.txt`.

Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L08 in_phien_ban.py` (máy chấm của khoá dùng môi trường đã cài sẵn các thư viện này).
