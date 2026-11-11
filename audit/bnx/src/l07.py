from lib import *

# ── Mã hiện trên màn hình (chạy NGUYÊN VĂN: audit/bnx/screen/l07.yaml, audit/bnx/ver/l07.py) ──
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

AQ_CLEAN = """
BEGIN
  DBMS_AQADM.STOP_QUEUE('bnx_l07_q');
  DBMS_AQADM.DROP_QUEUE('bnx_l07_q');
  DBMS_AQADM.DROP_QUEUE_TABLE('bnx_l07_qt');
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
DROP TYPE IF EXISTS bnx_l07_msg FORCE;
"""

AQ_SETUP = """
CREATE TYPE bnx_l07_msg AS OBJECT (ma_gd NUMBER, so_tien NUMBER);
/
BEGIN
  DBMS_AQADM.CREATE_QUEUE_TABLE('bnx_l07_qt', 'bnx_l07_msg');
  DBMS_AQADM.CREATE_QUEUE('bnx_l07_q', 'bnx_l07_qt');
  DBMS_AQADM.START_QUEUE('bnx_l07_q');
END;
/
"""

AQ_ENQ = """
DECLARE
  eo  DBMS_AQ.ENQUEUE_OPTIONS_T;
  mp  DBMS_AQ.MESSAGE_PROPERTIES_T;
  id  RAW(16);
BEGIN
  DBMS_AQ.ENQUEUE('bnx_l07_q', eo, mp, bnx_l07_msg(101, 500000), id);
  ROLLBACK;
  DBMS_AQ.ENQUEUE('bnx_l07_q', eo, mp, bnx_l07_msg(102, 200000), id);
  COMMIT;
END;
/
SELECT COUNT(*) AS so_thong_diep FROM bnx_l07_qt;
"""

AQ_DEQ = """
DECLARE
  dq  DBMS_AQ.DEQUEUE_OPTIONS_T;
  mp  DBMS_AQ.MESSAGE_PROPERTIES_T;
  m   bnx_l07_msg;
  id  RAW(16);
BEGIN
  dq.wait := DBMS_AQ.NO_WAIT;
  DBMS_AQ.DEQUEUE('bnx_l07_q', dq, mp, m, id);
  DBMS_OUTPUT.PUT_LINE('nhan: ' || m.ma_gd || ' ' || m.so_tien);
  COMMIT;
END;
/
"""

IM_CHECK = """
SELECT value AS inmemory_size FROM v$parameter
 WHERE name = 'inmemory_size';
ALTER TABLE bnx_l07_gd INMEMORY;
SELECT def_inmemory FROM user_part_tables
 WHERE table_name = 'BNX_L07_GD';
"""

# ── Đầu ra THẬT (chạy 2026-11-11 trên bnx-ora, Oracle AI Database 26ai Free 23.26.3; sqlplus căn cột bằng tab) — lược bằng "…" ──
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
AQ_ENQ_OUT = """
SO_THONG_DIEP
-------------
\t    1
"""
AQ_DEQ_OUT = """
nhan: 102 200000
"""
IM_OUT = """
INMEMORY_SIZE
--------------------…
0
DEF_INME
--------
ENABLED
"""

# BRIEF mục 6 (2026-11-11): JSON đã dò 8/8, được đọc trong lời.
SAY_WORDS = {"«JSON»": "JSON"}


def S(show, say, **kw):
    for a_, b_ in SAY_WORDS.items():
        say = say.replace(a_, b_)
    return st(show, say, **kw)


LOAD = "alg.bnx_l07_load(3650)"


def C(text, title=None, lines=None):
    """Khối mã có ký tự đô la (đường dẫn JSON, v$parameter): viết thành thực thể &#36; để lint/KaTeX không ghép hai dấu đô la thành công thức;
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
                 ["báo cho hệ khác sau khi ghi", "hàng đợi trong cơ sở dữ liệu, chung giao dịch với dữ liệu"],
                 ["khi nào cần hơn nữa", "bộ nhớ cột cho báo cáo, phân mảnh khi một máy không đủ"]]),
          """Hôm nay ta trả lời bốn câu hỏi. Làm sao chỉ đọc đúng tháng cần, bằng cách phân vùng bảng theo tháng và đọc kế hoạch thực thi.
          Dữ liệu mỗi kênh một kiểu thì lưu ra sao, bằng dữ liệu dạng «JSON» ngay trong Oracle. Báo cho hệ khác sau khi ghi thế nào, bằng hàng đợi nằm trong cơ sở dữ liệu.
          Và khi nào cần bộ nhớ cột hay phân mảnh."""),
    ], checks=["alg.bnx_l07_partitions(alg.bnx_l07_load(3650)) == 12"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        S(table(["khái niệm", "nghĩa", "ví dụ"],
                [["① Quét toàn bảng và chỉ mục", "không có đường tắt thì đọc từng dòng; chỉ mục cây B đi thẳng tới dòng cần", "tìm một mã giao dịch: chỉ mục; đếm cả tháng: thường phải quét"],
                 ["② Kế hoạch thực thi", "bản kế hoạch máy chọn để chạy câu lệnh: đọc bảng nào, theo cách nào", "đọc toàn bảng giao dịch"],
                 ["③ Giao dịch", "chốt thì mọi thay đổi cùng ở lại, hoàn tác thì cùng mất", "thủ tục chuyển tiền ở bài 6"],
                 ["④ Kafka", "nơi lưu thông điệp theo chủ đề; người đọc tự giữ vị trí đọc, có thể đọc lại; “phân vùng” của Kafka là phần của chủ đề, khác phân vùng bảng", "dịch vụ thông báo đọc chủ đề giao dịch"]]),
          """Trước hết ta cần hiểu bốn điều. Khi không có đường tắt, máy đọc từng dòng, gọi là quét toàn bảng. Chỉ mục cây B thì đi thẳng tới dòng cần mà không phải đọc hết các dòng.
          Kế hoạch thực thi là bản kế hoạch máy chọn để chạy một câu lệnh, đọc bảng nào và đọc theo cách nào.
          Giao dịch thì chốt là mọi thay đổi cùng ở lại, hoàn tác là cùng mất, đúng như thủ tục chuyển tiền ở bài sáu.
          Còn Kafka lưu thông điệp theo chủ đề, người đọc tự giữ vị trí đọc nên có thể đọc lại. Kafka cũng gọi các phần của chủ đề là phân vùng, nhưng đó khác với phân vùng bảng trong bài này."""),
        S("""<p>Dữ liệu mẫu của bài: năm 2025, mỗi ngày 10 giao dịch.</p>
