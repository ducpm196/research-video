# Lab PYT L13 — Dựng dự án nhỏ và tự chấm bằng thang 10 điểm

**cần: pip install -r labs/requirements-py.txt** (trong môi trường ảo của bài 8). Tạo `du_an.py` gồm:

1. dòng đầu `import pytest` (máy chấm cần thấy thư viện này);
2. hàm chấm dưới đây, **chép nguyên**;
3. chuỗi `MODULE` và `TESTS` **do bạn viết**, rồi ghi `phan_tich.py`, `test_phan_tich.py`, `requirements.txt` vào một thư mục tạm (`tempfile.TemporaryDirectory()`) và gọi `cham(thu_muc)`. Lưu ý: viết `MODULE` và `TESTS` bằng chuỗi ba nháy thô `r'''…'''` (chuỗi ba nháy: mọi thứ giữa hai bộ ba nháy, kể cả xuống dòng thật, là một chuỗi; chữ `r` giữ nguyên dấu gạch chéo, nên `\n` trong tệp mã viết y như thường). Mỗi tiêu chí CHUA có dòng `Ly do` ngay dưới.

**Yêu cầu của dự án** (khớp thang điểm):
- `phan_tich.py`: `tong_theo_loai(duong_dan)` đọc CSV (cột `ma,loai,so_tien`) **từng dòng** (không `.read(`, không `readlines`), trả `(dict tổng theo loại, số dòng bỏ qua)`; dòng `so_tien` không phải số thì **bỏ qua và đếm**.
- `test_phan_tich.py`: đúng **3** ca (`test_tong`, `test_dong_hong`, `test_rong`), qua hết.
- `requirements.txt`: có dòng ghim `==` (ví dụ `pytest==9.2.0`).

**Thang điểm (hàm chấm):** 1) đọc từng dòng 2đ · 2) kết quả đúng 3đ · 3) tệp rỗng 2đ · 4) ba ca kiểm qua 2đ · 5) ghim phiên bản 1đ.

**Cách đọc hàm chấm** (đọc trước khi chép; không cần hiểu từng chữ của máy, chỉ cần nắm mỗi việc nó làm): `read_text` đọc tệp thành chuỗi, và việc 1 kiểm trong mã của bạn không có `.read(`; việc 2 và 3 nạp mô-đun bạn vừa ghi rồi gọi hàm của bạn với dữ liệu mẫu (`sys.path` là danh sách thư mục mà máy tìm mô-đun, theo thứ tự; `sys.path.insert(0, …)` chèn thư mục của bạn lên **đầu**; `import phan_tich` nạp tệp `phan_tich.py` ở đó); việc 4 chạy công cụ kiểm thử như gõ lệnh ở cửa sổ lệnh (`subprocess.run([...], capture_output=True, text=True)`: `sys.executable` là đường dẫn chính bản Python đang chạy, `capture_output=True` giữ đầu ra lại, `text=True` cho đầu ra là chữ); việc 5 kiểm `requirements.txt` có dấu `==`.

