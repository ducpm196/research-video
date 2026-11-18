"""Kiểm độc lập BNX L15 — tính lại bằng đường KHÁC checklib (số nguyên thuần, chia theo giờ, vòng lặp đếm), chạy thật đúng chuỗi mã
Python trên màn hình, phân tích thật đặc tả OpenAPI trên màn hình, rồi đối chiếu với alg.bnx_l15_*. Mọi độ trễ và hệ số cao điểm là số minh hoạ."""
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import l15  # noqa: E402


def round_half_up_int(num, den, nd=0):
    """Làm tròn nửa lên num/den tới nd chữ số thập phân, chỉ bằng số nguyên; trả chuỗi kiểu '11.6'."""
    scale = 10 ** nd
    q, r = divmod(num * scale * 2 + den, den * 2)   # floor((x·scale) + 1/2)
    s = str(q)
    return s if nd == 0 else (s[:-nd] or "0") + "." + s[-nd:].rjust(nd, "0")


def run_wp4(rec):
    """Nâng AF2 (WP4): chạy lại chương trình quy mô, kiểm số đếm bằng đường khác (phép nhân Little, đếm cửa sổ trượt), chấm lab bằng cham.sh."""
    import math
    import os
    import re
    import lib2
    lib2.verify_programs(rec, "L15")
    rec("L15", all(len(l) <= 70 for p in lib2.PROGRAMS if p.lesson == "L15" for l in p.code.split("\n")), "chương trình trên màn hình: dòng ≤ 70 ký tự")
    out = next(p for p in lib2.PROGRAMS if p.key == "L15_CungLuc").out
    rows = [(int(a), float(b), int(c)) for a, b, c in re.findall(r"^(\d+) ([\d.]+) (\d+)$", out, re.M)]

    def dem_cua_so(tps, w_us=40_000):
        """Đường khác: tại mỗi thời điểm đến, đếm số lệnh đã đến trong cửa sổ (t − w, t] bằng bisect trên danh sách thời điểm."""
        import bisect
        vao = [i * 1_000_000 // tps for i in range(tps // 5)]
        return max(i + 1 - bisect.bisect_right(vao, t - w_us) for i, t in enumerate(vao))
    rec("L15", [r[0] for r in rows] == [116, 11574, 1157407] and all(r[2] == dem_cua_so(r[0]) for r in rows),
        "số lệnh chồng nhau đếm thật = đếm bằng cửa sổ trượt (bisect): 5, 463, 46 297")
    rec("L15", all(abs(r[1] - float(alg.bnx_l15_inflight(r[0], 40))) < 0.006 for r in rows) and all(math.ceil(r[1]) == r[2] for r in rows),
        "phép nhân Little (4,64; 462,96; 46 296,28) khớp alg và số đếm bằng làm tròn lên")
    rec("L15", [round(alg.bnx_l15_tps(d, 10)) for d in (1_000_000, 100_000_000, 10_000_000_000)] == [r[0] for r in rows],
        "cao điểm 116, 11 574, 1 157 407 = tải trung bình của 1e6, 1e8, 1e10 giao dịch/ngày × 10")
    rec("L15", alg.bnx_l15_pool_tps(50, 40) == 1250 and 11574 - 1250 == 10324 and 1157407 - 1250 == 1156157 and 50 / 0.04 == 1250,
        "bể 50 kết nối, 40 ms mỗi lệnh chịu 1 250 giao dịch/giây; hàng chờ dài thêm 10 324 và 1 156 157 lệnh mỗi giây")
    r = subprocess.run([lib2._bash(), "labs/cham.sh", "BNX", "L15", "labs/BNX/L15/loi_giai.py"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=120)
    rec("L15", r.returncode == 0 and "ĐÚNG" in r.stdout, f"lab loi_giai.py chấm bằng cham.sh: {r.stdout.strip()[:60]}")
    exp = (ROOT / "labs" / "BNX" / "L15" / "mong_doi.txt").read_text(encoding="utf-8").strip().split("\n")
    tb, cao = 5_000_000 / 86400, 6 * 5_000_000 / 86400
    rec("L15", exp == [f"trung binh {round(tb, 1)} giao dich/giay", f"cao diem {round(cao)} giao dich/giay", f"con du {400 - (12 + 6 + 25 + 120 + 3)} ms",
                       f"cung luc o Oracle {round(cao * 0.12, 1)}", f"be 30 ket noi: khong du - can it nhat {math.ceil(cao * 0.12)}"]
        and alg.bnx_l15_left(400, [12, 6, 25, 120, 3]) == 234, "mong_doi.txt của lab: 57,9; 347; dư 234 ms; 41,7 cùng lúc; cần ít nhất 42 kết nối")


def run(rec):
    run_wp4(rec)
    # số giây trong ngày: đếm bằng vòng lặp
    sec = sum(1 for _h in range(24) for _m in range(60) for _s in range(60))
    rec("L15", sec == 86400 == 1 / alg.bnx_l15_tps(1), f"giây mỗi ngày đếm từng giây: {sec}")
    # ① trung bình, ② cao điểm — số nguyên
    rec("L15", round_half_up_int(10**6, 86400, 1) == "11.6" == str(alg.bnx_l15_round(alg.bnx_l15_tps(10**6), 1)), "① 1 000 000 / 86 400 ≈ 11,6")
    rec("L15", round_half_up_int(10**6, 86400, 3) == "11.574", "① chưa làm tròn: 11,574…")
    rec("L15", round_half_up_int(10 * 10**6, 86400) == "116" == str(alg.bnx_l15_round(alg.bnx_l15_tps(10**6, 10))), "② cao điểm gấp 10 ≈ 116")
    # đường khác: theo giờ
    per_h = round_half_up_int(10**6, 24)
    rec("L15", per_h == "41667" and round_half_up_int(41667, 3600, 1) == "11.6", f"theo giờ: {per_h}/giờ → 41 667 / 3 600 ≈ 11,6")
    # ③ ④ ngân sách: trừ dần từng chặng
    left = 300
    for part in (10, 5, 20, 40):
        left -= part
    rec("L15", left == 225 == alg.bnx_l15_left(300, [10, 5, 20, 40]) and 300 - left == 75, "③ 10 + 5 + 20 + 40 = 75; ④ 300 − 75 = 225 ms")
    rec("L15", 10 + 5 + 20 + 40 + 225 == 300 and 75 * 4 == 300, "cộng ngược = 300; 75 là 25% của 300")
    rec("L15", [(1400 * x * 2 + 300) // 600 for x in (10, 5, 20, 40, 225)] == [47, 23, 93, 187, 1050],
        "độ rộng các đoạn trong hình (1400 px cho 300 ms, làm tròn)")
    # ⑤ định luật Little — mô phỏng: lệnh đến đều với tải cao điểm CHƯA làm tròn 10·10^6/86 400 = 115,74/giây, mỗi lệnh ở 40 ms;
    # đếm số lệnh đang ở trong chặng, lấy trung bình theo thời gian trong cửa sổ ổn định [1 giây, 9 giây) (bỏ hiệu ứng lúc bắt đầu và lúc cắt)
    from fractions import Fraction as Fr
    w0, w1, stay, total = Fr(1), Fr(9), Fr(40, 1000), Fr(0)
    for k in range(1200):
        start = Fr(k * 86400, 10 * 10**6)  # lệnh k đến lúc k / 115,74 giây
        total += max(Fr(0), min(start + stay, w1) - max(start, w0))
    avg = float(total / (w1 - w0))
    little = alg.bnx_l15_inflight(alg.bnx_l15_tps(10**6, 10), 40)
    rec("L15", abs(avg - 4.6296) < 0.01 and str(alg.bnx_l15_round(little, 2)) == "4.63" and round(float(little)) == 5,
        f"⑤ mô phỏng: trung bình {avg:.4f} lệnh cùng lúc ở Oracle (tải chưa làm tròn); Little 115,74·0,040 ≈ 4,63")
    rec("L15", alg.bnx_l15_inflight(116, 40) * 100 == 464, "quymo: tải đã làm tròn 116·0,040 = 4,64 (khác 4,63 chỉ do làm tròn)")
    rec("L15", alg.bnx_l15_inflight(10, 100) == 1 and alg.bnx_l15_tps(86400, 10) == 10 and alg.bnx_l15_left(100, [30, 50]) == 20,
        "làm thử của các bước: 10·0,1 = 1; 1·10 = 10; 100 − 80 = 20")
    # chạy thật đúng chuỗi mã trên màn hình
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", "-c", l15.CAP_PY], capture_output=True, text=True, encoding="utf-8")
    rec("L15", r.returncode == 0 and r.stdout.strip() == l15.CAP_OUT, f"chạy thật mã trên màn hình: {r.stdout.strip().splitlines()}")
    # đặc tả OpenAPI trên màn hình: phân tích thật + trường bắt buộc theo OAS 3.0.3
    d = yaml.safe_load(l15.OAS_YAML)
    op = d["paths"]["/transfers"]["post"]
    prm = op["parameters"][0]
    ok = (d["openapi"] == "3.0.3" and isinstance(d["info"]["version"], str) and d["info"]["title"]
          and prm["name"] == "Idempotency-Key" and prm["in"] == "header" and prm["required"] is True and prm["schema"]["type"] == "string"
          and sorted(op["responses"]) == ["201", "400", "429"] and all(v.get("description") for v in op["responses"].values()))
    rec("L15", bool(ok), "OpenAPI trên màn hình: YAML hợp lệ, có openapi/info/paths, tham số header bắt buộc, 3 phản hồi có description")
    # quiz
    rec("L15", round_half_up_int(2 * 10**6, 86400, 1) == "23.1" and round_half_up_int(2 * 10**6, 86400, 3) == "23.148"
        and round_half_up_int(8 * 2 * 10**6, 86400) == "185" == str(alg.bnx_l15_round(alg.bnx_l15_tps(2 * 10**6, 8))),
        "quiz 1: 2 000 000/ngày ≈ 23,1/giây; gấp 8 ≈ 185")
    left2 = 250
    for part in (10, 5, 20, 40, 2):
        left2 -= part
    rec("L15", left2 == 173 == alg.bnx_l15_left(250, [10, 5, 20, 40, 2]) and 250 - left2 == 77, "quiz 2: 250 − 77 = 173 ms")
    # nhắc lại bài trước (prereq)
    rec("L15", alg.bnk_unique_key_rows(3) == 1 and alg.bnk_ledger_unbalanced([(1, "A", -200000), (1, "B", 200000)]) == []
        and 300000 + 1000000 == 100000 + 1200000 == 1300000, "nền: 3 lần gửi cùng khoá → 1 dòng; nợ/có tổng 0; tổng hai tài khoản giữ 1 300 000")
