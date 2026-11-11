"""Kiểm độc lập BNX L12 — tính lại bằng đường KHÁC checklib (sổ kép Nợ/Có dựng tay theo từng tài khoản, mô phỏng hạn mức
bằng tổng tiền tố, đối soát bằng phép trừ tập hợp; chạy thật mã trên màn hình) rồi đối chiếu với alg.bnx_* mà `checks:` dùng."""
import itertools
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402
import l12 as L  # noqa: E402


def _run_py(code, post=""):
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", "-c", code + ("\n" + post if post else "")],
                       capture_output=True, text=True, encoding="utf-8", timeout=60)
    return r.returncode, r.stdout.replace("\r\n", "\n").strip("\n"), r.stderr


def _double_entry_day():
    """Đường khác: sổ ngân hàng ghi từng bút toán (tài khoản Nợ, tài khoản Có, tiền) cho tài khoản tiền gửi (Có tăng, Nợ giảm);
    sổ ví ghi riêng. Số dư = số đầu + tổng Có − tổng Nợ."""
    open_bal = {"khach_A": 5_000_000, "khach_B": 0, "dam_bao": 500_000}
    bank = [("khach_A", "dam_bao", 2_000_000),      # nạp
            ("dam_bao", "khach_B", 500_000)]        # rút của B (chuyển ví → ví không có bút toán ngân hàng)
    wallet_ops = [("A", +2_000_000), ("A", -800_000), ("B", +800_000), ("B", -500_000)]
    bal = dict(open_bal)
    for dr, cr, amt in bank:
        bal[dr] -= amt
        bal[cr] += amt
    w = {"A": 0, "B": 0, "C": 500_000}
    for k, d in wallet_ops:
        w[k] += d
    return bal, w, bank


