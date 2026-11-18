"""Kiểm độc lập BNX L25 (Giao dịch Spring và AOP). Đường khác với tools/checklib_bnx/l25.py:
- CHẠY LẠI THẬT (không đệm) chương trình trên màn hình: Spring 7.0.10 + AspectJ weaver + H2 (jar ở audit/bnx/deps/l25, so sha256 với README trước khi chạy),
  đầu ra phải bằng từng ký tự đầu ra đã hiện; phần bể kết nối chạy thêm hai lần nữa để chắc kết quả tất định;
- số dư/nhật ký của bốn ca đọc từ đầu ra thật rồi đối chiếu mô hình alg.bnx_l25_*;
- luật hoàn tác tính lại bằng đường khác: phân cấp lớp ngoại lệ THẬT của Java (reflection: Throwable → RuntimeException/Error/Exception) dựng bằng javac/java;
- bảng quyết định hoàn tác của lab chạy lại và so mong_doi.txt;
Thiếu jar / sha256 sai → SKIP (rec None: cổng FAIL, NOT_VERIFIED), không PASS lặng lẽ."""
import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import lib2  # noqa: E402
import l25 as src  # noqa: E402

DEPS = ROOT / "audit" / "bnx" / "deps" / "l25"

JAVA_HIER = r'''
public class Hier {
  static String kind(Class<?> c) {
    if (Error.class.isAssignableFrom(c)) return "Error";
    if (RuntimeException.class.isAssignableFrom(c)) return "unchecked";
    return "checked";
  }
  public static void main(String[] a) {
    for (Class<?> c : new Class<?>[] {IllegalArgumentException.class, IllegalStateException.class, java.io.IOException.class,
        java.sql.SQLException.class, Exception.class, Error.class, StackOverflowError.class, NullPointerException.class})
      System.out.println(c.getSimpleName() + " " + kind(c));
  }
}
'''


JAVA_UNEXPECTED = r'''
import java.sql.DriverManager;
import org.springframework.jdbc.datasource.*;
import org.springframework.transaction.UnexpectedRollbackException;
import org.springframework.transaction.support.TransactionTemplate;
public class Unexp {
  public static void main(String[] a) throws Exception {
    var ds = new DriverManagerDataSource("jdbc:h2:mem:u;DB_CLOSE_DELAY=-1", "sa", "");
    var tm = new DataSourceTransactionManager(ds);
    var ngoai = new TransactionTemplate(tm);
    var trong = new TransactionTemplate(tm);
    // ca A: hàm NGOÀI bắt lỗi do hàm TRONG (cùng giao dịch, REQUIRED) ném, rồi chốt
    try {
      ngoai.executeWithoutResult(s -> {
        try { trong.executeWithoutResult(t -> { throw new IllegalStateException("x"); }); }
        catch (RuntimeException e) { }
      });
      System.out.println("A: khong loi");
    } catch (UnexpectedRollbackException e) { System.out.println("A: UnexpectedRollbackException"); }
    // ca B: chính hàm TRONG tự bắt lỗi của nó: proxy không thấy lỗi
    try {
      ngoai.executeWithoutResult(s -> {
        trong.executeWithoutResult(t -> {
          try { throw new IllegalStateException("x"); } catch (RuntimeException e) { }
        });
      });
      System.out.println("B: khong loi");
    } catch (UnexpectedRollbackException e) { System.out.println("B: UnexpectedRollbackException"); }
  }
}
'''


def sha_ok():
    readme = DEPS / "README.md"
    if not readme.exists():
        return None
    want = dict(re.findall(r"\| (\S+\.jar) \| ([0-9a-f]{64}) \|", readme.read_text(encoding="utf-8")))
    if not want:
        return None
    for name, h in want.items():
        f = DEPS / name
        if not f.exists():
            return None
        if hashlib.sha256(f.read_bytes()).hexdigest() != h:
            return False
    return True


