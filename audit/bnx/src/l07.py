import lib2
from lib2 import *
from l16 import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
from labkit import write_lab, practice_scene  # noqa: E402

# ── Mã hiện trên màn hình (chạy NGUYÊN VĂN: audit/bnx/screen/l07.yaml, audit/bnx/ver/l07.py) ──
# Bài L07 đã được tách (2026-11-14): hàng đợi, bộ nhớ cột và phân mảnh sang bài L38; ở đây còn phân vùng và JSON.
PART_DDL = """
DROP TABLE IF EXISTS bnx_l07_gd;
CREATE TABLE bnx_l07_gd (
  id      NUMBER,
  ngay    DATE,
  so_tien NUMBER)
PARTITION BY RANGE (ngay)
INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))
(PARTITION p_2025_01 VALUES LESS THAN (DATE '2025-02-01'));
"""

ROWNUM_DEMO = """
SELECT ROWNUM FROM dual CONNECT BY ROWNUM <= 3;
"""

PART_LOAD = """
INSERT INTO bnx_l07_gd
SELECT ROWNUM, DATE '2025-01-01' + TRUNC((ROWNUM - 1) / 10),
       (MOD(ROWNUM, 100) + 1) * 100000
FROM dual CONNECT BY ROWNUM <= 3650;
COMMIT;
SELECT COUNT(*) AS so_dong FROM bnx_l07_gd;
SELECT COUNT(*) AS so_phan_vung FROM user_tab_partitions
 WHERE table_name = 'BNX_L07_GD';
"""

PLAN_MONTH = """
EXPLAIN PLAN FOR
SELECT COUNT(*) FROM bnx_l07_gd
 WHERE ngay >= DATE '2025-03-01' AND ngay < DATE '2025-04-01';
SELECT * FROM TABLE(
  DBMS_XPLAN.DISPLAY(NULL, NULL, 'BASIC +PARTITION'));
"""

PLAN_ALL = """
EXPLAIN PLAN FOR
SELECT COUNT(*) FROM bnx_l07_gd WHERE so_tien > 5000000;
SELECT * FROM TABLE(
  DBMS_XPLAN.DISPLAY(NULL, NULL, 'BASIC +PARTITION'));
"""

PLAN_TRUNC = """
EXPLAIN PLAN FOR
SELECT COUNT(*) FROM bnx_l07_gd
 WHERE TRUNC(ngay, 'MM') = DATE '2025-03-01';
SELECT * FROM TABLE(
  DBMS_XPLAN.DISPLAY(NULL, NULL, 'BASIC +PARTITION'));
"""

PART_CHECK = """
SELECT COUNT(*) AS loc_ngay FROM bnx_l07_gd
 WHERE ngay >= DATE '2025-03-01' AND ngay < DATE '2025-04-01';
SELECT COUNT(*) AS trong_pv FROM bnx_l07_gd
 PARTITION FOR (DATE '2025-03-15');
"""

JSON_DDL = """
DROP TABLE IF EXISTS bnx_l07_js;
CREATE TABLE bnx_l07_js (
  id       NUMBER PRIMARY KEY,
  chi_tiet VARCHAR2(400)
           CONSTRAINT bnx_l07_isj CHECK (chi_tiet IS JSON));
INSERT INTO bnx_l07_js VALUES (1, '{"kenh":"app","so_tien":500000}');
INSERT INTO bnx_l07_js VALUES (2, '{"kenh":"atm","so_tien":2000000}');
COMMIT;
"""

JSON_QUERY = """
INSERT INTO bnx_l07_js VALUES (3, '{"kenh":"app"');
SELECT id,
       JSON_VALUE(chi_tiet, '$.kenh' RETURNING VARCHAR2(10)) AS kenh
FROM bnx_l07_js
WHERE JSON_VALUE(chi_tiet, '$.so_tien' RETURNING NUMBER) > 1000000;
"""

JSON_LAX = """
SELECT CASE WHEN '{kenh:''app''}' IS JSON
            THEN 'nhan' ELSE 'tu choi' END AS lax,
       CASE WHEN '{kenh:''app''}' IS JSON (STRICT)
            THEN 'nhan' ELSE 'tu choi' END AS strict
FROM dual;
"""

DROP_PART = """
ALTER TABLE bnx_l07_gd DROP PARTITION FOR (DATE '2025-01-15');
ROLLBACK;
SELECT COUNT(*) AS so_dong FROM bnx_l07_gd;
"""

DOCKER_RUN = r"""
docker run -d --name ora-thu -p 1521:1521 \
  -e ORACLE_PASSWORD=Mat_Khau_Thu \
  -e APP_USER=bnx -e APP_USER_PASSWORD=bnx_pass \
  gvenzl/oracle-free:23-slim
docker logs -f ora-thu
docker exec -it ora-thu sqlplus bnx/bnx_pass@//localhost/FREEPDB1
"""

# ── Đầu ra THẬT (chạy trên bnx-ora, Oracle AI Database 26ai Free 23.26.3; sqlplus căn cột bằng tab) — lược bằng "…" ──
ROWNUM_OUT = """
    ROWNUM
----------
\t 1
\t 2
\t 3
"""
LOAD_OUT = """
   SO_DONG
----------
      3650
SO_PHAN_VUNG
------------
\t  12
"""
PLAN_MONTH_OUT = """
--------------------------------------------------------------
| Id  | Operation\t\t| Name\t     | Pstart| Pstop |
--------------------------------------------------------------
|   0 | SELECT STATEMENT\t|\t     |\t     |\t     |
|   1 |  SORT AGGREGATE \t|\t     |\t     |\t     |
|   2 |   PARTITION RANGE SINGLE|\t     |\t   3 |\t   3 |
|   3 |    TABLE ACCESS FULL\t| BNX_L07_GD |\t   3 |\t   3 |
--------------------------------------------------------------
"""
PLAN_ALL_OUT = """
-----------------------------------------------------------
| Id  | Operation\t     | Name\t  | Pstart| Pstop |
-----------------------------------------------------------
|   0 | SELECT STATEMENT     |\t\t  |\t  |\t  |
|   1 |  SORT AGGREGATE      |\t\t  |\t  |\t  |
|   2 |   PARTITION RANGE ALL|\t\t  |\t1 |1048575|
|   3 |    TABLE ACCESS FULL | BNX_L07_GD |\t1 |1048575|
-----------------------------------------------------------
"""
PLAN_TRUNC_OUT = """
…
|   2 |   PARTITION RANGE ALL|\t\t  |\t1 |1048575|
|   3 |    TABLE ACCESS FULL | BNX_L07_GD |\t1 |1048575|
"""
CHECK_OUT = """
  LOC_NGAY
----------
       310
  TRONG_PV
----------
       310
"""
JSON_OUT = """
ORA-02290: check constraint (BNX.BNX_L07_ISJ) violated
\tID KENH
---------- ----------
\t 2 atm
"""
JSON_LAX_OUT = """
LAX\tSTRICT
------- -------
nhan\ttu choi
"""
DROP_PART_OUT = """
   SO_DONG
----------
      3340
"""

