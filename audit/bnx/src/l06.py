import lib2
from lib2 import *
from labkit import write_lab, practice_scene  # noqa: E402

lib2.begin("L06")

# ── Mã hiện trên màn hình (chạy NGUYÊN VĂN: audit/bnx/screen/l06.yaml, audit/bnx/ver/l06.py) ──
ORA_SETUP = """
DROP TABLE IF EXISTS bnx_l06_tk;
CREATE TABLE bnx_l06_tk (
  id    NUMBER PRIMARY KEY,
  ten   VARCHAR2(10),
  so_du NUMBER CONSTRAINT bnx_l06_ck CHECK (so_du >= 0));
INSERT INTO bnx_l06_tk VALUES (1, 'A', 300000);
INSERT INTO bnx_l06_tk VALUES (2, 'B', 1000000);
COMMIT;
"""

ORA_PROC = """
CREATE OR REPLACE PROCEDURE bnx_l06_chuyen_tien (
  p_from   IN  NUMBER,
  p_to     IN  NUMBER,
  p_amt    IN  NUMBER,
  p_status OUT VARCHAR2) AS
  v_x   NUMBER;
  v_bal NUMBER;
BEGIN
  IF p_amt IS NULL OR p_amt <= 0 THEN
    RAISE_APPLICATION_ERROR(-20002, 'So tien phai lon hon 0');
  END IF;
  SELECT so_du INTO v_x FROM bnx_l06_tk
   WHERE id = LEAST(p_from, p_to) FOR UPDATE;
  SELECT so_du INTO v_x FROM bnx_l06_tk
   WHERE id = GREATEST(p_from, p_to) FOR UPDATE;
  SELECT so_du INTO v_bal FROM bnx_l06_tk WHERE id = p_from;
  IF v_bal < p_amt THEN
    RAISE_APPLICATION_ERROR(-20001, 'So du khong du');
  END IF;
  UPDATE bnx_l06_tk SET so_du = so_du - p_amt WHERE id = p_from;
  UPDATE bnx_l06_tk SET so_du = so_du + p_amt WHERE id = p_to;
  COMMIT;
  p_status := 'OK';
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    RAISE;
END;
/
"""

ORA_CALL_500 = """
DECLARE
  v_st VARCHAR2(20);
BEGIN
  bnx_l06_chuyen_tien(1, 2, 500000, v_st);
END;
/
SELECT SUM(so_du) AS tong FROM bnx_l06_tk;
"""

ORA_CALL_200 = """
DECLARE
  v_st VARCHAR2(20);
BEGIN
  bnx_l06_chuyen_tien(1, 2, 200000, v_st);
  DBMS_OUTPUT.PUT_LINE('trang thai: ' || v_st);
END;
/
SELECT ten, so_du FROM bnx_l06_tk ORDER BY id;
SELECT SUM(so_du) AS tong FROM bnx_l06_tk;
"""

ORA_NOHANDLER = """
BEGIN
  UPDATE bnx_l06_tk SET so_du = so_du + 500000 WHERE id = 2;
  UPDATE bnx_l06_tk SET so_du = so_du - 500000 WHERE id = 1;
  COMMIT;
END;
/
COMMIT;
SELECT SUM(so_du) AS tong FROM bnx_l06_tk;
"""

ORA_SWALLOW = """
BEGIN
  UPDATE bnx_l06_tk SET so_du = so_du + 500000 WHERE id = 2;
  UPDATE bnx_l06_tk SET so_du = so_du - 500000 WHERE id = 1;
  COMMIT;
EXCEPTION
  WHEN OTHERS THEN NULL;
END;
/
COMMIT;
SELECT SUM(so_du) AS tong FROM bnx_l06_tk;
"""



# ── Đầu ra THẬT (chạy 2026-11-11 trên bnx-ora / bnx-mss; sổ: kind output, of: khối chạy) — lược bằng "…" ──
ORA_CALL_500_OUT = """
ORA-20001: So du khong du
ORA-06512: at "BNX.BNX_L06_CHUYEN_TIEN", line 27
ORA-06512: at "BNX.BNX_L06_CHUYEN_TIEN", line 18
…
      TONG
----------
   1300000
"""
ORA_CALL_200_OUT = """
trang thai: OK
TEN\t\tSO_DU
---------- ----------
A\t       100000
B\t      1200000
      TONG
----------
   1300000
"""
ORA_NOHANDLER_OUT = """
ORA-02290: check constraint (BNX.BNX_L06_CK) violated
      TONG
----------
   1300000
"""
ORA_SWALLOW_OUT = """
      TONG
----------
   1800000
"""

# Phần của thủ tục hiện ở từng bước (dòng tính từ 1)
ORA_PARTS = {"thamso": (1, 11), "khoa": (12, 15), "kiem": (16, 19), "ghi": (20, 23), "loi": (24, 29)}
B0 = "{1: 300000, 2: 1000000}"

# ── Quy mô (AF2, WP4): đếm THẬT số câu lệnh gửi tới cơ sở dữ liệu khi logic chuyển tiền nằm ở ứng dụng. sqlite3 đại diện cho cơ sở dữ liệu
# (sqlite không có thủ tục lưu trữ nên số lần gọi thủ tục chỉ đếm số lần chuyển). ──
Q6 = prog("DemCau", r'''
import sqlite3
db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE tk (id INT, so_du INT)")
db.execute("INSERT INTO tk VALUES (1, 99999999), (2, 0)")
dem = []
db.set_trace_callback(dem.append)      # ghi mỗi câu gửi tới CSDL
def chuyen():                          # logic nằm ở ứng dụng
    for c in ("BEGIN", "SELECT so_du FROM tk WHERE id = 1",
              "UPDATE tk SET so_du = so_du - 1 WHERE id = 1",
              "UPDATE tk SET so_du = so_du + 1 WHERE id = 2", "COMMIT"):
        db.execute(c)
for n in (10, 1000, 100000):
    dem.clear()
    for _ in range(n): chuyen()
    print(n, "chuyen:", len(dem), "cau | thu tuc:", n, "goi")
''', lang="python", claims=["ứng dụng tự làm logic: 5 câu lệnh mỗi lần chuyển (BEGIN, SELECT, 2 UPDATE, COMMIT): 10 → 50, 1000 → 5000, 100000 → 500000 câu"])

