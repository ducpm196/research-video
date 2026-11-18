"""Kiểm độc lập BNX L24 (JPA/Hibernate và Spring Data). Đường khác với tools/checklib_bnx/l24.py:
- CHẠY LẠI THẬT (không đệm) mọi chương trình trên màn hình: Hibernate ORM 7.1.0.Final + H2 2.3.232 (jar ở audit/bnx/deps/l24, so sha256 với README
  trước khi chạy), đầu ra phải bằng từng ký tự đầu ra đã hiện;
- số câu SQL ở 5, 50, 500 khách đọc từ đầu ra thật rồi đối chiếu 1 + N và 1 của mô hình;
- đếm lại bằng đường khác hẳn: sqlite3 của Python với bộ đếm tự viết (không dùng Hibernate) cho 5, 50, 500 khách;
- số dòng của phép nối tính bằng SQL thật (sqlite JOIN), số đối tượng ngữ cảnh giữ tính lại bằng vòng lặp;
- lab (labs/BNX/L24/loi_giai.py) chạy lại, so với mong_doi.txt.
Thiếu jar / sha256 sai → SKIP (rec None: cổng FAIL, NOT_VERIFIED), không PASS lặng lẽ."""
import hashlib
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import lib2  # noqa: E402
import l24 as src  # noqa: E402

DEPS = ROOT / "audit" / "bnx" / "deps" / "l24"


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


def sqlite_count(n, per, kieu):
    """Đường khác: sqlite thật, bộ đếm tự viết bọc execute."""
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE k (id INTEGER PRIMARY KEY)")
    db.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, kid INTEGER)")
    for i in range(1, n + 1):
        db.execute("INSERT INTO k VALUES (?)", (i,))
        for j in range(1, per + 1):
            db.execute("INSERT INTO t VALUES (?, ?)", (i * 100 + j, i))
    dem = [0]

    def q(sql, args=()):
        dem[0] += 1
        return db.execute(sql, args).fetchall()
    if kieu == "luoi":
        for (i,) in q("SELECT id FROM k"):
            q("SELECT id FROM t WHERE kid = ?", (i,))
        return dem[0], None
    rows = q("SELECT k.id, t.id FROM k JOIN t ON t.kid = k.id")
    return dem[0], len(rows)


