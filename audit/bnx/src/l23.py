from lib import *

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

NOTE_ILL = "<span class='note'>(số minh hoạ: dữ liệu sinh ngẫu nhiên, hạt giống cố định, không phải của tổ chức nào)</span>"


def build():
    hook = sc("hook", "hook", "Sáng thứ hai: 1010 giao dịch, chưa ai gán nhãn, máy chỉ ra giao dịch lạ thế nào?", [
        st(f"""<p>Mỗi sáng, bộ phận rủi ro nhận <b>1010</b> giao dịch chuyển tiền của hôm qua: <b>1000</b> giao dịch quanh <b>500 nghìn</b> đồng và <b>10</b> giao dịch ở mức <b>50 triệu</b> đồng.</p>
<div class="box key">Không giao dịch nào có nhãn “gian lận” hay “bình thường”. Làm sao để máy <b>chỉ ra giao dịch lạ</b> cho người xét, mà không cần ai gán nhãn trước? Và mô hình huấn luyện bằng Python chạy ra sao khi đem đi vận hành?</div>
{NOTE_ILL}""",
           """Chào bạn, mỗi sáng bộ phận rủi ro nhận một nghìn không trăm mười giao dịch chuyển tiền của hôm qua. Một nghìn giao dịch quanh năm trăm nghìn đồng, và mười giao dịch ở mức năm mươi triệu đồng.
           Không giao dịch nào có nhãn gian lận hay bình thường. Làm sao để máy chỉ ra giao dịch lạ cho người xét, mà không cần ai gán nhãn trước?
           Và mô hình huấn luyện bằng Python chạy ra sao khi đem đi vận hành? Mọi số liệu trong bài là số minh hoạ, dữ liệu sinh ngẫu nhiên với hạt giống cố định.""",
           focus=[1, 1, 2, 2, 2, 3]),
        st(table(["câu hỏi", "phần trả lời trong bài"],
                 [["vì sao điểm lạ nổi lên mà không cần nhãn", "cắt ngẫu nhiên: điểm lạ bị cô lập sau ít lần cắt"],
                  ["huấn luyện và đọc kết quả thế nào", "rừng cô lập trong thư viện học máy: nhãn 1 và âm 1"],
                  ["đem sang môi trường vận hành ra sao", "xuất tệp ONNX, chạy bằng ONNX Runtime, so với mô hình trong Python"],
                  ["mô hình KHÔNG làm được gì", "không biết gian lận; tỉ lệ nhiễm là giả định; chưa đo độ trễ; dữ liệu mẫu chỉ có một cột"]]),
           """Bài này trả lời bốn câu hỏi. Vì sao điểm lạ nổi lên mà không cần nhãn. Huấn luyện và đọc kết quả thế nào. Đem sang môi trường vận hành ra sao.
           Và điều quan trọng nhất, mô hình không làm được gì.""", clear=True),
    ], checks=["1000 + 10 == 1010",
               "alg.bnx_l23_expected_flags(1010, 0.01) == 11"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Trung bình và độ lệch chuẩn", "trung bình là mức ở giữa; độ lệch chuẩn cho biết các giá trị tản ra quanh nó bao xa; dữ liệu bài rải hình chuông (phân phối chuẩn)", "quanh 500 nghìn, độ lệch chuẩn 50 nghìn: hầu hết nằm trong khoảng 400 tới 600"],
                  ["② Cắt đôi một dãy số", "chọn một điểm cắt rồi chia dãy thành nửa nhỏ hơn và nửa lớn hơn", "cắt dãy 1, 2, 3, 10 tại 5: nửa trái 1, 2, 3; nửa phải 10"],
                  ["③ Phân vị", "mức mà một tỉ lệ cho trước của các giá trị nằm dưới nó; số giá trị dưới ngưỡng: phần nguyên của p × (n−1), cộng một", "1% của 1010 giá trị: 11 giá trị dưới ngưỡng (tính ở bước sau)"],
                  ["④ Mô hình và nhãn", "mô hình: bản ghi cách tính điểm, học từ dữ liệu; nhãn thật: đáp án do người gán (ta không có); nhãn của mô hình: 1 (thường) hoặc âm 1 (lạ)", "mô hình không nói “gian lận”, chỉ nói “lạ”"]]),
           """Trước hết ta cần hiểu bốn điều. Trung bình là mức ở giữa, còn độ lệch chuẩn cho biết các giá trị tản ra quanh nó bao xa. Dữ liệu của bài rải theo hình chuông quanh trung bình, gọi là phân phối chuẩn.
           Cắt đôi một dãy số là chọn một điểm cắt rồi chia dãy thành nửa nhỏ hơn và nửa lớn hơn.
           Phân vị là mức mà một tỉ lệ cho trước của các giá trị nằm dưới nó. Quy tắc đếm của bài: với n giá trị và tỉ lệ p, số giá trị dưới ngưỡng là phần nguyên của p nhân n trừ một, rồi cộng một.
           Mô hình là bản ghi cách tính điểm, học từ dữ liệu bằng bước huấn luyện. Nhãn thật là đáp án do người gán, ta không có. Nhãn của mô hình là kết quả máy trả ra, một cho điểm thường, hoặc âm một cho điểm lạ. Mô hình không nói gian lận, chỉ nói lạ."""),
        st("""$$p \\cdot (n-1) = 0{,}01 \\cdot (1010 - 1) = 10{,}09 \\text{ nên phần nguyên là } 10, \\text{ cộng một } = \\hl{11}$$
<span class='note'>Điều kiện của quy tắc: p × (n−1) không tròn và các giá trị không trùng nhau. Làm thử: dãy 1, 2, 3, 10 cắt tại 5 thì 10 đứng một mình ở nửa phải sau đúng một lần cắt; còn 1, 2, 3 cần thêm cắt nữa mới tách rời nhau.</span>""",
           """Một ví dụ số cho phân vị. Với một phần trăm của một nghìn không trăm mười giá trị, ta nhân không phẩy không một với một nghìn không trăm lẻ chín, được mười phẩy không chín. Phần nguyên là mười, cộng một thì có mười một giá trị dưới ngưỡng, và ta sẽ gặp lại quy tắc này khi đặt ngưỡng.
           Làm thử với dãy một, hai, ba, mười. Cắt tại năm thì số mười đứng một mình sau đúng một lần cắt, còn một, hai, ba cần thêm lần cắt nữa mới tách rời nhau.""", clear=True),
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
           """Bảng này giải mã các từ của bài. Rừng cô lập là rừng gồm nhiều cây cắt ngẫu nhiên, điểm càng nhanh bị cô lập càng lạ. Số cây là số cây trong rừng.
           Tỉ lệ nhiễm là tỉ lệ điểm lạ mà ta đặt giả định cho dữ liệu huấn luyện, dùng để chọn ngưỡng. Số thực phải thuộc khoảng từ không tới không phẩy năm, và nếu không đặt thì giá trị mặc định là tự động.
           Hàm huấn luyện học từ dữ liệu, hàm dự đoán gắn nhãn một hoặc âm một.
           Hàm tính điểm cho điểm bất thường, càng âm càng lạ. Điểm trừ ngưỡng là điểm quyết định, âm thì nhãn âm một.
           Cuối cùng, ONNX là định dạng tệp mô hình, còn ONNX Runtime là thư viện đọc tệp ấy và chạy mô hình."""),
        st(table(["từ (tên trên màn hình)", "nghĩa"],
                 [["opset, miền (domain)", "opset là số phiên bản của bộ phép toán ONNX; mỗi miền có phiên bản riêng, miền ai.onnx.ml chứa phép toán cây của học máy; bộ chuyển và thư viện chạy phải hiểu cùng phiên bản"],
                  ["InferenceSession, run", "phiên chạy: nạp tệp một lần, rồi gọi run nhiều lần trên dữ liệu số thực 32 bit"]]),
           """Hai từ nữa dùng khi xuất và chạy ONNX. Phiên bản bộ phép toán của ONNX gọi là bản phép toán, mỗi miền có bản riêng, và bộ chuyển với thư viện chạy phải hiểu cùng một bản.
           Phiên chạy nạp tệp một lần rồi gọi chạy nhiều lần trên dữ liệu số thực ba mươi hai bit.""", clear=True),
        st(table(["ký hiệu", "nghĩa"],
                 [["h(x)", "số lần cắt cần để cô lập điểm x trong một cây (độ sâu)"],
                  ["E[h(x)]", "độ sâu trung bình của x trên cả rừng"],
                  ["c(n)", "độ sâu trung bình để cô lập một điểm trong cây n điểm; dùng để chuẩn hoá"],
                  ["s(x, n)", "điểm bất thường 2 mũ của (−E[h(x)] / c(n)); s = 0,5 khi độ sâu bằng c(n); s lớn hơn 0,5 nghĩa là độ sâu nhỏ hơn c(n), càng gần 1 càng lạ"]])
           + "<p class='small'>Thư viện học máy trả về điểm mang dấu âm, tức là âm s: càng âm càng lạ. Điểm thường trong bài này có s = 0,4475.</p>",
           """Bốn ký hiệu của công thức. H của x là số lần cắt cần để cô lập điểm x trong một cây, gọi là độ sâu. E của h là độ sâu trung bình của x trên cả rừng.
           C của n là độ sâu trung bình để cô lập một điểm trong cây n điểm, dùng để chuẩn hoá. S là điểm bất thường, bằng hai mũ của âm E trên c: bằng không phẩy năm khi độ sâu đúng bằng c, và càng gần một thì càng lạ.
           Thư viện học máy trả về điểm mang dấu âm, nên càng âm càng lạ, và điểm thường trong bài này có s bằng không phẩy bốn bốn bảy năm.""", clear=True),
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
           """Hình này cho thấy vì sao điểm lạ nổi lên. Mỗi lần cắt chọn ngẫu nhiên một điểm giữa giá trị nhỏ nhất và lớn nhất của các điểm còn lại.
           Bên trái là một nghìn giao dịch thường dày đặc, bên phải là mười giao dịch lạ ở xa. Giữa hai nhóm là khoảng trống rất rộng, nên lần cắt đầu rơi vào đó với xác suất khoảng chín mươi bốn phần trăm, và khi ấy tách cả nhóm lạ ra.
           Vì vậy điểm lạ cần ít lần cắt hơn nhiều: khoảng năm lần, so với khoảng mười sáu lần cho điểm thường."""),
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
               txt(750, 474, "chưa nói gì về độ trễ khi vận hành thật; dữ liệu mẫu chỉ có MỘT cột (số tiền)", 22, "middle", "#1f2937", True)),
           """Hình thứ hai là đường đi từ huấn luyện tới chấm điểm. Dữ liệu vào rừng cô lập, hàm huấn luyện dựng một trăm cây.
           Bộ chuyển sang ONNX xuất mô hình thành một tệp. Ở môi trường chạy, ONNX Runtime đọc tệp, rồi phiên chạy cho ra nhãn và điểm.
           Dải đỏ ở cuối nhắc bốn điều mô hình chưa làm được. Một, không biết đó có phải gian lận. Hai, tỉ lệ nhiễm là giả định của ta.
           Ba, chưa nói gì về độ trễ khi vận hành thật. Bốn, dữ liệu mẫu chỉ có một cột là số tiền."""),
    ], checks=["round(100 * (48541 - 659) / (51512 - 318)) == 94",
               "round(15.775 * 60) == 946 and round(5.075 * 60) == 304"])

    form = sc("formula", "formula", "Suy ra từng bước: dữ liệu, cắt, điểm, huấn luyện, ngưỡng, xuất ONNX", [
        st(code(DATA_PY, "Bước 1. Sinh dữ liệu với hạt giống cố định"),
           """Bước một, ta sinh dữ liệu bằng thư viện số học, và cố định hạt giống nên chạy lại luôn ra y nguyên. Một nghìn giao dịch thường quanh năm trăm nghìn, độ lệch chuẩn cỡ năm mươi.
           Mười giao dịch lạ quanh năm mươi nghìn nghìn đồng, tức năm mươi triệu, độ lệch chuẩn cỡ hai nghìn. Bốn dòng in ở cuối cho biết hình dạng, trung bình, nhỏ nhất và lớn nhất của từng nhóm.""",
           focus=["2.2", "2.3", "2.4", "2.6"]),
        st(code(DATA_PY, lines=(6, 9)) + out(DATA_OUT),
           """Kết quả chạy thật: một nghìn không trăm mười dòng, một cột. Giao dịch thường nằm từ khoảng ba trăm mười tám tới sáu trăm năm mươi chín.
           Giao dịch lạ nằm từ khoảng bốn mươi tám nghìn tới năm mươi mốt nghìn. Hai nhóm tách xa nhau, nên ta kỳ vọng điểm lạ dễ bị cô lập.""",
           focus=["3.1", "3.3", "3.4", 3], clear=True),
        st(code(CUT_PY, "Bước 2. Tự cắt: đếm số lần cắt để cô lập một điểm")
           + "<p class='small'>Hàm này chỉ để minh hoạ: nếu dãy có các giá trị trùng nhau thì vòng lặp không bao giờ dừng, còn thư viện có độ sâu tối đa.</p>",
           """Bước hai, ta tự viết phép cắt ngẫu nhiên. Hàm nhận một điểm cần cô lập và dãy các điểm còn lại.
           Mỗi vòng, nó chọn một điểm cắt ngẫu nhiên giữa giá trị nhỏ nhất và lớn nhất, rồi giữ lại nửa chứa điểm đang xét.
           Vì mỗi lần cắt loại đi một nửa không chứa điểm, nên đếm số vòng cho tới khi chỉ còn một điểm chính là độ sâu của điểm đó.
           Hàm này chỉ để minh hoạ, vì nếu dãy có các giá trị trùng nhau thì vòng lặp không bao giờ dừng, còn thư viện có độ sâu tối đa.""",
           clear=True),
        st(code(CUT_RUN) + out(CUT_OUT, "Làm thử — kết quả chạy thật"),
           """Làm thử, ta cô lập hai điểm, mỗi điểm hai trăm lần, vì một lần chạy ngẫu nhiên chưa đủ tin. Điểm thứ nhất là một giao dịch thường, khoảng năm trăm mười lăm nghìn.
           Điểm thứ hai là một giao dịch lạ, khoảng bốn mươi chín nghìn tám trăm tám mươi mốt. Kết quả chạy thật: điểm thường cần trung bình mười lăm phẩy tám lần cắt, điểm lạ chỉ năm phẩy không bảy lần.""",
           clear=True),
        st("""<p><b>Bước 3.</b> Độ sâu trung bình c(n) và điểm bất thường. Vì cây có thể sâu hay nông tuỳ số điểm, ta chia độ sâu cho một mức tham chiếu để điểm không phụ thuộc cỡ mẫu:</p>
$$c(n) = 2\\,(\\ln(n-1) + \\gamma) - \\frac{2\\,(n-1)}{n}, \\qquad s(x,n) = 2^{-E[h(x)]\\,/\\,c(n)}$$
<span class='note'>γ ≈ 0,5772 là hằng số Euler–Mascheroni. Mỗi cây của thư viện huấn luyện trên tối đa 256 điểm, nên mức tham chiếu là c(256).</span>""",
           """Bước ba là độ sâu trung bình và điểm bất thường. Vì cây có thể sâu hay nông tuỳ số điểm, ta chia độ sâu cho một mức tham chiếu, để điểm không phụ thuộc cỡ mẫu.
           Mức tham chiếu c của n bằng hai lần tổng của lốc tự nhiên n trừ một và một hằng số cỡ không phẩy năm bảy bảy, trừ đi hai nhân n trừ một chia n.
           Điểm s bằng hai mũ âm độ sâu trung bình chia c. Mỗi cây của thư viện huấn luyện trên tối đa hai trăm năm mươi sáu điểm, nên mức tham chiếu là c của hai trăm năm mươi sáu.""",
           clear=True, introduces=["gamma", "log"]),
        st(code(AVG_PY, "Bước 3 (tiếp). Viết lại bằng Python"),
           """Ta viết lại hai công thức thành hai hàm Python. Hàm c cho mức tham chiếu theo số điểm n.
           Hàm điểm nhận độ sâu trung bình, và đặt dấu âm như thư viện học máy.""",
           focus=[2, "2.3", "2.5"], clear=True),
        st(code(AVG_PY, lines=(6, 9)) + out(AVG_OUT),
           """Kết quả chạy thật: c của hai trăm năm mươi sáu bằng mười phẩy hai bốn bốn tám. Điểm có độ sâu bằng đúng mức tham chiếu là âm không phẩy năm, vì hai mũ âm một là một phần hai.
           Độ sâu bằng một nửa mức tham chiếu cho âm không phẩy bảy không bảy một. Độ sâu chỉ bằng một lần cắt cho âm không phẩy chín ba bốn sáu.
           Độ sâu càng nhỏ thì điểm càng gần âm một, tức càng lạ.""",
           focus=["3.1", "3.2", "3.3", "3.4", 3], clear=True),
        st(code(TRAIN_PY, "Bước 4. Huấn luyện rừng cô lập: 100 cây, tỉ lệ nhiễm 1%"),
           """Bước bốn, ta huấn luyện rừng cô lập bằng thư viện học máy, với một trăm cây và tỉ lệ nhiễm một phần trăm. Hạt giống cố định nên chạy lại luôn ra y nguyên.
           Hàm huấn luyện học từ dữ liệu, rồi hàm dự đoán gắn nhãn cho chính dữ liệu huấn luyện.""",
           focus=["2.2", "2.3", "2.5"], clear=True),
        st(code(TRAIN_PY, lines=(6, 9)) + out(TRAIN_OUT),
           """Kết quả chạy thật: cả mười điểm lạ đều nhận nhãn âm một. Nhưng tổng số nhãn âm một là mười một, nghĩa là có một giao dịch thường bị gắn lạ.
           Ngưỡng bằng âm không phẩy bảy ba năm ba.""",
           focus=["3.1", "3.2", "3.4"], clear=True),
        st(f"""<p><b>Bước 5.</b> Vì sao ra đúng ngưỡng ấy. Tỉ lệ nhiễm 1% nghĩa là: lấy điểm của chính dữ liệu huấn luyện, đặt ngưỡng ở phân vị 1% thấp nhất. Điểm nào thấp hơn ngưỡng nhận nhãn -1:</p>
$$\\text{{quyết định}} = \\text{{điểm}} - \\text{{offset\\_}}, \\qquad \\text{{quyết định}} < 0 \\;\\Rightarrow\\; \\text{{nhãn}} = \\hl{{-1}}$$
<span class='note'>Theo quy tắc đếm: 0,01 × 1009 = 10,09, phần nguyên 10, cộng một là 11 điểm nằm dưới ngưỡng, dù thật sự lạ chỉ có 10: ngưỡng do ta đặt, không do mô hình tìm ra.</span>""",
           """Bước năm là vì sao ra đúng ngưỡng ấy. Tỉ lệ nhiễm một phần trăm nghĩa là ta lấy điểm của chính dữ liệu huấn luyện, rồi đặt ngưỡng ở phân vị một phần trăm thấp nhất.
           Điểm quyết định bằng điểm trừ ngưỡng. Điểm quyết định âm thì nhãn là âm một.
           Theo quy tắc đếm, không phẩy không một nhân một nghìn không trăm lẻ chín bằng mười phẩy không chín.
           Phần nguyên mười, cộng một là mười một điểm nằm dưới ngưỡng, dù thật sự lạ chỉ có mười. Ngưỡng do ta đặt, không do mô hình tự tìm ra.""",
           clear=True),
        st(code(SCORE_PY, "Bước 5 (tiếp). Điểm trung bình của hai nhóm, quy ra độ sâu") + out(SCORE_OUT),
           """Ta lấy điểm bất thường của từng giao dịch, tính trung bình cho hai nhóm, rồi quy về độ sâu vì độ sâu dễ hình dung hơn. Kết quả chạy thật: nhóm thường có điểm trung bình âm không phẩy bốn bốn bảy năm, quy ra độ sâu khoảng mười một phẩy tám tám.
           Nhóm lạ có điểm âm không phẩy tám bốn bốn tám, quy ra độ sâu chỉ hai phẩy bốn chín. Điểm của nhóm lạ nằm dưới ngưỡng, điểm của nhóm thường nằm trên ngưỡng.""",
           focus=["2.1", "4.1", "4.2", 4], clear=True),
        st(code(ONNX_PY, "Bước 6. Xuất sang ONNX, chạy bằng ONNX Runtime, so với mô hình trong Python")
           + "<p class='small'>Đầu ra thứ hai của tệp ONNX là điểm quyết định (điểm trừ ngưỡng), nên ta so nó với decision_function.</p>",
           """Bước sáu, ta xuất mô hình sang ONNX bằng bộ chuyển, ghi ra một tệp, rồi nạp tệp vào ONNX Runtime.
           Dữ liệu đưa vào là số thực ba mươi hai bit, vì mô hình ONNX này nhận kiểu đó. Rồi ta chạy mô hình trên cả một nghìn không trăm mười điểm, và nhận hai đầu ra: nhãn, và điểm quyết định tức điểm trừ ngưỡng.""",
           focus=["2.4", "2.3", "3"], clear=True),
        st(code(ONNX_PY, lines=(10, 12)) + out(ONNX_OUT),
           """Ta so kết quả với mô hình trong Python. Kết quả chạy thật: cả một nghìn không trăm mười nhãn đều giống nhau.
           Điểm quyết định sai khác nhau nhiều nhất chỉ cỡ một phẩy tám nhân mười mũ âm bảy, vì số thực ba mươi hai bit làm tròn thô hơn số thực sáu mươi bốn bit.
           Nên trên dữ liệu khác, điểm sát ngưỡng vẫn có thể bị lật nhãn.""",
           focus=["1.1", "3.1", "3.2", "3.2"], clear=True),
    ], checks=["round(alg.bnx_l23_c(256), 4) == 10.2448",
               "round(alg.bnx_l23_score(alg.bnx_l23_c(256) / 2, 256), 4) == -0.7071",
               "round(alg.bnx_l23_score(1, 256), 4) == -0.9346 and alg.bnx_l23_score(alg.bnx_l23_c(256), 256) == -0.5",
               "alg.bnx_l23_label(-0.8448, -0.7353) == -1 and alg.bnx_l23_label(-0.4475, -0.7353) == 1",
               "alg.bnx_l23_expected_flags(1010, 0.01) == 11 and 11 - 10 == 1",
               "round(alg.bnx_l23_depth_from_score(-0.8448, 256), 2) == 2.49 and round(alg.bnx_l23_depth_from_score(-0.4475, 256), 2) == 11.88"])

    ex = sc("example", "example", "Ví dụ rừng cô lập trên 1010 giao dịch, từng phép tính", [
        st(f"""<p>1000 giao dịch thường quanh 500 nghìn đồng, 10 giao dịch lạ 50 triệu đồng; rừng 100 cây, tỉ lệ nhiễm 1%; mỗi cây huấn luyện trên tối đa 256 điểm. {NOTE_ILL}</p>
$$① \\; c(256) = 2\\,(\\ln 255 + 0{{,}}57722) - \\frac{{2 \\cdot 255}}{{256}} = 12{{,}}2370 - 1{{,}}9922 = \\hl{{10{{,}}2448}}$$""",
           """Ta làm trọn một ví dụ. Một nghìn giao dịch thường quanh năm trăm nghìn đồng, mười giao dịch lạ năm mươi triệu đồng, rừng một trăm cây, tỉ lệ nhiễm một phần trăm.
           Mỗi cây huấn luyện trên tối đa hai trăm năm mươi sáu điểm. Phép tính thứ nhất, mức tham chiếu c của hai trăm năm mươi sáu bằng mười hai phẩy hai ba bảy không trừ một phẩy chín chín hai hai, bằng mười phẩy hai bốn bốn tám."""),
        st("""<p>Dùng lại c(256) = 10,2448 ở phép ①. Nhóm lạ có điểm trung bình −0,8448.</p>
$$② \\; \\text{độ sâu} = -c \\cdot \\log_2(0{,}8448) = 10{,}2448 \\cdot 0{,}2433 = \\hl{2{,}49} \\text{ lần cắt}$$""",
           """Phép tính thứ hai dùng lại mười phẩy hai bốn bốn tám. Nhóm lạ có điểm trung bình âm không phẩy tám bốn bốn tám.
           Độ sâu quy đổi bằng âm c nhân lốc hai của không phẩy tám bốn bốn tám. Đó là mười phẩy hai bốn bốn tám nhân không phẩy hai bốn ba ba, khoảng hai phẩy bốn chín lần cắt.""", introduces=["sub"]),
        st("""<p>Nhóm thường có điểm trung bình −0,4475.</p>
$$③ \\; \\text{độ sâu} = -10{,}2448 \\cdot \\log_2(0{,}4475) = 10{,}2448 \\cdot 1{,}1600 = \\hl{11{,}88} \\text{ lần cắt}$$""",
           """Phép tính thứ ba, cho nhóm thường có điểm trung bình âm không phẩy bốn bốn bảy năm. Cũng dùng mười phẩy hai bốn bốn tám, độ sâu bằng mười phẩy hai bốn bốn tám nhân một phẩy một sáu không không, khoảng mười một phẩy tám tám lần cắt.
           Điểm thường cần nhiều lần cắt hơn điểm lạ khoảng bốn phẩy tám lần."""),
        st("""<p>Ngưỡng của rừng: offset_ = −0,7353 (phân vị 1%). Dùng điểm ở ② và ③.</p>
$$④ \\; \\text{lạ: } -0{,}8448 + 0{,}7353 = \\hl{-0{,}1095} < 0 \\Rightarrow -1;\\quad \\text{thường: } -0{,}4475 + 0{,}7353 = \\hlg{+0{,}2878} \\Rightarrow 1$$
<span class='note'>Toàn tập: 11 điểm dưới ngưỡng = 10 điểm lạ + 1 điểm thường bị gắn oan.</span>""",
           """Phép tính thứ tư, đặt ngưỡng. Ngưỡng của rừng là âm không phẩy bảy ba năm ba, ở phân vị một phần trăm. Với điểm ở phép hai và phép ba, nhóm lạ có điểm quyết định âm không phẩy một không chín năm, nhỏ hơn không nên nhãn âm một.
           Nhóm thường có điểm quyết định dương không phẩy hai tám bảy tám nên nhãn một. Trên toàn tập có mười một điểm dưới ngưỡng, gồm mười điểm lạ và một điểm thường bị gắn oan.""",
           clear=True),
        st("""<p>Xuất ONNX, chạy trên cả 1010 điểm.</p>
$$⑤ \\; \\text{cùng nhãn với mô hình Python: } \\hlg{1010 / 1010}; \\quad \\text{sai khác điểm lớn nhất} = \\hl{1{,}8 \\cdot 10^{-7}}$$""",
           """Phép tính thứ năm, xuất mô hình sang ONNX và chạy trên cả một nghìn không trăm mười điểm. Kết quả chạy thật: một nghìn không trăm mười trên một nghìn không trăm mười nhãn giống mô hình trong Python.
           Điểm quyết định sai khác nhau nhiều nhất chỉ cỡ một phẩy tám nhân mười mũ âm bảy."""),
    ], checks=["round(2 * (__import__('math').log(255) + 0.57722) - 2 * 255 / 256, 4) == 10.2448",
               "round(alg.bnx_l23_depth_from_score(-0.8448, 256), 2) == 2.49",
               "round(alg.bnx_l23_depth_from_score(-0.4475, 256), 2) == 11.88 and round(11.88 / 2.49, 1) == 4.8",
               "round(alg.bnx_l23_decision(-0.8448, -0.7353), 4) == -0.1095 and round(alg.bnx_l23_decision(-0.4475, -0.7353), 4) == 0.2878",
               "alg.bnx_l23_expected_flags(1010, 0.01) == 10 + 1"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: danh tính điểm, năm hạt giống và tay cắt", [
        st(code(CHECK_ID_PY, "Kiểm 1. decision_function đúng bằng score_samples trừ offset_") + out(CHECK_ID_OUT),
           """Kiểm bằng đường khác. Thư viện định nghĩa điểm quyết định bằng điểm bất thường trừ ngưỡng. Vì vậy ta tính hai vế riêng rồi so.
           Kết quả chạy thật: hai vế sai khác nhau không, và điểm quyết định âm trùng khít với nhãn âm một trên mọi điểm.""",
           focus=[1, "2.2", "2.3", "4.1"]),
        st(code(CHECK_SEED_PY, "Kiểm 2. Đổi hạt giống: kết quả có đổi không?") + out(CHECK_SEED_OUT),
           """Kiểm hai, ta đổi hạt giống năm lần, từ không tới bốn. Mỗi dòng in hạt giống, số điểm lạ thật bị gắn âm một, và tổng số gắn âm một.
           Kết quả chạy thật: năm lần đều bắt đủ mười điểm lạ và gắn tổng cộng mười một điểm. Vì dữ liệu tách xa như thế này, kết quả không phụ thuộc vào một hạt giống may mắn; dữ liệu khó hơn thì chưa chắc.""",
           focus=[1, "2.5", "4.1", 4], clear=True),
        st(table(["cách kiểm", "phép tính", "kết luận"],
                 [["độ sâu: tay và máy", "tự cắt: 5,1 lần (lạ) so với 15,8 lần (thường); thư viện: 2,49 và 11,88 sau khi quy đổi", "cùng thứ tự: lạ nông hơn thường; số khác nhau vì thư viện dùng mẫu con tối đa 256 điểm, dừng ở độ sâu 8 rồi cộng c của số điểm còn ở lá"],
                  ["ngưỡng theo phân vị", "phần nguyên của 0,01 × 1009 = 10,09 là 10, cộng một: 11 điểm dưới ngưỡng", "khớp 11 điểm gắn -1"],
                  ["sai khác điểm ONNX", "1,8 × 10⁻⁷ so với khoảng cách điểm sát ngưỡng nhất tới ngưỡng, cỡ 3 × 10⁻⁴", "bé hơn hơn một nghìn lần: không lật nhãn nào (chỉ trên 1010 điểm này)"],
                  ["tệp chạy một mình", "nạp tệp ONNX trong một tiến trình mới đã chặn nhập thư viện học máy (mã không hiện ở đây; bộ kiểm ghi ở audit/bnx/ver/l23.py)", "chạy được: tệp chứa cây và ngưỡng"]]),
           """Bảng này kiểm thêm bằng bốn đường. Về độ sâu, tay cắt cho năm lần so với mười sáu lần, thư viện quy đổi ra hai phẩy bốn chín và mười một phẩy tám tám, cùng thứ tự: điểm lạ nông hơn.
           Số tuyệt đối khác vì thư viện chỉ dùng mẫu con hai trăm năm mươi sáu điểm, dừng ở độ sâu tám, rồi cộng mức tham chiếu của số điểm còn lại ở lá.
           Về ngưỡng, phần nguyên của mười phẩy không chín là mười, cộng một thành mười một điểm dưới ngưỡng, khớp với mười một nhãn âm một.
           Về điểm sai khác, một phẩy tám nhân mười mũ âm bảy bé hơn khoảng cách từ điểm sát ngưỡng nhất tới ngưỡng, cỡ ba nhân mười mũ âm bốn.
           Nên trên một nghìn không trăm mười điểm này không nhãn nào bị lật.
           Cuối cùng, trong một tiến trình mới đã chặn thư viện học máy, tệp ONNX vẫn chạy, vì tệp đã chứa cây và ngưỡng.""",
           focus=[0, "1.2", "1.2", "1.3", "1.4", "1.4", "1.5"], clear=True),
        st(table(["cách đánh giá khi KHÔNG có nhãn thật", "làm gì"],
                 [["lưu ý trước", "mười trên mười điểm lạ chỉ nói được vì ta tự dựng dữ liệu nên biết đáp án; dữ liệu thật không có đáp án"],
                  ["người xét duyệt mẫu", "lấy các điểm bị gắn -1 (nhất là điểm thấp nhất), cho người xét đánh dấu đúng hay sai, rồi tính tỉ lệ đúng"],
                  ["tiêm điểm lạ giả", "thêm vài giao dịch lạ do ta tự tạo vào dữ liệu thử, xem rừng có bắt không"],
                  ["theo dõi theo thời gian", "so phân bố điểm và tỉ lệ nhãn -1 hôm nay với lúc huấn luyện"]])
           + "<span class='note'>Đây là các cách thường dùng, không phải kết quả đo của bài.</span>",
           """Còn khi không có nhãn thật thì sao. Mười trên mười điểm lạ chỉ nói được vì ta tự dựng dữ liệu nên biết đáp án, còn dữ liệu thật không có đáp án.
           Cách thứ nhất là cho người xét duyệt mẫu các điểm bị gắn âm một, rồi tính tỉ lệ đúng. Cách thứ hai là tiêm vài giao dịch lạ do ta tự tạo, xem rừng có bắt không.
           Cách thứ ba là theo dõi phân bố điểm và tỉ lệ nhãn âm một theo thời gian. Đây là các cách thường dùng, không phải kết quả đo của bài.""",
           clear=True),
    ], checks=["alg.bnx_l23_expected_flags(1010, 0.01) == 11 and int(0.01 * (1010 - 1)) + 1 == 11",
               "round(alg.bnx_l23_depth_from_score(-0.8448, 256), 2) < round(alg.bnx_l23_depth_from_score(-0.4475, 256), 2)",
               "round(3e-4 / 1.8e-7) > 1000"])

    pit = sc("pitfalls", "pitfall", "Điều mô hình KHÔNG làm được, và lỗi theo từng giai đoạn", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Tin rằng nhãn -1 là “gian lận”, và tỉ lệ nhiễm là điều mô hình tự tìm ra. Đổi tỉ lệ nhiễm, số điểm bị gắn đổi theo, còn lạ thật vẫn là 10: đặt thấp thì bỏ sót, đặt cao thì gắn oan.</div>""" + code(LIMIT_PY) + out(LIMIT_OUT),
           """Lỗi thứ nhất, của người mới, là tin rằng nhãn âm một nghĩa là gian lận, và tỉ lệ nhiễm là điều mô hình tự tìm ra. Ta thử ba tỉ lệ nhiễm, và thêm giá trị mặc định là tự động.
           Kết quả chạy thật: với không phẩy không không một, rừng chỉ gắn hai điểm, tức bỏ sót tám điểm lạ. Với một phần trăm gắn mười một điểm. Với năm phần trăm gắn năm mươi mốt điểm, trong đó vẫn chỉ mười điểm lạ thật.
           Nếu không đặt gì, ngưỡng cố định ở âm không phẩy năm và rừng gắn một trăm ba mươi bảy điểm.
           Vậy số điểm bị gắn do ta đặt, không do dữ liệu tự nói: đặt thấp thì bỏ sót, đặt cao thì gắn oan.""",
           focus=[1, "2.1", "4.1", "4.2", "4.3", "4.4", 4]),
        st(code(LIMIT2_PY, "Hai điểm mô hình trả lời sai điều ta cần") + out(LIMIT2_OUT)
           + "<div class='box key'>Số tiền 520 nghìn trông như người thường nên nhãn 1: <b>kẻ gian tiêu nhỏ không bị thấy</b>. Số tiền 50 triệu lạ nên nhãn -1 (vì rừng đã thấy nhóm này hiếm): <b>lương hợp lệ vẫn bị gắn</b>. Lạ không đồng nghĩa gian lận: cần người xét lại.</div>",
           """Ta thử thêm hai điểm. Một kẻ gian chuyển số tiền năm trăm hai mươi nghìn, trông như người thường, nên nhãn là một: mô hình không thấy kẻ gian tiêu nhỏ.
           Một công ty trả lương hợp lệ năm mươi triệu, nên nhãn là âm một, dù không có gì sai, vì rừng đã thấy nhóm năm mươi triệu là hiếm. Lạ không đồng nghĩa với gian lận, nên mọi nhãn âm một cần người xét lại.""",
           focus=[1, "2.1", "4.1", 5], clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Xuất ONNX mà không khai phiên bản miền <code>ai.onnx.ml</code>, hoặc xuất xong chỉ thử vài điểm mẫu rồi cho chạy. Thư viện xuất của máy này dừng ngay với một lỗi:</div>"""
           + code(ONNX_ERR_PY) + out(ONNX_ERR_OUT, "Thông báo lỗi thật (dòng cuối của vết lỗi, lược bớt)")
           + """<p class="small">Cách chữa: khai target_opset như bước 6 (ở đây ai.onnx.ml bản 3), ghi lại bản của ba thư viện lúc xuất (học máy, bộ chuyển, ONNX Runtime), rồi so nhãn VÀ điểm trên TOÀN BỘ dữ liệu, nhất là các điểm sát ngưỡng, không chỉ vài mẫu.</p>""",
           """Lỗi thứ hai, của người đã đi làm, gặp lúc mới dựng. Xuất ONNX mà không khai phiên bản của miền học máy, hoặc xuất xong chỉ thử vài điểm mẫu rồi cho chạy.
           Trên máy này, thư viện xuất dừng ngay với một lỗi, nói mô hình dùng bản bốn của miền học máy trong ONNX, mà thư viện chưa hỗ trợ.
           Cách chữa là khai phiên bản đích như bước sáu, ghi lại bản của ba thư viện lúc xuất, rồi so cả nhãn lẫn điểm trên toàn bộ dữ liệu, nhất là các điểm sát ngưỡng.""",
           focus=[1, "2.1", "4.1", 5], clear=True),
        st(code(DRIFT_PY, "Lỗi 3 (vận hành lâu dài): tháng sau mức chi tiêu thường đổi") + out(DRIFT_OUT)
           + """<p class="small">Vì sao: mức 1500 nghìn nằm trong khoảng trống giữa hai nhóm cũ, nên bị cô lập rất nhanh.</p>
<p class="small">Cách chữa: theo dõi tỉ lệ nhãn -1 và phân bố điểm mỗi ngày, so với lúc huấn luyện (tỉ lệ 1% chỉ đáng so khi dữ liệu giống lúc huấn luyện, vì 1% vốn là giả định); huấn luyện lại theo lịch.</p>""",
           """Lỗi thứ ba lộ ra khi vận hành lâu dài, là trôi dữ liệu. Một tháng sau, mức chi tiêu thường tăng lên quanh một triệu rưỡi, nhưng mô hình vẫn là bản huấn luyện cũ.
           Kết quả chạy thật: chín trăm bảy mươi bảy trên một nghìn giao dịch thường bị gắn âm một, nên hộp thư người xét ngập.
           Mức một triệu rưỡi nằm trong khoảng trống giữa hai nhóm cũ, nên bị cô lập rất nhanh.
           Cách chữa là theo dõi tỉ lệ nhãn âm một và phân bố điểm mỗi ngày, so với lúc huấn luyện, và huấn luyện lại theo lịch. Tỉ lệ một phần trăm chỉ đáng so khi dữ liệu giống lúc huấn luyện, vì một phần trăm vốn là giả định.""",
           focus=[1, "2.2", "4.1", 5, 6, 6], clear=True),
        st("""<div class="box warn"><b>Lỗi 4 (lúc tải tăng).</b> Nạp lại tệp ONNX cho từng yêu cầu, hoặc tin vì “chạy ngon trên máy cá nhân”: số đo trên máy cá nhân chưa nói gì về <b>độ trễ</b> khi vận hành thật.</div>
<p class="small">Cách đo: nạp tệp một lần lúc khởi động; bỏ vài lần chạy đầu; rồi đo nhiều lần với dữ liệu và số luồng như vận hành; báo phân vị 50, 95, 99 chứ không chỉ trung bình. Số đo chỉ đúng cho máy đã đo.</p>""",
           """Lỗi thứ tư gặp lúc tải tăng: nạp lại tệp cho từng yêu cầu, hoặc tin vì chạy ngon trên máy cá nhân. Tạo phiên chạy thường tốn kém, nên cần nạp tệp một lần lúc khởi động.
           Số đo trên máy cá nhân chưa nói gì về độ trễ khi vận hành thật, vì tải, số luồng và máy đều khác.
           Cách đo là bỏ vài lần chạy đầu, rồi đo nhiều lần với dữ liệu giống thật. Hãy báo phân vị năm mươi, chín mươi lăm và chín mươi chín chứ không chỉ trung bình, và nhớ rằng số đo chỉ đúng cho máy đã đo.""",
           focus=[1, 1, 1, 2, 2], clear=True),
    ], checks=["alg.bnx_l23_expected_flags(1010, 0.001) == 2 and alg.bnx_l23_expected_flags(1010, 0.01) == 11 and alg.bnx_l23_expected_flags(1010, 0.05) == 51",
               "alg.bnx_l23_expected_flags(1010, 0.05) - 10 == 41",
               "alg.bnx_l23_expected_flags(1010, 0.05) == int(0.05 * (1010 - 1)) + 1 and 10 - 2 == 8",
               "977 + 23 == 1000"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề (dùng c(256) = 10,2448 và offset_ = −0,7353 của bài)"],
                 [["1", "Một điểm có độ sâu trung bình bằng một nửa c(256). Điểm bất thường (dấu âm kiểu thư viện) là bao nhiêu? Điểm quyết định là bao nhiêu, nhãn là gì?"],
                  ["2", "Đặt tỉ lệ nhiễm 2% cho 1010 điểm. Theo quy tắc đếm ở phần phân vị, bao nhiêu điểm bị gắn -1? Nếu thật sự lạ chỉ có 10, bao nhiêu điểm thường bị gắn oan?"],
                  ["3", "Quyết định: giao dịch bị gắn -1. Chặn tự động hay chuyển người xét? Cho biết được và mất."]]),
           """Đến lượt bạn. Câu một, một điểm có độ sâu trung bình bằng một nửa mức tham chiếu c của hai trăm năm mươi sáu. Điểm bất thường là bao nhiêu, điểm quyết định là bao nhiêu, nhãn là gì?
           Câu hai, đặt tỉ lệ nhiễm hai phần trăm cho một nghìn không trăm mười điểm. Theo quy tắc đếm ở phần phân vị, bao nhiêu điểm bị gắn âm một, và nếu thật sự lạ chỉ có mười thì bao nhiêu điểm thường bị gắn oan?
           Câu ba, giao dịch bị gắn âm một: chặn tự động hay chuyển người xét? Hãy nêu cái được và cái mất. Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""$$2^{-1/2} \\approx 0{,}7071 \\;\\Rightarrow\\; \\text{điểm} = -0{,}7071;\\quad -0{,}7071 + 0{,}7353 = \\hl{+0{,}0282} \\geq 0 \\;\\Rightarrow\\; \\text{nhãn } \\hlg{1}$$""",
           """Đáp án câu một. Độ sâu bằng một nửa mức tham chiếu thì số mũ là âm một phần hai. Hai mũ âm một phần hai xấp xỉ không phẩy bảy không bảy một, nên điểm là âm không phẩy bảy không bảy một.
           Điểm quyết định bằng âm không phẩy bảy không bảy một cộng không phẩy bảy ba năm ba, bằng dương không phẩy không hai tám hai. Không âm nên nhãn là một, vừa đủ nằm trong vùng thường."""),
        st("""$$0{,}02 \\cdot (1010 - 1) = 20{,}18 \\;\\Rightarrow\\; 20 + 1 = \\hl{21} \\text{ điểm bị gắn};\\quad 21 - 10 = \\hlg{11} \\text{ điểm thường bị gắn oan}$$""",
           """Đáp án câu hai. Ngưỡng là phân vị hai phần trăm, vị trí hai mươi phẩy mười tám trong dãy đã sắp, phần nguyên là hai mươi, cộng một nên có hai mươi mốt điểm nằm dưới ngưỡng. Kết quả chạy thật cũng cho hai mươi mốt.
           Nếu thật sự lạ chỉ có mười thì mười một điểm thường bị gắn oan."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["chuyển người xét", "giao dịch hợp lệ lớn, như lương 50 triệu, không bị chặn oan; kẻ gian vẫn bị giữ lại để xem", "chậm hơn, tốn công; tỉ lệ nhiễm cao thì hộp thư ngập"],
                  ["giữ lại và yêu cầu xác thực thêm", "đỡ chặn oan, người xét chỉ nhận ca còn nghi", "thêm một bước cho khách; cần có kênh xác thực"],
                  ["chặn tự động mọi nhãn -1", "nhanh, không tốn người", "chặn oan khách thật; không sửa được sai sót của giả định tỉ lệ nhiễm"]]),
           """Đáp án câu ba. Nhãn âm một chỉ nói giao dịch lạ, không nói gian lận, nên chuyển người xét.
           Chuyển người xét thì không chặn oan giao dịch hợp lệ lớn như lương năm mươi triệu, mà vẫn giữ lại giao dịch đáng ngờ để xem. Đổi lại chậm hơn, tốn công, và nếu tỉ lệ nhiễm đặt cao thì hộp thư ngập.
           Còn có mức giữa là giữ lại và yêu cầu xác thực thêm, đỡ chặn oan mà người xét chỉ nhận ca còn nghi, đổi lại khách phải qua thêm một bước.
           Chặn tự động thì nhanh, nhưng chặn oan khách thật, và không có ai sửa sai cho giả định về tỉ lệ nhiễm."""),
    ], checks=["round(alg.bnx_l23_score(alg.bnx_l23_c(256) / 2, 256), 4) == -0.7071",
               "round(alg.bnx_l23_decision(-0.7071, -0.7353), 4) == 0.0282 and alg.bnx_l23_label(-0.7071, -0.7353) == 1",
               "alg.bnx_l23_expected_flags(1010, 0.02) == 21 and int(0.02 * (1010 - 1)) + 1 == 21 and 21 - 10 == 11"])

    rec = sc("recap", "recap", "Chuỗi logic, góc phỏng vấn & tư duy cần mang theo", [
        st(chain("điểm lạ bị cô lập sau ít lần cắt", "điểm = 2 mũ âm độ sâu / c(n)", "tỉ lệ nhiễm → ngưỡng → nhãn 1 / -1", "xuất ONNX, chạy ONNX Runtime", "so nhãn và điểm trên toàn tập", "lạ ≠ gian lận: người xét"),
           """Tổng kết chuỗi logic. Điểm lạ bị cô lập sau ít lần cắt. Điểm bất thường là hai mũ âm độ sâu chia mức tham chiếu.
           Tỉ lệ nhiễm cho ra ngưỡng, ngưỡng cho ra nhãn một hoặc âm một. Mô hình được xuất sang ONNX và chạy bằng ONNX Runtime, rồi ta so nhãn và điểm trên toàn tập.
           Cuối cùng, lạ không có nghĩa là gian lận, nên cần người xét.""",
           focus=[0, "1.1", "1.3", "1.5", "1.7", "1.9"]),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời một dòng"],
                 [["Isolation Forest hoạt động thế nào?", "cắt ngẫu nhiên nhiều lần; điểm lạ bị cô lập sau ít lần cắt hơn nên có độ sâu trung bình nhỏ, điểm gần âm 1"],
                  ["Tỉ lệ nhiễm (contamination) là gì, ai quyết định nhãn -1?", "giả định của người đặt, dùng chọn ngưỡng theo phân vị; mặc định 'auto' thì ngưỡng cố định −0,5"],
                  ["Vì sao xuất ONNX, và kiểm gì sau khi xuất?", "tệp ONNX chạy không cần mã Python; tệp đóng gói của thư viện học máy không nạp được qua bản khác; ghi lại bản thư viện, so nhãn và điểm trên toàn tập"]]),
           """Đây là năm câu người phỏng vấn hay hỏi về dòng này trên hồ sơ xin việc, và ta xem ba câu đầu. Hỏi Isolation Forest hoạt động thế nào, thì trả lời cắt ngẫu nhiên nhiều lần, điểm lạ bị cô lập sau ít lần cắt hơn nên điểm gần âm một.
           Hỏi tỉ lệ nhiễm là gì và ai quyết định nhãn âm một, thì trả lời đó là giả định của người đặt, dùng để chọn ngưỡng theo phân vị.
           Nếu để mặc định thì ngưỡng cố định ở âm không phẩy năm.
           Hỏi vì sao xuất ONNX và kiểm gì, thì trả lời tệp ONNX chạy không cần mã Python lẫn thư viện học máy.
           Tệp đóng gói của thư viện học máy không hỗ trợ nạp qua bản khác, nên ghi lại bản các thư viện và so nhãn lẫn điểm trên toàn tập.""",
           focus=[0, "1.2", "1.3", "1.3", "1.4", "1.4"], clear=True),
        st(table(["Nếu bị hỏi về dòng này trên CV (tiếp)", "ý trả lời một dòng"],
                 [["Không có nhãn thật thì đánh giá và theo dõi ra sao?", "bài biết đáp án vì tự dựng dữ liệu; thật thì cho người xét duyệt mẫu, tiêm điểm lạ giả, theo dõi phân bố điểm và tỉ lệ nhãn -1 theo thời gian"],
                  ["Đo độ trễ thế nào, và gọi mô hình từ Java được không?", "nạp tệp một lần, bỏ vài lần đầu, đo nhiều lần, báo phân vị 95 và 99; số đo chỉ đúng cho máy đã đo; ONNX Runtime có thư viện Java, bài này chưa chạy thử mã Java"]])
           + "<span class='note'>Trả lời bằng cơ chế; không nêu số liệu của tổ chức thật, không nói đã làm ở quy mô nào.</span>",
           """Hai câu còn lại nói về đánh giá và vận hành. Hỏi khi không có nhãn thật thì đánh giá ra sao, thì trả lời bài biết đáp án vì tự dựng dữ liệu.
           Còn thật thì cho người xét duyệt mẫu, tiêm điểm lạ giả và theo dõi phân bố điểm theo thời gian.
           Hỏi đo độ trễ thế nào, thì trả lời nạp tệp một lần, đo nhiều lần, báo phân vị chín mươi lăm và chín mươi chín, và nhớ số đo chỉ đúng cho máy đã đo.
           Hỏi gọi từ Java được không, thì trả lời ONNX Runtime có thư viện cho Java, nhưng bài này chưa chạy thử mã Java.
           Hãy trả lời bằng cơ chế, không nêu số liệu của tổ chức thật.""",
           focus=[0, "1.2", "1.2", "1.3", "1.3", 2], clear=True),
        st("""<div class='box key'><b>Tư duy:</b> với mỗi mô hình phát hiện bất thường, hỏi ba điều: con số nào là <b>giả định của ta</b> (tỉ lệ nhiễm), kết quả nào cần <b>người xét lại</b> (lạ chưa phải gian lận), và vận hành thật <b>đã được đo</b> chưa (độ trễ, trôi dữ liệu).</div>""",
           """Điều cần mang theo. Với mỗi mô hình phát hiện bất thường, hãy hỏi ba điều: con số nào là giả định của ta, kết quả nào cần người xét lại, và vận hành thật đã được đo chưa.""",
           clear=True),
    ], checks=["alg.bnx_l23_label(alg.bnx_l23_score(alg.bnx_l23_c(256) / 2, 256), -0.7353) == 1",
               "alg.bnx_l23_expected_flags(1010, 0.01) == 11"])
    return lesson("L23", "scikit_learn_onnx_rung_co_lap",
                  "Bài 23 — Từ scikit-learn tới ONNX Runtime: rừng cô lập cho phát hiện bất thường",
                  "curriculum/bnx.yaml L23; audit/bnx/verify_bnx.py L23; audit/bnx/sources_l23.md [SKIF] scikit-learn 1.9.1 IsolationForest "
                  "(tài liệu và mã nguồn, đọc 2026-11-12), [SKOD] hướng dẫn phát hiện ngoại lai scikit-learn, [ORTP] ONNX Runtime Python, "
                  "[S2O] sklearn-onnx 1.20.0, [SKPERS] lưu và nạp mô hình scikit-learn, [ORTJ] ONNX Runtime với Java, [ORTAPI] ONNX Runtime Python (khai nhà cung cấp thực thi); chạy thật bằng scikit-learn 1.9.1, skl2onnx 1.20.0, onnxruntime 1.31.1, numpy 2.5.4 "
                  "(audit/bnx/deps/l23/README.md); dữ liệu sinh với hạt giống cố định; mọi số liệu là số minh hoạ",
                  ["Giải thích vì sao điểm lạ bị cô lập sau ít lần cắt hơn điểm thường",
                   "Huấn luyện một rừng cô lập bằng scikit-learn và đọc nhãn 1, âm 1",
                   "Xuất mô hình sang ONNX và chạy bằng ONNX Runtime, so kết quả với mô hình scikit-learn",
                   "Nêu giới hạn của nguyên mẫu học thuật so với hệ thống vận hành thật"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