# BRIEF mục 6 (2026-11-11): JSON đã dò 8/8, được đọc trong lời.
SAY_WORDS = {"«JSON»": "JSON"}


def S(show, say, **kw):
    for a_, b_ in SAY_WORDS.items():
        say = say.replace(a_, b_)
    return st(show, say, **kw)


LOAD = "alg.bnx_l07_load(3650)"

# ── Quy mô (AF2, WP4): nạp lại bảng gấp 100 lần (365 000 dòng) trên Oracle thật rồi đếm cả bảng và riêng phân vùng tháng 3 ──
ORA_SCALE = """
DROP TABLE IF EXISTS bnx_l07_lon;
CREATE TABLE bnx_l07_lon (id NUMBER, ngay DATE, so_tien NUMBER)
PARTITION BY RANGE (ngay) INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))
(PARTITION p0 VALUES LESS THAN (DATE '2025-02-01'));
INSERT INTO bnx_l07_lon
SELECT ROWNUM, DATE '2025-01-01' + TRUNC((ROWNUM - 1) / 1000), 100000
FROM dual CONNECT BY ROWNUM <= 365000;
COMMIT;
SELECT COUNT(*) AS ca_nam FROM bnx_l07_lon;
SELECT COUNT(*) AS thang_3 FROM bnx_l07_lon
 PARTITION FOR (DATE '2025-03-15');
"""
ORA_SCALE_OUT = """
    CA_NAM
----------
    365000
   THANG_3
----------
     31000
"""

# ── Lab (số liệu KHÁC ví dụ; sqlite làm đại diện vì bộ chấm không có Oracle) ──
LAB_PY = r'''
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE gd (id INTEGER PRIMARY KEY,"
           " chi_tiet TEXT CHECK (json_valid(chi_tiet)))")
DONG = [(1, '{"kenh":"atm","may":"A7","tien":500000}'),
        (2, '{"kenh":"app","thiet_bi":"d9","tien":200000}'),
        (3, '{"kenh":"atm","may":"B2"'),
        (4, '{"kenh":"app","thiet_bi":"d1","tien":900000}'),
        (5, '{"kenh":"atm","may":"A7","tien":300000}')]
for i, js in DONG:
    try:
        db.execute("INSERT INTO gd VALUES (?, ?)", (i, js))
    except sqlite3.IntegrityError:
        print(f"dong {i}: tu choi (JSON hong)")
tong = db.execute("SELECT SUM(json_extract(chi_tiet, '$.tien')) FROM gd"
                  " WHERE json_extract(chi_tiet, '$.kenh') = 'atm'").fetchone()[0]
print("tong tien kenh atm:", tong)
app = db.execute("SELECT COUNT(*) FROM gd WHERE chi_tiet ->> '$.kenh' = 'app'").fetchone()[0]
print("so giao dich kenh app:", app)
a7 = db.execute("SELECT COUNT(*) FROM gd WHERE chi_tiet ->> '$.may' = 'A7'").fetchone()[0]
print("may A7:", a7, "giao dich")
'''
LAB_OUT = """dong 3: tu choi (JSON hong)
tong tien kenh atm: 800000
so giao dich kenh app: 2
may A7: 2 giao dich"""
LAB_DE = """# Lab BNX L07 — JSON có ràng buộc kiểm hợp lệ, truy vấn theo trường

Oracle không có trong bộ chấm, nên lab dùng **sqlite** (có sẵn trong Python; cần bản sqlite từ 3.38, có sẵn hàm JSON) để luyện ý của bài: cột JSON có ràng buộc `IS JSON` bên Oracle tương ứng `CHECK (json_valid(...))` bên sqlite (`json_valid` trả đúng khi chuỗi là JSON hợp lệ), và lấy trường trong JSON bằng `json_extract` (lấy một trường theo đường dẫn như `'$.tien'`) hoặc toán tử `->>`. Số liệu là số minh hoạ.

Viết `mau.py`:
1. Bảng `gd (id INTEGER PRIMARY KEY, chi_tiet TEXT CHECK (json_valid(chi_tiet)))`.
2. Chèn lần lượt năm dòng sau; dòng nào vi phạm `CHECK` (sqlite ném `sqlite3.IntegrityError`) thì in `dong <id>: tu choi (JSON hong)` và bỏ qua:
```python
DONG = [(1, '{"kenh":"atm","may":"A7","tien":500000}'),
        (2, '{"kenh":"app","thiet_bi":"d9","tien":200000}'),
        (3, '{"kenh":"atm","may":"B2"'),
        (4, '{"kenh":"app","thiet_bi":"d1","tien":900000}'),
        (5, '{"kenh":"atm","may":"A7","tien":300000}')]
```
3. In tổng `tien` của kênh `atm`, số giao dịch của kênh `app`, và số giao dịch của máy `A7` (lấy trường bằng `json_extract(chi_tiet, '$.tien')` hoặc toán tử `->>`).

Trong Python, `try … except sqlite3.IntegrityError` thử làm và chạy phần `except` khi ràng buộc bị vi phạm; dấu `?` trong câu SQL là chỗ điền giá trị (`db.execute("INSERT INTO gd VALUES (?, ?)", (i, js))`).

In đúng bốn dòng:
```
dong 3: tu choi (JSON hong)
tong tien kenh atm: <số>
so giao dich kenh app: <số>
may A7: <số> giao dich
```
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L07 mau.py`.

**Làm thêm trên Oracle thật (không chấm tự động):** dựng Oracle Free bằng Docker theo bài, dán lại khối tạo bảng, nạp 3 650 dòng và chạy kế hoạch của tháng ba; bạn phải thấy `PARTITION RANGE SINGLE` với Pstart = Pstop = 3.
"""


def C(text, title=None, lines=None):
    """Khối mã có ký tự đô la (đường dẫn JSON): viết thành thực thể &#36; để lint/KaTeX không ghép hai dấu đô la thành công thức;
    trình duyệt và cổng screen_code (giải mã thực thể) vẫn thấy đúng ký tự đô la."""
    return code(text, title, lines).replace("$", "&#36;")


