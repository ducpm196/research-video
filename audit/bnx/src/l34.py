import lib2
from lib2 import *
from libj import jstep
from l16 import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
_st0 = st


def st(show, say, **kw):
    """Lời đọc: tên ngoại chưa có luật đọc → diễn đạt tiếng Việt (tên gốc vẫn hiện trên màn hình)."""
    return _st0(show, say.replace("sqlite", "cơ sở dữ liệu nhỏ"), **kw)


from labkit import write_lab, practice_scene

lib2.begin("L34")

# ── Mã chạy THẬT: Python 3 + sqlite3 (thư viện chuẩn). Đầu ra tất định: không in giờ; ngày là chuỗi cố định. Đệm ở audit/bnx/progcache/L34.json ──
PY_MAY = prog("MayTrangThai", r'''
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE cho_phep (tu TEXT, den TEXT);
CREATE TABLE ho_so (id INTEGER PRIMARY KEY, loai TEXT, tt TEXT);
CREATE TABLE lich_su (hs INTEGER, tu TEXT, den TEXT, nguoi TEXT);
""")
CANH = [("KHOI_TAO", "THAM_DINH"), ("THAM_DINH", "CHAM_DIEM"),
        ("THAM_DINH", "TU_CHOI"), ("CHAM_DIEM", "CHO_DUYET"),
        ("CHO_DUYET", "DA_DUYET"), ("CHO_DUYET", "TU_CHOI"),
        ("DA_DUYET", "GIAI_NGAN")]
db.executemany("INSERT INTO cho_phep VALUES (?, ?)", CANH)
db.execute("INSERT INTO ho_so VALUES (1, 'CN', 'KHOI_TAO')")


def chuyen(hs, den, nguoi):
    sql = "SELECT tt FROM ho_so WHERE id = ?"
    tu = db.execute(sql, (hs,)).fetchone()[0]
    sql = "SELECT 1 FROM cho_phep WHERE tu = ? AND den = ?"
    if not db.execute(sql, (tu, den)).fetchone():
        print(f"{tu} -> {den}: tu choi")
        return
    db.execute("UPDATE ho_so SET tt = ? WHERE id = ?", (den, hs))
    db.execute("INSERT INTO lich_su VALUES (?, ?, ?, ?)",
               (hs, tu, den, nguoi))
    print(f"{tu} -> {den}: {nguoi} ghi nhan")


chuyen(1, "GIAI_NGAN", "an")
chuyen(1, "THAM_DINH", "an")
chuyen(1, "CHAM_DIEM", "binh")
chuyen(1, "CHO_DUYET", "he_thong")
chuyen(1, "DA_DUYET", "chi")
chuyen(1, "KHOI_TAO", "chi")
chuyen(1, "GIAI_NGAN", "he_thong")
n = db.execute("SELECT COUNT(*) FROM lich_su").fetchone()[0]
tt = db.execute("SELECT tt FROM ho_so").fetchone()[0]
print("nhat ky:", n, "dong; trang thai cuoi:", tt)
''', lang="python", claims=["máy trạng thái chặn nhảy cóc và quay lui; 5 chuyển hợp lệ ghi nhật ký; trạng thái cuối GIAI_NGAN"])

PY_QUYEN = prog("PhanQuyen", r'''
BAC = {"CN": [(100, "chuyen vien"), (500, "truong phong"),
              (None, "hoi dong")],
       "DN": [(2000, "truong phong"), (10000, "giam doc khoi"),
              (None, "hoi dong")]}
HANG = {"chuyen vien": 1, "truong phong": 2,
        "giam doc khoi": 3, "hoi dong": 4}


def can_ai(loai, du_no, moi):
    tong = du_no + moi
    for tran, vai in BAC[loai]:
        if tran is None or tong <= tran:
            return tong, vai


def duoc_duyet(tao, duyet, vai_duyet, can):
    if tao == duyet:
        return "tu choi (tu duyet)"
    if HANG[vai_duyet] < HANG[can]:
        return "tu choi (thieu quyen)"
    return "dong y"


for loai, moi in [("CN", 80), ("CN", 300), ("CN", 900), ("DN", 3000)]:
    tong, vai = can_ai(loai, 0, moi)
    print(f"{loai} xin {moi}: tong {tong} -> {vai}")
du_no = 0
for moi in (90, 90, 90):
    tong, vai = can_ai("CN", du_no, moi)
    rieng = can_ai("CN", 0, moi)[1]
    print(f"ho so {moi}: rieng le {rieng}; theo tong {tong} -> {vai}")
    du_no += moi
print("an tao, an duyet:", duoc_duyet("an", "an", "truong phong", "truong phong"))
print("an tao, binh duyet (chuyen vien):", duoc_duyet("an", "binh", "chuyen vien", "truong phong"))
print("an tao, chi duyet (truong phong):", duoc_duyet("an", "chi", "truong phong", "truong phong"))
''', lang="python", claims=["quyền duyệt theo bậc và theo tổng dư nợ; ba hồ sơ 90 gộp thành 270 cần trưởng phòng; tự duyệt và thiếu quyền bị từ chối (số minh hoạ)"])

PY_LSU = prog("LichSuTinDung", r'''
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE dong_y (khach TEXT, muc_dich TEXT,
                     het_han TEXT, thu_hoi INT);
CREATE TABLE ls (khach TEXT, thang TEXT, nhom INT);
CREATE TABLE nhat_ky (nguoi TEXT, khach TEXT, muc_dich TEXT,
                      ngay TEXT, kq TEXT);
""")
db.executemany("INSERT INTO dong_y VALUES (?, ?, ?, ?)", [
    ("K1", "tham dinh", "2026-12-31", 0),
    ("K3", "tham dinh", "2026-01-31", 0),
    ("K4", "tham dinh", "2026-12-31", 1)])
db.executemany("INSERT INTO ls VALUES (?, ?, ?)", [
    ("K1", "2026-01", 1), ("K1", "2026-02", 2), ("K1", "2026-03", 1),
    ("K2", "2026-02", 5), ("K3", "2026-02", 3), ("K4", "2026-03", 4)])


def tra_cuu(nguoi, khach, muc_dich, ngay):
    sql = ("SELECT 1 FROM dong_y WHERE khach = ? AND muc_dich = ? "
           "AND het_han >= ? AND thu_hoi = 0")
    ok = db.execute(sql, (khach, muc_dich, ngay)).fetchone()
    kq = "cho phep" if ok else "tu choi"
    db.execute("INSERT INTO nhat_ky VALUES (?, ?, ?, ?, ?)",
               (nguoi, khach, muc_dich, ngay, kq))
    if not ok:
        return kq, None
    sql = "SELECT MAX(nhom) FROM ls WHERE khach = ?"
    return kq, db.execute(sql, (khach,)).fetchone()[0]


CA = [("an", "K1", "tham dinh", "2026-03-10"),
      ("an", "K2", "tham dinh", "2026-03-10"),
      ("an", "K3", "tham dinh", "2026-03-10"),
      ("an", "K4", "tham dinh", "2026-03-10"),
      ("an", "K1", "tiep thi", "2026-03-10")]
for nguoi, khach, md, ngay in CA:
    kq, nhom = tra_cuu(nguoi, khach, md, ngay)
    print(f"{khach} {md}: {kq}, nhom cao nhat {nhom}")
sql = "SELECT kq, COUNT(*) FROM nhat_ky GROUP BY kq ORDER BY kq"
for kq, dem in db.execute(sql):
    print("nhat ky", kq + ":", dem)
''', lang="python", claims=["tra cứu lịch sử chỉ khi có đồng ý còn hạn, đúng mục đích, chưa thu hồi; nhật ký ghi cả lần từ chối: 1 cho phép, 4 từ chối (số minh hoạ)"])

