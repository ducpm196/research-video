"""Kiểm độc lập BNX L23 (scikit-learn → ONNX Runtime, rừng cô lập). Chạy bằng MÔI TRƯỜNG RIÊNG audit/bnx/deps/l23/venv
(scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.1, numpy 2.5.4; xem audit/bnx/deps/l23/README.md). Thiếu venv → SKIP (NOT_VERIFIED).
Đường khác với tools/checklib_bnx/l23.py và với thư viện:
- chạy NGUYÊN VĂN các khối mã trên màn hình (cùng một chương trình nối tiếp, hằng ở audit/bnx/src/l23.py) rồi so từng khối với đầu ra ghi trên màn hình;
- điểm bất thường tính LẠI bằng cách tự đi từng cây (children_left/right, threshold, n_node_samples) rồi lấy 2^(-độ sâu TB / c(n)),
  không gọi score_samples; so với score_samples, nhãn, offset_ (np.percentile) và số điểm dưới ngưỡng;
- số lần cắt: cài đặt thứ hai bằng danh sách Python thuần với random.Random (khác khối trên màn hình), và xác suất lần cắt đầu rơi vào khoảng trống tính bằng phép chia;
- c(256): so với hàm riêng của scikit-learn (_average_path_length) và với tổng điều hoà 2H(n-1) (bài dùng công thức xấp xỉ ln + γ như mã nguồn thư viện);
- ONNX: nạp lại tệp trong tiến trình CHẶN sklearn (sys.modules['sklearn'] = None), so nhãn và điểm trên cả 1010 điểm với bản tự đi cây;
- tỉ lệ nhiễm 0,001 / 0,01 / 0,02 / 0,05: số điểm bị gắn -1 so với số điểm dưới phân vị tính bằng sắp xếp;
- trôi dữ liệu (977/1000) tính lại bằng bản tự đi cây; lỗi to_onnx mặc định (miền ai.onnx.ml bản 4) bắt bằng try/except."""
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import l23 as L  # noqa: E402

VENV = ROOT / "audit" / "bnx" / "deps" / "l23" / "venv"
PY = VENV / "Scripts" / "python.exe"

CHAIN = [("DATA_PY", L.DATA_PY, L.DATA_OUT), ("CUT_PY", L.CUT_PY, None), ("CUT_RUN", L.CUT_RUN, L.CUT_OUT),
         ("AVG_PY", L.AVG_PY, L.AVG_OUT), ("TRAIN_PY", L.TRAIN_PY, L.TRAIN_OUT), ("SCORE_PY", L.SCORE_PY, L.SCORE_OUT),
         ("ONNX_PY", L.ONNX_PY, L.ONNX_OUT), ("CHECK_ID_PY", L.CHECK_ID_PY, L.CHECK_ID_OUT),
         ("CHECK_SEED_PY", L.CHECK_SEED_PY, L.CHECK_SEED_OUT), ("LIMIT_PY", L.LIMIT_PY, L.LIMIT_OUT),
         ("LIMIT2_PY", L.LIMIT2_PY, L.LIMIT2_OUT), ("DRIFT_PY", L.DRIFT_PY, L.DRIFT_OUT)]

