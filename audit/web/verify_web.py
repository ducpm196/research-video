"""Kiểm độc lập mọi khẳng định của khoá WEB — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Vòng khứ hồi: dòng thời gian sự kiện. Cây HTML: xml.etree (cây thật). Độ ưu tiên: đếm tay từng ký hiệu. Vòng lặp sự kiện: chạy Node từ tệp tạm.
Bất đồng bộ: asyncio của Python làm phép đối chứng. So khớp danh sách: vét cạn mọi tập con giữ nguyên chỗ. Khoá lũy đẳng: sqlite3 với ràng buộc
UNIQUE. Phân trang: EXPLAIN QUERY PLAN của sqlite3. Bộ nhớ đệm: bảng luật RFC 9111. PKCE: hashlib + base64 thủ công. Tương phản: numpy.
Ngoại tuyến: mọi hoán vị thứ tự đến. Phiên bản cũ: Monte Carlo một triệu người dùng. Chạy: .venv/Scripts/python audit/web/verify_web.py"""
import asyncio
import base64
import hashlib
import itertools
import math
import random
import sqlite3
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
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


# ── L00: dòng thời gian: mỗi bước gửi ở t, nhận ở t + RTT ──
def first_byte(rtt, steps=("bắt tay giao vận", "bắt tay mã hoá", "yêu cầu")):
    t = 0
    for _ in steps:
        t += rtt
    return t


rec("L00", first_byte(50) == 150 == alg.rtt_before_first_byte(50) and first_byte(200) + 4 * 200 == 1400 and 10 * 50 == 500, "dòng thời gian: 150 ms; người dùng xa 600 + 4 · 200 = 1400 ms")


# ── L01: cây thật bằng xml.etree ──
def tree(html):
    root = ET.fromstring(html)
    depth = lambda e: 1 + max((depth(c) for c in e), default=0)
    return sum(1 for _ in root.iter()), depth(root)


rec("L01", tree("<ul><li>A</li><li>B<b>!</b></li></ul>") == (4, 3) == alg.html_tree_stats("<ul><li>A</li><li>B<b>!</b></li></ul>")
    and tree("<article><h1>T</h1><p>a<em>b</em> c</p></article>") == (4, 3) and tree("<nav><ul><li><a>A</a></li><li><a>B</a></li></ul></nav>") == (6, 4),
    "xml.etree: 4 phần tử độ sâu 3; câu hỏi (4, 3) và (6, 4)")


# ── L02: đếm tay ký hiệu ──
def spec_hand(sel):
    ids = sel.count("#")
    cls = sel.count(".") + sel.count("[") + sum(1 for i, ch in enumerate(sel) if ch == ":" and (i + 1 < len(sel) and sel[i + 1] != ":") and (i == 0 or sel[i - 1] != ":"))
    tags = sum(1 for part in sel.split() if part[0].isalpha())
    return ids, cls, tags


ok2 = all(spec_hand(s) == alg.specificity(s) for s in ("#menu .muc", "nav .muc .con", "ul li:hover", ".x.y.z"))
rec("L02", ok2 and 200 + 2 * 20 + 2 * 5 == 250 == alg.box_width(200, 20, 5) and 300 + 32 + 4 == 336 and (1, 1, 0) > (0, 2, 1) and (0, 3, 0) > (0, 1, 2),
    "đếm tay khớp: (1,1,0) thắng (0,2,1); (0,3,0) thắng (0,1,2); hộp 250 và 336 px")


# ── L03: Node chạy từ tệp tạm (đường khác với node -e) ──
def node_file(js):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
    try:
        return subprocess.run(["node", f.name], capture_output=True, text=True, timeout=30).stdout.split()
    finally:
        Path(f.name).unlink()


