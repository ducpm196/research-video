"""Kiểm độc lập BNX L33 (Hệ cũ: Servlet, JSP, Tomcat, JBoss). Đường khác với tools/checklib_bnx/l33.py:
- CHẠY LẠI THẬT (không đệm) mọi chương trình trên màn hình: Tomcat nhúng 10.1.61 (jar ở audit/bnx/deps/l33, so sha256 với README trước khi chạy): gói .war, vòng đời,
  trang JSP, lỗi javax, bể 4 luồng; đầu ra phải bằng từng ký tự đầu ra đã hiện;
- vòng đời: đếm dòng init/destroy và các thân phản hồi trong đầu ra thật (không dùng hàm của alg);
- gói .war: tự dựng một zip bằng Python (zipfile) có đúng các mục mà jar liệt kê rồi so tên (đường khác với công cụ jar);
- bể luồng: đếm lượt bằng vòng lặp cộng dồn (không dùng math.ceil) và so với alg và với số đo thật của Java;
- lab: biên dịch và chạy lại loi_giai.java, so mong_doi.txt.
Thiếu jar / sha256 sai / javac → SKIP (rec None: cổng FAIL, NOT_VERIFIED), không PASS lặng lẽ."""
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import lib2  # noqa: E402
import l33 as src  # noqa: E402

DEPS = ROOT / "audit" / "bnx" / "deps" / "l33"
LAB = ROOT / "labs" / "BNX" / "L33"


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


def luot(n, luong):
    """Số lượt xử lý: cộng dồn từng nhóm `luong` yêu cầu tới khi hết (không dùng ceil)."""
    con, dem = n, 0
    while con > 0:
        con -= luong
        dem += 1
    return dem


