"""Kiểm độc lập mọi khẳng định của khoá DEN — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Hàng / cột: mảng numpy thật, đếm byte của các cột được đọc. Bộ lọc nhiều hàm băm: cài đặt thật bằng hashlib, đo tỉ lệ dương tính giả.
Gộp theo bậc: công thức đóng 1 + 1 + log_fanout(số lần xả). Phân vùng: băm md5 thay cho FNV. Đồ thị: lũy thừa ma trận kề.
BM25: phân số đúng ngoài logarit, đếm tay từ văn bản thô. Nhóm tiêu thụ: chia vòng tròn rồi so tải. Luồng: mô phỏng từng giây có sập.
Hộp thư đi: sqlite3 thật với giao dịch bị huỷ. Kho dữ liệu: truy vấn con thay cho phép nối có điều kiện. Xáo trộn: đếm dòng đổi máy.
Chạy: .venv/Scripts/python audit/den/verify_den.py"""
import hashlib
import math
import random
import sqlite3
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00: mảng thật 10 000 dòng × 50 cột × 8 byte, nhân tỉ lệ lên 10^8 dòng ──
tbl = np.zeros((10_000, 50), dtype=np.float64)
row_bytes = tbl.nbytes                       # đọc theo hàng: mọi cột
col_bytes = sum(np.ascontiguousarray(tbl[:, c]).nbytes for c in (3, 7, 11))
scale = 1e8 / 10_000
rec("L00", row_bytes * scale / 1e9 == 40 == alg.scan_bytes(100e6, 50, 8) / 1e9 and round(col_bytes * scale / 1e9, 1) == 2.4
    and alg.scan_bytes(1e9, 20, 4, "col", 2) / 1e9 == 8, "mảng thật: theo hàng 40 GB, 3 cột 2,4 GB; câu hỏi 80 / 8 GB")


# ── L01: bộ lọc nhiều hàm băm cài đặt thật ──
def bloom_fpr(n, bits_per_key, k, probes=200_000):
    m = int(n * bits_per_key)
    bits = np.zeros(m, bool)

    def idx(s):
        h = hashlib.sha256(s.encode()).digest()
        a, b = int.from_bytes(h[:8], "little"), int.from_bytes(h[8:16], "little") | 1
        return [(a + i * b) % m for i in range(k)]
    for i in range(n):
        bits[idx(f"k{i}")] = True
    return sum(all(bits[j] for j in idx(f"x{i}")) for i in range(probes)) / probes


fpr = bloom_fpr(50_000, 9.59, 7)
T = [{"a": 1, "b": 2}, {"b": 5, "c": 7}, {"a": None}]
rec("L01", abs(fpr - 0.01) < 0.002 and alg.lsm_lookup(T, "b") == (5, 2) and alg.lsm_lookup(T, "a") == (None, 1) and alg.lsm_compact(T) == {"b": 5, "c": 7}
    and round(5 * fpr, 2) in (0.04, 0.05, 0.06), f"bộ lọc thật 9,59 bit/khoá, 7 hàm băm: dương tính giả {fpr:.4f} ≈ 1%; đường đọc và gộp khớp")

# ── L02: công thức đóng cho gộp theo bậc; độ sâu cây B bằng logarit ──
rec("L02", all(alg.tiered_compaction_wa(f ** L, f) == 2 + L for f, L in ((4, 4), (4, 5), (10, 2))) and math.ceil(math.log(1e9, 500) - 1e-12) == 4 == alg.btree_depth(1e9, 500)
    and 4096 / 100 == 40.96 and 16384 / 128 == 128, "khuếch đại = 1 + 1 + số bậc (6 với 256 lần xả, 7 với 1024); 1 tỉ khoá, 500 con → 4 tầng")

