import lib2
from lib2 import *
from spoken_b import _spoken
from libj import jstep, nowrap
from labkit import write_lab, practice_scene

lib2.begin("L23")

# ── Mã hiện trên màn hình (chạy NGUYÊN VĂN ở audit/bnx/ver/l23.py với venv audit/bnx/deps/l23/venv, và ở cổng screen_code) ──
DATA_PY = """import numpy as np
rng = np.random.default_rng(42)
thuong = rng.normal(500, 50, 1000)      # nghìn đồng
la = rng.normal(50_000, 2_000, 10)      # 50 triệu đồng
X = np.concatenate([thuong, la]).reshape(-1, 1)
print(X.shape)
print(round(thuong.mean()), round(la.mean()))
print(round(thuong.min()), round(thuong.max()))
print(round(la.min()), round(la.max()))"""
DATA_OUT = """(1010, 1)
499 50241
318 659
48541 51512"""

CUT_PY = """def so_lan_cat(x, d, rng):
    n = 0
    while len(d) > 1:
        c = rng.uniform(d.min(), d.max())
        d = d[d <= c] if x <= c else d[d > c]
        n += 1
    return n"""
CUT_RUN = """d = X.ravel()
rng2 = np.random.default_rng(7)
for i in (0, 1000):
    cat = [so_lan_cat(d[i], d, rng2) for _ in range(200)]
    print(round(d[i]), sum(cat) / len(cat))"""
CUT_OUT = """515 15.775
49881 5.075"""

AVG_PY = """import math
def c(n):    # độ sâu trung bình để cô lập một điểm trong n điểm
    return 2 * (math.log(n - 1) + np.euler_gamma) - 2 * (n - 1) / n
def diem(h, n):     # h: độ sâu trung bình; dấu âm như scikit-learn
    return -2 ** (-h / c(n))
print(round(c(256), 4))
print(round(diem(c(256), 256), 4))
print(round(diem(c(256) / 2, 256), 4))
print(round(diem(1, 256), 4))"""
AVG_OUT = """10.2448
-0.5
-0.7071
-0.9346"""

TRAIN_PY = """from sklearn.ensemble import IsolationForest
mo_hinh = IsolationForest(n_estimators=100, contamination=0.01,
                          random_state=42)
mo_hinh.fit(X)
nhan = mo_hinh.predict(X)
print("điểm lạ bị gắn -1:", (nhan[1000:] == -1).sum(), "trên 10")
print("tổng số gắn -1:", (nhan == -1).sum(), "trên", len(X))
print("điểm thường bị gắn -1:", (nhan[:1000] == -1).sum())
print("offset_ =", round(mo_hinh.offset_, 4))"""
TRAIN_OUT = """điểm lạ bị gắn -1: 10 trên 10
tổng số gắn -1: 11 trên 1010
điểm thường bị gắn -1: 1
offset_ = -0.7353"""

SCORE_PY = """diem_so = mo_hinh.score_samples(X)
for ten, s in (("thường", diem_so[:1000].mean()),
               ("lạ", diem_so[1000:].mean())):
    h = -c(mo_hinh.max_samples_) * math.log2(-s)
    print(ten, round(s, 4), "độ sâu quy đổi", round(h, 2))"""
SCORE_OUT = """thường -0.4475 độ sâu quy đổi 11.88
lạ -0.8448 độ sâu quy đổi 2.49"""

ONNX_PY = """from skl2onnx import to_onnx
import onnxruntime as rt
x32 = X.astype(np.float32)
onx = to_onnx(mo_hinh, x32[:1],
              target_opset={"": 17, "ai.onnx.ml": 3})
open("rung.onnx", "wb").write(onx.SerializeToString())
phien = rt.InferenceSession("rung.onnx")
ten = phien.get_inputs()[0].name
nhan_onnx, diem_onnx = phien.run(None, {ten: x32})
print("cùng nhãn:", (nhan_onnx.ravel() == nhan).sum(), "trên", len(X))
lech = abs(diem_onnx.ravel() - mo_hinh.decision_function(X)).max()
print(f"sai khác điểm lớn nhất: {lech:.1e}")"""
ONNX_OUT = """cùng nhãn: 1010 trên 1010
sai khác điểm lớn nhất: 1.8e-07"""

CHECK_ID_PY = """dd = mo_hinh.decision_function(X)
ss = mo_hinh.score_samples(X) - mo_hinh.offset_
print(abs(dd - ss).max(), ((dd < 0) == (nhan == -1)).all())"""
CHECK_ID_OUT = "0.0 True"
CHECK_SEED_PY = """for hat in (0, 1, 2, 3, 4):
    mm = IsolationForest(n_estimators=100, contamination=0.01,
                         random_state=hat).fit(X)
    p = mm.predict(X)
    print(hat, (p[1000:] == -1).sum(), (p == -1).sum())"""
CHECK_SEED_OUT = """0 10 11
1 10 11
2 10 11
3 10 11
4 10 11"""

LIMIT_PY = """for ti_le in (0.001, 0.01, 0.05, "auto"):
    m = IsolationForest(n_estimators=100, contamination=ti_le,
                        random_state=42).fit(X)
    p = m.predict(X)
    print(ti_le, "gắn -1:", (p == -1).sum(),
          "| lạ thật:", (p[1000:] == -1).sum())"""
LIMIT_OUT = """0.001 gắn -1: 2 | lạ thật: 2
0.01 gắn -1: 11 | lạ thật: 10
0.05 gắn -1: 51 | lạ thật: 10
auto gắn -1: 137 | lạ thật: 10"""
LIMIT2_PY = """gian_lan_nho = [[520]]     # kẻ gian chuyển số tiền như người thường
luong_lon = [[50_000]]     # công ty trả lương hợp lệ, số tiền lớn
print(mo_hinh.predict(gian_lan_nho), mo_hinh.predict(luong_lon))"""
LIMIT2_OUT = "[1] [-1]"
ONNX_ERR_PY = """onx = to_onnx(mo_hinh, x32[:1])"""
ONNX_ERR_OUT = "RuntimeError: The model is using version 4 of domain 'ai.onnx.ml'…"
DRIFT_PY = """rng3 = np.random.default_rng(99)
thang_sau = rng3.normal(1500, 150, 1000).reshape(-1, 1)
p = mo_hinh.predict(thang_sau)
print("thường mà bị gắn -1:", (p == -1).sum(), "trên 1000")"""
DRIFT_OUT = "thường mà bị gắn -1: 977 trên 1000"

NOTE_ILL = "<span class='note'>(số minh hoạ: dữ liệu sinh ngẫu nhiên; hạt giống là số khởi đầu của bộ sinh số ngẫu nhiên, đặt cố định thì chạy lại ra y hệt, không phải dữ liệu của tổ chức nào)</span>"



# ── AF2 (nhánh B): cảnh quy mô + lab. Chương trình quy mô chạy THẬT lúc import (đệm ở audit/bnx/progcache/L23.json), bằng .venv + sys.path vào
#    audit/bnx/deps/l23/venv (như nguồn L23_venv của sổ); hai dòng đầu là đoạn nối thư viện, KHÔNG hiện trên màn hình ──
QUYMO = prog("QuyMo", r'''
import sys
sys.path.insert(0, "D:/research-video/audit/bnx/deps/l23/venv/Lib/site-packages")
import numpy as np
from sklearn.ensemble import IsolationForest
for n_la in (10, 100, 1000):
    rng = np.random.default_rng(42)
    thuong = rng.normal(500, 50, n_la * 100)
    la = rng.normal(50_000, 2_000, n_la)
    X = np.concatenate([thuong, la]).reshape(-1, 1)
    mm = IsolationForest(n_estimators=100, contamination=0.01,
                         random_state=42).fit(X)
    p = mm.predict(X)
    nut = sum(t.tree_.node_count for t in mm.estimators_)
    print(len(X), "diem:", (p == -1).sum(), "bi gan -1,",
          (p[len(thuong):] == -1).sum(), "la that,", nut, "nut cua rung")
''', lang="python", timeout=400,
    claims=["rừng cô lập tỉ lệ nhiễm 1% trên 1 010, 10 100, 101 000 điểm: gắn 11, 101, 1 005 nhãn -1, bắt đủ 10, 100, 1 000 điểm lạ; tổng số nút của rừng quanh 11 400 ở cả ba cỡ"])