$$365 \\cdot 10 = \\hl{3\\,650}\\ \\text{dòng}, \\qquad 31 \\cdot 10 = \\hl{310}\\ \\text{dòng của tháng 3}$$""",
          """Một ví dụ số làm dữ liệu mẫu cho cả bài. Năm hai nghìn không trăm hai mươi lăm có ba trăm sáu mươi lăm ngày, mỗi ngày mười giao dịch, nên có ba nghìn sáu trăm năm mươi dòng.
          Dấu chấm ở giữa là phép nhân. Tháng ba có ba mươi mốt ngày, nên có ba trăm mười dòng.""", clear=True),
    ], checks=["alg.bnx_l07_days('2025-01-01', '2026-01-01') * 10 == len(alg.bnx_l07_load(3650))",
               "alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-03-01', '2025-04-01') == alg.bnx_l07_month_days(2025, 3) * 10 == 310"])

    sym = sc("sym", "symbol", "Giải mã từ khoá", [
        S(table(["trên màn hình", "nghĩa"],
                [["<code>PARTITION BY RANGE (ngay)</code>", "chia bảng thành phân vùng theo khoảng giá trị của cột ngày (khoá phân vùng)"],
                 ["<code>INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))</code>", "mỗi phân vùng dài 1 tháng; có dữ liệu vượt mốc thì Oracle tự tạo phân vùng mới"],
                 ["<code>EXPLAIN PLAN FOR</code> … <code>DBMS_XPLAN.DISPLAY</code>", "ghi kế hoạch thực thi mà không chạy câu lệnh, rồi in ra"],
                 ["<code>PARTITION RANGE SINGLE</code> / <code>ALL</code>", "chỉ đọc một phân vùng / đọc mọi phân vùng"],
                 ["<code>Pstart</code>, <code>Pstop</code>", "phân vùng đầu và cuối sẽ đọc (đánh số từ 1)"]]),
          """Bảng này giải mã từ khoá về phân vùng. Dòng đầu chia bảng thành các phân vùng theo khoảng giá trị của cột ngày, cột đó gọi là khoá phân vùng.
          Dòng thứ hai nói mỗi phân vùng dài một tháng, có dữ liệu vượt mốc cuối thì Oracle tự tạo phân vùng mới.
          Lệnh xem kế hoạch ghi lại cách máy sẽ chạy câu lệnh mà không chạy nó, rồi một hàm in kế hoạch ra.
          Trong kế hoạch, chữ đơn nghĩa là chỉ đọc một phân vùng, chữ tất cả nghĩa là đọc mọi phân vùng. Hai cột cuối cho biết phân vùng đầu và cuối sẽ đọc."""),
        S(table(["trên màn hình", "nghĩa"],
                [["<code>CHECK (chi_tiet IS JSON)</code>", "chỉ nhận chuỗi có dạng JSON; mặc định chế độ lỏng (nhận cả tên trường không có nháy kép); muốn đúng chuẩn chặt: <code>IS JSON (STRICT)</code>"],
                 ["<code>JSON_VALUE(chi_tiet, '&#36;.kenh')</code>", "lấy một giá trị đơn trong JSON; <code>&#36;</code> là gốc, <code>.kenh</code> là trường kenh"],
                 ["<code>DBMS_AQ.ENQUEUE</code> / <code>DEQUEUE</code>", "gói DBMS_AQ (nhóm thủ tục có sẵn, gọi bằng tên gói chấm tên thủ tục): gửi vào / nhận ra khỏi hàng đợi"],
                 ["<code>INMEMORY</code>", "đánh dấu bảng được nạp thêm một bản dạng cột vào bộ nhớ"]]),
          """Bảng thứ hai giải mã các từ khoá còn lại. Ràng buộc kiểm tra chỉ nhận chuỗi có dạng «JSON», và mặc định ở chế độ lỏng. Muốn đúng chuẩn chặt thì thêm chữ chặt trong ngoặc, như trên màn hình.
          Hàm lấy giá trị lấy ra một giá trị đơn, trong đường dẫn thì ký hiệu đô la là gốc, chấm kênh là trường kênh.
          Gói là một nhóm thủ tục có sẵn, gọi bằng tên gói, dấu chấm, rồi tên thủ tục. Hai thủ tục của gói hàng đợi dùng để gửi thông điệp vào và nhận thông điệp ra. Từ khoá cuối đánh dấu bảng được nạp thêm một bản dạng cột vào bộ nhớ.""",
          clear=True),
    ], checks=["alg.bnx_l07_prune('2025-03-01', '2025-04-01') == (3, 3)"])

    boxes = []
    for i in range(12):
        x = 40 + i * 120
        hot = i == 2
        boxes.append(box(x, 120, 105, 90, [f"T{i + 1}", "310" if hot else ""], C_GREEN if hot else C_GRAY, size=22, bold=hot))
    allb = [box(40 + i * 120, 330, 105, 70, f"T{i + 1}", C_AMBER, size=22) for i in range(12)]
    intu = sc("intuition", "intuition", "Hình dung: đọc một ngăn thay vì cả tủ, và gửi thư trong cùng giao dịch", [
        S(svg(1500, 470,
              txt(750, 50, "Truy vấn tháng 3: chỉ mở ngăn T3 (310 dòng)", 26, "middle", "#16a34a", True), *boxes,
              arrow(332, 80, 332, 115, "#16a34a"),
              txt(750, 280, "Không lọc theo ngày, không có chỉ mục: mở cả 12 ngăn (3 650 dòng)", 26, "middle", "#d97706", True), *allb),
          """Hình dung bảng phân vùng như một tủ mười hai ngăn, mỗi ngăn là một tháng. Truy vấn tháng ba chỉ cần mở ngăn thứ ba, có ba trăm mười dòng.
          Vì máy biết ngăn nào chứa ngày nào, nó bỏ qua mười một ngăn kia, việc này gọi là cắt tỉa phân vùng.
          Còn truy vấn không lọc theo ngày thì không biết ngăn nào chứa kết quả. Nếu không có chỉ mục riêng trên cột lọc, máy phải mở cả mười hai ngăn, ba nghìn sáu trăm năm mươi dòng."""),
        S(svg(1500, 470,
              panel(30, 20, 820, 430, "Hàng đợi trong cơ sở dữ liệu: một giao dịch", C_GREEN, size=24),
              box(70, 110, 360, 90, ["ghi giao dịch", "vào bảng"], C_BLUE, size=22),
              box(460, 110, 360, 90, ["gửi thông điệp", "vào hàng đợi"], C_PURPLE, size=22),
              box(70, 260, 360, 80, "chốt: cả hai ở lại", C_GREEN, size=22),
              box(460, 260, 360, 80, "hoàn tác: cả hai mất", C_RED, size=22),
              arrow(250, 205, 250, 255), arrow(640, 205, 640, 255),
              txt(440, 400, "mặc định: không có thông điệp “ma” cho giao dịch đã huỷ", 22, "middle", "#16a34a", True),
              panel(900, 20, 570, 430, "Kafka: hệ riêng bên ngoài", C_AMBER, size=24),
              box(940, 110, 490, 90, ["ghi cơ sở dữ liệu và gửi Kafka", "là hai việc riêng"], C_AMBER, size=22),
              box(940, 260, 490, 80, "cần thêm cách giữ nhất quán", C_GRAY, size=22),
              arrow(1185, 205, 1185, 255),
              txt(1185, 400, "bù lại: lưu lâu, đọc lại được", 22, "middle", "#d97706", True)),
          """Hình thứ hai so hai cách báo cho hệ khác. Với hàng đợi trong cơ sở dữ liệu, ghi giao dịch và gửi thông điệp nằm trong cùng một giao dịch.
          Ở chế độ mặc định, chốt thì cả hai ở lại, hoàn tác thì cả hai mất, nên không có thông điệp cho một giao dịch đã bị huỷ.
          Với Kafka, ghi cơ sở dữ liệu và gửi thông điệp là hai việc riêng, nên cần thêm một cách giữ nhất quán. Bù lại, Kafka lưu lâu và cho đọc lại."""),
    ], checks=["alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-03-01', '2025-04-01') == 310",
               "alg.bnx_l07_partitions(alg.bnx_l07_load(3650)) == 12",
               "alg.bnx_l07_queue([('enq', 101), ('rollback',), ('enq', 102), ('commit',)]) == ([], 2 - 1)"])

    form = sc("formula", "formula", "Suy ra từng bước: phân vùng, JSON, hàng đợi, bộ nhớ cột, phân mảnh", [
        S("""<p><b>Bước 1. Chọn khoá phân vùng là ngày</b>, vì sao kê, đối soát, xoá dữ liệu hết hạn đều theo khoảng ngày.</p>""" + code(PART_DDL)
          + """<p class='note'>Làm thử: ngày 15/3/2025 ≥ 1/2/2025 nên không vào phân vùng đầu; nó vào phân vùng tháng 3, vị trí 3. Xoá cả tháng: <code>ALTER TABLE … DROP PARTITION FOR (…)</code>.</p>""",
          """Bước một, chọn khoá phân vùng. Vì sao kê, đối soát và xoá dữ liệu hết hạn đều làm theo khoảng ngày, nên ta chia theo cột ngày, mỗi phân vùng một tháng.
          Ta chỉ khai phân vùng đầu, chứa các ngày trước mùng một tháng hai, còn các tháng sau để Oracle tự tạo. Hết hạn lưu thì bỏ cả phân vùng của tháng đó bằng một lệnh, thay vì xoá từng dòng.
          Làm thử, ngày mười lăm tháng ba không nhỏ hơn mùng một tháng hai, nên nó rơi vào phân vùng tháng ba, ở vị trí thứ ba."""),
        S("""<p><b>Bước 2. Nạp một năm dữ liệu</b>: Oracle tự tạo 11 phân vùng cho tháng 2 tới tháng 12.</p>""" + code(PART_LOAD),
          """Bước hai, nạp ba nghìn sáu trăm năm mươi dòng, mỗi ngày mười dòng, số tiền thay đổi theo từng dòng. Vì dữ liệu vượt mốc của phân vùng đầu, Oracle tự tạo thêm phân vùng.
          Câu chọn dữ liệu sinh ra ba nghìn sáu trăm năm mươi dòng đánh số từ một. Vì số thứ tự trừ một rồi chia mười, bỏ phần lẻ, nên cứ mười dòng liền nhau có cùng một ngày.
          Hai câu cuối đếm số dòng và số phân vùng.""", clear=True),
        S(out(LOAD_OUT) + """<p class='note'>Làm thử: 1 phân vùng khai sẵn + 11 phân vùng tự tạo = 12.</p>""",
          """Làm thử, vì năm có mười hai tháng, một phân vùng khai sẵn cộng mười một phân vùng tự tạo là mười hai. Đầu ra thật in ba nghìn sáu trăm năm mươi dòng và mười hai phân vùng, khớp với phép tính.""",
          clear=True),
        S("""<p><b>Bước 3. Hỏi máy định đọc mấy phân vùng</b>, không cần chạy thật câu lệnh.</p>""" + code(PLAN_MONTH)
          + """<p class='note'>Làm thử: điều kiện từ 1/3 tới trước 1/4 nằm gọn trong phân vùng 3, nên chờ Pstart = Pstop = 3. Ngày truyền qua biến gắn: Pstart, Pstop ghi KEY (chọn lúc chạy).</p>""",
          """Bước ba, muốn biết máy định đọc mấy phân vùng mà không phải chạy câu lệnh, ta dùng lệnh xem kế hoạch rồi in kế hoạch ra.
          Điều kiện viết thẳng trên cột ngày, từ mùng một tháng ba tới trước mùng một tháng tư. Làm thử, khoảng này nằm gọn trong phân vùng thứ ba, nên ta chờ phân vùng đầu và cuối đều là ba.
          Nếu ngày được truyền qua biến gắn, tức chỗ giữ chỗ có giá trị truyền riêng, thì kế hoạch không ghi số phân vùng, vì phân vùng chỉ được chọn lúc chạy.""",
          clear=True),
        S("""<p><b>Bước 4. Phần thay đổi theo kênh lưu dạng JSON</b>, có ràng buộc <code>IS JSON</code> chặn chuỗi hỏng.</p>""" + code(JSON_DDL),
          """Bước bốn, mỗi kênh có thông tin riêng, máy rút tiền có mã máy, ứng dụng có mã thiết bị. Vì không muốn thêm cột mỗi khi có kênh mới, ta lưu phần đó ở dạng «JSON».
          Ràng buộc kiểm tra chỉ nhận chuỗi có dạng «JSON», mặc định ở chế độ lỏng, nên chuỗi hỏng không lọt vào bảng. Từ bản hai mươi mốt, Oracle khuyên dùng kiểu cột «JSON» riêng; cột chữ kèm ràng buộc thì chạy được cả trên bản cũ. Hai dòng mẫu là năm trăm nghìn qua ứng dụng và hai triệu qua máy rút tiền.""",
          clear=True),
        S("""<p><b>Bước 5. Thử chèn chuỗi hỏng, rồi lọc theo một trường bên trong.</b></p>""" + C(JSON_QUERY) + out(JSON_OUT),
          """Bước năm, chèn một chuỗi thiếu dấu đóng ngoặc, ràng buộc từ chối ngay. Rồi ta lọc các dòng có số tiền bên trong lớn hơn một triệu, và lấy ra trường kênh.
          Làm thử, năm trăm nghìn không lớn hơn một triệu, hai triệu thì lớn hơn, nên chỉ còn dòng hai, kênh máy rút tiền, khớp đầu ra thật.""", clear=True),
        S("""<p><b>Bước 6. Tạo hàng đợi trong cơ sở dữ liệu</b>: kiểu thông điệp, bảng hàng đợi, hàng đợi, rồi bật nó.</p>""" + code(AQ_SETUP),
          """Bước sáu, tạo hàng đợi ngay trong cơ sở dữ liệu. Vì hàng đợi phải biết mỗi thông điệp chứa gì, nên trước hết khai kiểu thông điệp gồm mã giao dịch và số tiền.
          Rồi tạo bảng hàng đợi để chứa thông điệp, tạo hàng đợi trên bảng đó, và bật hàng đợi để gửi nhận được.
          Đây là hàng đợi kiểu cổ điển. Với thông điệp cần lưu bền ở tải lớn, bản hai mươi ba của Oracle khuyên dùng hàng đợi sự kiện giao dịch.""", clear=True),
        S("""<p><b>Bước 7. Gửi trong giao dịch</b>: gửi 101 rồi hoàn tác, gửi 102 rồi chốt.</p>""" + code(AQ_ENQ),
          """Bước bảy, gửi thông điệp một trăm linh một rồi hoàn tác, sau đó gửi một trăm linh hai rồi chốt. Vì việc gửi mặc định là một phần của giao dịch đang chạy, nên hoàn tác thì thông điệp đầu biến mất.
          Năm đối số của lệnh gửi là tên hàng đợi, tuỳ chọn gửi, thuộc tính thông điệp, nội dung, và biến nhận lại mã thông điệp. Câu cuối đếm số thông điệp trong bảng hàng đợi.""", clear=True),
        S(out(AQ_ENQ_OUT) + """<p class='note'>Làm thử: 2 lần gửi − 1 lần bị hoàn tác = 1 thông điệp.</p>""",
          """Làm thử, vì lần gửi đầu đã bị hoàn tác, hai lần gửi trừ một còn một thông điệp, khớp với đầu ra thật.""", clear=True),
        S("""<p><b>Bước 8. Nhận rồi chốt.</b></p>""" + code(AQ_DEQ),
          """Bước tám, nhận một thông điệp, in ra rồi chốt. Vì không muốn treo khi hàng đợi trống, ta đặt chế độ không chờ.""", clear=True),
        S(out(AQ_DEQ_OUT) + """<p class='note'>Sau khi chốt, đếm lại bảng hàng đợi được 0: thông điệp đã nhận rời khỏi hàng đợi.</p>""",
          """Máy nhận đúng thông điệp một trăm linh hai, hai trăm nghìn. Vì việc nhận cũng nằm trong giao dịch, nên chỉ sau khi chốt thông điệp mới rời hàng đợi, và đếm lại thì còn không.""",
          clear=True),
        S("""<p><b>Bước 9. Bộ nhớ cột</b>: báo cáo cộng một cột trên hàng triệu dòng thì đọc theo cột thường nhanh hơn. Kiểm trên máy của bài:</p>""" + C(IM_CHECK) + out(IM_OUT),
          """Bước chín là bộ nhớ cột. Báo cáo thường cộng một cột trên hàng triệu dòng, nên đọc dữ liệu xếp theo cột thường ít việc hơn đọc từng dòng đầy đủ.
          Trên máy của bài, kích thước vùng nhớ cột đang là không. Ta vẫn đánh dấu bảng được, nhưng vì vùng nhớ bằng không nên chưa có gì được nạp, và bài không đo được tốc độ.""",
          clear=True),
        S(svg(1500, 430,
              box(560, 20, 380, 80, ["bộ định tuyến", "theo khoá phân mảnh"], C_PURPLE, size=22),
              box(60, 230, 380, 110, ["Mảnh 0", "một cơ sở dữ liệu riêng", "tài khoản 3, 6, 9…"], C_BLUE, size=22),
              box(560, 230, 380, 110, ["Mảnh 1", "một cơ sở dữ liệu riêng", "tài khoản 4, 7, 10…"], C_BLUE, size=22),
              box(1060, 230, 380, 110, ["Mảnh 2", "một cơ sở dữ liệu riêng", "tài khoản 5, 8, 11…"], C_BLUE, size=22),
              arrow(650, 105, 250, 225), arrow(750, 105, 750, 225), arrow(850, 105, 1250, 225),
              txt(750, 400, "quy tắc minh hoạ: mảnh = mã tài khoản chia lấy dư cho 3", 24, "middle", "#1f2937", True)),
          """Bước mười là phân mảnh, khi một cơ sở dữ liệu không đủ sức. Dữ liệu được chia theo khoá phân mảnh, như mã tài khoản, ra nhiều cơ sở dữ liệu độc lập, mỗi cái gọi là một mảnh.
          Bộ định tuyến nhìn khoá để đưa yêu cầu tới đúng mảnh. Ở đây dùng quy tắc minh hoạ, lấy mã tài khoản chia lấy dư cho ba, ví dụ tài khoản bảy vào mảnh một.""",
          clear=True),
    ], checks=["alg.bnx_l07_position('2025-03-15') == 3",
               "alg.bnx_l07_partitions(alg.bnx_l07_load(3650)) == 1 + 11",
               "alg.bnx_l07_prune('2025-03-01', '2025-04-01') == (3, 3)",
               "alg.bnx_l07_json_ids({1: '{\"kenh\":\"app\",\"so_tien\":500000}', 2: '{\"kenh\":\"atm\",\"so_tien\":2000000}', 3: '{\"kenh\":\"app\"'}, 'so_tien', 1000000) == ([1, 2], [2])",
               "alg.bnx_l07_queue([('enq', 101), ('rollback',), ('enq', 102), ('commit',)])[1] == 1",
               "alg.bnx_l07_queue([('enq', 101), ('rollback',), ('enq', 102), ('commit',), ('deq',), ('commit',)]) == ([102], 0)",
               "alg.bnx_l07_shard(7, 3) == 1"])

    ex = sc("example", "example", "Ví dụ chạy thật: cắt tỉa phân vùng, từng phép tính", [
        S("""$$① \\; 365 \\cdot 10 = \\hl{3\\,650}\\ \\text{dòng}$$
