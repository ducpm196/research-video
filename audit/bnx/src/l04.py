from lib import *

# ── Mã hiện trên màn hình (chạy NGUYÊN VĂN: audit/bnx/screen/l04.yaml, audit/bnx/ver/l04.py) ──
HTTP_TOKEN = """
POST /token HTTP/1.1
Host: server.example.com
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&scope=payments:write
"""

JSON_TOKEN = """
{
  "access_token": "eyJ0eXAiOiJhdCtqd3QiLCJhbGciOiJ…",
  "token_type": "Bearer",
  "expires_in": 300,
  "scope": "payments:write"
}
"""

PY_RS = r'''
def kiem(c, can, toi, bay_gio, lech=60):
    # c: các trường của mã; chữ ký đã kiểm như bài 3
    aud = c["aud"] if isinstance(c["aud"], list) else [c["aud"]]
    if toi not in aud:
        return 401       # mã không cấp cho API này
    if bay_gio >= c["exp"] + lech:
        return 401       # hết hạn, đã cộng lệch đồng hồ
    if can not in c["scope"].split(" "):
        return 403       # biết ai gọi, nhưng thiếu quyền
    return 200
'''

PY_CASES = r'''
cap = 1000                        # giây cấp mã (iat)
doc = {"aud": "api-a", "exp": cap + 300, "scope": "accounts:read"}
ghi = {"aud": "api-a", "exp": cap + 300, "scope": "payments:write"}
print(kiem(doc, "payments:write", "api-a", cap + 10))
print(kiem(ghi, "payments:write", "api-b", cap + 10))
print(kiem(ghi, "payments:write", "api-a", cap + 359))
print(kiem(ghi, "payments:write", "api-a", cap + 360))
idt = {"aud": "app-di-dong", "exp": cap + 300, "nonce": "n-0S6"}
print(kiem(idt, "payments:write", "api-a", cap + 10))
'''

PY_COUNT = r'''
nhan = [g for g in range(0, 1000)
        if kiem(ghi, "payments:write", "api-a", cap + g) == 200]
print(len(nhan), nhan[0], nhan[-1])
'''

# Đầu ra thật (chạy 2026-11-11, .venv Python 3.13)
OUT_CASES = """
403
401
200
401
401
"""
OUT_COUNT = """
360 0 359
"""

# Từ ngoại KHÔNG đạt dò phát âm (BRIEF §6: JWT 0/8, OAuth 3/8, TLS 4/8; OpenID chưa dò): lời đọc tiếng Việt, tên gốc chỉ hiện trên màn hình
SPOKEN = {"OAuth 2.0": "chuẩn ủy quyền", "OpenID Connect": "chuẩn đăng nhập mở", "JWT": "mã Token tự mang thông tin"}

C = "alg.bnx_oauth_case"


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


