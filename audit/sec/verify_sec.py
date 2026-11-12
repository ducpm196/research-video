"""Kiểm độc lập mọi khẳng định của khoá SEC — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Mật khẩu: PBKDF2 tự cài theo RFC 8018 (chỉ dùng hmac). TOTP: vector chính thức RFC 6238 (phụ lục B). HMAC: tự cài ipad/opad theo RFC 2104,
vector RFC 4231 ca 2. CRC-32: binascii thay zlib. Chứng chỉ: sympy kiểm số nguyên tố, nghịch đảo khoá. Ngày sinh: tích chính xác + Monte Carlo.
Ngẫu nhiên hoá địa chỉ: Monte Carlo cả hai mô hình (giữ nguyên bố trí / bố trí lại). Báo động: Fraction + mô phỏng 10⁶ sự kiện.
Chạy: .venv/Scripts/python audit/sec/verify_sec.py → PASS/FAIL từng dòng và tổng."""
import binascii
import hashlib
import hmac
import html
import math
import sqlite3
import struct
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []
rng = np.random.default_rng(2026)


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


def my_hmac(key, msg, hf=hashlib.sha256):
    """HMAC theo RFC 2104, tự cài: H((K ⊕ opad) ‖ H((K ⊕ ipad) ‖ m))."""
    bs = hf().block_size
    if len(key) > bs:
        key = hf(key).digest()
    key = key.ljust(bs, b"\0")
    ipad = bytes(k ^ 0x36 for k in key)
    opad = bytes(k ^ 0x5C for k in key)
    return hf(opad + hf(ipad + msg).digest()).digest()


def my_pbkdf2(pw, salt, it, dklen=32):
    """PBKDF2-HMAC-SHA256 theo RFC 8018 mục 5.2, tự cài (một khối vì dklen = 32)."""
    u = my_hmac(pw, salt + struct.pack(">I", 1))
    t = bytearray(u)
    for _ in range(it - 1):
        u = my_hmac(pw, u)
        t = bytearray(a ^ b for a, b in zip(t, u))
    return bytes(t[:dklen])


# ── L00: STRIDE — 6 mối đe doạ, mỗi mối đúng một tính chất bị vi phạm ──
props = [p for _, p in alg.STRIDE]
rec("L00a", len(alg.STRIDE) == 6 and len(set(props)) == 6 and dict(alg.STRIDE)["lộ thông tin"] == "bí mật", "STRIDE: 6 mối đe doạ ↔ 6 tính chất khác nhau")

# ── L01: thời gian vét, muối ──
rec("L01a", Fraction(26 ** 8, 10 ** 10) == Fraction(208827064576, 10 ** 10) and round(float(Fraction(26 ** 8, 10 ** 10)), 1) == 20.9
    and round(26 ** 8 / 10 ** 4 / 86400) == 242 and round(62 ** 10 / 1e10 / 86400 / 365) == 3 and 10 ** 6 / 10 ** 10 * 1e6 == 100,
    "26⁸ = 208 827 064 576; 20,9 giây ở 10¹⁰/s; 242 ngày ở 10⁴/s; 62¹⁰: 3 năm; 10⁶: 100 micro giây")
pa, pb = my_pbkdf2(b"matkhau123", b"muoi-A", 1000).hex()[:16], my_pbkdf2(b"matkhau123", b"muoi-B", 1000).hex()[:16]
rec("L01b", (pa, pb) == ("da5a72b54dd74dba", "6967938f6d0f7237") == (alg.hash_password("matkhau123", b"muoi-A", 1000), alg.hash_password("matkhau123", b"muoi-B", 1000)),
    "PBKDF2 tự cài (RFC 8018) trùng hashlib: cùng mật khẩu, muối khác → mã băm khác")