$$② \\; 1 + 11 = \\hl{12}\\ \\text{phân vùng}$$""",
          """Ta tính và so với máy. Phép tính thứ nhất, ba trăm sáu mươi lăm ngày nhân mười, bằng ba nghìn sáu trăm năm mươi dòng, khớp số dòng thật ở bước hai.
          Phép tính thứ hai, một phân vùng khai sẵn cộng mười một phân vùng tự tạo, bằng mười hai."""),
        S("""$$③ \\; 31 \\cdot 10 = \\hl{310}\\ \\text{dòng của tháng 3, nằm trong phân vùng 3}$$""" + out(PLAN_MONTH_OUT),
          """Phép tính thứ ba, tháng ba có ba mươi mốt ngày nhân mười, bằng ba trăm mười dòng, tất cả nằm trong phân vùng thứ ba.
          Kế hoạch thật ghi đọc đơn một phân vùng, phân vùng đầu và cuối đều là ba, đúng như ta chờ.""", clear=True),
        S("""$$④ \\; \\frac{310}{3\\,650} \\approx \\hlg{8{,}5\\%}\\ \\text{số dòng phải đọc}$$""",
          """Phép tính thứ tư dùng lại hai số trên. Ba trăm mười chia ba nghìn sáu trăm năm mươi, xấp xỉ tám phẩy năm phần trăm. Nhờ cắt tỉa, máy chỉ đọc chừng ấy số dòng."""),
        S("""<p>Truy vấn không lọc theo ngày (tìm giao dịch trên 5 000 000):</p>""" + code(PLAN_ALL) + out(PLAN_ALL_OUT),
          """Giờ thử một truy vấn không lọc theo ngày, tìm giao dịch trên năm triệu. Kế hoạch thật ghi đọc tất cả, từ phân vùng một.
          Cột cuối là một triệu không trăm bốn mươi tám nghìn năm trăm bảy mươi lăm, đúng bằng số phân vùng tối đa một bảng được có.
          Vì bảng tự thêm phân vùng theo tháng, máy chưa biết trước sẽ có bao nhiêu tháng.""",
          clear=True),
        S("""$$⑤ \\; \\frac{3\\,650}{310} \\approx \\hl{11{,}8}\\ \\text{lần nhiều dòng hơn}$$