LAB_PY = r'''
import math
n = 128
c = 2 * (math.log(n - 1) + 0.5772156649) - 2 * (n - 1) / n
offset = -0.6
print("c(128) =", round(c, 4))
for ten, h in (("A", 2), ("B", 9)):
    diem = -2 ** (-h / c)
    qd = diem - offset
    print(ten, "diem", round(diem, 4), "quyet dinh", round(qd, 4), "nhan", -1 if qd < 0 else 1)
so = math.ceil(0.03 * (3000 - 1))
print("bi gan -1:", so, "| gan oan:", so - 25)
'''
LAB = prog("LabL23", LAB_PY, lang="python", kind="run")
LAB_DE = """# Lab BNX L23 — Điểm bất thường, nhãn và số điểm bị gắn (Python thuần, không cần cài thư viện học máy)

Số liệu là số minh hoạ, khác ví dụ trong bài. Một rừng cô lập huấn luyện mỗi cây trên `n = 128` điểm. Viết `mau.py` (chỉ dùng `import math`) để tính:

1. **Mức tham chiếu** `c(n) = 2·(ln(n−1) + γ) − 2·(n−1)/n` với `γ = 0.5772156649` (`math.log` là lôgarit tự nhiên). In `c(128) = <số làm tròn 4 chữ số>`.
2. Hai điểm A và B có **độ sâu trung bình** `h` lần lượt là 2 và 9. Điểm bất thường `s = −2^(−h / c)` (dấu âm như thư viện). Ngưỡng `offset = −0.6`; **điểm quyết định** = `s − offset`; nhãn là `−1` nếu điểm quyết định âm, ngược lại `1`.
3. Tập có `N = 3000` giao dịch, tỉ lệ nhiễm `p = 0.03`. Theo quy tắc đếm của bài (đúng khi các điểm khác nhau), số điểm bị gắn `−1` là `p·(N−1)` làm tròn lên (`math.ceil`). Thật sự lạ chỉ có 25 điểm: tính số điểm thường bị gắn oan.

In đúng bốn dòng (làm tròn bằng `round(x, 4)`):

```
c(128) = <số>
A diem <số> quyet dinh <số> nhan <1 hoặc -1>
B diem <số> quyet dinh <số> nhan <1 hoặc -1>
bi gan -1: <số> | gan oan: <số>
```

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L23 mau.py`.
"""


