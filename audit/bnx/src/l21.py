import lib2
from lib2 import *
from libj import jstep, nowrap
from spoken_b import _spoken
from labkit import write_lab, practice_scene

lib2.begin("L21")

# ── Mã hiện trên màn hình (chạy NGUYÊN VĂN ở audit/bnx/ver/l21.py và cổng screen_code) ──
STATE_PY = """BUOC = {"NOP": ["CHAM_DIEM"], "CHAM_DIEM": ["THAM_DINH", "TU_CHOI"],
        "THAM_DINH": ["DUYET", "TU_CHOI", "XET_TAY"],
        "XET_TAY": ["DUYET", "TU_CHOI"], "DUYET": ["DA_KY"],
        "DA_KY": ["GIAI_NGAN"], "GIAI_NGAN": [], "TU_CHOI": []}
def chuyen(tu, den):
    if den not in BUOC[tu]:
        raise ValueError(f"không được đi {tu} -> {den}")
    return den"""
STATE_RUN = """tt = "NOP"
for den in ["CHAM_DIEM", "THAM_DINH", "DUYET", "DA_KY", "GIAI_NGAN"]:
    tt = chuyen(tt, den)
print("hồ sơ tới", tt)
try:
    chuyen("DUYET", "GIAI_NGAN")
except ValueError as loi:
    print("chặn:", loi)"""
STATE_OUT = """hồ sơ tới GIAI_NGAN
chặn: không được đi DUYET -> GIAI_NGAN"""

GROUP_PY = """def nhom_no(ngay):      # Thông tư 31/2024/TT-NHNN, Điều 10
    for nhom, tran in ((1, 9), (2, 90), (3, 180), (4, 360)):
        if ngay <= tran:
            return nhom
    return 5
print([nhom_no(n) for n in (0, 9, 10, 90, 91, 180, 181, 360, 361)])"""
GROUP_OUT = "[1, 1, 2, 2, 3, 3, 4, 4, 5]"

DECIDE_PY = """NGUONG_DTI, NGUONG_DIEM = 50, 70     # số minh hoạ
def tham_dinh(thu_nhap, dang_tra, khoan_moi, nhom, thang):
    no = dang_tra + khoan_moi
    diem = ((35 if thu_nhap >= 15_000_000 else 20)
            + (25 if nhom == 1 else 0) + (20 if thang >= 24 else 10))
    if nhom >= 2:
        kq = "XET_TAY"
    elif no * 100 > NGUONG_DTI * thu_nhap or diem < NGUONG_DIEM:
        kq = "TU_CHOI"
    else:
        kq = "DUYET"
    return no * 100 / thu_nhap, diem, kq"""
DECIDE_RUN = """print(tham_dinh(20_000_000, 4_000_000, 5_000_000, 1, 36))
print(tham_dinh(20_000_000, 4_000_000, 7_000_000, 1, 36))
print(tham_dinh(20_000_000, 4_000_000, 5_000_000, 2, 36))"""
DECIDE_OUT = """(45.0, 80, 'DUYET')
(55.0, 80, 'TU_CHOI')
(45.0, 55, 'XET_TAY')"""

HASH_PY = """import hashlib
hd = "Hop dong vay 50000000 dong, ky han 12 thang\\n"
sua = hd.replace("50000000", "60000000")
a = hashlib.sha256(hd.encode()).hexdigest()
b = hashlib.sha256(sua.encode()).hexdigest()
print(a[:16], "dài", len(a))
print(b[:16], "dài", len(b))
print("số vị trí khác nhau:", sum(x != y for x, y in zip(a, b)))"""
HASH_OUT = """662097aa0554ed46 dài 64
93938eab15e6cccc dài 64
số vị trí khác nhau: 60"""

SIGN_SH = """printf 'Hop dong vay 50000000 dong, ky han 12 thang\\n' > hd.txt
openssl genrsa -out rieng.pem 2048 2>/dev/null
openssl rsa -in rieng.pem -pubout -out cong.pem 2>/dev/null
openssl dgst -sha256 -sign rieng.pem -out hd.sig hd.txt
openssl dgst -sha256 -verify cong.pem -signature hd.sig hd.txt
sed 's/50000000/60000000/' hd.txt > hd_sua.txt
openssl dgst -sha256 -verify cong.pem -signature hd.sig hd_sua.txt
cp hd.txt ten_khac.txt
openssl dgst -sha256 -verify cong.pem -signature hd.sig ten_khac.txt"""
SIGN_OUT = """Verified OK
Verification failure
Verified OK"""

OFS_PY = """ofs = ("UNG.DUNG.MAU,/I/PROCESS,NGUOI.DUNG/******/CN001,HS001,"
       "DIEN.THOAI:1:1=0901000111,DIEN.THOAI:2:1=0902000222,"
       "DIA.CHI:1:1=12 Le Loi,DIA.CHI:1:2=Quan 1")
truong = {}
for phan in ofs.split(",")[4:]:
    toa_do, gia_tri = phan.split("=", 1)
    ten, mv, sv = toa_do.split(":")
    truong.setdefault(ten, {})[(int(mv), int(sv))] = gia_tri
print(truong["DIEN.THOAI"])
print(len({mv for mv, sv in truong["DIEN.THOAI"]}), "số điện thoại")
print(truong["DIA.CHI"][(1, 2)])"""
OFS_OUT = """{(1, 1): '0901000111', (2, 1): '0902000222'}
2 số điện thoại
Quan 1"""

FRAUD_PY = """import hashlib
def dau_van_tay(may):
    chuoi = "|".join(may[k] for k in sorted(may))
    return hashlib.sha256(chuoi.encode()).hexdigest()[:12]
may_a = {"he": "Android 14", "man": "1080x2400", "mui": "UTC+7"}
may_b = dict(may_a, man="1170x2532")
ho_so = [("HS1", "CCCD 001", may_a), ("HS2", "CCCD 002", may_a),
         ("HS3", "CCCD 003", may_a), ("HS4", "CCCD 004", may_b)]
dem = {}
for ma, giay_to, may in ho_so:
    dem.setdefault(dau_van_tay(may), set()).add(giay_to)
print({k: len(v) for k, v in dem.items()})"""
FRAUD_OUT = "{'f7286011deef': 3, '3b0dc756fcb5': 1}"

NOTE_ILL = "<span class='note'>(mọi ngưỡng, trọng số và số tiền trong bài là số minh hoạ, không phải chính sách của tổ chức nào)</span>"
HD = "Hop dong vay 50000000 dong, ky han 12 thang\n"
A1 = {"he": "Android 14", "man": "1080x2400", "mui": "UTC+7"}
OFS_MSG = ("UNG.DUNG.MAU,/I/PROCESS,NGUOI.DUNG/******/CN001,HS001,DIEN.THOAI:1:1=0901000111,DIEN.THOAI:2:1=0902000222,"
           "DIA.CHI:1:1=12 Le Loi,DIA.CHI:1:2=Quan 1")



# ── AF2 (nhánh B): cảnh quy mô + lab. Chương trình quy mô chạy THẬT lúc import (đệm ở audit/bnx/progcache/L21.json) ──
QUYMO = prog("QuyMo", r'''
import hashlib
def dau_van_tay(may):
    chuoi = "|".join(may[k] for k in sorted(may))
    return hashlib.sha256(chuoi.encode()).hexdigest()[:12]
HE = ["Android 13", "Android 14", "iOS 17", "iOS 18"]
MAN = ["720x1600", "1080x2400", "1170x2532", "1290x2796", "1440x3200", "1080x1920"]
def ho_so(i):
    h = int(hashlib.sha256(f"hs{i}".encode()).hexdigest(), 16)
    return {"he": HE[h % 4], "man": MAN[h // 4 % 6], "mui": "UTC+7"}
for n in (5, 500, 50_000):
    dem = {}
    for i in range(n):
        dem.setdefault(dau_van_tay(ho_so(i)), set()).add(f"CCCD {i}")
    co = sum(len(v) for v in dem.values() if len(v) >= 3)
    print(n, "ho so,", len(dem), "ma khac nhau,", co, "ho so bi gan co")
''', lang="python", claims=["luật gắn cờ từ 3 giấy tờ trên cùng dấu vân tay: 0 hồ sơ bị gắn cờ ở 5 hồ sơ, 500 ở 500 hồ sơ, 50 000 ở 50 000 hồ sơ (chỉ 24 mã)"])

