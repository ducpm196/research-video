import re

import lib2
from lib2 import *
from labkit import write_lab, practice_scene  # noqa: E402

# ── Mã hiện trên màn hình (chạy NGUYÊN VĂN: audit/bnx/screen/l05.yaml, audit/bnx/ver/l05.py) ──
# Bash không dùng biến ($): dấu $ trong khối mã sẽ bị KaTeX của trình phát hiểu là công thức.
SH_CA = """
export MSYS_NO_PATHCONV=1      # chỉ cần trên Git Bash (Windows)
# hai nơi cấp (CA) tự ký, được phép ký chứng chỉ khác
openssl req -x509 -newkey ed25519 -noenc -subj /CN=ca1 -days 365 \\
  -addext keyUsage=critical,keyCertSign \\
  -keyout ca1.key -out ca1.crt
openssl req -x509 -newkey ed25519 -noenc -subj /CN=ca2 -days 365 \\
  -addext keyUsage=critical,keyCertSign \\
  -keyout ca2.key -out ca2.crt
"""

SH_SERVER = """
# máy chủ (tên localhost) và hai khách, cùng do ca1 ký
openssl req -x509 -newkey ed25519 -noenc -subj /CN=localhost \\
  -addext basicConstraints=CA:FALSE -CA ca1.crt -CAkey ca1.key \\
  -addext subjectAltName=DNS:localhost -days 90 \\
  -keyout may_chu.key -out may_chu.crt
openssl req -x509 -newkey ed25519 -noenc -subj /CN=thanh_toan \\
  -addext basicConstraints=CA:FALSE -CA ca1.crt -CAkey ca1.key \\
  -days 90 -keyout thanh_toan.key -out thanh_toan.crt
openssl req -x509 -newkey ed25519 -noenc -subj /CN=ke_toan \\
  -addext basicConstraints=CA:FALSE -CA ca1.crt -CAkey ca1.key \\
  -days 90 -keyout ke_toan.key -out ke_toan.crt
"""

SH_BAD = """
# khách lạ: do ca2 ký; khách cũ: hạn dùng đã qua
openssl req -x509 -newkey ed25519 -noenc -subj /CN=la_mat \\
  -addext basicConstraints=CA:FALSE -CA ca2.crt -CAkey ca2.key \\
  -days 90 -keyout la_mat.key -out la_mat.crt
openssl req -x509 -newkey ed25519 -noenc -subj /CN=het_han \\
  -addext basicConstraints=CA:FALSE -CA ca1.crt -CAkey ca1.key \\
  -not_before 20250101000000Z -not_after 20250401000000Z \\
  -keyout het_han.key -out het_han.crt
openssl verify -CAfile ca1.crt thanh_toan.crt la_mat.crt het_han.crt
"""

PY_CTX = r'''
import socket, ssl
from threading import Thread, Event
mc = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
mc.load_cert_chain("may_chu.crt", "may_chu.key")
mc.load_verify_locations("ca1.crt")     # chỉ tin nơi cấp ca1
mc.verify_mode = ssl.CERT_REQUIRED      # bắt buộc chứng chỉ khách
nghe = socket.create_server(("127.0.0.1", 0))  # cổng ngẫu nhiên
DUOC_PHEP = {"thanh_toan"}   # tên được gọi API này
'''

PY_SERVE = r'''
def phuc_vu(loi, xong):
    c, _ = nghe.accept()
    t = mc.wrap_socket(c, server_side=True,
                       do_handshake_on_connect=False)
    try:
        t.do_handshake()
        ten = dict(x[0] for x in t.getpeercert()["subject"])
        if ten["commonName"] in DUOC_PHEP:    # cửa ④: kiểm tên
            t.sendall(("chào " + ten["commonName"]).encode())
        else:
            loi.append("tên không được phép")
            t.sendall("từ chối".encode())
    except ssl.SSLError as e:
        loi.append(getattr(e, "verify_message", e.reason))
    xong.wait(); t.close()      # đợi khách đọc xong mới đóng
'''

PY_CLIENT = r'''
def thu(ten):
    loi, xong = [], Event()
    th = Thread(target=phuc_vu, args=(loi, xong)); th.start()
    kh = ssl.create_default_context(cafile="ca1.crt")
    if ten: kh.load_cert_chain(ten + ".crt", ten + ".key")
    try:
        with socket.create_connection(nghe.getsockname()) as s, \
             kh.wrap_socket(s, server_hostname="localhost") as t:
            kq = t.recv(64).decode()   # TLS 1.3: lỗi tới ở lần đọc
    except ssl.SSLError as e: kq = e.reason
    xong.set(); th.join()
    print(f"{ten}\n  khách: {kq}\n  máy chủ: {loi}")
'''

PY_RUN = r'''
for ten in [None, "la_mat", "het_han", "ke_toan", "thanh_toan"]:
    thu(ten)
'''

# Số đo quy mô (chạy thật; ver/l05.py tính lại bằng công thức đóng): số lần đổi chứng chỉ mỗi năm theo số dịch vụ và hạn
PY_SCALE = r'''
def xoay(dich_vu, han, nam=365):
    buoc = han * 2 // 3          # xoay khi đã dùng 2/3 hạn
    dem = 0
    for _ in range(dich_vu):
        ngay = buoc
        while ngay <= nam:
            dem += 1             # một lần đổi chứng chỉ
            ngay += buoc
    return dem
for n in (10, 1000, 100000):
    print(n, "dv: han365 =", xoay(n, 365), "| han30 =", xoay(n, 30))
'''
OUT_SCALE = """
10 dv: han365 = 10 | han30 = 180
1000 dv: han365 = 1000 | han30 = 18000
100000 dv: han365 = 100000 | han30 = 1800000
"""

# ── Lab (số liệu KHÁC ví dụ: ba chứng chỉ khác, hôm nay 15/6/2026) ──
LAB_PY = r'''
from datetime import date, timedelta

HOM_NAY = date(2026, 6, 15)
CHUNG_CHI = [("so_cai", "2026-04-20", 60),
             ("bao_cao", "2026-01-10", 365),
             ("doi_soat", "2026-05-01", 30)]

can_xu_ly = 0
for ten, cap, han in CHUNG_CHI:
    ngay_cap = date.fromisoformat(cap)
    xoay = ngay_cap + timedelta(days=han * 2 // 3)
    het = ngay_cap + timedelta(days=han)
    if HOM_NAY > het:
        tt = "da het han"
    elif HOM_NAY >= xoay:
        tt = f"can xoay, con {(het - HOM_NAY).days} ngay"
    else:
        tt = "chua den han xoay"
    if tt != "chua den han xoay":
        can_xu_ly += 1
    print(f"{ten}: xoay {xoay}, het han {het}: {tt}")
print("So chung chi can xu ly:", can_xu_ly)
'''
LAB_OUT = """so_cai: xoay 2026-05-30, het han 2026-06-19: can xoay, con 4 ngay
bao_cao: xoay 2026-09-10, het han 2027-01-10: chua den han xoay
doi_soat: xoay 2026-05-21, het han 2026-05-31: da het han
So chung chi can xu ly: 2"""
LAB_DE = """# Lab BNX L05 — Lịch xoay vòng chứng chỉ

Hôm nay là **15/6/2026**. Ba chứng chỉ dịch vụ (số minh hoạ) cho dưới dạng (tên, ngày cấp, hạn dùng tính bằng ngày):

```python
CHUNG_CHI = [("so_cai", "2026-04-20", 60),
             ("bao_cao", "2026-01-10", 365),
             ("doi_soat", "2026-05-01", 30)]
```
Quy tắc của bài: **ngày hết hạn** = ngày cấp + hạn; **ngày xoay** = ngày cấp + (hạn × 2 // 3) ngày (xoay khi đã dùng 2/3 thời hạn).
Chứng chỉ **đã hết hạn** nếu hôm nay đứng sau ngày hết hạn; **cần xoay** nếu chưa hết hạn nhưng hôm nay đã tới (hoặc qua) ngày xoay, kèm số ngày còn lại tới hết hạn; còn lại là **chưa đến hạn xoay**.

Viết `mau.py` (dùng `datetime.date` và `timedelta` của Python) in mỗi chứng chỉ một dòng, rồi dòng đếm số chứng chỉ phải xử lý (đã hết hạn hoặc cần xoay):
```
<tên>: xoay <ngày>, het han <ngày>: <da het han | can xoay, con N ngay | chua den han xoay>
So chung chi can xu ly: <số>
```
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L05 mau.py`.
"""

