"""Kiểm độc lập mọi khẳng định của khoá AGT — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Chuỗi bước, thử lại, bộ kiểm chứng, biểu quyết: Monte Carlo (numpy). Lược đồ: bộ kiểm tự viết theo json (kiểu JSON thật sau json.dumps/loads).
Đồ thị phụ thuộc: nới lỏng kiểu Bellman–Ford trên đường dài nhất. pass@k không chệch: liệt kê mọi tổ hợp k lần chạy.
Từ tố vòng lặp: cộng dồn bằng vòng lặp mô phỏng từng bước. Chạy: .venv/Scripts/python audit/agt/verify_agt.py"""
import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []
rng = np.random.default_rng(2026)
N = 200_000


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00: Monte Carlo chuỗi bước và thử lại ──
def mc_chain(p, n, tries=1):
    ok = np.ones(N, bool)
    for _ in range(n):
        step = np.zeros(N, bool)
        for _ in range(tries):
            step |= rng.random(N) < p
        ok &= step
    return ok.mean()


rec("L00a", abs(mc_chain(0.95, 20) - 0.358) < 0.005 and abs(mc_chain(0.95, 20, 2) - 0.951) < 0.003 and abs(mc_chain(0.9, 10, 2) - 0.904) < 0.003
    and round(alg.chain_success(0.95, 20), 3) == 0.358 and round(alg.chain_with_retry(0.95, 20, 3), 3) == 0.998,
    "Monte Carlo: 20 bước × 95% ≈ 0,358; thử lại 2 lần ≈ 0,951; 10 bước × 90%, thử lại 2 lần ≈ 0,904")


# ── L01: lược đồ trên dữ liệu JSON thật ──
def valid(js):
    d = json.loads(js)
    if set(d) != {"so_tien", "tai_khoan"}:
        return False
    v, t = d["so_tien"], d["tai_khoan"]
    return type(v) is int and 1 <= v <= 10_000_000 and type(t) is str and len(t) == 10 and t.isdigit()


calls = [{"so_tien": 500000, "tai_khoan": "0123456789"}, {"so_tien": -200, "tai_khoan": "0123456789"}, {"so_tien": "1000", "tai_khoan": "98765"},
         {"so_tien": 1000, "tai_khoan": "9876543210", "ghi_chu": "x"}, {"so_tien": 20_000_000, "tai_khoan": "0123456789"}, {"tai_khoan": "0123456789"}]
schema = {"so_tien": (int, lambda v: 0 < v <= 10_000_000), "tai_khoan": (str, lambda v: len(v) == 10 and v.isdigit())}
mine = [valid(json.dumps(c)) for c in calls]
rec("L01a", mine == [True, False, False, False, False, False] == [alg.check_args(c, schema)[0] for c in calls] and valid('{"so_tien": true, "tai_khoan": "0123456789"}') is False
    and alg.check_args({"so_tien": True, "tai_khoan": "0123456789"}, schema)[0] is False, "6 lời gọi qua JSON thật: chỉ lời gọi đầu hợp lệ; giá trị true không được coi là số")

# ── L02: đường dài nhất bằng nới lỏng ──
dur = {"tim": 2, "docA": 3, "docB": 4, "docC": 5, "tonghop": 2, "kiem": 1}
edges = [("tim", "docA"), ("tim", "docB"), ("docA", "tonghop"), ("docB", "tonghop"), ("tonghop", "kiem")]


def longest(es, nodes):
    f = {k: dur[k] for k in nodes}
    for _ in nodes:
        for a, b in es:
            f[b] = max(f[b], f[a] + dur[b])
    return max(f.values())


nodes5 = ["tim", "docA", "docB", "tonghop", "kiem"]
rec("L02a", longest(edges, nodes5) == 9 and sum(dur[k] for k in nodes5) == 12 and longest(edges + [("tim", "docC"), ("docC", "tonghop")], nodes5 + ["docC"]) == 10
    and alg.dag_times({k: dur[k] for k in nodes5}, {"tim": [], "docA": ["tim"], "docB": ["tim"], "tonghop": ["docA", "docB"], "kiem": ["tonghop"]})[1] == 9,
    "nới lỏng đường dài nhất: 9 s (tuần tự 12 s); thêm đọc C 5 s → 10 s")

