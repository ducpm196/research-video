from lib import *

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

MSS_DB = """
IF DB_ID('bnx_l06') IS NULL CREATE DATABASE bnx_l06;
GO
USE bnx_l06;
GO
"""

MSS_SETUP = """
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

JAVA_CALL = """
try (Connection c = DriverManager.getConnection(url, user, pass);
     CallableStatement cs = c.prepareCall(
         "{call bnx_l06_chuyen_tien(?, ?, ?, ?)}")) {
  cs.setLong(1, 1);
  cs.setLong(2, 2);
  cs.setLong(3, 200000);
  cs.registerOutParameter(4, Types.VARCHAR);
  cs.execute();
  System.out.println("trang thai: " + cs.getString(4));
} catch (SQLException e) {
  System.out.println(e.getErrorCode() + " " + e.getMessage());
}
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

# Phần của thủ tục hiện ở từng bước (dòng tính từ 1)
ORA_PARTS = {"thamso": (1, 11), "khoa": (12, 15), "kiem": (16, 19), "ghi": (20, 23), "loi": (24, 29)}
MSS_PARTS = {"dau": (1, 10), "giua": (11, 21), "cuoi": (22, 32)}

# Tên hệ thứ hai trong lời đọc: "Server" chưa có luật đọc đã dò (BRIEF mục 4) → nói "máy chủ SQL"; màn hình ghi SQL Server.
MS = "máy chủ SQL"
B0 = "{1: 300000, 2: 1000000}"


def S(show, say, **kw):
    return st(show, say.replace("«MS»", MS), **kw)


