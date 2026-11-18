import lib2
from lib2 import *
from spoken_b import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
from libj import jstep
from l06 import ORA_SETUP, ORA_PROC  # bảng và thủ tục Oracle của bài 6, để Java gọi (cổng JDBC dựng lại đúng hai khối này)
from labkit import write_lab, practice_scene

lib2.begin("L37")

# ── Mã hiện trên màn hình: T-SQL chạy NGUYÊN VĂN trên SQL Server 2022 (audit/bnx/screen/l37.yaml, audit/bnx/ver/l37.py) ──
MSS_BASE = """
IF DB_ID('bnx_l37') IS NULL CREATE DATABASE bnx_l37;
GO
USE bnx_l37;
GO
DROP TABLE IF EXISTS dbo.tk;
CREATE TABLE dbo.tk (
  id    INT PRIMARY KEY,
  ten   VARCHAR(10),
  so_du BIGINT CONSTRAINT ck_so_du CHECK (so_du >= 0));
INSERT INTO dbo.tk VALUES (1, 'A', 300000), (2, 'B', 1000000);
GO
"""

MSS_PROC = """
CREATE OR ALTER PROCEDURE dbo.chuyen_tien
  @from   INT,
  @to     INT,
  @amt    BIGINT,
  @status VARCHAR(20) OUTPUT
AS
BEGIN
  SET NOCOUNT ON;
  SET XACT_ABORT ON;
  DECLARE @x BIGINT, @bal BIGINT;
  BEGIN TRY
    IF @amt IS NULL OR @amt <= 0
      THROW 50002, 'So tien phai lon hon 0', 1;
    BEGIN TRAN;
    SELECT @x = so_du FROM dbo.tk WITH (UPDLOCK, ROWLOCK)
     WHERE id = LEAST(@from, @to);
    SELECT @x = so_du FROM dbo.tk WITH (UPDLOCK, ROWLOCK)
     WHERE id = GREATEST(@from, @to);
    SELECT @bal = so_du FROM dbo.tk WHERE id = @from;
    IF @bal < @amt
      THROW 50001, 'So du khong du', 1;
    UPDATE dbo.tk SET so_du = so_du - @amt WHERE id = @from;
    UPDATE dbo.tk SET so_du = so_du + @amt WHERE id = @to;
    COMMIT;
    SET @status = 'OK';
  END TRY
  BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK;
    THROW;
  END CATCH
END;
GO
"""

MSS_CALL_500 = """
DECLARE @st VARCHAR(20);
EXEC dbo.chuyen_tien 1, 2, 500000, @st OUTPUT;
GO
SELECT SUM(so_du) AS tong FROM dbo.tk;
"""

MSS_CALL_200 = """
DECLARE @st VARCHAR(20);
EXEC dbo.chuyen_tien 1, 2, 200000, @st OUTPUT;
SELECT @st AS trang_thai;
SELECT ten, so_du FROM dbo.tk;
SELECT SUM(so_du) AS tong FROM dbo.tk;
"""

MSS_PARTIAL = """
SET XACT_ABORT OFF;
BEGIN TRAN;
UPDATE dbo.tk SET so_du = so_du + 500000 WHERE id = 2;
UPDATE dbo.tk SET so_du = so_du - 500000 WHERE id = 1;
GO
IF @@TRANCOUNT > 0 COMMIT;
SELECT SUM(so_du) AS tong FROM dbo.tk;
"""

MSS_FIXED = """
SET XACT_ABORT ON;
BEGIN TRAN;
UPDATE dbo.tk SET so_du = so_du + 500000 WHERE id = 2;
UPDATE dbo.tk SET so_du = so_du - 500000 WHERE id = 1;
GO
IF @@TRANCOUNT > 0 COMMIT;
SELECT SUM(so_du) AS tong FROM dbo.tk;
"""

MSS_INJ_BAD = """
DECLARE @ten VARCHAR(50) = 'X'' OR ''1''=''1';
DECLARE @sql NVARCHAR(200) =
  N'SELECT ten, so_du FROM dbo.tk WHERE ten = ''' + @ten + N'''';
EXEC (@sql);
"""

MSS_INJ_GOOD = """
DECLARE @ten VARCHAR(50) = 'X'' OR ''1''=''1';
EXEC sp_executesql
  N'SELECT ten, so_du FROM dbo.tk WHERE ten = @p',
  N'@p VARCHAR(50)', @p = @ten;
"""

# Quy mô: bảng tk_lon có 2, 200, 20 000 dòng cùng tên 'K'; đếm số dòng lộ ra (đếm tất định, không đo thời gian)
MSS_SCALE = """
SET NOCOUNT ON;
DECLARE @n INT = 2, @sql NVARCHAR(200);
DECLARE @ten VARCHAR(50) = 'X'' OR ''1''=''1';
WHILE @n <= 20000
BEGIN
  DROP TABLE IF EXISTS dbo.tk_lon;
  SELECT TOP (@n) 'K' AS ten INTO dbo.tk_lon
    FROM sys.all_objects a, sys.all_objects b;
  SET @sql = N'SELECT ''ghep'', COUNT(*) FROM dbo.tk_lon WHERE ten = '''
           + @ten + N'''';
  EXEC (@sql);
  EXEC sp_executesql
    N'SELECT ''tham so'', COUNT(*) FROM dbo.tk_lon WHERE ten = @p',
    N'@p VARCHAR(50)', @p = @ten;
  SET @n = @n * 100;
END
"""

# ── Đầu ra THẬT (chạy trên bnx-mss, SQL Server 2022 RTM-CU27-GDR 16.0.4315.2; sqlcmd -h -1 -W) — lược bằng "…" ──
MSS_CALL_500_OUT = """
Msg 50001, Level 16, State 1, …
So du khong du
1300000
"""
MSS_CALL_200_OUT = """
OK
A 100000
B 1200000
1300000
"""
MSS_PARTIAL_OUT = """
Msg 547, Level 16, State 1, …
The UPDATE statement conflicted with the CHECK constraint …
The statement has been terminated.
1800000
"""
MSS_FIXED_OUT = """
Msg 547, Level 16, State 1, …
The UPDATE statement conflicted with the CHECK constraint …
1300000
"""
MSS_INJ_BAD_OUT = """
A 300000
B 1000000
(2 rows affected)
"""
MSS_INJ_GOOD_OUT = """
(0 rows affected)
"""
MSS_SCALE_OUT = """
ghep 2
tham so 0
ghep 200
tham so 0
ghep 20000
tham so 0
"""
MSS_PARTS = {"dau": (1, 10), "giua": (11, 21), "cuoi": (22, 32)}
MS = "máy chủ SQL"   # "Server" chưa có luật đọc đã dò: lời nói "máy chủ SQL", màn hình ghi SQL Server
B0 = "{1: 300000, 2: 1000000}"
MOVE = "[(2, 500000), (1, -500000)]"

# ── JDBC (Java 21 + ojdbc11-23.26.4.0.0 trong audit/bnx/deps/l37; gọi thủ tục Oracle của bài 6) ──
JAVA_GOI = prog("Goi", r'''
import java.sql.*;

public class Goi {
  static void chuyen(Connection c, long tien) {
    String goi = "{call bnx_l06_chuyen_tien(?, ?, ?, ?)}";
    try (CallableStatement cs = c.prepareCall(goi)) {
      cs.setLong(1, 1); cs.setLong(2, 2);
      cs.setLong(3, tien);
      cs.registerOutParameter(4, Types.VARCHAR);
      cs.execute();
      System.out.println(tien + ": " + cs.getString(4));
    } catch (SQLException e) {
      System.out.println(tien + ": loi " + e.getErrorCode());
    }
  }

  public static void main(String[] args) throws Exception {
    String url = "jdbc:oracle:thin:@//localhost:1521/FREEPDB1";
    String pass = System.getenv("BNX_PASS");
    try (Connection c = DriverManager.getConnection(
             url, "bnx", pass)) {
      chuyen(c, 500000);
      chuyen(c, 200000);
    }
  }
}
''', lang="java", kind="other")