<p class='note'>$1\\,048\\,575 = 1024 \\cdot 1024 - 1$: giới hạn số phân vùng của một bảng Oracle.</p>""",
          """Phép tính thứ năm, không lọc theo ngày thì phải đọc cả ba nghìn sáu trăm năm mươi dòng. Chia cho ba trăm mười, ta được xấp xỉ mười một phẩy tám lần nhiều dòng hơn.
          Con số lớn ở cột cuối bằng một nghìn không trăm hai mươi bốn nhân một nghìn không trăm hai mươi bốn, trừ một.""", clear=True),
    ], checks=["len(alg.bnx_l07_load(3650)) == 365 * 10",
               "alg.bnx_l07_partitions(alg.bnx_l07_load(3650)) == 12",
               "alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-03-01', '2025-04-01') == 310",
               "alg.bnx_l07_prune('2025-03-01', '2025-04-01') == (3, 3)",
               "round(100 * alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-03-01', '2025-04-01') / len(alg.bnx_l07_load(3650)), 1) == 8.5",
               "round(len(alg.bnx_l07_load(3650)) / alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-03-01', '2025-04-01'), 1) == 11.8",
               "alg.bnx_l07_max_partitions() == 1048575"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm thẳng trong phân vùng", [
        S("""<p>Đường khác: đếm theo điều kiện ngày, rồi đếm thẳng trong phân vùng chứa ngày 15/3 (không có điều kiện nào).</p>""" + code(PART_CHECK) + out(CHECK_OUT),
          """Kiểm bằng đường khác. Câu đầu đếm theo điều kiện ngày như trước. Câu sau không có điều kiện nào, chỉ đếm thẳng mọi dòng trong phân vùng chứa ngày mười lăm tháng ba.
          Cả hai đều ra ba trăm mười, khớp với phép tính thứ ba. Vậy phân vùng thứ ba chứa đúng và đủ tháng ba, nên đọc riêng nó là đủ."""),
        S(table(["điều bài nói", "kiểm thế nào"],
                [["phân vùng, kế hoạch, JSON, hàng đợi", "chạy thật trên Oracle bản miễn phí trong bài, đầu ra dán nguyên"],
                 ["bộ nhớ cột", "chỉ thấy vùng nhớ cột = 0 và thuộc tính đã bật; <b>chưa đo</b> tốc độ"],
                 ["phân mảnh", "chỉ ở mức khái niệm, theo hướng dẫn của Oracle; cần nhiều cơ sở dữ liệu, bài <b>không chạy</b>"]]),
          """Bảng này nói rõ điều gì đã kiểm. Phân vùng, kế hoạch thực thi, dữ liệu dạng «JSON» và hàng đợi đều chạy thật trên Oracle bản miễn phí, đầu ra dán nguyên.
          Bộ nhớ cột thì ta chỉ thấy vùng nhớ bằng không và thuộc tính đã bật, chưa đo tốc độ. Phân mảnh cần nhiều cơ sở dữ liệu, nên bài chỉ dạy ở mức khái niệm.""",
          clear=True),
    ], checks=["alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-03-01', '2025-04-01') == alg.bnx_l07_month_days(2025, 3) * 10"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        S("""<div class="box warn"><b>Lỗi 1 (người đã đi làm): bọc cột phân vùng trong hàm.</b> Cùng ý “tháng 3”, viết bằng <code>TRUNC</code>:</div>""" + code(PLAN_TRUNC) + out(PLAN_TRUNC_OUT),
          """Lỗi thứ nhất, của người đã đi làm, là bọc cột phân vùng trong một hàm. Câu này cũng hỏi tháng ba, nhưng cắt ngày về đầu tháng rồi mới so.
          Kế hoạch thật ghi đọc tất cả phân vùng, vì máy không cắt tỉa được khi cột bị biến đổi. Cách chữa là viết điều kiện khoảng trên cột gốc, như ở bước ba."""),
        S(table(["", "hàng đợi trong Oracle", "Kafka"],
                [["chung giao dịch với dữ liệu", "có: hoàn tác thì thông điệp cũng mất (bước 7)", "không: hệ riêng"],
                 ["sau khi nhận và chốt", "mặc định (thời gian lưu giữ 0): thông điệp rời hàng đợi, đếm lại được 0 (bước 8)", "vẫn lưu; người đọc tự giữ vị trí, đọc lại được"],
                 ["tải đặt lên đâu", "chính cơ sở dữ liệu giao dịch", "cụm máy riêng"]]),
          """Lỗi thứ hai là coi hàng đợi trong cơ sở dữ liệu giống hệt Kafka. Nó chung giao dịch với dữ liệu, hoàn tác thì thông điệp cũng mất, điều Kafka không làm được.
          Nhưng ở cấu hình mặc định, thời gian lưu giữ bằng không, thông điệp đã nhận và chốt thì rời hàng đợi, không đọc lại như Kafka. Và mọi tải gửi nhận đặt lên chính cơ sở dữ liệu giao dịch.""",
          clear=True),
        S("""<div class="box warn"><b>Lỗi 3 (người đã đi làm): coi phân mảnh như một cơ sở dữ liệu lớn.</b> Mỗi mảnh là một cơ sở dữ liệu riêng.</div>"""
          + table(["lệnh", "mảnh (mã mod 3, minh hoạ)", "hệ quả"],
                  [["chuyển từ tài khoản 4 sang 7", "1 và 1", "một mảnh: giao dịch trong một cơ sở dữ liệu"],
                   ["chuyển từ tài khoản 4 sang 5", "1 và 2", "xuyên mảnh: hai cơ sở dữ liệu phải cùng chốt, đắt hơn"],
                   ["tổng tiền mọi tài khoản", "không có khoá", "bộ điều phối hỏi mọi mảnh, chậm hơn đi thẳng theo khoá"]]),
          """Lỗi thứ ba, của người đã đi làm, là coi phân mảnh như một cơ sở dữ liệu lớn. Chuyển từ tài khoản bốn sang bảy, cả hai đều ở mảnh một, nên là giao dịch trong một cơ sở dữ liệu.
          Chuyển từ bốn sang năm thì xuyên hai mảnh, hai cơ sở dữ liệu phải cùng chốt, đắt hơn nhiều.
          Còn câu hỏi không có khoá phân mảnh, như tổng tiền mọi tài khoản, phải qua bộ điều phối hỏi mọi mảnh, chậm hơn đi thẳng theo khoá.""",
          clear=True),
    ], checks=["alg.bnx_l07_shard(4, 3) == alg.bnx_l07_shard(7, 3) == 1", "alg.bnx_l07_shard(5, 3) == 2",
               "alg.bnx_l07_queue([('enq', 102), ('commit',), ('deq',), ('commit',)])[1] == 0"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        S(table(["câu", "đề"],
                [["1", "Cùng bảng của bài. Truy vấn <code>ngay &gt;= DATE '2025-03-15' AND ngay &lt; DATE '2025-05-15'</code>: đọc những phân vùng nào, đếm được bao nhiêu dòng?"],
                 ["2", "Ba mảnh, mảnh = mã tài khoản chia lấy dư cho 3 (minh hoạ). Lệnh chuyển 7 → 10 và 7 → 8: lệnh nào xuyên mảnh?"],
                 ["3", "Quyết định: gửi thông báo “đã chuyển tiền” bằng hàng đợi trong Oracle hay bằng Kafka?"]]),
          """Đến lượt bạn. Câu một, cùng bảng của bài, truy vấn từ ngày mười lăm tháng ba tới trước ngày mười lăm tháng năm. Máy đọc những phân vùng nào, và đếm được bao nhiêu dòng?
          Câu hai, ba mảnh, mảnh bằng mã tài khoản chia lấy dư cho ba. Lệnh chuyển từ bảy sang mười và từ bảy sang tám, lệnh nào xuyên mảnh?
          Câu ba là một quyết định. Gửi thông báo đã chuyển tiền bằng hàng đợi trong Oracle hay bằng Kafka? Hãy dừng video và làm ra giấy.""",
          pause=25),
        S("""<p>Câu 1: khoảng chạm tháng 3, 4, 5 → phân vùng 3 tới 5 (kế hoạch thật: <code>PARTITION RANGE ITERATOR</code> = đọc lần lượt một dãy phân vùng liền nhau, Pstart 3, Pstop 5).</p>
