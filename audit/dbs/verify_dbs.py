"""Kiểm độc lập mọi khẳng định số của khoá DBS — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
SQL: chạy trên một kết nối sqlite3 riêng (không qua alg.sql). Phụ thuộc hàm: vét cạn mọi tập con thay cho thuật toán lặp.
Tách không mất thông tin: sinh mọi bảng nhỏ thoả phụ thuộc hàm rồi chiếu–nối thật. Chu trình: thuật toán Kahn thay cho DFS.
Chạy: .venv/Scripts/python audit/dbs/verify_dbs.py → PASS/FAIL từng dòng và tổng."""
import itertools
import math
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


def db(extra=""):
    con = sqlite3.connect(":memory:")
    con.executescript(alg.DB_DEMO + extra)
    return con


def q(sql, extra=""):
    con = db(extra)
    try:
        return [tuple(r) for r in con.execute(sql).fetchall()]
    finally:
        con.close()


def err(stmt, extra=""):
    con = db(extra)
    try:
        con.executescript(stmt)
        return None
    except sqlite3.Error as e:
        return str(e)
    finally:
        con.close()


# ── L00–L03: SQL trên kết nối riêng ──
rec("L00a", err("INSERT INTO SinhVien VALUES (5, 'Em', 'K9', 5)") == "FOREIGN KEY constraint failed", "K9 bị từ chối (khoá ngoại)")
rec("L00b", err("INSERT INTO SinhVien VALUES (2, 'Giang', 'K1', 7)").startswith("UNIQUE"), "trùng khoá chính bị từ chối")
rec("L00c", err("DELETE FROM Lop WHERE ma_lop = 'K1'") == "FOREIGN KEY constraint failed" and err("INSERT INTO SinhVien VALUES (6, 'Hà', NULL, 5)") is None,
    "xoá lớp còn tham chiếu bị từ chối; khoá ngoại rỗng được nhận")
rec("L01a", q("SELECT COUNT(*) FROM SinhVien CROSS JOIN Lop") == [(8,)] and q("SELECT COUNT(*) FROM SinhVien JOIN Lop ON lop = ma_lop") == [(3,)], "tích 8, nối 3")
rec("L01b", q("SELECT ten FROM SinhVien JOIN Lop ON lop = ma_lop WHERE ten_lop = 'Khoa học máy tính' AND diem >= 7") == [("An",)], "câu hỏi mở đầu → An")
rec("L02a", q("SELECT ten FROM SinhVien WHERE diem >= 7 ORDER BY ten") == [("An",), ("Chi",), ("Dũng",)], "điểm ≥ 7 → An, Chi, Dũng")
rec("L02b", len(q("SELECT ten FROM SinhVien LEFT JOIN Lop ON lop = ma_lop")) == 4 and len(q("SELECT ten FROM SinhVien LEFT JOIN Lop ON lop = ma_lop WHERE ten_lop = 'Khoa học máy tính'")) == 2,
    "nối ngoài 4 dòng; lọc bảng phải ở WHERE còn 2")
rec("L03a", q("SELECT COUNT(*), COUNT(lop) FROM SinhVien") == [(4, 3)] and q("SELECT COUNT(*) FROM SinhVien WHERE lop = NULL") == [(0,)]
    and q("SELECT COUNT(*) FROM SinhVien WHERE lop IS NULL") == [(1,)], "COUNT 4/3; = NULL 0 dòng; IS NULL 1 dòng")
rec("L03b", q("SELECT ten FROM SinhVien WHERE lop NOT IN ('K1', NULL)") == [], "NOT IN có NULL → 0 dòng")
rec("L03c", q("SELECT lop, AVG(diem) FROM SinhVien GROUP BY lop HAVING AVG(diem) >= 7.5") == [("K2", 9.0)], "HAVING → K2")
rec("L03x", alg.sql("SELECT COUNT(*), COUNT(lop) FROM SinhVien") == q("SELECT COUNT(*), COUNT(lop) FROM SinhVien"), "alg.sql khớp kết nối riêng")


