"""Kiểm độc lập BNX L06 (sau khi tách T-SQL/JDBC sang L37) — chạy THẬT các hằng mã của audit/bnx/src/l06.py trên Oracle (bnx-ora), đọc con số
từ đầu ra bằng biểu thức chính quy, rồi so với alg.bnx_l06_* (mô hình thuần Python). Thêm: bế tắc thật giữa hai phiên Oracle khi khoá
theo chiều chuyển và không bế tắc khi khoá theo mã tăng dần; khoảng mã của RAISE_APPLICATION_ERROR; banner phiên bản. SQL Server, XACT_ABORT,
chèn mã, Java: xem audit/bnx/ver/l37.py. Không chạy được Docker → rec(..., None) (SKIP, cổng FAIL)."""
import pathlib
import re
import subprocess
import sys
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
    if not ok_o:
        rec("L06", None, f"container Oracle chưa chạy: oracle={ok_o}")
        return
    ora = dbrun.ora

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

    # 8. Sổ mã: nguồn thủ tục Oracle trong audit/bnx/screen/l06.yaml trùng hằng đang hiện
    import yaml
    reg = yaml.safe_load((ROOT / "audit" / "bnx" / "screen" / "l06.yaml").read_text(encoding="utf-8"))
    srcs = reg.get("sources") or {}
    same = srcs.get("L06_ora_proc", {}).get("code", "").strip("\n") == L.ORA_PROC.strip("\n")
    rec("L06", same, "sổ screen/l06.yaml: nguồn thủ tục Oracle trùng từng ký tự với hằng của src/l06.py")

    # 8b. Phiên bản Oracle đúng như bài nói (Free 23, banner 26ai Free 23.26.3)
    o = ora("SELECT banner FROM v$version WHERE ROWNUM = 1;")
    rec("L06", "26ai Free" in o and "23.26.3" in o, f"Oracle: banner thật chứa '26ai Free' và '23.26.3' ({o.strip().splitlines()[-1][:60] if o.strip() else ''})")

    # 8c. Mô hình Python (cảnh check) trùng đầu ra Oracle: 500 000 bị từ chối, 200 000 → A 100 000, B 1 200 000
    mo = L.PY_MODEL.out.split("\n")
    rec("L06", mo[0] == "500000 loi {1: 300000, 2: 1000000} 1300000" and mo[1] == "200000 OK {1: 100000, 2: 1200000} 1300000"
        and alg.bnx_l06_transfer(B0, 1, 2, 500000)[0] is False, "mô hình Python thuần cho cùng kết quả như Oracle (cảnh check)")

    # ── AF2 (WP4): quy mô và lab (sqlite/Python, không cần Docker) ──
    import lib2
    lib2.verify_programs(rec, "L06")
    import sqlite3

    def count_wrapped(n):
        """Đường khác: bọc hàm execute (không dùng set_trace_callback), chạy n lệnh chuyển theo đúng năm câu."""
        cx = sqlite3.connect(":memory:", isolation_level=None)
        cx.execute("CREATE TABLE tk (id INT, so_du INT)")
        cx.execute("INSERT INTO tk VALUES (1, 99999999), (2, 0)")
        calls = [0]

        def ex(sql):
            calls[0] += 1
            return cx.execute(sql)
        for _ in range(n):
            ex("BEGIN"); ex("SELECT so_du FROM tk WHERE id = 1")
            ex("UPDATE tk SET so_du = so_du - 1 WHERE id = 1"); ex("UPDATE tk SET so_du = so_du + 1 WHERE id = 2"); ex("COMMIT")
        return calls[0], cx.execute("SELECT so_du FROM tk ORDER BY id").fetchall()
    got = [count_wrapped(n) for n in (10, 1000)]
    rec("L06", [g[0] for g in got] == [50, 5000] == [alg.bnx_l06_statements(10), alg.bnx_l06_statements(1000)]
        and got[1][1] == [(99999999 - 1000,), (1000,)], f"đếm bằng hàm bọc: 10 → {got[0][0]}, 1000 → {got[1][0]} câu; số dư đúng sau 1000 lệnh chuyển")
    outp = L.Q6.out.split("\n")
    rec("L06", [int(x.split()[2]) for x in outp] == [50, 5000, 500000] == [alg.bnx_l06_statements(n) for n in (10, 1000, 100000)],
        "đầu ra thật của khối quy mô: 50, 5000, 500000 câu (= 5 × số lệnh chuyển)")
    # lab: mô hình thuần dict (cộng nhận trước, trừ gửi, không âm), so với lời giải chạy thật
    lab = ROOT / "labs" / "BNX" / "L06"
    bal, lines = {1: 500, 2: 400, 3: 300}, []
    for a, b, t in [(1, 2, 300), (2, 3, 900), (3, 1, 50), (1, 3, 250)]:
        nb = dict(bal)
        nb[b] += t
        nb[a] -= t
        if nb[a] < 0:
            lines.append(f"chuyen {a}->{b} {t}: loi so du khong du")
        else:
            bal = nb
            lines.append(f"chuyen {a}->{b} {t}: OK")
    lines.append(f"tong tien: {sum(bal.values())}")
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", str(lab / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8")
    rec("L06", r.returncode == 0 and r.stdout.strip() == (lab / "mong_doi.txt").read_text(encoding="utf-8").strip() == "\n".join(lines) and sum(bal.values()) == 1200,
        "lab: lời giải sqlite chạy lại = mong_doi = mô hình dict (một lệnh bị hoàn tác, tổng 1200 giữ nguyên)")
