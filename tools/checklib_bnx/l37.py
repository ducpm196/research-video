"""BNX L37 — T-SQL và JDBC: số dòng lộ ra khi ghép chuỗi so với tham số hoá (chèn mã). Mô hình thuần Python + sqlite3 (thư viện chuẩn, không mạng, không Docker).
Kiểm độc lập ở audit/bnx/ver/l37.py: chạy THẬT trên SQL Server 2022 (bnx-mss), Oracle (qua JDBC) và so với hàm này. Mô hình tổng tiền dùng lại alg.bnx_l06_*."""
import sqlite3 as _sq


def bnx_l37_rows(n, user_input, param, ten_cot="K"):
    """Bảng có n dòng cùng tên 'K'; tìm theo tên với chuỗi người dùng gõ. param=False: ghép chuỗi vào câu lệnh; param=True: truyền tham số.
    Trả số dòng trả về."""
    c = _sq.connect(":memory:")
    c.execute("CREATE TABLE tk (ten TEXT)")
    c.executemany("INSERT INTO tk VALUES (?)", [(ten_cot,)] * n)
    if param:
        rows = c.execute("SELECT ten FROM tk WHERE ten = ?", (user_input,)).fetchall()
    else:
        rows = c.execute("SELECT ten FROM tk WHERE ten = '" + user_input + "'").fetchall()
    return len(rows)
