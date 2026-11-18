import lib2
from lib2 import *
from l16 import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
_st0 = st


def st(show, say, **kw):
    """Lời đọc: tên ngoại chưa có luật đọc → diễn đạt tiếng Việt (tên gốc vẫn hiện trên màn hình)."""
    return _st0(show, say.replace("trigger", "đoạn lệnh tự chạy").replace("sqlite", "cơ sở dữ liệu nhỏ"), **kw)

from labkit import write_lab, practice_steps, practice_scene
from libj import jstep, nowrap

lib2.begin("L29")

# ── Mã chạy THẬT: Python 3 + sqlite3 (thư viện chuẩn). Đầu ra tất định: đếm sự kiện, số dư, không in thời gian (đệm ở audit/bnx/progcache/L29.json) ──
PY_KHO = prog("KhoSuKien", r'''
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE su_kien (seq INTEGER PRIMARY KEY AUTOINCREMENT, tk TEXT, loai TEXT, tien INTEGER);
CREATE TRIGGER khong_sua BEFORE UPDATE ON su_kien
BEGIN SELECT RAISE(ABORT, 'kho su kien chi them, khong sua'); END;
CREATE TRIGGER khong_xoa BEFORE DELETE ON su_kien
BEGIN SELECT RAISE(ABORT, 'kho su kien chi them, khong xoa'); END;
""")
def ghi(tk, loai, tien):
    db.execute("INSERT INTO su_kien (tk, loai, tien) VALUES (?, ?, ?)", (tk, loai, tien))
ghi("001", "NAP", 1000)
ghi("001", "RUT", 300)
ghi("001", "NAP", 50)
try:
    db.execute("UPDATE su_kien SET tien = 900 WHERE seq = 2")
except sqlite3.DatabaseError as e:
    print("sua su kien:", e)
try:
    db.execute("DELETE FROM su_kien WHERE seq = 2")
except sqlite3.DatabaseError as e:
    print("xoa su kien:", e)
print("so su kien:", db.execute("SELECT COUNT(*) FROM su_kien").fetchone()[0])
''', lang="python", claims=["kho sự kiện chỉ thêm: UPDATE và DELETE bị chặn, còn 3 sự kiện"])

PY_PHAT = prog("PhatLai", r'''
SU_KIEN = [("NAP", 1000), ("RUT", 300), ("NAP", 50), ("RUT", 120)]

def ap_dung(so_du, su_kien):
    loai, tien = su_kien
    return so_du + tien if loai == "NAP" else so_du - tien

so_du = 0
for i, sk in enumerate(SU_KIEN, 1):
    so_du = ap_dung(so_du, sk)
    print(f"sau su kien {i}: {so_du}")
print("phat lai tu dau:", sum(1 for _ in SU_KIEN), "su kien ->", so_du)
''', lang="python", claims=["số dư dựng lại bằng phát lại sự kiện: 1000, 700, 750, 630"])

PY_BUCHU = prog("BuChu", r'''
from functools import reduce

def ap_dung(so_du, su_kien):
    loai, tien = su_kien
    return so_du + tien if loai == "NAP" else so_du - tien

kho = [("NAP", 1000), ("RUT", 300), ("NAP", 50), ("RUT", 120)]
sai = ("RUT", 500)       # ghi nhầm, đáng ra 50
kho.append(sai)
print("sau su kien sai:", reduce(ap_dung, kho, 0))
kho.append(("NAP", 500))  # sự kiện bù
kho.append(("RUT", 50))   # sự kiện đúng
print("sau khi bu:", reduce(ap_dung, kho, 0), "|", len(kho), "su kien")
''', lang="python", claims=["sửa sai bằng sự kiện bù: số dư đúng 580, kho có 7 sự kiện"])

PY_BANCHUP = prog("BanChup", r'''
def doc_bao_nhieu(n, k):
    """Số sự kiện phải đọc tại sự kiện thứ n.
    k = 0: không bản chụp, đọc hết n; k > 0: nạp bản chụp, đọc phần dư."""
    return n if k == 0 else n % k

for n in (2500, 2500500):
    print(f"{n} su kien: khong ban chup doc {doc_bao_nhieu(n, 0)}, chup moi 1000 su kien doc {doc_bao_nhieu(n, 1000)}")
''', lang="python", claims=["quy mô: 2 500 và 2 500 500 sự kiện; có bản chụp mỗi 1000 sự kiện thì chỉ đọc 500"])

PY_DOC = prog("DocTre", r'''
su_kien = []                       # kho ghi: nguồn sự thật
doc = {"001": 0}                   # mô hình đọc (bảng tóm tắt)
da_xu_ly = 0                       # vị trí đã chiếu

def ghi(loai, tien):
    su_kien.append((loai, tien))

def chieu(toi_da):
    global da_xu_ly
    while da_xu_ly < len(su_kien) and toi_da > 0:
        loai, tien = su_kien[da_xu_ly]
        doc["001"] += tien if loai == "NAP" else -tien
        da_xu_ly += 1
        toi_da -= 1

ghi("NAP", 1000); ghi("RUT", 300); ghi("NAP", 50)
chieu(2)
print("doc sau khi chieu 2/3 su kien:", doc["001"], "(da xu ly", da_xu_ly, "/", len(su_kien), ")")
chieu(5)
print("doc sau khi chieu het:", doc["001"], "(da xu ly", da_xu_ly, "/", len(su_kien), ")")
''', lang="python", claims=["mô hình đọc đọc trễ: 700 khi mới chiếu 2/3 sự kiện, 750 khi chiếu hết"])

PY_SCALE = prog("QuyMoPhat", r'''
import sqlite3
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE sk (seq INTEGER PRIMARY KEY, loai INTEGER, tien INTEGER)")
db.executemany("INSERT INTO sk (loai, tien) VALUES (?, ?)",
               ((i % 2, i % 97 + 1) for i in range(1000000)))
def dung_lai(toi):
    so_du, dem = 0, 0
    for loai, tien in db.execute("SELECT loai, tien FROM sk WHERE seq <= ?", (toi,)):
        so_du += tien if loai == 0 else -tien
        dem += 1
    return so_du, dem
for n in (1000, 1000000):
    so_du, dem = dung_lai(n)
    print(f"{n} su kien: da doc {dem} su kien, so du {so_du}")
''', lang="python", timeout=200, claims=["dựng lại số dư từ 10^3 và 10^6 sự kiện: đọc đúng ngần ấy sự kiện"])