def run(rec):
    ok = sha_ok()
    if ok is None:
        rec("L25", None, "thiếu jar Spring/AspectJ/H2 hoặc README (audit/bnx/deps/l25): NOT_VERIFIED")
    elif not ok:
        rec("L25", False, "sha256 của jar không khớp README")
    else:
        rec("L25", True, "sha256 của 13 jar khớp README")
        lib2.verify_programs(rec, "L25")
        p = next(q for q in lib2.PROGRAMS if q.key == "L25_ChaySpring")
        out = p.out
        m = {int(n): (int(sd), int(nk)) for n, sd, nk in re.findall(r"^(\d) .*: so du (\d+), nhat ky (\d+)$", out, re.M)}
        rec("L25", m == {1: (1000, 0), 2: (1000, 1), 3: (900, 0), 4: (1000, 0)}, "bốn ca số dư/nhật ký: (1000,0) (1000,1) (900,0) (1000,0)")
        rec("L25", m[1] == (alg.bnx_l25_balance(1000, 100, alg.bnx_l25_rolls_back("IllegalStateException", ())), alg.bnx_l25_log_rows("REQUIRED"))
            and m[2] == (1000, alg.bnx_l25_log_rows("REQUIRES_NEW"))
            and m[3][0] == alg.bnx_l25_balance(1000, 100, alg.bnx_l25_rolls_back("Exception", ()))
            and m[4][0] == alg.bnx_l25_balance(1000, 100, alg.bnx_l25_rolls_back("Exception", ("Exception",))), "bốn ca khớp mô hình luật hoàn tác")
        rec("L25", "ct la proxy: true" in out and "goi qua proxy: giao dich true" in out and "goi noi bo: giao dich false" in out
            and "doan cat chay 1 lan, khong am true" in out, "proxy; qua proxy có giao dịch; tự gọi không giao dịch; đoạn cắt chạy 1 lần (bỏ qua ở tự gọi)")
        rec("L25", "READ_COMMITTED: 1000 -> 1050" in out and "REPEATABLE_READ: 1000 -> 1000" in out and "SERIALIZABLE: 1000 -> 1000" in out
            and alg.bnx_l25_isolation_reread("READ_COMMITTED", 1000, 50) == 1050, "mức cô lập đo bằng JDBC thuần: 1050 / 1000 / 1000")
        pool = {(int(a), int(b)): int(c) for a, b, c in re.findall(r"^(\d+) luong, be (\d+) ket noi: (\d+) luong het gio$", out, re.M)}
        rec("L25", pool == {(3, 3): 3, (3, 4): 0, (6, 6): 6, (6, 7): 0} and all(alg.bnx_l25_timeouts(a, b) == c for (a, b), c in pool.items()),
            "bể kết nối: bể ≤ luồng thì mọi luồng hết giờ, bể = luồng + 1 thì 0 (khớp mô hình)")
        for i in range(2):  # chạy riêng phần bể thêm 2 lần: tất định
            r2 = lib2.Prog("L25", "ChaySpring", p.code, "bash", p.files, "run", p.extra).execute()
            rec("L25", r2[0] == 0 and r2[1].strip("\n") == out, f"chạy lại lần {i + 2}: đầu ra y hệt (tất định, kể cả phần bể)")
    # đường khác: phân cấp lớp ngoại lệ của JDK thật
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
        Path(d, "Hier.java").write_text(JAVA_HIER, encoding="utf-8")
        a = subprocess.run(["javac", "-encoding", "UTF-8", "-d", d, str(Path(d, "Hier.java"))], capture_output=True, text=True)
        b = subprocess.run(["java", "-cp", d, "Hier"], capture_output=True, text=True)
        if a.returncode or b.returncode:
            rec("L25", None, "không chạy được javac/java: NOT_VERIFIED")
        else:
            kinds = dict(l.split() for l in b.stdout.strip().splitlines())
            want = {n: (k != "checked") for n, k in kinds.items()}
            good = all(alg.bnx_l25_rolls_back(n, ()) == w for n, w in want.items())
            rec("L25", good, "phân cấp lớp ngoại lệ của JDK thật (reflection): không kiểm tra và Error ↔ hoàn tác mặc định, khớp mô hình: " + str(kinds))
    if ok:  # Lỗi 4: hàm ngoài bắt lỗi của hàm trong → UnexpectedRollbackException; hàm trong tự nuốt lỗi → không có gì
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
            Path(d, "Unexp.java").write_text(JAVA_UNEXPECTED, encoding="utf-8")
            cp = d + ";" + ";".join(str(j) for j in DEPS.glob("*.jar"))
            a = subprocess.run(["javac", "-encoding", "UTF-8", "-cp", cp, "-d", d, str(Path(d, "Unexp.java"))], capture_output=True, text=True)
            b = subprocess.run(["java", "-cp", cp, "Unexp"], capture_output=True, text=True)
            rec("L25", a.returncode == 0 and b.returncode == 0 and b.stdout.splitlines()[:2] == ["A: UnexpectedRollbackException", "B: khong loi"],
                "Lỗi 4 chạy thật (Spring 7.0.10): hàm ngoài bắt lỗi của hàm trong → UnexpectedRollbackException; hàm trong tự nuốt lỗi → không có ngoại lệ (" + " | ".join(b.stdout.splitlines()) + ")")
    # REPEATABLE_READ chỉ chắc đúng trên H2 (bài nói rõ "trên H2"): đo thật Oracle và SQL Server qua dbrun
    try:
        import threading
        import time
        import dbrun
        ok_o, ok_m = dbrun.ready()
    except Exception as ex:
        rec("L25", None, f"không gọi được dbrun ({type(ex).__name__}): NOT_VERIFIED")
        ok_o = ok_m = False
    if ok_o:
        o = dbrun.ora("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;")
        rec("L25", "ORA-02179" in o, "Oracle thật: SET TRANSACTION ISOLATION LEVEL REPEATABLE READ → ORA-02179 (không có mức này)")
    if ok_m:
        dbrun.mss("IF DB_ID('bnx_l25') IS NOT NULL DROP DATABASE bnx_l25;\nCREATE DATABASE bnx_l25;")
        dbrun.mss("CREATE TABLE tk (id INT, so_du BIGINT); INSERT INTO tk VALUES (1, 1000);", db="bnx_l25")
        kq = {}
        a = threading.Thread(target=lambda: kq.__setitem__("A", dbrun.mss(
            "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;\nBEGIN TRAN;\nSELECT so_du FROM tk;\nWAITFOR DELAY '00:00:04';\nSELECT so_du FROM tk;\nCOMMIT;", db="bnx_l25")))
        a.start()
        time.sleep(2.5)
        kq["B"] = dbrun.mss("SET LOCK_TIMEOUT 500;\nUPDATE tk SET so_du = so_du + 50 WHERE id = 1;", db="bnx_l25")
        a.join()
        dbrun.mss("DROP DATABASE bnx_l25;")
        rec("L25", "Msg 1222" in kq["B"] and kq["A"].split().count("1000") == 2, "SQL Server thật: REPEATABLE READ giữ khoá đọc nên UPDATE của B bị chặn (Msg 1222 khi hết hạn chờ), A đọc lại vẫn 1000")
    rec("L25", [alg.bnx_l25_pool_min(n) for n in (3, 6, 300, 30000, 40)] ==[n + 1 for n in (3, 6, 300, 30000, 40)] == [4, 7, 301, 30001, 41], "bể tối thiểu = luồng + 1: 4, 7, 301, 30 001, 41")
    lab = ROOT / "labs" / "BNX" / "L25"
    r = subprocess.run([sys.executable, "-X", "utf8", str(lab / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8")
    rec("L25", r.returncode == 0 and r.stdout.strip() == (lab / "mong_doi.txt").read_text(encoding="utf-8").strip(), "lab: loi_giai.py cho đúng mong_doi.txt")
    exp = [("IllegalArgumentException", (), True), ("IOException", (), False), ("IOException", ("Exception",), True), ("Error", (), True), (None, (), False)]
    rec("L25", all(alg.bnx_l25_rolls_back(l, k) == w for l, k, w in exp), "lab: năm ca khớp mô hình luật hoàn tác")
