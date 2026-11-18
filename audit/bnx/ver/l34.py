"""Kiểm độc lập BNX L34 (Hệ thống phê duyệt tín dụng). Đường khác với tools/checklib_bnx/l34.py và với mã trên màn hình:
- CHẠY LẠI THẬT (không đệm) mọi chương trình trên màn hình (Python 3 + sqlite3) và so từng ký tự với đầu ra đã hiện;
- máy trạng thái: duyệt đồ thị bằng BFS (đường đi ngắn nhất 5 cạnh, GIAI_NGAN không tới được trong 1 bước, hai trạng thái cuối);
- quyền duyệt: tính lại bằng bisect trên danh sách trần (không vòng lặp if của bài);
- đồng ý/lịch sử: dựng lại bằng SQL khác (date(), LEFT JOIN, COUNT) trên bộ dữ liệu của chương trình;
- số dòng đọc: dựng lại hai cỡ (10^3 và 10^6) và đếm bằng EXPLAIN (mã máy ảo: Rewind/Next so với SeekGE) và đếm trực tiếp dòng của khách 7;
- lab: chạy loi_giai.py, so mong_doi.txt, tính lại số bằng công thức khác."""
import bisect
import re
import sqlite3
import subprocess
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import lib2  # noqa: E402
import l34 as src  # noqa: E402

LAB = ROOT / "labs" / "BNX" / "L34"


def bfs(canh, a, b):
    g = {}
    for u, v in canh:
        g.setdefault(u, []).append(v)
    d, q = {a: 0}, deque([a])
    while q:
        u = q.popleft()
        for v in g.get(u, []):
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return d.get(b), d, g