# ── Lab (số liệu KHÁC ví dụ: 3 tài khoản 500/400/300, bốn lệnh chuyển) ──
LAB_PY = r'''
import sqlite3

db = sqlite3.connect(":memory:", isolation_level=None)
db.executescript("""
CREATE TABLE tk (id INTEGER PRIMARY KEY, so_du INTEGER CHECK (so_du >= 0));
INSERT INTO tk VALUES (1, 500), (2, 400), (3, 300);
""")


def chuyen(a, b, tien):
    try:
        db.execute("BEGIN")
        db.execute("UPDATE tk SET so_du = so_du + ? WHERE id = ?", (tien, b))
        db.execute("UPDATE tk SET so_du = so_du - ? WHERE id = ?", (tien, a))
        db.execute("COMMIT")
        return "OK"
    except sqlite3.IntegrityError:
        db.execute("ROLLBACK")
        return "loi so du khong du"


for a, b, t in [(1, 2, 300), (2, 3, 900), (3, 1, 50), (1, 3, 250)]:
    print(f"chuyen {a}->{b} {t}: {chuyen(a, b, t)}")
print("tong tien:", db.execute("SELECT SUM(so_du) FROM tk").fetchone()[0])
'''
LAB_OUT = """chuyen 1->2 300: OK
chuyen 2->3 900: loi so du khong du
chuyen 3->1 50: OK
chuyen 1->3 250: OK
tong tien: 1200"""
LAB_DE = """# Lab BNX L06 — Giao dịch chuyển tiền: hoàn tác khi vi phạm ràng buộc số dư

Oracle không có trong bộ chấm, nên lab dùng **sqlite** (có sẵn trong Python, không cần cài thêm) để luyện đúng ý của bài: nhóm câu lệnh cùng thành công hoặc cùng bị huỷ, và tổng tiền giữ nguyên. Số liệu là số minh hoạ. `isolation_level=None` nghĩa là Python không tự mở giao dịch hộ, ta tự gõ `BEGIN` và `COMMIT`. Trong câu SQL, dấu `?` là chỗ điền giá trị (`db.execute("… + ? WHERE id = ?", (tien, b))` điền `tien` rồi `b`); `try … except sqlite3.IntegrityError` thử làm, nếu ràng buộc bị vi phạm thì chạy phần `except`.

Dựng bảng bằng đoạn sau (cho sẵn):

```python
import sqlite3
db = sqlite3.connect(":memory:", isolation_level=None)   # tự quản lý giao dịch
db.executescript('''
CREATE TABLE tk (id INTEGER PRIMARY KEY, so_du INTEGER CHECK (so_du >= 0));
INSERT INTO tk VALUES (1, 500), (2, 400), (3, 300);
''')
```
Viết `mau.py` có hàm `chuyen(a, b, tien)` làm đúng theo thứ tự **cộng tài khoản nhận trước, rồi trừ tài khoản gửi** trong MỘT giao dịch (`BEGIN` … `COMMIT`). Nếu ràng buộc `CHECK` bị vi phạm (sqlite ném `sqlite3.IntegrityError`) thì `ROLLBACK` để phần cộng đã làm cũng bị huỷ, và hàm trả chữ `loi so du khong du`; thành công thì trả `OK`.

Chạy bốn lệnh `(1, 2, 300)`, `(2, 3, 900)`, `(3, 1, 50)`, `(1, 3, 250)` theo thứ tự, mỗi lệnh in một dòng, rồi in tổng tiền sau cùng:
```
chuyen <a>-><b> <tien>: <OK | loi so du khong du>
tong tien: <số>
```
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L06 mau.py`.
"""

# ── Đường khác (AF2): cùng thủ tục viết bằng Python thuần, không có cơ sở dữ liệu ──
PY_MODEL = prog("MoHinh", r'''
so_du = {1: 300000, 2: 1000000}


def chuyen(tu, den, tien):
    if tien <= 0 or so_du[tu] < tien:
        return "loi"
    so_du[tu] -= tien
    so_du[den] += tien
    return "OK"


for tien in (500000, 200000):
    kq = chuyen(1, 2, tien)
    print(tien, kq, so_du, sum(so_du.values()))
''', lang="python", claims=["mô hình Python: chuyển 500 000 bị từ chối (loi), số dư giữ nguyên, tổng 1 300 000; chuyển 200 000 thành OK, A 100 000, B 1 200 000, tổng 1 300 000"])