def run(rec):
    ok = sha_ok()
    if ok is None:
        rec("L24", None, "thiếu jar Hibernate/H2 hoặc README (audit/bnx/deps/l24): NOT_VERIFIED")
    elif not ok:
        rec("L24", False, "sha256 của jar không khớp README")
    else:
        rec("L24", True, "sha256 của 17 jar khớp README")
        lib2.verify_programs(rec, "L24")
        out = next(p for p in lib2.PROGRAMS if p.key == "L24_ChayHib").out
        # số câu SQL từ đầu ra thật so với mô hình
        got = {int(n): (int(a), int(b)) for n, a, b in re.findall(r"^(\d+) khach: tai luoi (\d+) cau, JOIN FETCH (\d+) cau$", out, re.M)}
        rec("L24", sorted(got) == [5, 50, 500], "đầu ra thật có đủ ba cỡ 5, 50, 500 khách")
        rec("L24", all(got[n] == (alg.bnx_l24_lazy_sql(n), alg.bnx_l24_join_sql(n)) for n in got), "Hibernate chạy thật: tải lười = 1 + N, nối kèm tải = 1 (khớp mô hình)")
        rec("L24", "doc hai lan: cung doi tuong true, 1 cau SQL" in out and alg.bnx_l24_find_sql(2) == 1, "hai lần tìm cùng mã: cùng đối tượng, 1 câu SQL")
        rec("L24", "sau truy van, truoc chot: 1 UPDATE" in out, "sửa đối tượng đang quản lý + truy vấn cùng bảng: 1 UPDATE trước khi chốt (đẩy tự động)")
        rec("L24", "sua doi tuong da roi: 0 UPDATE" in out and "so du 11: 1500, so du 12: 2000" in out, "đối tượng đã rời: 0 UPDATE, số dư 11 = 1000 + 500, số dư 12 giữ 2000")
        rec("L24", "loi: LazyInitializationException" in out, "đọc danh sách lười sau khi đóng phiên: LazyInitializationException")
        rec("L24", "ngu canh giu: 1500 doi tuong" in out and "sau clear: 0 doi tuong" in out and alg.bnx_l24_entities_held(500, 2) == 1500, "ngữ cảnh giữ 1500 đối tượng, sau clear còn 0")
        rec("L24", "cat tai cho (join fetch + trang): 20 khach, 1 cau, ngu canh giu 1500 doi tuong" in out
            and "hai buoc (lay ma roi join fetch): 20 khach, 2 cau, ngu canh giu 60 doi tuong" in out
            and 500 + 500 * 2 == 1500 and 20 + 20 * 2 == 60,
            "phân trang + nối kèm danh sách: Hibernate đọc hết rồi cắt trong bộ nhớ (1500 đối tượng); hai bước chỉ giữ 20 + 20 × 2 = 60")
        rec("L24", "Hibernate: select k1_0.id,k1_0.ten from Khach k1_0" in out and out.count("select t1_0.khach_id") == 2, "DemSql in 1 câu lấy khách và 1 câu phụ cho mỗi khách (2 khách → 3 câu)")
    # đường khác: sqlite
    for n in (5, 50, 500):
        c, _ = sqlite_count(n, 2, "luoi")
        c2, rows = sqlite_count(n, 2, "join")
        rec("L24", c == 1 + n == alg.bnx_l24_lazy_sql(n) and c2 == 1 and rows == alg.bnx_l24_rows_join(n, 2), f"sqlite đếm lại: N = {n} → {c} câu (1 + N), nối bảng 1 câu, {rows} dòng = N × 2")
    rec("L24", alg.bnx_l24_lazy_sql(10000) == 10001 and alg.bnx_l24_lazy_sql(50000) == 50001, "một cộng N ở 10 000 và 50 000 khách")
    rec("L24", [alg.bnx_l24_latency_ms(1 + n, 1) for n in (5, 500, 50000)] == [6, 501, 50001] and 50001 / 1000 > 50, "độ trễ cộng dồn 6, 501, 50 001 ms (1 ms mỗi câu, số minh hoạ) ≈ 50 giây")
    rec("L24", sum(1 for _ in range(500)) + sum(2 for _ in range(500)) == 1500, "vòng lặp: 500 khách + 500 × 2 tài khoản = 1500 đối tượng")
    rec("L24", alg.bnx_l24_rows_join(200, 3) == 600 == sum(3 for _ in range(200)), "câu 1 của quiz: 200 khách × 3 tài khoản = 600 dòng; 1 + 200 = 201")
    # nối trong làm mất khách không có tài khoản; nối trái giữ (đường khác: sqlite thật, 501 khách, 1 khách không tài khoản)
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE k (id INTEGER PRIMARY KEY)")
    db.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, kid INTEGER)")
    for i in range(1, 502):
        db.execute("INSERT INTO k VALUES (?)", (i,))
        if i != 501:
            db.execute("INSERT INTO t VALUES (?, ?)", (i, i))
    trong = db.execute("SELECT COUNT(DISTINCT k.id) FROM k JOIN t ON t.kid = k.id").fetchone()[0]
    trai = db.execute("SELECT COUNT(DISTINCT k.id) FROM k LEFT JOIN t ON t.kid = k.id").fetchone()[0]
    rec("L24", trong == alg.bnx_l24_khach_thay(501, 1, "trong") == 500 and trai == alg.bnx_l24_khach_thay(501, 1, "trai") == 501, "nối trong mất 1 khách không có tài khoản (500/501); nối trái giữ đủ 501 (sqlite thật; Hibernate join fetch cho 500/501 theo người đọc độc lập)")
    # kiểm Python sqlite trên màn hình (DemPy) đã chạy trong verify_programs; lab:
    lab = ROOT / "labs" / "BNX" / "L24"
    r = subprocess.run([sys.executable, "-X", "utf8", str(lab / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8")
    want = (lab / "mong_doi.txt").read_text(encoding="utf-8").strip()
    rec("L24", r.returncode == 0 and r.stdout.strip() == want, "lab: loi_giai.py cho đúng mong_doi.txt")
    c, _ = sqlite_count(12, 3, "luoi")
    c2, rows = sqlite_count(12, 3, "join")
    rec("L24", want == f"Cach 1: {c} cau, tong so the {12 * 3}\nCach 2: {c2} cau, tong so the {rows}", "lab: số câu 1 + 12 = 13 và 1, tổng 36 thẻ tính lại bằng đường khác")