# Đầu ra thật (chạy 2026-11-11: Git Bash + OpenSSL 3.5.5; .venv Python 3.13 với OpenSSL 3.0.16; 30/30 lần chạy cùng kết quả)
OUT_VERIFY = """
thanh_toan.crt: OK
error 20 at 0 depth lookup: unable to get local issuer certificate
error la_mat.crt: verification failed
error 10 at 0 depth lookup: certificate has expired
error het_han.crt: verification failed
"""
OUT_TLS = """
None
  khách: TLSV13_ALERT_CERTIFICATE_REQUIRED
  máy chủ: ['PEER_DID_NOT_RETURN_A_CERTIFICATE']
la_mat
  khách: TLSV1_ALERT_UNKNOWN_CA
  máy chủ: ['unable to get local issuer certificate']
het_han
  khách: SSLV3_ALERT_CERTIFICATE_EXPIRED
  máy chủ: ['certificate has expired']
ke_toan
  khách: từ chối
  máy chủ: ['tên không được phép']
thanh_toan
  khách: chào thanh_toan
  máy chủ: []
"""

# Từ ngoại KHÔNG đạt dò phát âm (BRIEF §6: JWT 0/8, OAuth 3/8, TLS 4/8; OpenID chưa dò): lời đọc tiếng Việt, tên gốc chỉ hiện trên màn hình
SPOKEN = [(r"(?<![\w])TLS(?![\w])", "mã hoá đường truyền"), (r"(?<![\w])OAuth 2\.0(?![\w])", "chuẩn ủy quyền")]

N = "__import__('datetime').datetime.now()"


_KEEP_CASE = {"RFC", "API", "HMAC", "SHA256", "Python", "Oracle", "M", "Token", "JSON", "B", "A", "C"}


def _lower_first(t):
    w = t.split(" ", 1)[0].strip(",:")
    if w in _KEEP_CASE or (len(w) > 1 and w.isupper()):
        return t
    return t[:1].lower() + t[1:]


def _fmerge(a, b):
    if a in (0, None):
        return b
    if b in (0, None):
        return a
    la, lb = (a if isinstance(a, list) else [a]), (b if isinstance(b, list) else [b])
    return la + [x for x in lb if x not in la]


def _merge_short(st_, minw=8, maxc=170, maxw=38):
    """Câu ≤ 7 từ (TTS/ASR dễ méo; yêu cầu rà 2026-11-11) ghép vào câu sau (hoặc câu trước) bằng dấu phẩy; focus ghép theo."""
    ss = lv.sentences(st_["say"])
    foc = st_.get("focus")
    fl = list(foc) if isinstance(foc, list) and len(foc) == len(ss) else None
    j = 0
    while j < len(ss):
        if len(ss[j].split()) < minw and ss[j].endswith("."):
            nxt = ss[j][:-1] + ", " + _lower_first(ss[j + 1]) if j + 1 < len(ss) else None
            if nxt and len(nxt) <= maxc and len(nxt.split()) <= maxw:
                ss[j:j + 2] = [nxt]
                if fl:
                    fl[j:j + 2] = [_fmerge(fl[j], fl[j + 1])]
                continue
            if j > 0 and ss[j - 1].endswith("."):
                prv = ss[j - 1][:-1] + ", " + _lower_first(ss[j])
                if len(prv) <= maxc and len(prv.split()) <= maxw:
                    ss[j - 1:j + 1] = [prv]
                    if fl:
                        fl[j - 1:j + 1] = [_fmerge(fl[j - 1], fl[j])]
                    j -= 1
                    continue
        j += 1
    st_["say"] = " ".join(ss)
    if fl is not None:
        st_["focus"] = fl


def _spoken(scenes):
    for sc_ in scenes:
        for s_ in sc_["steps"]:
            for a_, b_ in SPOKEN:
                s_["say"] = re.sub(a_, b_, s_["say"])
            _merge_short(s_)
    return scenes


def build():
    hook = sc("hook", "hook", "Hai giờ sáng, mọi lệnh gọi sổ cái bị từ chối", [
        st("""<p>Dịch vụ thanh toán gọi API sổ cái trong mạng nội bộ. Hai câu hỏi người vận hành hay gặp (số minh hoạ):</p>
<div class="box key">① Một máy lạ cắm vào mạng nội bộ có gọi được API sổ cái không, nếu API chỉ tin “ở trong mạng là người nhà”?<br>
② Chứng chỉ của dịch vụ hạn 90 ngày, cấp 1/3/2026. Ngày 30/5/2026 không ai nhớ đổi: chuyện gì xảy ra?</div>""",
           """Chào bạn, dịch vụ thanh toán gọi giao diện lập trình của sổ cái trong mạng nội bộ. Người vận hành hay gặp hai câu hỏi.
           Một, máy lạ cắm vào mạng nội bộ có gọi được sổ cái không, nếu sổ cái chỉ tin người ở trong mạng?
           Hai, chứng chỉ hạn chín mươi ngày, cấp ngày một tháng ba, đến ngày ba mươi tháng năm không ai nhớ đổi thì chuyện gì xảy ra?""",
           focus=[1, 1, 2, 2]),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["máy chủ biết người gọi là ai bằng cách nào", "mTLS: máy chủ đòi chứng chỉ của khách và tự kiểm"],
                  ["kiểm những gì", "chuỗi tin cậy, hạn dùng, tên; chạy thật bằng openssl và Python"],
                  ["tránh sự cố hết hạn thế nào", "theo dõi ngày hết hạn, xoay vòng trước, không tắt kiểm"]]),
           """Hôm nay ta trả lời ba câu. Máy chủ biết người gọi là ai nhờ M T L S, hai bên cùng trình chứng chỉ.
           Máy chủ kiểm những gì, ta chạy thật. Và làm sao tránh sự cố hết hạn.""",
           focus=[0, "1.2", "1.3", "1.4"]),
    ], checks=["alg.bnx_add_days('2026-03-01', 90) == '2026-05-30'"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① khoá riêng, khoá công khai", "khoá riêng dùng để ký, giữ kín; khoá công khai dùng để kiểm chữ ký, ai cũng có", "<code>thanh_toan.key</code> giữ kín, <code>.crt</code> gửi đi"],
                  ["② chứng chỉ", "tên + khoá công khai + hạn dùng, có chữ ký của <b>nơi cấp</b> (CA)", "CN=thanh_toan, do ca1 ký, hạn 90 ngày"],
                  ["③ chuỗi tin cậy", "tin nơi cấp thì tin chứng chỉ nơi đó ký, nếu còn hạn và đúng tên; thường có nơi cấp <b>trung gian</b>: gốc → trung gian → lá, bên trình chứng chỉ gửi kèm chứng chỉ trung gian", "tin ca1 thì tin <code>may_chu.crt</code> (ở bài này không có trung gian)"],
                  ["④ TLS một chiều", "lớp bọc kết nối: dữ liệu được mã hoá, và khách kiểm chứng chỉ máy chủ (tên, hạn, nơi cấp) để biết chắc nói với đúng máy chủ; máy chủ <b>không biết</b> khách là ai", "trình duyệt mở trang ngân hàng"]]),
           """Trước hết ta cần hiểu bốn điều. Thứ nhất, khoá riêng dùng để ký và giữ kín, khoá công khai dùng để kiểm chữ ký.
           Thứ hai, chứng chỉ gồm tên, khoá công khai và hạn dùng, có chữ ký của nơi cấp. Thứ ba, chuỗi tin cậy nghĩa là tin nơi cấp thì tin chứng chỉ nơi đó ký, nếu còn hạn và đúng tên.
           Thứ tư, TLS là lớp bọc kết nối, mã hoá dữ liệu và cho khách biết chắc đúng máy chủ. Ở kiểu một chiều, máy chủ không biết khách là ai.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"]),
        st("""<p>Làm thử: chứng chỉ cấp ngày 1/3/2026, hạn 90 ngày.</p>