o1 = node_file("console.log(1);setTimeout(()=>console.log(2),0);Promise.resolve().then(()=>console.log(3));console.log(4)")
o2 = node_file("console.log('A');setTimeout(()=>console.log('B'),0);Promise.resolve().then(()=>console.log('C')).then(()=>console.log('D'));queueMicrotask(()=>console.log('E'));console.log('F')")
o3 = node_file("const t=Date.now();setTimeout(()=>console.log(Date.now()-t),0);const e=Date.now()+200;while(Date.now()<e){}")
rec("L03", o1 == ["1", "4", "3", "2"] and o2 == list("AFCEDB") and int(o3[0]) >= 195, f"Node (tệp): {o1}, {''.join(o2)}, hẹn giờ 0 ms chạy sau {o3[0]} ms")


# ── L04: asyncio đối chứng ──
async def l04():
    w = lambda ms: asyncio.sleep(ms / 1000)
    t = time.perf_counter(); await w(100); await w(200); await w(300); a = time.perf_counter() - t
    t = time.perf_counter(); await asyncio.gather(w(100), w(200), w(300)); b = time.perf_counter() - t
    sem = asyncio.Semaphore(2)

    async def job():
        async with sem:
            await w(100)
    t = time.perf_counter(); await asyncio.gather(*(job() for _ in range(5))); c = time.perf_counter() - t
    return a * 1000, b * 1000, c * 1000


a4, b4, c4 = asyncio.run(l04())
rec("L04", 590 <= a4 <= 800 and 295 <= b4 <= 450 and 295 <= c4 <= 450 and math.ceil(5 / 2) * 100 == 300,
    f"asyncio: tuần tự {a4:.0f} ms, đồng thời {b4:.0f} ms, bể 2 cho 5 việc {c4:.0f} ms")


# ── L05: vét cạn tập con giữ nguyên chỗ ──
def brute_moves(old, new):
    pos = [old.index(k) for k in new]
    n = len(pos)
    for keep in range(n, 0, -1):
        for idx in itertools.combinations(range(n), keep):
            if all(pos[idx[i]] < pos[idx[i + 1]] for i in range(keep - 1)):
                return n - keep
    return n


rec("L05", all(brute_moves(list(o), list(n)) == alg.keyed_moves(list(o), list(n)) for o, n in (("ABCDE", "CABDE"), ("ABCD", "BCDA"), ("ABCDE", "EDCBA")))
    and brute_moves(list("ABCDE"), list("CABDE")) == 1 and brute_moves(list("ABCDE"), list("EDCBA")) == 4, "vét cạn: CABDE cần 1, BCDA cần 1, EDCBA cần 4")

# ── L06: sqlite3 với ràng buộc UNIQUE trên khoá lũy đẳng ──
cn = sqlite3.connect(":memory:")
cn.execute("CREATE TABLE don(id INTEGER PRIMARY KEY, khoa TEXT UNIQUE)")
rng = random.Random(1)
for i in range(10_000):
    while True:
        cn.execute("INSERT OR IGNORE INTO don(khoa) VALUES (?)", (f"k{i}",))
        if rng.random() >= 0.02:
            break
with_key = cn.execute("SELECT COUNT(*) FROM don").fetchone()[0]
rec("L06", with_key == 10_000 == alg.api_retry_sim(10_000, 0.02, True) and abs(alg.api_retry_sim(10_000, 0.02) - 10_000 / 0.98) < 3 * math.sqrt(10_000 * 0.02)
    and alg.HTTP_METHODS["PUT"] == (False, True) and alg.HTTP_METHODS["POST"] == (False, False) and alg.HTTP_METHODS["GET"] == (True, True),
    "UNIQUE trên khoá: đúng 10 000 đơn; không khoá ≈ 10 204; GET an toàn + lũy đẳng, PUT lũy đẳng, POST không")

