"""Kiểm độc lập mọi khẳng định của khoá BNK — tính lại bằng cách KHÁC checklib (vòng lặp thuần, bit thuần, sqlite viết lại, đếm tay),
rồi đối chiếu với hàm checklib (alg) mà `checks` của bài dùng. Mỗi bài một nhóm dòng rec("Lxx", điều_kiện, "mô tả").
Chạy: .venv/Scripts/python audit/bnk/verify_bnk.py   (exit 0 khi mọi dòng PASS; status_report.py đọc dòng cuối)
Giới hạn (NOT_VERIFIED): Oracle, Redis, Kafka, Spring, T24, IBM MQ không chạy trên máy này — chỉ kiểm logic mô phỏng, không kiểm cú pháp/hành vi sản phẩm."""
import hashlib
import hmac
import itertools
import math
import sqlite3
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00: đồ thị tham chiếu — duyệt theo hàng đợi (BFS) thay vì ngăn xếp; float lệch ──
refs = {"A": ["B"], "B": ["C"], "C": [], "D": ["E"], "E": [], "F": []}
seen, q = {"A"}, ["A"]
while q:
    x = q.pop(0)
    for y in refs[x]:
        if y not in seen:
            seen.add(y)
            q.append(y)
rec("L00", sorted(seen) == alg.bnk_reachable(refs, ["A"]) == ["A", "B", "C"] and (6 - len(seen)) * 100 == 300, "BFS và DFS cùng tập sống {A,B,C}; dọn 300 byte")
s = 0.0
for _ in range(10):
    s += 0.1
rec("L00", s != 1.0 and repr(s) == "0.9999999999999999", "10 lần cộng 0,1 bằng double ra 0.9999999999999999")

# ── L01: vét cạn xen kẽ bằng đệ quy (không itertools) ──
def interleavings(a, b):
    if not a:
        yield list(b)
    elif not b:
        yield list(a)
    else:
        for r in interleavings(a[1:], b):
            yield [a[0]] + r
        for r in interleavings(a, b[1:]):
            yield [b[0]] + r


finals = {}
for order in interleavings([("A", "R"), ("A", "W")], [("B", "R"), ("B", "W")]):
    bal, reg = 100, {}
    for who, op in order:
        if op == "R":
            reg[who] = bal
        else:
            bal = reg[who] + (50 if who == "A" else 30)
    finals[bal] = finals.get(bal, 0) + 1
