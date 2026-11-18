import lib2
from lib2 import *
from labkit import write_lab, practice_steps, practice_scene  # noqa: F401

# ── Mã hiện trên màn hình (chạy NGUYÊN VĂN: audit/bnx/screen/l03.yaml, audit/bnx/ver/l03.py) ──
PY_DATA = r'''
import base64, hmac, hashlib, json
def b64u(b):      # base64url, bỏ dấu "=" ở cuối
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()
def unb64u(s):    # thêm lại "=" rồi giải mã
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
dau = b'{"typ":"JWT",\r\n "alg":"HS256"}'
than = (b'{"iss":"joe",\r\n "exp":1300819380,\r\n'
        b' "http://example.com/is_root":true}')
k = unb64u("AyM1SysPpbyDfgZld3umj1qzKObwVMkoqQ-EstJQLr_T-1qS0g"
           "ZH75aKtMN3Yj0iPS4hcgUuTwjAzZr1Z9CAow")
'''

PY_SIGN = r'''
def ky(than):                 # ký phần thân bằng khoá k
    vao = b64u(dau) + "." + b64u(than)
    mac = hmac.new(k, vao.encode(), hashlib.sha256).digest()
    return vao + "." + b64u(mac)
ma = ky(than)
for phan in ma.split("."):
    print(phan)
'''

PY_READ = r'''
from datetime import datetime, timezone
t = ma.split(".")[1]          # chỉ cần chuỗi mã, KHÔNG cần khoá
print(json.loads(unb64u(t)))
print(datetime.fromtimestamp(1300819380, timezone.utc))
'''

PY_CHECK = r'''
def kiem(ma, aud, bay_gio):
    d, t, s = ma.split(".")
    if json.loads(unb64u(d))["alg"] != "HS256": return "thuật toán lạ"
    mac = hmac.new(k, (d + "." + t).encode(), hashlib.sha256)
    if not hmac.compare_digest(b64u(mac.digest()), s):
        return "chữ ký sai"
    c = json.loads(unb64u(t))
    if bay_gio >= c["exp"]:
        return "hết hạn"
    if c.get("iss") != "joe" or c.get("aud") != aud:
        return "sai người phát hành/nhận"
    return "nhận"
'''

PY_CASES = r'''
import time
print(kiem(ma, "api-a", time.time()))          # mã RFC, hôm nay
d, t, s = ma.split(".")
t2 = b64u(than.replace(b"1300", b"9300"))      # sửa 1 ký tự
print(kiem(d + "." + t2 + "." + s, "api-a", 1300819379))
dn = b64u(b'{"alg":"none"}')                   # alg "none"
print(kiem(dn + "." + t + ".", "api-a", 0))
ma2 = ky(b'{"iss":"joe","aud":"api-a","exp":1300819380}')
print(kiem(ma2, "api-a", 1300819379))
print(kiem(ma2, "api-b", 1300819379))
'''

SH_OPENSSL = r'''
printf %s eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9. \
  eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFt \
  cGxlLmNvbS9pc19yb290Ijp0cnVlfQ > vao.txt
openssl dgst -sha256 -mac HMAC -binary -macopt hexkey:\
0323354b2b0fa5bc837e0665777ba68f5ab328e6f054c928a90f84b2d2502ebf\
d3fb5a92d20647ef968ab4c377623d223d2e2172052e4f08c0cd9af567d080a3 \
  vao.txt | openssl base64 -A | tr '+/' '-_' | tr -d '='
echo
date -u -d @1300819380 '+%F %T'
'''

# Đầu ra thật (chạy 2026-11-11, .venv Python 3.13 và Git Bash + OpenSSL 3.5.5); dòng dài cắt bằng "…"
OUT_SIGN = """
eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9
eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6…
dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
"""
OUT_READ = """
{'iss': 'joe', 'exp': 1300819380, 'http://example.com/is_root': True}
2011-03-22 18:43:00+00:00
"""
OUT_CASES = """
hết hạn
chữ ký sai
thuật toán lạ
nhận
sai người phát hành/nhận
"""
OUT_OPENSSL = """
dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
2011-03-22 18:43:00
"""

# Từ ngoại KHÔNG đạt dò phát âm (BRIEF §6: JWT 0/8, OAuth 3/8, TLS 4/8; OpenID chưa dò): lời đọc tiếng Việt, tên gốc chỉ hiện trên màn hình
SPOKEN = {"JWT": "mã Token tự mang thông tin"}  # BRIEF §6: JWT 0/8 không đạt; JSON đạt 8/8

T = "alg.bnx_jwt_rfc_token()"

# Cảnh quy mô/thời gian (AF2): dùng lại ky và kiem (khối ký, khối kiểm ở cảnh ví dụ). Kẻ gian lấy mã ở giây 60, mỗi giây thử một lần tới giây 4000.
SCALE_PY = r'''
for han in (300, 3600):                 # hạn dùng của mã, giây
    ma = ky(b'{"iss":"joe","aud":"api-a","exp":%d}' % han)
    dung = sum(kiem(ma, "api-a", t) == "nhận" for t in range(60, 4001))
    print("han", han, "giay:", dung, "lan dung duoc sau khi lo o giay 60")
for u in (1000, 1000000):               # số người dùng
    moi = u * 3600 // 300
    cu = u * 3600 // 3600
    print(u, "nguoi dung:", moi, "so voi", cu, "ma moi moi gio")
'''
SCALE_OUT = """
han 300 giay: 240 lan dung duoc sau khi lo o giay 60
han 3600 giay: 3540 lan dung duoc sau khi lo o giay 60
1000 nguoi dung: 12000 so voi 1000 ma moi moi gio
1000000 nguoi dung: 12000000 so voi 1000000 ma moi moi gio
"""

# Lab labs/BNX/L03 (số liệu KHÁC bài: khoá khoa-lab-l03, người nhận app-b, hạn 2000)
LAB_PY = r'''
import base64, hmac, hashlib, json

KHOA = b"khoa-lab-l03"


def b64u(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def ky(dau, than):
    vao = b64u(dau) + "." + b64u(than)
    mac = hmac.new(KHOA, vao.encode(), hashlib.sha256).digest()
    return vao + "." + b64u(mac)


def kiem(ma, aud, bay_gio):
    d, t, s = ma.split(".")
    mac = hmac.new(KHOA, (d + "." + t).encode(), hashlib.sha256).digest()
    if not hmac.compare_digest(b64u(mac), s):
        return "chu ky sai"
    c = json.loads(base64.urlsafe_b64decode(t + "=" * (-len(t) % 4)))
    if bay_gio >= c["exp"]:
        return "het han"
    if c["aud"] != aud:
        return "sai nguoi nhan"
    return "nhan"


dau = b'{"alg":"HS256","typ":"JWT"}'
than = b'{"sub":"u42","aud":"app-b","exp":2000}'
ma = ky(dau, than)
print(ma.split(".")[2])
print(kiem(ma, "app-b", 1999))
print(kiem(ma, "app-b", 2000))
d, t, s = ma.split(".")
sua = b64u(than.replace(b"u42", b"u43"))
print(kiem(d + "." + sua + "." + s, "app-b", 1000))
print(kiem(ma, "app-c", 1000))
'''
LAB_OUT = """2u2clZLfYxRXtF71hz8jZrR1eoKZh8OoqbdfEAFV5_w
nhan
het han
chu ky sai
sai nguoi nhan"""