def build():
    write_lab("BNX", "L23", LAB_DE, "py", LAB_PY, LAB.out)
    hook = sc("hook", "hook", "Sáng thứ hai: 1010 giao dịch, chưa ai gán nhãn, máy chỉ ra giao dịch lạ thế nào?", [
        st(f"""<p>Mỗi sáng, bộ phận rủi ro nhận <b>1010</b> giao dịch chuyển tiền của hôm qua: <b>1000</b> giao dịch quanh <b>500 nghìn</b> đồng và <b>10</b> giao dịch ở mức <b>50 triệu</b> đồng.</p>
<div class="box key">Không giao dịch nào có nhãn “gian lận” hay “bình thường”. Làm sao để máy <b>chỉ ra giao dịch lạ</b> cho người xét mà không cần ai gán nhãn trước? Và khi số giao dịch tăng gấp trăm lần, người xét có theo kịp không?</div>
<p>{NOTE_ILL}</p>""",
           """Chào bạn, mỗi sáng bộ phận rủi ro nhận một nghìn không trăm mười giao dịch chuyển tiền của hôm qua. Một nghìn giao dịch quanh năm trăm nghìn, mười giao dịch ở mức năm mươi triệu. Không giao dịch nào có nhãn, vậy làm sao để máy chỉ ra giao dịch lạ mà không cần ai gán nhãn trước? Và khi số giao dịch tăng gấp trăm lần thì người xét có theo kịp không? Mọi số liệu trong bài là số minh hoạ.""",
           focus=[1, 2, 2, 3]),
    ], checks=["1000 + 10 == 1010",
               "alg.bnx_l23_expected_flags(1010, 0.01) == 11"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Trung bình và độ lệch chuẩn", "trung bình là mức ở giữa; độ lệch chuẩn cho biết các giá trị tản ra quanh nó bao xa; dữ liệu bài rải hình chuông (phân phối chuẩn)", "quanh 500 nghìn, độ lệch chuẩn 50 nghìn: hầu hết nằm trong khoảng 400 tới 600"],
                  ["② Cắt đôi một dãy số", "chọn một điểm cắt rồi chia dãy thành nửa nhỏ hơn và nửa lớn hơn", "cắt dãy 1, 2, 3, 10 tại 5: nửa trái 1, 2, 3; nửa phải 10"],
                  ["③ Phân vị", "mức mà một tỉ lệ cho trước của các giá trị nằm dưới nó; số giá trị dưới ngưỡng ở phân vị p: p × (n−1) làm tròn lên (khi p × (n−1) đã là số nguyên thì giữ nguyên), nếu mọi điểm khác nhau; điểm trùng nhau thì số thật có thể thấp hơn", "1% của 1010 giá trị: 0,01 × 1009 = 10,09, làm tròn lên: 11 giá trị dưới ngưỡng; 1% của 101 giá trị: 0,01 × 100 = 1 đúng: 1 giá trị"],
                  ["④ Mô hình và nhãn", "mô hình: bản ghi cách tính điểm, học từ dữ liệu; nhãn của mô hình: 1 (thường) hoặc âm 1 (lạ)", "mô hình không nói “gian lận”, chỉ nói “lạ”"]]),
           """Trước hết ta cần hiểu bốn điều. Trung bình là mức ở giữa, độ lệch chuẩn cho biết giá trị tản ra quanh nó bao xa, và dữ liệu rải hình chuông là phân phối chuẩn. Cắt đôi một dãy số là chọn một điểm cắt rồi chia thành nửa nhỏ và nửa lớn. Phân vị là mức mà một tỉ lệ các giá trị nằm dưới nó, và số điểm dưới ngưỡng là p nhân n trừ một, làm tròn lên. Mô hình là bản ghi cách tính điểm học từ dữ liệu, nhãn của nó là một cho điểm thường hoặc âm một cho điểm lạ.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], introduces=["bnx_do_lech_chuan", "bnx_phan_phoi_chuan"]),
    ], checks=["alg.bnx_l23_expected_flags(1010, 0.01) == 11 and int(0.01 * (1010 - 1)) + 1 == 11 and round(0.01 * 1009, 2) == 10.09",
               "[x for x in (1, 2, 3, 10) if x <= 5] == [1, 2, 3] and [x for x in (1, 2, 3, 10) if x > 5] == [10]"])

    sym = sc("sym", "symbol", "Giải mã từ ngữ và ký hiệu", [
        st(table(["từ (tên trên màn hình)", "nghĩa"],
                 [["Isolation Forest, rừng cô lập", "rừng gồm nhiều cây cắt ngẫu nhiên; điểm càng nhanh bị cô lập càng lạ"],
                  ["n_estimators", "số cây trong rừng"],
                  ["contamination, tỉ lệ nhiễm", "tỉ lệ điểm lạ mà ta ĐẶT GIẢ ĐỊNH cho dữ liệu huấn luyện; dùng để chọn ngưỡng; số thực phải thuộc (0; 0,5]; mặc định là 'auto'"],
                  ["fit, predict", "huấn luyện trên dữ liệu; gắn nhãn 1 hoặc -1 cho từng điểm"],
                  ["score_samples, offset_, decision_function", "điểm bất thường (càng âm càng lạ); ngưỡng; điểm trừ ngưỡng, âm thì nhãn -1"],
                  ["ONNX, ONNX Runtime", "định dạng tệp mô hình; thư viện đọc tệp ấy và chạy mô hình"]]),
           """Bảng này giải mã các từ của bài. Rừng cô lập là rừng nhiều cây cắt ngẫu nhiên, điểm càng nhanh bị cô lập càng lạ. Tỉ lệ nhiễm là tỉ lệ điểm lạ ta đặt giả định để chọn ngưỡng. ONNX là định dạng tệp mô hình, còn ONNX Runtime là thư viện chạy tệp ấy.""",
           focus=[["1.2", "1.3"], "1.4", ["1.5", "1.6"], "1.7"], introduces=["bnx_ti_le_nhiem", "bnx_onnx"]),
        st(table(["ký hiệu", "nghĩa"],
                 [["h(x)", "số lần cắt cần để cô lập điểm x trong một cây (độ sâu)"],
                  ["E[h(x)]", "độ sâu trung bình của x trên cả rừng"],
                  ["c(n)", "độ sâu trung bình để cô lập một điểm trong cây n điểm; dùng để chuẩn hoá"],
                  ["s(x, n)", "điểm bất thường 2 mũ của (−E[h(x)] / c(n)); s = 0,5 khi độ sâu bằng c(n); s lớn hơn 0,5 nghĩa là độ sâu nhỏ hơn c(n), càng gần 1 càng lạ"]])
           + "<p class='small'>Thư viện học máy trả về điểm mang dấu âm, tức là âm s: càng âm càng lạ. Điểm thường trong bài này có s = 0,4475.</p>",
           """Bốn ký hiệu của công thức. H của x là số lần cắt để cô lập điểm x, gọi là độ sâu, và E của h là độ sâu trung bình trên cả rừng. C của n là mức chuẩn hoá, còn s là điểm bất thường, bằng không phẩy năm khi độ sâu đúng bằng c và càng gần một thì càng lạ.""",
           focus=[1, "1.2", "1.4", "2"], clear=True),
        st(table(["chữ trong mã Python", "nghĩa"],
                 [["<code>np.random.default_rng(42)</code>, <code>.normal(tâm, lệch, n)</code>", "bộ sinh số ngẫu nhiên cố định theo hạt giống 42 / sinh n số hình chuông quanh tâm"],
                  ["<code>np.concatenate</code>, <code>.reshape(-1, 1)</code>, <code>.ravel()</code>", "nối hai mảng / xếp thành một cột / trải lại thành một hàng"],
                  ["<code>float32</code>, <code>tree_.node_count</code>", "số thực 32 bit (làm tròn thô hơn) / số nút của một cây"],
                  ["<code>target_opset</code>, <code>InferenceSession</code>, <code>math.log2</code>", "phiên bản bộ phép toán của ONNX / phiên chạy một mô hình ONNX / lôgarit cơ số 2: 2 mũ mấy ra số đó"]]),
           """Bảng cuối giải mã vài chữ trong mã Python sẽ gặp: bộ sinh số, cách xếp mảng, số thực ba mươi hai bit và lôgarit cơ số hai.""", clear=True, introduces=["bnx_numpy_rng"]),
    ], checks=["alg.bnx_l23_score(0, 256) == -1.0",
               "alg.bnx_l23_score(alg.bnx_l23_c(256), 256) == -0.5"])

    intu = sc("intuition", "intuition", "Hình dung: cắt ngẫu nhiên, và từ tệp mô hình tới điểm số", [
        st(svg(1500, 480,
               panel(20, 20, 1460, 300, "Cắt ngẫu nhiên giữa giá trị nhỏ nhất và lớn nhất của các điểm còn lại (trục không theo tỉ lệ)", C_BLUE, size=24),
               "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#2a78d6" opacity="0.8"/>'
                       for x, y in [(110, 170), (150, 200), (185, 160), (225, 215), (260, 175), (295, 195), (330, 150), (365, 205), (400, 168),
                                    (435, 190), (470, 158), (505, 212), (540, 178), (575, 198), (610, 165), (645, 185), (690, 205), (730, 172)]),
               "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#dc2626" opacity="0.9"/>'
                       for x, y in [(1120, 170), (1160, 205), (1195, 160), (1230, 195), (1265, 175), (1300, 210), (1335, 165), (1370, 190), (1405, 150), (1440, 200)]),
               txt(420, 250, "≈ 1000 giao dịch thường quanh 500 nghìn", 22, "middle", "#1f2937"),
               txt(1280, 250, "10 giao dịch quanh 50 triệu", 22, "middle", "#1f2937"),
               txt(905, 212, "khoảng trống", 22, "middle", "#6b7280"),
               '<line x1="905" y1="112" x2="905" y2="180" stroke="#d97706" stroke-width="5" stroke-dasharray="10 6"/>',
               txt(905, 100, "cắt 1: rơi vào khoảng trống, xác suất ≈ 94%", 22, "middle", "#d97706", True),
               txt(750, 295, "khi đó cắt đầu tiên đã tách riêng cả nhóm điểm lạ khỏi đám đông", 24, "middle", "#1f2937", True),
               panel(20, 340, 1460, 125, "Số lần cắt trung bình để cô lập một điểm (200 lần thử, chạy thật ở bước 2)", C_GREEN, size=22),
               box(60, 392, round(15.775 * 60), 54, "điểm thường: 15,8 lần cắt", C_BLUE, size=22, bold=True),
               box(1100, 392, round(5.075 * 60), 54, "điểm lạ: 5,1 lần", C_RED, size=22, bold=True)),
           """Mỗi lần cắt chọn ngẫu nhiên một điểm giữa giá trị nhỏ nhất và lớn nhất của các điểm còn lại. Giữa hai nhóm có khoảng trống rộng, nên lần cắt đầu rơi vào đó với xác suất khoảng chín mươi bốn phần trăm và tách cả nhóm lạ ra. Vì vậy điểm lạ cần khoảng năm lần cắt, điểm thường khoảng mười sáu."""),
        st(svg(1500, 520,
               panel(20, 20, 1460, 330, "Từ huấn luyện tới chấm điểm", C_BLUE),
               box(50, 120, 220, 110, ["dữ liệu X", "1010 × 1"], C_GRAY, size=22, bold=True),
               box(340, 100, 280, 150, ["IsolationForest", "fit(X)", "100 cây"], C_BLUE, size=22, bold=True),
               box(690, 120, 230, 110, ["to_onnx", "(xuất mô hình)"], C_AMBER, size=22, bold=True),
               box(990, 120, 200, 110, ["rung.onnx", "(tệp)"], C_PURPLE, size=22, bold=True),
               box(1250, 100, 200, 150, ["ONNX Runtime", "InferenceSession", "run"], C_GREEN, size=20, bold=True),
               arrow(270, 175, 335, 175), arrow(620, 175, 685, 175), arrow(920, 175, 985, 175), arrow(1190, 175, 1245, 175),
               txt(480, 295, "môi trường huấn luyện (Python)", 22, "middle", "#1f2937"),
               txt(1350, 295, "môi trường chạy", 22, "middle", "#1f2937"),
               txt(1350, 325, "→ nhãn 1 / -1 và điểm", 22, "middle", "#16a34a", True),
               panel(20, 370, 1460, 135, "Điều mô hình KHÔNG làm được", C_RED, size=22),
               txt(750, 436, "không biết đó có phải gian lận; tỉ lệ nhiễm là giả định của ta;", 22, "middle", "#1f2937", True),
               txt(750, 474, "chưa nói gì về độ trễ (thời gian chờ một lần chạy) khi vận hành; dữ liệu mẫu chỉ có MỘT cột (số tiền)", 22, "middle", "#1f2937", True)),
           """Hình thứ hai là đường đi từ huấn luyện tới chấm điểm: rừng cô lập, bộ chuyển xuất tệp, rồi ONNX Runtime đọc tệp và cho nhãn cùng điểm. Dải đỏ nhắc bốn điều mô hình chưa làm được, từ việc không biết có phải gian lận tới việc chưa đo độ trễ."""),
    ], checks=["round(100 * (48541 - 659) / (51512 - 318)) == 94",
               "round(15.775 * 60) == 946 and round(5.075 * 60) == 304"])

    form = sc("formula", "formula", "Suy ra từng bước: dữ liệu, cắt, điểm, huấn luyện, ngưỡng, xuất ONNX", [
        st(code(DATA_PY, "Bước 1. Sinh dữ liệu với hạt giống cố định"),
           """Bước một, ta sinh dữ liệu bằng thư viện số học, hạt giống cố định nên chạy lại luôn ra y nguyên. Một nghìn giao dịch thường quanh năm trăm nghìn, mười giao dịch lạ quanh năm mươi triệu.""",
           focus=["2.2", "2.3"]),
        st(code(DATA_PY, lines=(6, 9)) + out(DATA_OUT),
           """Kết quả chạy thật: một nghìn không trăm mười dòng. Giao dịch thường từ ba trăm tới sáu trăm năm mươi, giao dịch lạ từ bốn mươi tám nghìn tới năm mươi mốt nghìn, nên hai nhóm tách xa.""",
           focus=["3.1", "3.3"], clear=True),
        st(table(["viết trong mã", "nghĩa"],
                 [["<code>d[d &lt;= c]</code>", "lọc bằng điều kiện: giữ các phần tử của <code>d</code> nhỏ hơn hoặc bằng <code>c</code>"],
                  ["<code>A if đk else B</code>", "chọn <code>A</code> nếu <code>đk</code> đúng, ngược lại chọn <code>B</code>: ở đây chọn nửa nào của <code>d</code> để giữ"],
                  ["<code>rng.uniform(d.min(), d.max())</code>, <code>while len(d) &gt; 1</code>", "số ngẫu nhiên đều giữa nhỏ nhất và lớn nhất của <code>d</code> / lặp tới khi <code>d</code> chỉ còn một phần tử"]]),
           """Hàm cắt dùng vài chỗ mới nên ta giải trước. Điều kiện trong ngoặc vuông giữ các phần tử thoả nó, và dòng chọn nửa cần giữ.""", clear=True),
        st(code(CUT_PY, "Bước 2. Tự cắt: đếm số lần cắt để cô lập một điểm")
           + "<p class='small'>Hàm này chỉ để minh hoạ: nếu dãy có các giá trị trùng nhau thì vòng lặp không bao giờ dừng, còn thư viện có độ sâu tối đa.</p>",
           """Bước hai, ta tự viết phép cắt ngẫu nhiên: mỗi vòng chọn một điểm cắt giữa giá trị nhỏ nhất và lớn nhất rồi giữ nửa chứa điểm đang xét. Nên số vòng cho tới khi còn một điểm là độ sâu.""",
           clear=True),
        jstep([("pfor", "<code>for i in (0, 1000):</code> chạy hai lần, i bằng 0 rồi 1000: điểm đầu là giao dịch thường, điểm thứ 1000 là giao dịch lạ", ""),
               (("<code>[so_lan_cat(d[i], d, rng2) for _ in range(200)]</code>", "danh sách sinh sẵn chạy 200 lần: <code>range(200)</code> là các số 0 tới 199; <code>_</code> là tên bỏ đi vì ta không dùng số vòng; gom 200 kết quả vào <code>cat</code>", "Danh sách sinh sẵn lặp hai trăm lần, gạch dưới là tên bỏ đi vì ta không dùng số vòng, và gom hai trăm kết quả vào một danh sách."), "", "")]),
        st(code(CUT_RUN) + out(CUT_OUT, "Làm thử — kết quả chạy thật"),
           """Làm thử, ta cô lập hai điểm, mỗi điểm hai trăm lần vì một lần chưa đủ tin. Điểm thường cần trung bình mười lăm phẩy tám lần cắt, điểm lạ chỉ năm phẩy không bảy lần.""",
           clear=True),
        st("""<p><b>Bước 3.</b> Độ sâu trung bình c(n) và điểm bất thường. Vì cây có thể sâu hay nông tuỳ số điểm, ta chia độ sâu cho một mức tham chiếu để điểm không phụ thuộc cỡ mẫu:</p>
