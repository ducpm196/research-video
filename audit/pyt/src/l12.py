from lib import *
from labkit import write_lab, practice_steps, practice_scene
from pyt_b import nbsp_spec

V = "venv"


def intro(steps, i, ids):
    steps[i]["introduces"] = ids
    return steps


PHI_DUNG = '''def phi_chuyen(tien):
    if tien < 50000:
        return 0
    phi = tien // 1000
    if phi < 1100:
        return 1100
    if phi > 11000:
        return 11000
    return phi
'''
PHI_LOI = PHI_DUNG.replace("tien < 50000", "tien <= 50000")
TEST_PHI = '''import pytest
from phi import phi_chuyen
def test_nho_mien_phi():
    assert phi_chuyen(49999) == 0
def test_toi_thieu():
    assert phi_chuyen(500000) == 1100
@pytest.mark.parametrize("tien, phi", [
    (50000, 1100), (1100000, 1100), (1101000, 1101),
    (11000000, 11000), (12000000, 11000),
])
def test_bien(tien, phi):
    assert phi_chuyen(tien) == phi
'''
DRV = 'import pytest\npytest.main(["-q", "--tb=short", "-p", "no:cacheprovider", "{}"])'
TEST_FLOAT = '''import pytest
def test_cong():
    assert 0.1 + 0.2 == 0.3
def test_cong_dung():
    assert 0.1 + 0.2 == pytest.approx(0.3)
'''
TEST_RONG = '''from phi import phi_chuyen


def test_phi():
    phi_chuyen(50000)
'''
TEST_CHEP = '''from phi import phi_chuyen


def test_chep():
    tien = 50000
    mong_doi = 0 if tien <= 50000 else max(tien // 1000, 1100)
    assert phi_chuyen(tien) == mong_doi
'''
SUA_DAU = [("tien < 50000", "tien <= 50000")]
P_OK = py("chay_ok", DRV.format("test_phi.py"), '.......                                                                  [100%]\n7 passed in 0.05s', files={"phi.py": PHI_DUNG, "test_phi.py": TEST_PHI}, env=V, show_files={"phi.py": [], "test_phi.py": []})
P_BUG = py("chay_loi", DRV.format("test_phi.py"), '..F....                                                                  [100%]\n================================== FAILURES ===================================\n____________________________ test_bien[50000-1100] ____________________________\ntest_phi.py:12: in test_bien\n    assert phi_chuyen(tien) == phi\nE   assert 0 == 1100\nE    +  where 0 = phi_chuyen(50000)\n=========================== short test summary info ===========================\nFAILED test_phi.py::test_bien[50000-1100] - assert 0 == 1100\n1 failed, 6 passed in 0.12s', files={"phi.py": PHI_LOI, "test_phi.py": TEST_PHI}, env=V, show_files={"phi.py": SUA_DAU, "test_phi.py": []})
P_FLOAT = py("so_thuc", DRV.format("test_float.py"), 'F.                                                                       [100%]\n================================== FAILURES ===================================\n__________________________________ test_cong __________________________________\ntest_float.py:3: in test_cong\n    assert 0.1 + 0.2 == 0.3\nE   assert (0.1 + 0.2) == 0.3\n=========================== short test summary info ===========================\nFAILED test_float.py::test_cong - assert (0.1 + 0.2) == 0.3\n1 failed, 1 passed in 0.15s', files={"test_float.py": TEST_FLOAT}, env=V, show_files={"test_float.py": []})
P_RONG = py("khong_assert", DRV.format("test_rong.py"), '.                                                                        [100%]\n1 passed in 0.04s', files={"phi.py": PHI_LOI, "test_rong.py": TEST_RONG}, env=V, show_files={"phi.py": SUA_DAU, "test_rong.py": []})
P_CHEP = py("sao_chep_logic", DRV.format("test_chep.py"), '.                                                                        [100%]\n1 passed in 0.03s', files={"phi.py": PHI_LOI, "test_chep.py": TEST_CHEP}, env=V, show_files={"phi.py": SUA_DAU, "test_chep.py": []})
measure("l12_scale", '''import json, os, subprocess, sys, tempfile, time
PHI = """def phi_chuyen(tien):
    if tien < 50000:
        return 0
    phi = tien // 1000
    if phi < 1100:
        return 1100
    if phi > 11000:
        return 11000
    return phi
"""
d = tempfile.mkdtemp()
with open(os.path.join(d, "phi.py"), "w") as f:
    f.write(PHI)
res = {}
for k, n in (("1e2", 100), ("1e3", 1000), ("1e4", 10000)):
    src = "import pytest\\nfrom phi import phi_chuyen\\n\\n@pytest.mark.parametrize('t', range(%d))\\ndef test_x(t):\\n    assert phi_chuyen(t * 1000) >= 0\\n" % n
    with open(os.path.join(d, "test_x.py"), "w") as f:
        f.write(src)
    t0 = time.perf_counter()
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "test_x.py"], cwd=d, capture_output=True, text=True)
    res["t_" + k] = time.perf_counter() - t0
    assert ("%d passed" % n) in r.stdout
print(json.dumps(res))''', env=V)

# Thử đột biến bằng máy: mỗi lần sửa MỘT chỗ của phi_chuyen (đổi dấu so sánh, hoặc dịch một hằng số ±1); đếm bao nhiêu cách sửa không đổi kết quả
# ở bất kỳ giá trị nào thử (tương đương, không phải lỗi) và bảy ca của bài (cùng hai ca thêm) bắt được bao nhiêu cách làm hàm sai. Số đếm tất định.
measure("l12_mut", '''import json, re
SRC = """def phi_chuyen(tien):
    if tien < 50000:
        return 0
    phi = tien // 1000
    if phi < 1100:
        return 1100
    if phi > 11000:
        return 11000
    return phi
"""


def mk(src):
    ns = {}
    exec(src, ns)
    return ns["phi_chuyen"]


orig = mk(SRC)
BAY = [(49999, 0), (500000, 1100), (50000, 1100), (1100000, 1100), (1101000, 1101), (11000000, 11000), (12000000, 11000)]
THEM = BAY + [(1099999, 1100), (11001000, 11000)]
assert all(orig(t) == p for t, p in THEM)
muts = []
for m in re.finditer(r"(<=|>=|<|>)", SRC):
    op = m.group(1)
    for new in {"<": ["<=", ">"], "<=": ["<", ">="], ">": [">=", "<"], ">=": [">", "<="]}[op]:
        muts.append(SRC[:m.start()] + new + SRC[m.end():])
for m in re.finditer(r"\\b(50000|1100|11000|1000)\\b", SRC):
    for d in (-1, 1):
        muts.append(SRC[:m.start()] + str(int(m.group(1)) + d) + SRC[m.end():])
P = set(range(0, 200000))
for c in (50000, 1100000, 11000000, 1099000, 1101000, 10999000, 11001000):
    P.update(range(c - 3000, c + 3001))
P.update(range(0, 13000001, 997))
n_equiv = c7 = c9 = 0
for src in muts:
    f = mk(src)
    if all(f(t) == orig(t) for t in P):
        n_equiv += 1
        continue
    c7 += any(f(t) != p for t, p in BAY)
    c9 += any(f(t) != p for t, p in THEM)
print(json.dumps({"n_mut": len(muts), "n_equiv": n_equiv, "n_real": len(muts) - n_equiv, "c7": c7, "c9": c9}))''')

