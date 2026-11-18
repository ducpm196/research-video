import lib2
from lib2 import *
from spoken_b import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
from libj import JHEAD
from labkit import write_lab, practice_scene

lib2.begin("L38")

# ── Mã Oracle hiện trên màn hình (chạy NGUYÊN VĂN trên bnx-ora qua audit/bnx/screen_ora.py; audit/bnx/ver/l38.py) ──
# Bài L38 nhận phần hàng đợi, bộ nhớ cột, phân mảnh tách khỏi L07 (2026-11-14); bảng/hàng đợi dùng tiền tố bnx_l38_.
AQ_CLEAN = """
BEGIN
  DBMS_AQADM.STOP_QUEUE('bnx_l38_q');
  DBMS_AQADM.DROP_QUEUE('bnx_l38_q');
  DBMS_AQADM.DROP_QUEUE_TABLE('bnx_l38_qt');
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
DROP TYPE IF EXISTS bnx_l38_msg FORCE;
"""

AQ_SETUP = """
CREATE TYPE bnx_l38_msg AS OBJECT (ma_gd NUMBER, so_tien NUMBER);
/
BEGIN
  DBMS_AQADM.CREATE_QUEUE_TABLE('bnx_l38_qt', 'bnx_l38_msg');
  DBMS_AQADM.CREATE_QUEUE('bnx_l38_q', 'bnx_l38_qt');
  DBMS_AQADM.START_QUEUE('bnx_l38_q');
END;
/
"""

AQ_ENQ = """
DECLARE
  eo  DBMS_AQ.ENQUEUE_OPTIONS_T;
  mp  DBMS_AQ.MESSAGE_PROPERTIES_T;
  id  RAW(16);
BEGIN
  DBMS_AQ.ENQUEUE('bnx_l38_q', eo, mp, bnx_l38_msg(101, 500000), id);
  ROLLBACK;
  DBMS_AQ.ENQUEUE('bnx_l38_q', eo, mp, bnx_l38_msg(102, 200000), id);
  COMMIT;
END;
/
SELECT COUNT(*) AS so_thong_diep FROM bnx_l38_qt;
"""

AQ_DEQ = """
DECLARE
  dq  DBMS_AQ.DEQUEUE_OPTIONS_T;
  mp  DBMS_AQ.MESSAGE_PROPERTIES_T;
  m   bnx_l38_msg;
  id  RAW(16);
BEGIN
  dq.wait := DBMS_AQ.NO_WAIT;
  DBMS_AQ.DEQUEUE('bnx_l38_q', dq, mp, m, id);
  DBMS_OUTPUT.PUT_LINE('nhan: ' || m.ma_gd || ' ' || m.so_tien);
  COMMIT;
END;
/
SELECT COUNT(*) AS so_thong_diep FROM bnx_l38_qt;
"""

IM_CHECK = """
DROP TABLE IF EXISTS bnx_l38_gd;
CREATE TABLE bnx_l38_gd (id NUMBER, so_tien NUMBER);
ALTER TABLE bnx_l38_gd INMEMORY;
SELECT value AS inmemory_size FROM v$parameter
 WHERE name = 'inmemory_size';
SELECT inmemory FROM user_tables
 WHERE table_name = 'BNX_L38_GD';
"""

# ── Đầu ra THẬT (chạy trên bnx-ora, Oracle AI Database 26ai Free 23.26.3; sqlplus căn cột bằng tab) — lược bằng "…" ──
AQ_ENQ_OUT = """
SO_THONG_DIEP
-------------
\t    1
"""
AQ_DEQ_OUT = """
nhan: 102 200000
SO_THONG_DIEP
-------------
\t    0
"""
IM_OUT = """
INMEMORY_SIZE
--------------------…
0
INMEMORY
--------
ENABLED
"""

# ── Mã Python chạy THẬT (đầu ra tất định, đệm ở audit/bnx/progcache/L38.json). Mọi số đầu vào là số minh hoạ. ──
P_CELLS = prog("DemO", r'''
COT = 8

def doc_theo_hang(bang, c):
    o, tong = 0, 0
    for hang in bang:
        o += len(hang)
        tong += hang[c]
    return tong, o

def doc_theo_cot(cot, c):
    return sum(cot[c]), len(cot[c])

for n in (1000, 100_000):
    bang = [tuple(range(i, i + COT)) for i in range(n)]
    cot = [[h[c] for h in bang] for c in range(COT)]
    t1, o1 = doc_theo_hang(bang, 3)
    t2, o2 = doc_theo_cot(cot, 3)
    print(f"{n} dong: hang {o1} o, cot {o2} o, cung tong {t1 == t2}")
''', lang="python", claims=["mô hình đếm ô, 8 cột: 1 000 dòng đọc theo hàng 8 000 ô, theo cột 1 000 ô; 100 000 dòng: 800 000 ô và 100 000 ô; hai cách cùng tổng (số minh hoạ, không đo thời gian)"])

P_MODEL = prog("MoHinh", r'''
def chay(thao_tac):
    hang, cho, nhan = [], [], []
    for t in thao_tac:
        if t[0] == "gui":
            cho.append(t[1])
        elif t[0] == "huy":
            cho = []
        elif t[0] == "chot":
            hang, cho = hang + cho, []
        elif t[0] == "nhan" and hang:
            nhan.append(hang.pop(0))
    return nhan, len(hang)

CA1 = [("gui", 101), ("huy",), ("gui", 102), ("chot",)]
print(chay(CA1))
print(chay(CA1 + [("nhan",)]))
''', lang="python", claims=["mô hình hàng đợi có giao dịch: gửi 101 rồi huỷ, gửi 102 rồi chốt → ([], 1); nhận thêm một lần → ([102], 0), khớp Oracle"])

P_SHARD = prog("XuyenManh", r'''
def xuyen(tk, manh):
    cap = [(a, b) for a in range(tk) for b in range(tk) if a != b]
    x = sum(1 for a, b in cap if a % manh != b % manh)
    return len(cap), x

for manh in (1, 3, 30):
    n, x = xuyen(60, manh)
    print(f"{manh} manh: {x}/{n} lenh xuyen manh, {100 * x / n:.1f}%")
''', lang="python", claims=["60 tài khoản, mảnh = mã chia lấy dư: 1 mảnh 0/3540; 3 mảnh 2 400/3 540 (67,8%); 30 mảnh 3 480/3 540 (98,3%) lệnh chuyển xuyên mảnh (số minh hoạ)"])

P_MOVE = prog("DoiManh", r'''
chuyen = sum(1 for a in range(1000) if a % 3 != a % 4)
print(f"3 -> 4 manh: {chuyen}/1000 tai khoan doi manh")
''', lang="python", claims=["quy tắc chia lấy dư: thêm một mảnh (3 → 4) làm 748 trong 1 000 tài khoản đổi mảnh (số minh hoạ)"])