def build():
    hook = sc("hook", "hook", "Chuyển 500 000 thất bại mà ngân hàng mất 500 000", [
        st("""<p>Tài khoản A có $300\\,000$, tài khoản B có $1\\,000\\,000$. Khách A ra lệnh chuyển $500\\,000$ sang B.</p>
<p>Một thủ tục viết vội: <b>cộng B trước</b>, rồi trừ A. Trừ A lỗi vì không đủ tiền, nhưng phần cộng B vẫn được chốt.</p>
<div class="box warn">Tổng tiền hai tài khoản: trước $1\\,300\\,000$, sau <b class="red">$1\\,800\\,000$</b>. Ngân hàng vừa tự sinh ra $500\\,000$.</div>""",
           """Chào bạn, tài khoản A có ba trăm nghìn, B có một triệu, và khách A ra lệnh chuyển năm trăm nghìn sang B. Một thủ tục viết vội cộng cho B trước, rồi mới trừ A.
           Trừ A lỗi vì không đủ tiền, nhưng phần cộng cho B vẫn được chốt, nên tổng từ một triệu ba trăm nghìn thành một triệu tám trăm nghìn."""),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["viết thủ tục chuyển tiền thế nào", "tham số vào và ra, bằng PL/SQL: ngôn ngữ lập trình của Oracle, chạy ngay trong cơ sở dữ liệu"],
                  ["lỗi giữa chừng thì sao", "khối bắt lỗi: hoàn tác cả giao dịch rồi báo lỗi lên"],
                  ["hai lệnh chuyển ngược chiều cùng lúc", "khoá hai tài khoản theo thứ tự mã tăng dần"],
                  ["gọi một thủ tục khác gì gửi từng câu lẻ", "đếm số câu gửi tới cơ sở dữ liệu ở ba quy mô"]]),
           """Hôm nay ta trả lời bốn câu hỏi. Viết thủ tục chuyển tiền thế nào, bằng PL/SQL, ngôn ngữ lập trình riêng của Oracle chạy ngay trong cơ sở dữ liệu.
           Lỗi giữa chừng thì hoàn tác ra sao. Hai lệnh ngược chiều cùng lúc thì khoá thế nào cho khỏi bế tắc. Và gọi một thủ tục khác gì so với gửi từng câu lẻ.""", clear=True, introduces=["bnx_plsql"]),
    ], checks=[f"alg.bnx_l06_total({B0}) == 1300000",
               f"alg.bnx_l06_total(alg.bnx_l06_batch({B0}, [(2, 500000), (1, -500000)], False)) == 1800000"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu, rồi dựng bảng", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Giao dịch", "nhóm câu lệnh cùng thành công (chốt) hoặc cùng huỷ (hoàn tác)", "trừ A 200 000 và cộng B 200 000: cả hai, hoặc không gì"],
                  ["② Khoá hàng", "<code>SELECT … FOR UPDATE</code> đọc và giữ hàng tới khi chốt hoặc hoàn tác; phiên khác muốn sửa phải chờ", "phiên 1 khoá A, phiên 2 sửa A phải đợi"],
                  ["③ Bế tắc ORA-00060", "<b>phiên</b> là một lần làm việc nối vào cơ sở dữ liệu; bế tắc là khi hai phiên khoá ngược thứ tự rồi chờ nhau; Oracle phát hiện và hoàn tác một câu lệnh của một phiên", "phiên 1 giữ A chờ B, phiên 2 giữ B chờ A"],
                  ["④ Thủ tục lưu trữ", "đoạn mã có tên, cất sẵn trong cơ sở dữ liệu, nhận tham số; ứng dụng gọi bằng tên", "chuyen_tien(1, 2, 200000)"]]),
           """Trước hết ta cần hiểu bốn điều. Giao dịch là nhóm câu lệnh cùng thành công, gọi là chốt, hoặc cùng bị huỷ, gọi là hoàn tác.
           Khoá hàng là đọc một hàng kèm ý định sửa, cơ sở dữ liệu giữ hàng đó tới khi chốt hoặc hoàn tác, nên phiên khác phải chờ. Bế tắc, mã ORA-00060, là khi hai phiên, mỗi phiên là một lần làm việc nối vào cơ sở dữ liệu, khoá ngược thứ tự rồi chờ nhau mãi.
           Thủ tục lưu trữ là đoạn mã có tên, cất sẵn trong cơ sở dữ liệu, để ứng dụng chỉ cần gọi tên."""),
        st(table(["viết trong SQL", "đọc là", "ví dụ"],
                 [["<code>NUMBER</code>, <code>VARCHAR2(10)</code>", "kiểu số; kiểu chuỗi của Oracle, dài tối đa 10 ký tự", "<code>so_du NUMBER</code>, <code>ten VARCHAR2(10)</code>"],
                  ["<code>INSERT INTO bảng VALUES (…)</code>", "thêm một dòng, các giá trị theo thứ tự cột; nhiều dòng thì ngăn các bộ giá trị bằng dấu phẩy", "<code>VALUES (1, 'A', 300000)</code>: mã 1, tên A, số dư 300000"]]),
           """Bảng sắp dựng dùng thêm hai cách viết. Kiểu số, và kiểu chuỗi dài tối đa mười ký tự, khai kiểu cho từng cột. Lệnh thêm dòng đưa các giá trị vào theo thứ tự cột, và nhiều dòng thì ngăn bằng dấu phẩy.""",
           clear=True),
        st("""<p>Dựng bảng hai tài khoản. Chạy trên Oracle Database Free 23 (báo phiên bản 26ai Free 23.26.3), trong <b>Docker</b> (công cụ chạy phần mềm đóng gói sẵn trong một “thùng”).</p>""" + code(ORA_SETUP)
           + """$$300\\,000 + 1\\,000\\,000 = \\hlg{1\\,300\\,000}$$""",
           """Ta dựng bảng trên Oracle chạy trong Docker, công cụ chạy phần mềm đóng gói sẵn. Lệnh xoá bảng nếu đã có giúp chạy lại nhiều lần. Khoá chính là cột mà mỗi dòng có một giá trị riêng.
           Ràng buộc kiểm tra cấm số dư âm, nên dù thủ tục quên kiểm, cơ sở dữ liệu vẫn chặn. Lệnh chốt ghi hai dòng vừa chèn lại. Tổng ba trăm nghìn cộng một triệu là một triệu ba trăm nghìn, phép thử cho mọi lần chạy.""", clear=True),
    ], checks=[f"alg.bnx_l06_total({B0}) == 1300000", "alg.bnx_l06_lock_order(2, 1) == (1, 2)"])

    sym = sc("sym", "symbol", "Giải mã từ khoá PL/SQL", [
        st(table(["PL/SQL (Oracle)", "nghĩa"],
                 [["<code>p_amt IN NUMBER</code>", "tham số vào: người gọi đưa số tiền vào"],
                  ["<code>p_status OUT VARCHAR2</code>", "tham số ra: thủ tục trả chữ <code>OK</code> về cho người gọi"],
                  ["<code>CREATE OR REPLACE PROCEDURE … AS … BEGIN … END;</code>", "đặt tên cho đoạn mã; sau <code>AS</code> khai biến; thân nằm giữa <code>BEGIN</code> và <code>END</code>"],
                  ["<code>SELECT … INTO v_x</code>, <code>p_status := 'OK'</code>", "đưa kết quả câu chọn vào biến; <code>:=</code> gán giá trị cho biến"],
                  ["<code>LEAST(2, 1)</code>, <code>GREATEST(2, 1)</code>", "số nhỏ hơn là 1, số lớn hơn là 2"]]),
           """Từ khoá vào nghĩa là tham số vào, người gọi đưa số tiền vào, còn từ khoá ra là tham số ra, thủ tục ghi chữ báo thành công vào đó để trả về.
           Lệnh tạo thủ tục đặt tên cho đoạn mã, thân nằm giữa từ khoá mở đầu và kết thúc. Câu chọn kèm từ khoá đưa vào chuyển kết quả vào biến, dấu hai chấm bằng gán giá trị cho biến. Hai hàm cuối lấy số nhỏ hơn và số lớn hơn."""),
        st(table(["PL/SQL (Oracle)", "nghĩa"],
                 [["<code>RAISE_APPLICATION_ERROR(-20001, '…')</code>", "tự báo một lỗi có mã riêng, mã nằm trong khoảng −20000 tới −20999"],
                  ["<code>EXCEPTION WHEN OTHERS THEN</code>", "phần bắt lỗi: bắt mọi lỗi xảy ra phía trên"],
                  ["<code>RAISE;</code>", "ném tiếp lỗi vừa bắt lên người gọi"],
                  ["<code>DECLARE … BEGIN … END;</code> rồi <code>/</code>", "khối không tên để gọi thủ tục; dòng <code>/</code> báo công cụ dòng lệnh chạy khối vừa gõ"],
                  ["<code>DBMS_OUTPUT.PUT_LINE('…')</code>", "in một dòng chữ ra màn hình"]]),
           """Lệnh báo lỗi riêng tự tạo một lỗi có mã từ âm hai mươi nghìn tới âm hai mươi nghìn chín trăm chín mươi chín. Phần bắt lỗi bắt mọi lỗi phía trên nó, còn lệnh ném tiếp chuyển lỗi lên người gọi.
           Khối không tên là cách gọi thủ tục từ công cụ dòng lệnh, và dấu gạch chéo ở dòng riêng báo công cụ chạy khối. Hàm cuối in một dòng chữ.""", clear=True, introduces=["bnx_raise_app_error", "bnx_dbms_output"]),
        st(table(["viết trong PL/SQL", "đọc là", "ví dụ"],
                 [["<code>IF điều kiện THEN … END IF;</code>", "nếu điều kiện đúng thì chạy phần giữa", "<code>IF v_bal &lt; p_amt THEN …</code>"],
                  ["<code>p_amt IS NULL</code>", "ô chưa có giá trị (NULL, khác 0); phải hỏi bằng <code>IS NULL</code>, vì <code>= NULL</code> không bao giờ cho đúng", "gọi mà quên đưa số tiền"],
                  ["<code>a OR b</code>", "một trong hai vế đúng là đủ", "<code>p_amt IS NULL OR p_amt &lt;= 0</code>: trống hoặc không dương đều bị chặn"]]),
           """Câu kiểm số tiền dùng ba cách viết. Nếu điều kiện đúng thì chạy phần giữa. Giá trị trống là ô chưa có gì, khác không, nên phải hỏi bằng từ khoá là trống chứ không so bằng. Từ hoặc nối hai vế: một vế đúng là đủ, nên số tiền trống hay không dương đều bị chặn.""",
           clear=True),
        st(table(["câu SQL", "nghĩa"],
                 [["<code>SELECT cột FROM bảng WHERE điều kiện</code>", "chọn cột từ bảng, chỉ những dòng thoả điều kiện; <code>UPDATE bảng SET cột = giá trị WHERE …</code> sửa những dòng đó"],
                  ["<code>SUM(so_du) AS tong</code>", "cộng cả cột <code>so_du</code>; <code>AS tong</code> đặt tên <code>tong</code> cho cột kết quả"],
                  ["<code>ORDER BY id</code>", "sắp xếp kết quả theo cột <code>id</code>"],
                  ["<code>'trang thai: ' || v_st</code>", "<code>||</code> nối hai chuỗi lại với nhau"]]),
           """Trước các câu SQL đầu tiên, ta nhắc lại cách đọc. Câu chọn lấy cột từ bảng, chỉ những dòng thoả điều kiện, còn câu cập nhật sửa những dòng đó. Hàm tổng cộng cả cột và đặt tên cho kết quả, rồi sắp xếp theo một cột, và hai gạch đứng nối hai chuỗi.""",
           clear=True),
    ], checks=["alg.bnx_l06_lock_order(2, 1) == (1, 2)", "alg.bnx_l06_lock_order(1, 2) == (1, 2)"])

    intu = sc("intuition", "intuition", "Hình dung: thứ tự khoá, và số phận giao dịch khi một câu lỗi", [
        st(svg(1500, 470,
               panel(20, 20, 700, 430, "Khoá theo chiều chuyển: bế tắc", C_RED),
               box(60, 100, 280, 80, ["Lệnh 1: A sang B", "khoá A rồi B"], C_BLUE, size=22),
               box(400, 100, 280, 80, ["Lệnh 2: B sang A", "khoá B rồi A"], C_AMBER, size=22),
               box(60, 290, 280, 90, ["giữ A", "chờ B"], C_GRAY, size=22),
               box(400, 290, 280, 90, ["giữ B", "chờ A"], C_GRAY, size=22),
               arrow(200, 185, 200, 285), arrow(540, 185, 540, 285),
               arrow(345, 315, 395, 315, "#dc2626"), arrow(395, 360, 345, 360, "#dc2626"),
               txt(370, 425, "chờ nhau mãi: ORA-00060", 22, "middle", "#dc2626", True),
               panel(780, 20, 700, 430, "Khoá theo mã tăng dần: không bế tắc", C_GREEN),
               box(820, 100, 280, 80, ["Lệnh 1: A sang B", "khoá 1 rồi 2"], C_BLUE, size=22),
               box(1160, 100, 280, 80, ["Lệnh 2: B sang A", "khoá 1 rồi 2"], C_AMBER, size=22),
               box(820, 290, 280, 90, ["giữ 1 và 2", "chạy xong, nhả"], C_GREEN, size=22),
               box(1160, 290, 280, 90, ["chờ 1", "rồi chạy tiếp"], C_GRAY, size=22),
               arrow(960, 185, 960, 285), arrow(1300, 185, 1300, 285),
               arrow(1155, 335, 1105, 335, "#16a34a"),
               txt(1130, 425, "chỉ chờ một chiều, không có vòng tròn", 22, "middle", "#16a34a", True)),
           """Bên trái khoá theo chiều chuyển. Lệnh một khoá A trước, lệnh hai chuyển ngược lại nên khoá B trước, nên mỗi lệnh giữ một tài khoản và chờ tài khoản kia mãi, và Oracle báo bế tắc.
           Bên phải khoá theo mã tăng dần: cả hai lệnh đều khoá mã một trước, nên lệnh sau chỉ chờ lệnh trước xong, không có vòng tròn."""),
        st(svg(1500, 520,
               box(40, 40, 400, 80, "Bắt đầu giao dịch", C_GRAY, size=24),
               box(40, 160, 400, 80, ["Câu 1: cộng B 500 000", "thành công"], C_GREEN, size=22),
               box(40, 280, 400, 80, ["Câu 2: trừ A 500 000", "lỗi: A chỉ có 300 000"], C_RED, size=22),
               arrow(240, 125, 240, 155), arrow(240, 245, 240, 275),
               panel(540, 20, 440, 430, "Phần bắt lỗi nuốt lỗi", C_AMBER, size=24),
               box(570, 110, 380, 90, ["lỗi bị nuốt", "khối chạy xong như thành công"], C_AMBER, size=22),
               box(570, 240, 380, 90, ["chốt: còn phần cộng B"], C_AMBER, size=22),
               box(570, 350, 380, 80, "tổng 1 800 000", C_RED, size=24, bold=True),
               panel(1030, 20, 440, 430, "Không bắt, hoặc hoàn tác rồi ném tiếp", C_GREEN, size=21),
               box(1060, 110, 380, 90, ["hoàn tác phần đã làm", "huỷ luôn câu 1"], C_GREEN, size=22),
               box(1060, 240, 380, 90, ["báo lỗi lên người gọi"], C_GREEN, size=22),
               box(1060, 350, 380, 80, "tổng 1 300 000", C_GREEN, size=24, bold=True),
               arrow(445, 320, 565, 165, "#d97706"),
               '<line x1="240" y1="365" x2="240" y2="495" stroke="#16a34a" stroke-width="3.5" stroke-dasharray="8 6"/>',
               '<line x1="240" y1="495" x2="1250" y2="495" stroke="#16a34a" stroke-width="3.5" stroke-dasharray="8 6"/>',
               arrow(1250, 495, 1250, 455, "#16a34a", dash=True)),
           """Câu một cộng B thành công, câu hai trừ A lỗi vì bảng cấm số dư âm. Nếu phần bắt lỗi nuốt lỗi, câu cộng B được chốt, tổng thành một triệu tám trăm nghìn.
           Nếu không bắt, hoặc hoàn tác rồi ném tiếp, cả câu một bị huỷ và tổng giữ một triệu ba trăm nghìn."""),
    ], checks=[f"alg.bnx_l06_total(alg.bnx_l06_swallow({B0}, [(2, 500000), (1, -500000)], 'null')) == 1800000",
               f"alg.bnx_l06_total(alg.bnx_l06_swallow({B0}, [(2, 500000), (1, -500000)], 'none')) == 1300000"])

    def op(part, title=None):
        return code(ORA_PROC, title, lines=ORA_PARTS[part])

    form = sc("formula", "formula", "Suy ra từng bước: dựng thủ tục chuyển tiền trên Oracle", [
        st("""<p><b>Bước 1. Tham số, rồi chặn số tiền không dương.</b> Người gọi đưa vào: từ tài khoản nào, tới tài khoản nào, bao nhiêu tiền. Thủ tục trả ra một chữ trạng thái.</p>"""
           + op("thamso") + """<p class='note'>Làm thử: chuyển 200 000 từ 1 sang 2 thì p_from = 1, p_to = 2, p_amt = 200 000; gọi với −100 000 thì báo lỗi −20002.</p>""",
           """Bước một là tham số. Người gọi phải nói chuyển từ đâu, tới đâu và bao nhiêu, nên thủ tục có ba tham số vào và một tham số ra để trả chữ trạng thái.
           Vì số tiền âm kéo tiền ngược từ người nhận về, nên việc đầu tiên là chặn số tiền không lớn hơn không; gọi với âm một trăm nghìn thì bị báo lỗi."""),
        st("""<p><b>Bước 2. Khoá hai tài khoản theo mã tăng dần</b>, dù tiền đi chiều nào.</p>""" + op("khoa")
           + """<p class='note'>Làm thử: chuyển từ 2 sang 1 thì vẫn khoá LEAST(2, 1) = 1 trước, rồi GREATEST(2, 1) = 2.</p>""",
           """Bước hai, khoá hai tài khoản. Vì hai lệnh khoá ngược thứ tự sẽ bế tắc, ta luôn khoá mã nhỏ trước, mã lớn sau, dù tiền đi chiều nào.
           Mỗi câu chọn kèm cụm khoá để cập nhật, nên hàng bị giữ tới khi chốt hoặc hoàn tác. Chuyển từ hai sang một vẫn khoá mã một trước.""", clear=True),
        st("""<p><b>Bước 3. Kiểm số dư, thiếu thì báo lỗi</b> trước khi ghi bất cứ gì.</p>""" + op("kiem")
           + """<p class='note'>Làm thử: 300 000 &lt; 500 000 nên báo lỗi −20001.</p>""",
           """Bước ba, kiểm số dư. Hai tài khoản đã bị khoá, số dư đọc lúc này không ai đổi được, nên kiểm ở đây là chắc chắn. Khối điều kiện chỉ chạy phần bên trong khi điều kiện đúng.
           Thiếu tiền thì báo lỗi mã âm hai mươi nghìn lẻ một: ba trăm nghìn nhỏ hơn năm trăm nghìn nên thủ tục báo lỗi.""", clear=True),
        st("""<p><b>Bước 4. Trừ, cộng, chốt</b>, rồi mới ghi trạng thái.</p>""" + op("ghi")
           + """<p class='note'>Làm thử: 300 000 − 200 000 = 100 000; 1 000 000 + 200 000 = 1 200 000.</p>""",
           """Bước bốn, trừ tài khoản gửi, cộng tài khoản nhận, rồi chốt. Hai câu cập nhật cùng một giao dịch, nên cùng được ghi hoặc cùng bị huỷ.
           Dấu hai chấm bằng gán chữ thành công vào tham số ra.""", clear=True),
        st("""<p><b>Bước 5. Bắt lỗi: hoàn tác, rồi báo lên.</b></p>""" + op("loi")
           + """<p class='note'>Làm thử: lỗi ở bước 3, hoàn tác, người gọi nhận lỗi −20001, tổng vẫn 1 300 000.</p>""",
           """Bước năm là phần bắt lỗi. Lỗi trong chương trình còn gọi là ngoại lệ, tức một sự cố được ném ra và có thể bị bắt lại.
           Câu nào phía trên cũng có thể ném ngoại lệ, nên phần này hoàn tác mọi thứ đã làm và nhả hai khoá. Rồi lệnh ném tiếp đẩy lỗi lên người gọi.""", clear=True, introduces=["bnx_ngoai_le"]),
    ], checks=["alg.bnx_l06_lock_order(2, 1) == (1, 2)",
               f"alg.bnx_l06_transfer({B0}, 1, 2, 500000) == (False, {B0})",
               f"alg.bnx_l06_transfer({B0}, 1, 2, 200000) == (True, {{1: 100000, 2: 1200000}})"])

    ex = sc("example", "example", "Ví dụ chạy thật trên Oracle, từng phép tính", [
        st("""<p>Gọi thủ tục chuyển $500\\,000$ từ A sang B, rồi cộng tổng số dư.</p>""" + code(ORA_CALL_500),
           """Ta chạy thật trên Oracle. Khối không tên này khai một biến nhận trạng thái, gọi thủ tục chuyển năm trăm nghìn từ tài khoản một sang hai, và dấu gạch chéo báo công cụ chạy khối.
           Câu chọn cuối cộng tổng số dư để xem tiền có lệch không."""),
        st("""$$① \\; 300\\,000 < 500\\,000 \\;\\Rightarrow\\; \\hl{\\text{báo lỗi −20001}}$$""" + out(ORA_CALL_500_OUT),
           """Phép tính thứ nhất, ba trăm nghìn nhỏ hơn năm trăm nghìn, nên thủ tục báo lỗi mã âm hai mươi nghìn lẻ một.""",
           introduces=["implies"], clear=True),
        st("""$$② \\; 300\\,000 + 1\\,000\\,000 = \\hlg{1\\,300\\,000}$$
<p>Phần bắt lỗi đã hoàn tác: hai số dư không đổi, tổng in ra đúng $1\\,300\\,000$.</p>""",
           """Phép tính thứ hai, phần bắt lỗi đã hoàn tác nên hai số dư không đổi. Ba trăm nghìn cộng một triệu vẫn là một triệu ba trăm nghìn, khớp tổng máy in ra."""),
        st("""<p>Gọi lại với $200\\,000$:</p>""" + code(ORA_CALL_200)
           + """$$③ \\; 300\\,000 - 200\\,000 = \\hl{100\\,000}\\ \\text{(A)}$$""",
           """Bây giờ gọi lại với hai trăm nghìn. Lệnh in cho ta thấy trạng thái trả về, rồi hai câu chọn in số dư và tổng.
           Phép tính thứ ba, A còn ba trăm nghìn trừ hai trăm nghìn, bằng một trăm nghìn.""",
           clear=True),
        st("""$$④ \\; 1\\,000\\,000 + 200\\,000 = \\hl{1\\,200\\,000}\\ \\text{(B)}$$
$$⑤ \\; 100\\,000 + 1\\,200\\,000 = \\hlg{1\\,300\\,000}$$""" + out(ORA_CALL_200_OUT),
           """Phép tính thứ tư, B có một triệu cộng hai trăm nghìn, bằng một triệu hai trăm nghìn. Phép tính thứ năm cộng hai kết quả trên, bằng một triệu ba trăm nghìn, tổng không đổi.""", clear=True),
    ], checks=[f"alg.bnx_l06_transfer({B0}, 1, 2, 500000)[0] is False",
               f"alg.bnx_l06_total(alg.bnx_l06_transfer({B0}, 1, 2, 500000)[1]) == 1300000",
               f"alg.bnx_l06_transfer({B0}, 1, 2, 200000)[1][1] == 100000",
               f"alg.bnx_l06_transfer({B0}, 1, 2, 200000)[1][2] == 1200000",
               f"alg.bnx_l06_total(alg.bnx_l06_transfer({B0}, 1, 2, 200000)[1]) == 1300000"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: tính lại bằng Python thuần", [
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>so_du = {1: 300000, 2: 1000000}</code>", "từ điển: bảng tra từ mã tài khoản sang số dư; <code>so_du[tu] -= tien</code> trừ bớt <code>tien</code> ở mục <code>tu</code>"],
                  ["<code>def chuyen(tu, den, tien): … return \"OK\"</code>", "định nghĩa hàm nhận ba đầu vào; <code>return</code> trả kết quả ra"],
                  ["<code>sum(so_du.values())</code>", "<code>.values()</code> lấy các giá trị của từ điển, <code>sum</code> cộng chúng lại"]]),
           """Mã Python sắp tới có vài cách viết mới, nên ta giải nghĩa trước. Từ điển là bảng tra từ mã tài khoản sang số dư, hàm nhận ba đầu vào rồi trả kết quả ra, và hàm cuối cộng mọi giá trị của từ điển.""",
           clear=True),
        st(PY_MODEL.show(title="Mô hình Python thuần: cùng thủ tục, không có cơ sở dữ liệu"),
           """Ta kiểm bằng đường khác, vì muốn chắc kết quả không phụ thuộc Oracle: viết lại thủ tục bằng Python thuần, rồi chạy hai lần chuyển như trên.""",
           clear=True),
        st(PY_MODEL.out_html(),
           """Vì kiểm số dư trước khi ghi, lần chuyển năm trăm nghìn bị từ chối và số dư giữ nguyên. Lần hai trăm nghìn cho A một trăm nghìn và B một triệu hai trăm nghìn, trùng với đầu ra của Oracle.""",
           clear=True),
    ], checks=[f"alg.bnx_l06_transfer({B0}, 1, 2, 200000)[1] == {{1: 100000, 2: 1200000}}"])

    quymo = sc("quymo", "example", "Khi số lệnh chuyển tăng: số câu lệnh gửi tới cơ sở dữ liệu (mô hình giản lược)", [
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>sqlite3.connect(\":memory:\", isolation_level=None)</code>", "mở một cơ sở dữ liệu nhỏ trong bộ nhớ; <code>isolation_level=None</code>: Python không tự mở giao dịch, ta tự gõ <code>BEGIN</code>"],
                  ["<code>db.set_trace_callback(dem.append)</code>", "mỗi câu SQL gửi tới <code>db</code> thì thêm vào danh sách <code>dem</code>, để đếm"],
                  ["<code>for _ in range(n): …</code>", "lặp <code>n</code> lần; <code>_</code> là tên biến bỏ đi, không dùng giá trị"]]),
           """Khối đo dùng vài cách viết mới, nên ta giải nghĩa trước. Tuỳ chọn cách ly bằng không nghĩa là Python không tự mở giao dịch. Hàm theo dõi ghi mỗi câu gửi đi vào một danh sách để đếm, và dấu gạch dưới là tên biến bỏ đi trong vòng lặp.""",
           clear=True),
        st(Q6.show(lines=(1, 11), title="Mô hình giản lược: logic nằm ở ứng dụng, đếm mọi câu gửi đi (sqlite làm đại diện)"),
           """Đây là mô hình giản lược, không phải số đo của Oracle. Ta giả sử logic nằm ở ứng dụng, và mỗi lần chuyển gửi năm câu: mở giao dịch, đọc số dư, hai câu cập nhật, chốt.
           Số câu thật phụ thuộc cách viết, và Java thật không gửi riêng câu mở giao dịch.""",
           clear=True),
        st(Q6.show(lines=(12, 15), title="Vòng ngoài: thử ba mức")
           + Q6.out_html(),
           """Vòng ngoài thử ba mức. Kết quả chạy thật của mô hình: mười lần chuyển gửi năm mươi câu, một nghìn lần gửi năm nghìn câu, một trăm nghìn lần gửi năm trăm nghìn câu. Số câu gấp năm lần số lệnh vì ta giả định năm câu mỗi lần.""", clear=True),
        st(table(["số lệnh chuyển", "ứng dụng tự làm (mô hình 5 câu): câu gửi đi", "gọi thủ tục: lần gọi", "chờ nếu 1 ms mỗi lần đi–về, tức gửi câu lệnh qua mạng rồi nhận kết quả (số minh hoạ)"],
                 [["10", "50", "10", "50 ms so với 10 ms"], ["1 000 (gấp 100 lần)", "5 000", "1 000", "5 giây so với 1 giây"],
                  ["100 000 (gấp 10 000 lần)", "500 000", "100 000", "500 giây so với 100 giây"]]),
           """Bảng đặt hai cách cạnh nhau. Một lượt đi về là gửi câu lệnh qua mạng rồi nhận kết quả. Gọi thủ tục chỉ cần một lượt cho mỗi lệnh, nên với một mili giây mỗi lượt, một trăm nghìn lệnh chờ một trăm giây thay vì năm trăm giây.""",
           clear=True),
        st(table(["cách", "được", "mất", "khi nào chọn"],
                 [["logic ở ứng dụng", "dễ viết, dễ kiểm thử, dễ đổi cơ sở dữ liệu", "nhiều lần đi–về hơn (mô hình: gấp năm); khoá bị giữ lâu hơn vì chờ mạng giữa các câu", "tải thấp"],
                  ["thủ tục lưu trữ", "một lần gọi; khoá chỉ giữ lúc thủ tục chạy", "logic nằm trong cơ sở dữ liệu: khó kiểm thử, gắn chặt với một hệ, sửa là phải triển khai vào đó", "đường nóng, nhiều lệnh mỗi giây"]]),
           """Bảng này cho thấy điều phải chọn. Logic ở ứng dụng dễ viết, dễ kiểm thử, nhưng đi về nhiều hơn và giữ khoá lâu hơn vì chờ mạng giữa các câu.
           Thủ tục lưu trữ gọi một lần và giữ khoá ngắn, đổi lại logic nằm trong cơ sở dữ liệu, khó kiểm thử, gắn chặt một hệ.""",
           focus=[0, "1.2", "1.3"], clear=True),
    ], checks=["[alg.bnx_l06_statements(n) for n in (10, 1000, 100000)] == [50, 5000, 500000]",
               "[alg.bnx_l06_statements(n) // 5 for n in (10, 1000, 100000)] == [10, 1000, 100000]",
               "alg.bnx_l06_statements(1000) * 1 // 1000 == 5 and 100000 * 1 // 1000 == 100 and alg.bnx_l06_statements(100000) // 1000 == 500"])

    write_lab("BNX", "L06", LAB_DE, "py", LAB_PY, LAB_OUT)
    lab_pr = practice_scene(sc, "Tự làm: chuyển tiền có hoàn tác (sqlite)", lib2.practice_steps2(
        st, "BNX", "L06",
        """<p><b>Đề</b>: sqlite có bảng <code>tk</code> (3 tài khoản 500, 400, 300; <code>CHECK (so_du &gt;= 0)</code>). Viết <code>mau.py</code> có <code>chuyen(a, b, tien)</code>:</p>
<ol><li>trong một giao dịch: <b>cộng B trước, rồi trừ A</b></li><li>vi phạm <code>CHECK</code> (<code>sqlite3.IntegrityError</code>) thì <code>ROLLBACK</code>, trả <code>loi so du khong du</code>; không thì <code>COMMIT</code>, trả <code>OK</code></li></ol>
<p>Chạy bốn lệnh, in mỗi lệnh một dòng, rồi in tổng tiền. <code>isolation_level=None</code> nghĩa là Python không tự mở giao dịch, ta tự gõ <code>BEGIN</code>. Dữ liệu và khuôn dòng in nằm trong <code>de.md</code>.</p>
<p class="note">Trong câu SQL, <code>?</code> là chỗ điền giá trị; <code>try … except</code> thử làm, lỗi ràng buộc thì chạy phần <code>except</code>. Phần Oracle của bài (thủ tục, ORA-20001, bế tắc) bộ chấm không có; muốn tự chạy, xem lệnh Docker ở cuối phần này.</p>""",
        """Bây giờ tới phần bạn tự làm, trên cơ sở dữ liệu nhỏ có sẵn trong Python vì bộ chấm không có Oracle. Viết hàm chuyển tiền: cộng bên nhận trước rồi trừ bên gửi trong một giao dịch, hoàn tác nếu vi phạm ràng buộc số dư.
        Phần Oracle chỉ để bạn tự chạy thêm, lệnh ở cuối phần này. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> mở giao dịch bằng <code>db.execute("BEGIN")</code>, đặt hai câu cập nhật và <code>COMMIT</code> trong <code>try</code>, và <code>ROLLBACK</code> trong <code>except sqlite3.IntegrityError</code>. Tổng tiền phải bằng 1200 trước và sau.
Lời giải ở <code>labs/BNX/L06/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, mở giao dịch bằng lệnh bắt đầu, đặt hai câu cập nhật và lệnh chốt trong khối thử, và hoàn tác trong khối bắt lỗi ràng buộc. Tổng tiền phải bằng một nghìn hai trăm trước và sau. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã tự thử.""", pause=120), "BNX", "L06")
    lab_pr["steps"].append(st(table(["lệnh", "nghĩa"],
                                    [["<code>docker run -d --name ora-thu -p 1521:1521 -e … gvenzl/oracle-free:23-slim</code>", "chạy một “thùng” phần mềm ở nền (<code>-d</code>), đặt tên <code>ora-thu</code>, mở cổng 1521 ra máy (<code>-p</code>), đặt biến cấu hình như mật khẩu (<code>-e</code>); dòng cuối là tên ảnh phần mềm"],
                                     ["<code>docker logs ora-thu</code>", "xem nhật ký của thùng; đợi dòng <code>DATABASE IS READY TO USE!</code> rồi mới vào"],
                                     ["<code>docker exec -it ora-thu sqlplus bnx/…@//localhost/FREEPDB1</code>", "chạy <code>sqlplus</code>, dòng lệnh SQL của Oracle, bên trong thùng, với tài khoản <code>bnx</code>"]]),
                              """Muốn chạy phần Oracle của bài, bạn dựng bản miễn phí bằng Docker, công cụ chạy phần mềm trong một thùng đóng gói sẵn. Lệnh đầu chạy thùng ở nền và mở cổng, lệnh thứ hai xem nhật ký để đợi sẵn sàng, và lệnh cuối mở dòng lệnh SQL trong thùng.""",
                              clear=True))

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người đã đi làm): bắt lỗi rồi nuốt lỗi.</b> Trước hết xem khối <b>không</b> bắt lỗi: cộng B trước, trừ A sau.</div>"""
           + code(ORA_NOHANDLER),
           """Lỗi thứ nhất, của người đã đi làm, là bắt lỗi rồi nuốt lỗi. Trước hết xem khối không bắt lỗi: cộng B trước, rồi trừ A năm trăm nghìn."""),
        st(out(ORA_NOHANDLER_OUT) + """<p class='note'>Câu trừ A vi phạm ràng buộc; lỗi về tới người gọi, Oracle hoàn tác mọi thay đổi của lời gọi đó.</p>""",
           """Câu trừ A vi phạm ràng buộc, lỗi đi thẳng về người gọi, và Oracle hoàn tác mọi thay đổi của lời gọi đó, nên tổng vẫn một triệu ba trăm nghìn.
           Nếu có ai bắt lỗi ở giữa thì thay đổi còn nguyên.""",
           clear=True),
        st(code(ORA_SWALLOW),
           """Giờ chỉ thêm một phần bắt mọi lỗi mà không làm gì cả. Các câu còn lại giữ nguyên.""", clear=True),
        st(out(ORA_SWALLOW_OUT)
           + """<p class='note'><code>WHEN OTHERS THEN NULL</code>: không báo lỗi nào, câu cộng B còn lại và được chốt. Cách chữa: hoàn tác rồi <code>RAISE</code> như bước 5.</p>""",
           """Lỗi bị nuốt, nên khối chạy xong như thành công, câu cộng cho B còn lại và được chốt, tổng thành một triệu tám trăm nghìn mà không có thông báo nào.
           Cách chữa là hoàn tác rồi ném tiếp lỗi, như bước năm.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm): quên rằng chốt và hoàn tác trong thủ tục tác động lên cả giao dịch của người gọi.</b> Dòng người gọi ghi trước mà chưa chốt bị chốt theo khi thủ tục chốt, và mất theo khi thủ tục hoàn tác.</div>""",
           """Lỗi thứ hai là quên rằng chốt và hoàn tác trong thủ tục tác động lên cả giao dịch của người gọi.
           Dòng người gọi ghi trước mà chưa chốt sẽ bị chốt theo, hoặc mất theo. Vậy hãy gọi thủ tục khi người gọi chưa có việc dở.""", clear=True),
    ], checks=[f"alg.bnx_l06_total(alg.bnx_l06_swallow({B0}, [(2, 500000), (1, -500000)], 'none')) == 1300000",
               f"alg.bnx_l06_total(alg.bnx_l06_swallow({B0}, [(2, 500000), (1, -500000)], 'null')) == 1800000"])

    Q = "{1: 800000, 2: 200000}"
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "A = 800 000, B = 200 000. Gọi thủ tục chuyển 900 000 từ A sang B. Người gọi nhận gì, A còn bao nhiêu, tổng bao nhiêu?"],
                  ["2", "Cùng lúc: lệnh P chuyển 100 000 từ A (mã 1) sang B (mã 2), lệnh Q chuyển 50 000 từ B sang A. Mỗi lệnh khoá mã nào trước? Số dư cuối?"],
                  ["3", "Quyết định: đặt logic chuyển tiền trong thủ tục lưu trữ, hay trong dịch vụ Java (mã Java mở giao dịch, gửi từng câu lệnh)?"]]),
           """Đến lượt bạn, ba câu trên màn hình. Câu ba chọn thủ tục lưu trữ hay dịch vụ Java. Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: $800\\,000 < 900\\,000$ nên thủ tục báo lỗi −20001 và hoàn tác.</p>
