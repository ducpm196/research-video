from lib import *
from labkit import write_lab, practice_steps, practice_scene
from pyt_b import nbsp_spec

V = "venv"


def intro(steps, i, ids):
    steps[i]["introduces"] = ids
    return steps


GD = "ma,loai,so_tien\n1,chuyen,500000\n2,nap,2000000\n3,rut,300000\n4,chuyen,150000\n5,nap,1000000\n6,chuyen,800000\n7,rut,250000\n8,nap,400000\n"
F = {"gd.csv": GD}

P_DO = py("cach_do", '''import time
import tracemalloc
tracemalloc.start()
t0 = time.perf_counter()
dong = open("gd.csv", encoding="utf-8").read().split("\\n")
giay = time.perf_counter() - t0
dinh = tracemalloc.get_traced_memory()[1]
print(len(dong), giay > 0, dinh > 0)''', "10 True True", files=F)
P_A = py("ca_tep", '''def tong_ca_tep(duong_dan):
    tong = {}
    with open(duong_dan, encoding="utf-8") as f:
        dong = f.read().split("\\n")[1:-1]
    for d in dong:
        ma, loai, tien = d.split(",")
        tong[loai] = tong.get(loai, 0) + int(tien)
    return tong
print(tong_ca_tep("gd.csv"))''', "{'chuyen': 1450000, 'nap': 3400000, 'rut': 550000}", files=F)
P_B = py("tung_dong", '''import csv
def tong_theo_loai(duong_dan):
    tong = {}
    with open(duong_dan, encoding="utf-8", newline="") as f:
        for hang in csv.DictReader(f):
            loai = hang["loai"]
            tong[loai] = tong.get(loai, 0) + int(hang["so_tien"])
    return tong
print(tong_theo_loai("gd.csv"))''', "{'chuyen': 1450000, 'nap': 3400000, 'rut': 550000}", files=F)
P_C = py("theo_khoi", '''import pandas as pd
tong = {}
for khoi in pd.read_csv("gd.csv", chunksize=3):
    cong = khoi.groupby("loai")["so_tien"].sum()
    for loai, tien in cong.items():
        tong[loai] = tong.get(loai, 0) + int(tien)
print(tong)''', "{'chuyen': 1450000, 'nap': 3400000, 'rut': 550000}", files=F, env=V)
P_CBUG = py("quen_cong_don", '''import pandas as pd
for khoi in pd.read_csv("gd.csv", chunksize=3):
    tong = khoi.groupby("loai")["so_tien"].sum()
print({loai: int(tien) for loai, tien in tong.items()})''', "{'nap': 400000, 'rut': 250000}", files=F, env=V)
P_BA = py("ba_nhay", '''tep = """ma,loai
1,nap
2,rut"""
print(tep.split("\\n"))
print(len("a\\nb"), len(r"a\\nb"))''', "['ma,loai', '1,nap', '2,rut']\n3 4")
P_CHECK = py("tong_chung", '''import csv
with open("gd.csv", encoding="utf-8", newline="") as f:
    tong = 0
    for hang in csv.DictReader(f):
        tong = tong + int(hang["so_tien"])
print(tong)''', '5400000', files=F)
# Dự án mẫu cho mục tiêu 7 (khác bài tự làm: cộng mọi số tiền, không nhóm, không bỏ dòng hỏng): mô-đun + ca kiểm + chạy công cụ kiểm thử.
MOD_MAU = '''import csv

def tong_tien(duong_dan):
    tong = 0
    with open(duong_dan, encoding="utf-8", newline="") as f:
        for hang in csv.DictReader(f):
            tong = tong + int(hang["so_tien"])
    return tong
'''
TEST_MAU = '''import tempfile
from pathlib import Path
from tong_tien import tong_tien

def chay(noi_dung):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "gd.csv"
        p.write_text(noi_dung, encoding="utf-8")
        return tong_tien(str(p))

def test_hai_dong():
    assert chay("ma,loai,so_tien\\n1,nap,100\\n2,rut,50\\n") == 150

def test_rong():
    assert chay("ma,loai,so_tien\\n") == 0
'''
DRV = 'import pytest\npytest.main(["-q", "--tb=short", "-p", "no:cacheprovider", "{}"])'
P_MAU = py("du_an_mau", DRV.format("test_tong_tien.py"), ".." + " " * 71 + "[100%]\n2 passed in 0.02s", files={"tong_tien.py": MOD_MAU, "test_tong_tien.py": TEST_MAU},
           env=V, show_files={"tong_tien.py": [], "test_tong_tien.py": []})


def pt_mau(p):
    """Khung cửa sổ lệnh: chạy công cụ kiểm thử rồi đầu ra thật của p."""
    body = '<div><span class="cm"><span>&#36;</span> </span>python -m pytest -q</div>' + "".join(f"<div>{esc(l) or ' '}</div>" for l in p["out"].split("\n"))
    return '<div class="code">' + body + "</div>"


measure("l13_scale", '''import csv, json, os, tempfile, time, tracemalloc
import pandas as pd
res = {}
d = tempfile.mkdtemp()
LOAI = ["chuyen", "nap", "rut"]
for k, n in (("1e3", 10 ** 3), ("1e6", 10 ** 6)):
    p = os.path.join(d, "g" + k + ".csv")
    with open(p, "w", encoding="utf-8", newline="\\n") as f:
        f.write("ma,loai,so_tien\\n")
        for i in range(n):
            f.write("%d,%s,%d\\n" % (i, LOAI[i % 3], 100000 + i % 900000))
    res["size_" + k] = os.path.getsize(p)
    t0 = time.perf_counter()
    with open(p, encoding="utf-8") as f:
        dong = f.read().split("\\n")[1:-1]
    ta = {}
    for l in dong:
        a = l.split(",")
        ta[a[1]] = ta.get(a[1], 0) + int(a[2])
    res["t_all_" + k] = time.perf_counter() - t0
    del dong
    t0 = time.perf_counter()
    tb = {}
    with open(p, encoding="utf-8", newline="") as f:
        for h in csv.DictReader(f):
            tb[h["loai"]] = tb.get(h["loai"], 0) + int(h["so_tien"])
    res["t_line_" + k] = time.perf_counter() - t0
    t0 = time.perf_counter()
    tc = {}
    for khoi in pd.read_csv(p, chunksize=100000):
        for loai, tien in khoi.groupby("loai")["so_tien"].sum().items():
            tc[loai] = tc.get(loai, 0) + int(tien)
    res["t_chunk_" + k] = time.perf_counter() - t0
    assert ta == tb == tc
    tracemalloc.start()
    with open(p, encoding="utf-8") as f:
        dong = f.read().split("\\n")[1:-1]
    res["m_all_" + k] = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    del dong
    tracemalloc.start()
    with open(p, encoding="utf-8", newline="") as f:
        for j, h in enumerate(csv.DictReader(f)):
            int(h["so_tien"])
            if j >= 20000:
                break
    res["m_line_" + k] = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    tracemalloc.start()
    for khoi in pd.read_csv(p, chunksize=100000):
        khoi.groupby("loai")["so_tien"].sum()
    res["m_chunk_" + k] = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
print(json.dumps(res))''', env=V)

