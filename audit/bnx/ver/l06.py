"""Kiểm độc lập BNX L06 — chạy THẬT các hằng mã của audit/bnx/src/l06.py trên Oracle (bnx-ora) và SQL Server (bnx-mss), đọc con số
từ đầu ra bằng biểu thức chính quy, rồi so với alg.bnx_l06_* (mô hình thuần Python). Thêm: bế tắc thật giữa hai phiên Oracle khi khoá
theo chiều chuyển và không bế tắc khi khoá theo mã tăng dần; khoảng mã của RAISE_APPLICATION_ERROR; mặc định XACT_ABORT; javac mã Java.
Không chạy được Docker → rec(..., None) (SKIP, cổng FAIL)."""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402
import l06 as L  # noqa: E402

B0 = {1: 300000, 2: 1000000}
MOVE = [(2, 500000), (1, -500000)]


def _ints(out):
    """Mọi số nguyên đứng riêng một dòng (cột TONG của sqlplus, kết quả SUM của sqlcmd)."""
    return [int(x) for x in re.findall(r"^\s*(\d+)\s*$", out, re.M)]


def _bal(out):
    return {m.group(1): int(m.group(2)) for m in re.finditer(r"^([AB])\s+(\d+)\s*$", out, re.M)}


def run(rec):
    try:
        import dbrun
        ok_o, ok_m = dbrun.ready()
    except Exception as ex:  # noqa: BLE001
        rec("L06", None, f"không gọi được Docker: {type(ex).__name__}")
        return
    if not ok_o or not ok_m:
        rec("L06", None, f"container chưa chạy: oracle={ok_o}, mssql={ok_m}")
        return
    ora, mss = dbrun.ora, dbrun.mss

    # 1. Oracle: thủ tục biên dịch được, rồi 500 000 (lỗi) và 200 000 (thành công) trong CÙNG một phiên
    o = ora(L.ORA_SETUP + L.ORA_PROC + "SELECT status FROM user_objects WHERE object_name = 'BNX_L06_CHUYEN_TIEN';")
    rec("L06", "VALID" in o and "ORA-" not in o, "Oracle: CREATE OR REPLACE PROCEDURE bnx_l06_chuyen_tien biên dịch VALID")
    o = ora(L.ORA_SETUP + L.ORA_PROC + L.ORA_CALL_500 + L.ORA_CALL_200)
    t = _ints(o)
    ok500, b500 = alg.bnx_l06_transfer(B0, 1, 2, 500000)
    ok200, b200 = alg.bnx_l06_transfer(b500, 1, 2, 200000)
    rec("L06", "ORA-20001: So du khong du" in o and not ok500, "Oracle: chuyển 500 000 từ 300 000 → ORA-20001 (alg: thất bại)")
    rec("L06", t[:1] == [alg.bnx_l06_total(b500)] == [1300000], f"Oracle: sau lỗi tổng thật {t[:1]} = alg 1 300 000 (đã hoàn tác)")
    rec("L06", "trang thai: OK" in o and ok200, "Oracle: chuyển 200 000 → p_status = OK (alg: thành công)")
    rec("L06", _bal(o) == {"A": b200[1], "B": b200[2]} == {"A": 100000, "B": 1200000}, f"Oracle: số dư thật {_bal(o)} = alg A 100 000, B 1 200 000")
    rec("L06", t[-1:] == [alg.bnx_l06_total(b200)] == [1300000], f"Oracle: tổng cuối thật {t[-1:]} = 1 300 000")
    a = re.search(r'line (\d+)\nORA-06512: at "BNX.BNX_L06_CHUYEN_TIEN", line (\d+)', o)
    lines = L.ORA_PROC.strip("\n").split("\n")
    rec("L06", bool(a) and lines[int(a.group(1)) - 1].strip() == "RAISE;" and "RAISE_APPLICATION_ERROR" in lines[int(a.group(2)) - 1],
        "Oracle: ORA-06512 chỉ đúng dòng RAISE; và dòng RAISE_APPLICATION_ERROR của thủ tục đang hiện")

    # 1b. Oracle: số tiền âm bị chặn (−20002), số dư giữ nguyên; lệnh chốt/hoàn tác trong thủ tục tác động cả giao dịch của người gọi
    neg = """DECLARE v VARCHAR2(20); BEGIN bnx_l06_chuyen_tien(1, 2, -100000, v); END;
/
SELECT so_du FROM bnx_l06_tk ORDER BY id;"""
    o = ora(L.ORA_SETUP + L.ORA_PROC + neg)
    rec("L06", "ORA-20002" in o and _ints(o)[-2:] == [300000, 1000000] and alg.bnx_l06_transfer(B0, 1, 2, -100000) == (False, B0),
        f"Oracle: chuyển −100 000 → ORA-20002, số dư thật {_ints(o)[-2:]} không đổi (alg: thất bại)")
    ct = """DROP TABLE IF EXISTS bnx_l06_log;
CREATE TABLE bnx_l06_log (ghi VARCHAR2(20));
INSERT INTO bnx_l06_log VALUES ('chua chot 1');
DECLARE v VARCHAR2(20); BEGIN bnx_l06_chuyen_tien(1, 2, 500000, v); END;
/
SELECT COUNT(*) FROM bnx_l06_log;
INSERT INTO bnx_l06_log VALUES ('chua chot 2');
DECLARE v VARCHAR2(20); BEGIN bnx_l06_chuyen_tien(1, 2, 200000, v); END;
/
ROLLBACK;
SELECT COUNT(*) FROM bnx_l06_log;
DROP TABLE bnx_l06_log;"""
    o = ora(L.ORA_SETUP + L.ORA_PROC + ct)
    rec("L06", _ints(o)[-2:] == [0, 1], f"Oracle: dòng người gọi chưa chốt mất khi thủ tục hoàn tác, còn lại khi thủ tục đã chốt dù người gọi hoàn tác {_ints(o)[-2:]} = [0, 1]")

    # 2. Oracle: không bắt lỗi → hoàn tác cả lời gọi; nuốt lỗi → tiền lệch
    o1, o2 = ora(L.ORA_SETUP + L.ORA_NOHANDLER), ora(L.ORA_SETUP + L.ORA_SWALLOW)
    rec("L06", "ORA-02290" in o1 and _ints(o1)[-1:] == [alg.bnx_l06_total(alg.bnx_l06_swallow(B0, MOVE, "none"))] == [1300000],
        f"Oracle: khối không bắt lỗi → ORA-02290, tổng thật {_ints(o1)[-1:]} = alg 1 300 000")
    rec("L06", "ORA-" not in o2 and _ints(o2)[-1:] == [alg.bnx_l06_total(alg.bnx_l06_swallow(B0, MOVE, "null"))] == [1800000],
        f"Oracle: WHEN OTHERS THEN NULL → không báo lỗi, tổng thật {_ints(o2)[-1:]} = alg 1 800 000")

    # 3. Oracle: khoảng mã của RAISE_APPLICATION_ERROR (-20000..-20999)
    o = ora("BEGIN RAISE_APPLICATION_ERROR(-20999, 'x'); END;\n/\nBEGIN RAISE_APPLICATION_ERROR(-21000, 'x'); END;\n/")
    rec("L06", "ORA-20999: x" in o and "ORA-21000" in o and "out of range" in o, "Oracle: −20999 dùng được, −21000 bị từ chối (out of range)")

    # 4. Oracle: bế tắc thật khi khoá theo chiều chuyển, không bế tắc khi khoá theo mã tăng dần (hai phiên song song)
    naive = (L.ORA_PROC.replace("bnx_l06_chuyen_tien", "bnx_l06_naive")
             .replace("LEAST(p_from, p_to)", "p_from").replace("GREATEST(p_from, p_to)", "p_to"))
    assert naive != L.ORA_PROC

    def race(proc):
        ora(L.ORA_SETUP + L.ORA_PROC + naive)
        res = {}
        s1 = ("SELECT so_du FROM bnx_l06_tk WHERE id = 1 FOR UPDATE;\nEXEC DBMS_SESSION.SLEEP(3);\n"
              "SELECT so_du FROM bnx_l06_tk WHERE id = 2 FOR UPDATE;\nROLLBACK;\nSELECT 'phien1 xong' FROM dual;")
        s2 = f"EXEC DBMS_SESSION.SLEEP(1);\nDECLARE v VARCHAR2(20); BEGIN {proc}(2, 1, 100000, v); DBMS_OUTPUT.PUT_LINE('phien2 ' || v); END;\n/"
        th = [threading.Thread(target=lambda k=k, q=q: res.__setitem__(k, ora(q))) for k, q in (("s1", s1), ("s2", s2))]
        for x in th:
            x.start()
            time.sleep(0.3)
        for x in th:
            x.join(120)
        return res.get("s1", "") + res.get("s2", "")

    r_naive, r_ord = race("bnx_l06_naive"), race("bnx_l06_chuyen_tien")
    rec("L06", "ORA-00060" in r_naive, "Oracle: hai phiên khoá ngược thứ tự (thủ tục khoá p_from trước) → ORA-00060 thật")
    rec("L06", "ORA-00060" not in r_ord and "phien2 OK" in r_ord and alg.bnx_l06_lock_order(2, 1) == (1, 2),
        "Oracle: thủ tục khoá LEAST trước → phiên 2 chỉ chờ, chạy xong OK, không ORA-00060 (alg: thứ tự (1, 2))")
    ora("DROP PROCEDURE IF EXISTS bnx_l06_naive;")

    # 5. SQL Server: cùng hai lời gọi
    base = L.MSS_DB + L.MSS_SETUP + L.MSS_PROC
    m = mss(base + L.MSS_CALL_500 + "\nGO\n" + L.MSS_CALL_200)
    t = _ints(m)
    rec("L06", "Msg 50001" in m and "So du khong du" in m, "SQL Server: chuyển 500 000 → THROW 50001")
    rec("L06", t[:1] == [1300000] and t[-1:] == [1300000], f"SQL Server: tổng sau lỗi và sau khi chuyển 200 000 thật {t[:1]}, {t[-1:]} = 1 300 000")
    rec("L06", re.search(r"^OK\s*$", m, re.M) is not None and _bal(m) == {"A": b200[1], "B": b200[2]},
        f"SQL Server: @status = OK, số dư thật {_bal(m)} = alg")

    m = mss(base + """DECLARE @st VARCHAR(20);
EXEC dbo.chuyen_tien 1, 2, -100000, @st OUTPUT;
GO
SELECT SUM(so_du) FROM dbo.tk;""")
    rec("L06", "Msg 50002" in m and _ints(m)[-1:] == [1300000], "SQL Server: chuyển −100 000 → THROW 50002, tổng 1 300 000")
    catch = """SET XACT_ABORT OFF;
BEGIN TRAN;
BEGIN TRY
  UPDATE dbo.tk SET so_du = so_du + 500000 WHERE id = 2;
  UPDATE dbo.tk SET so_du = so_du - 500000 WHERE id = 1;
END TRY
BEGIN CATCH
  PRINT 'bat loi';
END CATCH
IF @@TRANCOUNT > 0 COMMIT;
GO
SELECT SUM(so_du) FROM dbo.tk;"""
    m = mss(L.MSS_DB + L.MSS_SETUP + catch)
    rec("L06", "bat loi" in m and _ints(m)[-1:] == [1800000], "SQL Server: CATCH không ROLLBACK rồi chốt → tổng 1 800 000 (vì thế hình ghi “CATCH có ROLLBACK”)")

    # 6. SQL Server: mặc định XACT_ABORT OFF và hệ quả
    m = mss("SELECT CASE WHEN (@@OPTIONS & 16384) = 16384 THEN 'xact_on' ELSE 'xact_off' END;")
    rec("L06", "xact_off" in m, "SQL Server: phiên sqlcmd mới có XACT_ABORT OFF (bit 16384 của @@OPTIONS)")
    m1, m2 = mss(L.MSS_DB + L.MSS_SETUP + L.MSS_PARTIAL), mss(L.MSS_DB + L.MSS_SETUP + L.MSS_FIXED)
    rec("L06", "Msg 547" in m1 and _ints(m1)[-1:] == [alg.bnx_l06_total(alg.bnx_l06_batch(B0, MOVE, False))] == [1800000],
        f"SQL Server: XACT_ABORT OFF → tổng thật {_ints(m1)[-1:]} = alg 1 800 000")
    rec("L06", "Msg 547" in m2 and _ints(m2)[-1:] == [alg.bnx_l06_total(alg.bnx_l06_batch(B0, MOVE, True))] == [1300000],
        f"SQL Server: XACT_ABORT ON → tổng thật {_ints(m2)[-1:]} = alg 1 300 000")

    # 7. SQL Server: chèn mã
    i1, i2 = mss(L.MSS_DB + L.MSS_SETUP + L.MSS_INJ_BAD), mss(L.MSS_DB + L.MSS_SETUP + L.MSS_INJ_GOOD)
    n1 = len(re.findall(r"^[AB] \d+$", i1, re.M))
    n2 = len(re.findall(r"^[AB] \d+$", i2, re.M))
    rec("L06", n1 == alg.bnx_l06_inject_rows("X' OR '1'='1", False) == 2, f"SQL Server: ghép chuỗi trả {n1} dòng = alg (SQLite) 2")
    rec("L06", n2 == alg.bnx_l06_inject_rows("X' OR '1'='1", True) == 0 and "(0 rows affected)" in i2, f"SQL Server: sp_executesql có tham số trả {n2} dòng = 0")

    # 8. Sổ mã: nguồn trong audit/bnx/screen/l06.yaml trùng hằng đang hiện
    import yaml
    reg = yaml.safe_load((ROOT / "audit" / "bnx" / "screen" / "l06.yaml").read_text(encoding="utf-8"))
    srcs = reg.get("sources") or {}
    same = (srcs.get("L06_ora_proc", {}).get("code", "").strip("\n") == L.ORA_PROC.strip("\n")
            and srcs.get("L06_mss_proc", {}).get("code", "").strip("\n") == L.MSS_PROC.strip("\n")
            and srcs.get("L06_mss_base", {}).get("code", "").strip("\n") == (L.MSS_DB + L.MSS_SETUP).strip("\n"))
    rec("L06", same, "sổ screen/l06.yaml: nguồn thủ tục Oracle, T-SQL, dữ liệu SQL Server trùng từng ký tự với hằng của src/l06.py")

    # 9. Java: biên dịch đúng mã đang hiện (chạy cần trình điều khiển ojdbc — NOT_VERIFIED ở cổng, xem báo cáo)
    if not shutil.which("javac"):
        rec("L06", None, "không có javac")
        return
    with tempfile.TemporaryDirectory() as d:
        src = ("import java.sql.*;\npublic class Main {\n  public static void main(String[] args) throws Exception {\n"
               "    String url = \"jdbc:oracle:thin:@//localhost:1521/FREEPDB1\", user = \"bnx\", pass = \"bnx_pass\";\n"
               + L.JAVA_CALL + "\n  }\n}\n")
        pathlib.Path(d, "Main.java").write_text(src, encoding="utf-8")
        r = subprocess.run(["javac", "-encoding", "UTF-8", "-d", d, str(pathlib.Path(d, "Main.java"))], capture_output=True, text=True)
        rec("L06", r.returncode == 0 and "registerOutParameter(4, Types.VARCHAR)" in L.JAVA_CALL and "{call bnx_l06_chuyen_tien(?, ?, ?, ?)}" in L.JAVA_CALL,
            "Java: mã CallableStatement trên màn hình biên dịch được bằng javac (chỉ java.sql của JDK)")