# Phần phân tích: chạy TIẾP trong cùng không gian tên với chuỗi khối trên (X, mo_hinh, nhan, onnx đã có).
ANALYSIS = r'''
import json as _json, math as _m, random as _r, subprocess as _sp, sys as _sys, os as _os
import sklearn, skl2onnx, onnxruntime, numpy
from sklearn.ensemble._iforest import _average_path_length as _sk_c

def _c(n):
    return 0.0 if n <= 1 else 1.0 if n == 2 else 2.0 * (_m.log(n - 1) + 0.5772156649015329) - 2.0 * (n - 1) / n

def _manual_depths(model, Xin):
    """Tự đi từng cây: độ sâu = số cạnh tới lá + c(số mẫu ở lá)."""
    xs = np.asarray(Xin, dtype=np.float32)
    tot = np.zeros(len(xs))
    for est, feats in zip(model.estimators_, model.estimators_features_):
        t = est.tree_
        for i, x in enumerate(xs):
            node, d = 0, 0
            while t.children_left[node] != -1:
                node = t.children_left[node] if x[feats[t.feature[node]]] <= t.threshold[node] else t.children_right[node]
                d += 1
            tot[i] += d + _c(int(t.n_node_samples[node]))
    return tot / len(model.estimators_)

def _manual_scores(model, Xin):
    return -(2.0 ** (-_manual_depths(model, Xin) / _c(model.max_samples_)))

R = {"versions": [sklearn.__version__, skl2onnx.__version__, onnxruntime.__version__, numpy.__version__]}
ms = _manual_scores(mo_hinh, X)
sc_lib = mo_hinh.score_samples(X)
R["max_diff_manual_vs_lib"] = float(abs(ms - sc_lib).max())
R["manual_labels_equal"] = bool(((ms - mo_hinh.offset_ < 0) == (nhan == -1)).all())
R["offset_percentile"] = float(np.percentile(sc_lib, 1.0))
R["offset"] = float(mo_hinh.offset_)
R["below_offset"] = int((ms < mo_hinh.offset_).sum())
R["max_samples"] = int(mo_hinh.max_samples_)
R["n_estimators"] = len(mo_hinh.estimators_)
R["mean_thuong"], R["mean_la"] = float(ms[:1000].mean()), float(ms[1000:].mean())
dec = mo_hinh.decision_function(X)
R["closest_abs_decision"] = float(abs(dec).min())
R["flagged_normal_score"] = float(sc_lib[:1000][nhan[:1000] == -1][0])
R["c256_sklearn"] = float(_sk_c(np.array([256]))[0])
R["c256_harmonic"] = 2.0 * sum(1.0 / k for k in range(1, 256)) - 2.0 * 255 / 256
d1 = [float(v) for v in X.ravel()]
gap = (min(d1[1000:]) - max(d1[:1000])) / (max(d1) - min(d1))
R["p_first_cut_in_gap"] = gap
def _iso(x, pts, rg):
    n = 0
    while len(pts) > 1:
        lo, hi = min(pts), max(pts)
        cut = lo + (hi - lo) * rg.random()
        pts = [v for v in pts if v <= cut] if x <= cut else [v for v in pts if v > cut]
        n += 1
    return n
rg = _r.Random(123)
R["hand_cuts"] = [sum(_iso(d1[i], d1, rg) for _ in range(300)) / 300 for i in (0, 1000)]
# ONNX trong tiến trình chặn sklearn
np.save("x32.npy", X.astype(np.float32))
code = ("import sys; sys.modules['sklearn'] = None; sys.path.insert(0, %r); import numpy as np, onnxruntime as rt, json; "
        "s = rt.InferenceSession('rung.onnx'); x = np.load('x32.npy'); l, sc = s.run(None, {'X': x}); "
        "print(json.dumps([l.ravel().tolist(), sc.ravel().tolist()]))") % _os.path.dirname(np.__file__).rsplit(_os.sep, 1)[0]
r = _sp.run([_sys.executable, "-I", "-X", "utf8", "-c", code], capture_output=True, text=True)
if r.returncode == 0:
    lab, osc = _json.loads(r.stdout)
    R["onnx_blocked_rc"] = 0
    R["onnx_label_equal"] = sum(1 for a, b in zip(lab, nhan) if a == b)
    R["onnx_vs_manual_decision"] = float(max(abs(o - (m - mo_hinh.offset_)) for o, m in zip(osc, ms)))
    R["onnx_vs_lib_decision"] = float(max(abs(o - v) for o, v in zip(osc, dec)))
else:
    R["onnx_blocked_rc"] = r.returncode
    R["onnx_blocked_err"] = r.stderr[-300:]
# tỉ lệ nhiễm
cont = {}
for ti in (0.001, 0.01, 0.02, 0.05):
    m2 = IsolationForest(n_estimators=100, contamination=ti, random_state=42).fit(X)
    p2 = m2.predict(X)
    s2 = np.sort(m2.score_samples(X))
    cont[str(ti)] = [int((p2 == -1).sum()), int((p2[1000:] == -1).sum()), int((s2 < m2.offset_).sum())]
R["contamination"] = cont
# auto
ma = IsolationForest(n_estimators=100, random_state=42).fit(X)
R["auto"] = [float(ma.offset_), int((ma.predict(X) == -1).sum())]
# trôi dữ liệu và điểm thử
sau = np.random.default_rng(99).normal(1500, 150, 1000).reshape(-1, 1)
R["drift_manual"] = int((_manual_scores(mo_hinh, sau) - mo_hinh.offset_ < 0).sum())
R["probe"] = [int(mo_hinh.predict([[520]])[0]), int(mo_hinh.predict([[50_000]])[0])]
R["max_tree_depth"] = max(int(e.tree_.max_depth) for e in mo_hinh.estimators_)
R["default_contamination"] = IsolationForest().contamination
R["drift_in_gap"] = [float(sau.min()), float(sau.max()), float(X[:1000].max()), float(X[1000:].min())]
R["offset_auto_default_flags"] = int((IsolationForest(n_estimators=100, random_state=42).fit(X).predict(X) == -1).sum())
# lỗi to_onnx mặc định
try:
    to_onnx(mo_hinh, x32[:1])
    R["err"] = None
except Exception as e:
    R["err"] = f"{type(e).__name__}: {e}"
# ví dụ giáo án, quiz
h_half = _c(256) / 2
R["quiz1"] = [-(2.0 ** (-h_half / _c(256))), -(2.0 ** (-h_half / _c(256))) - mo_hinh.offset_]
print("###JSON" + _json.dumps(R))
'''


