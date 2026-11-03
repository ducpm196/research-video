"""Kiểm độc lập mọi khẳng định của khoá LLM — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
n-gram: đếm bằng dict tự viết, độ hỗn loạn qua log. BPE: cài lại bằng danh sách ký hiệu (không dùng regex). Cosin, mặt nạ, hàm chuẩn hoá mũ: numpy.
Tham số: đếm từ kích thước ma trận thật của một tầng; bộ nhớ đệm: cấp phát numpy float16 ở cỡ nhỏ rồi nhân theo tỉ lệ. LoRA: numpy, kiểm hạng.
Khoảng tin cậy, kiểm định dấu, biểu quyết, giải mã suy đoán: Monte Carlo. Chạy: .venv/Scripts/python audit/llm/verify_llm.py"""
import math
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []
rng = np.random.default_rng(2026)


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00, L01: đếm lại ──
corpus = ["<s> tôi thích mèo </s>", "<s> tôi thích chó </s>", "<s> bạn thích mèo </s>"]
ctx, pair = defaultdict(int), defaultdict(int)
for c in corpus:
    t = c.split()
    for a, b in zip(t, t[1:]):
        ctx[a] += 1
        pair[(a, b)] += 1
V = len({w for c in corpus for w in c.split()} - {"<s>"})


def prob(sent, k=0):
    t = sent.split()
    p = Fraction(1)
    for a, b in zip(t, t[1:]):
        if ctx[a] + k * V == 0:
            return Fraction(0)
        p *= Fraction(pair[(a, b)] + k, ctx[a] + k * V)
    return p


rec("L00a", prob("<s> tôi thích mèo </s>") == Fraction(4, 9) == alg.bigram_prob("<s> tôi thích mèo </s>")
    and [prob(s) for s in ("<s> bạn thích mèo </s>", "<s> tôi thích chó </s>")] == [Fraction(2, 9)] * 2, "đếm lại: 4/9; 2/9 và 2/9")
pp = lambda p, n: math.exp(-math.log(p) / n)  # noqa: E731
rec("L01a", round(pp(4 / 9, 4), 3) == 1.225 and prob("<s> chó thích mèo </s>") == 0 and prob("<s> chó thích mèo </s>", 1) == Fraction(1, 504) == alg.bigram_prob("<s> chó thích mèo </s>", add_k=1)
    and round(pp(1 / 504, 4), 3) == 4.738 and prob("<s> tôi thích mèo </s>", 1) == Fraction(1, 64) and round(pp(1 / 9, 4), 3) == 1.732 and round(pp(6.0 ** -4, 4), 6) == 6,
    "độ hỗn loạn qua log: 1,225; làm trơn 1/504 (4,738), 1/64 (2,828); 9^(1/4) = 1,732; mô hình đều 6 từ → 6")


# ── L02: BPE cài lại bằng danh sách ──
def bpe(words, n):
    seqs = {tuple(w) + ("</w>",): f for w, f in words.items()}
    out = []
    for _ in range(n):
        cnt = {}
        for s, f in seqs.items():
            for a, b in zip(s, s[1:]):
                cnt[(a, b)] = cnt.get((a, b), 0) + f
        best = max(cnt, key=cnt.get)
        out.append((best, cnt[best]))
        new = {}
        for s, f in seqs.items():
            i, t = 0, []
            while i < len(s):
                if i + 1 < len(s) and (s[i], s[i + 1]) == best:
                    t.append(s[i] + s[i + 1])
                    i += 2
                else:
                    t.append(s[i])
                    i += 1
            new[tuple(t)] = f
        seqs = new
    return out


mine = bpe({"low": 5, "lower": 2, "newest": 6, "widest": 3}, 6)
theirs = alg.bpe_merges({"l o w </w>": 5, "l o w e r </w>": 2, "n e w e s t </w>": 6, "w i d e s t </w>": 3}, 6)[0]
rec("L02a", mine == theirs and [m[0] for m in mine[:5]] == [("e", "s"), ("es", "t"), ("est", "</w>"), ("l", "o"), ("lo", "w")]
    and alg.bpe_encode("lowest", [m[0] for m in mine[:5]]) == ["low", "est</w>"] and len("Tôi thích mèo".encode("utf-8")) == 16,
    f"BPE cài lại trùng checklib: {[(''.join(m[0]), m[1]) for m in mine]}; lowest → low + est</w>; “Tôi thích mèo” 16 byte")