# ── L03 ──
rec("L03a", max(t for t in range(200) if 8000 + 2000 * t <= 128000) == 60 == alg.turns_until_full(128000, 8000, 2000)
    and max(t for t in range(100) if 4000 + 1500 * t <= 32000) == 18 and max(t for t in range(100) if 4000 + 2000 + 1500 * t <= 32000) == 17,
    "tìm số lượt lớn nhất còn vừa: 60; 18; 17 khi dành 2 000 cho tóm tắt")

# ── L04 ──
miss = 0.4
for _ in range(2):
    miss *= 0.5
src = {"S1": "Nhân viên chính thức được nghỉ phép 12 ngày mỗi năm.", "S2": "Nghỉ phép năm được cộng thêm 1 ngày sau mỗi 5 năm làm việc."}
found = [src.get(s, "").find(q) >= 0 for q, s in (("được nghỉ phép 12 ngày mỗi năm", "S1"), ("cộng thêm 2 ngày sau mỗi 5 năm", "S2"), ("được nghỉ 15 ngày", "S3"))]
rec("L04a", round(1 - miss, 3) == 0.9 and found == [True, False, False] and [x[1] for x in alg.citation_check([("được nghỉ phép 12 ngày mỗi năm", "S1"), ("cộng thêm 2 ngày sau mỗi 5 năm", "S2"), ("được nghỉ 15 ngày", "S3")], src)] == found
    and round(1 - 0.5 * 0.6 ** 2, 2) == 0.82, "độ phủ 0,6 → 0,8 → 0,9; tìm chuỗi bằng str.find trùng checklib; câu tự làm 0,82")

# ── L05: Monte Carlo bộ kiểm chứng ──
corr = rng.random(N) < 0.6
acc = np.where(corr, rng.random(N) < 0.9, rng.random(N) < 0.2)
prec = corr[acc].mean()
rec("L05a", abs(prec - 0.871) < 0.004 and abs(acc.mean() - 0.62) < 0.003 and round(1 - 0.38 ** 3, 3) == 0.945 and round(alg.verifier_precision(0.3, 0.9, 0.2), 3) == 0.659
    and round(alg.verifier_precision(0.6, 0.95, 0.05), 3) == 0.966, f"mô phỏng: nhận {acc.mean():.3f}, đúng trong số được nhận {prec:.3f}; 0,659 khi bài khó; 0,966 với bộ kiểm thử")

# ── L06 ──
rec("L06a", [len(list(itertools.permutations(range(n), 2))) for n in (3, 6, 10)] == [6, 30, 90] == [alg.comm_channels(n, "full") for n in (3, 6, 10)]
    and [2 * (n - 1) for n in (3, 6, 10)] == [4, 10, 18] and round(0.9 ** 3, 3) == 0.729 and round(0.95 ** 4, 3) == 0.815, "đếm cặp có thứ tự: 6, 30, 90; qua điều phối 4, 10, 18")


# ── L07: liệt kê tổ hợp ──
def passk_enum(n, c, k):
    runs = [1] * c + [0] * (n - c)
    combos = list(itertools.combinations(range(n), k))
    return sum(1 for cb in combos if any(runs[i] for i in cb)) / len(combos)


rec("L07a", abs(passk_enum(10, 7, 3) - alg.pass_at_k_unbiased(10, 7, 3)) < 1e-12 and round(passk_enum(10, 7, 3), 3) == 0.992
    and abs(mc_chain(0.7, 3) - 0.343) < 0.004 and round(alg.pass_at_k(0.7, 3), 3) == 0.973 and round(0.9 ** 5, 3) == 0.59,
    "liệt kê 120 tổ hợp: 0,992 (khớp công thức không chệch); mô phỏng mọi lần ≈ 0,343")


# ── L08: mô phỏng từng bước ──
def tokens(S, G, n, cached=None):
    total = eff = 0.0
    ctx = S
    prev = 0
    for i in range(n):
        total += ctx
        eff += ctx if cached is None or i == 0 else prev * cached + (ctx - prev)
        prev = ctx
        ctx += G
    return total, eff