$$c(n) = 2\\,(\\ln(n-1) + \\gamma) - \\frac{2\\,(n-1)}{n}, \\qquad s(x,n) = 2^{-E[h(x)]\\,/\\,c(n)}$$
<span class='note'>ln là lôgarit tự nhiên (Python: <code>math.log</code>, ví dụ ln(e) = 1); γ ≈ 0,5772 là hằng số Euler–Mascheroni. c(n) là độ sâu trung bình của một cây cô lập n điểm, thư viện dùng đúng công thức này. Mỗi cây học tối đa 256 điểm, nên mức tham chiếu là c(256).</span>""",
           """Bước ba là mức tham chiếu c của n, độ sâu trung bình của một cây n điểm, dùng lôgarit tự nhiên, và điểm bất thường s. Vì cây sâu nông tuỳ số điểm, nên ta chia độ sâu cho c để điểm không phụ thuộc cỡ mẫu, và mỗi cây học tối đa hai trăm năm mươi sáu điểm.""",
           clear=True, introduces=["gamma", "log"]),
        jstep([("pdef", "<code>def c(n):</code> nhận n, trả độ sâu tham chiếu; <code>def diem(h, n):</code> nhận độ sâu h và n, trả điểm", ""),
               (("<code>-2 ** (-h / c(n))</code>", "<code>**</code> là lũy thừa: <code>2 ** x</code> là 2 mũ x; dấu trừ đứng đầu được tính sau cùng, nên kết quả là âm của 2 mũ x", "Hai dấu sao là lũy thừa, và dấu trừ đứng đầu được tính sau cùng nên kết quả là số âm."), "<code>-2 ** 3</code> ra <code>-8</code>", "")]),
        st(code(AVG_PY, "Bước 3 (tiếp). Viết lại bằng Python"),
           """Ta viết hai công thức thành hai hàm Python, vì như vậy thử được bằng số, rồi hàm điểm đặt dấu âm như thư viện học máy.""",
           focus=[2, "2.3"], clear=True),
        st(code(AVG_PY, lines=(6, 9)) + out(AVG_OUT),
           """Kết quả chạy thật: c của hai trăm năm mươi sáu bằng mười phẩy hai bốn bốn tám, nên độ sâu càng nhỏ thì điểm càng gần âm một.""",
           focus=["3.1", 3], clear=True),
        st(table(["viết trong mã", "nghĩa"],
                 [["<code>a[1000:]</code>, <code>a[:1000]</code>", "cắt lát: từ phần tử thứ 1000 trở đi (máy đếm từ 0) / 1000 phần tử đầu"],
                  ["<code>(nhan == -1).sum()</code>", "so từng phần tử với −1 ra dãy đúng hoặc sai; <code>sum</code> đếm số chỗ đúng"]]),
           """Mã huấn luyện in số điểm gắn nhãn, nên ta giải trước hai ký hiệu. Dấu hai chấm trong ngoặc vuông cắt phần cuối hoặc phần đầu dãy, nên tách được hai nhóm. So với âm một rồi cộng lại là đếm số điểm gắn âm một.""", clear=True),
        st(code(TRAIN_PY, "Bước 4. Huấn luyện rừng cô lập: 100 cây, tỉ lệ nhiễm 1%")
           + "<p class='small'>Cài: <code>pip install scikit-learn==1.9.1 skl2onnx==1.20.0 onnxruntime==1.31.1</code> (bài chạy Python 3.13, numpy 2.5.4; <code>gói==số</code> là cài đúng phiên bản đó). Số nút và lỗi ONNX ở bước sau phụ thuộc phiên bản. <code>random_state</code>: hạt giống của rừng, đặt cố định để chạy lại ra y hệt.</p>",
           """Bước bốn, ta huấn luyện rừng cô lập bằng thư viện học máy, với một trăm cây và tỉ lệ nhiễm một phần trăm. Rồi ta dự đoán nhãn cho chính dữ liệu huấn luyện, vì muốn biết máy gắn nhãn thế nào.""",
           focus=["2.2", "2.5"], clear=True),
        st(code(TRAIN_PY, lines=(6, 9)) + out(TRAIN_OUT),
           """Kết quả chạy thật: cả mười điểm lạ nhận nhãn âm một, nhưng tổng là mười một nhãn, nghĩa là một giao dịch thường bị gắn oan.""",
           focus=["3.1", "3.2", "3.4"], clear=True),
        st(f"""<p><b>Bước 5.</b> Vì sao ra đúng ngưỡng ấy. Tỉ lệ nhiễm 1% nghĩa là: lấy điểm của chính dữ liệu huấn luyện, đặt ngưỡng ở phân vị 1% thấp nhất. Điểm nào thấp hơn ngưỡng nhận nhãn -1:</p>