$$31 + 30 + 29 = 90 \\;\\Rightarrow\\; \\text{hết hạn ngày } \\hl{30/5/2026}$$""",
           """Làm thử, chứng chỉ cấp ngày một tháng ba, hạn chín mươi ngày. Tháng ba còn ba mươi mốt ngày, tháng tư ba mươi ngày, cộng hai mươi chín ngày của tháng năm là đủ chín mươi, nên hết hạn ngày ba mươi tháng năm.""", clear=True),
    ], checks=["alg.bnx_add_days('2026-03-01', 90) == '2026-05-30'", "alg.bnx_days_between('2026-03-01', '2026-05-30') == 31 + 30 + 29 == 90"])

    sym = sc("sym", "symbol", "Giải mã các từ trên chứng chỉ", [
        st(table(["từ trên màn hình", "nghĩa"],
                 [["CA (nơi cấp)", "bên ký chứng chỉ; ở đây tự dựng hai nơi cấp ca1, ca2"],
                  ["CN, subjectAltName", "tên trong chứng chỉ: <code>CN=thanh_toan</code>; máy chủ ghi tên miền (tên chữ của máy, như <code>localhost</code>, thay cho địa chỉ số) ở <code>DNS:localhost</code>"],
                  ["notBefore, notAfter", "hạn dùng: từ ngày nào tới ngày nào"],
                  ["keyUsage=keyCertSign", "chứng chỉ này được phép <b>ký chứng chỉ khác</b> (chỉ nơi cấp mới có); nơi cấp còn cần <code>basicConstraints=CA:TRUE</code>, lệnh <code>req -x509</code> tự thêm"],
                  ["basicConstraints=CA:FALSE", "chứng chỉ lá: không được làm nơi cấp"],
                  ["CERT_REQUIRED", "máy chủ <b>bắt buộc</b> khách trình chứng chỉ hợp lệ"]]),
           """Nơi cấp là bên ký chứng chỉ, ở đây ta tự dựng hai nơi. Tên trong chứng chỉ ghi ở trường tên chung, máy chủ ghi tên miền, tức tên chữ của máy.
           Hai trường thời điểm là hạn dùng. Cờ ký chứng chỉ cho phép ký chứng chỉ khác, chỉ nơi cấp mới có. Cờ không phải nơi cấp đánh dấu chứng chỉ lá. Chế độ bắt buộc nghĩa là máy chủ đòi khách trình chứng chỉ hợp lệ.""",
           focus=[["1.1", "1.2"], "1.3", "1.4", "1.5", "1.6", "1.7"]),
    ])

    one_two = svg(1500, 470,
                  panel(20, 15, 700, 440, "TLS một chiều", C_GRAY),
                  box(50, 90, 230, 90, "Khách", C_BLUE, 26, True), box(460, 90, 230, 90, "Máy chủ", C_GREEN, 26, True),
                  arrow(455, 230, 285, 230, "#475569"), txt(370, 215, "chứng chỉ máy chủ", 22),
                  txt(165, 300, "khách kiểm:", 22, bold=True), txt(165, 334, "tên, hạn, nơi cấp", 22),
                  txt(575, 300, "máy chủ:", 22, bold=True), txt(575, 334, "không biết khách", 22, fill="#dc2626"),
                  panel(780, 15, 700, 440, "mTLS (hai chiều)", C_PURPLE),
                  box(810, 90, 230, 90, "Khách", C_BLUE, 26, True), box(1220, 90, 230, 90, "Máy chủ", C_GREEN, 26, True),
                  arrow(1215, 220, 1045, 220, "#475569"), txt(1130, 205, "chứng chỉ máy chủ + xin chứng chỉ", 20),
                  arrow(1045, 285, 1215, 285, "#475569"), txt(1130, 270, "chứng chỉ khách + chữ ký", 20),
                  txt(925, 360, "khách kiểm máy chủ", 22), txt(1335, 360, "máy chủ kiểm khách", 22, fill="#16a34a", bold=True),
                  txt(1130, 420, "chữ ký bằng khoá riêng: chép tệp .crt thôi là không đủ", 20))
    gate = svg(1500, 470,
               box(20, 180, 210, 100, ["khách", "kết nối"], C_BLUE, 24, True),
               box(300, 40, 330, 90, "① có chứng chỉ?", C_GRAY, 24),
               box(300, 190, 330, 90, "② do ca1 ký?", C_PURPLE, 24),
               box(300, 340, 330, 90, "③ còn hạn?", C_AMBER, 24),
               box(730, 340, 330, 90, ["④ tên được phép?", "(ứng dụng tự kiểm)"], C_BLUE, 22),
               box(1150, 340, 320, 90, "phục vụ", C_GREEN, 26, True),
               txt(660, 92, "không: PEER_DID_NOT_RETURN_A_CERTIFICATE", 20, "start", "#dc2626"),
               txt(660, 242, "không: unable to get local issuer certificate", 20, "start", "#dc2626"),
               txt(465, 458, "không: certificate has expired", 20, "middle", "#dc2626"),
               arrow(230, 210, 295, 100), arrow(465, 135, 465, 185), arrow(465, 285, 465, 335),
               arrow(635, 385, 725, 385), arrow(1065, 385, 1145, 385, "#16a34a"))
    intu = sc("intuition", "intuition", "Hình dung: thêm một chiều kiểm", [
        st(one_two,
           """Bên trái là TLS một chiều: máy chủ gửi chứng chỉ, khách kiểm, còn máy chủ không biết khách là ai.
           Bên phải là M T L S: máy chủ xin chứng chỉ của khách, khách gửi lại kèm chữ ký bằng khoá riêng, nên kẻ chỉ chép tệp chứng chỉ không qua được."""),
        st(gate,
           """Máy chủ kiểm khách qua các cửa. Một, có trình chứng chỉ không. Hai, có do nơi cấp mình tin ký không. Ba, còn hạn không.
           Ba cửa này do thư viện mật mã làm, mỗi cửa hỏng có thông báo riêng bằng chữ đỏ. Cửa bốn, tên khách có được gọi không, là việc của ứng dụng."""),
    ])

    form = sc("formula", "formula", "Suy ra từng bước: máy chủ biết khách là ai", [
        st("""<p><b>Bước 1.</b> TLS một chiều chỉ chứng minh <b>máy chủ</b> là ai. Ai vào được mạng nội bộ cũng mở được kết nối tới sổ cái.</p>
