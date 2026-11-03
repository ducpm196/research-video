"""Kiểm độc lập mọi khẳng định của khoá DVO — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Chia đôi: module bisect của Python. Xung đột, chập chờn, sẵn sàng: Monte Carlo (numpy, hạt giống riêng). Phiên bản: packaging.version.
Mã băm: tarfile thật (khác zipfile của checklib). Lịch sử kho mã: dựng kho git THẬT trong thư mục tạm. Nhị thức: sympy (hữu tỉ chính xác).
Di chuyển lược đồ: sqlite3 trên tệp tạm. Khoá RSA đồ chơi: sympy.mod_inverse và sympy.isprime.
Chạy: .venv/Scripts/python audit/dvo/verify_dvo.py → PASS/FAIL từng dòng và tổng."""
import bisect
import hashlib
import io
import math
import os
import sqlite3
import statistics
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

import numpy as np
import sympy as sp
from packaging.version import Version

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []
rng = np.random.default_rng(2026)


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00: chia đôi bằng bisect (số lần thử tối đa = ⌈log₂ n⌉) ──
def builds_bisect(n, bad):
    lo, hi, c = 0, n, 0
    keys = [1 if i >= bad else 0 for i in range(n)]   # “đã hỏng tính tới thay đổi i” đơn điệu
    while hi - lo > 1:
        mid = (lo + hi) // 2
        c += 1
        if keys[mid - 1]:
            hi = mid
        else:
            lo = mid
    return c


rec("L00a", [max(builds_bisect(n, b) for b in range(n)) for n in (3, 30, 300)] == [2, 5, 9] == [max(alg.bisect_builds(n, b) for b in range(n)) for n in (3, 30, 300)]
    and [math.ceil(math.log2(n)) for n in (3, 30, 300)] == [2, 5, 9] and bisect.bisect_left([0, 0, 1], 1) == 2, "chia đôi: 3 → 2, 30 → 5, 300 → 9 lần (= ⌈log₂ n⌉)")

# ── L01: Monte Carlo xung đột ──
mine = set(range(5))
def mc_conf(k, trials=200000):
    hits = rng.integers(0, 100, size=(trials, k))
    return np.isin(hits, list(mine)).any(axis=1).mean()
c40, c3 = mc_conf(40), mc_conf(3)
rec("L01a", abs(c40 - 0.871) < 0.005 and abs(c3 - 0.143) < 0.005 and round(float(alg.conflict_prob(10)), 3) == 0.401 and round(float(alg.conflict_prob(2)), 3) == 0.098,
    f"Monte Carlo: 40 thay đổi → {c40:.3f}, 3 thay đổi → {c3:.3f}; quiz 0,401 và 0,098")

# ── L02: packaging.version ──
vs = ["1.9.3", "1.10.0", "1.2.0"]
rec("L02a", sorted(vs, key=Version) == sorted(vs, key=alg.version_key) == ["1.2.0", "1.9.3", "1.10.0"] and sorted(vs) == ["1.10.0", "1.2.0", "1.9.3"]
    and Version("2.0.10") > Version("2.0.9") and [v for v in ["1.3.9", "1.4.0", "1.12.1", "2.0.0"] if Version("1.4.0") <= Version(v) < Version("2.0.0")] == ["1.4.0", "1.12.1"],
    "packaging.version: thứ tự đúng; so chuỗi sai; 2.0.10 > 2.0.9; khoảng [1.4.0, 2.0.0) chọn 1.4.0 và 1.12.1")

# ── L03: Monte Carlo chập chờn ──
red = (rng.random((100000, 300)) < 0.005).any(axis=1).mean()
rec("L03a", abs(red - 0.778) < 0.006 and round(alg.flaky_red(100, 0.005), 3) == 0.394 and round(alg.flaky_red(300, 0.001), 3) == 0.259,
    f"Monte Carlo 300 kiểm thử × 0,5%: đỏ {red:.3f} ≈ 0,778; quiz 0,394 và 0,259")