# ── Lab (cham.sh, Python) ──
LAB_PY = r'''
def ap_dung(so_du, sk):
    loai, tien = sk
    return so_du + tien if loai == "NAP" else so_du - tien


def phat_lai(kho, tu=0, so_du=0):
    for sk in kho[tu:]:
        so_du = ap_dung(so_du, sk)
    return so_du


kho = [("NAP", 500), ("RUT", 100), ("NAP", 200), ("RUT", 50), ("NAP", 25), ("RUT", 75)]
print("phat lai het:", phat_lai(kho), "(doc", len(kho), "su kien)")
ban_chup = (4, phat_lai(kho[:4]))
print("ban chup tai su kien", ban_chup[0], ":", ban_chup[1])
print("phat lai tu ban chup:", phat_lai(kho, ban_chup[0], ban_chup[1]), "(doc", len(kho) - ban_chup[0], "su kien)")
kho += [("RUT", 300), ("NAP", 300)]
print("sau khi bu su kien rut nham:", phat_lai(kho))
'''
LAB_OUT = """phat lai het: 500 (doc 6 su kien)
ban chup tai su kien 4 : 550
phat lai tu ban chup: 500 (doc 2 su kien)
sau khi bu su kien rut nham: 500"""
LAB_DE = """# Lab BNX L29 — Phát lại sự kiện, bản chụp và sự kiện bù

Kho sự kiện của một tài khoản (số minh hoạ), theo thứ tự: `NAP 500`, `RUT 100`, `NAP 200`, `RUT 50`, `NAP 25`, `RUT 75`. Số dư = phát lại từ 0: `NAP` cộng, `RUT` trừ.

Viết `mau.py`:
1. Hàm `phat_lai(kho, tu=0, so_du=0)`: áp dụng các sự kiện từ vị trí `tu` (đếm từ 0) bắt đầu với `so_du`. In `phat lai het: <số dư> (doc <n> su kien)`.
2. Bản chụp sau 4 sự kiện đầu: in `ban chup tai su kien 4 : <số dư>`, rồi phát lại phần còn lại từ bản chụp và in `phat lai tu ban chup: <số dư> (doc <m> su kien)`.
3. Giả sử có thêm một sự kiện `RUT 300` bị GHI NHẦM vào cuối kho (thêm nó: kho thành 7 sự kiện). Không sửa, không xoá nó: thêm sự kiện bù `NAP 300` ở cuối (kho thành 8 sự kiện), phát lại toàn bộ rồi in số dư mới: `sau khi bu su kien rut nham: <số dư>`.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L29 mau.py`.
"""

PY_SODU = prog("BangSoDu", r'''
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE tk (so TEXT PRIMARY KEY, so_du INTEGER)")
db.execute("INSERT INTO tk VALUES ('001', 0)")
for loai, tien in [("NAP", 1000), ("RUT", 300), ("NAP", 50), ("RUT", 120)]:
    dau = 1 if loai == "NAP" else -1
    db.execute("UPDATE tk SET so_du = so_du + ? WHERE so = '001'", (dau * tien,))
print("bang so du:", db.execute("SELECT so_du FROM tk").fetchone()[0], "- khong the biet 630 den tu dau")
print("so_du sau 3 lan cap nhat dau tien: khong con de doc lai")
''', lang="python", claims=["bảng số dư chỉ giữ giá trị cuối 630"])


