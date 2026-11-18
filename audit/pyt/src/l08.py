from lib import *
from labkit import write_lab, practice_steps, practice_scene

REQ = (ROOT / "labs" / "requirements-py.txt").read_text(encoding="utf-8").replace("\r\n", "\n")
NREQ = len([l for l in REQ.split("\n") if l.strip()])
MOD_GD = '''def tong_tien(ds):
    tong = 0
    for x in ds:
        tong = tong + x
    return tong

print("__name__ =", __name__)
if __name__ == "__main__":
    print("tu kiem:", tong_tien([100, 200]))
'''
MOD_CHAY = '''import giao_dich

print(giao_dich.tong_tien([500000, 250000]))
'''
SH_MOD = sh("Module", [
    ("python giao_dich.py", "__name__ = __main__\ntu kiem: 300"),
    ("python chay.py", "__name__ = giao_dich\n750000"),
], files={"giao_dich.py": MOD_GD, "chay.py": MOD_CHAY})
PKG_PHI = '''def phi_chuyen(tien):
    phi = tien // 1000
    if phi < 1100:
        return 1100
    return phi
'''
PKG_CHAY = '''from ngan_hang.phi import phi_chuyen
import ngan_hang.phi as p

print(phi_chuyen(500000), phi_chuyen(5000000))
print(p.phi_chuyen(2000000))
'''
SH_PKG = sh("Goi", [
    ("ls ngan_hang", "__init__.py  phi.py"),
    ("python chay_goi.py", "1100 5000\n2000"),
], files={"ngan_hang/__init__.py": "", "ngan_hang/phi.py": PKG_PHI, "chay_goi.py": PKG_CHAY})
SH_SHADOW = sh("TrungTen", [
    ("python chay.py 2>&1 | tail -n 1 | cut -c1-58", "AttributeError: module 'csv' has no attribute 'DictReader'"),
    ("mv csv.py csv_cua_toi.py", ""),
    ("python chay.py", "<class 'csv.DictReader'>"),
], files={"csv.py": "# tep tu viet, vo tinh trung ten voi bo csv co san\n", "chay.py": "import csv\n\nprint(csv.DictReader)\n"},
    show_files={"csv.py": [], "chay.py": []})
SH_VENV = sh("Venv", [
    ("python -m venv .venv", ""),
    ('python -c "import sys; print(sys.prefix != sys.base_prefix)"', "False"),
    ('.venv/Scripts/python -c "import sys; print(sys.prefix != sys.base_prefix)"', "True"),
    ('.venv/Scripts/python -c "import numpy" 2>&1 | tail -n 1', "ModuleNotFoundError: No module named 'numpy'"),
], only311=True)
SH_ACT = sh("Kich", [
    ("python -m venv .venv", ""),
    ('source .venv/Scripts/activate && python -c "import sys; print(sys.prefix != sys.base_prefix)"', "True"),
])
SH_REQ = sh("Req", [
    ("grep pandas requirements.txt", "pandas==3.1.1"),
    ("wc -l requirements.txt", f"{NREQ} requirements.txt"),
], files={"requirements.txt": REQ})
P_MAIN = py("khong_guard", '''def tong_tien(ds):
    tong = 0
    for x in ds:
        tong = tong + x
    return tong


print("chay thu:", tong_tien([1, 2, 3]))''', "chay thu: 6")
SH_IMP = sh("NapKhongGuard", [("python -c \"import khong_guard\"", "chay thu: 6")], files={"khong_guard.py": P_MAIN["code"] + "\n"}, show_files={"khong_guard.py": []})
measure("l08_pkgs", '''import json
from importlib import metadata
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name


def dong(ten):
    seen, stack = set(), [canonicalize_name(n) for n in ten]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        try:
            d = metadata.distribution(n)
        except metadata.PackageNotFoundError:
            continue
        seen.add(n)
        for r in d.requires or []:
            q = Requirement(r)
            if q.marker is not None and not q.marker.evaluate({"extra": ""}):
                continue
            stack.append(canonicalize_name(q.name))
    return len(seen)


print(json.dumps({"n_numpy": dong(["numpy"]), "n_pandas": dong(["numpy", "pandas"]), "n_mpl": dong(["numpy", "pandas", "matplotlib"]),
                  "n_all": dong(["numpy", "pandas", "matplotlib", "pytest"])}))''', env="venv")
measure("l08_import", '''import json, subprocess, sys, time
res = {}
for name in ("json", "numpy", "pandas", "matplotlib", "pytest"):
    best = 1e9
    for _ in range(3):
        t0 = time.perf_counter()
        subprocess.run([sys.executable, "-c", "import " + name], check=True)
        best = min(best, time.perf_counter() - t0)
    res["t_import_" + name] = best
print(json.dumps(res))''', env="venv")

LAB_SOL = '''import matplotlib
import numpy
import pandas
import pytest

print("matplotlib", matplotlib.__version__.split(".")[0])
print("numpy", numpy.__version__.split(".")[0])
print("pandas", pandas.__version__.split(".")[0])
print("pytest", pytest.__version__.split(".")[0])'''
LAB_OUT = "matplotlib 3\nnumpy 2\npandas 3\npytest 9"
P_LAB = py("lab_l08", LAB_SOL, LAB_OUT, env="venv")


def shown_sec(txt):
    """Giây ứng với chữ t_show đã hiện trên màn hình ('≈ 2 s' -> 2)."""
    v, u = txt[2:].split()
    return float(v) * {"ns": 1e-9, "µs": 1e-6, "ms": 1e-3, "s": 1, "phút": 60, "giờ": 3600, "ngày": 86400}[u]


def x_k(x, k):
    """Ngoại suy từ số ĐÃ LÀM TRÒN hiện trên màn hình (bảng khớp phép nhân: 2 s x 100 = 3 phút, không phải 4 phút)."""
    return t_show(shown_sec(t_show(x)[0]) * k)