def _seq(cols, rows, h):
    """Sơ đồ tuần tự: cols = [(nhãn, màu)], rows = [(từ cột, tới cột, nhãn)]."""
    xs = [190 + i * (1120 // (len(cols) - 1)) for i in range(len(cols))]
    parts = []
    for (lab, col), x in zip(cols, xs):
        parts.append(box(x - 165, 15, 330, 90, lab, col, 24, True))
        parts.append(f'<line x1="{x}" y1="105" x2="{x}" y2="{h - 10}" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 6"/>')
    for i, (a, b, lab) in enumerate(rows):
        y = 165 + i * 66
        x1, x2 = xs[a], xs[b]
        d = 1 if x2 > x1 else -1
        parts.append(arrow(x1 + 8 * d, y, x2 - 12 * d, y, "#334155"))
        # nhãn đặt giữa hai đường đời sát đích, để đường đứt nét ở giữa không cắt qua chữ
        near = xs[b - d] if abs(b - a) > 1 else x1
        lo, hi = min(near, x2), max(near, x2)
        parts.append(txt((lo + hi) // 2, y - 12, lab, 22, "middle", "#1f2937"))
    return svg(1500, h, *parts)


def build():
    hook = sc("hook", "hook", "Có nên đưa mật khẩu ngân hàng cho ứng dụng khác?", [
        st("""<p>Một ứng dụng quản lý chi tiêu muốn đọc lịch sử giao dịch của khách qua Open API của ngân hàng (Thông tư 64/2024/TT-NHNN về Open API).</p>
<div class="box key">Cách tệ: khách đưa <b>mật khẩu</b> cho ứng dụng đó. Ứng dụng làm được <b>mọi việc</b>, kể cả chuyển tiền, và khách không rút lại được nếu không đổi mật khẩu.</div>""",
           """Chào bạn, một ứng dụng quản lý chi tiêu muốn đọc lịch sử giao dịch của khách qua giao diện lập trình mở của ngân hàng.
           Cách tệ nhất là khách đưa mật khẩu cho ứng dụng đó. Khi ấy ứng dụng làm được mọi việc, kể cả chuyển tiền, và khách không rút lại được nếu không đổi mật khẩu.""",
           focus=[1, 2, 2]),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["ai cấp mã, ai kiểm mã", "bốn vai của OAuth 2.0: máy chủ ủy quyền cấp, máy chủ tài nguyên kiểm"],
                  ["mã được làm gì", "phạm vi quyền: mã <code>accounts:read</code> gọi lệnh cần <code>payments:write</code> bị <b>403</b>"],
                  ["đăng nhập thì sao", "OpenID Connect thêm <b>mã định danh</b>; không dùng nó để gọi API"]]),
           """Hôm nay ta trả lời ba câu. Ai cấp mã và ai kiểm mã, theo bốn vai của OAuth 2.0.
           Mã được làm những gì, gọi là phạm vi quyền: mã chỉ được đọc tài khoản mà gọi lệnh ghi thanh toán sẽ bị từ chối bốn trăm lẻ ba.
           Và đăng nhập khác ủy quyền ra sao, với mã định danh của OpenID Connect.""", focus=[0, "1.2", "1.3", "1.4"]),
    ], checks=[f"{C}('accounts:read', 'api-a', 'payments:write', 'api-a', 10) == 403"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① mã truy cập ở bài 3", "ba phần đầu.thân.chữ ký; phía nhận kiểm chữ ký, hạn <code>exp</code>, người nhận <code>aud</code>", "hạn 1300819380 là năm 2011: hết hạn"],
                  ["② 401 và 403", "401: mã không dùng được ở đây (thiếu, sai, hết hạn); 403: mã tốt nhưng thiếu quyền (RFC 6750 mục 3.1)", "mã hết hạn → 401; thiếu quyền → 403"],
                  ["③ chuyển hướng", "máy chủ bảo trình duyệt mở một địa chỉ khác, kèm tham số", "ứng dụng → trang đăng nhập của ngân hàng"],
                  ["④ PKCE (băm chuỗi bí mật)", "mỗi lần đăng nhập, ứng dụng sinh một chuỗi ngẫu nhiên giữ kín, gửi <b>băm SHA256</b> của nó trước, gửi <b>chuỗi gốc</b> sau để máy chủ băm lại và so", "băm của <code>dBjftJeZ…</code> = <code>E9Melhoa…</code> (RFC 7636)"]]),
           """Trước hết ta cần hiểu bốn điều. Thứ nhất, mã truy cập như ở bài ba có ba phần, phía nhận kiểm chữ ký, hạn dùng và người nhận.
           Thứ hai, mã bốn trăm lẻ một nghĩa là mã không dùng được ở đây, còn bốn trăm lẻ ba nghĩa là mã tốt nhưng thiếu quyền.
           Thứ ba, chuyển hướng là máy chủ bảo trình duyệt mở một địa chỉ khác, ví dụ trang đăng nhập của ngân hàng.
           Thứ tư là cơ chế băm chuỗi bí mật: mỗi lần đăng nhập, ứng dụng sinh một chuỗi ngẫu nhiên, gửi băm SHA256 của nó trước, rồi gửi chuỗi gốc sau để máy chủ băm lại và so.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"]),
        st("""<p>Làm thử với chuỗi mẫu của RFC 7636 (RFC này chép lại đúng chuỗi chữ ký ở bài 3 làm chuỗi ngẫu nhiên mẫu; ở đây nó <b>không</b> phải chữ ký): băm SHA256 rồi viết base64url.</p>
$$\\text{dBjftJeZ4CVP…OEjXk} \\to \\hl{\\text{E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM}}$$""",
           """Làm thử với chuỗi mẫu trong RFC bảy nghìn sáu trăm ba mươi sáu, chuỗi này tình cờ trùng chữ ký ở bài ba vì RFC chép lại nó làm ví dụ. Băm SHA256 rồi viết lại bằng cơ số sáu mươi tư, ta được chuỗi bắt đầu bằng E chín M, đúng như RFC.
           Ai bắt được chuỗi băm này cũng không suy ngược ra chuỗi gốc, nên dù chặn được mã tạm mà máy chủ cấp giữa chừng, kẻ gian vẫn không đổi được nó lấy mã truy cập.""", clear=True),
    ], checks=["alg.bnx_pkce_s256('dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk') == 'E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM'",
               "alg.bnx_utc(1300819380)[:4] == '2011'", f"{C}('payments:write', 'api-a', 'payments:write', 'api-a', 360) == 401"])

    sym = sc("sym", "symbol", "Giải mã bốn vai và các từ hay gặp", [
        st(table(["vai (RFC 6749 mục 1.1)", "nghĩa", "trong ví dụ ngân hàng"],
                 [["chủ tài nguyên", "người có quyền cho phép truy cập", "khách hàng"],
                  ["máy khách (client)", "ứng dụng gọi API thay mặt chủ tài nguyên, hoặc cho chính nó (dịch vụ gọi dịch vụ)", "ứng dụng quản lý chi tiêu, dịch vụ thanh toán"],
                  ["máy chủ ủy quyền", "xác thực chủ tài nguyên rồi <b>cấp</b> mã truy cập", "máy chủ đăng nhập của ngân hàng"],
                  ["máy chủ tài nguyên", "giữ dữ liệu, <b>kiểm</b> mã rồi mới trả lời", "API tài khoản; API sổ cái <code>api-a</code>"]]),
           """Bảng này giải mã bốn vai. Chủ tài nguyên là người có quyền cho phép, ở đây là khách hàng.
           Máy khách là ứng dụng gọi giao diện lập trình thay mặt khách, hoặc cho chính nó khi dịch vụ gọi dịch vụ. Máy chủ ủy quyền xác thực khách rồi cấp mã.
           Máy chủ tài nguyên giữ dữ liệu, kiểm mã rồi mới trả lời.""", focus=["1.2", "1.2", "1.3", "1.4", "1.5"]),
        st(table(["từ trên màn hình", "nghĩa"],
                 [["scope (phạm vi)", "danh sách quyền ngăn bằng dấu cách: <code>accounts:read payments:write</code>"],
                  ["mã ủy quyền (code)", "mã tạm, dùng một lần, chỉ để đổi lấy mã truy cập"],
                  ["Bearer", "“người cầm”: ai cầm mã là dùng được, nên phải giữ kín và hạn ngắn"],
                  ["mã định danh (ID token)", "của OpenID Connect: nói <b>ai</b> vừa đăng nhập (<code>sub</code>), cấp cho ứng dụng (<code>aud</code>), có <code>iss</code>, <code>iat</code>, <code>exp</code>; <code>nonce</code> nếu ứng dụng đã gửi, để chống dùng lại mã cũ"]]),
           """Thêm bốn từ nữa. Phạm vi là danh sách quyền ngăn bằng dấu cách, ví dụ đọc tài khoản và ghi thanh toán. Mã ủy quyền là mã tạm, chỉ dùng một lần để đổi lấy mã truy cập.
           Kiểu người cầm nghĩa là ai cầm mã là dùng được, nên phải giữ kín. Mã định danh nói ai vừa đăng nhập, cấp cho chính ứng dụng, và mang lại số dùng một lần mà ứng dụng đã gửi, để chống dùng lại mã cũ.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], clear=True),
    ], checks=["alg.bnx_scopes('accounts:read payments:write') == ['accounts:read', 'payments:write']"])

    flow = _seq([("Khách", C_GREEN), ("Ứng dụng di động", C_BLUE), ("Máy chủ ủy quyền", C_PURPLE), ("API tài khoản", C_AMBER)],
                [(1, 2, "① xin mã + băm chuỗi bí mật"), (0, 2, "② khách đăng nhập, đồng ý phạm vi"),
                 (2, 1, "③ mã ủy quyền (dùng một lần)"), (1, 2, "④ mã ủy quyền + chuỗi bí mật gốc"),
                 (2, 1, "⑤ mã truy cập (+ mã định danh)"), (1, 3, "⑥ gọi API kèm mã truy cập")], 560)
    cc = _seq([("Dịch vụ thanh toán", C_BLUE), ("Máy chủ ủy quyền", C_PURPLE), ("API sổ cái (api-a)", C_AMBER)],
              [(0, 1, "① POST /token, phạm vi payments:write"), (1, 0, "② mã truy cập: aud api-a, hạn 300 giây"),
               (0, 2, "③ gọi API sổ cái, kèm mã"), (2, 0, "④ 200, hoặc 401 / 403")], 440)
    intu = sc("intuition", "intuition", "Hình dung: luồng các bên", [
        st(flow,
           """Hình này là luồng mã ủy quyền cho ứng dụng di động. Một, ứng dụng chuyển khách sang máy chủ ủy quyền, kèm băm của chuỗi bí mật.
           Hai, khách đăng nhập ngay tại máy chủ ủy quyền và đồng ý phạm vi, nên ứng dụng không thấy mật khẩu.
           Điều đó chỉ đúng khi trang đăng nhập mở bằng trình duyệt của hệ thống, chứ không phải khung nhúng trong ứng dụng. Ba, máy chủ trả về mã ủy quyền dùng một lần.
           Bốn, ứng dụng gửi mã ủy quyền cùng chuỗi bí mật gốc. Năm, máy chủ băm lại thấy khớp thì cấp mã truy cập. Sáu, ứng dụng gọi giao diện lập trình kèm mã đó."""),
        st(cc,
           """Còn khi dịch vụ gọi dịch vụ thì không có khách nào đăng nhập. Dịch vụ thanh toán chạy trên máy chủ, giữ được bí mật, nên tự xin mã bằng mã máy khách và bí mật đi kèm.
           Mã máy khách là tên định danh mà máy chủ ủy quyền cấp cho dịch vụ khi đăng ký.
           Máy chủ ủy quyền trả mã truy cập có người nhận là API A, hạn ba trăm giây. Dịch vụ gọi API sổ cái kèm mã, và API trả hai trăm, hoặc từ chối.""",
           ),
    ], checks=[f"{C}('payments:write', 'api-a', 'payments:write', 'api-a', 300) == 200"])

    form = sc("formula", "formula", "Suy ra từng bước: chọn luồng và kiểm mã", [
        st("""<p><b>Bước 1.</b> API không nên thấy mật khẩu của khách. Vì vậy tách vai: máy chủ ủy quyền <b>cấp</b> mã, máy chủ tài nguyên chỉ <b>kiểm</b> mã.</p>
<span class='note'>Làm thử: khách gõ mật khẩu ở 1 nơi (máy chủ ủy quyền), 0 lần ở ứng dụng và API.</span>""",
           """Bước một, vì giao diện lập trình không nên thấy mật khẩu của khách, ta tách vai. Máy chủ ủy quyền cấp mã, còn máy chủ tài nguyên chỉ kiểm mã.
           Làm thử, khách gõ mật khẩu ở đúng một nơi là máy chủ ủy quyền, và không lần nào ở ứng dụng hay giao diện lập trình.""", clear=True),
        st("""<p><b>Bước 2.</b> Ứng dụng di động là <b>máy khách công khai</b>: mọi bí mật đóng gói trong ứng dụng đều trích ra được (RFC 6749 mục 2.1).
Nên dùng <b>luồng mã ủy quyền có PKCE</b>: kẻ chặn được mã ở bước ③ không có chuỗi gốc để làm bước ④.</p>""",
           """Bước hai, ứng dụng di động là máy khách công khai, vì mọi bí mật đóng gói trong ứng dụng đều trích ra được.
           Nên ta dùng luồng mã ủy quyền có băm chuỗi bí mật. Kẻ chặn được mã ủy quyền ở bước ba vẫn không có chuỗi gốc để làm bước bốn."""),
        st("""<p><b>Bước 3.</b> Dịch vụ gọi dịch vụ thì không có khách, và dịch vụ chạy trên máy chủ <b>giữ được</b> bí mật. Nên dùng <b>luồng thông tin máy khách</b> (client credentials, RFC 6749 mục 4.4).</p>""",
           """Bước ba, khi dịch vụ gọi dịch vụ thì không có khách nào, và dịch vụ chạy trên máy chủ giữ được bí mật. Nên ta dùng luồng thông tin máy khách, chỉ cần mã máy khách và bí mật.""",
           clear=True),
        st(code(HTTP_TOKEN, "Yêu cầu xin mã (RFC 6749 mục 4.4.2, thêm phạm vi)"),
           """Đây là yêu cầu xin mã của luồng thông tin máy khách, theo ví dụ của RFC. Dòng xác thực mang mã máy khách và bí mật, viết lại bằng cơ số sáu mươi tư.
           Thân yêu cầu ghi loại luồng là thông tin máy khách, và phạm vi xin là ghi thanh toán, nên mã cấp ra chỉ được ghi thanh toán.""", focus=[0, "2.3", "2.6"], clear=True),
        st(code(JSON_TOKEN, "Phản hồi (RFC 6749 mục 5.1)"),
           """Phản hồi trả mã truy cập, kiểu người cầm, hạn ba trăm giây, và phạm vi đã cấp, nên dịch vụ biết sau ba trăm giây phải xin mã mới.""", focus=[["2.2", "2.3", "2.4", "2.5"]], clear=True),
        st("""<p><b>Bước 4.</b> API kiểm theo thứ tự: chữ ký và người phát hành (như bài 3) → <code>aud</code> đúng là mình → hạn (có lệch đồng hồ) → phạm vi.
Lỗi ở ba cửa đầu là <b>401</b> (mã không dùng được ở đây); qua hết mà thiếu phạm vi là <b>403</b>.</p>
$$300 + 60 = \\hl{360}\\ \\text{: từ giây này từ chối, giây cuối còn nhận là } \\hlg{359}$$""",
           """Bước bốn, giao diện lập trình kiểm theo thứ tự. Chữ ký và người phát hành như bài ba, rồi người nhận phải đúng là mình, rồi hạn dùng, rồi phạm vi.
           Sai ở các cửa đầu là bốn trăm lẻ một, vì mã không dùng được ở đây. Qua hết mà thiếu phạm vi thì là bốn trăm lẻ ba.
           Vì đồng hồ hai máy có thể lệch nhau, ta cho lệch sáu mươi giây, nên hạn cộng lệch là giây ba trăm sáu mươi.
           Giống bài ba, mã không được nhận từ đúng giây đó, nên giây cuối còn nhận là ba trăm năm mươi chín.""",
           focus=[1, 1, 1, 1, 2, 2], clear=True),
    ], checks=["alg.bnx_last_ok_age(300, 60) == 359", f"{C}('payments:write', 'api-a', 'payments:write', 'api-a', 359) == 200",
               f"{C}('payments:write', 'api-a', 'payments:write', 'api-a', 360) == 401",
               "__import__('base64').b64decode('czZCaGRSa3F0MzpnWDFmQmF0M2JW') == b's6BhdRkqt3:gX1fBat3bV'"])

    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Mã cấp lúc giây <code>iat</code> = 1000, <code>expires_in</code> = 300.</p>