$$\\text{{quyết định}} = \\text{{điểm}} - \\text{{offset\\_}}, \\qquad \\text{{quyết định}} < 0 \\;\\Rightarrow\\; \\text{{nhãn}} = \\hl{{-1}}$$
<span class='note'>Theo quy tắc đếm (đúng khi các điểm khác nhau): 0,01 × 1009 = 10,09, làm tròn lên là 11 điểm nằm dưới ngưỡng, dù thật sự lạ chỉ có 10: ngưỡng do ta đặt, không do mô hình tìm ra.</span>""",
           """Bước năm là vì sao ra đúng ngưỡng ấy. Tỉ lệ nhiễm một phần trăm nghĩa là đặt ngưỡng ở phân vị một phần trăm thấp nhất của điểm trên dữ liệu huấn luyện. Theo quy tắc đếm, mười phẩy không chín làm tròn lên thành mười một điểm dưới ngưỡng dù lạ thật chỉ có mười, vì ngưỡng do ta đặt.""",
           clear=True),
        st(code(SCORE_PY, "Bước 5 (tiếp). Điểm trung bình của hai nhóm, quy ra độ sâu") + out(SCORE_OUT)
           + "<p class='small'>11,88 khác 15,8 ở hình trước vì hai thước đo: 15,8 là số lần cắt riêng một điểm, không giới hạn độ sâu, trên cả 1 010 điểm; 11,88 quy từ điểm trung bình của nhóm trong rừng, mỗi cây chỉ học tối đa 256 điểm và cắt cụt độ sâu. <code>max_samples_</code>: số điểm mỗi cây học.</p>",
           """Ta lấy điểm trung bình của hai nhóm rồi quy về độ sâu. Nhóm thường có điểm âm không phẩy bốn bốn bảy năm, độ sâu khoảng mười một phẩy tám tám, còn nhóm lạ chỉ hai phẩy bốn chín. Số này khác mười lăm phẩy tám ở hình trước vì hai thước đo khác nhau.""",
           focus=["2.1", "4.1", "4.2"], clear=True),
        st(table(["viết trong mã", "nghĩa"],
                 [["<code>open(\"rung.onnx\", \"wb\").write(…)</code>", "ghi chuỗi byte vào tệp (<code>wb</code>: ghi nhị phân)"],
                  ["<code>phien.get_inputs()[0].name</code>", "tên ô nhập đầu tiên của mô hình"],
                  ["<code>nhan_onnx, diem_onnx = phien.run(None, {ten: x32})</code>", "chạy mô hình (<code>None</code>: lấy mọi đầu ra), đưa dữ liệu vào ô nhập tên <code>ten</code>; gán hai kết quả cho hai biến"]]),
           """Phần ONNX có ba chỗ mới nên ta giải trước. Lệnh ghi byte ra tệp, lệnh lấy tên ô nhập, và lệnh chạy trả hai kết quả.""", clear=True),
        jstep([("pimp", "<code>from skl2onnx import to_onnx</code>, <code>import onnxruntime as rt</code>: lấy thư viện về, gọi <code>onnxruntime</code> là <code>rt</code>", ""),
               ("pf", "<code>f\"sai khác điểm lớn nhất: {lech:.1e}\"</code>: <code>.1e</code> in dạng khoa học, ví dụ <code>1.8e-07</code> là 1,8 nhân mười mũ âm bảy", ""),
               (("<code>abs(a - b).max()</code>", "hiệu từng cặp, lấy giá trị tuyệt đối rồi chọn số lớn nhất", "Hiệu từng cặp, lấy giá trị tuyệt đối, rồi chọn số lớn nhất, tức sai khác nhiều nhất."), "", "")]),
        st(code(ONNX_PY, "Bước 6. Xuất sang ONNX, chạy bằng ONNX Runtime, so với mô hình trong Python")
           + "<p class='small'>Đầu ra thứ hai của tệp ONNX là điểm quyết định (điểm trừ ngưỡng), nên ta so nó với decision_function. target_opset: phiên bản bộ phép toán (opset) của từng miền.</p>",
           """Bước sáu, ta xuất mô hình sang ONNX, ghi ra một tệp rồi nạp vào ONNX Runtime. Ta khai phiên bản bộ phép toán, vì bộ chuyển và thư viện chạy phải hiểu cùng một bản.""",
           focus=["2.4", "2.3"], clear=True),
        st(code(ONNX_PY, lines=(10, 12)) + out(ONNX_OUT),
           """Kết quả chạy thật: một nghìn không trăm mười nhãn đều giống mô hình trong Python, điểm quyết định sai khác nhiều nhất cỡ mười mũ âm bảy. Số thực ba mươi hai bit làm tròn thô hơn, nên điểm sát ngưỡng vẫn có thể bị lật nhãn.""",
           focus=["1.1", "3.1", "3.2"], clear=True),
    ], checks=["round(alg.bnx_l23_c(256), 4) == 10.2448",
               "round(alg.bnx_l23_score(alg.bnx_l23_c(256) / 2, 256), 4) == -0.7071",
               "round(alg.bnx_l23_score(1, 256), 4) == -0.9346 and alg.bnx_l23_score(alg.bnx_l23_c(256), 256) == -0.5",
               "alg.bnx_l23_label(-0.8448, -0.7353) == -1 and alg.bnx_l23_label(-0.4475, -0.7353) == 1",
               "alg.bnx_l23_expected_flags(1010, 0.01) == 11 and 11 - 10 == 1",
               "round(alg.bnx_l23_depth_from_score(-0.8448, 256), 2) == 2.49 and round(alg.bnx_l23_depth_from_score(-0.4475, 256), 2) == 11.88"])

    ex = sc("example", "example", "Ví dụ rừng cô lập trên 1010 giao dịch, từng phép tính", [
        st(f"""<p>1000 giao dịch thường quanh 500 nghìn đồng, 10 giao dịch lạ 50 triệu đồng; rừng 100 cây, tỉ lệ nhiễm 1%; mỗi cây huấn luyện trên tối đa 256 điểm. {NOTE_ILL}</p>
$$① \\; c(256) = 2\\,(\\ln 255 + 0{{,}}57722) - \\frac{{2 \\cdot 255}}{{256}} = 12{{,}}2370 - 1{{,}}9922 = \\hl{{10{{,}}2448}}$$""",
           """Ta làm trọn một ví dụ, rừng một trăm cây. Phép tính thứ nhất, c của hai trăm năm mươi sáu bằng mười hai phẩy hai ba bảy không trừ một phẩy chín chín hai hai, bằng mười phẩy hai bốn bốn tám."""),
        st("""<p>Dùng lại c(256) = 10,2448 ở phép ①. Nhóm lạ có điểm trung bình −0,8448.</p>