def run(rec):
    C = "L23"
    # 0. kích thước khối mã trên màn hình
    blocks = [t for _, t, _ in CHAIN] + [L.ONNX_ERR_PY]
    rec(C, all(len(l) <= 70 for t in blocks for l in t.split("\n")) and all(len(t.split("\n")) <= 12 for t in blocks),
        "mọi khối mã ≤ 12 dòng, dòng ≤ 70 ký tự")
    # 1. công thức thuần toán (không cần venv)
    h_ln = 2 * (math.log(255) + 0.5772156649015329) - 2 * 255 / 256
    h_harm = 2 * sum(1.0 / k for k in range(1, 256)) - 2 * 255 / 256
    rec(C, abs(alg.bnx_l23_c(256) - h_ln) < 1e-12 and round(h_ln, 4) == 10.2448 and abs(h_harm - h_ln) < 0.01,
        f"c(256) = {h_ln:.4f} (công thức ln + γ); tổng điều hoà cho {h_harm:.4f}, lệch {h_harm - h_ln:.4f} < 0,01 (bài dùng công thức xấp xỉ như thư viện)")
    rec(C, round(alg.bnx_l23_score(h_ln / 2, 256), 4) == -0.7071 and round(alg.bnx_l23_score(h_ln / 2, 256) + 0.7353, 4) == 0.0282
        and round(alg.bnx_l23_score(1, 256), 4) == -0.9346 and alg.bnx_l23_score(h_ln, 256) == -0.5,
        "quiz 1: độ sâu c/2 → -0,7071, điểm quyết định +0,0282, nhãn 1; độ sâu 1 → -0,9346; độ sâu c → -0,5")
    for n, c_ in ((1010, 0.001), (1010, 0.01), (1010, 0.02), (1010, 0.05)):
        k = sum(1 for i in range(n) if i < c_ * (n - 1))   # số chỉ số i nhỏ hơn vị trí phân vị: các điểm dưới ngưỡng
        want = {0.001: 2, 0.01: 11, 0.02: 21, 0.05: 51}[c_]
        rec(C, alg.bnx_l23_expected_flags(n, c_) == want == k, f"số điểm dưới phân vị {c_}: đếm chỉ số = alg = {want}")
    # 2. chạy thật
    if not PY.exists():
        rec(C, None, "NOT_VERIFIED: thiếu audit/bnx/deps/l23/venv (scikit-learn, skl2onnx, onnxruntime, numpy) — không chạy được các khối mã và ONNX; xem audit/bnx/deps/l23/README.md")
        return
    script = ["import warnings; warnings.filterwarnings('ignore')"]
    for name, text, _ in CHAIN:
        script.append(f"print('###{name}')")
        script.append(text)
    script.append("print('###END')")
    script.append("from skl2onnx import to_onnx")
    script.append(ANALYSIS)
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "chay.py").write_text("\n".join(script) + "\n", encoding="utf-8")
        r = subprocess.run([str(PY), "-I", "-X", "utf8", "-B", "chay.py"], cwd=d, capture_output=True, text=True, encoding="utf-8", timeout=420)
    so = r.stdout.replace("\r\n", "\n")
    if r.returncode != 0:
        rec(C, False, f"chạy chuỗi khối mã bằng venv thất bại, rc={r.returncode}: {r.stderr.strip()[-400:]}")
        return
    parts, cur = {}, None
    for line in so.split("\n"):
        if line.startswith("###JSON"):
            parts["JSON"] = line[len("###JSON"):]
        elif line.startswith("###"):
            cur = line[3:]
            parts[cur] = []
        elif cur and cur != "END":
            parts[cur].append(line)
    for name, text, want in CHAIN:
        if want is None:
            rec(C, name in parts, f"chạy {name} không lỗi (khối chỉ định nghĩa hàm)")
            continue
        got = "\n".join(l.rstrip() for l in parts.get(name, [])).strip("\n")
        rec(C, got == want.strip("\n"), f"chạy NGUYÊN VĂN {name}: {got.splitlines()[:3]}…" if got != want.strip("\n") else f"chạy NGUYÊN VĂN {name}: đầu ra đúng bằng khối trên màn hình ({len(want.splitlines())} dòng)")
    R = json.loads(parts["JSON"])
    rec(C, R["versions"] == ["1.9.1", "1.20.0", "1.31.1", "2.5.4"], f"phiên bản trong venv: scikit-learn, skl2onnx, onnxruntime, numpy = {R['versions']}")
    rec(C, R["n_estimators"] == 100 and R["max_samples"] == 256, "rừng 100 cây, mỗi cây tối đa 256 điểm (max_samples_ = 256)")
    rec(C, R["max_diff_manual_vs_lib"] < 1e-9 and R["manual_labels_equal"],
        f"tự đi từng cây rồi tính 2^(-độ sâu/c(256)): lệch score_samples tối đa {R['max_diff_manual_vs_lib']:.1e}; nhãn trùng trên 1010 điểm")
    rec(C, abs(R["offset_percentile"] - R["offset"]) < 1e-12 and round(R["offset"], 4) == -0.7353 and R["below_offset"] == 11 == alg.bnx_l23_expected_flags(1010, 0.01),
        f"offset_ = np.percentile(điểm, 1) = {R['offset']:.4f}; số điểm dưới ngưỡng = {R['below_offset']} = alg (1% của 1009 = 10,09 → 11)")
    rec(C, round(R["mean_la"], 4) == -0.8448 and round(R["mean_thuong"], 4) == -0.4475
        and round(alg.bnx_l23_depth_from_score(R["mean_la"], 256), 2) == 2.49 and round(alg.bnx_l23_depth_from_score(R["mean_thuong"], 256), 2) == 11.88
        and round(alg.bnx_l23_decision(round(R["mean_la"], 4), round(R["offset"], 4)), 4) == -0.1095
        and round(alg.bnx_l23_decision(round(R["mean_thuong"], 4), round(R["offset"], 4)), 4) == 0.2878
        and round(R["mean_la"] - R["offset"], 4) == -0.1095 and round(R["mean_thuong"] - R["offset"], 4) == 0.2877,
        f"ví dụ ①–④: điểm TB nhóm lạ {R['mean_la']:.4f}, thường {R['mean_thuong']:.4f}; độ sâu quy đổi 2,49 và 11,88; điểm quyết định -0,1095 và +0,2878 "
        f"tính từ các số đã làm tròn hiện trên màn hình (không làm tròn trước: +0,2877)")
    rec(C, abs(R["c256_sklearn"] - alg.bnx_l23_c(256)) < 1e-9 and abs(R["c256_harmonic"] - R["c256_sklearn"]) < 0.01,
        f"c(256): hàm riêng của scikit-learn {R['c256_sklearn']:.6f} = alg; tổng điều hoà {R['c256_harmonic']:.4f}")
    gap_pct = round(100 * R["p_first_cut_in_gap"])
    rec(C, gap_pct == 94, f"xác suất lần cắt đầu rơi vào khoảng trống = (48541 - 659)/(51512 - 318) ≈ {R['p_first_cut_in_gap']:.4f} → {gap_pct}% (hình ghi 94%)")
    hc = R["hand_cuts"]
    rec(C, 14 < hc[0] < 17.5 and 4 < hc[1] < 6.5 and hc[0] > 2.5 * hc[1],
        f"cài đặt thứ hai (danh sách thuần, 300 lần): điểm thường {hc[0]:.2f}, điểm lạ {hc[1]:.2f} lần cắt (khối trên màn hình ghi 15,8 và 5,1: cùng bậc, lạ ít hơn gần 3 lần)")
    rec(C, R.get("onnx_blocked_rc") == 0 and R.get("onnx_label_equal") == 1010 and R["onnx_vs_manual_decision"] < 1e-5 and R["onnx_vs_lib_decision"] < 1e-5,
        f"ONNX nạp trong tiến trình chặn sklearn: {R.get('onnx_label_equal')}/1010 nhãn trùng; điểm lệch bản tự đi cây {R.get('onnx_vs_manual_decision', -1):.1e}, lệch thư viện {R.get('onnx_vs_lib_decision', -1):.1e}"
        + ("" if R.get("onnx_blocked_rc") == 0 else f" — LỖI: {R.get('onnx_blocked_err')}"))
    rec(C, R["onnx_vs_lib_decision"] < 1.8e-7 * 1.5 and R["closest_abs_decision"] / R["onnx_vs_lib_decision"] > 1000,
        f"điểm sát ngưỡng nhất cách ngưỡng {R['closest_abs_decision']:.2e} (điểm thường bị gắn oan có điểm {R['flagged_normal_score']:.4f}), lớn hơn độ lệch ONNX {R['onnx_vs_lib_decision']:.1e} hơn 1000 lần")
    ct = R["contamination"]
    rec(C, ct["0.001"] == [2, 2, 2] and ct["0.01"] == [11, 10, 11] and ct["0.02"] == [21, 10, 21] and ct["0.05"] == [51, 10, 51],
        f"tỉ lệ nhiễm → [số gắn -1, trong đó lạ thật, số điểm dưới phân vị tính bằng sắp xếp]: {ct}")
    rec(C, R["auto"][0] == -0.5 and R["auto"][1] == 137, f"contamination='auto': offset_ = {R['auto'][0]}, gắn -1 {R['auto'][1]} điểm (bài chỉ dùng 0,01 và các giá trị trên; số này chỉ ghi nhận)")
    rec(C, R["max_tree_depth"] <= 8 and R["default_contamination"] == "auto" and R["offset_auto_default_flags"] == 137,
        f"độ sâu cây tối đa = {R['max_tree_depth']} (≤ ceil(log2 256) = 8); contamination mặc định = {R['default_contamination']!r}; không đặt gì → gắn {R['offset_auto_default_flags']} điểm (bài nói 137)")
    lo, hi, mx_th, mn_la = R["drift_in_gap"]
    rec(C, mx_th < lo and hi < mn_la,
        f"dữ liệu tháng sau nằm trong khoảng {lo:.0f}–{hi:.0f}, giữa nhóm thường (tối đa {mx_th:.0f}) và nhóm lạ (tối thiểu {mn_la:.0f}): đúng 'khoảng trống giữa hai nhóm cũ'")
    rec(C, all(int(c * 1009) + 1 == alg.bnx_l23_expected_flags(1010, c) for c in (0.001, 0.01, 0.02, 0.05)),
        "quy tắc đếm của bài, phần nguyên của p × (n − 1) cộng một = số điểm gắn -1 cho p = 0,001 / 0,01 / 0,02 / 0,05 (n = 1010)")
    rec(C, R["drift_manual"] == 977 == 1000 - 23, f"trôi dữ liệu: bản tự đi cây cho {R['drift_manual']}/1000 điểm thường mới dưới ngưỡng (khối ghi 977)")
    rec(C, R["probe"] == [1, -1], f"điểm thử 520 nghìn → {R['probe'][0]}, 50 triệu → {R['probe'][1]} (kẻ gian tiêu nhỏ không bị thấy; lương lớn bị gắn)")
    rec(C, R["err"] is not None and "RuntimeError" in R["err"] and "version 4 of domain 'ai.onnx.ml' not supported yet by this library" in R["err"]
        and "target_opset={'ai.onnx.ml': 3}" in R["err"],
        f"to_onnx mặc định lỗi: {(R['err'] or 'KHÔNG LỖI')[:130]}…")
    rec(C, L.ONNX_ERR_OUT.startswith("RuntimeError: The model is using version 4 of domain 'ai.onnx.ml'") and L.ONNX_ERR_OUT.rstrip("…") in (R["err"] or ""),
        "dòng lỗi hiện trên màn hình là phần đầu nguyên văn của thông báo thật")