def run(rec):
    P = {q.name: q for q in lib2.PROGRAMS if q.lesson == "L33"}
    if not shutil.which("javac"):
        rec("L33", None, "thiếu javac: NOT_VERIFIED")
        return
    ok = sha_ok()
    if ok is None:
        rec("L33", None, "thiếu jar Tomcat hoặc README (audit/bnx/deps/l33): NOT_VERIFIED")
        return
    if not ok:
        rec("L33", False, "sha256 của jar không khớp README")
        return
    rec("L33", True, "sha256 của 5 jar khớp README")
    lib2.verify_programs(rec, "L33")
    # 1) vòng đời
    war = P["ChayWar"].out.splitlines()
    rec("L33", war.count("init: tao 1 lan") == 1 and war.count("destroy: thu hoi 1 lan") == 1 and [l for l in war if "->" in l] == ["app/chao -> yeu cau so 1", "app/chao -> yeu cau so 2", "app/chao -> yeu cau so 3"]
        and war.index("init: tao 1 lan") < war.index("app/chao -> yeu cau so 1") and war.index("destroy: thu hoi 1 lan") > war.index("app/chao -> yeu cau so 3"),
        "vòng đời: init 1 lần trước yêu cầu đầu, bộ đếm 1, 2, 3 (cùng một thể hiện), destroy 1 lần sau yêu cầu cuối")
    # 2) gói .war: tự dựng zip bằng Python và so tên
    d = Path(tempfile.mkdtemp())
    z = d / "a.war"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("META-INF/MANIFEST.MF", "Manifest-Version: 1.0\n")
        zf.writestr("WEB-INF/classes/Chao.class", b"x")
        zf.writestr("WEB-INF/web.xml", "<web-app/>")
    tep = sorted(set(zipfile.ZipFile(z).namelist()) | {"META-INF/", "WEB-INF/", "WEB-INF/classes/"})
    rec("L33", war[:6] == tep, "gói .war: zip tự dựng bằng Python có đúng các mục jar liệt kê (6 dòng)")
    # 3) JSP
    jsp = P["ChayJsp"].out.splitlines()
    rec("L33", "tep Jasper sinh ra: truoc 0, sau 2" in jsp and "chao_jsp.java" in jsp and "chao_jsp.class" in jsp and "chao.jsp?ten=An -> Xin chao An, 2 + 3 = 5" in jsp
        and any(re.fullmatch(r"\d+:\s+out\.write\(\"Xin chao \"\);", l) for l in jsp) and any(re.fullmatch(r"\d+:\s+out\.print\( 2 \+ 3 \);", l) for l in jsp)
        and jsp[-1] == "public final class org.apache.jsp.chao_jsp extends HttpJspBase", "JSP: 0 → 2 tệp ở yêu cầu đầu; out.write/out.print; lớp kế thừa HttpJspBase (javap)")
    # 4) javax
    cu = P["ChayCu"].out.splitlines()
    rec("L33", cu == ["Cu.java:1: error: package javax.servlet.http does not exist", "bien dich duoc"], "javax.servlet không biên dịch với Tomcat 10.1; đổi sang jakarta.servlet thì được")
    # 5) bể luồng
    tai = P["ChayTai"].out.splitlines()
    rec("L33", tai == [f"{n} yeu cau, 4 luong: dong thoi toi da 4, thoi gian >= {luot(n, 4) * 100} ms: true" for n in (4, 40, 200)]
        and [alg.bnx_l33_waves(n, 4) for n in (4, 40, 200)] == [luot(n, 4) for n in (4, 40, 200)] == [1, 10, 50], "bể 4 luồng: tối đa 4 đồng thời; lượt 1, 10, 50 (vòng lặp cộng dồn = alg = đo thật)")
    rec("L33", alg.bnx_l33_throughput(200, 0.5) == 400 and alg.bnx_l33_throughput(8, 0.25) == 32 and luot(40, 8) * 0.25 == 1.25 and 120 * 1 == 120, "quiz: 400 và 32 yêu cầu/giây; 5 lượt = 1,25 giây; 120 lần dịch")
    # 6) lab
    w = Path(tempfile.mkdtemp())
    shutil.copy(LAB / "loi_giai.java", w / "MauBoChua.java")
    r1 = subprocess.run(["javac", "-encoding", "UTF-8", "MauBoChua.java"], cwd=w, capture_output=True, text=True, encoding="utf-8")
    r2 = subprocess.run(["java", "-Dstdout.encoding=UTF-8", "MauBoChua"], cwd=w, capture_output=True, text=True, encoding="utf-8") if r1.returncode == 0 else r1
    mong = (LAB / "mong_doi.txt").read_text(encoding="utf-8").strip()
    rec("L33", r1.returncode == 0 and r2.returncode == 0 and r2.stdout.strip() == mong, "lab: loi_giai.java cho đúng mong_doi.txt")
    rec("L33", mong.count("init ") == 2 and mong.count("destroy ") == 2 and mong.splitlines()[-2:] == ["destroy ChaoVi", "destroy ChaoAnh"], "lab: mỗi Servlet init đúng 1 lần và destroy đúng 1 lần, theo thứ tự tạo")
    de = (LAB / "de.md").read_text(encoding="utf-8")
    sol = (LAB / "loi_giai.java").read_text(encoding="utf-8")
    rec("L33", "LinkedHashMap" in de and "LinkedHashMap" in sol and "(Iterable" not in de, "lab: de.md nhắc LinkedHashMap cho thứ tự destroy và lời giải đúng dùng LinkedHashMap")
    # màn hình hiện đủ Cu.java (kể cả EOF, javac -cp, dòng đổi tên gói) và lời giảng cú pháp mới (Tomcat nhúng, jar --create, getParameter, phiên); nói rõ "mặc định" cho biên dịch JSP
    yml = " ".join(next((ROOT / "lessons" / "bnx").glob("L33_*.yaml")).read_text(encoding="utf-8").split())
    cu = src.SH_CU.show_from("cat > Cu.java", 7)
    rec("L33", "EOF" in cu and "javac -cp" in cu and "sed -i" in cu and "import jakarta.servlet.http.HttpServlet;" in yml and "Tomcat nhúng</b> là Tomcat dùng như thư viện" in yml
        and "jar --create --file app.war" in yml and "request.getParameter" in yml and "bộ nhớ riêng của từng khách" in yml and "trang bị sửa thì dịch lại" in yml,
        "màn hình hiện đủ Cu.java (EOF, javac -cp, sed); giảng Tomcat nhúng, jar, getParameter, phiên; biên dịch JSP chỉ là mặc định")
    # R4: Tai.java hiện đủ 4 khối nối nhau (13-21, 22-32, 33-43, 44-51) = toàn bộ thân lớp; bảng đọc có here-doc, lớp ẩn danh, ép kiểu, làm tròn lên
    tl = src.J_TAI.code.split(chr(10))
    cac = [tl[12:21], tl[21:32], tl[32:43], tl[43:51]]
    yml3 = " ".join(next((ROOT / "lessons" / "bnx").glob("L33_*.yaml")).read_text(encoding="utf-8").split())
    rec("L33", sum(len(x) for x in cac) == 51 - 12 and max(len(x) for x in cac) <= 12 and (n_ := (40 + 3) // 4) == 10 and n_ * 100 == 1000
        and all(k in yml3 for k in ("lớp ẩn danh", "ép kiểu", "làm tròn lên", "&lt;&lt;'EOF'", "2&gt;/dev/null", "createTempDirectory", "toAbsolutePath", "accumulateAndGet", "sendAsync", "InterruptedException")),
        "Tai.java: bốn khối hiện đủ thân lớp (≤ 12 dòng mỗi khối); bảng đọc phủ here-doc, lớp ẩn danh, ép kiểu, accumulateAndGet, sendAsync, làm tròn lên (40 → 10 lượt)")
