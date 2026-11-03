# CVI L11 — tính lại bằng liệt kê bảng bốn ô (đếm nguyên), mô phỏng numpy hạt giống khác (khác random.Random của alg.cvi_shortcut_sim),
# và chạy thật hai “mô hình” A (lối tắt) và B (nhìn vật, đúng 90%) trên tập cùng phân bố và tập đổi nền.
from fractions import Fraction as F

import numpy as np

cells = {("bò", "cỏ"): 475, ("bò", "không cỏ"): 25, ("không bò", "cỏ"): 25, ("không bò", "không cỏ"): 475}
rule_ok = sum(n for (c, g), n in cells.items() if (c == "bò") == (g == "cỏ"))
rec("L11a", rule_ok == 950 and F(rule_ok, 1000) == F(95, 100), "bảng bốn ô: quy tắc “có cỏ thì là bò” đúng 950/1000")
r = np.random.default_rng(21)
n = 200000
cow = r.random(n) < 0.5
grass = np.where(cow, r.random(n) < 0.95, r.random(n) < 0.05)
rec("L11b", abs((grass == cow).mean() - 0.95) < 0.003 and abs(alg.cvi_shortcut_sim(100000)[0] - 0.95) < 0.005, f"mô phỏng numpy 200 000 ảnh: {(grass == cow).mean():.4f}")
# tập đổi nền: 500 bò không cỏ, 500 không bò có cỏ
cow2 = np.array([True] * 500 + [False] * 500)
grass2 = ~cow2
A2 = grass2
B_correct = r.random(1000) < 0.9  # B đúng 90% bất kể nền
rec("L11c", (A2 == cow2).sum() == 0 and abs(B_correct.mean() - 0.9) < 0.03 and alg.cvi_shortcut_sim(1000)[1] == 0.0,
    "đổi nền: A đúng 0/1000; B ≈ 90%; bò trên bãi biển: 0")
rec("L11d", F(475 * 10 + 475 * 10, 10000) == F(95, 100), "thu gấp 10 lần theo cách cũ: vẫn 95%")
rec("L11e", F(5, 10) * F(97, 100) + F(5, 10) * F(70, 100) == F(835, 1000) and F(5, 10) * F(93, 100) + F(5, 10) * F(90, 100) == F(915, 1000)
    and F(97 - 70, 100) == F(27, 100) and F(93 - 90, 100) == F(3, 100), "bãi đỗ: A 0,835, B 0,915; tụt 27 và 3 điểm")
rec("L11f", F(900 * 95 + 100 * 50, 100000) == F(905, 1000) and F(475, 500) == F(95, 100), "ôn nền: 90,5%; 475/500 = 95%")