# ── L04–L05: phụ thuộc hàm bằng vét cạn ──
def closure_brute(X, fds, attrs):
    """Bao đóng = hợp mọi Y mà X → Y suy ra được: vét cạn mọi bảng 2 dòng trên miền {0, 1} thoả F (định nghĩa ngữ nghĩa)."""
    attrs = sorted(attrs)
    out = set(attrs)
    for r1 in itertools.product((0, 1), repeat=len(attrs)):
        for r2 in itertools.product((0, 1), repeat=len(attrs)):
            t1, t2 = dict(zip(attrs, r1)), dict(zip(attrs, r2))
            if all(not all(t1[a] == t2[a] for a in L) or all(t1[b] == t2[b] for b in Rr) for L, Rr in fds):
                if all(t1[a] == t2[a] for a in X):
                    out &= {a for a in attrs if t1[a] == t2[a]}
    return out


F1 = [("A", "B"), ("B", "C")]
rec("L04a", closure_brute("A", F1, "ABCD") == {"A", "B", "C"} == alg.attr_closure("A", F1)[0], "A⁺ = ABC (vét cạn bảng 2 dòng = thuật toán lặp)")
keys = [k for n in range(1, 5) for k in itertools.combinations("ABCD", n) if closure_brute(k, F1, "ABCD") == set("ABCD")]
minimal = ["".join(k) for k in keys if not any(set(o) < set(k) for o in keys)]
rec("L04b", minimal == ["AD"] == alg.candidate_keys("ABCD", F1), "khoá duy nhất AD")
G = [("A", "B"), ("BC", "D"), ("D", "E")]
rec("L04c", closure_brute("AC", G, "ABCDE") == set("ABCDE") and closure_brute("A", G, "ABCDE") == {"A", "B"} and alg.candidate_keys("ABCDE", G) == ["AC"], "câu đố: (AC)⁺ = R, A⁺ = AB, khoá AC")


def lossless_by_instances(R1, R2, fds, attrs):
    """Không mất thông tin ⟺ với MỌI bảng thoả F, chiếu rồi nối lại ra đúng bảng. Vét cạn bảng ≤ 3 dòng trên miền {0, 1}."""
    attrs = sorted(attrs)
    rows_all = list(itertools.product((0, 1), repeat=len(attrs)))
    for n in (2, 3):
        for rows in itertools.combinations(rows_all, n):
            ok = all(not all(r[attrs.index(a)] == s[attrs.index(a)] for a in L) or all(r[attrs.index(b)] == s[attrs.index(b)] for b in Rr)
                     for r in rows for s in rows for L, Rr in fds)
            if not ok:
                continue
            j = alg.natural_join(alg.project(rows, list(R1), attrs), list(R1), alg.project(rows, list(R2), attrs), list(R2))
            back = {tuple(t[j[1].index(a)] for a in attrs) for t in j[0]}
            if back != set(rows):
                return False
    return True


rec("L05a", lossless_by_instances("AB", "AC", [("A", "B")], "ABC") and not lossless_by_instances("BA", "BC", [("A", "B")], "ABC"),
    "tách theo A không mất; theo B mất (vét cạn bảng nhỏ)")
rec("L05b", lossless_by_instances("AB", "BC", [("B", "C")], "ABC") and not lossless_by_instances("AC", "BC", [("B", "C")], "ABC"), "câu đố L05")
rec("L05c", alg.bcnf_violations("MTLN", [("M", "TL"), ("L", "N")]) == [("L", "N")] and lossless_by_instances("MTL", "LN", [("M", "TL"), ("L", "N")], "MTLN"),
    "BCNF: ma_lop → ten_lop vi phạm; tách thành SinhVien, Lop không mất")
rows2 = [(1, "K1", "M1"), (2, "K1", "M2")]
j = alg.natural_join(alg.project(rows2, ["lop", "mssv"], ["mssv", "lop", "mon"]), ["lop", "mssv"], alg.project(rows2, ["lop", "mon"], ["mssv", "lop", "mon"]), ["lop", "mon"])
rec("L05d", len(j[0]) == 4, "ví dụ tách sai: 2 dòng thành 4")