<span class='note'>Làm thử: máy lạ gọi bằng kênh một chiều → máy chủ không có gì để từ chối.</span>""",
           """Bước một, vì TLS một chiều chỉ chứng minh máy chủ là ai, nên ai vào được mạng nội bộ cũng mở được kết nối tới sổ cái. Máy chủ không có căn cứ từ chối.""", clear=True),
        st("""<p><b>Bước 2.</b> Máy chủ <b>xin</b> chứng chỉ khách. Khách gửi chứng chỉ và một <b>chữ ký</b> bằng khoá riêng trên cuộc <b>bắt tay</b>, tức vài thông điệp đầu hai bên trao đổi để trình chứng chỉ và thống nhất khoá trước khi gửi dữ liệu (RFC 8446 mục 4.4.3).
<br><span class='note'>Làm thử: tệp .crt có thể lộ; tệp .key không rời máy, nên kẻ chép .crt vẫn không ký được.</span></p>""",
           """Bước hai, máy chủ xin chứng chỉ của khách. Bắt tay là vài thông điệp đầu để trình chứng chỉ và thống nhất khoá.
           Khách gửi chứng chỉ kèm chữ ký bằng khoá riêng, nên máy chủ biết khách giữ khoá. Tệp chứng chỉ có thể lộ, nhưng khoá riêng không rời máy, nên kẻ chép chứng chỉ vẫn không ký được."""),
        st("""<p><b>Bước 3.</b> Máy chủ kiểm <b>chuỗi tin cậy</b> (do ca1 ký) và <b>hạn dùng</b> (notBefore ≤ bây giờ ≤ notAfter). Ứng dụng kiểm thêm <b>tên</b>.</p>
$$\\text{het\\_han: notAfter } = 1/4/2025, \\text{ sớm hơn hôm nay} \\;\\Rightarrow\\; \\hl{\\text{hỏng}}$$""",
           """Bước ba, máy chủ kiểm chuỗi tin cậy, tức chứng chỉ có do nơi cấp một ký không, và kiểm hạn dùng. Ứng dụng kiểm thêm tên.
           Làm thử, chứng chỉ khách cũ hết hạn ngày một tháng tư năm hai nghìn hai mươi lăm, nên hỏng.""", clear=True),
        st("""<p><b>Bước 4.</b> Ở TLS 1.3, khách gửi chứng chỉ <b>sau</b> thông điệp kết thúc của máy chủ, nên phía khách thấy bắt tay đã xong rồi máy chủ mới kiểm.
Lỗi chứng chỉ khách vì vậy hiện ra ở <b>lần đọc đầu tiên</b> (quan sát khi chạy thật).</p>""",
           """Bước bốn, một chi tiết hay gây bối rối. Ở TLS một chấm ba, khách gửi chứng chỉ sau thông điệp kết thúc của máy chủ, nên khách tưởng bắt tay đã xong. Vì vậy lỗi hiện ra ở lần đọc đầu tiên."""),
        st("""<p><b>Bước 5.</b> Chứng chỉ hết hạn là sự cố <b>có lịch hẹn trước</b>: xoay vòng khi đã dùng 2/3 thời hạn (số minh hoạ).</p>