LAB_PY = r'''
import hashlib
thu, dang, moi = 14_000_000, 3_000_000, 3_000_000
dti = (dang + moi) * 100 / thu
diem = (35 if thu >= 15_000_000 else 20) + 25 + 20
kq = "TU_CHOI" if (dang + moi) * 100 > 50 * thu or diem < 70 else "DUYET"
hd = "Hop dong vay 14000000 dong, ky han 24 thang\n"
sua = hd.replace("24", "25")
a = hashlib.sha256(hd.encode()).hexdigest()
b = hashlib.sha256(sua.encode()).hexdigest()
print(f"DTI: {dti:.1f} %")
print("Diem:", diem)
print("Quyet dinh:", kq)
print("Ma bam goc:", a[:12])
print("Vi tri khac:", sum(x != y for x, y in zip(a, b)))
'''
LAB = prog("LabL21", LAB_PY, lang="python", kind="run")
LAB_DE = """# Lab BNX L21 — Thẩm định một hồ sơ và băm hợp đồng

Viết chương trình Python `mau.py` cho hồ sơ sau (số minh hoạ, khác ví dụ trong bài):

- thu nhập 14 000 000, đang trả 3 000 000 mỗi tháng, khoản mới trả 3 000 000 mỗi tháng; nhóm nợ 1; làm việc 30 tháng.
- **Tỉ lệ nghĩa vụ** = (đang trả + khoản mới) × 100 / thu nhập; in một chữ số thập phân.
- **Điểm** = thu nhập từ 15 000 000 trở lên 35 điểm, thấp hơn 20; nhóm nợ 1 được 25, nhóm khác 0; làm việc từ 24 tháng 20, ngắn hơn 10.
- **Quyết định**: `TU_CHOI` nếu tỉ lệ vượt 50 % (so bằng nhân chéo: `(đang trả + khoản mới) * 100 > 50 * thu nhập`) hoặc điểm dưới 70, ngược lại `DUYET`.
- **Hợp đồng**: chuỗi `"Hop dong vay 14000000 dong, ky han 24 thang\\n"` (có ký tự xuống dòng cuối). Băm SHA-256 bằng `hashlib` (`import hashlib`; `hashlib.sha256(chuoi.encode()).hexdigest()`), in 12 ký tự đầu của mã băm. Rồi đổi `24` thành `25` và đếm số vị trí (trong 64 ký tự) mà hai mã băm khác nhau.

In đúng năm dòng:

```
DTI: <số> %
Diem: <số>
Quyet dinh: <TU_CHOI hoặc DUYET>
Ma bam goc: <12 ký tự>
Vi tri khac: <số>
```

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L21 mau.py`.
""".replace("\\\\n", "\\n")