LAB_SOL = '''import re
import subprocess
import sys
from pathlib import Path

import pytest  # noqa: F401

LOI = """def tong_n_dau(ds, n):
    tong = 0
    for i in range(1, n):
        tong = tong + ds[i]
    return tong
"""
DUNG = LOI.replace("range(1, n)", "range(n)")
KIEM = """import pytest
from tong import tong_n_dau

DS = [10, 20, 30, 40, 50]


@pytest.mark.parametrize("n, mong_doi", [(0, 0), (1, 10), (2, 30), (3, 60), (4, 100), (5, 150)])
def test_tong(n, mong_doi):
    assert tong_n_dau(DS, n) == mong_doi
"""


def chay(ma):
    Path("tong.py").write_text(ma, encoding="utf-8")
    Path("test_tong.py").write_text(KIEM, encoding="utf-8")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--tb=no", "-p", "no:cacheprovider", "test_tong.py"], capture_output=True, text=True)
    return re.sub(r" in [0-9.]+s", "", r.stdout.strip().split("\\n")[-1])


print("Ban loi:", chay(LOI))
print("Ban sua:", chay(DUNG))'''
P_LAB = py("lab_l12", LAB_SOL, 'Ban loi: 5 failed, 1 passed\nBan sua: 6 passed', env=V)
LAB_OUT = P_LAB["out"]