JAVA_TIM = prog("Tim", r'''
import java.sql.*;

public class Tim {
  public static void main(String[] args) throws Exception {
    String url = "jdbc:oracle:thin:@//localhost:1521/FREEPDB1";
    String sql = "SELECT COUNT(*) FROM bnx_l06_tk WHERE ten = ?";
    try (Connection c = DriverManager.getConnection(
             url, "bnx", System.getenv("BNX_PASS"));
         PreparedStatement ps = c.prepareStatement(sql)) {
      for (String ten : new String[] {"A", "X' OR '1'='1"}) {
        ps.setString(1, ten);
        try (ResultSet rs = ps.executeQuery()) {
          rs.next();
          System.out.println(ten + ": " + rs.getInt(1) + " dong");
        }
      }
    }
  }
}
''', lang="java", kind="other")

SH_JDBC = prog("ChayJdbc", """
D=/d/research-video/audit/bnx/deps/l37
ls $D/ojdbc11-23.26.4.0.0.jar >/dev/null 2>&1 || { echo "NOT_VERIFIED: thiếu jar" >&2; exit 97; }
export BNX_PASS=bnx_pass
MSYS_NO_PATHCONV=1 docker exec -i bnx-ora sqlplus -s -L bnx/bnx_pass@//localhost/FREEPDB1 >/dev/null <<'SQL'
""" + ORA_SETUP.strip("\n") + "\n" + ORA_PROC.strip("\n") + """
exit
SQL
mkdir -p lib out && cp $D/*.jar lib/
javac -encoding UTF-8 -cp "lib/*" -d out Goi.java Tim.java
java -cp "out;lib/*" Goi
java -cp "out;lib/*" Tim
""", lang="bash", files={"Goi.java": "Goi", "Tim.java": "Tim"}, timeout=300,
    claims=["gọi thủ tục Oracle qua CallableStatement: 500000 báo lỗi 20001, 200000 trả OK",
            "PreparedStatement: tên A trả 1 dòng, chuỗi tấn công trả 0 dòng"])

# ── Lab (số liệu KHÁC ví dụ; sqlite làm đại diện vì bộ chấm không có SQL Server) ──
LAB_PY = r'''
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE tk (ten TEXT, so_du INTEGER)")
db.executemany("INSERT INTO tk VALUES (?, ?)",
               [("An", 500), ("Binh", 700), ("Chi", 900), ("Dung", 100)])


def ghep(ten):
    sql = "SELECT ten FROM tk WHERE ten = '" + ten + "'"
    return db.execute(sql).fetchall()


def tham_so(ten):
    sql = "SELECT ten FROM tk WHERE ten = ?"
    return db.execute(sql, (ten,)).fetchall()


CHUOI = ("An", "X' OR '1'='1", "B' OR so_du > 600 --")
for i, ten in enumerate(CHUOI, 1):
    print(f"chuoi {i}: ghep {len(ghep(ten))} dong, tham so {len(tham_so(ten))} dong")
'''
LAB_OUT = """chuoi 1: ghep 1 dong, tham so 1 dong
chuoi 2: ghep 4 dong, tham so 0 dong
chuoi 3: ghep 2 dong, tham so 0 dong"""
LAB_DE = """# Lab BNX L37 — Chống chèn mã: ghép chuỗi so với tham số hoá

SQL Server không có trong bộ chấm, nên lab dùng **sqlite** (có sẵn trong Python) để luyện đúng ý của bài: chuỗi người dùng gõ phải đi vào câu lệnh như một **giá trị**, không như một phần **câu lệnh**. Số liệu là số minh hoạ.

Dựng bảng bằng đoạn sau (cho sẵn):

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE tk (ten TEXT, so_du INTEGER)")
db.executemany("INSERT INTO tk VALUES (?, ?)",
               [("An", 500), ("Binh", 700), ("Chi", 900), ("Dung", 100)])
```

Viết `mau.py` có hai hàm tìm theo tên, mỗi hàm trả danh sách dòng `SELECT ten FROM tk WHERE ten = …`:
1. `ghep(ten)`: **ghép chuỗi** `ten` thẳng vào câu lệnh (cách sai, để thấy lỗi);
2. `tham_so(ten)`: truyền `ten` qua dấu `?` (cách đúng).

Với ba chuỗi sau (dòng 2 và 3 là chuỗi tấn công; trong chuỗi 3, `--` mở đầu chú thích SQL nên phần sau nó bị bỏ qua), đánh số từ 1, in mỗi chuỗi một dòng:
```python
CHUOI = ("An", "X' OR '1'='1", "B' OR so_du > 600 --")
```
```
chuoi <số thứ tự>: ghep <số dòng> dong, tham so <số dòng> dong
```
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L37 mau.py`.
"""


def S(show, say, **kw):
    return st(show, say.replace("«MS»", MS), **kw)


def mp(part):
    return code(MSS_PROC, lines=MSS_PARTS[part])