# ── L02: entropy ──
rec("L02a", [round(math.log2(n ** k), 1) for n, k in ((26, 8), (7776, 4), (62, 12), (10, 4), (7776, 6))] == [37.6, 51.7, 71.5, 13.3, 77.5]
    == [round(alg.entropy_bits(n, k), 1) for n, k in ((26, 8), (7776, 4), (62, 12), (10, 4), (7776, 6))] and 6 ** 5 == 7776 and 2 ** 14 == 16384,
    "log₂ của cỡ không gian: 37,6 / 51,7 / 71,5 / 13,3 / 77,5 bit; 7776 = 6⁵")

# ── L03: TOTP theo vector RFC 6238 phụ lục B (SHA-1, 8 chữ số) ──
seed = b"12345678901234567890"
rfc = {59: "94287082", 1111111109: "07081804", 1111111111: "14050471", 1234567890: "89005924", 2000000000: "69279037"}
rec("L03a", all(alg.totp(seed, t, digits=8) == v for t, v in rfc.items()) and [alg.totp(seed, t) for t in (59, 60, 89, 90)] == ["287082", "359152", "359152", "969429"]
    and alg.totp(seed, 59) == rfc[59][-6:], "5 vector RFC 6238 khớp; 6 chữ số = 6 chữ số cuối; t = 60 và 89 cùng ô 30 giây")
p_guess = 1 - (1 - Fraction(1, 10 ** 6)) ** 2880
rec("L03b", round(float(p_guess), 4) == 0.0029 and round(1 - 0.999 ** 2880, 2) == 0.94 and math.isclose(5 * 10 / 10 ** 6, 5e-5) and round(1 - (1 - 3e-6) ** 1000, 4) == 0.003,
    "đoán 1 mã/lần: 1 − 0,999²⁸⁸⁰ = 0,94 khi không giới hạn 1000 lần/30 giây; giới hạn 3 lần × 1000 tài khoản = 0,3%")

# ── L04: phân quyền — dựng ma trận quyền bằng sqlite, truy vấn JOIN ──
con = sqlite3.connect(":memory:")
con.executescript("CREATE TABLE ur(u, r); CREATE TABLE rp(r, res, act);")
con.executemany("INSERT INTO rp VALUES (?,?,?)", [(r, res, a) for r, ps in alg.RBAC.items() for res, a in ps])
def can(roles, res, act):  # noqa: E302
    q = "SELECT COUNT(*) FROM rp WHERE r IN (%s) AND res = ? AND act = ?" % ",".join("?" * len(roles))
    return con.execute(q, (*roles, res, act)).fetchone()[0] > 0
cases = [(["ke_toan"], "tạo"), (["kiem_toan"], "tạo"), (["ke_toan"], "duyệt"), (["kiem_toan", "ke_toan"], "tạo"), (["kiem_toan"], "duyệt")]
rec("L04a", [can(r, "hoa_don", a) for r, a in cases] == [True, False, False, True, False] == [alg.rbac_allowed(r, "hoa_don", a) for r, a in cases],
    "sqlite JOIN vai trò–quyền trùng alg.rbac_allowed trên 5 ca")
logs = ([("lan", "tạo", "HD1"), ("minh", "duyệt", "HD1"), ("lan", "tạo", "HD2"), ("lan", "duyệt", "HD2")],
        [("an", "tạo", "HD7"), ("an", "duyệt", "HD8"), ("binh", "tạo", "HD8"), ("binh", "duyệt", "HD7")])
brute = [sorted({i for u, a, i in L if a == "duyệt" and any(u2 == u and a2 == "tạo" and i2 == i for u2, a2, i2 in L)}) for L in logs]
rec("L04b", brute == [["HD2"], []] == [alg.sod_violation(L) for L in logs], "tách bạch nhiệm vụ: HD2 vi phạm; ca chéo người không vi phạm")

# ── L05: bảng chân trị SameSite theo RFC 6265bis mục 5.4.7 (Strict: chỉ cùng trang; Lax: thêm điều hướng GET cấp cao; None: luôn gửi) ──
def sent_spec(cross, method, ss):  # noqa: E302
    return {"Strict": not cross, "Lax": (not cross) or method == "GET", "None": True}[ss]