def build():
    write_lab("BNX", "L29", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Số dư 630: bảng chỉ nhớ con số, kho sự kiện nhớ cả đường đi", [
        st("""<p>Hai cách giữ số dư của một tài khoản qua bốn giao dịch: nạp 1000, rút 300, nạp 50, rút 120.</p>
<div class="box key">Cách 1 (một bảng số dư, mỗi giao dịch <b>sửa</b> con số): còn <b>630</b>, nhưng không ai trả lời được &laquo;630 đến từ đâu&raquo;. Cách 2 (<b>kho sự kiện chỉ thêm</b>): cũng <b>630</b> và còn đủ bốn sự kiện.
Sự kiện nhập sai thì sửa ra sao khi kho cấm sửa? Và 10⁶ sự kiện thì dựng lại số dư mất bao nhiêu lần đọc?</div>""",
           """Chào bạn, hai cách giữ số dư qua bốn giao dịch: nạp một nghìn, rút ba trăm, nạp năm mươi, rút một trăm hai mươi. Cách một là bảng số dư mà mỗi giao dịch sửa con số, còn sáu trăm ba mươi nhưng không ai biết nó từ đâu. Cách hai là kho sự kiện chỉ thêm, cũng ra sáu trăm ba mươi và còn đủ bốn sự kiện. Sự kiện sai thì sửa ra sao khi kho cấm sửa, và một triệu sự kiện thì mất bao nhiêu lần đọc?""", focus=[1, 2, 2, 2, 2, 2]),
    ], checks=["alg.bnx_l29_replay([('NAP', 1000), ('RUT', 300), ('NAP', 50), ('RUT', 120)]) == 630"])

    pre = sc("prereq", "prereq", "Trước hết: sáu điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① sự kiện (event)", "ghi lại <b>điều đã xảy ra</b>, thì quá khứ, không đổi được", "<code>NAP 1000</code> trên tài khoản 001"],
                  ["② số dư là suy ra", "số dư không phải dữ liệu gốc: nó là <b>tổng</b> của các sự kiện", "1000 − 300 + 50 − 120 = 630"],
                  ["③ chỉ thêm (append-only)", "chỉ ghi thêm vào cuối, không sửa, không xoá", "như sổ cái có bút mực"],
                  ["④ trigger", "đoạn lệnh cơ sở dữ liệu tự chạy trước hoặc sau một lệnh ghi", "chặn <code>UPDATE</code> và <code>DELETE</code>"],
                  ["⑤ bản chiếu (projection)", "bảng tóm tắt <b>dựng từ sự kiện</b> để đọc nhanh; có thể xoá và dựng lại", "bảng số dư theo tài khoản"],
                  ["⑥ <b>CQRS</b> và <b>Event Sourcing</b>", "CQRS (Command Query Responsibility Segregation): tách mô hình <b>ghi</b> khỏi mô hình <b>đọc</b>. Event Sourcing: lưu <b>chuỗi sự kiện</b> làm nguồn sự thật, không lưu con số cuối", "bài này làm cả hai: kho sự kiện để ghi, bảng số dư để đọc"]]),
           """Trước hết ta cần hiểu sáu điều. Sự kiện ghi lại điều đã xảy ra và không đổi được. Số dư là tổng các sự kiện, không phải dữ liệu gốc. Chỉ thêm nghĩa là chỉ ghi vào cuối, không sửa, không xoá. Đoạn lệnh tự chạy là đoạn lệnh của cơ sở dữ liệu chạy quanh một lệnh ghi. Bản chiếu là bảng tóm tắt dựng từ sự kiện để đọc nhanh, và dựng lại được. Hai tên viết tắt trên màn hình là tách mô hình ghi khỏi mô hình đọc, và lưu chuỗi sự kiện làm nguồn sự thật.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"], introduces=["bnx_cqrs", "bnx_event_sourcing"]),
    ], checks=["1000 - 300 + 50 - 120 == 630"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên", "nghĩa"],
                 [["<code>NAP</code>, <code>RUT</code>", "hai loại sự kiện: nạp thì cộng, rút thì trừ"],
                  ["<code>seq</code>", "số thứ tự tăng dần của sự kiện trong kho: thứ tự là một phần của sự thật"],
                  ["<code>CREATE TRIGGER … BEFORE UPDATE ON su_kien BEGIN … END</code>", "đoạn tự chạy trước mỗi lệnh sửa của bảng; bên trong, <code>RAISE(ABORT, …)</code> huỷ lệnh đang chạy và báo lỗi"],
                  ["phát lại (replay)", "đọc sự kiện từ đầu và áp dụng lần lượt để dựng trạng thái"],
                  ["bản chụp (snapshot)", "số dư đã dựng tại một vị trí; lần sau chỉ phát lại phần sau nó"],
                  ["sự kiện bù", "sự kiện mới đảo ngược tác dụng của một sự kiện sai, thay vì sửa nó"]]),
           """Hai loại sự kiện là nạp thì cộng và rút thì trừ. Số thứ tự tăng dần cho biết thứ tự, một phần của sự thật. Đoạn lệnh tự chạy trước mỗi lệnh sửa, và lệnh huỷ bên trong dừng lệnh đang chạy rồi báo lỗi. Phát lại là áp dụng sự kiện từ đầu để dựng trạng thái. Bản chụp là số dư đã dựng tại một vị trí, để chỉ phát lại phần sau nó. Sự kiện bù đảo ngược tác dụng của một sự kiện sai, thay vì sửa nó.""",
           focus=["1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
    ], checks=["alg.bnx_l29_replay([('NAP', 5), ('RUT', 2)]) == 3"])

    intu = sc("intuition", "intuition", "Hình dung: tách ghi và đọc, và bản chụp", [
        st(svg(1500, 500,
               txt(750, 40, "Tách ghi và đọc: phía ghi chỉ thêm sự kiện, phía đọc giữ bản chiếu", 26, "middle", "#1f2937", True),
               box(40, 150, 240, 100, ["lệnh ghi", "nạp / rút"], C_GRAY, 22, True),
               box(360, 120, 360, 160, ["kho sự kiện", "chỉ thêm, có số thứ tự", "NAP 1000, RUT 300", "NAP 50, RUT 120"], C_BLUE, 22, True),
               box(820, 150, 280, 100, ["bộ chiếu", "đọc sự kiện mới, cập nhật"], C_AMBER, 22),
               box(1200, 120, 260, 160, ["mô hình đọc", "bảng số dư: 630", "truy vấn nhanh"], C_GREEN, 22, True),
               arrow(285, 200, 355, 200), arrow(725, 200, 815, 200), txt(770, 150, "theo", 20), txt(770, 174, "thứ tự", 20), arrow(1105, 200, 1195, 200),
               box(360, 350, 740, 80, ["kho là nguồn sự thật: mô hình đọc hỏng thì xoá và chiếu lại từ đầu"], C_PURPLE, 22),
               txt(750, 470, "Đánh đổi: đọc có thể trễ so với ghi (chấp nhận được khi nào, xem phần ví dụ)", 24, "middle", "#1f2937", True)),
           """Hình này tách ghi và đọc. Lệnh ghi chỉ thêm sự kiện vào kho, kho có số thứ tự và không sửa được.
           Bộ chiếu đọc sự kiện mới theo thứ tự rồi cập nhật bảng số dư cho truy vấn nhanh.
           Kho là nguồn sự thật, nên mô hình đọc hỏng thì chiếu lại từ đầu. Đánh đổi là phía đọc có thể trễ."""),
        st(svg(1500, 460,
               txt(750, 40, "Bản chụp: dựng số dư tại sự kiện 2 500 500 mà không đọc từ đầu", 26, "middle", "#1f2937", True),
               box(40, 120, 1420, 70, ["sự kiện 1 … 1 000 … 2 000 … 2 500 000 (bản chụp) … 2 500 500"], C_GRAY, 22),
               box(40, 230, 640, 80, ["không bản chụp: đọc 2 500 500 sự kiện"], C_RED, 22, True),
               box(760, 230, 700, 80, ["có bản chụp mỗi 1 000: nạp bản chụp rồi đọc 500 sự kiện"], C_GREEN, 22, True),
               txt(750, 380, "số lần đọc có bản chụp: n mod 1 000 (tối đa 999), không tăng theo cỡ kho", 24, "middle", "#1f2937", True)),
           """Hình thứ hai là bản chụp, để biết số dư tại sự kiện hai triệu năm trăm nghìn năm trăm mà không đọc từ đầu. Không có bản chụp thì phải đọc hết. Có bản chụp mỗi một nghìn sự kiện thì nạp bản chụp gần nhất rồi chỉ đọc năm trăm, tối đa chín trăm chín mươi chín."""),
    ], checks=["alg.bnx_l29_events_to_read(2500, 0) == 2500 and alg.bnx_l29_events_to_read(2500, 1000) == 500", "alg.bnx_l29_events_to_read(2500500, 1000) == 500"])

    form = sc("formula", "formula", "Suy ra từng bước: từ sự kiện tới số dư", [
        jstep([(("<code>sqlite3.connect(\":memory:\")</code>, <code>db.executescript(\"\"\"…\"\"\")</code>", "mở một cơ sở dữ liệu nhỏ nằm trong bộ nhớ, tắt chương trình là mất; <code>executescript</code> chạy nhiều lệnh SQL (câu lệnh nói với cơ sở dữ liệu) viết giữa ba dấu nháy kép", "Mở cơ sở dữ liệu nhỏ trong bộ nhớ rồi chạy một loạt lệnh viết giữa ba dấu nháy kép."), "kho tạm, không để lại tệp", ""),
               (("<code>CREATE TABLE su_kien (seq INTEGER PRIMARY KEY AUTOINCREMENT, tk TEXT, …)</code>", "tạo bảng: mỗi cột là tên rồi kiểu (<code>INTEGER</code> số nguyên, <code>TEXT</code> chữ); <code>PRIMARY KEY AUTOINCREMENT</code>: cột không trùng, tự tăng 1, 2, 3 ở mỗi dòng mới", "Tạo bảng gồm các cột, mỗi cột có tên và kiểu, và cột khoá chính tự tăng một ở mỗi dòng mới."), "dòng đầu có <code>seq</code> = 1", ""),
               (("<code>INSERT OR REPLACE</code>, <code>DROP TRIGGER</code>, chuỗi băm", "<code>INSERT OR REPLACE</code>: ghi đè dòng cùng <code>seq</code>; <code>DROP TRIGGER</code>: gỡ đoạn tự chạy; chuỗi băm: mỗi sự kiện kèm mã băm có cả mã băm sự kiện trước, nên sửa lén một sự kiện làm đứt chuỗi", "Ba chỗ hở của việc chặn: ghi đè, gỡ đoạn tự chạy, và chuỗi băm là cách phát hiện sửa lén."), "", "")],
              intro="Mã dựng kho dùng ba chỗ mới nên ta giải trước.", introduces=["bnx_ma_bam"]),
        st("""<p><b>Bước 1.</b> Muốn mọi con số có thể giải thích, ta ghi <b>điều đã xảy ra</b> thay vì ghi con số. Mỗi giao dịch là một dòng thêm vào cuối kho, với số thứ tự tăng dần.</p>"""
           + PY_KHO.show(lines=(3, 10), title="KhoSuKien.py (trích): bảng sự kiện và hai trigger chặn sửa, xoá")
           + """<p class="note"><b>Giới hạn:</b> hai trigger chỉ chặn lệnh <code>UPDATE</code> và <code>DELETE</code> thông thường. <code>INSERT OR REPLACE</code> vẫn ghi đè sự kiện cùng <code>seq</code> (đo trên SQLite 3.49), còn <code>DROP TRIGGER</code> và <code>DROP TABLE</code> vẫn chạy. Nên cần thêm quyền tối thiểu và chuỗi băm nối các sự kiện để phát hiện sửa lén.</p>""",
           """Bước một: để con số giải thích được, ta ghi điều đã xảy ra thay vì ghi con số, mỗi giao dịch là một dòng thêm vào cuối kho. Hai đoạn lệnh tự chạy chặn lệnh sửa và xoá thông thường, nhưng lệnh ghi đè hay gỡ vẫn lách được, nên cần thêm quyền tối thiểu và chuỗi băm.""",
           clear=True),
        st("""<p><b>Bước 2. Số dư là kết quả phát lại.</b> Bắt đầu từ 0, áp dụng từng sự kiện theo thứ tự: nạp cộng, rút trừ. Cùng kho thì luôn ra cùng số dư.</p>"""
           + """$$0 + 1000 = 1000;\\;\\; 1000 - 300 = 700;\\;\\; 700 + 50 = 750;\\;\\; 750 - 120 = \\hl{630}$$""",
           """Bước hai, số dư là kết quả phát lại: bắt đầu từ không, áp dụng từng sự kiện theo thứ tự, nạp cộng, rút trừ. Cùng một kho thì ra cùng một số dư, và số dư cuối là sáu trăm ba mươi.""", focus=[1, 2],
           clear=True),
        st("""<p><b>Bước 3. Tách ghi và đọc.</b> Truy vấn &laquo;số dư?&raquo; mà phát lại cả kho mỗi lần thì chậm. Nên phía ghi chỉ thêm sự kiện, còn một <b>bộ chiếu</b> đọc sự kiện mới và cập nhật <b>bản chiếu</b> (bảng số dư) cho truy vấn nhanh. Bản chiếu chạy <b>sau</b> kho nên có thể <b>trễ</b>.</p>""",
           """Bước ba tách ghi và đọc. Phát lại cả kho mỗi lần hỏi thì chậm, nên phía ghi chỉ thêm sự kiện, còn bộ chiếu cập nhật bảng số dư cho truy vấn nhanh. Bản chiếu chạy sau kho nên có thể trễ.""",
           clear=True),
        st("""<p><b>Bước 4. Sự kiện sai thì bù.</b> Không sửa được, nên thêm sự kiện <b>đảo ngược</b> rồi thêm sự kiện đúng. Lịch sử giữ nguyên cả cái sai lẫn cách sửa, nên kiểm toán thấy hết.</p>"""
           + """$$630 - 500 = 130 \\;\\Rightarrow\\; 130 + 500 = 630 \\;\\Rightarrow\\; 630 - 50 = \\hl{580}$$""",
           """Bước bốn, sự kiện sai thì bù: không sửa được nên ta thêm sự kiện đảo ngược rồi sự kiện đúng.
           Lịch sử giữ cả cái sai lẫn cách sửa, và số dư đúng là năm trăm tám mươi.""",
           clear=True),
        st("""<p><b>Bước 5. Bản chụp.</b> Phát lại từ đầu tốn thời gian tỉ lệ với số sự kiện. Cứ mỗi <b>k</b> sự kiện, lưu số dư tại đó. Dựng số dư tại sự kiện thứ <b>n</b>: nạp bản chụp gần nhất, đọc phần dư.</p>"""
           + """$$\\text{số lần đọc} = \\text{(n chia lấy dư cho k)} \\quad (k = 1000,\\; n = 2\\,500\\,500 \\Rightarrow \\hl{500})$$""",
           """Bước năm là bản chụp. Phát lại từ đầu tốn thời gian tỉ lệ với số sự kiện, nên cứ mỗi k sự kiện ta lưu số dư. Dựng số dư tại sự kiện thứ n thì nạp bản chụp gần nhất rồi đọc phần dư, tức n chia lấy dư cho k: với k bằng một nghìn, chỉ đọc năm trăm.""",
           clear=True),
    ], checks=["alg.bnx_l29_replay([('NAP', 1000), ('RUT', 300), ('NAP', 50), ('RUT', 120)]) == 630", "alg.bnx_l29_replay([('NAP', 1000), ('RUT', 300), ('NAP', 50), ('RUT', 120), ('RUT', 500)]) == 130",
               "alg.bnx_l29_replay([('NAP', 1000), ('RUT', 300), ('NAP', 50), ('RUT', 120), ('RUT', 500), ('NAP', 500), ('RUT', 50)]) == 580", "2500500 % 1000 == 500"])

    ex = sc("example", "example", "Ví dụ chạy thật, từng phép tính", [
        jstep([(("<code>def ghi(tk, loai, tien):</code>, <code>ghi(\"001\", \"NAP\", 1000)</code>", "khai hàm <code>ghi</code> nhận ba đối số; dòng sau gọi nó với ba giá trị cụ thể", "Hàm ghi nhận ba đối số, và dòng sau gọi nó với ba giá trị cụ thể."), "mỗi lần gọi thêm một sự kiện", ""),
               (("<code>INSERT INTO su_kien (tk, loai, tien) VALUES (?, ?, ?)</code>", "thêm một dòng vào bảng; mỗi <code>?</code> là chỗ giữ, bộ ngoặc theo sau điền giá trị vào đúng thứ tự", "Lệnh thêm một dòng, mỗi dấu hỏi là chỗ giữ được điền theo thứ tự."), "<code>('001', 'NAP', 1000)</code>", ""),
               (("<code>UPDATE su_kien SET tien = 900 WHERE seq = 2</code>, <code>DELETE FROM su_kien WHERE seq = 2</code>", "<code>UPDATE … SET … WHERE</code>: sửa cột của các dòng thoả điều kiện; <code>DELETE FROM … WHERE</code>: xoá các dòng thoả điều kiện", "Một lệnh sửa cột của dòng thoả điều kiện, một lệnh xoá dòng thoả điều kiện."), "cả hai nhắm dòng có <code>seq</code> bằng 2", "")],
              intro="Trước khi đọc mã, ta giải các lệnh viết trong đó."),
        jstep([(("<code>try: … except sqlite3.DatabaseError as e:</code>", "chạy thử lệnh; cơ sở dữ liệu báo lỗi thì nhảy sang <code>except</code>, biến <code>e</code> giữ thông báo", "Khối thử chạy lệnh, nếu cơ sở dữ liệu báo lỗi thì nhảy sang phần bắt lỗi, nơi biến giữ thông báo."), "in <code>kho su kien chi them, khong sua</code>", ""),
               (("<code>SELECT COUNT(*) FROM su_kien</code>, <code>.fetchone()[0]</code>", "<code>COUNT(*)</code> đếm số dòng; <code>fetchone()</code> lấy dòng kết quả đầu, <code>[0]</code> lấy cột đầu của dòng đó", "Lệnh đếm số dòng, rồi lấy dòng kết quả đầu và cột đầu của nó."), "dòng <code>(3,)</code> cho <code>3</code>", "")]),
        st(PY_KHO.show(lines=(11, 24), title="KhoSuKien.py (trích): ghi ba sự kiện rồi thử sửa và xoá"),
           """Ta chạy thật bằng Python và cơ sở dữ liệu nhỏ trong bộ nhớ. Chương trình ghi ba sự kiện, rồi thử sửa số tiền của sự kiện thứ hai và thử xoá nó.""",
           clear=True),
        st(PY_KHO.out_html()
           + """$$① \\; \\text{sửa} \\Rightarrow \\text{bị chặn}; \\;\\; \\text{xoá} \\Rightarrow \\text{bị chặn}; \\;\\; \\text{kho còn } \\hlg{3} \\text{ sự kiện}$$""",
           """Phép tính thứ nhất, kết quả thật: lệnh sửa và lệnh xoá đều bị đoạn lệnh tự chạy huỷ, kho vẫn còn ba sự kiện. Lệnh ghi đè hay gỡ đoạn lệnh thì vẫn lách được.""",
           clear=True),
        jstep([(("<code>loai, tien = su_kien</code>, <code>so_du + tien if loai == \"NAP\" else so_du - tien</code>", "gán hai biến một lúc từ một cặp; <code>a if đk else b</code> cho a nếu điều kiện đúng, ngược lại cho b; <code>def</code> … <code>return</code>: hàm trả giá trị về chỗ gọi", "Tách một cặp thành hai biến, rồi chọn cộng hoặc trừ theo điều kiện, và hàm trả kết quả về chỗ gọi."), "<code>(\"NAP\", 1000)</code> thì <code>loai</code> là NAP, <code>tien</code> là 1000", ""),
               (("<code>for i, sk in enumerate(SU_KIEN, 1):</code>", "lặp qua danh sách, kèm số thứ tự bắt đầu từ 1", "Vòng lặp kèm số thứ tự bắt đầu từ một."), "<code>1 ('NAP', 1000)</code>, rồi <code>2 ('RUT', 300)</code>", ""),
               (("<code>f\"sau su kien {i}: {so_du}\"</code>", "chuỗi có chữ <code>f</code> đứng trước: mỗi <code>{…}</code> được thay bằng giá trị", "Chuỗi có chữ f thay mỗi cặp ngoặc nhọn bằng giá trị."), "<code>sau su kien 2: 700</code>", ""),
               (("<code>sum(1 for _ in SU_KIEN)</code>", "cộng một cho mỗi phần tử của danh sách, tức đếm số phần tử; <code>_</code> là tên bỏ đi, không dùng giá trị", "Cộng một cho mỗi phần tử tức là đếm, và gạch dưới là tên bỏ đi."), "4 sự kiện cho <code>4</code>", "")],
              intro="Đây là cách đọc phần phát lại."),
        st(PY_PHAT.show(lines=(1, 11), title="PhatLai.py: phát lại bốn sự kiện từ số dư 0"),
           """Phép tính thứ hai là phát lại: lặp qua bốn sự kiện, áp dụng từng cái vào số dư và in số dư sau mỗi sự kiện.""",
           clear=True),
        st(PY_PHAT.out_html()
           + """$$② \\; 1000 \\to 700 \\to 750 \\to \\hl{630}; \\quad 4 \\text{ sự kiện đọc}$$""",
           """Kết quả thật là một nghìn, bảy trăm, bảy trăm năm mươi, rồi sáu trăm ba mươi, đọc từ bốn sự kiện và có đủ vết để giải thích từng bước.""",
           clear=True),
        jstep([(("<code>from functools import reduce</code>, <code>reduce(ap_dung, kho, 0)</code>", "nạp hàm <code>reduce</code>; nó bắt đầu từ 0, đưa từng sự kiện của <code>kho</code> qua <code>ap_dung</code> cùng kết quả trước, ra một số", "Hàm rút gọn bắt đầu từ không, đưa từng sự kiện qua hàm áp dụng cùng kết quả trước, ra một số."), "<code>0</code> → <code>1000</code> → <code>700</code>", ""),
               (("<code>kho.append(sai)</code>, <code># ghi nhầm</code>", "<code>append</code> thêm một phần tử vào cuối danh sách; từ <code>#</code> tới hết dòng là ghi chú, máy bỏ qua", "Lệnh thêm một phần tử vào cuối danh sách, và dấu thăng mở đầu ghi chú mà máy bỏ qua."), "kho có thêm một sự kiện ở cuối", "")]),
        st(PY_BUCHU.show(lines=(7, 13), title="BuChu.py (trích): ghi nhầm rút 500, rồi bù, rồi ghi sự kiện đúng"),
           """Phép tính thứ ba là sự kiện bù: ghi nhầm rút năm trăm, đáng ra rút năm mươi. Không sửa mà thêm sự kiện nạp năm trăm để đảo ngược, rồi sự kiện rút năm mươi đúng.""", focus=[1, 2],
           clear=True),
        st(PY_BUCHU.out_html()
           + """$$③ \\; 630 - 500 = 130; \\;\\; 130 + 500 - 50 = \\hlg{580}; \\;\\; \\text{kho } 7 \\text{ sự kiện, không sửa cái nào}$$""",
           """Kết quả thật: sau sự kiện sai số dư là một trăm ba mươi, sau khi bù và ghi lại là năm trăm tám mươi, và kho có bảy sự kiện không sự kiện nào bị sửa.""",
           clear=True),
        st(table(["viết trong mã", "nghĩa", "ví dụ nhỏ"],
                 [["<code>global da_xu_ly</code>", "cho phép hàm gán lại biến nằm ngoài hàm; thiếu dòng này, Python tạo biến mới chỉ trong hàm và biến ngoài đứng yên", "<code>da_xu_ly += 1</code> làm tăng biến ngoài"],
                  ["<code>while da_xu_ly &lt; len(su_kien) and toi_da &gt; 0:</code>", "lặp khi cả hai điều kiện còn đúng: còn sự kiện chưa chiếu và còn lượt", "chiếu 2 trong 3 sự kiện thì dừng"],
                  ["<code>su_kien = []</code>, <code>su_kien.append((loai, tien))</code>", "danh sách rỗng, rồi thêm vào cuối một cặp", "kho ban đầu rỗng"],
                  ["<code>doc = {\"001\": 0}</code>, <code>doc[\"001\"] += tien</code>", "từ điển: khoá <code>\"001\"</code> có giá trị 0; <code>+=</code> cộng thêm vào giá trị đó", "tài khoản 001 bắt đầu từ 0"]]),
           """Hàm chiếu sửa một biến nằm ngoài hàm, nên có dòng khai báo toàn cục; thiếu nó thì biến ngoài đứng yên. Vòng lặp chạy khi còn sự kiện chưa chiếu và còn lượt. Kho là danh sách thêm vào cuối, mô hình đọc là từ điển khoá tài khoản.""",
           clear=True),
        st(PY_DOC.show(lines=(8, 14), title="DocTre.py (trích): bộ chiếu xử lý tối đa một số sự kiện mỗi lần"),
           """Phép tính thứ tư là đọc trễ: ghi ba sự kiện, cho bộ chiếu chạy hai, rồi đọc mô hình đọc.""",
           clear=True),
        st(PY_DOC.out_html()
           + """$$④ \\; \\text{mới chiếu } 2/3 \\Rightarrow \\hl{700}; \\quad \\text{chiếu hết} \\Rightarrow \\hlg{750}$$""",
           """Kết quả thật: mới chiếu hai trên ba sự kiện, mô hình đọc trả bảy trăm, một số cũ; chiếu hết thì trả bảy trăm năm mươi. Chấp nhận được khi chịu số cũ vài giây, không khi cần số dư chính xác.""", focus=[1, 3],
           clear=True),
    ], checks=["alg.bnx_l29_replay([('NAP', 1000), ('RUT', 300), ('NAP', 50)]) == 750 and alg.bnx_l29_replay([('NAP', 1000), ('RUT', 300)]) == 700",
               "alg.bnx_l29_replay([('NAP', 1000), ('RUT', 300), ('NAP', 50), ('RUT', 120), ('RUT', 500), ('NAP', 500), ('RUT', 50)]) == 580"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: bảng số dư tự cập nhật", [
        jstep([(("<code>CREATE TABLE tk (so TEXT PRIMARY KEY, so_du INTEGER)</code>, <code>INSERT INTO tk VALUES ('001', 0)</code>", "bảng hai cột: số tài khoản (không trùng) và số dư; lệnh thêm không liệt kê cột thì điền giá trị theo thứ tự cột", "Bảng có hai cột, và lệnh thêm không nêu tên cột thì điền giá trị theo thứ tự các cột."), "tài khoản 001 bắt đầu từ 0", ""),
               (("<code>for loai, tien in [(\"NAP\", 1000), …]:</code>, <code>dau = 1 if loai == \"NAP\" else -1</code>", "mỗi vòng tách một cặp thành hai biến; dấu là 1 nếu nạp, −1 nếu rút", "Mỗi vòng tách một cặp thành hai biến, và dấu là một nếu nạp, âm một nếu rút."), "rút 300 cho <code>dau * tien</code> = −300", ""),
               (("<code>UPDATE tk SET so_du = so_du + ? WHERE so = '001'</code>", "sửa số dư của tài khoản 001 thành giá trị cũ cộng thêm; giá trị cũ bị ghi đè", "Lệnh sửa số dư thành giá trị cũ cộng thêm, và giá trị cũ bị ghi đè."), "1000, rồi 700…", "")]),
        st(PY_SODU.show(lines=(3, 9), title="BangSoDu.py (trích): cách cũ, mỗi giao dịch SỬA con số trong một bảng"),
           """Ta kiểm bằng đường khác hẳn: cách cũ chỉ có một bảng số dư, mỗi giao dịch sửa chính con số đó, nên bảng chỉ còn con số mới nhất.""",
           clear=True),
        st(PY_SODU.out_html("""bang so du: 630 - khong the biet 630 den tu dau""") + table(["cách", "số dư", "trả lời được 'vì sao 630'?", "sửa được giao dịch sai?"],
                                                                                      [["bảng số dư (sửa tại chỗ)", "630", "không: chỉ còn con số cuối", "chỉ bằng cách sửa đè, mất dấu vết"],
                                                                                       ["kho sự kiện", "630", "có: bốn sự kiện", "bằng sự kiện bù, còn dấu vết"]]),
           """Cả hai cách cùng ra sáu trăm ba mươi. Khác biệt nằm ở câu hỏi kiểm toán: bảng số dư không biết vì sao, còn kho sự kiện trả lời được và sửa sai bằng sự kiện bù.""",
           focus=[1, 2, 3], clear=True),
    ], checks=["alg.bnx_l29_replay([('NAP', 1000), ('RUT', 300), ('NAP', 50), ('RUT', 120)]) == 1000 - 300 + 50 - 120 == 630"])

    quymo = sc("quymo", "example", "Khi kho lớn dần: bao nhiêu lần đọc để dựng số dư?", [
        jstep([(("<code>db.executemany(\"INSERT …\", ((i % 2, i % 97 + 1) for i in range(1000000)))</code>", "chạy một lệnh thêm cho mỗi bộ trong dãy; dãy sinh ra từng bộ <code>(i % 2, i % 97 + 1)</code> cho <code>i</code> từ 0 tới 999999 (<code>%</code> là phần dư)", "Chạy một lệnh thêm cho mỗi bộ giá trị trong dãy sinh sẵn, với i chạy từ không tới chín trăm chín mươi chín nghìn chín trăm chín mươi chín."), "<code>i = 5</code> cho <code>(1, 6)</code>", ""),
               (("<code>for loai, tien in db.execute(\"SELECT loai, tien FROM sk WHERE seq &lt;= ?\", (toi,)):</code>", "<code>SELECT … FROM … WHERE</code> lấy các dòng thoả điều kiện; <code>(toi,)</code> điền vào chỗ giữ; vòng lặp nhận từng dòng, tách thành hai biến", "Lệnh lấy các dòng thoả điều kiện, và vòng lặp nhận từng dòng, tách thành hai biến."), "<code>toi = 1000</code> lấy 1000 dòng đầu", ""),
               (("<code>so_du, dem = 0, 0</code>, <code>return so_du, dem</code>, <code>for n in (1000, 1000000):</code>", "gán hai biến cùng bằng 0; hàm trả hai giá trị; vòng lặp thử hai cỡ", "Gán hai biến cùng bằng không, hàm trả hai giá trị, và vòng lặp thử hai cỡ."), "", "")],
              intro="Mã đo quy mô có ba chỗ cần đọc trước."),
        st(PY_SCALE.show(lines=(3, 14), title="QuyMoPhat.py (trích): sinh một triệu sự kiện, rồi dựng số dư từ n sự kiện đầu")
           + """<p class="note">Dữ liệu sinh: số thứ tự chẵn là nạp, lẻ là rút, số tiền là <code>i % 97 + 1</code> (số minh hoạ).</p>""",
           """Đây là số đo thật. Chương trình sinh một triệu sự kiện, rồi hàm dựng lại đọc n sự kiện đầu và cộng trừ ra số dư. Ta thử với một nghìn sự kiện, rồi một triệu, gấp một nghìn lần.""", focus=[1, 1, 2],
           clear=True),
        st(PY_SCALE.out_html() + """<p class="note">Số dư âm là bình thường: dữ liệu sinh minh hoạ không chặn rút quá số dư.</p>""" + PY_BANCHUP.out_html("""2500 su kien: khong ban chup doc 2500, chup moi 1000 su kien doc 500
