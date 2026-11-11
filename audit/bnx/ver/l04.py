"""Kiểm độc lập BNX L04 (OAuth 2.0 / OpenID Connect). Đường khác với tools/checklib_bnx/l04.py:
- dựng mã truy cập THẬT (JWT ký HS256 bằng hmac), máy chủ tài nguyên giải mã + kiểm chữ ký rồi mới xét aud/exp/scope;
  so với alg trên lưới mọi tổ hợp (phạm vi × người nhận × giây 0..400);
- giây biên tìm bằng chia đôi, số giây được nhận đếm thẳng;
- PKCE: openssl dgst -sha256 thật + base64url tự làm; Basic của RFC 6749 giải mã thật;
- chạy NGUYÊN VĂN các hằng mã ở audit/bnx/src/l04.py và so với đầu ra trên màn hình."""
import base64
import hashlib
import hmac
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import l04 as src  # noqa: E402

K = b"khoa-thu-cua-may-chu-uy-quyen-32b"


def u(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def ud(s):
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def issue(claims):
    h = u(json.dumps({"typ": "at+jwt", "alg": "HS256"}).encode()) + "." + u(json.dumps(claims).encode())
    return h + "." + u(hmac.new(K, h.encode(), hashlib.sha256).digest())


def resource_server(tok, need, me, now, skew=60):
    d, t, s = tok.split(".")
    if not hmac.compare_digest(u(hmac.new(K, (d + "." + t).encode(), hashlib.sha256).digest()), s):
        return 401
    c = json.loads(ud(t))
    aud = c.get("aud")
    if isinstance(aud, str):
        aud = [aud]
    if me not in aud:
        return 401
    if not now < c["exp"] + skew:   # RFC 7519 §4.1.4: không nhận "on or after" exp (+ lệch)
        return 401
    return 200 if need in c.get("scope", "").split() else 403


def run_py(code):
    with tempfile.TemporaryDirectory() as d:
        Path(d, "k.py").write_text(code, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", "k.py"], cwd=d, capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout


def run(rec):
    iat = 1000
    # lưới tổ hợp: máy chủ tài nguyên dựng từ mã ký thật = alg
    bad = 0
    for scope in ("accounts:read", "payments:write", "accounts:read payments:write", ""):
        for aud in ("api-a", "api-b", "app-di-dong", ["api-b", "api-a"], ["api-b", "api-c"], "api-ab"):
            for age in range(0, 401):
                tok = issue({"iss": "https://auth", "sub": "svc", "aud": aud, "exp": iat + 300, "scope": scope, "iat": iat})
                a = resource_server(tok, "payments:write", "api-a", iat + age)
                b = alg.bnx_oauth_case(scope, aud, "payments:write", "api-a", age)
                bad += a != b
    rec("L04", bad == 0, f"máy chủ tài nguyên từ mã JWT ký thật khớp alg trên 4 × 6 × 401 tổ hợp, gồm aud là danh sách (lệch {bad})")
    four = (alg.bnx_oauth_case("accounts:read", "api-a", "payments:write", "api-a", 10), alg.bnx_oauth_case("payments:write", "api-a", "payments:write", "api-b", 10),
            alg.bnx_oauth_case("payments:write", "api-a", "payments:write", "api-a", 359), alg.bnx_oauth_case("payments:write", "api-a", "payments:write", "api-a", 360))
    rec("L04", four == (403, 401, 200, 401), f"ví dụ giáo án: thiếu phạm vi 403, sai aud 401, giây 359 → 200, giây 360 → 401 {four}")
    rec("L04", resource_server(issue({"aud": "api-a", "exp": 1300, "scope": "payments:write"}), "payments:write", "api-a", 1300, skew=0) == 401
        and alg.bnx_rs_check({"aud": "api-a", "exp": 1300, "scope": "payments:write"}, "payments:write", "api-a", 1300, skew=0) == 401,
        "lệch 0, đúng giây exp → 401 (khớp RFC 7519 §4.1.4 và bài 3)")
    # chữ ký giả → 401 dù aud, phạm vi đúng
    tok = issue({"aud": "api-a", "exp": 1300, "scope": "payments:write"})
    forged = tok[:-2] + ("AA" if tok[-2:] != "AA" else "BB")
    rec("L04", resource_server(tok, "payments:write", "api-a", 1010) == 200 and resource_server(forged, "payments:write", "api-a", 1010) == 401,
        "đường khác có kiểm chữ ký: mã sửa chữ ký → 401")
    # giây biên bằng chia đôi
    lo, hi = 0, 10000
    while lo < hi:
        mid = (lo + hi + 1) // 2
        ok = resource_server(issue({"aud": "api-a", "exp": iat + 300, "scope": "payments:write"}), "payments:write", "api-a", iat + mid) == 200
        lo, hi = (mid, hi) if ok else (lo, mid - 1)
    rec("L04", lo == 359 == alg.bnx_last_ok_age(300, 60) and 300 + 60 - 1 == 359, f"chia đôi tìm giây cuối còn nhận: {lo} (từ giây 300 + 60 là từ chối)")
    rec("L04", alg.bnx_ok_seconds(300, 60, 999) == 360 == len(range(0, 360)), "đếm thẳng: 360 giây được nhận (0..359)")
    lo2 = max(g for g in range(0, 2000) if resource_server(issue({"aud": "api-a", "exp": iat + 600, "scope": "payments:write"}), "payments:write", "api-a", iat + g) == 200)
    rec("L04", lo2 == 659 == alg.bnx_last_ok_age(600, 60), f"câu 2: hạn 600 + lệch 60 → giây cuối {lo2}, từ giây 660 từ chối")
    q3 = resource_server(issue({"aud": ["api-a", "api-b", "api-c", "api-d", "api-e"], "exp": 1300, "scope": "payments:write"}), "payments:write", "api-c", 1100)
    rec("L04", q3 == 200, "câu 3: một mã chung, aud là danh sách 5 API → api-c nhận (tìm tên mình trong danh sách)")
    q1 = resource_server(issue({"aud": "api-a", "exp": 1300, "scope": "accounts:read payments:write"}), "payments:write", "api-a", 1100)
    rec("L04", q1 == 200, "câu 1: phạm vi hai quyền ngăn bằng dấu cách, aud đúng, giây 1100 → 200")
    rec("L04", (1 * (3600 // 300), 5 * (3600 // 300)) == (alg.bnx_token_requests_per_hour(1, 300), alg.bnx_token_requests_per_hour(5, 300)) == (12, 60),
        "câu 3: 12 lần xin mã mỗi giờ (một mã), 60 lần (5 mã riêng)")
    idt = issue({"iss": "https://auth", "sub": "kh-001", "aud": "app-di-dong", "exp": 1300, "iat": 1000, "nonce": "n-0S6"})
    rec("L04", resource_server(idt, "payments:write", "api-a", 1010) == 401, "mã định danh (aud = ứng dụng) đem gọi api-a → 401")
    # PKCE RFC 7636 phụ lục B
    v, want = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk", "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
    ossl = shutil.which("openssl")
    if not ossl:
        rec("L04", None, "thiếu openssl")
    else:
        r = subprocess.run([ossl, "dgst", "-sha256", "-binary"], input=v.encode(), capture_output=True)
        rec("L04", r.returncode == 0 and u(r.stdout) == want == alg.bnx_pkce_s256(v), "PKCE: openssl sha256 của chuỗi RFC 7636 → E9Melhoa… (khớp alg)")
    rec("L04", base64.b64decode("czZCaGRSa3F0MzpnWDFmQmF0M2JW") == b"s6BhdRkqt3:gX1fBat3bV", "Basic của RFC 6749 §4.4.2 = client_id:client_secret của ví dụ")
    j = json.loads(src.JSON_TOKEN)
    pre = j["access_token"].rstrip("…")
    rec("L04", j["expires_in"] == 300 and j["token_type"] == "Bearer" and j["scope"] == "payments:write"
        and u(b'{"typ":"at+jwt","alg":"RS256"}').startswith(pre) and ud(pre[:32]).startswith(b'{"typ":"at+jwt","alg"'),
        "phản hồi JSON phân tích được; phần đầu rút gọn là base64url của {\"typ\":\"at+jwt\",\"alg\"…")
    rec("L04", "grant_type=client_credentials&scope=payments:write" in src.HTTP_TOKEN and "\n\n" in src.HTTP_TOKEN, "yêu cầu xin mã: thân đúng tham số, có dòng trống")
    rc, so = run_py(src.PY_RS.strip("\n") + "\n" + src.PY_CASES.strip("\n") + "\n")
    rec("L04", rc == 0 and so.split() == ["403", "401", "200", "401", "401"] == src.OUT_CASES.split(), "khối năm ca thử chạy nguyên văn = màn hình")
    rc, so = run_py("\n".join(x.strip("\n") for x in (src.PY_RS, src.PY_CASES, src.PY_COUNT)) + "\n")
    rec("L04", rc == 0 and so.strip().split("\n")[-1] == src.OUT_COUNT.strip() == "360 0 359", "khối đếm chạy nguyên văn: 360 0 359")
    blocks = (src.PY_RS, src.PY_CASES, src.PY_COUNT, src.HTTP_TOKEN, src.JSON_TOKEN)
    m = max(len(l) for c in blocks for l in c.strip("\n").split("\n"))
    rec("L04", m <= 70 and all(len(c.strip("\n").split("\n")) <= 12 for c in blocks), f"khối mã ≤ 12 dòng, dòng dài nhất {m} ký tự")
