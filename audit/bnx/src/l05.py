import re

from lib import *

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
# máy chủ (tên localhost) và khách đúng, cùng do ca1 ký
openssl req -x509 -newkey ed25519 -noenc -subj /CN=localhost \\
  -addext basicConstraints=CA:FALSE -CA ca1.crt -CAkey ca1.key \\
  -addext subjectAltName=DNS:localhost -days 90 \\
  -keyout may_chu.key -out may_chu.crt
openssl req -x509 -newkey ed25519 -noenc -subj /CN=thanh_toan \\
  -addext basicConstraints=CA:FALSE -CA ca1.crt -CAkey ca1.key \\
  -days 90 -keyout thanh_toan.key -out thanh_toan.crt
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
'''

PY_SERVE = r'''
def phuc_vu(loi, xong):
    c, _ = nghe.accept()
    t = mc.wrap_socket(c, server_side=True,
                       do_handshake_on_connect=False)
    try:
        t.do_handshake()
        ten = dict(x[0] for x in t.getpeercert()["subject"])
        t.sendall(("chào " + ten["commonName"]).encode())
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
for ten in [None, "la_mat", "het_han", "thanh_toan"]:
    thu(ten)
'''

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
           """Chào bạn, dịch vụ thanh toán gọi giao diện lập trình của sổ cái trong mạng nội bộ. Người vận hành hay gặp hai câu hỏi, với số minh hoạ.
           Một, một máy lạ cắm vào mạng nội bộ có gọi được sổ cái không, nếu sổ cái chỉ tin rằng ở trong mạng là người nhà?
           Hai, chứng chỉ của dịch vụ hạn chín mươi ngày, cấp ngày một tháng ba. Đến ngày ba mươi tháng năm không ai nhớ đổi, chuyện gì xảy ra?""",
           focus=[1, 1, 2, 2, 2]),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["máy chủ biết người gọi là ai bằng cách nào", "mTLS: máy chủ đòi chứng chỉ của khách và tự kiểm"],
                  ["kiểm những gì", "chuỗi tin cậy, hạn dùng, tên; chạy thật bằng openssl và Python"],
                  ["tránh sự cố hết hạn thế nào", "theo dõi ngày hết hạn, xoay vòng trước, không tắt kiểm"]]),
           """Hôm nay ta trả lời ba câu. Máy chủ biết người gọi là ai bằng cách nào, câu trả lời là M T L S, hai bên cùng trình chứng chỉ.
           Máy chủ kiểm những gì, ta sẽ chạy thật bằng công cụ dòng lệnh và Python. Và làm sao tránh sự cố hết hạn.""",
           focus=[0, "1.2", "1.3", "1.4"]),
    ], checks=["alg.bnx_add_days('2026-03-01', 90) == '2026-05-30'"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① khoá riêng, khoá công khai", "khoá riêng dùng để ký, giữ kín; khoá công khai dùng để kiểm chữ ký, ai cũng có", "<code>thanh_toan.key</code> giữ kín, <code>.crt</code> gửi đi"],
                  ["② chứng chỉ", "tên + khoá công khai + hạn dùng, có chữ ký của <b>nơi cấp</b> (CA)", "CN=thanh_toan, do ca1 ký, hạn 90 ngày"],
                  ["③ chuỗi tin cậy", "tin nơi cấp thì tin chứng chỉ nơi đó ký, nếu còn hạn và đúng tên; thường có nơi cấp <b>trung gian</b>: gốc → trung gian → lá, bên trình chứng chỉ gửi kèm chứng chỉ trung gian", "tin ca1 thì tin <code>may_chu.crt</code> (ở bài này không có trung gian)"],
                  ["④ TLS một chiều", "lớp bọc kết nối: dữ liệu được mã hoá, và khách kiểm chứng chỉ máy chủ (tên, hạn, nơi cấp) để biết chắc nói với đúng máy chủ; máy chủ <b>không biết</b> khách là ai", "trình duyệt mở trang ngân hàng"]]),
           """Trước hết ta cần hiểu bốn điều. Thứ nhất, khoá riêng dùng để ký và phải giữ kín, còn khoá công khai dùng để kiểm chữ ký, ai cũng có.
           Thứ hai, chứng chỉ gồm tên, khoá công khai và hạn dùng, có chữ ký của nơi cấp. Thứ ba, chuỗi tin cậy nghĩa là tin nơi cấp thì tin chứng chỉ nơi đó ký, nếu chứng chỉ còn hạn và đúng tên.
           Thực tế thường có nơi cấp trung gian đứng giữa nơi cấp gốc và chứng chỉ lá, và bên trình chứng chỉ phải gửi kèm chứng chỉ trung gian.
           Thứ tư, TLS là lớp bọc kết nối, để dữ liệu được mã hoá và khách biết chắc mình đang nói với đúng máy chủ.
           Ở kiểu một chiều, chỉ khách kiểm chứng chỉ máy chủ, còn máy chủ không biết khách là ai.""",
           focus=[0, "1.2", "1.3", "1.4", "1.4", "1.5", "1.5"]),
        st("""<p>Làm thử: chứng chỉ cấp ngày 1/3/2026, hạn 90 ngày.</p>
$$31 + 30 + 29 = 90 \\;\\Rightarrow\\; \\text{hết hạn ngày } \\hl{30/5/2026}$$""",
           """Làm thử, chứng chỉ cấp ngày một tháng ba, hạn chín mươi ngày. Tháng ba còn ba mươi mốt ngày, tháng tư ba mươi ngày, cộng hai mươi chín ngày của tháng năm là đủ chín mươi, nên hết hạn ngày ba mươi tháng năm.""", clear=True),
    ], checks=["alg.bnx_add_days('2026-03-01', 90) == '2026-05-30'", "alg.bnx_days_between('2026-03-01', '2026-05-30') == 31 + 30 + 29 == 90"])

    sym = sc("sym", "symbol", "Giải mã các từ trên chứng chỉ", [
        st(table(["từ trên màn hình", "nghĩa"],
                 [["CA (nơi cấp)", "bên ký chứng chỉ; ở đây tự dựng hai nơi cấp ca1, ca2"],
                  ["CN, subjectAltName", "tên trong chứng chỉ: <code>CN=thanh_toan</code>; máy chủ ghi tên miền ở <code>DNS:localhost</code>"],
                  ["notBefore, notAfter", "hạn dùng: từ ngày nào tới ngày nào"],
                  ["keyUsage=keyCertSign", "chứng chỉ này được phép <b>ký chứng chỉ khác</b> (chỉ nơi cấp mới có); nơi cấp còn cần <code>basicConstraints=CA:TRUE</code>, lệnh <code>req -x509</code> tự thêm"],
                  ["basicConstraints=CA:FALSE", "chứng chỉ lá: không được làm nơi cấp"],
                  ["CERT_REQUIRED", "máy chủ <b>bắt buộc</b> khách trình chứng chỉ hợp lệ"]]),
           """Bảng này giải mã các từ trên chứng chỉ. Nơi cấp là bên ký chứng chỉ, hôm nay ta tự dựng hai nơi cấp.
           Tên trong chứng chỉ ghi ở trường tên chung, còn máy chủ ghi tên miền ở trường tên thay thế.
           Hai trường thời điểm cho biết hạn dùng từ ngày nào tới ngày nào. Cờ ký chứng chỉ cho phép ký chứng chỉ khác, chỉ nơi cấp mới có, cùng cờ là nơi cấp mà lệnh tạo chứng chỉ tự ký tự thêm vào.
           Cờ không phải nơi cấp đánh dấu chứng chỉ lá. Cuối cùng, chế độ bắt buộc nghĩa là máy chủ đòi khách trình chứng chỉ hợp lệ.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
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
           """Bên trái là TLS một chiều. Máy chủ gửi chứng chỉ, khách kiểm tên, hạn và nơi cấp, còn máy chủ không biết khách là ai.
           Bên phải là M T L S. Máy chủ gửi chứng chỉ của mình và xin chứng chỉ của khách. Khách gửi lại chứng chỉ, kèm một chữ ký làm bằng khoá riêng.
           Vì có chữ ký đó, kẻ chỉ chép được tệp chứng chỉ mà không có khoá riêng thì vẫn không qua được."""),
        st(gate,
           """Máy chủ kiểm khách qua các cửa. Một, khách có trình chứng chỉ không. Hai, chứng chỉ có do nơi cấp mình tin ký không. Ba, còn trong hạn không.
           Ba cửa này do thư viện mật mã làm, và mỗi cửa hỏng có một thông báo riêng, ghi bằng chữ đỏ. Cửa bốn, tên khách có được gọi API này không, là việc của ứng dụng."""),
    ])

    form = sc("formula", "formula", "Suy ra từng bước: máy chủ biết khách là ai", [
        st("""<p><b>Bước 1.</b> TLS một chiều chỉ chứng minh <b>máy chủ</b> là ai. Ai vào được mạng nội bộ cũng mở được kết nối tới sổ cái.</p>
<span class='note'>Làm thử: máy lạ gọi bằng kênh một chiều → máy chủ không có gì để từ chối.</span>""",
           """Bước một, vì TLS một chiều chỉ chứng minh máy chủ là ai, nên ai vào được mạng nội bộ cũng mở được kết nối tới sổ cái.
           Làm thử, một máy lạ gọi bằng kênh một chiều, máy chủ không có căn cứ gì để từ chối.""", clear=True),
        st("""<p><b>Bước 2.</b> Máy chủ <b>xin</b> chứng chỉ khách. Khách gửi chứng chỉ và một <b>chữ ký</b> bằng khoá riêng trên cuộc <b>bắt tay</b>, tức vài thông điệp đầu hai bên trao đổi để trình chứng chỉ và thống nhất khoá trước khi gửi dữ liệu (RFC 8446 mục 4.4.3).
<br><span class='note'>Làm thử: tệp .crt có thể lộ; tệp .key không rời máy, nên kẻ chép .crt vẫn không ký được.</span></p>""",
           """Bước hai, máy chủ xin chứng chỉ của khách. Bắt tay là vài thông điệp đầu hai bên trao đổi để trình chứng chỉ và thống nhất khoá, trước khi gửi dữ liệu.
           Khách gửi chứng chỉ, kèm một chữ ký trên cuộc bắt tay làm bằng khoá riêng, nên máy chủ biết khách thật sự giữ khoá.
           Làm thử, tệp chứng chỉ của dịch vụ thanh toán có thể lộ vì nó công khai, nhưng tệp khoá riêng không rời máy, nên kẻ chép tệp chứng chỉ vẫn không ký được."""),
        st("""<p><b>Bước 3.</b> Máy chủ kiểm <b>chuỗi tin cậy</b> (do ca1 ký) và <b>hạn dùng</b> (notBefore ≤ bây giờ ≤ notAfter). Ứng dụng kiểm thêm <b>tên</b>.</p>
$$\\text{het\\_han: notAfter } = 1/4/2025, \\text{ sớm hơn hôm nay} \\;\\Rightarrow\\; \\hl{\\text{hỏng}}$$""",
           """Bước ba, máy chủ kiểm chuỗi tin cậy, tức chứng chỉ có do nơi cấp một ký không, và kiểm hạn dùng. Ứng dụng kiểm thêm tên của khách.
           Làm thử, chứng chỉ khách cũ hết hạn ngày một tháng tư năm hai nghìn hai mươi lăm, sớm hơn hôm nay, nên hỏng.""", clear=True),
        st("""<p><b>Bước 4.</b> Ở TLS 1.3, khách gửi chứng chỉ <b>sau</b> thông điệp kết thúc của máy chủ, nên phía khách thấy bắt tay đã xong rồi máy chủ mới kiểm.
Lỗi chứng chỉ khách vì vậy hiện ra ở <b>lần đọc đầu tiên</b> (quan sát khi chạy thật).</p>""",
           """Bước bốn, một chi tiết làm nhiều người bối rối. Ở TLS phiên bản một chấm ba, khách gửi chứng chỉ sau thông điệp kết thúc của máy chủ.
           Nên phía khách tưởng bắt tay đã xong, rồi máy chủ mới kiểm. Vì vậy lỗi chứng chỉ khách hiện ra ở lần đọc đầu tiên, như ta sẽ thấy khi chạy thật."""),
        st("""<p><b>Bước 5.</b> Chứng chỉ hết hạn là sự cố <b>có lịch hẹn trước</b>: xoay vòng khi đã dùng 2/3 thời hạn (số minh hoạ).</p>
$$90 \\cdot \\frac{2}{3} = \\hl{60} \\text{ ngày}; \\quad 90 - 60 = \\hlg{30} \\text{ ngày dự phòng}$$""",
           """Bước năm, vì ngày hết hạn biết trước, sự cố hết hạn là sự cố có lịch hẹn. Ta xoay vòng khi đã dùng hai phần ba thời hạn, theo số minh hoạ.
           Làm thử, chín mươi nhân hai phần ba là sáu mươi ngày, còn ba mươi ngày dự phòng nếu lần xoay đầu trục trặc.""", clear=True),
    ], checks=["alg.bnx_l05_cases(" + N + ")[2] == 'expired'", "alg.bnx_rotate_day(90) == 60", "90 - alg.bnx_rotate_day(90) == 30"])

    ex = sc("example", "example", "Ví dụ chạy thật, từng ca", [
        st(code(SH_CA, "Bước A: hai nơi cấp tự ký (openssl 3.5, Git Bash)"),
           """Ta làm thật. Bước A tạo hai nơi cấp tự ký, ca một và ca hai, mỗi nơi một cặp khoá và một chứng chỉ hạn ba trăm sáu mươi lăm ngày.
           Dòng đầu chỉ cần khi chạy cửa sổ lệnh này trên máy văn phòng, như chú thích ghi, để đường dẫn bắt đầu bằng dấu gạch chéo không bị tự đổi.
           Cờ ký chứng chỉ là bắt buộc, vì thiếu nó thì Python ba chấm mười ba từ chối nơi cấp ngay.""",
           focus=[0, ["2.3", "2.6"], "2.1", ["2.4", "2.7"]], clear=True),
        st(code(SH_SERVER, "Bước B: chứng chỉ máy chủ và khách đúng, do ca1 ký"),
           """Bước B cho ca một ký hai chứng chỉ lá hạn chín mươi ngày. Một cho máy chủ, mang tên máy cục bộ. Một cho dịch vụ thanh toán, là khách đúng.""",
           focus=["2.1", ["2.2", "2.3", "2.4", "2.5"], ["2.6", "2.7", "2.8"]], clear=True),
        st(code(SH_BAD, "Bước C: hai khách sai, rồi tự kiểm bằng openssl verify"),
           """Bước C tạo hai khách sai. Khách lạ do ca hai ký. Khách cũ do ca một ký nhưng hạn dùng từ một tháng một tới một tháng tư năm hai nghìn hai mươi lăm.
           Dòng cuối kiểm ba chứng chỉ khách với nơi cấp ca một, ta sẽ đọc kết quả ở phần tự kiểm.""",
           focus=["2.1", ["2.2", "2.3", "2.4"], ["2.5", "2.6", "2.7", "2.8"], "2.9"], clear=True),
        st(code(PY_CTX, "Máy chủ Python: bắt buộc chứng chỉ khách"),
           """Giờ dựng máy chủ bằng thư viện chuẩn của Python. Máy chủ nạp chứng chỉ và khoá của mình, chỉ tin nơi cấp ca một, và đặt chế độ bắt buộc chứng chỉ khách.
           Nó nghe ở một cổng ngẫu nhiên trên chính máy này.""", focus=["2.1", ["2.3", "2.4", "2.5", "2.6"], "2.7"], clear=True),
        st(code(PY_SERVE, "Mỗi kết nối: bắt tay, chào theo tên, hoặc ghi lý do (mã minh hoạ CHƯA kiểm tên: cửa ④ để trống)"),
           """Mỗi kết nối, máy chủ bắt tay. Nếu được, nó đọc tên chung trong chứng chỉ khách và gửi lời chào theo tên đó.
           Nếu hỏng, nó ghi lại lý do. Dòng cuối đợi khách đọc xong mới đóng, để khách kịp nhận thông báo lỗi, còn cửa bốn vẫn để trống vì mã chỉ đọc tên để chào, chưa so với danh sách được phép.""",
           focus=[["2.2", "2.3", "2.4", "2.6"], ["2.7", "2.8"], ["2.9", "2.10"], "2.11"], clear=True),
        st(code(PY_CLIENT, "Khách: thử với một chứng chỉ (hoặc không có)"),
           """Hàm thử mở một luồng phục vụ, rồi làm khách. Khách tin ca một để kiểm máy chủ, và nạp chứng chỉ của mình nếu có.
           Khách đọc lời chào, hoặc bắt lỗi. Cuối cùng in ra điều khách thấy và điều máy chủ ghi.""",
           focus=[["2.2", "2.3"], ["2.4", "2.5"], ["2.6", "2.7", "2.8", "2.9", "2.10"], "2.12"], clear=True),
        st(code(PY_RUN, "Bốn lần thử"),
           """Ta thử bốn lần: không có chứng chỉ, khách lạ, khách cũ, và khách đúng.""", clear=True),
        st(out(OUT_TLS),
           """Kết quả chạy thật. Không có chứng chỉ thì máy chủ báo khách không trình chứng chỉ. Khách lạ thì máy chủ không tìm được nơi cấp mình tin.
           Khách cũ thì chứng chỉ đã hết hạn. Khách đúng thì nhận được lời chào theo đúng tên.""",
           focus=[0, ["2.1", "2.2", "2.3"], ["2.4", "2.5", "2.6"], ["2.7", "2.8", "2.9"], ["2.10", "2.11", "2.12"]], clear=True),
        st("""<p>Đếm theo các cửa ở hình trước:</p>
$$① \\text{ không chứng chỉ} \\to \\hl{\\text{cửa ①}}; \\quad ② \\text{ la\\_mat} \\to \\hl{\\text{cửa ②}}; \\quad ③ \\text{ het\\_han} \\to \\hl{\\text{cửa ③}}$$
$$④ \\text{ thanh\\_toan} \\to \\hlg{\\text{qua cả ba}}; \\quad ⑤ \\; 31 + 28 + 31 = 90 \\text{ ngày hạn của het\\_han, đã qua}$$""",
           """Đối chiếu với các cửa. Ca một hỏng ở cửa một, ca hai hỏng ở cửa hai, ca ba hỏng ở cửa ba, còn ca bốn qua cả ba cửa.
           Phép tính thứ năm, hạn của khách cũ từ một tháng một tới một tháng tư là ba mươi mốt cộng hai mươi tám cộng ba mươi mốt, bằng chín mươi ngày, và đã qua lâu.""",
           focus=[1, 2, 3], clear=True),
    ], checks=["alg.bnx_l05_cases(" + N + ") == ['none', 'ca', 'expired', 'ok']",
               "alg.bnx_l05_server_reason['ca'] == 'unable to get local issuer certificate'",
               "alg.bnx_days_between('2025-01-01', '2025-04-01') == 31 + 28 + 31 == 90"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: openssl verify", [
        st(out(OUT_VERIFY, "Kết quả thật của dòng openssl verify ở bước C (bỏ bớt hai dòng tên CN=…)"),
           """Bây giờ ta kiểm lại kết luận bằng một đường hoàn toàn khác. Vì công cụ dòng lệnh mật mã dùng một bản thư viện khác với bản Python dùng, nó cho một ý kiến độc lập khi kiểm từng chứng chỉ khách, không qua bắt tay.
           Khách đúng được báo đạt. Khách lạ báo lỗi hai mươi, không tìm được nơi cấp. Khách cũ báo lỗi mười, chứng chỉ đã hết hạn.""",
           focus=[0, 0, "2.1", ["2.2", "2.3"], ["2.4", "2.5"]], clear=True),
        st(table(["khách", "Python bắt tay thật (máy chủ ghi)", "openssl verify"],
                 [["thanh_toan", "chào thanh_toan", "OK"],
                  ["la_mat", "unable to get local issuer certificate", "error 20: unable to get local issuer certificate"],
                  ["het_han", "certificate has expired", "error 10: certificate has expired"]]),
           """Bảng này đặt hai đường cạnh nhau. Bắt tay thật bằng Python và lệnh kiểm riêng cho cùng kết luận ở cả ba khách, nên ta tin các cửa kiểm hoạt động đúng.""",
           clear=True),
    ], checks=["alg.bnx_l05_server_reason['expired'] == 'certificate has expired'", "alg.bnx_l05_cases(" + N + ")[3] == 'ok'"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Gặp lỗi chứng chỉ thì <b class="red">tắt kiểm</b> “để chạy tạm” (<code>CERT_NONE</code>, <code>verify=False</code>).
Khi đó cả ba khách sai ở trên đều vào được, và “tạm” thường thành mãi mãi.
<br><span class="note">Cách chữa: đọc thông báo lỗi như ở ví dụ, sửa đúng chứng chỉ hoặc nơi cấp.</span></div>""",
           """Lỗi thứ nhất, của người mới. Gặp lỗi chứng chỉ thì tắt kiểm để chạy tạm. Khi đó cả ba khách sai ở trên đều vào được, và cái tạm thường thành mãi mãi.
           Cách chữa là đọc thông báo lỗi như ta vừa làm, rồi sửa đúng chứng chỉ hoặc nơi cấp.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Coi mTLS là <b class="red">phân quyền</b>. Chứng chỉ chỉ nói “đây là máy <code>thanh_toan</code>”, không nói khách hàng nào, được làm gì.
<br><span class="note">Cách chữa: mTLS xác thực máy; quyền theo người dùng vẫn đi bằng mã truy cập có phạm vi (OAuth 2.0), và ứng dụng tự kiểm tên ở cửa ④.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là coi M T L S là phân quyền. Chứng chỉ chỉ nói đây là máy của dịch vụ thanh toán, không nói khách hàng nào, được làm việc gì.
           Cách chữa là dùng M T L S để xác thực máy, còn quyền theo người dùng vẫn đi bằng mã truy cập có phạm vi như ở bài bốn, và ứng dụng tự kiểm tên.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> <b class="red">Quên ngày hết hạn</b>: hai giờ sáng, mọi lệnh gọi trả lỗi như khách <code>het_han</code>. Hoặc <b class="red">đổi nơi cấp cùng lúc cho mọi máy</b>: lỗi như khách <code>la_mat</code> (unable to get local issuer certificate).
<br><span class="note">Cách chữa: cảnh báo trước 30 ngày, xoay vòng tự động; khi đổi nơi cấp, máy chủ tin <b>cả cũ lẫn mới</b> tới khi mọi khách đã đổi.</span></div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, có hai dạng. Quên ngày hết hạn thì hai giờ sáng mọi lệnh gọi trả lỗi như khách cũ ở ví dụ.
           Còn đổi nơi cấp cùng lúc cho mọi máy thì lỗi giống khách lạ, máy chủ không tìm được nơi cấp mình tin.
           Cách chữa là cảnh báo trước ba mươi ngày và xoay vòng tự động. Khi đổi nơi cấp, máy chủ tin cả nơi cấp cũ lẫn mới, cho tới khi mọi khách đã đổi xong.""", clear=True),
    ], checks=["alg.bnx_l05_cases(" + N + ").count('ok') == 1", "90 - alg.bnx_rotate_day(90) == 30"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Chứng chỉ khách cấp 1/3/2026, hạn 90 ngày, xoay vòng khi đã dùng 2/3 thời hạn. Xoay ngày nào? Còn bao nhiêu ngày dự phòng?"],
                  ["2", "Nhật ký máy chủ ghi <code>unable to get local issuer certificate</code>. Nguyên nhân khả dĩ nhất là gì, sửa ở đâu?"],
                  ["3", "Quyết định (số minh hoạ): chứng chỉ khách hạn 365 ngày đổi bằng tay, hay hạn 30 ngày đổi tự động? Giả sử khoá riêng lộ ở ngày 10."]]),
           """Đến lượt bạn. Câu một, chứng chỉ cấp ngày một tháng ba, hạn chín mươi ngày, xoay khi đã dùng hai phần ba thời hạn. Xoay ngày nào, còn bao nhiêu ngày dự phòng?
           Câu hai, nhật ký máy chủ ghi không tìm được nơi cấp. Nguyên nhân khả dĩ nhất là gì, sửa ở đâu?
           Câu ba, chọn chứng chỉ hạn một năm đổi bằng tay, hay hạn ba mươi ngày đổi tự động, khi khoá riêng lộ ở ngày thứ mười? Hãy dừng video lại và làm từng câu ra giấy trước khi xem đáp án.""",
           pause=25),
        st("""<p>Câu 1: dùng 2/3 của 90 ngày.</p>
$$90 \\cdot \\frac{2}{3} = 60 \\Rightarrow 1/3/2026 + 60 = \\hlg{30/4/2026}; \\quad 90 - 60 = \\hlg{30} \\text{ ngày}$$""",
           """Đáp án câu một. Hai phần ba của chín mươi là sáu mươi ngày, nên xoay vào ngày ba mươi tháng tư. Còn chín mươi trừ sáu mươi, bằng ba mươi ngày dự phòng trước ngày hết hạn ba mươi tháng năm."""),
        st("""<p>Câu 2: giống khách <code>la_mat</code>: chứng chỉ khách do nơi cấp mà máy chủ <b>không tin</b> ký (hoặc khách quên gửi chứng chỉ trung gian).
<br><span class='note'>Sửa: cấp lại từ đúng nơi cấp, hoặc thêm nơi cấp hợp lệ vào danh sách tin. Không tắt kiểm.</span></p>""",
           """Đáp án câu hai. Giống khách lạ ở ví dụ, chứng chỉ khách do một nơi cấp mà máy chủ không tin ký, hoặc khách quên gửi chứng chỉ trung gian.
           Cách sửa là cấp lại từ đúng nơi cấp, hoặc thêm nơi cấp đó vào danh sách tin nếu nó hợp lệ, chứ không tắt kiểm.""", clear=True),
        st(table(["lựa chọn", "được", "mất"],
                 [["hạn 365 ngày, đổi bằng tay", "mỗi năm đổi 1 lần", "khoá lộ ở ngày 10: kẻ gian còn dùng 365 − 10 = 355 ngày; đổi bằng tay dễ quên"],
                  ["hạn 30 ngày, đổi tự động", "khoá lộ ở ngày 10: chỉ còn 30 − 10 = 20 ngày; quen đổi nên ít sự cố", "xoay ở ngày 20 (2/3 của 30 ngày), nên đổi 365 : 20 ≈ 18 lần mỗi năm (lấy phần nguyên); cần hệ thống cấp tự động"]]),
           """Đáp án câu ba. Hạn một năm đổi bằng tay thì mỗi năm đổi một lần, nhưng khoá lộ ở ngày mười cho kẻ gian ba trăm năm mươi lăm ngày, và đổi bằng tay dễ quên.
           Hạn ba mươi ngày đổi tự động chỉ để hở hai mươi ngày, đổi lại vì xoay ở ngày hai mươi, mỗi năm phải đổi mười tám lần và cần hệ thống cấp tự động.""",
           focus=[0, "1.2", "1.3"]),
    ], checks=["alg.bnx_rotate_day(90) == 60", "alg.bnx_add_days('2026-03-01', 60) == '2026-04-30'",
               "alg.bnx_add_days('2026-03-01', 90) == '2026-05-30'", "alg.bnx_leak_window(365, 10) == 355",
               "alg.bnx_leak_window(30, 10) == 20", "alg.bnx_rotate_day(30) == 20", "alg.bnx_rotations_per_year(30) == 18", "alg.bnx_rotations_per_year(365) == 1"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("máy chủ xin chứng chỉ khách", "khách ký bằng khoá riêng", "kiểm nơi cấp, hạn", "ứng dụng kiểm tên", "xoay vòng trước hạn"),
           """Tổng kết chuỗi logic. Máy chủ xin chứng chỉ của khách, khách chứng minh giữ khoá riêng bằng một chữ ký.
           Thư viện kiểm nơi cấp và hạn dùng, ứng dụng kiểm tên, và người vận hành xoay vòng chứng chỉ trước khi hết hạn."""),
        st("""<div class='box key'><b>Tư duy:</b> mTLS trả lời “máy nào đang gọi”, mã truy cập trả lời “được làm gì, thay mặt ai”. Cần cả hai.
Mỗi thông báo lỗi ở ví dụ chỉ về một cửa (riêng “unable to get local issuer certificate” có hai nguyên nhân, như câu 2): đọc nó trước khi sửa.</div>""",
           """Điều cần mang theo. M T L S trả lời câu hỏi máy nào đang gọi, còn mã truy cập trả lời được làm gì và thay mặt ai, nên cần cả hai.
           Mỗi thông báo lỗi ở ví dụ chỉ về một cửa, nên hãy đọc nó trước khi sửa, và nhớ có thông báo mang hai nguyên nhân như câu hai."""),
        st("""<p>Bài sau: viết thủ tục chuyển tiền chạy ngay trong cơ sở dữ liệu Oracle và SQL Server.</p>""",
           """Ở bài sáu, ta chuyển sang cơ sở dữ liệu. Ta viết thủ tục lưu trữ chuyển tiền chạy ngay trong Oracle và một hệ cơ sở dữ liệu phổ biến khác, có tham số, giao dịch và bắt lỗi.""",
           forward_ref=True),
    ])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
    return lesson("L05", "mtls_chung_chi_hai_chieu", "Bài 5 — mTLS: hai bên cùng trình chứng chỉ khi các dịch vụ gọi nhau",
                  "curriculum/bnx.yaml L05; audit/bnx/verify_bnx.py L05 (chạy thật openssl 3.5.5 + Python 3.13 ssl, 2026-11-11); "
                  "RFC 8446 mục 4.4.2.4, 4.4.3 (2018); Python 3.13 tài liệu mô-đun ssl (create_default_context, CERT_REQUIRED; đọc 2026-11-11)",
                  ["Phân biệt TLS một chiều và hai chiều", "Kiểm một chứng chỉ khách: chuỗi tin cậy, hạn dùng, tên",
                   "Đọc lỗi bắt tay khi thiếu hoặc sai chứng chỉ", "Lên kế hoạch xoay vòng chứng chỉ trước khi hết hạn"],
                  scenes)