LAB_DE = """# Lab BNX L03 — Ký và kiểm một JWT HS256

Viết `mau.py` (Python) gồm bốn việc, số liệu là số minh hoạ:

1. Khoá bí mật `KHOA = b"khoa-lab-l03"`.
2. Hàm `b64u(b)`: base64url của các byte, **bỏ dấu `=` ở cuối** (dùng `base64.urlsafe_b64encode` rồi `.rstrip(b"=")`, rồi `.decode()`).
3. Hàm `ky(dau, than)` nhận hai chuỗi byte: ghép `b64u(dau) + "." + b64u(than)` làm chuỗi vào, tính HMAC-SHA256 của chuỗi vào bằng `KHOA` (`hmac.new(KHOA, vao.encode(), hashlib.sha256).digest()`), trả `vao + "." + b64u(mac)`.
4. Hàm `kiem(ma, aud, bay_gio)` tách ba phần, **tính lại chữ ký** và so bằng `hmac.compare_digest`; rồi đọc phần thân (thêm lại `=` cho đủ bội số 4 trước khi giải mã, rồi `json.loads`). Trả đúng một trong các chữ, theo thứ tự kiểm:
   - `chu ky sai`; nếu chữ ký đúng thì
   - `het han` khi `bay_gio >= exp`; nếu chưa hết hạn thì
   - `sai nguoi nhan` khi `aud` của phần thân khác `aud` truyền vào; còn lại là
   - `nhan`.

Sau các hàm, chép nguyên văn đoạn thử (in năm dòng):

```python
dau = b'{"alg":"HS256","typ":"JWT"}'
than = b'{"sub":"u42","aud":"app-b","exp":2000}'
ma = ky(dau, than)
print(ma.split(".")[2])
print(kiem(ma, "app-b", 1999))
print(kiem(ma, "app-b", 2000))
d, t, s = ma.split(".")
sua = b64u(than.replace(b"u42", b"u43"))
print(kiem(d + "." + sua + "." + s, "app-b", 1000))
print(kiem(ma, "app-c", 1000))
```

Đầu vào chữ `import` đầu tệp: `import base64, hmac, hashlib, json`. Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L03 mau.py`.
"""


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
            for a_, b_ in SPOKEN.items():
                s_["say"] = s_["say"].replace(a_, b_)
            _merge_short(s_)
    return scenes