$$② \\; \\text{độ sâu} = -c \\cdot \\log_2(0{,}8448) = 10{,}2448 \\cdot 0{,}2433 = \\hl{2{,}49} \\text{ lần cắt}$$""",
           """Phép tính thứ hai, nhóm lạ có điểm trung bình âm không phẩy tám bốn bốn tám, nên độ sâu quy đổi khoảng hai phẩy bốn chín lần cắt.""", introduces=["sub"]),
        st("""<p>Nhóm thường có điểm trung bình −0,4475.</p>
$$③ \\; \\text{độ sâu} = -10{,}2448 \\cdot \\log_2(0{,}4475) = 10{,}2448 \\cdot 1{,}1600 = \\hl{11{,}88} \\text{ lần cắt}$$""",
           """Phép tính thứ ba, nhóm thường có độ sâu khoảng mười một phẩy tám tám, nhiều hơn điểm lạ khoảng bốn phẩy tám lần."""),
        st("""<p>Ngưỡng của rừng: offset_ = −0,7353 (phân vị 1%). Dùng điểm ở ② và ③.</p>
$$④ \\; \\text{lạ: } -0{,}8448 + 0{,}7353 = \\hl{-0{,}1095} < 0 \\Rightarrow -1;\\quad \\text{thường: } -0{,}4475 + 0{,}7353 = \\hlg{+0{,}2878} \\Rightarrow 1$$
<span class='note'>Toàn tập: 11 điểm dưới ngưỡng = 10 điểm lạ + 1 điểm thường bị gắn oan.</span>""",
           """Phép tính thứ tư, với ngưỡng âm không phẩy bảy ba năm ba, nhóm lạ có điểm quyết định âm nên nhãn âm một, còn nhóm thường dương nên nhãn một.""",
           clear=True),
        st("""<p>Xuất ONNX, chạy trên cả 1010 điểm.</p>
