# CAS L05 — Knight Capital. Đường KHÁC `checks`: Fraction, liệt kê mọi tổ hợp máy sót (thay 1 − 0,99^n), mô phỏng vòng gửi lệnh con,
# và chạy NGUYÊN VĂN mã kiểm đồng nhất trên màn hình (lấy từ tệp bài).
import html
import itertools
import re
from fractions import Fraction as F

import yaml

rec("L05a", F(460, 45) > 10 and round(float(F(460, 45)), 1) == 10.2, "hơn 460 triệu / 45 phút > 10,2 triệu đô la mỗi phút")
rec("L05b", round(4_000_000 / 2700) == 1481 and round(397 / 4) == 99, "4 triệu khớp / 2700 s ≈ 1481 mỗi giây; 397 triệu / 4 triệu ≈ 99 cổ phiếu")
rec("L05c", 80 + 74 == 154 and F("3.5") + F("3.15") == F("6.65"), "80 + 74 = 154 mã; 3,5 + 3,15 = 6,65 tỉ")
rec("L05d", 2012 - 2003 == 9 and (9 * 60 + 30) - (8 * 60 + 1) == 89, "mã chết 9 năm; 8:01 → 9:30 = 89 phút")


def route(parent, child, per_s, seconds, counter):     # mô phỏng vòng gửi lệnh con, có / không có bộ đếm (số minh hoạ)
    sent = filled = 0
    for _ in range(per_s * seconds):
        if counter and filled >= parent:
            break
        sent += 1
        filled += child
    return sent, sent * child


rec("L05e", route(100, 10, 100, 60, True) == (10, 100) and route(100, 10, 100, 60, False) == (6000, 60000) and 60000 // 100 == 600,
    "có bộ đếm: 10 lệnh con; không có: 6000 lệnh, 60 000 cổ phiếu = 600 lần")


def p_any_miss(n, p):                                    # liệt kê mọi tổ hợp sót/không sót của n máy
    q = F(0)
    for combo in itertools.product((0, 1), repeat=n):
        if any(combo):
            k = sum(combo)
            q += p ** k * (1 - p) ** (n - k)
    return q


p = F(1, 100)
rec("L05f", round(float(p_any_miss(8, p)), 3) == 0.077 and round(float(1 - (1 - p) ** 20), 3) == 0.182, "ít nhất một máy sót: 8 máy 7,7%; 20 máy 18,2%")
rec("L05g", p * p == F(1, 10000) and round(float(1 - (1 - p * p) ** 20), 4) == 0.002, "thêm phép kiểm độc lập 1%: 0,01% mỗi máy; 20 máy ≈ 0,2%")
spec = yaml.safe_load((ROOT / "lessons" / "cas" / "L05_knight_capital.yaml").read_text(encoding="utf-8"))
show = next(st["show"] for sc in spec["scenes"] if sc["id"] == "check" for st in sc["steps"])
ns = {}
exec(html.unescape(re.search(r'<pre class="code">(.*?)</pre>', show, re.S).group(1)), ns)
ok_all, _ = ns["kiem_dong_nhat"]({f"may{i}": "ban_moi" for i in range(1, 9)})
ok_7, dau = ns["kiem_dong_nhat"]({**{f"may{i}": "ban_moi" for i in range(1, 8)}, "may8": "ban_cu"})
odd = [k for k, v in dau.items() if list(dau.values()).count(v) == 1]
rec("L05h", ok_all and not ok_7 and odd == ["may8"], "mã trên màn hình chạy thật: 8 máy bản mới → đồng nhất; máy 8 bản cũ → không đồng nhất, chỉ ra may8")