def build():
    write_lab("BNX", "L21", LAB_DE, "py", LAB_PY, LAB.out)
    hook = sc("hook", "hook", "21 giờ, một hồ sơ vay nộp qua ứng dụng: máy quyết định thế nào?", [
        st(f"""<p>21 giờ, một khách nộp hồ sơ vay trên ứng dụng. Thu nhập <b>20 triệu</b> đồng mỗi tháng, đang trả nợ cũ <b>4 triệu</b> mỗi tháng, khoản vay mới sẽ phải trả <b>5 triệu</b> mỗi tháng.</p>
<div class="box key">Không có nhân viên nào thức. Máy dựa vào đâu để <b>duyệt hay từ chối</b>? Khách <b>ký hợp đồng</b> thế nào khi không có giấy? Làm sao biết hồ sơ không phải của kẻ gian, và khi hồ sơ tăng lên hàng chục nghìn, luật chặn gian lận nào gãy trước?</div>
{NOTE_ILL}""",
           """Chào bạn, hai mươi mốt giờ, một khách nộp hồ sơ vay trên ứng dụng, thu nhập hai mươi triệu mỗi tháng, đang trả nợ bốn triệu, khoản mới năm triệu. Không có nhân viên nào thức, vậy máy dựa vào đâu để duyệt hay từ chối, và khách ký hợp đồng thế nào khi không có giấy? Khi số hồ sơ tăng lên hàng chục nghìn thì luật chặn gian lận nào gãy trước? Mọi số tiền trong bài là số minh hoạ.""",
           focus=[1, 2, 2, 3]),
    ], checks=["alg.bnx_dti(20_000_000, 4_000_000, 5_000_000) == 45",
               "alg.bnx_loan_path_ok(['NOP', 'CHAM_DIEM', 'THAM_DINH', 'DUYET', 'DA_KY', 'GIAI_NGAN']) == (True, -1)"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Phần trăm", "tỉ số nhân với 100", "9 trên 20 là 45%; (4 + 5) / 20 = 0,45"],
                  ["② Máy trạng thái", "một vật chỉ ở một trạng thái tại một lúc, và chỉ được đi theo các bước cho phép", "đèn giao thông: xanh → vàng → đỏ, không có xanh → đỏ"],
                  ["③ Hàm băm", "biến một chuỗi dài bất kỳ thành một mã độ dài cố định, gọi là <b>mã băm</b>; đổi một ký tự thì mã đổi gần như toàn bộ", "SHA-256, một hàm băm chuẩn, luôn cho 64 ký tự thập lục phân (chữ số và a–f)"],
                  ["④ Cặp khoá", "khoá riêng giữ kín để ký; khoá công khai phát cho mọi người để kiểm", "ký bằng khoá riêng, ai có khoá công khai cũng kiểm được"]]),
           """Trước hết ta cần hiểu bốn điều. Phần trăm là tỉ số nhân với một trăm, ví dụ chín trên hai mươi là bốn mươi lăm phần trăm. Máy trạng thái chỉ ở một trạng thái tại một lúc và chỉ đi theo các bước cho phép, giống đèn giao thông. Hàm băm biến chuỗi dài bất kỳ thành một mã độ dài cố định gọi là mã băm, và đổi một ký tự thì mã đổi gần như toàn bộ. Cặp khoá gồm khoá riêng để ký và khoá công khai để kiểm.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], introduces=["bnx_ma_bam", "bnx_thap_luc_phan"]),
    ], checks=["alg.bnx_dti(20, 4, 5) == 45 and 9 * 100 == 45 * 20",
               "len(alg.bnx_sha256_hex('a')) == 64 and len(alg.bnx_sha256_hex('a' * 1000)) == 64",
               "alg.bnx_loan_path_ok(['NOP', 'GIAI_NGAN']) == (False, 0)"])

    sym = sc("sym", "symbol", "Giải mã từ ngữ và nhóm nợ", [
        st(table(["từ", "nghĩa"],
                 [["LOS (Loan Origination System)", "hệ khởi tạo khoản vay: nhận hồ sơ, chấm điểm, thẩm định, duyệt, ký, tới lúc giải ngân (chuyển tiền vay cho khách)"],
                  ["LMS (Loan Management System)", "hệ quản lý khoản vay: sau giải ngân, giữ lịch trả nợ, thu nợ, theo dõi quá hạn, tất toán (trả hết nợ, đóng khoản vay)"],
                  ["DTI (debt-to-income)", "tỉ lệ nghĩa vụ trả nợ hằng tháng trên thu nhập hằng tháng"],
                  ["thẻ điểm (scorecard)", "bảng đổi từng đặc trưng của khách thành điểm rồi cộng lại"],
                  ["thẩm định (underwriting)", "áp các luật theo thứ tự để ra: duyệt, từ chối, hoặc chuyển người xét"],
                  ["ký số từ xa, ECM", "khoá riêng nằm ở nơi cấp chứng thư số (CA); chứng thư số là giấy điện tử xác nhận khoá công khai này của ai, do nơi cấp ký; ECM là kho lưu hồ sơ và văn bản"],
                  ["2FA, OTP, dấu vân tay thiết bị", "xác thực hai yếu tố; OTP là mã dùng một lần gửi tới điện thoại; dấu vân tay thiết bị là mã rút ra từ thuộc tính của máy"]]),
           """Bảng này giải mã các từ của bài. LOS là hệ khởi tạo khoản vay, còn LMS là hệ quản lý khoản vay sau giải ngân. DTI là tỉ lệ nghĩa vụ trả nợ trên thu nhập, thẻ điểm là bảng đổi đặc trưng thành điểm. Ký số từ xa để khoá riêng ở nơi cấp chứng thư, OTP là mã dùng một lần, và dấu vân tay thiết bị là mã rút ra từ thuộc tính của máy.""",
           focus=[["1.2", "1.3"], ["1.4", "1.5"], "1.6", "1.7", "1.8"],
           introduces=["bnx_los", "bnx_lms", "bnx_dti", "bnx_the_diem", "bnx_otp", "bnx_ecm"]),
        st(code(GROUP_PY, "Bảng nhóm nợ viết thành hàm: dò từng mốc trần") + out(GROUP_OUT)
           + "<p class='small'>Thông tư 31/2024/TT-NHNN, Điều 10, phần tính theo số ngày quá hạn; thông tư này đã được Thông tư 37/2025/TT-NHNN sửa đổi một số điều (chưa đối chiếu bản hợp nhất); văn bản còn các điều kiện khác, đọc nguyên văn trước khi áp dụng.</p>",
           """Lịch sử trả nợ tóm thành nhóm nợ theo Thông tư ba mươi mốt năm hai nghìn không trăm hai mươi tư, Điều mười, phần số ngày quá hạn. Chạy thật cho thấy ngày chín còn nhóm một, ngày mười sang nhóm hai, ngày chín mươi mốt sang nhóm ba. Thông tư này đã được thông tư năm hai nghìn không trăm hai mươi lăm sửa một số điều, nên phải đọc bản mới.""",
           focus=["2.2", "3.1", "3.1", 4], clear=True),
    ], checks=["[alg.bnx_debt_group(n) for n in (0, 9, 10, 90, 91, 180, 181, 360, 361)] == [1, 1, 2, 2, 3, 3, 4, 4, 5]",
               "alg.bnx_debt_group(9) == 1 and alg.bnx_debt_group(10) == 2 and alg.bnx_debt_group(91) == 3"])

    intu = sc("intuition", "intuition", "Hình dung: đường đi của hồ sơ, và chữ ký trên mã băm", [
        st(svg(1500, 470,
               panel(20, 20, 950, 400, "LOS: hệ khởi tạo khoản vay", C_BLUE),
               box(40, 110, 135, 90, ["NOP", "nộp"], C_GRAY, size=20, bold=True),
               box(195, 110, 135, 90, ["CHAM_DIEM", "chấm điểm"], C_GRAY, size=20, bold=True),
               box(350, 110, 135, 90, ["THAM_DINH", "thẩm định"], C_AMBER, size=20, bold=True),
               box(505, 110, 135, 90, ["DUYET", "duyệt"], C_GREEN, size=20, bold=True),
               box(660, 110, 135, 90, ["DA_KY", "đã ký"], C_PURPLE, size=20, bold=True),
               box(815, 110, 140, 90, ["GIAI_NGAN", "giải ngân"], C_GREEN, size=20, bold=True),
               arrow(175, 155, 192, 155), arrow(330, 155, 347, 155), arrow(485, 155, 502, 155), arrow(640, 155, 657, 155), arrow(795, 155, 812, 155),
               box(272, 290, 215, 80, ["TU_CHOI", "từ chối"], C_RED, size=20, bold=True),
               arrow(262, 203, 330, 285, "#dc2626"), arrow(417, 203, 400, 285, "#dc2626"),
               box(540, 290, 190, 80, ["XET_TAY", "xét tay"], C_AMBER, size=20, bold=True),
               arrow(470, 203, 560, 287), arrow(620, 287, 590, 203), arrow(540, 330, 490, 330, "#dc2626"),
               txt(845, 320, "không có đường tắt", 20, "middle", "#dc2626", True),
               txt(845, 352, "DUYET → GIAI_NGAN", 20, "middle", "#dc2626", True),
               panel(1030, 20, 450, 400, "LMS: hệ quản lý khoản vay", C_GREEN),
               box(1060, 90, 390, 65, "lịch trả nợ từng kỳ", C_GRAY, size=22),
               box(1060, 170, 390, 65, "thu nợ, ghi nhận đã trả", C_GRAY, size=22),
               box(1060, 250, 390, 65, "quá hạn → nhóm nợ", C_AMBER, size=22),
               box(1060, 330, 390, 65, "tất toán", C_GRAY, size=22),
               arrow(958, 155, 1025, 155, "#16a34a"),
               txt(750, 455, "Trước giải ngân là việc của LOS; sau giải ngân là việc của LMS", 24, "middle", "#1f2937", True)),
           """Hình này là đường đi của một hồ sơ vay. Bên trái là LOS với sáu trạng thái từ nộp tới giải ngân, không có đường tắt từ duyệt tới giải ngân vì chưa ký thì chưa có hợp đồng. Bên phải là LMS, lo việc sau giải ngân."""),
        st(svg(1500, 480,
               panel(20, 20, 700, 370, "Lúc ký", C_BLUE),
               box(50, 90, 190, 110, ["hợp đồng", "(tệp)"], C_GRAY, size=22, bold=True),
               box(285, 90, 190, 110, ["băm", "SHA-256", "→ mã băm"], C_AMBER, size=22, bold=True),
               box(520, 90, 180, 110, ["ký bằng", "khoá riêng", "→ chữ ký"], C_PURPLE, size=22, bold=True),
               arrow(240, 145, 280, 145), arrow(475, 145, 515, 145),
               txt(370, 260, "Ký số từ xa: khoá riêng nằm ở nơi cấp chứng thư,", 21, "middle", "#1f2937"),
               txt(370, 292, "người ký xác nhận từng lần ký (ví dụ bằng mã OTP)", 21, "middle", "#1f2937"),
               txt(370, 345, "chữ ký gắn với mã băm của NỘI DUNG, không gắn tên tệp", 21, "middle", "#9333ea", True),
               panel(780, 20, 700, 370, "Lúc kiểm", C_GREEN),
               box(810, 90, 200, 110, ["tệp nhận được", "→ băm lại"], C_AMBER, size=22, bold=True),
               box(810, 240, 200, 110, ["chữ ký +", "khoá công khai"], C_PURPLE, size=22, bold=True),
               box(1090, 165, 150, 110, ["so", "khớp?"], C_GRAY, size=22, bold=True),
               arrow(1010, 150, 1085, 200), arrow(1010, 290, 1085, 245),
               box(1300, 100, 165, 80, "khớp: hợp lệ", C_GREEN, size=20, bold=True),
               box(1300, 260, 165, 80, "lệch: đã bị sửa", C_RED, size=20, bold=True),
               arrow(1240, 200, 1295, 150, "#16a34a"), arrow(1240, 240, 1295, 290, "#dc2626"),
               txt(750, 440, "Kho hồ sơ (ECM) lưu ba thứ: đúng tệp đã ký, chữ ký, mã băm", 24, "middle", "#1f2937", True)),
           """Hình thứ hai là cơ chế ký số. Lúc ký, hợp đồng được băm, rồi khoá riêng ký lên mã băm. Lúc kiểm, người nhận băm lại tệp rồi dùng khoá công khai so với chữ ký, khớp thì hợp lệ, lệch thì đã bị sửa."""),
    ])

    form = sc("formula", "formula", "Suy ra từng bước: trạng thái, thẩm định, ký, chống gian lận, gửi lõi", [
        st(table(["viết trong mã Python", "nghĩa"],
                 [["<code>{\"A\": [\"B\"]}</code>, <code>BUOC[tu]</code>", "bảng tra: khoá A ứng với danh sách <code>[\"B\"]</code>; <code>BUOC[tu]</code> lấy danh sách của <code>tu</code>"],
                  ["<code>if den not in …: raise ValueError(…)</code>", "nếu <code>den</code> không có trong danh sách thì báo lỗi, dừng hàm"],
                  ["<code>try: … except ValueError as loi:</code>", "thử chạy khối trên; nếu có lỗi loại đó thì chạy khối dưới, lỗi nằm trong <code>loi</code>"],
                  ["<code>f\"… {tu} …\"</code>", "chuỗi có chỗ điền giá trị của biến đặt trong ngoặc nhọn"],
                  ["<code>d.setdefault(k, set()).add(x)</code>", "lấy mục k của bảng (chưa có thì tạo tập rỗng) rồi thêm x"],
                  ["<code>zip(a, b)</code>, <code>sum(x != y for x, y in zip(a, b))</code>", "ghép từng cặp phần tử của hai chuỗi; mỗi cặp khác nhau tính 1, <code>sum</code> cộng lại: đếm số vị trí khác nhau"]]),
           """Trước khi đọc mã, ta nhắc vài cú pháp Python vì mã dùng chúng liên tục. Bảng tra ghi mỗi trạng thái đi được tới đâu, và lệnh báo lỗi dừng hàm khi bước đi không có trong bảng. Khối thử bắt lỗi đó.""", clear=True),
        st(code(STATE_PY, "Bước 1. Máy trạng thái của hồ sơ: bảng các bước được phép"),
           """Bước một, ta viết máy trạng thái bằng Python: một bảng ghi từ mỗi trạng thái được đi tới đâu. Hàm chuyển kiểm bước đi có trong bảng không, vì nếu không kiểm thì một lỗi có thể giải ngân hồ sơ chưa ký.""",
           focus=[1, "2.1"], clear=True),
        st(code(STATE_RUN) + out(STATE_OUT, "Làm thử — kết quả chạy thật"),
           """Làm thử: cho hồ sơ đi đúng năm bước thì máy in hồ sơ tới giải ngân. Nhảy từ duyệt thẳng sang giải ngân thì máy chặn, vì bước đó không có trong bảng.""",
           focus=["1.1", "3.2"], clear=True),
        st("""<p><b>Bước 2.</b> Tỉ lệ nghĩa vụ trả nợ trên thu nhập (DTI). Khoản vay mới làm tăng số tiền phải trả mỗi tháng, nên ta cộng nó vào nợ đang trả rồi mới chia:</p>