rec("L08a", tokens(2000, 500, 10) == (42500, 42500) and tokens(2000, 500, 10, 0.1)[1] == alg.loop_tokens(2000, 500, 10, 0.1)[1] == 10100
    and tokens(1000, 300, 20) == (77000, 77000) and round(tokens(1000, 300, 20, 0.1)[1]) == 13730 and tokens(2000, 500, 20)[0] == 135000,
    "mô phỏng từng bước: 42 500 / 10 100; 77 000 / 13 730; 20 bước 135 000")

# ── L09 ──
rec("L09a", [alg.tool_gate(a) for a in ("đọc trang", "tìm kiếm", "gửi thư", "chuyển tiền", "xoá dữ liệu", "chạy lệnh")] == ["chạy", "chạy", "hỏi", "hỏi", "cấm", "cấm"]
    and all(alg.AGT_POLICY[a] in ("chạy", "hỏi", "cấm") for a in alg.AGT_POLICY), "cổng quyền: đọc chạy, gửi hỏi, xoá cấm, công cụ lạ cấm")

# ── L10, L11 ──
rec("L10a", 22 + 15 + 9 + 4 == 50 and round(22 / 50, 2) == 0.44 and (200 - 34) / 200 == 0.83 and round(3.0 / 8.1, 2) == 0.37, "44% nhóm lớn nhất; 75% → 83%; đọc trang 37%")
rec("L11a", abs(mc_chain(0.98, 4) - 0.922) < 0.003 and abs(mc_chain(0.95, 6) - 0.735) < 0.004 and abs(mc_chain(0.95, 6, 2) - 0.985) < 0.002
    and [round(x, 3) for x in alg.workflow_vs_agent(0.97, 3, 0.97, 5)] == [0.913, 0.859], "mô phỏng: quy trình 0,922; tác tử 0,735; tác tử có kiểm chứng 0,985")

# ── L12: hành trình tác tử dùng công cụ (audit/agt/sources_L12.md) — tính lại từ số của nguồn ──
_sb_full, _sb_prs, _lite, _ver = 2294, 90000, 300, 500
_res23 = round(0.0196 * _sb_full)                      # SB24: 1,96% của 2294
_res24 = 286                                           # SA24: “12.47% (286/2,294)”
rec("L12a", 71 - 37 == 34 and 71 - 45 == 26 and 50 * 2 * 2 == 200 and round(400 / 1400, 2) == 0.29 and 40.4 / 14.8 > 2,
    "ReAct: 71 − 37 = 34 điểm (khớp “absolute … 34%”), 200 vết; Toolformer: 400/1400 ≈ 0,29, 40,4/14,8 ≈ 2,73 > 2 (“more than doubles”)")
rec("L12b", _res23 == 45 and round(_res23 / _sb_full * 100, 2) == 1.96 and round(_res24 / _sb_full * 100, 2) == 12.47
    and round(_res24 / _res23, 1) == 6.4 and round(_sb_full / _sb_prs * 100, 1) == 2.5 and round(438000 / 32.8) == 13354,
    f"SWE-bench: 1,96% × 2294 = {_res23} bài; 286/2294 = 12,47% ≈ 6,4 lần trên CÙNG tập; 2294/90 000 ≈ 2,5%; 438 000/32,8 ≈ 13 354")
rec("L12c", round(0.18 * _lite) - round(0.15 * _lite) == 9 and round(0.157 * _lite) - round(0.12 * _lite) == 11
    and round(0.65 * _ver) == 325 and _ver - 325 == 175 and round(0.65 * _ver) / _ver != _res23 / _sb_full,
    "tập nhẹ: kiểm cú pháp +9 bài, tìm từng kết quả −11 bài; Verified 65% × 500 = 325, còn 175 (khác tập — không chia cho 1,96)")

nf = sum(1 for _, ok in R if not ok)
print(f"TỔNG: {len(R) - nf} PASS · {nf} FAIL")
sys.exit(1 if nf else 0)
