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

bad = [c for c, ok in R if not ok]
print(f"\nverify_bnk:{len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