# ── L04: tarfile thật — cùng nội dung + cùng thời điểm thì cùng băm, khác thời điểm thì khác ──
def tar_digest(data, mtime):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.USTAR_FORMAT) as t:
        ti = tarfile.TarInfo("app.py")
        ti.size, ti.mtime, ti.uid, ti.gid, ti.uname, ti.gname = len(data), mtime, 0, 0, "", ""
        t.addfile(ti, io.BytesIO(data))
    return hashlib.sha256(buf.getvalue()).hexdigest()


src = b'print("xin chao")\n'
rec("L04a", tar_digest(src, 1759309200) == tar_digest(src, 1759309200) != tar_digest(src, 1759415400)
    and alg.artifact_digest({"app.py": src}, (2026, 10, 1, 9, 0, 0)) == "dac8a9bd655a" != alg.artifact_digest({"app.py": src}, (2026, 10, 2, 14, 30, 0)),
    "tar và zip đều cho: cùng nội dung + cùng thời điểm → cùng băm; khác thời điểm → khác băm")
rec("L04b", alg.artifact_digest({"app.py": b'print("xin chao!")\n'}, (2026, 10, 1, 9, 0, 0)) != alg.artifact_digest({"app.py": src}, (2026, 10, 1, 9, 0, 0)), "đổi một byte → đổi băm")

# ── L05: khai báo và mệnh lệnh ──
state = {"web": 3}
decl = lambda s, want: {**s, **want}  # noqa: E731
rec("L05a", decl(decl(state, {"web": 5}), {"web": 5}) == {"web": 5} == alg.iac_apply(state, desired={"web": 5}) and alg.iac_apply(alg.iac_apply(alg.iac_apply(state, add={"web": 2}), add={"web": 2}), add={"web": 2}) == {"web": 9}
    and decl({"web": 8, "db": 2}, {"web": 5, "db": 2}) == {"web": 5, "db": 2}, "khai báo áp 2 lần vẫn 5; mệnh lệnh 3 lần thành 9; quiz {web: 5, db: 2}")

# ── L06: kho git thật — xoá ở lần ghi sau, lần ghi trước vẫn chứa mật khẩu ──
with tempfile.TemporaryDirectory() as td:
    env = {**os.environ, "GIT_AUTHOR_NAME": "a", "GIT_AUTHOR_EMAIL": "a@x", "GIT_COMMITTER_NAME": "a", "GIT_COMMITTER_EMAIL": "a@x"}
    g = lambda *a: subprocess.run(["git", "-C", td, *a], capture_output=True, text=True, env=env, check=True).stdout  # noqa: E731
    g("init", "-q")
    Path(td, "config.ini").write_text("db_password = hunter2\n", encoding="utf-8")
    g("add", "config.ini")
    g("commit", "-q", "-m", "them cau hinh")
    Path(td, "config.ini").write_text("", encoding="utf-8")
    g("commit", "-q", "-am", "xoa mat khau")
    head_has = "hunter2" in Path(td, "config.ini").read_text(encoding="utf-8")
    hist_has = "hunter2" in g("log", "-p")
rec("L06a", (head_has, hist_has) == (False, True) and 90 / 2 == 45 and 30 / 2 == 15, "git thật: bản hiện tại không còn, lịch sử vẫn còn mật khẩu; cửa sổ phơi nhiễm T/2: 45 và 15 ngày")

# ── L07: nhị thức chính xác bằng sympy ──
def tail_exact(n, k, p):
    p = sp.Rational(p)
    return float(sum(sp.binomial(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1)))


t20, t15g, t15b, s3g, s3b = tail_exact(1000, 20, "1/100"), tail_exact(1000, 15, "1/100"), tail_exact(1000, 15, "1/50"), tail_exact(100, 3, "1/100"), tail_exact(100, 3, "1/50")
rec("L07a", (round(t20, 4), round(t15g, 4), round(t15b, 3), round(s3g, 3), round(s3b, 3)) == (0.0033, 0.0824, 0.897, 0.079, 0.323)
    and abs(alg.binom_tail(1000, 20, 0.01) - t20) < 1e-12, "P(X ≥ 20 | 1%) = 0,0033; P(X ≥ 15 | 1%) = 0,0824; P(X ≥ 15 | 2%) = 0,897; 100 yêu cầu: 0,079 và 0,323")