CHECKER = '''import subprocess
import sys
import tempfile
from pathlib import Path

DU_LIEU = "ma,loai,so_tien\\n1,chuyen,500000\\n2,nap,2000000\\n3,rut,300000\\n4,chuyen,xyz\\n5,nap,1000000\\n6,chuyen,150000\\n"

def cham(thu_muc):
    p = Path(thu_muc)
    ma = (p / "phan_tich.py").read_text(encoding="utf-8")
    diem = 0
    c1 = ".read(" not in ma and "readlines" not in ma
    print("1. Doc tung dong:", "DAT" if c1 else "CHUA", "(2/2)" if c1 else "(0/2)")
    if not c1:
        print("   Ly do: phan_tich.py con dung .read( hoac readlines")
    diem = diem + (2 if c1 else 0)
    sys.path.insert(0, str(p))  # sys.path: danh sach thu muc may tim mo-dun; chen thu muc cua ban len dau
    import phan_tich as mo_dun  # nap phan_tich.py vua ghi
    (p / "du_lieu.csv").write_text(DU_LIEU, encoding="utf-8")
    ket = mo_dun.tong_theo_loai(str(p / "du_lieu.csv"))
    c2 = ket == ({"chuyen": 650000, "nap": 3000000, "rut": 300000}, 1)
    print("2. Ket qua dung:", "DAT" if c2 else "CHUA", "(3/3)" if c2 else "(0/3)")
    if not c2:
        print("   Ly do: nhan duoc", ket, "- mong doi ({'chuyen': 650000, 'nap': 3000000, 'rut': 300000}, 1)")
    diem = diem + (3 if c2 else 0)
    (p / "rong.csv").write_text("ma,loai,so_tien\\n", encoding="utf-8")
    ket = mo_dun.tong_theo_loai(str(p / "rong.csv"))
    c3 = ket == ({}, 0)
    print("3. Tep rong:", "DAT" if c3 else "CHUA", "(2/2)" if c3 else "(0/2)")
    if not c3:
        print("   Ly do: nhan duoc", ket, "- mong doi ({}, 0)")
    diem = diem + (2 if c3 else 0)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "--tb=line", "-p", "no:cacheprovider", "test_phan_tich.py"], cwd=p, capture_output=True, text=True)
    c4 = r.returncode == 0 and "3 passed" in r.stdout
    print("4. Ba ca kiem qua:", "DAT" if c4 else "CHUA", "(2/2)" if c4 else "(0/2)")
    if not c4:
        print("   Ly do (pytest):", " | ".join(r.stdout.strip().split("\\n")[-4:]))
    diem = diem + (2 if c4 else 0)
    req = (p / "requirements.txt").read_text(encoding="utf-8")
    c5 = "==" in req
    print("5. Ghim phien ban:", "DAT" if c5 else "CHUA", "(1/1)" if c5 else "(0/1)")
    if not c5:
        print("   Ly do: requirements.txt khong co dong ghim ==")
    diem = diem + (1 if c5 else 0)
    print("Tong diem:", str(diem) + "/10")
'''
MODULE = '''import csv

def tong_theo_loai(duong_dan):
    tong = {}
    bo_qua = 0
    with open(duong_dan, encoding="utf-8", newline="") as f:
        for hang in csv.DictReader(f):
            try:
                tien = int(hang["so_tien"])
            except ValueError:
                bo_qua = bo_qua + 1
                continue
            tong[hang["loai"]] = tong.get(hang["loai"], 0) + tien
    return tong, bo_qua
'''
TESTS = '''import tempfile
from pathlib import Path

from phan_tich import tong_theo_loai

def chay(noi_dung):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "gd.csv"
        p.write_text(noi_dung, encoding="utf-8")
        return tong_theo_loai(str(p))

def test_tong():
    assert chay("ma,loai,so_tien\\n1,nap,100\\n2,nap,50\\n") == ({"nap": 150}, 0)

def test_dong_hong():
    assert chay("ma,loai,so_tien\\n1,nap,abc\\n") == ({}, 1)

def test_rong():
    assert chay("ma,loai,so_tien\\n") == ({}, 0)
'''
LAB_SOL = '''import pytest  # noqa: F401  (máy chấm cần thấy thư viện kiểm thử)
''' + CHECKER + '''

MODULE = """''' + MODULE + '''"""
TESTS = """''' + TESTS.replace(chr(92), chr(92) * 2) + '''"""

with tempfile.TemporaryDirectory() as d:
    (Path(d) / "phan_tich.py").write_text(MODULE, encoding="utf-8")
    (Path(d) / "test_phan_tich.py").write_text(TESTS, encoding="utf-8")
    (Path(d) / "requirements.txt").write_text("pytest==9.2.0\\n", encoding="utf-8")
    cham(d)

    import tracemalloc
    ns = {}
    exec(MODULE, ns)
    dinh = []
    for n in (2000, 20000):
        (Path(d) / "lon.csv").write_text("ma,loai,so_tien\\n" + "".join("%d,nap,100\\n" % i for i in range(n)), encoding="utf-8")
        tracemalloc.start()
        ns["tong_theo_loai"](str(Path(d) / "lon.csv"))
        dinh.append(tracemalloc.get_traced_memory()[1])
        tracemalloc.stop()
    print("Bo nho khi dong tang 10 lan:", "gan nhu khong doi" if dinh[1] < 3 * dinh[0] else "tang theo so dong")
'''
LAB_OUT_EXPECT = "1. Doc tung dong: DAT (2/2)\n2. Ket qua dung: DAT (3/3)\n3. Tep rong: DAT (2/2)\n4. Ba ca kiem qua: DAT (2/2)\n5. Ghim phien ban: DAT (1/1)\nTong diem: 10/10\nBo nho khi dong tang 10 lan: gan nhu khong doi"
P_LAB = py("lab_l13", LAB_SOL, LAB_OUT_EXPECT, env=V)
LAB_OUT = P_LAB["out"]


def shown_sec(txt):
    """Giây ứng với chữ t_show đã hiện trên màn hình ('≈ 2 s' -> 2)."""
    v, u = txt[2:].split()
    return float(v) * {"ns": 1e-9, "µs": 1e-6, "ms": 1e-3, "s": 1, "phút": 60, "giờ": 3600, "ngày": 86400}[u]


def x_k(x, k):
    """Ngoại suy từ số ĐÃ LÀM TRÒN hiện trên màn hình (bảng khớp phép nhân: 2 s x 100 = 3 phút, không phải 4 phút)."""
    return t_show(shown_sec(t_show(x)[0]) * k)