$$90 \\cdot \\frac{2}{3} = \\hl{60} \\text{ ngày}; \\quad 90 - 60 = \\hlg{30} \\text{ ngày dự phòng}$$""",
           """Bước năm, vì ngày hết hạn biết trước, sự cố hết hạn là sự cố có lịch hẹn. Ta xoay vòng khi đã dùng hai phần ba thời hạn, số minh hoạ.
           Chín mươi nhân hai phần ba là sáu mươi, còn ba mươi ngày dự phòng.""", clear=True),
    ], checks=["alg.bnx_l05_cases(" + N + ")[2] == 'expired'", "alg.bnx_rotate_day(90) == 60", "90 - alg.bnx_rotate_day(90) == 30"])

    ex = sc("example", "example", "Ví dụ chạy thật, từng ca", [
        st(table(["lệnh <code>openssl</code>", "nghĩa"],
                 [["<code>req -x509</code>", "tạo luôn một chứng chỉ (tự ký, hoặc do một nơi cấp khác ký nếu có <code>-CA</code>)"],
                  ["<code>-newkey ed25519 -noenc</code>", "tạo khoá mới kiểu <code>ed25519</code> (kiểu khoá hiện đại, ngắn); <code>-noenc</code>: không đặt mật khẩu cho tệp khoá"],
                  ["<code>-subj /CN=ca1 -days 365</code>", "đặt tên chủ thể (CN) là <code>ca1</code>; chứng chỉ sống 365 ngày"],
                  ["<code>-addext tên=giá trị</code>", "thêm một thuộc tính vào chứng chỉ; <code>keyUsage=critical,keyCertSign</code>: <code>keyCertSign</code> là được ký chứng chỉ khác, <code>critical</code> là phần mềm không hiểu thuộc tính này thì phải từ chối cả chứng chỉ"],
                  ["<code>-keyout … -out …</code>", "tên tệp khoá riêng; tên tệp chứng chỉ"],
                  ["dấu <code>\\</code> cuối dòng", "nối dòng này với dòng sau thành một lệnh duy nhất"]]),
           """Các lệnh sắp tới dùng nhiều tuỳ chọn. Lệnh tạo luôn một chứng chỉ, với tên chủ thể, số ngày sống và khoá kiểu hiện đại không mật khẩu. Thuộc tính thêm vào có thể đánh dấu bắt buộc phải hiểu. Dấu gạch ngược nối lệnh dài.""",
           clear=True),
        st(code(SH_CA, "Bước A: hai nơi cấp tự ký (cần OpenSSL từ 3.4: kiểm bằng openssl version, thấp hơn thì cập nhật; chạy trên Git Bash)"),
           """Bước A tạo hai nơi cấp tự ký, ca một và ca hai, mỗi nơi một cặp khoá và một chứng chỉ hạn ba trăm sáu mươi lăm ngày.
           Dòng đầu chỉ cần trên hệ điều hành ghi ở chú thích. Cờ ký chứng chỉ là bắt buộc, vì thiếu nó thì Python ba chấm mười ba từ chối nơi cấp ngay. Công cụ cần bản ba chấm bốn trở lên.""",
           focus=[0, ["2.3", "2.6"], "2.1", ["2.4", "2.7"]], clear=True),
        st(table(["lệnh <code>openssl</code> thêm", "nghĩa"],
                 [["<code>-CA ca1.crt -CAkey ca1.key</code>", "ký bằng chứng chỉ và khoá riêng của nơi cấp <code>ca1</code>, không tự ký"],
                  ["<code>basicConstraints=CA:FALSE</code>, <code>subjectAltName=DNS:localhost</code>", "chứng chỉ lá, không được ký chứng chỉ khác; tên máy mà chứng chỉ nhận là đúng"],
                  ["<code>-not_before … -not_after …</code>", "ngày bắt đầu và ngày hết hạn tự chọn, viết năm tháng ngày giờ phút giây rồi chữ Z: <code>20250401000000Z</code> là 1/4/2025"],
                  ["<code>openssl verify -CAfile ca1.crt a.crt b.crt</code>", "kiểm từng chứng chỉ có do nơi cấp trong <code>ca1.crt</code> ký và còn hạn không: in <code>OK</code> hoặc lỗi"]]),
           """Hai bước sau dùng thêm bốn cách viết. Chứng chỉ được ký bằng khoá riêng của nơi cấp, không tự ký. Chứng chỉ lá không được ký chứng chỉ khác.
           Hai tuỳ chọn ngày đặt ngày bắt đầu và hết hạn. Lệnh cuối kiểm chứng chỉ với nơi cấp.""", clear=True),
        st(code(SH_SERVER, "Bước B: chứng chỉ máy chủ và khách đúng, do ca1 ký"),
           """Bước B cho ca một ký ba chứng chỉ lá hạn chín mươi ngày: một cho máy chủ, một cho dịch vụ thanh toán là khách đúng, một cho kế toán, còn hạn nhưng không được gọi sổ.""",
           focus=["2.1", ["2.2", "2.3", "2.4", "2.5"], ["2.6", "2.7", "2.8"], ["2.9", "2.10", "2.11"]], clear=True),
        st(code(SH_BAD, "Bước C: hai khách sai, rồi tự kiểm bằng openssl verify"),
           """Bước C tạo hai khách sai. Khách lạ do ca hai ký. Khách cũ do ca một ký nhưng hạn dùng đã qua từ tháng tư năm hai nghìn hai mươi lăm.
           Dòng cuối kiểm ba chứng chỉ khách với ca một.""",
           focus=["2.1", ["2.2", "2.3", "2.4"], ["2.5", "2.6", "2.7", "2.8"], "2.9"], clear=True),
        st(table(["từ trong mã Python", "nghĩa"],
                 [["<code>socket</code>", "ổ cắm mạng: đầu mút của một kết nối giữa hai chương trình"],
                  ["<code>(\"127.0.0.1\", 0)</code>", "địa chỉ của chính máy này (tên chữ là <code>localhost</code>) và số <b>cổng</b>; cổng là số chỉ chương trình nào trên máy nhận kết nối, như số phòng; số 0 là để hệ điều hành chọn một cổng trống"],
                  ["<code>ssl</code>", "thư viện TLS có sẵn của Python"],
                  ["<code>ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)</code>", "tạo bộ cấu hình TLS cho phía <b>máy chủ</b> (sẽ kiểm khách)"],
                  ["<code>load_cert_chain(crt, key)</code>, <code>load_verify_locations(ca)</code>", "nạp chứng chỉ và khoá riêng của mình; nạp nơi cấp mình tin"]]),
           """Ổ cắm mạng là đầu mút của một kết nối giữa hai chương trình. Địa chỉ một hai bảy chấm không chấm không chấm một là chính máy này, cổng là số chỉ chương trình nhận kết nối.
           Hai lệnh sau tạo cấu hình máy chủ, nạp chứng chỉ, khoá của mình và nơi cấp mình tin.""", clear=True, introduces=["bnx_o_cam_mang"]),
        st(code(PY_CTX, "Máy chủ Python: bắt buộc chứng chỉ khách"),
           """Giờ dựng máy chủ bằng Python. Máy chủ nạp chứng chỉ và khoá của mình, chỉ tin ca một, và bắt buộc chứng chỉ khách. Nó nghe ở một cổng ngẫu nhiên. Dòng cuối là danh sách tên được gọi sổ cái, hiện chỉ có dịch vụ thanh toán.""", focus=["2.1", ["2.3", "2.4", "2.5", "2.6"], "2.7", "2.8"], clear=True),
        st(table(["từ trong mã Python", "nghĩa"],
                 [["<code>Thread(target=…).start()</code>", "<b>luồng</b>: một việc chạy song song với việc chính; ở đây một luồng làm máy chủ, luồng chính làm khách; <code>th.join()</code> chờ luồng <code>th</code> chạy xong"],
                  ["<code>Event</code>: <code>xong.set()</code>, <code>xong.wait()</code>", "cờ hiệu giữa hai luồng: một bên chờ, bên kia bật cờ khi xong"],
                  ["<code>try: … except ssl.SSLError as e:</code>", "thử làm; nếu bắt tay hỏng thì nhảy xuống phần xử lý lỗi, <code>e</code> là lỗi nhận được"],
                  ["<code>with … as s:</code>", "dùng một hay nhiều tài nguyên (ngăn bằng dấu phẩy; dấu <code>\\</code> cuối dòng nối dòng) rồi tự đóng khi ra khỏi khối"]]),
           """Phần mã máy chủ dùng thêm bốn khái niệm. Luồng là một việc chạy song song với việc chính, lệnh nối chờ nó xong, và cờ hiệu giúp hai luồng đợi nhau. Thử làm và bắt lỗi chạy phần xử lý khi bắt tay hỏng, còn khối dùng tài nguyên tự đóng khi xong.""", clear=True),
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>mc.wrap_socket(c, server_side=True, do_handshake_on_connect=False)</code>", "bọc ổ cắm <code>c</code> thành kết nối TLS phía máy chủ; <code>False</code>: chưa bắt tay ngay, để bắt tay ở dòng sau"],
                  ["<code>dict(x[0] for x in t.getpeercert()[\"subject\"])</code>", "lấy chứng chỉ khách, gom tên chủ thể thành từ điển; <code>ten[\"commonName\"]</code> là tên chung (CN)"],
                  ["<code>getattr(e, \"verify_message\", e.reason)</code>", "lấy thuộc tính <code>verify_message</code> của lỗi <code>e</code>; nếu không có thì lấy <code>e.reason</code>"]]),
           """Mã sắp tới còn ba cách viết nữa. Lệnh bọc ổ cắm thành kết nối mã hoá và hoãn bắt tay sang dòng sau. Dòng gom tên trong chứng chỉ khách vào một từ điển, lệnh cuối lấy lý do lỗi, thiếu thì lấy lý do chung.""", clear=True),
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>c, _ = nghe.accept()</code>", "chờ một khách nối vào; trả về hai giá trị, gán cho <code>c</code> (ổ cắm của khách) và <code>_</code> (địa chỉ khách, bỏ không dùng)"],
                  ["<code>t.sendall(x.encode())</code>", "gửi hết chữ <code>x</code> cho khách; <code>.encode()</code> đổi chữ thành byte, vì mạng chỉ chở byte"],
                  ["<code>loi.append(x)</code>", "thêm <code>x</code> vào cuối danh sách <code>loi</code>"],
                  ["<code>a; b</code>", "hai lệnh trên một dòng, chạy lần lượt"]]),
           """Mã máy chủ còn bốn cách viết. Lệnh chờ khách trả về hai giá trị gán cho hai tên, tên gạch dưới là giá trị bỏ đi. Lệnh gửi chữ cho khách, đổi thành byte vì mạng chỉ chở byte.
           Lệnh thêm vào danh sách thêm phần tử cuối, dấu chấm phẩy nối hai lệnh.""", clear=True),
        st(code(PY_SERVE, "Mỗi kết nối: bắt tay, kiểm tên ở cửa ④, chào hoặc từ chối, hoặc ghi lý do"),
           """Mỗi kết nối, máy chủ bắt tay, rồi đọc tên chung trong chứng chỉ khách, đó là cửa bốn.
           Tên nằm trong danh sách được phép thì chào theo tên đó, còn không thì ghi lý do và từ chối. Nếu bắt tay hỏng, nó ghi lý do của thư viện.""",
           focus=[["2.2", "2.3", "2.4", "2.6"], "2.7", ["2.8", "2.9", "2.10", "2.11", "2.12"], ["2.13", "2.14"], "2.15"], clear=True),
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>if ten:</code>", "chạy phần sau khi <code>ten</code> có giá trị thật (không phải <code>None</code>, không rỗng)"],
                  ["<code>socket.create_connection(nghe.getsockname())</code>", "nối tới đúng địa chỉ và cổng mà máy chủ đang nghe"],
                  ["<code>t.recv(64).decode()</code>", "đọc tối đa 64 byte nhận được, rồi <code>.decode()</code> đổi byte về chữ"],
                  ["<code>f\"{ten}\\n  khách: {kq}\"</code>", "chuỗi có chữ <code>f</code> đứng đầu: phần trong ngoặc nhọn được thay bằng giá trị của biến; <code>\\n</code> là xuống dòng"]]),
           """Hàm thử dùng thêm bốn cách viết. Điều kiện có tên chạy khi có tên chứng chỉ. Lệnh nối tới địa chỉ máy chủ đang nghe. Lệnh đọc tối đa sáu mươi bốn byte rồi đổi về chữ.
           Chuỗi có chữ f đứng đầu thay phần trong ngoặc nhọn bằng giá trị, gạch ngược n là xuống dòng.""", clear=True),
        st(code(PY_CLIENT, "Khách: thử với một chứng chỉ (hoặc không có)"),
           """Hàm thử mở một luồng phục vụ, rồi làm khách. Khách tin ca một để kiểm máy chủ, và nạp chứng chỉ của mình nếu có. Khách đọc lời chào hoặc bắt lỗi, rồi in kết quả hai phía.""",
           focus=[["2.2", "2.3"], ["2.4", "2.5"], ["2.6", "2.7", "2.8", "2.9", "2.10"], "2.12"], clear=True),
        st(code(PY_RUN, "Năm lần thử"),
           """Ta thử năm lần, từ không có chứng chỉ tới khách đúng.""", clear=True),
        st(out(OUT_TLS),
           """Không có chứng chỉ thì máy chủ báo khách không trình chứng chỉ. Khách lạ thì không tìm được nơi cấp mình tin. Khách cũ thì chứng chỉ đã hết hạn.
           Kế toán qua ba cửa nhưng tên không có trong danh sách nên bị từ chối ở cửa bốn. Khách đúng thì nhận được lời chào.""",
           focus=[0, ["2.1", "2.2", "2.3"], ["2.4", "2.5", "2.6"], ["2.7", "2.8", "2.9"], ["2.10", "2.11", "2.12"], ["2.13", "2.14", "2.15"]], clear=True),
    ], checks=["alg.bnx_l05_cases(" + N + ") == ['none', 'ca', 'expired', 'ok']",
               "alg.bnx_l05_server_reason['ca'] == 'unable to get local issuer certificate'",
               "alg.bnx_days_between('2025-01-01', '2025-04-01') == 31 + 28 + 31 == 90"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: openssl verify", [
        st(out(OUT_VERIFY, "Kết quả thật của dòng openssl verify ở bước C (bỏ bớt hai dòng tên CN=…)"),
           """Ta kiểm lại bằng một đường khác. Công cụ dòng lệnh khác đường gọi và khác phiên bản với Python, nên cho thêm một ý kiến khi kiểm từng chứng chỉ khách.
           Khách đúng được báo đạt. Khách lạ báo lỗi hai mươi, không tìm được nơi cấp. Khách cũ báo lỗi mười, đã hết hạn.""",
           focus=[0, 0, "2.1", ["2.2", "2.3"], ["2.4", "2.5"]], clear=True),
        st(table(["khách", "Python bắt tay thật (máy chủ ghi)", "openssl verify"],
                 [["thanh_toan", "chào thanh_toan", "OK"],
                  ["la_mat", "unable to get local issuer certificate", "error 20: unable to get local issuer certificate"],
                  ["het_han", "certificate has expired", "error 10: certificate has expired"]]),
           """Bắt tay thật bằng Python và lệnh kiểm riêng cho cùng kết luận ở cả ba khách, nên ta tin các cửa kiểm hoạt động đúng.""",
           clear=True),
    ], checks=["alg.bnx_l05_server_reason['expired'] == 'certificate has expired'", "alg.bnx_l05_cases(" + N + ")[3] == 'ok'"])

    quymo = sc("quymo", "example", "Khi số dịch vụ tăng: số lần đổi chứng chỉ mỗi năm", [
        st(table(["cách viết trong Python", "nghĩa", "ví dụ"],
                 [["<code>def xoay(dich_vu, han, nam=365):</code>", "định nghĩa hàm; <code>nam=365</code> là giá trị mặc định nếu lúc gọi không đưa", "<code>xoay(10, 30)</code> dùng nam = 365"],
                  ["<code>han * 2 // 3</code>", "<code>//</code> chia rồi bỏ phần lẻ", "<code>365 * 2 // 3</code> = 730 // 3 = 243"],
                  ["<code>for _ in range(n):</code>", "lặp n lần; tên <code>_</code> nghĩa là không cần giá trị đếm", "n = 3: chạy 3 lần"],
                  ["<code>while ngay &lt;= nam:</code>, <code>dem += 1</code>", "lặp khi điều kiện còn đúng; <code>+= 1</code> là tăng thêm 1", "dem = 4 thì thành 5"]]),
           """Tham số cuối của hàm có thể có giá trị mặc định. Hai dấu gạch chéo chia rồi bỏ phần lẻ, nên ba trăm sáu mươi lăm nhân hai chia ba ra hai trăm bốn mươi ba.
           Vòng lặp một chạy đúng số lần cho trước, vòng lặp hai chạy khi điều kiện còn đúng, và cộng một là tăng biến đếm.""", clear=True),
        st(code(PY_SCALE, "Mỗi dịch vụ xoay chứng chỉ khi đã dùng 2/3 hạn, đếm trong 365 ngày"),
           """Hàm này đếm số lần đổi chứng chỉ trong một năm, khi mỗi dịch vụ xoay lúc đã dùng hai phần ba hạn, với mười, một nghìn, một trăm nghìn dịch vụ.""",
           clear=True),
        st(out(OUT_SCALE, "Kết quả chạy thật")
           + table(["số dịch vụ", "hạn 365 ngày: lần đổi trong 365 ngày đầu", "hạn 30 ngày: lần đổi mỗi năm"],
                   [["10", "10", "180"], ["1 000 (gấp 100 lần)", "1 000", "18 000"], ["100 000 (gấp 10 000 lần)", "100 000", "1 800 000"]])
           + """<p class="note">Hạn 365 ngày: số liệu là trong 365 ngày đầu; về lâu dài cứ 243 ngày đổi một lần, khoảng 1,5 lần mỗi năm (365 : 243).</p>""",
           """Hạn một năm thì trong năm đầu mỗi dịch vụ đổi một lần, về lâu dài khoảng một lần rưỡi mỗi năm. Hạn ba mươi ngày thì mỗi dịch vụ đổi mười tám lần, nên một trăm nghìn dịch vụ phải đổi một triệu tám trăm nghìn lần.
           Chia ra gần năm nghìn lần mỗi ngày, nên hạn ngắn bắt buộc đi cùng hệ thống cấp tự động.""",
           focus=[0, "2.1", "2.2", "2.3", "2.3"], clear=True),
        st(table(["cách", "được", "mất", "khi nào chọn"],
                 [["hạn dài, đổi bằng tay", "ít lần đổi: khoảng 1 đến 1,5 lần mỗi năm mỗi dịch vụ", "khoá lộ còn dùng được gần cả năm; quên ngày hết hạn là sự cố lúc hai giờ sáng", "ít dịch vụ, hệ thống nhỏ"],
                  ["hạn ngắn, đổi tự động", "khoá lộ chỉ hở vài chục ngày; hạn hết là chuyện thường ngày", "phải xây và giữ hệ thống cấp, giám sát; hỏng nó thì mọi dịch vụ cùng gặp lỗi", "nhiều dịch vụ, dữ liệu nhạy cảm"]]),
           """Đổi bằng tay chạy được với mười dịch vụ, nhưng gãy ở hàng nghìn, vì quên một ngày là sự cố.
           Hạn ngắn tự động thu hẹp khoảng hở khi lộ khoá, đổi lại phải giữ một hệ thống cấp mà hỏng thì mọi dịch vụ cùng lỗi.""",
           focus=[0, "1.2", "1.3", "1.3"], clear=True),
    ], checks=["[alg.bnx_l05_rotations_fleet(n, 365) for n in (10, 1000, 100000)] == [10, 1000, 100000]",
               "[alg.bnx_l05_rotations_fleet(n, 30) for n in (10, 1000, 100000)] == [180, 18000, 1800000]",
               "round(1800000 / 365) == 4932 and 100000 // 10 == 10000 and 1000 // 10 == 100"])

    write_lab("BNX", "L05", LAB_DE, "py", LAB_PY, LAB_OUT)
    lab_pr = practice_scene(sc, "Tự làm: lịch xoay vòng chứng chỉ", lib2.practice_steps2(
        st, "BNX", "L05",
        """<p><b>Đề</b>: hôm nay 15/6/2026; ba chứng chỉ (tên, ngày cấp, hạn dùng bằng ngày) <code>so_cai</code> cấp 20/4 hạn 60, <code>bao_cao</code> cấp 10/1 hạn 365, <code>doi_soat</code> cấp 1/5 hạn 30 (số minh hoạ). Viết <code>mau.py</code> in mỗi chứng chỉ một dòng:</p>