# ── L08: sqlite3 trên tệp tạm ──
with tempfile.TemporaryDirectory() as td:
    db = sqlite3.connect(os.path.join(td, "kh.db"))
    db.execute("CREATE TABLE kh (id INTEGER PRIMARY KEY, ten TEXT)")
    db.execute("ALTER TABLE kh RENAME COLUMN ten TO ho_ten")
    try:
        db.execute("SELECT ten FROM kh")
        old_ok = True
    except sqlite3.OperationalError:
        old_ok = False
    db.close()
rec("L08a", old_ok is False and alg.migration_sim("mot_buoc")[0][1] is False and all(o is not False and n for _, o, n in alg.migration_sim("mo_rong_thu_hep")),
    "đổi tên một bước: bản cũ lỗi ngay; mở rộng rồi thu hẹp: không bước nào có bản đang chạy bị lỗi")

# ── L09: statistics ──
rec("L09a", (40 / 30, 3 / 40, statistics.mean([30, 90, 45]), statistics.median([2, 5, 26, 8, 3])) == alg.dora(40, 3, [30, 90, 45], [2, 5, 26, 8, 3])
    and statistics.mean([2, 5, 26, 8, 3]) == 8.8 and alg.dora(60, 3, [10, 20, 30], [1, 1, 2]) == (2.0, 0.05, 20.0, 1), "1,33/ngày; 7,5%; 55 phút; trung vị 5 giờ (trung bình 8,8); quiz 2, 5%, 20, 1")

# ── L10: mô phỏng chu kỳ chạy/hỏng với thời gian mũ ──
def sim_avail(mtbf, mttr, cycles=200000):
    up = rng.exponential(mtbf, cycles).sum()
    down = rng.exponential(mttr, cycles).sum()
    return up / (up + down)


a1, a2 = sim_avail(720, 1), sim_avail(720, 0.25)
rec("L10a", abs(a1 - 0.99861) < 1e-4 and abs(a2 - 0.99965) < 5e-5 and round(alg.availability_mtbf(360, 0.25), 5) == round(alg.availability_mtbf(1440, 1), 5) == 0.99931,
    f"mô phỏng 200 000 chu kỳ: {a1:.5f} và {a2:.5f}; 360 h/15 phút = 1440 h/1 h = 0,99931")

# ── L11: dung lượng nhật ký ──
rec("L11a", (1000 * 1000 * 86400 / 10 ** 9, 1000 * 1000 * 86400 * 30 / 10 ** 9, 500 * 2000 * 86400 * 7 / 10 ** 9) == (alg.log_volume(1000, 1000), alg.log_volume(1000, 1000, 30), alg.log_volume(500, 2000, 7)) == (86.4, 2592.0, 604.8),
    "86,4 GB/ngày; 2592 GB/30 ngày; quiz 604,8 GB")

# ── L12: khoá RSA đồ chơi bằng sympy ──
n, e, d = alg.TOY_RSA["n"], alg.TOY_RSA["e"], alg.TOY_RSA["d"]
h = int(hashlib.sha256(b"anh-web-1.4.3").hexdigest(), 16) % n
rec("L12a", sp.isprime(61) and sp.isprime(53) and n == 61 * 53 and sp.mod_inverse(e, 60 * 52) == d and h == 1917 and pow(h, d, n) == 2336 and pow(2336, e, n) == h
    and int(hashlib.sha256(b"anh-web-1.4.3-sua").hexdigest(), 16) % n == 3216 and not alg.toy_verify(b"anh-web-1.4.3-sua", 2336),
    "d = e⁻¹ mod φ(n) = 2753; băm mod n = 1917; chữ ký 2336; gói sửa băm 3216 → từ chối")