def build():
    ti = {k: M("l08_import", "t_import_" + k) for k in ("json", "numpy", "pandas", "matplotlib", "pytest")}
    si = {k: t_show(v) for k, v in ti.items()}
    s100 = x_k(ti["pandas"], 100)
    npk = {k: int(M("l08_pkgs", "n_" + k)) for k in ("numpy", "pandas", "mpl", "all")}
    assert npk["all"] in (17, 1), npk
    sc_hook = sc("hook", "hook", "Chạy được trên máy tôi, hỏng trên máy bạn: vì phiên bản thư viện", [
        st(table(["người", "cài thư viện", "kết quả"],
                 [["An (tháng 3)", "pandas bản mới nhất lúc đó", "chương trình chạy đúng"], ["Bình (tháng 9)", "pandas bản mới nhất lúc đó", "cùng chương trình, in số khác hoặc báo lỗi"]])
           + "<p>Hai người cùng mã, khác <b>phiên bản thư viện</b>: một số hàm đổi hành vi giữa các phiên bản. Không ai sửa mã, nhưng kết quả đã đổi.</p>",
           """Chào bạn, hai đồng nghiệp cùng chạy một chương trình. An cài thư viện vào tháng ba, Bình cài vào tháng chín. Không ai sửa một dòng mã, nhưng chương trình của An chạy đúng còn của Bình in số khác hoặc báo lỗi.
           Hôm nay ta học cách chia chương trình thành nhiều tệp, và cách cố định môi trường để chạy ở đâu cũng giống nhau."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Chia chương trình thành <b>mô-đun</b> và <b>gói</b> thế nào, và dòng kiểm tra <b>tên mô-đun</b> để làm gì?</li>
<li><b>Môi trường ảo</b> là gì, và vì sao mỗi dự án nên có một cái riêng?</li>
<li><b>Ghim phiên bản</b> trong tệp danh sách thư viện để người khác cài giống hệt ra sao?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Một, chia chương trình thành mô-đun và gói thế nào, và dòng kiểm tra tên mô-đun để làm gì. Hai, môi trường ảo là gì, và vì sao mỗi dự án nên có một cái riêng. Ba, ghim phiên bản trong tệp danh sách thư viện để người khác cài giống hệt ra sao."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: hàm, tệp, và thư mục chứa chương trình", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① hàm", "gói một việc, nhận tham số, trả về; ta đã dùng <code>import re</code>, <code>import json</code> để mang bộ công cụ có sẵn vào"],
                  ["② tệp và thư mục", "tệp <code>chay.py</code> nằm trong một thư mục; đường dẫn ghép bằng <code>/</code>"],
                  ["③ biến PATH", "máy tìm chương trình <code>python</code> theo danh sách thư mục trong <code>PATH</code>; thứ tự quyết định cái nào thắng"]]),
           """Ta ôn lại ba điều. Hàm gói một việc, và ta đã dùng lệnh nạp để mang các bộ công cụ có sẵn vào chương trình. Tệp nằm trong thư mục, và đường dẫn ghép bằng dấu gạch chéo. Và biến tìm đường cho biết máy tìm một chương trình ở những thư mục nào, thứ tự quyết định cái nào thắng.""",
           focus=[1, "1.2", "1.3", "1.4"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã mô-đun, gói, lệnh nạp, tên mô-đun, lệnh cửa sổ lệnh và môi trường ảo", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["tệp <code>giao_dich.py</code>", "mô-đun", "<b>một tệp</b> mã; tên mô-đun là tên tệp bỏ đuôi <code>.py</code>"],
                  ["thư mục có <code>__init__.py</code>", "gói", "<b>một thư mục</b> các mô-đun; tệp <code>__init__.py</code> (có thể rỗng) đánh dấu nó là gói"],
                  ["<code>import x</code>, <code>from x import f</code>, <code>import x as y</code>", "ba cách nạp", "mang cả <code>x</code>; chỉ lấy <code>f</code>; đặt tên ngắn <code>y</code> cho <code>x</code>"],
                  ["<code>if __name__ == \"__main__\":</code>", "chỉ khi chạy trực tiếp", "<code>__name__</code> là <code>\"__main__\"</code> khi chạy tệp bằng <code>python tệp.py</code>, còn là <b>tên mô-đun</b> khi tệp bị nạp"]]),
           """Bảng đầu là cách chia chương trình. Một tệp mã là một mô-đun, tên mô-đun là tên tệp bỏ đuôi. Một thư mục chứa các mô-đun và một tệp đánh dấu đặc biệt là một gói. Có ba cách nạp, nạp cả mô-đun, chỉ lấy một thứ, hoặc đặt tên ngắn.
           Biến tên mô-đun nhận một chữ đặc biệt khi tệp chạy trực tiếp, và nhận tên mô-đun khi tệp bị nạp. Nên dòng kiểm tra nó cho tệp vừa là chương trình vừa là thư viện.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.5"]),
        st(table(["viết (trong Git Bash)", "đọc là", "nghĩa"],
                 [["<code>ls ngan_hang</code>", "liệt kê", "in tên các tệp trong thư mục <code>ngan_hang</code>"],
                  ["<code>grep pandas requirements.txt</code>", "lọc dòng", "in các dòng của tệp có chứa chữ <code>pandas</code>"],
                  ["<code>wc -l requirements.txt</code>", "đếm dòng", "in số dòng của tệp (<code>-l</code>: lines, dòng)"],
                  ["<code>mv csv.py csv_cua_toi.py</code>", "đổi tên", "đổi tên tệp (cũng dùng để chuyển tệp sang thư mục khác)"],
                  ["<code>lệnh1 | lệnh2</code>", "nối ống", "kết quả của lệnh trước thành đầu vào của lệnh sau; <code>tail -n 1</code> giữ dòng cuối, <code>cut -c1-58</code> giữ 58 ký tự đầu"],
                  ["<code>2&gt;&amp;1</code>", "gộp lỗi", "đưa thông báo lỗi chung dòng với kết quả thường, để lọc được cả hai"],
                  ["<code>python -m tên</code>", "chạy mô-đun", "<code>-m</code> chạy một mô-đun có sẵn theo tên: <code>python -m venv .venv</code> chạy mô-đun <code>venv</code>"]]),
           """Bảng thứ hai là các lệnh của cửa sổ lệnh. Lệnh liệt kê in tên các tệp trong một thư mục. Lệnh lọc in những dòng của tệp có chứa chữ cho trước. Lệnh đếm dòng in số dòng của tệp. Lệnh di chuyển ở đây dùng để đổi tên tệp. Dấu gạch đứng nối hai lệnh, kết quả của lệnh trước thành đầu vào của lệnh sau.
           Hai lớn hơn một gộp thông báo lỗi chung với kết quả thường, để lọc được cả hai. Cuối cùng, cờ chữ m bảo ngôn ngữ chạy một mô-đun có sẵn theo tên.""", clear=True, introduces=["pyt_cut"]),
        st(table(["viết (trong Git Bash)", "đọc là", "nghĩa"],
                 [["<code>python -m venv .venv</code>", "tạo môi trường ảo", "dựng thư mục <code>.venv</code>: <b>một bản Python riêng</b> cùng nơi chứa thư viện riêng"],
                  ["<code>source .venv/Scripts/activate</code>", "kích hoạt", "trong cửa sổ này, <code>python</code> và <code>pip</code> là của <code>.venv</code> (Windows; trên macOS và Linux: <code>.venv/bin/activate</code>)"],
                  ["<code>pip install -r requirements.txt</code>", "cài theo danh sách", "<code>pip</code> là chương trình tải thư viện của người khác từ kho chung trên mạng (PyPI) về cài; lệnh này cài mọi thư viện ghi trong tệp; <code>numpy==2.4.6</code> là <b>ghim</b>: đúng phiên bản đó"],
                  ["<code>pip freeze</code>", "liệt kê đã cài", "in mọi thư viện đang cài, kèm phiên bản, đúng dạng của <code>requirements.txt</code>"]]),
           """Bảng thứ ba là môi trường ảo. Lệnh tạo dựng một thư mục chứa một bản ngôn ngữ riêng cùng nơi chứa thư viện riêng. Lệnh kích hoạt làm cho trong cửa sổ này, lệnh chạy và lệnh cài đều là của môi trường đó. Công cụ cài đặt là chương trình tải thư viện của người khác từ một kho chung trên mạng. Lệnh cài theo danh sách cài mọi thư viện trong tệp, và dấu hai bằng ghim đúng phiên bản.
           Lệnh liệt kê in những gì đang cài, đúng dạng của tệp danh sách.""",
           focus=[1, "1.2", "1.3", "1.4", "1.4", "1.5"], clear=True, introduces=["pyt_pip"]),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: thứ tự tìm mô-đun, và mỗi dự án một hộp riêng", [
        st(svg(1500, 430,
               box(30, 50, 300, 80, ["import giao_dich"], C_BLUE, 26, True),
               txt(450, 40, "máy tìm lần lượt theo danh sách:", 26, "start", "#1f2937", True),
               box(430, 60, 430, 70, ["1. thư mục của tệp đang chạy"], C_GREEN, 23, True),
               box(430, 145, 430, 70, ["2. bộ công cụ có sẵn của Python"], C_AMBER, 23),
               box(430, 230, 430, 70, ["3. thư viện đã cài bằng pip", "(thư mục site-packages)"], C_AMBER, 22),
               arrow(335, 90, 425, 95, "#2a78d6"),
               txt(1150, 100, "thấy tên khớp ĐẦU TIÊN là dùng ngay,", 26, "middle", "#dc2626", True),
               txt(1150, 140, "không xét tiếp", 26, "middle", "#dc2626", True),
               txt(1150, 220, "tệp csv.py của bạn nằm ở mục 1", 26, "middle", "#1f2937"),
               txt(1150, 260, "nên che mất bộ csv có sẵn ở mục 2", 26, "middle", "#1f2937"),
               txt(750, 350, "đặt tên tệp trùng tên bộ công cụ có sẵn viết bằng Python là lỗi gây khó hiểu: tránh csv.py, json.py, random.py, test.py", 22, "middle", "#6b7280"),
               txt(750, 390, "(trên Windows với Python cài từ python.org: sys, time, math không bị che; hệ khác có thể bị che, nên cứ tránh tên trùng)", 22, "middle", "#6b7280")),
           """Hình này cho thấy máy tìm mô-đun thế nào. Khi gặp lệnh nạp, máy tìm lần lượt theo một danh sách. Đầu tiên là thư mục của tệp đang chạy, rồi tới bộ công cụ có sẵn, rồi tới thư viện đã cài bằng công cụ cài đặt, nằm trong một thư mục tên đặc biệt. Thấy tên khớp đầu tiên là dùng ngay, không xét tiếp.
           Nếu bạn đặt tên tệp của mình trùng với một bộ công cụ có sẵn viết bằng Python, như bộ đọc bảng, tệp của bạn nằm ở mục đầu nên che mất bộ có sẵn. Trên bản cài chuẩn đã kiểm, vài bộ lõi như thời gian và toán không bị che, nhưng máy khác có thể che, nên cứ tránh tên trùng.""", introduces=["pyt_site_packages"]),
        st(svg(1500, 400,
               box(30, 40, 430, 320, ["", "", ""], C_GRAY),
               txt(245, 80, "Python hệ thống", 26, "middle", "#1f2937", True),
               txt(245, 130, "dùng chung cho mọi dự án", 24, "middle", "#6b7280"),
               box(60, 160, 370, 70, ["numpy 1.26 (cho dự án A)"], C_AMBER, 24),
               box(60, 250, 370, 70, ["numpy 2.4 (cho dự án B)?"], C_RED, 24, True),
               txt(245, 337, "hai bản numpy không ở chung được", 24, "middle", "#dc2626", True),
               box(560, 40, 400, 320, ["", "", ""], C_GRAY),
               txt(760, 80, "dự án A: .venv riêng", 26, "middle", "#1f2937", True),
               box(590, 130, 340, 70, ["numpy 1.26"], C_GREEN, 24, True),
               box(590, 220, 340, 70, ["pandas bản cũ"], C_GREEN, 24),
               box(1000, 40, 440, 320, ["", "", ""], C_GRAY),
               txt(1220, 80, "dự án B: .venv riêng", 26, "middle", "#1f2937", True),
               box(1030, 130, 380, 70, ["numpy 2.4.6"], C_GREEN, 24, True),
               box(1030, 220, 380, 70, ["pandas 3.1.1"], C_GREEN, 24),
               txt(1220, 330, "mỗi dự án một hộp: không đụng nhau", 22, "middle", "#16a34a", True)),
           """Hình thứ hai là môi trường ảo. Nếu mọi dự án dùng chung một bản ngôn ngữ, hai dự án cần hai phiên bản khác nhau của cùng một thư viện sẽ không ở chung được. Môi trường ảo cho mỗi dự án một hộp riêng. Trong mỗi hộp, cài, xoá và nâng cấp không ảnh hưởng dự án khác.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: tên mô-đun, gói, môi trường ảo, ghim phiên bản", [
        st(raw_block(MOD_GD.strip().split("\n"), title="Bước 1. Tệp giao_dich.py: một hàm, và khối kiểm tên mô-đun", py_hl=True)
           + "<p>Dòng đầu tiên in tên mô-đun hiện tại <code>__name__</code>; khối <code>if</code> ở cuối chỉ chạy khi tệp này được chạy trực tiếp.</p>",
           """Bước một, tên mô-đun. Đây là tệp giao dịch, gồm một hàm cộng danh sách. Vì ta cần biết tệp đang được chạy trực tiếp hay bị nạp, dòng in đầu tiên cho thấy giá trị của biến tên mô-đun. Khối kiểm ở cuối chỉ chạy khi chính tệp này được chạy trực tiếp."""),
        st(raw_block(MOD_CHAY.strip().split("\n"), title="Tệp chay.py nạp giao_dich.py", py_hl=True)
           + term_block(SH_MOD, title="Cùng một tệp, hai cách chạy, hai giá trị __name__")
           + "<p>Vì khi chạy trực tiếp <code>__name__</code> là <code>\"__main__\"</code>, khối tự kiểm chạy; khi <b>bị nạp</b> nó là <code>\"giao_dich\"</code> nên khối đó <b>không</b> chạy, và <code>chay.py</code> chỉ nhận hàm.</p>",
           """Cùng một tệp, chạy trực tiếp thì biến tên nhận chữ đặc biệt đó, nên khối tự kiểm chạy và in ba trăm. Khi tệp chay nạp nó, biến tên bằng tên mô-đun, nên khối tự kiểm không chạy, và tệp gọi chỉ nhận hàm để dùng, in bảy trăm năm mươi nghìn. Nhờ vậy một tệp vừa là chương trình vừa là thư viện.""", clear=True),
        st(raw_block(PKG_PHI.strip().split("\n"), title="Bước 2. Gói ngan_hang: tệp ngan_hang/phi.py", py_hl=True)
           + raw_block(PKG_CHAY.strip().split("\n"), title="Tệp chay_goi.py nạp hàm từ gói", py_hl=True),
           """Bước hai, ta gói các tệp liên quan vào một thư mục chung gọi là gói. Thư mục ngân hàng chứa một mô-đun tính phí chuyển. Phí bằng số tiền chia một nghìn, nhưng thấp nhất là một nghìn một trăm. Tệp chạy nạp hàm đó từ bên trong gói, theo hai cách, và in vài phí thử.""", clear=True),
        st(term_block(SH_PKG, title="Thư mục có __init__.py (tệp rỗng) là gói; nạp bằng dấu chấm")
           + "<p>Tệp <code>__init__.py</code> (có thể rỗng) đánh dấu rõ thư mục là <b>gói</b>; từ Python $3.3$ thiếu nó vẫn nạp được, nhưng nên có. Dấu chấm đi vào bên trong: <code>ngan_hang.phi</code>. Phí chuyển $500\\,000$ chia $1000$ chỉ được $500$, thấp hơn mức tối thiểu, nên lấy $1\\,100$.</p>",
           """Tệp đánh dấu đặc biệt, có thể rỗng, cho biết rõ thư mục là gói. Từ phiên bản ba chấm ba, thiếu tệp này máy vẫn nạp được, nhưng nên có để ý định rõ ràng. Dấu chấm đi vào bên trong gói. Phí chuyển năm trăm nghìn chia một nghìn bằng năm trăm, thấp hơn mức tối thiểu, nên phí là một nghìn một trăm.""", clear=True),
        st(term_block(SH_VENV, 0, 4, title="Bước 3. Môi trường ảo là một bản Python riêng, chưa có thư viện nào")
           + "<p>Vì <code>python -m venv .venv</code> dựng bản riêng, <code>sys.prefix</code> (thư mục của bản đang chạy) của nó <b>khác</b> <code>sys.base_prefix</code> (thư mục của Python hệ thống): <code>True</code>; Python hệ thống thì hai thư mục trùng nhau (<code>False</code>). <code>python -c \"…\"</code> chạy ngay một dòng mã đặt trong ngoặc kép, không cần tệp; trong đó dấu <code>;</code> ngăn hai câu lệnh trên một dòng, <code>!=</code> là “khác”. Bản mới <b>chưa có</b> <code>numpy</code>: phải cài vào.</p>",
           """Bước ba, môi trường ảo. Sau khi tạo, ta hỏi hai bản bằng cách chạy ngay một dòng mã đặt trong ngoặc kép, không cần tệp. Dấu chấm phẩy ngăn hai câu lệnh trên một dòng, và dòng đó so thư mục của bản đang chạy với thư mục của Python hệ thống. Bản hệ thống cho sai, vì hai thư mục trùng nhau, nên nó không phải môi trường ảo. Bản trong thư mục mới cho đúng. Và bản mới chưa có thư viện tính trên mảng nào, nên nạp nó báo lỗi không tìm thấy.""", clear=True, introduces=["pyt_sys_prefix"]),
        st(term_block(SH_REQ, title="Bước 4. Ghim phiên bản: tệp danh sách là công thức tái tạo môi trường")
           + f"<p>Vì mỗi dòng <code>tên==phiên_bản</code> chốt <b>đúng một phiên bản</b>, ai cài từ tệp này cũng được cùng bộ. Bốn thư viện ta cần kéo theo {NREQ - 4} thư viện khác: tệp có ${NREQ}$ dòng. Lệnh <code>pip freeze</code> in đúng dạng này cho mọi thư viện đang cài, nên dùng nó để sinh tệp.</p>",
           f"""Bước bốn, ghim phiên bản. Mỗi dòng ghi tên và đúng một phiên bản, nên ai cài từ tệp này cũng được cùng một bộ. Ở đây hai thư viện chính có phiên bản cố định. Tệp có {words(NREQ)} dòng, nghĩa là bốn thư viện ta cần kéo theo mười ba thư viện khác. Lệnh liệt kê các thư viện đang cài in đúng dạng này, nên ta dùng nó để sinh tệp."""),
    ], checks=[f"{NREQ} - 4 == {NREQ - 4}", "500000 // 1000 == 500 and 500 < 1100", "5000000 // 1000 == 5000 and 2000000 // 1000 == 2000"])
    sc_ex = sc("example", "example", "Ví dụ: chia dự án thành mô-đun, kích hoạt môi trường, cài từ danh sách", [
        st(term_block(SH_ACT, title="Kích hoạt môi trường ảo trong Git Bash")
           + "<p>Sau <code>source .venv/Scripts/activate</code>, lệnh <code>python</code> trong cửa sổ này là bản của <code>.venv</code> (<code>True</code>). Dấu nhắc thường hiện thêm <code>(.venv)</code> ở đầu dòng. <code>A &amp;&amp; B</code>: chạy <code>A</code>, <b>chỉ khi A thành công</b> (mã thoát $0$) mới chạy <code>B</code>.</p>",
           """Ví dụ một, kích hoạt. Tạo môi trường rồi dùng lệnh kích hoạt trong cửa sổ lệnh. Hai dấu và nối hai lệnh: lệnh sau chỉ chạy nếu lệnh trước thành công. Từ đó lệnh chạy trong cửa sổ này là bản của môi trường, và máy trả lời đúng."""),
        st('<div class="code"><div><span class="cm"><span>&#36;</span> </span>source .venv/Scripts/activate</div><div><span class="cm"><span>&#36;</span> </span>pip install -r requirements.txt</div>'
           '<div><span class="cm"><span>&#36;</span> </span>python chay.py</div></div>'
           "<p>Ba lệnh dựng lại môi trường từ tệp danh sách ở máy mới (bước cài cần mạng nên video không chạy; kết quả bạn sẽ kiểm bằng bài tự làm).</p>",
           """Ví dụ hai, dựng môi trường ở máy mới. Kích hoạt môi trường, cài theo tệp danh sách, rồi chạy chương trình. Bước cài cần mạng nên video không chạy, bạn sẽ kiểm nó trong bài tự làm.""", clear=True),
        st(code_block(P_MAIN, title="Tệp khong_guard.py: hàm cộng, và một dòng in thử ở ngoài cùng"),
           """Ví dụ ba, hậu quả khi quên khối kiểm tên mô-đun. Tệp này có hàm cộng và một dòng in thử ở ngoài cùng, không nằm trong khối kiểm.""", clear=True),
        st(term_block(SH_IMP, title="Quên khối kiểm tên mô-đun: nạp là chạy luôn")
           + "<p>Tệp không có <code>if __name__ == \"__main__\":</code> nên <b>mọi dòng chạy ngay khi bị nạp</b>, kể cả dòng in thử. Gói mã thử vào khối kiểm tên mô-đun.</p>",
           """Chỉ nạp tệp đó vào từ nơi khác mà dòng in thử cũng chạy. Hãy gói mã thử vào khối kiểm tên mô-đun.""", clear=True),
        st(raw_block(["# tep tu viet, vo tinh trung ten voi bo csv co san"], title="Tệp csv.py: do ta tự viết, vô tình trùng tên", py_hl=True)
           + raw_block(["import csv", "", "print(csv.DictReader)"], title="Tệp chay.py: nạp bộ csv có sẵn rồi in lớp đọc bảng", py_hl=True),
           """Ví dụ bốn, trùng tên. Trong thư mục có hai tệp. Tệp thứ nhất do ta tự viết, tình cờ mang đúng tên của bộ đọc bảng có sẵn. Tệp thứ hai nạp bộ đọc bảng rồi in tên lớp đọc.""", clear=True),
        st(term_block(SH_SHADOW, 0, 3, title="Tệp tên csv.py che mất bộ csv có sẵn; đổi tên là hết")
           + "<p>Đọc dòng cuối: mô-đun <code>csv</code> không có <code>DictReader</code>, vì máy nạp <b>tệp của bạn</b>. Đổi tên tệp, bộ có sẵn trở lại. Lệnh đầu lấy dòng cuối của thông báo (<code>tail -n 1</code>) rồi chỉ giữ $58$ ký tự đầu (<code>cut -c1-58</code>): từ Python $3.13$ dòng đó còn dài thêm gợi ý đổi tên tệp.</p>",
           """Ta chạy chương trình. Máy nạp tệp của ta nên báo mô-đun không có lớp đọc bảng. Lệnh đầu giữ năm mươi tám ký tự đầu của dòng cuối, vì từ phiên bản ba chấm mười ba dòng này dài thêm gợi ý. Đổi tên tệp của mình, bộ có sẵn trở lại và lớp được tìm thấy.""", clear=True),
    ], checks=["1100 > 500"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: hai cách xác nhận đang ở môi trường ảo", [
        st(term_block(SH_VENV, 1, 3, title="Cách 1: hỏi sys.prefix") + "<p>Cách 2: dùng đường dẫn đầy đủ tới <code>.venv/Scripts/python</code> thay vì kích hoạt. Cả hai phải cho cùng câu trả lời: bản hệ thống <code>False</code>, bản trong <code>.venv</code> <code>True</code>.</p>",
           """Đường kiểm khác. Cách một là hỏi giá trị tiền tố của bản chạy, so với tiền tố gốc. Cách hai là gọi thẳng bản trong thư mục môi trường bằng đường dẫn đầy đủ thay vì kích hoạt. Cả hai cách phải cho cùng câu trả lời, bản hệ thống sai và bản trong môi trường đúng."""),
    ], checks=["True != False"])
    sc_scale = sc("scale", "concept", "Khi dự án lớn dần: thư viện kéo theo thư viện, mỗi cái tốn thời gian", [
        st(table(["nhóm thư viện mình nhập", "tổng số thư viện phải cài (cộng dồn, kể cả thư viện kéo theo)", "thời gian nạp RIÊNG thư viện đó (đo trên máy kiểm, số minh hoạ)"],
                 [["chỉ bộ có sẵn", "0", si["json"][0]], ["thư viện tính trên mảng", str(npk["numpy"]), si["numpy"][0]],
                  ["thêm thư viện bảng dữ liệu (kéo theo thư viện mảng và hai thư viện ngày giờ)", str(npk["pandas"]), si["pandas"][0]],
                  ["thêm thư viện vẽ biểu đồ", str(npk["mpl"]), si["matplotlib"][0]], ["thêm thư viện kiểm thử", str(npk["all"]), si["pytest"][0]]])
           + "<p class='note'>Cột thời gian đo từng thư viện nạp một mình, không cộng dồn (thư viện bảng dữ liệu đã nạp luôn thư viện mảng).</p>",
           f"""Bảng này cho thấy quy mô. Cột giữa là tổng số thư viện phải cài, cộng dồn từ trên xuống. Thư viện tính trên mảng đứng một mình. Thêm thư viện bảng dữ liệu, tổng thành {words(npk['pandas'])}. Thêm thư viện vẽ biểu đồ, tổng thành {words(npk['mpl'])}. Thêm thư viện kiểm thử, tổng thành {words(npk['all'])}, đúng số dòng trong tệp ghim.
           Cột bên phải là thời gian nạp riêng từng thư viện. Chỉ dùng bộ có sẵn mất {si['json'][1]}. Thư viện tính trên mảng mất {si['numpy'][1]}, thư viện bảng dữ liệu mất {si['pandas'][1]}. Thư viện vẽ biểu đồ mất {si['matplotlib'][1]}, thư viện kiểm thử mất {si['pytest'][1]}. Số đo trên máy kiểm, số minh hoạ."""),
        st("<div class='box key'><b>Đánh đổi:</b> mỗi thư viện thêm vào là <b>mã của người khác</b> chạy trong chương trình của bạn: tốn thời gian khởi động, tốn dung lượng, và là một rủi ro an toàn. "
           f"Một chương trình nhỏ chạy {{100}} lần mỗi ngày với pandas mất thêm {s100[0]} chỉ để khởi động. Người làm nghề <b>ghim phiên bản</b>, <b>chỉ cài thứ cần</b>, và cập nhật có kiểm soát.</div>".replace("{100}", "100"),
           f"""Đánh đổi là mỗi thư viện thêm vào là mã của người khác chạy trong chương trình của bạn. Nó tốn thời gian khởi động, tốn dung lượng, và là một rủi ro an toàn. Một chương trình nhỏ chạy một trăm lần mỗi ngày với thư viện bảng dữ liệu mất thêm {s100[1]} chỉ để khởi động. Người làm nghề ghim phiên bản, chỉ cài thứ cần, và cập nhật có kiểm soát.""", clear=True),
    ], checks=[f"{NREQ} == 4 + 13", "4 * 25 // 100 == 1"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Đặt tên tệp trùng bộ công cụ có sẵn (<code>csv.py</code>, <code>random.py</code>, <code>json.py</code>).</div>'
           + term_block(SH_SHADOW, 0, 1) + "<p>Lỗi nói “không có thuộc tính” dù bạn nạp đúng tên: <b>máy nạp tệp của bạn</b>. Phép thử: <code>print(csv.__file__)</code> cho thấy tệp nào được nạp.</p>",
           """Lỗi thứ nhất, của người mới, là đặt tên tệp trùng bộ công cụ có sẵn. Thông báo nói không có thuộc tính dù bạn nạp đúng tên, vì máy nạp tệp của bạn. Phép thử là in đường dẫn tệp của mô-đun, cho thấy tệp nào đã được nạp."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Quên kích hoạt môi trường rồi cài thư viện: cài nhầm vào Python hệ thống.</div>'
           + term_block(SH_VENV, 1, 3) + "<p>Phép thử: trước khi <code>pip install</code>, hỏi <code>sys.prefix != sys.base_prefix</code>; nếu <code>False</code> thì <b>chưa</b> ở trong môi trường ảo. Cài nhầm làm các dự án khác đổi phiên bản mà không ai hay.</p>",
           """Lỗi thứ hai, của người đã đi làm, là quên kích hoạt môi trường rồi cài thư viện, nên cài nhầm vào bản hệ thống. Cách phòng là hỏi trước khi cài. Nếu câu trả lời là sai thì chưa ở trong môi trường ảo. Cài nhầm làm các dự án khác đổi phiên bản mà không ai biết.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Không ghim phiên bản, hoặc ghim lỏng (<code>pandas&gt;=2</code>).</div>'
           + "<p>Mỗi lần cài có thể được bộ <b>khác</b>: kết quả hôm nay và tháng sau lệch nhau. Ghim <code>==</code> cho dự án chạy thật; sinh tệp bằng <code>pip freeze</code>; nâng phiên bản <b>có chủ ý</b>, chạy lại kiểm thử rồi mới chốt.</p>",
           """Lỗi thứ ba, của người đã đi làm, là không ghim phiên bản, hoặc ghim lỏng. Mỗi lần cài có thể được một bộ khác, nên kết quả hôm nay và tháng sau lệch nhau. Hãy ghim đúng phiên bản cho dự án chạy thật, sinh tệp bằng lệnh liệt kê, và nâng phiên bản có chủ ý, chạy lại kiểm thử rồi mới chốt.""", clear=True),
    ], checks=["True"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Tệp <code>phi.py</code> có <code>print("nap xong")</code> ở ngoài cùng, và <code>chay.py</code> có <code>import phi</code>.</p>
<ol><li>Chạy <code>python chay.py</code>: dòng <code>nap xong</code> có hiện không? Vì sao?</li>
<li>Muốn dòng đó chỉ hiện khi chạy <code>python phi.py</code>, sửa thế nào?</li></ol>
<p><b>Quyết định:</b> hai dự án cần <code>numpy</code> bản cũ và bản mới: một môi trường chung hay hai môi trường riêng? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Tệp phí có một dòng in ở ngoài cùng, và tệp chạy nạp tệp phí. Câu một, chạy tệp chạy thì dòng in có hiện không, và vì sao. Câu hai, muốn dòng đó chỉ hiện khi chạy trực tiếp tệp phí thì sửa thế nào.
           Sau đó là một quyết định, hai dự án cần hai phiên bản khác nhau của thư viện tính trên mảng, dùng một môi trường chung hay hai môi trường riêng, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(table(["câu", "đáp án"], [["1", "<b>có</b>: nạp một mô-đun là chạy mọi dòng ngoài cùng của nó"], ["2", "đặt dòng in vào <code>if __name__ == \"__main__\":</code>, vì khi bị nạp, <code>__name__</code> là <code>\"phi\"</code> nên khối đó bị bỏ qua"]]),
           """Đáp án như sau. Câu một, có hiện, vì nạp một mô-đun là chạy mọi dòng ngoài cùng của nó. Câu hai, đặt dòng in vào khối kiểm tên mô-đun. Khi bị nạp, tên là tên mô-đun nên khối đó bị bỏ qua."""),
        st("<div class='box key'><b>Quyết định:</b> <b>hai môi trường riêng</b>. Một bản Python chỉ giữ được một phiên bản mỗi thư viện, nên hai dự án cần hai bản khác nhau không ở chung được. "
           "Mỗi dự án một môi trường, kèm tệp danh sách đã ghim, là thông lệ của người làm nghề: chi phí chỉ là vài trăm megabyte đĩa.</div>",
           """Quyết định, hai môi trường riêng. Một bản ngôn ngữ chỉ giữ được một phiên bản mỗi thư viện, nên hai dự án cần hai bản khác nhau không ở chung được. Mỗi dự án một môi trường, kèm tệp danh sách đã ghim, là thông lệ của người làm nghề.""", clear=True),
    ], checks=["True"])
    sc_prac = practice_scene(sc, "Tự làm: tạo môi trường ảo, cài từ danh sách, in phiên bản", pr_steps(
        st, "PYT", "L08",
        """<p><b>Đề</b> (làm trong Git Bash, ở thư mục gốc của bộ khoá: <code>pwd</code> rồi <code>ls</code> phải thấy <code>labs/</code>; chưa đúng thì <code>cd</code> tới đó, hoặc mở lại bằng <i>Open Git Bash here</i>, như bài 0):</p>
<ol><li><code>python -m venv .venv-hoc</code>, rồi <code>source .venv-hoc/Scripts/activate</code>;</li>
<li><code>pip install -r labs/requirements-py.txt</code> (cần mạng, vài phút);</li>
<li>tạo <code>in_phien_ban.py</code>: nạp <code>matplotlib, numpy, pandas, pytest</code>, in bốn dòng <code>tên số_chính</code> (số đứng trước dấu chấm đầu của <code>__version__</code>), <b>theo thứ tự chữ cái</b>;</li>
<li>chạy trong môi trường vừa tạo và <b>đối chiếu</b> với các dòng <code>==</code> trong <code>labs/requirements-py.txt</code>.</li></ol>""",
        """Bây giờ tới phần bạn tự làm, làm trong cửa sổ lệnh tại thư mục gốc của bộ khoá, nơi lệnh liệt kê phải thấy thư mục thực hành. Chưa đúng thì đổi thư mục tới đó. Một, tạo một môi trường ảo và kích hoạt nó. Hai, cài theo tệp danh sách của khoá, bước này cần mạng và mất vài phút. Ba, viết một tệp nạp bốn thư viện chính và in tên cùng phiên bản của từng cái, theo thứ tự chữ cái. Bốn, chạy trong môi trường vừa tạo và đối chiếu với các dòng ghim trong tệp danh sách.
        Hãy dừng video và làm.""",
        LAB_OUT, "in_phien_ban.py",
        """<div class="box key"><b>Nếu kẹt:</b> <code>import numpy</code> rồi <code>print("numpy", numpy.__version__.split(".")[0])</code>; mỗi thư viện một dòng. Nếu báo <code>ModuleNotFoundError</code>: chưa kích hoạt môi trường hoặc chưa cài xong. Chấm bằng máy: <code>bash labs/cham.sh PYT L08 in_phien_ban.py</code> chạy trong môi trường có sẵn thư viện.
Lời giải ở <code>labs/PYT/L08/loi_giai.py</code>.</div>""",
        """Nếu kẹt, nạp từng thư viện rồi in tên cùng phiên bản của nó. Nếu máy báo không tìm thấy mô-đun thì chưa kích hoạt môi trường hoặc chưa cài xong. Có thể chấm bằng máy trong môi trường đã cài thư viện.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=420), "PYT", "L08")
    write_lab("PYT", "L08", """# Lab PYT L08 — Tạo môi trường ảo, cài từ danh sách, in phiên bản

**cần: mạng (bước cài), Python 3.11 trở lên.** Làm trong Git Bash, tại thư mục gốc của bộ khoá (nơi có thư mục `labs`: gõ `pwd` rồi `ls` để kiểm; chưa đúng thì `cd` tới đó, hoặc mở lại bằng *Open Git Bash here*, như bài 0). Lưu ý: `python -m venv .venv-hoc` **tạo thư mục mới `.venv-hoc`** ngay trong thư mục bạn đang đứng (xoá thư mục này là xoá môi trường, không hại gì khác); `pip install` **tải thư viện từ mạng** (PyPI), mất vài phút và có thể in nhiều dòng; không có mạng thì lệnh này báo lỗi, hãy nối mạng rồi chạy lại. Lệnh `-m` chạy một mô-đun có sẵn theo tên (`venv` là mô-đun tạo môi trường ảo):

```bash
python -m venv .venv-hoc
source .venv-hoc/Scripts/activate          # macOS/Linux: source .venv-hoc/bin/activate
pip install -r labs/requirements-py.txt
```

Tạo `in_phien_ban.py`: nạp `matplotlib`, `numpy`, `pandas`, `pytest` và in **bốn dòng** `<tên> <số chính>` (số đứng trước dấu chấm đầu của `<tên>.__version__`), theo thứ tự chữ cái. Chạy `python in_phien_ban.py` trong môi trường vừa tạo và **đối chiếu** từng dòng với các dòng `==` của `labs/requirements-py.txt`.

Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L08 in_phien_ban.py` (máy chấm của khoá dùng môi trường đã cài sẵn các thư viện này).
""", "py", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("tệp = mô-đun; thư mục có __init__.py = gói", "máy tìm mô-đun theo danh sách; tên trùng bộ viết bằng Python thì che", "if __name__ == \"__main__\": vừa chạy được vừa nạp được",
                 "mỗi dự án một môi trường ảo", "requirements.txt ghim phiên bản bằng ==", "mỗi thư viện thêm vào là mã của người khác"),
           """Tổng kết chuỗi logic. Tệp là mô-đun, thư mục có tệp đánh dấu là gói. Máy tìm mô-đun theo một danh sách, và tên trùng thì che. Khối kiểm tên mô-đun cho tệp vừa chạy được vừa nạp được. Mỗi dự án một môi trường ảo.
           Tệp danh sách ghim phiên bản bằng dấu hai bằng. Và mỗi thư viện thêm vào là mã của người khác chạy trong chương trình của bạn."""),
        st("""<div class='box key'><b>Tư duy:</b> chương trình của bạn gồm <b>mã của bạn và môi trường nó chạy</b>. Ghi lại cả hai: mô-đun nhỏ, rõ; môi trường dựng lại được từ một tệp. “Chạy được trên máy tôi” chưa phải là xong.</div>
<p>Bài sau: thư viện tính trên mảng, để tính trên triệu số trong một lệnh thay vì một vòng lặp.</p>""",
           """Điều cần mang theo, chương trình của bạn gồm mã của bạn và môi trường nó chạy. Hãy ghi lại cả hai, mô-đun nhỏ và rõ, môi trường dựng lại được từ một tệp. Chạy được trên máy tôi chưa phải là xong.
           Bài sau, ta học thư viện tính trên mảng, để tính trên triệu số trong một lệnh thay vì một vòng lặp.""", forward_ref=True),
    ])
    return lesson("L08", "mo_dun_goi_moi_truong_ao", "Bài 8 — Mô-đun, gói và môi trường ảo",
                  "curriculum/pyt.yaml L08; audit/pyt/verify_pyt.py L08 (Git Bash chạy thật trên Python 3.11 và 3.13: tạo venv, nạp mô-đun, gói); thời gian nạp thư viện đo bằng verify_pyt (máy kiểm, số minh hoạ); "
                  "Python Tutorial §6 (Modules) và §12 (Virtual Environments and Packages), Library Reference: venv; pip documentation: Requirements File Format, pip freeze; "
                  "labs/requirements-py.txt (17 dòng ghim, kho kiểm trên Python 3.11.9)",
                  ["Chia chương trình thành mô-đun và gói và nạp chúng bằng import",
                   "Giải thích khối kiểm tên mô-đun cho tệp vừa chạy được vừa nạp được",
                   "Tạo, kích hoạt và kiểm môi trường ảo bằng Git Bash",
                   "Giải thích ghim phiên bản trong tệp requirements.txt và vai trò của pip freeze",
                   "Nêu thứ tự máy tìm mô-đun và vì sao tên tệp trùng tên bộ có sẵn gây lỗi",
                   "Nêu số thư viện phải cài khi thêm từng nhóm thư viện và thời gian nạp riêng của từng thư viện",
                   "Chỉ ra ba lỗi hay gặp: trùng tên bộ có sẵn, quên kích hoạt môi trường, không ghim phiên bản",
                   "Cài thư viện từ danh sách ghim vào môi trường ảo và in phiên bản đã cài"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  assumes=["pyt_cd"],
                  covers=[(1, "formula"), (2, "formula"), (3, "formula"), (4, "formula"), (5, "intuition"), (6, "scale"), (7, "pitfalls"), (8, "practice")])