<ol><li>ngày xoay = ngày cấp + hạn × 2 // 3 ngày; ngày hết hạn = ngày cấp + hạn</li><li>trạng thái: <code>da het han</code>, <code>can xoay, con N ngay</code> hoặc <code>chua den han xoay</code></li><li>dòng cuối đếm chứng chỉ phải xử lý</li></ol>
<p class="note">Định dạng từng dòng và dữ liệu mẫu nằm trong <code>de.md</code>.</p>""",
        """Bây giờ tới phần bạn tự làm: hôm nay là mười lăm tháng sáu, có ba chứng chỉ khác nhau. Viết chương trình Python tính ngày xoay, ngày hết hạn, in trạng thái từng chứng chỉ và đếm số cái phải xử lý. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> <code>date.fromisoformat("2026-04-20")</code> đổi chữ thành ngày; cộng <code>timedelta(days=60)</code> là cộng 60 ngày (ra 2026-06-19); trừ hai ngày rồi lấy <code>.days</code> cho số ngày giữa chúng; <code>//</code> chia bỏ phần lẻ (<code>7 // 2</code> = 3). Xét hết hạn trước, rồi mới tới cần xoay.
Lời giải ở <code>labs/BNX/L05/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, đổi chữ thành ngày bằng hàm đọc ngày chuẩn, cộng số ngày bằng khoảng thời gian, và trừ hai ngày để ra số ngày còn lại. Xét hết hạn trước, rồi mới tới cần xoay. Chỉ mở lời giải sau khi đã tự thử.""", pause=120), "BNX", "L05")

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Gặp lỗi chứng chỉ thì <b class="red">tắt kiểm</b> “để chạy tạm” (<code>CERT_NONE</code>, <code>verify=False</code>).
Khi đó cả ba khách sai ở trên đều vào được, và “tạm” thường thành mãi mãi.
<br><span class="note">Cách chữa: đọc thông báo lỗi như ở ví dụ, sửa đúng chứng chỉ hoặc nơi cấp.</span></div>""",
           """Lỗi thứ nhất, của người mới. Gặp lỗi chứng chỉ thì tắt kiểm để chạy tạm. Khi đó cả ba khách sai đều vào được, và cái tạm thường thành mãi mãi. Cách chữa là đọc thông báo lỗi.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Coi mTLS là <b class="red">phân quyền</b>. Chứng chỉ chỉ nói “đây là máy <code>thanh_toan</code>”, không nói khách hàng nào, được làm gì.
<br><span class="note">Cách chữa: mTLS xác thực máy; quyền theo người dùng vẫn đi bằng mã truy cập có phạm vi (OAuth 2.0), và ứng dụng tự kiểm tên ở cửa ④.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là coi M T L S là phân quyền. Chứng chỉ chỉ nói đây là máy nào, không nói khách hàng nào, được làm việc gì.
           Cách chữa là dùng M T L S để xác thực máy, còn quyền theo người dùng đi bằng mã truy cập có phạm vi.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> <b class="red">Quên ngày hết hạn</b>: hai giờ sáng, mọi lệnh gọi trả lỗi như khách <code>het_han</code>. Hoặc <b class="red">đổi nơi cấp cùng lúc cho mọi máy</b>: lỗi như khách <code>la_mat</code> (unable to get local issuer certificate).
<br><span class="note">Cách chữa: cảnh báo trước 30 ngày, xoay vòng tự động; khi đổi nơi cấp, máy chủ tin <b>cả cũ lẫn mới</b> tới khi mọi khách đã đổi.</span></div>""",
           """Lỗi thứ ba, của người đã đi làm, có hai dạng. Quên ngày hết hạn thì hai giờ sáng mọi lệnh gọi trả lỗi như khách cũ. Đổi nơi cấp cùng lúc cho mọi máy thì lỗi giống khách lạ.
           Cách chữa là cảnh báo trước ba mươi ngày, xoay vòng tự động, và tin cả nơi cấp cũ lẫn mới tới khi mọi khách đã đổi.""", clear=True),
    ], checks=["alg.bnx_l05_cases(" + N + ").count('ok') == 1", "90 - alg.bnx_rotate_day(90) == 30"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Chứng chỉ khách cấp 1/3/2026, hạn 90 ngày, xoay vòng khi đã dùng 2/3 thời hạn. Xoay ngày nào? Còn bao nhiêu ngày dự phòng?"],
                  ["2", "Nhật ký máy chủ ghi <code>unable to get local issuer certificate</code>. Nguyên nhân khả dĩ nhất là gì, sửa ở đâu?"],
                  ["3", "Quyết định (số minh hoạ): chứng chỉ khách hạn 365 ngày đổi bằng tay, hay hạn 30 ngày đổi tự động? Giả sử khoá riêng lộ ở ngày 10 và không ai phát hiện hay thu hồi chứng chỉ sớm."]]),
           """Đến lượt bạn, ba câu trên màn hình. Câu ba chọn hạn một năm đổi tay hay hạn ba mươi ngày đổi tự động. Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: dùng 2/3 của 90 ngày.</p>
$$90 \\cdot \\frac{2}{3} = 60 \\Rightarrow 1/3/2026 + 60 = \\hlg{30/4/2026}; \\quad 90 - 60 = \\hlg{30} \\text{ ngày}$$""",
           """Đáp án câu một. Hai phần ba của chín mươi là sáu mươi ngày, nên xoay vào ngày ba mươi tháng tư, còn ba mươi ngày dự phòng."""),
        st("""<p>Câu 2: giống khách <code>la_mat</code>: chứng chỉ khách do nơi cấp mà máy chủ <b>không tin</b> ký (hoặc khách quên gửi chứng chỉ trung gian).
<br><span class='note'>Sửa: cấp lại từ đúng nơi cấp, hoặc thêm nơi cấp hợp lệ vào danh sách tin. Không tắt kiểm.</span></p>""",
           """Đáp án câu hai. Giống khách lạ ở ví dụ, chứng chỉ khách do nơi cấp mà máy chủ không tin ký, hoặc thiếu chứng chỉ trung gian. Cách sửa là cấp lại từ đúng nơi cấp, hoặc thêm nơi cấp hợp lệ vào danh sách tin, không tắt kiểm.""", clear=True),
        st(table(["lựa chọn", "được", "mất"],
                 [["hạn 365 ngày, đổi bằng tay", "năm đầu đổi 1 lần, về lâu dài khoảng 1,5 lần mỗi năm", "khoá lộ ở ngày 10 (không thu hồi): kẻ gian còn dùng 365 − 10 = 355 ngày; đổi bằng tay dễ quên"],
                  ["hạn 30 ngày, đổi tự động", "khoá lộ ở ngày 10 (không thu hồi): chỉ còn 30 − 10 = 20 ngày; quen đổi nên ít sự cố", "xoay ở ngày 20 (2/3 của 30 ngày), nên đổi 365 : 20 ≈ 18 lần mỗi năm (lấy phần nguyên); cần hệ thống cấp tự động"]])
           + "<div class='box key'><b>Chốt:</b> chọn hạn 30 ngày, đổi tự động: khoảng hở 20 ngày thay vì 355. Cái giá là phải có hệ thống cấp tự động và theo dõi; chưa có thì dựng nó trước, không lùi về hạn một năm đổi tay. Nếu thu hồi được ngay khi phát hiện, khoảng hở nhỏ hơn, nhưng hạn ngắn vẫn là lớp phòng thêm.</div>",
           """Đáp án câu ba. Hạn một năm đổi bằng tay thì khoá lộ ở ngày mười cho kẻ gian ba trăm năm mươi lăm ngày.
           Hạn ba mươi ngày đổi tự động chỉ để hở hai mươi ngày, đổi lại mỗi năm phải đổi mười tám lần và cần hệ thống cấp tự động.
           Chốt lại, chọn hạn ba mươi ngày, nhưng dựng hệ thống cấp tự động trước.""",
           focus=[0, "1.2", "1.3", 2]),
    ], checks=["alg.bnx_rotate_day(90) == 60", "alg.bnx_add_days('2026-03-01', 60) == '2026-04-30'",
               "alg.bnx_add_days('2026-03-01', 90) == '2026-05-30'", "alg.bnx_leak_window(365, 10) == 355",
               "alg.bnx_leak_window(30, 10) == 20", "alg.bnx_rotate_day(30) == 20", "alg.bnx_rotations_per_year(30) == 18", "alg.bnx_rotations_per_year(365) == 1"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("máy chủ xin chứng chỉ khách", "khách ký bằng khoá riêng", "kiểm nơi cấp, hạn", "ứng dụng kiểm tên", "xoay vòng trước hạn"),
           """Máy chủ xin chứng chỉ khách, khách ký bằng khoá riêng.
           Thư viện kiểm nơi cấp và hạn, ứng dụng kiểm tên, người vận hành xoay vòng trước khi hết hạn."""),
        st("""<div class='box key'><b>Tư duy:</b> mTLS trả lời “máy nào đang gọi”, mã truy cập trả lời “được làm gì, thay mặt ai”. Cần cả hai.
Mỗi thông báo lỗi ở ví dụ chỉ về một cửa (riêng “unable to get local issuer certificate” có hai nguyên nhân, như câu 2): đọc nó trước khi sửa.</div>""",
           """Điều cần mang theo. M T L S trả lời máy nào đang gọi, còn mã truy cập trả lời được làm gì và thay mặt ai, nên cần cả hai.
           Mỗi thông báo lỗi thường chỉ về một cửa, nên hãy đọc nó trước khi sửa."""),
        st("""<p>Bài sau: viết thủ tục chuyển tiền chạy ngay trong cơ sở dữ liệu Oracle và SQL Server.</p>""",
           """Ở bài sáu, ta viết thủ tục chuyển tiền chạy ngay trong cơ sở dữ liệu, có tham số, giao dịch và bắt lỗi.""",
           forward_ref=True),
    ])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L05", "mtls_chung_chi_hai_chieu", "Bài 5 — mTLS: hai bên cùng trình chứng chỉ khi các dịch vụ gọi nhau",
                  "curriculum/bnx.yaml L05; audit/bnx/verify_bnx.py L05 (chạy thật openssl 3.5.5 + Python 3.13 ssl, 2026-11-11); "
                  "RFC 8446 mục 4.4.2.4, 4.4.3 (2018); Python 3.13 tài liệu mô-đun ssl (create_default_context, CERT_REQUIRED; đọc 2026-11-11)",
                  ["Phân biệt TLS một chiều và hai chiều", "Kiểm một chứng chỉ khách: chuỗi tin cậy, hạn dùng, tên",
                   "Đọc lỗi bắt tay khi thiếu hoặc sai chứng chỉ", "Lên kế hoạch xoay vòng chứng chỉ trước khi hết hạn",
                   "So số lần đổi chứng chỉ mỗi năm ở 10, 1 000 và 100 000 dịch vụ với hạn 365 và 30 ngày",
                   "Tính ngày xoay, ngày hết hạn và trạng thái của một danh sách chứng chỉ"],
                  scenes,
                  covers=[(1, "intuition"), (2, "example"), (3, "example"), (4, "formula"), (5, "quymo"), (6, "practice")])