def nofill(steps):
    """Bỏ hai câu đệm tự động của lib.split_note (lời bài đã nêu lý do ở cả hai nửa)."""
    for s_ in steps:
        t_ = s_["say"].replace("Nghĩa là mỗi kết luận ở đây đều kiểm được bằng con số trên màn hình. ", "").replace(" Vì vậy ta đọc kết quả thật của máy ngay bên dưới.", "")
        if t_ != s_["say"]:  # tính lại `focus` cho khớp số câu mới
            s_["say"] = t_
            sents_, units_ = lv.sentences(t_), lv.html_units(s_["show"])
            if len(units_) >= 2 and len(sents_) >= 2:
                s_["focus"] = [1 + (j * len(units_)) // len(sents_) for j in range(len(sents_))]
            else:
                s_.pop("focus", None)
    return steps


def pt(p, a=None, b=None, title=None):
    """Khung cửa sổ lệnh: lệnh chạy công cụ kiểm thử rồi các dòng đầu ra [a:b] (đầu ra thật của p)."""
    outl = p["out"].split("\n")[a:b]
    body = '<div><span class="cm"><span>&#36;</span> </span>python -m pytest -q --tb=short</div>' + "".join(f"<div>{esc(l) or ' '}</div>" for l in outl)
    return (f"<p><b>{title}</b></p>" if title else "") + '<div class="code">' + body + "</div>"


def tl(src, a, b):
    """Các dòng a..b (tính từ 1) của một chuỗi mã, để hiện lên màn hình."""
    return src.strip("\n").split("\n")[a - 1:b]


def shown_sec(txt):
    """Giây ứng với chữ t_show đã hiện trên màn hình ('≈ 2 s' -> 2)."""
    v, u = txt[2:].split()
    return float(v) * {"ns": 1e-9, "µs": 1e-6, "ms": 1e-3, "s": 1, "phút": 60, "giờ": 3600, "ngày": 86400}[u]


def x_k(x, k):
    """Ngoại suy từ số ĐÃ LÀM TRÒN hiện trên màn hình (bảng khớp phép nhân: 2 s x 100 = 3 phút, không phải 4 phút)."""
    return t_show(shown_sec(t_show(x)[0]) * k)


def t_tay(sec):
    """Như t_show nhưng 2 chữ số có nghĩa: 300 000 s -> ('≈ 3,5 ngày', 'khoảng ba phẩy năm ngày')."""
    if sec < 60:
        v, u, uv = sig(sec, 2), "s", "giây"
    elif sec < 3600:
        v, u, uv = sig(sec / 60, 2), "phút", "phút"
    elif sec < 86400:
        v, u, uv = sig(sec / 3600, 2), "giờ", "giờ"
    else:
        v, u, uv = sig(sec / 86400, 2), "ngày", "ngày"
    return f"≈ {str(v).replace('.', ',')} {u}", f"khoảng {vi_num(v)} {uv}"


def build():
    mu = {k: int(M("l12_mut", k)) for k in ("n_mut", "n_equiv", "n_real", "c7", "c9")}
    t2, t3, t4 = M("l12_scale", "t_1e2"), M("l12_scale", "t_1e3"), M("l12_scale", "t_1e4")
    s2, s3, s4 = t_show(t2), t_show(t3), t_show(t4)
    s5 = x_k(t4, 10)
    m2, m3, m4 = t_tay(100 * 30), t_tay(1000 * 30), t_tay(10000 * 30)
    sc_hook = sc("hook", "hook", "Đổi một dấu so sánh: giao dịch 50 000 đồng được miễn phí nhầm", [
        st(raw_block(tl(PHI_DUNG, 1, 9), title="Tệp phi.py (đúng): phí chuyển khoản theo số tiền", py_hl=True)
           + raw_block(["- if tien < 50000:", "+ if tien <= 50000:"], title="Sửa một dòng vào thứ sáu")
           + "<p>Bản sửa (<b>diff</b>): <code>-</code> bỏ dòng, <code>+</code> thay dòng vào.</p>",
           """Hôm thứ sáu có người sửa một dòng. Trong bản sửa, dòng có dấu trừ bị bỏ, dòng có dấu cộng thay vào: đổi dấu nhỏ hơn thành nhỏ hơn hoặc bằng. Giao dịch đúng năm mươi nghìn đồng phải mất phí tối thiểu một nghìn một trăm đồng, nay được miễn phí nhầm."""),
        st(pt(P_BUG, 0, None, title="Chạy bảy ca kiểm: sáu ca qua, một ca đỏ"),
           """Bảy ca kiểm chạy tự động, sáu ca qua, đúng một ca đỏ, chính là ca đặt ở đúng biên năm mươi nghìn. Dòng đầu có bảy ký tự, mỗi ca một ký tự, và chữ hoa F là ca đỏ. Máy chỉ ra ca nào hỏng và giá trị nào: máy nhận được không, mong đợi một nghìn một trăm. Dòng bắt đầu bằng chữ khẳng định là điều ta tin là đúng, và ở đây nó sai.""", clear=True, introduces=["pyt_assert"]),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Viết một <b>ca kiểm</b> thế nào, và đọc kết quả <b>xanh – đỏ</b> ra sao?</li>
<li>Chọn <b>ca biên</b> ở đâu, vì sao lỗi hay nằm đúng chỗ đổi nhánh?</li>
<li>Khi mã lớn dần, <b>kiểm thử tự động</b> giúp gì so với kiểm tay, và những ca kiểm nào <b>không</b> giúp được gì?</li></ol></div>""",
           """Hôm nay ta học viết một ca kiểm và đọc kết quả xanh đỏ, chọn ca biên, và xem kiểm thử tự động giúp gì khi mã lớn dần, cùng những ca kiểm không giúp được gì."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: hàm, ngoại lệ, mô-đun và môi trường ảo", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① hàm và giá trị trả về", "<code>phi_chuyen(tien)</code> nhận số tiền, <b>trả về</b> phí"],
                  ["② tệp là mô-đun", "<code>from phi import phi_chuyen</code> nạp hàm từ tệp <code>phi.py</code> cùng thư mục"],
                  ["③ môi trường ảo", "công cụ kiểm thử cài trong môi trường ảo, từ tệp ghim của khoá"],
                  ["④ lỗi (ngoại lệ)", "một điều sai làm chương trình dừng với thông báo rõ; ca kiểm sẽ dùng chính cơ chế này"]]),
           """Hàm nhận số tiền và trả về phí. Tệp là mô-đun, nạp hàm từ tệp cùng thư mục. Công cụ kiểm thử được cài trong môi trường ảo từ tệp ghim của khoá. Và một điều sai làm chương trình dừng với thông báo rõ, đó là ý của ngoại lệ, mà ca kiểm sẽ dùng.""",
           focus=["1.2", "1.3", "1.4", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã tệp kiểm, khẳng định, dấu chấm và chữ F, tham số hoá và so số thực", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["tệp <code>test_phi.py</code>, hàm <code>def test_…():</code>", "tệp kiểm, ca kiểm", "tên tệp và tên hàm <b>bắt đầu bằng <code>test</code></b> thì công cụ tự tìm và chạy"],
                  ["<code>assert phi_chuyen(49999) == 0</code>", "khẳng định", "một điều ta tin là đúng; <b>đúng</b> thì ca qua, <b>sai</b> thì ca đỏ và báo giá trị thật"],
                  ["<code>python -m pytest -q --tb=short</code>", "chạy mọi ca kiểm", "<code>-m pytest</code> = chạy mô-đun <code>pytest</code> theo tên (như <code>python -m venv</code> ở bài 8); <code>-q</code> = gọn; <code>--tb=short</code> = phần chi tiết của ca đỏ in thật ngắn; in <code>.</code> mỗi ca qua, <code>F</code> mỗi ca đỏ, rồi dòng tổng kết"]]),
           """Tệp và hàm có tên bắt đầu bằng tiền tố quy ước thì công cụ tự tìm và chạy. Khẳng định là một điều ta tin là đúng: đúng thì ca qua, sai thì ca đỏ và máy báo giá trị thật. Trong lệnh chạy, cờ chữ m chạy một mô-đun theo tên, một cờ cho in gọn, một cờ cho phần chi tiết của ca đỏ thật ngắn. Máy in một dấu chấm cho mỗi ca qua, chữ F cho mỗi ca đỏ, rồi dòng tổng kết."""),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>@pytest.mark.parametrize(\"tien, phi\", [(50000, 1100), …])</code>", "tham số hoá", "dòng bắt đầu bằng <code>@</code> đứng ngay trên hàm là <b>trang trí</b>: gắn thêm hành vi cho hàm bên dưới, ở đây là chạy hàm đó <b>nhiều lần</b>, mỗi lần với một cặp giá trị trong danh sách"],
                  ["<code>pytest.approx(0.3)</code>", "xấp xỉ", "so số thực với một sai lệch nhỏ cho phép, thay cho <code>==</code>"],
                  ["<b>ca biên</b>", "ca ở sát chỗ đổi nhánh", "giá trị ngay <b>trước</b>, <b>đúng tại</b>, và ngay <b>sau</b> một ngưỡng"]]),
           """Tham số hoá cho một hàm kiểm chạy nhiều lần, mỗi lần với một cặp giá trị. Dòng bắt đầu bằng dấu a còng đứng trên hàm là dòng trang trí, gắn thêm hành vi cho hàm bên dưới. Hàm so xấp xỉ so số thực với một sai lệch nhỏ, thay cho dấu hai bằng. Ca biên là ca ở sát chỗ đổi nhánh, ngay trước, đúng tại, và ngay sau một ngưỡng.""", clear=True, introduces=["pyt_decorator"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: lỗi sống ở đường biên, nên đặt ca kiểm hai bên mỗi ngưỡng", [
        st(svg(1500, 470,
               '<line x1="60" y1="190" x2="1440" y2="190" stroke="#475569" stroke-width="4"/>',
               box(60, 50, 330, 100, ["tiền < 50 000", "phí 0"], C_GRAY, 26, True),
               box(430, 50, 240, 100, ["từ 50 000", "phí tối thiểu 1 100"], C_BLUE, 22, True),
               box(710, 50, 240, 100, ["từ 1 100 000", "phí = tiền // 1000"], C_GREEN, 22, True),
               box(990, 50, 450, 100, ["trên 11 000 000", "phí tối đa 11 000"], C_AMBER, 24, True),
               *[box(a_, 135, 8, 55, [""], C_RED) for a_ in (396, 676, 956)],
               txt(396, 220, "50 000", 24, "middle", "#dc2626", True), txt(676, 220, "1 100 000", 24, "middle", "#dc2626", True), txt(956, 220, "11 000 000", 24, "middle", "#dc2626", True),
               txt(396, 262, "49 999 | 50 000 | 50 001", 21, "middle", "#16a34a"),
               txt(676, 294, "1 099 999 | 1 100 000 | 1 101 000", 21, "middle", "#16a34a"),
               txt(1110, 262, "10 999 999 | 11 000 000 | 11 001 000", 21, "middle", "#16a34a"),
               txt(750, 340, "50 000: hàm NHẢY (phí 0 → 1 100), nên đổi dấu &lt; thành &lt;= lộ ra ở đúng một giá trị", 26, "middle", "#1f2937", True),
               txt(750, 385, "ca kiểm ở GIỮA vùng thường qua cả mã sai; ca ở SÁT ngưỡng mới bắt được", 26, "middle", "#16a34a", True),
               txt(750, 430, "1 100 000 và 11 000 000: hàm liền mạch, ca sát ngưỡng kiểm giá trị chặn (1 100, 11 000)", 24, "middle", "#6b7280")),
           """Hình này là trục số tiền, chia làm bốn vùng bởi ba ngưỡng. Dưới năm mươi nghìn thì miễn phí, rồi phí tối thiểu, rồi phí bằng tiền chia một nghìn, rồi mức tối đa. Ở năm mươi nghìn hàm nhảy, từ phí không lên một nghìn một trăm, nên đổi nhầm dấu ở đó làm kết quả khác đúng tại một giá trị. Hai ngưỡng kia phí liền mạch, nên ca sát ngưỡng ở đó kiểm giá trị chặn."""),
        st(svg(1500, 380,
               box(40, 130, 280, 100, ["sửa mã"], C_BLUE, 28, True), arrow(325, 180, 430, 180, "#475569"),
               box(435, 130, 330, 100, ["chạy mọi ca kiểm", "(vài giây)"], C_AMBER, 26, True),
               arrow(770, 150, 900, 80, "#16a34a", "xanh"), arrow(770, 210, 900, 280, "#dc2626", "đỏ"),
               box(905, 40, 360, 80, ["yên tâm, chốt thay đổi"], C_GREEN, 24, True),
               box(905, 240, 360, 80, ["xem ca nào đỏ, sửa tiếp"], C_RED, 24, True),
               arrow(1090, 245, 1090, 230, "#dc2626"),
               txt(750, 350, "vòng này lặp hàng chục lần mỗi ngày: máy làm thay người, không mệt và không bỏ sót", 26, "middle", "#1f2937", True)),
           """Hình thứ hai là vòng làm việc. Sửa mã, chạy mọi ca kiểm trong vài giây. Xanh thì chốt thay đổi, đỏ thì xem ca nào đỏ rồi sửa tiếp. Vòng này lặp hàng chục lần mỗi ngày, máy làm thay người, không mệt và không bỏ sót.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: ca kiểm đầu tiên, tham số hoá, đọc ca đỏ, vì sao chọn ca biên", nofill(splitall([
        st(raw_block(tl(TEST_PHI, 1, 6), title="Bước 1. Hai ca kiểm đầu: một khẳng định mỗi ca (nửa trên của test_phi.py)", py_hl=True)
           + "<p>Theo <b>đặc tả</b> (bản mô tả bằng lời: đầu vào nào thì kết quả phải là gì; <b>không</b> theo mã): dưới $50\\,000$ phí $0$; phí là tiền chia $1000$ <b>lấy phần nguyên</b> (làm tròn xuống), nhưng tối thiểu $1\\,100$, tối đa $11\\,000$. $500\\,000$ chia $1000$ được $500$, thấp hơn mức tối thiểu nên phí $1\\,100$.</p>",
           """Bước một, hai ca kiểm đầu, mỗi ca một khẳng định. Đặc tả là bản mô tả bằng lời đầu vào nào thì kết quả phải là gì, và giá trị mong đợi lấy từ đó, không lấy từ mã. Dưới năm mươi nghìn thì phí là không. Còn lại phí là tiền chia một nghìn, làm tròn xuống. Năm trăm nghìn chia một nghìn được năm trăm, thấp hơn mức tối thiểu, nên phí là một nghìn một trăm."""),
        st(raw_block(tl(TEST_PHI, 7, 12), title="Bước 2. Tham số hoá: một hàm, năm ca biên (nửa dưới, nối ngay sau nửa trên)", py_hl=True)
           + "<p>Vì mỗi cặp <code>(tiền, phí)</code> là một ca riêng, năm cặp thành năm ca; khi một cặp đỏ, máy nêu <b>đúng cặp nào</b>. Tổng số ca: $2 + 5 = 7$.</p>",
           """Bước hai, tham số hoá. Một hàm kiểm với danh sách năm cặp giá trị cho năm ca riêng. Vì mỗi cặp là một ca, khi một cặp đỏ, máy nêu đúng cặp nào. Cộng với hai ca ở bước một, ta có bảy ca. Hai nửa nối liền là tệp kiểm trọn vẹn; hãy lưu nó cạnh tệp chứa hàm tính phí rồi chạy công cụ kiểm thử.""", clear=True),
        st(pt(P_OK, title="Chạy với mã đúng: bảy dấu chấm") + "<p>Mỗi <code>.</code> là một ca qua; dòng cuối: <code>7 passed</code>. Thời gian ghi ở cuối là số minh hoạ.</p>",
           """Chạy với mã đúng, máy in bảy dấu chấm và dòng tổng kết. Vì mỗi ca qua in một dấu chấm, bảy dấu chấm nghĩa là bảy ca qua. Thời gian ghi ở cuối là số minh hoạ, do mỗi máy chạy nhanh chậm khác nhau.""", clear=True),
        st(pt(P_BUG, 5, 10, title="Bước 3. Đọc một ca đỏ từ dưới lên") + "<p>Dòng cuối: <code>1 failed, 6 passed</code>. Dòng <code>FAILED …[50000-1100]</code>: ca có <code>tien = 50000</code>. <code>assert 0 == 1100</code>: mã trả $0$, đặc tả đòi $1\\,100$. Số <code>:12</code> là dòng thứ mười hai của tệp bạn gõ (không có dòng trống); thêm dòng trống thì số này đổi, không sao. Màn hình đã <b>rút gọn</b>: máy thật còn in thêm, phía trên, dòng <code>..F....</code> và dòng tiêu đề <code>FAILURES</code>.</p>",
           """Bước ba, đọc một ca đỏ từ dưới lên. Màn hình này đã rút gọn, máy thật còn in thêm ở phía trên hai dòng bạn đã thấy ở đầu bài. Vì dòng cuối tóm tắt tất cả, nó cho biết một ca đỏ, sáu ca qua. Dòng báo ca hỏng nêu rõ ca có số tiền năm mươi nghìn. Dòng khẳng định cho thấy mã trả về không, trong khi đặc tả đòi một nghìn một trăm. Vì đủ ba mẩu thông tin đó, ta tìm ra dòng lỗi.""", clear=True),
        st(raw_block(["if tien < 50000:    # mã đúng", "if tien <= 50000:   # mã sai"], title="Hai bản mã chỉ khác dòng thứ hai của hàm", py_hl=True)
           + "<p>Vì mã sai chỉ khác ở dấu <code>&lt;=</code> so với <code>&lt;</code>, <b>chỉ</b> giá trị <code>50000</code> cho kết quả khác; các giá trị $49\\,999$ và $500\\,000$ đều ra như nhau ở cả hai bản mã. Hai ca ở bước $1$ <b>qua cả mã sai</b>.</p>",
           """Vì sao chỉ một ca bắt được? Vì mã sai chỉ khác ở dấu so sánh, nên chỉ đúng giá trị năm mươi nghìn cho kết quả khác. Giá trị bốn mươi chín nghìn chín trăm chín mươi chín và năm trăm nghìn ra như nhau ở cả hai bản mã. Hai ca ở bước một qua cả mã sai.""", clear=True),
    ], only=[2, 3])), checks=["500000 // 1000 == 500 and 500 < 1100", "2 + 5 == 7", "[x for x in (49999, 50000, 50001) if x < 50000] == [49999] and [x for x in (49999, 50000, 50001) if x <= 50000] == [49999, 50000]"])
    sc_ex = sc("example", "example", "Ví dụ: so số thực bằng xấp xỉ, và các ca biên của ba ngưỡng", [
        st(raw_block(tl(TEST_FLOAT, 1, 5), title="Tệp test_float.py: một ca so bằng ==, một ca so xấp xỉ", py_hl=True),
           """Ví dụ một, số thực. Đây là tệp kiểm có hai ca, lưu thành một tệp riêng. Ca đầu khẳng định không phẩy một cộng không phẩy hai bằng không phẩy ba, bằng dấu hai bằng. Ca sau khẳng định điều đó bằng hàm so xấp xỉ."""),
        st(pt(P_FLOAT, 2, None, title="Số thực: so bằng == đỏ, so bằng xấp xỉ thì qua")
           + "<p>Vì $0{,}1 + 0{,}2$ lệch $0{,}3$ một chút nhỏ (bài đầu khoá), ca có <code>==</code> đỏ: <code>assert (0.1 + 0.2) == 0.3</code>. Ca dùng xấp xỉ qua.</p>",
           """Nhớ rằng không phẩy một cộng không phẩy hai lệch không phẩy ba một chút nhỏ, từ bài đầu khoá. Ca so bằng dấu hai bằng đỏ, và máy in ra biểu thức đã khẳng định. Ca dùng hàm so xấp xỉ qua. Khi kiểm số thực, luôn dùng so xấp xỉ.""", clear=True),
        st(table(["ngưỡng", "ca trước", "ca đúng tại", "ca sau"],
                 [["50 000 (miễn phí)", "49 999 → 0", "50 000 → 1 100", "50 001 → 1 100"],
                  ["1 100 000 (hết tối thiểu)", "1 099 999 → 1 100", "1 100 000 → 1 100", "1 101 000 → 1 101"],
                  ["11 000 000 (tối đa)", "10 999 999 → 10 999", "11 000 000 → 11 000", "11 001 000 → 11 000"]])
           + "<p class='note'>Ở hai ngưỡng sau, ca “ngay sau” cách ngưỡng $1\\,000$ vì phí $=$ tiền chia $1000$ (bước nhỏ nhất làm phí đổi); ở $50\\,000$ các ca cách $1$ đồng. Giá trị ở cột phải <b>tính tay từ đặc tả</b> (chia nghìn, <b>làm tròn xuống</b>, kẹp trong khoảng $[1\\,100, 11\\,000]$), không chạy mã để lấy.</p>",
           """Ví dụ hai, các ca biên của ba ngưỡng. Quanh năm mươi nghìn, quanh một triệu một trăm nghìn, nơi hết mức tối thiểu, và quanh mười một triệu, nơi chạm mức tối đa. Mỗi ngưỡng có ba ca, ngay trước, đúng tại và ngay sau. Ở hai ngưỡng sau, ca ngay sau cách ngưỡng một nghìn đồng. Giá trị mong đợi tính tay từ đặc tả, chia nghìn và làm tròn xuống, rồi kẹp vào khoảng cho phép, không chạy mã để lấy.""", clear=True),
        st(table(["ca", "mã đúng", "mã sai (<=)", "ca bắt được lỗi?"],
                 [["49 999 → 0", "qua", "qua", "không"], ["500 000 → 1 100", "qua", "qua", "không"], ["50 000 → 1 100", "qua", "<b>đỏ (0)</b>", "<b>có</b>"],
                  ["1 100 000 → 1 100", "qua", "qua", "không"], ["1 101 000 → 1 101", "qua", "qua", "không"], ["11 000 000 → 11 000", "qua", "qua", "không"], ["12 000 000 → 11 000", "qua", "qua", "không"]]),
           """Ví dụ ba, ca nào bắt được lỗi. Với mã đúng cả bảy ca qua. Với mã sai chỉ khác ở dấu so sánh, sáu ca vẫn qua, và đúng một ca đỏ, ca đặt đúng tại ngưỡng năm mươi nghìn. Vì thế ca biên không phải là thừa, nó là ca duy nhất có giá trị ở đây.""", clear=True),
        st(f"<div class='box key'><b>Thử đột biến bằng máy.</b> Sửa hàm mỗi lần một chỗ: ba dấu so sánh, mỗi dấu đổi hai cách (ví dụ <code>&lt;</code> thành <code>&lt;=</code>, hoặc <code>&lt;</code> thành <code>&gt;</code>), là $3 \\times 2 = 6$; sáu chỗ có hằng số (<code>50000</code> một lần, <code>1100</code> hai lần, <code>11000</code> hai lần, <code>1000</code> một lần), mỗi chỗ dịch lên hoặc xuống $1$, là $6 \\times 2 = 12$. Cộng lại {mu['n_mut']} cách. {mu['n_equiv']} cách <b>không đổi kết quả ở mọi giá trị đã thử</b>, nên không phải lỗi; {mu['n_real']} cách làm hàm sai. Bảy ca của bài bắt {mu['c7']} trong {mu['n_real']} cách đó.</div>",
           f"""Sửa hàm mỗi lần một chỗ. Ba dấu so sánh, mỗi dấu đổi hai cách, như nhỏ hơn thành nhỏ hơn hoặc bằng, hoặc thành lớn hơn. Sáu chỗ có hằng số, mỗi chỗ dịch lên hoặc xuống một. Cộng lại được {words(mu['n_mut'])} cách. Có {words(mu['n_equiv'])} cách không đổi kết quả ở đâu cả, nên không phải lỗi, và {words(mu['n_real'])} cách làm hàm sai. Bảy ca của bài bắt {words(mu['c7'])} trong số đó.""", clear=True),
        st(f"<p>Ở $50\\,000$ hàm <b>nhảy</b> (phí từ $0$ lên $1\\,100$), nên đổi <code>&lt;</code> thành <code>&lt;=</code> lộ ra ở đúng một giá trị. Ở $1\\,100\\,000$ và $11\\,000\\,000$ hàm <b>liền mạch</b> ($1\\,100$ gặp $1\\,100$; $11\\,000$ gặp $11\\,000$), nên đổi dấu ở đó cho kết quả y hệt: không ca nào bắt được, và cũng không là lỗi; ca sát ngưỡng ở đó kiểm <b>giá trị chặn</b>. Thêm hai ca <code>1 099 999 → 1 100</code> và <code>11 001 000 → 11 000</code> thì bắt {mu['c9']} trong {mu['n_real']}.</p>",
           f"""Ở năm mươi nghìn hàm nhảy nên đổi dấu lộ ra ở đúng một giá trị. Ở hai ngưỡng kia hàm liền mạch, đổi dấu cho kết quả y hệt, không ca nào bắt được và cũng không là lỗi, nên ca sát ngưỡng ở đó kiểm giá trị chặn. Thêm hai ca, ngay trước ngưỡng thứ hai và ngay sau ngưỡng thứ ba, thì bắt đủ {words(mu['c9'])} cách.""", clear=True),
    ], checks=["(lambda f, g: [f(t) == g(t) for t in (49999, 500000, 50000, 1100000, 1101000, 11000000, 12000000)])(lambda t: 0 if t < 50000 else min(max(t // 1000, 1100), 11000), lambda t: 0 if t <= 50000 else min(max(t // 1000, 1100), 11000)) == [True, True, False, True, True, True, True]", "1099999 // 1000 == 1099 and max(1099, 1100) == 1100", "1101000 // 1000 == 1101", "10999999 // 1000 == 10999", "12000000 // 1000 == 12000 and min(12000, 11000) == 11000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: tính tay giá trị mong đợi, và đếm số ca", [
        st(repl_block(repl("KiemTay", [("[0, 500000 // 1000, 1100000 // 1000, 1101000 // 1000, 11000000 // 1000, 12000000 // 1000]", "[0, 500, 1100, 1101, 11000, 12000]"),
                                       ("[0, max(500, 1100), 1100, 1101, min(11000, 11000), min(12000, 11000)]", "[0, 1100, 1100, 1101, 11000, 11000]"), ("2 + 5", "7")]), title="Tính tay giá trị mong đợi từ đặc tả")
           + "<p>Hai bước tính tay (chia nghìn, rồi kẹp vào $[1\\,100, 11\\,000]$) cho đúng các giá trị trong bảng ca kiểm; $2 + 5 = 7$ ca khớp dòng tổng kết. <code>max(a, b)</code> lấy số lớn hơn, <code>min(a, b)</code> số nhỏ hơn: dùng để kẹp.</p>",
           """Đường kiểm khác, tính tay giá trị mong đợi từ đặc tả. Bước một chia nghìn. Bước hai kẹp vào khoảng từ một nghìn một trăm đến mười một nghìn, bằng lệnh lấy số lớn hơn và lệnh lấy số nhỏ hơn. Vì hai bước đó độc lập với mã, kết quả trùng với các giá trị trong bảng ca kiểm là đáng tin. Đếm số ca, hai cộng năm bằng bảy, khớp dòng tổng kết của máy."""),
    ], checks=["[0, max(500, 1100), 1100, 1101, min(11000, 11000), min(12000, 11000)] == [0, 1100, 1100, 1101, 11000, 11000]"])
    sc_scale = sc("scale", "concept", "Khi mã lớn dần: kiểm tay không theo kịp, máy chạy tự động vẫn nhanh", [
        st(table(["số ca kiểm", "máy chạy tự động (đo, số minh hoạ)", "người chạy tay (giả định 30 giây mỗi ca, số minh hoạ)"],
                 [["×1: 100", s2[0], m2[0]], ["×10: 1 000", s3[0], m3[0]], ["×100: 10 000", s4[0], m4[0]], ["×1 000 (ngoại suy): 100 000", s5[0], t_tay(100000 * 30)[0]]])
           + "<p class='note'>Thời gian máy đo trên máy kiểm, gồm cả khởi động công cụ; số minh hoạ; <b>ngoại suy</b> = nhân theo tỉ lệ từ số đã đo (ước lượng, chưa đo).</p>",
           f"""Bảng này cho thấy quy mô. Một trăm ca máy chạy trong {s2[1]}, một nghìn ca mất {s3[1]}, mười nghìn ca mất {s4[1]}. Giả sử một người chạy tay mỗi ca ba mươi giây, số giả định để minh hoạ. Khi đó một trăm ca mất {m2[1]}, một nghìn ca mất {m3[1]}, mười nghìn ca mất {m4[1]}. Máy tăng chậm hơn rất nhiều."""),
        st("<div class='box key'><b>Đánh đổi:</b> ca kiểm là <b>mã bạn phải viết và giữ</b>: tốn công lúc đầu, và khi đặc tả đổi thì phải sửa cả ca kiểm. "
           "Đổi lại, mỗi lần sửa mã, máy kiểm lại <b>toàn bộ</b> trong vài giây. Ca kiểm chậm (gọi mạng, đọc tệp lớn) làm người ta ngại chạy: tách ca nhanh khỏi ca chậm. <b>Hàm thuần</b> (kết quả chỉ phụ thuộc đầu vào, không đọc tệp hay gọi mạng) kiểm rất nhanh.</div>",
           """Đánh đổi: ca kiểm là mã bạn phải viết và giữ, tốn công lúc đầu, và phải sửa khi đặc tả đổi. Đổi lại, mỗi lần sửa mã, máy kiểm lại toàn bộ trong vài giây. Ca kiểm chậm, như gọi mạng hay đọc tệp lớn, làm người ta ngại chạy, nên hãy tách ca nhanh khỏi ca chậm. Ca nhanh kiểm hàm thuần, tức hàm có kết quả chỉ phụ thuộc đầu vào.""", clear=True, introduces=["pyt_ham_thuan"]),
    ], checks=["100 * 30 == 3000 and 1000 * 30 == 30000 and 10000 * 30 == 300000", "100000 // 10000 == 10"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Khẳng định số thực bằng <code>==</code>.</div>' + pt(P_FLOAT, 2, 6)
           + "<p>Ca đỏ dù mã đúng. Phép thử: <b>dùng xấp xỉ</b> cho mọi so sánh số thực.</p>",
           """Lỗi thứ nhất, của người mới, là khẳng định số thực bằng dấu hai bằng. Ca đỏ dù mã đúng, vì số thực lệch một chút nhỏ. Phép thử là dùng so xấp xỉ cho mọi so sánh số thực."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Ca kiểm không có khẳng định: luôn qua.</div>'
           + raw_block(tl(TEST_RONG, 1, 5), title="Tệp test_rong.py: gọi hàm, không có dòng khẳng định", py_hl=True),
           """Lỗi thứ hai, của người đã đi làm, là ca kiểm không có khẳng định, chỉ gọi hàm rồi thôi, như trong tệp này.""", clear=True),
        st(pt(P_RONG, title="Chạy với phi.py vẫn mang dấu nhỏ hơn hoặc bằng")
           + "<p>Hàm <code>phi.py</code> vẫn <b>sai</b> (<code>&lt;=</code>) nhưng ca <b>xanh</b>, vì không có gì để sai. Xanh giả tệ hơn không có ca. Phép thử: <b>cố ý làm hỏng mã</b> (đổi dấu) rồi xem ca có đỏ không.</p>",
           """Hàm vẫn sai, nhưng ca xanh, vì không có gì để sai. Xanh giả tệ hơn không có ca kiểm, vì nó cho cảm giác an toàn. Phép thử là cố ý làm hỏng mã, ví dụ đổi một dấu, rồi xem ca có đỏ không.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Giá trị mong đợi tính bằng cùng công thức của mã: mã sai thì ca sai theo.</div>'
           + raw_block(tl(TEST_CHEP, 1, 7), title="Tệp test_chep.py: mong đợi tính bằng chính công thức của mã", py_hl=True)
           + "<p><code>A if điều_kiện else B</code> là <b>biểu thức điều kiện một dòng</b>: lấy <code>A</code> nếu điều kiện đúng, nếu không thì lấy <code>B</code>. Dòng <code>mong_doi = 0 if tien &lt;= 50000 else max(…)</code> đọc là “mong đợi bằng $0$ nếu tiền không quá $50\\,000$, còn lại bằng số lớn hơn trong hai số”.</p>",
           """Lỗi thứ ba, của người đã đi làm, là tính giá trị mong đợi bằng cùng công thức của mã, như dòng tính ở giữa tệp kiểm này. Dòng đó là biểu thức điều kiện một dòng: lấy giá trị đứng đầu nếu điều kiện đúng, nếu không thì lấy giá trị sau từ khoá còn lại. Lệnh lấy số lớn chọn số lớn hơn trong hai số.""", clear=True),
        st(pt(P_CHEP, title="Chạy với phi.py vẫn mang dấu nhỏ hơn hoặc bằng")
           + "<p>Ca <b>lặp lại đúng cái lỗi</b> (<code>&lt;=</code>) nên luôn khớp mã. Giá trị mong đợi phải đến từ <b>đặc tả hoặc tính tay</b>, độc lập với mã.</p>",
           """Ca lặp lại đúng cái lỗi nên luôn khớp mã, và xanh. Giá trị mong đợi phải đến từ đặc tả hoặc tính tay, độc lập với mã.""", clear=True),
    ], checks=["abs((0.1 + 0.2) - 0.3) < 1e-9", "0.1 + 0.2 != 0.3"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Hàm <code>phi_chuyen</code> ở trên.</p>
<ol><li>Kể ba ca biên quanh ngưỡng $11\\,000\\,000$ và phí mong đợi của từng ca (tính tay).</li>
<li>Sau khi sửa mã, ca <code>test_bien[50000-1100]</code> vẫn đỏ. Sửa <b>ca kiểm</b> hay sửa <b>mã</b>?</li></ol>
<p><b>Quyết định:</b> bạn có $5$ phút. Viết $1$ ca ở giữa vùng hay $3$ ca sát ngưỡng? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Câu một, kể ba ca biên quanh ngưỡng mười một triệu và phí mong đợi của từng ca, tính tay. Câu hai, sau khi sửa mã, ca ở năm mươi nghìn vẫn đỏ, sửa ca kiểm hay sửa mã.
           Sau đó là một quyết định, bạn có năm phút, viết một ca ở giữa vùng hay ba ca sát ngưỡng, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(table(["câu", "đáp án"], [["1", "$10\\,999\\,999 \\to 10\\,999$; $11\\,000\\,000 \\to 11\\,000$; $11\\,001\\,000 \\to 11\\,000$ (ngay sau, đã chạm mức tối đa; cách $1\\,000$ vì phí $=$ tiền chia $1000$, nên phải thêm $1\\,000$ đồng phí mới đổi một đơn vị)"],
                                     ["2", "sửa <b>mã</b>, nếu ca khớp đặc tả. Chỉ sửa ca khi <b>đặc tả đổi có chủ ý</b>"]]),
           """Đáp án như sau. Câu một, ngay trước ngưỡng cho phí mười nghìn chín trăm chín mươi chín. Đúng tại ngưỡng cho mười một nghìn. Ngay sau ngưỡng, mười một triệu một nghìn đồng, phí vẫn mười một nghìn, đã chạm mức tối đa. Câu hai, sửa mã, nếu ca khớp đặc tả. Chỉ sửa ca khi đặc tả đổi có chủ ý."""),
        st("<div class='box key'><b>Quyết định:</b> <b>ba ca sát ngưỡng</b>. Ca ở giữa vùng thường qua cả mã sai (như hai ca ở bước $1$); lỗi sống ở chỗ đổi nhánh. "
           "Ở chỗ hàm <b>nhảy</b> ($50\\,000$), ba ca ngay trước, đúng tại, ngay sau bắt lỗi đổi dấu và lỗi lệch một; ở chỗ hàm <b>liền mạch</b> ($1\\,100\\,000$, $11\\,000\\,000$), đổi dấu không đổi kết quả và ca sát ngưỡng kiểm giá trị chặn.</div>",
           """Quyết định, ba ca sát ngưỡng. Ca ở giữa vùng thường qua cả mã sai, và lỗi sống ở chỗ đổi nhánh. Ở chỗ hàm nhảy, ba ca ngay trước, đúng tại và ngay sau bắt lỗi đổi dấu và lỗi lệch một. Ở chỗ hàm liền mạch, đổi dấu không đổi kết quả, và ca sát ngưỡng kiểm giá trị chặn.""", clear=True),
    ], checks=["10999999 // 1000 == 10999", "min(11000000 // 1000, 11000) == 11000 and min(11001000 // 1000, 11000) == 11000 and 11001000 // 1000 == 11001"])
    sc_prac = practice_scene(sc, "Tự làm: viết ca kiểm bắt lỗi lệch một", intro(intro(pr_steps(
        st, "PYT", "L12",
        """<p><b>Đề</b> (cần môi trường ảo đã cài thư viện): hàm trong <code>de.md</code> cộng <code>n</code> phần tử đầu của danh sách nhưng có lỗi <b>lệch một</b> (<code>range(1, n)</code>). Viết <code>kiem_thu.py</code>:</p>
<ol><li>ghi hai bản mã (<code>LOI</code> và <code>DUNG</code>) và tệp kiểm <code>test_tong.py</code> với <code>DS = [10, 20, 30, 40, 50]</code>, tham số hoá <b>6 ca</b> <code>n = 0..5</code>, giá trị mong đợi <b>tự tính tay</b>;</li>
<li>chạy công cụ kiểm thử trên từng bản bằng <code>subprocess</code> (chạy một chương trình khác từ chương trình của bạn, rồi lấy đầu ra), in dòng tổng kết (bỏ phần thời gian): <code>Ban loi: …</code> và <code>Ban sua: …</code>.</li></ol>""",
        """Bây giờ tới phần bạn tự làm, trong môi trường ảo đã cài thư viện. Đề bài cho một hàm cộng n phần tử đầu của danh sách nhưng có lỗi lệch một. Viết một chương trình ghi hai bản mã, bản lỗi và bản đúng, cùng một tệp kiểm với danh sách năm số và sáu ca, n từ không đến năm, giá trị mong đợi tự tính tay. Rồi chạy công cụ kiểm thử trên từng bản bằng cách chạy một chương trình khác từ chương trình của mình, và in dòng tổng kết, bỏ phần thời gian.
        Hãy dừng video và làm.""",
        LAB_OUT, "kiem_thu.py",
        """<div class="box key"><b>Nếu kẹt:</b> giá trị mong đợi: tổng $n$ phần tử đầu của $[10, 20, 30, 40, 50]$ là $0, 10, 30, 60, 100, 150$. Chạy: <code>subprocess.run([sys.executable, "-m", "pytest", "-q", "--tb=no", "-p", "no:cacheprovider", "test_tong.py"], capture_output=True, text=True)</code>; <code>.stdout</code> là chữ chương trình con đã in, và dòng tổng kết là dòng cuối của nó.</div>
<div class="box key"><code>sys.executable</code> là đường dẫn tới <b>chính bản Python đang chạy bạn</b>, để chương trình con dùng đúng môi trường ảo; <code>capture_output=True</code> <b>giữ</b> đầu ra lại để bạn lấy, thay vì in thẳng ra màn hình; <code>text=True</code> cho đầu ra là <b>chữ</b>, không phải byte; <code>--tb=no</code> bỏ phần chi tiết ca đỏ, nên dòng cuối là dòng tổng kết; <code>-p no:cacheprovider</code> tắt thư mục nhớ tạm của công cụ. Lời giải ở <code>labs/PYT/L12/loi_giai.py</code>.</div>""",
        """Nếu kẹt, giá trị mong đợi là tổng n phần tử đầu, lần lượt không, mười, ba mươi, sáu mươi, một trăm, một trăm năm mươi. Chạy công cụ kiểm thử bằng lệnh chạy tiến trình con, rồi lấy dòng cuối của đầu ra làm tổng kết.
        Hãy gọi đường dẫn của chính bản Python đang chạy, để chương trình con dùng đúng môi trường ảo. Tham số giữ đầu ra cho ta lấy chữ in ra, thay vì để nó trôi lên màn hình, và tham số kiểu chữ cho đầu ra là chữ chứ không phải byte.
        Cờ bỏ chi tiết làm dòng cuối thành dòng tổng kết. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=1200), 0, ["pyt_subprocess"]), 2, ["pyt_sys_executable", "pyt_capture_output"]), "PYT", "L12")
    write_lab("PYT", "L12", """# Lab PYT L12 — Viết ca kiểm bắt lỗi lệch một

**cần: pip install -r labs/requirements-py.txt** (trong môi trường ảo của bài 8). Hàm có lỗi **lệch một** (`range(1, n)` bỏ phần tử đầu), và bản đúng (`range(n)`):

```python
def tong_n_dau(ds, n):
    tong = 0
    for i in range(1, n):      # LỖI: phải là range(n)
        tong = tong + ds[i]
    return tong
```

Viết `kiem_thu.py` (số minh hoạ; khác ví dụ trong bài):

1. Ghi `tong.py` (lần lượt bản **lỗi** rồi bản **đúng**) và `test_tong.py` có `DS = [10, 20, 30, 40, 50]` và `@pytest.mark.parametrize("n, mong_doi", […])` với **6 ca** `n = 0, 1, 2, 3, 4, 5`. **Tự tính tay** giá trị mong đợi (tổng `n` phần tử đầu), không chạy mã để lấy.
2. Với mỗi bản: chạy `python -m pytest -q --tb=no -p no:cacheprovider test_tong.py` bằng `subprocess.run([sys.executable, "-m", "pytest", …], capture_output=True, text=True)` (`sys.executable` là đường dẫn tới chính bản Python đang chạy bạn, để chương trình con dùng cùng môi trường ảo; `capture_output=True` giữ đầu ra lại thay vì in ra màn hình; `text=True` cho `stdout` là chữ, không phải byte; `--tb=no` bỏ chi tiết ca đỏ; `-p no:cacheprovider` tắt thư mục nhớ tạm); lấy dòng cuối của `stdout`, bỏ phần ` in …s`; in `Ban loi: <dòng>` rồi `Ban sua: <dòng>`.
3. Nhớ `import pytest` ở đầu tệp (máy chấm cần thấy thư viện này để dùng môi trường đã cài).

Chạy: `python kiem_thu.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L12 kiem_thu.py`.
""", "py", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("ca kiểm = một khẳng định có giá trị mong đợi từ ĐẶC TẢ", "tham số hoá: một hàm, nhiều ca", "ca biên: ngay trước, đúng tại, ngay sau mỗi ngưỡng",
                 "số thực: so xấp xỉ", "xanh giả: ca không khẳng định gì; cố ý làm hỏng mã để thử ca", "mã lớn dần: máy kiểm lại tất cả trong vài giây"),
           """Ca kiểm là một khẳng định với giá trị mong đợi lấy từ đặc tả. Tham số hoá cho một hàm, nhiều ca. Ca biên đặt ngay trước, đúng tại và ngay sau mỗi ngưỡng. Số thực thì so xấp xỉ. Xanh giả là ca không khẳng định gì, nên cố ý làm hỏng mã để thử ca.
           Và khi mã lớn dần, máy kiểm lại tất cả trong vài giây."""),
        st("""<div class='box key'><b>Tư duy:</b> hỏi “nếu mã sai, ca này có đỏ không?”. Ca chưa từng đỏ là ca chưa được thử. Viết ca <b>từ đặc tả</b>, đặt <b>sát ngưỡng</b>, và chạy sau <b>mỗi</b> thay đổi.</div>
<p>Bài sau, bài cuối của khoá: một dự án phân tích tệp giao dịch lớn dần từ một nghìn đến một trăm triệu dòng, ghép mọi thứ đã học.</p>""",
           """Điều cần mang theo, hãy hỏi nếu mã sai thì ca này có đỏ không. Ca chưa từng đỏ là ca chưa được thử. Viết ca từ đặc tả, đặt sát ngưỡng, và chạy sau mỗi thay đổi.
           Bài sau, bài cuối của khoá, là một dự án phân tích tệp giao dịch lớn dần từ một nghìn đến một trăm triệu dòng, ghép mọi thứ đã học.""", forward_ref=True),
    ])
    return nbsp_spec(lesson("L12", "kiem_thu_tu_dong", "Bài 12 — Kiểm thử tự động: ca kiểm, ca biên",
                  "curriculum/pyt.yaml L12; audit/pyt/verify_pyt.py L12 (chạy thật trên Python 3.11, labs/.venv-pyt: pytest 9.2.0 theo labs/requirements-py.txt; thời gian chạy N ca đo bằng verify_pyt, máy kiểm, số minh hoạ; chạy tay 30 giây/ca là giả định minh hoạ); "
                  "pytest documentation: Get Started, How to parametrize fixtures and test functions, How to write and report assertions, approx; phân tích giá trị biên (boundary value analysis): Myers, The Art of Software Testing (1979) — NOT_VERIFIED trang; quy tắc phí là số minh hoạ",
                  ["Viết ca kiểm bằng khẳng định và chạy bằng công cụ kiểm thử",
                   "Đọc kết quả xanh đỏ và tìm ca hỏng, giá trị thật, giá trị mong đợi",
                   "Tham số hoá nhiều ca trong một hàm kiểm",
                   "Chọn ca biên ngay trước, đúng tại và ngay sau mỗi ngưỡng",
                   "Tính giá trị mong đợi độc lập với mã và kiểm số ca",
                   "Nêu thời gian kiểm tự động và kiểm tay thay đổi thế nào khi số ca tăng",
                   "Chỉ ra ba lỗi hay gặp: so số thực bằng dấu hai bằng, ca không khẳng định, mong đợi lấy từ chính công thức của mã",
                   "Viết ca kiểm bắt được lỗi lệch một"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  assumes=["pyt_ngoai_suy", "pyt_ngoai_le"],
                  covers=[(1, "formula"), (2, "formula"), (3, "formula"), (4, "example"), (5, "check"), (6, "scale"), (7, "pitfalls"), (8, "practice")]))