ok5 = all(alg.csrf_check("la.vn" if c else "nganhang.vn", "nganhang.vn", m, ss, tk) == (sent_spec(c, m, ss), sent_spec(c, m, ss) and tk)
          for c in (True, False) for m in ("GET", "POST") for ss in ("Strict", "Lax", "None") for tk in (True, False))
rec("L05a", ok5 and alg.csrf_check("la.vn", "nganhang.vn", "POST", "Lax", True) == (False, False) and alg.csrf_check("la.vn", "nganhang.vn", "GET", "Lax", True) == (True, True),
    "24 tổ hợp trùng bảng chân trị; POST chéo trang với Lax: không gửi cookie; GET chéo trang với Lax: vẫn gửi")

# ── L06: chèn truy vấn — sqlite3 thật, bảng riêng; mã hoá đầu ra — tự thay thực thể ──
con2 = sqlite3.connect(":memory:")
con2.executescript("CREATE TABLE users(name TEXT, pw TEXT); INSERT INTO users VALUES ('alice','a1'),('bob','b2');")
inj = "x' OR '1'='1"
n_concat = len(con2.execute(f"SELECT name FROM users WHERE name = '{inj}'").fetchall())
n_param = len(con2.execute("SELECT name FROM users WHERE name = ?", (inj,)).fetchall())
n_ok = len(con2.execute("SELECT name FROM users WHERE name = ?", ("alice",)).fetchall())
rec("L06a", (n_concat, n_param, n_ok) == (2, 0, 1) and alg.sql_concat_vs_param(inj)[1:] == (2, 0) and alg.sql_concat_vs_param("bob")[1:] == (1, 1),
    "ghép chuỗi trả 2 dòng (mọi người), tham số hoá trả 0; tên đúng trả 1")
esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#x27;")  # noqa: E731
rec("L06b", all(esc(s) == alg.render_safe(s) == html.escape(s) for s in ("<script>alert(1)</script>", "<b>An</b>", "O'Brien")),
    "thay thực thể tự cài trùng html.escape trên 3 chuỗi")

# ── L07: chế độ mã — tính chất cấu trúc kiểm trên 200 khoá ngẫu nhiên ──
blk = [b"TRA 100K", b"CHO  LAN", b"TRA 100K"]
ok7 = True
for _ in range(200):
    k, nonce = rng.bytes(16), rng.bytes(4)
    e = alg.ecb_encrypt(k, blk)
    c = alg.ctr_like(k, nonce, blk)
    p1, p2 = b"LUONG 9M", b"LUONG 5M"
    c1, c2 = alg.ctr_like(k, nonce, [p1])[0], alg.ctr_like(k, nonce, [p2])[0]
    ok7 &= e[0] == e[2] != e[1] and c[0] != c[2] and bytes(a ^ b for a, b in zip(c1, c2)) == bytes(a ^ b for a, b in zip(p1, p2))
    ok7 &= alg.ctr_like(k, nonce, alg.ctr_like(k, nonce, blk)) == blk  # giải mã = mã lại
x = bytes(a ^ b for a, b in zip(b"LUONG 9M", b"LUONG 5M"))
rec("L07a", ok7 and x.hex() == "0000000000000c00" and x[:6] == b"\0" * 6 and x[6] != 0 and x[7] == 0
    and [v.hex()[:8] for v in alg.ecb_encrypt(b"khoa-bi-mat", blk)] == [hashlib.sha256(b"khoa-bi-mat" + b).hexdigest()[:8] for b in blk],
    "200 khoá: ECB lặp khối 1 = khối 3, kiểu bộ đếm không lặp; dùng lại số dùng một lần → XOR bản mã = XOR bản rõ; 6 byte đầu trùng, khác ở byte thứ 7")