def build():
    K = lambda k: M("l13_scale", k)
    z3, z6 = K("size_1e3"), K("size_1e6")
    ta3, ta6, tb3, tb6, tc3, tc6 = K("t_all_1e3"), K("t_all_1e6"), K("t_line_1e3"), K("t_line_1e6"), K("t_chunk_1e3"), K("t_chunk_1e6")
    ma3, ma6, mb3, mb6, mc3, mc6 = K("m_all_1e3"), K("m_all_1e6"), K("m_line_1e3"), K("m_line_1e6"), K("m_chunk_1e3"), K("m_chunk_1e6")
    T = lambda x: t_show(x)
    B = lambda x: b_show(x)
    zz6, zz8 = B(z6), B(z6 * 100)
    sc_hook = sc("hook", "hook", "Báo cáo chết lúc 3 giờ sáng: tệp giao dịch đã lớn một trăm nghìn lần", [
        st(table(["quy mô", "dòng giao dịch", "dung lượng tệp", "kết quả của cách đọc cả tệp"],
                 [["ngày đầu", "1 000", B(z3)[0], f"chạy trong {T(ta3)[0]}, dùng {B(ma3)[0]} bộ nhớ"], ["sau vài tháng", "1 000 000", zz6[0], f"chạy trong {T(ta6)[0]}, dùng {B(ma6)[0]} bộ nhớ"],
                  ["sau hai năm (ngoại suy)", "100 000 000", zz8[0], f"cần {B(ma6 * 100)[0]} bộ nhớ: hết bộ nhớ, chương trình chết"]])
           + "<p class='note'><b>Ngoại suy</b> = nhân theo tỉ lệ từ số đã đo (ước lượng, chưa đo).</p>",
           f"""Chào bạn, đây là câu chuyện của một chương trình báo cáo tổng tiền theo loại giao dịch. Ngày đầu, tệp có một nghìn dòng, chương trình đọc cả tệp rồi tính, chạy trong {T(ta3)[1]}. Vài tháng sau, một triệu dòng, mất {T(ta6)[1]} và dùng {B(ma6)[1]} bộ nhớ. Hai năm sau, một trăm triệu dòng, theo ngoại suy, tức nhân theo tỉ lệ từ số đã đo, cần cỡ {B(ma6 * 100)[1]} bộ nhớ. Đó là nhiều hơn cái máy có, nên chương trình chết lúc ba giờ sáng. Đây là số minh hoạ."""),
        st("""<div class="box key">Bài tình huống cuối khoá, ba câu hỏi:
<ol><li>Ba cách đọc: <b>cả tệp</b>, <b>từng dòng</b>, <b>từng khối</b>: mỗi cách tốn bao nhiêu <b>thời gian và bộ nhớ</b> ở từng quy mô?</li>
<li>Ở quy mô nào thì <b>thiết kế phải đổi</b>, và đổi theo hướng nào?</li>
<li>Một <b>dự án nhỏ</b> trông ra sao: mô-đun, ca kiểm, danh sách thư viện ghim?</li></ol></div>""",
           """Bài tình huống cuối khoá hỏi ba điều. Ba cách đọc, cả tệp, từng dòng, từng khối, tốn bao nhiêu thời gian và bộ nhớ ở từng quy mô. Ở quy mô nào thiết kế phải đổi. Và một dự án nhỏ trông ra sao."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại những mảnh ghép sẽ dùng", [
        st(table(["điều đã học", "dùng ở đây thế nào"],
                 [["đọc tệp từng dòng", "bộ nhớ không đổi, dù tệp lớn đến đâu; đọc cả tệp thì bộ nhớ tăng theo tệp"],
                  ["từ điển cộng dồn", "<code>tong[loai] = tong.get(loai, 0) + tien</code>: nhóm khi không cần giữ mọi dòng"],
                  ["bảng và đọc theo khối", "<code>read_csv(…, chunksize=n)</code>: mỗi lần đọc <code>n</code> dòng thành một bảng nhỏ (một <b>khối</b>), tính nhanh bằng <b>mã đã biên dịch</b>: thư viện viết sẵn, chạy nhanh hơn vòng lặp Python; <code>khoi.groupby(\"loai\")[\"so_tien\"].sum()</code>: nhóm các dòng theo cột <code>loai</code> rồi cộng cột <code>so_tien</code> mỗi nhóm"],
                  ["ca kiểm và môi trường ảo", "ca kiểm chạy sau mỗi thay đổi; tệp thư viện ghim để dựng lại môi trường"]]),
           """Ta ôn lại những mảnh ghép sẽ dùng. Đọc từng dòng giữ bộ nhớ không đổi, còn đọc cả tệp làm bộ nhớ tăng theo tệp. Từ điển cộng dồn cho phép nhóm mà không giữ mọi dòng. Bảng đọc theo khối cho mỗi lần một bảng nhỏ, tính nhanh bằng mã đã biên dịch, tức thư viện viết sẵn chạy nhanh hơn vòng lặp của ngôn ngữ. Nhóm theo một cột rồi cộng cột khác cho tổng mỗi nhóm. Ca kiểm và môi trường ảo giữ cho chương trình đúng và dựng lại được.""",
           focus=[1, "1.2", "1.3", "1.4", "1.4", 1], introduces=["pyt_chunksize"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã ba chiến lược và cấu trúc dự án", [
        st(table(["chiến lược", "viết", "bộ nhớ", "ghi chú"],
                 [["A. đọc cả tệp", "<code>f.read().split(\"\\n\")</code> rồi duyệt", "tăng theo số dòng", "đơn giản; hợp tệp nhỏ"],
                  ["B. từng dòng", "<code>for hang in csv.DictReader(f):</code>", "gần như không đổi", "chậm hơn một chút mỗi dòng (nhiều lệnh Python)"],
                  ["C. từng khối", "<code>for khoi in pd.read_csv(p, chunksize=100000):</code>", "bằng một khối", "nhanh nhờ mã biên dịch; phải <b>cộng dồn</b> kết quả các khối"]]),
           """Bảng đầu là ba chiến lược. Đọc cả tệp: bộ nhớ tăng theo số dòng, hợp tệp nhỏ. Đọc từng dòng: bộ nhớ gần như không đổi, nhưng chậm hơn chút. Đọc từng khối: bộ nhớ bằng một khối, nhanh nhờ mã biên dịch, nhưng phải cộng dồn."""),
        st(table(["tệp", "vai trò"],
                 [["<code>phan_tich.py</code>", "mô-đun: hàm <code>tong_theo_loai(duong_dan)</code> làm <b>một việc</b>, nhận đường dẫn, trả kết quả"],
                  ["<code>test_phan_tich.py</code>", "các ca kiểm: dữ liệu nhỏ có đáp án tính tay, gồm tệp rỗng và dòng hỏng"],
                  ["<code>requirements.txt</code>", "danh sách thư viện ghim <code>tên==phiên_bản</code>"]]),
           """Bảng thứ hai là cấu trúc dự án nhỏ. Một mô-đun có hàm làm một việc, nhận đường dẫn và trả kết quả. Một tệp ca kiểm với dữ liệu nhỏ có đáp án tính tay, gồm cả tệp rỗng và dòng hỏng. Và một tệp danh sách thư viện ghim đúng phiên bản.""", clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: ba cách đọc, nhìn bằng bộ nhớ", [
        st(svg(1500, 430,
               txt(250, 35, "A. cả tệp", 28, "middle", "#dc2626", True),
               box(40, 60, 420, 260, ["toàn bộ tệp", "nằm trong bộ nhớ"], C_RED, 28, True),
               txt(250, 355, "bộ nhớ tăng theo số dòng", 26, "middle", "#dc2626", True),
               txt(750, 35, "B. từng dòng", 28, "middle", "#2a78d6", True),
               box(560, 130, 380, 70, ["một dòng"], C_BLUE, 26, True),
               txt(750, 235, "dòng xử lý xong là bỏ", 24, "middle", "#1f2937"),
               txt(750, 355, "bộ nhớ gần như không đổi", 26, "middle", "#2a78d6", True),
               txt(1250, 35, "C. từng khối", 28, "middle", "#16a34a", True),
               box(1060, 100, 380, 130, ["một khối (100 000 dòng)"], C_GREEN, 26, True),
               txt(1250, 265, "tính cả khối bằng một lệnh, rồi cộng dồn", 24, "middle", "#1f2937"),
               txt(1250, 355, "bộ nhớ ≈ một khối", 26, "middle", "#16a34a", True),
               txt(750, 405, "kết quả cộng dồn (từ điển vài khoá) luôn nhỏ, dù tệp lớn", 26, "middle", "#1f2937", True)),
           """Hình này nhìn ba cách bằng bộ nhớ. Cách một giữ toàn bộ tệp, nên bộ nhớ tỉ lệ với số dòng. Cách hai giữ một dòng rồi bỏ, bộ nhớ gần như không đổi. Cách ba giữ một khối, tính bằng một lệnh rồi cộng dồn. Kết quả cộng dồn luôn nhỏ, dù tệp lớn đến đâu."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: bộ nhớ theo số dòng, và vì sao đổi thiết kế", [
        st(run_block(P_DO, title="Bước 0. Cách đo: thời gian và đỉnh bộ nhớ của một việc")
           + "<p><code>perf_counter()</code> đọc hai lần: hiệu là số giây; <code>tracemalloc</code> cho đỉnh bộ nhớ; in <code>True</code> khi chúng dương. <code>gd.csv</code> có $1$ tiêu đề và $8$ giao dịch, mỗi dòng kết thúc bằng xuống dòng, nên tách theo xuống dòng thừa một phần rỗng cuối: $10 = 1 + 8 + 1$.</p>",
           """Ta đọc đồng hồ hai lần, trước và sau việc cần đo, hiệu là số giây. Công cụ theo dõi bộ nhớ bật trước, rồi cho đỉnh bộ nhớ. Tệp có một tiêu đề và tám giao dịch, mỗi dòng kết thúc bằng xuống dòng, nên tách theo xuống dòng thừa một phần rỗng ở cuối.""", clear=True),
        st(f"<p>Vì cách A giữ <b>mọi dòng</b>, bộ nhớ $\\approx$ (số byte mỗi dòng trong bộ nhớ) $\\times$ (số dòng). Đo ở $10^6$ dòng: {B(ma6)[0]}, tức cỡ ${sig(ma6 / 1e6, 2)}$ byte mỗi dòng.</p>"
           f"<table class='t'><tr><th>quy mô</th><th>A: cả tệp</th><th>B: từng dòng</th><th>C: từng khối</th></tr>"
           f"<tr><td>10<sup>3</sup> dòng</td><td>{B(ma3)[0]}</td><td>{B(mb3)[0]}</td><td>{B(mc3)[0]}</td></tr>"
           f"<tr><td>10<sup>6</sup> dòng</td><td>{B(ma6)[0]}</td><td>{B(mb6)[0]}</td><td>{B(mc6)[0]}</td></tr></table>",
           f"""Bước một, bộ nhớ theo số dòng. Vì cách đọc cả tệp giữ mọi dòng, bộ nhớ xấp xỉ số byte mỗi dòng nhân số dòng. Đo ở một triệu dòng được {B(ma6)[1]}, tức cỡ {vi_num(sig(ma6 / 1e6, 2))} byte mỗi dòng. Hai cách còn lại gần như không đổi giữa một nghìn và một triệu dòng, một cái cỡ {B(mb6)[1]}, một cái cỡ {B(mc6)[1]}."""),
        st(table(["quy mô", "A: cả tệp", "B: từng dòng", "C: từng khối"],
                 [["10<sup>3</sup> dòng", T(ta3)[0], T(tb3)[0], T(tc3)[0]], ["10<sup>6</sup> dòng", T(ta6)[0], T(tb6)[0], T(tc6)[0]],
                  ["10<sup>8</sup> dòng (ngoại suy)", "hết bộ nhớ", x_k(tb6, 100)[0], x_k(tc6, 100)[0]]])
           + "<p>Vì thời gian của B và C tăng <b>tuyến tính</b> theo số dòng ($\\times 100$ dòng $\\to \\times 100$ thời gian) và bộ nhớ không đổi, chúng <b>xử lý được mọi cỡ tệp</b>; chỉ A thất bại vì bộ nhớ, không phải vì thời gian.</p>",
           f"""Bước hai, thời gian. Ở một triệu dòng, cả tệp mất {T(ta6)[1]}, từng dòng mất {T(tb6)[1]}, từng khối mất {T(tc6)[1]}. Vì thời gian của hai cách sau tăng tuyến tính và bộ nhớ không đổi, chúng xử lý được mọi cỡ tệp. Ngoại suy một trăm triệu dòng, từng dòng cỡ {x_k(tb6, 100)[1]}, từng khối cỡ {x_k(tc6, 100)[1]}. Cách cả tệp thất bại vì bộ nhớ, không phải vì thời gian.""", clear=True),
        st(raw_block(GD.strip().split("\n"), title="Tệp gd.csv dùng ở các ví dụ: tám giao dịch"),
           """Đây là tệp giao dịch dùng ở các ví dụ tiếp theo, tám dòng với mã, loại và số tiền. Ta tính tay được tổng theo loại từ đây, và dùng nó để kiểm các cách đọc.""", clear=True),
        st(run_block(P_CBUG, title="Bước 3. Cái bẫy của chiến lược C: quên cộng dồn qua các khối") + "<p>Gán <code>tong = …</code> mỗi khối <b>ghi đè</b>: chỉ còn kết quả của khối cuối, ở đây $400\\,000 + 250\\,000$ thay vì tổng đúng ($5\\,400\\,000$).</p>"
           + "<p><code>tong.items()</code> cho từng cặp (khoá, giá trị); <code>{loai: int(tien) for loai, tien in tong.items()}</code> là <b>từ điển suy ra</b>: vòng lặp một dòng dựng từ điển mới, như danh sách suy ra nhưng mỗi phần tử có dạng <code>khoá: giá_trị</code>.</p>",
           """Bước ba, cái bẫy của cách đọc theo khối. Gán kết quả mỗi khối vào cùng một biến thì khối sau ghi đè khối trước, chỉ còn bốn trăm nghìn và hai trăm năm mươi nghìn, thay vì năm triệu bốn trăm nghìn. Dòng in cuối lấy từng cặp khoá và giá trị, rồi dựng từ điển mới bằng vòng lặp một dòng, gọi là từ điển suy ra. Chương trình không báo lỗi, nên ta cần phép kiểm tổng.""", clear=True, introduces=["pyt_items"]),
    ], checks=["10 ** 6 * 100 == 10 ** 8", "400000 + 250000 == 650000 and 650000 < 5400000"])
    sc_ex = sc("example", "example", "Ví dụ: ba cách đọc cho cùng kết quả, rồi một dự án nhỏ mẫu", [
        st(run_block(P_A, title="Cách A: đọc cả tệp rồi duyệt"),
           """Ví dụ một, cách đọc cả tệp. Hàm đọc toàn bộ nội dung, tách thành từng dòng, bỏ dòng tiêu đề và dòng trống cuối, rồi cộng dồn tiền theo loại. Với tệp tám dòng, nó cho ba tổng, và đây là cách để so với hai cách sau."""),
        st(run_block(P_B, title="Cách B: từng dòng, hàm làm một việc")
           + "<p><code>csv.DictReader(f)</code> cho mỗi dòng một từ điển, khoá là tên cột; <code>newline=\"\"</code> để bộ đọc tự xử lý xuống dòng trong ô.</p>",
           """Ví dụ hai, cách đọc từng dòng, đóng gói thành một hàm làm một việc. Bộ đọc bảng cho mỗi dòng một từ điển, ta cộng dồn tiền theo loại vào một từ điển khác. Kết quả giống hệt cách đọc cả tệp.""", clear=True),
        st(run_block(P_C, title="Cách C: từng khối ba dòng, cộng dồn kết quả các khối"),
           """Ví dụ ba, cách đọc theo khối. Mỗi khối ba dòng, nhóm theo loại trong khối rồi cộng dồn vào từ điển chung. Kết quả giống hệt cách trước, vì cộng dồn qua các khối cho đúng tổng. Với tệp một trăm triệu dòng, khối sẽ là một trăm nghìn dòng, và ta chỉ đổi một con số.""", clear=True),
        st(table(["khối", "dòng", "chuyển", "nạp", "rút"], [["1", "1–3", "500 000", "2 000 000", "300 000"], ["2", "4–6", "950 000", "1 000 000", "—"], ["3", "7–8", "—", "400 000", "250 000"],
                                                     ["<b>cộng dồn</b>", "1–8", "<b>1 450 000</b>", "<b>3 400 000</b>", "<b>550 000</b>"]])
           + "<p>Mỗi khối ba dòng cho một bảng nhóm nhỏ; cộng dồn từng ô qua các khối ra đúng ba tổng cuối: $500\\,000 + 950\\,000 = 1\\,450\\,000$.</p>",
           """Ví dụ bốn, nhìn từng khối. Khối một có ba dòng, khối hai có ba dòng, khối ba có hai dòng cuối. Mỗi khối cho một bảng nhóm nhỏ. Cộng dồn từng ô qua các khối ra đúng ba tổng cuối, chuyển năm trăm nghìn cộng chín trăm năm mươi nghìn bằng một triệu bốn trăm năm mươi nghìn. Bộ nhớ chỉ giữ một khối và từ điển tổng.""", clear=True),
        st(table(["viết trong mã", "đọc là", "nghĩa"],
                 [["<code>\"\"\"…\"\"\"</code> hoặc <code>'''…'''</code>", "chuỗi ba nháy", "chuỗi <b>nhiều dòng</b>: mọi thứ giữa hai bộ ba nháy, kể cả xuống dòng thật, thuộc chuỗi; dùng để viết cả một tệp mã vào một biến"],
                  ["<code>\\n</code>", "ký tự xuống dòng", "hai ký tự <code>\\</code> và <code>n</code> trong chuỗi thường là <b>một</b> ký tự xuống dòng"],
                  ["<code>r\"…\"</code>, <code>r'''…'''</code>", "chuỗi thô", "chữ <code>r</code> đứng trước nháy giữ nguyên dấu <code>\\</code>, nên <code>\\n</code> vẫn là hai ký tự; dùng khi ghi ra tệp mã có chứa <code>\\n</code>"]]),
           """Bài tự làm ghi cả tệp mã từ một chương trình, nên cần chuỗi nhiều dòng. Chuỗi ba nháy giữ nguyên các dòng xuống dòng thật nằm giữa hai bộ ba nháy. Hai ký tự gạch ngược và n trong chuỗi thường là một ký tự xuống dòng. Chữ r đặt trước nháy làm chuỗi thô, giữ nguyên dấu gạch ngược, dùng khi ghi ra tệp mã có chứa gạch ngược n.""", clear=True),
        st(run_block(P_BA, title="Thử: chuỗi ba nháy, xuống dòng và chuỗi thô")
           + "<p>Chuỗi ba nháy tách tại xuống dòng thành $3$ phần tử; <code>\"a\\nb\"</code> dài $3$ ký tự (a, xuống dòng, b), còn chuỗi thô <code>r\"a\\nb\"</code> dài $4$ ký tự.</p>",
           """Chương trình thử tách chuỗi ba nháy tại ký tự xuống dòng, được ba phần tử. Chuỗi thường chứa gạch ngược n dài ba ký tự, còn chuỗi thô cùng nội dung dài bốn ký tự.""", clear=True),
        st(raw_block(MOD_MAU.strip().split("\n"), title="Dự án nhỏ mẫu (1/3): mô-đun tong_tien.py, một hàm làm một việc", py_hl=True)
           + "<p>Khác bài tự làm: hàm này chỉ cộng mọi số tiền trong tệp, đọc từng dòng, không nhóm theo loại.</p>",
           """Giờ ta dựng một dự án nhỏ mẫu, khác với bài tự làm. Mô-đun có một hàm làm một việc, nhận đường dẫn và trả về tổng mọi số tiền trong tệp, đọc từng dòng.""", clear=True),
        st(raw_block(TEST_MAU.strip().split("\n")[0:9], title="Dự án nhỏ mẫu (2/3): ca kiểm test_tong_tien.py, nửa trên", py_hl=True)
           + "<p><code>tempfile.TemporaryDirectory()</code> tạo một thư mục tạm và tự xoá khi ra khỏi khối <code>with</code>; hàm <code>chay</code> ghi tệp CSV nhỏ vào đó (<code>p.write_text(s, …)</code> ghi chuỗi <code>s</code> vào tệp <code>p</code>) rồi gọi hàm cần kiểm.</p>",
           """Tệp ca kiểm nạp hàm từ mô-đun, vì hai tệp nằm cùng thư mục. Hàm phụ ghi một tệp bảng nhỏ vào thư mục tạm, tự xoá khi xong, rồi gọi hàm cần kiểm.""",
           clear=True, introduces=["pyt_tempfile"]),
        st(raw_block(TEST_MAU.strip().split("\n")[10:15], title="Ca kiểm, nửa dưới (nối ngay sau nửa trên)", py_hl=True)
           + "<p><code>assert điều_kiện</code> là <b>khẳng định</b>: sai thì ca đỏ. Mỗi ca có đáp án tính tay: $100 + 50 = 150$; tệp chỉ có dòng tiêu đề cho $0$.</p>",
           """Mỗi ca là một khẳng định, sai thì ca đỏ. Đáp án tính tay: một trăm cộng năm mươi bằng một trăm năm mươi, và tệp chỉ có dòng tiêu đề cho không.""", clear=True),
        st(pt_mau(P_MAU) + "<p>Tệp thứ ba, <code>requirements.txt</code>, chỉ một dòng ghim: <code>pytest==9.2.0</code>.</p>",
           """Chạy công cụ kiểm thử ở thư mục có hai tệp, hai ca đều qua. Tệp thứ ba là danh sách thư viện ghim, một dòng, tên thư viện, hai dấu bằng, rồi phiên bản. Ba tệp này đã là một dự án nhỏ hoàn chỉnh, và bài tự làm chỉ thay phần ruột.""", clear=True),
    ], checks=["500000 + 150000 + 800000 == 1450000", "2000000 + 1000000 + 400000 == 3400000", "300000 + 250000 == 550000", "500000 + 950000 == 1450000 and 2000000 + 1000000 + 400000 == 3400000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: tổng ba nhóm bằng tổng chung, hai cách cùng kết quả", [
        st(run_block(P_CHECK, title="Tổng chung bằng một vòng lặp, không nhóm")
           + "<p>$1\\,450\\,000 + 3\\,400\\,000 + 550\\,000 = 5\\,400\\,000$ ✓ Cách B và cách C cho cùng ba số; phép kiểm này bắt được lỗi quên cộng dồn ở bước $3$.</p>",
           """Đường kiểm khác, cộng tổng chung bằng một vòng lặp, không nhóm. Vì cách này độc lập với việc nhóm, nên nó kiểm được cả hai. Được năm triệu bốn trăm nghìn, đúng bằng tổng ba nhóm cộng lại. Phép kiểm này bắt được lỗi quên cộng dồn."""),
    ], checks=["1450000 + 3400000 + 550000 == 5400000"])
    sc_scale = sc("scale", "concept", "Ba quy mô, ba quyết định: thiết kế phải đổi khi dữ liệu đổi bậc", [
        st(table(["quy mô", "A: cả tệp", "B: từng dòng", "C: từng khối", "nên chọn"],
                 [["10<sup>3</sup> dòng", f"{T(ta3)[0]}, {B(ma3)[0]}", f"{T(tb3)[0]}, {B(mb3)[0]}", f"{T(tc3)[0]}, {B(mc3)[0]}", "cách đơn giản nhất"],
                  ["10<sup>6</sup> dòng", f"{T(ta6)[0]}, {B(ma6)[0]}", f"{T(tb6)[0]}, {B(mb6)[0]}", f"{T(tc6)[0]}, {B(mc6)[0]}", "B hoặc C; A còn chạy được"],
                  ["10<sup>8</sup> dòng (ngoại suy)", f"{B(ma6 * 100)[0]} (hết bộ nhớ)", f"{x_k(tb6, 100)[0]}, {B(mb6)[0]}", f"{x_k(tc6, 100)[0]}, {B(mc6)[0]}", "C (hoặc cơ sở dữ liệu: chương trình chuyên lưu và tìm trong bảng rất lớn)"]])
           + "<p class='note'>Cách đo: thời gian = <code>time.perf_counter()</code> sau trừ trước việc cần đo; đỉnh bộ nhớ = <code>tracemalloc.get_traced_memory()[1]</code>. Số minh hoạ trên máy kiểm; ở $10^3$ dòng cả ba cách chỉ vài phần nghìn giây nên chênh lệch không có ý nghĩa; <b>ngoại suy</b> = nhân theo tỉ lệ từ số đã đo.</p>",
           f"""Bảng này tóm tắt ba quy mô. Ở một nghìn dòng, chọn cách đơn giản nhất, vì cả ba đều rẻ. Ở một triệu dòng, từng dòng hay từng khối đều tốt, còn cả tệp tốn {B(ma6)[1]}. Ở một trăm triệu dòng, cả tệp cần {B(ma6 * 100)[1]}, hết bộ nhớ, nên từng khối là lựa chọn hợp lý, cỡ {x_k(tc6, 100)[1]} với bộ nhớ không đổi."""),
        st("<div class='box key'><b>Đánh đổi và điều kiện áp dụng:</b> cách C nhanh nhưng cần thư viện ngoài và phải <b>cộng dồn đúng</b>; cách B không cần gì ngoài thư viện chuẩn nhưng chậm hơn. "
           "Cách cộng dồn chỉ dùng được cho thống kê <b>có thể gộp</b> (tổng, đếm, nhỏ nhất, lớn nhất). <b>Trung vị</b> (giá trị đứng giữa khi xếp các số từ nhỏ đến lớn; ví dụ trung vị của $1, 2, 9$ là $2$), hay nối hai tệp lớn, <b>không</b> gộp được theo khối: cần xếp trên đĩa (sắp xếp bằng cách ghi từng phần ra đĩa rồi trộn lại), ước lượng, hoặc cơ sở dữ liệu. "
           "Và <b>đo trước khi đổi</b>: ở $10^3$ dòng, mọi tối ưu chỉ làm mã khó đọc hơn.</div>",
           """Đánh đổi và điều kiện áp dụng. Cách từng khối nhanh nhưng cần thư viện ngoài và phải cộng dồn đúng. Cách từng dòng không cần gì ngoài thư viện chuẩn nhưng chậm hơn. Cách cộng dồn chỉ dùng được cho thống kê có thể gộp, như tổng, đếm, nhỏ nhất, lớn nhất. Trung vị là giá trị đứng giữa khi xếp các số từ nhỏ đến lớn, và không gộp được theo khối: cần xếp trên đĩa, ước lượng, hoặc cơ sở dữ liệu. Hãy đo trước khi đổi, vì ở một nghìn dòng mọi tối ưu chỉ làm mã khó đọc hơn.""", clear=True, introduces=["pyt_trung_vi"]),
    ], checks=["10 ** 8 // 10 ** 6 == 100"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Quên cộng dồn qua các khối.</div>' + run_block(P_CBUG)
           + "<p>Kết quả sai mà <b>không báo lỗi</b>. Phép thử: đối chiếu với <b>tổng chung</b> tính bằng đường khác (bước kiểm).</p>",
           """Lỗi thứ nhất, của người mới, là quên cộng dồn qua các khối. Kết quả sai mà không báo lỗi. Phép thử là đối chiếu với tổng chung tính bằng đường khác."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Tối ưu trước khi đo: viết lại cách phức tạp khi dữ liệu chưa tới ngưỡng cần.</div>'
           + f"<p>Ở $10^3$ dòng, cách đơn giản mất {T(ta3)[0]}: viết lại thành khối là <b>tốn công, thêm lỗi, không lợi gì</b>. Ngược lại, <b>không đo quy mô sắp tới</b> làm chương trình chết lúc nửa đêm. Phép thử: <b>đo ở hai quy mô</b> rồi ngoại suy bộ nhớ.</p>",
           f"""Lỗi thứ hai, của người đã đi làm, là tối ưu trước khi đo. Ở một nghìn dòng, cách đơn giản mất {T(ta3)[1]}, viết lại thành khối là tốn công, thêm lỗi, không lợi gì. Nhưng ngược lại, không đo quy mô sắp tới làm chương trình chết lúc nửa đêm. Phép thử là đo ở hai quy mô rồi ngoại suy bộ nhớ.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Nhầm thống kê gộp được với không gộp được.</div>'
           + "<p>Tổng, đếm, nhỏ nhất, lớn nhất: gộp qua các khối đúng. <b>Trung bình của các trung bình</b> chỉ đúng khi mọi khối cùng cỡ; <b>trung vị</b> thì không gộp được: trung vị của các trung vị khối <b>khác</b> trung vị cả tệp. Ví dụ: hai khối $[1, 2, 9]$ và $[3, 4, 5]$ có trung vị $2$ và $4$, trung vị của hai số đó là $3$; nhưng trung vị cả sáu số là $\\frac{3 + 4}{2} = 3{,}5$.</p>",
           """Lỗi thứ ba, của người đã đi làm, là nhầm thống kê gộp được với không gộp được. Tổng, đếm, nhỏ nhất, lớn nhất gộp qua các khối đúng, còn trung vị thì không. Hai khối một, hai, chín và ba, bốn, năm có trung vị hai và bốn, trung vị của hai số đó là ba. Nhưng trung vị của cả sáu số là ba phẩy năm.""", clear=True),
    ], checks=["650000 != 5400000", "(2 + 4) / 2 == 3 and (3 + 4) / 2 == 3.5"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Tệp $5$ GB, máy có $8$ GB bộ nhớ.</p>
<ol><li>Cần tổng tiền theo $50\\,000$ tài khoản: cách A, B hay C? Vì sao?</li>
<li>Cần <b>trung vị</b> số tiền của cả tệp: cộng dồn theo khối có đủ không?</li></ol>
<p><b>Quyết định:</b> báo cáo chạy $2$ giây trên $10^3$ dòng. Có nên viết lại ngay theo khối không?</p>""",
           """Bây giờ tới phần bạn tự làm. Tệp năm tỉ byte, máy có tám tỉ byte bộ nhớ. Câu một, cần tổng tiền theo năm mươi nghìn tài khoản, dùng cách một, hai hay ba, và vì sao. Câu hai, cần trung vị số tiền của cả tệp, cộng dồn theo khối có đủ không.
           Sau đó là một quyết định, báo cáo chạy hai giây trên một nghìn dòng, có nên viết lại ngay theo khối không. Hãy dừng video và làm.""", pause=60),
        st(table(["câu", "đáp án"], [["1", "<b>B hoặc C</b>: kết quả chỉ là $50\\,000$ khoá, nhỏ; mỗi dòng xem xong là bỏ. A giữ bộ nhớ cỡ $5$ lần dung lượng tệp, tức cỡ $25$ GB, nhiều hơn $8$ GB nên chắc chắn hết bộ nhớ"],
                                     ["2", "<b>không đủ</b>: trung vị không gộp được từ trung vị các khối; cần xếp trên đĩa, lấy mẫu để ước lượng, hoặc cơ sở dữ liệu"]]),
           """Đáp án như sau. Câu một, từng dòng hoặc từng khối, vì kết quả chỉ năm mươi nghìn khoá. Cách cả tệp cần cỡ hai mươi lăm tỉ byte, nhiều hơn tám tỉ byte của máy. Câu hai, không đủ, vì trung vị không gộp được từ trung vị các khối; cần xếp trên đĩa, lấy mẫu ước lượng, hoặc cơ sở dữ liệu."""),
        st("<div class='box key'><b>Quyết định:</b> <b>chưa</b>. Hai giây ở $10^3$ dòng là do lệnh khác (hoặc đo sai), không phải do cách đọc. Hãy <b>đo</b> chỗ nào chậm trước, rồi mới sửa. "
           "Chỉ cần đổi thiết kế khi số dòng hoặc bộ nhớ sắp chạm ngưỡng, và có phép kiểm tổng để chắc kết quả không đổi.</div>",
           """Quyết định, chưa. Hai giây ở một nghìn dòng là do việc khác, hoặc đo sai, không phải do cách đọc. Hãy đo chỗ nào chậm trước rồi mới sửa. Chỉ đổi thiết kế khi số dòng hoặc bộ nhớ sắp chạm ngưỡng, và có phép kiểm tổng để chắc kết quả không đổi.""", clear=True),
    ], checks=["5 * 10 ** 9 < 8 * 10 ** 9", "5 * 5 * 10 ** 9 > 8 * 10 ** 9"])
    cham_a = st(table(["việc của hàm chấm", "lệnh trong hàm", "đọc là"],
                      [["1. kiểm đọc từng dòng", "<code>ma = (p / \"phan_tich.py\").read_text(…)</code>, <code>\".read(\" not in ma</code>", "đọc mã mô-đun của bạn thành chuỗi <code>ma</code>, rồi kiểm trong đó không có chữ <code>.read(</code>"],
                       ["2–3. kết quả, tệp rỗng", "<code>sys.path.insert(0, str(p))</code>, <code>import phan_tich as mo_dun</code>", "<code>sys.path</code> là <b>danh sách thư mục</b> máy tìm mô-đun, theo thứ tự; <code>insert(0, …)</code> chèn thư mục của bạn lên <b>đầu</b>; rồi nạp mô-đun vừa ghi, gọi hàm của bạn với dữ liệu mẫu và so đáp án"]]),
                """Trước khi làm, hãy đọc hàm chấm qua bảng này, nó làm năm việc. Việc một kiểm mã mô-đun của bạn không có lệnh đọc cả tệp. Việc hai và ba nạp mô-đun vừa ghi, vì máy tìm mô-đun trong một danh sách thư mục theo thứ tự, nên ta chèn thư mục của bạn lên đầu.""",
                introduces=["pyt_sys_path"])
    cham_b = st(table(["việc của hàm chấm", "lệnh trong hàm", "đọc là"],
                      [["4. ba ca kiểm qua", "<code>subprocess.run([sys.executable, \"-m\", \"pytest\", …], capture_output=True, text=True)</code>", "chạy công cụ kiểm thử như gõ lệnh ở cửa sổ lệnh; <code>sys.executable</code> là chính bản Python đang chạy, <code>capture_output=True</code> giữ đầu ra lại, <code>text=True</code> cho đầu ra là chữ"],
                       ["5. ghim phiên bản", "<code>\"==\" in req</code>", "đọc <code>requirements.txt</code>, kiểm có dấu <code>==</code>"]]),
                """Việc bốn chạy công cụ kiểm thử như gõ lệnh ở cửa sổ lệnh, và giữ đầu ra lại để kiểm. Việc năm kiểm tệp thư viện có dấu ghim, nên cả hàm cho đủ mười điểm khi cả năm việc đạt.""")
    hint_b = st("""<div class="box key">Viết <code>MODULE</code> và <code>TESTS</code> bằng chuỗi ba nháy thô <code>r'''…'''</code>: chữ <code>r</code> giữ nguyên dấu gạch chéo, nên <code>\\n</code> trong tệp mã viết y như thường. Tiêu chí nào <b>CHUA</b> thì đọc dòng <code>Ly do</code> ngay dưới. Danh sách ghim: <code>pytest==9.2.0</code>. Phần đo: ghi tệp CSV hai cỡ vào thư mục tạm, <code>tracemalloc.start()</code> trước khi gọi hàm, <code>tracemalloc.get_traced_memory()[1]</code> sau khi gọi, rồi <code>tracemalloc.stop()</code>; so đỉnh ở $20\\,000$ dòng với <b>3 lần</b> đỉnh ở $2\\,000$ dòng. Lời giải ở <code>labs/PYT/L13/loi_giai.py</code>.</div>""",
                """Viết chuỗi mã bằng chuỗi ba nháy thô, để giữ nguyên dấu gạch ngược. Tiêu chí nào chưa đạt thì máy in lý do ngay dưới. Phần đo thì so đỉnh bộ nhớ của tệp lớn với ba lần đỉnh của tệp nhỏ. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", clear=True)
    sc_prac = practice_scene(sc, "Tự làm: dựng dự án nhỏ và tự chấm bằng thang 10 điểm", intro([cham_a, cham_b] + pr_steps(
        st, "PYT", "L13",
        """<p><b>Đề</b> (cần môi trường ảo đã cài thư viện): tạo <code>du_an.py</code> gồm: dòng đầu <code>import pytest</code>; hàm chấm <code>cham(thu_muc)</code> <b>chép nguyên</b> từ <code>de.md</code> (5 tiêu chí, 10 điểm); chuỗi <code>MODULE</code>, <code>TESTS</code> do <b>bạn viết</b>; rồi ghi ba tệp vào một thư mục tạm và gọi <code>cham</code>:</p>
<ol><li><code>phan_tich.py</code>: <code>tong_theo_loai(duong_dan)</code> trả <code>(tổng theo loại, số dòng bỏ qua)</code>, đọc <b>từng dòng</b>, bỏ qua dòng <code>so_tien</code> hỏng;</li>
<li><code>test_phan_tich.py</code>: <b>3</b> ca (tổng đúng, dòng hỏng, tệp rỗng); <code>requirements.txt</code> có dòng ghim <code>==</code>;</li>
<li><b>đo</b>: với tệp $2\\,000$ rồi $20\\,000$ dòng, đo đỉnh bộ nhớ của hàm bằng <code>tracemalloc</code>, rồi in <code>Bo nho khi dong tang 10 lan: …</code> (<code>gan nhu khong doi</code> hay <code>tang theo so dong</code>).</li></ol>
<p class="note">Video dừng 20 phút cho lượt đầu; cả bài dự kiến 45–60 phút (xem <code>de.md</code>): cứ làm tiếp sau khi video chạy lại.</p>""",
        """Bây giờ tới phần bạn tự làm, trong môi trường ảo đã cài thư viện. Viết một chương trình chép nguyên hàm chấm từ tệp đề bài. Rồi bạn viết mô-đun đọc từng dòng, trả về tổng theo loại và số dòng bỏ qua, ba ca kiểm, và tệp thư viện có dòng ghim. Ghi ba tệp vào thư mục tạm, gọi hàm chấm, rồi đo đỉnh bộ nhớ với tệp hai nghìn và hai mươi nghìn dòng.
        Video dừng hai mươi phút cho lượt đầu, còn cả bài dự kiến bốn mươi lăm đến sáu mươi phút. Hãy dừng video và làm.""",
        LAB_OUT, "du_an.py",
        '<div class="box key"><b>Nếu kẹt:</b> thân vòng đọc của mô-đun:</div>' + raw_block([
            "for hang in csv.DictReader(f):", "    try:", "        tien = int(hang[\"so_tien\"])", "    except ValueError:", "        bo_qua = bo_qua + 1", "        continue"], py_hl=True)
        + """<div class="box key">Ca kiểm tự ghi tệp CSV nhỏ vào thư mục tạm (<code>tempfile.TemporaryDirectory()</code> tạo một thư mục tạm và tự xoá khi xong) rồi gọi hàm.</div>""",
        """Nếu kẹt, trong mô-đun bắt lỗi giá trị khi đổi số tiền, đếm dòng bỏ qua rồi sang dòng kế. Ca kiểm tự ghi một tệp bảng nhỏ vào thư mục tạm rồi gọi hàm.""", pause=1200) + [hint_b], 0, ["pyt_sys_path"]), "PYT", "L13")
    write_lab("PYT", "L13", """# Lab PYT L13 — Dựng dự án nhỏ và tự chấm bằng thang 10 điểm

**cần: pip install -r labs/requirements-py.txt** (trong môi trường ảo của bài 8). Tạo `du_an.py` gồm:

1. dòng đầu `import pytest` (máy chấm cần thấy thư viện này);
2. hàm chấm dưới đây, **chép nguyên**;
3. chuỗi `MODULE` và `TESTS` **do bạn viết**, rồi ghi `phan_tich.py`, `test_phan_tich.py`, `requirements.txt` vào một thư mục tạm (`tempfile.TemporaryDirectory()`) và gọi `cham(thu_muc)`. Lưu ý: viết `MODULE` và `TESTS` bằng chuỗi ba nháy thô `r'''…'''` (chuỗi ba nháy: mọi thứ giữa hai bộ ba nháy, kể cả xuống dòng thật, là một chuỗi; chữ `r` giữ nguyên dấu gạch chéo, nên `\\n` trong tệp mã viết y như thường). Mỗi tiêu chí CHUA có dòng `Ly do` ngay dưới.

**Yêu cầu của dự án** (khớp thang điểm):
- `phan_tich.py`: `tong_theo_loai(duong_dan)` đọc CSV (cột `ma,loai,so_tien`) **từng dòng** (không `.read(`, không `readlines`), trả `(dict tổng theo loại, số dòng bỏ qua)`; dòng `so_tien` không phải số thì **bỏ qua và đếm**.
- `test_phan_tich.py`: đúng **3** ca (`test_tong`, `test_dong_hong`, `test_rong`), qua hết.
- `requirements.txt`: có dòng ghim `==` (ví dụ `pytest==9.2.0`).

**Thang điểm (hàm chấm):** 1) đọc từng dòng 2đ · 2) kết quả đúng 3đ · 3) tệp rỗng 2đ · 4) ba ca kiểm qua 2đ · 5) ghim phiên bản 1đ.

**Cách đọc hàm chấm** (đọc trước khi chép; không cần hiểu từng chữ của máy, chỉ cần nắm mỗi việc nó làm): `read_text` đọc tệp thành chuỗi, và việc 1 kiểm trong mã của bạn không có `.read(`; việc 2 và 3 nạp mô-đun bạn vừa ghi rồi gọi hàm của bạn với dữ liệu mẫu (`sys.path` là danh sách thư mục mà máy tìm mô-đun, theo thứ tự; `sys.path.insert(0, …)` chèn thư mục của bạn lên **đầu**; `import phan_tich` nạp tệp `phan_tich.py` ở đó); việc 4 chạy công cụ kiểm thử như gõ lệnh ở cửa sổ lệnh (`subprocess.run([...], capture_output=True, text=True)`: `sys.executable` là đường dẫn chính bản Python đang chạy, `capture_output=True` giữ đầu ra lại, `text=True` cho đầu ra là chữ); việc 5 kiểm `requirements.txt` có dấu `==`.

```python
""" + CHECKER + """```

4. **Phần đo** (không nằm trong thang điểm trên; máy chấm so cả dòng này): sau khi gọi `cham`, ghi hai tệp CSV `lon.csv` (cột `ma,loai,so_tien`, mọi dòng là `nap` và `100`) — lần một `2000` dòng, lần hai `20000` dòng. Với mỗi tệp: `tracemalloc.start()`, gọi `tong_theo_loai` (nạp từ mô-đun đã ghi, ví dụ `exec(MODULE, ns)` hay `sys.path.insert(0, thu_muc)` rồi `from phan_tich import tong_theo_loai`), lấy đỉnh bộ nhớ bằng `tracemalloc.get_traced_memory()[1]`, rồi `tracemalloc.stop()`. In đúng một dòng: `Bo nho khi dong tang 10 lan: gan nhu khong doi` nếu đỉnh ở 20000 dòng nhỏ hơn 3 lần đỉnh ở 2000 dòng, ngược lại `Bo nho khi dong tang 10 lan: tang theo so dong`. (Lab chấm hình dạng của kết quả, không chấm số byte tuyệt đối vì mỗi máy một khác.)

**Cách nạp mô-đun vừa ghi từ thư mục tạm** (chọn một; làm khi thư mục tạm còn tồn tại, tức còn trong khối `with`):

```python
# Cách 1: sys.path là danh sách thư mục mà máy tìm mô-đun, theo thứ tự; chèn thư mục tạm lên đầu rồi nạp như thường
import sys
sys.path.insert(0, str(thu_muc))
from phan_tich import tong_theo_loai

# Cách 2: chạy chuỗi mã MODULE vào một từ điển rỗng, rồi lấy hàm ra từ đó
ns = {}
exec(MODULE, ns)                      # exec chạy một chuỗi mã như chạy một tệp
tong_theo_loai = ns["tong_theo_loai"]
```

**Thời gian:** bài này nặng nhất khoá, dự kiến 45 đến 60 phút. Video dừng 20 phút cho lượt đầu (hàm chấm và ba tệp); phần đo làm ở lượt sau, tiếp tục sau khi video chạy lại. Dự án nhỏ mẫu (`tong_tien.py` + `test_tong_tien.py`) ở phần ví dụ của bài là hình mẫu cho cấu trúc ba tệp.

Chạy: `python du_an.py` (kỳ vọng `Tong diem: 10/10` rồi dòng đo). Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L13 du_an.py`.
""", "py", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("đo ở hai quy mô rồi ngoại suy: bộ nhớ và thời gian", "cả tệp: bộ nhớ tăng theo số dòng, sẽ chết khi tệp vượt bộ nhớ", "từng dòng hoặc từng khối: bộ nhớ không đổi, thời gian tuyến tính",
                 "chỉ thống kê gộp được mới cộng dồn theo khối", "mã chia mô-đun, ca kiểm từ đặc tả, môi trường ghim phiên bản", "kiểm tổng bằng một đường thứ hai sau mỗi thay đổi thiết kế"),
           """Tổng kết chuỗi logic. Đo ở hai quy mô rồi ngoại suy. Đọc cả tệp thì bộ nhớ tỉ lệ với số dòng. Đọc từng dòng hoặc từng khối thì bộ nhớ không đổi và thời gian tuyến tính. Chỉ thống kê gộp được mới cộng dồn theo khối.
           Và kiểm tổng bằng một đường thứ hai sau mỗi thay đổi."""),
        st("""<div class='box key'><b>Tư duy của người làm nghề:</b> một chương trình đúng hôm nay chưa chắc đúng ở quy mô ngày mai. <b>Hỏi “khi dữ liệu lớn gấp trăm lần thì cái gì gãy trước?”</b>, đo để biết, giữ ca kiểm để thay đổi mà không sợ, và ghi lại môi trường để người khác chạy lại được.</div>
<p>Từ giờ, mọi chương trình bạn gặp về sau dùng đúng những mảnh này: giá trị, hàm, cấu trúc dữ liệu, tệp, lớp, ngoại lệ, thư viện, kiểm thử.</p>""",
           """Tư duy của người làm nghề, một chương trình đúng hôm nay chưa chắc đúng ở quy mô ngày mai, nên hãy hỏi khi dữ liệu lớn gấp trăm lần thì cái gì gãy trước. Đo để biết, giữ ca kiểm, và ghi lại môi trường để người khác chạy lại được.
           Từ giờ, mọi chương trình bạn gặp sẽ dùng đúng những mảnh này, từ giá trị đến kiểm thử."""),
    ])
    return nbsp_spec(lesson("L13", "tinh_huong_phan_tich_tep_lon", "Bài 13 — Tình huống chuyên gia: phân tích tệp giao dịch từ một nghìn đến một trăm triệu dòng",
                  "curriculum/pyt.yaml L13; audit/pyt/verify_pyt.py L13 (chạy thật trên Python 3.11, labs/.venv-pyt; thời gian và đỉnh bộ nhớ của ba cách đọc ở 10^3 và 10^6 dòng đo bằng verify_pyt, máy kiểm, số minh hoạ; ngoại suy 10^8 tuyến tính; tình huống là giả định minh hoạ, không phải sự cố có thật); "
                  "pandas documentation: Scaling to large datasets, IO tools (chunksize); Python Library Reference: csv, tracemalloc; Python Packaging User Guide: Requirements files",
                  ["Đo thời gian và bộ nhớ của ba cách đọc tệp ở hai quy mô và ngoại suy lên quy mô lớn",
                   "Giải thích vì sao thiết kế phải đổi khi số dòng tăng bậc",
                   "Nêu cách đọc hợp lý cho từng quy mô và điều kiện áp dụng",
                   "Cộng dồn kết quả qua các khối và kiểm bằng tổng chung",
                   "Phân biệt thống kê gộp được với không gộp được theo khối",
                   "Chỉ ra ba lỗi hay gặp: quên cộng dồn, tối ưu trước khi đo, nhầm thống kê gộp được",
                   "Dựng dự án nhỏ gồm mô-đun, ca kiểm và danh sách thư viện ghim, và tự chấm bằng thang điểm"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  assumes=["pyt_ngoai_suy", "pyt_bien_dich", "pyt_perf_counter", "pyt_tracemalloc", "pyt_ngoai_le", "pyt_assert", "pyt_subprocess", "pyt_sys_executable", "pyt_capture_output"],
                  covers=[(1, "formula"), (2, "formula"), (3, "scale"), (4, "check"), (5, "pitfalls"), (6, "pitfalls"), (7, "example"), (7, "practice")]))