PY_KIEM = prog("KiemNhatKy", r'''
LOG = [("KHOI_TAO", "THAM_DINH"), ("THAM_DINH", "CHAM_DIEM"),
       ("CHAM_DIEM", "CHO_DUYET"), ("CHO_DUYET", "DA_DUYET"),
       ("DA_DUYET", "GIAI_NGAN")]
DUOC = {"KHOI_TAO": {"THAM_DINH"},
        "THAM_DINH": {"CHAM_DIEM", "TU_CHOI"},
        "CHAM_DIEM": {"CHO_DUYET"},
        "CHO_DUYET": {"DA_DUYET", "TU_CHOI"},
        "DA_DUYET": {"GIAI_NGAN"}}


def canh_sai(log):
    return sum(1 for tu, den in log if den not in DUOC.get(tu, set()))


def cho_dut(log):
    return sum(1 for a, b in zip(log, log[1:]) if a[1] != b[0])


print("canh sai trong nhat ky:", canh_sai(LOG))
print("cho dut:", cho_dut(LOG), "; trang thai dung lai:", LOG[-1][1])
print("xoa dong 3:", cho_dut(LOG[:2] + LOG[3:]), "cho dut")
''', lang="python", claims=["nhật ký đúng: 0 cạnh sai, 0 chỗ đứt, dựng lại GIAI_NGAN; xoá một dòng thì 1 chỗ đứt"])

PY_DUA = prog("HaiNguoiCungDuyet", r'''
import sqlite3


def thu(co_dieu_kien):
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE ho_so (id INTEGER PRIMARY KEY, tt TEXT)")
    db.execute("INSERT INTO ho_so VALUES (1, 'CHO_DUYET')")
    kq = []
    for ai in ("an", "binh"):
        sql = "UPDATE ho_so SET tt = 'DA_DUYET' WHERE id = 1"
        if co_dieu_kien:
            sql += " AND tt = 'CHO_DUYET'"
        ok = db.execute(sql).rowcount
        kq.append(ai + (" thanh cong" if ok else " bi tu choi"))
    return ", ".join(kq)


print("khong dieu kien:", thu(False))
print("co dieu kien:", thu(True))
''', lang="python", claims=["hai người cùng thấy CHO_DUYET: ghi không điều kiện cho cả hai thành công, ghi có điều kiện chỉ một người thành công"])

PY_QUYMO = prog("QuyMoTraCuu", r'''
import sqlite3
dem = 0
def tick():
    global dem
    dem += 1
    return 1
SQL = "SELECT COUNT(*) FROM ls WHERE tick() AND khach = 7"
for n in (1000, 1000000):
    db = sqlite3.connect(":memory:")
    db.create_function("tick", 0, tick)
    db.execute("CREATE TABLE ls (khach INT, thang INT, nhom INT)")
    db.executemany("INSERT INTO ls VALUES (?, ?, ?)",
                   ((i // 5, i % 5, i % 3) for i in range(n)))
    kq = []
    for co_chi_muc in (False, True):
        if co_chi_muc:
            db.execute("CREATE INDEX ix ON ls (khach)")
        kh = db.execute("EXPLAIN QUERY PLAN " + SQL).fetchone()[3]
        dem = 0
        db.execute(SQL).fetchone()
        kq.append(f"{kh.split()[0]} doc {dem}")
    print(f"{n} dong: khong chi muc {kq[0]}; co chi muc {kq[1]}")
''', lang="python", timeout=200, claims=["tra lịch sử một khách: không chỉ mục quét hết 1 000 và 1 000 000 dòng; có chỉ mục chỉ đọc 5 dòng ở cả hai cỡ"])

# ── Lab (cham.sh, Python): số liệu KHÁC ví dụ ──
LAB_PY = r'''
import sqlite3

BAC = [(50, "chuyen vien"), (200, "truong phong"), (None, "hoi dong")]
CANH = {("KHOI_TAO", "THAM_DINH"), ("THAM_DINH", "DUYET"),
        ("THAM_DINH", "TU_CHOI")}


def can_ai(du_no, moi):
    tong = du_no + moi
    for tran, vai in BAC:
        if tran is None or tong <= tran:
            return tong, vai


def chuyen(tu, den):
    return "cho phep" if (tu, den) in CANH else "tu choi"


db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE dong_y (khach TEXT, muc_dich TEXT, het_han TEXT, thu_hoi INT)")
db.execute("INSERT INTO dong_y VALUES ('K9', 'tham dinh', '2026-06-30', 0)")


def tra_cuu(khach, muc_dich, ngay):
    sql = "SELECT het_han, thu_hoi FROM dong_y WHERE khach = ? AND muc_dich = ?"
    row = db.execute(sql, (khach, muc_dich)).fetchone()
    if row is None:
        return "tu choi (khong co dong y)"
    if row[1]:
        return "tu choi (da thu hoi)"
    if row[0] < ngay:
        return "tu choi (het han)"
    return "cho phep"


for ten, du_no, moi in (("A", 120, 100), ("B", 0, 40)):
    tong, vai = can_ai(du_no, moi)
    print(f"ho so {ten}: tong {tong} -> {vai}")
print("THAM_DINH -> KHOI_TAO:", chuyen("THAM_DINH", "KHOI_TAO"))
for ngay in ("2026-05-31", "2026-07-01"):
    print("K9 tham dinh", ngay + ":", tra_cuu("K9", "tham dinh", ngay))
'''
LAB_OUT = """ho so A: tong 220 -> hoi dong
ho so B: tong 40 -> chuyen vien
THAM_DINH -> KHOI_TAO: tu choi
K9 tham dinh 2026-05-31: cho phep
K9 tham dinh 2026-07-01: tu choi (het han)"""
LAB_DE = """# Lab BNX L34 — Bậc duyệt theo tổng dư nợ, máy trạng thái và tra cứu có đồng ý

Số liệu (số minh hoạ, đơn vị triệu đồng; khác ví dụ trong bài):
- Bậc duyệt: tổng ≤ 50 → `chuyen vien`; ≤ 200 → `truong phong`; trên 200 → `hoi dong`.
- Hồ sơ A: dư nợ hiện có 120, xin thêm 100. Hồ sơ B: dư nợ 0, xin 40.
- Các cạnh được phép: `KHOI_TAO → THAM_DINH`, `THAM_DINH → DUYET`, `THAM_DINH → TU_CHOI`.
- Bảng `dong_y` có một dòng: khách `K9`, mục đích `tham dinh`, hết hạn `2026-06-30`, chưa thu hồi.

Viết `mau.py` in năm dòng:
1. `ho so A: tong <tổng> -> <vai trò>` và dòng tương tự cho hồ sơ B (tính theo TỔNG dư nợ cộng khoản mới).
2. `THAM_DINH -> KHOI_TAO: <cho phep | tu choi>` (quay lui có được phép không).
3. Hàm tra cứu: `K9 tham dinh <ngày>: cho phep` khi đồng ý còn hạn; ngược lại `tu choi (het han)` (ngày dạng `2026-05-31`, so sánh chuỗi). In cho hai ngày `2026-05-31` và `2026-07-01`.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L34 mau.py`.
"""