def run(rec):
    lib2.verify_programs(rec, "L34")
    P = {q.name: q for q in lib2.PROGRAMS if q.lesson == "L34"}
    # ── máy trạng thái ──
    canh = [("KHOI_TAO", "THAM_DINH"), ("THAM_DINH", "CHAM_DIEM"), ("THAM_DINH", "TU_CHOI"), ("CHAM_DIEM", "CHO_DUYET"),
            ("CHO_DUYET", "DA_DUYET"), ("CHO_DUYET", "TU_CHOI"), ("DA_DUYET", "GIAI_NGAN")]
    rec("L34", set(canh) == alg.bnx_l34_canh() and all(c in P["MayTrangThai"].code for c in (f'("{a}", "{b}")' for a, b in canh)), "bảng cạnh: 7 cạnh trong mã = trong checklib")
    dist, reach, g = bfs(canh, "KHOI_TAO", "GIAI_NGAN")
    cuoi = sorted(s for s in reach if s not in g)
    rec("L34", dist == 5 and "GIAI_NGAN" not in g.get("KHOI_TAO", []) and cuoi == ["GIAI_NGAN", "TU_CHOI"], "BFS: GIAI_NGAN cách KHOI_TAO 5 cạnh (6 trạng thái trên đường), không tới trực tiếp; hai trạng thái cuối GIAI_NGAN và TU_CHOI")
    lines = P["MayTrangThai"].out.splitlines()
    cur, exp = "KHOI_TAO", []
    for den, ai in [("GIAI_NGAN", "an"), ("THAM_DINH", "an"), ("CHAM_DIEM", "binh"), ("CHO_DUYET", "he_thong"), ("DA_DUYET", "chi"), ("KHOI_TAO", "chi"), ("GIAI_NGAN", "he_thong")]:
        if (cur, den) in set(canh):
            exp.append(f"{cur} -> {den}: {ai} ghi nhan")
            cur = den
        else:
            exp.append(f"{cur} -> {den}: tu choi")
    exp.append(f"nhat ky: {sum('ghi nhan' in e for e in exp)} dong; trang thai cuoi: {cur}")
    rec("L34", lines == exp and sum("tu choi" in l for l in lines) == 2 and sum("ghi nhan" in l for l in lines) == 5 and cur == "GIAI_NGAN", "7 lần thử: 5 hợp lệ + 2 bị chặn, kết thúc GIAI_NGAN (mô phỏng lại bằng tập cạnh)")
    # ── quyền duyệt (bisect) ──
    bac = {"CN": ([100, 500], ["chuyen vien", "truong phong", "hoi dong"]), "DN": ([2000, 10000], ["truong phong", "giam doc khoi", "hoi dong"])}

    def vai(loai, tong):
        tran, ten = bac[loai]
        return ten[bisect.bisect_left(tran, tong)]  # tong <= tran → bậc đó
    rec("L34", [vai("CN", t) for t in (80, 100, 101, 300, 500, 501, 900)] == ["chuyen vien", "chuyen vien", "truong phong", "truong phong", "truong phong", "hoi dong", "hoi dong"], "bisect: biên 100 → chuyên viên, 101 → trưởng phòng, 500 → trưởng phòng, 501 → hội đồng")
    rec("L34", [alg.bnx_l34_nguoi_duyet("CN", 0, t)[1] for t in (80, 100, 101, 300, 500, 501, 900)] == [vai("CN", t) for t in (80, 100, 101, 300, 500, 501, 900)] and alg.bnx_l34_nguoi_duyet("DN", 0, 3000) == (3000, "giam doc khoi") and vai("DN", 3000) == "giam doc khoi", "checklib khớp bisect ở mọi biên; doanh nghiệp 3000 → giám đốc khối")
    out = P["PhanQuyen"].out.splitlines()
    du, rows = 0, []
    for m in (90, 90, 90):
        rows.append(f"ho so {m}: rieng le {vai('CN', m)}; theo tong {du + m} -> {vai('CN', du + m)}")
        du += m
    rec("L34", out[:4] == ["CN xin 80: tong 80 -> chuyen vien", "CN xin 300: tong 300 -> truong phong", "CN xin 900: tong 900 -> hoi dong", "DN xin 3000: tong 3000 -> giam doc khoi"] and out[4:7] == rows and du == 270 and vai("CN", 270) == "truong phong", "ba hồ sơ 90: riêng lẻ chuyên viên; theo tổng 90, 180, 270 → chuyên viên, trưởng phòng, trưởng phòng")
    rec("L34", out[7:] == ["an tao, an duyet: tu choi (tu duyet)", "an tao, binh duyet (chuyen vien): tu choi (thieu quyen)", "an tao, chi duyet (truong phong): dong y"]
        and alg.bnx_l34_duoc_duyet("an", "chi", "truong phong", "truong phong") and not alg.bnx_l34_duoc_duyet("an", "binh", "chuyen vien", "truong phong") and not alg.bnx_l34_duoc_duyet("an", "an", "truong phong", "truong phong"), "tách nhiệm vụ: tự duyệt bị từ chối, thiếu quyền bị từ chối, đủ quyền thì đồng ý")
    # ── đồng ý và lịch sử: SQL khác (date(), LEFT JOIN) ──
    dy = [("K1", "tham dinh", "2026-12-31", 0), ("K3", "tham dinh", "2026-01-31", 0), ("K4", "tham dinh", "2026-12-31", 1)]
    ls = [("K1", "2026-01", 1), ("K1", "2026-02", 2), ("K1", "2026-03", 1), ("K2", "2026-02", 5), ("K3", "2026-02", 3), ("K4", "2026-03", 4)]
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE dy (khach TEXT, md TEXT, hh TEXT, th INT)")
    db.execute("CREATE TABLE ls (khach TEXT, thang TEXT, nhom INT)")
    db.executemany("INSERT INTO dy VALUES (?,?,?,?)", dy)
    db.executemany("INSERT INTO ls VALUES (?,?,?)", ls)
    ca = [("K1", "tham dinh"), ("K2", "tham dinh"), ("K3", "tham dinh"), ("K4", "tham dinh"), ("K1", "tiep thi")]
    exp, cho = [], 0
    for khach, md in ca:
        r = db.execute("SELECT MAX(l.nhom) FROM dy d JOIN ls l ON l.khach = d.khach WHERE d.khach = ? AND d.md = ? AND date(d.hh) >= date('2026-03-10') AND d.th = 0", (khach, md)).fetchone()[0]
        ok = r is not None
        cho += ok
        exp.append(f"{khach} {md}: {'cho phep' if ok else 'tu choi'}, nhom cao nhat {r}")
    exp += [f"nhat ky cho phep: {cho}", f"nhat ky tu choi: {len(ca) - cho}"]
    rec("L34", P["LichSuTinDung"].out.splitlines() == exp and cho == 1 and len(ca) - cho == 4, "tra cứu có đồng ý: 1 cho phép (nhóm cao nhất 2), 4 từ chối; nhật ký 1 + 4 (SQL khác: date(), JOIN)")
    rec("L34", db.execute("SELECT MAX(nhom) FROM ls WHERE khach = 'K2'").fetchone()[0] == 5 and "nhom cao nhat 5" not in P["LichSuTinDung"].out, "dữ liệu nhóm 5 của K2 có thật nhưng KHÔNG lọt ra khi thiếu đồng ý")
    rec("L34", alg.bnx_l34_con_han("2026-03-31", "2026-03-31") and not alg.bnx_l34_con_han("2026-03-31", "2026-04-01") and db.execute("SELECT date('2026-03-31') >= date('2026-03-31'), date('2026-03-31') >= date('2026-04-01')").fetchone() == (1, 0), "biên ngày hết hạn (quiz câu 2): cùng ngày còn hạn, hôm sau hết hạn")
    # ── nhật ký, đua ghi ──
    rec("L34", P["KiemNhatKy"].out.splitlines() == ["canh sai trong nhat ky: 0", "cho dut: 0 ; trang thai dung lai: GIAI_NGAN", "xoa dong 3: 1 cho dut"], "nhật ký: 0 cạnh sai, 0 chỗ đứt, kết thúc GIAI_NGAN; xoá dòng 3 → 1 chỗ đứt")
    d2 = sqlite3.connect(":memory:")
    d2.execute("CREATE TABLE h (id INTEGER PRIMARY KEY, tt TEXT)")
    d2.execute("INSERT INTO h VALUES (1, 'CHO_DUYET')")
    a1 = d2.execute("UPDATE h SET tt='DA_DUYET' WHERE id=1 AND tt='CHO_DUYET'").rowcount
    a2 = d2.execute("UPDATE h SET tt='DA_DUYET' WHERE id=1 AND tt='CHO_DUYET'").rowcount
    d2.execute("UPDATE h SET tt='CHO_DUYET'")
    b1 = d2.execute("UPDATE h SET tt='DA_DUYET' WHERE id=1").rowcount
    b2 = d2.execute("UPDATE h SET tt='DA_DUYET' WHERE id=1").rowcount
    rec("L34", (a1, a2, b1, b2) == (1, 0, 1, 1) and P["HaiNguoiCungDuyet"].out.splitlines() == ["khong dieu kien: an thanh cong, binh thanh cong", "co dieu kien: an thanh cong, binh bi tu choi"], "đua ghi: có điều kiện rowcount 1 rồi 0; không điều kiện 1 rồi 1")
    # ── quy mô: đếm bằng EXPLAIN và đếm trực tiếp ──
    ql = P["QuyMoTraCuu"].out.splitlines()
    ok_all = []
    for n in (1000, 1000000):
        d3 = sqlite3.connect(":memory:")
        d3.execute("CREATE TABLE ls (khach INT, thang INT, nhom INT)")
        d3.executemany("INSERT INTO ls VALUES (?,?,?)", ((i // 5, i % 5, i % 3) for i in range(n)))
        q = "SELECT COUNT(*) FROM ls WHERE khach = 7"
        ops0 = [r[1] for r in d3.execute("EXPLAIN " + q)]
        d3.execute("CREATE INDEX ix ON ls (khach)")
        ops1 = [r[1] for r in d3.execute("EXPLAIN " + q)]
        trung = d3.execute(q).fetchone()[0]
        ok_all.append("Rewind" in ops0 and "SeekGE" not in ops0 and "SeekGE" in ops1 and "Rewind" not in ops1 and trung == 5
                      and d3.execute("SELECT COUNT(*) FROM ls").fetchone()[0] == n
                      and ql[len(ok_all)] == f"{n} dong: khong chi muc SCAN doc {n}; co chi muc SEARCH doc 5")
    rec("L34", all(ok_all), "số dòng đọc: quét toàn bảng 1 000 và 1 000 000 (EXPLAIN: Rewind), có chỉ mục 5 ở cả hai (EXPLAIN: SeekGE, đếm trực tiếp 5)")
    rec("L34", alg.bnx_l34_doc(10 ** 3, False) == 1000 and alg.bnx_l34_doc(10 ** 6, False) == 10 ** 6 and alg.bnx_l34_doc(10 ** 6, True) == 5 and 1000 * 10 ** 6 == 10 ** 9, "checklib: 1 000 hồ sơ × 10^6 dòng = 10^9 dòng đọc mỗi ngày")
    # ── lab ──
    r = subprocess.run([sys.executable, "-I", str(LAB / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8", timeout=60)
    want = (LAB / "mong_doi.txt").read_text(encoding="utf-8").strip()
    tong_a = 120 + 100
    rec("L34", r.returncode == 0 and r.stdout.strip() == want and want.splitlines()[0] == f"ho so A: tong {tong_a} -> hoi dong" and tong_a > 200 and 0 + 40 <= 50, "lab: loi_giai.py in đúng mong_doi.txt; A = 120 + 100 = 220 > 200 → hội đồng, B = 40 ≤ 50 → chuyên viên")
    rec("L34", "2026-05-31" <= "2026-06-30" < "2026-07-01" and want.splitlines()[3:] == ["K9 tham dinh 2026-05-31: cho phep", "K9 tham dinh 2026-07-01: tu choi (het han)"], "lab: ngày 05-31 còn hạn, ngày 07-01 hết hạn (hết hạn 06-30)")
    rec("L34", all((LAB / f).exists() for f in ("de.md", "mong_doi.txt", "loi_giai.py")), "lab: có de.md, mong_doi.txt, loi_giai.py")
    # ── mã hiện trên màn hình đủ để dựng lại số đo (khung 1/2 và 2/2) và biên 100 thống nhất ──
    ls_ = P["QuyMoTraCuu"].code.split("\n")
    rec("L34", len(ls_) == 22 and "def tick" in "\n".join(ls_[:10]) and "create_function" in ls_[9] and "CREATE INDEX" in ls_[16]
        and all(len(x) <= 70 for x in ls_) and 11 <= len(ls_[10:22]) <= 12,
        "quymo: hai khung (dòng 1–10, 11–22) chứa tick(), create_function và CREATE INDEX; mỗi khung ≤ 12 dòng, dòng ≤ 70 ký tự")
    import yaml
    sp = next((ROOT / "lessons" / "bnx").glob("L34_*.yaml"))
    txt = sp.read_text(encoding="utf-8")
    rec("L34", "không quá 100 triệu" in txt and "không quá một trăm triệu" in txt and "dưới 100 triệu" not in txt and "dưới một trăm triệu" not in txt and "tong <= tran" in P["PhanQuyen"].code
        and "≤ 100 chuyên viên" in txt, "biên 100 thống nhất: hook (chữ và lời) 'không quá 100', mã `tong <= tran`, quiz '≤ 100'")
    # ── ví dụ nhỏ trong bảng "cách đọc" (P1, vòng fix4): chạy thật từng ví dụ ──
    db_ = sqlite3.connect(":memory:")
    db_.execute("CREATE TABLE t (id INTEGER, v TEXT)")
    db_.execute("INSERT INTO t VALUES (7, 'x')")
    rec("L34", db_.execute("SELECT v FROM t WHERE id = ?", (7,)).fetchone()[0] == "x" and (7,)[0] == 7 and (5,)[0] == 5 and db_.execute("SELECT v FROM t WHERE id = 99").fetchone() is None,
        "bảng cách đọc: `?` với (7,) = `id = 7`; fetchone()[0] lấy giá trị đầu; không có dòng thì None")
    rec("L34", sum(1 for x in [3, 8, 9] if x > 5) == 2 and [1, 2, 3][1:] == [2, 3] and list(zip([1, 2, 3], [2, 3])) == [(1, 2), (2, 3)] and {"a": 1}.get("b", 0) == 0
        and 7 // 5 == 1 and 7 % 5 == 2 and 3000 > 2000 and 3000 <= 10000, "bảng cách đọc: sum/zip/slice/get/phép chia nguyên và dư; DN 3 000 vượt 2 000 và ≤ 10 000 nên giám đốc khối")
    gh = db_.execute("SELECT kq, COUNT(*) FROM (SELECT 'a' AS kq UNION ALL SELECT 'b' UNION ALL SELECT 'b') GROUP BY kq ORDER BY kq").fetchall()
    rec("L34", gh == [("a", 1), ("b", 2)] and all(s in P["HaiNguoiCungDuyet"].out for s in ("an thanh cong, binh thanh cong", "an thanh cong, binh bi tu choi")),
        "GROUP BY/COUNT/ORDER BY đúng nhóm; Lỗi 2: không điều kiện cả hai thành công, có điều kiện chỉ một (rowcount 1 rồi 0)")
    # R4: bảng SQL nền đứng trước mã; nhãn MÔ PHỎNG ở Lỗi 2
    yml4 = " ".join(next((ROOT / "lessons" / "bnx").glob("L34_*.yaml")).read_text(encoding="utf-8").split())
    rec("L34", all(k in yml4 for k in ("INSERT INTO ho_so VALUES", "UPDATE ho_so SET tt = ? WHERE id = ?", "COUNT(*)", "CREATE INDEX ix ON ls (khach)", "EXPLAIN QUERY PLAN", "kh.split()[0]", "MÔ PHỎNG: hai lần ghi nối tiếp"))
        and yml4.index("INSERT INTO ho_so VALUES") < yml4.index("Bước 1. Luật là một bảng") + 400,
        "bảng SQL nền (INSERT/SELECT/UPDATE/COUNT, CREATE INDEX, EXPLAIN, split) có mặt; Lỗi 2 gắn nhãn MÔ PHỎNG: hai lần ghi nối tiếp")