def run(rec):
    C = "L12"
    # 1. bút toán kép dựng tay
    bal, w, bank = _double_entry_day()
    dr_side, cr_side = {}, {}
    for dr, cr, amt in bank:
        dr_side[dr] = dr_side.get(dr, 0) + amt
        cr_side[cr] = cr_side.get(cr, 0) + amt
    rec(C, sum(dr_side.values()) == sum(cr_side.values()) == 2_500_000
        and sum(bal.values()) == sum({"khach_A": 5_000_000, "khach_B": 0, "dam_bao": 500_000}.values()),
        "sổ ngân hàng trong ngày: tổng Nợ = tổng Có = 2 500 000; tổng số dư các tài khoản không đổi (tiền chỉ đổi chỗ)")
    rec(C, bal["khach_A"] == 3_000_000 == alg.bnx_wallet_run(500000, {"A": 0, "B": 0, "C": 500000}, [("nap", "A", 2000000)], {"A": 5000000})[2]["A"],
        "nạp: tài khoản khách A 5 000 000 − 2 000 000 = 3 000 000 (sổ kép = alg)")
    r = alg.bnx_wallet_run(500000, {"A": 0, "B": 0, "C": 500000},
                           [("nap", "A", 2000000), ("chuyen", "A", "B", 800000), ("rut", "B", 500000)])
    rec(C, bal["dam_bao"] == 2_000_000 == r[0] and w == r[1] == {"A": 1200000, "B": 300000, "C": 500000},
        f"cuối ngày: đảm bảo {bal['dam_bao']}, ví {w} (sổ kép = alg)")
    rec(C, sum(w.values()) == 2_000_000 and bal["dam_bao"] >= sum(w.values()) and alg.bnx_invariant(r[0], r[1]) == (True, 2000000, 0),
        "ba ví 500 000 + 1 200 000 + 300 000 = 2 000 000; đảm bảo ≥ tổng ví, phần dư 0")
    rec(C, [b for b in r[3]] == [("tiền gửi khách A", "đảm bảo thanh toán", 2000000), ("đảm bảo thanh toán", "tiền gửi khách B", 500000)],
        "alg ghi đúng hai bút toán ngân hàng (nạp, rút); chuyển ví → ví không có bút toán ngân hàng")
    # mọi thứ tự hợp lệ của ba giao dịch: hiệu (đảm bảo − tổng ví) không đổi
    evs = [("nap", "A", 2000000), ("chuyen", "A", "B", 800000), ("rut", "B", 500000)]
    diffs = set()
    for perm in itertools.permutations(evs):
        try:
            e, ww, _, _ = alg.bnx_wallet_run(500000, {"A": 0, "B": 0, "C": 500000}, list(perm))
            diffs.add(e - sum(ww.values()))
        except ValueError:
            pass   # thứ tự không hợp lệ (ví không đủ tiền)
    rec(C, diffs == {0}, "bất biến: mọi thứ tự hợp lệ của nạp/chuyển/rút giữ hiệu đảm bảo − tổng ví = 0")
    # lỗi 2: cộng ví trước khi ngân hàng trích
    rec(C, alg.bnx_invariant(2000000, [3000000]) == (False, 3000000, -1000000), "lỗi 2: ví 3 000 000 > đảm bảo 2 000 000, thiếu 1 000 000")
    # quiz 1
    rec(C, 700000 + 900000 + 400000 - 1900000 == 100000 and alg.bnx_invariant(1900000, [700000, 900000, 400000])[2] == -100000,
        "quiz 1: thiếu 100 000")
    # 2. hạn mức: chạy thật mã trên màn hình + đường khác (tổng tiền tố)
    rc, so, se = _run_py(L.LIMIT_PY)
    rec(C, rc == 0 and so == L.LIMIT_OUT, f"chạy LIMIT_PY: {so.splitlines()}")
    tx, lim = [30_000_000, 45_000_000, 20_000_000, 10_000_000], 100_000_000
    prefix = list(itertools.accumulate(tx))
    rec(C, prefix[:3] == [30_000_000, 75_000_000, 95_000_000] and prefix[3] == 105_000_000 > lim
        and [x[1] for x in alg.bnx_monthly_limit(tx, lim)] == [True, True, True, False],
        "hạn mức: tổng tiền tố 30, 75, 95, 105 triệu → giao dịch thứ tư bị từ chối (= alg)")
    rec(C, 92_000_000 + 10_000_000 > lim and lim - 92_000_000 == 8_000_000
        and alg.bnx_monthly_limit([92_000_000, 10_000_000], lim)[1][1] is False, "quiz 2: từ chối, còn 8 000 000")
    rec(C, alg.bnx_monthly_limit([95_000_000, 10_000_000], 300_000_000)[1][1] is True, "lỗi 3: với 300 triệu (TT41, một số giao dịch) giao dịch đó được nhận")
    # 3. đối soát thuế
    rc, so, _ = _run_py(L.TAX_PY)
    rec(C, rc == 0 and so == L.TAX_OUT, f"chạy TAX_PY: {so.splitlines()}")
    bank_refs = {"R1": 1_500_000, "R2": 2_000_000, "R3": 800_000}
    kb = {"R1": 1_500_000, "R3": 800_000}
    rec(C, sorted(set(bank_refs) - set(kb)) == ["R2"] == alg.bnx_tax_recon(bank_refs, kb)["chua_sang"]
        and sorted(set(kb) - set(bank_refs)) == alg.bnx_tax_recon(bank_refs, kb)["thua"] == [],
        "đối soát hai chiều bằng phép trừ tập hợp: R2 chưa sang, không có dòng thừa (= alg)")
    rec(C, alg.bnx_tax_recon({"R1": 5}, {"R1": 6, "R9": 1}) == {"khop": [], "chua_sang": [], "lech_tien": ["R1"], "thua": ["R9"]},
        "đối chứng: alg bắt lệch số tiền và dòng thừa phía Kho bạc")
    # 4. chạy lại nhật ký trên màn hình, kèm khẳng định
    rc, so, _ = _run_py(L.REPLAY_PY, "assert bao_dam >= sum(vi.values()) and bao_dam == 2_000_000")
    rec(C, rc == 0 and so == L.REPLAY_OUT, f"chạy REPLAY_PY: {so}")
    rec(C, all(len(l) <= 70 for t in (L.LIMIT_PY, L.TAX_PY, L.REPLAY_PY) for l in t.split("\n"))
        and all(len(t.split("\n")) <= 12 for t in (L.LIMIT_PY, L.TAX_PY, L.REPLAY_PY)), "mọi khối mã ≤ 12 dòng, dòng ≤ 70 ký tự")