$$① \\; 1000 + 300 = \\hl{1300} = \\text{exp}$$""",
           """Ta tính năm ca. Mã được cấp ở giây một nghìn, hạn ba trăm giây. Phép tính thứ nhất, hạn dùng là một nghìn cộng ba trăm, bằng một nghìn ba trăm.""",
           clear=True),
        st("""$$② \\; \\text{phạm vi “accounts:read” không có “payments:write”} \\Rightarrow \\hl{403}$$""",
           """Phép tính thứ hai. Mã chỉ có phạm vi đọc tài khoản, không có ghi thanh toán, nên gọi lệnh ghi bị từ chối bốn trăm lẻ ba.""",
           introduces=["implies"]),
        st("""$$③ \\; \\text{aud} = \\text{api-a} \\ne \\text{api-b} \\Rightarrow \\hl{401}$$""",
           """Phép tính thứ ba. Mã cấp cho người nhận API A mang sang API B, người nhận không khớp, nên API B từ chối bốn trăm lẻ một."""),
        st("""<p>Dùng lại exp = 1300 ở phép ①.</p>
$$④ \\; 1000 + 359 = 1359 \\text{ nhỏ hơn } 1300 + 60 = 1360 \\Rightarrow \\hlg{200}$$""",
           """Phép tính thứ tư dùng lại hạn một nghìn ba trăm. Ở giây thứ ba trăm năm mươi chín, bây giờ là một nghìn ba trăm năm mươi chín, còn nhỏ hơn hạn cộng lệch, nên còn nhận.""", clear=True),
        st("""$$⑤ \\; 1000 + 360 = 1360 \\text{ không nhỏ hơn } 1360 \\Rightarrow \\hl{401}$$""",
           """Phép tính thứ năm. Chỉ một giây sau, bây giờ là một nghìn ba trăm sáu mươi, đã bằng hạn cộng lệch, nên theo đúng quy tắc của bài ba, mã bị từ chối bốn trăm lẻ một."""),
        st(code(PY_RS, "Máy chủ tài nguyên kiểm mã (Python)"),
           """Bây giờ viết thành mã Python. Hàm kiểm nhận các trường của mã, quyền cần, tên của chính API, và thời điểm hiện tại.
           Cửa đầu tìm tên mình trong người nhận, vì người nhận có thể là một tên hoặc một danh sách tên. Cửa hai từ chối khi thời điểm đã tới hạn cộng lệch.
           Cửa ba tìm quyền cần trong danh sách phạm vi.""",
           focus=[0, "2.1", ["2.3", "2.4", "2.5"], ["2.6", "2.7"], ["2.8", "2.9"]], clear=True),
        st(code(PY_CASES, "Năm ca thử"),
           """Năm ca thử. Mã chỉ đọc gọi lệnh ghi. Mã ghi mang sang API B. Mã ghi ở giây ba trăm năm mươi chín, rồi ba trăm sáu mươi.
           Ca cuối là một mã định danh, người nhận là chính ứng dụng di động, bị đem đi gọi API A.""",
           focus=[0, "2.4", "2.5", ["2.6", "2.7"], ["2.8", "2.9"]], clear=True),
        st(out(OUT_CASES),
           """Kết quả chạy thật, đúng thứ tự: bốn trăm lẻ ba, bốn trăm lẻ một, hai trăm, bốn trăm lẻ một, và bốn trăm lẻ một cho mã định danh.
           Bốn số đầu khớp các phép tính ta vừa làm bằng tay, từ phép hai tới phép năm.""", clear=True),
    ], checks=["1000 + 300 == 1300", f"{C}('accounts:read', 'api-a', 'payments:write', 'api-a', 10) == 403",
               f"{C}('payments:write', 'api-a', 'payments:write', 'api-b', 10) == 401",
               f"{C}('payments:write', 'api-a', 'payments:write', 'api-a', 359) == 200",
               f"{C}('payments:write', 'api-a', 'payments:write', 'api-a', 360) == 401",
               "alg.bnx_rs_check({'aud': 'app-di-dong', 'exp': 1300, 'nonce': 'n-0S6'}, 'payments:write', 'api-a', 1010) == 401"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: đếm từng giây", [
        st(code(PY_COUNT, "Đếm thẳng mọi giây từ 0 tới 999"),
           """Kiểm bằng đường khác. Thay vì tính giây biên, ta thử hết một nghìn giây kể từ lúc cấp, và giữ lại những giây được nhận.""",
           clear=True),
        st(out(OUT_COUNT),
           """Kết quả chạy thật cho thấy, vì mọi giây đều được thử, có đúng ba trăm sáu mươi giây được nhận, từ giây không tới giây ba trăm năm mươi chín. Vậy giây biên ở phép bốn và phép năm là đúng."""),
        st(table(["quy tắc so ở giây biên", "giây 359", "giây 360"],
                 [["bài này: từ chối khi bây giờ ≥ exp + lệch (khớp RFC 7519 và bài 3)", "nhận", "từ chối"],
                  ["một số thư viện: từ chối khi bây giờ &gt; exp + lệch", "nhận", "nhận (giây 361 mới từ chối)"]]),
           """Bảng này nhắc một điều người đi làm hay gặp. Bài này từ chối ngay khi bây giờ bằng hạn cộng lệch, khớp RFC và bài ba, còn có thư viện chỉ từ chối khi lớn hơn.
           Vì hai cách chỉ khác nhau đúng một giây, hãy đọc kỹ mô tả của thư viện mình dùng, rồi chạy thử đúng giây biên, thay vì đoán.""", focus=[0, 1, 1], clear=True),
    ], checks=["alg.bnx_ok_seconds(300, 60, 999) == 360", "alg.bnx_last_ok_age(300, 60) == 359"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Coi OAuth 2.0 là <b class="red">đăng nhập</b>. Mã truy cập dành cho API; ứng dụng không được dựa vào nó để biết ai đăng nhập.
Đó là việc của OpenID Connect: mã định danh bắt buộc có <code>iss</code>, <code>sub</code>, <code>aud</code>, <code>exp</code>, <code>iat</code>; có <code>nonce</code> nếu ứng dụng đã gửi (OpenID Connect Core 1.0 mục 2).</div>""",
           """Lỗi thứ nhất, của người mới, là coi OAuth 2.0 là đăng nhập. Mã truy cập dành cho giao diện lập trình, và ứng dụng không được dựa vào nó để biết ai đăng nhập.
           Đó là việc của OpenID Connect, qua mã định danh bắt buộc có người phát hành, chủ thể, người nhận, hạn dùng, lúc cấp, và số dùng một lần nếu ứng dụng đã gửi.""",
           clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Dùng mã định danh để gọi API</b>. Người nhận của nó là chính ứng dụng (<code>app-di-dong</code>), nên API kiểm <code>aud</code> phải trả <b>401</b>, như ca cuối.
