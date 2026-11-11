"""Kiểm độc lập BNX L03 (JWT). Đường khác với tools/checklib_bnx/l03.py:
- HMAC SHA256 tự dựng theo RFC 2104 (ipad/opad, chỉ dùng hashlib.sha256), base64url tự dựng bằng phép dịch bit;
- openssl dgst thật (không qua Python hmac); date của Git Bash chạy nguyên văn khối mã trên màn hình;
- đổi giây Unix ra ngày bằng thuật toán lịch (đếm ngày), không dùng datetime;
- chạy NGUYÊN VĂN các hằng mã ở audit/bnx/src/l03.py rồi so với đầu ra trên màn hình."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import l03 as src  # noqa: E402

A = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"


def b64u(b):
    bits = "".join(f"{x:08b}" for x in b)
    bits += "0" * (-len(bits) % 6)
    return "".join(A[int(bits[i:i + 6], 2)] for i in range(0, len(bits), 6))


def unb64u(s):
    bits = "".join(f"{A.index(c):06b}" for c in s)
    return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits) - len(bits) % 8, 8))


def hmac256(k, m):
    if len(k) > 64:
        k = hashlib.sha256(k).digest()
    k = k + b"\0" * (64 - len(k))
    ipad, opad = bytes(x ^ 0x36 for x in k), bytes(x ^ 0x5C for x in k)
    return hashlib.sha256(opad + hashlib.sha256(ipad + m).digest()).digest()


def civil(ts):
    """Giây Unix → (năm, tháng, ngày, giờ, phút, giây) bằng đếm ngày thuần (lịch Gregory)."""
    d, r = divmod(ts, 86400)
    y = 1970
    while True:
        n = 366 if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0 else 365
        if d < n:
            break
        d -= n
        y += 1
    ml = [31, 29 if n == 366 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    mo = 0
    while d >= ml[mo]:
        d -= ml[mo]
        mo += 1
    return y, mo + 1, d + 1, r // 3600, r % 3600 // 60, r % 60


def verify(tok, k, aud, now):
    d, t, s = tok.split(".")
    if json.loads(unb64u(d)).get("alg") != "HS256":
        return "thuật toán lạ"
    if b64u(hmac256(k, (d + "." + t).encode())) != s:
        return "chữ ký sai"
    c = json.loads(unb64u(t))
    if not now < c["exp"]:
        return "hết hạn"
    if c.get("iss") != "joe" or c.get("aud") != aud:
        return "sai người phát hành/nhận"
    return "nhận"


def line_match(want, got):
    rx = re.compile("^" + ".*".join(re.escape(p) for p in want.strip().split("…")) + "$")
    return bool(rx.match(got.strip()))


def screen_matches(screen, actual):
    lines, pos = [l for l in actual.replace("\r\n", "\n").split("\n")], 0
    for w in [x for x in screen.strip("\n").split("\n") if x.strip()]:
        while pos < len(lines) and not line_match(w, lines[pos]):
            pos += 1
        if pos == len(lines):
            return False
        pos += 1
    return True


def run_py(code):
    with tempfile.TemporaryDirectory() as d:
        Path(d, "k.py").write_text(code, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", "k.py"], cwd=d, capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout


def run(rec):
    # dữ liệu RFC 7515 A.1, giải mã bằng bộ giải mã tự dựng
    h = b'{"typ":"JWT",\r\n "alg":"HS256"}'
    p = b'{"iss":"joe",\r\n "exp":1300819380,\r\n "http://example.com/is_root":true}'
    k = unb64u("AyM1SysPpbyDfgZld3umj1qzKObwVMkoqQ-EstJQLr_T-1qS0gZH75aKtMN3Yj0iPS4hcgUuTwjAzZr1Z9CAow")
    rec("L03", (h, p, k) == alg.bnx_jwt_rfc7515() and len(k) == 64, "dữ liệu RFC 7515 A.1: phần đầu 30 byte, thân 70 byte, khoá 64 byte (giải mã tự dựng)")
    hd, bd = b64u(h), b64u(p)
    sig = b64u(hmac256(k, (hd + "." + bd).encode()))
    RFC = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
    rec("L03", sig == RFC == alg.bnx_jwt_part(2), f"HMAC tự dựng (ipad/opad) ra đúng chữ ký RFC {sig}")
    rec("L03", (len(hd), len(bd), len(sig)) == (40, 94, 43) == (alg.bnx_b64u_len(30), alg.bnx_b64u_len(70), alg.bnx_b64u_len(32)),
        "độ dài base64url 40 / 94 / 43 ký tự (30, 70, 32 byte) — đếm bằng bộ mã tự dựng")
    rec("L03", hd == "eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9" and b64u(b"abc") == "YWJj" and b64u(bytes([251, 255])) == "-_8",
        "① phần đầu viết lại; abc → YWJj; byte 251 255 → -_8 (thay + / bằng - _)")
    rec("L03", all(len(b64u(bytes(n))) == alg.bnx_b64u_len(n) == ((4 * n + 2) // 3) for n in range(0, 100)) and alg.bnx_b64u_len(27) == 36,
        "công thức độ dài base64url khớp bộ mã tự dựng với mọi n < 100; 27 byte → 36 ký tự (đáp án câu 1)")
    hq = b'{"alg":"HS256","typ":"JWT"}'
    rec("L03", len(hq) == 27 and len(b64u(hq)) == 36, "câu 1: phần đầu {\"alg\":\"HS256\",\"typ\":\"JWT\"} dài 27 byte → 36 ký tự")
    # ④ sửa 1 ký tự
    p2 = p.replace(b"1300", b"9300")
    diff = sum(1 for a, b in zip(p, p2) if a != b)
    sig2 = b64u(hmac256(k, (hd + "." + b64u(p2)).encode()))
    rec("L03", diff == 1 and len(p2) == len(p) and sig2 != RFC and alg.bnx_jwt_tamper().split(".")[2] == RFC
        and verify(alg.bnx_jwt_tamper(), k, "api-a", 1300819379) == "chữ ký sai",
        "④ sửa đúng 1 byte (1300→9300) thì chữ ký tính lại khác; giữ chữ ký cũ → chữ ký sai")
    # ⑤ ngày giờ
    rec("L03", civil(1300819380) == (2011, 3, 22, 18, 43, 0) and alg.bnx_utc(1300819380) == "2011-03-22 18:43:00",
        "⑤ 1300819380 = 22/3/2011 18:43:00 UTC (đếm ngày thuần)")
    rec("L03", civil(9300819380)[0] == 2264 and alg.bnx_utc(9300819380)[:4] == "2264", "hook: 9300819380 rơi vào năm 2264")
    # năm ca thử: bộ kiểm tự dựng so với alg
    none = b64u(b'{"alg":"none"}') + "." + bd + "."
    ma2 = b64u(h) + "." + b64u(b'{"iss":"joe","aud":"api-a","exp":1300819380}')
    ma2 += "." + b64u(hmac256(k, ma2.encode()))
    mine = [verify(hd + "." + bd + "." + sig, k, "api-a", int(time.time())), verify(alg.bnx_jwt_tamper(), k, "api-a", 1300819379),
            verify(none, k, "api-a", 0), verify(ma2, k, "api-a", 1300819379), verify(ma2, k, "api-b", 1300819379)]
    rec("L03", mine == alg.bnx_jwt_cases(time.time()) == ["hết hạn", "chữ ký sai", "thuật toán lạ", "nhận", "sai người phát hành/nhận"],
        f"năm ca thử (bộ kiểm tự dựng = alg): {mine}")
    rec("L03", verify(hd + "." + bd + "." + sig, k, None, 1300819379) == "nhận" and verify(hd + "." + bd + "." + sig, k, None, 1300819380) == "hết hạn"
        and alg.bnx_exp_ok(1300819380, 1300819379) and not alg.bnx_exp_ok(1300819380, 1300819380),
        "giây biên exp (RFC 7519 §4.1.4): 1300819379 nhận, 1300819380 từ chối")
    rec("L03", (300 - 60, 3600 - 60, 3600 // 300, 64 * 43) == (alg.bnx_risk_window(300, 60), alg.bnx_risk_window(3600, 60), 12, 2752)
        and (240, 3540) == (alg.bnx_risk_window(300, 60), alg.bnx_risk_window(3600, 60)),
        "thu hồi: hở 240 s (hạn 300) và 3540 s (hạn 3600); 12 lần xin mã mỗi giờ; 64 · 43 = 2752")
    # openssl thật, gọi thẳng (không shell)
    ossl = shutil.which("openssl")
    if not ossl:
        rec("L03", None, "thiếu openssl")
    else:
        r = subprocess.run([ossl, "dgst", "-sha256", "-mac", "HMAC", "-binary", "-macopt", "hexkey:" + k.hex()],
                           input=(hd + "." + bd).encode(), capture_output=True)
        rec("L03", r.returncode == 0 and b64u(r.stdout) == RFC, "openssl dgst -mac HMAC thật cho cùng chữ ký RFC")
    # chạy NGUYÊN VĂN các khối mã trên màn hình
    rc, so = run_py("\n".join(x.strip("\n") for x in (src.PY_DATA, src.PY_SIGN)) + "\n")
    rec("L03", rc == 0 and so.split() == [hd, bd, RFC] and screen_matches(src.OUT_SIGN, so), "khối ký chạy thật: in đúng ba phần; màn hình khớp đầu ra")
    rc, so = run_py("\n".join(x.strip("\n") for x in (src.PY_DATA, src.PY_SIGN, src.PY_READ)) + "\n")
    rec("L03", rc == 0 and screen_matches(src.OUT_READ, so) and "2011-03-22 18:43:00" in so, "khối đọc phần thân chạy thật: không cần khoá; màn hình khớp")
    rc, so = run_py("\n".join(x.strip("\n") for x in (src.PY_DATA, src.PY_SIGN, src.PY_CHECK, src.PY_CASES)) + "\n")
    rec("L03", rc == 0 and so.strip().split("\n")[3:] == mine and screen_matches(src.OUT_CASES, so), "khối năm ca thử chạy thật = bộ kiểm tự dựng; màn hình khớp")
    bash = shutil.which("bash")
    if not bash:
        rec("L03", None, "thiếu bash")
    else:
        with tempfile.TemporaryDirectory() as d:
            Path(d, "k.sh").write_text(src.SH_OPENSSL.strip("\n") + "\n", encoding="utf-8", newline="\n")
            r = subprocess.run([bash, "k.sh"], cwd=d, capture_output=True, text=True)
        rec("L03", r.returncode == 0 and r.stdout.split("\n")[:2] == [RFC, "2011-03-22 18:43:00"] and screen_matches(src.OUT_OPENSSL, r.stdout),
            "khối bash (openssl + date) chạy nguyên văn: cùng chữ ký và ngày; màn hình khớp")
    lines = [l for c in (src.PY_DATA, src.PY_SIGN, src.PY_READ, src.PY_CHECK, src.PY_CASES, src.SH_OPENSSL) for l in c.strip("\n").split("\n")]
    rec("L03", max(map(len, lines)) <= 70 and all(len(c.strip("\n").split("\n")) <= 12 for c in (src.PY_DATA, src.PY_SIGN, src.PY_READ, src.PY_CHECK, src.PY_CASES, src.SH_OPENSSL)),
        f"khối mã ≤ 12 dòng, dòng dài nhất {max(map(len, lines))} ký tự (≤ 70)")
