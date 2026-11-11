"""BNX L04 — OAuth 2.0 và OpenID Connect: máy chủ tài nguyên kiểm người nhận, hạn dùng (có lệch đồng hồ), phạm vi quyền.
Quy tắc của bài (khớp VER BNX:L04 ở audit/verify_plan_curricula.py, sửa 2026-11-11 theo RFC 7519 §4.1.4 và bài 3):
tên mình không có trong aud (một chuỗi hoặc danh sách, §4.1.3) → 401; bây giờ ≥ exp + lệch → 401; thiếu phạm vi → 403
(RFC 6750 §3.1: invalid_token 401, insufficient_scope 403). Chỉ thư viện chuẩn."""
import base64 as _b64
import hashlib as _hl


def bnx_rs_check(c, need, me, now, skew=60):
    """c: các trường của mã truy cập (chữ ký đã kiểm). Trả mã trạng thái HTTP."""
    aud = c.get("aud")
    if me not in (aud if isinstance(aud, list) else [aud]):
        return 401
    if now >= c["exp"] + skew:
        return 401
    if need not in str(c.get("scope", "")).split(" "):
        return 403
    return 200


def bnx_oauth_case(scope, aud, need, me, age, ttl=300, skew=60, iat=1000):
    return bnx_rs_check({"aud": aud, "exp": iat + ttl, "scope": scope}, need, me, iat + age, skew)


def bnx_last_ok_age(ttl, skew):
    """Giây cuối (tính từ lúc cấp, số nguyên) còn được nhận: từ giây ttl + skew là từ chối."""
    return ttl + skew - 1


def bnx_ok_seconds(ttl, skew, upto=10000):
    """Số giây nguyên 0..upto (tính từ lúc cấp) được nhận — đếm thẳng."""
    return sum(1 for g in range(upto + 1) if bnx_oauth_case("payments:write", "api-a", "payments:write", "api-a", g, ttl, skew) == 200)


def bnx_pkce_s256(verifier):
    """RFC 7636 §4.2: code_challenge = BASE64URL(SHA256(ASCII(code_verifier)))."""
    return _b64.urlsafe_b64encode(_hl.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode()


def bnx_scopes(s):
    """RFC 6749 §3.3: phạm vi là danh sách ngăn bằng dấu cách."""
    return s.split(" ")


def bnx_token_requests_per_hour(n_api, ttl):
    """Mỗi mã riêng một API, hạn ttl giây: số lần xin mã mỗi giờ."""
    return n_api * (3600 // ttl)