<br><span class="note">API bỏ qua <code>aud</code> sẽ nhận nhầm. RFC 9068 thêm kiểu <code>at+jwt</code> để phân biệt mã truy cập với mã định danh.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là dùng mã định danh để gọi giao diện lập trình. Người nhận của nó là chính ứng dụng, nên API kiểm người nhận phải trả bốn trăm lẻ một, như ca cuối.
           API nào bỏ qua người nhận sẽ nhận nhầm, vì cả hai loại mã đều có chữ ký đúng.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Đặt <b class="red">bí mật máy khách trong ứng dụng di động</b>. Ai tải ứng dụng cũng trích ra được (RFC 6749 mục 2.1).
<br><span class="note">Cách chữa: ứng dụng là máy khách công khai, dùng mã ủy quyền có PKCE; bí mật chỉ nằm ở dịch vụ phía máy chủ.</span></div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là đặt bí mật máy khách trong ứng dụng di động. Ai tải ứng dụng về cũng trích ra được.
           Cách chữa là coi ứng dụng là máy khách công khai, dùng mã ủy quyền có băm chuỗi bí mật, còn bí mật chỉ nằm ở dịch vụ phía máy chủ.""", clear=True),
    ], checks=["alg.bnx_rs_check({'aud': 'app-di-dong', 'exp': 1300}, 'payments:write', 'api-a', 1010) == 401"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Mã có phạm vi <code>accounts:read payments:write</code>, aud <code>api-a</code>, cấp lúc 1000, hạn 300. Gọi <code>api-a</code> cần <code>payments:write</code> lúc 1100. Kết quả?"],
                  ["2", "Mã hạn 600 giây, cho lệch đồng hồ 60 giây (quy tắc của bài). Giây cuối còn nhận là giây thứ mấy?"],
                  ["3", "Quyết định (số minh hoạ): 5 API, mã hạn 300 giây. Một mã chung có aud cả 5 API, hay mỗi API một mã riêng?"]]),
           """Đến lượt bạn. Câu một, mã có hai phạm vi đọc tài khoản và ghi thanh toán, gọi API A cần ghi thanh toán ở giây một nghìn một trăm, kết quả ra sao?
           Câu hai, mã hạn sáu trăm giây, cho lệch sáu mươi giây, giây cuối còn nhận là giây thứ mấy?
           Câu ba, có năm giao diện lập trình, nên dùng một mã chung hay mỗi nơi một mã riêng? Hãy dừng video lại và làm từng câu ra giấy trước khi xem đáp án.""",
           pause=25),
        st("""<p>Câu 1: aud đúng; 1100 &lt; 1300 + 60; phạm vi tách theo dấu cách có <code>payments:write</code>.</p>