# ── L07: kế hoạch truy vấn của sqlite3 ──
cw = sqlite3.connect(":memory:")
cw.execute("CREATE TABLE t(id INTEGER PRIMARY KEY, v)")
cw.executemany("INSERT INTO t VALUES (?, ?)", ((i, i) for i in range(1, 30001)))
plan_cur = " ".join(r[-1] for r in cw.execute("EXPLAIN QUERY PLAN SELECT id FROM t WHERE id > 19980 ORDER BY id LIMIT 20"))
plan_off = " ".join(r[-1] for r in cw.execute("EXPLAIN QUERY PLAN SELECT id FROM t ORDER BY id LIMIT 20 OFFSET 19980"))
rec("L07", "SEARCH" in plan_cur and "SCAN" in plan_off and alg.offset_page(1000, 20)[0] == alg.offset_page(1000, 20, cursor=True)[0]
    and alg.offset_insert_anomaly() == [41] and alg.offset_insert_anomaly(cursor=True) == [] and (500 - 1) * 50 == 24950,
    f"kế hoạch: con trỏ “{plan_cur}”, độ lệch “{plan_off}”; trùng bản ghi 41 khi chèn giữa hai trang")

# ── L08: bảng luật RFC 9111 viết lại ──
rule = lambda age, ma, e1, e2: "fresh" if age < ma else (304 if e1 == e2 else 200)
cases = [(500, 600, "v7", "v8"), (700, 600, "v7", "v7"), (700, 600, "v7", "v8"), (1800, 3600, "a", "b"), (3700, 3600, "a", "a")]
rec("L08", all(rule(*c) == alg.http_cache_decision(*c) for c in cases) and [rule(*c) for c in cases] == ["fresh", 304, 200, "fresh", 304],
    "tươi / 304 / 200 / tươi / 304")

# ── L09: SHA-256 + base64 thủ công ──
B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
dig = hashlib.sha256(b"dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk").digest()
bits = "".join(f"{b:08b}" for b in dig)
manual = "".join(B64[int(bits[i:i + 6].ljust(6, "0"), 2)] for i in range(0, len(bits), 6))
rec("L09", manual == "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM" == alg.pkce_challenge("dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk")
    and 43 <= len("dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk") <= 128 and base64.urlsafe_b64encode(dig).decode().rstrip("=") == manual,
    "base64url thủ công khớp vector RFC 7636 phụ lục B; chuỗi bí mật dài 43 (trong giới hạn 43–128)")

# ── L10: thời gian tải ──
rec("L10", 2e6 / 200e3 == 10 == alg.load_seconds(2e6, 200e3) and 500e3 / 200e3 == 2.5 and 1.2e6 / 150e3 == 8 and 2.5 * 150 == 375, "10 s → 2,5 s; 8 s; ngân sách 375 KB")


# ── L11: tương phản bằng numpy ──
def contrast_np(a, b):
    def lum(h):
        c = np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)]) / 255.0
        c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
        return float(c @ np.array([0.2126, 0.7152, 0.0722]))
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


pairs = [("777777", "ffffff", 4.48), ("767676", "ffffff", 4.54), ("ffffff", "ff9900", 2.14), ("0066cc", "ffffff", 5.57), ("000000", "ffffff", 21.0)]
rec("L11", all(round(contrast_np(a, b), 2) == v == round(alg.wcag_contrast(a, b), 2) for a, b, v in pairs), "numpy: 4,48 / 4,54 / 2,14 / 5,57 / 21")

# ── L12: ngân sách khung ──
rec("L12", [round(1000 / h, 1) for h in (60, 90, 120)] == [16.7, 11.1, 8.3] and 8.3 < 12 < 16.7 and round(50 / (1000 / 60)) == 3, "16,7 / 11,1 / 8,3 ms; 12 ms mượt ở 60 Hz, khựng ở 120 Hz")