# ── L03 ──
cosn = lambda a, b: float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))  # noqa: E731
rec("L03a", round(cosn([1, 2, 0], [2, 3, 1]), 3) == 0.956 and abs(cosn([1, 2, 0], [-2, 1, 0])) < 1e-12 and round(cosn([3, 2, 4, 0], [3, 2, 3, 0]), 2) == 0.99
    and round(cosn([3, 2, 4, 0], [0, 1, 1, 4]), 3) == 0.263 and round(cosn([10, 20, 0], [2, 3, 1]), 3) == 0.956 and round(cosn([1, 0], [1, 1]), 3) == 0.707,
    "numpy: 0,956; 0; nóng–lạnh 0,99; nóng–ngon 0,263; nhân 10 lần vẫn 0,956; 0,707")

# ── L04 ──
M = np.tril(np.ones((4, 4)))
z = np.array([2.0, 1, 0, 5])
masked = np.where(M[2] > 0, z, -np.inf)
w = np.exp(masked - masked.max()) / np.exp(masked - masked.max()).sum()
w2 = np.exp(z - z.max()) / np.exp(z - z.max()).sum()
rec("L04a", int(M.sum()) == 10 == sum(map(sum, alg.causal_mask(4))) and int(np.tril(np.ones((6, 6))).sum()) == 21
    and [round(x, 3) for x in w] == [0.665, 0.245, 0.09, 0.0] and round(w2[3], 2) == 0.93, "numpy: mặt nạ 10/16, 21/36; hàng 3 có che: 0,665/0,245/0,09/0; không che: 0,93 vào vị trí 4")

# ── L05 ──
d, L = 4096, 32
layer = {"q": (d, d), "k": (d, d), "v": (d, d), "o": (d, d), "up": (d, 4 * d), "down": (4 * d, d)}
per = sum(a * b for a, b in layer.values())
small = np.zeros((2, 2, 64, 128), dtype=np.float16).nbytes  # 2 (k, v) · 2 tầng · 64 chiều · 128 vị trí
rec("L05a", per == 12 * d * d and L * per == 6442450944 and small == 2 * 2 * 64 * 128 * 2 and alg.kv_cache_bytes(2, 64, 128) == small
    and alg.kv_cache_bytes(32, 4096, 4096) == 2 * 2 ** 30 and round(1 / (L * per * 2 / 1e12)) == 78 and alg.kv_cache_bytes(40, 5120, 8192) == 6710886400,
    "đếm ma trận thật của một tầng: 12d²; 32 tầng 6,44 tỉ; bộ nhớ đệm khớp cấp phát numpy float16; 2 GiB; 78 từ tố/s ở 1 TB/s; 6 710 886 400 byte")

# ── L06 ──
ps = np.array([0.25, 0.5, 0.8])
rec("L06a", round(float(-np.log(ps).mean()), 3) == 0.768 and round(math.exp(2), 2) == 7.39 and round(alg.train_flops(7e9, 20 * 7e9) / 1e21, 2) == 5.88
    and alg.train_flops(7e10, 1.4e12) == 5.88e23 and round(2 / math.log(2), 3) == 2.885, "mất mát trung bình 0,768; e² = 7,39; 6ND = 5,88·10²¹ và 5,88·10²³; 2 nat = 2,885 bit")


# ── L07 ──
def sm(zz, T=1):
    e = np.exp(np.array(zz, float) / T)
    return e / e.sum()


def topp(p, th):
    o = np.argsort(-p)
    c = np.cumsum(p[o])
    return sorted(o[: int(np.searchsorted(c, th - 1e-12) + 1)].tolist())


rec("L07a", [round(x, 3) for x in sm([2, 1, 0])] == [0.665, 0.245, 0.09] and [round(x, 3) for x in sm([2, 1, 0], 0.5)] == [0.867, 0.117, 0.016]
    and topp(sm([2, 1, 0]), 0.9) == [0, 1] == alg.top_p_keep(alg.softmax_t([2, 1, 0]), 0.9) and topp(sm([2, 1, 0], 0.5), 0.85) == [0] and topp(sm([2, 1, 0], 2), 0.9) == [0, 1, 2]
    and topp(sm([5, 1, 0]), 0.9) == [0] and round(float(sm([2, 1, 0], 2)[:2].sum()), 3) == 0.814,
    "numpy: nhiệt độ 1 / 0,5; lấy mẫu hạt nhân bằng tổng tích luỹ; A + B ở T = 2 là 0,814")