$$\\text{DTI} = \\frac{\\text{đang trả} + \\text{khoản mới}}{\\text{thu nhập}} \\cdot 100\\%$$
<span class='note'>Làm thử: (4 + 5) / 20 = 45%. Ngưỡng minh hoạ 50%: 45% không vượt nên qua. Ngưỡng là chính sách của từng tổ chức, không phải hằng số.</span>""",
           """Bước hai là tỉ lệ nghĩa vụ trên thu nhập. Khoản mới làm tăng số tiền phải trả mỗi tháng, nên ta cộng nó vào nợ đang trả rồi chia cho thu nhập. Chín chia hai mươi là bốn mươi lăm phần trăm, không vượt ngưỡng nên qua.""",
           focus=[1, 1, 3, 3], clear=True),
        st(table(["Bước 3: thẻ điểm (trọng số minh hoạ)", "điều kiện", "điểm"],
                 [["thu nhập", "từ 15 triệu trở lên / thấp hơn", "35 / 20"],
                  ["lịch sử trả nợ", "nhóm 1 / nhóm khác", "25 / 0"],
                  ["thời gian làm việc", "từ 24 tháng / ngắn hơn", "20 / 10"],
                  ["tổng của khách trong ví dụ", "20 triệu, nhóm 1, 36 tháng", "35 + 25 + 20 = 80"]])
           + "<span class='note'>Ngưỡng duyệt minh hoạ: 70 điểm. 80 không thấp hơn 70 nên qua.</span>",
           """Bước ba là thẻ điểm với trọng số minh hoạ. Khách trong ví dụ có ba mươi lăm cộng hai mươi lăm cộng hai mươi, bằng tám mươi điểm, không thấp hơn ngưỡng bảy mươi nên qua.""",
           focus=[[1, 2, 3], 4, 5], clear=True),
        jstep([(("<code>(35 if thu_nhap &gt;= 15_000_000 else 20)</code>", "biểu thức điều kiện: giá trị là 35 nếu thu nhập từ 15 triệu trở lên, ngược lại là 20; <code>15_000_000</code>: dấu gạch dưới chỉ để dễ đọc số", "Biểu thức điều kiện cho giá trị đầu nếu điều kiện đúng, ngược lại cho giá trị sau; dấu gạch dưới trong số chỉ để dễ đọc."), "thu nhập 20 triệu ra 35", ""),
               (("<code>return no * 100 / thu_nhap, diem, kq</code>", "trả về ba giá trị một lúc; nơi gọi nhận cả bộ ba", "Một hàm có thể trả về ba giá trị một lúc, và nơi gọi nhận cả bộ ba."), "<code>(45.0, 80, 'DUYET')</code>", "")],
              intro="Mã quyết định dùng hai chỗ mới nên ta giải trước."),
        st(code(DECIDE_PY, "Bước 4. Bộ máy quyết định: luật loại trước, rồi tỉ lệ, rồi điểm"),
           """Bước bốn ghép thành bộ máy quyết định, và thứ tự luật quan trọng. Nhóm nợ từ hai trở lên thì chuyển người xét, rồi tỉ lệ vượt hoặc điểm thấp thì từ chối, còn lại là duyệt. Phép so dùng nhân chéo vì làm tròn có thể cho qua hồ sơ vừa vượt ngưỡng.""",
           focus=[1, "2.6", "2.8"], clear=True),
        jstep([(("<code>hashlib.sha256(hd.encode()).hexdigest()</code>", "<code>import hashlib</code> nạp thư viện băm; <code>encode()</code> đổi chuỗi chữ thành dãy byte; <code>sha256</code> băm nó; <code>hexdigest()</code> viết mã băm bằng chữ số thập lục phân", "Đổi chuỗi thành dãy byte, băm rồi viết mã băm bằng chữ số thập lục phân."), "ra chuỗi 64 ký tự", ""),
               (("<code>a[:16]</code>, <code>len(a)</code>", "cắt lát: <code>a[:16]</code> là 16 ký tự đầu của a; <code>len(a)</code>: số ký tự", "Cắt lát lấy mười sáu ký tự đầu, còn hàm độ dài đếm số ký tự."), "<code>662097aa0554ed46</code>", ""),
               (("<code>hd.replace(\"50000000\", \"60000000\")</code>", "bản sao của chuỗi với mọi chỗ <code>50000000</code> đổi thành <code>60000000</code>", "Hàm thay chữ tạo bản sao của chuỗi với chữ cũ đổi thành chữ mới."), "đổi một ký tự 5 thành 6", "")],
              intro="Bước năm dùng ba cú pháp mới nên ta giải trước."),
        st(code(HASH_PY, "Bước 5. Băm hợp đồng, rồi đổi đúng một ký tự (5 thành 6)") + out(HASH_OUT),
           """Bước năm là băm hợp đồng. Ta đổi đúng một ký tự, số năm thành số sáu, rồi băm cả hai bản. Hai mã cùng dài sáu mươi tư ký tự nhưng khác nhau ở sáu mươi vị trí, nên sửa một ký tự là lộ.""",
           focus=["2.2", "2.3", "4.3"], clear=True),
        st(table(["lệnh vỏ ở bước 6 (sắp chạy)", "nghĩa"],
                 [["<code>printf '…' &gt; hd.txt</code>", "<code>printf</code> in chữ; dấu <code>&gt;</code> ghi chữ đó vào tệp <code>hd.txt</code> thay vì hiện ra màn hình"],
                  ["<code>sed 's/50000000/60000000/' hd.txt &gt; hd_sua.txt</code>", "đọc <code>hd.txt</code>, đổi chữ <code>50000000</code> thành <code>60000000</code>, ghi kết quả vào <code>hd_sua.txt</code>"],
                  ["<code>cp hd.txt ten_khac.txt</code>", "sao chép tệp sang tên khác, nội dung giữ nguyên"]]),
           """Ba lệnh vỏ mới, vì bước ký cần tệp: ghi chữ ra tệp, thay chữ rồi ghi tệp khác, và sao chép tệp.""", clear=True),
        st(table(["phần của lệnh ở bước 6 (sắp chạy)", "nghĩa"],
                 [["<code>genrsa 2048</code>", "sinh khoá RSA (thuật toán dùng cặp khoá riêng và công khai) dài 2048 bit (bit là chữ số 0 hoặc 1); <code>rieng.pem</code> là tệp khoá"],
                  ["<code>2&gt;/dev/null</code>", "bỏ các dòng thông báo phụ, chỉ giữ kết quả chính"],
                  ["<code>rsa -pubout</code>", "lấy khoá công khai ra từ khoá riêng"],
                  ["<code>dgst -sha256 -sign … -out hd.sig</code>; <code>-verify … -signature hd.sig</code>", "băm tệp rồi ký bằng khoá riêng, chữ ký ghi vào <code>hd.sig</code> / kiểm chữ ký trong <code>hd.sig</code> của tệp bằng khoá công khai"],
                  ["dòng <code>error:…</code>", "kiểm thất bại thì openssl còn in dòng lỗi ra luồng lỗi (nơi in thông báo lỗi, tách khỏi kết quả); màn hình lược bớt"]]),
           """Trước khi ký, đây là các phần của lệnh sắp chạy: sinh khoá dài hai nghìn không trăm bốn mươi tám bit và bỏ thông báo phụ. Ta ký bằng khoá riêng nên kiểm được bằng khoá công khai.""", clear=True, introduces=["bnx_genrsa"]),
        st(code(SIGN_SH, "Bước 6. Ký và kiểm bằng cặp khoá (openssl; chỉ minh hoạ phần toán, không có chứng thư)") + out(SIGN_OUT),
           """Bước sáu, ta ký thật bằng công cụ mật mã dòng lệnh. Ba lệnh đầu tạo hợp đồng và cặp khoá, lệnh sau cho khoá riêng ký lên mã băm. Tệp gốc hợp lệ, tệp sửa một ký tự thất bại, còn bản sao mang tên khác vẫn hợp lệ vì chữ ký gắn với nội dung.""",
           focus=[1, "2.4", "4.2", "4.3"], clear=True),
        st(table(["viết trong mã Python", "nghĩa"],
                 [["<code>dict(may_a, man=\"1170x2532\")</code>", "sao chép từ điển <code>may_a</code> rồi đặt (hoặc ghi đè) khoá <code>man</code>"],
                  ["<code>\"|\".join(may[k] for k in sorted(may))</code>", "lấy giá trị theo thứ tự khoá đã sắp xếp, nối thành một chuỗi, ngăn bằng <code>|</code>"],
                  ["<code>for ma, giay_to, may in ho_so:</code>", "mỗi phần tử của <code>ho_so</code> là một bộ ba, tách vào ba biến <code>ma</code>, <code>giay_to</code>, <code>may</code>"],
                  ["<code>….hexdigest()[:12]</code>", "cắt lát: chỉ giữ 12 ký tự đầu của mã băm"]]),
           """Đoạn mã tiếp theo còn dùng thêm bốn chỗ nữa. Lệnh sao chép từ điển rồi ghi đè một khoá, lệnh nối lấy giá trị theo thứ tự khoá, vòng lặp tách bộ ba, và cắt lát giữ mười hai ký tự đầu.""", clear=True),
        st(code(FRAUD_PY, "Bước 7. Dấu vân tay thiết bị: đếm số giấy tờ khác nhau trên một máy"),
           """Bước bảy chống gian lận có hai lớp. Lớp một là xác thực hai yếu tố, ngoài mật khẩu còn cần mã OTP gửi tới thứ khách có. Lớp hai là dấu vân tay thiết bị, vì kẻ gian hay nộp nhiều hồ sơ từ một máy: ta băm thuộc tính của máy rồi đếm giấy tờ khác nhau dùng chung mã.""",
           focus=[1, 1, "2.2"], clear=True),
        st(out(FRAUD_OUT, "Kết quả chạy thật")
           + "<div class='box key'>Một mã có 3 giấy tờ khác nhau → gắn cờ, chuyển người xét (ngưỡng 3 là số minh hoạ; <code>CCCD</code> là căn cước công dân, giấy tờ tuỳ thân). Dấu vân tay là <b>tín hiệu rủi ro, không phải danh tính</b>.</div>",
           """Kết quả chạy thật: một máy nộp ba căn cước khác nhau nên bị gắn cờ. Đó chỉ là tín hiệu rủi ro, không phải danh tính.""",
           clear=True),
        st(code(OFS_PY, "Bước 8. Trường đa trị trong bản tin gửi lõi (mẫu minh hoạ, tên trường giả định)", lines=(1, 3))
           + table(["phần", "nghĩa"],
                   [["DIEN.THOAI:1:1 và DIEN.THOAI:2:1", "trường điện thoại có hai giá trị: giá trị thứ 1 và giá trị thứ 2"],
                    ["DIA.CHI:1:1 và DIA.CHI:1:2", "giá trị thứ 1 của địa chỉ gồm hai phần con: phần 1 và phần 2"]]),
           """Bước tám, hồ sơ được ghi vào lõi ngân hàng, tức phần mềm giữ tài khoản và khoản vay, tên là T24. Hồ sơ đi bằng bản tin OFS, và vì một trường có nhiều giá trị nên mỗi giá trị kèm hai số vị trí: thứ tự giá trị, và thứ tự phần con trong giá trị.""",
           focus=[1, 1, "2.2"], clear=True, introduces=["bnx_ofs"]),
        jstep([(("<code>ofs.split(\",\")[4:]</code>", "cắt chuỗi ofs ở mỗi dấu phẩy thành danh sách; <code>[4:]</code> lấy từ phần thứ 4 (đếm từ 0) tới hết, tức bỏ bốn phần đầu", "Cắt chuỗi ở mỗi dấu phẩy thành danh sách, rồi lấy từ phần thứ tư tới hết, tức bỏ bốn phần đầu."), "bỏ <code>UNG.DUNG.MAU</code>, <code>/I/PROCESS</code>, …, <code>HS001</code>", ""),
               (("<code>truong.setdefault(ten, {})[(int(mv), int(sv))] = gia_tri</code>", "lấy bảng con của <code>ten</code> (chưa có thì tạo rỗng), rồi ghi giá trị vào ô có khoá là cặp số vị trí <code>(mv, sv)</code>", "Lấy bảng con của tên trường, chưa có thì tạo rỗng, rồi ghi giá trị vào ô có khoá là cặp số vị trí."), "<code>(1, 1)</code> ứng với <code>0901000111</code>", ""),
               (("<code>len({mv for mv, sv in truong[\"DIEN.THOAI\"]})</code>", "tập hợp sinh sẵn <code>{… for …}</code> gom các <code>mv</code> không trùng nhau; <code>len</code> đếm số phần tử", "Tập hợp sinh sẵn gom các số không trùng nhau, rồi hàm độ dài đếm chúng."), "hai số điện thoại", "")],
              intro="Chương trình tách bản tin dùng ba chỗ mới nên ta giải trước."),
        st(code(OFS_PY) + out(OFS_OUT, "Bước 8 (tiếp) — kết quả chạy thật: tách bản tin thành từng trường"),
           """Chương trình bỏ bốn phần đầu rồi tách từng phần theo dấu bằng và dấu hai chấm. Kết quả chạy thật cho hai số điện thoại ở hai vị trí, và phần con thứ hai của địa chỉ.""",
           focus=["1.5", "3.1"], clear=True),
    ], checks=["alg.bnx_loan_path_ok(['NOP', 'CHAM_DIEM', 'THAM_DINH', 'DUYET', 'DA_KY', 'GIAI_NGAN']) == (True, -1)",
               "alg.bnx_loan_path_ok(['DUYET', 'GIAI_NGAN']) == (False, 0)",
               "alg.bnx_dti(20_000_000, 4_000_000, 5_000_000) == 45 and alg.bnx_dti_pass(20_000_000, 4_000_000, 5_000_000, 50)",
               "alg.bnx_scorecard(20_000_000, 1, 36) == (35, 25, 20, 80)",
               "alg.bnx_scorecard(10_000_000, 2, 12) == (20, 0, 10, 30)",
               "alg.bnx_underwrite(20_000_000, 4_000_000, 5_000_000, 1, 36) == 'DUYET'",
               f"alg.bnx_sha256_hex({HD!r})[:16] == '662097aa0554ed46'",
               f"alg.bnx_sha256_hex({HD!r}.replace('50000000', '60000000'))[:16] == '93938eab15e6cccc'",
               f"alg.bnx_hex_diff(alg.bnx_sha256_hex({HD!r}), alg.bnx_sha256_hex({HD!r}.replace('50000000', '60000000'))) == 60",
               f"alg.bnx_device_fp({A1!r}) == 'f7286011deef' and alg.bnx_device_fp(dict({A1!r}, man='1170x2532')) == '3b0dc756fcb5'",
               f"sorted(alg.bnx_fp_counts([('HS1', 'CCCD 001', {A1!r}), ('HS2', 'CCCD 002', {A1!r}), ('HS3', 'CCCD 003', {A1!r}), ('HS4', 'CCCD 004', dict({A1!r}, man='1170x2532'))]).values()) == [1, 3]",
               f"alg.bnx_ofs_fields({OFS_MSG!r})['DIEN.THOAI'] == {{(1, 1): '0901000111', (2, 1): '0902000222'}}",
               f"alg.bnx_ofs_fields({OFS_MSG!r})['DIA.CHI'][(1, 2)] == 'Quan 1'"])

    ex = sc("example", "example", "Ví dụ một hồ sơ, từng phép tính", [
        st(f"""<p>Thu nhập <b>20 triệu</b>, đang trả <b>4 triệu</b>, khoản mới trả <b>5 triệu</b> mỗi tháng; nhóm nợ 1; làm việc 36 tháng. {NOTE_ILL}</p>