# ── Lab (cham.sh, Python + sqlite): số liệu KHÁC ví dụ ──
LAB_PY = r'''
import sqlite3

db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE hang_doi (id INTEGER PRIMARY KEY AUTOINCREMENT,"
           " ma_gd INTEGER, so_tien INTEGER)")


def gui(ma, tien, chot):
    db.execute("BEGIN")
    db.execute("INSERT INTO hang_doi (ma_gd, so_tien) VALUES (?, ?)", (ma, tien))
    db.execute("COMMIT" if chot else "ROLLBACK")


def nhan():
    db.execute("BEGIN")
    dong = db.execute("SELECT id, ma_gd, so_tien FROM hang_doi"
                      " ORDER BY id LIMIT 1").fetchone()
    if dong:
        db.execute("DELETE FROM hang_doi WHERE id = ?", (dong[0],))
    db.execute("COMMIT")
    return dong


def dem():
    return db.execute("SELECT COUNT(*) FROM hang_doi").fetchone()[0]


gui(201, 750000, True)
gui(202, 300000, False)
gui(203, 120000, True)
gui(204, 900000, True)
print("sau gui:", dem(), "thong diep")
for _ in range(2):
    _, ma, tien = nhan()
    print("nhan:", ma, tien)
print("con lai:", dem())
LENH = [(3, 8), (4, 9), (7, 11), (10, 14), (6, 13)]
xuyen = sum(1 for a, b in LENH if a % 4 != b % 4)
print(f"xuyen manh: {xuyen}/{len(LENH)}")
'''
LAB_OUT = """sau gui: 3 thong diep
nhan: 201 750000
nhan: 203 120000
con lai: 1
xuyen manh: 3/5"""
LAB_DE = """# Lab BNX L38 — Hàng đợi có giao dịch và lệnh chuyển xuyên mảnh

Oracle không có trong bộ chấm, nên lab dùng **sqlite** (có sẵn trong Python) để luyện đúng ý của bài: gửi vào hàng đợi nằm trong giao dịch (hoàn tác thì thông điệp mất), nhận ra theo thứ tự vào trước ra trước, và đếm lệnh chuyển xuyên mảnh. Số liệu là số minh hoạ.

Viết `mau.py`:
1. Bảng `hang_doi (id INTEGER PRIMARY KEY AUTOINCREMENT, ma_gd INTEGER, so_tien INTEGER)`; mở kết nối bằng `sqlite3.connect(":memory:", isolation_level=None)` để tự quản lý giao dịch (`BEGIN`, `COMMIT`, `ROLLBACK`).
2. Hàm `gui(ma, tien, chot)`: trong một giao dịch, chèn một dòng; `chot` đúng thì `COMMIT`, sai thì `ROLLBACK`.
3. Hàm `nhan()`: trong một giao dịch, lấy dòng có `id` nhỏ nhất, xoá nó, `COMMIT`, trả về dòng đó (hàng trống thì trả `None`).
4. Gửi lần lượt `(201, 750000)` chốt, `(202, 300000)` hoàn tác, `(203, 120000)` chốt, `(204, 900000)` chốt. In `sau gui: <số dòng> thong diep`. Nhận hai lần, mỗi lần in `nhan: <ma_gd> <so_tien>`. In `con lai: <số dòng>`.
5. Mảnh của một tài khoản = mã chia lấy dư cho 4. Với năm lệnh chuyển `(3, 8)`, `(4, 9)`, `(7, 11)`, `(10, 14)`, `(6, 13)`, in `xuyen manh: <số lệnh xuyên mảnh>/5`.

In đúng năm dòng:
```
sau gui: <số> thong diep
nhan: <ma_gd> <so_tien>
nhan: <ma_gd> <so_tien>
con lai: <số>
xuyen manh: <số>/5
```
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L38 mau.py`.
"""


def jt(rows, say, **kw):
    """Bảng 'viết trong mã / đọc là / ví dụ' (<= 4 hàng) đứng TRƯỚC khối mã; lời đọc tóm tắt, chi tiết nằm trên màn hình."""
    html = lib2.table(JHEAD, [[r[0], r[1], r[2] if len(r) > 2 else ""] for r in rows]).replace("$", "<span>&#36;</span>")
    return st(html, say, clear=True, **kw)


def C(text, title=None, lines=None):
    """Khối mã có ký tự đô la (v$parameter): viết thành thực thể &#36; để lint/KaTeX không ghép hai dấu đô la thành công thức;
    trình duyệt và cổng screen_code (giải mã thực thể) vẫn thấy đúng ký tự đô la."""
    return code(text, title, lines).replace("$", "&#36;")


