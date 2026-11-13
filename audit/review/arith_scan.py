"""E54 (plan AF2): phép tính hiển thị trên màn hình phải đúng với CHÍNH số đang hiện.
Lỗi thật mẫu F: LLM L05 "12,9 + 34,4 = 47,2" (đúng với số đang hiện là 47,3); IRS L11 "(0,631 + 0,431)/2,562 ≈ 41,4%" (ra 41,5%).
Quét `show` của mọi bài: chuỗi dạng  a ± b … = c  gồm toàn số, số kiểu Việt (dấu phẩy thập phân, khoảng trắng ngăn nghìn) hoặc kiểu mã (dấu chấm thập phân).
FAIL khi |tính − c| > nửa đơn vị chữ số cuối của c ("=") hoặc cộng thêm độ chính xác của số hạng ("≈").
Bỏ qua ngữ cảnh có mũ/chỉ số/căn/tổng/phần trăm/ký hiệu mod, log, ẩn số; chuỗi mơ hồ (12,345; 1,234,567).
Dùng: .venv/Scripts/python -B audit/review/arith_scan.py [KHOÁ ...]   — mã thoát 1 nếu có FAIL."""
import html
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
NBSP = chr(160)
MINUS = chr(0x2212)
TIMES = chr(0xD7)
DOT = chr(0xB7)
DIV = chr(0xF7)
APPROX = chr(0x2248)
NUM = r"\d[\d" + NBSP + r" .,]*\d|\d"
OP = "[+\\-" + MINUS + TIMES + DOT + "*/" + DIV + "]"
EQ = re.compile("((?:\\(\\s*)*(?:" + NUM + ")(?:\\s*(?:\\)\\s*)*" + OP + "\\s*(?:\\(\\s*)*(?:" + NUM + "))+(?:\\s*\\))*)\\s*(=|" + APPROX + ")\\s*(" + NUM + ")(?!\\d)")
SKIP_NEAR = re.compile("[\\^_!%" + chr(0x221A) + chr(0x2211) + chr(0x220F) + chr(0x222B) + "]|mod|log|sqrt|\\bmax\\b|\\bmin\\b|[A-Za-z]\\s*=")


ALLOW_FILE = Path(__file__).with_name("arith_allow.yaml")
ALLOW = set((yaml.safe_load(ALLOW_FILE.read_text(encoding="utf-8")) or {}).get("allow", [])) if ALLOW_FILE.exists() else set()


def clean(show):
    show = re.sub(r"\$\$.*?\$\$|\$[^$]*\$", " \u0000 ", show, flags=re.S)       # bỏ công thức KaTeX: chỉ quét chữ/bảng thường
    t = re.sub(r"<sup[^>]*>(.*?)</sup>", lambda m: "^" + m.group(1) + " ", show, flags=re.S)
    t = re.sub(r"<sub[^>]*>(.*?)</sub>", lambda m: "_" + m.group(1) + " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    for a, b in (("\\,", ""), ("\\;", " "), ("\\ ", " "), ("\\hl{", ""), ("\\times", TIMES), ("\\cdot", DOT), ("\\div", DIV),
                 ("\\approx", APPROX), ("\\frac", ""), ("$", " ")):
        t = t.replace(a, b)
    return re.sub(r"[{}]", " ", t)


def parse(tok):
    """Số → (Decimal, số chữ số thập phân) hoặc None nếu mơ hồ."""
    s = tok.replace(NBSP, " ").strip()
    if re.fullmatch(r"\d{1,3}(,\d{3})+", s) or re.fullmatch(r"\d+,\d{3}", s):
        return None                                   # 1,234,567 hoặc 12,345: mơ hồ
    if " " in s:
        if not re.fullmatch(r"\d{1,3}( \d{3})+(,\d+)?", s):
            return None
        s = s.replace(" ", "")
    elif re.fullmatch(r"\d{1,3}(\.\d{3}){2,}(,\d+)?", s):
        s = s.replace(".", "")                        # 1.234.567
    elif re.fullmatch(r"\d+\.\d{3}", s):
        return None                                   # 33.333 mơ hồ (nghìn hay thập phân)
    if s.count(",") > 1 or s.count(".") > 1 or ("," in s and "." in s):
        return None
    s = s.replace(",", ".")
    try:
        d = Decimal(s)
    except InvalidOperation:
        return None
    return d, (len(s.split(".")[1]) if "." in s else 0)


def evaluate(expr):
    out, infos, last = [], [], 0
    for m in re.finditer(NUM, expr):
        pr = parse(m.group(0))
        if pr is None:
            return None
        out.append(expr[last:m.start()])
        out.append("Decimal('" + str(pr[0]) + "')")
        infos.append(pr[1])
        last = m.end()
    out.append(expr[last:])
    py = "".join(out).replace(MINUS, "-").replace(TIMES, "*").replace(DOT, "*").replace(DIV, "/")
    if re.search(r"[^\dDecimal()'.+\-*/ ]", py.replace("Decimal", "")):
        return None
    try:
        return eval(py, {"Decimal": Decimal}), infos
    except Exception:
        return None


def main():
    want = {a.upper() for a in sys.argv[1:] if not a.startswith("--")}
    bad = tot = 0
    for f in sorted((ROOT / "lessons").glob("*/L*.yaml")):
        if want and f.parent.name.upper() not in want:
            continue
        spec = yaml.safe_load(f.read_text(encoding="utf-8"))
        for sc in spec.get("scenes") or []:
            for si, st in enumerate(sc.get("steps") or []):
                text = clean(str(st.get("show", "")))
                for m in EQ.finditer(text):
                    before = text[:m.start()].rstrip()[-1:]
                    after = text[m.end():].lstrip()[:1]
                    if (before and before in "+-*/=^._(" + MINUS + TIMES + DOT + DIV + APPROX) or (after and after in "+-*/=^(%" + MINUS + TIMES + DOT + DIV + APPROX + "0123456789,"):
                        continue                                  # chuỗi đẳng thức nối tiếp, hoặc kết quả bị cắt
                    if text[m.end():].lstrip().startswith(("đến", "tới", "hoặc")):
                        continue                                  # khoảng giá trị: 700 đến 850
                    key = f"{f.parent.name.upper()}/{f.name[:3]}: {m.group(1).strip()} {m.group(2)} {m.group(3)}".replace(NBSP, " ")
                    if key in ALLOW:
                        continue
                    if SKIP_NEAR.search(text[max(0, m.start() - 4): m.end() + 4]):
                        continue
                    expr, rel, rhs = m.group(1).strip(), m.group(2), m.group(3)
                    pr, ev = parse(rhs), evaluate(expr)
                    if pr is None or ev is None:
                        continue
                    val, infos = ev
                    c, dec = pr
                    tot += 1
                    tol = Decimal(1) / (Decimal(10) ** dec) / 2
                    if rel == APPROX and infos:
                        tol += sum(Decimal(1) / (Decimal(10) ** i) / 2 for i in infos)
                    if abs(val - c) > tol:
                        bad += 1
                        shown = f"{val:.6g}"
                        print(f"FAIL {f.parent.name.upper()}/{f.name[:3]} {sc.get('id')}#{si}: “{expr} {rel} {rhs}” — tính ra {shown} (lệch {abs(val - c):.6g} > {tol:.6g})")
    print(f"arith_scan: {tot} phép tính kiểm được, {bad} FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