$$\\Rightarrow \\hlg{200}$$""",
           """Đáp án câu một. Người nhận đúng, giây một nghìn một trăm còn trong hạn, và tách phạm vi theo dấu cách thì có ghi thanh toán, nên kết quả là hai trăm."""),
        st("""<p>Câu 2: từ chối khi bây giờ ≥ hạn + lệch.</p>
$$600 + 60 = 660 \\Rightarrow 660 \\to 401; \\quad \\text{giây cuối còn nhận } \\hlg{659}$$""",
           """Đáp án câu hai. Hạn cộng lệch là sáu trăm cộng sáu mươi, bằng sáu trăm sáu mươi, nên từ giây đó bị từ chối. Giây cuối còn nhận là sáu trăm năm mươi chín."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["một mã chung, aud là danh sách 5 API", "xin mã 3600 : 300 = 12 lần mỗi giờ", "lộ mã thì cả 5 API bị dùng"],
                  ["mỗi API một mã riêng", "lộ một mã chỉ hở 1 API; aud hẹp", "xin mã $5 \\cdot 12 = 60$ lần mỗi giờ"]]),
           """Đáp án câu ba, ta so hai cách theo số lần xin mã và vùng thiệt hại. Một mã chung có người nhận là danh sách năm tên, hàm kiểm tìm tên mình trong danh sách, nên mỗi giờ chỉ xin mười hai lần, nhưng lộ mã là cả năm nơi bị dùng.
           Mỗi nơi một mã riêng thì lộ một mã chỉ hở một nơi, đổi lại mỗi giờ phải xin sáu mươi lần. Nên chọn vùng thiệt hại nhỏ, rồi lưu mã đệm đến gần hạn để giảm số lần xin.""",
           focus=[0, "1.2", "1.3", 0]),
    ], checks=[f"alg.bnx_rs_check({{'aud': 'api-a', 'exp': 1300, 'scope': 'accounts:read payments:write'}}, 'payments:write', 'api-a', 1100) == 200",
               "alg.bnx_last_ok_age(600, 60) == 659", f"{C}('payments:write', 'api-a', 'payments:write', 'api-a', 660, ttl=600) == 401",
               f"{C}('payments:write', 'api-a', 'payments:write', 'api-a', 659, ttl=600) == 200",
               "alg.bnx_rs_check({'aud': ['api-a', 'api-b', 'api-c', 'api-d', 'api-e'], 'exp': 1300, 'scope': 'payments:write'}, 'payments:write', 'api-c', 1100) == 200",
               "alg.bnx_token_requests_per_hour(1, 300) == 12", "alg.bnx_token_requests_per_hour(5, 300) == 60"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("máy chủ ủy quyền cấp mã", "ứng dụng: mã ủy quyền + PKCE", "dịch vụ: thông tin máy khách", "API kiểm aud, hạn, phạm vi", "401 hay 403"),
           """Tổng kết chuỗi logic. Máy chủ ủy quyền cấp mã. Ứng dụng di động dùng mã ủy quyền có băm chuỗi bí mật, còn dịch vụ gọi dịch vụ dùng thông tin máy khách.
           Giao diện lập trình kiểm người nhận, hạn và phạm vi, rồi trả bốn trăm lẻ một hoặc bốn trăm lẻ ba cho đúng."""),
        st("""<div class='box key'><b>Tư duy:</b> tách “ai cấp” khỏi “ai kiểm”, và cho mỗi mã <b>ít quyền nhất, ít nơi nhận nhất, hạn ngắn nhất</b> đủ dùng.
Mã định danh để biết ai đăng nhập; mã truy cập để gọi API.</div>""",
           """Điều cần mang theo. Tách ai cấp khỏi ai kiểm, và cho mỗi mã ít quyền nhất, ít nơi nhận nhất, hạn ngắn nhất mà vẫn đủ dùng.
           Mã định danh để biết ai đăng nhập, còn mã truy cập để gọi giao diện lập trình."""),
        st("""<p>Bài sau: khi các dịch vụ gọi nhau, <b>máy</b> cũng phải chứng minh mình là ai: hai bên cùng trình chứng chỉ.</p>""",
           """Ở bài năm, ta xem khi các dịch vụ gọi nhau, chính máy cũng phải chứng minh mình là ai, bằng cách hai bên cùng trình chứng chỉ.""",
           forward_ref=True),
    ])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
    return lesson("L04", "oauth2_openid_connect", "Bài 4 — OAuth 2.0 và OpenID Connect: ai cấp mã, ai kiểm mã, phạm vi quyền",
                  "curriculum/bnx.yaml L04; audit/bnx/verify_bnx.py L04; RFC 6749 mục 1.1, 2.1, 3.3, 4.4, 5.1 (2012); RFC 6750 mục 3.1 (2012); "
                  "RFC 7636 phụ lục B (2015); RFC 7519 mục 4.1.3, 4.1.4 (2015); RFC 9068 (2021); RFC 8252 mục 8.12 (2017); OpenID Connect Core 1.0 mục 2 (đọc 2026-11-11)",
                  ["Gọi tên bốn vai trong OAuth 2.0", "Chọn luồng cấp mã: mã ủy quyền có PKCE cho ứng dụng, thông tin máy khách cho dịch vụ với dịch vụ",
                   "Kiểm phạm vi quyền và người nhận của mã truy cập", "Phân biệt mã truy cập với mã định danh của OpenID Connect"],
                  scenes)