$$⑤ \\; \\text{cùng nhãn với mô hình Python: } \\hlg{1010 / 1010}; \\quad \\text{sai khác điểm lớn nhất} = \\hl{1{,}8 \\cdot 10^{-7}}$$""",
           """Phép tính thứ năm, xuất ONNX rồi chạy trên cả một nghìn không trăm mười điểm cho một nghìn không trăm mười nhãn giống mô hình trong Python.""",
           ),
    ], checks=["round(2 * (__import__('math').log(255) + 0.57722) - 2 * 255 / 256, 4) == 10.2448",
               "round(alg.bnx_l23_depth_from_score(-0.8448, 256), 2) == 2.49",
               "round(alg.bnx_l23_depth_from_score(-0.4475, 256), 2) == 11.88 and round(11.88 / 2.49, 1) == 4.8",
               "round(alg.bnx_l23_decision(-0.8448, -0.7353), 4) == -0.1095 and round(alg.bnx_l23_decision(-0.4475, -0.7353), 4) == 0.2878",
               "alg.bnx_l23_expected_flags(1010, 0.01) == 10 + 1"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: danh tính điểm và năm hạt giống", [
        st(code(CHECK_ID_PY, "Kiểm 1. decision_function đúng bằng score_samples trừ offset_") + out(CHECK_ID_OUT),
           """Kiểm bằng đường khác: thư viện định nghĩa điểm quyết định bằng điểm bất thường trừ ngưỡng, nên ta tính hai vế riêng. Kết quả chạy thật: hai vế sai khác không, và điểm âm trùng khít nhãn âm một.""",
           focus=[1, "4.1"]),
        st(code(CHECK_SEED_PY, "Kiểm 2. Đổi hạt giống: kết quả có đổi không?") + out(CHECK_SEED_OUT),
           """Kiểm hai, đổi hạt giống năm lần từ không tới bốn: lần nào cũng bắt đủ mười điểm lạ và gắn tổng cộng mười một điểm. Dữ liệu tách xa nên kết quả không phụ thuộc hạt giống.""",
           focus=["2.5", "4.1"], clear=True),
    ], checks=["alg.bnx_l23_expected_flags(1010, 0.01) == 11 and int(0.01 * (1010 - 1)) + 1 == 11",
               "round(alg.bnx_l23_depth_from_score(-0.8448, 256), 2) < round(alg.bnx_l23_depth_from_score(-0.4475, 256), 2)"])

    quymo = sc("quymo", "example", "Khi giao dịch tăng ×10 và ×100: mô hình và người xét thay đổi ra sao", [
        st(QUYMO.show(lines=(3, 9), title="QuyMo.py (trích): dữ liệu ở ba cỡ, vẫn 1% là điểm lạ"),
           """Ta đo khi giao dịch tăng dần, ở ba cỡ là một nghìn không trăm mười, mười nghìn một trăm và một trăm lẻ một nghìn, vẫn một phần trăm là lạ.""",
           clear=True),
        st(QUYMO.show(lines=(10, 15), title="QuyMo.py (tiếp): huấn luyện lại, đếm nhãn âm một và số nút của rừng") + QUYMO.out_html(),
           """Mỗi lần ta huấn luyện lại rừng, đếm số nhãn âm một, số điểm lạ thật bị bắt và tổng số nút. Kết quả chạy thật: nhãn âm một tăng theo cỡ dữ liệu, còn số nút giữ quanh mười một nghìn bốn trăm.""",
           focus=["1.1", "2.1", "2.2", "2.3"], clear=True),
        st(table(["số giao dịch N", "gắn nhãn −1", "điểm lạ thật bị bắt", "tổng số nút của rừng", "người xét cần mỗi ngày (40 ca mỗi người, số minh hoạ)"],
                 [[nowrap("1 010 (×1)"), "11", "10 / 10", "11 384", "1"],
                  [nowrap("10 100 (×10)"), "101", "100 / 100", "11 802", "3"],
                  [nowrap("101 000 (×100)"), "1 005", "1 000 / 1 000", "11 436", "26"]])
           + "<p class='small'>Ở 101 000 điểm quy tắc đếm cho 1 010 nhưng chạy thật ra 1 005: chỉ có 3 613 giá trị khác nhau trên 101 000 điểm, nên nhiều điểm trùng đúng ở ngưỡng và quy tắc không còn chính xác.</p>",
           """Bảng cho thấy hai cách tăng khác nhau. Mô hình không to lên vì mỗi cây chỉ học tối đa hai trăm năm mươi sáu điểm, nhưng số giao dịch bị gắn tăng theo tỉ lệ. Nếu mỗi người xét bốn mươi ca một ngày thì cần hai mươi sáu người.""",
           focus=[0, "1.2", "1.3"], clear=True),
        st(table(["cách", "được", "mất"],
                 [["hạ tỉ lệ nhiễm", "ít ca hơn cho người xét", "bỏ sót điểm lạ thật nếu đặt quá thấp (ở trên, 0,001 chỉ bắt 2 trên 10)"],
                  ["xếp ca theo điểm, xét ca đáng ngờ nhất trước", "người xét xem đúng ca cần xem", "cần quy trình và hàng đợi; ca ở cuối có thể không bao giờ được xem"],
                  ["chặn tự động mọi nhãn −1", "nhanh, không tốn người", "chặn oan khách thật, như lương lớn hợp lệ"]]),
           """Người làm nghề phải chọn khi quy mô tăng. Hạ tỉ lệ nhiễm thì ít ca hơn nhưng bỏ sót. Xếp ca theo điểm thì cần thêm quy trình. Chặn tự động thì nhanh, nhưng chặn oan khách thật.""",
           focus=["1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_l23_expected_flags(1010, 0.01) == 11 and alg.bnx_l23_expected_flags(10100, 0.01) == 101",
               "abs(1005 - alg.bnx_l23_expected_flags(101000, 0.01)) <= 5",
               "[alg.bnx_l23_reviewers(f, 40) for f in (11, 101, 1005)] == [1, 3, 26]",
               "10100 // 1010 == 10 and 101000 // 1010 == 100"])

    pit = sc("pitfalls", "pitfall", "Điều mô hình KHÔNG làm được, và lỗi theo từng giai đoạn", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Tin rằng nhãn -1 là “gian lận”, và tỉ lệ nhiễm là điều mô hình tự tìm ra. Đổi tỉ lệ nhiễm, số điểm bị gắn đổi theo, còn lạ thật vẫn là 10: đặt thấp thì bỏ sót, đặt cao thì gắn oan.</div>""" + code(LIMIT_PY) + out(LIMIT_OUT),
           """Lỗi thứ nhất, của người mới, là tin rằng nhãn âm một nghĩa là gian lận và tỉ lệ nhiễm do mô hình tự tìm ra. Đổi tỉ lệ nhiễm thì số điểm bị gắn đổi theo, còn lạ thật vẫn là mười.""",
           focus=[1, 4], clear=True),
        st(code(LIMIT2_PY, "Hai điểm mô hình trả lời sai điều ta cần") + out(LIMIT2_OUT)
           + "<div class='box key'>Số tiền 520 nghìn trông như người thường nên nhãn 1: <b>kẻ gian tiêu nhỏ không bị thấy</b>. Số tiền 50 triệu lạ nên nhãn -1 (vì rừng đã thấy nhóm này hiếm): <b>lương hợp lệ vẫn bị gắn</b>. Lạ không đồng nghĩa gian lận: cần người xét lại.</div>",
           """Hai điểm thêm vào cho thấy giới hạn: kẻ gian chuyển năm trăm hai mươi nghìn trông như người thường nên không bị thấy, còn lương hợp lệ năm mươi triệu bị gắn âm một.""",
           focus=["2.1", "4.1"], clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Xuất ONNX mà không khai phiên bản miền (nhóm phép toán) <code>ai.onnx.ml</code>, tức các phép toán học máy cổ điển, hoặc xuất xong chỉ thử vài điểm mẫu rồi cho chạy. Thư viện xuất của máy này dừng ngay với một lỗi:</div>"""
           + code(ONNX_ERR_PY) + out(ONNX_ERR_OUT, "Thông báo lỗi thật (dòng cuối của vết lỗi, lược bớt)")
           + """<p class="small">Cách chữa: khai target_opset như bước 6 (ở đây ai.onnx.ml bản 3), ghi lại bản của ba thư viện lúc xuất (học máy, bộ chuyển, ONNX Runtime), rồi so nhãn VÀ điểm trên TOÀN BỘ dữ liệu, nhất là các điểm sát ngưỡng, không chỉ vài mẫu.</p>""",
           """Lỗi thứ hai, của người đã đi làm, là xuất ONNX mà không khai phiên bản miền học máy, và thư viện dừng ngay với một lỗi. Cách chữa là khai phiên bản đích và so cả nhãn lẫn điểm trên toàn bộ dữ liệu.""",
           focus=[1, 4], clear=True),
        st(code(DRIFT_PY, "Lỗi 3 (vận hành lâu dài): tháng sau mức chi tiêu thường đổi") + out(DRIFT_OUT)
           + """<p class="small">Vì sao: mức 1500 nghìn nằm trong khoảng trống giữa hai nhóm cũ, nên bị cô lập rất nhanh.</p>
<p class="small">Cách chữa: theo dõi tỉ lệ nhãn -1 và phân bố điểm mỗi ngày, so với lúc huấn luyện (tỉ lệ 1% chỉ đáng so khi dữ liệu giống lúc huấn luyện, vì 1% vốn là giả định); huấn luyện lại theo lịch. Chạy ngon trên máy cá nhân chưa nói gì về <b>độ trễ</b> (thời gian chờ một lần chạy) khi vận hành thật: nạp tệp một lần lúc khởi động, đo nhiều lần, báo phân vị 95 và 99.</p>""",
           """Lỗi thứ ba lộ ra khi vận hành lâu: tháng sau mức chi tiêu đổi, và chín trăm bảy mươi bảy trên một nghìn giao dịch thường bị gắn âm một. Hãy theo dõi tỉ lệ nhãn âm một mỗi ngày và huấn luyện lại theo lịch.""",
           focus=[1, 1, 2, 3], clear=True),
    ], checks=["alg.bnx_l23_expected_flags(1010, 0.001) == 2 and alg.bnx_l23_expected_flags(1010, 0.01) == 11 and alg.bnx_l23_expected_flags(1010, 0.05) == 51",
               "alg.bnx_l23_expected_flags(1010, 0.05) - 10 == 41",
               "alg.bnx_l23_expected_flags(1010, 0.05) == int(0.05 * (1010 - 1)) + 1 and 10 - 2 == 8",
               "977 + 23 == 1000"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề (dùng c(256) = 10,2448 và offset_ = −0,7353 của bài)"],
                 [["1", "Một điểm có độ sâu trung bình bằng một nửa c(256). Điểm bất thường (dấu âm kiểu thư viện) là bao nhiêu? Điểm quyết định là bao nhiêu, nhãn là gì?"],
                  ["2", "Đặt tỉ lệ nhiễm 2% cho 1010 điểm. Theo quy tắc đếm ở phần phân vị, bao nhiêu điểm bị gắn -1? Nếu thật sự lạ chỉ có 10, bao nhiêu điểm thường bị gắn oan?"],
                  ["3", "Quyết định: giao dịch bị gắn -1. Chặn tự động hay chuyển người xét? Cho biết được và mất."]]),
           """Đến lượt bạn. Câu một, điểm có độ sâu trung bình bằng một nửa c của hai trăm năm mươi sáu thì điểm bất thường, điểm quyết định và nhãn là gì? Câu hai, đặt tỉ lệ nhiễm hai phần trăm cho một nghìn không trăm mười điểm thì bao nhiêu điểm bị gắn âm một và bao nhiêu bị gắn oan? Câu ba, giao dịch bị gắn âm một thì chặn tự động hay chuyển người xét? Hãy dừng video và làm ra giấy.""",
           focus=[0, "1.2", "1.3", "1.4"], pause=25),
        st("""$$2^{-1/2} \\approx 0{,}7071 \\;\\Rightarrow\\; \\text{điểm} = -0{,}7071;\\quad -0{,}7071 + 0{,}7353 = \\hl{+0{,}0282} \\geq 0 \\;\\Rightarrow\\; \\text{nhãn } \\hlg{1}$$""",
           """Đáp án câu một: số mũ là âm một phần hai nên điểm là âm không phẩy bảy không bảy một. Điểm quyết định là dương không phẩy không hai tám hai, không âm nên nhãn là một."""),
        st("""$$0{,}02 \\cdot (1010 - 1) = 20{,}18 \\;\\Rightarrow\\; \\text{làm tròn lên } \\hl{21} \\text{ điểm bị gắn};\\quad 21 - 10 = \\hlg{11} \\text{ điểm thường bị gắn oan}$$""",
           """Đáp án câu hai: hai phần trăm của một nghìn không trăm lẻ chín là hai mươi phẩy mười tám, làm tròn lên thành hai mươi mốt điểm bị gắn, và mười một điểm thường bị gắn oan."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["chuyển người xét", "giao dịch hợp lệ lớn, như lương 50 triệu, không bị chặn oan; kẻ gian vẫn bị giữ lại để xem", "chậm hơn, tốn công; tỉ lệ nhiễm cao thì hộp thư ngập"],
                  ["giữ lại và yêu cầu xác thực thêm", "đỡ chặn oan, người xét chỉ nhận ca còn nghi", "thêm một bước cho khách; cần có kênh xác thực"],
                  ["chặn tự động mọi nhãn -1", "nhanh, không tốn người", "chặn oan khách thật; không sửa được sai sót của giả định tỉ lệ nhiễm"]]),
           """Đáp án câu ba: nhãn âm một chỉ nói giao dịch lạ, không nói gian lận, nên chuyển người xét, đổi lại chậm hơn. Chặn tự động thì nhanh nhưng chặn oan khách thật.""",
           focus=["1.2", "1.3", "1.4"]),
    ], checks=["round(alg.bnx_l23_score(alg.bnx_l23_c(256) / 2, 256), 4) == -0.7071",
               "round(alg.bnx_l23_decision(-0.7071, -0.7353), 4) == 0.0282 and alg.bnx_l23_label(-0.7071, -0.7353) == 1",
               "alg.bnx_l23_expected_flags(1010, 0.02) == 21 and int(0.02 * (1010 - 1)) + 1 == 21 and 21 - 10 == 11"])

    lab_pr = practice_scene(sc, "Tự làm: mức tham chiếu, điểm, nhãn và số điểm bị gắn", practice_steps2(
        st, "BNX", "L23",
        """<p><b>Đề</b>: viết <code>mau.py</code> (chỉ <code>import math</code>), mỗi cây học trên <code>n = 128</code> điểm:</p>
<ol><li>mức tham chiếu <code>c(128)</code> theo công thức bước 3, <code>γ = 0.5772156649</code></li><li>hai điểm A, B có độ sâu trung bình 2 và 9: điểm bất thường <code>s = −2^(−h/c)</code>; ngưỡng <code>offset = −0.6</code>; điểm quyết định; nhãn</li><li>3000 giao dịch, tỉ lệ nhiễm 3%: số điểm bị gắn −1 theo quy tắc đếm; lạ thật chỉ 25 nên bao nhiêu điểm thường bị gắn oan</li></ol>
<p class="note">Khuôn bốn dòng in nằm ở <code>de.md</code>; số liệu khác ví dụ trong bài.</p>""",
        """Bây giờ tới phần bạn tự làm, chỉ cần Python thuần. Hãy tính mức tham chiếu, rồi điểm bất thường, điểm quyết định và nhãn của hai điểm có độ sâu hai và chín. Sau đó đếm điểm bị gắn âm một và điểm thường bị gắn oan, với ba nghìn giao dịch, tỉ lệ nhiễm ba phần trăm và lạ thật hai mươi lăm. Hãy dừng video và tự viết.""",
        LAB.out, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> <code>c = 2 * (math.log(n - 1) + 0.5772156649) - 2 * (n - 1) / n</code>; <code>diem = -2 ** (-h / c)</code>; nhãn −1 nếu <code>diem - offset &lt; 0</code>; số điểm gắn: <code>math.ceil(p * (N - 1))</code>.
Lời giải ở <code>labs/BNX/L23/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, nhãn là âm một nếu điểm trừ ngưỡng âm, và số điểm gắn là p nhân N trừ một, làm tròn lên. Lời giải chỉ mở sau khi đã thử.""", pause=120), "BNX", "L23")

    rec = sc("recap", "recap", "Chuỗi logic, góc phỏng vấn & tư duy cần mang theo", [
        st(chain("điểm lạ bị cô lập sau ít lần cắt", "điểm = 2 mũ âm độ sâu / c(n)", "tỉ lệ nhiễm → ngưỡng → nhãn 1 / -1", "xuất ONNX, chạy ONNX Runtime", "so nhãn và điểm trên toàn tập", "lạ ≠ gian lận: người xét"),
           """Tổng kết: điểm lạ bị cô lập sau ít lần cắt, tỉ lệ nhiễm cho ra ngưỡng rồi nhãn, và mô hình ONNX được so nhãn lẫn điểm trên toàn tập. Lạ không có nghĩa là gian lận.""",
           focus=[0, "1.1", "1.3", "1.5", "1.7", "1.9"]),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời một dòng"],
                 [["Isolation Forest hoạt động thế nào?", "cắt ngẫu nhiên nhiều lần; điểm lạ bị cô lập sau ít lần cắt hơn nên có độ sâu trung bình nhỏ, điểm gần âm 1"],
                  ["Tỉ lệ nhiễm (contamination) là gì, ai quyết định nhãn -1?", "giả định của người đặt, dùng chọn ngưỡng theo phân vị; mặc định 'auto' thì ngưỡng cố định −0,5"],
                  ["Vì sao xuất ONNX, và kiểm gì sau khi xuất?", "tệp ONNX chạy không cần mã Python; ghi lại bản thư viện, so nhãn và điểm trên toàn tập"]])
           + "<span class='note'>Trả lời bằng cơ chế; không nêu số liệu của tổ chức thật, không nói đã làm ở quy mô nào.</span>",
           """Người phỏng vấn hay hỏi: rừng cô lập hoạt động thế nào, tỉ lệ nhiễm là gì, và vì sao xuất ONNX rồi kiểm gì. Hãy trả lời bằng cơ chế, không nêu số liệu thật.""",
           focus=[1, 1], clear=True),
        st("""<div class='box key'><b>Tư duy:</b> với mỗi mô hình phát hiện bất thường, hỏi ba điều: con số nào là <b>giả định của ta</b> (tỉ lệ nhiễm), kết quả nào cần <b>người xét lại</b> (lạ chưa phải gian lận), và khi giao dịch tăng gấp trăm lần thì người xét và độ trễ ra sao.</div>
<p class='small'>Bài sau (Bài 24): JPA/Hibernate và Spring Data — thực thể, ngữ cảnh bền vững và vấn đề N+1.</p>""",
           """Điều cần mang theo: với mỗi mô hình phát hiện bất thường, hỏi con số nào là giả định, kết quả nào cần người xét lại. Ở bài hai mươi bốn, ta học cách chương trình Java đọc ghi cơ sở dữ liệu qua thực thể.""",
           clear=True, forward_ref=True),
    ], checks=["alg.bnx_l23_label(alg.bnx_l23_score(alg.bnx_l23_c(256) / 2, 256), -0.7353) == 1",
               "alg.bnx_l23_expected_flags(1010, 0.01) == 11"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L23", "scikit_learn_onnx_rung_co_lap",
                  "Bài 23 — Từ scikit-learn tới ONNX Runtime: rừng cô lập cho phát hiện bất thường",
                  "curriculum/bnx.yaml L23; audit/bnx/verify_bnx.py L23; audit/bnx/sources_l23.md [SKIF] scikit-learn 1.9.1 IsolationForest "
                  "(tài liệu và mã nguồn, đọc 2026-11-12), [SKOD] hướng dẫn phát hiện ngoại lai scikit-learn, [ORTP] ONNX Runtime Python, "
                  "[S2O] sklearn-onnx 1.20.0, [SKPERS] lưu và nạp mô hình scikit-learn, [ORTJ] ONNX Runtime với Java, [ORTAPI] ONNX Runtime Python (khai nhà cung cấp thực thi); chạy thật bằng scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.1, numpy 2.5.4 "
                  "(audit/bnx/deps/l23/README.md); dữ liệu sinh với hạt giống cố định; mọi số liệu là số minh hoạ; quy mô: huấn luyện lại rừng ở 1 010, 10 100, 101 000 điểm (audit/bnx/progcache/L23.json); lab: Python thuần chạy thật",
                  ["Giải thích vì sao điểm lạ bị cô lập sau ít lần cắt hơn điểm thường",
                   "Huấn luyện một rừng cô lập bằng scikit-learn và đọc nhãn 1, âm 1",
                   "Xuất mô hình sang ONNX và chạy bằng ONNX Runtime, so kết quả với mô hình scikit-learn",
                   "Nêu giới hạn của nguyên mẫu học thuật so với hệ thống vận hành thật",
                   "So sánh số nhãn âm một, số nút của rừng và số người xét khi giao dịch tăng từ 1 010 lên 10 100 và 101 000",
                   "Tính mức tham chiếu, điểm bất thường, nhãn và số điểm bị gắn của một rừng khác bằng mã Python"],
                  scenes,
                  covers=[(1, "example"), (2, "formula"), (3, "formula"), (4, "pitfalls"), (5, "quymo"), (6, "practice")])