rec("L12b", alg.vuln_scan({"a": "1.4.2", "b": "2.10.1", "c": "0.9.0"}, {"a": "1.4.3", "b": "2.9.0", "c": "1.0.0"}) == ["a", "c"]
    and Version("2.10.1") > Version("2.9.0"), "quét: a và c dính lỗ hổng; b an toàn (2.10.1 > 2.9.0)")

# ── L13 (hành trình đo năng lực, audit/dvo/sources_L13.md): chuẩn hoá khoảng bằng statistics.mean, tỉ số bằng Fraction,
#    đổi đơn vị bằng datetime.timedelta, chia đôi bằng builds_bisect ở trên — không dùng lại biểu thức của `checks` ──
from datetime import timedelta  # noqa: E402
from fractions import Fraction as Fr  # noqa: E402

hi_dep = 4 * 365                                                      # “four deploys per day x 365 days”
r16 = Fr(hi_dep) / Fr(statistics.mean([2, 12]))                       # 2016 và 2019: nhóm thấp 2–12 lần/năm
r17 = Fr(hi_dep) / Fr(statistics.mean([52, 12]))                      # 2017: 12–52 lần/năm
r21 = Fr(hi_dep) / Fr(statistics.mean([2, 1]))                        # 2021: dưới 2 lần/năm → (2 + 1)/2
lt16 = timedelta(minutes=43800) * statistics.mean([1, 6]) / timedelta(minutes=60)       # 3,5 tháng / 60 phút
lt17 = timedelta(minutes=statistics.mean([10080, 43800])) / timedelta(minutes=60)       # số của báo cáo 2017
lt19 = timedelta(hours=statistics.mean([730, 4380])) / timedelta(hours=24)               # 2019: < 1 ngày → 24 giờ
rec("L13a", int(r16) == 208 and round(float(r16), 1) == 208.6 and round(float(r17), 1) == 45.6 and int(r21) == 973
    and lt16 == 2555 and round(lt17) == 449 and lt17 != 440 and int(lt19) == 106
    and statistics.mean([24, 168]) == 96 and round(38.5 / 7.5, 2) == 5.13 and round(23 / 7.5, 2) == 3.07,
    f"bội số: {float(r16):.1f} (≈200/208), {float(r17):.1f} (46), {float(r21):.1f} (973); thời gian đưa lên 2555, 2017 tính lại {lt17:.0f} ≠ 440, 2019 {lt19:.1f}")
pct18, pct19, pct21, pct23 = [7, 48, 37, 15], [20, 23, 44, 12], [26, 40, 28, 7], [18, 31, 33, 17]
rec("L13b", round(pct19[0] / pct18[0], 2) == 2.86 and pct21[0] + pct21[1] == 66 and sum(pct23) == 99 and sum(pct19) == 99
    and all(0 <= v <= 15 for v in (5, 10)) and statistics.mean([0, 15]) == 7.5 and 5 < Fr(3, 40) * 100 < 10,
    "tinh hoa 7% → 20% ≈ 2,86 lần; 26 + 40 = 66%; 2023 cộng 99% (làm tròn); 5% và 10% cùng lọt khoảng cũ 0–15% (điểm giữa 7,5)")
rec("L13c", max(builds_bisect(60, b) for b in range(60)) == 6 and max(builds_bisect(15, b) for b in range(15)) == 4
    and Fr(3, 12) == Fr(1, 4) and 15 < 25 < 64 and 12 * 30 == 360 and 20 // 2 == 10,
    "quiz: lô 60 → 6 lần dựng kiểm, lô 15 → 4; 3/12 = 25% nằm giữa 15% và 64%; chặng 1: 12 × 30 = 360, 20 lỗi → 10 (số minh hoạ)")

nf = sum(1 for _, ok in R if not ok)
print(f"TỔNG: {len(R) - nf} PASS · {nf} FAIL")
sys.exit(1 if nf else 0)
