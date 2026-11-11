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


def run(rec):
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
    # ⑤ định luật Little — mô phỏng: lệnh đến đều 116/giây, mỗi lệnh ở 40 ms; đếm số lệnh đang ở trong chặng, lấy trung bình theo thời gian
    # đơn vị thời gian 1/(116·1000) giây để mọi mốc là số nguyên: lệnh k đến lúc k·1000, ở lại 40·116 đơn vị
    # lấy trung bình trong cửa sổ ổn định [1 giây, 9 giây) để bỏ hiệu ứng lúc bắt đầu và lúc cắt
    w0, w1 = 116 * 1000 * 1, 116 * 1000 * 9
    stay, total = 40 * 116, 0
    for k in range(116 * 10):
        start = k * 1000
        total += max(0, min(start + stay, w1) - max(start, w0))
    avg = total / (w1 - w0)
    rec("L15", abs(avg - 4.64) < 1e-9 and alg.bnx_l15_inflight(116, 40) * 100 == 464, f"⑤ mô phỏng: trung bình {avg} lệnh cùng lúc ở Oracle")
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