def build():
    hook = sc("hook", "hook", "Cùng một lỗi giữa chừng, máy chủ khác thì tiền khác", [
        S("""<p>Cùng hai tài khoản A $300\\,000$ và B $1\\,000\\,000$, cùng lệnh chuyển $500\\,000$ lỗi giữa chừng. Trên Oracle, với thủ tục có khối ngoại lệ hoàn tác, giao dịch hoàn tác <small>(không đo ở bài này)</small>. Trên SQL Server, ở chế độ mặc định, tổng thành <b class="red">$1\\,800\\,000$</b>.</p>
<div class="box warn">Và một ô tìm tên tài khoản: người gõ <code>X' OR '1'='1</code> lấy được <b>mọi</b> dòng của bảng.</div>""",
          """Chào bạn, hai tài khoản A ba trăm nghìn và B một triệu, lệnh chuyển năm trăm nghìn bị lỗi giữa chừng. Trên Oracle, thủ tục có khối ngoại lệ hoàn tác thì giao dịch hoàn tác, nhưng bài này không đo điều đó. Trên «MS», ở chế độ mặc định, tổng thành một triệu tám trăm nghìn. Và ô tìm tên ghép chuỗi có thể lộ mọi dòng của bảng."""),
        S(table(["câu hỏi", "bài này trả lời"],
                [["viết thủ tục chuyển tiền bằng T-SQL", "T-SQL là ngôn ngữ thủ tục riêng của SQL Server; chạy thật và đọc kết quả"],
                 ["lỗi giữa chừng thì sao", "tuỳ chọn <code>XACT_ABORT</code>: khi bật, lỗi lúc chạy huỷ cả giao dịch"],
                 ["chuỗi người dùng gõ thành câu lệnh", "chèn mã: kẻ xấu đưa câu lệnh vào chuỗi người dùng gõ; chặn bằng tham số"],
                 ["Java gọi thủ tục, mở kết nối an toàn", "JDBC: thư viện kết nối cơ sở dữ liệu chuẩn của Java"]]),
          """Hôm nay ta trả lời bốn câu. Viết thủ tục chuyển tiền bằng ngôn ngữ riêng của «MS»; lỗi giữa chừng thì sao khi tuỳ chọn huỷ cả giao dịch bật hay tắt. Chèn mã là gì và chặn bằng tham số thế nào; Java gọi thủ tục và mở kết nối an toàn ra sao.""",
          clear=True, introduces=["bnx_tsql", "bnx_xact_abort", "bnx_chen_ma", "bnx_jdbc"]),
    ], checks=[f"alg.bnx_l06_total(alg.bnx_l06_batch({B0}, {MOVE}, False)) == 1800000",
               "alg.bnx_l37_rows(2, \"X' OR '1'='1\", False) == 2"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu, rồi dựng bảng", [
        S(table(["khái niệm", "nghĩa", "ví dụ"],
                [["① Giao dịch", "nhóm câu lệnh cùng chốt (giữ lại) hoặc cùng hoàn tác (huỷ hết)", "trừ A và cộng B: cả hai hoặc không gì"],
                 ["② Lô lệnh và <code>GO</code>", "máy nhận lệnh theo lô; dòng <code>GO</code> báo công cụ gửi lô phía trên đi chạy", "hai lô: tạo thủ tục, rồi gọi nó"],
                 ["③ Biến <code>@</code>", "tên bắt đầu bằng @, khai bằng <code>DECLARE</code>", "<code>DECLARE @st VARCHAR(20)</code>"],
                 ["④ Kết nối", "chương trình mở kết nối tới cơ sở dữ liệu bằng địa chỉ, tên, mật khẩu, và phải đóng nó sau khi dùng", "mỗi kết nối bị bỏ quên là một chỗ chiếm không trả"]]),
          """Trước hết ta cần hiểu bốn điều. Giao dịch là nhóm câu lệnh cùng chốt hoặc cùng hoàn tác. Máy chủ nhận lệnh theo lô, dòng GO báo công cụ gửi lô phía trên đi chạy. Biến bắt đầu bằng ký hiệu a còng, khai bằng lệnh khai báo. Kết nối là đường chương trình mở tới cơ sở dữ liệu, và phải đóng sau khi dùng."""),
        jstep([(("<code>IF DB_ID('bnx_l37') IS NULL CREATE DATABASE …;</code>, <code>USE …;</code>", "tạo cơ sở dữ liệu nếu chưa có; <code>USE</code> chọn nó để các lệnh sau chạy trong đó", "Tạo cơ sở dữ liệu nếu chưa có rồi chọn nó."), "", ""),
               (("<code>dbo.tk</code>, <code>VARCHAR(10)</code>, <code>BIGINT</code>", "<code>dbo.</code>: nhóm mặc định đứng trước tên bảng; <code>VARCHAR(10)</code>: chuỗi chữ tối đa 10 ký tự; <code>BIGINT</code>: số nguyên lớn", "Nhóm mặc định đứng trước tên bảng, chuỗi tối đa mười ký tự, số nguyên lớn."), "", ""),
               (("<code>PRIMARY KEY</code>, <code>CHECK (so_du &gt;= 0)</code>", "khoá chính: mỗi dòng một giá trị riêng; ràng buộc kiểm tra: lệnh nào làm số dư âm bị từ chối", "Khoá chính định danh dòng, ràng buộc kiểm tra cấm số dư âm."), "", ""),
               (("<code>INSERT INTO dbo.tk VALUES (1, 'A', 300000), …</code>, <code>DROP TABLE IF EXISTS</code>", "thêm hai dòng, giá trị theo thứ tự cột; <code>DROP … IF EXISTS</code> xoá bảng cũ nếu có", "Chèn thêm hai dòng, và xoá bảng cũ nếu có."), "", "")]),
        S("""<p>Dựng bảng hai tài khoản trên SQL Server 2022 (RTM-CU27-GDR 16.0.4315.2), trong Docker.</p>""" + code(MSS_BASE)
          + """$$300\\,000 + 1\\,000\\,000 = \\hlg{1\\,300\\,000}$$""",
          """Ta dựng cơ sở dữ liệu và bảng trên «MS» hai nghìn không trăm hai mươi hai, chạy trong Docker. Hai dòng chèn thêm hai tài khoản, tổng một triệu ba trăm nghìn.""",
          clear=True),
    ], checks=[f"alg.bnx_l06_total({B0}) == 1300000"])

    sym = sc("sym", "symbol", "Giải mã từ khoá T-SQL", [
        S(table(["T-SQL (SQL Server)", "nghĩa"],
                [["<code>@amt BIGINT</code>, <code>@status … OUTPUT</code>", "tham số bắt đầu bằng @; <code>OUTPUT</code> là tham số ra"],
                 ["<code>SET NOCOUNT ON</code>", "tắt dòng báo số hàng bị ảnh hưởng"],
                 ["<code>SET XACT_ABORT ON</code>", "câu lệnh lỗi lúc chạy làm hoàn tác <b>cả</b> giao dịch"],
                 ["<code>BEGIN TRY … END TRY BEGIN CATCH … END CATCH</code>", "khối thử; khối bắt lỗi chạy khi khối thử lỗi"]]),
          """Bảng này giải mã từ khoá T-SQL. Tham số bắt đầu bằng ký hiệu a còng, và từ khoá sau tham số đánh dấu tham số ra. Một lệnh tắt dòng báo số hàng bị ảnh hưởng. Tuỳ chọn huỷ giao dịch khi lỗi, lúc bật, làm câu lệnh lỗi hoàn tác cả giao dịch. Khối bắt lỗi chạy khi khối thử có lỗi."""),
        S(table(["T-SQL (SQL Server)", "nghĩa"],
                [["<code>WITH (UPDLOCK, ROWLOCK)</code>", "khoá để cập nhật, khoá từng hàng: đọc dòng và giữ khoá tới khi chốt, giống <code>FOR UPDATE</code> ở cuối câu <code>SELECT</code> của Oracle"],
                 ["<code>@@TRANCOUNT</code>", "số lệnh mở giao dịch chưa kết thúc; lớn hơn 0 là còn giao dịch mở"],
                 ["<code>THROW 50001, '…', 1;</code> và <code>THROW;</code>", "báo lỗi gồm ba phần: mã (từ 50000 do mình chọn), thông báo, số trạng thái (ở đây 1); đứng một mình trong khối bắt lỗi thì ném lại lỗi vừa bắt"],
                 ["<code>EXEC dbo.chuyen_tien 1, 2, 500000, @st OUTPUT</code>", "gọi thủ tục theo tên, truyền tham số theo thứ tự"],
                 ["<code>sp_executesql</code>", "thủ tục có sẵn chạy một câu lệnh ghép sẵn, kèm giá trị truyền riêng"]]),
          """Bảng thứ hai nói về khoá, đếm giao dịch và lệnh gọi. Hai gợi ý trong ngoặc là khoá để cập nhật, khoá từng hàng, giống khoá dòng của Oracle. Biến đếm cho biết còn giao dịch mở hay không. Lệnh ném báo lỗi gồm mã riêng, thông báo và số trạng thái, đứng một mình thì ném lại lỗi vừa bắt. Thủ tục có sẵn cuối chạy câu lệnh ghép sẵn, kèm giá trị truyền riêng.""", clear=True, introduces=["bnx_sp_executesql"]),
        S(table(["viết / thấy trên màn hình", "nghĩa"],
                [["bế tắc", "hai giao dịch mỗi bên giữ một khoá và chờ khoá của bên kia, nên không bên nào đi tiếp. Ví dụ: A giữ tài khoản 1 chờ 2, B giữ tài khoản 2 chờ 1"],
                 ["<code>Msg 547, Level 16, State 1</code>", "đầu dòng lỗi của SQL Server: 547 là mã lỗi vi phạm ràng buộc, 16 là mức nặng (lỗi do câu lệnh), 1 là số trạng thái"],
                 ["<code>--</code>", "mở đầu chú thích SQL: từ đó tới hết dòng bị bỏ qua. Ví dụ: <code>WHERE ten = 'B' OR so_du &gt; 600 --'</code> bỏ dấu nháy cuối"],
                 ["<code>'X'' OR ''1''=''1'</code>", "trong chuỗi SQL, hai dấu nháy đơn liền nhau là một dấu nháy thật; nên đây là chuỗi <code>X' OR '1'='1</code>"]]),
          """Bảng này nói thêm về vài thứ sẽ gặp. Bế tắc là hai giao dịch mỗi bên giữ một khoá và chờ khoá của bên kia, nên không bên nào đi tiếp được. Dòng lỗi bắt đầu bằng mã lỗi, mức nặng và số trạng thái. Hai gạch ngang mở đầu chú thích, và trong chuỗi, hai nháy đơn liền nhau là một nháy thật.""",
          clear=True),
    ], checks=["alg.bnx_l06_lock_order(2, 1) == (1, 2)"])

    intu = sc("intuition", "intuition", "Hình dung: số phận giao dịch khi một câu lỗi, và chuỗi gõ thành câu lệnh", [
        S(svg(1500, 520,
              box(40, 40, 400, 80, "Bắt đầu giao dịch", C_GRAY, size=24),
              box(40, 160, 400, 80, ["Câu 1: cộng B 500 000", "thành công"], C_GREEN, size=22),
              box(40, 280, 400, 80, ["Câu 2: trừ A 500 000", "lỗi: A chỉ có 300 000"], C_RED, size=22),
              arrow(240, 125, 240, 155), arrow(240, 245, 240, 275),
              panel(540, 20, 440, 430, "Mặc định của SQL Server", C_AMBER, size=24),
              box(570, 110, 380, 90, ["chỉ huỷ câu 2", "giao dịch vẫn mở"], C_AMBER, size=22),
              box(570, 240, 380, 90, ["chốt: còn phần cộng B"], C_AMBER, size=22),
              box(570, 350, 380, 80, "tổng 1 800 000", C_RED, size=24, bold=True),
              panel(1030, 20, 440, 430, "XACT_ABORT ON / CATCH có ROLLBACK", C_GREEN, size=21),
              box(1060, 110, 380, 90, ["hoàn tác cả giao dịch", "huỷ luôn câu 1"], C_GREEN, size=22),
              box(1060, 240, 380, 90, ["báo lỗi lên người gọi"], C_GREEN, size=22),
              box(1060, 350, 380, 80, "tổng 1 300 000", C_GREEN, size=24, bold=True),
              arrow(445, 320, 565, 165, "#d97706"),
              '<line x1="240" y1="365" x2="240" y2="495" stroke="#16a34a" stroke-width="3.5" stroke-dasharray="8 6"/>',
              '<line x1="240" y1="495" x2="1250" y2="495" stroke="#16a34a" stroke-width="3.5" stroke-dasharray="8 6"/>',
              arrow(1250, 495, 1250, 455, "#16a34a", dash=True)),
          """Hình này cho thấy số phận giao dịch khi một câu lỗi. Câu một cộng B thành công, câu hai trừ A lỗi vì cấm số dư âm. Ở chế độ mặc định của «MS», chỉ câu hai bị huỷ, giao dịch vẫn mở, chốt thì phần cộng B còn, tổng thành một triệu tám trăm nghìn. Bật tuỳ chọn huỷ cả giao dịch, hoặc để khối bắt lỗi hoàn tác, thì cả câu một cũng bị huỷ, tổng giữ một triệu ba trăm nghìn."""),
        S(svg(1500, 470,
              panel(20, 20, 700, 430, "Ghép chuỗi: chuỗi gõ thành câu lệnh", C_RED),
              box(60, 100, 620, 80, ["câu lệnh = chữ + chuỗi người dùng gõ", "… WHERE ten = 'X' OR '1'='1'"], C_AMBER, size=22),
              box(60, 230, 620, 80, ["điều kiện 1 = 1 luôn đúng", "máy hiểu phần OR như một phần câu lệnh"], C_GRAY, size=22),
              box(60, 350, 620, 70, "trả về mọi dòng của bảng", C_RED, size=24, bold=True),
              arrow(370, 185, 370, 225), arrow(370, 315, 370, 345),
              panel(780, 20, 700, 430, "Tham số: chuỗi chỉ là một giá trị", C_GREEN),
              box(820, 100, 620, 80, ["câu lệnh cố định: … WHERE ten = @p", "giá trị @p truyền riêng"], C_BLUE, size=22),
              box(820, 230, 620, 80, ["cả chuỗi X' OR '1'='1 chỉ là một cái tên", "không có tài khoản nào tên đó"], C_GRAY, size=22),
              box(820, 350, 620, 70, "trả về 0 dòng", C_GREEN, size=24, bold=True),
              arrow(1130, 185, 1130, 225), arrow(1130, 315, 1130, 345)),
          """Hình thứ hai so hai cách đưa chuỗi người dùng gõ vào câu lệnh. Ghép chuỗi: chuỗi gõ thành một phần câu lệnh, điều kiện một bằng một luôn đúng, nên máy trả về mọi dòng. Truyền tham số: câu lệnh cố định, chuỗi đi riêng như một giá trị, chỉ là một cái tên không tồn tại, nên không có dòng nào.""", clear=True),
    ], checks=[f"alg.bnx_l06_total(alg.bnx_l06_batch({B0}, {MOVE}, False)) == 1800000",
               f"alg.bnx_l06_total(alg.bnx_l06_batch({B0}, {MOVE}, True)) == 1300000",
               "alg.bnx_l37_rows(2, \"X' OR '1'='1\", False) == 2 and alg.bnx_l37_rows(2, \"X' OR '1'='1\", True) == 0"])

    form = sc("formula", "formula", "Suy ra từng bước: dựng thủ tục chuyển tiền bằng T-SQL", [
        jstep([(("<code>CREATE OR ALTER PROCEDURE dbo.chuyen_tien … AS BEGIN … END;</code>", "tạo thủ tục, hoặc thay bản cũ nếu đã có; sau <code>AS</code>, khối <code>BEGIN … END</code> là thân thủ tục", "Tạo thủ tục hoặc thay bản cũ, thân nằm giữa chữ bắt đầu và kết thúc."), "", ""),
               (("<code>BEGIN TRAN;</code> … <code>COMMIT;</code> … <code>ROLLBACK;</code>", "mở giao dịch; chốt (giữ lại); hoàn tác (huỷ hết)", "Mở giao dịch, chốt để giữ lại, hoặc hoàn tác để huỷ hết."), "", ""),
               (("<code>SELECT SUM(so_du) AS tong FROM dbo.tk;</code>", "cộng cột <code>so_du</code> của mọi dòng, đặt tên cột kết quả là <code>tong</code>", "Cộng số dư mọi dòng, gọi kết quả là tổng."), "", "")],
              intro="Mã có chỗ lạ nên ta đọc trước."),
        S("""<p><b>Bước 1. Tham số, rồi bật huỷ cả giao dịch khi lỗi.</b> Bốn tham số; <code>@status</code> là tham số ra.</p>""" + mp("dau")
          + """<p class='note'>Làm thử: chuyển 200 000 từ 1 sang 2 thì @from = 1, @to = 2, @amt = 200 000. <code>GO</code> không phải lệnh của máy chủ, chỉ báo công cụ gửi lô.</p>""",
          """Bước một là tham số. Vì người gọi phải nói chuyển từ đâu, tới đâu và bao nhiêu, nên thủ tục có ba tham số vào và một tham số ra để trả chữ trạng thái.
          Vì muốn lỗi nào cũng hoàn tác cả giao dịch, nên ta bật tuỳ chọn huỷ cả giao dịch khi lỗi ngay từ đầu. Biến ở dòng cuối giữ tạm số dư đọc được.""",
          clear=True),
        S("""<p><b>Bước 2. Khối thử:</b> chặn số tiền không dương, mở giao dịch, khoá theo mã tăng dần, kiểm số dư.</p>""" + mp("giua")
          + """<p class='note'>Làm thử: 300 000 &lt; 500 000 nên <code>THROW 50001</code>; gọi với −100 000 thì <code>THROW 50002</code>.</p>""",
          """Bước hai là khối thử. Nó chặn số tiền không dương bằng lỗi năm mươi nghìn lẻ hai, rồi mở giao dịch. Vì hai lệnh khoá ngược thứ tự sẽ bế tắc, ta khoá hai tài khoản theo mã tăng dần.
          Hai hàm số nhỏ hơn và số lớn hơn có từ bản hai nghìn không trăm hai mươi hai. Thiếu tiền thì ném lỗi năm mươi nghìn lẻ một.""", clear=True),
        S("""<p><b>Bước 3. Ghi, chốt; khối bắt lỗi hoàn tác nếu còn giao dịch mở, rồi ném lại lỗi.</b></p>""" + mp("cuoi")
          + """<p class='note'>Làm thử: lỗi ở bước 2 thì <code>@@TRANCOUNT</code> = 1, nên hoàn tác; người gọi nhận lỗi, tổng vẫn 1 300 000.</p>""",
          """Bước ba trừ, cộng, chốt rồi ghi trạng thái. Lỗi có thể xảy ra trước hay sau khi mở giao dịch, nên khối bắt lỗi kiểm biến đếm giao dịch.
          Còn mở thì hoàn tác, rồi ném lại lỗi vừa bắt để người gọi biết. Lỗi ở bước hai làm biến đếm bằng một, nên giao dịch được hoàn tác và tổng vẫn một triệu ba trăm nghìn.""", clear=True),
    ], checks=["alg.bnx_l06_lock_order(2, 1) == (1, 2)",
               f"alg.bnx_l06_transfer({B0}, 1, 2, 500000) == (False, {B0})",
               f"alg.bnx_l06_transfer({B0}, 1, 2, 200000) == (True, {{1: 100000, 2: 1200000}})"])

    ex = sc("example", "example", "Ví dụ chạy thật trên SQL Server, từng phép tính", [
        S("""<p>Gọi thủ tục chuyển $500\\,000$ từ A sang B, rồi cộng tổng.</p>""" + code(MSS_CALL_500) + out(MSS_CALL_500_OUT)
          + """$$① \\; 300\\,000 < 500\\,000 \\;\\Rightarrow\\; \\hl{\\text{THROW 50001, tổng giữ } 1\\,300\\,000}$$""",
          """Ta chạy thật trên «MS». Chuyển năm trăm nghìn từ tài khoản một sang hai khiến thủ tục ném lỗi năm mươi nghìn lẻ một, vì ba trăm nghìn nhỏ hơn năm trăm nghìn.
          Khối bắt lỗi đã hoàn tác, nên tổng vẫn một triệu ba trăm nghìn.""", introduces=["implies"], clear=True),
        S("""<p>Gọi lại với $200\\,000$:</p>""" + code(MSS_CALL_200) + out(MSS_CALL_200_OUT)
          + """$$② \\; 300\\,000 - 200\\,000 = \\hl{100\\,000}; \\quad ③ \\; 1\\,000\\,000 + 200\\,000 = \\hl{1\\,200\\,000}; \\quad ④ \\; \\hlg{1\\,300\\,000}$$""",
          """Chuyển hai trăm nghìn thì trạng thái thành công: A còn một trăm nghìn, B thành một triệu hai trăm nghìn, tổng vẫn một triệu ba trăm nghìn.""", clear=True),
        S("""<p><b>Dựng lại bảng</b> bằng đúng khối ở phần đầu, để A và B về $300\\,000$ và $1\\,000\\,000$ trước phép thử lỗi giữa chừng:</p>""" + code(MSS_BASE),
          """Trước phép thử lỗi giữa chừng, ta dựng lại bảng bằng đúng khối ở phần đầu, để A và B về ba trăm nghìn và một triệu.""", clear=True),
        S("""<p>Cùng lỗi giữa chừng, tuỳ chọn huỷ cả giao dịch khi lỗi <b>tắt</b> (mặc định). Dòng <code>GO</code> chia khối thành hai lô:</p>""" + code(MSS_PARTIAL) + out(MSS_PARTIAL_OUT)
          + """$$⑤ \\; 1\\,300\\,000 + 500\\,000 = \\hl{1\\,800\\,000}$$""",
          """Giờ chạy cùng lỗi giữa chừng khi tuỳ chọn huỷ cả giao dịch đang tắt, đúng như mặc định. Câu trừ A lỗi, nhưng chỉ riêng câu đó bị huỷ.
          Giao dịch vẫn mở nên lệnh chốt chạy, phần cộng cho B ở lại, tổng thành một triệu tám trăm nghìn.""", clear=True),
        S("""<p><b>Dựng lại bảng lần nữa</b>, vì phép thử vừa rồi để lại tổng $1\\,800\\,000$; nếu không dựng lại, lệnh chạy tiếp từ trạng thái hỏng đó sẽ in lại $1\\,800\\,000$:</p>""" + code(MSS_BASE),
          """Phép thử vừa rồi để lại tổng một triệu tám trăm nghìn, nên ta dựng lại bảng bằng cùng khối. Nếu chạy tiếp từ trạng thái hỏng đó, kết quả vẫn là một triệu tám trăm nghìn.""", clear=True),
        S("""<p>Bảng đã dựng lại. Chỉ đổi một dòng: bật <code>XACT_ABORT</code>.</p>""" + code(MSS_FIXED) + out(MSS_FIXED_OUT),
          """Chỉ đổi một dòng, bật tuỳ chọn huỷ cả giao dịch khi lỗi. Lần này câu lỗi hoàn tác luôn phần cộng cho B và bỏ phần còn lại của lô, nên không còn gì để chốt, tổng giữ một triệu ba trăm nghìn.""", clear=True),
    ], checks=[f"alg.bnx_l06_transfer({B0}, 1, 2, 500000)[0] is False",
               f"alg.bnx_l06_total(alg.bnx_l06_transfer({B0}, 1, 2, 500000)[1]) == 1300000",
               f"alg.bnx_l06_transfer({B0}, 1, 2, 200000)[1] == {{1: 100000, 2: 1200000}}",
               f"alg.bnx_l06_total(alg.bnx_l06_batch({B0}, {MOVE}, False)) == 1800000",
               f"alg.bnx_l06_total(alg.bnx_l06_batch({B0}, {MOVE}, True)) == 1300000"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: Java gọi thủ tục qua JDBC", [
        S(table(["cần có để chạy lại", "chi tiết"],
                [["Oracle Free trong Docker", "tài khoản <code>bnx</code>; mật khẩu đặt vào biến môi trường <code>BNX_PASS</code>"],
                 ["thư viện kết nối", "tệp jar <code>ojdbc11-23.26.4.0.0.jar</code> tải từ <code>repo1.maven.org/maven2/com/oracle/database/jdbc/ojdbc11/</code>, đưa vào <code>-cp</code> khi biên dịch và chạy"],
                 ["bảng và thủ tục", "bảng <code>bnx_l06_tk</code> (id, ten, so_du) với A 300 000 và B 1 000 000; thủ tục <code>bnx_l06_chuyen_tien(p_from, p_to, p_amt, p_status OUT)</code> cùng ý như thủ tục T-SQL: thiếu tiền thì báo lỗi mã 20001"]]),
          """Ta kiểm bằng đường khác: chương trình Java gọi thủ tục qua thư viện kết nối chuẩn. Muốn chạy lại cần Oracle trong Docker, mật khẩu trong biến môi trường, tệp thư viện, và thủ tục cùng ý với thủ tục T-SQL nên kết quả so được.""",
          clear=True),
        jstep([(("<code>public class Goi { … }</code>, <code>public static void main(String[] args) throws Exception</code>", "khai lớp <code>Goi</code>; <code>main</code> là hàm máy chạy đầu tiên, <code>args</code> là mảng chuỗi gõ kèm lúc chạy; <code>throws Exception</code>: hàm có thể ném lỗi", "Hàm chính là chỗ máy bắt đầu chạy, và lời báo rằng hàm có thể ném lỗi."), "", ""),
               (("<code>import java.sql.*;</code>, <code>long tien</code>, <code>String goi = \"…\"</code>", "nạp mọi lớp của gói <code>java.sql</code>; khai biến: kiểu, tên, rồi <code>=</code> giá trị; <code>long</code>: số nguyên lớn", "Nạp các lớp kết nối; khai biến là kiểu, tên, giá trị."), "", ""),
               (("<code>catch (SQLException e) { … e.getErrorCode() … }</code>", "lỗi cơ sở dữ liệu thì nhảy vào khối <code>catch</code>; <code>e.getErrorCode()</code> cho mã lỗi", "Lỗi cơ sở dữ liệu nhảy vào khối bắt lỗi, hàm lấy ra mã lỗi."), "", "")],
              intro="Mã Java có chỗ lạ nên ta đọc trước."),
        S(JAVA_GOI.show(lines=(1, 3), title="Goi.java (1/4): đưa lớp kết nối vào, khai báo lớp, mở kết nối, mật khẩu lấy từ biến môi trường") + JAVA_GOI.show(lines=(17, 26)),
          """Địa chỉ ghi giao thức, máy, cổng và tên dịch vụ. Mật khẩu lấy từ biến môi trường nên không nằm trong mã, và khối thử mở ngoặc tự đóng kết nối khi xong, kể cả khi có lỗi.""",
          clear=True),
        S(JAVA_GOI.show(lines=(4, 15), title="Goi.java (2/4): gọi thủ tục, tham số ra, lỗi thành ngoại lệ"),
          """Hàm chuyển gọi thủ tục. Chuỗi trong ngoặc nhọn là cú pháp gọi thủ tục, mỗi dấu chấm hỏi là một tham số. Ba tham số vào gán bằng số, tham số thứ tư là tham số ra nên phải đăng ký kiểu chữ trước. Thủ tục ném lỗi thì Java nhận ngoại lệ mang mã hai mươi nghìn lẻ một.""",
          clear=True),
        jstep([(("<code>new String[] {\"A\", \"X' OR '1'='1\"}</code>, <code>for (String ten : …)</code>", "tạo mảng chuỗi với hai phần tử liệt kê; vòng lặp duyệt từng phần tử, mỗi vòng <code>ten</code> là một phần tử", "Mảng hai chuỗi, vòng lặp cho biến nhận từng chuỗi."), "", ""),
               (("<code>rs.next()</code>, <code>rs.getInt(1)</code>", "<code>rs</code> là bảng kết quả; <code>next()</code> nhảy tới dòng kế tiếp (lần đầu là dòng đầu); <code>getInt(1)</code> đọc cột số 1 dạng số nguyên", "Phải nhảy tới dòng đầu rồi mới đọc cột thứ nhất dạng số nguyên."), "", "")],
              intro="Mã Java có chỗ lạ nên ta đọc trước."),
        S(JAVA_TIM.show(lines=(1, 11), title="Tim.java (3/4): tham số hoá bằng PreparedStatement"),
          """Với câu tìm tên, ta dùng câu lệnh chuẩn bị sẵn. Dấu chấm hỏi giữ chỗ cho giá trị, và giá trị được gán riêng ở dòng sau, nên chuỗi người dùng gõ không bao giờ thành một phần câu lệnh.""",
          clear=True),
        S(JAVA_TIM.show(lines=(12, 19), title="Tim.java (4/4)") + SH_JDBC.out_html(title="Kết quả chạy thật (Goi rồi Tim)"),
          """Kết quả thật khớp với công cụ dòng lệnh nên hai đường cùng kết luận: năm trăm nghìn báo lỗi hai mươi nghìn lẻ một, hai trăm nghìn thành công. Tên A một dòng, chuỗi tấn công không dòng.""",
          clear=True),
    ], checks=["alg.bnx_l37_rows(1, 'A', True, 'A') == 1 and alg.bnx_l37_rows(2, \"X' OR '1'='1\", True) == 0"])

    quymo = sc("quymo", "example", "Khi bảng lớn dần: bao nhiêu dòng lộ ra khi ghép chuỗi", [
        S(table(["viết trong mã", "nghĩa", "ví dụ nhỏ"],
                [["<code>SELECT TOP (@n) 'K' AS ten INTO dbo.tk_lon FROM sys.all_objects a, sys.all_objects b</code>", "<code>FROM … a, … b</code> ghép mỗi dòng của bảng hệ thống với mọi dòng của chính nó, ra rất nhiều dòng; <code>TOP (@n)</code> giữ n dòng đầu; <code>INTO</code> ghi vào bảng mới; <code>'K' AS ten</code> là cột hằng tên <code>ten</code>", "<code>@n = 200</code> thì bảng mới có 200 dòng, đều tên <code>K</code>"],
                 ["<code>WHILE @n &lt;= 20000 … SET @n = @n * 100</code>", "lặp: mỗi vòng nhân n với 100", "n: 2, 200, 20 000"],
                 ["<code>@sql NVARCHAR(200)</code>, <code>N'…'</code>, <code>+</code>", "<code>NVARCHAR(200)</code>: chuỗi chữ tối đa 200 ký tự; <code>N'…'</code>: chuỗi hằng kiểu đó; <code>+</code> nối chuỗi", "<code>N'a' + N'b'</code> ra <code>ab</code>"],
                 ["<code>EXEC (@sql)</code>", "chạy chuỗi trong <code>@sql</code> như một câu lệnh", "<code>@sql = N'SELECT 1'</code> thì chạy <code>SELECT 1</code>"]]),
          """Mã đo quy mô dùng vài cách viết mới. Ghép bảng hệ thống với chính nó cho rất nhiều dòng, rồi chỉ giữ n dòng đầu. Vòng lặp nhân n với một trăm, và chuỗi hằng nối bằng dấu cộng được chạy như một câu lệnh.""",
          clear=True),
        S(code(MSS_SCALE, "Bảng có 2, 200, 20 000 dòng; đếm dòng lộ ra (1/2)", lines=(1, 8)),
          """Bây giờ xem vấn đề đổi thế nào khi bảng lớn dần. Ta tạo bảng hai dòng, rồi hai trăm, rồi hai mươi nghìn dòng. Ta đếm số dòng lộ ra, chứ không đo thời gian, nên kết quả luôn như nhau.""",
          clear=True),
        S(code(MSS_SCALE, "(2/2): mỗi vòng thử hai cách", lines=(9, 16)),
          """Mỗi vòng chạy cùng chuỗi tấn công hai lần, một lần ghép chuỗi, một lần truyền tham số.""",
          clear=True),
        S(out(MSS_SCALE_OUT, "Kết quả chạy thật trên SQL Server: số dòng lộ ra"),
          """Kết quả thật: ghép chuỗi lộ hai, hai trăm rồi hai mươi nghìn dòng, đúng bằng cả bảng, còn tham số luôn không dòng. Bảng càng lớn, kẻ xấu càng lấy được nhiều.""",
          clear=True),
        S(table(["cách", "được", "mất", "khi nào chọn"],
                [["tham số hoá", "chuỗi chỉ là giá trị; máy dùng lại kế hoạch", "không dùng được cho tên bảng, tên cột", "mọi giá trị người dùng gõ"],
                 ["ghép chuỗi", "linh hoạt, ghép được cả tên cột", "mở cửa chèn mã; lộ cả bảng", "gần như không bao giờ với giá trị gõ vào"],
                 ["danh sách cho phép", "chỉ nhận tên cột nằm trong danh sách viết sẵn", "phải cập nhật danh sách khi thêm cột", "tên cột, tên bảng do người dùng chọn"]]),
          """Bảng này cho thấy người làm nghề phải chọn gì. Tham số hoá an toàn nhưng không dùng được cho tên cột hay tên bảng, nên với tên cột do người dùng chọn ta dùng danh sách cho phép viết sẵn.
          Ghép chuỗi đổi sự linh hoạt lấy cái giá là mở cửa chèn mã.""",
          focus=[0, "1.2", "1.3", "1.3"], clear=True),
    ], checks=["[alg.bnx_l37_rows(n, \"X' OR '1'='1\", False) for n in (2, 200, 20000)] == [2, 200, 20000]",
               "[alg.bnx_l37_rows(n, \"X' OR '1'='1\", True) for n in (2, 200, 20000)] == [0, 0, 0]",
               "[2 * 100 ** k for k in range(3)] == [2, 200, 20000]"])

    write_lab("BNX", "L37", LAB_DE, "py", LAB_PY, LAB_OUT)
    lab_pr = practice_scene(sc, "Tự làm: ghép chuỗi so với tham số hoá (sqlite)", lib2.practice_steps2(
        st, "BNX", "L37",
        """<p><b>Đề</b>: sqlite có bảng <code>tk (ten, so_du)</code> với 4 tài khoản. Viết <code>mau.py</code> có hai hàm tìm theo tên:</p>
<ol><li><code>ghep(ten)</code>: ghép chuỗi <code>ten</code> thẳng vào câu lệnh</li><li><code>tham_so(ten)</code>: truyền <code>ten</code> qua dấu <code>?</code></li></ol>
<p>Với ba chuỗi cho sẵn (có hai chuỗi tấn công), in mỗi chuỗi một dòng: số dòng của cách ghép và cách tham số. SQL Server không có trong bộ chấm: sqlite đại diện. Dữ liệu và khuôn dòng in nằm trong <code>de.md</code>.</p>""",
        """Bây giờ tới phần bạn tự làm, trên cơ sở dữ liệu nhỏ có sẵn trong Python vì bộ chấm không có máy chủ SQL. Viết hai hàm tìm theo tên, một ghép chuỗi, một truyền tham số, rồi thử ba chuỗi cho sẵn và in số dòng của mỗi cách. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> ghép chuỗi là <code>"... WHERE ten = '" + ten + "'"</code>; tham số là <code>db.execute("... WHERE ten = ?", (ten,))</code> — nhớ dấu phẩy để thành bộ một phần tử. Đếm bằng <code>len(...fetchall())</code>.
Lời giải ở <code>labs/BNX/L37/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, ghép chuỗi là nối tên vào giữa hai dấu nháy đơn, còn tham số là truyền tên trong một bộ một phần tử qua dấu chấm hỏi. Đếm bằng độ dài danh sách kết quả. Lời giải nằm trong thư mục thực hành.""", pause=120), "BNX", "L37")

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        S("""<div class="box warn"><b>Lỗi 1 (người đã đi làm): tin rằng SQL Server tự hoàn tác cả giao dịch.</b> Mặc định tuỳ chọn <code>XACT_ABORT</code> tắt: ví dụ ⑤ cho tổng 1 800 000. Chữa: bật nó và để khối bắt lỗi hoàn tác rồi ném lại.</div>""",
          """Lỗi thứ nhất, của người đã đi làm, là tin rằng «MS» tự hoàn tác cả giao dịch. Mặc định tuỳ chọn đang tắt, nên phép tính thứ năm cho tổng một triệu tám trăm nghìn. Cách chữa là bật nó, và để khối bắt lỗi hoàn tác rồi ném lại."""),
        S("""<div class="box warn"><b>Lỗi 2 (người đã đi làm): ghép chuỗi người dùng gõ vào câu lệnh động.</b> Người dùng gõ <code>X' OR '1'='1</code>.</div>"""
          + code(MSS_INJ_BAD) + "<p class='note'><code>EXEC (@sql)</code>: chạy chuỗi vừa nối như một câu lệnh.</p>" + out(MSS_INJ_BAD_OUT),
          """Lỗi thứ hai là ghép chuỗi người dùng gõ vào câu lệnh động, tức câu lệnh ghép thành chuỗi lúc chạy rồi mới thực thi. Điều kiện một bằng một luôn đúng, nên máy trả về cả hai tài khoản. Thủ tục lưu trữ không tự chống được kiểu chèn mã này.""", clear=True),
        S(code(MSS_INJ_GOOD) + out(MSS_INJ_GOOD_OUT)
          + """<p class='note'>Truyền chuỗi làm <b>tham số</b> qua <code>sp_executesql</code>: cả chuỗi chỉ là một cái tên. Oracle: biến gắn, <code>EXECUTE IMMEDIATE … USING</code>.</p>""",
          """Cách chữa là truyền chuỗi đó làm tham số, qua thủ tục hệ thống chạy câu lệnh động có tham số. Cả chuỗi chỉ là một cái tên, nên không có dòng nào, và Oracle cũng truyền giá trị riêng qua biến gắn.""",
          clear=True),
        S("""<div class="box warn"><b>Lỗi 3 (người đã đi làm): kết nối cẩu thả.</b> Mật khẩu viết thẳng trong mã (lọt vào kho mã); mở kết nối mà không đóng; ghép chuỗi thay vì <code>PreparedStatement</code>. Chữa: mật khẩu từ biến môi trường, <code>try</code> tự đóng, dấu <code>?</code>.</div>""",
          """Lỗi thứ ba là kết nối cẩu thả: mật khẩu viết thẳng trong mã lọt vào kho mã, kết nối không đóng chiếm chỗ mãi, ghép chuỗi mở cửa chèn mã. Cách chữa là mật khẩu từ biến môi trường, khối thử tự đóng, giá trị qua dấu chấm hỏi.""",
          clear=True),
    ], checks=[f"alg.bnx_l06_total(alg.bnx_l06_batch({B0}, {MOVE}, False)) == 1800000",
               "alg.bnx_l37_rows(2, \"X' OR '1'='1\", False) == 2", "alg.bnx_l37_rows(2, \"X' OR '1'='1\", True) == 0"])

    Q = "{1: 800000, 2: 200000}"
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        S(table(["câu", "đề"],
                [["1", "A = 800 000, B = 200 000, XACT_ABORT tắt. Lô: cộng B 900 000, rồi trừ A 900 000 (vi phạm ràng buộc), rồi chốt. Tổng cuối? Bật XACT_ABORT thì tổng cuối?"],
                 ["2", "Bảng có 500 dòng cùng tên K, tìm theo chuỗi <code>X' OR '1'='1</code>. Ghép chuỗi lộ bao nhiêu dòng? Tham số hoá lộ bao nhiêu?"],
                 ["3", "Quyết định: bảo đảm hoàn tác chỉ bằng <code>XACT_ABORT ON</code>, chỉ bằng <code>TRY…CATCH</code> có <code>ROLLBACK</code>, hay cả hai?"]]),
          """Đến lượt bạn. Câu một: A tám trăm nghìn, B hai trăm nghìn, tuỳ chọn tắt; lô cộng B chín trăm nghìn, trừ A chín trăm nghìn vi phạm ràng buộc, rồi chốt. Tổng cuối bao nhiêu, và khi bật thì sao? Câu hai: bảng năm trăm dòng cùng tên K, ghép chuỗi lộ bao nhiêu dòng, tham số lộ bao nhiêu? Câu ba: hoàn tác bằng tuỳ chọn, khối bắt lỗi, hay cả hai? Hãy dừng video và làm ra giấy.""",
          pause=25),
        S("""<p>Câu 1: câu trừ A bị huỷ riêng, câu cộng B ở lại.</p>
$$800\\,000 + (200\\,000 + 900\\,000) = \\hl{1\\,900\\,000}; \\quad \\text{bật: } 800\\,000 + 200\\,000 = \\hlg{1\\,000\\,000}$$""",
          """Đáp án câu một. Khi tắt, câu trừ A bị huỷ riêng còn câu cộng B ở lại, nên B thành một triệu một trăm nghìn và tổng là một triệu chín trăm nghìn. Khi bật, cả lô hoàn tác, tổng giữ một triệu."""),
        S("""<p>Câu 2: ghép chuỗi → điều kiện luôn đúng → cả bảng.</p>
<div class='box key'>ghép chuỗi: <b>500</b> dòng; tham số hoá: <b>0</b> dòng.</div>""",
          """Đáp án câu hai. Ghép chuỗi lộ cả năm trăm dòng, vì điều kiện luôn đúng, còn tham số hoá lộ không dòng."""),
        S(table(["lựa chọn", "được", "mất"],
                [["chỉ <code>XACT_ABORT ON</code>", "mọi lỗi lúc chạy đều huỷ cả giao dịch", "không có chỗ báo lỗi rõ hay dọn dẹp"],
                 ["chỉ <code>TRY…CATCH</code>", "tự xử lý và báo lỗi rõ", "quên <code>ROLLBACK</code> là giao dịch dở vẫn chốt"],
                 ["cả hai", "lưới an toàn cộng báo lỗi rõ", "hai điều phải nhớ; khối bắt lỗi vẫn phải hoàn tác"]]),
          """Đáp án câu ba, nên dùng cả hai. Chỉ dùng tuỳ chọn thì mọi lỗi đều hoàn tác, nhưng không có chỗ báo lỗi rõ. Chỉ dùng khối bắt lỗi thì quên lệnh hoàn tác là giao dịch dở vẫn chốt. Dùng cả hai thì có lưới an toàn cộng báo lỗi rõ."""),
    ], checks=[f"alg.bnx_l06_total(alg.bnx_l06_batch({Q}, [(2, 900000), (1, -900000)], False)) == 1900000",
               f"alg.bnx_l06_total(alg.bnx_l06_batch({Q}, [(2, 900000), (1, -900000)], True)) == 1000000",
               "alg.bnx_l37_rows(500, \"X' OR '1'='1\", False) == 500 and alg.bnx_l37_rows(500, \"X' OR '1'='1\", True) == 0"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        S(chain("bật huỷ cả giao dịch khi lỗi", "khối bắt lỗi hoàn tác rồi ném lại", "giá trị đi qua tham số", "kết nối tự đóng, mật khẩu ngoài mã"),
          """Tổng kết chuỗi logic. Bật tuỳ chọn huỷ cả giao dịch khi lỗi, để khối bắt lỗi hoàn tác rồi ném lại. Giá trị người dùng gõ chỉ đi qua tham số. Kết nối tự đóng và mật khẩu nằm ngoài mã."""),
        S("""<div class='box key'><b>Tư duy:</b> đừng tin mặc định của một hệ. Chạy thử một lỗi giữa giao dịch và một chuỗi tấn công trên đúng hệ bạn dùng, rồi đo tổng tiền và số dòng lộ ra.</div>""",
          """Điều cần mang theo. Đừng tin mặc định của một hệ. Hãy chạy thử một lỗi giữa giao dịch và một chuỗi tấn công trên đúng hệ bạn dùng, rồi đo tổng tiền và số dòng lộ ra."""),
        S("""<p class="note">Bài sau: hàng đợi nằm ngay trong Oracle, rồi hai cách xử lý dữ liệu rất lớn.</p>""",
          """Ở bài sau, ta xem hàng đợi nằm ngay trong cơ sở dữ liệu Oracle, rồi hai cách xử lý dữ liệu rất lớn khi một máy không đủ.""",
          forward_ref=True),
    ])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L37", "tsql_jdbc_xact_abort_chen_ma",
                  "Bài 37 — T-SQL và JDBC: XACT_ABORT, chống chèn mã, kết nối an toàn",
                  "curriculum/bnx.yaml L37; audit/bnx/verify_bnx.py L37; audit/bnx/sources_l37.md: Microsoft Learn (SET XACT_ABORT, TRY...CATCH, THROW, sp_executesql, LEAST/GREATEST), "
                  "Java SE 21 API java.sql (CallableStatement, PreparedStatement), Oracle JDBC ojdbc11 23.26.4.0.0 (đọc 2026-11-14); SQL Server 2022 RTM-CU27-GDR 16.0.4315.2 và "
                  "Oracle AI Database 26ai Free 23.26.3 chạy thật trong Docker",
                  ["Viết thủ tục chuyển tiền có tham số vào và ra bằng T-SQL và chạy trên SQL Server 2022",
                   "Nêu và đo tổng tiền khi một lỗi xảy ra giữa giao dịch với XACT_ABORT tắt và bật",
                   "Hoàn tác khi lỗi bằng khối TRY…CATCH có ROLLBACK và THROW",
                   "Đếm số dòng lộ ra khi ghép chuỗi và khi tham số hoá, ở bảng 2, 200 và 20 000 dòng",
                   "Gọi thủ tục từ Java bằng CallableStatement và đọc tham số ra",
                   "Mở kết nối an toàn: đóng bằng try-with-resources, lấy mật khẩu từ biến môi trường, tham số hoá bằng PreparedStatement",
                   "Chọn cách chặn chèn mã theo tình huống và nêu cái được, cái mất",
                   "Viết hàm tìm tài khoản theo tên bằng ghép chuỗi và bằng tham số, rồi so số dòng với chuỗi tấn công"],
                  scenes, assumes=["bnx_ngoai_le"],
                  covers=[(1, "formula"), (2, "example"), (3, "formula"), (4, "quymo"), (5, "check"), (6, "check"), (7, "quymo"), (8, "practice")])