def build():
    write_lab("BNX", "L03", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Sửa một chữ số để mã sống tới năm 2264?", [
        st("""<p>Khách đăng nhập ứng dụng ngân hàng một lần, rồi mỗi lời gọi tới các dịch vụ đều kèm một <b>mã truy cập</b>.
Mã có dạng ba phần nối bằng hai dấu chấm: <code>eyJ0eXAi….eyJpc3Mi….dBjftJeZ…</code></p>
<div class="box key">Phần giữa ghi hạn dùng <b>1300819380</b>. Kẻ gian sửa <b>một chữ số</b> thành <b>9300819380</b>, tức năm <b>2264</b>.
Dịch vụ có nhận không, khi nó không hỏi cơ sở dữ liệu?</div>""",
           """Chào bạn, khách đăng nhập ứng dụng ngân hàng một lần, rồi mỗi lời gọi kèm một mã truy cập ba phần nối bằng hai dấu chấm.
           Phần giữa ghi hạn dùng. Kẻ gian sửa đúng một chữ số đầu, từ một thành chín, để mã sống tới năm hai nghìn hai trăm sáu mươi tư.
           Dịch vụ có nhận mã đó không, khi nó không hỏi lại cơ sở dữ liệu?""", focus=[1, 2, 2, 2]),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["mã mang được thông tin gì, ai đọc được", "phần đầu và phần thân chỉ được viết lại, ai cầm mã cũng đọc được"],
                  ["vì sao sửa một ký tự là lộ", "chữ ký tính trên đúng từng byte, chỉ máy chủ có khoá mới tính được"],
                  ["chữ ký đúng đã đủ chưa", "chưa: còn kiểm hạn dùng, người phát hành, người nhận, và lo chuyện thu hồi"],
                  ["mã bị lộ thì kẻ gian dùng được bao lâu", "đo thật: hạn 300 giây so với hạn 3 600 giây"]]),
           """Hôm nay ta trả lời bốn câu: mã mang thông tin gì và ai đọc được, vì sao sửa một ký tự là bị lộ. Vì sao chữ ký đúng vẫn chưa đủ, và khi mã bị lộ thì kẻ gian dùng được bao lâu."""),
    ], checks=[f"len({T}.split('.')) == 3", "alg.bnx_utc(9300819380)[:4] == '2264'",
               "alg.bnx_jwt_check(alg.bnx_jwt_tamper(), alg.bnx_jwt_rfc7515()[2], 'api-a', 1300819379) == 'chữ ký sai'"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① byte, bit và base64url", "1 <b>byte</b> gồm 8 <b>bit</b>, mỗi bit là 0 hoặc 1; base64url viết dãy byte bằng 64 ký tự an toàn cho đường dẫn; mỗi ký tự mang 6 bit, nên 3 byte (24 bit) thành 4 ký tự; dư 1 byte thành 2 ký tự, dư 2 byte thành 3 ký tự", "<code>abc</code> (3 byte) → <code>YWJj</code>"],
                  ["② JSON", "văn bản dạng khoá và giá trị", "<code>{\"iss\":\"joe\"}</code>"],
                  ["③ SHA256", "hàm băm: đầu vào dài bao nhiêu cũng ra 32 byte; đổi 1 ký tự là ra kết quả khác hẳn", "32 byte → 43 ký tự base64url"],
                  ["④ HMAC", "băm có trộn một khoá bí mật: không có khoá thì không tính được", "khoá 64 byte của ví dụ"],
                  ["⑤ giờ Unix", "số giây kể từ 0 giờ ngày 1/1/1970 theo giờ quốc tế", "1300819380 → 22/3/2011 18:43:00"],]),
           """Trước hết ta cần hiểu năm điều. Thứ nhất, một byte gồm tám bit. Cách viết cơ số sáu mươi tư cho đường dẫn cho mỗi ký tự mang sáu bit, nên ba byte thành bốn ký tự.
           Thứ hai, dữ liệu trong mã là các cặp tên và giá trị. Thứ ba, SHA256 là hàm băm, ra ba mươi hai byte. Thứ tư, HMAC là băm trộn khoá bí mật nên không có khoá thì không tính được. Thứ năm, thời điểm là số giây từ năm một nghìn chín trăm bảy mươi.""",
           introduces=["bnx_base64url", "bnx_hmac"]),
        st("""<p>Làm thử: phần đầu của ví dụ dài 30 byte, tức 10 nhóm 3 byte.</p>
$$10 \\cdot 4 = \\hl{40}\\ \\text{ký tự}$$""",
           """Làm thử, phần đầu của ví dụ dài ba mươi byte, tức mười nhóm ba byte, mỗi nhóm thành bốn ký tự nên ta được bốn mươi ký tự."""),
    ], checks=["alg.bnx_b64u(b'abc') == 'YWJj'", "len(alg.bnx_jwt_rfc7515()[0]) == 30", "alg.bnx_b64u_len(30) == 40",
               "len(alg.bnx_jwt_part(0)) == 40", "alg.bnx_b64u_len(32) == 43", "len(alg.bnx_jwt_rfc7515()[2]) == 64",
               "alg.bnx_utc(1300819380) == '2011-03-22 18:43:00'"])

    sym = sc("sym", "symbol", "Giải mã các từ của một JWT", [
        st(table(["từ trên màn hình", "nghĩa"],
                 [["JWT (JSON Web Token)", "mã ba phần: <b>đầu</b> . <b>thân</b> . <b>chữ ký</b>, mỗi phần viết bằng base64url"],
                  ["phần đầu (header)", "<code>alg</code>: thuật toán ký, ví dụ <code>HS256</code> = HMAC dùng SHA256; <code>typ</code>: loại mã, ở đây <code>JWT</code>"],
                  ["phần thân (payload)", "các trường: <code>iss</code> người phát hành, <code>sub</code> chủ thể, <code>aud</code> người nhận, <code>exp</code> hạn dùng, <code>iat</code> lúc cấp"],
                  ["chữ ký (signature)", "với HS256: HMAC của chuỗi “đầu.thân” bằng khoá bí mật của máy chủ (thuật toán khác ký bằng một khoá giữ kín, kiểm bằng một khoá công bố)"],
                  ["base64url", "base64 đổi <code>+</code> thành <code>-</code>, <code>/</code> thành <code>_</code>, bỏ dấu <code>=</code> ở cuối"]]),
           """Mã này có ba phần nối bằng dấu chấm: đầu, thân và chữ ký. Phần đầu ghi thuật toán ký và loại mã, phần thân ghi người phát hành, chủ thể, người nhận, hạn dùng và lúc cấp.
           Chữ ký là HMAC của chuỗi đầu chấm thân, tính bằng khoá bí mật của máy chủ.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"]),
    ], checks=["alg.bnx_b64u(bytes([251, 255])) == '-_8'", "'=' not in alg.bnx_jwt_rfc_token()"])

    intu = sc("intuition", "intuition", "Hình dung: ai cũng đọc được, chỉ máy chủ ký được", [
        st(svg(1500, 470,
               box(40, 40, 400, 90, ["phần đầu", "eyJ0eXAi… (40 ký tự)"], C_BLUE, 24, True),
               box(550, 40, 400, 90, ["phần thân", "eyJpc3Mi… (94 ký tự)"], C_AMBER, 24, True),
               box(1060, 40, 400, 90, ["chữ ký", "dBjftJeZ… (43 ký tự)"], C_GREEN, 24, True),
               txt(495, 95, ".", 40, bold=True), txt(1005, 95, ".", 40, bold=True),
               box(380, 260, 520, 100, ["HMAC SHA256", "của “đầu.thân” với khoá k"], C_PURPLE, 24, True),
               box(1000, 260, 420, 100, ["khoá k (64 byte)", "chỉ máy chủ giữ"], C_RED, 24, True),
               arrow(240, 135, 470, 255, "#2a78d6"), arrow(750, 135, 700, 255, "#d97706"),
               arrow(995, 310, 905, 310, "#dc2626"), arrow(880, 255, 1180, 135, "#16a34a"), txt(1110, 235, "ra chữ ký", 22, "start", "#16a34a"),
               txt(750, 430, "Ai cầm mã cũng giải được phần đầu và phần thân; không có k thì không làm ra chữ ký đúng", 24, "middle", "#1f2937", True)),
           """Phần đầu và phần thân chỉ được viết lại bằng cơ số sáu mươi tư. Máy chủ ghép hai phần bằng dấu chấm rồi tính HMAC với khoá k mà chỉ nó giữ, nên ai cầm mã cũng đọc được phần thân nhưng không làm ra được chữ ký đúng."""),
        st(svg(1500, 470,
               box(30, 170, 250, 110, ["mã gửi tới", "đầu.thân.chữ ký"], C_BLUE, 24, True),
               box(360, 40, 330, 90, "① thuật toán = HS256?", C_GRAY, 24),
               box(360, 180, 330, 90, "② tính lại chữ ký, so", C_PURPLE, 24),
               box(360, 320, 330, 90, "③ bây giờ trước exp?", C_AMBER, 24),
               box(780, 180, 330, 90, "④ đúng iss và aud?", C_BLUE, 24),
               box(1200, 60, 260, 90, "nhận", C_GREEN, 26, True),
               box(1200, 300, 260, 90, ["từ chối", "(401)"], C_RED, 26, True),
               arrow(280, 200, 355, 90), arrow(525, 135, 525, 175), arrow(525, 275, 525, 315),
               arrow(695, 355, 775, 245), arrow(1115, 200, 1195, 110, "#16a34a"),
               arrow(1115, 250, 1195, 330, "#dc2626"), txt(1140, 350, "sai một cửa", 22, "end", "#dc2626"),
               txt(750, 455, "Sai ở cửa nào cũng từ chối ngay; chữ ký sai thì khỏi đọc phần thân", 24, "middle", "#1f2937", True)),
           """Ở phía nhận, dịch vụ đi qua bốn cửa. Một, thuật toán phải đúng thứ máy chủ chọn sẵn. Hai, tính lại chữ ký và so với chữ ký gửi kèm.
           Ba, bây giờ phải trước hạn dùng. Bốn, người phát hành và người nhận phải đúng, và sai một cửa là từ chối với mã bốn trăm lẻ một, nghĩa là chưa xác thực được người gọi.""",
           ),
    ], checks=["len(alg.bnx_jwt_part(1)) == 94", "len(alg.bnx_jwt_part(2)) == 43", "alg.bnx_jwt_part(0).startswith('eyJ0eXAi')",
               "alg.bnx_jwt_part(1).startswith('eyJpc3Mi')", "alg.bnx_jwt_part(2).startswith('dBjftJeZ')"])

    form = sc("formula", "formula", "Suy ra từng bước: ký và kiểm một JWT", [
        st("""<p><b>Bước 1.</b> Mã nằm trong điện thoại của khách, nên ai cũng có thể sửa nó. Cần một dấu mà <b>chỉ máy chủ</b> làm ra được:
chữ ký = HMAC(k, “đầu.thân”).</p>
$$\\text{sửa } 1300819380 \\to 9300819380 \\;\\Rightarrow\\; \\text{phần thân đổi} \\;\\Rightarrow\\; \\text{chữ ký đúng đổi theo}$$""",
           """Bước một, vì mã nằm trong điện thoại của khách nên ai cũng sửa được. Ta cần một dấu chỉ máy chủ làm ra được, là HMAC của chuỗi đầu chấm thân với khoá k, và đổi một chữ số của hạn dùng thì chữ ký đúng cũng đổi theo.""", clear=True),
        st("""<p><b>Bước 2.</b> Ký đúng <b>chuỗi đã viết lại</b> “đầu.thân”, không ký JSON đã đọc ra, vì cùng một nội dung có thể viết khác khoảng trắng hay thứ tự trường.</p>
<span class='note'>Làm thử: phần thân của ví dụ có cả ký tự xuống dòng \\r\\n, vẫn ký được nguyên văn.</span>""",
           """Bước hai, ta ký đúng chuỗi đã viết lại, không ký nội dung đã đọc ra, vì cùng nội dung có thể viết khác khoảng trắng hay thứ tự trường. Phần thân của ví dụ có cả ký tự xuống dòng, vẫn ký nguyên văn."""),
        st("""<p><b>Bước 3.</b> Phía nhận <b>tính lại</b> chữ ký bằng k và so với chữ ký gửi kèm. Thuật toán do máy chủ <b>cố định</b> là HS256, không đọc theo trường <code>alg</code> của mã gửi tới.</p>
<span class='note'>Làm thử: mã ghi <code>alg</code> = <code>none</code> bị loại ngay ở cửa ①.</span>""",
           """Bước ba, phía nhận tính lại chữ ký bằng khoá k rồi so với chữ ký gửi kèm. Thuật toán do máy chủ cố định, vì nếu đọc theo mã thì kẻ gian tự chọn, nên mã ghi thuật toán là không có gì bị loại ở cửa thứ nhất.""", clear=True),
        st("""<p><b>Bước 4.</b> Chữ ký đúng chỉ chứng minh “không ai sửa”. Mã cũ vẫn có chữ ký đúng mãi, nên phải kiểm <b>hạn dùng</b>: chỉ nhận khi bây giờ &lt; <code>exp</code>.</p>
<span class='note'>Làm thử: exp = 1300819380; lúc 1300819379 thì nhận, lúc 1300819380 thì từ chối.</span>""",
           """Bước bốn, chữ ký đúng chỉ chứng minh không ai sửa mã. Mã cũ vẫn có chữ ký đúng mãi, nên phải kiểm hạn dùng: chỉ nhận khi bây giờ còn trước hạn.
           Làm thử, trước hạn một giây thì nhận, đúng giây hết hạn thì từ chối."""),
        st("""<p><b>Bước 5.</b> Mã cấp cho dịch vụ này không được dùng ở dịch vụ khác: kiểm <code>iss</code> (ai phát hành) và <code>aud</code> (cấp cho ai; <code>aud</code> có thể là một danh sách tên, khi đó kiểm tên mình có trong danh sách, RFC 7519 mục 4.1.3).
Mã tự mang thông tin nên <b>không hỏi ai</b> khi kiểm, vì vậy khó thu hồi: dùng <b>hạn ngắn</b> và <b>mã làm mới</b>.</p>
<p class='note'><b>Mã làm mới</b> (refresh token): một mã thứ hai, sống lâu hơn, chỉ dùng để xin mã mới khi mã đang dùng hết hạn; nơi cấp mã có thể thu hồi nó.</p>
<p>Làm thử (số minh hoạ): hạn 300 giây, mã lộ ở giây 60.</p>
$$300 - 60 = \\hl{240}\\ \\text{giây kẻ gian còn dùng được}$$""",
           """Bước năm, mã cấp cho dịch vụ này không được dùng ở dịch vụ khác, nên kiểm thêm người phát hành và người nhận.
           Vì mã tự mang thông tin nên khó thu hồi giữa chừng. Cách chữa là hạn ngắn cộng mã làm mới, tức một mã thứ hai chỉ để xin mã mới khi mã đang dùng hết hạn. Làm thử, hạn ba trăm giây, mã lộ ở giây sáu mươi thì kẻ gian dùng được hai trăm bốn mươi giây.""", clear=True),
    ], checks=["alg.bnx_exp_ok(1300819380, 1300819379)", "not alg.bnx_exp_ok(1300819380, 1300819380)",
               "alg.bnx_risk_window(300, 60) == 240",
               "alg.bnx_jwt_sign(alg.bnx_jwt_rfc7515()[0], alg.bnx_jwt_rfc7515()[1].replace(b'1300', b'9300'), alg.bnx_jwt_rfc7515()[2]).split('.')[2] != alg.bnx_jwt_part(2)",
               "b'\\r\\n' in alg.bnx_jwt_rfc7515()[1]",
               "alg.bnx_jwt_check(alg.bnx_b64u(b'{\"alg\":\"none\"}') + '.' + alg.bnx_jwt_part(1) + '.', alg.bnx_jwt_rfc7515()[2], 'api-a', 0) == 'thuật toán lạ'"])

    ex = sc("example", "example", "Ví dụ của RFC 7515, từng phép tính", [
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>import base64, hmac, hashlib, json</code>", "nạp các thư viện có sẵn: viết base64, tính HMAC, băm, đọc JSON"],
                  ["<code>b'{\"iss\":\"joe\"}'</code>", "dãy byte: chữ <code>b</code> đứng trước dấu nháy"],
                  ["<code>.rstrip(b\"=\")</code>, <code>.decode()</code>", "bỏ các dấu <code>=</code> ở cuối; đổi dãy byte thành chữ"],
                  ["<code>\"=\" * (-len(s) % 4)</code>", "lặp dấu <code>=</code> cho đủ bội số của 4"],
                  ["<code>ma.split(\".\")</code>", "cắt chuỗi ở mỗi dấu chấm thành danh sách các phần"],
                  ["<code>hmac.new(k, vao.encode(), hashlib.sha256).digest()</code>", "tính HMAC bằng khoá <code>k</code>, kết quả 32 byte"]])
           + """<p class="note"><b>RFC</b>: bản chuẩn kỹ thuật công khai cho mạng máy tính, mỗi chuẩn một số; RFC 7515 mô tả chữ ký của dữ liệu JSON.</p>""",
           """Ta tính lại ví dụ trong RFC, một bản chuẩn kỹ thuật công khai. Mã Python sắp tới có vài cách viết mới, nên ta giải nghĩa trước. Chữ b trước dấu nháy là dãy byte, hai lệnh sau bỏ dấu bằng và đổi byte thành chữ.
           Dòng nhân thêm dấu bằng cho đủ bội số bốn, lệnh cắt chuỗi ở mỗi dấu chấm, lệnh cuối tính HMAC bằng khoá k.""", clear=True),
        st(code(PY_DATA, "Chương trình Python: dữ liệu của RFC 7515 Phụ lục A.1"),
           """Ta tính lại ví dụ trong RFC bảy nghìn năm trăm mười lăm, phụ lục A một. Hai hàm đầu viết và đọc theo cơ số sáu mươi tư cho đường dẫn.
           Phần đầu và phần thân chép đúng từng byte, và khoá k sáu mươi tư byte đọc ra từ chuỗi trong RFC.""",
           focus=[1, ["2.2", "2.3", "2.4", "2.5"], ["2.3", "2.5"], ["2.6", "2.7", "2.8"], ["2.9", "2.10"]], clear=True),
        st("""<p>Phần đầu dài 30 byte, là 10 nhóm 3 byte.</p>
$$① \\; 10 \\cdot 4 = \\hl{40}\\ \\text{ký tự: eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9}$$""",
           """Phép tính thứ nhất. Phần đầu dài ba mươi byte, là mười nhóm ba byte, nên viết lại thành bốn mươi ký tự, bắt đầu bằng e y J không."""),
        st(code(PY_SIGN, "Ký: HMAC SHA256 của “đầu.thân”"),
           """Đây là hàm ký, nó ghép phần đầu và phần thân đã viết lại bằng một dấu chấm, gọi là chuỗi vào. Rồi nó tính HMAC với SHA256 của chuỗi vào bằng khoá k, nối chữ ký đã viết lại vào sau và in từng phần.""",
           focus=["2.1", "2.2", "2.3", ["2.4", "2.5", "2.6", "2.7"]], clear=True),
        st(out(OUT_SIGN),
           """Kết quả chạy thật in ba dòng, dòng giữa là phần thân bị cắt bớt vì dài chín mươi tư ký tự, và dòng cuối là chữ ký."""),
        st("""<p>Phần thân dài 70 byte = 23 nhóm 3 byte, dư 1 byte (viết thành 2 ký tự).</p>
$$② \\; 23 \\cdot 4 + 2 = \\hl{94}\\ \\text{ký tự}$$""",
           """Phép tính thứ hai. Phần thân dài bảy mươi byte, là hai mươi ba nhóm ba byte và dư một byte. Vì byte dư viết thành hai ký tự, ta được chín mươi tư ký tự.""",
           clear=True),
        st("""$$③ \\; \\text{HMAC: 32 byte} = 10 \\cdot 3 + 2 \\;\\Rightarrow\\; 10 \\cdot 4 + 3 = \\hlg{43}\\ \\text{ký tự}$$
<p>Chữ ký <code>dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk</code> <b class="green">khớp từng ký tự</b> với RFC.</p>""",
           """Phép tính thứ ba: HMAC cho ba mươi hai byte, là mười nhóm ba byte dư hai byte, nên chữ ký dài bốn mươi ba ký tự và khớp từng ký tự với chữ ký in trong RFC."""),
        st("""$$④ \\; 1300819380 \\to 9300819380 \\;\\Rightarrow\\; \\text{chữ ký tính lại} \\ne \\text{dBjftJeZ…} \\;\\Rightarrow\\; \\hl{\\text{chữ ký sai}}$$""",
           """Phép tính thứ tư. Sửa chữ số đầu của hạn dùng từ một thành chín thì phần thân đổi, nên chữ ký tính lại khác hẳn chữ ký ở phép ba, và dịch vụ báo chữ ký sai.""",
           ),
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>from datetime import datetime, timezone</code>", "nạp hai tên từ thư viện ngày giờ; <code>timezone.utc</code> là giờ quốc tế"],
                  ["<code>ma.split(\".\")[1]</code>", "cắt mã thành danh sách các phần rồi lấy phần số 1; ngoặc vuông đếm từ 0, nên đó là phần thứ hai, phần thân"],
                  ["<code>json.loads(unb64u(t))</code>", "<code>unb64u</code> đổi base64url về byte; <code>json.loads</code> đọc chuỗi JSON thành từ điển, tức bảng tên và giá trị"],
                  ["<code>datetime.fromtimestamp(n, timezone.utc)</code>, <code>time.time()</code>", "đổi số giây Unix thành ngày giờ quốc tế; <code>time.time()</code> cho số giây của đồng hồ máy lúc này"]]),
           """Đoạn đọc phần thân dùng vài cách viết mới. Ngoặc vuông số một lấy phần thứ hai của danh sách, vì đếm từ không. Hàm đọc JSON biến chuỗi thành từ điển, và hàm thời gian cho giây hiện tại của đồng hồ máy.""",
           clear=True),
        st(code(PY_READ, "Đọc phần thân mà không cần khoá"),
           """Bây giờ ta đọc phần thân mà không cần khoá, chỉ cần tách chuỗi mã ở dấu chấm rồi đọc ngược phần thứ hai. Dòng cuối đổi số giây của hạn dùng sang ngày giờ quốc tế.""", focus=["2.3", "2.4"], clear=True),
        st(out(OUT_READ),
           """Kết quả chạy thật: dòng đầu là toàn bộ phần thân, ai cũng đọc được, còn dòng hai là hạn dùng, ngày hai mươi hai tháng ba năm hai nghìn mười một."""),
        st("""$$⑤ \\; 1300819380 \\to \\text{22/3/2011 18:43:00, sớm hơn hôm nay} \\;\\Rightarrow\\; \\hl{\\text{hết hạn}}$$""",
           """Phép tính thứ năm, hạn dùng rơi vào năm hai nghìn mười một, sớm hơn hôm nay rất xa, nên mã của RFC dù chữ ký đúng vẫn bị từ chối vì hết hạn."""),
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>d, t, s = ma.split(\".\")</code>", "cắt mã thành ba phần rồi gán lần lượt vào ba biến <code>d</code>, <code>t</code>, <code>s</code>"],
                  ["<code>json.loads(chuỗi)</code>", "đọc một chuỗi JSON thành từ điển; <code>c[\"exp\"]</code> lấy giá trị trường <code>exp</code>"],
                  ["<code>c.get(\"iss\")</code>", "lấy trường <code>iss</code>; không có thì cho <code>None</code>, nghĩa là rỗng"],
                  ["<code>hmac.compare_digest(a, b)</code>", "so hai chuỗi bằng <b>hàm thời gian hằng</b>: luôn so hết chuỗi, không dừng ở ký tự sai đầu tiên; dùng thay cho <code>==</code>"]]),
           """Hàm kiểm dùng thêm vài cách viết, nên ta giải nghĩa trước. Dòng đầu cắt mã thành ba phần, hàm đọc JSON biến chuỗi thành từ điển, và lệnh lấy trường cho kết quả rỗng khi thiếu. Hàm so thời gian hằng luôn so hết chuỗi.""",
           clear=True),
        st(code(PY_CHECK, "Ráp bốn cửa thành hàm kiểm"),
           """Ta ráp bốn cửa thành một hàm kiểm: thuật toán đúng, chữ ký khớp khi so bằng hàm thời gian hằng, chưa hết hạn, và đúng người phát hành, người nhận. Chỉ khi qua cả bốn cửa thì mã mới được nhận.""",
           focus=["2.1", "2.3", ["2.4", "2.5", "2.6"], ["2.7", "2.8", "2.9"], ["2.10", "2.11"], "2.12"], clear=True),
        st(code(PY_CASES, "Năm ca thử"),
           """Năm ca thử như sau: ca một là mã RFC kiểm hôm nay, ca hai là mã bị sửa một chữ số mà giữ chữ ký cũ, ca ba ghi thuật toán là không có gì.
           Ca bốn và ca năm là mã mới cho dịch vụ api-a, kiểm ở API A rồi ở API B.""",
           focus=[0, ["2.1", "2.2"], ["2.3", "2.4", "2.5"], ["2.6", "2.7"], ["2.8", "2.9", "2.10"]], clear=True),
        st(out(OUT_CASES),
           """Kết quả đúng thứ tự: mã RFC hết hạn, mã bị sửa thì chữ ký sai, mã không có thuật toán bị loại. Mã mới được nhận ở API A nhưng sang API B thì bị từ chối vì sai người nhận.""",
           focus=[0, "2.1", "2.2", "2.3", ["2.4", "2.5"]], clear=True),
    ], checks=["alg.bnx_b64u_len(30) == 40", "alg.bnx_jwt_part(0) == 'eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9'",
               "len(alg.bnx_jwt_rfc7515()[1]) == 70 and alg.bnx_b64u_len(70) == 23 * 4 + 2 == 94",
               "alg.bnx_b64u_len(32) == 10 * 4 + 3 == 43",
               "alg.bnx_jwt_part(2) == 'dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk'",
               "alg.bnx_jwt_tamper().split('.')[1] != alg.bnx_jwt_part(1) and alg.bnx_jwt_tamper().split('.')[2] == alg.bnx_jwt_part(2)",
               "alg.bnx_utc(1300819380) == '2011-03-22 18:43:00'",
               "alg.bnx_jwt_cases(__import__('time').time()) == ['hết hạn', 'chữ ký sai', 'thuật toán lạ', 'nhận', 'sai người phát hành/nhận']"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: công cụ dòng lệnh OpenSSL", [
        st(table(["lệnh", "nghĩa"],
                 [["<code>printf %s … &gt; vao.txt</code>", "in chuỗi đã cho, ghi vào tệp <code>vao.txt</code>"],
                  ["<code>openssl dgst -sha256 -mac HMAC -macopt hexkey:…</code>", "tính HMAC-SHA256 của tệp, khoá cho dưới dạng thập lục phân"],
                  ["<code>… | openssl base64 -A | tr '+/' '-_' | tr -d '='</code>", "dấu <code>|</code> chuyển đầu ra sang lệnh sau; đổi sang base64 (<code>-A</code>: viết liền một dòng), thay <code>+/</code> bằng <code>-_</code>, bỏ <code>=</code>"],
                  ["<code>\\</code> cuối dòng", "nối dòng này với dòng sau thành một lệnh duy nhất (lệnh dài nên ngắt dòng)"],
                  ["<code>-binary</code>, <code>echo</code>", "<code>-binary</code>: in byte thô thay vì chữ, để lệnh sau đổi sang base64; <code>echo</code> không kèm gì: xuống dòng"],
                  ["<code>date -u -d @1300819380 '+%F %T'</code>", "đổi số giây Unix thành ngày giờ quốc tế; chuỗi <code>'+%F %T'</code> đặt mẫu in: <code>%F</code> năm-tháng-ngày, <code>%T</code> giờ:phút:giây"]]),
           """Công cụ dòng lệnh có vài cách viết mới, nên ta giải nghĩa trước. Lệnh đầu ghi chuỗi vào tệp, lệnh thứ hai tính HMAC với khoá ở thập lục phân, dấu gạch đứng chuyển đầu ra sang lệnh sau.
           Dấu gạch ngược cuối dòng nối lệnh dài, tuỳ chọn nhị phân in byte thô, và lệnh ngày đổi số giây thành ngày giờ theo mẫu in.""", clear=True),
        st(code(SH_OPENSSL, "Đường khác: tính lại bằng openssl (Git Bash)"),
           """Ta kiểm bằng một đường khác, là công cụ dòng lệnh mật mã, không dùng Python. Ba dòng đầu ghi chuỗi đầu chấm thân vào một tệp. Lệnh tiếp theo tính HMAC với SHA256 bằng khoá k ở thập lục phân, rồi đổi kết quả sang cơ số sáu mươi tư.""",
           focus=[0, ["2.1", "2.2", "2.3"], ["2.4", "2.5", "2.6"], "2.7", "2.9"], clear=True),
        st(out(OUT_OPENSSL),
           """Chữ ký giống hệt chữ ký Python và chữ ký in trong RFC, nên hai đường cho cùng kết quả, ngày giờ cũng khớp.""", clear=True),
    ], checks=["alg.bnx_jwt_part(2) == 'dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk'", "alg.bnx_jwt_rfc7515()[2].hex()[:6] == '032335'",
               "alg.bnx_utc(1300819380) == '2011-03-22 18:43:00'"])

    quymo = sc("quymo", "example", "Khi mã bị lộ: kẻ gian dùng được bao lâu, và ứng dụng xin mã mới bao nhiêu lần", [
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>b'…%d…' % han</code>", "thay chỗ <code>%d</code> bằng số <code>han</code>"],
                  ["<code>sum(kiem(…) == \"nhận\" for t in range(60, 4001))</code>", "đếm số giây <code>t</code> từ 60 đến 4000 mà mã còn được nhận"],
                  ["<code>u * 3600 // 300</code>", "<code>//</code> là chia lấy phần nguyên"]]),
           """Khối đo dùng ba cách viết mới nên ta giải nghĩa trước: thay số vào chỗ định dạng, đếm số giây mà mã còn được nhận, và phép chia lấy phần nguyên.""", clear=True),
        st(code(SCALE_PY, "Đo thật: kẻ gian lấy mã ở giây 60, mỗi giây thử một lần tới giây 4000"),
           """Ta đo theo thời gian, dùng lại hai hàm đó. Ta cấp mã hạn ba trăm giây rồi ba nghìn sáu trăm giây, kẻ gian lấy được mã ở giây sáu mươi. Hàm đếm cho biết mã còn được nhận bao nhiêu giây, còn hai dòng cuối tính số mã mới mỗi giờ.""",
           clear=True),
        st(out(SCALE_OUT) + table(["hạn dùng", "kẻ gian dùng được", "mã mới mỗi giờ: 1 000 người", "1 000 000 người (×1 000)"],
                                   [["300 giây", "240 lần", "12 000", "12 000 000"], ["3 600 giây", "3 540 lần", "1 000", "1 000 000"]])
           + """<p class="note">Số người dùng và nhịp mỗi người xin mã mới đúng một lần khi mã hết hạn là số minh hoạ.</p>""",
           """Hạn ba trăm giây thì kẻ gian dùng được hai trăm bốn mươi lần, hạn ba nghìn sáu trăm giây thì ba nghìn năm trăm bốn mươi lần, gấp hơn mười bốn lần.
           Đổi lại, hạn ngắn làm mỗi người xin mã mới mười hai lần mỗi giờ thay vì một.""",
           clear=True),
        st(table(["cách", "được", "mất", "khi nào chọn"],
                 [["hạn dài (3 600 giây)", "ít mã mới, máy cấp mã nhàn", "mã lộ thì hở lâu", "dịch vụ rủi ro thấp, ít người dùng"],
                  ["hạn ngắn + mã làm mới", "hở ngắn; thu hồi ở nơi cấp mã", "tải xin mã mới nhân 12, máy cấp mã thành điểm nghẽn", "ngân hàng: lệnh chuyển tiền, nhiều người dùng"],
                  ["danh sách thu hồi tra mỗi lời gọi", "chặn ngay", "mỗi lời gọi hỏi một kho chung: mất ưu điểm tự mang thông tin", "cần chặn tức thì (mất điện thoại, nghi gian lận)"]]),
           """Hạn dài tiện nhưng mã lộ thì hở lâu, hạn ngắn kèm mã làm mới thu hẹp khoảng hở nhưng nhân tải lên máy cấp mã mười hai lần.
           Danh sách thu hồi chặn được ngay nhưng mất ưu điểm tự mang thông tin, nên chỉ dùng khi cần chặn tức thì.""",
           clear=True),
    ], checks=["[alg.bnx_l03_exposed(h, 60) for h in (300, 3600)] == [240, 3540]",
               "alg.bnx_risk_window(300, 60) == 240 and alg.bnx_risk_window(3600, 60) == 3540",
               "[alg.bnx_l03_refresh_per_hour(u, 300) for u in (1000, 1000000)] == [12000, 12000000] and alg.bnx_l03_refresh_per_hour(1000000, 3600) == 1000000",
               "1000000 // 1000 == 1000 and 3540 // 240 == 14"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Để số căn cước, số dư vào phần thân vì nghĩ mã đã được “mã hoá”.
Phần thân chỉ được <b class="red">viết lại</b> bằng base64url: ở phép ⑤, ta đọc được toàn bộ mà không cần khoá.
<br><span class="note">Cách chữa: phần thân chỉ chứa mã định danh và quyền; thông tin nhạy cảm để ở máy chủ.</span></div>""",
           """Lỗi thứ nhất, của người mới, là để số căn cước hay số dư vào phần thân vì nghĩ mã đã được mã hoá. Phần thân chỉ được viết lại, ta đã đọc được không cần khoá, nên chỉ để mã định danh và quyền.""",
           clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Tin trường <code>alg</code></b> của mã gửi tới.
Kẻ gian ghi <code>none</code> để bỏ chữ ký. Hoặc: có thuật toán ký bằng <b>một cặp khoá</b> (khoá riêng giữ kín để ký, khoá công khai phát cho mọi người để kiểm); kẻ gian đổi sang HS256 rồi lấy <b>khoá công khai</b> làm khoá HMAC.
<br><span class="note">Cách chữa: máy chủ cố định danh sách thuật toán (RFC 8725 mục 3.1); ca thử ③ bị loại.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là tin trường thuật toán trong mã gửi tới. Kẻ gian ghi không có thuật toán để bỏ chữ ký. Hoặc, nếu ký bằng cặp khoá riêng và công khai, thì đổi sang HMAC và lấy khoá công khai làm khoá bí mật. Vì vậy máy chủ phải cố định danh sách thuật toán.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> So chữ ký bằng <code>==</code>. Phép so dừng ở ký tự sai đầu tiên, nên thời gian trả lời lộ ra đã đoán đúng bao nhiêu ký tự.
<br><span class="note">Về nguyên tắc (qua mạng thật, độ trễ nhiễu làm việc đo khó hơn nhiều), đoán lần lượt từng ký tự: tối đa $64 \\cdot 43 = 2752$ giá trị phải thử, mỗi giá trị đo lặp nhiều lần, thay vì đoán cả chuỗi. Cách chữa: <code>hmac.compare_digest</code>.</span></div>""",
           """Lỗi thứ ba, của người đã đi làm, là so chữ ký bằng phép so thường. Phép so dừng ở ký tự sai đầu tiên, nên thời gian trả lời lộ ra đã đoán đúng bao nhiêu ký tự. Về nguyên tắc kẻ gian đoán từng ký tự, tối đa hai nghìn bảy trăm năm mươi hai giá trị, dù qua mạng thật khó đo hơn nhiều. Cách chữa là hàm so thời gian hằng.""", clear=True),
    ], checks=["64 * len(alg.bnx_jwt_part(2)) == 2752", "'joe' in alg.bnx_unb64u(alg.bnx_jwt_part(1)).decode()",
               "alg.bnx_jwt_cases(0)[2] == 'thuật toán lạ'"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Phần đầu <code>{\"alg\":\"HS256\",\"typ\":\"JWT\"}</code> dài 27 byte. Viết bằng base64url dài bao nhiêu ký tự?"],
                  ["2", "Mã có exp = 1300819380, máy chủ không cộng thêm khoảng lệch đồng hồ (độ chênh cho phép giữa đồng hồ hai máy). Lúc 1300819379 và lúc 1300819380: nhận hay từ chối?"],
                  ["3", "Quyết định (số minh hoạ): mã truy cập hạn 3600 giây, hay hạn 300 giây kèm mã làm mới? Giả sử mã lộ ở giây 60."]]),
           """Đến lượt bạn, ba câu trên màn hình. Câu ba chọn hạn dài hay hạn ngắn kèm mã làm mới. Hãy dừng video và làm từng câu ra giấy.""",
           pause=25),
        st("""<p>Câu 1: 27 byte = 9 nhóm 3 byte, không dư.</p>
$$9 \\cdot 4 = \\hlg{36}\\ \\text{ký tự}$$""",
           """Đáp án câu một. Hai mươi bảy byte là chín nhóm ba byte, không dư, nên viết lại thành ba mươi sáu ký tự."""),
        st("""<p>Câu 2: chỉ nhận khi bây giờ &lt; exp.</p>
$$1300819379 \\text{ trước } 1300819380 \\Rightarrow \\hlg{\\text{nhận}}; \\quad 1300819380 \\text{ không trước chính nó} \\Rightarrow \\hl{\\text{từ chối}}$$""",
           """Đáp án câu hai. Chỉ nhận khi bây giờ còn trước hạn. Trước một giây thì nhận. Đúng giây hết hạn thì điều kiện sai, nên từ chối."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["hạn 3600 giây", "ứng dụng ít phải xin mã mới", "lộ ở giây 60: kẻ gian dùng thêm 3600 − 60 = 3540 giây"],
                  ["hạn 300 giây + mã làm mới", "lộ ở giây 60: chỉ còn 240 giây; mã làm mới thu hồi được ở máy chủ cấp mã", "ứng dụng xin mã mới 3600 : 300 = 12 lần mỗi giờ"],
                  ["danh sách thu hồi, tra mỗi lời gọi", "chặn được ngay", "mỗi lời gọi lại phải hỏi một kho chung: mất ưu điểm tự mang thông tin"]]),
           """Đáp án câu ba, hạn ba nghìn sáu trăm giây thì ít phải xin mã mới, nhưng mã lộ ở giây sáu mươi cho kẻ gian ba nghìn năm trăm bốn mươi giây. Hạn ba trăm giây kèm mã làm mới chỉ hở hai trăm bốn mươi giây, đổi lại xin mã mới mười hai lần mỗi giờ.""",
           focus=[0, "1.2", "1.3", "1.4"]),
    ], checks=["len(b'{\"alg\":\"HS256\",\"typ\":\"JWT\"}') == 27", "alg.bnx_b64u_len(27) == 36",
               "len(alg.bnx_b64u(b'{\"alg\":\"HS256\",\"typ\":\"JWT\"}')) == 36",
               "alg.bnx_exp_ok(1300819380, 1300819379) and not alg.bnx_exp_ok(1300819380, 1300819380)",
               "alg.bnx_risk_window(3600, 60) == 3540", "alg.bnx_risk_window(300, 60) == 240", "3600 // 300 == 12"])

    lab_pr = practice_scene(sc, "Tự làm: ký và kiểm một JWT HS256", practice_steps2(
        st, "BNX", "L03",
        """<p><b>Đề</b> (số minh hoạ): khoá <code>KHOA = b"khoa-lab-l03"</code>. Viết <code>mau.py</code> có ba hàm:</p>
<ol><li><code>b64u(b)</code>: base64url, bỏ dấu <code>=</code></li><li><code>ky(dau, than)</code>: ký HMAC-SHA256 của <code>đầu.thân</code>, trả mã ba phần</li>
<li><code>kiem(ma, aud, bay_gio)</code>: tính lại chữ ký rồi kiểm hạn, người nhận; trả <code>chu ky sai</code>, <code>het han</code>, <code>sai nguoi nhan</code> hoặc <code>nhan</code></li></ol>
<p>Rồi chép đoạn thử trong <code>de.md</code> (in 5 dòng).</p>""",
        """Bây giờ tới phần bạn tự làm, gồm ba hàm. Một hàm viết lại bằng cơ số sáu mươi tư cho đường dẫn, một hàm ký bằng HMAC, và một hàm kiểm tính lại chữ ký rồi kiểm hạn dùng và người nhận.
        Sau đó chép đoạn thử có sẵn, chạy và so năm dòng kết quả, rồi dừng video để tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> làm đúng như hàm <code>ky</code> và <code>kiem</code> trong bài: so chữ ký bằng <code>hmac.compare_digest</code>; thêm lại <code>=</code> bằng <code>"=" * (-len(t) % 4)</code> trước khi giải mã phần thân; kiểm theo thứ tự chữ ký, hạn, người nhận.
Lời giải ở <code>labs/BNX/L03/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>""",
        """Nếu kẹt, làm đúng như hàm ký và hàm kiểm trong bài: so chữ ký bằng hàm thời gian hằng, và thêm lại dấu bằng cho đủ bội số bốn trước khi giải mã phần thân.
        Kiểm theo thứ tự chữ ký, hạn dùng, người nhận. Lời giải ở thư mục thực hành, chỉ mở sau khi tự thử.""", pause=240), "BNX", "L03")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("đầu.thân: ai cũng đọc", "HMAC với khoá k: chữ ký", "tính lại, so thời gian hằng", "kiểm exp, iss, aud", "hạn ngắn + mã làm mới"),
           """Tổng kết chuỗi logic. Phần đầu và phần thân ai cũng đọc được, còn chữ ký là HMAC với khoá k mà chỉ máy chủ giữ.
           Phía nhận tính lại chữ ký và so bằng hàm thời gian hằng, rồi kiểm hạn dùng, người phát hành, người nhận, và vì khó thu hồi nên mã cần hạn ngắn cùng mã làm mới."""),
        st("""<div class='box key'><b>Tư duy:</b> chữ ký chứng minh “không ai sửa”, không chứng minh “còn hiệu lực” và cũng không giấu gì cả.
Mỗi điều cần một phép kiểm riêng.</div>""",
           """Điều cần mang theo. Chữ ký chứng minh không ai sửa mã, nhưng không chứng minh mã còn hiệu lực, và cũng không giấu gì cả. Mỗi điều cần một phép kiểm riêng."""),
        st("""<p>Bài sau: ai được <b>cấp</b> mã, ai <b>kiểm</b> mã, và mã được làm những gì (phạm vi quyền).</p>""",
           """Ở bài bốn, ta xem ai được cấp mã, ai kiểm mã, và một mã được phép làm những việc gì, gọi là phạm vi quyền.""",
           forward_ref=True),
    ])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L03", "jwt_chu_ky_han_dung", "Bài 3 — JWT: mã truy cập tự mang thông tin, chữ ký HMAC và hạn dùng",
                  "curriculum/bnx.yaml L03; audit/bnx/verify_bnx.py L03; RFC 7515 Phụ lục A.1 (2015, ví dụ HS256); RFC 7519 mục 4.1 (2015); "
                  "RFC 7519 mục 4.1.3 (aud có thể là danh sách); RFC 8725 mục 2.1, 3.1 (2020, đọc 2026-11-11)",
                  ["Tách và giải mã ba phần của một JWT", "Tính lại chữ ký HS256 và phát hiện phần thân bị sửa",
                   "Kiểm hạn dùng, người phát hành và người nhận", "Nêu cách thu hồi khi mã tự mang thông tin",
                   "Đo số lần kẻ gian dùng được mã bị lộ với hạn 300 giây và 3 600 giây, và số mã mới mỗi giờ khi số người dùng tăng",
                   "Tự viết hàm ký và hàm kiểm một JWT HS256 rồi chạy năm ca thử"],
                  scenes,
                  assumes=["bnx_ma_bam", "bnx_thap_luc_phan"],
                  covers=[(1, "example"), (2, "example"), (3, "example"), (4, "formula"), (5, "quymo"), (6, "practice")])