2500500 su kien: khong ban chup doc 2500500, chup moi 1000 su kien doc 500""", "TÍNH TỪ CÔNG THỨC n mod k (không đo kho thật): số lần đọc khi có và không có bản chụp")
           + """$$10^3 \\to 10^6 \\;(\\times 1000): \\; \\text{đọc } 1\\,000 \\to 1\\,000\\,000; \\quad \\text{có bản chụp: } 500 \\to 500$$""",
           """Kết quả đo thật là đọc đúng một nghìn rồi đúng một triệu sự kiện, nên chi phí dựng lại tăng theo cỡ kho. Hai dòng sau không đo kho thật mà tính từ công thức chia lấy dư: với bản chụp mỗi một nghìn sự kiện, hai cỡ kho đều chỉ đọc năm trăm. Bản chụp giữ chi phí dưới một nghìn.""",
           clear=True),
        st(table(["cách", "chi phí dựng số dư", "đánh đổi", "chọn khi"],
                 [["phát lại từ đầu", "tỉ lệ với số sự kiện: 10³ → 10⁶ lần đọc", "đơn giản, không dữ liệu phụ", "tài khoản ít giao dịch, kiểm toán một lần"],
                  ["bản chụp mỗi k sự kiện", "tối đa k − 1 lần đọc", "lưu thêm bản chụp; phải dựng lại khi đổi quy tắc áp dụng", "tài khoản nhiều giao dịch"],
                  ["bản chiếu chạy liên tục", "một lần đọc dòng đã dựng", "đọc trễ; thêm thành phần phải giám sát", "truy vấn số dư rất nhiều"]]),
           """Phát lại từ đầu đơn giản nhưng chi phí tỉ lệ với số sự kiện. Bản chụp giới hạn chi phí dưới k, đổi lại phải lưu thêm. Bản chiếu truy vấn nhanh nhất, đổi lại đọc có thể trễ.""",
           focus=[0, ["1.2", "1.3"], "1.4"], clear=True),
    ], checks=["alg.bnx_l29_events_to_read(1000000, 0) == 1000000 and 1000000 // 1000 == 1000", "alg.bnx_l29_events_to_read(2500500, 1000) == alg.bnx_l29_events_to_read(2500, 1000) == 500"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Dùng kho sự kiện nhưng <b class="red">vẫn cho sửa và xoá</b> &laquo;cho tiện&raquo;. Chạy thật: trigger chặn cả hai lệnh thông thường (<code>INSERT OR REPLACE</code> và gỡ trigger vẫn lách được, nên vẫn cần phân quyền). Một kho sửa được thì không còn là bằng chứng: kiểm toán mất giá trị.</div>"""
           + PY_KHO.out_html(),
           """Lỗi thứ nhất là dùng kho sự kiện nhưng vẫn cho sửa và xoá cho tiện. Đoạn lệnh tự chạy chặn lệnh thông thường, nhưng lệnh ghi đè hay gỡ nó vẫn lách được nên cần phân quyền.""", focus=[1, 3], clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Đọc <b class="red">mô hình đọc ngay sau khi ghi</b> và tin nó đã cập nhật. Chạy thật: mới chiếu 2 trên 3 sự kiện thì đọc ra 700 chứ không phải 750.