# ── L13: mọi hoán vị thứ tự đến ──
ops = [{"a", "b"}, {"b", "c"}, {"d"}]
res = {frozenset(set().union(*perm)) for perm in itertools.permutations(ops)}
dup = {frozenset(set().union(*(list(perm) + [perm[0]]))) for perm in itertools.permutations(ops)}
rec("L13", res == dup == {frozenset("abcd")} and alg.lww_merge((959, "tên mới"), (1002, "tên cũ"))[1] == "tên cũ" and len({"mua sữa"} | {"gọi mẹ"}) == 2,
    "6 thứ tự (kể cả nhận trùng) đều ra {a, b, c, d}; đồng hồ chậm 5 phút làm ghi sau thắng giữ bản cũ")

# ── L14: Monte Carlo một triệu người dùng ──
rs = np.random.default_rng(14)
old = np.ones(1_000_000, bool)
share = []
for w in range(1, 10):
    old &= rs.random(old.size) >= 0.3
    share.append(old.mean())
rec("L14", abs(share[3] - 0.2401) < 0.002 and abs(share[7] - 0.0576) < 0.001 and share[8] < 0.05 <= share[7] and math.ceil(math.log(0.05) / math.log(0.7)) == 9,
    f"Monte Carlo: sau 4 tuần {share[3]:.4f}, 8 tuần {share[7]:.4f}, 9 tuần {share[8]:.4f} < 5%")


# ── L15: hành trình HTTP — mô phỏng dòng thời gian theo vòng (nguồn: audit/web/sources_L15.md) ──
def rounds_http(n_files, mode):
    """Số vòng khứ hồi để tải 1 tệp trang + (n_files - 1) tệp nhúng, bỏ qua truyền và mã hoá.
    mode: 'per_conn' mỗi tệp một kết nối, lần lượt; 'persist' một kết nối, chờ từng phản hồi; 'pipeline' gửi liền / nhiều luồng."""
    t = 0
    if mode == "per_conn":
        for _ in range(n_files):
            t += 1  # bắt tay giao vận
            t += 1  # yêu cầu → phản hồi
        return t
    t += 1  # bắt tay một lần
    if mode == "persist":
        return t + n_files
    return t + 1 + (1 if n_files > 1 else 0)  # trang, rồi mọi tệp nhúng cùng một vòng


def slow_start_rounds(total, w0):
    sent, w, r = 0, w0, 0
    while sent < total:
        sent, w, r = sent + w, 2 * w, r + 1
    return r


def fifo_finish(times):
    out, t = [], 0
    for x in times:
        t = max(t, x)  # máy chủ xử lý song song nhưng phải trả đúng thứ tự
        out.append(t)
    return out


rec("L15", rounds_http(11, "per_conn") == 22 and 22 * 50 == 1100 and rounds_http(11, "persist") == 12 and rounds_http(11, "pipeline") == 3
    and round(1100 / 150, 1) == 7.3 and fifo_finish([300, 10, 10]) == [300, 300, 300]
    and slow_start_rounds(100 * 500, 10 * 1460) == 3 and slow_start_rounds(500 + 99 * 20, 10 * 1460) == 1
    and 4 * 50 == 200 and rounds_http(31, "per_conn") * 80 == 4960 and rounds_http(31, "pipeline") * 80 == 240
    # khoảng giữa bộ chuẩn ĐẦU TIÊN của mỗi phiên bản: HTTP/1.1 đầu tiên là RFC 2068 (1/1997), không phải RFC 2616 (1999) — sửa 2026-11-08,
    # nguồn rfc-editor.org/rfc/rfc2068.txt (truy cập 2026-11-08); 1.0 (5/1996) → 1.1 (1/1997) = 8 tháng
    and (1997 - 1996) * 12 + 1 - 5 == 8 and (2015 - 1997, 2022 - 2015) == (18, 7),
    "trang 11 tệp: 22 / 12 / 3 vòng (1100 / 600 / 150 ms); chặn đầu hàng 300, 300, 300; tiêu đề 50 000 B: 3 vòng, nén 2480 B: 1 vòng; "
    "mất gói 4 luồng 200 ms vs 50; quiz 31 tệp 4960 → 240 ms")

bad =[c for c, ok in R if not ok]
print(f"\nverify_web: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
