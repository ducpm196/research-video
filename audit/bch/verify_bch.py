"""Kiểm độc lập mọi khẳng định của khoá BCH — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Chuỗi băm: hashlib trực tiếp, kẻ sửa tính lại toàn bộ. Merkle: dựng đệ quy. RSA đồ chơi: khoá bí mật suy từ nghịch đảo mô-đun. Đồng chưa tiêu: vét cạn
tập con. Bằng chứng công việc: đếm bit 0 bằng chuỗi nhị phân + Monte Carlo trung bình số lần thử. Nakamoto: mô phỏng cuộc đua khối. Hai phần ba:
vét cạn giao của mọi cặp tập đủ phiếu. Gọi lại: mô phỏng bằng lớp đối tượng có hàm nhận gọi lại. Trung vị: tìm kiếm đối kháng ngẫu nhiên.
Chạy: .venv/Scripts/python audit/bch/verify_bch.py"""
import hashlib
import itertools
import math
import random
import statistics
import sys
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


sha = lambda b: hashlib.sha256(b).hexdigest()

# ── L00: bốn câu hỏi quyết định (Wüst & Gervais 2018, rút gọn) ──
need = lambda state, writers, ttp, trust: state and writers and not ttp and not trust
rec("L00", not need(True, True, True, False) and need(True, True, False, False) and not need(True, False, False, False),
    "trường đại học (có bên tin cậy) → không cần; năm công ty đối thủ → có thể cần")

# ── L01: hashlib trực tiếp ──
D0 = ["khối 0", "A trả B 5", "B trả C 2", "C trả A 1"]
H, p = [], "0" * 64
for d in D0:
    p = sha((p + "|" + d).encode()); H.append(p)
D2 = list(D0); D2[2] = "B trả C 20"
H_full, p = [], "0" * 64
for d in D2:
    p = sha((p + "|" + d).encode()); H_full.append(p)
rec("L01", H == alg.build_chain(D0) and [h[:8] for h in H] == ["7532f7b2", "fb7c50f3", "adc720a0", "febb5dfe"] and alg.first_bad_block(D2, H) == 2
    and alg.first_bad_block(D2, H_full) is None and sum(a != b for a, b in zip(H, H_full)) == 2,
    "hashlib: mã khớp; sửa khối 3 lộ ở khối 3; kẻ sửa tính lại toàn bộ thì đổi 2 mã cuối — mọi bản sao cũ vẫn giữ mã cũ")


# ── L02: Merkle đệ quy ──
def root_rec(leaves):
    if len(leaves) == 1:
        return hashlib.sha256(leaves[0]).digest()
    m = len(leaves) // 2
    return hashlib.sha256(root_rec(leaves[:m]) + root_rec(leaves[m:])).digest()


leaves = [f"gd{i}".encode() for i in range(1024)]
L = alg.merkle_levels(leaves)
rec("L02", root_rec(leaves) == L[-1][0] and alg.merkle_verify(b"gd357", 357, alg.merkle_proof(L, 357), root_rec(leaves))
    and not alg.merkle_verify(b"gd357x", 357, alg.merkle_proof(L, 357), root_rec(leaves)) and len(alg.merkle_proof(L, 357)) == 10 == int(math.log2(1024))
    and math.ceil(math.log2(10 ** 6)) == 20, "gốc đệ quy khớp; bằng chứng 10 mã đúng, sửa giao dịch thì sai; 10⁶ giao dịch cần 20 mã")

# ── L03: khoá bí mật suy từ nghịch đảo mô-đun ──
phi = (61 - 1) * (53 - 1)
d_inv = pow(17, -1, phi)
h5 = int(sha("A trả B 5".encode()), 16) % 3233
rec("L03", d_inv == 2753 and h5 == 3010 and pow(h5, d_inv, 3233) == 2164 == alg.toy_rsa_sign("A trả B 5") and pow(2164, 17, 3233) == h5
    and int(sha("A trả B 50".encode()), 16) % 3233 == 2441 and all(pow(pow(m, 2753, 3233), 17, 3233) == m for m in range(3233)),
    "d = 17⁻¹ mod 3120 = 2753; ký 3010 → 2164; kiểm đúng; sửa thành 50 → băm 2441; ký rồi kiểm đúng với MỌI m < 3233")


# ── L04: vét cạn tập con ──
def best_subset(coins, need):
    best = None
    for r in range(1, len(coins) + 1):
        for sub in itertools.combinations(coins, r):
            if sum(sub) >= need and (best is None or (len(sub), sum(sub)) < (len(best), sum(best))):
                best = sub
    return best


