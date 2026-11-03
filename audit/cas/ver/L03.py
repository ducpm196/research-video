# CAS L03 — Mars Climate Orbiter. Đường KHÁC `checks`: Fraction từ bảng NIST (1 lb = 0,4535924 kg, g chuẩn 9,80665), chạy NGUYÊN VĂN mã trên màn hình
# (lấy từ tệp bài), đổi giờ bằng datetime.
import datetime as dt
import html
import re
from fractions import Fraction as F

import yaml

lbf = F("0.4535924") * F("9.80665")
rec("L03a", round(float(lbf), 6) == 4.448222 and round(float(lbf), 2) == 4.45, "1 lbf = 0,4535924 × 9,80665 = 4,448222 N (NIST: 4,448 222)")
rec("L03b", round(float(1 / lbf), 3) == 0.225 and round(float(100 * (1 - 1 / lbf)), 1) == 77.5, "đọc lbf·s như N·s: thấy 22,5%, bỏ sót 77,5% với mọi x")
m = 629                                             # khối lượng lúc phóng [MIB99]
dv_true, dv_model = float(10 * lbf / m), 10 / m
rec("L03c", (round(dv_true, 4), round(dv_model, 4), round(dv_true - dv_model, 4), round(100 * (dv_true - dv_model), 1)) == (0.0707, 0.0159, 0.0548, 5.5),
    "xung 10 lbf·s, 629 kg: 0,0707 / 0,0159 / thiếu 0,0548 m/s; 100 lần → 5,5 m/s (số minh hoạ)")
rec("L03d", 226 - 57 == 169 and abs(169 - 170) <= 1 and 80 - 57 == 23, "cận điểm 226 → 57 km: thấp hơn 169 ≈ “170 km”; dưới ngưỡng 80 km 23 km")
t = lambda s: dt.datetime.strptime("1999-09-23 " + s, "%Y-%m-%d %H:%M:%S")
rec("L03e", (t("09:04:52") - t("09:00:46")).seconds == 246 and divmod(246, 60) == (4, 6), "09:00:46 → 09:04:52 = 246 s = 4 phút 6 giây")
rec("L03f", round(float(2 * lbf), 1) == 8.9 and round(float(100 * (1 - 2 / (2 * lbf)))) == 78, "quiz: 2,0 lbf·s = 8,9 N·s; bỏ sót ≈ 78%")
# mã trên màn hình: chép nguyên văn từ tệp bài rồi chạy
spec = yaml.safe_load((ROOT / "lessons" / "cas" / "L03_mars_climate_orbiter.yaml").read_text(encoding="utf-8"))
show = next(st["show"] for sc in spec["scenes"] if sc["id"] == "design" for st in sc["steps"])
src = html.unescape(re.search(r'<pre class="code">(.*?)</pre>', show, re.S).group(1))
ns = {}
exec(src, ns)
rec("L03g", round(ns["tu_pao_luc_giay"](10).niuton_giay(), 2) == 44.48 and ns["tu_niuton_giay"](10).niuton_giay() == 10,
    "mã trên màn hình chạy thật: từ 10 pao lực giây → 44,48 N·s; từ 10 N·s → 10")