# ── L08: toàn vẹn — CRC-32 bằng binascii, HMAC tự cài, vector RFC 4231 ca 2 ──
rfc4231 = my_hmac(b"Jefe", b"what do ya want for nothing?").hex()
crc = [format(binascii.crc32(m) & 0xFFFFFFFF, "08x") for m in (b"chuyen 100", b"chuyen 900")]
tags = [my_hmac(k, m).hex()[:16] for k, m in ((b"khoa-chung", b"chuyen 100"), (b"khoa-chung", b"chuyen 900"), (b"khoa-khac", b"chuyen 100"))]
rec("L08a", rfc4231 == "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843" and crc == ["a19e8fb6", "af8dde0e"]
    and tags == ["06c6f7f2f943b79e", "bfa8cd7e9747cb9d", "8b59fe333ac89816"] == [alg.hmac_tag(b"khoa-chung", b"chuyen 100"), alg.hmac_tag(b"khoa-chung", b"chuyen 900"), alg.hmac_tag(b"khoa-khac", b"chuyen 100")],
    "HMAC tự cài qua vector RFC 4231; CRC-32 (binascii) a19e8fb6 / af8dde0e; 3 mã xác thực khớp alg")

# ── L09: chứng chỉ — khoá đồ chơi hợp lệ (sympy), chuỗi đúng / bị sửa / thiếu gốc / thiếu trung gian ──
okk = all(sympy.isprime(p) and sympy.isprime(q) and math.gcd(e, (p - 1) * (q - 1)) == 1
          and (alg.toy_key(n)[1] * alg.toy_key(n)[2]) % sympy.totient(p * q) == 1 for n, (p, q, e) in alg.TOY_KEYS.items())
chain, roots = alg.toy_cert_chain()
bad, _ = alg.toy_cert_chain(True)
rec("L09a", okk and alg.chain_verify(chain, roots) == (True, "hợp lệ") and alg.chain_verify(bad, roots)[0] is False
    and alg.chain_verify(chain, {})[0] is False and alg.chain_verify(chain[:1], roots)[0] is False,
    "sympy: p, q nguyên tố, e·d ≡ 1 (mod φ); chuỗi đúng hợp lệ; sửa tên, thiếu gốc, thiếu trung gian đều bị từ chối")

# ── L10: ngày sinh — tích chính xác; Monte Carlo ở 20 bit; công thức ──
p23 = 1 - math.prod(Fraction(365 - i, 365) for i in range(23))
n20 = alg.birthday_n(20)
mc = np.mean([len(np.unique(rng.integers(0, 2 ** 20, round(n20)))) < round(n20) for _ in range(4000)])
rec("L10a", round(float(p23), 3) == 0.507 and math.comb(23, 2) == 253 and abs(mc - 0.5) < 0.03
    and round(alg.birthday_n(64) / 1e9, 2) == 5.06 and round(alg.birthday_n(128) / 1e19, 2) == 2.17 and round(alg.birthday_n(32)) == 77163
    and round(math.sqrt(2 * math.log(2)), 2) == 1.18,
    f"23 người: 50,7% (tích chính xác), 253 cặp; Monte Carlo 20 bit với n = {round(n20)}: {mc:.3f} ≈ 0,5; 64 bit: 5,06 tỉ; 32 bit: 77 163")
rec("L10b", round(alg.collision_prob(1e9, 64), 4) == 0.0267 and round(alg.collision_prob(1e5, 32), 2) == 0.69
    and round(-math.expm1(-(10 ** 5) * (10 ** 5 - 1) / 2 / 2 ** 32), 2) == 0.69, "64 bit, 10⁹ giá trị: 2,67%; 32 bit, 10⁵ tệp: 69% (cả n(n−1)/2)")