```python
import subprocess
import sys
import tempfile
from pathlib import Path

DU_LIEU = "ma,loai,so_tien\n1,chuyen,500000\n2,nap,2000000\n3,rut,300000\n4,chuyen,xyz\n5,nap,1000000\n6,chuyen,150000\n"

def cham(thu_muc):
    p = Path(thu_muc)
    ma = (p / "phan_tich.py").read_text(encoding="utf-8")
    diem = 0
    c1 = ".read(" not in ma and "readlines" not in ma
    print("1. Doc tung dong:", "DAT" if c1 else "CHUA", "(2/2)" if c1 else "(0/2)")
    if not c1:
        print("   Ly do: phan_tich.py con dung .read( hoac readlines")
    diem = diem + (2 if c1 else 0)
    sys.path.insert(0, str(p))  # sys.path: danh sach thu muc may tim mo-dun; chen thu muc cua ban len dau
    import phan_tich as mo_dun  # nap phan_tich.py vua ghi
    (p / "du_lieu.csv").write_text(DU_LIEU, encoding="utf-8")
    ket = mo_dun.tong_theo_loai(str(p / "du_lieu.csv"))
    c2 = ket == ({"chuyen": 650000, "nap": 3000000, "rut": 300000}, 1)
    print("2. Ket qua dung:", "DAT" if c2 else "CHUA", "(3/3)" if c2 else "(0/3)")
    if not c2:
        print("   Ly do: nhan duoc", ket, "- mong doi ({'chuyen': 650000, 'nap': 3000000, 'rut': 300000}, 1)")
    diem = diem + (3 if c2 else 0)
    (p / "rong.csv").write_text("ma,loai,so_tien\n", encoding="utf-8")
    ket = mo_dun.tong_theo_loai(str(p / "rong.csv"))
    c3 = ket == ({}, 0)
    print("3. Tep rong:", "DAT" if c3 else "CHUA", "(2/2)" if c3 else "(0/2)")
    if not c3:
        print("   Ly do: nhan duoc", ket, "- mong doi ({}, 0)")
    diem = diem + (2 if c3 else 0)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--tb=line", "-p", "no:cacheprovider", "test_phan_tich.py"], cwd=p, capture_output=True, text=True)
    c4 = r.returncode == 0 and "3 passed" in r.stdout
    print("4. Ba ca kiem qua:", "DAT" if c4 else "CHUA", "(2/2)" if c4 else "(0/2)")
    if not c4:
        print("   Ly do (pytest):", " | ".join(r.stdout.strip().split("\n")[-4:]))
    diem = diem + (2 if c4 else 0)
    req = (p / "requirements.txt").read_text(encoding="utf-8")
    c5 = "==" in req
    print("5. Ghim phien ban:", "DAT" if c5 else "CHUA", "(1/1)" if c5 else "(0/1)")
    if not c5:
        print("   Ly do: requirements.txt khong co dong ghim ==")
    diem = diem + (1 if c5 else 0)
    print("Tong diem:", str(diem) + "/10")
```

4. **Phần đo** (không nằm trong thang điểm trên; máy chấm so cả dòng này): sau khi gọi `cham`, ghi hai tệp CSV `lon.csv` (cột `ma,loai,so_tien`, mọi dòng là `nap` và `100`) — lần một `2000` dòng, lần hai `20000` dòng. Với mỗi tệp: `tracemalloc.start()`, gọi `tong_theo_loai` (nạp từ mô-đun đã ghi, ví dụ `exec(MODULE, ns)` hay `sys.path.insert(0, thu_muc)` rồi `from phan_tich import tong_theo_loai`), lấy đỉnh bộ nhớ bằng `tracemalloc.get_traced_memory()[1]`, rồi `tracemalloc.stop()`. In đúng một dòng: `Bo nho khi dong tang 10 lan: gan nhu khong doi` nếu đỉnh ở 20000 dòng nhỏ hơn 3 lần đỉnh ở 2000 dòng, ngược lại `Bo nho khi dong tang 10 lan: tang theo so dong`. (Lab chấm hình dạng của kết quả, không chấm số byte tuyệt đối vì mỗi máy một khác.)

**Cách nạp mô-đun vừa ghi từ thư mục tạm** (chọn một; làm khi thư mục tạm còn tồn tại, tức còn trong khối `with`):

```python
# Cách 1: sys.path là danh sách thư mục mà máy tìm mô-đun, theo thứ tự; chèn thư mục tạm lên đầu rồi nạp như thường
import sys
sys.path.insert(0, str(thu_muc))
from phan_tich import tong_theo_loai

# Cách 2: chạy chuỗi mã MODULE vào một từ điển rỗng, rồi lấy hàm ra từ đó
ns = {}
exec(MODULE, ns)                      # exec chạy một chuỗi mã như chạy một tệp
tong_theo_loai = ns["tong_theo_loai"]
```

**Thời gian:** bài này nặng nhất khoá, dự kiến 45 đến 60 phút. Video tạm dừng 4 phút để bạn bắt đầu (bạn có thể bấm dừng thêm cho đủ lượt đầu: hàm chấm và ba tệp); phần đo làm ở lượt sau, tiếp tục sau khi video chạy lại. Dự án nhỏ mẫu (`tong_tien.py` + `test_tong_tien.py`) ở phần ví dụ của bài là hình mẫu cho cấu trúc ba tệp.

Chạy: `python du_an.py` (kỳ vọng `Tong diem: 10/10` rồi dòng đo). Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L13 du_an.py`.