rec("L04", sorted(best_subset([5, 3, 2], 6.1)) == [2, 5] and alg.utxo_select([5, 3, 2], 6, 0.1)[0] == [5, 3] and round(8 - 6 - 0.1, 1) == 1.9 and round(7 - 6 - 0.1, 1) == 0.9
    and sorted(best_subset([4, 4, 1], 7.7)) == [4, 4] and round(8 - 7.5 - 0.2, 1) == 0.3,
    "vét cạn: ví chọn lớn trước dùng {5, 3}, thừa 1,9; cách ít tiền thừa nhất là {5, 2}, thừa 0,9 (bài đã nêu cả hai); đủ 7,7 chỉ có {4, 4}, thừa 0,3")


# ── L05: đếm bit 0 + Monte Carlo trung bình ──
def lead_zeros(b):
    return len(bin(int.from_bytes(b, "big"))[2:].zfill(256)) - len(bin(int.from_bytes(b, "big"))[2:].zfill(256).lstrip("0"))


n = 0
while lead_zeros(hashlib.sha256(b"khoi-1|" + str(n).encode()).digest()) < 16:
    n += 1
trials = [alg.pow_mine(f"mc-{k}".encode(), 10) for k in range(300)]
rec("L05", n + 1 == 50845 == alg.pow_mine(b"khoi-1", 16) and abs(statistics.mean(trials) - 1024) < 3 * 1024 / math.sqrt(300)
    and round((1 - 2 ** -16) ** 65536, 4) == round(math.exp(-1), 4) == 0.3679,
    f"đếm bit tay: trúng ở lần 50 845; Monte Carlo 300 khối 10 bit: trung bình {statistics.mean(trials):.0f} ≈ 1024")


# ── L06: mô phỏng cuộc đua (đúng giả định mục 11 của Nakamoto) ──
def race(q, z, trials=200_000, seed=6, cap=60):
    rng = random.Random(seed)
    wins = 0
    for _ in range(trials):
        # trong lúc phía trung thực đào z khối, kẻ tấn công đào k khối (mỗi khối mới là của kẻ tấn công với xác suất q)
        k, h = 0, 0
        while h < z:
            if rng.random() < q:
                k += 1
            else:
                h += 1
        gap = z - k  # kẻ tấn công còn thiếu
        while 0 < gap < cap:
            gap += -1 if rng.random() < q else 1
        wins += gap <= 0
    return wins / trials


mc3 = race(0.3, 5)
mc1 = race(0.1, 2)
rec("L06", abs(mc3 - alg.exact_double_spend(0.3, 5)) < 0.004 and abs(mc1 - alg.exact_double_spend(0.1, 2)) < 0.002
    and alg.exact_double_spend(0.3, 5) > alg.nakamoto_catch_up(0.3, 5) and round(alg.nakamoto_catch_up(0.3, 5), 7) == 0.1773523
    and round(alg.nakamoto_catch_up(0.1, 6), 7) == 0.0002428 and alg.nakamoto_catch_up(0.5, 30) == 1.0,
    f"mô phỏng đua khối khớp công thức CHÍNH XÁC: q = 0,3, z = 5 → {mc3:.4f} (chính xác {alg.exact_double_spend(0.3, 5):.4f}, Nakamoto 0,1774); q = 0,1, z = 2 → {mc1:.4f} (chính xác {alg.exact_double_spend(0.1, 2):.4f}) — bảng 2008 đánh giá thấp")


# ── L07: vét cạn giao của các tập đủ phiếu ──
def quorums_intersect_honest(n):
    f, q = alg.bft_tolerance(n)
    for bad in itertools.combinations(range(n), f):
        honest = set(range(n)) - set(bad)
        for A in itertools.combinations(range(n), q):
            for B in itertools.combinations(range(n), q):
                if not (set(A) & set(B) & honest):
                    return False
    return True


small_bad = alg.bft_tolerance(4)
rec("L07", quorums_intersect_honest(4) and quorums_intersect_honest(5) and alg.bft_tolerance(100) == (33, 67) and alg.bft_tolerance(10) == (3, 7) and small_bad == (1, 3)
    and 67 + 67 - 100 == 34 > 33, "vét cạn n = 4, 5: mọi cặp tập đủ phiếu đều chung ≥ 1 bên trung thực; 100 → (33, 67); 10 → (3, 7)")

# ── L08: Decimal ──
rec("L08", D(21000) * 20 * D("1e-9") == D("0.00042") and D(50000) * 30 * D("1e-9") == D("0.0015"), "Decimal: 0,00042 và 0,0015 ETH")


# ── L09: mô phỏng bằng đối tượng có hàm nhận gọi lại ──
class Vault:
    def __init__(self, pool, safe):
        self.pool, self.safe, self.bal = pool, safe, {}

    def withdraw(self, who):
        amt = self.bal.get(who.name, 0)
        if amt <= 0 or self.pool < amt:
            return
        if self.safe:
            self.bal[who.name] = 0
            self.pool -= amt
            who.receive(self, amt)
        else:
            self.pool -= amt
            who.receive(self, amt)
            self.bal[who.name] = 0


class Attacker:
    name = "x"

    def __init__(self):
        self.got = 0

    def receive(self, vault, amt):
        self.got += amt
        vault.withdraw(self)  # gọi lại


