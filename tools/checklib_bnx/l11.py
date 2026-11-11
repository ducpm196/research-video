"""BNX L11 — Thanh toán quốc tế và ngoại tệ: hàm tham chiếu cho `checks:` (chỉ thư viện chuẩn).
Nguồn: [IBAN] ISO 13616 (kiểm mod 97 = 1), [BIC] ISO 9362 (8 hoặc 11 ký tự), [ISO4217] số chữ số lẻ (USD 2, VND 0),
[MT103] trường 71A OUR/SHA/BEN, [P8UG] pacs.008 ChrgBr DEBT/CRED/SHAR — xem audit/bnx/sources.md."""
from decimal import Decimal, ROUND_HALF_UP

# ISO 4217, danh sách một của SIX (Pblshd 2026-09-17): CcyMnrUnts USD = 2, VND = 0
_MINOR = {"USD": 2, "VND": 0}


def bnx_iban_digits(iban):
    """Đưa 4 ký tự đầu ra cuối, đổi chữ thành số (A=10 … Z=35); trả chuỗi chữ số."""
    s = iban.replace(" ", "").upper()
    s = s[4:] + s[:4]
    out = []
    for c in s:
        if c.isdigit():
            out.append(c)
        else:
            out.append(str(ord(c) - ord("A") + 10))
    return "".join(out)


def bnx_iban_mod97(iban):
    """Số dư khi chia chuỗi số của IBAN cho 97 (đúng thì bằng 1)."""
    return int(bnx_iban_digits(iban)) % 97


def bnx_iban_check_digits(country, bban):
    """Tính hai chữ số kiểm: đặt '00' vào chỗ số kiểm, lấy 98 − (số dư mod 97)."""
    r = int(bnx_iban_digits(country + "00" + bban)) % 97
    return f"{98 - r:02d}", r


def bnx_bic_parts(bic):
    """Tách BIC 8 hoặc 11 ký tự: mã tổ chức 4, quốc gia 2, địa điểm 2, chi nhánh 3 (8 ký tự → 'XXX', trụ sở chính)."""
    if len(bic) not in (8, 11) or not bic.isalnum():
        raise ValueError("BIC phải có 8 hoặc 11 ký tự chữ/số")
    if not bic[4:6].isalpha():
        raise ValueError("mã quốc gia là 2 chữ cái")
    return {"to_chuc": bic[:4], "quoc_gia": bic[4:6], "dia_diem": bic[6:8], "chi_nhanh": bic[8:] or "XXX"}


def bnx_minor_units(ccy):
    return _MINOR[ccy]


def bnx_round(x, ccy):
    """Làm tròn theo đơn vị nhỏ nhất của đồng tiền (ISO 4217); quy tắc nửa lên là quy ước của bài (ngân hàng phải viết rõ)."""
    return Decimal(x).quantize(Decimal(1).scaleb(-_MINOR[ccy]), rounding=ROUND_HALF_UP)


def bnx_fx_vnd(usd, rate):
    """Số đồng khách bị trừ khi mua `usd` đô la theo tỉ giá bán `rate` (chuỗi/Decimal, không dùng float)."""
    return int(bnx_round(Decimal(str(usd)) * Decimal(str(rate)), "VND"))


def bnx_fee(amount, option, sender_fee, inter_fee):
    """Phí theo trường 71A / ChrgBr. Trả (đô la người gửi trả, đô la người nhận được).
    OUR (DEBT): người gửi chịu mọi phí; SHA (SHAR): người gửi chịu phí ngân hàng của mình, phí khác trừ vào tiền chuyển;
    BEN (CRED): mọi phí trừ vào tiền chuyển. Phí là số minh hoạ."""
    a, s, i = (Decimal(str(v)) for v in (amount, sender_fee, inter_fee))
    if option == "OUR":
        pay, get = a + s + i, a
    elif option == "SHA":
        pay, get = a + s, a - i
    elif option == "BEN":
        pay, get = a, a - s - i
    else:
        raise ValueError(option)
    return bnx_round(pay, "USD"), bnx_round(get, "USD")


def bnx_nostro_entries(usd, rate):
    """Bút toán ở ngân hàng gửi khi khách mua `usd` đô la và chuyển đi qua tài khoản nostro.
    Mỗi dòng: (đồng tiền, tài khoản, nợ, có). Tên tài khoản là minh hoạ."""
    vnd = bnx_fx_vnd(usd, rate)
    u = bnx_round(usd, "USD")
    return [("VND", "tiền gửi của khách", vnd, 0), ("VND", "mua bán ngoại tệ (VND)", 0, vnd),
            ("USD", "mua bán ngoại tệ (USD)", u, 0), ("USD", "nostro USD tại ngân hàng đại lý", 0, u)]


def bnx_balanced_by_ccy(entries):
    """Tổng nợ − tổng có theo từng đồng tiền (cân thì mọi giá trị bằng 0)."""
    t = {}
    for ccy, _acc, dr, cr in entries:
        t[ccy] = t.get(ccy, 0) + dr - cr
    return t


def bnx_float_demo():
    """Hai lỗi số thực: 0.1 + 0.2 và round(2.675, 2); so với Decimal làm tròn nửa lên."""
    return 0.1 + 0.2, round(2.675, 2), Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