# ── L11: ngẫu nhiên hoá địa chỉ — Monte Carlo cả hai mô hình ──
N = 2 ** 8
# giữ nguyên bố trí: thử lần lượt theo một thứ tự, không lặp → vị trí của đáp án trong hoán vị; bố trí lại: mỗi lần trúng với xác suất 1/N
keep = np.mean([int(np.where(rng.permutation(N) == rng.integers(N))[0][0]) + 1 for _ in range(20000)])
rerand = np.mean(rng.geometric(1 / N, 20000))
rec("L11a", abs(keep - (N + 1) / 2) < 3 and abs(rerand - N) < 8 and [2 ** b // 2 for b in (16, 28, 8, 19)] == [32768, 134217728, 128, 262144],
    f"8 bit: giữ nguyên bố trí trung bình {keep:.1f} ≈ (2⁸+1)/2; bố trí lại {rerand:.1f} ≈ 2⁸; 2¹⁵ = 32 768, 2²⁷ = 134 217 728, 2¹⁸ = 262 144")

# ── L12: tường lửa — tự cài khớp luật đầu tiên bằng cách khác (lọc rồi lấy phần tử đầu) ──
rules = [("ứng dụng", "csdl", 5432, "cho"), ("*", "web", 443, "cho")]
def fw(rs, s, d, p):  # noqa: E302
    m = [a for (rs_, rd, rp, a) in rs if rs_ in ("*", s) and rd in ("*", d) and rp in ("*", p)]
    return m[0] if m else "chặn"
reqs = [("ứng dụng", "csdl", 5432), ("internet", "csdl", 5432), ("internet", "web", 443), ("internet", "web", 22), ("máy in", "csdl", 5432), ("văn phòng", "web", 443), ("ứng dụng", "csdl", 22)]
bad_rules = [("*", "*", "*", "cho"), ("internet", "csdl", 5432, "chặn")]
rec("L12a", [fw(rules, *r) for r in reqs] == ["cho", "chặn", "cho", "chặn", "chặn", "cho", "chặn"] == [alg.firewall(rules, *r) for r in reqs]
    and fw(bad_rules, "internet", "csdl", 5432) == alg.firewall(bad_rules, "internet", "csdl", 5432) == "cho", "7 yêu cầu khớp; luật “cho tất cả” đặt đầu làm luật chặn vô dụng")

# ── L13: tỉ lệ nền — Fraction chính xác và mô phỏng 10⁶ sự kiện ──
def ppv(t, f, b):  # noqa: E302
    return t * b / (t * b + f * (1 - b))
fr = ppv(Fraction(99, 100), Fraction(1, 100), Fraction(1, 10 ** 4))
ev = rng.random(10 ** 6) < 1e-4
alert = np.where(ev, rng.random(10 ** 6) < 0.99, rng.random(10 ** 6) < 0.01)
sim = ev[alert].mean()
rec("L13a", fr == Fraction(99, 10098) and round(float(fr) * 100, 2) == 0.98 == round(alg.alert_precision(0.99, 0.01, 1e-4) * 100, 2)
    and round(float(ppv(Fraction(99, 100), Fraction(1, 1000), Fraction(1, 10 ** 4))) * 100, 1) == 9.0 and ppv(Fraction(99, 100), Fraction(1, 100), Fraction(1, 100)) == Fraction(1, 2)
    and abs(sim - 0.0098) < 0.003, f"99/(99 + 9 999) = 0,98%; báo nhầm 0,1% → 9,0%; nền 1% → 50%; mô phỏng 10⁶ sự kiện: {sim * 100:.2f}%")

# ── L14: sao lưu 3-2-1 + bản không ghi đè được — tự cài bằng đếm ──
def b321(c):  # noqa: E302
    return [len(c) >= 3, len(set(m for m, _, _ in c)) >= 2, sum(w != "tại chỗ" for _, w, _ in c) >= 1, sum(bool(r) for _, _, r in c) >= 1]
plans = [[("đĩa", "tại chỗ", False), ("đĩa", "tại chỗ", False)],
         [("đĩa", "tại chỗ", False), ("đĩa", "tại chỗ", False), ("đám mây", "vùng khác", False)],
         [("đĩa", "tại chỗ", False), ("băng", "kho khác", True), ("đám mây", "vùng khác", True)],
         [("đĩa", "tại chỗ", False), ("đám mây", "vùng khác", False), ("đám mây", "vùng khác 2", False)]]
rec("L14a", [b321(p) for p in plans] == [[False] * 4, [True, True, True, False], [True] * 4, [True, True, True, False]]
    and [alg.backup_321(p)[0] for p in plans] == [False, False, True, False] and [len(alg.backup_321(p)[1]) for p in plans] == [4, 1, 0, 1],
    "2 bản cùng đĩa: thiếu 4; có đám mây ghi đè được: thiếu 1; đĩa + băng ngoại tuyến + đám mây khoá ghi (2 bản không ghi đè được): đạt")

# ── L15: hành trình HTTPS (nguồn: audit/sec/sources_L15.md) — chỉ khái niệm phòng thủ ──
import datetime as _dt  # noqa: E402


def bounds_ok(declared, received):  # kiểm biên của bản vá [D14] §2.3: bỏ thông điệp nếu độ dài khai báo > dữ liệu thật
    return declared <= received


rec("L15a", struct.calcsize(">H") == 2 and 2 ** (8 * struct.calcsize(">H")) == 65536 == 256 * 256 and 65536 // 1024 == 64
    and bounds_ok(5, 5) and not bounds_ok(6, 5),
    "trường độ dài 2 byte → 2^16 = 65 536 = 256·256 byte ≈ 64 KB; kiểm biên: khai báo ≤ nhận thì dùng, lớn hơn thì bỏ")
rec("L15b", (_dt.date(2014, 4, 7) - _dt.date(2012, 3, 14)).days == 754 == 365 + 365 + (_dt.date(2014, 4, 7) - _dt.date(2014, 3, 14)).days,
    "14/3/2012 (OpenSSL 1.0.1) → 7/4/2014 (công bố): 754 ngày = 365 + 365 + 24")
_n = 1000  # số minh hoạ
_rep = _n * 10 // 100
_keep = _rep * 14 // 100
rec("L15c", (_rep, _keep, _rep - _keep, (_rep - _keep) / _n) == (100, 14, 86, 0.086), "1000 trang → 10% thay chứng chỉ = 100 → 14% giữ khoá = 14 → 86 / 1000 = 8,6%")
rec("L15d", 100 * 178 == 17800 and 20 * 178 == 3560 and Fraction(60, 90) == Fraction(2, 3) and 90 - 60 == 30 and 365 // 60 == 6,
    "100 tên miền × 178 USD = 17 800; 20 × 178 = 3560; 60/90 = 2/3; dự phòng 30 ngày; 6 lần/năm")
rec("L15e", round(538 / 223, 2) == 2.41 and round(1_000_000 / 86_400, 1) == 11.6 and 64 + 16 + 19 == 99 and round(100 - 2.9, 1) == 97.1,
    "538/223 ≈ 2,41 chứng chỉ/tên miền; 1 triệu/ngày ≈ 11,6/s; 64+16+19 = 99%; 97,1% gia hạn kịp")
rec("L15f", Fraction(2, 3) * 45 == 30 and round(float(Fraction(2, 3) * 64), 1) == 42.7 and 60 - 45 == 15 and (365 // 30) / (365 // 60) == 2
    and 45 - 30 == 15 and 3 * 15 == 45,
    "2/3 · 45 = 30; 2/3 · 64 ≈ 42,7; lịch cứng 60 ngày hỏng 15 ngày; 6 → 12 lần/năm; ba phần 15 ngày")

nf =sum(1 for _, ok in R if not ok)
print(f"TỔNG: {len(R) - nf} PASS · {nf} FAIL")
sys.exit(1 if nf else 0)