$$800\\,000 + 200\\,000 = \\hlg{1\\,000\\,000}\\ \\text{(A vẫn 800 000)}$$""",
           """Đáp án câu một. Tám trăm nghìn nhỏ hơn chín trăm nghìn, nên người gọi nhận lỗi âm hai mươi nghìn lẻ một và giao dịch được hoàn tác. A vẫn tám trăm nghìn, tổng vẫn một triệu."""),
        st("""<p>Câu 2: cả P và Q đều khoá mã 1 rồi mã 2, nên lệnh sau chờ lệnh trước, không bế tắc.</p>
$$A = 800\\,000 - 100\\,000 + 50\\,000 = \\hl{750\\,000}$$
$$B = 200\\,000 + 100\\,000 - 50\\,000 = \\hl{250\\,000}$$""",
           """Đáp án câu hai. Cả hai lệnh đều khoá mã một trước rồi mã hai, nên lệnh sau chỉ chờ lệnh trước, không bế tắc.
           A còn bảy trăm năm mươi nghìn, B còn hai trăm năm mươi nghìn, tổng vẫn một triệu."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["thủ tục lưu trữ", "một lần gọi qua mạng; khoá giữ ngắn vì mọi câu chạy ngay trong cơ sở dữ liệu", "mỗi hệ một ngôn ngữ riêng; khó kiểm thử, khó quản lý phiên bản cùng mã ứng dụng"],
                  ["dịch vụ Java", "một ngôn ngữ, kiểm thử và triển khai như mã thường", "nhiều lượt đi về qua mạng trong lúc đang giữ khoá; phải cấu hình đúng việc hoàn tác khi lỗi"]]),
           """Đáp án câu ba, không có lựa chọn đúng cho mọi nơi. Thủ tục lưu trữ chỉ cần một lần gọi qua mạng, đổi lại mỗi hệ một ngôn ngữ riêng và khó kiểm thử.
           Dịch vụ Java kiểm thử như mã thường, nhưng mỗi câu là một lượt đi về trong lúc giữ khoá."""),
    ], checks=[f"alg.bnx_l06_transfer({Q}, 1, 2, 900000) == (False, {Q})",
               f"alg.bnx_l06_total({Q}) == 1000000",
               "alg.bnx_l06_lock_order(1, 2) == alg.bnx_l06_lock_order(2, 1) == (1, 2)",
               f"alg.bnx_l06_transfer(alg.bnx_l06_transfer({Q}, 1, 2, 100000)[1], 2, 1, 50000)[1] == {{1: 750000, 2: 250000}}",
               f"alg.bnx_l06_transfer(alg.bnx_l06_transfer({Q}, 2, 1, 50000)[1], 1, 2, 100000)[1] == {{1: 750000, 2: 250000}}"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("tham số vào, ra", "khoá theo mã tăng dần", "kiểm rồi mới ghi", "lỗi thì hoàn tác và báo lên", "tổng giữ nguyên"),
           """Tổng kết: thủ tục nhận tham số vào và trả tham số ra, khoá hai tài khoản theo mã tăng dần, kiểm số dư rồi mới ghi.
           Có lỗi thì hoàn tác cả giao dịch và báo lên người gọi, nhờ vậy tổng tiền giữ nguyên."""),
        st("""<div class='box key'><b>Tư duy:</b> đừng tin “lỗi thì tự hoàn tác”. Hãy chạy thử một lỗi ở <b>giữa</b> giao dịch và đo tổng tiền trước và sau, trên đúng hệ bạn dùng.</div>""",
           """Điều cần mang theo. Đừng tin rằng có lỗi thì hệ thống tự hoàn tác. Hãy chạy thử một lỗi ở giữa giao dịch và đo tổng tiền trước và sau, trên đúng hệ bạn dùng."""),
        st("""<p class="note">Bài sau: Oracle cho khối lượng lớn, chia bảng giao dịch theo tháng và lưu dữ liệu JSON. Bài 37: thủ tục chuyển tiền trên SQL Server, chặn câu lệnh lạ chèn qua chuỗi người dùng gõ, và gọi từ Java.</p>""",
           """Ở bài sau, ta xem Oracle xử lý bảng giao dịch rất lớn: chia bảng theo tháng và lưu dữ liệu dạng JSON.""",
           forward_ref=True),
    ])
    return lesson("L06", "thu_tuc_luu_tru_plsql_tsql",
                  "Bài 6 — Thủ tục lưu trữ trên Oracle: tham số, giao dịch và bắt lỗi",
                  "curriculum/bnx.yaml L06; audit/bnx/verify_bnx.py L06; Oracle Database PL/SQL Language Reference 23 (RAISE_APPLICATION_ERROR, unhandled exceptions) "
                  "và Concepts (statement-level rollback, row locks, deadlocks), chạy thật trên Oracle AI Database 26ai Free 23.26.3 (đọc 2026-11-11)",
                  ["Viết thủ tục chuyển tiền có tham số vào và ra bằng PL/SQL", "Hoàn tác khi lỗi bằng khối bắt lỗi PL/SQL và nhận ra lỗi bị nuốt",
                   "Khoá hai tài khoản theo một thứ tự cố định",
                   "So số câu lệnh gửi tới cơ sở dữ liệu khi logic nằm ở ứng dụng (mô hình giản lược 5 câu mỗi lần) với khi gọi thủ tục, ở 10, 1 000 và 100 000 lần chuyển",
                   "Viết hàm chuyển tiền có giao dịch và hoàn tác khi vi phạm ràng buộc số dư"],
                  [hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec],
                  covers=[(1, "formula"), (2, "example"), (3, "formula"), (4, "quymo"), (5, "practice")])
