# IRS L02 — trọng số tần suất nhân độ hiếm và cosin: tính lại bằng cách KHÁC `checks` (Counter + từ điển thay vì danh sách theo bộ từ,
# numpy cho tích vô hướng và độ dài, sympy cho lôgarit chính xác, xếp hạng bằng sorted), đối chiếu alg.irs_tfidf / alg.cosine.
from collections import Counter
import math
import numpy as np
import sympy as sp

kho = {"d1": "máy ổ máy", "d2": "máy pin", "d3": "máy pin màn"}
V = ["máy", "ổ", "pin", "màn"]
N = len(kho)
df = Counter(t for d in kho.values() for t in set(d.split()))
idf = {t: sp.log(sp.Rational(N, df[t])) for t in V}
rec("L02a", df == Counter({"máy": 3, "pin": 2, "ổ": 1, "màn": 1}) and idf["máy"] == 0
    and [round(float(idf[t]), 3) for t in V] == [0, 1.099, 0.405, 1.099], "df 3, 1, 2, 1; độ hiếm 0; 1,099; 0,405; 1,099")


def vec(text, idf=idf):
    c = Counter(text.split())
    return np.array([c[t] * float(idf[t]) for t in V])


vs = {k: vec(v) for k, v in kho.items()}
_, alg_vs = alg.irs_tfidf([d.split() for d in kho.values()], V)
rec("L02b", all(np.allclose(vs[k], a) for k, a in zip(kho, alg_vs)) and np.allclose(vs["d3"], [0, 0, 0.4055, 1.0986], atol=1e-4),
    "vector trọng số khớp alg.irs_tfidf")
cs = lambda u, v: float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v))) if u.any() and v.any() else 0.0
q = vec("máy pin")
scores = {k: cs(q, v) for k, v in vs.items()}
order = sorted(scores, key=scores.get, reverse=True)
rec("L02c", order == ["d2", "d3", "d1"] and round(scores["d3"], 3) == 0.346 and scores["d2"] == 1 and scores["d1"] == 0
    and round(float(np.linalg.norm(vs["d3"])), 3) == 1.171 and round(float(q @ vs["d3"]), 3) == 0.164,
    "“máy pin”: d2 1 > d3 0,346 > d1 0; ‖d3‖ 1,171; tích 0,164")
cnt = lambda t: np.array([Counter(t.split())[w] for w in V], float)
raw = {k: cs(cnt("máy pin"), cnt(v)) for k, v in kho.items()}
rec("L02d", [round(raw[k], 3) for k in ("d1", "d2", "d3")] == [0.632, 1.0, 0.816] and abs(raw["d1"] - alg.cosine([1, 0, 1, 0], [2, 1, 0, 0])) < 1e-12,
    "đếm thô: 0,632; 1; 0,816")
d1x2 = vec("máy ổ máy máy ổ máy")
q2 = vec("máy ổ")
rec("L02e", round(float(q2 @ vs["d1"]), 3) == 1.207 and round(float(q2 @ d1x2), 3) == 2.414 and abs(cs(q2, d1x2) - 1) < 1e-12,
    "ghép đôi: tích 1,207 → 2,414, cosin vẫn 1")
kho10 = list(kho.values()) + ["bàn phím"] * 7
df10 = Counter(t for d in kho10 for t in set(d.split()))
rec("L02f", round(math.log(10 / df10["máy"]), 3) == 1.204 and round(math.log(10 / df10["pin"]), 3) == 1.609, "kho 10: máy 1,204; pin 1,609")
rec("L02g", abs(cs(vec("pin"), vec("pin pin pin pin pin")) - 1) < 1e-12 and round(cs(vec("pin"), vs["d3"]), 3) == 0.346,
    "nhồi từ khoá: 1 so với 0,346")
q3 = vec("pin màn")
u3 = vs["d3"] / np.linalg.norm(vs["d3"])
rec("L02h", abs(cs(q3, vs["d3"]) - 1) < 1e-12 and round(cs(q3, vs["d2"]), 3) == 0.346 and [round(x, 3) for x in u3[2:]] == [0.346, 0.938]
    and abs(float(u3 @ (q3 / np.linalg.norm(q3))) - cs(q3, vs["d3"])) < 1e-12, "quiz: d3 1, d2 0,346; chuẩn hoá (0,346; 0,938), tích = cosin")
rec("L02i", df.get("sạc", 0) == 0, "từ “sạc” không có trong kho: df = 0 (không lấy được lôgarit)")