Cách chữa: khi cần chắc chắn (kiểm số dư trước khi rút), đọc từ kho hoặc kiểm vị trí đã chiếu; còn màn hình hiển thị thì chấp nhận trễ.</div>""",
           """Lỗi thứ hai: đọc mô hình đọc ngay sau khi ghi và tin nó đã cập nhật. Mới chiếu hai trên ba sự kiện thì đọc ra bảy trăm chứ không phải bảy trăm năm mươi. Khi cần chắc chắn, như trước khi rút, hãy đọc từ kho.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc tải tăng).</b> <b class="red">Phát lại từ đầu</b> cho mỗi lần hỏi số dư. Ở 10³ sự kiện thấy nhanh; ở 10⁶ là đọc 1 000 000 sự kiện mỗi lần. Chữa: bản chụp (đọc tối đa 999 sự kiện) hoặc bản chiếu chạy liên tục.</div>""",
           """Lỗi thứ ba: phát lại từ đầu cho mỗi lần hỏi số dư. Ở một nghìn sự kiện thấy nhanh, ở một triệu là đọc một triệu sự kiện mỗi lần. Chữa bằng bản chụp hoặc bản chiếu.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 4 (người đã đi làm, lúc vận hành lâu dài).</b> <b class="red">Đổi quy tắc áp dụng sự kiện</b> (ví dụ cách tính phí) mà bản chụp cũ vẫn dùng quy tắc cũ: số dư dựng từ bản chụp khác số dư phát lại từ đầu.