def build():
    hook = sc("hook", "hook", "Chuyển 500 000 thất bại mà ngân hàng mất 500 000", [
        S("""<p>Tài khoản A có $300\\,000$, tài khoản B có $1\\,000\\,000$. Khách A ra lệnh chuyển $500\\,000$ sang B.</p>
<p>Một thủ tục viết vội: <b>cộng B trước</b>, rồi trừ A. Trừ A lỗi vì không đủ tiền, nhưng phần cộng B vẫn được chốt.</p>
<div class="box warn">Tổng tiền hai tài khoản: trước $1\\,300\\,000$, sau <b class="red">$1\\,800\\,000$</b>. Ngân hàng vừa tự sinh ra $500\\,000$.</div>""",
          """Chào bạn, tài khoản A có ba trăm nghìn, tài khoản B có một triệu, và khách A ra lệnh chuyển năm trăm nghìn sang B.
          Một thủ tục viết vội cộng tiền cho B trước, rồi mới trừ A. Trừ A bị lỗi vì không đủ tiền, nhưng phần cộng cho B vẫn được chốt.
          Tổng tiền hai tài khoản trước là một triệu ba trăm nghìn, sau lại là một triệu tám trăm nghìn, tức ngân hàng vừa tự sinh ra năm trăm nghìn."""),
        S(table(["câu hỏi", "bài này trả lời"],
                [["viết thủ tục chuyển tiền thế nào", "tham số vào và ra, bằng PL/SQL của Oracle và T-SQL của SQL Server"],
                 ["lỗi giữa chừng thì sao", "khối bắt lỗi: hoàn tác cả giao dịch rồi báo lỗi lên"],
                 ["hai lệnh chuyển ngược chiều cùng lúc", "khoá hai tài khoản theo thứ tự mã tăng dần"],
                 ["ứng dụng gọi thủ tục ra sao", "Java gọi qua JDBC"]]),
          """Hôm nay ta trả lời bốn câu hỏi. Viết thủ tục chuyển tiền có tham số vào và ra thế nào, bằng PL/SQL của Oracle và bằng ngôn ngữ thủ tục của «MS».
          Lỗi giữa chừng thì làm gì, để cả giao dịch được hoàn tác. Hai lệnh chuyển ngược chiều chạy cùng lúc thì khoá thế nào cho khỏi bế tắc.
          Và chương trình Java gọi thủ tục ra sao, qua thư viện kết nối cơ sở dữ liệu chuẩn của Java."""),
    ], checks=[f"alg.bnx_l06_total({B0}) == 1300000",
               f"alg.bnx_l06_total(alg.bnx_l06_batch({B0}, [(2, 500000), (1, -500000)], False)) == 1800000"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        S(table(["khái niệm", "nghĩa", "ví dụ"],
                [["① Giao dịch", "nhóm câu lệnh cùng thành công (chốt) hoặc cùng huỷ (hoàn tác)", "trừ A 200 000 và cộng B 200 000: cả hai, hoặc không gì"],
                 ["② Khoá hàng", "<code>SELECT … FOR UPDATE</code> đọc và giữ hàng tới khi chốt hoặc hoàn tác; phiên khác muốn sửa phải chờ", "phiên 1 khoá A, phiên 2 sửa A phải đợi"],
                 ["③ Bế tắc ORA-00060", "hai phiên khoá ngược thứ tự rồi chờ nhau; Oracle phát hiện và hoàn tác một câu lệnh của một phiên", "phiên 1 giữ A chờ B, phiên 2 giữ B chờ A"],
                 ["④ Thủ tục lưu trữ", "đoạn mã có tên, cất sẵn trong cơ sở dữ liệu, nhận tham số; ứng dụng gọi bằng tên", "chuyen_tien(1, 2, 200000)"]]),
          """Trước hết ta cần hiểu bốn điều. Giao dịch là một nhóm câu lệnh cùng thành công, gọi là chốt, hoặc cùng bị huỷ, gọi là hoàn tác.
          Khoá hàng là khi ta đọc một hàng kèm ý định sửa, cơ sở dữ liệu giữ hàng đó tới khi chốt hoặc hoàn tác, nên phiên khác muốn sửa phải chờ.
          Bế tắc mang mã lỗi ORA-00060 xảy ra khi hai phiên khoá ngược thứ tự rồi chờ nhau mãi. Oracle phát hiện và hoàn tác một câu lệnh của một phiên.
          Cuối cùng, thủ tục lưu trữ là một đoạn mã có tên, cất sẵn trong cơ sở dữ liệu và nhận tham số, để ứng dụng chỉ cần gọi tên nó."""),
        S("""<p>Chuyển tiền giữa hai tài khoản trong cùng ngân hàng không làm tiền sinh ra hay mất đi, nên tổng phải giữ nguyên:</p>
$$300\\,000 + 1\\,000\\,000 = \\hlg{1\\,300\\,000}$$
<p class="note">Đây là phép thử cho mọi lần chạy trong bài: trước và sau, tổng phải là 1 300 000.</p>""",
          """Một ví dụ số. Chuyển tiền giữa hai tài khoản trong cùng ngân hàng không làm tiền sinh ra hay mất đi, nên tổng phải giữ nguyên.
          Ba trăm nghìn cộng một triệu bằng một triệu ba trăm nghìn. Đó là phép thử ta dùng cho mọi lần chạy trong bài.""", clear=True),
    ], checks=[f"alg.bnx_l06_total({B0}) == 1300000", "alg.bnx_l06_lock_order(2, 1) == (1, 2)"])

    sym = sc("sym", "symbol", "Giải mã từ khoá của hai hệ", [
        S(table(["PL/SQL (Oracle)", "nghĩa"],
                [["<code>p_amt IN NUMBER</code>", "tham số vào: người gọi đưa số tiền vào"],
                 ["<code>p_status OUT VARCHAR2</code>", "tham số ra: thủ tục trả chữ <code>OK</code> về cho người gọi"],
                 ["<code>LEAST(2, 1)</code>, <code>GREATEST(2, 1)</code>", "số nhỏ hơn là 1, số lớn hơn là 2"],
                 ["<code>RAISE_APPLICATION_ERROR(-20001, '…')</code>", "tự báo một lỗi có mã riêng, mã nằm trong khoảng −20000 tới −20999"],
                 ["<code>EXCEPTION WHEN OTHERS THEN</code>", "phần bắt lỗi: bắt mọi lỗi xảy ra phía trên"],
                 ["<code>RAISE;</code>", "ném tiếp lỗi vừa bắt lên người gọi"]]),
          """Bảng này giải mã từ khoá PL/SQL. Từ khoá vào sau tên tham số nghĩa là tham số vào, người gọi đưa số tiền vào.
          Từ khoá ra đánh dấu tham số ra, thủ tục ghi chữ báo thành công vào đó để trả về. Hai hàm tiếp theo lấy số nhỏ hơn và số lớn hơn, với hai và một thì được một và hai.
          Lệnh báo lỗi riêng của ứng dụng tự tạo một lỗi có mã riêng, nằm trong khoảng từ âm hai mươi nghìn tới âm hai mươi nghìn chín trăm chín mươi chín.
          Phần bắt lỗi bắt mọi lỗi xảy ra phía trên nó. Còn lệnh ném tiếp chuyển lỗi vừa bắt lên cho người gọi."""),
        S(table(["T-SQL (SQL Server)", "nghĩa"],
                [["<code>@amt BIGINT</code>, <code>@status … OUTPUT</code>", "tham số bắt đầu bằng @; OUTPUT là tham số ra"],
                 ["<code>SET XACT_ABORT ON</code>", "câu lệnh lỗi lúc chạy làm hoàn tác <b>cả</b> giao dịch"],
                 ["<code>BEGIN TRY … END TRY BEGIN CATCH … END CATCH</code>", "khối thử, và khối bắt lỗi chạy khi khối thử lỗi"],
                 ["<code>WITH (UPDLOCK, ROWLOCK)</code>", "khoá để cập nhật, khoá từng hàng: giống FOR UPDATE"],
                 ["<code>@@TRANCOUNT</code>", "số lệnh BEGIN TRAN chưa kết thúc (độ lồng); lớn hơn 0 là còn giao dịch mở"],
                 ["<code>THROW;</code>", "trong khối bắt lỗi: ném lại lỗi vừa bắt"]]),
          """Còn đây là từ khoá của ngôn ngữ thủ tục bên «MS». Tham số bắt đầu bằng ký hiệu a còng, và từ khoá đứng sau một tham số đánh dấu tham số đó là tham số ra.
          Tuỳ chọn huỷ giao dịch khi lỗi, lúc bật lên, làm một câu lệnh lỗi hoàn tác cả giao dịch. Khối thử chứa việc chính, khối bắt lỗi chạy khi khối thử có lỗi.
          Hai gợi ý trong ngoặc là khoá để cập nhật và khoá từng hàng, giống khoá để cập nhật của Oracle. Biến đếm cho biết số lệnh mở giao dịch chưa kết thúc, lớn hơn không là còn giao dịch đang mở.
          Cuối cùng, lệnh ném không kèm gì, đặt trong khối bắt lỗi, ném lại đúng lỗi vừa bắt.""", clear=True),
    ], checks=["alg.bnx_l06_lock_order(2, 1) == (1, 2)", "alg.bnx_l06_lock_order(1, 2) == (1, 2)"])

    intu = sc("intuition", "intuition", "Hình dung: thứ tự khoá, và số phận giao dịch khi một câu lỗi", [
        S(svg(1500, 470,
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
          """Hình bên trái là cách khoá theo chiều chuyển. Lệnh một chuyển từ A sang B nên khoá A trước, lệnh hai chuyển ngược lại nên khoá B trước.
          Mỗi lệnh giữ một tài khoản và chờ tài khoản kia, nên hai lệnh chờ nhau mãi, và Oracle báo bế tắc.
          Hình bên phải khoá theo mã tăng dần, A có mã một, B có mã hai. Cả hai lệnh đều khoá mã một trước, nên lệnh sau chỉ việc chờ lệnh trước xong, không có vòng tròn."""),
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
          """Hình này cho thấy số phận của giao dịch khi một câu lệnh lỗi. Câu một cộng cho B năm trăm nghìn, thành công. Câu hai trừ A năm trăm nghìn, lỗi vì A chỉ có ba trăm nghìn mà bảng có ràng buộc kiểm tra cấm số dư âm.
          Với lỗi vi phạm ràng buộc như thế này, ở chế độ mặc định của «MS», chỉ câu hai bị huỷ. Giao dịch vẫn mở, và khi chốt thì phần cộng cho B còn nguyên, tổng thành một triệu tám trăm nghìn.
          Khi bật tuỳ chọn huỷ giao dịch khi lỗi, hoặc khối bắt lỗi có lệnh hoàn tác, cả câu một cũng bị huỷ, lỗi được báo lên, và tổng giữ một triệu ba trăm nghìn."""),
    ], checks=[f"alg.bnx_l06_total(alg.bnx_l06_batch({B0}, [(2, 500000), (1, -500000)], False)) == 1800000",
               f"alg.bnx_l06_total(alg.bnx_l06_batch({B0}, [(2, 500000), (1, -500000)], True)) == 1300000"])

    def op(part, title=None):
        return code(ORA_PROC, title, lines=ORA_PARTS[part])

    form = sc("formula", "formula", "Suy ra từng bước: dựng thủ tục chuyển tiền trên Oracle", [
        S("""<p><b>Bước 1. Tham số, rồi chặn số tiền không dương.</b> Người gọi đưa vào: từ tài khoản nào, tới tài khoản nào, bao nhiêu tiền. Thủ tục trả ra một chữ trạng thái.</p>"""
          + op("thamso") + """<p class='note'>Làm thử: chuyển 200 000 từ 1 sang 2 thì p_from = 1, p_to = 2, p_amt = 200 000; gọi với −100 000 thì báo lỗi −20002.</p>""",
          """Bước một là tham số. Vì người gọi phải nói chuyển từ đâu, tới đâu và bao nhiêu, nên thủ tục có ba tham số vào, và một tham số ra để trả chữ trạng thái.
          Hai biến bên dưới dùng để chứa số dư đọc được. Vì số tiền âm sẽ kéo tiền ngược từ người nhận về, nên việc đầu tiên là chặn số tiền không lớn hơn không.
          Làm thử, chuyển hai trăm nghìn từ tài khoản một sang tài khoản hai thì ba tham số vào là một, hai và hai trăm nghìn, còn gọi với âm một trăm nghìn thì bị báo lỗi."""),
        S("""<p><b>Bước 2. Khoá hai tài khoản theo mã tăng dần</b>, dù tiền đi chiều nào.</p>""" + op("khoa")
          + """<p class='note'>Làm thử: chuyển từ 2 sang 1 thì vẫn khoá LEAST(2, 1) = 1 trước, rồi GREATEST(2, 1) = 2.</p>""",
          """Bước hai, khoá hai tài khoản. Vì hai lệnh khoá ngược thứ tự sẽ bế tắc, nên ta luôn khoá tài khoản có mã nhỏ trước, mã lớn sau, dù tiền đi chiều nào.
          Mỗi câu đọc kèm khoá để cập nhật, nên hàng bị giữ tới khi chốt hoặc hoàn tác. Làm thử, chuyển từ hai sang một thì vẫn khoá mã một trước, rồi mới tới mã hai.""", clear=True),
        S("""<p><b>Bước 3. Kiểm số dư, thiếu thì báo lỗi</b> trước khi ghi bất cứ gì.</p>""" + op("kiem")
          + """<p class='note'>Làm thử: 300 000 &lt; 500 000 nên báo lỗi −20001.</p>""",
          """Bước ba, kiểm số dư. Vì hai tài khoản đã bị khoá, số dư đọc lúc này không ai đổi được nữa, nên kiểm ở đây là chắc chắn.
          Thiếu tiền thì gọi lệnh báo lỗi riêng với mã âm hai mươi nghìn lẻ một. Làm thử, ba trăm nghìn nhỏ hơn năm trăm nghìn, nên thủ tục báo lỗi.""", clear=True),
        S("""<p><b>Bước 4. Trừ, cộng, chốt</b>, rồi mới ghi trạng thái.</p>""" + op("ghi")
          + """<p class='note'>Làm thử: 300 000 − 200 000 = 100 000; 1 000 000 + 200 000 = 1 200 000.</p>""",
          """Bước bốn, trừ tài khoản gửi, cộng tài khoản nhận, rồi chốt. Vì hai câu cập nhật nằm trong cùng một giao dịch, nên chúng cùng được ghi hoặc cùng bị huỷ.
          Làm thử với hai trăm nghìn, A còn một trăm nghìn, B lên một triệu hai trăm nghìn, và tham số ra nhận chữ báo thành công.""", clear=True),
        S("""<p><b>Bước 5. Bắt lỗi: hoàn tác, rồi báo lên.</b></p>""" + op("loi")
          + """<p class='note'>Làm thử: lỗi ở bước 3, hoàn tác, người gọi nhận lỗi −20001, tổng vẫn 1 300 000.</p>""",
          """Bước năm là phần bắt lỗi. Vì bất cứ câu nào phía trên cũng có thể lỗi, nên phần này hoàn tác mọi thứ giao dịch đã làm, và nhả luôn hai khoá.
          Rồi lệnh ném tiếp đẩy lỗi lên người gọi, để ứng dụng biết lệnh chuyển thất bại. Làm thử, lỗi ở bước ba được hoàn tác, người gọi nhận lỗi, tổng vẫn một triệu ba trăm nghìn.
          Lưu ý, lệnh chốt và hoàn tác trong thủ tục tác động lên cả giao dịch của người gọi, nên dòng người gọi ghi trước đó mà chưa chốt cũng bị chốt hoặc bị huỷ theo.
          Dấu gạch chéo ở cuối báo cho công cụ dòng lệnh chạy lệnh tạo thủ tục phía trên.""", clear=True),
        S("""<p><b>Bước 6. Gọi từ Java qua JDBC</b>: chuỗi <code>{call …}</code>, mỗi dấu <code>?</code> là một tham số; tham số ra phải đăng ký kiểu trước khi chạy.</p>"""
          + code(JAVA_CALL),
          """Bước sáu, chương trình Java gọi thủ tục qua thư viện kết nối cơ sở dữ liệu chuẩn của Java. Chuỗi trong ngoặc nhọn là cú pháp gọi thủ tục, mỗi dấu chấm hỏi là một tham số, đánh số từ một.
          Dòng đầu mở kết nối bằng địa chỉ cơ sở dữ liệu, tên và mật khẩu, và kết nối tự đóng khi khối thử kết thúc. Ba tham số vào được gán bằng số. Vì tham số thứ tư là tham số ra, nên phải đăng ký kiểu chữ cho nó trước khi chạy, rồi mới đọc giá trị sau khi chạy.
          Nếu thủ tục ném lỗi, Java nhận một ngoại lệ mang mã lỗi hai mươi nghìn lẻ một, đúng số sau chữ O R A, không có dấu âm, nên ứng dụng biết lệnh chuyển thất bại.""", clear=True),
    ], checks=["alg.bnx_l06_lock_order(2, 1) == (1, 2)",
               f"alg.bnx_l06_transfer({B0}, 1, 2, 500000) == (False, {B0})",
               f"alg.bnx_l06_transfer({B0}, 1, 2, 200000) == (True, {{1: 100000, 2: 1200000}})"])

    ex = sc("example", "example", "Ví dụ chạy thật trên Oracle, từng phép tính", [
        S("""<p>Tạo bảng hai tài khoản; ràng buộc <code>CHECK</code> cấm số dư âm.</p>""" + code(ORA_SETUP),
          """Ta chạy thật trên Oracle. Khối này tạo bảng hai tài khoản, A có ba trăm nghìn, B có một triệu.
          Ràng buộc kiểm tra cấm số dư âm, nên dù thủ tục có quên kiểm số dư, cơ sở dữ liệu vẫn chặn được."""),
        S("""<p>Gọi thủ tục chuyển $500\\,000$ từ A sang B, rồi cộng tổng số dư.</p>""" + code(ORA_CALL_500),
          """Khối này gọi thủ tục chuyển năm trăm nghìn từ tài khoản một sang tài khoản hai, rồi cộng tổng số dư hai tài khoản để xem tiền có lệch không.""",
          clear=True),
        S("""$$① \\; 300\\,000 < 500\\,000 \\;\\Rightarrow\\; \\hl{\\text{báo lỗi −20001}}$$""" + out(ORA_CALL_500_OUT),
          """Phép tính thứ nhất, ba trăm nghìn nhỏ hơn năm trăm nghìn, nên thủ tục báo lỗi mã âm hai mươi nghìn lẻ một. Trong đầu ra thật, dòng hai mươi bảy là lệnh ném tiếp, còn dòng mười tám là nơi lỗi được ném ra.""",
          introduces=["implies"], clear=True),
        S("""$$② \\; 300\\,000 + 1\\,000\\,000 = \\hlg{1\\,300\\,000}$$
<p>Phần bắt lỗi đã hoàn tác: hai số dư không đổi, tổng in ra đúng $1\\,300\\,000$.</p>""",
          """Phép tính thứ hai, vì phần bắt lỗi đã hoàn tác, hai số dư không đổi. Ba trăm nghìn cộng một triệu vẫn là một triệu ba trăm nghìn, khớp với tổng máy in ra."""),
        S("""<p>Gọi lại với $200\\,000$:</p>""" + code(ORA_CALL_200)
          + """$$③ \\; 300\\,000 - 200\\,000 = \\hl{100\\,000}\\ \\text{(A)}$$""",
          """Bây giờ gọi lại với hai trăm nghìn, rồi in số dư từng tài khoản. Phép tính thứ ba, A còn ba trăm nghìn trừ hai trăm nghìn, bằng một trăm nghìn.""",
          clear=True),
        S("""$$④ \\; 1\\,000\\,000 + 200\\,000 = \\hl{1\\,200\\,000}\\ \\text{(B)}$$
$$⑤ \\; 100\\,000 + 1\\,200\\,000 = \\hlg{1\\,300\\,000}$$""" + out(ORA_CALL_200_OUT),
          """Phép tính thứ tư, B có một triệu cộng hai trăm nghìn, bằng một triệu hai trăm nghìn. Phép tính thứ năm dùng lại hai kết quả trên, một trăm nghìn cộng một triệu hai trăm nghìn bằng một triệu ba trăm nghìn.
          Đầu ra thật in trạng thái thành công, A một trăm nghìn, B một triệu hai trăm nghìn, tổng không đổi.""", clear=True),
    ], checks=[f"alg.bnx_l06_transfer({B0}, 1, 2, 500000)[0] is False",
               f"alg.bnx_l06_total(alg.bnx_l06_transfer({B0}, 1, 2, 500000)[1]) == 1300000",
               f"alg.bnx_l06_transfer({B0}, 1, 2, 200000)[1][1] == 100000",
               f"alg.bnx_l06_transfer({B0}, 1, 2, 200000)[1][2] == 1200000",
               f"alg.bnx_l06_total(alg.bnx_l06_transfer({B0}, 1, 2, 200000)[1]) == 1300000"])

    def mp(part):
        return code(MSS_PROC, lines=MSS_PARTS[part])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: cùng thủ tục viết lại trên SQL Server", [
        S("""<p>Đường khác: viết lại thủ tục bằng T-SQL, chạy trên một hệ khác hẳn, xem có ra cùng tổng không. Phần đầu (<code>SET NOCOUNT ON</code>: tắt dòng báo số hàng bị ảnh hưởng):</p>""" + mp("dau"),
          """Kiểm bằng đường khác. Ta viết lại thủ tục bằng ngôn ngữ thủ tục của «MS» và chạy trên hệ đó, một hệ khác hẳn, xem có ra cùng kết quả không.
          Phần đầu khai bốn tham số, tham số cuối là tham số ra, rồi tắt dòng thông báo số hàng bị ảnh hưởng. Vì muốn lỗi nào cũng hoàn tác cả giao dịch, nên ta bật tuỳ chọn huỷ cả giao dịch khi lỗi, ngay từ đầu thủ tục."""),
        S("""<p>Khối thử: chặn số tiền không dương, mở giao dịch, khoá theo mã tăng dần, kiểm số dư.</p>""" + mp("giua"),
          """Khối thử chặn số tiền không dương bằng lỗi năm mươi nghìn lẻ hai, mở giao dịch, rồi khoá hai tài khoản theo mã tăng dần bằng gợi ý khoá để cập nhật. Hai hàm số nhỏ hơn và số lớn hơn có từ bản hai nghìn không trăm hai mươi hai.
          Thiếu tiền thì lệnh ném tạo lỗi mã năm mươi nghìn lẻ một.""", clear=True),
        S("""<p>Ghi, chốt; khối bắt lỗi hoàn tác nếu còn giao dịch mở, rồi ném lại lỗi.</p>""" + mp("cuoi"),
          """Phần cuối trừ, cộng, chốt rồi ghi trạng thái. Vì lỗi có thể xảy ra trước hay sau khi mở giao dịch, nên khối bắt lỗi kiểm biến đếm giao dịch, còn giao dịch mở thì hoàn tác, rồi ném lại đúng lỗi vừa bắt.
          Dòng chữ GO ở cuối báo cho công cụ dòng lệnh gửi các dòng phía trên đi chạy thành một lô.""", clear=True),
        S(code(MSS_CALL_500) + out(MSS_CALL_500_OUT),
          """Chạy thật lệnh chuyển năm trăm nghìn như trên Oracle. Thủ tục báo lỗi năm mươi nghìn lẻ một, khối bắt lỗi đã hoàn tác, nên tổng vẫn một triệu ba trăm nghìn.""",
          clear=True),
        S(code(MSS_CALL_200) + out(MSS_CALL_200_OUT),
          """Chuyển hai trăm nghìn thì trạng thái thành công, A một trăm nghìn, B một triệu hai trăm nghìn, tổng vẫn một triệu ba trăm nghìn.
          Vì hai hệ khác nhau, hai cách viết khác nhau mà cho cùng các con số, nên ta tin kết quả hơn.""", clear=True),
    ], checks=[f"alg.bnx_l06_total(alg.bnx_l06_transfer({B0}, 1, 2, 500000)[1]) == 1300000",
               f"alg.bnx_l06_transfer({B0}, 1, 2, 200000) == (True, {{1: 100000, 2: 1200000}})"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        S("""<div class="box warn"><b>Lỗi 1 (người đã đi làm): bắt lỗi rồi nuốt lỗi.</b> Trước hết xem khối <b>không</b> bắt lỗi: cộng B trước, trừ A sau.</div>"""
          + code(ORA_NOHANDLER),
          """Lỗi thứ nhất, của người đã đi làm, là bắt lỗi rồi nuốt lỗi. Trước hết xem khối này không có phần bắt lỗi, nó cộng B trước, rồi trừ A năm trăm nghìn."""),
        S(out(ORA_NOHANDLER_OUT) + """<p class='note'>Câu trừ A vi phạm ràng buộc; lỗi về tới người gọi, Oracle hoàn tác mọi thay đổi của lời gọi đó.</p>""",
          """Câu trừ A vi phạm ràng buộc số dư không âm. Lỗi đi thẳng về người gọi, và Oracle hoàn tác mọi thay đổi của chính lời gọi đó, nên tổng vẫn một triệu ba trăm nghìn.
          Lưu ý, đây là hoàn tác cấp câu lệnh của lời gọi từ ứng dụng. Bản thân khối mã không tự hoàn tác, nên nếu có ai bắt lỗi ở giữa thì thay đổi còn nguyên.""",
          clear=True),
        S(code(ORA_SWALLOW),
          """Giờ chỉ thêm một phần bắt mọi lỗi mà không làm gì cả. Các câu còn lại giữ nguyên.""", clear=True),
        S(out(ORA_SWALLOW_OUT)
          + """<p class='note'><code>WHEN OTHERS THEN NULL</code>: không báo lỗi nào, câu cộng B còn lại và được chốt. Cách chữa: hoàn tác rồi <code>RAISE</code> như bước 5.</p>""",
          """Lỗi bị nuốt, nên khối chạy xong như thành công, câu cộng cho B còn lại và được chốt. Kết quả là tổng một triệu tám trăm nghìn mà không có thông báo nào.
          Cách chữa là hoàn tác rồi ném tiếp lỗi, đúng như bước năm.""", clear=True),
        S("""<div class="box warn"><b>Lỗi 2 (người đã đi làm): tin rằng SQL Server tự hoàn tác.</b> Mặc định <code>XACT_ABORT OFF</code>.</div>"""
          + code(MSS_PARTIAL),
          """Lỗi thứ hai, cũng của người đã đi làm, là tin rằng «MS» tự hoàn tác cả giao dịch. Khối này để tuỳ chọn huỷ giao dịch khi lỗi ở mức tắt, đúng như mặc định.
          Nó cộng B, trừ A, rồi chốt nếu còn giao dịch đang mở. Dòng chữ GO chia khối thành hai lô, nên lệnh chốt nằm ở lô sau.""", clear=True),
        S(out(MSS_PARTIAL_OUT) + """<p class='note'>Chỉ câu trừ A bị huỷ; giao dịch vẫn mở nên lệnh chốt chạy, phần cộng B ở lại.</p>""",
          """Câu trừ A lỗi chỉ bị huỷ riêng, máy in là câu lệnh đã bị dừng. Vì giao dịch vẫn mở, lệnh chốt được chạy, và tổng thành một triệu tám trăm nghìn.""",
          clear=True),
        S(code(MSS_FIXED) + out(MSS_FIXED_OUT),
          """Chỉ đổi một dòng, bật tuỳ chọn huỷ cả giao dịch khi lỗi. Lần này câu lỗi hoàn tác luôn phần cộng cho B và bỏ phần còn lại của lô, nên không còn giao dịch nào để chốt, tổng giữ một triệu ba trăm nghìn.
          Trong thủ tục thật, ta dùng cả tuỳ chọn này lẫn khối thử và bắt lỗi.""", clear=True),
        S("""<div class="box warn"><b>Lỗi 3: ghép chuỗi người dùng gõ vào câu lệnh động.</b> Người dùng gõ <code>X' OR '1'='1</code>.</div>"""
          + code(MSS_INJ_BAD) + out(MSS_INJ_BAD_OUT),
          """Lỗi thứ ba là ghép chuỗi người dùng gõ vào một câu lệnh động, tức câu lệnh được ghép thành chuỗi lúc chạy rồi mới đưa máy thực thi. Người dùng gõ chữ X, một dấu nháy, rồi thêm điều kiện một bằng một luôn đúng.
          Sau khi ghép, điều kiện tìm theo tên luôn đúng, nên máy trả về cả hai tài khoản. Thủ tục lưu trữ không tự chống được kiểu chèn mã này.""", clear=True),
        S(code(MSS_INJ_GOOD) + out(MSS_INJ_GOOD_OUT)
          + """<p class='note'>Truyền chuỗi làm <b>tham số</b> qua <code>sp_executesql</code>: cả chuỗi chỉ là một cái tên. Oracle: biến gắn, <code>EXECUTE IMMEDIATE … USING</code>.</p>""",
          """Cách chữa là truyền chuỗi đó làm tham số, qua thủ tục hệ thống chạy câu lệnh động có tham số. Cả chuỗi chỉ được coi là một cái tên, không ai tên như vậy, nên không có dòng nào.
          Trên Oracle cũng vậy, câu lệnh động nhận giá trị qua biến gắn, tức một chỗ giữ chỗ có tên mà giá trị được truyền riêng, không ghép chuỗi.""", clear=True),
    ], checks=[f"alg.bnx_l06_total(alg.bnx_l06_swallow({B0}, [(2, 500000), (1, -500000)], 'none')) == 1300000",
               f"alg.bnx_l06_total(alg.bnx_l06_swallow({B0}, [(2, 500000), (1, -500000)], 'null')) == 1800000",
               f"alg.bnx_l06_total(alg.bnx_l06_batch({B0}, [(2, 500000), (1, -500000)], False)) == 1800000",
               f"alg.bnx_l06_total(alg.bnx_l06_batch({B0}, [(2, 500000), (1, -500000)], True)) == 1300000",
               "alg.bnx_l06_inject_rows(\"X' OR '1'='1\", False) == 2", "alg.bnx_l06_inject_rows(\"X' OR '1'='1\", True) == 0"])

    Q = "{1: 800000, 2: 200000}"
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        S(table(["câu", "đề"],
                [["1", "A = 800 000, B = 200 000. Gọi thủ tục chuyển 900 000 từ A sang B. Người gọi nhận gì, A còn bao nhiêu, tổng bao nhiêu?"],
                 ["2", "Cùng lúc: lệnh P chuyển 100 000 từ A (mã 1) sang B (mã 2), lệnh Q chuyển 50 000 từ B sang A. Mỗi lệnh khoá mã nào trước? Số dư cuối?"],
                 ["3", "Quyết định: đặt logic chuyển tiền trong thủ tục lưu trữ, hay trong dịch vụ Java (mã Java mở giao dịch, gửi từng câu lệnh)?"]]),
          """Đến lượt bạn. Câu một, A có tám trăm nghìn, B có hai trăm nghìn, gọi thủ tục chuyển chín trăm nghìn từ A sang B. Người gọi nhận gì, A còn bao nhiêu, tổng bao nhiêu?
          Câu hai, cùng lúc lệnh P chuyển một trăm nghìn từ A sang B, lệnh Q chuyển năm mươi nghìn từ B sang A. Mỗi lệnh khoá mã nào trước, và số dư cuối là bao nhiêu?
          Câu ba là một quyết định. Đặt logic chuyển tiền trong thủ tục lưu trữ, hay trong dịch vụ Java? Hãy dừng video và làm ra giấy.""",
          pause=25),
        S("""<p>Câu 1: $800\\,000 < 900\\,000$ nên thủ tục báo lỗi −20001 và hoàn tác.</p>
$$800\\,000 + 200\\,000 = \\hlg{1\\,000\\,000}\\ \\text{(A vẫn 800 000)}$$""",
          """Đáp án câu một. Tám trăm nghìn nhỏ hơn chín trăm nghìn, nên người gọi nhận lỗi âm hai mươi nghìn lẻ một, và giao dịch được hoàn tác.
          A vẫn tám trăm nghìn, tổng vẫn tám trăm nghìn cộng hai trăm nghìn, bằng một triệu."""),
        S("""<p>Câu 2: cả P và Q đều khoá mã 1 rồi mã 2, nên lệnh sau chờ lệnh trước, không bế tắc.</p>
$$A = 800\\,000 - 100\\,000 + 50\\,000 = \\hl{750\\,000}$$
$$B = 200\\,000 + 100\\,000 - 50\\,000 = \\hl{250\\,000}$$""",
          """Đáp án câu hai. Cả hai lệnh đều khoá mã một trước rồi mới tới mã hai, nên lệnh đến sau chỉ chờ lệnh đến trước, không có bế tắc.
          A bằng tám trăm nghìn trừ một trăm nghìn cộng năm mươi nghìn, là bảy trăm năm mươi nghìn.
          B bằng hai trăm nghìn cộng một trăm nghìn trừ năm mươi nghìn, là hai trăm năm mươi nghìn, và tổng vẫn một triệu."""),
        S(table(["lựa chọn", "được", "mất"],
                [["thủ tục lưu trữ", "một lần gọi qua mạng; khoá giữ ngắn vì mọi câu chạy ngay trong cơ sở dữ liệu", "mỗi hệ một ngôn ngữ (bài này viết hai lần); khó kiểm thử, khó quản lý phiên bản cùng mã ứng dụng"],
                 ["dịch vụ Java", "một ngôn ngữ, kiểm thử và triển khai như mã thường", "nhiều lượt đi về qua mạng trong lúc đang giữ khoá; phải cấu hình đúng việc hoàn tác khi lỗi"]]),
          """Đáp án câu ba, không có lựa chọn đúng cho mọi nơi. Thủ tục lưu trữ chỉ cần một lần gọi qua mạng, và khoá được giữ ngắn vì mọi câu chạy ngay trong cơ sở dữ liệu.
          Đổi lại, mỗi hệ một ngôn ngữ, như bài này phải viết hai lần, và khó kiểm thử cũng như quản lý phiên bản cùng mã ứng dụng.
          Dịch vụ Java dùng một ngôn ngữ, kiểm thử như mã thường, nhưng mỗi câu lệnh là một lượt đi về qua mạng trong lúc giữ khoá, và phải cấu hình đúng việc hoàn tác khi lỗi."""),
    ], checks=[f"alg.bnx_l06_transfer({Q}, 1, 2, 900000) == (False, {Q})",
               f"alg.bnx_l06_total({Q}) == 1000000",
               "alg.bnx_l06_lock_order(1, 2) == alg.bnx_l06_lock_order(2, 1) == (1, 2)",
               f"alg.bnx_l06_transfer(alg.bnx_l06_transfer({Q}, 1, 2, 100000)[1], 2, 1, 50000)[1] == {{1: 750000, 2: 250000}}",
               f"alg.bnx_l06_transfer(alg.bnx_l06_transfer({Q}, 2, 1, 50000)[1], 1, 2, 100000)[1] == {{1: 750000, 2: 250000}}"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        S(chain("tham số vào, ra", "khoá theo mã tăng dần", "kiểm rồi mới ghi", "lỗi thì hoàn tác và báo lên", "tổng giữ nguyên"),
          """Tổng kết chuỗi logic. Thủ tục nhận tham số vào và trả tham số ra. Nó khoá hai tài khoản theo mã tăng dần, kiểm số dư rồi mới ghi.
          Có lỗi thì hoàn tác cả giao dịch và báo lên người gọi, nhờ vậy tổng tiền luôn giữ nguyên."""),
        S("""<div class='box key'><b>Tư duy:</b> đừng tin “lỗi thì tự hoàn tác”. Hãy chạy thử một lỗi ở <b>giữa</b> giao dịch và đo tổng tiền trước và sau, trên đúng hệ bạn dùng.</div>""",
          """Điều cần mang theo. Đừng tin rằng có lỗi thì hệ thống tự hoàn tác. Hãy chạy thử một lỗi ở giữa giao dịch và đo tổng tiền trước và sau, trên đúng hệ bạn dùng."""),
        S("""<p class="note">Bài sau: Oracle cho khối lượng lớn, chia bảng giao dịch theo tháng, lưu dữ liệu JSON, hàng đợi ngay trong cơ sở dữ liệu.</p>""",
          """Ở bài sau, ta xem Oracle xử lý bảng giao dịch rất lớn ra sao, chia bảng theo tháng để chỉ đọc phần cần, và gửi thông điệp qua hàng đợi nằm ngay trong cơ sở dữ liệu.""",
          forward_ref=True),
    ])
    return lesson("L06", "thu_tuc_luu_tru_plsql_tsql",
                  "Bài 6 — Thủ tục lưu trữ trên Oracle và SQL Server: tham số, giao dịch và bắt lỗi",
                  "curriculum/bnx.yaml L06; audit/bnx/verify_bnx.py L06; Oracle Database PL/SQL Language Reference 23 (RAISE_APPLICATION_ERROR, unhandled exceptions) "
                  "và Concepts (statement-level rollback, row locks, deadlocks); Microsoft Learn: SET XACT_ABORT, TRY...CATCH, THROW, sp_executesql, LEAST/GREATEST; "
                  "Java SE 21 API java.sql.CallableStatement (đọc 2026-11-11)",
                  ["Viết thủ tục chuyển tiền có tham số vào và ra bằng PL/SQL và T-SQL", "Hoàn tác khi lỗi bằng khối bắt lỗi của mỗi hệ",
                   "Khoá hai tài khoản theo một thứ tự cố định", "Gọi thủ tục từ Java bằng JDBC"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
