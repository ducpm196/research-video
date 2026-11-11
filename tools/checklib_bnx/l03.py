"""BNX L03 — JWT: base64url, chữ ký HS256 (RFC 7515 Phụ lục A.1), kiểm thuật toán / chữ ký / hạn dùng / người phát hành / người nhận (RFC 7519).
Chỉ thư viện chuẩn. Kiểm độc lập ở audit/bnx/ver/l03.py (HMAC tự dựng từ SHA256, base64 tự dựng, openssl thật)."""
import base64 as _b64
import datetime as _dt
import hashlib as _hl
import hmac as _hm
import json as _js


def bnx_b64u(b):
    """base64url bỏ dấu '=' cuối (RFC 7515 §2)."""
    return _b64.urlsafe_b64encode(b).rstrip(b"=").decode()


def bnx_unb64u(s):
    return _b64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def bnx_b64u_len(n):
    """Số ký tự base64url (không đệm) của n byte: mỗi 3 byte → 4 ký tự; dư 1 byte → 2 ký tự, dư 2 byte → 3 ký tự."""
    return 4 * (n // 3) + {0: 0, 1: 2, 2: 3}[n % 3]


def bnx_jwt_rfc7515():
    """Phần đầu, phần thân, khoá của ví dụ RFC 7515 Phụ lục A.1 (đúng từng byte, có \\r\\n)."""
    h = b'{"typ":"JWT",\r\n "alg":"HS256"}'
    p = b'{"iss":"joe",\r\n "exp":1300819380,\r\n "http://example.com/is_root":true}'
    k = bnx_unb64u("AyM1SysPpbyDfgZld3umj1qzKObwVMkoqQ-EstJQLr_T-1qS0gZH75aKtMN3Yj0iPS4hcgUuTwjAzZr1Z9CAow")
    return h, p, k


def bnx_jwt_sign(h, p, k):
    vao = bnx_b64u(h) + "." + bnx_b64u(p)
    return vao + "." + bnx_b64u(_hm.new(k, vao.encode(), _hl.sha256).digest())


def bnx_jwt_rfc_token():
    return bnx_jwt_sign(*bnx_jwt_rfc7515())


def bnx_jwt_part(i):
    return bnx_jwt_rfc_token().split(".")[i]


def bnx_jwt_tamper():
    """Sửa đúng một ký tự phần thân (1300… → 9300…), giữ chữ ký cũ."""
    h, p, k = bnx_jwt_rfc7515()
    d, t, s = bnx_jwt_rfc_token().split(".")
    return d + "." + bnx_b64u(p.replace(b"1300", b"9300")) + "." + s


def bnx_jwt_check(tok, k, aud, now, iss="joe", alg="HS256"):
    """Thứ tự kiểm như khối mã trên màn hình: thuật toán cố định → chữ ký (so thời gian hằng) → hạn → người phát hành/nhận."""
    d, t, s = tok.split(".")
    if _js.loads(bnx_unb64u(d)).get("alg") != alg:
        return "thuật toán lạ"
    if not _hm.compare_digest(bnx_b64u(_hm.new(k, (d + "." + t).encode(), _hl.sha256).digest()), s):
        return "chữ ký sai"
    c = _js.loads(bnx_unb64u(t))
    if now >= c["exp"]:
        return "hết hạn"
    if c.get("iss") != iss or c.get("aud") != aud:
        return "sai người phát hành/nhận"
    return "nhận"


def bnx_jwt_cases(now):
    """Năm ca của khối mã: mã RFC hôm nay; sửa 1 ký tự; alg none; mã có aud api-a đúng/sai người nhận."""
    h, p, k = bnx_jwt_rfc7515()
    tok = bnx_jwt_rfc_token()
    d, t, s = tok.split(".")
    none = bnx_b64u(b'{"alg":"none"}') + "." + t + "."
    ma2 = bnx_jwt_sign(h, b'{"iss":"joe","aud":"api-a","exp":1300819380}', k)
    return [bnx_jwt_check(tok, k, "api-a", now), bnx_jwt_check(bnx_jwt_tamper(), k, "api-a", 1300819379),
            bnx_jwt_check(none, k, "api-a", 0), bnx_jwt_check(ma2, k, "api-a", 1300819379),
            bnx_jwt_check(ma2, k, "api-b", 1300819379)]


def bnx_utc(ts):
    return _dt.datetime.fromtimestamp(ts, _dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def bnx_exp_ok(exp, now, leeway=0):
    """RFC 7519 §4.1.4: chỉ nhận khi bây giờ < exp (+ độ lệch cho phép)."""
    return now < exp + leeway


def bnx_risk_window(ttl_s, revoke_at_s):
    """Mã bị lộ ở giây revoke_at_s sau khi cấp, không có danh sách thu hồi: kẻ gian còn dùng được tới hết hạn."""
    return max(0, ttl_s - revoke_at_s)