def build():
    write_lab("BNX", "L38", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Thông báo đã đi mà giao dịch bị hoàn tác", [
        st("""<p>Một lệnh chuyển tiền ghi sổ xong thì phải <b>báo cho hệ thống khác</b> (thông báo cho khách, đối soát).</p>
<div class="box warn">Giao dịch bị <b>hoàn tác</b> mà thông báo đã đi: khách thấy “đã chuyển 500 000” nhưng tiền vẫn nguyên. Số minh hoạ: mỗi ngày 1 000 lệnh, 1% bị hoàn tác = <b class="red">10 thông báo ma</b>.</div>""",
           """Chào bạn, một lệnh chuyển tiền ghi sổ xong thì phải báo cho hệ thống khác.
           Nếu giao dịch bị hoàn tác mà thông báo đã đi, khách thấy đã chuyển năm trăm nghìn dù tiền vẫn nguyên.
           Số minh hoạ: mỗi ngày một nghìn lệnh, một phần trăm bị hoàn tác, tức mười thông báo ma."""),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["gửi thông báo cùng giao dịch với việc ghi sổ", "hàng đợi ngay trong Oracle, chạy thật"],
                  ["báo cáo cộng một cột trên hàng triệu dòng", "đọc theo cột: đếm số ô phải đọc"],
                  ["một máy không đủ sức", "chia dữ liệu ra nhiều máy: đếm lệnh phải qua nhiều máy"]]),
           """Bài này trả lời ba câu. Gửi thông báo cùng giao dịch với việc ghi sổ thì dùng hàng đợi trong Oracle. Báo cáo cộng một cột thì đọc theo cột và đếm số ô, còn một máy không đủ sức thì chia dữ liệu ra nhiều máy và đếm lệnh phải qua nhiều máy.""",
           focus=[0, "1.2", "1.3", "1.4", "1.4"], clear=True),
    ], checks=["1000 * 1 // 100 == 10"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Hàng đợi, thông điệp", "danh sách xếp hàng: người gửi thêm vào cuối, người nhận lấy ở đầu; mỗi thông điệp là một gói dữ liệu", "gói (mã giao dịch 102, số tiền 200 000)"],
                  ["② Giao dịch", "chốt thì mọi thay đổi ở lại, hoàn tác thì mất hết", "gửi rồi hoàn tác = chưa từng gửi"],
                  ["③ Kafka", "nơi lưu thông điệp theo chủ đề; người đọc tự giữ vị trí đọc nên đọc lại được", "dịch vụ thông báo đọc chủ đề giao dịch"],
                  ["④ Lưu theo hàng, theo cột", "theo hàng: các ô của một dòng nằm liền nhau; theo cột: các ô của một cột nằm liền nhau", "cộng cột số tiền"],
                  ["⑤ Phân mảnh", "chia dữ liệu ra nhiều cơ sở dữ liệu độc lập, mỗi cái là một mảnh, theo khoá như mã tài khoản", "tài khoản 4 vào mảnh 1"]]),
           """Trước hết ta cần hiểu năm điều. Hàng đợi là danh sách xếp hàng, người gửi thêm vào cuối, người nhận lấy ở đầu. Giao dịch thì chốt là mọi thay đổi ở lại, hoàn tác là mất hết. Kafka lưu thông điệp theo chủ đề, người đọc tự giữ vị trí nên đọc lại được. Lưu theo hàng hay theo cột là các ô của một dòng hay một cột nằm liền nhau, và phân mảnh là chia dữ liệu ra nhiều cơ sở dữ liệu độc lập.""",
           introduces=["bnx_phan_manh"]),
        st("""<p>Ví dụ số xuyên suốt: gửi hai thông điệp, một cái bị hoàn tác, thì trong hàng đợi còn:</p>
$$2 - 1 = \\hl{1}\\ \\text{thông điệp}$$""",
           """Một ví dụ số xuyên suốt cả bài. Gửi hai thông điệp, một cái bị hoàn tác, thì trong hàng đợi chỉ còn hai trừ một, bằng một thông điệp.""", clear=True),
    ], checks=["2 - 1 == 1"])

    sym = sc("sym", "symbol", "Giải mã từ khoá", [
        st(table(["trên màn hình", "nghĩa"],
                 [["<code>AQ</code>, <code>DBMS_AQADM</code>, <code>DBMS_AQ</code>", "AQ (Advanced Queuing, hàng đợi nâng cao) là tính năng hàng đợi có sẵn của Oracle; tên bắt đầu <code>DBMS_</code> là gói thủ tục có sẵn: <code>…ADM</code> để quản trị hàng đợi, không có <code>ADM</code> để gửi và nhận"],
                  ["<code>DECLARE … BEGIN … END; /</code>", "khối lệnh PL/SQL (ngôn ngữ lập trình riêng của Oracle, chạy trong cơ sở dữ liệu): khai biến sau DECLARE, phần chạy giữa BEGIN và END; dấu gạch chéo báo công cụ chạy khối"],
                  ["<code>DBMS_OUTPUT.PUT_LINE('…')</code>", "in một dòng chữ ra màn hình dòng lệnh"],
                 ]),
           """Bảng này giải mã phần hàng đợi của Oracle. Dòng đầu, chữ viết tắt là hàng đợi nâng cao, tính năng hàng đợi có sẵn của Oracle, còn hai tên sau là gói thủ tục có sẵn, một gói quản trị và một gói gửi nhận. Khối lệnh là mã viết bằng ngôn ngữ riêng của Oracle, có phần khai biến, phần chạy giữa hai chữ mở và đóng, và dấu gạch chéo báo chạy khối.""",
           introduces=["bnx_dbms_aq", "bnx_plsql", "bnx_dbms_output"]),
        st(table(["trên màn hình", "nghĩa"],
                 [["<code>CREATE TYPE … AS OBJECT (ma_gd NUMBER, …)</code>", "tạo kiểu mới gộp vài trường thành một gói; mỗi thông điệp là một gói như vậy"],
                  ["<code>RAW(16)</code>", "dãy 16 byte thô; Oracle dùng làm mã của thông điệp"],
                  ["<code>DBMS_AQADM.CREATE_QUEUE_TABLE / CREATE_QUEUE / START_QUEUE</code>", "gói quản trị hàng đợi: tạo bảng chứa, tạo hàng đợi, bật hàng đợi"],
                  ["<code>DBMS_AQ.ENQUEUE</code> / <code>DEQUEUE</code>", "gửi thông điệp vào / nhận ra khỏi hàng đợi; <code>NO_WAIT</code>: hàng trống thì báo ngay, không chờ"]]),
           """Kiểu mới gộp vài trường thành một gói thông điệp. Dãy mười sáu byte thô là mã thông điệp.
           Gói quản trị tạo bảng chứa, tạo hàng đợi và bật nó. Hai thủ tục còn lại gửi vào và nhận ra.""",
           clear=True),
        st(table(["trên màn hình", "nghĩa"],
                 [["<code>ALTER TABLE … INMEMORY</code>", "đánh dấu bảng được nạp thêm một bản dạng cột vào bộ nhớ, để đọc báo cáo"],
                  ["<code>INMEMORY_SIZE</code>, <code>v&#36;parameter</code>", "tham số: dung lượng vùng nhớ cột (0 là chưa có vùng); <code>v&#36;parameter</code> là bảng ảo liệt kê tham số đang chạy"],
                  ["<code>user_tables.inmemory</code>", "cột báo bảng đã được đánh dấu chưa"],
                  ["<code>mã % 3</code>", "mảnh = mã tài khoản chia lấy dư cho 3; quy tắc minh hoạ của bài"]]),
           """Bảng thứ hai giải mã bộ nhớ cột và phân mảnh. Lệnh đánh dấu bảng được nạp thêm một bản dạng cột vào bộ nhớ, để đọc báo cáo, và tham số dung lượng bằng không nghĩa là chưa có vùng nhớ cột nào. Bảng ảo liệt kê các tham số đang chạy, một cột báo bảng đã được đánh dấu chưa, và mảnh bằng mã chia lấy dư cho ba là quy tắc minh hoạ.""",
           clear=True, introduces=["bnx_inmemory", "bnx_bo_nho_cot"]),
    ], checks=["alg.bnx_l38_shard(7, 3) == 1"])

    def rowbox(r):
        return "".join(box(60 + c * 160, 100 + r * 62, 150, 52, f"ô {c + 1}", C_AMBER, size=22) for c in range(4))
    intu = sc("intuition", "intuition", "Hình dung: hàng đợi cùng giao dịch, đọc theo cột, và bộ định tuyến mảnh", [
        st(svg(1500, 470,
               panel(30, 20, 820, 430, "Hàng đợi trong cơ sở dữ liệu: một giao dịch", C_GREEN, size=24),
               box(70, 110, 360, 90, ["ghi giao dịch", "vào bảng"], C_BLUE, size=22),
               box(460, 110, 360, 90, ["gửi thông điệp", "vào hàng đợi"], C_PURPLE, size=22),
               box(70, 260, 360, 80, "chốt: cả hai ở lại", C_GREEN, size=22),
               box(460, 260, 360, 80, "hoàn tác: cả hai mất", C_RED, size=22),
               arrow(250, 205, 250, 255), arrow(640, 205, 640, 255),
               txt(440, 400, "mặc định: không có thông điệp “ma” cho giao dịch đã huỷ", 22, "middle", "#16a34a", True),
               panel(900, 20, 570, 430, "Kafka: hệ riêng bên ngoài", C_AMBER, size=24),
               box(940, 110, 490, 90, ["ghi cơ sở dữ liệu và gửi Kafka", "là hai việc riêng"], C_AMBER, size=22),
               box(940, 260, 490, 80, "cần thêm cách giữ nhất quán", C_GRAY, size=22),
               arrow(1185, 205, 1185, 255),
               txt(1185, 400, "bù lại: lưu lâu, đọc lại được", 22, "middle", "#d97706", True)),
           """Hình đầu so hai cách báo cho hệ khác. Với hàng đợi trong cơ sở dữ liệu, ghi giao dịch và gửi thông điệp nằm trong cùng một giao dịch.
           Ở chế độ mặc định, chốt thì cả hai ở lại, hoàn tác thì cả hai mất. Với Kafka, hai việc là riêng nên cần thêm cách giữ nhất quán, bù lại Kafka lưu lâu và cho đọc lại."""),
        st(svg(1500, 430,
               panel(30, 20, 700, 390, "Lưu theo hàng: cộng cột 3 phải đọc cả dòng", C_AMBER, size=24),
               *[rowbox(r) for r in range(4)],
               txt(380, 395, "đọc 4 dòng × 4 ô = 16 ô", 24, "middle", "#d97706", True),
               panel(770, 20, 700, 390, "Lưu theo cột: chỉ đọc cột 3", C_GREEN, size=24),
               *[box(800 + c * 165, 90, 150, 240, f"cột {c + 1}", C_GREEN if c == 2 else C_GRAY, size=22, bold=(c == 2)) for c in range(4)],
               txt(1120, 395, "đọc 1 cột × 4 ô = 4 ô", 24, "middle", "#16a34a", True)),
           """Hình thứ hai so hai cách lưu cùng một bảng bốn dòng, bốn cột. Cộng cột ba thì lưu theo hàng đọc cả bốn dòng, mười sáu ô, còn lưu theo cột chỉ đọc bốn ô.""",
           clear=True),
        st(svg(1500, 430,
               box(560, 20, 380, 80, ["bộ định tuyến", "theo khoá phân mảnh"], C_PURPLE, size=22),
               box(60, 230, 380, 110, ["Mảnh 0", "một cơ sở dữ liệu riêng", "tài khoản 3, 6, 9…"], C_BLUE, size=22),
               box(560, 230, 380, 110, ["Mảnh 1", "một cơ sở dữ liệu riêng", "tài khoản 4, 7, 10…"], C_BLUE, size=22),
               box(1060, 230, 380, 110, ["Mảnh 2", "một cơ sở dữ liệu riêng", "tài khoản 5, 8, 11…"], C_BLUE, size=22),
               arrow(650, 105, 250, 225), arrow(750, 105, 750, 225), arrow(850, 105, 1250, 225),
               txt(750, 400, "quy tắc minh hoạ: mảnh = mã tài khoản chia lấy dư cho 3", 24, "middle", "#1f2937", True)),
           """Hình thứ ba là phân mảnh. Bộ định tuyến nhìn khoá để đưa yêu cầu tới đúng mảnh, mỗi mảnh là một cơ sở dữ liệu riêng.
           Ở đây dùng quy tắc minh hoạ, mã tài khoản chia lấy dư cho ba, nên tài khoản bảy vào mảnh một.""",
           clear=True),
    ], checks=["alg.bnx_l38_cells(4, 4, 'hang') == 16 and alg.bnx_l38_cells(4, 4, 'cot') == 4",
               "alg.bnx_l38_queue([('enq', 101), ('rollback',), ('enq', 102), ('commit',)]) == ([], 1)"])

    form = sc("formula", "formula", "Suy ra từng bước: hàng đợi, bộ nhớ cột và phân mảnh", [
        st("""<p><b>Bước 1. Tạo hàng đợi</b>: kiểu thông điệp, bảng hàng đợi, hàng đợi, rồi bật nó.</p>""" + code(AQ_SETUP),
           """Bước một, tạo hàng đợi ngay trong cơ sở dữ liệu. Hàng đợi phải biết mỗi thông điệp chứa gì, nên trước hết khai kiểu thông điệp gồm mã giao dịch và số tiền. Rồi tạo bảng hàng đợi, tạo hàng đợi trên bảng đó, và bật hàng đợi.""", clear=True),
        jt([("<code>eo  DBMS_AQ.ENQUEUE_OPTIONS_T;</code>, <code>id  RAW(16);</code>", "khai biến trong PL/SQL: tên rồi kiểu; kiểu là loại có sẵn của gói; <code>RAW(16)</code> là dãy 16 byte thô", "<code>eo</code> là biến tuỳ chọn gửi"),
            ("<code>bnx_l38_msg(101, 500000)</code>", "tạo một thông điệp kiểu <code>bnx_l38_msg</code>, giá trị các trường theo thứ tự: mã 101, số tiền 500000", "mã giao dịch 101, số tiền 500000"),
            ("<code>DBMS_AQ.ENQUEUE('bnx_l38_q', eo, mp, msg, id)</code>", "gửi: năm đối số là tên hàng đợi, tuỳ chọn, thuộc tính, nội dung, biến nhận mã thông điệp", ""),
            ("<code>ROLLBACK;</code>, <code>COMMIT;</code>", "hoàn tác giao dịch đang mở (mọi thay đổi mất); chốt (mọi thay đổi ở lại)", "")],
           """Đọc trước bốn chỗ: khai biến là tên rồi kiểu, tạo thông điệp bằng các giá trị theo thứ tự trường, lệnh gửi năm đối số, và hoàn tác hay chốt."""),
        st("""<p><b>Bước 2. Gửi trong giao dịch</b>: gửi 101 rồi hoàn tác, gửi 102 rồi chốt.</p>""" + code(AQ_ENQ),
           """Bước hai, gửi thông điệp một trăm linh một rồi hoàn tác, sau đó gửi một trăm linh hai rồi chốt. Vì việc gửi mặc định là một phần của giao dịch đang chạy, nên hoàn tác thì thông điệp đầu biến mất. Câu cuối đếm thông điệp trong bảng hàng đợi.""", clear=True),
        st(out(AQ_ENQ_OUT) + """<p class='note'>Làm thử: 2 lần gửi − 1 lần bị hoàn tác = 1 thông điệp.</p>""",
           """Làm thử, vì lần gửi đầu đã bị hoàn tác, hai lần gửi trừ một còn một thông điệp, khớp với đầu ra thật.""", clear=True),
        jt([("<code>dq.wait := DBMS_AQ.NO_WAIT;</code>", "<code>:=</code> gán giá trị; <code>dq.wait</code> là trường <code>wait</code> của <code>dq</code>; <code>NO_WAIT</code>: hàng trống thì báo ngay, không chờ", "<code>x := 5</code> đặt x bằng 5"),
            ("<code>'nhan: ' || m.ma_gd || ' ' || m.so_tien</code>", "<code>||</code> nối chuỗi và số thành một dòng; <code>m.ma_gd</code> đọc trường mã giao dịch của thông điệp <code>m</code>", "<code>'a' || 1</code> ra <code>a1</code>")],
           """Dấu hai chấm bằng gán giá trị, dấu chấm đọc một trường, và hai gạch đứng nối chuỗi vì ta cần in số cạnh chữ."""),
        st("""<p><b>Bước 3. Nhận rồi chốt</b>, ở chế độ không chờ; rồi đếm lại.</p>""" + code(AQ_DEQ),
           """Bước ba, nhận một thông điệp, in ra rồi chốt. Vì không muốn treo khi hàng đợi trống, ta đặt chế độ không chờ. Câu cuối đếm lại bảng hàng đợi.""", clear=True),
        st(out(AQ_DEQ_OUT) + """<p class='note'>Làm thử: 1 thông điệp − 1 đã nhận = 0: nhận và chốt xong, thông điệp rời hàng đợi.</p>""",
           """Máy nhận đúng thông điệp một trăm linh hai, hai trăm nghìn. Vì việc nhận cũng nằm trong giao dịch, nên chỉ sau khi chốt thông điệp mới rời hàng đợi, và đếm lại thì còn không.""",
           clear=True),
        st("""<p><b>Bước 4. Bộ nhớ cột</b>: báo cáo cộng một cột trên hàng triệu dòng thì đọc theo cột thường ít việc hơn. Kiểm trên máy của bài:</p>""" + C(IM_CHECK),
           """Bước bốn là bộ nhớ cột. Báo cáo thường cộng một cột trên hàng triệu dòng, nên đọc dữ liệu xếp theo cột thường ít việc hơn.
           Ta tạo một bảng nhỏ, đánh dấu nó, rồi hỏi dung lượng vùng nhớ cột và hỏi bảng đã được đánh dấu chưa.""",
           clear=True),
        st(out(IM_OUT),
           """Trên máy của bài, dung lượng vùng nhớ cột đang là không. Ta vẫn đánh dấu bảng được, nhưng vì vùng nhớ bằng không nên chưa có gì được nạp, và bài không đo được tốc độ.""",
           clear=True),
        st("""<p><b>Bước 5. Phân mảnh</b>, khi một cơ sở dữ liệu không đủ sức: bộ định tuyến đưa yêu cầu tới mảnh theo khoá (hình bên trên).</p>"""
           + table(["lệnh", "mảnh (mã mod 3, minh hoạ)", "hệ quả"],
                   [["chuyển từ tài khoản 4 sang 7", "1 và 1", "một mảnh: giao dịch trong một cơ sở dữ liệu"],
                    ["chuyển từ tài khoản 4 sang 5", "1 và 2", "xuyên mảnh: hai cơ sở dữ liệu phải cùng chốt, đắt hơn"]]),
           """Bước năm là phân mảnh, khi một cơ sở dữ liệu không đủ sức. Chuyển từ tài khoản bốn sang bảy, cả hai ở mảnh một, nên là giao dịch trong một cơ sở dữ liệu.
           Chuyển từ bốn sang năm thì xuyên hai mảnh, hai cơ sở dữ liệu phải cùng chốt, đắt hơn nhiều.""", clear=True),
    ], checks=["alg.bnx_l38_queue([('enq', 101), ('rollback',), ('enq', 102), ('commit',)])[1] == 1",
               "alg.bnx_l38_queue([('enq', 101), ('rollback',), ('enq', 102), ('commit',), ('deq',), ('commit',)]) == ([102], 0)",
               "alg.bnx_l38_shard(4, 3) == alg.bnx_l38_shard(7, 3) == 1 and alg.bnx_l38_shard(5, 3) == 2"])

    ex = sc("example", "example", "Ví dụ chạy thật, từng phép tính", [
        st("""$$① \\; 2 - 1 = \\hl{1}\\ \\text{thông điệp sau khi gửi (đã đo trên Oracle)}$$
$$② \\; 1 - 1 = \\hl{0}\\ \\text{thông điệp sau khi nhận và chốt}$$""",
           """Ta tính và so với máy. Phép tính thứ nhất, hai lần gửi trừ một lần hoàn tác còn một thông điệp, khớp bảng hàng đợi thật. Phép tính thứ hai, nhận một cái và chốt thì còn không."""),
        jt([("<code>def doc_theo_hang(bang, c): … return tong, o</code>", "khai hàm; các dòng thụt vào là thân hàm; <code>return</code> trả hai giá trị một lúc", "<code>return 3, 5</code> trả cả 3 và 5"),
            ("<code>for hang in bang:</code>, <code>o += len(hang)</code>, <code>tong += hang[c]</code>", "mỗi vòng <code>hang</code> là một dòng của <code>bang</code>; <code>len</code> đếm số ô; <code>+=</code> cộng dồn; <code>hang[c]</code> là ô thứ c, ô đầu là 0", "<code>len((7, 8, 9))</code> ra 3"),
            ("<code>sum(cot[c])</code>", "cộng mọi phần tử của danh sách <code>cot[c]</code>", "<code>sum([1, 2, 3])</code> ra 6")],
           """Hàm nhận bảng và chỉ số cột, lặp từng dòng để đếm ô và cộng dồn, hoặc cộng thẳng cả cột bằng hàm tổng."""),
        st(P_CELLS.show(lines=(1, 11), title="DemO.py (trích): mô hình đếm ô phải đọc"),
           """Giờ đến bộ nhớ cột, ta đo bằng mô hình đếm ô, không đo thời gian. Bảng có tám cột, ta cộng cột thứ tư.
           Cách theo hàng phải đi qua cả dòng nên đếm mọi ô, cách theo cột chỉ đếm đúng một cột.""", clear=True),
        jt([("<code>for n in (1000, 100_000):</code>", "vòng lặp trên một dãy; dấu gạch dưới trong số chỉ để dễ đọc", "<code>100_000</code> là 100000"),
            ("<code>[tuple(range(i, i + COT)) for i in range(n)]</code>", "danh sách sinh sẵn: mỗi <code>i</code> từ 0 tới n − 1 tạo một dòng gồm COT số liên tiếp bắt đầu từ i", "<code>i = 2</code>, <code>COT = 3</code>: <code>(2, 3, 4)</code>"),
            ("<code>[[h[c] for h in bang] for c in range(COT)]</code>", "danh sách lồng: với mỗi cột <code>c</code>, lấy ô thứ c của mọi dòng <code>h</code>; ra danh sách các cột", "bảng 2 dòng: cột 0 gồm ô 0 của hai dòng"),
            ("<code>{t1 == t2}</code>", "trong chuỗi f: in <code>True</code> nếu hai tổng bằng nhau", "")],
           """Dòng đầu tạo bảng giả bằng danh sách sinh sẵn, dòng sau tách bảng thành các cột bằng danh sách lồng, rồi ta so hai tổng."""),
        st(P_CELLS.show(lines=(13, 18), title="Vòng ngoài: hai cỡ") + P_CELLS.out_html(),
           """Vòng ngoài thử hai cỡ, một nghìn dòng và một trăm nghìn dòng, rồi so tổng của hai cách. Kết quả thật: một nghìn dòng đọc tám nghìn ô so với một nghìn ô, và hai cách cùng một tổng.""",
           clear=True),
        st("""$$③ \\; 8 \\cdot 1\\,000 = \\hl{8\\,000}\\ \\text{ô (theo hàng)}$$
$$④ \\; 8\\,000 : 1\\,000 = \\hlg{8}\\ \\text{lần, bằng đúng số cột}$$
$$⑤ \\; 8 \\cdot 100\\,000 = \\hl{800\\,000}\\ \\text{ô, so với }100\\,000$$""",
           """Phép tính thứ ba và thứ tư: tám cột nhân một nghìn dòng bằng tám nghìn ô, gấp tám lần một nghìn, đúng bằng số cột. Phép tính thứ năm, ở một trăm nghìn dòng, theo hàng đọc tám trăm nghìn ô còn theo cột chỉ một trăm nghìn.""", clear=True),
    ], checks=["alg.bnx_l38_cells(1000, 8, 'hang') == 8000 and alg.bnx_l38_cells(1000, 8, 'cot') == 1000",
               "alg.bnx_l38_cells(1000, 8, 'hang') // alg.bnx_l38_cells(1000, 8, 'cot') == 8",
               "alg.bnx_l38_cells(100000, 8, 'hang') == 800000 and alg.bnx_l38_cells(100000, 8, 'cot') == 100000"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: mô hình hàng đợi", [
        jt([("<code>def chay(thao_tac):</code>, <code>hang, cho, nhan = [], [], []</code>", "hàm nhận danh sách thao tác; gán một lúc ba danh sách rỗng, mỗi tên một danh sách", ""),
            ("<code>t[0] == \"gui\"</code>, <code>elif</code>, <code>cho.append(t[1])</code>", "<code>t[0]</code> là phần tử đầu của bộ <code>t</code>; <code>elif</code>: các nhánh trên sai thì thử điều kiện này; <code>append</code> thêm vào cuối danh sách", "<code>t = (\"gui\", 101)</code>: <code>t[0]</code> là <code>gui</code>"),
            ("<code>hang, cho = hang + cho, []</code>", "tính vế phải trước: nối hai danh sách, rồi gán đồng thời; <code>cho</code> thành rỗng", ""),
            ("<code>elif t[0] == \"nhan\" and hang:</code>, <code>hang.pop(0)</code>, <code>return nhan, len(hang)</code>", "<code>and</code>: cả hai vế đúng, <code>hang</code> rỗng thì tính là sai; <code>pop(0)</code> lấy và bỏ phần tử đầu; trả hai giá trị", "<code>[5, 6].pop(0)</code> ra 5, còn <code>[6]</code>")],
           """Hàm duyệt từng thao tác: gửi thì thêm vào danh sách chờ, chốt thì nối vào hàng, và nhận thì lấy phần tử đầu, vì hàng đợi vào trước ra trước."""),
        st(P_MODEL.show(lines=(1, 12), title="MoHinh.py: hàng đợi có giao dịch viết lại bằng một danh sách"),
           """Ta kiểm bằng đường khác: viết lại hàng đợi bằng hai danh sách, một danh sách đã chốt và một danh sách chờ chốt. Vì hoàn tác chỉ cần bỏ danh sách chờ, còn chốt thì nối nó vào hàng, nên mô hình ngắn gọn hơn Oracle nhiều.""",
           clear=True),
        st(P_MODEL.show(lines=(14, 16), title="Hai ca thử, giống hai việc đã chạy trên Oracle") + "<p class='note'><code>(\"huy\",)</code>: dấu phẩy cuối làm thành bộ một phần tử; <code>CA1 + [(\"nhan\",)]</code>: nối thêm một thao tác.</p>" + P_MODEL.out_html()
           + table(["ca", "Oracle thật", "mô hình"],
                   [["gửi 101 rồi hoàn tác, gửi 102 rồi chốt", "1 thông điệp", "còn 1"], ["nhận một lần", "nhận 102, còn 0", "nhận 102, còn 0"]]),
           """Hai ca thử giống hệt hai việc đã chạy trên Oracle: ca đầu còn một thông điệp, ca sau nhận được một trăm linh hai và còn không, khớp từng số. Bảng này nói rõ điều đã kiểm. Hàng đợi chạy thật trên Oracle, còn bộ nhớ cột và phân mảnh chỉ kiểm bằng mô hình, vì vùng nhớ cột bằng không và phân mảnh cần nhiều cơ sở dữ liệu.""",
           focus=[0, "1.2", "1.3", "2.1", "2.1"], clear=True),
    ], checks=["alg.bnx_l38_queue([('enq', 101), ('rollback',), ('enq', 102), ('commit',)]) == ([], 1)",
               "alg.bnx_l38_queue([('enq', 101), ('rollback',), ('enq', 102), ('commit',), ('deq',), ('commit',)]) == ([102], 0)"])

    quymo = sc("quymo", "example", "Khi số mảnh tăng: lệnh chuyển xuyên mảnh", [
        jt([("<code>[(a, b) for a in range(tk) for b in range(tk) if a != b]</code>", "hai vòng lồng: mọi cặp (a, b) với mã từ 0 tới tk − 1, bỏ cặp a bằng b", "<code>tk = 3</code>: 6 cặp"),
            ("<code>sum(1 for a, b in cap if a % manh != b % manh)</code>", "đếm các cặp mà phần dư của a và của b khi chia cho <code>manh</code> khác nhau; <code>%</code> là phần dư", "<code>7 % 3</code> ra 1"),
            ("<code>{100 * x / n:.1f}</code>", "phần trăm x trên n, giữ một chữ số sau dấu chấm thập phân", "<code>3480 / 3540</code> ra <code>98.3</code>"),
            ("<code>n, x = xuyen(60, manh)</code>", "hàm trả hai giá trị, gán vào n và x một lúc", "")],
           """Hàm liệt kê mọi cặp tài khoản khác nhau, đếm cặp có phần dư khác nhau, và in tỉ lệ phần trăm một chữ số thập phân."""),
        st("""<p class="note">Giả định (số minh hoạ): 60 tài khoản, mọi cặp chuyển có thứ tự (60 × 59 = 3 540 cặp), mảnh = mã chia lấy dư cho số mảnh.</p>"""
           + P_SHARD.show(lines=(1, 8), title="XuyenManh.py"),
           """Giả định, số minh hoạ: sáu mươi tài khoản, mọi cặp chuyển có thứ tự, tức ba nghìn năm trăm bốn mươi cặp, mảnh bằng mã chia lấy dư cho số mảnh. Ta đếm các cặp rơi vào hai mảnh khác nhau, ở một, ba và ba mươi mảnh.""",
           clear=True),
        st(P_SHARD.out_html()
           + """$$1 \\to 3 \\to 30 \\text{ mảnh: } \\hl{0} \\to \\hl{2\\,400} \\to \\hl{3\\,480} \\text{ lệnh xuyên mảnh}$$""",
           """Một mảnh thì không lệnh nào xuyên mảnh. Ba mảnh thì hai nghìn bốn trăm lệnh xuyên mảnh, hơn sáu mươi bảy phần trăm. Ba mươi mảnh thì gần chín mươi tám phần trăm.
           Vậy càng thêm mảnh, gần như mọi lệnh chuyển đều phải đi qua nhiều cơ sở dữ liệu.""",
           clear=True),
        st(table(["cách", "được", "mất", "khi nào chọn"],
                 [["một cơ sở dữ liệu, thêm chỉ mục và bản sao đọc", "mọi lệnh chuyển là giao dịch của một máy", "một máy là giới hạn: nó hỏng thì ngừng", "chưa đo thấy một máy hết sức"],
                  ["phân mảnh theo khoá", "tải ghi chia ra nhiều máy", "lệnh xuyên mảnh phải nhiều cơ sở dữ liệu cùng chốt: đắt, khó", "một máy đã hết sức dù đã thêm chỉ mục và bản sao"]]),
           """Bảng này cho thấy người làm nghề phải chọn gì. Một cơ sở dữ liệu thì mọi lệnh chuyển là giao dịch của một máy, đổi lại một máy là giới hạn.
           Phân mảnh chia tải ghi ra nhiều máy, đổi lại lệnh xuyên mảnh đắt và khó. Vì thế chỉ phân mảnh khi đã đo thấy một máy hết sức.""",
           focus=[0, "1.2", "1.3", "1.3"], clear=True),
    ], checks=["alg.bnx_l38_cross(60, 1) == (3540, 0)", "alg.bnx_l38_cross(60, 3) == (3540, 2400)", "alg.bnx_l38_cross(60, 30) == (3540, 3480)"])

    lab_pr = practice_scene(sc, "Tự làm: hàng đợi có giao dịch và lệnh xuyên mảnh", lib2.practice_steps2(
        st, "BNX", "L38",
        """<p><b>Đề</b>: sqlite có bảng <code>hang_doi (id, ma_gd, so_tien)</code>. Viết <code>mau.py</code>:</p>
<ol><li><code>gui(ma, tien, chot)</code>: chèn một dòng trong giao dịch; <code>chot</code> sai thì hoàn tác</li><li><code>nhan()</code>: lấy dòng <code>id</code> nhỏ nhất, xoá, chốt</li><li>gửi 201 (chốt), 202 (hoàn tác), 203, 204 (chốt), nhận hai lần, đếm; rồi đếm lệnh xuyên mảnh với mảnh = mã mod 4</li></ol>
<p class="note">Oracle không có trong bộ chấm: sqlite đại diện. Số liệu và khuôn năm dòng in ra nằm trong <code>de.md</code>.</p>""",
        """Bây giờ tới phần bạn tự làm, trên cơ sở dữ liệu nhỏ có sẵn trong Python vì bộ chấm không có Oracle. Viết hàm gửi trong giao dịch, hoàn tác thì thông điệp mất, và hàm nhận lấy thông điệp vào trước, rồi đếm lệnh xuyên mảnh với quy tắc mới. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> mở giao dịch bằng <code>db.execute("BEGIN")</code> (kết nối <code>isolation_level=None</code>), rồi <code>COMMIT</code> hoặc <code>ROLLBACK</code>. Nhận: <code>SELECT … ORDER BY id LIMIT 1</code> rồi <code>DELETE</code>. Xuyên mảnh: <code>a % 4 != b % 4</code>.
Lời giải ở <code>labs/BNX/L38/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, mở giao dịch bằng lệnh bắt đầu rồi chốt hoặc hoàn tác. Nhận bằng cách chọn dòng có mã nhỏ nhất rồi xoá nó. Xuyên mảnh là hai mã có phần dư khác nhau. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã tự thử.""", pause=120), "BNX", "L38")

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người đã đi làm): coi hàng đợi trong Oracle giống hệt Kafka.</b></div>"""
           + table(["", "hàng đợi trong Oracle", "Kafka"],
                   [["chung giao dịch với dữ liệu", "có: hoàn tác thì thông điệp cũng mất (bước 2)", "không: hệ riêng"],
                    ["sau khi nhận và chốt", "mặc định, thời gian lưu giữ là 0 (hàng đợi không giữ lại thông điệp đã nhận): thông điệp rời hàng đợi, đếm lại được 0 (bước 3)", "vẫn lưu; người đọc tự giữ vị trí, đọc lại được"],
                    ["tải đặt lên đâu", "chính cơ sở dữ liệu giao dịch", "cụm máy riêng"]]),
           """Lỗi thứ nhất, của người đã đi làm, là coi hàng đợi trong cơ sở dữ liệu giống hệt Kafka. Nó chung giao dịch với dữ liệu nên hoàn tác thì thông điệp cũng mất, điều Kafka không làm được. Nhưng thời gian lưu giữ mặc định là không, nên thông điệp đã nhận và chốt thì rời hàng đợi, và mọi tải đặt lên chính cơ sở dữ liệu giao dịch.""",
           ),
        st("""<div class="box warn"><b>Lỗi 2: bật <code>INMEMORY</code> rồi tin là báo cáo nhanh hơn.</b> Trên máy của bài vùng nhớ cột bằng 0: bảng được đánh dấu <code>ENABLED</code> nhưng chưa có gì được nạp, nên chưa có gì để đo. Muốn biết nhanh hơn bao nhiêu phải đo trên chính tải của bạn.</div>""",
           """Lỗi thứ hai là bật bộ nhớ cột rồi tin là báo cáo nhanh hơn. Trên máy của bài vùng nhớ cột bằng không, bảng chỉ được đánh dấu mà chưa có gì được nạp, nên chưa có gì để đo. Muốn biết nhanh hơn bao nhiêu phải đo trên tải thật.""",
           clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm): chia lấy dư rồi thêm một mảnh.</b> Quy tắc <code>mã % 3</code> đổi sang <code>mã % 4</code>:</div>"""
           + P_MOVE.show() + "<p class='note'><code>sum(1 for a in range(1000) if a % 3 != a % 4)</code>: đếm số a mà phần dư khi chia 3 khác phần dư khi chia 4.</p>" + P_MOVE.out_html(),
           """Lỗi thứ ba, của người đã đi làm, là chia lấy dư rồi thêm một mảnh. Khi đổi từ ba mảnh sang bốn, bảy trăm bốn mươi tám trong một nghìn tài khoản đổi mảnh, tức gần ba phần tư. Hệ thật thiết kế cách chia để thêm mảnh chỉ di chuyển một phần dữ liệu.""", clear=True),
    ], checks=["alg.bnx_l38_moved(1000, 3, 4) == 748",
               "alg.bnx_l38_queue([('enq', 102), ('commit',), ('deq',), ('commit',)])[1] == 0"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Bảng 8 cột, 50 000 dòng, cộng một cột. Đọc theo hàng và theo cột, mỗi cách phải đọc bao nhiêu ô? Báo cáo hay tra một dòng hợp bộ nhớ cột hơn?"],
                  ["2", "Gửi 301 rồi chốt, gửi 302 rồi hoàn tác, rồi nhận một thông điệp. Nhận được gì, còn mấy thông điệp?"],
                  ["3", "12 tài khoản mã 0 tới 11, 4 mảnh, mảnh = mã mod 4. Bao nhiêu cặp chuyển có thứ tự cùng mảnh, bao nhiêu xuyên mảnh? Có nên phân mảnh ngay khi một máy dùng 30% sức?"],
                  ["4", "Quyết định: báo “đã chuyển tiền” bằng hàng đợi trong Oracle hay bằng Kafka?"]]),
           """Đến lượt bạn. Câu một: bảng tám cột, năm mươi nghìn dòng, cộng một cột; mỗi cách đọc bao nhiêu ô, báo cáo hay tra một dòng hợp bộ nhớ cột hơn? Câu hai: gửi ba trăm linh một chốt, ba trăm linh hai hoàn tác, rồi nhận một thông điệp; nhận gì, còn mấy? Câu ba: mười hai tài khoản, bốn mảnh, bao nhiêu cặp xuyên mảnh, có nên phân mảnh khi một máy dùng ba mươi phần trăm sức? Câu bốn: hàng đợi trong Oracle hay Kafka. Hãy dừng video và làm ra giấy.""",
           pause=40),
        st("""<p>Câu 1: theo hàng đọc cả dòng, theo cột chỉ một cột.</p>
$$8 \\cdot 50\\,000 = \\hlg{400\\,000}\\ \\text{ô}; \\qquad 1 \\cdot 50\\,000 = \\hlg{50\\,000}\\ \\text{ô}$$""",
           """Đáp án câu một. Theo hàng đọc tám nhân năm mươi nghìn, bốn trăm nghìn ô, theo cột chỉ năm mươi nghìn ô. Báo cáo cộng cả cột hợp bộ nhớ cột, còn tra một dòng thì lưu theo hàng là đủ."""),
        st("""<p>Câu 2: 301 đã chốt ở lại, 302 bị hoàn tác nên mất; nhận lấy cái đầu hàng.</p>
<div class='box key'>nhận <b>301</b>, còn <b>0</b> thông điệp</div>""",
           """Đáp án câu hai. Ba trăm linh một đã chốt nên ở lại, ba trăm linh hai bị hoàn tác nên mất. Nhận lấy thông điệp đầu hàng là ba trăm linh một, và hàng đợi còn không.""", clear=True),
        st("""<p>Câu 3: mỗi mảnh 3 tài khoản.</p>
$$12 \\cdot 11 = 132;\\quad 4 \\cdot (3 \\cdot 2) = \\hl{24}\\ \\text{cùng mảnh};\\quad 132 - 24 = \\hl{108}\\ \\text{xuyên mảnh}$$""",
           """Đáp án câu ba. Mười hai nhân mười một là một trăm ba mươi hai cặp có thứ tự. Mỗi mảnh có ba tài khoản, nên cùng mảnh là bốn nhân sáu, hai mươi bốn cặp, còn một trăm lẻ tám cặp xuyên mảnh. Một máy mới dùng ba mươi phần trăm sức thì chưa nên phân mảnh.""", clear=True),
        st(table(["lựa chọn", "được", "mất"],
                 [["hàng đợi trong Oracle", "cùng giao dịch với lệnh chuyển: không gửi nhầm cho lệnh đã huỷ", "tải đặt lên cơ sở dữ liệu giao dịch; mặc định nhận xong là mất"],
                  ["Kafka", "lưu lâu, nhiều dịch vụ cùng đọc, đọc lại được, chịu tải lớn", "ghi và gửi là hai việc riêng: cần mẫu hộp thư đi hoặc cách tương tự để không lệch"]]),
           """Đáp án câu bốn, tuỳ nhu cầu. Hàng đợi trong Oracle đi cùng giao dịch của lệnh chuyển nên không gửi nhầm, đổi lại tải đặt lên cơ sở dữ liệu giao dịch. Kafka lưu lâu và nhiều dịch vụ cùng đọc, nhưng ghi và gửi là hai việc riêng, nên cần mẫu hộp thư đi.""", clear=True),
    ], checks=["alg.bnx_l38_cells(50000, 8, 'hang') == 400000 and alg.bnx_l38_cells(50000, 8, 'cot') == 50000",
               "alg.bnx_l38_queue([('enq', 301), ('commit',), ('enq', 302), ('rollback',), ('deq',), ('commit',)]) == ([301], 0)",
               "alg.bnx_l38_cross(12, 4) == (132, 108) and 4 * 3 * 2 == 24"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("gửi cùng giao dịch", "hàng đợi trong cơ sở dữ liệu", "đọc theo cột khi báo cáo", "phân mảnh khi một máy hết sức"),
           """Tổng kết chuỗi logic. Thông báo gửi cùng giao dịch với việc ghi sổ thì dùng hàng đợi trong cơ sở dữ liệu. Báo cáo cộng một cột thì đọc theo cột, và phân mảnh khi một máy hết sức."""),
        st("""<div class='box key'><b>Tư duy:</b> mỗi tính năng của Oracle đáng dùng khi bạn nêu được con số nó cải thiện và cái giá nó đòi. Hàng đợi đổi tải lấy tính nhất quán, phân mảnh đổi giao dịch một máy lấy khả năng chia tải.</div>""",
           """Điều cần mang theo. Mỗi tính năng của Oracle đáng dùng khi bạn nêu được con số nó cải thiện và cái giá nó đòi. Hàng đợi đổi tải lấy tính nhất quán, phân mảnh đổi giao dịch một máy lấy khả năng chia tải."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["Hàng đợi trong Oracle", "gửi cùng giao dịch với ghi sổ, hoàn tác thì thông điệp mất; nhận xong mặc định rời hàng; khác Kafka ở chỗ lưu lâu, đọc lại"],
                  ["Bộ nhớ cột", "đọc theo cột ít ô hơn cho báo cáo cộng một cột (8 cột: ít hơn 8 lần ô phải đọc); phải đo trên tải thật, vùng nhớ cột phải bật"],
                  ["Phân mảnh", "chia dữ liệu theo khoá; lệnh xuyên mảnh đắt; chỉ làm khi một máy hết sức"]]),
           """Nếu bị hỏi về dòng này trên hồ sơ, có ba ý. Hàng đợi trong Oracle gửi cùng giao dịch với ghi sổ. Bộ nhớ cột giảm số ô phải đọc nhưng phải đo trên tải thật. Phân mảnh chia dữ liệu theo khoá, lệnh xuyên mảnh đắt, nên chỉ làm khi một máy hết sức.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L38", "oracle_hang_doi_bo_nho_cot_phan_manh",
                  "Bài 38 — Hàng đợi AQ, bộ nhớ cột và phân mảnh Oracle",
                  "curriculum/bnx.yaml L38; audit/bnx/verify_bnx.py L38; audit/bnx/sources_l38.md: Oracle Database 23 (docs.oracle.com, đọc 2026-11-14): "
                  "PL/SQL Packages DBMS_AQADM/DBMS_AQ và AQ types (visibility ON_COMMIT), In-Memory Guide (INMEMORY_SIZE), Globally Distributed Database Guide; "
                  "Oracle AI Database 26ai Free 23.26.3 chạy thật trong Docker (hàng đợi); mã Python 3 + sqlite3 chạy thật; mọi số của mô hình ô và mảnh là số minh hoạ",
                  ["Tạo hàng đợi trong Oracle, gửi và nhận thông điệp trong giao dịch và chỉ ra thông điệp gửi rồi hoàn tác không còn trong hàng đợi",
                   "Nêu khác biệt của hàng đợi trong cơ sở dữ liệu so với Kafka và chọn một trong hai theo nhu cầu",
                   "Đọc thuộc tính INMEMORY của bảng và vùng nhớ cột trên Oracle, rồi nêu khi nào bộ nhớ cột đáng dùng",
                   "Đếm số ô phải đọc khi lưu theo hàng và theo cột ở 1 000 và 100 000 dòng",
                   "Đếm số lệnh chuyển xuyên mảnh ở 1, 3 và 30 mảnh và nêu khi nào cần phân mảnh",
                   "Kiểm kết quả hàng đợi bằng mô hình đếm cùng chuỗi thao tác",
                   "Viết hàng đợi có giao dịch và hàm đếm lệnh chuyển xuyên mảnh trên số liệu mới"],
                  scenes, assumes=["bnx_ban_sao_doc"],
                  covers=[(1, "formula"), (2, "quiz"), (3, "formula"), (4, "example"), (5, "quymo"), (6, "check"), (7, "practice")])