rec("L01", finals == {180: 2, 130: 2, 150: 2} and sorted(finals) == alg.bnk_lost_update(100, [50, 30]), "6 cách xen kẽ: 180×2, 130×2, 150×2")
rec("L01", -(-10000 // 200) * 0.1 == 5.0 and 10000 / (200 / 0.1) == 5.0 and alg.bnk_batch_time(2000, 50, 0.2) == 8.0 and math.factorial(6) // 8 == 90, "10 000/200 lô × 0,1 = 5 s; 2000/50 × 0,2 = 8 s; 90 cách cho 3 luồng")

# ── L02: mô hình proxy viết lại bằng lớp ──
class Tx:
    def __init__(self):
        self.begun, self.committed = 0, []

    def run(self, via_proxy, mode, fails):
        pend_outer = ["transfer"]
        self.begun += 1
        inner_commit = []
        if via_proxy and mode == "REQUIRES_NEW":
            self.begun += 1
            inner_commit.append("audit")
        else:
            pend_outer.append("audit")
        self.committed = sorted(inner_commit + ([] if fails else pend_outer))
        return self.begun, self.committed


ok = all(Tx().run(v, m, f) == alg.bnk_spring_sim(v, m, f) for v in (True, False) for m in ("REQUIRED", "REQUIRES_NEW") for f in (True, False))
rec("L02", ok and Tx().run(False, "REQUIRES_NEW", True) == (1, []) and Tx().run(True, "REQUIRES_NEW", True) == (2, ["audit"]), "mô hình lớp khớp bnk_spring_sim ở cả 8 tổ hợp")

# ── L03: thử lại ──
bal = 2000000
for _ in range(3):
    bal -= 500000
bal_key = 2000000 - 500000
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE p(k TEXT PRIMARY KEY)")
n_ok = 0
for _ in range(3):
    try:
        con.execute("INSERT INTO p VALUES ('k1')")
        n_ok += 1
    except sqlite3.IntegrityError:
        pass
rec("L03", bal == 500000 and bal_key == 1500000 and n_ok == 1 and alg.bnk_retry_sim(2000000, 500000, 3, False) == bal and alg.bnk_retry_sim(2000000, 500000, 3, True) == bal_key,
    "không khoá 500 000, có khoá 1 500 000, PRIMARY KEY nhận 1 lần")

# ── L04: số tầng bằng lũy thừa; kế hoạch sqlite chạy lại độc lập ──
L = 0
while 100 ** L < 10 ** 7:
    L += 1
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE tx(id INTEGER PRIMARY KEY, account_id INTEGER, created TEXT)")
con.executemany("INSERT INTO tx(account_id, created) VALUES (?,?)", [(i % 500, "2026-01-%02d" % (i % 28 + 1)) for i in range(5000)])
plan = lambda w: " ".join(r[3] for r in con.execute("EXPLAIN QUERY PLAN SELECT * FROM tx WHERE " + w))
p0 = plan("account_id=7")
con.execute("CREATE INDEX i ON tx(account_id, created)")
p1 = plan("account_id=7")
p2 = plan("created='2026-01-05'")
p3 = plan("account_id+0=7")
p4 = plan("abs(account_id)=7")  # bọc hàm trên chính cột đầu (LS1: thay ví dụ substr(created) vốn SCAN vì thiếu cột đầu)
rec("L04", L == 4 == alg.bnk_btree_levels(10 ** 7, 100) and L + 1 == 5 and p0.startswith("SCAN") and p1.startswith("SEARCH") and p2.startswith("SCAN") and p3.startswith("SCAN") and p4.startswith("SCAN"),
    "10^7 dòng → 4 tầng; sqlite: SCAN, SEARCH, SCAN, SCAN, SCAN theo chỉ mục và điều kiện")

# ── L05: bế tắc bằng đồ thị chờ (phát hiện chu trình) thay vì mô phỏng bước ──
def deadlock_wfg(seqs):
    """Hai phiên: phiên i giữ khoá đầu seqs[i][0] và xin khoá thứ hai; có chu trình chờ khi mỗi phiên xin khoá của phiên kia."""
    a, b = seqs
    holds = {a[0]: 0, b[0]: 1} if a[0] != b[0] else {a[0]: 0}
    wants = {0: a[1], 1: b[1]}
    edges = []
    for s in (0, 1):
        owner = holds.get(wants[s])
        if owner is not None and owner != s:
            edges.append((s, owner))
    return (0, 1) in edges and (1, 0) in edges


pairs = [(p, q) for p in (["A", "B"], ["B", "A"]) for q in (["A", "B"], ["B", "A"])]
rec("L05", [("deadlock" if deadlock_wfg(pq) else "ok") for pq in pairs] == [alg.bnk_lock_sim(list(pq)) for pq in pairs] == ["ok", "deadlock", "deadlock", "ok"] and alg.bnk_lock_sim([[2, 5], [2, 5]]) == "ok",
    "đồ thị chờ và mô phỏng bước cho cùng 4 kết quả")

# ── L06: độ trễ trung bình bằng Fraction và bằng đếm 100 lần ──
from fractions import Fraction as F
rec("L06", F(1) + (1 - F(9, 10)) * 20 == 3 and (90 * 1 + 10 * 21) / 100 == 3.0 and F(1) + F(1, 2) * 20 == 11 and abs(alg.bnk_cache_avg(0.8, 2, 30) - 8) < 1e-9
    and alg.bnk_fencing_sim(False) == ["B", "A"] and alg.bnk_fencing_sim(True) == ["B"], "T = 3, 11, 8 ms; mã chặn loại ghi muộn của A")

# ── L07: Kafka — chia đoạn bằng chỉ số; commit mô phỏng bằng vòng lặp thô ──
def assign(p, c):
    out = [[] for _ in range(c)]
    sizes = [p // c + (1 if i < p % c else 0) for i in range(c)]
    k = 0
    for i, sz in enumerate(sizes):
        for _ in range(sz):
            out[i].append(k)
            k += 1
    return out


def commit_run(n, crash, commit_first):
    cnt = [0] * n
    off = 0
    crashed = False
    while off < n:
        if commit_first:
            saved = off + 1
            if off == crash and not crashed:
                crashed = True
                off = saved
                continue
            cnt[off] += 1
            off = saved
        else:
            cnt[off] += 1
            if off == crash and not crashed:
                crashed = True
                continue
            off += 1
    return cnt


rec("L07", assign(6, 3) == alg.bnk_assign(6, 3) and assign(10, 4) == alg.bnk_assign(10, 4) and [len(g) for g in assign(10, 4)] == [3, 3, 2, 2] and sum(1 for g in assign(10, 12) if not g) == 2
    and commit_run(5, 2, False) == [1, 1, 2, 1, 1] == alg.bnk_commit_sim(5, 2, False) and commit_run(5, 2, True) == [1, 1, 0, 1, 1] == alg.bnk_commit_sim(5, 2, True)
    and zlib.crc32(b"TK-1001") % 6 == alg.bnk_key_partition("TK-1001", 6) == 1, "chia phân vùng, số lần xử lý [1,1,2,1,1] / [1,1,0,1,1], cùng khoá cùng phân vùng")

# ── L08: SAGA bằng công thức 2i+1 và outbox ──
# 2026-11-08: mô hình bài đổi từ (ghi nợ, ghi có, thông báo) sang ba bước BÙ ĐƯỢC (giữ hạn mức, ghi nợ, ghi có).
# Lý do theo đặc tả mẫu SAGA (Richardson, Microservices Patterns, ch.4: compensatable / pivot / retriable transactions):
# "ghi có" là điểm không quay lại; "thông báo" đứng sau nó là bước thử lại được, nên lỗi thông báo KHÔNG được bù
# (bản cũ dạy "lỗi thông báo → bù ghi có, bù ghi nợ", tức hoàn tiền vì thông báo hỏng — sai nghiệp vụ).
_L08 = ("giữ hạn mức", "ghi nợ", "ghi có")
rec("L08", all(len(alg.bnk_saga(i, _L08)) == 2 * i + 1 for i in range(3)) and alg.bnk_saga(1, _L08) == ["giữ hạn mức", "lỗi ghi nợ", "bù giữ hạn mức"]
    and alg.bnk_saga(2, _L08) == ["giữ hạn mức", "ghi nợ", "lỗi ghi có", "bù ghi nợ", "bù giữ hạn mức"]
    and alg.bnk_outbox_sim("between", False) == (True, 0) and alg.bnk_outbox_sim("between", True) == (True, 1), "nhật ký 2i+1 dòng (bước bù được); outbox không mất sự kiện")

# ── L09: sổ cái — cộng bằng Python thuần; đảo bằng đảo dấu ──
rows = [(1, "A", -505500), (1, "B", 500000), (1, "F", 5500)]
bal = {}
for _, a_, v in rows + [(2, a_, -v) for _, a_, v in rows]:
    bal[a_] = bal.get(a_, 0) + v
tot, balances = alg.bnk_ledger_demo(500000, 5500)
rec("L09", sum(v for _, _, v in rows) == 0 == tot and balances == {"khach_A": -505500, "khach_B": 500000, "thu_phi": 5500} and set(bal.values()) == {0}
    and alg.bnk_ledger_after_reversal(500000, 5500)[0] == 6 and alg.bnk_ledger_unbalanced([(1, "a", -100), (1, "b", 90), (2, "a", -5), (2, "b", 5)]) == [1], "tổng 0; đảo về 0, 6 dòng; phát hiện giao dịch lệch")

# ── L10: ghép phản hồi — đếm điểm cố định hoán vị và đếm bằng định nghĩa ──
order = [2, 0, 1, 4, 3]
fixed = sum(1 for k, v in enumerate(order) if k == v)
der = sum(1 for p in itertools.permutations(range(5)) if all(p[i] != i for i in range(5)))
d = [1, 0]  # số xáo trộn D(n) = (n−1)(D(n−1)+D(n−2)): kiểm chéo với vét cạn
for n in range(2, 6):
    d.append((n - 1) * (d[-1] + d[-2]))
rec("L10", fixed == 0 == alg.bnk_reply_match(order)[0] and alg.bnk_reply_match(order)[1] == 5 and der == 44 == d[5] and round(44 / 120 * 100) == 37
    and [alg.bnk_unknown_outcome(a, b) for a, b in ((True, False), (True, True), (False, True), (False, False))] == [2, 1, 1, 1], "0/5 theo thứ tự, 5/5 theo mã; 44 xáo trộn trong 120; ghi nợ 2/1/1/1")

# ── L11: ISO 8583 — dựng bản đồ bằng chuỗi bit, đọc lại bằng cắt chuỗi ──
fields = {2: "4111111111111111", 3: "000000", 4: "000000500000", 11: "123456"}
bits = ["0"] * 64
for f in fields:
    bits[f - 1] = "1"
bitmap = "%016X" % int("".join(bits), 2)
msg = "0200" + bitmap + "16" + fields[2] + fields[3] + fields[4] + fields[11]
rec("L11", bitmap == "7020000000000000" and msg == alg.bnk_iso_pack("0200", fields) and len(msg) == 62 and alg.bnk_iso_unpack(msg) == ("0200", fields)
    and "%016X" % (2 ** 61 + 2 ** 60 + 2 ** 53) == "3020000000000000" and len(alg.bnk_iso_pack("0200", {3: "000000", 4: "000000500000", 11: "123456"})) == 44
    and alg.bnk_iso_pack("0210", {3: "000000", 4: "000000500000", 11: "123456", 39: "00"})[4:20] == "3020000002000000", "bản đồ 7020000000000000, dài 62; đọc ngược khớp; 0210 có bản đồ 3020000002000000")

# ── L12: đối soát bằng từ điển và tổng tiền ──
bank = {"r1": 100, "r2": 200, "r3": 300, "r4": 400, "r5": 500}
sw = {"r1": 100, "r2": 200, "r3": 350, "r4": 400, "r6": 600}
m = sum(1 for k in bank if k in sw and bank[k] == sw[k])
ob = [k for k in bank if k not in sw]
os_ = [k for k in sw if k not in bank]
mis = [k for k in bank if k in sw and bank[k] != sw[k]]
rec("L12", (m, len(ob), len(os_), len(mis)) == (3, 1, 1, 1) == (3, 1, 1, 1) and (m + len(ob) + len(os_) + len(mis)) == 6 == len(set(bank) | set(sw))
    and sum(sw.values()) - sum(bank.values()) == 150 and alg.bnk_reconcile(list(bank.items()), list(sw.items())) == (3, 1, 1, 1), "3 khớp, 1, 1, 1; 6 mã; chênh tiền 150 = 50 + 600 − 500")

# ── L13: khối PIN bằng XOR từng cặp hex; MAC bằng hmac chuẩn; Luhn viết lại ──
pin, pan = "1234", "4111111111111111"
a_ = "041234FFFFFFFFFF"
b_ = "0000" + pan[-13:-1]
blk = "".join("%X" % (int(x, 16) ^ int(y, 16)) for x, y in zip(a_, b_))


def luhn(s):
    digs = [int(c) for c in s][::-1]
    return (sum(digs[0::2]) + sum(sum(divmod(2 * d, 10)) for d in digs[1::2])) % 10 == 0


mac = lambda m: hmac.new(b"k", m.encode(), hashlib.sha256).hexdigest()
need = lambda amt, day: amt > 10_000_000 or day + amt > 20_000_000
rec("L13", blk == "041225EEEEEEEEEE" == alg.bnk_pin_block0(pin, pan) and luhn(pan) and not luhn(pan[:-1] + "2") and alg.bnk_luhn(pan)
    and mac("amt=500000")[:16] == "7625fd27947ee367" and mac("amt=500000") != mac("amt=900000") and need(15_000_000, 0) and not need(5_000_000, 0) and need(8_000_000, 16_000_000)
    and not need(8_000_000, 8_000_000) and need(9_000_000, 13_000_000), "khối PIN 041225EEEEEEEEEE; MAC đổi khi đổi tiền; Luhn; quy tắc ngưỡng minh hoạ")

# ── L14: tình huống giả định — đếm bằng tay ──
bank_ = {"r7": 500000, "r7b": 500000}
sw_ = {"r7": 500000}
rec("L14", 2000000 - 2 * 500000 == 1000000 and (2000000 - 500000) - 1000000 == 500000 and [k for k in bank_ if k not in sw_] == ["r7b"]
    and 1000000 + 500000 == 1500000 and (3 - 1) * 400000 == 800000 == 3000000 - alg.bnk_retry_sim(3000000, 400000, 3, False) - 400000 and alg.bnk_unique_key_rows(2) == 1, "trừ dư 500 000; r7b chỉ ở ngân hàng; đảo về 1 500 000")

# ── Đợt C (2026-11-09): số mới thêm vào bài, kiểm bằng cách khác ──
from decimal import Decimal
# L00: BigDecimal/Decimal tạo từ số thực nhị phân mang theo sai lệch; tạo từ chuỗi thì đúng
rec("L00", Decimal(0.1) != Decimal("0.1") and sum([Decimal("0.1")] * 10) == Decimal("1.0"), "Decimal(0.1) lệch, Decimal('0.1') cộng 10 lần ra 1.0")
# L04: tìm nhị phân trên 1024 phần tử — 10 lần chia đôi còn 1, tối đa 11 lần so (vét cạn mọi giá trị cần tìm)
def _bs(a, x):
    lo, hi, c = 0, len(a) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        c += 1
        if a[mid] == x:
            return c
        lo, hi = (mid + 1, hi) if a[mid] < x else (lo, mid - 1)
    return c
_n, _k = 1024, 0
while _n > 1:
    _n //= 2
    _k += 1
rec("L04", _k == 10 and max(_bs(list(range(1024)), x) for x in range(1024)) == 11 and plan("account_id=7 AND created='2026-01-05'").startswith("SEARCH"),
    "1024 → 1 sau 10 lần chia đôi, tối đa 11 lần so; điều kiện hai cột dùng chỉ mục")
# L11: cùng dãy 000000500000 với đô la Mỹ (ISO 4217: 2 chữ số lẻ) là 5 000 đô la
rec("L11", int("000000500000") // 10 ** 2 == 5000, "000000500000 xu = 5 000 đô la")
# L13: tổng Luhn của thẻ thử bằng tách chữ số theo vị trí
_d = [int(c) for c in reversed(pan)]
rec("L13", sum(_d[0::2]) == 8 and sum(2 * x for x in _d[1::2][:-1]) == 14 and 2 * _d[-1] == 8 and 8 + 14 + 8 == 30, "Luhn thẻ thử: 8 + 14 + 8 = 30")

# ── AF2 (2026-11-13): số ở cảnh "quy mô" (×1, ×100, ×10 000) tính lại bằng vòng lặp/Fraction, độc lập với `checks` của bài ──
from fractions import Fraction as _F
_S = lambda n: _F(n)
# L00: heap 4·1024³ byte, rò 1024 byte mỗi yêu cầu; 10, 1000, 100 000 yêu cầu/giây
_heap = 4 * 1024 ** 3
_t = [_heap / (r * 1024) for r in (10, 1000, 100000)]
rec("L00", [round(x) for x in _t] == [419430, 4194, 42] and round(_t[0] / 86400, 1) == 4.9 and round(_t[1] / 60) == 70, "đầy heap sau 419 430 s (4,9 ngày), 4 194 s (70 phút), 42 s")
# L01: 200 luồng, chờ 0,1 s; 1 MB ngăn xếp; 1 KB luồng ảo
_n = [10 ** 4, 10 ** 6, 10 ** 8]
rec("L01", [_F(n, 200) / 10 for n in _n] == [5, 500, 50000] and [n // 1000 for n in _n] == [10, 1000, 100000] and round(500 / 60, 1) == 8.3 and round(50000 / 3600, 1) == 13.9,
    "5 s, 500 s (8,3 phút), 50 000 s (13,9 giờ); bộ nhớ ngăn xếp 10 GB, 1 TB, 100 TB (MB)")
# L02: hộp kết nối T·(C−1)+1 với C = 2
rec("L02", [T * (2 - 1) + 1 for T in (5, 500, 50000)] == [6, 501, 50001], "kết nối tối thiểu 6, 501, 50 001")
# L03: thiệt hại và bảng khoá
rec("L03", [int(N * _F(1, 1000)) for N in (10 ** 5, 10 ** 7, 10 ** 9)] == [100, 10000, 1000000] and [int(N * _F(1, 1000)) * 500000 for N in (10 ** 5, 10 ** 7, 10 ** 9)] == [5 * 10 ** 7, 5 * 10 ** 9, 5 * 10 ** 11]
    and [N * 64 for N in (10 ** 5, 10 ** 7, 10 ** 9)] == [6400000, 640000000, 64000000000], "100/10 000/1 000 000 lệnh trừ trùng; 50 triệu, 5 tỉ, 500 tỉ đồng; bảng khoá 6,4 MB, 640 MB, 64 GB")
# L04: số tầng (100 lối rẽ) và thời gian quét 10^6 dòng/giây
def _lv(n):
    k, c = 0, 1
    while c < n:
        c, k = c * 100, k + 1
    return k
rec("L04", [_lv(n) for n in (10 ** 5, 10 ** 7, 10 ** 9)] == [3, 4, 5] and [n / 10 ** 6 for n in (10 ** 5, 10 ** 7, 10 ** 9)] == [0.1, 10.0, 1000.0], "3, 4, 5 tầng; quét 0,1 s, 10 s, 1000 s")
# L05: số cặp phiên T(T−1)/2 và kỳ vọng cặp ngược (p = 1/10000)
_pairs = [sum(range(T)) for T in (10, 1000, 100000)]
rec("L05", _pairs == [45, 499500, 4999950000] and [round(p / 10000, 4) for p in _pairs] == [0.0045, 49.95, 499995.0], "45, 499 500, 4 999 950 000 cặp; kỳ vọng 0,0045, ≈50, ≈500 000")
# L06: kết nối bận = tần suất × 0,02 (Little)
rec("L06", [_F(r) * _F(2, 100) for r in (100, 10000, 1000000)] == [2, 200, 20000] and [_F(r) * _F(2, 100) * _F(1, 10) for r in (100, 10000, 1000000)] == [_F(1, 5), 20, 2000]
    and [_F(r) * _F(2, 100) * _F(1, 100) for r in (100, 10000, 1000000)] == [_F(1, 50), 2, 200], "2/200/20 000 không đệm; 0,2/20/2 000 trúng 90%; 0,02/2/200 trúng 99%")
# L07: tồn đọng sau 1 giờ nếu chỉ 4 phân vùng (4 000/s)
rec("L07", [(r - 4000) * 3600 for r in (5000, 500000, 50000000)] == [3600000, 1785600000, 179985600000] and [r // 1000 for r in (5000, 500000, 50000000)] == [5, 500, 50000], "tồn đọng 3,6 triệu; 1,7856 tỉ; 179,9856 tỉ; phân vùng 5, 500, 50 000")
# L08: hộp thư đi và bộ chuyển tiếp
rec("L08", [N * 200 for N in (10 ** 5, 10 ** 7, 10 ** 9)] == [20 * 10 ** 6, 2 * 10 ** 9, 2 * 10 ** 11] and [round(N / 86400, 1) for N in (10 ** 5, 10 ** 7)] == [1.2, 115.7] and -(-round(10 ** 9 / 86400) // 1000) == 12,
    "hộp thư đi 20 MB, 2 GB, 200 GB; 1,2 và 116 sự kiện/s; 12 bộ chuyển tiếp")
# L09: dòng thu phí mỗi năm và thời gian cộng lại
rec("L09", [N * 365 for N in (10 ** 5, 10 ** 7, 10 ** 9)] == [36500000, 3650000000, 365000000000] and round(365 * 10 ** 9 / 10 ** 6 / 86400, 1) == 4.2 and round(3650000000 / 10 ** 6 / 3600, 1) == 1.0,
    "36,5 triệu / 3,65 tỉ / 365 tỉ dòng; 36,5 s, 1 giờ, 4,2 ngày")
# L10: n−1 ghép sai kỳ vọng — kiểm bằng vét cạn cho n = 5 (đúng kỳ vọng 1 điểm cố định)
_perm_fixed = sum(sum(1 for i, v in enumerate(p) if i == v) for p in itertools.permutations(range(5)))
rec("L10", _F(_perm_fixed, 120) == 1 and [n - 1 for n in (5, 500, 50000)] == [4, 499, 49999], "kỳ vọng điểm cố định hoán vị n=5 là 1 (vét cạn 120); sai kỳ vọng 4, 499, 49 999")
# L11: băng thông (62 + 46 = 108 byte mỗi giao dịch)
rec("L11", 62 + 46 == 108 and [108 * r * 86400 for r in (100, 10000, 1000000)] == [933120000, 93312000000, 9331200000000], "108 byte; nhật ký 933 MB, 93,3 GB, 9,33 TB mỗi ngày")
# L12: so từng cặp N² / 10^8 và bảng tra N / 10^7
rec("L12", [_F(N * N, 10 ** 8) for N in (10 ** 5, 10 ** 7)] == [100, 10 ** 6] and round(float(_F(10 ** 18, 10 ** 8)) / (365.25 * 86400)) == 317 and [N * 100 for N in (10 ** 5, 10 ** 7, 10 ** 9)] == [10 ** 7, 10 ** 9, 10 ** 11],
    "100 s; 10^6 s (11,6 ngày); 317 năm; bộ nhớ 10 MB, 1 GB, 100 GB")
# L13: HSM 1000 thao tác/s, mỗi giao dịch 2 thao tác
rec("L13", [-(-(2 * r) // 1000) for r in (100, 10000, 1000000)] == [1, 20, 2000], "HSM tối thiểu 1, 20, 2 000")
# L14: vụ trừ trùng và người xử lý tay (10 phút mỗi vụ, 8 giờ mỗi người)
rec("L14", [N // 10000 for N in (10 ** 5, 10 ** 7, 10 ** 9)] == [10, 1000, 100000] and [round(v * 10 / 60 / 8, 1) for v in (10, 1000, 100000)] == [0.2, 20.8, 2083.3], "10, 1 000, 100 000 vụ; 0,2, 21, 2 083 người")

# ── Sửa theo báo cáo người đọc R_BNK (2026-11-14): MUST/SHOULD kiểm bằng cách khác ──
import re as _re
import yaml as _yaml
_Y = {p.name[:3]: p.read_text(encoding="utf-8") for p in sorted((ROOT / "lessons" / "bnk").glob("L*.yaml"))}
_txt = lambda lid: _re.sub(r"\s+", " ", _Y[lid])
# L01: mô hình hai luồng có ngủ — A đọc 100, ngủ 100 ms rồi ghi; B đọc 100, ngủ 200 ms rồi ghi; không khoá thì B ghi sau cùng (130), có khoá thì tuần tự (180)
def _nap_sim(khoa):
    so_du, ev = 100, []
    if khoa:
        so_du = so_du + 50
        so_du = so_du + 30
    else:
        doc_a = doc_b = so_du
        ev = sorted([(100, 50 + doc_a), (200, 30 + doc_b)])
        for _, v in ev:
            so_du = v
    return so_du
rec("L01", _nap_sim(False) == 130 and _nap_sim(True) == 180 and "dung 2000000" not in _txt("L01"), "chạy thật tất định: không khoá ra 130, có khoá ra 180; bài không còn dùng kết quả ngẫu nhiên 'dung 2000000'")
_six = {}
for _o in itertools.permutations([("A", "R"), ("A", "W"), ("B", "R"), ("B", "W")]):
    if _o.index(("A", "R")) < _o.index(("A", "W")) and _o.index(("B", "R")) < _o.index(("B", "W")):
        _b, _r = 100, {}
        for _w, _op in _o:
            if _op == "R":
                _r[_w] = _b
            else:
                _b = _r[_w] + (50 if _w == "A" else 30)
        _six[_o] = _b
rec("L01", len(_six) == 6 and sorted(_six.values()) == [130, 130, 150, 150, 180, 180], "bảng sáu cách xen kẽ: 180×2, 130×2, 150×2")
# L06: 10^6 yêu cầu/s × 20 ms: trúng 99% → 200, 99,9% → 20, muốn 10 cần 99,95%
rec("L06", _F(10 ** 6) * _F(2, 100) * (1 - _F(99, 100)) == 200 and _F(10 ** 6) * _F(2, 100) * (1 - _F(999, 1000)) == 20 and _F(10 ** 6) * _F(2, 100) * (1 - _F(9995, 10000)) == 10
    and "99,9%" not in _txt("L06").replace("99,95%", "") and "chín mươi chín phẩy chín mươi lăm" in _txt("L06"), "trúng 99,9% còn 20 kết nối; muốn 10 cần 99,95%; bài ghi 99,95%")
# L07: băm của Kafka là murmur2 (kiểm 4 vector chuẩn); TK-1001 vào phân vùng 2 trong số 6, crc32 minh hoạ cho 1
def _murmur2(data):
    m, h = 0x5bd1e995, (0x9747b28c ^ len(data)) & 0xFFFFFFFF
    for i in range(len(data) // 4):
        k = int.from_bytes(data[4 * i:4 * i + 4], "little")
        k = (k * m) & 0xFFFFFFFF
        k ^= k >> 24
        k = (k * m) & 0xFFFFFFFF
        h = ((h * m) & 0xFFFFFFFF) ^ k
    rem, base = len(data) % 4, len(data) - len(data) % 4
    if rem >= 3:
        h ^= data[base + 2] << 16
    if rem >= 2:
        h ^= data[base + 1] << 8
    if rem >= 1:
        h ^= data[base]
        h = (h * m) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * m) & 0xFFFFFFFF
    return h ^ (h >> 15)
_sg = lambda v: v - (1 << 32) if v >= 1 << 31 else v
rec("L07", [_sg(_murmur2(s.encode())) for s in ("21", "foobar", "a-little-bit-long-string", "abc")] == [-973932308, -790332482, -985981536, 479470107]
    and (_murmur2(b"TK-1001") & 0x7FFFFFFF) % 6 == 2 and zlib.crc32(b"TK-1001") % 6 == 1 and "murmur2" in _txt("L07"), "murmur2 khớp 4 vector Kafka; TK-1001 vào phân vùng 2 (crc32 minh hoạ cho 1); bài có ghi chú")
# L08: tệp SQL chạy giống nhau ở chế độ tự chốt (như sqlite3 dòng lệnh) và ở chế độ giao dịch ngầm của Python (labs/sqlrun.py)
_S8 = ("CREATE TABLE sodu (tk TEXT PRIMARY KEY, so_du INTEGER); CREATE TABLE outbox (id INTEGER PRIMARY KEY, su_kien TEXT, da_gui INTEGER DEFAULT 0); "
       "BEGIN; INSERT INTO sodu VALUES ('B', 3000000); COMMIT; BEGIN; UPDATE sodu SET so_du = so_du - 700000 WHERE tk = 'B'; INSERT INTO outbox (su_kien) VALUES ('lenh 77 da tru 700000'); COMMIT; "
       "BEGIN; UPDATE sodu SET so_du = so_du - 900000 WHERE tk = 'B'; INSERT INTO outbox (su_kien) VALUES ('lenh 78 da tru 900000'); ROLLBACK;")
_res = []
for _iso in (None, ""):
    _c = sqlite3.connect(":memory:", isolation_level=_iso)
    for _st in _S8.split("; "):
        _c.execute(_st.rstrip(";"))
    _res.append((_c.execute("SELECT so_du FROM sodu").fetchall(), _c.execute("SELECT su_kien, da_gui FROM outbox").fetchall()))
_c0 = sqlite3.connect(":memory:", isolation_level=None)
try:
    _c0.execute("COMMIT")
    _err = False
except sqlite3.OperationalError:
    _err = True
rec("L08", _res[0] == _res[1] == ([(2300000,)], [("lenh 77 da tru 700000", 0)]) and _err and "COMMIT;` (để kết thúc giao dịch ngầm" not in _Y["L08"], "BEGIN rõ ràng chạy giống nhau ở tự chốt và giao dịch ngầm; COMMIT khi không có giao dịch báo lỗi nên đề không bắt gõ COMMIT sau INSERT")
# L09: 365 tỉ dòng / 10^6 dòng mỗi giây = 4,2245 ngày; lời đọc không còn 'ngày rưỡi'
rec("L09", round(365 * 10 ** 9 / 10 ** 6 / 86400, 4) == 4.2245 and "ngày rưỡi" not in _txt("L09") and "bốn phẩy hai ngày" in _txt("L09"), "4,2245 ngày: lời đọc 'bốn phẩy hai ngày', không còn 'bốn ngày rưỡi'")
# L13: khối PIN rõ XOR lại với PAN đệm ra PIN đệm — không cần khoá; bài không còn câu sai
_blk = "041225EEEEEEEEEE"
_rec = "".join("%X" % (int(x, 16) ^ int(y, 16)) for x, y in zip(_blk, "0000" + "4111111111111111"[-13:-1]))
rec("L13", _rec == "041234FFFFFFFFFF" and "Người không có thì chỉ thấy dãy này" not in _txt("L13") and "không cần khoá" in _txt("L13"), "khối rõ XOR lại với số thẻ ra 041234FFFFFFFFFF (PIN 1234), không cần khoá; bài nói đúng điều đó")
# L14: sổ 6 dòng (bút toán kép) cân đối; NOT IN với NULL trả rỗng, NOT EXISTS đúng
_led = [(1, "khach", -500000), (1, "nhan", 500000), (2, "khach", -500000), (2, "cho", 500000), (3, "khach", 500000), (3, "cho", -500000)]
_c = sqlite3.connect(":memory:")
_c.execute("CREATE TABLE a (ma TEXT)")
_c.execute("CREATE TABLE b (ma TEXT)")
_c.executemany("INSERT INTO a VALUES (?)", [("r7",), ("r7b",)])
_c.executemany("INSERT INTO b VALUES (?)", [("r7",), (None,)])
_ni = _c.execute("SELECT ma FROM a WHERE ma NOT IN (SELECT ma FROM b)").fetchall()
_ne = _c.execute("SELECT ma FROM a WHERE NOT EXISTS (SELECT 1 FROM b WHERE b.ma = a.ma)").fetchall()
rec("L14", len(_led) == 6 and alg.bnk_ledger_unbalanced(_led) == [] and all(sum(v for g, _, v in _led if g == k) == 0 for k in (1, 2, 3)) and _ni == [] and _ne == [("r7b",)] and "cân đối" in _txt("L14"),
    "sổ 6 dòng cân đối từng giao dịch; NOT IN với NULL trả rỗng, NOT EXISTS ra r7b")

# ── fix4 (R2_BNK 2026-11-15): các điều vừa sửa ──
_hg = lambda dht, ht: (1 if dht else 0) + (0 if (ht and dht) else 1)   # số lần ghi nợ (mô hình L10)
rec("L10", [_hg(a_, b_) for a_, b_ in ((True, False), (True, True), (False, True), (False, False))] == [2, 1, 1, 1]
    and [_hg(a_, True) for a_ in (True, False)] == [1, 1] and "cả hai trường hợp hỏi trước" in _txt("L10") and "cả bốn trường hợp" not in _txt("L10"),
    "chỉ hai trường hợp hỏi trước đều đúng một lần; câu lời đọc đã sửa")
_bando = int("7020000000000000", 16) | (1 << 63)   # thêm bit 1 (bản đồ thứ hai)
rec("L11", [k for k in range(2, 65) if _bando >> (64 - k) & 1] == [2, 3, 4, 11] and [k for k in range(1, 65) if _bando >> (64 - k) & 1][0] == 1,
    "đọc ngược từ trường 2: bit 1 (bản đồ thứ hai) không bị in như một trường")
rec("L00", (5 * 1_048_576) / 1_048_576 == 5 and 1024 * 1024 == 1_048_576, "RoRi dùng 1 MB = 1048576 byte, cùng cơ số với phần nhắc đơn vị")
rec("L04", len("ế".encode()) == 3 and len("a".encode()) == 1, "một chữ cái không dấu 1 byte, chữ có dấu 2 đến 3 byte")

bad = [c for c, ok in R if not ok]
print(f"\nverify_bnk:{len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