# ── L08 ──
Wm = rng.normal(size=(64, 64))
B0, A0 = np.zeros((64, 8)), rng.normal(size=(8, 64))
x = rng.normal(size=64)
Bt = rng.normal(size=(64, 8))
rec("L08a", np.allclose((Wm + B0 @ A0) @ x, Wm @ x) and np.linalg.matrix_rank(Bt @ A0) == 8 and B0.size + A0.size == alg.lora_params(64, 64, 8)
    and alg.lora_params(4096, 4096, 8) == 65536 and 32 * 4 * 65536 == 8388608 and alg.lora_params(5120, 5120, 16) == 163840,
    "numpy: B = 0 cho kết quả y như W; hạng của BA đúng bằng r = 8; đếm tham số khớp r(d + d)")

# ── L09 ──
rec("L09a", [round(1 / (1 + math.exp(-dd)), 3) for dd in (0, 1, 3, -1)] == [0.5, 0.731, 0.953, 0.269] == [round(alg.bradley_terry(dd, 0), 3) for dd in (0, 1, 3, -1)]
    and round(math.log(1 + math.exp(1)), 3) == 1.313, "logistic: 0,5 / 0,731 / 0,953 / 0,269; mất mát khi chọn ngược ln(1 + e) = 1,313")

# ── L10: Monte Carlo ──
sims = rng.binomial(500, 0.82, 200_000) / 500
half = (np.quantile(sims, 0.975) - np.quantile(sims, 0.025)) / 2
mc = np.mean([abs(rng.binomial(50, 0.5) - 25) >= 5 for _ in range(200_000)])
rec("L10a", abs(half - alg.acc_ci95(0.82, 500)) < 0.003 and abs(mc - alg.paired_sign_p(30, 20)) < 0.005 and alg.n_for_margin(0.8, 0.01) == 6147,
    f"mô phỏng: nửa khoảng 95% = {half:.4f} (công thức 0,0337); lệch ≥ 5 trong 50 câu bất đồng: {mc:.3f} (chính xác 0,203)")

# ── L11: Monte Carlo ──
votes = rng.random((200_000, 5)) < 0.6
ind = np.mean(votes.sum(1) >= 3)
same = rng.random(200_000) < 0.5
corr = np.mean(np.where(same, votes[:, 0], votes.sum(1) >= 3))
rec("L11a", abs(ind - 0.683) < 0.004 and abs(corr - 0.641) < 0.004 and round(alg.majority_vote(0.4, 5), 3) == 0.317 and round(alg.ece([(60, 0.9, 0.7), (40, 0.6, 0.55)]), 2) == 0.14,
    f"mô phỏng biểu quyết: độc lập {ind:.3f}, tương quan một nửa {corr:.3f}; 0,317 khi p = 0,4; sai số hiệu chuẩn 0,14")

# ── L12 ──
docs = {"A": [2, 3, 1], "B": [-2, 1, 0], "C": [1, 1, 1]}
rank = sorted(docs, key=lambda k: -cosn([1, 2, 0], docs[k]))
hit = lambda rk, g, k: sum(bool(set(r[:k]) & s) for r, s in zip(rk, g)) / len(rk)  # noqa: E731
rk, g = [["A", "C", "B"], ["B", "A", "D"], ["D", "C", "A"]], [{"A"}, {"A"}, {"B"}]
rec("L12a", rank == ["A", "C", "B"] and [round(hit(rk, g, k), 3) for k in (1, 2, 3)] == [0.333, 0.667, 0.667]
    and [hit([["C", "A"], ["A", "B"], ["B", "D"], ["D", "A"]], [{"A"}, {"B"}, {"B"}, {"C"}], k) for k in (1, 2)] == [0.25, 0.75], "xếp hạng A, C, B; độ phủ 1/3, 2/3, 2/3; câu tự làm 1/4, 3/4")


# ── L13: Monte Carlo giải mã suy đoán ──
def sim_spec(a, k, n=200_000):
    acc = rng.random((n, k)) < a
    first_rej = np.where(acc.all(1), k, acc.argmin(1))
    return float(np.mean(first_rej + 1))


rec("L13a", abs(sim_spec(0.8, 4) - 3.36) < 0.02 and abs(sim_spec(0.6, 4) - 2.306) < 0.02 and [round(6442450944 * b / 1e9, 1) for b in (2, 1, 0.5)] == [12.9, 6.4, 3.2]
    and (128 / 8) ** 2 == 256, "mô phỏng: 3,36 và 2,31 từ tố mỗi lần kiểm (mỗi lần kiểm luôn có thêm 1 từ của mô hình lớn); 12,9 / 6,4 / 3,2 GB; 256 lần")

