"""Kiểm độc lập BNX L37 — chạy THẬT các hằng mã của audit/bnx/src/l37.py trên SQL Server 2022 (bnx-mss) và qua JDBC tới Oracle (bnx-ora), đọc con số
từ đầu ra bằng biểu thức chính quy, rồi so với alg.bnx_l06_* (tổng tiền) và alg.bnx_l37_rows (chèn mã, mô hình sqlite). Thêm: mặc định XACT_ABORT OFF,
CATCH không ROLLBACK vẫn chốt phần dở, thủ tục THROW 50002 với số tiền âm, quy mô 2/200/20 000 dòng, đáp án quiz chạy thật, phiên bản máy chủ, lab sqlite.
Thiếu Docker → rec(..., None) (SKIP, cổng FAIL); thiếu jar JDBC → nguồn L37_ChayJdbc thoát 97 (SKIP)."""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402
import l37 as L  # noqa: E402

B0 = {1: 300000, 2: 1000000}
MOVE = [(2, 500000), (1, -500000)]
ATK = "X' OR '1'='1"


def _ints(out):
    return [int(x) for x in re.findall(r"^\s*(\d+)\s*$", out, re.M)]


def _bal(out):
    return {m.group(1): int(m.group(2)) for m in re.finditer(r"^([AB])\s+(\d+)\s*$", out, re.M)}