def build():
    hook = sc("hook", "hook", "Sao kê một tháng mà phải đọc cả năm giao dịch", [
        S("""<p>Bảng giao dịch thẻ của một ngân hàng thêm hàng trăm triệu dòng mỗi năm (số minh hoạ). Khách xin sao kê <b>tháng 3</b>.</p>
<div class="box warn">Nếu bảng là một khối liền, máy có thể phải quét cả <b>12 tháng</b> để lấy ra 1 tháng. Xoá dữ liệu cũ hết hạn lưu cũng phải xoá từng dòng.</div>""",
          """Chào bạn, bảng giao dịch thẻ của một ngân hàng có thể thêm hàng trăm triệu dòng mỗi năm, đây là số minh hoạ. Một khách xin sao kê tháng ba.
          Nếu bảng là một khối liền, máy có thể phải quét cả mười hai tháng chỉ để lấy ra một tháng. Xoá dữ liệu cũ hết hạn lưu cũng phải xoá từng dòng."""),
        S(table(["câu hỏi", "bài này trả lời"],
                [["chỉ đọc đúng tháng cần", "phân vùng bảng theo tháng, đọc kế hoạch thực thi"],
                 ["dữ liệu mỗi kênh một kiểu", "lưu và truy vấn JSON ngay trong Oracle"],
                 ["chạy thử ở đâu", "Oracle Free 23 trong Docker: bạn tự dựng được"]])
          + """<p class="note"><b>JSON</b>: chuỗi chữ ghi các cặp <code>tên trường: giá trị</code> trong ngoặc nhọn, như <code>{"kenh":"app","tien":200000}</code>.</p>""",
          """Hôm nay ta trả lời ba câu hỏi. Chỉ đọc đúng tháng cần bằng cách phân vùng bảng theo tháng. Lưu dữ liệu mỗi kênh một kiểu dạng «JSON», tức chuỗi chữ ghi các cặp tên trường và giá trị trong ngoặc nhọn, ngay trong Oracle.
          Và mọi ví dụ chạy thật trên Oracle bản miễn phí số hai mươi ba, loại bạn tự dựng được bằng Docker."""),
    ], checks=["alg.bnx_l07_partitions(alg.bnx_l07_load(3650)) == 12"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        S(table(["khái niệm", "nghĩa", "ví dụ"],
                [["① Quét toàn bảng và chỉ mục", "không có đường tắt thì đọc từng dòng; chỉ mục cây B là cấu trúc phụ giữ giá trị đã xếp thứ tự thành cây nhiều tầng, như mục lục sách, nên đi thẳng tới dòng cần", "tìm một mã giao dịch: chỉ mục; đếm cả tháng: thường phải quét"],
                 ["② Kế hoạch thực thi", "bản kế hoạch máy chọn để chạy câu lệnh: đọc bảng nào, theo cách nào", "đọc toàn bảng giao dịch"],
                 ["③ Kiểu dữ liệu và mốc ngày", "<code>NUMBER</code> là số, <code>DATE</code> là ngày; <code>DATE '2025-02-01'</code> viết một ngày cụ thể", "mốc 1/2/2025"],
                 ["④ Chốt (<code>COMMIT</code>)", "lệnh làm mọi thay đổi trước đó thành chính thức", "nạp dữ liệu xong thì chốt"],
                 ["⑤ Từ điển dữ liệu", "các bảng hệ thống do Oracle tự giữ, liệt kê bảng và phân vùng của bạn", "<code>user_tab_partitions</code>"]]),
          """Trước hết ta cần hiểu năm điều. Khi không có đường tắt, máy đọc từng dòng, gọi là quét toàn bảng. Chỉ mục cây B xếp sẵn giá trị thành cây nhiều tầng, như mục lục sách, nên đi thẳng tới dòng cần.
          Kế hoạch thực thi là bản kế hoạch máy chọn để chạy một câu lệnh. Chữ ngày kèm một chuỗi viết một ngày cụ thể, như mùng một tháng hai năm hai nghìn không trăm hai mươi lăm.
          Lệnh chốt làm mọi thay đổi thành chính thức. Từ điển dữ liệu là các bảng hệ thống của Oracle, liệt kê bảng và phân vùng của bạn."""),
        S("""<p>Dữ liệu mẫu của bài: năm 2025, mỗi ngày 10 giao dịch.</p>
$$365 \\cdot 10 = \\hl{3\\,650}\\ \\text{dòng}, \\qquad 31 \\cdot 10 = \\hl{310}\\ \\text{dòng của tháng 3}$$""",
          """Một ví dụ số làm dữ liệu mẫu cho cả bài. Năm hai nghìn không trăm hai mươi lăm có ba trăm sáu mươi lăm ngày, mỗi ngày mười giao dịch, nên có ba nghìn sáu trăm năm mươi dòng.
          Dấu chấm ở giữa là phép nhân. Tháng ba có ba mươi mốt ngày, nên có ba trăm mười dòng.""", clear=True),
    ], checks=["alg.bnx_l07_days('2025-01-01', '2026-01-01') * 10 == len(alg.bnx_l07_load(3650))",
               "alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-03-01', '2025-04-01') == alg.bnx_l07_month_days(2025, 3) * 10 == 310"])

    sym = sc("sym", "symbol", "Giải mã từ khoá", [
        S(table(["trên màn hình", "nghĩa"],
                [["<code>PARTITION BY RANGE (ngay)</code>", "chia bảng thành phân vùng theo khoảng giá trị của cột ngày (khoá phân vùng)"],
                 ["<code>INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))</code>", "mỗi phân vùng dài 1 tháng (hàm đổi số 1 thành khoảng 1 tháng); dữ liệu vượt mốc thì Oracle tự tạo phân vùng mới"],
                 ["<code>(PARTITION p_2025_01 VALUES LESS THAN (DATE '2025-02-01'))</code>", "khai phân vùng đầu tên <code>p_2025_01</code>: chứa các dòng có ngày nhỏ hơn 1/2/2025"],
                 ["<code>DATE '2025-01-01' + TRUNC((ROWNUM - 1) / 10)</code>", "cộng số ngày vào một ngày; <code>TRUNC</code> bỏ phần lẻ, <code>MOD(a, b)</code> lấy phần dư; ví dụ <code>TRUNC(25 / 10)</code> = 2, <code>MOD(25, 10)</code> = 5"]]),
          """Bảng đầu giải mã lệnh tạo bảng. Dòng đầu chia bảng theo khoảng giá trị của cột ngày, gọi là khoá phân vùng. Dòng hai nói mỗi phân vùng dài một tháng, vượt mốc thì Oracle tự tạo phân vùng mới.
          Dòng ba khai phân vùng đầu, chứa các dòng có ngày nhỏ hơn mùng một tháng hai. Dòng cuối cộng số ngày vào một ngày, một hàm bỏ phần lẻ, một hàm lấy phần dư.""",
          introduces=["bnx_khoa_phan_vung"]),
        S(table(["trên màn hình", "nghĩa"],
                [["<code>EXPLAIN PLAN FOR</code> …", "ghi kế hoạch thực thi của câu lệnh sau nó, mà không chạy câu lệnh"],
                 ["<code>SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY(NULL, NULL, 'BASIC +PARTITION'))</code>", "in kế hoạch vừa ghi: <code>TABLE(…)</code> biến kết quả của hàm thành bảng để <code>SELECT *</code> đọc ra; <code>NULL, NULL</code> bỏ trống hai tham số, chuỗi cuối chọn cột hiện"],
                 ["<code>PARTITION RANGE SINGLE</code> / <code>ALL</code>; <code>Pstart</code>, <code>Pstop</code>", "chỉ đọc một phân vùng / đọc mọi phân vùng; phân vùng đầu và cuối sẽ đọc (đánh số từ 1)"],
                 ["<code>TABLE ACCESS FULL</code>, <code>SORT AGGREGATE</code>", "đọc hết phần được chọn; gom kết quả thành một số của <code>COUNT</code>"]]),
          """Bảng thứ hai giải mã phần xem kế hoạch. Lệnh xem kế hoạch ghi cách máy sẽ chạy mà không chạy nó, rồi hàm in kế hoạch đọc ra bằng câu chọn.
          Trong kế hoạch, chữ đơn là đọc một phân vùng, chữ tất cả là đọc mọi phân vùng, hai cột cuối là phân vùng đầu và cuối. Hai dòng cuối là đọc hết phần được chọn, và gom kết quả đếm.""",
          clear=True, introduces=["bnx_explain"]),
        S(table(["trên màn hình", "nghĩa"],
                [["<code>CHECK (chi_tiet IS JSON)</code>", "chỉ nhận chuỗi có dạng JSON; mặc định chế độ lỏng (nhận cả tên trường không có nháy kép); muốn đúng chuẩn chặt: <code>IS JSON (STRICT)</code>"],
                 ["<code>JSON_VALUE(chi_tiet, '&#36;.kenh')</code>", "lấy một giá trị đơn trong JSON; <code>&#36;</code> là gốc, <code>.kenh</code> là trường kenh"],
                 ["<code>RETURNING NUMBER</code>", "ép giá trị lấy ra thành kiểu số, để so sánh lớn hơn được"]]),
          """Bảng ba giải mã phần JSON. Ràng buộc kiểm tra chỉ nhận chuỗi có dạng «JSON», và mặc định ở chế độ lỏng. Muốn đúng chuẩn chặt thì thêm chữ chặt trong ngoặc.
          Hàm lấy giá trị lấy ra một giá trị đơn, trong đường dẫn thì ký hiệu đô la là gốc, chấm kênh là trường kênh. Mệnh đề trả về kiểu số ép giá trị thành số để so lớn hơn.""",
          clear=True),
        S(table(["câu SQL", "nghĩa"],
                [["<code>SELECT COUNT(*) FROM bảng WHERE điều kiện</code>", "<code>SELECT</code> chọn, <code>FROM</code> chỉ bảng, <code>WHERE</code> lọc dòng; <code>COUNT(*)</code> đếm số dòng thoả điều kiện; <code>AND</code> nối hai điều kiện"],
                 ["<code>INSERT INTO bảng SELECT …</code>", "chèn vào bảng các dòng do câu <code>SELECT</code> sinh ra"],
                 ["<code>ALTER TABLE bảng DROP PARTITION FOR (ngày)</code>", "sửa bảng: bỏ nguyên phân vùng chứa ngày đó, cả dữ liệu trong nó"]]),
          """Trước các câu SQL của bài, ta nhắc lại cách đọc. Câu chọn lấy dữ liệu từ một bảng, chỉ những dòng thoả điều kiện, và hàm đếm cho số dòng. Câu chèn có thể lấy dòng từ một câu chọn. Câu sửa bảng bỏ phân vùng thì bỏ cả dữ liệu trong nó.""",
          clear=True),
    ], checks=["alg.bnx_l07_prune('2025-03-01', '2025-04-01') == (3, 3)"])

    boxes = []
    for i in range(12):
        x = 40 + i * 120
        hot = i == 2
        boxes.append(box(x, 120, 105, 90, [f"T{i + 1}", "310" if hot else ""], C_GREEN if hot else C_GRAY, size=22, bold=hot))
    allb = [box(40 + i * 120, 330, 105, 70, f"T{i + 1}", C_AMBER, size=22) for i in range(12)]
    intu = sc("intuition", "intuition", "Hình dung: đọc một ngăn thay vì cả tủ", [
        S(svg(1500, 470,
              txt(750, 50, "Truy vấn tháng 3: chỉ mở ngăn T3 (310 dòng)", 26, "middle", "#16a34a", True), *boxes,
              arrow(332, 80, 332, 115, "#16a34a"),
              txt(750, 280, "Không lọc theo ngày, không có chỉ mục: mở cả 12 ngăn (3 650 dòng)", 26, "middle", "#d97706", True), *allb),
          """Hình dung bảng phân vùng như một tủ mười hai ngăn, mỗi ngăn là một tháng. Truy vấn tháng ba chỉ cần mở ngăn thứ ba, có ba trăm mười dòng.
          Vì máy biết ngăn nào chứa ngày nào, nó bỏ qua mười một ngăn kia, việc này gọi là cắt tỉa phân vùng. Còn truy vấn không lọc theo ngày, nếu không có chỉ mục riêng, thì máy phải mở cả mười hai ngăn.""",
          introduces=["bnx_cat_tia"]),
    ], checks=["alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-03-01', '2025-04-01') == 310",
               "alg.bnx_l07_partitions(alg.bnx_l07_load(3650)) == 12"])

    form = sc("formula", "formula", "Suy ra từng bước: phân vùng và JSON", [
        S("""<p><b>Bước 1. Chọn khoá phân vùng là ngày</b>, vì sao kê, đối soát, xoá dữ liệu hết hạn đều theo khoảng ngày.</p>""" + code(PART_DDL)
          + """<p class='note'>Làm thử: ngày 15/3/2025 ≥ 1/2/2025 nên không vào phân vùng đầu; nó vào phân vùng tháng 3, vị trí 3. <code>DROP TABLE IF EXISTS</code> xoá bảng cũ nếu có.</p>""",
          """Bước một, chọn khoá phân vùng. Hai dòng đầu xoá bảng cũ nếu có rồi tạo bảng mới có ba cột. Vì sao kê, đối soát và xoá dữ liệu hết hạn đều làm theo khoảng ngày, nên ta chia theo cột ngày, mỗi phân vùng một tháng.
          Ta chỉ khai phân vùng đầu, còn các tháng sau để Oracle tự tạo. Làm thử, ngày mười lăm tháng ba rơi vào phân vùng thứ ba."""),
        S("""<p><b>Bước 2. Nạp một năm dữ liệu.</b> Mẹo sinh nhiều dòng: <code>dual</code> là bảng một dòng có sẵn; <code>CONNECT BY ROWNUM &lt;= 3</code> nhân nó lên 3 dòng, <code>ROWNUM</code> là số thứ tự dòng.</p>"""
          + code(ROWNUM_DEMO) + out(ROWNUM_OUT),
          """Bước hai, nạp dữ liệu, và trước hết một mẹo sinh nhiều dòng. Bảng một dòng có sẵn của Oracle, mệnh đề lặp theo số thứ tự dòng nhỏ hơn hoặc bằng ba, nhân dòng ấy lên ba dòng.
          Số thứ tự dòng đếm từ một, nên ta được một, hai, ba.""", clear=True),
        S("""<p>Nạp 3 650 dòng bằng cùng mẹo: Oracle tự tạo 11 phân vùng cho tháng 2 tới tháng 12.</p>""" + code(PART_LOAD),
          """Giờ nạp ba nghìn sáu trăm năm mươi dòng, mỗi ngày mười dòng. Số thứ tự trừ một rồi chia mười, bỏ phần lẻ, làm cho mười dòng liền nhau có cùng một ngày, còn phần dư làm số tiền thay đổi theo dòng.
          Lệnh chốt, rồi hai câu đếm số dòng và số phân vùng. Vì dữ liệu vượt mốc của phân vùng đầu, Oracle tự tạo thêm phân vùng.""", clear=True),
        S(out(LOAD_OUT) + """<p class='note'>Làm thử: 1 phân vùng khai sẵn + 11 phân vùng tự tạo = 12.</p>""",
          """Làm thử, vì năm có mười hai tháng, một phân vùng khai sẵn cộng mười một tự tạo là mười hai. Đầu ra thật in ba nghìn sáu trăm năm mươi dòng và mười hai phân vùng.""",
          clear=True),
        S("""<p><b>Bước 3. Hỏi máy định đọc mấy phân vùng</b>, không cần chạy thật câu lệnh.</p>""" + code(PLAN_MONTH)
          + """<p class='note'>Làm thử: điều kiện từ 1/3 tới trước 1/4 nằm gọn trong phân vùng 3, nên chờ Pstart = Pstop = 3. Ngày truyền qua <b>biến gắn</b> (giữ chỗ dạng <code>:ngay</code>, giá trị đưa vào lúc chạy): Pstart, Pstop ghi KEY (chọn lúc chạy).</p>""",
          """Bước ba, muốn biết máy định đọc mấy phân vùng mà không phải chạy câu lệnh, ta dùng lệnh xem kế hoạch rồi in ra.
          Điều kiện viết thẳng trên cột ngày, từ mùng một tháng ba tới trước mùng một tháng tư. Làm thử, khoảng này nằm gọn trong phân vùng thứ ba, nên ta chờ phân vùng đầu và cuối đều là ba. Nếu ngày truyền qua biến gắn, tức chỗ giữ dạng hai chấm kèm tên cho giá trị đưa vào lúc chạy, kế hoạch ghi chữ khoá, vì phân vùng chọn lúc chạy.""",
          clear=True),
        S("""<p><b>Bước 4. Phần thay đổi theo kênh lưu dạng JSON</b>, có ràng buộc <code>IS JSON</code> chặn chuỗi hỏng. <code>PRIMARY KEY</code>: khoá chính, mã không được trùng.</p>""" + code(JSON_DDL),
          """Bước bốn, mỗi kênh có thông tin riêng, máy rút tiền có mã máy, ứng dụng có mã thiết bị. Vì không muốn thêm cột mỗi khi có kênh mới, ta lưu phần đó ở dạng «JSON», trong cột chữ dài tối đa bốn trăm ký tự.
          Ràng buộc kiểm tra chỉ nhận chuỗi có dạng «JSON», nên chuỗi hỏng không lọt vào bảng. Khoá chính nghĩa là mã không được trùng.""",
          clear=True),
        S("""<p><b>Bước 5. Thử chèn chuỗi hỏng, rồi lọc theo một trường bên trong.</b></p>""" + C(JSON_QUERY) + out(JSON_OUT),
          """Bước năm, chèn một chuỗi thiếu dấu đóng ngoặc, ràng buộc từ chối ngay. Rồi lọc các dòng có số tiền bên trong lớn hơn một triệu, và lấy ra trường kênh.
          Làm thử, năm trăm nghìn không lớn hơn một triệu, hai triệu thì lớn hơn, nên chỉ còn dòng hai, kênh máy rút tiền, khớp đầu ra thật.""", clear=True),
    ], checks=["alg.bnx_l07_position('2025-03-15') == 3",
               "alg.bnx_l07_partitions(alg.bnx_l07_load(3650)) == 1 + 11",
               "alg.bnx_l07_prune('2025-03-01', '2025-04-01') == (3, 3)",
               "alg.bnx_l07_json_ids({1: '{\"kenh\":\"app\",\"so_tien\":500000}', 2: '{\"kenh\":\"atm\",\"so_tien\":2000000}', 3: '{\"kenh\":\"app\"'}, 'so_tien', 1000000) == ([1, 2], [2])"])

    ex = sc("example", "example", "Ví dụ chạy thật: cắt tỉa phân vùng, từng phép tính", [
        S("""$$① \\; 365 \\cdot 10 = \\hl{3\\,650}\\ \\text{dòng}$$
$$② \\; 1 + 11 = \\hl{12}\\ \\text{phân vùng}$$""",
          """Phép tính thứ nhất, ba trăm sáu mươi lăm ngày nhân mười, bằng ba nghìn sáu trăm năm mươi dòng, khớp số dòng thật ở bước hai.
          Phép tính thứ hai, một phân vùng khai sẵn cộng mười một phân vùng tự tạo, bằng mười hai."""),
        S("""$$③ \\; 31 \\cdot 10 = \\hl{310}\\ \\text{dòng của tháng 3, nằm trong phân vùng 3}$$""" + out(PLAN_MONTH_OUT),
          """Phép tính thứ ba, tháng ba có ba mươi mốt ngày nhân mười, bằng ba trăm mười dòng, tất cả nằm trong phân vùng thứ ba.
          Kế hoạch thật ghi đọc đơn một phân vùng, phân vùng đầu và cuối đều là ba, đúng như ta chờ.""", clear=True),
        S("""$$④ \\; \\frac{310}{3\\,650} \\approx \\hlg{8{,}5\\%}\\ \\text{số dòng phải đọc}$$""",
          """Phép tính thứ tư dùng lại hai số trên. Ba trăm mười chia ba nghìn sáu trăm năm mươi, xấp xỉ tám phẩy năm phần trăm. Nhờ cắt tỉa, máy chỉ đọc chừng ấy số dòng."""),
        S("""<p>Truy vấn không lọc theo ngày (tìm giao dịch trên 5 000 000):</p>""" + code(PLAN_ALL) + out(PLAN_ALL_OUT),
          """Giờ thử một truy vấn không lọc theo ngày, tìm giao dịch trên năm triệu. Kế hoạch thật ghi đọc tất cả, từ phân vùng một.
          Cột cuối là một triệu không trăm bốn mươi tám nghìn năm trăm bảy mươi lăm, đúng bằng số phân vùng tối đa một bảng được có.""",
          clear=True),
        S("""$$⑤ \\; \\frac{3\\,650}{310} \\approx \\hl{11{,}8}\\ \\text{lần nhiều dòng hơn}$$
<p class='note'>$1\\,048\\,575 = 1024 \\cdot 1024 - 1$: giới hạn số phân vùng của một bảng Oracle.</p>""",
          """Phép tính thứ năm, không lọc theo ngày thì phải đọc cả ba nghìn sáu trăm năm mươi dòng. Chia cho ba trăm mười, ta được xấp xỉ mười một phẩy tám lần nhiều dòng hơn.""", clear=True),
    ], checks=["len(alg.bnx_l07_load(3650)) == 365 * 10",
               "alg.bnx_l07_partitions(alg.bnx_l07_load(3650)) == 12",
               "alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-03-01', '2025-04-01') == 310",
               "alg.bnx_l07_prune('2025-03-01', '2025-04-01') == (3, 3)",
               "round(100 * alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-03-01', '2025-04-01') / len(alg.bnx_l07_load(3650)), 1) == 8.5",
               "round(len(alg.bnx_l07_load(3650)) / alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-03-01', '2025-04-01'), 1) == 11.8",
               "alg.bnx_l07_max_partitions() == 1048575"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm thẳng trong phân vùng", [
        S("""<p>Đường khác: đếm theo điều kiện ngày, rồi đếm thẳng trong phân vùng chứa ngày 15/3 (<code>PARTITION FOR</code>: chỉ đọc phân vùng chứa ngày đó, không cần điều kiện nào).</p>""" + code(PART_CHECK) + out(CHECK_OUT),
          """Kiểm bằng đường khác. Câu đầu đếm theo điều kiện ngày như trước. Câu sau không có điều kiện nào, chỉ đếm thẳng mọi dòng trong phân vùng chứa ngày mười lăm tháng ba.
          Cả hai đều ra ba trăm mười, khớp với phép tính thứ ba."""),
        S(table(["điều bài nói", "kiểm thế nào"],
                [["phân vùng, kế hoạch, JSON", "chạy thật trên Oracle bản miễn phí 23, đầu ra dán nguyên"],
                 ["bài tự làm", "chấm tự động trên sqlite vì bộ chấm không có Oracle; bước làm thêm dùng Oracle thật"]]),
          """Phân vùng, kế hoạch và dữ liệu «JSON» đều chạy thật trên Oracle bản miễn phí. Bài tự làm chấm trên cơ sở dữ liệu nhỏ, nên bước làm thêm mới dùng Oracle thật.""",
          clear=True),
    ], checks=["alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-03-01', '2025-04-01') == alg.bnx_l07_month_days(2025, 3) * 10"])

    quymo = sc("quymo", "example", "Khi bảng lớn dần: số dòng máy phải đọc", [
        S(code(ORA_SCALE, "Nạp lại bảng gấp 100 lần: 1 000 dòng mỗi ngày, rồi đếm cả bảng và riêng phân vùng tháng 3"),
          """Bây giờ xem vấn đề đổi thế nào khi dữ liệu lớn dần. Ta nạp lại bảng, lần này một nghìn dòng mỗi ngày, gấp một trăm lần ví dụ, tức ba trăm sáu mươi lăm nghìn dòng cả năm.
          Hai câu cuối đếm cả bảng và riêng phân vùng tháng ba.""",
          clear=True),
        S(out(ORA_SCALE_OUT, "Kết quả chạy thật trên Oracle")
          + table(["số dòng cả năm", "máy đọc nếu cắt tỉa (một tháng)", "máy đọc nếu không cắt tỉa", "tỉ lệ (nếu phân bố đều)"],
                  [["3 650 (ví dụ)", "310", "3 650", "31 / 365"], ["365 000 (gấp 100, đo)", "31 000", "365 000", "31 / 365"],
                   ["36 500 000 (gấp 10 000, tính)", "3 100 000", "36 500 000", "31 / 365"]]),
          """Cả bảng có ba trăm sáu mươi lăm nghìn dòng, còn phân vùng tháng ba chỉ ba mươi mốt nghìn. Dữ liệu phân bố đều như mẫu này thì tỉ lệ vẫn là ba mươi mốt trên ba trăm sáu mươi lăm ở mọi quy mô. Dữ liệu thật lệch theo mùa thì tỉ lệ khác.
          Ở ba mươi sáu triệu rưỡi dòng, theo cùng tỉ lệ, là ba triệu một trăm nghìn dòng thay vì cả bảng.""",
          clear=True),
        S(table(["cách", "được", "mất", "khi nào chọn"],
                [["phân vùng theo tháng", "đọc một tháng thay vì cả bảng; xoá dữ liệu cũ bằng cách bỏ nguyên phân vùng",
                  "truy vấn không lọc theo cột phân vùng vẫn đọc mọi phân vùng; thêm việc quản lý phân vùng", "bảng lớn, truy vấn thường lọc theo ngày"],
                 ["không phân vùng, chỉ thêm chỉ mục", "đơn giản, ít việc quản lý", "chỉ mục phình theo bảng; xoá dữ liệu cũ là xoá từng dòng", "bảng vừa"]]),
          """Bảng này cho thấy người làm nghề phải chọn gì. Phân vùng giúp đọc một tháng thay vì cả bảng, và xoá dữ liệu cũ bằng cách bỏ nguyên phân vùng.
          Đổi lại, truy vấn không lọc theo cột phân vùng vẫn đọc mọi phân vùng. Với bảng vừa, chỉ mục thường đã đủ.""",
          focus=[0, "1.2", "1.3", "1.3"], clear=True),
    ], checks=["len(alg.bnx_l07_load(365000, per_day=1000)) == 365000 and alg.bnx_l07_count(alg.bnx_l07_load(365000, per_day=1000), '2025-03-01', '2025-04-01') == 31000",
               "[alg.bnx_l07_month_rows(p, 3) for p in (10, 1000, 100000)] == [310, 31000, 3100000]",
               "[p * 365 for p in (10, 1000, 100000)] == [3650, 365000, 36500000]"])

    write_lab("BNX", "L07", LAB_DE, "py", LAB_PY, LAB_OUT)
    lab_pr = practice_scene(sc, "Tự làm: JSON có ràng buộc (sqlite) và Oracle Free tự dựng", lib2.practice_steps2(
        st, "BNX", "L07",
        """<p><b>Đề</b>: sqlite có bảng <code>gd (id, chi_tiet)</code> với <code>CHECK (json_valid(chi_tiet))</code>. Viết <code>mau.py</code>:</p>
<ol><li>chèn năm dòng cho sẵn; dòng nào JSON hỏng thì in <code>dong N: tu choi (JSON hong)</code></li><li>in tổng <code>tien</code> kênh <code>atm</code>, số giao dịch kênh <code>app</code>, số giao dịch máy <code>A7</code> (lấy trường bằng <code>json_extract</code> hoặc cách viết ngắn <code>-&gt;&gt;</code>, như <code>chi_tiet -&gt;&gt; '&#36;.tien'</code>)</li></ol>
<p class="note">Oracle không có trong bộ chấm: sqlite đại diện, <code>CHECK (json_valid)</code> ứng với <code>IS JSON</code>. Năm dòng dữ liệu nằm trong <code>de.md</code>.</p>""",
        """Bây giờ tới phần bạn tự làm, trên cơ sở dữ liệu nhỏ có sẵn trong Python vì bộ chấm không có Oracle. Chèn năm dòng cho sẵn, in dòng bị từ chối, rồi tính tổng và đếm giao dịch. Mũi tên kép là cách viết ngắn của hàm lấy trường. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> bắt <code>sqlite3.IntegrityError</code> quanh mỗi lệnh chèn. Lấy trường bằng <code>json_extract(chi_tiet, '$.tien')</code>, lọc kênh bằng <code>json_extract(chi_tiet, '$.kenh') = 'atm'</code>.
Lời giải ở <code>labs/BNX/L07/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""".replace("$", "&#36;"),
        """Nếu kẹt, bắt lỗi ràng buộc quanh mỗi lệnh chèn, rồi lấy trường trong JSON bằng hàm trích theo đường dẫn và lọc theo kênh. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã tự thử.""", pause=120), "BNX", "L07")
    lab_pr["steps"].append(st(table(["lệnh", "nghĩa"],
                                    [["<code>docker run -d --name ora-thu -p 1521:1521 -e … gvenzl/oracle-free:23-slim</code>", "chạy một “thùng” phần mềm ở nền (<code>-d</code>), đặt tên <code>ora-thu</code>, mở cổng 1521 ra máy (<code>-p</code>), đặt biến cấu hình như mật khẩu (<code>-e</code>); dòng cuối là tên ảnh phần mềm"],
                                     ["<code>docker logs -f ora-thu</code>", "xem nhật ký của thùng; đợi dòng <code>DATABASE IS READY TO USE!</code> rồi mới vào"],
                                     ["<code>docker exec -it ora-thu sqlplus bnx/bnx_pass@//localhost/FREEPDB1</code>", "chạy <code>sqlplus</code>, dòng lệnh SQL của Oracle, bên trong thùng, với tài khoản <code>bnx</code>"]]),
                              """Muốn làm trên Oracle thật, bạn dựng bản miễn phí bằng Docker, công cụ chạy phần mềm trong một thùng đóng gói sẵn. Lệnh đầu chạy thùng ở nền và mở cổng, lệnh thứ hai xem nhật ký để đợi sẵn sàng, và lệnh cuối mở dòng lệnh SQL trong thùng.""",
                              clear=True))
    lab_pr["steps"].append(st("""<p><b>Làm thêm trên Oracle thật</b> (không chấm tự động): dựng Oracle Free 23 bằng Docker rồi vào dòng lệnh <code>sqlplus</code>.</p>"""
                              + code(DOCKER_RUN)
                              + """<p class="note">Dán lại khối tạo bảng và nạp ở bước 1–2, chạy kế hoạch ở bước 3: phải thấy <code>PARTITION RANGE SINGLE</code>, Pstart = Pstop = 3.</p>""",
                              """Sau khi vào được, dán lại khối tạo bảng và nạp, rồi chạy kế hoạch tháng ba: máy phải chỉ đọc đơn phân vùng ba.""",
                              clear=True))

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        S("""<div class="box warn"><b>Lỗi 1 (người đã đi làm): bọc cột phân vùng trong hàm.</b> Cùng ý “tháng 3”, viết bằng <code>TRUNC</code>:</div>""" + code(PLAN_TRUNC) + out(PLAN_TRUNC_OUT),
          """Lỗi thứ nhất, của người đã đi làm, là bọc cột phân vùng trong một hàm. Câu này cũng hỏi tháng ba, nhưng cắt ngày về đầu tháng rồi mới so.
          Kế hoạch thật ghi đọc tất cả phân vùng, vì máy không cắt tỉa được khi cột bị biến đổi. Cách chữa là viết điều kiện khoảng trên cột gốc."""),
        S(table(["cách viết trong SQL", "nghĩa"],
                [["<code>CASE WHEN điều kiện THEN a ELSE b END</code>", "nếu điều kiện đúng thì cho <code>a</code>, không thì cho <code>b</code>"],
                 ["<code>'{kenh:''app''}'</code>", "trong chuỗi, hai dấu nháy đơn liền nhau <code>''</code> là một dấu nháy đơn; chuỗi này là <code>{kenh:'app'}</code>"]]),
          """Câu sắp tới có hai cách viết mới, nên ta giải nghĩa trước. Cách viết chọn một trong hai giá trị tuỳ điều kiện. Hai dấu nháy đơn liền nhau trong một chuỗi là một dấu nháy đơn.""", clear=True),
        S("""<div class="box warn"><b>Lỗi 2: tưởng <code>IS JSON</code> là JSON chuẩn.</b> Chuỗi <code>{kenh:'app'}</code> (tên trường không nháy kép, nháy đơn quanh giá trị):</div>""" + code(JSON_LAX) + out(JSON_LAX_OUT),
          """Lỗi thứ hai là tưởng ràng buộc JSON luôn đúng chuẩn. Chuỗi này có tên trường không nháy kép và nháy đơn quanh giá trị, không phải JSON chuẩn.
          Chế độ lỏng mặc định vẫn nhận nó, còn chế độ chặt từ chối, nên cần chế độ chặt.""", clear=True),
        S("""<div class="box warn"><b>Lỗi 3 (người đã đi làm): bỏ nhầm phân vùng.</b> Bỏ phân vùng tháng 1, rồi thử hoàn tác:</div>""" + code(DROP_PART) + out(DROP_PART_OUT),
          """Lỗi thứ ba, của người đã đi làm, là bỏ nhầm phân vùng. Lệnh bỏ phân vùng tự chốt ngay, nên lệnh hoàn tác sau đó không cứu được gì.
          Bảng còn ba nghìn ba trăm bốn mươi dòng, tức mất đúng ba trăm mười dòng của tháng một. Vì thế phải kiểm kỹ ngày trước khi bỏ.""", clear=True),
    ], checks=["alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-01-01', '2025-02-01') == 310",
               "len(alg.bnx_l07_load(3650)) - alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-01-01', '2025-02-01') == 3340"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        S(table(["câu", "đề"],
                [["1", "Cùng bảng của bài. Truy vấn <code>ngay &gt;= DATE '2025-03-15' AND ngay &lt; DATE '2025-05-15'</code>: đọc những phân vùng nào, đếm được bao nhiêu dòng?"],
                 ["2", "Truy vấn <code>ngay &gt;= DATE '2025-02-10' AND ngay &lt; DATE '2025-02-20'</code>: kế hoạch ghi <code>PARTITION RANGE</code> gì, Pstart và Pstop bằng mấy, đếm bao nhiêu dòng?"],
                 ["3", "Quyết định: lưu thông tin riêng của từng kênh bằng cột JSON hay thêm một cột cho mỗi thông tin?"]]),
          """Đến lượt bạn, ba câu trên màn hình. Câu ba chọn cột JSON hay thêm cột. Hãy dừng video và làm ra giấy.""",
          pause=25),
        S("""<p>Câu 1: khoảng chạm tháng 3, 4, 5 → phân vùng 3 tới 5 (kế hoạch thật: <code>PARTITION RANGE ITERATOR</code> = đọc lần lượt một dãy phân vùng liền nhau, Pstart 3, Pstop 5).</p>
$$17 + 30 + 14 = 61\\ \\text{ngày}, \\qquad 61 \\cdot 10 = \\hl{610}\\ \\text{dòng}$$""",
          """Đáp án câu một. Khoảng này chạm tháng ba, tháng tư và tháng năm, nên máy đọc dãy phân vùng liền nhau, từ ba tới năm.
          Mười bảy ngày cuối tháng ba, cộng ba mươi ngày tháng tư, cộng mười bốn ngày đầu tháng năm, là sáu mươi mốt ngày, nhân mười được sáu trăm mười dòng."""),
        S("""<p>Câu 2: cả khoảng nằm trong tháng 2, phân vùng 2: <code>PARTITION RANGE SINGLE</code>, Pstart = Pstop = 2.</p>
$$10 \\cdot 10 = \\hl{100}\\ \\text{dòng}$$""",
          """Đáp án câu hai. Cả khoảng nằm trong tháng hai, nên kế hoạch ghi đọc đơn một phân vùng, hai cột cuối đều là hai. Mười ngày nhân mười dòng là một trăm."""),
        S(table(["lựa chọn", "được", "mất"],
                [["cột JSON", "kênh mới không phải đổi bảng; <code>IS JSON</code> chặn chuỗi hỏng", "kiểm kiểu từng trường yếu hơn; lọc theo trường nếu chưa có chỉ mục riêng thì phải đọc từng dòng"],
                 ["một cột cho mỗi thông tin", "kiểu và ràng buộc từng cột, chỉ mục thường", "kênh mới là phải đổi bảng; nhiều cột trống"]]),
          """Đáp án câu ba, tuỳ nhu cầu. Cột JSON thêm kênh mới không phải đổi bảng, đổi lại kiểm kiểu từng trường yếu hơn, và lọc theo trường chưa có chỉ mục riêng thì phải đọc từng dòng.
          Một cột cho mỗi thông tin thì kiểu chặt, nhưng thêm kênh mới là phải đổi bảng. Thông tin ổn định, hay lọc thì nên là cột."""),
    ], checks=["alg.bnx_l07_prune('2025-03-15', '2025-05-15') == (3, 5)",
               "alg.bnx_l07_days('2025-03-15', '2025-05-15') == 17 + 30 + 14 == 61",
               "alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-03-15', '2025-05-15') == 610",
               "alg.bnx_l07_prune('2025-02-10', '2025-02-20') == (2, 2)",
               "alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-02-10', '2025-02-20') == 100"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        S(chain("lọc theo ngày", "phân vùng theo tháng", "kế hoạch ghi một phân vùng", "phần riêng từng kênh: JSON có ràng buộc"),
          """Tổng kết chuỗi logic. Truy vấn ngân hàng thường lọc theo ngày, nên ta phân vùng theo tháng, và đọc kế hoạch để chắc máy chỉ mở một phân vùng.
          Phần riêng của từng kênh lưu dạng «JSON», có ràng buộc để chặn chuỗi hỏng."""),
        S("""<div class='box key'><b>Tư duy:</b> đừng đoán máy đọc gì, hãy hỏi kế hoạch thực thi. Một tính năng mới chỉ đáng dùng khi bạn chỉ ra được con số nó cải thiện.</div>""",
          """Điều cần mang theo. Đừng đoán máy đọc gì, hãy hỏi kế hoạch thực thi. Tính năng mới chỉ đáng dùng khi bạn chỉ ra được con số nó cải thiện."""),
        S("""<p class="note">Bài sau: tìm kiếm toàn văn phân tán, chia dữ liệu thành nhiều mảnh có bản sao, và vì sao dữ liệu vừa ghi chưa tìm thấy ngay.</p>""",
          """Ở bài sau, ta gặp lại ý chia dữ liệu thành nhiều mảnh, lần này trong một hệ tìm kiếm toàn văn, có bản sao.""",
          forward_ref=True),
    ])
    return lesson("L07", "oracle_phan_vung_json_hang_doi",
                  "Bài 7 — Oracle cho khối lượng lớn: phân vùng và JSON",
                  "curriculum/bnx.yaml L07; audit/bnx/verify_bnx.py L07; Oracle Database 23 (docs.oracle.com, trang đọc 2026-11-11): VLDB and Partitioning Guide "
                  "(interval partitioning, partition pruning), Reference (Logical Database Limits), JSON Developer's Guide (IS JSON, JSON_VALUE); "
                  "Oracle AI Database 26ai Free 23.26.3 chạy thật trong Docker (hàng đợi, bộ nhớ cột, phân mảnh: xem bài L38)",
                  ["Phân vùng bảng giao dịch theo tháng và đọc kế hoạch cắt tỉa phân vùng", "Lưu và truy vấn dữ liệu JSON trong Oracle",
                   "So số dòng phải đọc khi cắt tỉa phân vùng với khi đọc cả bảng, ở 3 650, 365 000 và 36 500 000 dòng",
                   "Lưu dữ liệu JSON có ràng buộc kiểm hợp lệ và truy vấn theo trường trong JSON (lab sqlite)"],
                  _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec]),
                  covers=[(1, "example"), (2, "formula"), (3, "quymo"), (4, "practice")])
