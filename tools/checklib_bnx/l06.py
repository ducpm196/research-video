"""BNX L06 — mô hình thuần Python của thủ tục chuyển tiền (Oracle PL/SQL và T-SQL) và của hai chế độ xử lý lỗi giữa giao dịch.
Không gọi cơ sở dữ liệu. Bộ kiểm audit/bnx/ver/l06.py chạy THẬT trên Oracle và SQL Server trong Docker rồi so với các hàm này."""
import sqlite3 as _sq


def bnx_l06_lock_order(frm, to):
    """Thứ tự khoá của thủ tục: tài khoản có mã nhỏ trước, mã lớn sau (LEAST rồi GREATEST)."""
    return (min(frm, to), max(frm, to))


def bnx_l06_transfer(bal, frm, to, amt):
    """Thủ tục chuyển tiền: số tiền không dương hoặc không đủ số dư thì báo lỗi và hoàn tác (số dư giữ nguyên), đủ thì trừ, cộng, chốt.
    Trả (thành công?, bảng số dư mới)."""
    b = dict(bal)
    if amt is None or amt <= 0 or b[frm] < amt:   # số tiền không dương: lỗi −20002 / 50002; thiếu số dư: −20001 / 50001
        return False, dict(bal)
    b[frm] -= amt
    b[to] += amt
    return True, b


def bnx_l06_total(bal):
    t = 0
    for v in bal.values():
        t += v
    return t


def bnx_l06_batch(bal, stmts, xact_abort):
    """Một giao dịch gồm các câu UPDATE (mã tài khoản, số cộng thêm), ràng buộc số dư >= 0, cuối cùng chốt nếu giao dịch còn mở.
    xact_abort=False (mặc định của SQL Server): câu lỗi bị huỷ riêng, giao dịch chạy tiếp và được chốt.
    xact_abort=True: câu lỗi làm hoàn tác cả giao dịch. Trả bảng số dư sau cùng."""
    b = dict(bal)
    for acc, delta in stmts:
        if b[acc] + delta < 0:
            if xact_abort:
                return dict(bal)
            continue
        b[acc] += delta
    return b


def bnx_l06_swallow(bal, stmts, handler):
    """Khối PL/SQL chạy các câu UPDATE; câu lỗi ném ngoại lệ, các câu sau không chạy.
    handler='none': không bắt lỗi → lỗi về tới ứng dụng, Oracle hoàn tác cả lời gọi (hoàn tác cấp câu lệnh).
    handler='null': WHEN OTHERS THEN NULL → lỗi bị nuốt, các câu đã chạy vẫn còn và được chốt sau đó."""
    b = dict(bal)
    for acc, delta in stmts:
        if b[acc] + delta < 0:
            return dict(bal) if handler == "none" else b
        b[acc] += delta
    return b


def bnx_l06_inject_rows(user_input, param):
    """Số dòng trả về khi tìm theo tên với chuỗi người dùng gõ: ghép chuỗi (param=False) hay truyền tham số (param=True).
    Chạy thật trên SQLite trong bộ nhớ với hai tài khoản A, B."""
    c = _sq.connect(":memory:")
    c.execute("CREATE TABLE tk (ten TEXT, so_du INTEGER)")
    c.executemany("INSERT INTO tk VALUES (?, ?)", [("A", 300000), ("B", 1000000)])
    if param:
        rows = c.execute("SELECT ten, so_du FROM tk WHERE ten = ?", (user_input,)).fetchall()
    else:
        rows = c.execute("SELECT ten, so_du FROM tk WHERE ten = '" + user_input + "'").fetchall()
    return len(rows)