# ── L06 ──
S6 = ("CREATE TABLE MonHoc (ma_mon TEXT PRIMARY KEY, ten_mon TEXT NOT NULL); CREATE TABLE DangKy (mssv INTEGER REFERENCES SinhVien(mssv), "
      "ma_mon TEXT REFERENCES MonHoc(ma_mon), diem REAL, PRIMARY KEY (mssv, ma_mon)); INSERT INTO MonHoc VALUES ('M1', 'Cơ sở dữ liệu'), "
      "('M2', 'Mạng máy tính'), ('M10', 'Lý thuyết tính toán'); INSERT INTO DangKy VALUES (1, 'M1', 8), (1, 'M2', 7), (2, 'M1', 6), (3, 'M10', 9);")
rec("L06a", err("INSERT INTO DangKy VALUES (1, 'M1', 5)", S6).startswith("UNIQUE") and err("INSERT INTO DangKy VALUES (1, 'M10', 5)", S6) is None, "khoá ghép DangKy")
con = sqlite3.connect(":memory:")
con.executescript("CREATE TABLE SV_Mon (mssv INTEGER, ds_mon TEXT); INSERT INTO SV_Mon VALUES (1, 'M1,M2'), (2, 'M1'), (3, 'M10');")
rec("L06b", [r[0] for r in con.execute("SELECT mssv FROM SV_Mon WHERE ds_mon LIKE '%M1%'")] == [1, 2, 3], "LIKE '%M1%' bắt nhầm M10")

