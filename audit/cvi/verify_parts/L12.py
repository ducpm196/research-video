# CVI L12 — tính lại bằng phân số chính xác, liệt kê, và hàm checklib trường tiếp nhận — khác `checks` (số thực nhân thẳng).
from fractions import Fraction as F
import itertools

E = {2010: F("28.2"), 2011: F("25.8"), 2012: F("16.4"), 2014: F("6.7"), 2015: F("3.57"), 2017: F("2.251")}
rec("L12a", round(float(E[2010] / E[2014]), 1) == 4.2 and round(float(E[2012] / E[2014]), 1) == 2.4 and round(float(E[2010] / E[2017]), 1) == 12.5,
    "4,2 lần (CITED [RU15] “4.2x”), 2,4 lần (“2.4x”), 2010 → 2017: 12,5 lần")
rec("L12b", E[2010] / 100 * 150000 == 42300 and F(5, 1500) * 100 == F(1, 3) and round(float(F(5, 1500) * 100), 2) == 0.33,
    "2010: 42 300 ảnh sai trên 150 000; nhãn sai 5/1500 = 0,33%")
crops = list(itertools.product(range(256 - 224), range(256 - 224), (False, True)))
rec("L12c", len(crops) == 2048 and round(float((E[2011] - E[2012]) / E[2011]) * 100) == 36 and F("26.2") - F("15.3") == F("10.9"),
    "liệt kê (dời ngang, dời dọc, lật) = 2048 (CITED [KR12] “factor of 2048”); giảm tương đối 36%; cách đội nhì 10,9 điểm")
C = 64
rec("L12d", alg.cvi_receptive_field([(3, 1)] * 3) == 7 and alg.cvi_receptive_field([(3, 1)] * 2) == 5 and 3 * 9 * C * C == 27 * C * C
    and round((F(49, 27) - 1) * 100) == 81, "ba lớp 3 × 3: trường 7 × 7, 27C² so với 49C² — nhiều hơn 81% (CITED [SI14])")
rec("L12e", round(float(F("5.1") / 100 * 1500)) == 76 and F("6.8") / 100 * 1500 == 102 and F(1500, 60) == 25, "người 76 ảnh, máy 102 ảnh trên 1500; 25 giờ")
rec("L12f", F(152, 19) == 8 and F("3.57") / 100 * 100000 == 3570 and E[2015] < F("5.1"), "152/19 = 8 (CITED [HE15] “8× deeper”); 3570 ảnh sai")
prev16 = E[2017] / F(3, 4)
rec("L12g", round(float(prev16), 2) == 3.0 and E[2017] / 100 * 100000 == 2251 and round(float(F(5, 1500) * 100000)) == 333
    and round(float(F(5, 1500) * 100000 / 2251) * 100) == 15, "2016 ≈ 3,0%; 2251 ảnh sai; ~333 nhãn sai ≈ 15% (phép tính của bài)")
rec("L12h", 83 - 72 == 11 and round(72 / 83, 3) == 0.867 and F(300, 14) > 21 and F("88.55") - 83 == F("5.55"),
    "83 → 72 (CITED [RE19]); 300/14 > 21; 88,55 − 83 = 5,55 (CITED [DO20])")
rec("L12i", [round(380 - 10 * float(e)) for e in E.values()] == [98, 122, 216, 313, 344, 357] and 380 - 51 == 329, "toạ độ cột trong hình (10 điểm hình mỗi %)")
rec("L12j", F(3000, 60) == 50 and F(300, 60) == 5 and round(float(F(5, 1500) * 3000)) == 10, "tự làm: 50 giờ / 5 giờ; ~10 nhãn sai (số minh hoạ)")