# ── L14 (hành trình mở rộng): tính lại bằng đường khác — đếm tham số từ kích thước ma trận từng tầng, cộng dồn thời gian từng bước,
#    đếm phép tính theo từng từ tố (2N đi tới + 4N lan truyền ngược), so với số trong nguồn (audit/llm/sources_L14.md) ──
def body_params(n_layer, d):
    attn = 4 * d * d                     # Q, K, V, O: bốn ma trận d × d
    ffn = d * (4 * d) + (4 * d) * d      # hai ma trận d × 4d và 4d × d
    return n_layer * (attn + ffn)


t_big = sum(1.0 for _ in range(300_000))                   # cộng dồn 300 000 bước × 1,0 s
t_base = sum(0.4 for _ in range(100_000))
flops_v17 = 3.5 * 86_400 * 8 * 9.5e12                      # thời gian × số thẻ × tốc độ (V17 §6.1, chú thích 5)
n_gpt3 = body_params(96, 12288)
per_tok = 2 * 174.6e9 + 4 * 174.6e9                       # đi tới + lan truyền ngược, mỗi từ tố
c_gpt3 = per_tok * 300e9
pf_days = c_gpt3 / (1e15 * 24 * 3600)
c_chin = (2 + 4) * 70e9 * 1.4e12
ratios = [round(t / n, 1) for n, t in ((1e9, 20.2e9), (10e9, 205.1e9), (67e9, 1.5e12), (175e9, 3.7e12), (1e12, 21.2e12))]
quizA = [(6 * n * d, d / n, 2 * n * 1e9) for n, d in ((2e9, 40e9), (8e9, 10e9))]
rec("L14a", round(t_base / 3600, 1) == 11.1 and round(t_big / 86_400, 2) == 3.47 and abs(flops_v17 / 2.3e19 - 1) < 0.01
    and abs(12 * 3600 * 8 * 9.5e12 / 3.3e18 - 1) < 0.01,
    f"V17: 100 000 × 0,4 s = {t_base / 3600:.1f} giờ (nguồn “12 hours”), 300 000 × 1 s = {t_big / 86400:.2f} ngày (“3.5 days”); "
    f"thời gian × 8 × 9,5·10¹² = {flops_v17:.2e} (bảng 2: 2,3·10¹⁹)")
rec("L14b", n_gpt3 == 12 * 96 * 12288 ** 2 and abs(n_gpt3 / 174.6e9 - 1) < 0.01 and round(c_gpt3 / 1e23, 2) == 3.14
    and abs(pf_days - 3640) < 5 and round(570 / 45_000 * 100, 1) == 1.3,
    f"B20: đếm ma trận 96 tầng, d = 12 288 → {n_gpt3 / 1e9:.1f} tỉ (bảng D.1: 174,6 tỉ); 6ND = {c_gpt3:.3e}; {pf_days:.0f} PF-ngày (bảng: 3640); 570 GB / 45 TB ≈ 1,3%")
rec("L14c", round(c_chin / 1e23, 2) == 5.88 and abs(c_chin / 5.76e23 - 1) < 0.03 and 1.4e12 / 70e9 == 20 and 280 / 70 == 4
    and all(20 <= r <= 22.5 for r in ratios) and round(8 ** 0.74, 2) == 4.66,
    f"H22: 6 · 70·10⁹ · 1,4·10¹² = {c_chin:.3e} ≈ 5,76·10²³ (lệch {c_chin / 5.76e23 - 1:.1%}); từ tố/tham số theo bảng 3: {ratios}; K20: 8^0,74 = {8 ** 0.74:.2f}")
rec("L14d", [q[0] for q in quizA] == [4.8e20, 4.8e20] and [q[1] for q in quizA] == [20, 1.25]
    and [round(4.8e20 / q[2]) for q in quizA] == [120, 30],
    "quiz (số minh hoạ): cùng 4,8·10²⁰; 20 và 1,25 từ tố mỗi tham số; chi phí sinh 1 tỉ từ tố/ngày bằng ngân sách sau 120 và 30 ngày")

nf = sum(1 for _, ok in R if not ok)
print(f"TỔNG: {len(R) - nf} PASS · {nf} FAIL")
sys.exit(1 if nf else 0)