# ── L07–L10: số học chi phí ──
rec("L07a", 10 ** 6 // 100 == 10000 and 10000 * 8 / 1000 == 80 and 10000 * 0.05 / 1000 == 0.5 and 2 * 10 ** 6 // 50 == 40000, "số trang và thời gian quét")
h = lambda n, f: next(k for k in range(1, 100) if f ** k >= n)  # noqa: E731
rec("L08a", h(10 ** 6, 100) == 3 == alg.bplus_height(10 ** 6, 100) and h(10 ** 6, 200) == 3 and h(10 ** 8, 100) == 4 and h(10 ** 6, 2) == 20, "độ cao cây B+")
leaves = alg.BPT_LEAVES
rec("L08b", [x for l in leaves for x in l] == sorted(x for l in leaves for x in l) and alg.bpt_search(45)[1] == next(i for i, l in enumerate(leaves) if 45 in l),
    "cây mẫu: lá có thứ tự, tra 45 đúng lá")
rec("L08c", len([l for l in leaves if not (l[-1] < 35 or l[0] > 65)]) + 2 == alg.bpt_range(35, 65)[1] == 6, "khoảng 35–65: 6 trang")
con = db("CREATE INDEX idx_lop_diem ON SinhVien(lop, diem);")
plans = [con.execute("EXPLAIN QUERY PLAN " + s).fetchall()[0][3] for s in
         ("SELECT ten FROM SinhVien WHERE lop = 'K1'", "SELECT ten FROM SinhVien WHERE diem >= 7")]
rec("L09a", plans[0].startswith("SEARCH") and plans[1] == "SCAN SinhVien", f"chỉ mục ghép: {plans}")
rec("L10a", 1000 + 1000 * 500 == alg.join_costs(1000, 500)["page_nlj"] and 1000 + 10 * 500 == alg.join_costs(1000, 500, B=102)["block_nlj"]
    and 3 * 1500 == alg.join_costs(1000, 500)["hash"], "chi phí nối 501 000 / 6 000 / 4 500")
con = db()
p1 = con.execute("EXPLAIN QUERY PLAN SELECT ten FROM SinhVien JOIN Lop ON lop = ma_lop").fetchall()
p2 = con.execute("EXPLAIN QUERY PLAN SELECT ten FROM Lop JOIN SinhVien ON lop = ma_lop").fetchall()
rec("L10b", [r[3] for r in p1] == [r[3] for r in p2], "đổi thứ tự bảng, kế hoạch y hệt")

# ── L11–L15: giao dịch ──
con = sqlite3.connect(":memory:")
con.executescript("CREATE TABLE TaiKhoan (ten TEXT PRIMARY KEY, so_du INTEGER CHECK (so_du >= 0)); INSERT INTO TaiKhoan VALUES ('A', 100), ('B', 50);")
con.execute("BEGIN")
try:
    con.execute("UPDATE TaiKhoan SET so_du = so_du + 150 WHERE ten = 'B'")
    con.execute("UPDATE TaiKhoan SET so_du = so_du - 150 WHERE ten = 'A'")
    con.execute("COMMIT")
except sqlite3.IntegrityError:
    con.execute("ROLLBACK")
rec("L11a", con.execute("SELECT so_du FROM TaiKhoan ORDER BY ten").fetchall() == [(100,), (50,)], "chuyển 150 thất bại, giao dịch huỷ cả nhóm")
rec("L11b", alg.lost_update(100, [10, 10]) == (110, 120), "mất cập nhật 110 thay vì 120")


def cyclic_kahn(edges):
    nodes = {a for a, _ in edges} | {b for _, b in edges}
    indeg = {n: sum(1 for _, b in edges if b == n) for n in nodes}
    queue, seen = [n for n in nodes if indeg[n] == 0], 0
    while queue:
        u = queue.pop()
        seen += 1
        for a, b in edges:
            if a == u:
                indeg[b] -= 1
                if indeg[b] == 0:
                    queue.append(b)
    return seen < len(nodes)


for code, sch, exp in (("L12a", [("T1", "R", "A"), ("T2", "W", "A"), ("T2", "R", "B"), ("T1", "W", "B")], True),
                       ("L12b", [("T1", "R", "A"), ("T1", "W", "A"), ("T2", "R", "A"), ("T2", "W", "A"), ("T1", "R", "B"), ("T1", "W", "B"), ("T2", "R", "B"), ("T2", "W", "B")], False),
                       ("L12c", [("T1", "R", "A"), ("T2", "R", "A"), ("T1", "W", "A"), ("T2", "W", "A")], True)):
    e = {(ti, tj) for i, (ti, ai, xi) in enumerate(sch) for tj, aj, xj in sch[i + 1:] if ti != tj and xi == xj and "W" in (ai, aj)}
    rec(code, cyclic_kahn(e) == exp and alg.precedence_graph(sch) == (e, exp), f"đồ thị ưu tiên {sorted(e)}, chu trình = {exp} (Kahn)")
rec("L13a", alg.strict_2pl([("T1", "W", "A"), ("T2", "W", "B"), ("T1", "W", "B"), ("T2", "W", "A")])[2] and alg.strict_2pl([("T1", "R", "A"), ("T2", "R", "A"), ("T1", "W", "A"), ("T2", "W", "A")])[2],
    "khoá hai pha: hai kịch bản bế tắc")


def recover_alt(log, disk):
    """Cách khác: giá trị cuối của mỗi mục = giá trị mới nhất do một giao dịch ĐÃ commit ghi; nếu không có thì giá trị cũ ở bản ghi
    đầu tiên của mục (trước mọi giao dịch trong nhật ký); mục không có trong nhật ký giữ như đĩa."""
    committed = {r[0] for r in log if r[1] == "C"}
    out = dict(disk)
    for x in {r[2] for r in log if r[1] == "U"}:
        ups = [r for r in log if r[1] == "U" and r[2] == x]
        good = [r for r in ups if r[0] in committed]
        out[x] = good[-1][4] if good else ups[0][3]
    return out


L1 = [("T1", "U", "A", 100, 70), ("T1", "U", "B", 50, 80), ("T1", "C"), ("T2", "U", "A", 70, 60)]
L2 = [("T1", "U", "A", 10, 20), ("T2", "U", "B", 5, 7), ("T2", "C"), ("T1", "U", "C", 1, 2)]
rec("L14a", recover_alt(L1, {"A": 60, "B": 50}) == alg.wal_recover(L1, {"A": 60, "B": 50})[0] == {"A": 70, "B": 80}, "khôi phục: A 70, B 80")
rec("L14b", recover_alt(L2, {"A": 20, "B": 5, "C": 1}) == alg.wal_recover(L2, {"A": 20, "B": 5, "C": 1})[0] == {"A": 10, "B": 7, "C": 1}, "câu đố L14")
rec("L15a", alg.iso_reads("RU", {"A": 100}, [("T2", "W", "A", 200), ("T1", "R", "A"), ("T2", "A")]) == [200]
    and alg.iso_reads("RC", {"A": 100}, [("T1", "R", "A"), ("T2", "W", "A", 200), ("T2", "C"), ("T1", "R", "A")]) == [100, 200]
    and alg.iso_reads("SNAP", {"A": 100}, [("T1", "R", "A"), ("T2", "W", "A", 200), ("T2", "C"), ("T1", "R", "A")]) == [100, 100], "ba dị thường đọc")

# ── L16 ──
E = [("An", "Bình"), ("An", "Chi"), ("Bình", "Dũng"), ("Chi", "Dũng"), ("Chi", "Em"), ("Dũng", "Giang")]
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE Ban (a TEXT, b TEXT)")
con.executemany("INSERT INTO Ban VALUES (?, ?)", E + [(b, a) for a, b in E])
sqlres = sorted(r[0] for r in con.execute("SELECT DISTINCT f2.b FROM Ban f1 JOIN Ban f2 ON f1.b = f2.a WHERE f1.a = 'An' AND f2.b <> 'An' AND f2.b NOT IN (SELECT b FROM Ban WHERE a = 'An')"))
adj = {}
for a, b in E:
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)
dist = {"An": 0}
frontier = ["An"]
while frontier:
    nxt = []
    for u in frontier:
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                nxt.append(v)
    frontier = nxt