# ── L03: giới hạn văn bản ──
rec("L03", (16 << 20) // 200 == 83886 and (16 << 20) // 1024 == 16384 and (16 << 20) // 500 == 33554, "16 MiB: 83 886 dòng 200 byte; 16 384 mục 1 KiB; 33 554 bình luận 500 byte")

# ── L04: phân vùng bằng md5 thay cho FNV ──
md5 = lambda s, n: int(hashlib.md5(s.encode()).hexdigest(), 16) % n
loads = Counter(md5(f"u{i}", 8) for i in range(100_000))
hot = Counter(md5(k, 8) for k in ["sao"] * 30_000 + [f"u{i}" for i in range(70_000)])
rec("L04", max(loads.values()) / 1e5 < 0.13 and abs(max(hot.values()) / 1e5 - 0.3875) < 0.01 and round(max(alg.partition_loads(["sao"] * 30000 + [f"u{i}" for i in range(70000)], 8, lambda x: alg.stable_hash(x) % 8)), 4) == 0.3875,
    f"md5: tải lớn nhất {max(loads.values()) / 1e5:.4f} ≈ 12,5%; khoá ngôi sao 30% → {max(hot.values()) / 1e5:.4f} ≈ 38,75%")

# ── L05: kích thước phân vùng ──
rec("L05", 100 * 24 * 3600 / 1e6 == 8.64 and round(100 * 24 * 3600 * 365 / 1e9, 2) == 3.15 and 1000 * (24 * 3600 // 10) * 30 / 1e6 == 259.2, "8,64 MB/ngày; 3,15 GB/năm; 259,2 MB/tháng")

# ── L06: lũy thừa ma trận kề ──
names = ["An", "Bình", "Chi", "Dũng", "Em", "Giang"]
E = [("An", "Bình"), ("An", "Chi"), ("Bình", "Dũng"), ("Chi", "Dũng"), ("Chi", "Em"), ("Dũng", "Giang")]
A = np.zeros((6, 6), int)
for u, v in E:
    A[names.index(u), names.index(v)] = A[names.index(v), names.index(u)] = 1
walks2 = A @ A
reach = lambda k: int((((np.linalg.matrix_power(A + np.eye(6, dtype=int), k))[0] > 0).sum()) - 1)
adj = {n: {names[j] for j in range(6) if A[names.index(n), j]} for n in names}
rec("L06", walks2[0, names.index("Dũng")] == 2 and walks2[0, names.index("Em")] == 1 and reach(2) == 4 == alg.graph_reach(adj, "An", 2) and reach(3) == 5 == alg.graph_reach(adj, "An", 3)
    and 50 ** 4 == 6_250_000, "ma trận kề: An → Dũng 2 đường (2 bạn chung), → Em 1; trong 2 bước 4 người, 3 bước 5 người")

# ── L07: BM25 tính lại từ văn bản thô ──
docs = ["mèo đen mèo", "chó đen", "mèo trắng chó con"]
toks = [d.split() for d in docs]
avg = sum(len(t) for t in toks) / len(toks)


def score(q, i):
    s = 0.0
    for w in q.split():
        n = sum(w in t for t in toks)
        tf = toks[i].count(w)
        if tf:
            s += math.log(1 + (len(toks) - n + 0.5) / (n + 0.5)) * tf * 2.2 / (tf + 1.2 * (0.25 + 0.75 * len(toks[i]) / avg))
    return s


ok7 = all([round(score(q, i), 3) for i in range(3)] == [round(x, 3) for x in alg.bm25(q.split(), toks)] for q in ("mèo", "chó", "mèo đen"))
rec("L07", ok7 and [round(score("mèo", i), 3) for i in range(3)] == [0.646, 0.0, 0.414] and [round(score("chó", i), 3) for i in range(3)] == [0.0, 0.544, 0.414]
    and round(score("mèo đen", 0), 3) == 1.116 and round((2 * 2.2 / 3.2) / (2.2 / 2.2), 3) == 1.375,
    "từ văn bản thô: “mèo” 0,646 / 0 / 0,414; “chó” 0 / 0,544 / 0,414; “mèo đen” 1,116; tf 1 → 2 nhân 1,375")


# ── L08: chia vòng tròn (cách khác) cho cùng số phân vùng mỗi người ──
def round_robin(P, C):
    c = Counter(p % C for p in range(P))
    return sorted((c.get(i, 0) for i in range(C)), reverse=True)


rec("L08", round_robin(12, 5) == sorted(alg.range_assign(12, 5), reverse=True) == [3, 3, 2, 2, 2] and round_robin(12, 13).count(0) == 1
    and max(round_robin(8, 3)) * 1000 > 2500 >= max(round_robin(8, 4)) * 1000, "vòng tròn khớp khoảng: 3,3,2,2,2; 13 người → 1 rảnh; 8 phân vùng: 3 người quá tải, 4 người đủ")


# ── L09: mô phỏng từng giây, sập ở giây 40, điểm kiểm tra mỗi 30 giây ──
def run(crash_at=None, ckpt=30, rate=1000, end=60):
    count, saved, processed = 0, (0, 0), 0
    t = 0
    while t < end:
        count += rate; processed += rate; t += 1
        if t % ckpt == 0:
            saved = (count, t)
        if crash_at and t == crash_at:
            count, t = saved; crash_at = None
    return count, processed


good, _ = run()
recovered, processed = run(crash_at=40)
rec("L09", good == recovered == 60_000 and processed - 60_000 == 10_000 == alg.replay_events(30, 40, 1000) and 300000 / 15000 == 20,
    "mô phỏng: có sập vẫn đếm đúng 60 000, xử lý thêm đúng 10 000 sự kiện phát lại; đuổi kịp 300 000 cần 20 s")

# ── L10: sqlite3 thật — ghi đôi so với hộp thư đi ──
cn = sqlite3.connect(":memory:", isolation_level=None)
cn.executescript("CREATE TABLE don(id INT PRIMARY KEY); CREATE TABLE hop_thu(id INT, da_gui INT DEFAULT 0);")
sent, rng = [], random.Random(11)
for i in range(20_000):
    crash = rng.random() < 0.001
    cn.execute("BEGIN"); cn.execute("INSERT INTO don VALUES (?)", (i,)); cn.execute("INSERT INTO hop_thu(id) VALUES (?)", (i,))
    if rng.random() < 0.01:
        cn.execute("ROLLBACK")          # giao dịch huỷ: không có đơn, không có sự kiện
        continue
    cn.execute("COMMIT")
    if not crash:
        pass
for (i,) in cn.execute("SELECT id FROM hop_thu WHERE da_gui = 0").fetchall():
    sent.append(i)                       # bộ chuyển tiếp gửi
    if rng.random() < 0.001:
        sent.append(i)                   # sập sau khi gửi, trước khi đánh dấu → gửi lại
    cn.execute("UPDATE hop_thu SET da_gui = 1 WHERE id = ?", (i,))
orders = {r[0] for r in cn.execute("SELECT id FROM don")}
rec("L10", set(sent) == orders and len(sent) >= len(orders) and abs(alg.dual_write_sim(10 ** 6, 0.001)[0] - 1000) < 5 * math.sqrt(1000) and alg.dual_write_sim(10 ** 6, 0.001, outbox=True)[0] == 0,
    f"sqlite3: {len(orders)} đơn đã cam kết, mọi đơn có sự kiện, {len(sent) - len(orders)} sự kiện trùng, giao dịch huỷ không phát gì")

# ── L11: nhóm hàng tự dựng ──
rs = random.Random(3)
grp_sorted = [[d] * 1000 for d in range(100)]
grp_rand = [[rs.randrange(100) for _ in range(1000)] for _ in range(100)]
stats = lambda G: [(min(g), max(g)) for g in G]
need = lambda G, lo, hi: sum(1 for a, b in stats(G) if b >= lo and a <= hi)
rec("L11", need(grp_sorted, 42, 42) == 1 and need(grp_rand, 42, 42) == 100 and need(grp_sorted, 10, 16) == 7 and need(grp_rand, 10, 16) == 100 == alg.rowgroups_read(grp_rand, 10, 16),
    "thống kê nhỏ nhất–lớn nhất: sắp → 1 nhóm (7 cho một tuần); không sắp → 100")

# ── L12: truy vấn con thay cho nối có điều kiện ──
c2 = sqlite3.connect(":memory:")
c2.executescript("""CREATE TABLE dim(sk INT, kh TEXT, tinh TEXT, tu TEXT);
INSERT INTO dim VALUES (1,'k1','Hà Nội','2026-01-01'),(2,'k1','Đà Nẵng','2026-03-01');
CREATE TABLE fact(ngay TEXT, kh TEXT, tien INT); INSERT INTO fact VALUES ('2026-02-10','k1',100),('2026-03-10','k1',200);""")
hist = c2.execute("""SELECT substr(ngay,1,7), (SELECT tinh FROM dim d WHERE d.kh=f.kh AND d.tu<=f.ngay ORDER BY d.tu DESC LIMIT 1), tien FROM fact f ORDER BY 1""").fetchall()
over = c2.execute("""SELECT substr(ngay,1,7), (SELECT tinh FROM dim d WHERE d.kh=f.kh ORDER BY d.tu DESC LIMIT 1), tien FROM fact f ORDER BY 1""").fetchall()
naive = c2.execute("SELECT COUNT(*), SUM(tien) FROM fact f JOIN dim d ON d.kh=f.kh").fetchone()
rec("L12", hist == alg.scd_report(True) and over == alg.scd_report(False) and naive == (4, 600),
    "truy vấn con: lịch sử → Hà Nội 100 / Đà Nẵng 200; ghi đè → Đà Nẵng cả hai; nối chỉ theo mã → 4 dòng, doanh thu 600 (gấp đôi 300)")

# ── L13: đếm dòng đổi máy khi xáo trộn ──
rm = random.Random(5)
M, N = 100, 200_000
moved = sum(1 for i in range(N) if rm.randrange(M) != md5(f"r{i}", M)) / N
rec("L13", abs(moved - 0.99) < 0.002 and alg.join_network_gb(1000, 1, 100, "broadcast") == 99 and round(1001 * moved) in range(989, 994)
    and alg.join_network_gb(500, 2, 50, "broadcast") == 98 and round(alg.join_network_gb(500, 2, 50, "shuffle"), 2) == 491.96
    and (lambda rows: (len(rows) - len({r[0] for r in rows}), sum(r[1] is None for r in rows)))([(1, 10), (2, None), (2, 5), (3, 7)]) == (1, 1),
    f"tỉ lệ dòng đổi máy {moved:.4f} ≈ 99/100 → xáo trộn ≈ 991 GB; phát tán 99 GB; kiểm chất lượng: 1 trùng, 1 rỗng")

# ── L14 (hành trình): cộng dồn từng lượt / từng ngày, gộp phiên bằng quét thật, rút lại bằng mô phỏng bên nhận ──
def run_iters(first, later, n):
    t = 0
    for i in range(n):
        t += first if i == 0 else later
    return t


hadoop10, spark10 = run_iters(80, 76, 10), run_iters(46, 3, 10)          # [RDD12] Hình 7, hồi quy logistic, 100 máy
km_fail = sum(80 if i == 6 else 58 for i in range(1, 11))               # [RDD12] §6.3: lượt 6 mất một máy
deaths = sum(1.2 for _ in range(29_423))                                # [MR04] Bảng 1: 1,2 máy chết mỗi việc
busy = 79_186 / 31                                                      # máy-ngày của tháng 8/2004 chia 31 ngày


def sessions(times, gap):
    """Gộp phiên như [DF15] Hình 4: mỗi sự kiện mở cửa sổ [t, t + gap); hai cửa sổ chồng nhau thì gộp."""
    out = []
    for t in sorted(times):
        if out and t < out[-1][1]:
            out[-1][1] = max(out[-1][1], t + gap)
        else:
            out.append([t, t + gap])
    return [tuple(w) for w in out]


hm = lambda s: int(s[:2]) * 60 + int(s[3:])
k1 = sessions([hm("13:02"), hm("13:57"), hm("13:20")], 30)
k2 = sessions([hm("13:14")], 30)
slide = [w for w in range(hm("11:58"), hm("12:03")) if w <= hm("12:00") < w + 2]   # cửa sổ rộng 2 phút, mỗi phút một cửa sổ


def downstream(panes, retract):
    total, last = 0, None
    for v in panes:
        if retract and last is not None:
            total -= last
        total += v
        last = v
    return total


pieces = 10 ** 12 // (64 * 10 ** 6)
rec("L14", (hadoop10, spark10) == (764, 73) and round(hadoop10 / spark10, 1) == 10.5 and round(76 / 3, 1) == 25.3 and round(62 / 3, 1) == 20.7
    and km_fail - 58 * 10 == 22 and round(deaths) == 35_308 and round(busy) == 2554
    and round(1283 / 891 - 1, 2) == 0.44 and round(933 / 891 - 1, 3) == 0.047 and round(3800 / 700, 1) == 5.4 and pieces == 15_625
    and k1 == [(hm("13:02"), hm("13:50")), (hm("13:57"), hm("14:27"))] and k2 == [(hm("13:14"), hm("13:44"))] and len(slide) == 2
    and downstream([7, 10], True) == 10 and downstream([7, 10], False) == 17
    and 1000 // 200 == 5 and 3600 * 5 == 18_000 and 3 * 10 == 30 and 2016 - 2010 == 6 and run_iters(80, 76, 20) == 1524 and run_iters(46, 3, 20) == 103,
    f"10 lượt: 764 s so với 73 s (≈ 10,5 lần), lượt sau 25,3 lần; mất máy +22 s; tháng 8/2004 ≈ {round(deaths)} lần máy chết, ≈ 2554 máy bận cả tháng; "
    "dự phòng +44%, giết 200 tiến trình +4,7%; 3800 → 700 dòng ≈ 5,4; 1 TB / 64 MB = 15 625 mảnh; phiên k1 [13:02, 13:50) và [13:57, 14:27); "
    "rút lại 10, không rút 17; 200 ms → 5 lô mỗi giây; 3 lần nhanh hơn với 10 lần ít máy → 30 lần mỗi máy; 20 lượt: 1524 s so với 103 s")

bad = [c for c, ok in R if not ok]
print(f"\nverify_den: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