def run(rec):
    try:
        import dbrun
        ok_o, ok_m = dbrun.ready()
    except Exception as ex:  # noqa: BLE001
        rec("L37", None, f"không gọi được Docker: {type(ex).__name__}")
        return
    if not ok_m:
        rec("L37", None, f"container SQL Server chưa chạy: mssql={ok_m}")
        return
    mss = dbrun.mss
    base = L.MSS_BASE + L.MSS_PROC

    # 0. Phiên bản đúng như bài nói
    v = mss("SELECT @@VERSION;")
    rec("L37", "16.0.4315.2" in v and "RTM-CU27" in v and "SQL Server 2022" in v, "SQL Server: @@VERSION là 2022 RTM-CU27-GDR 16.0.4315.2")

    # 1. Thủ tục T-SQL: 500 000 (lỗi) rồi 200 000 (thành công) — cùng kết quả như mô hình alg
    m = mss(base + L.MSS_CALL_500 + "\nGO\n" + L.MSS_CALL_200)
    t = _ints(m)
    ok500, b500 = alg.bnx_l06_transfer(B0, 1, 2, 500000)
    ok200, b200 = alg.bnx_l06_transfer(b500, 1, 2, 200000)
    rec("L37", "Msg 50001" in m and "So du khong du" in m and not ok500, "SQL Server: chuyển 500 000 → THROW 50001 (alg: thất bại)")
    rec("L37", t[:1] == [alg.bnx_l06_total(b500)] == [1300000] and t[-1:] == [alg.bnx_l06_total(b200)] == [1300000],
        f"SQL Server: tổng sau lỗi và sau khi chuyển 200 000 thật {t[:1]}, {t[-1:]} = alg 1 300 000")
    rec("L37", re.search(r"^OK\s*$", m, re.M) is not None and _bal(m) == {"A": b200[1], "B": b200[2]} == {"A": 100000, "B": 1200000},
        f"SQL Server: @status = OK, số dư thật {_bal(m)} = alg A 100 000, B 1 200 000")
    for k, txt in (("MSS_CALL_500_OUT", L.MSS_CALL_500_OUT), ("MSS_CALL_200_OUT", L.MSS_CALL_200_OUT)):
        want = [x for x in txt.strip("\n").split("\n") if x.strip()]
        got = [l.strip() for l in m.split("\n")]
        pos, ok = 0, True
        for w in want:
            wl = w.split("…")[0].strip()
            while pos < len(got) and not (got[pos].startswith(wl) if "…" in w else got[pos] == w.strip() or re.sub(r"\s+", " ", got[pos]) == w):
                pos += 1
            if pos == len(got):
                ok = False
                break
            pos += 1
        rec("L37", ok, f"đầu ra thật khớp từng dòng khối {k} đang hiện (… là đoạn lược)")
    m = mss(base + "DECLARE @st VARCHAR(20);\nEXEC dbo.chuyen_tien 1, 2, -100000, @st OUTPUT;\nGO\nSELECT SUM(so_du) FROM dbo.tk;")
    rec("L37", "Msg 50002" in m and _ints(m)[-1:] == [1300000] and alg.bnx_l06_transfer(B0, 1, 2, -100000)[0] is False,
        "SQL Server: chuyển −100 000 → THROW 50002, tổng 1 300 000 (alg: thất bại)")

    # 2. XACT_ABORT: mặc định OFF; OFF → 1 800 000, ON → 1 300 000 (như alg.bnx_l06_batch); CATCH không ROLLBACK vẫn chốt phần dở
    x = mss("SELECT CASE WHEN (@@OPTIONS & 16384) = 16384 THEN 'xact_on' ELSE 'xact_off' END;")
    rec("L37", "xact_off" in x, "SQL Server: phiên mới có XACT_ABORT OFF (bit 16384 của @@OPTIONS)")
    m1, m2 = mss(L.MSS_BASE + L.MSS_PARTIAL), mss(L.MSS_BASE + L.MSS_FIXED)
    rec("L37", "Msg 547" in m1 and "The statement has been terminated." in m1 and _ints(m1)[-1:] == [alg.bnx_l06_total(alg.bnx_l06_batch(B0, MOVE, False))] == [1800000],
        f"SQL Server: XACT_ABORT OFF → Msg 547, tổng thật {_ints(m1)[-1:]} = alg 1 800 000")
    rec("L37", "Msg 547" in m2 and "The statement has been terminated." not in m2 and _ints(m2)[-1:] == [alg.bnx_l06_total(alg.bnx_l06_batch(B0, MOVE, True))] == [1300000],
        f"SQL Server: XACT_ABORT ON → Msg 547, tổng thật {_ints(m2)[-1:]} = alg 1 300 000")
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
    m = mss(L.MSS_BASE + catch)
    rec("L37", "bat loi" in m and _ints(m)[-1:] == [1800000], "SQL Server: CATCH không ROLLBACK rồi chốt → tổng 1 800 000 (vì thế hình ghi “CATCH có ROLLBACK”)")

    # 3. Chèn mã trên bảng dbo.tk (hai tài khoản): ghép chuỗi lộ 2, tham số 0 — khớp mô hình sqlite
    i1, i2 = mss(L.MSS_BASE + L.MSS_INJ_BAD), mss(L.MSS_BASE + L.MSS_INJ_GOOD)
    n1, n2 = len(re.findall(r"^[AB] \d+$", i1, re.M)), len(re.findall(r"^[AB] \d+$", i2, re.M))
    rec("L37", n1 == alg.bnx_l06_inject_rows(ATK, False) == 2, f"SQL Server: ghép chuỗi trả {n1} dòng = mô hình sqlite 2")
    rec("L37", n2 == alg.bnx_l06_inject_rows(ATK, True) == 0 and "(0 rows affected)" in i2, f"SQL Server: sp_executesql có tham số trả {n2} dòng = 0")

    # 4. Quy mô: bảng 2 / 200 / 20 000 dòng; dòng lộ ra khớp alg.bnx_l37_rows và đầu ra đang hiện
    sc = mss(L.MSS_BASE + L.MSS_SCALE)
    got = [(a, int(b)) for a, b in re.findall(r"^(ghep|tham so) (\d+)$", sc, re.M)]
    want = [(c, alg.bnx_l37_rows(n, ATK, c == "tham so")) for n in (2, 200, 20000) for c in ("ghep", "tham so")]
    shown = [(a, int(b)) for a, b in re.findall(r"^(ghep|tham so) (\d+)$", L.MSS_SCALE_OUT, re.M)]
    rec("L37", got == want == shown == [("ghep", 2), ("tham so", 0), ("ghep", 200), ("tham so", 0), ("ghep", 20000), ("tham so", 0)],
        f"SQL Server: quy mô 2/200/20 000 dòng thật {got} = mô hình sqlite = đầu ra đang hiện")

    # 5. Đáp án quiz chạy thật: câu 1 (A 800 000, B 200 000; cộng B 900 000, trừ A 900 000 lỗi) và câu 2 (500 dòng)
    q = "UPDATE dbo.tk SET so_du = 800000 WHERE id = 1; UPDATE dbo.tk SET so_du = 200000 WHERE id = 2;\nGO\n"
    body = ("BEGIN TRAN;\nUPDATE dbo.tk SET so_du = so_du + 900000 WHERE id = 2;\nUPDATE dbo.tk SET so_du = so_du - 900000 WHERE id = 1;\nGO\n"
            "IF @@TRANCOUNT > 0 COMMIT;\nSELECT SUM(so_du) FROM dbo.tk;")
    qa = mss(L.MSS_BASE + q + "SET XACT_ABORT OFF;\n" + body)
    qb = mss(L.MSS_BASE + q + "SET XACT_ABORT ON;\n" + body)
    ba, bb = alg.bnx_l06_batch({1: 800000, 2: 200000}, [(2, 900000), (1, -900000)], False), alg.bnx_l06_batch({1: 800000, 2: 200000}, [(2, 900000), (1, -900000)], True)
    rec("L37", _ints(qa)[-1:] == [alg.bnx_l06_total(ba)] == [1900000] and _ints(qb)[-1:] == [alg.bnx_l06_total(bb)] == [1000000],
        f"Quiz câu 1 thật: XACT_ABORT tắt → {_ints(qa)[-1:]}, bật → {_ints(qb)[-1:]} (alg 1 900 000 / 1 000 000)")
    q2 = """SET NOCOUNT ON;
DROP TABLE IF EXISTS dbo.tk_q2;
SELECT TOP (500) 'K' AS ten INTO dbo.tk_q2 FROM sys.all_objects;
DECLARE @ten VARCHAR(50) = 'X'' OR ''1''=''1', @sql NVARCHAR(200);
SET @sql = N'SELECT COUNT(*) FROM dbo.tk_q2 WHERE ten = ''' + @ten + N'''';
EXEC (@sql);
EXEC sp_executesql N'SELECT COUNT(*) FROM dbo.tk_q2 WHERE ten = @p', N'@p VARCHAR(50)', @p = @ten;
DROP TABLE dbo.tk_q2;"""
    q2o = mss(L.MSS_BASE + q2)
    rec("L37", _ints(q2o)[-2:] == [alg.bnx_l37_rows(500, ATK, False), alg.bnx_l37_rows(500, ATK, True)] == [500, 0], f"Quiz câu 2 thật: ghép chuỗi / tham số → {_ints(q2o)[-2:]} = [500, 0]")

    # 6. Java qua JDBC (chạy thật cần ojdbc trong audit/bnx/deps/l37 và container Oracle; nguồn thoát 97 nếu thiếu jar → SKIP)
    import lib2
    lib2.verify_programs(rec, "L37")
    rec("L37", L.SH_JDBC.out == "500000: loi 20001\n200000: OK\nA: 1 dong\nX' OR '1'='1: 0 dong"
        and alg.bnx_l06_transfer(B0, 1, 2, 500000)[0] is False and alg.bnx_l06_transfer(B0, 1, 2, 200000)[0] is True
        and alg.bnx_l37_rows(1, "A", True, "A") == 1 and alg.bnx_l37_rows(1, ATK, True, "A") == 0,
        "đầu ra JDBC: lệnh 500 000 → mã 20001 (alg: thất bại), 200 000 → OK, tên A 1 dòng, chuỗi tấn công 0 dòng (mô hình sqlite)")
    # PreparedStatement: câu truy vấn trong mã Java đang hiện đúng là câu có dấu ? (không ghép chuỗi)
    rec("L37", "WHERE ten = ?" in L.JAVA_TIM.code and "ps.setString(1, ten)" in L.JAVA_TIM.code and "getenv(\"BNX_PASS\")" in L.JAVA_TIM.code
        and "getenv(\"BNX_PASS\")" in L.JAVA_GOI.code and "registerOutParameter(4, Types.VARCHAR)" in L.JAVA_GOI.code and "bnx_pass" not in L.JAVA_GOI.code.split("class Goi")[1],
        "Java: câu lệnh có dấu ?, mật khẩu lấy từ getenv (không có trong mã Goi/Tim), tham số ra được đăng ký")

    # 7. Sổ mã
    import yaml
    reg = yaml.safe_load((ROOT / "audit" / "bnx" / "screen" / "l37.yaml").read_text(encoding="utf-8"))
    srcs = reg.get("sources") or {}
    same = (srcs.get("L37_mss_base", {}).get("code", "").strip("\n") == L.MSS_BASE.strip("\n")
            and srcs.get("L37_mss_proc", {}).get("code", "").strip("\n") == L.MSS_PROC.strip("\n")
            and srcs.get("L37_mss_scale", {}).get("code", "").strip("\n") == L.MSS_SCALE.strip("\n"))
    rec("L37", same, "sổ screen/l37.yaml: nguồn dữ liệu, thủ tục T-SQL và đo quy mô trùng từng ký tự với hằng của src/l37.py")

    # 8. Lab sqlite: lời giải chạy lại = mong_doi = mô hình tính tay
    import sqlite3
    rows = [("An", 500), ("Binh", 700), ("Chi", 900), ("Dung", 100)]
    exp = []
    for i, ten in enumerate(("An", "X' OR '1'='1", "B' OR so_du > 600 --"), 1):
        if ten == "An":
            g, p = 1, 1
        elif ten == "X' OR '1'='1":
            g, p = len(rows), sum(1 for r in rows if r[0] == ten)
        else:
            g, p = sum(1 for r in rows if r[1] > 600), sum(1 for r in rows if r[0] == ten)
        exp.append(f"chuoi {i}: ghep {g} dong, tham so {p} dong")
    lab = ROOT / "labs" / "BNX" / "L37"
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", str(lab / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8")
    rec("L37", r.returncode == 0 and r.stdout.strip() == (lab / "mong_doi.txt").read_text(encoding="utf-8").strip() == "\n".join(exp),
        "lab: lời giải sqlite chạy lại = mong_doi = mô hình tính tay (ghép chuỗi lộ 4 và 2 dòng, tham số 0)")
    sqlite3.connect(":memory:").close()
    # ── vòng fix4: ⑤ rồi ⑥ KHÔNG dựng lại bảng (in 1 800 000) so với có dựng lại (1 300 000); Goi.java hiện đủ khung lớp ──
    cont = mss(L.MSS_BASE + L.MSS_PARTIAL + "\nGO\n" + L.MSS_FIXED)
    rebuilt = mss(L.MSS_BASE + L.MSS_PARTIAL + "\nGO\n" + L.MSS_BASE + L.MSS_FIXED)
    rec("L37", _ints(cont)[-1:] == [1800000] and _ints(rebuilt)[-1:] == [1300000],
        f"MUST ⑥: chạy ⑥ ngay sau ⑤ không dựng lại bảng → {_ints(cont)[-1:]} (1 800 000); dựng lại bảng (khối MSS_BASE hiện ở bài) rồi ⑥ → {_ints(rebuilt)[-1:]} (1 300 000)")
    gl = L.JAVA_GOI.code.split("\n")
    rec("L37", gl[0].startswith("import java.sql") and gl[2] == "public class Goi {" and gl[-1] == "}" and gl[16].startswith("  public static void main"),
        "Goi.java: dòng 1–3 (import, dòng trống, public class Goi {) và 17–26 (main, đóng lớp) cùng hiện: đủ khung lớp")
    txt = next((ROOT / "lessons" / "bnx").glob("L37_*.yaml")).read_text(encoding="utf-8")
    flat = " ".join(txt.split())
    rec("L37", "bài 6" not in flat and "bài sáu" not in flat and "ghép chuỗi chuỗi" not in flat and flat.count("Dựng lại bảng") >= 2, "bài tự đứng: không nhắc 'bài 6/bài sáu', hết 'ghép chuỗi chuỗi', có hai bước dựng lại bảng")