$$① \\; \\text{{nghĩa vụ mỗi tháng}} = 4 + 5 = \\hl{{9}} \\text{{ triệu}}$$""",
           """Hồ sơ này có thu nhập hai mươi triệu, đang trả bốn triệu, khoản mới năm triệu. Phép tính thứ nhất, nghĩa vụ mỗi tháng là bốn cộng năm, bằng chín triệu."""),
        st("""<p>Dùng lại 9 triệu ở phép ①.</p>
$$② \\; \\text{DTI} = \\frac{9}{20} = \\hl{45\\%} \\leq 50\\% \\;\\Rightarrow\\; \\text{qua}$$""",
           """Phép tính thứ hai, tỉ lệ là chín chia hai mươi, bằng bốn mươi lăm phần trăm, không vượt ngưỡng năm mươi nên qua."""),
        st("""$$③ \\; \\text{điểm} = 35 + 25 + 20 = \\hl{80} \\geq 70 \\;\\Rightarrow\\; \\text{qua}$$""",
           """Phép tính thứ ba, thẻ điểm là ba mươi lăm cộng hai mươi lăm cộng hai mươi, bằng tám mươi, không thấp hơn bảy mươi nên qua."""),
        st("""<p>Nhóm nợ 1, phép ② qua, phép ③ qua.</p>
