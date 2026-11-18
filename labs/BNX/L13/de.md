# Lab BNX L13 — Lớp Dockerfile phải dựng lại và số đợt cập nhật cuốn chiếu

Bài này không cần Docker hay Kubernetes: ta **mô phỏng** (mô hình Python, không phải Docker hay cụm thật) hai quy tắc đã học (`mau.py`, chỉ dùng Python có sẵn). Số liệu là số minh hoạ.

**Phần 1 — bộ nhớ đệm của lớp.** Mỗi lớp là một bộ `(tên, tệp đầu vào, số giây dựng)`. Chép hai danh sách này vào đầu tệp:

```python
tot = [("FROM", [], 5), ("WORKDIR", [], 1), ("COPY pom.xml", ["pom.xml"], 1),
       ("RUN tai phu thuoc", [], 80),
       ("COPY src", ["src/Dao.java", "src/Main.java"], 2), ("RUN dong goi", [], 25)]
xau = [("FROM", [], 5),
       ("COPY . .", ["pom.xml", "src/Dao.java", "src/Main.java"], 3),
       ("RUN tai va dong goi", [], 105)]
```

Quy tắc: lớp đầu tiên có tệp đầu vào vừa sửa phải dựng lại, và **mọi lớp sau nó** cũng vậy. Viết hàm `dung_lai(lop, sua)` trả về (danh sách số thứ tự lớp từ 1 phải dựng lại, tổng số giây). Rồi in ba dòng:

- `sua src/Dao.java: lop <các số> - <giây> giay` và `sua pom.xml: lop <các số> - <giây> giay` (danh sách `tot`);
- `sai thu tu, sua src/Dao.java: <giây> giay` (danh sách `xau`).

**Phần 2 — cập nhật cuốn chiếu.** `D` bản, được thiếu tối đa `mu` bản, thừa tối đa `ms` bản. Mỗi đợt chờ sẵn sàng thay tối đa `mu + ms` bản mới; sẵn sàng tối thiểu là `D − mu`, số Pod tối đa là `D + ms`. Khi viết bằng phần trăm: `mu` làm tròn **xuống**, `ms` làm tròn **lên**. In hai dòng (số đợt = số lần thay tối đa `mu + ms` bản cho tới khi đủ `D` bản mới):

- `D=12 thieu 1 thua 2: <đợt> dot, toi thieu <số> toi da <số>`
- `D=10 25%/25%: <đợt> dot, toi thieu <số> toi da <số>`

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L13 mau.py`. Đầu ra viết không dấu.