rec("L16a", sqlres == sorted(v for v, d in dist.items() if d == 2) == ["Dũng", "Em"], "bạn của bạn: SQL tự nối = BFS khoảng cách 2")


# ── L17 (hành trình thêm cột): mô phỏng từng lô / từng giờ / từng lần thay đổi, không dùng phép chia ──
def copy_chunks(rows, chunk, sec_per_chunk):
    left, n, t = rows, 0, 0.0
    while left > 0:
        left -= min(chunk, left)
        n += 1
        t += sec_per_chunk
    return n, t


def throttled_days(work_hours, stop_from, stop_to):
    done, hours = 0, 0
    while done < work_hours:
        if not (stop_from <= hours % 24 <= stop_to):
            done += 1
        hours += 1
    return -(-hours // 24) if done else 0


import datetime as _dt  # noqa: E402
yrs = (_dt.datetime(1970, 1, 1) + _dt.timedelta(seconds=10 ** 8)).year - 1970
n5, t5 = copy_chunks(5_000_000, 1000, 0.5)
n2, t2 = copy_chunks(2_000_000, 1000, 0.5)
n_s = copy_chunks(10 ** 8, 1000, 1.0)[0]
par_hours = copy_chunks(10 ** 8, 1000, 1.0)[1] / 3600  # 1000 tiến trình: mỗi tiến trình 1 đối tượng/giây → 1 lô 1000 đối tượng mỗi giây
versions, months = 0, 0
while versions + 2 <= 64:
    versions += 2
    months += 1
rec("L17a", (n5, t5) == (5000, 2500.0) and divmod(int(t5), 60) == (41, 40) and (n2, t2) == (2000, 1000.0)
    and copy_chunks(10_000, 1000, 0.5) == (10, 5.0), "chép theo lô: 5 triệu dòng 5000 lô 2500 s; 2 triệu 2000 lô 1000 s; 10 nghìn 10 lô 5 s")
rec("L17b", yrs == 3 and n_s == 100_000 and round(par_hours, 1) == 27.8 and throttled_days(28, 8, 17) == 2
    and sum(1 for h in range(24) if 8 <= h <= 17) == 10,
    "10⁸ giây sau 1/1/1970 là năm 1973 (hơn 3 năm); 100 000 lô; 27,8 giờ; điều tiết 8–17 giờ: 28 giờ việc → 2 ngày")
rec("L17c", months == 32 and versions == 64 and 50_000 == len(range(0, 5_000_000, 100)),
    "64 phiên bản dòng, 2 lần mỗi tháng → 32 tháng; 5 triệu dòng / 100 dòng mỗi trang = 50 000 trang")

n_ok = sum(ok for _, ok in R)
print(f"\n{n_ok}/{len(R)} PASS")
sys.exit(0 if n_ok == len(R) else 1)