Cách chữa: gắn <b>phiên bản quy tắc</b> vào bản chụp, đổi quy tắc thì bỏ bản chụp cũ và dựng lại; thêm ca kiểm so hai đường.</div>""",
           """Lỗi thứ tư: đổi quy tắc mà bản chụp cũ vẫn dùng quy tắc cũ, nên số dư từ bản chụp khác số dư phát lại từ đầu. Chữa bằng cách gắn phiên bản quy tắc vào bản chụp.""", clear=True),
    ], checks=["alg.bnx_l29_replay([('NAP', 1000), ('RUT', 300)]) == 700", "alg.bnx_l29_events_to_read(999999, 1000) == 999"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Kho: <code>NAP 800</code>, <code>RUT 150</code>, <code>RUT 90</code>, <code>NAP 40</code>. Số dư? Nếu sự kiện <code>RUT 150</code> hoá ra là <code>RUT 15</code>, viết các sự kiện bù và số dư đúng."],
                  ["2", "Kho có 7 300 000 sự kiện, bản chụp mỗi 5 000. Dựng số dư tại sự kiện cuối phải đọc bao nhiêu sự kiện? Không bản chụp thì sao?"],
                  ["3", "Quyết định (số minh hoạ): màn hình tổng quan hiển thị số dư mỗi giây cho 100 000 khách; lệnh rút cần số dư chính xác. Chọn: phát lại, bản chiếu, hay lai? Vì sao?"]]),
           """Đến lượt bạn, ba câu làm ra giấy. Câu một, tính số dư của kho bốn sự kiện, rồi viết sự kiện bù nếu rút một trăm năm mươi hoá ra là rút mười lăm. Câu hai, kho có bảy triệu ba trăm nghìn sự kiện, bản chụp mỗi năm nghìn: dựng số dư tại sự kiện cuối phải đọc bao nhiêu, và không có bản chụp thì sao? Câu ba, số dư cho một trăm nghìn khách mà lệnh rút cần số chính xác: chọn phát lại, bản chiếu hay lai? Hãy dừng lại làm rồi xem đáp án.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=30),
        st("""<p>Câu 1: kho <code>NAP 800</code>, <code>RUT 150</code>, <code>RUT 90</code>, <code>NAP 40</code>; phát lại, rồi bù bằng sự kiện đảo ngược, rồi sự kiện đúng <code>RUT 15</code>.</p>
$$800 - 150 - 90 + 40 = \\hlg{600}; \\quad \\text{bù: } \\text{NAP } 150, \\text{ RUT } 15 \\Rightarrow 600 + 150 - 15 = \\hlg{735}$$""",
           """Đáp án câu một: phát lại ra sáu trăm. Để sửa, thêm sự kiện nạp một trăm năm mươi để đảo ngược rồi sự kiện rút mười lăm cho đúng, ra sáu trăm cộng một trăm năm mươi trừ mười lăm, bằng bảy trăm ba mươi lăm.""", focus=[[1], 2, 2]),
        st("""<p>Câu 2: số lần đọc = n chia lấy dư cho k; không bản chụp thì đọc hết.</p>
$$7\\,300\\,000 : 5000 = 1460 \\text{ dư } \\hlg{0} \\text{ (dùng đúng bản chụp cuối)}; \\quad \\text{không bản chụp: } \\hlg{7\\,300\\,000}$$""",
           """Đáp án câu hai, bảy triệu ba trăm nghìn chia hết cho năm nghìn, nên sự kiện cuối trùng đúng một bản chụp và không phải đọc sự kiện nào thêm. Không có bản chụp thì phải đọc cả bảy triệu ba trăm nghìn sự kiện."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["phát lại mỗi lần hỏi", "luôn chính xác, đơn giản", "mỗi lần hỏi phát lại hàng nghìn sự kiện, 100 000 khách hỏi mỗi giây: quá tải kho"],
                  ["bản chiếu chạy liên tục", "đọc nhanh, nhẹ cho kho", "có thể trễ: lệnh rút dựa trên số cũ có thể cho rút quá số dư"],
                  ["lai: bản chiếu cho màn hình, kiểm chính xác tại kho (hoặc theo vị trí đã chiếu) cho lệnh rút", "màn hình nhanh, lệnh rút an toàn", "hai đường phải giữ cùng quy tắc; thêm ca kiểm so hai đường"]]),
           """Đáp án câu ba: phát lại mỗi lần hỏi thì chính xác nhưng quá tải kho. Bản chiếu nhanh nhưng có thể trễ, nên lệnh rút dựa trên số cũ có thể rút quá số dư. Cách lai dùng bản chiếu cho màn hình và kiểm tại kho cho lệnh rút, đổi lại hai đường phải giữ cùng quy tắc."""),
    ], checks=["alg.bnx_l29_replay([('NAP', 800), ('RUT', 150), ('RUT', 90), ('NAP', 40)]) == 600", "alg.bnx_l29_replay([('NAP', 800), ('RUT', 150), ('RUT', 90), ('NAP', 40), ('NAP', 150), ('RUT', 15)]) == 735",
               "7300000 % 5000 == 0"])

    lab_pr = practice_scene(sc, "Tự làm: phát lại, bản chụp và sự kiện bù", practice_steps(
        st, "BNX", "L29",
        """<p><b>Đề</b>: kho: <code>NAP 500</code>, <code>RUT 100</code>, <code>NAP 200</code>, <code>RUT 50</code>, <code>NAP 25</code>, <code>RUT 75</code>. Viết <code>mau.py</code>:</p>
<ol><li>hàm <code>phat_lai(kho, tu, so_du)</code>; in số dư phát lại hết và số sự kiện đọc</li><li>bản chụp sau 4 sự kiện đầu; phát lại phần còn lại từ bản chụp</li><li>coi <code>RUT 300</code> là ghi nhầm: thêm <code>RUT 300</code> rồi sự kiện bù <code>NAP 300</code>, in số dư</li></ol>
<p class="note">Số liệu khác ví dụ trong bài; định dạng 4 dòng in ra nằm trong <code>de.md</code>.</p>""",
        """Tới phần bạn tự làm: với kho sáu sự kiện cho trước, viết hàm phát lại. Dùng bản chụp sau bốn sự kiện đầu để chỉ đọc hai sự kiện còn lại, rồi thêm một sự kiện rút ghi nhầm cùng sự kiện bù. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> hàm phát lại là vòng lặp qua <code>kho[tu:]</code>, mỗi sự kiện cộng hoặc trừ vào <code>so_du</code>. Bản chụp là kết quả của <code>phat_lai(kho[:4])</code>; phát lại tiếp từ vị trí 4 với số dư đó.
Lời giải đầy đủ ở <code>labs/BNX/L29/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, hàm phát lại là vòng lặp qua phần kho từ vị trí cho trước, mỗi sự kiện cộng hoặc trừ vào số dư. Bản chụp là kết quả phát lại bốn sự kiện đầu. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã tự thử.""", pause=150), "BNX", "L29")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("ghi điều đã xảy ra", "số dư = phát lại", "tách ghi / đọc → bản chiếu", "sai thì bù, không sửa", "bản chụp giới hạn chi phí"),
           """Ta ghi điều đã xảy ra, và số dư là kết quả phát lại. Tách ghi và đọc cho bản chiếu nhanh nhưng có thể trễ. Sự kiện sai thì bù chứ không sửa, và bản chụp giới hạn chi phí khi kho lớn."""),
        st("""<div class='box key'><b>Tư duy:</b> con số là <b>kết quả</b>, không phải <b>sự thật gốc</b>; sự thật gốc là những gì đã xảy ra, theo thứ tự. Đổi lấy lịch sử đầy đủ, ta trả bằng độ phức tạp: đọc trễ, bản chụp, phiên bản quy tắc.
Không phải hệ nào cũng cần: dùng cho nơi kiểm toán và truy vết quan trọng, như sổ tiền.</div>""",
           """Con số là kết quả, sự thật gốc là điều đã xảy ra theo thứ tự. Đổi lấy lịch sử đầy đủ, ta trả bằng độ phức tạp, nên chỉ dùng ở nơi kiểm toán quan trọng như sổ tiền."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["CQRS và Event Sourcing: khác gì, khi nào dùng?", "CQRS tách mô hình ghi và đọc; Event Sourcing lưu sự kiện làm nguồn sự thật, số dư là suy ra; dùng cho sổ tiền cần kiểm toán, không bắt buộc cho mọi hệ"],
                  ["Sự kiện sai thì sửa thế nào?", "không sửa kho: thêm sự kiện bù đảo ngược rồi sự kiện đúng; lịch sử còn đủ vết"],
                  ["Kho lớn dần thì sao, đọc trễ thì sao?", "bản chụp mỗi k sự kiện (đọc tối đa k − 1); bản chiếu chạy liên tục đọc trễ nên lệnh quan trọng đọc từ kho hoặc kiểm vị trí đã chiếu"]]),
           """Người phỏng vấn thường hỏi ba câu: tách ghi đọc khác lưu sự kiện ra sao, sự kiện sai sửa thế nào, kho lớn dần thì làm gì. Câu trả lời nằm sẵn trên bảng.""", clear=True),
        st("""<p>Bài sau: <b>chịu lỗi bằng mã Java</b>: hết giờ, thử lại, cầu dao, và cổng API cùng cân bằng tải.</p>""",
           """Ở bài ba mươi, ta tự viết bằng Java các kỹ thuật chịu lỗi: hết giờ, thử lại có lùi, cầu dao, cùng cổng API và cân bằng tải.""",
           forward_ref=True),
    ], checks=["alg.bnx_l29_replay([('NAP', 1000), ('RUT', 300), ('NAP', 50), ('RUT', 120)]) == 630"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L29", "cqrs_event_sourcing",
                  "Bài 29 — CQRS và Event Sourcing cho sổ tiền: kho sự kiện, phát lại và bản chụp",
                  "curriculum/bnx.yaml L29; audit/bnx/verify_bnx.py L29; audit/bnx/sources_l29.md: không có số liệu sản phẩm ngoài; mã Python 3 + sqlite3 chạy thật; "
                  "mọi số đo là đếm sự kiện (tất định); khái niệm CQRS/Event Sourcing do bài tự cài đặt và nói rõ là mô hình của bài",
                  ["Giải thích vì sao kho sự kiện chỉ thêm và chặn sửa, xoá bằng trigger của cơ sở dữ liệu",
                   "Dựng lại số dư bằng cách phát lại sự kiện từ đầu",
                   "Sửa một sự kiện sai bằng sự kiện bù thay vì sửa kho",
                   "Chỉ ra vì sao mô hình đọc có thể trả số cũ và nói khi nào chấp nhận được",
                   "So sánh bảng số dư sửa tại chỗ với kho sự kiện về câu hỏi kiểm toán",
                   "Đếm số sự kiện phải đọc khi kho lớn gấp 1 000 lần, có và không có bản chụp",
                   "Viết hàm phát lại có bản chụp và sự kiện bù"],
                  scenes,
                  covers=[(1, "example"), (2, "formula"), (3, "example"), (4, "example"), (5, "check"), (6, "quymo"), (7, "practice")])