def run(pool, dep, safe):
    v, a = Vault(pool, safe), Attacker()
    v.bal["x"] = dep
    v.withdraw(a)
    return a.got


rec("L09", (run(10, 1, False), run(10, 1, True), run(12, 5, False), run(12, 5, True)) == (10, 1, 10, 5)
    == (alg.reentrancy_vault(10, 1, False), alg.reentrancy_vault(10, 1, True), alg.reentrancy_vault(12, 5, False), alg.reentrancy_vault(12, 5, True))
    and (3 - 5) % 256 == 254, "đối tượng có gọi lại: 10 / 1 / 10 / 5 khớp; 3 − 5 trên 8 bit không dấu = 254")

# ── L10: thông lượng ──
rec("L10", round(1e6 / 250 / 600, 1) == 6.7 and round(4e6 / 400 / 600, 1) == 16.7 and round(1e6 / 12 / 600, 1) == 138.9 and 1000 // 2 == 500 and 50 // 2 == 25,
    "6,7 / 16,7 / 138,9 giao dịch mỗi giây; kênh 1000 lần → 2, 50 lần → 2")

# ── L11: tìm kiếm đối kháng ──
rng = random.Random(11)
ok11 = True
for _ in range(20_000):
    honest = [rng.uniform(99, 101) for _ in range(4)]
    bad = [rng.choice([0, 1e9, rng.uniform(-1e6, 1e6)]) for _ in range(3)]
    m = statistics.median(honest + bad)
    ok11 &= min(honest) <= m <= max(honest)
broken = statistics.median([100, 101, 0, 0, 0])
rec("L11", ok11 and broken == 0 == alg.median_oracle([100, 101, 0, 0, 0]) and alg.median_oracle([100, 101, 99, 100, 0, 0, 10 ** 6]) == 100,
    "20 000 phép thử đối kháng: 7 nguồn, 3 nguồn sai bất kỳ → trung vị luôn trong khoảng giá trị đúng; 5 nguồn có 3 sai → trung vị 0")

# ── L12: hành trình — tính lại bằng đường khác (lịch thật, đếm byte, mô phỏng chu kỳ tín hiệu) ──
import datetime as _dt
hdr_year = sum(80 for _ in range(int(_dt.timedelta(days=365).total_seconds()) // 600))   # đếm từng khối 600 giây trong 365 ngày
weight = lambda base, wit: 4 * base + 1 * wit                                            # byte cơ sở nặng 4, nhân chứng nặng 1
def lockin_period(signals, period=2016, thr=1916):
    """Chu kỳ đầu tiên (đánh số từ 0) có ≥ thr khối báo tín hiệu; None nếu không có."""
    for k in range(len(signals) // period):
        if sum(signals[k * period:(k + 1) * period]) >= thr:
            return k
    return None
rng12 = random.Random(12)
sig_ok = [1] * 1916 + [0] * 100; rng12.shuffle(sig_ok)
sig_no = [1] * 1915 + [0] * 101; rng12.shuffle(sig_no)
days = (_dt.date(2022, 9, 15) - _dt.date(2020, 12, 1)).days
rec("L12", hdr_year == 4_204_800 and round(hdr_year / 1e6, 1) == 4.2 and 2 * 10**9 // hdr_year == 475
    and weight(1_000_000, 0) == 4_000_000 and weight(150, 100) == 700 and 4_000_000 // weight(150, 100) == 5714
    and lockin_period(sig_ok) == 0 and lockin_period(sig_no) is None and 481_824 % 2016 == 0 and 481_824 // 2016 == 239
    and round(269 / 336 * 100, 2) == 80.06 and round(336 * 600 / 86400, 2) == 2.33 and days == 653
    and round(21 / 0.0026) == 8077 and round((1 - 0.0026 / 21) * 100, 3) == 99.988
    and 32 * 12 == 384 and round(13.3 / 12, 3) == 1.108 and 32 / 4096 == 0.0078125 and round(100 / 0.33) == 303
    # trần rút sau Pectra (7/5/2025): 256 ETH mỗi kỷ nguyên (consensus-specs electra, sources_L12.md [E25]); đếm kỷ nguyên trong một ngày bằng lịch thật
    and int(_dt.timedelta(days=1).total_seconds()) // (32 * 12) * 256 == 57_600
    and alg.chain_tps(10**6, 250, 600) == 10**6 / 250 / 600,
    "tiêu đề 4 204 800 byte/năm (đếm từng khối); trọng lượng 4·cơ sở + nhân chứng: khối cũ 4 000 000, giao dịch 700, 5714/khối; "
    "1916/2016 khoá, 1915 thì không (101 khối không báo chặn được); 481 824 = 239·2016; 653 ngày; 8077 lần, 99,988%; 6,4 phút; 303 ngày; trần rút sau Pectra 57 600 ETH/ngày")

bad = [c for c, ok in R if not ok]
print(f"\nverify_bch: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
