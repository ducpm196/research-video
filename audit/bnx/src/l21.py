from lib import *

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


def build():
    hook = sc("hook", "hook", "21 giờ, một hồ sơ vay nộp qua ứng dụng: máy quyết định thế nào?", [
        st(f"""<p>21 giờ, một khách nộp hồ sơ vay trên ứng dụng. Thu nhập <b>20 triệu</b> đồng mỗi tháng, đang trả nợ cũ <b>4 triệu</b> mỗi tháng, khoản vay mới sẽ phải trả <b>5 triệu</b> mỗi tháng.</p>
<div class="box key">Không có nhân viên nào thức. Hệ thống dựa vào đâu để <b>duyệt hay từ chối</b>, khách <b>ký hợp đồng</b> thế nào khi không có giấy, và làm sao biết hồ sơ này không phải của kẻ gian?</div>
{NOTE_ILL}""",
           """Chào bạn, hai mươi mốt giờ, một khách nộp hồ sơ vay trên ứng dụng. Thu nhập hai mươi triệu đồng mỗi tháng, đang trả nợ cũ bốn triệu, khoản vay mới sẽ phải trả năm triệu mỗi tháng.
           Lúc đó không có nhân viên nào thức, vậy hệ thống dựa vào đâu để duyệt hay từ chối? Khách ký hợp đồng thế nào khi không có giấy, và làm sao biết hồ sơ không phải của kẻ gian?
           Mọi ngưỡng, trọng số và số tiền trong bài là số minh hoạ, không phải chính sách của tổ chức nào.""",
           focus=[1, 1, 2, 2, 3]),
        st(table(["câu hỏi", "phần trả lời trong bài"],
                 [["hồ sơ đi qua những trạng thái nào", "máy trạng thái: nộp, chấm điểm, thẩm định, duyệt, ký, giải ngân"],
                  ["duyệt dựa vào đâu", "tỉ lệ nghĩa vụ trả nợ trên thu nhập và thẻ điểm"],
                  ["ký không giấy thế nào", "băm hợp đồng rồi ký lên mã băm; lưu tệp đã ký vào kho hồ sơ"],
                  ["chặn kẻ gian bằng gì", "xác thực hai yếu tố và dấu vân tay thiết bị"],
                  ["gửi dữ liệu sang lõi ngân hàng ra sao", "bản tin có trường đa trị"]]),
           """Bài này trả lời năm câu hỏi. Hồ sơ đi qua những trạng thái nào. Hệ thống duyệt dựa vào đâu.
           Ký không giấy thế nào. Chặn kẻ gian bằng gì. Và dữ liệu được gửi sang lõi ngân hàng ra sao.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"]),
    ], checks=["alg.bnx_dti(20_000_000, 4_000_000, 5_000_000) == 45",
               "alg.bnx_loan_path_ok(['NOP', 'CHAM_DIEM', 'THAM_DINH', 'DUYET', 'DA_KY', 'GIAI_NGAN']) == (True, -1)"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Phần trăm", "tỉ số nhân với 100", "9 trên 20 là 45%"],
                  ["② Máy trạng thái", "một vật chỉ ở một trạng thái tại một lúc, và chỉ được đi theo các bước cho phép", "đèn giao thông: xanh → vàng → đỏ, không có xanh → đỏ"],
                  ["③ Hàm băm", "biến một chuỗi dài bất kỳ thành một mã có độ dài cố định; đổi một ký tự thì mã đổi gần như toàn bộ", "SHA-256 luôn cho 64 ký tự thập lục phân"],
                  ["④ Cặp khoá", "khoá riêng giữ kín để ký; khoá công khai phát cho mọi người để kiểm", "ký bằng khoá riêng, ai có khoá công khai cũng kiểm được"]]),
           """Trước hết ta cần hiểu bốn điều. Phần trăm là tỉ số nhân với một trăm, ví dụ chín trên hai mươi là bốn mươi lăm phần trăm.
           Máy trạng thái là một vật chỉ ở một trạng thái tại một lúc, và chỉ được đi theo các bước cho phép, giống đèn giao thông.
           Hàm băm biến một chuỗi dài bất kỳ thành một mã có độ dài cố định, và đổi một ký tự thì mã đổi gần như toàn bộ.
           Cặp khoá gồm khoá riêng giữ kín để ký, và khoá công khai phát cho mọi người để kiểm.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"]),
        st("""$$\\frac{9}{20} = 0{,}45 = 45\\%$$""",
           """Một ví dụ số cho phần trăm. Chín chia hai mươi bằng không phẩy bốn mươi lăm, tức là bốn mươi lăm phần trăm. Ta sẽ gặp lại đúng con số này khi thẩm định hồ sơ."""),
    ], checks=["alg.bnx_dti(20, 4, 5) == 45 and 9 * 100 == 45 * 20",
               "len(alg.bnx_sha256_hex('a')) == 64 and len(alg.bnx_sha256_hex('a' * 1000)) == 64",
               "alg.bnx_loan_path_ok(['NOP', 'GIAI_NGAN']) == (False, 0)"])

    sym = sc("sym", "symbol", "Giải mã từ ngữ và nhóm nợ", [
        st(table(["từ", "nghĩa"],
                 [["LOS (Loan Origination System)", "hệ khởi tạo khoản vay: nhận hồ sơ, chấm điểm, thẩm định, duyệt, ký, tới lúc giải ngân"],
                  ["LMS (Loan Management System)", "hệ quản lý khoản vay: sau giải ngân, giữ lịch trả nợ, thu nợ, theo dõi quá hạn, tất toán"],
                  ["DTI (debt-to-income)", "tỉ lệ nghĩa vụ trả nợ hằng tháng trên thu nhập hằng tháng"],
                  ["thẻ điểm (scorecard)", "bảng đổi từng đặc trưng của khách thành điểm rồi cộng lại"],
                  ["thẩm định (underwriting), bộ máy quyết định", "áp các luật theo thứ tự để ra: duyệt, từ chối, hoặc chuyển người xét"],
                  ["Cloud CA, ECM", "ký số từ xa: khoá riêng nằm ở nơi cấp chứng thư (CA); chứng thư số gắn khoá công khai với một chủ thể và do CA ký (RFC 5280); ECM là kho lưu hồ sơ và văn bản"],
                  ["2FA, device fingerprint", "xác thực hai yếu tố; dấu vân tay thiết bị: mã rút ra từ các thuộc tính của máy"]]),
           """Bảng này giải mã các từ của bài. LOS là hệ khởi tạo khoản vay, lo từ lúc nhận hồ sơ tới lúc giải ngân.
           LMS là hệ quản lý khoản vay, lo phần sau giải ngân như lịch trả nợ, thu nợ và theo dõi quá hạn.
           DTI là tỉ lệ nghĩa vụ trả nợ hằng tháng trên thu nhập hằng tháng.
           Thẻ điểm là bảng đổi từng đặc trưng của khách thành điểm rồi cộng lại.
           Thẩm định là áp các luật theo thứ tự để ra quyết định duyệt, từ chối, hoặc chuyển cho người xét.
           Ký số từ xa nghĩa là khoá riêng nằm ở nơi cấp chứng thư, chứng thư gắn khoá công khai với một người, còn ECM là kho lưu hồ sơ và văn bản.
           Cuối cùng là xác thực hai yếu tố, và dấu vân tay thiết bị, tức một mã rút ra từ các thuộc tính của máy.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"]),
        st(table(["nhóm nợ", "số ngày quá hạn"],
                 [["nhóm 1", "dưới 10 ngày (kể cả đang trong hạn)"], ["nhóm 2", "từ 10 đến 90 ngày"], ["nhóm 3", "từ 91 đến 180 ngày"],
                  ["nhóm 4", "từ 181 đến 360 ngày"], ["nhóm 5", "trên 360 ngày"]])
           + "<p class='small'>Thông tư 31/2024/TT-NHNN, Điều 10, phần tính theo số ngày quá hạn; văn bản còn các điều kiện khác, đọc nguyên văn thông tư trước khi áp dụng.</p>",
           """Lịch sử trả nợ của khách được tóm thành nhóm nợ. Theo Thông tư ba mươi mốt năm hai nghìn không trăm hai mươi tư, nhóm một là quá hạn dưới mười ngày, nhóm hai từ mười đến chín mươi ngày.
           Nhóm ba từ chín mươi mốt đến một trăm tám mươi ngày, nhóm bốn từ một trăm tám mươi mốt đến ba trăm sáu mươi ngày, nhóm năm trên ba trăm sáu mươi ngày.
           Đây là phần tính theo số ngày quá hạn, văn bản còn các điều kiện khác nên phải đọc nguyên văn thông tư trước khi áp dụng.""",
           focus=[1, "1.2", "1.4", 2], clear=True),
        st(code(GROUP_PY, "Bảng nhóm nợ viết thành hàm: dò từng mốc trần") + out(GROUP_OUT),
           """Ta viết bảng nhóm nợ thành một hàm Python, dò lần lượt từng mốc trần là chín, chín mươi, một trăm tám mươi và ba trăm sáu mươi ngày.
           Kết quả chạy thật cho thấy ngày thứ chín còn ở nhóm một, ngày thứ mười sang nhóm hai, ngày chín mươi mốt sang nhóm ba.""",
           focus=["2.2", "4.1"], clear=True),
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
           """Hình này là đường đi của một hồ sơ vay. Bên trái là LOS, hồ sơ đi qua sáu trạng thái: nộp, chấm điểm, thẩm định, duyệt, đã ký và giải ngân.
           Từ chấm điểm hoặc thẩm định, hồ sơ có thể rẽ xuống từ chối, và từ thẩm định còn rẽ sang xét tay, nơi người xét duyệt hoặc từ chối. Không có đường tắt từ duyệt thẳng tới giải ngân, vì chưa ký thì chưa có hợp đồng.
           Bên phải là LMS, nhận khoản vay sau khi giải ngân, giữ lịch trả nợ, thu nợ, theo dõi quá hạn để xếp nhóm nợ, rồi tất toán."""),
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
           """Hình thứ hai là cơ chế ký số. Lúc ký, hợp đồng được băm thành một mã băm, rồi khoá riêng ký lên mã băm đó để tạo chữ ký.
           Với ký số từ xa, khoá riêng nằm ở nơi cấp chứng thư, và người ký xác nhận từng lần ký, ví dụ bằng mã OTP.
           Lúc kiểm, người nhận băm lại tệp mình nhận được, rồi dùng khoá công khai để so với chữ ký. Khớp thì hợp lệ, lệch thì nội dung đã bị sửa.
           Vì vậy chữ ký gắn với nội dung đã băm, không gắn với tên tệp, và kho hồ sơ phải lưu đúng tệp đã ký cùng chữ ký và mã băm."""),
    ])

    form = sc("formula", "formula", "Suy ra từng bước: trạng thái, thẩm định, ký, chống gian lận, gửi lõi", [
        st(code(STATE_PY, "Bước 1. Máy trạng thái của hồ sơ: bảng các bước được phép"),
           """Bước một, ta viết máy trạng thái của hồ sơ bằng Python. Bảng này ghi từ mỗi trạng thái được đi tới những trạng thái nào.
           Hàm chuyển kiểm bước đi có nằm trong bảng không, vì nếu không kiểm thì một lỗi lập trình có thể giải ngân hồ sơ chưa ký.""",
           focus=[1, "2.1", "2.6"]),
        st(code(STATE_RUN) + out(STATE_OUT, "Làm thử — kết quả chạy thật"),
           """Làm thử, ta cho hồ sơ đi đúng năm bước, và máy in hồ sơ tới trạng thái giải ngân.
           Rồi ta thử nhảy từ duyệt thẳng sang giải ngân. Máy chặn lại, vì bước đó không có trong bảng.""",
           focus=["1.1", "1.5", "3.2"], clear=True),
        st("""<p><b>Bước 2.</b> Tỉ lệ nghĩa vụ trả nợ trên thu nhập (DTI). Vì khoản vay mới làm tăng số tiền phải trả mỗi tháng, ta cộng nó vào nợ đang trả rồi mới chia:</p>
$$\\text{DTI} = \\frac{\\text{đang trả} + \\text{khoản mới}}{\\text{thu nhập}} \\cdot 100\\%$$
<span class='note'>Làm thử: (4 + 5) / 20 = 45%. Ngưỡng minh hoạ 50%: 45% không vượt nên qua. Ngưỡng là chính sách của từng tổ chức, không phải hằng số.</span>""",
           """Bước hai là tỉ lệ nghĩa vụ trả nợ trên thu nhập. Vì khoản vay mới làm tăng số tiền phải trả mỗi tháng, nên ta cộng nó vào nợ đang trả rồi mới chia cho thu nhập.
           Công thức là nợ đang trả cộng khoản mới, chia thu nhập, nhân một trăm phần trăm.
           Làm thử, bốn cộng năm là chín, chín chia hai mươi là bốn mươi lăm phần trăm, không vượt ngưỡng minh hoạ năm mươi phần trăm nên qua. Ngưỡng này là chính sách của từng tổ chức, không phải hằng số.""",
           focus=[1, 1, 2, 3, 3], clear=True),
        st(table(["Bước 3: thẻ điểm (trọng số minh hoạ)", "điều kiện", "điểm"],
                 [["thu nhập", "từ 15 triệu trở lên / thấp hơn", "35 / 20"],
                  ["lịch sử trả nợ", "nhóm 1 / nhóm khác", "25 / 0"],
                  ["thời gian làm việc", "từ 24 tháng / ngắn hơn", "20 / 10"],
                  ["tổng của khách trong ví dụ", "20 triệu, nhóm 1, 36 tháng", "35 + 25 + 20 = 80"]])
           + "<span class='note'>Ngưỡng duyệt minh hoạ: 70 điểm. 80 không thấp hơn 70 nên qua.</span>",
           """Bước ba là thẻ điểm, với trọng số minh hoạ. Thu nhập từ mười lăm triệu trở lên được ba mươi lăm điểm, thấp hơn được hai mươi.
           Lịch sử trả nợ ở nhóm một được hai mươi lăm điểm, nhóm khác không điểm. Làm việc từ hai mươi bốn tháng được hai mươi điểm, ngắn hơn được mười.
           Khách trong ví dụ có ba mươi lăm cộng hai mươi lăm cộng hai mươi, bằng tám mươi điểm. Vì tám mươi không thấp hơn ngưỡng duyệt minh hoạ bảy mươi, nên qua.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", 2], clear=True),
        st(code(DECIDE_PY, "Bước 4. Bộ máy quyết định: luật loại trước, rồi tỉ lệ, rồi điểm"),
           """Bước bốn ghép lại thành bộ máy quyết định. Thứ tự luật quan trọng, vì luật loại phải chạy trước mọi phép tính điểm.
           Ở đây, nhóm nợ từ hai trở lên thì chuyển cho người xét. Tiếp theo, tỉ lệ vượt ngưỡng hoặc điểm dưới ngưỡng thì từ chối, còn lại là duyệt.
           Phép so tỉ lệ dùng nhân chéo thay cho chia rồi làm tròn, vì làm tròn có thể cho qua một hồ sơ vừa vượt ngưỡng.""",
           focus=[1, 1, "2.6", "2.8", "2.8"], clear=True),
        st(code(HASH_PY, "Bước 5. Băm hợp đồng, rồi đổi đúng một ký tự (5 thành 6)") + out(HASH_OUT),
           """Bước năm là băm hợp đồng. Chuỗi hợp đồng mẫu viết không dấu cho gọn, ghi khoản vay năm mươi triệu.
           Ta đổi đúng một ký tự, số năm thành số sáu, rồi băm cả hai bản.
           Kết quả chạy thật cho hai mã cùng dài sáu mươi tư ký tự, nhưng khác nhau ở sáu mươi trên sáu mươi tư vị trí. Vì vậy sửa một ký tự là lộ ngay.""",
           focus=[1, "2.2", "2.3", "4.3", "4.3"], clear=True),
        st(code(SIGN_SH, "Bước 6. Ký và kiểm bằng cặp khoá (openssl; chỉ minh hoạ phần toán, không có chứng thư)") + out(SIGN_OUT),
           """Bước sáu, ta ký thật bằng công cụ dòng lệnh. Ba lệnh đầu tạo tệp hợp đồng và một cặp khoá, rồi khoá riêng ký lên mã băm của tệp.
           Lần kiểm thứ nhất trên tệp gốc báo hợp lệ. Lần thứ hai trên tệp đã sửa một ký tự báo thất bại, vì mã băm mới không còn khớp chữ ký.
           Lần thứ ba kiểm một bản sao mang tên khác mà nội dung y nguyên, và vẫn hợp lệ. Đó là vì chữ ký gắn với nội dung đã băm, không gắn với tên tệp, và ví dụ này chỉ minh hoạ phần toán, không có chứng thư.""",
           focus=[1, "2.4", "4.1", "4.2", "4.3", "4.3"], clear=True),
        st(code(FRAUD_PY, "Bước 7. Dấu vân tay thiết bị: đếm số giấy tờ khác nhau trên một máy"),
           """Bước bảy là chống gian lận hồ sơ, gồm hai lớp. Lớp một là xác thực hai yếu tố: ngoài mật khẩu là thứ khách biết, còn cần mã OTP gửi tới thứ khách có.
           Lớp hai là dấu vân tay thiết bị, vì kẻ gian hay nộp nhiều hồ sơ từ cùng một máy. Chương trình băm các thuộc tính của máy thành một mã ngắn, rồi đếm số giấy tờ khác nhau nộp từ cùng một mã.""",
           focus=[1, 1, "2.2", "2.10"], clear=True),
        st(code(FRAUD_PY, "Bước 7 (tiếp). Bốn hồ sơ, hai máy", lines=(7, 12)) + out(FRAUD_OUT)
           + "<div class='box key'>Một mã có 3 giấy tờ khác nhau → gắn cờ, chuyển người xét (ngưỡng 3 là số minh hoạ). Hai máy cùng đời có thể trùng mã: dấu vân tay là <b>tín hiệu rủi ro, không phải danh tính</b>.</div>",
           """Đây là phần cuối của chương trình, với bốn hồ sơ nộp từ hai máy.
           Kết quả chạy thật cho thấy một máy nộp hồ sơ cho ba căn cước khác nhau, nên hệ thống gắn cờ để người xét, với ngưỡng ba là số minh hoạ.
           Nhưng hai máy cùng đời có thể trùng mã, nên dấu vân tay chỉ là tín hiệu rủi ro, không phải danh tính.""",
           focus=["2.1", "4.1", 5], clear=True),
        st(code(OFS_PY, "Bước 8. Trường đa trị trong bản tin gửi lõi (mẫu minh hoạ, tên trường giả định)", lines=(1, 3))
           + table(["phần", "nghĩa"],
                   [["DIEN.THOAI:1:1 và DIEN.THOAI:2:1", "trường điện thoại có hai giá trị: giá trị thứ 1 và giá trị thứ 2"],
                    ["DIA.CHI:1:1 và DIA.CHI:1:2", "giá trị thứ 1 của địa chỉ gồm hai phần con: phần 1 và phần 2"]]),
           """Bước tám, khi cần ghi vào lõi ngân hàng T24, ví dụ lúc giải ngân, hồ sơ được gửi bằng bản tin OFS. Một trường có thể mang nhiều giá trị, nên mỗi giá trị kèm hai số vị trí.
           Số thứ nhất là thứ tự giá trị, số thứ hai là thứ tự phần con bên trong giá trị đó. Đây là mẫu minh hoạ, tên trường là giả định.
           Trường điện thoại có hai giá trị, còn giá trị thứ nhất của địa chỉ gồm hai phần con.""",
           focus=[1, "2.2", "2.2", 1, "3.2"], clear=True),
        st(code(OFS_PY) + out(OFS_OUT, "Bước 8 (tiếp) — kết quả chạy thật: tách bản tin thành từng trường"),
           """Chương trình bỏ bốn phần đầu của bản tin, rồi tách từng phần còn lại theo dấu phẩy, dấu bằng và dấu hai chấm, và gom theo tên trường.
           Kết quả chạy thật cho hai số điện thoại ở hai vị trí, và phần con thứ hai của địa chỉ.""",
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
        st(f"""<p>Thu nhập <b>20 triệu</b>, đang trả <b>4 triệu</b> mỗi tháng, khoản mới trả <b>5 triệu</b> mỗi tháng; nhóm nợ 1; làm việc 36 tháng. {NOTE_ILL}</p>
$$① \\; \\text{{nghĩa vụ mỗi tháng}} = 4 + 5 = \\hl{{9}} \\text{{ triệu}}$$""",
           """Ta làm trọn một hồ sơ. Thu nhập hai mươi triệu, đang trả bốn triệu mỗi tháng, khoản mới trả năm triệu mỗi tháng, nhóm nợ một, làm việc ba mươi sáu tháng.
           Phép tính thứ nhất, nghĩa vụ trả nợ mỗi tháng bằng bốn cộng năm, bằng chín triệu."""),
        st("""<p>Dùng lại 9 triệu ở phép ①.</p>
$$② \\; \\text{DTI} = \\frac{9}{20} = \\hl{45\\%} \\leq 50\\% \\;\\Rightarrow\\; \\text{qua}$$""",
           """Phép tính thứ hai dùng lại chín triệu. Tỉ lệ nghĩa vụ trên thu nhập bằng chín chia hai mươi, bằng bốn mươi lăm phần trăm. Vì bốn mươi lăm không vượt ngưỡng minh hoạ năm mươi phần trăm, nên qua."""),
        st("""$$③ \\; \\text{điểm} = 35 + 25 + 20 = \\hl{80} \\geq 70 \\;\\Rightarrow\\; \\text{qua}$$""",
           """Phép tính thứ ba là thẻ điểm. Ba mươi lăm cộng hai mươi lăm cộng hai mươi, bằng tám mươi điểm. Vì tám mươi không thấp hơn ngưỡng duyệt minh hoạ bảy mươi, nên qua."""),
        st("""<p>Nhóm nợ 1, phép ② qua, phép ③ qua.</p>
$$④ \\; \\text{quyết định} = \\hlg{\\text{DUYET}};\\quad \\text{khoản trả mới tối đa} = 50\\% \\cdot 20 - 4 = \\hl{6} \\text{ triệu}$$""",
           """Phép tính thứ tư ghép ba kết quả. Nhóm nợ một nên không bị luật loại, tỉ lệ qua, điểm qua, vậy quyết định là duyệt.
           Ta cũng biết khách còn chỗ tới đâu. Năm mươi phần trăm của hai mươi triệu là mười triệu, trừ bốn triệu đang trả, còn tối đa sáu triệu cho khoản mới.""",
           clear=True),
        st("""<p>Hồ sơ đã duyệt thì sang bước ký: băm hợp đồng mẫu ghi 50 000 000 đồng.</p>
$$⑤ \\; \\text{mã băm ban đầu: } \\texttt{662097aa…};\\quad \\text{đổi 5 thành 6: } \\texttt{93938eab…} \\;\\Rightarrow\\; \\hl{\\text{chữ ký không còn khớp}}$$""",
           """Phép tính thứ năm, hồ sơ đã duyệt thì sang bước ký. Mã băm của hợp đồng gốc và của bản bị đổi một ký tự khác hẳn nhau, như hai dãy đang hiện.
           Chữ ký đã tạo trên mã băm gốc, nên với bản bị sửa thì chữ ký không còn khớp."""),
    ], checks=["4 + 5 == 9 and alg.bnx_dti(20, 4, 5) == 45",
               "alg.bnx_dti_pass(20_000_000, 4_000_000, 5_000_000, 50) is True",
               "alg.bnx_scorecard(20_000_000, 1, 36)[3] == 80 and 80 >= 70",
               "alg.bnx_underwrite(20_000_000, 4_000_000, 5_000_000, 1, 36) == 'DUYET'",
               "alg.bnx_max_new_payment(20_000_000, 4_000_000, 50) == 6_000_000",
               f"alg.bnx_sha256_hex({HD!r}).startswith('662097aa') and alg.bnx_sha256_hex({HD!r}.replace('5', '6', 1)).startswith('93938eab')"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: để máy quyết định, rồi thử hai hồ sơ lân cận", [
        st(code(DECIDE_RUN, "Gọi bộ máy quyết định ở bước 4 với ba hồ sơ") + out(DECIDE_OUT),
           """Kiểm bằng đường khác. Thay vì tin phép tính tay, ta gọi bộ máy quyết định ở bước bốn với ba hồ sơ.
           Hồ sơ thứ nhất là ví dụ vừa làm, máy in bốn mươi lăm phần trăm, tám mươi điểm, duyệt, khớp với tính tay.
           Hồ sơ thứ hai có khoản mới bảy triệu, tỉ lệ lên năm mươi lăm phần trăm nên bị từ chối. Hồ sơ thứ ba ở nhóm nợ hai nên chuyển cho người xét, dù tỉ lệ vẫn là bốn mươi lăm phần trăm.""",
           focus=[1, 1, "4.1", "4.2", "4.3"]),
        st(table(["cách kiểm", "phép tính", "kết luận"],
                 [["nhân chéo, không chia", "9 × 100 = 900 không lớn hơn 50 × 20 = 1000", "tỉ lệ qua"],
                  ["tính ngược từ khoản tối đa", "6 − 5 = 1 triệu còn dư", "khoản mới 5 triệu nằm trong giới hạn"],
                  ["điểm bị mất so với tối đa", "80 − 80 = 0", "khách đạt mức cao nhất của cả ba đặc trưng"],
                  ["bản sao hợp đồng mang tên khác", "kiểm chữ ký: hợp lệ", "chữ ký theo nội dung, không theo tên tệp"]]),
           """Bảng này kiểm thêm bằng bốn đường. Nhân chéo thì chín nhân một trăm là chín trăm, không lớn hơn năm mươi nhân hai mươi là một nghìn, nên tỉ lệ qua.
           Tính ngược thì khoản tối đa sáu triệu trừ khoản mới năm triệu còn dư một triệu. Về điểm, tám mươi là mức cao nhất của thẻ, khách không mất điểm nào.
           Còn bản sao hợp đồng mang tên khác vẫn kiểm chữ ký hợp lệ, vì chữ ký theo nội dung chứ không theo tên tệp.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], clear=True),
    ], checks=["9 * 100 <= 50 * 20 and alg.bnx_dti_pass(20, 4, 5, 50)",
               "alg.bnx_underwrite(20_000_000, 4_000_000, 7_000_000, 1, 36) == 'TU_CHOI' and alg.bnx_dti(20, 4, 7) == 55",
               "alg.bnx_underwrite(20_000_000, 4_000_000, 5_000_000, 2, 36) == 'XET_TAY' and alg.bnx_scorecard(20_000_000, 2, 36)[3] == 55",
               "alg.bnx_max_new_payment(20_000_000, 4_000_000, 50) - 5_000_000 == 1_000_000",
               "max(alg.bnx_scorecard(i, g, m)[3] for i in (10_000_000, 20_000_000) for g in (1, 2) for m in (12, 36)) == 80"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Coi ngưỡng 50% và 70 điểm là hằng số của nghề, và nghĩ chữ ký gắn với <b>tên tệp</b>.
<br><span class="note">Đúng: ngưỡng là chính sách của từng tổ chức, đặt thành cấu hình. Chữ ký gắn với nội dung đã băm: đổi tên tệp không sao, đổi một ký tự nội dung là lộ.</span></div>""",
           """Lỗi thứ nhất, của người mới, là coi ngưỡng năm mươi phần trăm và bảy mươi điểm là hằng số của nghề, và nghĩ chữ ký gắn với tên tệp.
           Thật ra ngưỡng là chính sách của từng tổ chức, nên đặt thành cấu hình. Còn chữ ký gắn với nội dung đã băm, đổi tên tệp không sao, đổi một ký tự nội dung là lộ."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Tính tỉ lệ bằng phép chia lấy phần nguyên rồi mới so ngưỡng. Thu nhập 20 000 000, đang trả 4 000 000, khoản mới 6 190 000:</div>
$$\\frac{10\\,190\\,000}{20\\,000\\,000} = 50{,}95\\% \\;\\text{bị cắt còn}\\; 50\\% \\;\\Rightarrow\\; \\text{qua sai}$$
<span class="note">Cách chữa: so bằng nhân chéo trên số nguyên, 1 019 000 000 lớn hơn 1 000 000 000 nên vượt; viết ca kiểm ngay tại biên.</span>""",
           """Lỗi thứ hai, của người đã đi làm, hay gặp lúc mới dựng hệ thống. Đó là tính tỉ lệ bằng phép chia lấy phần nguyên rồi mới so với ngưỡng.
           Với khoản mới sáu triệu một trăm chín mươi nghìn, tỉ lệ thật là năm mươi phẩy chín mươi lăm phần trăm, nhưng bị cắt còn năm mươi, nên hồ sơ qua sai.
           Cách chữa là so bằng nhân chéo trên số nguyên, và viết ca kiểm ngay tại biên của ngưỡng.""",
           focus=[1, 1, 2, 3], clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc vận hành lâu dài).</b> Kho hồ sơ chỉ lưu dữ liệu hợp đồng, khi cần thì <b>sinh lại tệp</b> từ mẫu. Một năm sau mẫu đổi một dấu cách: tệp sinh lại có mã băm khác, chữ ký cũ không còn kiểm được.
<br><span class="note">Cách chữa: lưu đúng tệp đã ký, chữ ký và mã băm; việc đồng bộ sang kho chỉ xong khi băm lại tệp trong kho ra đúng mã đã ký.</span></div>
<div class="box warn"><b>Cùng loại, lúc tải tăng.</b> Chặn cứng mọi hồ sơ trùng dấu vân tay thiết bị: nhiều khách dùng cùng đời máy bị từ chối oan. Dấu vân tay là tín hiệu rủi ro, không phải danh tính.</div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, lộ ra khi vận hành lâu dài. Kho hồ sơ chỉ lưu dữ liệu hợp đồng, khi cần thì sinh lại tệp từ mẫu.
           Một năm sau mẫu đổi một dấu cách, tệp sinh lại có mã băm khác, nên chữ ký cũ không còn kiểm được.
           Cách chữa là lưu đúng tệp đã ký cùng chữ ký và mã băm, và chỉ coi là đồng bộ xong khi băm lại tệp trong kho ra đúng mã đã ký.
           Một lỗi cùng loại lộ ra lúc tải tăng, là chặn cứng mọi hồ sơ trùng dấu vân tay thiết bị. Nhiều khách dùng cùng đời máy sẽ bị từ chối oan, vì dấu vân tay chỉ là tín hiệu rủi ro, không phải danh tính.""",
           focus=[1, 1, 1, 1, 2, 2], clear=True),
    ], checks=["float(alg.bnx_dti(20_000_000, 4_000_000, 6_190_000)) == 50.95",
               "(4_000_000 + 6_190_000) * 100 // 20_000_000 == 50 and not alg.bnx_dti_pass(20_000_000, 4_000_000, 6_190_000, 50)",
               "10_190_000 * 100 == 1_019_000_000 and 50 * 20_000_000 == 1_000_000_000",
               "alg.bnx_sha256_hex('Hop dong  vay') != alg.bnx_sha256_hex('Hop dong vay')",
               f"alg.bnx_device_fp({A1!r}) == alg.bnx_device_fp(dict({A1!r}))"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề (dùng ngưỡng và thẻ điểm minh hoạ của bài)"],
                 [["1", "Thu nhập 30 triệu, đang trả 6 triệu, khoản mới trả 10 triệu mỗi tháng. Tỉ lệ là bao nhiêu, có qua ngưỡng 50% không? Khoản trả mới tối đa là bao nhiêu?"],
                  ["2", "Khách quá hạn 95 ngày thuộc nhóm nợ mấy? Một khách khác thu nhập 12 triệu, nhóm 1, làm việc 12 tháng được bao nhiêu điểm, có đạt 70 không?"],
                  ["3", "Quyết định: trong một ngày, ba hồ sơ với ba căn cước khác nhau cùng một dấu vân tay thiết bị. Từ chối tự động cả ba, hay chuyển người xét kèm xác thực thêm?"]]),
           """Đến lượt bạn. Câu một, thu nhập ba mươi triệu, đang trả sáu triệu, khoản mới trả mười triệu mỗi tháng. Tỉ lệ là bao nhiêu, có qua ngưỡng năm mươi phần trăm không, và khoản trả mới tối đa là bao nhiêu?
           Câu hai, khách quá hạn chín mươi lăm ngày thuộc nhóm nợ mấy? Một khách khác thu nhập mười hai triệu, nhóm một, làm việc mười hai tháng được bao nhiêu điểm, có đạt bảy mươi không?
           Câu ba, trong một ngày có ba hồ sơ với ba căn cước khác nhau cùng một dấu vân tay thiết bị. Nên từ chối tự động cả ba, hay chuyển người xét kèm xác thực thêm? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""$$\\frac{6 + 10}{30} = \\frac{16}{30} \\approx 53{,}3\\% > 50\\% \\;\\Rightarrow\\; \\hl{\\text{không qua}};\\quad 50\\% \\cdot 30 - 6 = \\hlg{9} \\text{ triệu}$$""",
           """Đáp án câu một. Sáu cộng mười là mười sáu, mười sáu chia ba mươi xấp xỉ năm mươi ba phẩy ba phần trăm, lớn hơn năm mươi phần trăm nên không qua.
           Khoản trả mới tối đa là năm mươi phần trăm của ba mươi triệu, tức mười lăm triệu, trừ sáu triệu đang trả, còn chín triệu."""),
        st("""$$91 \\leq 95 \\leq 180 \\;\\Rightarrow\\; \\hl{\\text{nhóm 3}};\\quad 20 + 25 + 10 = \\hl{55} < 70 \\;\\Rightarrow\\; \\text{không đạt}$$""",
           """Đáp án câu hai. Chín mươi lăm ngày nằm trong khoảng từ chín mươi mốt đến một trăm tám mươi, nên là nhóm ba.
           Khách thứ hai được hai mươi cộng hai mươi lăm cộng mười, bằng năm mươi lăm điểm, thấp hơn bảy mươi nên không đạt."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["chuyển người xét, kèm xác thực thêm", "không từ chối oan gia đình hay cửa hàng dùng chung một máy; vẫn chặn được kẻ gian vì thiếu yếu tố thứ hai", "chậm hơn, tốn công người xét"],
                  ["từ chối tự động cả ba", "nhanh, không tốn người", "từ chối oan khách thật; kẻ gian chỉ cần đổi máy là qua"]]),
           """Đáp án câu ba. Dấu vân tay thiết bị là tín hiệu rủi ro, không phải danh tính, nên không đủ để kết luận.
           Chuyển người xét kèm xác thực thêm thì không từ chối oan một gia đình hay cửa hàng dùng chung máy, mà vẫn chặn được kẻ gian. Đổi lại chậm hơn và tốn công người xét.
           Từ chối tự động thì nhanh, nhưng từ chối oan khách thật, còn kẻ gian chỉ cần đổi máy. Vì vậy nên chuyển người xét."""),
    ], checks=["alg.bnx_dti(30, 6, 10) * 3 == 160 and not alg.bnx_dti_pass(30, 6, 10, 50)",
               "round(float(alg.bnx_dti(30, 6, 10)), 1) == 53.3",
               "alg.bnx_max_new_payment(30_000_000, 6_000_000, 50) == 9_000_000",
               "alg.bnx_debt_group(95) == 3",
               "alg.bnx_scorecard(12_000_000, 1, 12) == (20, 25, 10, 55) and alg.bnx_underwrite(12_000_000, 0, 1_000_000, 1, 12) == 'TU_CHOI'"])

    rec = sc("recap", "recap", "Chuỗi logic, góc phỏng vấn & tư duy cần mang theo", [
        st(chain("hồ sơ: máy trạng thái, không đường tắt", "thẩm định: luật loại → tỉ lệ → thẻ điểm", "ký: chữ ký trên mã băm của nội dung", "kho hồ sơ: lưu đúng tệp đã ký", "gian lận: hai yếu tố + tín hiệu thiết bị", "gửi lõi: trường đa trị có vị trí"),
           """Tổng kết chuỗi logic. Hồ sơ vay là một máy trạng thái không có đường tắt. Thẩm định chạy luật loại trước, rồi tỉ lệ nghĩa vụ trên thu nhập, rồi thẻ điểm.
           Chữ ký số nằm trên mã băm của nội dung, nên kho hồ sơ phải lưu đúng tệp đã ký.
           Chống gian lận dùng xác thực hai yếu tố cùng tín hiệu từ thiết bị. Còn dữ liệu gửi sang lõi đi trong các trường đa trị có vị trí.""",
           focus=[0, "1.1", "1.3", "1.5", "1.9", "1.11"]),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời một dòng"],
                 [["LOS khác LMS ở đâu?", "LOS lo hồ sơ từ lúc nộp tới giải ngân; LMS lo khoản vay sau giải ngân: lịch trả, thu nợ, quá hạn, tất toán"],
                  ["Bộ máy quyết định thẩm định chạy theo thứ tự nào?", "luật loại trước (ví dụ nhóm nợ), rồi tỉ lệ nghĩa vụ trên thu nhập, rồi thẻ điểm; ngưỡng là cấu hình theo chính sách"],
                  ["Ký số không giấy rồi đồng bộ kho hồ sơ: lưu gì, kiểm gì?", "lưu đúng tệp đã ký, chữ ký, mã băm; băm lại tệp trong kho phải ra đúng mã đã ký"]])
           + "<span class='note'>Trả lời bằng cơ chế; không nêu ngưỡng hay số liệu của tổ chức thật.</span>",
           """Đây là ba câu người phỏng vấn hay hỏi về các dòng này trên hồ sơ xin việc. Hỏi hai hệ khác nhau ở đâu, thì trả lời LOS lo từ lúc nộp tới giải ngân, LMS lo khoản vay sau giải ngân.
           Hỏi bộ máy quyết định chạy theo thứ tự nào, thì trả lời luật loại trước, rồi tỉ lệ nghĩa vụ trên thu nhập, rồi thẻ điểm, với ngưỡng là cấu hình.
           Hỏi ký không giấy rồi đồng bộ kho hồ sơ, thì trả lời lưu đúng tệp đã ký, chữ ký và mã băm, rồi băm lại để kiểm.
           Hãy trả lời bằng cơ chế, không nêu ngưỡng hay số liệu của tổ chức thật.""",
           focus=[0, "1.2", "1.3", "1.4", 2], clear=True),
        st("""<div class='box key'><b>Tư duy:</b> với mỗi quyết định tự động, hỏi ba điều: luật nào chạy trước, con số nào là <b>chính sách</b> (đổi được), và bằng chứng nào được <b>lưu lại</b> để sau này kiểm.</div>""",
           """Điều cần mang theo. Với mỗi quyết định tự động, hãy hỏi ba điều: luật nào chạy trước, con số nào là chính sách có thể đổi, và bằng chứng nào được lưu lại để sau này kiểm.""",
           clear=True),
        st("""<p class='small'>Bài sau: một hệ quản trị nội dung trang web, với kho nội dung dạng cây gồm nút và thuộc tính, và cách phân giải đường dẫn thành trang.</p>""",
           """Ở bài sau, ta học một hệ quản trị nội dung trang web, nơi mỗi trang nằm trong một kho nội dung dạng cây gồm nút và thuộc tính, và cách phân giải đường dẫn thành trang.""",
           forward_ref=True),
    ], checks=["alg.bnx_underwrite(20_000_000, 4_000_000, 5_000_000, 2, 36) == 'XET_TAY'",
               "alg.bnx_loan_path_ok(['DUYET', 'DA_KY', 'GIAI_NGAN'])[0]"])
    return lesson("L21", "he_thong_cho_vay_so", "Bài 21 — Hệ thống cho vay số: khởi tạo, chấm điểm, thẩm định, ký số và chống gian lận",
                  "curriculum/bnx.yaml L21; audit/bnx/verify_bnx.py L21; audit/bnx/sources_l21.md [TT31] Thông tư 31/2024/TT-NHNN Điều 10 "
                  "(nhóm nợ theo số ngày quá hạn; Công báo số 825+826 ngày 21-7-2024, người điều phối đối chiếu 2026-11-11); ký số: chỉ dạy cơ chế "
                  "“chữ ký trên mã băm của nội dung” (chạy thật bằng openssl 3.5.5, hashlib), không trích điều khoản Luật Giao dịch điện tử 2023; "
                  "định dạng trường TRƯỜNG:MV:SV=GIÁ TRỊ theo bài ACB L01 trong kho, bản tin là mẫu minh hoạ; mọi ngưỡng, trọng số, số tiền là số minh hoạ",
                  ["Mô tả các trạng thái của một hồ sơ vay từ lúc nộp tới lúc giải ngân và phân biệt hệ khởi tạo với hệ quản lý khoản vay",
                   "Tính tỉ lệ nghĩa vụ trả nợ trên thu nhập và áp một thẻ điểm đơn giản",
                   "Giải thích ký số một hợp đồng bằng mã băm và vì sao sửa một ký tự là lộ",
                   "Nêu hai lớp chống gian lận hồ sơ: xác thực hai yếu tố và dấu vân tay thiết bị",
                   "Đọc một trường đa trị trong bản tin gửi lõi ngân hàng"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