def build():
    write_lab("BNX", "L34", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Hồ sơ 270 triệu chia thành ba hồ sơ 90 triệu: ai được duyệt?", [
        st("""<p>Một khách xin vay <b>270 triệu đồng</b> (số minh hoạ). Quy tắc minh hoạ: không quá 100 triệu thì <b>chuyên viên</b> duyệt được; trên 100 đến 500 triệu cần <b>trưởng phòng</b>.
Khách chia thành <b>ba hồ sơ 90 triệu</b>: xét riêng, cả ba lọt qua chuyên viên.</p>
<div class="box key">Hệ thống phải chặn việc này thế nào? Khi nào được tra lịch sử tín dụng của khách? Và với <b>một triệu dòng</b> lịch sử, mỗi lần tra đọc bao nhiêu dòng?</div>""",
           """Chào bạn, một khách xin vay hai trăm bảy mươi triệu đồng, số minh hoạ. Chuyên viên duyệt khoản không quá một trăm triệu, trên đó cần trưởng phòng. Khách chia thành ba hồ sơ chín mươi triệu nên cả ba lọt qua chuyên viên. Hệ thống chặn việc này thế nào, và với một triệu dòng lịch sử thì mỗi lần tra đọc bao nhiêu dòng?""", focus=[1, 1, 2, 2, 2]),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["hồ sơ đi qua những bước nào", "một <b>máy trạng thái</b>: bảng liệt kê các bước chuyển được phép; bước lạ bị chặn"],
                  ["ai có quyền duyệt", "theo <b>tổng dư nợ</b> của khách (cũ + mới), và người duyệt khác người tạo"],
                  ["tra lịch sử tín dụng cần gì", "<b>đồng ý</b> của khách: đúng mục đích, còn hạn, chưa thu hồi; mọi lần tra có nhật ký"],
                  ["lịch sử lớn dần thì sao", "<b>chỉ mục</b> giữ số dòng đọc không đổi khi bảng lớn gấp nghìn lần"]]),
           """Bài này trả lời bốn câu: hồ sơ đi qua các bước nào, ai có quyền duyệt, tra lịch sử cần gì, và chỉ mục giúp gì khi lịch sử lớn dần.""",
           focus=[0, "1.2", "1.3", "1.5"], clear=True),
    ], checks=["alg.bnx_l34_nguoi_duyet('CN', 0, 90) == (90, 'chuyen vien')", "alg.bnx_l34_nguoi_duyet('CN', 180, 90) == (270, 'truong phong')"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① hồ sơ vay", "bộ thông tin một khách xin vay; đi qua nhiều bước, mỗi bước có người hoặc hệ thống phụ trách", "khởi tạo → thẩm định → chấm điểm → duyệt → giải ngân"],
                  ["② trạng thái", "nhãn cho biết hồ sơ đang ở bước nào; <b>chuyển trạng thái</b> là đổi nhãn", "<code>THAM_DINH</code> đổi thành <code>CHAM_DIEM</code>"],
                  ["③ dư nợ", "số tiền khách còn nợ; hạn mức duyệt tính trên dư nợ cộng khoản mới", "đang nợ 180, xin thêm 90 → 270"],
                  ["④ lịch sử tín dụng", "bản ghi vay và trả của khách; tóm thành <b>nhóm nợ</b> (bài dùng thang 1–5, số lớn là xấu hơn: số minh hoạ)", "nhóm cao nhất trong 12 tháng"],
                  ["⑤ chỉ mục", "bảng phụ giúp tìm dòng theo một cột mà không đọc cả bảng", "tìm theo mã khách"]]),
           """Trước hết ta cần hiểu năm điều. Hồ sơ vay đi qua nhiều bước, và trạng thái là nhãn cho biết hồ sơ ở bước nào. Hạn mức duyệt tính trên dư nợ cộng khoản mới. Lịch sử tín dụng tóm thành nhóm nợ, số lớn là xấu hơn. Chỉ mục là bảng phụ giúp tìm dòng mà không đọc cả bảng.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"]),
    ], checks=["180 + 90 == 270"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên", "nghĩa"],
                 [["<code>cho_phep</code>", "bảng các cặp (từ, đến) được phép chuyển: <b>luật</b> của máy trạng thái"],
                  ["<code>ho_so</code>", "mỗi dòng một hồ sơ: <code>id</code>, <code>loai</code> (<code>CN</code> cá nhân hay <code>DN</code> doanh nghiệp), <code>tt</code> (trạng thái hiện tại)"],
                  ["<code>lich_su</code>", "nhật ký chuyển trạng thái: hồ sơ nào, từ đâu, đến đâu, ai làm"],
                  ["<code>ls</code>", "lịch sử vay của khách: <code>khach</code>, <code>thang</code>, <code>nhom</code> (nhóm nợ)"],
                  ["<code>dong_y</code>", "đồng ý của khách: <code>muc_dich</code> (để làm gì), <code>het_han</code> (ngày hết), <code>thu_hoi</code> (1 là đã rút lại)"],
                  ["<code>nhat_ky</code>", "ghi mọi lần tra lịch sử: ai, khách nào, mục đích, ngày, kết quả"],
                  ["<code>SCAN</code>, <code>SEARCH</code>", "kế hoạch của cơ sở dữ liệu: quét cả bảng, hay tìm một phần của bảng qua chỉ mục"]]),
           """Bảng này giải mã các tên trên màn hình. Bảng cho phép chứa luật của máy trạng thái, bảng hồ sơ có loại cá nhân hoặc doanh nghiệp và trạng thái hiện tại, bảng lịch sử ghi từng lần chuyển. Bảng đồng ý ghi mục đích, ngày hết hạn và cờ thu hồi. Hai chữ quét và tìm là kế hoạch của cơ sở dữ liệu.""",
           focus=[0, "1.2", "1.3", "1.4", "1.6", "1.8"]),
    ], checks=["alg.bnx_l34_hop_le('THAM_DINH', 'CHAM_DIEM')"])

    intu = sc("intuition", "intuition", "Hình dung: máy trạng thái và đường tra cứu có đồng ý", [
        st(svg(1500, 470,
               txt(750, 34, "Máy trạng thái hồ sơ vay: chỉ đi theo mũi tên có trong bảng", 26, "middle", "#1f2937", True),
               '<path d="M130,120 L130,78 L1355,78 L1355,120" fill="none" stroke="#dc2626" stroke-width="3.5" stroke-dasharray="8 6" marker-end="url(#ah)"/>',
               txt(750, 68, "nhảy cóc thẳng tới giải ngân: không có trong bảng, bị chặn", 22, "middle", "#dc2626", True),
               box(40, 120, 180, 76, ["KHOI_TAO", "khởi tạo"], C_BLUE, 22, True), box(285, 120, 180, 76, ["THAM_DINH", "thẩm định"], C_BLUE, 22, True),
               box(530, 120, 180, 76, ["CHAM_DIEM", "chấm điểm"], C_BLUE, 22, True), box(775, 120, 180, 76, ["CHO_DUYET", "chờ duyệt"], C_AMBER, 22, True),
               box(1020, 120, 180, 76, ["DA_DUYET", "đã duyệt"], C_GREEN, 22, True), box(1265, 120, 190, 76, ["GIAI_NGAN", "giải ngân"], C_GREEN, 22, True),
               arrow(225, 158, 280, 158), arrow(470, 158, 525, 158), arrow(715, 158, 770, 158), arrow(960, 158, 1015, 158), arrow(1205, 158, 1260, 158),
               box(530, 300, 190, 76, ["TU_CHOI", "từ chối"], C_RED, 22, True),
               arrow(400, 200, 540, 296), arrow(860, 200, 715, 296),
               txt(750, 430, "mỗi mũi tên đi qua ghi một dòng vào nhật ký: hồ sơ, từ, đến, ai làm", 24, "middle", "#1f2937", True)),
           """Hình này là máy trạng thái của hồ sơ vay. Hồ sơ chỉ đi theo các mũi tên có trong bảng, và nhảy cóc thẳng tới giải ngân không có trong bảng nên bị chặn. Mỗi mũi tên đi qua ghi một dòng nhật ký."""),
        st(svg(1500, 470,
               txt(750, 40, "Tra lịch sử tín dụng: kiểm đồng ý trước, ghi nhật ký luôn luôn", 26, "middle", "#1f2937", True),
               box(40, 170, 270, 120, ["phiếu tra cứu", "ai, khách nào,", "mục đích, ngày"], C_BLUE, 22, True),
               box(380, 150, 430, 160, ["kiểm đồng ý", "đúng khách, đúng mục đích,", "còn hạn, chưa thu hồi"], C_AMBER, 22, True),
               box(900, 80, 300, 100, ["đọc lịch sử", "trả nhóm cao nhất thôi"], C_GREEN, 22, True),
               box(900, 280, 300, 100, ["từ chối", "không trả dữ liệu"], C_RED, 22, True),
               box(1260, 170, 210, 120, ["ghi nhật ký", "cả khi từ chối"], C_PURPLE, 22, True),
               arrow(315, 230, 375, 230), arrow(815, 200, 895, 140), arrow(815, 260, 895, 320), txt(835, 150, "đủ", 22, "middle", "#16a34a", True), txt(850, 345, "thiếu", 22, "middle", "#dc2626", True),
               arrow(1205, 130, 1290, 165), arrow(1205, 330, 1290, 295),
               txt(750, 440, "chỉ trả phần cần cho mục đích (nhóm cao nhất), không trả mọi dòng lịch sử", 24, "middle", "#1f2937", True)),
           """Hình thứ hai là đường tra lịch sử tín dụng. Bước kiểm đồng ý hỏi bốn điều: đúng khách, đúng mục đích, còn hạn, chưa thu hồi. Đủ bốn thì chỉ trả nhóm cao nhất, thiếu một thì từ chối, và cả hai nhánh đều ghi nhật ký."""),
    ], checks=["alg.bnx_l34_hop_le('CHO_DUYET', 'DA_DUYET') and not alg.bnx_l34_hop_le('KHOI_TAO', 'GIAI_NGAN')"])

    form = sc("formula", "formula", "Suy ra từng bước: từ hồ sơ tới quyền duyệt và đồng ý", [
        st("""<p><b>Cách đọc mã Python của bài này</b> (mỗi dòng: viết gì, nghĩa gì, ví dụ nhỏ):</p>"""
           + table(["viết trong mã", "nghĩa", "ví dụ nhỏ"],
                   [["<code>?</code> trong câu SQL", "chỗ giữ chỗ: giá trị truyền riêng ở tham số sau, đúng thứ tự", "<code>WHERE id = ?</code> với <code>(1,)</code> thành <code>WHERE id = 1</code>"],
                    ["<code>(hs,)</code>", "bộ giá trị; một phần tử thì phải có dấu phẩy", "<code>(7,)</code> là bộ một số"],
                    ["<code>.fetchone()[0]</code>", "lấy dòng kết quả đầu (một bộ), rồi <code>[0]</code> lấy giá trị đầu của bộ; không có dòng thì <code>None</code>", "dòng <code>(5,)</code> cho <code>5</code>"],
                    ["<code>executemany</code>", "chạy một câu SQL cho từng bộ trong danh sách", "7 bộ thì thêm 7 dòng"],
                    ["<code>f\"{tu} -&gt; {den}\"</code>", "chuỗi f: chỗ trong ngoặc nhọn được thay bằng giá trị biến", "<code>tu</code> là <code>A</code> thì ra <code>A -&gt; B</code>"]]),
           """Trước khi đọc mã, ta cần vài mẫu cú pháp. Dấu hỏi trong câu SQL là chỗ giữ chỗ, giá trị truyền riêng ở sau, và bộ một phần tử phải có dấu phẩy.
           Lấy một dòng trả về một bộ, nên thêm chỉ số không để lấy giá trị đầu. Chuỗi f thay chỗ trong ngoặc nhọn bằng giá trị biến.""",
           focus=[0, "2.2", "2.4", "2.6"], clear=True),
        jstep([(("<code>INSERT INTO ho_so VALUES (1, 'CN', 'KHOI_TAO')</code>", "thêm một dòng vào bảng <code>ho_so</code>; các giá trị theo đúng thứ tự cột", "Thêm một dòng vào bảng, giá trị theo thứ tự cột."), "", ""),
               (("<code>SELECT tt FROM ho_so WHERE id = ?</code>", "lấy cột <code>tt</code> từ bảng <code>ho_so</code>, chỉ ở các dòng thoả điều kiện sau <code>WHERE</code>", "Lấy một cột, chỉ ở các dòng thoả điều kiện."), "", ""),
               (("<code>UPDATE ho_so SET tt = ? WHERE id = ?</code>", "đổi giá trị cột <code>tt</code> ở các dòng thoả điều kiện sau <code>WHERE</code>", "Đổi giá trị một cột ở các dòng thoả điều kiện."), "", ""),
               (("<code>SELECT COUNT(*) FROM lich_su</code>, <code>MAX(nhom)</code>", "<code>COUNT(*)</code>: đếm số dòng; <code>MAX(cột)</code>: giá trị lớn nhất của cột", "Hàm đếm cho số dòng, hàm lớn nhất cho giá trị lớn nhất."), "", "")],
              intro="Mã dùng bốn kiểu câu SQL, nên ta đọc trước."),
        st("""<p><b>Bước 1. Luật là một bảng, không nằm rải rác trong mã.</b> Ta liệt kê mọi cặp (từ, đến) được phép vào bảng <code>cho_phep</code>. Cặp nào không có thì bị chặn.</p>"""
           + PY_MAY.show_from("CANH = [", 7, title="MayTrangThai.py (trích): bảy cạnh được phép"),
           """Bước một: luật là một bảng, không rải rác trong mã, nên thêm một bước chỉ là thêm một dòng, và cặp không có trong bảng thì bị chặn.
           Bài không dạy cách chấm điểm của ngân hàng nào, nên chấm điểm chỉ là một nhãn.""",
           clear=True),
        st("""<p><b>Bước 2. Đọc nhãn, kiểm luật, rồi mới đổi và ghi nhật ký.</b> <b>SQL</b> là ngôn ngữ hỏi và ghi bảng: <code>SELECT tt FROM ho_so WHERE id = 1</code> lấy cột <code>tt</code> của hồ sơ 1.</p>"""
           + PY_MAY.show_from("def chuyen", 11, title="MayTrangThai.py (trích): hàm chuyển"),
           """Bước hai: hàm đọc nhãn hiện tại, kiểm luật, rồi mới đổi nhãn và ghi nhật ký. Các câu lệnh trong hàm viết bằng SQL, ngôn ngữ để hỏi và ghi bảng, ví dụ câu lấy cột trạng thái của hồ sơ số một.
           Cặp không có luật thì in từ chối và dừng, nên nhật ký chỉ chứa bước hợp lệ.""",
           clear=True),
        st("""<p><b>Bước 3a. Bậc duyệt là dữ liệu.</b> <code>CN</code> là cá nhân, <code>DN</code> là doanh nghiệp. Mỗi cặp là <code>(trần, vai trò)</code>: tổng không vượt trần thì cần vai trò đó; <code>None</code> là không giới hạn. <code>HANG</code> cho mỗi vai trò một số để so cao thấp.</p>"""
           + PY_QUYEN.show(lines=(1, 8), title="PhanQuyen.py (trích): bậc và hạng"),
           """Bậc duyệt là dữ liệu. Có hai nhóm, cá nhân và doanh nghiệp, mỗi cặp gồm trần và vai trò cần, còn không có trần nghĩa là không giới hạn. Bảng hạng cho mỗi vai trò một số để so cao thấp.""",
           clear=True),
        st("""<p><b>Bước 3. Quyền duyệt theo bậc, tính trên TỔNG.</b> Hạn mức duyệt = dư nợ hiện có + khoản mới, không phải riêng khoản mới. Vòng <code>for</code> đi từ bậc thấp lên; gặp bậc đầu tiên mà tổng không vượt trần thì trả vai trò của bậc đó.</p>"""
           + PY_QUYEN.show_from("def can_ai", 6, title="PhanQuyen.py (trích)")
           + """$$\\text{tổng} = 180 + 90 = \\hl{270} \\Rightarrow \\text{trưởng phòng}$$""",
           """Bước ba: quyền duyệt theo bậc, tính trên tổng. Hạn mức là dư nợ hiện có cộng khoản mới, vì chỉ nhìn khoản mới thì khách chia nhỏ hồ sơ là lách được.
           Vòng lặp đi từ bậc thấp lên, gặp bậc đủ trần thì dừng. Nợ một trăm tám mươi triệu, xin thêm chín mươi, tổng hai trăm bảy mươi, rơi vào bậc trưởng phòng.""",
           clear=True),
        st("""<p><b>Bước 4. Hồ sơ doanh nghiệp khác cá nhân</b> (mô hình minh hoạ của bài):</p>"""
           + table(["điểm", "cá nhân", "doanh nghiệp"],
                   [["bậc 1 (số minh hoạ)", "≤ 100 triệu: chuyên viên", "≤ 2 000 triệu: trưởng phòng"],
                    ["bậc 2", "≤ 500 triệu: trưởng phòng", "≤ 10 000 triệu: giám đốc khối (người phụ trách một khối kinh doanh)"],
                    ["bậc 3", "trên 500: hội đồng (nhiều người cùng quyết)", "trên 10 000: hội đồng"],
                    ["nguồn trả nợ cần thẩm định", "thu nhập, nghĩa vụ trả nợ hiện có", "dòng tiền, báo cáo tài chính, tài sản bảo đảm (tài sản bên vay dùng để bảo đảm khoản vay)"],
                    ["dư nợ cần gộp", "của một khách", "của cả <b>nhóm bên liên quan</b> (các công ty có quan hệ sở hữu hoặc điều hành với nhau)"]]),
           """Bước bốn: hồ sơ doanh nghiệp khác cá nhân, theo mô hình minh hoạ. Bậc duyệt cao hơn vì số tiền lớn hơn, bậc hai do giám đốc khối, người phụ trách một khối kinh doanh, và trên đó là hội đồng. Cá nhân nhìn thu nhập, doanh nghiệp nhìn dòng tiền, báo cáo tài chính và tài sản bảo đảm, tức tài sản dùng để bảo đảm khoản vay. Dư nợ gộp cả nhóm bên liên quan, tức các công ty có quan hệ sở hữu hoặc điều hành với nhau.""",
           focus=[0, "2.3", "2.4", "2.5", "2.6"], clear=True, introduces=["bnx_nhom_ben_lien_quan"]),
        st("""<p><b>Bước 5. Tách người tạo khỏi người duyệt.</b> Theo bảng thuật ngữ của <b>NIST</b> (viện tiêu chuẩn và công nghệ của Mỹ), tách nhiệm vụ là nguyên tắc &laquo;no user should be given enough privileges to misuse the system on their own&raquo;.</p>"""
           + PY_QUYEN.show_from("def duoc_duyet", 6, title="PhanQuyen.py (trích)"),
           """Bước năm: tách người tạo khỏi người duyệt. Theo bảng thuật ngữ của một viện tiêu chuẩn của Mỹ, không ai được cấp đủ quyền để tự lạm dụng hệ thống.
           Hàm kiểm hai điều: người duyệt khác người tạo, và hạng vai trò đủ cao. Thiếu một thì từ chối.""",
           clear=True),
        jstep([(("<code>SELECT 1 FROM dong_y WHERE khach = ? AND muc_dich = ? AND het_han &gt;= ? AND thu_hoi = 0</code>", "<code>AND</code> nối các điều kiện: dòng phải thoả cả bốn; <code>SELECT 1</code> chỉ cần biết có dòng nào hay không", "Chữ nối đòi dòng thoả cả bốn điều kiện."), "", ""),
               (("<code>kq = \"cho phep\" if ok else \"tu choi\"</code>", "biểu thức điều kiện: <code>kq</code> là <code>cho phep</code> nếu <code>ok</code> có dòng, ngược lại <code>tu choi</code>", "Chọn kết quả theo có dòng khớp hay không."), "", "")],
              intro="Hàm tra cứu có hai chỗ mới."),
        st("""<p><b>Bước 6. Tra lịch sử: kiểm đồng ý, ghi nhật ký cả khi từ chối.</b></p>"""
           + PY_LSU.show_from("def tra_cuu", 12),
           """Bước sáu: tra lịch sử. Bốn điều kiện đồng ý nằm trong một câu truy vấn, và dù đủ hay thiếu đều ghi nhật ký, vì lần bị từ chối cũng là bằng chứng.
           Khi đủ, hàm chỉ trả nhóm cao nhất.""",
           clear=True),
        st("""<div class="box key"><b>Lưu ý pháp lý.</b> Luật về dữ liệu cá nhân và về tín dụng có yêu cầu riêng. Bài không trích điều khoản; bạn đọc văn bản hiện hành trước khi áp dụng.</div>""",
           """Lưu ý cuối: luật về dữ liệu cá nhân và về tín dụng có yêu cầu riêng. Bài không trích điều khoản, nên bạn đọc văn bản hiện hành trước khi áp dụng.""",
           clear=True),
    ], checks=["alg.bnx_l34_nguoi_duyet('CN', 180, 90) == (270, 'truong phong')", "alg.bnx_l34_duoc_duyet('an', 'chi', 'truong phong', 'truong phong') and not alg.bnx_l34_duoc_duyet('an', 'an', 'truong phong', 'truong phong')"])

    ex = sc("example", "example", "Ví dụ chạy thật, từng phép tính", [
        st(PY_MAY.show_from("chuyen(1, \"GIAI_NGAN\"", 10, title="MayTrangThai.py (trích): bảy lần thử chuyển"),
           """Phép tính thứ nhất là chạy máy trạng thái với bảy lần thử chuyển. Lần đầu nhảy cóc từ khởi tạo tới giải ngân, và các lần sau đi đúng đường, trừ một lần quay lui từ đã duyệt về khởi tạo.""",
           clear=True),
        st(PY_MAY.out_html()
           + """$$① \\; 7 \\text{ lần thử} = \\hl{5} \\text{ hợp lệ} + \\hl{2} \\text{ bị chặn}$$""",
           """Kết quả thật: nhảy cóc và quay lui đều bị từ chối. Năm lần còn lại hợp lệ nên nhật ký có năm dòng, và hồ sơ kết thúc ở giải ngân. Ở bước này ta chưa kiểm ai có quyền.""",
           clear=True),
        st(PY_QUYEN.out_html()
           + """$$② \\; 90 + 90 + 90 = \\hl{270}: \\; \\text{từng hồ sơ } 90 \\to \\text{chuyên viên; theo tổng} \\to \\hl{\\text{trưởng phòng}}$$""",
           """Phép tính thứ hai là quyền duyệt, chạy thật. Cá nhân xin tám mươi, ba trăm hoặc chín trăm triệu rơi vào ba bậc khác nhau, còn doanh nghiệp ba nghìn triệu vượt trần hai nghìn của bậc một nên cần giám đốc khối.
           Ba hồ sơ chín mươi triệu: xét riêng thì đều tới chuyên viên, theo tổng thì hồ sơ thứ hai và thứ ba cần trưởng phòng. Tự duyệt và thiếu quyền bị từ chối.""",
           clear=True),
        st(PY_LSU.show_from("CA = [", 11, title="LichSuTinDung.py (trích): năm ca tra cứu và đếm nhật ký")
           + """<p><code>GROUP BY kq</code> gom các dòng cùng giá trị cột <code>kq</code> thành một nhóm; <code>COUNT(*)</code> đếm dòng mỗi nhóm; <code>ORDER BY kq</code> xếp theo <code>kq</code>.</p>""",
           """Phép tính thứ ba là năm ca tra lịch sử trong cùng một ngày. Khách một có đồng ý còn hạn, khách hai không có, khách ba hết hạn, khách bốn đã thu hồi, và ca cuối là khách một nhưng sai mục đích.
           Câu cuối gom nhật ký theo kết quả, đếm mỗi nhóm rồi xếp theo tên.""",
           focus=[1, 1, 2],
           clear=True),
        st(PY_LSU.out_html()
           + """$$③ \\; \\text{5 ca tra: } \\hl{1} \\text{ cho phép, } \\hl{4} \\text{ từ chối; nhật ký ghi đủ } 5$$""",
           """Chỉ khách một được trả nhóm cao nhất là hai. Bốn ca còn lại bị từ chối, dù khách hai có nhóm năm trong dữ liệu. Nhật ký đếm một lần cho phép và bốn lần từ chối, khớp năm ca.""",
           clear=True),
    ], checks=["alg.bnx_l34_nguoi_duyet('CN', 0, 300) == (300, 'truong phong') and alg.bnx_l34_nguoi_duyet('DN', 0, 3000) == (3000, 'giam doc khoi')",
               "alg.bnx_l34_nguoi_duyet('CN', 90, 90) == (180, 'truong phong') and alg.bnx_l34_nguoi_duyet('CN', 180, 90)[0] == 270", "7 == 5 + 2 and 5 == 1 + 4"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: dựng lại trạng thái từ nhật ký", [
        st(table(["viết trong mã", "nghĩa", "ví dụ nhỏ"],
                 [["<code>sum(1 for x in log if …)</code>", "đếm các phần tử thoả điều kiện: mỗi phần tử đúng cộng 1", "<code>sum(1 for x in [3, 8, 9] if x &gt; 5)</code> cho <code>2</code>"],
                  ["<code>log[1:]</code>", "danh sách bỏ phần tử đầu", "<code>[1, 2, 3][1:]</code> là <code>[2, 3]</code>"],
                  ["<code>zip(log, log[1:])</code>", "ghép mỗi dòng với dòng kế tiếp", "<code>zip([1, 2, 3], [2, 3])</code> cho <code>(1, 2)</code>, <code>(2, 3)</code>"],
                  ["<code>DUOC.get(tu, set())</code>", "tra từ điển; không có khoá thì trả tập rỗng", "<code>{'a': 1}.get('b', 0)</code> cho <code>0</code>"]]),
           """Hàm kiểm dùng vài cách viết mới mà ta cần đọc trước. Hàm tổng cộng một cho mỗi phần tử đúng điều kiện, tức là phép đếm. Hàm ghép đôi đưa mỗi dòng nhật ký đi cùng dòng kế tiếp. Hàm tra từ điển có giá trị mặc định khi thiếu khoá.""",
           focus=[0, "1.2", "1.4", "1.5"], clear=True),
        st(PY_KIEM.show_from("def canh_sai", 8, title="KiemNhatKy.py: kiểm bằng từ điển, không dùng bảng"),
           """Ta kiểm bằng đường khác: dựng lại từ chính nhật ký năm dòng, không hỏi cơ sở dữ liệu. Hàm thứ nhất đếm cạnh sai theo từ điển luật. Hàm thứ hai đếm chỗ đứt, tức dòng sau không bắt đầu từ nơi dòng trước kết thúc.""",
           clear=True),
        st(PY_KIEM.out_html()
           + table(["cách", "kết luận"],
                   [["bảng luật trong cơ sở dữ liệu", "5 chuyển hợp lệ, 2 bị chặn"], ["từ điển luật + dựng lại từ nhật ký", "0 cạnh sai, 0 chỗ đứt, kết thúc GIAI_NGAN"],
                    ["xoá thử một dòng", "1 chỗ đứt: nhật ký bị sửa là lộ"]]),
           """Kết quả khớp: không cạnh sai, không chỗ đứt, dựng lại ra giải ngân. Xoá thử dòng thứ ba thì có một chỗ đứt, nên ai sửa nhật ký là bị lộ.""",
           focus=["3.3", "3.4"], clear=True),
    ], checks=["alg.bnx_l34_hop_le('DA_DUYET', 'GIAI_NGAN')"])

    quymo = sc("quymo", "example", "Khi lịch sử lớn dần: số dòng phải đọc mỗi lần tra", [
        st(table(["viết trong mã", "nghĩa", "ví dụ nhỏ"],
                 [["<code>global dem</code>", "cho hàm sửa biến <code>dem</code> nằm ngoài hàm, thay vì tạo biến mới", "mỗi lần gọi <code>tick()</code>, <code>dem</code> tăng 1"],
                  ["<code>create_function(\"tick\", 0, tick)</code>", "đăng ký hàm Python để câu SQL gọi được <code>tick()</code>", "mỗi dòng SQL đọc là một lần gọi"],
                  ["<code>i // 5</code>, <code>i % 5</code>", "chia lấy phần nguyên, chia lấy phần dư", "<code>7 // 5</code> là 1, <code>7 % 5</code> là 2"],
                  ["<code>(… for i in range(n))</code>", "sinh lần lượt n bộ giá trị, i chạy từ 0", "<code>i // 5</code> là mã khách: mỗi khách đúng 5 dòng"]]),
           """Bài đo này dùng vài cách viết mới. Từ khoá khai báo biến ngoài cho phép hàm sửa biến nằm ngoài hàm. Ta đăng ký hàm Python để câu SQL gọi, mỗi dòng đọc là một lần gọi.
           Chia lấy phần nguyên và phần dư cho ra mã khách và tháng, nên mỗi khách có đúng năm dòng.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st("""<p>Đo bằng hàm <code>tick()</code>: cơ sở dữ liệu gọi nó mỗi lần đọc một dòng của bảng <code>ls</code>.</p>"""
           + PY_QUYMO.show(lines=(1, 10), title="QuyMoTraCuu.py (1/2): hàm đếm dòng đọc và câu hỏi"),
           """Đây là số đo thật. Hàm đếm được gắn vào câu SQL, nên cơ sở dữ liệu gọi nó mỗi lần đọc một dòng. Câu hỏi là đếm các dòng của khách bảy.""",
           clear=True),
        jstep([(("<code>CREATE TABLE ls (khach INT, thang INT, nhom INT)</code>", "tạo bảng <code>ls</code> với ba cột, mỗi cột có kiểu số nguyên", "Tạo bảng với ba cột số nguyên."), "", ""),
               (("<code>CREATE INDEX ix ON ls (khach)</code>", "tạo <b>chỉ mục</b> tên <code>ix</code> trên cột <code>khach</code>: bảng phụ để tìm dòng theo khách mà không đọc cả bảng", "Tạo chỉ mục trên cột khách để tìm dòng nhanh."), "", ""),
               (("<code>EXPLAIN QUERY PLAN … .fetchone()[3]</code>", "hỏi kế hoạch thực hiện câu SQL thay vì chạy nó; <code>[3]</code> lấy cột thứ tư của dòng kế hoạch, là câu mô tả", "Hỏi kế hoạch thực hiện, và chỉ số ba lấy câu mô tả."), "", ""),
               (("<code>kh.split()[0]</code>", "cắt chuỗi <code>kh</code> ở khoảng trắng; <code>[0]</code> lấy từ đầu: <code>SCAN</code> (quét cả bảng) hoặc <code>SEARCH</code> (tìm qua chỉ mục)", "Cắt chuỗi ở khoảng trắng, lấy từ đầu: quét hoặc tìm."), "", "")],
              intro="Mã đo có bốn chỗ mới."),
        st("""<p>Mỗi khách có 5 dòng. Chạy hai lần: chưa có, rồi có <b>chỉ mục</b> theo cột <code>khach</code>; <code>EXPLAIN QUERY PLAN</code> hỏi kế hoạch của cơ sở dữ liệu.</p>"""
           + PY_QUYMO.show(lines=(11, 22), title="QuyMoTraCuu.py (2/2): bảng 1 000 và 1 000 000 dòng; thêm chỉ mục"),
           """Mỗi khách có năm dòng. Ta chạy câu hỏi hai lần: chưa có chỉ mục, rồi có chỉ mục theo cột khách. Kế hoạch của cơ sở dữ liệu cho biết nó quét cả bảng hay tìm qua chỉ mục.""",
           clear=True),
        st(PY_QUYMO.out_html()
           + """$$10^3 \\to 10^6 \\text{ dòng: không chỉ mục } \\hl{1\\,000} \\to \\hl{1\\,000\\,000}; \\; \\text{có chỉ mục } \\hl{5} \\to \\hl{5}$$""",
           """Bảng một nghìn dòng: không chỉ mục đọc cả một nghìn, có chỉ mục đọc năm dòng. Bảng một triệu dòng, gấp một nghìn lần: không chỉ mục đọc cả một triệu, có chỉ mục vẫn năm dòng.""",
           clear=True),
        st(table(["lựa chọn", "được", "mất"],
                 [["không chỉ mục", "đơn giản, ghi nhanh", "1 000 hồ sơ mỗi ngày × 10⁶ dòng = 10⁹ dòng đọc mỗi ngày"],
                  ["chỉ mục theo mã khách", "mỗi lần tra đọc 5 dòng, gần như không đổi theo cỡ bảng", "tốn chỗ và làm ghi chậm hơn một chút"],
                  ["lưu kết quả tra trong <b>bộ đệm</b> (nơi giữ sẵn kết quả đã tra)", "nhanh hơn nữa", "khách thu hồi đồng ý mà bộ đệm vẫn trả: <b>vi phạm đồng ý</b>"]]),
           """Bảng này là lựa chọn của người làm nghề. Không chỉ mục thì một nghìn hồ sơ mỗi ngày đọc một tỉ dòng. Chỉ mục giữ năm dòng mỗi lần, đổi lại tốn chỗ.
           Bộ đệm giữ sẵn kết quả đã tra, nhưng khách thu hồi đồng ý mà bộ đệm vẫn trả thì vi phạm đồng ý.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_l34_doc(1000, False) == 1000 and alg.bnx_l34_doc(1000000, False) == 1000000", "alg.bnx_l34_doc(1000, True) == 5 == alg.bnx_l34_doc(1000000, True)",
               "1000 * 10 ** 6 == 10 ** 9"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Xét quyền <b class="red">từng hồ sơ riêng lẻ</b>: ba hồ sơ 90 triệu đều lọt qua chuyên viên. Phải tính trên <b>tổng dư nợ</b>: hồ sơ thứ hai đã cần trưởng phòng.</div>""",
           """Lỗi thứ nhất, của người mới, là xét quyền từng hồ sơ riêng lẻ, nên ba hồ sơ chín mươi triệu đều lọt qua chuyên viên. Phải tính trên tổng dư nợ.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Hai người cùng thấy <code>CHO_DUYET</code> rồi cùng ghi <b class="red">không điều kiện</b>: cả hai &laquo;thành công&raquo;, nhật ký ghi hai lần duyệt. Ghi kèm điều kiện trạng thái cũ: chỉ một người thành công (bài <b>mô phỏng</b> bằng hai lần ghi nối tiếp). <code>sql += …</code> nối thêm vế điều kiện vào cuối câu SQL.</div>"""
           + PY_DUA.show_from("sql = \"UPDATE", 5, title="HaiNguoiCungDuyet.py (trích): thêm điều kiện nối vào câu SQL"),
           """Lỗi thứ hai, của người đã đi làm, lộ ra lúc mới dựng: hai người cùng thấy hồ sơ chờ duyệt rồi cùng ghi không điều kiện, nên cả hai thành công.
           Bản có điều kiện nối thêm vế đòi trạng thái cũ vẫn là chờ duyệt, và số dòng bị đổi cho biết ai thắng.""", clear=True),
        st(PY_DUA.out_html(title="Kết quả chạy thật — MÔ PHỎNG: hai lần ghi nối tiếp trên một kết nối, không phải hai người thật")
           + """<p><code>rowcount</code> là số dòng câu lệnh vừa đổi: 1 là thành công, 0 là điều kiện không còn đúng nên người đến sau bị từ chối.</p>""",
           """Đây là mô phỏng hai lần ghi nối tiếp. Bản không điều kiện cho cả hai thành công, còn bản có điều kiện chỉ người đầu thành công, vì lúc người sau ghi, trạng thái đã đổi.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc tải tăng).</b> Tra lịch sử theo khách mà <b class="red">không có chỉ mục</b>: nhỏ thì chạy tốt, rồi 10⁶ dòng và 1 000 hồ sơ mỗi ngày thành 10⁹ dòng đọc. Chạy thật: không chỉ mục đọc 1 000 000 dòng, có chỉ mục đọc 5.</div>""",
           """Lỗi thứ ba, lộ ra khi tải tăng: tra lịch sử theo khách mà không có chỉ mục. Nhỏ thì chạy tốt, rồi một triệu dòng với một nghìn hồ sơ mỗi ngày thành một tỉ dòng đọc.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 4 (người đã đi làm, lúc vận hành lâu dài).</b> Nhật ký <b class="red">chỉ ghi lần thành công</b>, hoặc ghi cả nội dung lịch sử vào nhật ký. Cần ghi cả lần bị từ chối (ai thử tra khách không đồng ý?) và <b>không</b> ghi nội dung nhạy cảm, chỉ ghi ai, khách nào, mục đích, ngày, kết quả.</div>"""
           + out("nhat ky cho phep: 1\nnhat ky tu choi: 4", "Kết quả chạy thật (trích)"),
           """Lỗi thứ tư, lộ ra khi vận hành lâu dài: nhật ký chỉ ghi lần thành công, hoặc ghi cả nội dung lịch sử. Cần ghi cả lần bị từ chối, và chỉ ghi ai, khách nào, mục đích, ngày và kết quả.""", clear=True),
    ], checks=["alg.bnx_l34_nguoi_duyet('CN', 90, 90)[1] == 'truong phong'", "alg.bnx_l34_doc(1000000, False) == 10 ** 6"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Bậc cá nhân: ≤ 100 chuyên viên, ≤ 500 trưởng phòng, trên 500 hội đồng (triệu đồng). Khách đang nợ 350, xin thêm 200. Ai duyệt? Nếu chỉ xét 200 thì ai, và sai ở đâu?"],
                  ["2", "Đồng ý của khách hết hạn ngày 2026-03-31, chưa thu hồi, đúng mục đích. Tra cứu ngày 2026-03-31 và ngày 2026-04-01: kết quả mỗi ngày? Điều kiện so sánh là <code>het_han >= ngay</code>."],
                  ["3", "Bảng lịch sử 2 triệu dòng, mỗi lần duyệt tra theo khách. Chọn: thêm chỉ mục theo mã khách, hay sao chép sang <b>kho đọc</b> (bản sao chỉ để đọc, đặt ở máy khác), hay lưu kết quả tra trong bộ đệm một ngày? Vì sao?"]]),
           """Đến lượt bạn. Câu một: khách nợ ba trăm năm mươi, xin thêm hai trăm, ai duyệt, và nếu chỉ xét hai trăm thì sai ở đâu? Câu hai: đồng ý hết hạn ngày ba mươi mốt tháng ba, tra cứu ngày đó và ngày mồng một tháng tư cho kết quả gì? Câu ba: bảng lịch sử hai triệu dòng, chọn chỉ mục, kho đọc hay bộ đệm, và vì sao? Hãy dừng lại làm ra giấy.""",
           pause=40, introduces=["bnx_kho_doc"]),
        st("""<p>Câu 1: tổng = dư nợ + khoản mới.</p>
$$350 + 200 = \\hlg{550} > 500 \\Rightarrow \\text{hội đồng}; \\quad \\text{chỉ xét } 200 \\to \\text{trưởng phòng: } \\hlg{\\text{sai bậc}}$$""",
           """Đáp án câu một. Tổng là ba trăm năm mươi cộng hai trăm, bằng năm trăm năm mươi, lớn hơn năm trăm, nên cần hội đồng. Nếu chỉ xét hai trăm thì ra trưởng phòng, sai bậc vì bỏ qua dư nợ cũ."""),
        st("""<p>Câu 2: so sánh chuỗi ngày theo thứ tự chữ cái; &laquo;lớn hơn hoặc bằng&raquo; nên ngày hết hạn vẫn còn hiệu lực.</p>
$$\\text{03-31}: 2026\\text{-}03\\text{-}31 \\ge 2026\\text{-}03\\text{-}31 \\Rightarrow \\hlg{\\text{cho phép}}; \\quad \\text{04-01}: 2026\\text{-}03\\text{-}31 < 2026\\text{-}04\\text{-}01 \\Rightarrow \\hlg{\\text{từ chối}}$$""",
           """Đáp án câu hai. Ngày ba mươi mốt tháng ba bằng ngày hết hạn, điều kiện lớn hơn hoặc bằng đúng, nên cho phép. Ngày mồng một tháng tư lớn hơn ngày hết hạn nên từ chối."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["chỉ mục theo mã khách", "mỗi lần đọc vài dòng; luôn đúng dữ liệu hiện tại và đồng ý hiện tại", "tốn chỗ, ghi chậm hơn một chút"],
                  ["sao chép sang kho đọc", "tách tải đọc khỏi bảng chính", "nhân đôi dữ liệu nhạy cảm; bản sao chậm nên có thể trả dữ liệu khi đồng ý đã thu hồi"],
                  ["bộ đệm một ngày", "nhanh nhất", "khách thu hồi giữa ngày mà vẫn trả dữ liệu: vi phạm đồng ý"]]),
           """Đáp án câu ba. Chỉ mục cho mỗi lần đọc vài dòng và luôn đúng đồng ý hiện tại, đổi lại tốn chỗ. Kho đọc nhân đôi dữ liệu nhạy cảm, và bản sao chậm có thể trả dữ liệu khi đồng ý đã thu hồi. Bộ đệm nhanh nhất nhưng thu hồi giữa ngày mà vẫn trả là vi phạm. Hợp lý là chọn chỉ mục.""",
           focus=[0, "1.2", "1.3", "1.4"]),
    ], checks=["alg.bnx_l34_nguoi_duyet('CN', 350, 200) == (550, 'hoi dong')", "alg.bnx_l34_con_han('2026-03-31', '2026-03-31') and not alg.bnx_l34_con_han('2026-03-31', '2026-04-01')", "alg.bnx_l34_nguoi_duyet('CN', 0, 200)[1] == 'truong phong'"])

    lab_pr = practice_scene(sc, "Tự làm: bậc duyệt, máy trạng thái và tra cứu có đồng ý", practice_steps2(
        st, "BNX", "L34",
        """<p><b>Đề</b> (số minh hoạ, triệu đồng): bậc ≤ 50 chuyên viên, ≤ 200 trưởng phòng, trên 200 hội đồng. Hồ sơ A: nợ 120, xin 100; hồ sơ B: nợ 0, xin 40. Cạnh được phép: <code>KHOI_TAO→THAM_DINH</code>, <code>THAM_DINH→DUYET</code>, <code>THAM_DINH→TU_CHOI</code>. Khách K9 đồng ý <code>tham dinh</code> tới <code>2026-06-30</code>. Viết <code>mau.py</code> in 5 dòng:</p>
<ol><li>vai trò cần cho A và B, theo tổng dư nợ</li><li>chuyển <code>THAM_DINH → KHOI_TAO</code> có được không</li><li>tra cứu K9 ngày <code>2026-05-31</code> và <code>2026-07-01</code></li></ol>
<p class="note">Định dạng năm dòng in ra nằm trong <code>de.md</code>.</p>""",
        """Bây giờ tới phần bạn tự làm trên máy, với số liệu mới. Tính vai trò cần của hồ sơ A và B theo tổng dư nợ.
        Kiểm xem chuyển từ thẩm định về khởi tạo có được không, rồi tra cứu khách K chín ở hai ngày. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> tổng = dư nợ + khoản mới, rồi duyệt từ bậc thấp lên cao tới khi tổng không vượt trần. Cạnh có trong tập hợp thì cho phép. Đồng ý còn hạn khi <code>het_han</code> không nhỏ hơn ngày tra.
Lời giải đầy đủ ở <code>labs/BNX/L34/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, tổng bằng dư nợ cộng khoản mới, rồi đi từ bậc thấp lên tới khi tổng không vượt trần. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=150), "BNX", "L34")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("luật là một bảng cạnh", "mỗi chuyển ghi nhật ký", "quyền theo tổng dư nợ", "đồng ý trước, nhật ký luôn", "chỉ mục giữ chi phí"),
           """Tổng kết: luật là một bảng cạnh được phép, và mỗi lần chuyển ghi một dòng nhật ký. Quyền duyệt tính theo tổng dư nợ, tra lịch sử kiểm đồng ý trước, và chỉ mục giữ chi phí tra không đổi."""),
        st("""<div class='box key'><b>Tư duy:</b> hệ thống phê duyệt là <b>bằng chứng có kiểm soát</b>: ai làm gì, lúc nào, theo luật nào, có đồng ý của ai. Mọi điều đó phải <b>kiểm được sau này</b>, không chỉ chạy đúng hôm nay.</div>""",
           """Điều cần mang theo. Hệ thống phê duyệt là bằng chứng có kiểm soát: ai làm gì, lúc nào, theo luật nào, có đồng ý của ai, và phải kiểm được sau này."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["Thiết kế luồng phê duyệt tín dụng thế nào?", "máy trạng thái: bảng cạnh được phép, chuyển ngoài bảng bị chặn, mỗi chuyển ghi nhật ký; ghi kèm điều kiện trạng thái cũ để hai người không cùng duyệt"],
                  ["Phân quyền duyệt theo hạn mức?", "bậc theo tổng dư nợ cũ + mới (chặn chia nhỏ hồ sơ), người duyệt khác người tạo, doanh nghiệp gộp cả nhóm bên liên quan"],
                  ["Truy vấn lịch sử tín dụng cần gì?", "đồng ý đúng mục đích, còn hạn, chưa thu hồi; trả phần cần thiết; nhật ký cả lần từ chối; chỉ mục theo mã khách"]]),
           """Về dòng phê duyệt tín dụng, đây là ba câu hay gặp. Luồng phê duyệt là máy trạng thái có nhật ký và ghi kèm điều kiện trạng thái cũ. Phân quyền theo tổng dư nợ để chặn chia nhỏ hồ sơ. Tra lịch sử cần đồng ý đúng mục đích.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st("""<p>Tiếp theo: <b>vận hành và bản thiết kế</b>, rồi <b>phỏng vấn thiết kế hệ thống</b>.</p>""",
           """Ở bài ba mươi lăm ta học vận hành và bản thiết kế, rồi ở bài ba mươi sáu ta tập phỏng vấn thiết kế hệ thống.""",
           forward_ref=True),
    ], checks=["alg.bnx_l34_hop_le('KHOI_TAO', 'THAM_DINH')"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L34", "he_thong_phe_duyet_tin_dung",
                  "Bài 34 — Phê duyệt tín dụng: máy trạng thái, quyền duyệt và tra lịch sử có đồng ý",
                  "curriculum/bnx.yaml L34; audit/bnx/verify_bnx.py L34; audit/bnx/sources_l34.md: SQLite (EXPLAIN QUERY PLAN, Query Planning), NIST CSRC Glossary (Separation of Duty) "
                  "(đọc 2026-11-14); mã Python 3 + sqlite3 chạy thật; mọi bậc duyệt, nhóm nợ, số tiền là số minh hoạ; bài không dạy chấm điểm của ngân hàng nào và không trích điều khoản pháp luật",
                  ["Chạy máy trạng thái hồ sơ vay từ khởi tạo tới giải ngân và chặn chuyển trạng thái không hợp lệ",
                   "Xác định người có quyền duyệt theo tổng dư nợ của khách và tách người tạo khỏi người duyệt",
                   "So sánh hồ sơ vay cá nhân với hồ sơ doanh nghiệp về bậc duyệt, nguồn trả nợ và dư nợ cần gộp",
                   "Chạy tra cứu lịch sử tín dụng chỉ khi có đồng ý còn hạn đúng mục đích và ghi nhật ký mọi lần tra",
                   "Kiểm nhật ký chuyển trạng thái bằng cách dựng lại trạng thái cuối và đếm cạnh sai",
                   "Đo số dòng phải đọc khi tra lịch sử có và không có chỉ mục ở 1 000 và 1 000 000 dòng",
                   "Viết hàm chọn người duyệt, hàm chặn chuyển trạng thái và hàm tra cứu có đồng ý trên số liệu mới"],
                  scenes, assumes=["bnx_explain"],
                  covers=[(1, "example"), (2, "example"), (3, "formula"), (4, "example"), (5, "check"), (6, "quymo"), (7, "practice")])