$$17 + 30 + 14 = 61\\ \\text{ngày}, \\qquad 61 \\cdot 10 = \\hl{610}\\ \\text{dòng}$$""",
          """Đáp án câu một. Khoảng này chạm tháng ba, tháng tư và tháng năm, nên máy đọc lần lượt một dãy phân vùng liền nhau, từ phân vùng ba tới phân vùng năm, kế hoạch thật ghi đúng như vậy.
          Số ngày là mười bảy ngày cuối tháng ba, cộng ba mươi ngày tháng tư, cộng mười bốn ngày đầu tháng năm, bằng sáu mươi mốt. Nhân mười được sáu trăm mười dòng."""),
        S("""<p>Câu 2: 7 mod 3 = 1, 10 mod 3 = 1, 8 mod 3 = 2.</p>
<div class='box key'>7 → 10 cùng mảnh 1; <b>7 → 8 xuyên mảnh</b> (mảnh 1 và mảnh 2).</div>""",
          """Đáp án câu hai. Bảy chia ba dư một, mười chia ba dư một, tám chia ba dư hai. Vậy chuyển từ bảy sang mười nằm gọn trong mảnh một, còn chuyển từ bảy sang tám là xuyên mảnh."""),
        S(table(["lựa chọn", "được", "mất"],
                [["hàng đợi trong Oracle", "cùng giao dịch với lệnh chuyển: không gửi nhầm cho lệnh đã huỷ, không cần thêm cơ chế", "tải đặt lên cơ sở dữ liệu giao dịch; mặc định nhận xong là mất (muốn giữ phải đặt thời gian lưu giữ)"],
                 ["Kafka", "lưu lâu, nhiều dịch vụ cùng đọc, đọc lại được, chịu tải lớn", "ghi và gửi là hai việc riêng: cần mẫu hộp thư đi hoặc cách tương tự để không lệch"]]),
          """Đáp án câu ba, tuỳ nhu cầu. Hàng đợi trong Oracle đi cùng giao dịch của lệnh chuyển, nên không gửi nhầm thông báo cho lệnh đã huỷ, và không cần thêm cơ chế nào.
          Đổi lại, tải đặt lên chính cơ sở dữ liệu giao dịch, và ở cấu hình mặc định thì thông điệp nhận xong là mất.
          Kafka lưu lâu, nhiều dịch vụ cùng đọc và đọc lại được. Nhưng ghi và gửi là hai việc riêng, nên cần mẫu hộp thư đi, tức ghi sự kiện vào một bảng cùng giao dịch rồi gửi sau, hoặc cách tương tự, để hai bên không lệch."""),
    ], checks=["alg.bnx_l07_prune('2025-03-15', '2025-05-15') == (3, 5)",
               "alg.bnx_l07_days('2025-03-15', '2025-05-15') == 17 + 30 + 14 == 61",
               "alg.bnx_l07_count(alg.bnx_l07_load(3650), '2025-03-15', '2025-05-15') == 610",
               "(alg.bnx_l07_shard(7, 3), alg.bnx_l07_shard(10, 3), alg.bnx_l07_shard(8, 3)) == (1, 1, 2)"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        S(chain("lọc theo ngày", "phân vùng theo tháng", "kế hoạch ghi một phân vùng", "hàng đợi chung giao dịch", "bộ nhớ cột, phân mảnh khi đo thấy cần"),
          """Tổng kết chuỗi logic. Truy vấn ngân hàng thường lọc theo ngày, nên ta phân vùng theo tháng, và đọc kế hoạch để chắc máy chỉ mở một phân vùng.
          Thông báo cho hệ khác có thể đi qua hàng đợi chung giao dịch với dữ liệu. Bộ nhớ cột và phân mảnh chỉ dùng khi đã đo thấy cần."""),
        S("""<div class='box key'><b>Tư duy:</b> đừng đoán máy đọc gì, hãy hỏi kế hoạch thực thi. Một tính năng mới chỉ đáng dùng khi bạn chỉ ra được con số nó cải thiện.</div>""",
          """Điều cần mang theo. Đừng đoán máy sẽ đọc gì, hãy hỏi kế hoạch thực thi. Một tính năng mới chỉ đáng dùng khi bạn chỉ ra được con số mà nó cải thiện."""),
        S("""<p class="note">Bài sau: tìm kiếm toàn văn phân tán, chia dữ liệu thành nhiều mảnh có bản sao, và vì sao dữ liệu vừa ghi chưa tìm thấy ngay.</p>""",
          """Ở bài sau, ta gặp lại ý chia dữ liệu thành nhiều mảnh, lần này trong một hệ tìm kiếm toàn văn, có bản sao, và xem vì sao dữ liệu vừa ghi chưa tìm thấy ngay.""",
          forward_ref=True),
    ])
    return lesson("L07", "oracle_phan_vung_json_hang_doi",
                  "Bài 7 — Oracle cho khối lượng lớn: phân vùng, JSON, hàng đợi, bộ nhớ cột và phân mảnh",
                  "curriculum/bnx.yaml L07; audit/bnx/verify_bnx.py L07; Oracle Database 23 (docs.oracle.com, trang đọc 2026-11-11): VLDB and Partitioning Guide "
                  "(interval partitioning, partition pruning), Reference (Logical Database Limits, INMEMORY_SIZE), JSON Developer's Guide (IS JSON, JSON_VALUE), "
                  "PL/SQL Packages DBMS_AQADM/DBMS_AQ và AQ types (visibility ON_COMMIT), In-Memory Guide, Licensing Information (Free), Globally Distributed Database Guide",
                  ["Phân vùng bảng giao dịch theo tháng và đọc kế hoạch cắt tỉa phân vùng", "Lưu và truy vấn dữ liệu JSON trong Oracle",
                   "Gửi và nhận thông điệp bằng hàng đợi trong cơ sở dữ liệu", "Nêu khi nào cần bộ nhớ cột và phân mảnh"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
