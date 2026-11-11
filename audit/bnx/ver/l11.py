"""Kiểm độc lập BNX L11 — tính lại bằng đường KHÁC checklib (số nguyên theo xu, thử hết 100 cặp số kiểm, chạy thật mã trên
màn hình, phân tích XML bằng xml.etree) rồi đối chiếu với alg.bnx_* mà `checks:` dùng."""
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402
import l11 as L  # noqa: E402


def _run_py(code):
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", "-c", code], capture_output=True, text=True,
                       encoding="utf-8", timeout=60)
    return r.returncode, r.stdout.replace("\r\n", "\n").strip("\n"), r.stderr


def _iban_rem_chunked(iban):
    """Đường khác: bảng chữ → số tự lập (không dùng int(c, 36), không dùng ord), lấy dư theo khúc 9 chữ số."""
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s = iban[4:] + iban[:4]
    digits = "".join(c if c in "0123456789" else str(10 + alpha.index(c)) for c in s)
    rem = 0
    for i in range(0, len(digits), 9):
        rem = int(str(rem) + digits[i:i + 9]) % 97
    return rem


def run(rec):
    C = "L11"
    iban = "GB82WEST12345698765432"
    # 1. mã IBAN trên màn hình chạy nguyên văn
    rc, so, se = _run_py(L.IBAN_PY)
    rec(C, rc == 0 and so == L.IBAN_OUT, f"chạy IBAN_PY: stdout {so.splitlines()} khớp IBAN_OUT")
    rem = _iban_rem_chunked(iban)
    rec(C, rem == 1 == alg.bnx_iban_mod97(iban), f"IBAN mẫu dư {rem} (khúc 9 chữ số) = alg.bnx_iban_mod97 = 1")
    rec(C, so.splitlines()[1] == alg.bnx_iban_digits(iban), "chuỗi 28 chữ số máy in = alg.bnx_iban_digits")
    # số kiểm: thử hết 00..99, chỉ đúng một cặp cho dư 1
    ok = [f"{k:02d}" for k in range(100) if _iban_rem_chunked("GB" + f"{k:02d}" + iban[4:]) == 1]
    rec(C, ok == ["82"] and alg.bnx_iban_check_digits("GB", iban[4:]) == ("82", 16),
        f"thử 100 cặp số kiểm: chỉ {ok} cho dư 1; 98 − 16 = 82 khớp alg")
    rec(C, _iban_rem_chunked("GB82WEST12345698765423") == 49 == alg.bnx_iban_mod97("GB82WEST12345698765423"),
        "đổi chỗ hai chữ số cuối: dư 49 (hai đường khớp)")
    # bảng chữ cái: W E S T G B
    rec(C, ["ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(c) + 10 for c in "WESTGB"] == [32, 14, 28, 29, 16, 11],
        "W=32, E=14, S=28, T=29, G=16, B=11")
    # 2. đường khác trên màn hình: chia từng chữ số
    rc, so, _ = _run_py(L.MOD_PY)
    rec(C, rc == 0 and so == L.MOD_OUT == "1", "chạy MOD_PY: in 1")
    # 3. đổi tiền và phí: tính bằng số nguyên theo xu (đường khác Decimal)
    rc, so, _ = _run_py(L.FX_PY)
    rec(C, rc == 0 and so == L.FX_OUT, f"chạy FX_PY: {so.splitlines()}")
    cents, rate = 1000 * 100, 25400
    vnd = cents * rate // 100
    rec(C, cents * rate % 100 == 0 and vnd == 25400000 == alg.bnx_fx_vnd("1000", "25400"), "1 000 USD × 25 400 = 25 400 000 đồng")

    def fee_cents(a, opt, s, i):
        pay, get = a, a
        for who, f in (("gửi", s), ("trung gian", i)):
            if opt == "OUR" or (opt == "SHA" and who == "gửi"):
                pay += f
            else:
                get -= f
        return pay, get
    for opt, want in (("SHA", (100500, 98500)), ("OUR", (102000, 100000)), ("BEN", (100000, 98000))):
        p, g = fee_cents(100000, opt, 500, 1500)
        a = alg.bnx_fee(1000, opt, 5, 15)
        rec(C, (p, g) == want and int(a[0] * 100) == p and int(a[1] * 100) == g,
            f"{opt}: người gửi trả {p / 100:.2f}, người nhận {g / 100:.2f} USD (theo xu) = alg")
    rec(C, 102000 * rate // 100 == 25908000 == alg.bnx_fx_vnd(alg.bnx_fee(1000, "OUR", 5, 15)[0], 25400)
        and 25908000 - 25400000 == 508000, "OUR: 1 020 USD = 25 908 000 đồng, hơn 508 000")
    rec(C, fee_cents(100000, "SHA", 0, 1500)[1] == 98500, "SHA không phí ngân hàng gửi: người nhận 985,00")
    rec(C, 250000 * rate // 100 == 63500000 == alg.bnx_fx_vnd(2500, 25400)
        and fee_cents(250000, "SHA", 0, 2000)[1] == 248000 == int(alg.bnx_fee(2500, "SHA", 0, 20)[1] * 100),
        "quiz 2: 63 500 000 đồng; người nhận 2 480 USD")
    # 4. bút toán nostro: cân theo từng đồng tiền (cộng tay)
    ent = alg.bnx_nostro_entries("1000", "25400")
    by = {}
    for ccy, _a, dr, cr in ent:
        by.setdefault(ccy, [0, 0])
        by[ccy][0] += dr
        by[ccy][1] += cr
    rec(C, by == {"VND": [25400000, 25400000], "USD": [1000, 1000]}, f"bút toán: tổng Nợ = tổng Có từng đồng tiền {by}")
    # 5. số thực
    rc, so, _ = _run_py(L.FLOAT_PY)
    rec(C, rc == 0 and so == L.FLOAT_OUT, f"chạy FLOAT_PY: {so.splitlines()}")
    from decimal import Decimal
    rec(C, str(Decimal(2.675)).startswith("2.67499"), "2.675 lưu dạng nhị phân là 2.67499… (vì vậy round ra 2.67)")
    # 6. XML pacs.008 rút gọn: phân tích thật
    root = ET.fromstring(L.PACS008_XML)
    amt = root.find("CdtTrfTxInf/IntrBkSttlmAmt")
    bic = root.find("CdtTrfTxInf/CdtrAgt/FinInstnId/BICFI").text
    rec(C, root.tag == "FIToFICstmrCdtTrf" and root.find("GrpHdr/MsgId").text == "MSG-0001"
        and amt.get("Ccy") == "USD" and amt.text == "1000.00" and len(amt.text.split(".")[1]) == alg.bnx_minor_units("USD")
        and root.find("CdtTrfTxInf/ChrgBr").text in {"DEBT", "CRED", "SHAR"} and root.find("CdtTrfTxInf/ChrgBr").text == "SHAR",
        "XML pacs.008 rút gọn: phân tích được; Ccy=USD, 1000.00 (2 chữ số lẻ), ChrgBr=SHAR")
    m = re.fullmatch(r"([A-Z0-9]{4})([A-Z]{2})([A-Z0-9]{2})([A-Z0-9]{3})?", bic)
    rec(C, m is not None and alg.bnx_bic_parts(bic) == {"to_chuc": m[1], "quoc_gia": m[2], "dia_diem": m[3], "chi_nhanh": m[4] or "XXX"}
        and alg.bnx_bic_parts("WESTGB2LXXX")["chi_nhanh"] == "XXX", f"BIC {bic}: 4+2+2(+3) qua biểu thức chính quy = alg")
    rec(C, all(len(l) <= 70 for t in (L.IBAN_PY, L.MOD_PY, L.FX_PY, L.FLOAT_PY, L.PACS008_XML) for l in t.split("\n"))
        and all(len(t.split("\n")) <= 12 for t in (L.IBAN_PY, L.MOD_PY, L.FX_PY, L.FLOAT_PY, L.PACS008_XML)),
        "mọi khối mã ≤ 12 dòng, dòng ≤ 70 ký tự")