$$④ \\; \\text{quyết định} = \\hlg{\\text{DUYET}};\\quad \\text{khoản trả mới tối đa} = 50\\% \\cdot 20 - 4 = \\hl{6} \\text{ triệu}$$""",
           """Phép tính thứ tư, nhóm nợ một nên không bị loại, quyết định là duyệt, và khoản trả mới tối đa là mười triệu trừ bốn triệu, còn sáu triệu.""",
           clear=True),
        st("""<p>Hồ sơ đã duyệt thì sang bước ký: băm hợp đồng mẫu ghi 50 000 000 đồng.</p>
$$⑤ \\; \\text{mã băm ban đầu: } \\texttt{662097aa…};\\quad \\text{đổi 5 thành 6: } \\texttt{93938eab…} \\;\\Rightarrow\\; \\hl{\\text{chữ ký không còn khớp}}$$""",
           """Phép tính thứ năm, mã băm của hợp đồng ban đầu và bản đổi một ký tự khác hẳn nhau, nên chữ ký tạo từ hợp đồng ban đầu không còn khớp với bản sửa.""",
           clear=True),
    ], checks=["4 + 5 == 9 and alg.bnx_dti(20, 4, 5) == 45",
               "alg.bnx_dti_pass(20_000_000, 4_000_000, 5_000_000, 50) is True",
               "alg.bnx_scorecard(20_000_000, 1, 36)[3] == 80 and 80 >= 70",
               "alg.bnx_underwrite(20_000_000, 4_000_000, 5_000_000, 1, 36) == 'DUYET'",
               "alg.bnx_max_new_payment(20_000_000, 4_000_000, 50) == 6_000_000",
               f"alg.bnx_sha256_hex({HD!r}).startswith('662097aa') and alg.bnx_sha256_hex({HD!r}.replace('5', '6', 1)).startswith('93938eab')"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: để máy quyết định, rồi thử hai hồ sơ lân cận", [
        st(code(DECIDE_RUN, "Gọi bộ máy quyết định ở bước 4 với ba hồ sơ") + out(DECIDE_OUT),
           """Kiểm bằng đường khác: gọi bộ máy ở bước bốn với ba hồ sơ. Hồ sơ đầu duyệt, khớp tính tay. Hồ sơ hai có khoản mới bảy triệu nên bị từ chối, hồ sơ ba ở nhóm nợ hai nên chuyển người xét.""",
           focus=[1, "4.1", "4.2", "4.3"]),
        st(table(["cách kiểm", "phép tính", "kết luận"],
                 [["nhân chéo, không chia", "9 × 100 = 900 không lớn hơn 50 × 20 = 1000", "tỉ lệ qua"],
                  ["tính ngược từ khoản tối đa", "6 − 5 = 1 triệu còn dư", "khoản mới 5 triệu nằm trong giới hạn"],
                  ["bản sao hợp đồng mang tên khác", "kiểm chữ ký: hợp lệ", "chữ ký theo nội dung, không theo tên tệp"]]),
           """Bảng này kiểm thêm: nhân chéo thì chín trăm không lớn hơn một nghìn nên qua, và bản sao tên khác vẫn hợp lệ vì chữ ký theo nội dung.""",
           focus=["1.2", "1.3", "1.4"], clear=True),
    ], checks=["9 * 100 <= 50 * 20 and alg.bnx_dti_pass(20, 4, 5, 50)",
               "alg.bnx_underwrite(20_000_000, 4_000_000, 7_000_000, 1, 36) == 'TU_CHOI' and alg.bnx_dti(20, 4, 7) == 55",
               "alg.bnx_underwrite(20_000_000, 4_000_000, 5_000_000, 2, 36) == 'XET_TAY' and alg.bnx_scorecard(20_000_000, 2, 36)[3] == 55",
               "alg.bnx_max_new_payment(20_000_000, 4_000_000, 50) - 5_000_000 == 1_000_000"])

    quymo = sc("quymo", "example", "Khi hồ sơ tăng lên: luật gắn cờ theo dấu vân tay còn đúng không?", [
        jstep([(("<code>int(hashlib.sha256(f\"hs{i}\".encode()).hexdigest(), 16)</code>", "băm chuỗi <code>hs0</code>, <code>hs1</code>… ra mã thập lục phân; <code>int(…, 16)</code> đổi mã đó thành một số nguyên lớn <code>h</code>", "Băm chuỗi mã hồ sơ, rồi đổi mã thập lục phân thành một số nguyên lớn."), "mỗi hồ sơ có một số h cố định", ""),
               (("<code>HE[h % 4]</code>, <code>MAN[h // 4 % 6]</code>", "<code>h % 4</code>: phần dư khi chia h cho 4, tức số 0 tới 3, chọn một phần tử của danh sách <code>HE</code>; <code>h // 4 % 6</code>: chia lấy phần nguyên cho 4 rồi lấy phần dư khi chia cho 6", "Phần dư chọn một phần tử của danh sách, còn chia lấy phần nguyên rồi lấy dư chọn kiểu màn hình."), "4 hệ điều hành × 6 màn hình = 24 kiểu máy", "")]),
        st(QUYMO.show(lines=(1, 9), title="QuyMo.py (trích): quần thể minh hoạ, mỗi hồ sơ một giấy tờ, chỉ 24 kiểu máy"),
           """Ta thử luật gắn cờ khi hồ sơ tăng. Quần thể minh hoạ có mỗi hồ sơ một giấy tờ khác nhau, nhưng chỉ hai mươi bốn kiểu máy. Luật cũ gắn cờ khi một mã có từ ba giấy tờ trở lên.""",
           clear=True),
        st(QUYMO.show(lines=(10, 15), title="QuyMo.py (tiếp): đếm, rồi đo ở 5, 500 và 50 000 hồ sơ") + QUYMO.out_html(),
           """Kết quả chạy thật: năm hồ sơ không ai bị gắn cờ, còn năm trăm và năm mươi nghìn hồ sơ thì tất cả bị gắn cờ, vì chỉ còn hai mươi bốn mã.""",
           clear=True),
        st(table(["số hồ sơ N", "mã khác nhau", "bị gắn cờ", "người xét cần mỗi ngày (40 hồ sơ mỗi người, số minh hoạ)"],
                 [[nowrap("5 (×1)"), "5", "0", "0"],
                  [nowrap("500 (×100)"), "24", "500", "13"],
                  [nowrap("50 000 (×10 000)"), "24", "50 000", "1 250"]]),
           """Luật chỉ có nghĩa khi quần thể nhỏ. Ở năm trăm hồ sơ tất cả bị gắn cờ, cần mười ba người xét mỗi ngày nếu mỗi người xét bốn mươi hồ sơ. Ở năm mươi nghìn hồ sơ cần một nghìn hai trăm năm mươi người.""",
           focus=[0, "1.2", "1.3"], clear=True),
        st(table(["cách chữa", "được", "mất"],
                 [["nâng ngưỡng theo quy mô", "ít cờ oan", "kẻ gian có chỗ lách; phải chỉnh lại mỗi khi quy mô đổi"],
                  ["thêm thuộc tính vào dấu vân tay", "nhiều mã hơn, ít trùng", "mã giòn hơn: khách đổi hệ điều hành thì mã đổi"],
                  ["đếm trong một cửa sổ thời gian ngắn", "bắt cụm nộp dồn dập", "bỏ sót kẻ nộp rải rác nhiều ngày"],
                  ["coi dấu vân tay là một điểm rủi ro, không chặn", "người xét chỉ nhận ca nhiều tín hiệu", "phải có thêm tín hiệu khác để chấm"]]),
           """Người làm nghề phải chọn và chấp nhận đánh đổi. Nâng ngưỡng thì ít cờ oan nhưng kẻ gian có chỗ lách, thêm thuộc tính thì mã ít trùng nhưng giòn hơn. An toàn nhất là coi dấu vân tay chỉ là một điểm rủi ro.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], clear=True),
    ], checks=["alg.bnx_l21_scale(5) == (5, 0)", "alg.bnx_l21_scale(500) == (24, 500)", "alg.bnx_l21_scale(50_000) == (24, 50_000)",
               "[alg.bnx_l21_reviewers(f, 40) for f in (0, 500, 50_000)] == [0, 13, 1250]",
               "500 // 5 == 50_000 // 500 == 100 and 50_000 // 5 == 10_000",
               "4 * 6 == 24"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Coi ngưỡng 50% và 70 điểm là hằng số của nghề, và nghĩ chữ ký gắn với <b>tên tệp</b>.
<br><span class="note">Đúng: ngưỡng là chính sách của từng tổ chức, đặt thành cấu hình. Chữ ký gắn với nội dung đã băm: đổi tên tệp không sao, đổi một ký tự nội dung là lộ.</span></div>""",
           """Lỗi thứ nhất, của người mới, là coi ngưỡng năm mươi phần trăm và bảy mươi điểm là hằng số, và nghĩ chữ ký gắn với tên tệp. Thật ra ngưỡng là chính sách nên đặt thành cấu hình, còn chữ ký gắn với nội dung đã băm."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Tính tỉ lệ bằng phép chia lấy phần nguyên rồi mới so ngưỡng. Thu nhập 20 000 000, đang trả 4 000 000, khoản mới 6 190 000:</div>
$$\\frac{10\\,190\\,000}{20\\,000\\,000} = 50{,}95\\% \\;\\text{bị cắt còn}\\; 50\\% \\;\\Rightarrow\\; \\text{qua sai}$$
<span class="note">Cách chữa: so bằng nhân chéo trên số nguyên, 1 019 000 000 lớn hơn 1 000 000 000 nên vượt; viết ca kiểm (phép thử viết sẵn) ngay tại biên, tức đúng giá trị ngưỡng, nơi dễ sai nhất.</span>""",
           """Lỗi thứ hai, của người đã đi làm, là chia lấy phần nguyên rồi mới so ngưỡng. Tỉ lệ thật là năm mươi phẩy chín mươi lăm nhưng bị cắt còn năm mươi, nên qua sai. Cách chữa là nhân chéo trên số nguyên và kiểm ngay tại biên.""",
           focus=[1, 2, 3], clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc vận hành lâu dài).</b> Kho hồ sơ chỉ lưu dữ liệu hợp đồng, khi cần thì <b>sinh lại tệp</b> từ mẫu. Một năm sau mẫu đổi một dấu cách: tệp sinh lại có mã băm khác, chữ ký cũ không còn kiểm được.
<br><span class="note">Cách chữa: lưu đúng tệp đã ký, chữ ký và mã băm; việc đồng bộ sang kho chỉ xong khi băm lại tệp trong kho ra đúng mã đã ký.</span></div>""",
           """Lỗi thứ ba lộ ra khi vận hành lâu: kho chỉ lưu dữ liệu rồi sinh lại tệp từ mẫu. Mẫu đổi một dấu cách thì tệp mới có mã băm khác, nên chữ ký cũ không kiểm được. Hãy lưu đúng tệp đã ký.""",
           clear=True),
    ], checks=["float(alg.bnx_dti(20_000_000, 4_000_000, 6_190_000)) == 50.95",
               "(4_000_000 + 6_190_000) * 100 // 20_000_000 == 50 and not alg.bnx_dti_pass(20_000_000, 4_000_000, 6_190_000, 50)",
               "10_190_000 * 100 == 1_019_000_000 and 50 * 20_000_000 == 1_000_000_000",
               "alg.bnx_sha256_hex('Hop dong  vay') != alg.bnx_sha256_hex('Hop dong vay')",
               f"alg.bnx_device_fp({A1!r}) == alg.bnx_device_fp(dict({A1!r}))"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề (dùng ngưỡng và thẻ điểm minh hoạ của bài)"],
                 [["1", "Thu nhập 30 triệu, đang trả 6 triệu, khoản mới trả 10 triệu mỗi tháng. Tỉ lệ là bao nhiêu, có qua ngưỡng 50% không? Khoản trả mới tối đa là bao nhiêu?"],
                  ["2", "Khách quá hạn 95 ngày thuộc nhóm nợ mấy? Một khách khác thu nhập 12 triệu, nhóm 1, làm việc 12 tháng được bao nhiêu điểm, có đạt 70 không?"],
                  ["3", "Quyết định: ba hồ sơ với ba căn cước khác nhau cùng một dấu vân tay thiết bị. Từ chối tự động cả ba, hay chuyển người xét kèm xác thực thêm?"]]),
           """Đến lượt bạn. Câu một, thu nhập ba mươi triệu, đang trả sáu triệu, khoản mới mười triệu, tỉ lệ bao nhiêu, có qua ngưỡng không? Câu hai, quá hạn chín mươi lăm ngày thuộc nhóm nào, và khách thu nhập mười hai triệu, nhóm một, làm việc mười hai tháng được bao nhiêu điểm? Câu ba, ba hồ sơ cùng một dấu vân tay thì từ chối tự động hay chuyển người xét? Hãy dừng video.""",
           focus=[0, "1.2", "1.3", "1.4"], pause=25),
        st("""$$\\frac{6 + 10}{30} = \\frac{16}{30} \\approx 53{,}3\\% > 50\\% \\;\\Rightarrow\\; \\hl{\\text{không qua}};\\quad 50\\% \\cdot 30 - 6 = \\hlg{9} \\text{ triệu}$$""",
           """Đáp án câu một: mười sáu chia ba mươi xấp xỉ năm mươi ba phẩy ba phần trăm, lớn hơn năm mươi nên không qua. Khoản tối đa là mười lăm triệu trừ sáu triệu, còn chín triệu."""),
        st("""$$91 \\leq 95 \\leq 180 \\;\\Rightarrow\\; \\hl{\\text{nhóm 3}};\\quad 20 + 25 + 10 = \\hl{55} < 70 \\;\\Rightarrow\\; \\text{không đạt}$$""",
           """Đáp án câu hai: chín mươi lăm ngày thuộc nhóm ba, còn khách kia được hai mươi cộng hai mươi lăm cộng mười, bằng năm mươi lăm điểm, không đạt."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["chuyển người xét, kèm xác thực thêm", "không từ chối oan gia đình hay cửa hàng dùng chung một máy; vẫn chặn được kẻ gian vì thiếu yếu tố thứ hai", "chậm hơn, tốn công người xét"],
                  ["từ chối tự động cả ba", "nhanh, không tốn người", "từ chối oan khách thật; kẻ gian chỉ cần đổi máy là qua"]]),
           """Đáp án câu ba: dấu vân tay chỉ là tín hiệu rủi ro, nên chuyển người xét kèm xác thực thêm. Cách này không từ chối oan người dùng chung máy, đổi lại chậm hơn.""",
           focus=["1.2", "1.3", "1.3"]),
    ], checks=["alg.bnx_dti(30, 6, 10) * 3 == 160 and not alg.bnx_dti_pass(30, 6, 10, 50)",
               "round(float(alg.bnx_dti(30, 6, 10)), 1) == 53.3",
               "alg.bnx_max_new_payment(30_000_000, 6_000_000, 50) == 9_000_000",
               "alg.bnx_debt_group(95) == 3",
               "alg.bnx_scorecard(12_000_000, 1, 12) == (20, 25, 10, 55) and alg.bnx_underwrite(12_000_000, 0, 1_000_000, 1, 12) == 'TU_CHOI'"])

    lab_pr = practice_scene(sc, "Tự làm: thẩm định một hồ sơ và băm hợp đồng", practice_steps2(
        st, "BNX", "L21",
        """<p><b>Đề</b>: viết <code>mau.py</code> cho hồ sơ: thu nhập 14 000 000, đang trả 3 000 000, khoản mới 3 000 000, nhóm 1, làm việc 30 tháng.</p>
<ol><li>in tỉ lệ nghĩa vụ (một chữ số thập phân) và điểm theo thẻ điểm của bài</li><li>in quyết định (nhân chéo, ngưỡng 50% và 70 điểm)</li><li>băm hợp đồng <code>Hop dong vay 14000000 dong, ky han 24 thang</code> (kèm xuống dòng cuối) bằng SHA-256, in 12 ký tự đầu, rồi đổi <code>24</code> thành <code>25</code> và đếm vị trí khác nhau</li></ol>
<p class="note">Quy tắc điểm và khuôn năm dòng in nằm ở <code>de.md</code>; số liệu khác ví dụ trong bài.</p>""",
        """Bây giờ tới phần bạn tự làm. Với hồ sơ thu nhập mười bốn triệu, đang trả ba triệu, khoản mới ba triệu, hãy viết chương trình in tỉ lệ, điểm và quyết định. Rồi băm một hợp đồng, đổi một ký tự và đếm vị trí khác nhau của hai mã băm.""",
        LAB.out, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> điểm = 20 (thu nhập dưới 15 triệu) + 25 + 20; quyết định là <code>TU_CHOI</code> nếu <code>(dang + moi) * 100 &gt; 50 * thu</code> hoặc điểm dưới 70. Băm: <code>hashlib.sha256(chuoi.encode()).hexdigest()</code>. Một chữ số thập phân: <code>f"{x:.1f}"</code>.
Lời giải ở <code>labs/BNX/L21/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, điểm là hai mươi cộng hai mươi lăm cộng hai mươi, và từ chối nếu tỉ lệ vượt năm mươi hoặc điểm dưới bảy mươi. Lời giải chỉ mở sau khi đã thử.""", pause=120), "BNX", "L21")

    rec = sc("recap", "recap", "Chuỗi logic, góc phỏng vấn & tư duy cần mang theo", [
        st(chain("hồ sơ: máy trạng thái, không đường tắt", "thẩm định: luật loại → tỉ lệ → thẻ điểm", "ký: chữ ký trên mã băm của nội dung", "kho hồ sơ: lưu đúng tệp đã ký", "gian lận: hai yếu tố + tín hiệu thiết bị", "gửi lõi: trường đa trị có vị trí"),
           """Tổng kết: hồ sơ vay là máy trạng thái không có đường tắt, và thẩm định chạy luật loại, rồi tỉ lệ, rồi thẻ điểm. Chữ ký nằm trên mã băm của nội dung nên kho phải lưu đúng tệp đã ký. Chống gian lận dùng hai yếu tố.""",
           focus=[0, "1.1", "1.3", "1.5", "1.6"]),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời một dòng"],
                 [["LOS khác LMS ở đâu?", "LOS lo hồ sơ từ lúc nộp tới giải ngân; LMS lo khoản vay sau giải ngân: lịch trả, thu nợ, quá hạn, tất toán"],
                  ["Bộ máy quyết định thẩm định chạy theo thứ tự nào?", "luật loại trước (ví dụ nhóm nợ), rồi tỉ lệ nghĩa vụ trên thu nhập, rồi thẻ điểm; ngưỡng là cấu hình theo chính sách"],
                  ["Ký số không giấy rồi đồng bộ kho hồ sơ: lưu gì, kiểm gì?", "lưu đúng tệp đã ký, chữ ký, mã băm; băm lại tệp trong kho phải ra đúng mã đã ký"]])
           + "<span class='note'>Trả lời bằng cơ chế; không nêu ngưỡng hay số liệu của tổ chức thật.</span>",
           """Người phỏng vấn hay hỏi ba câu. LOS lo từ lúc nộp tới giải ngân, còn LMS lo phần sau. Thẩm định chạy luật loại, tỉ lệ rồi thẻ điểm, và ký số thì lưu đúng tệp đã ký.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st("""<div class='box key'><b>Tư duy:</b> với mỗi quyết định tự động, hỏi ba điều: luật nào chạy trước, con số nào là <b>chính sách</b> (đổi được), và bằng chứng nào được <b>lưu lại</b> để sau này kiểm. Rồi hỏi thêm: luật này còn đúng khi hồ sơ tăng gấp trăm lần không?</div>
<p class='small'>Bài sau: một hệ quản trị nội dung trang web, với kho nội dung dạng cây gồm nút và thuộc tính, và cách phân giải đường dẫn thành trang.</p>""",
           """Điều cần mang theo: với mỗi quyết định tự động, hỏi luật nào chạy trước, con số nào là chính sách, và bằng chứng nào được lưu. Rồi hỏi luật còn đúng khi hồ sơ tăng gấp trăm lần không. Bài sau là một hệ quản trị nội dung trang web.""",
           clear=True, forward_ref=True),
    ], checks=["alg.bnx_underwrite(20_000_000, 4_000_000, 5_000_000, 2, 36) == 'XET_TAY'",
               "alg.bnx_loan_path_ok(['DUYET', 'DA_KY', 'GIAI_NGAN'])[0]"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L21", "he_thong_cho_vay_so", "Bài 21 — Hệ thống cho vay số: khởi tạo, chấm điểm, thẩm định, ký số và chống gian lận",
                  "curriculum/bnx.yaml L21; audit/bnx/verify_bnx.py L21; audit/bnx/sources_l21.md [TT31] Thông tư 31/2024/TT-NHNN Điều 10 "
                  "(nhóm nợ theo số ngày quá hạn; Công báo số 825+826 ngày 21-7-2024, người điều phối đối chiếu 2026-11-11; audit/legal/registry.yaml: hiệu lực); "
                  "ký số: chỉ dạy cơ chế “chữ ký trên mã băm của nội dung” (chạy thật bằng openssl 3.5.5, hashlib), không trích điều khoản Luật Giao dịch điện tử 2023; "
                  "định dạng trường TRƯỜNG:MV:SV=GIÁ TRỊ theo bài ACB L01 trong kho, bản tin là mẫu minh hoạ; mọi ngưỡng, trọng số, số tiền là số minh hoạ; "
                  "quy mô và lab: Python chạy thật (audit/bnx/progcache/L21.json)",
                  ["Mô tả các trạng thái của một hồ sơ vay từ lúc nộp tới lúc giải ngân và phân biệt hệ khởi tạo với hệ quản lý khoản vay",
                   "Tính tỉ lệ nghĩa vụ trả nợ trên thu nhập và áp một thẻ điểm đơn giản",
                   "Giải thích ký số một hợp đồng bằng mã băm và vì sao sửa một ký tự là lộ",
                   "Nêu hai lớp chống gian lận hồ sơ: xác thực hai yếu tố và dấu vân tay thiết bị",
                   "Đọc một trường đa trị trong bản tin gửi lõi ngân hàng",
                   "So sánh số hồ sơ bị gắn cờ của luật dấu vân tay thiết bị ở 5, 500 và 50 000 hồ sơ",
                   "Tính tỉ lệ nghĩa vụ, điểm thẻ và mã băm của một hồ sơ mới bằng mã Python"],
                  scenes,
                  covers=[(1, "intuition"), (2, "example"), (3, "formula"), (4, "formula"), (5, "formula"), (6, "quymo"), (7, "practice")])
