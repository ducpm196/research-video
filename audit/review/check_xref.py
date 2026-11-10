"""Cổng "bài độc lập": tìm chỗ bài/giáo án tham chiếu sang KHOÁ KHÁC trong phần người học thấy hoặc nghe.

Quy tắc (yêu cầu người dùng 2026-11-09): mỗi video, giáo án, bài học phải tự đứng được; không nói
"như ở khoá X", "đã học ở CS115", "khoá trước"… mà phải giảng lại đủ kỹ ngay trong bài.

Quét:
  - lessons/<k>/L*.yaml: title, objectives, và mọi chuỗi dưới scenes (show, say, quiz, title, …),
    bỏ qua source, checks, asr_reviewed (không hiện/không đọc) và chú thích YAML.
  - curriculum/<k>.yaml: title, objectives, example, fix của từng bài (requires_ext là siêu dữ liệu thứ tự, giữ).
Bắt:
  - mã khoá khác (CS115, DBS, …) đứng riêng; "ACB" chỉ tính khi đi sau chữ "khoá" (ACB còn là tên ngân hàng);
  - "khoá <Tên khoá khác>" (tên lấy từ series của khoá);
  - cụm chung: "khoá trước", "khoá nền", "khoá học trước/khác", "khoá tiên quyết", "các khoá trước/nền/khác/học".
Dùng:
  python -B audit/review/check_xref.py              # tóm tắt theo khoá, exit 1 nếu còn lượt
  python -B audit/review/check_xref.py --course DSC  # liệt kê chi tiết một khoá
  python -B audit/review/check_xref.py --list        # liệt kê toàn bộ
"""
import collections
import glob
import os
import re
import sys

import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
args = sys.argv[1:]
ONLY = args[args.index("--course") + 1].upper() if "--course" in args else None
LIST = "--list" in args or ONLY is not None

NAMES = {}
for d in sorted(glob.glob(os.path.join(ROOT, "lessons", "*"))):
    fs = sorted(glob.glob(os.path.join(d, "L*.yaml")))
    if not fs:
        continue
    y = yaml.safe_load(open(fs[0], encoding="utf-8"))
    code = str(y.get("course") or os.path.basename(d).upper())
    s = str(y.get("series", ""))
    NAMES[code] = s.split("·", 1)[-1].strip() if "·" in s else ""
CODES = sorted(NAMES, key=len, reverse=True)

code_rx = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(CODES) + r")(?![A-Za-z0-9_])")
UP = "A-ZĐÂĂÊÔƠƯÁÀẢÃẠÉÈẺẼẸÍÌỈĨỊÓÒỎÕỌÚÙỦŨỤÝỲỶỸỴẤẦẨẪẬẮẰẲẴẶẾỀỂỄỆỐỒỔỖỘỚỜỞỠỢỨỪỬỮỰ"
kh_rx = re.compile(r"\b[Kk]h(?:oá|óa)\s+(?:học\s+)?(?:về\s+)?([" + UP + r"][^,.;:<]{0,60})")
ALIASES = {"thuật toán": "CS112", "toán cho khoa học máy tính": "CS115", "toán rời rạc": "DMS", "hệ thống máy tính": "CSA",
           "hệ điều hành": "OSY", "mạng máy tính": "NET", "mạng": "NET", "cơ sở dữ liệu": "DBS", "lý thuyết tính toán": "TOC",
           "an toàn thông tin": "SEC", "java": "JVA", "lập trình java": "JVA", "học máy": "CS115",
           "toán cho robot": "RBM", "robot": "ROB", "hệ phân tán": "DSY", "khoa học dữ liệu": "DSC", "phân tích dữ liệu": "DAN",
           "kỹ thuật dữ liệu": "DEN", "trình biên dịch": "PLC", "ngôn ngữ lập trình": "PLC", "kiến trúc hệ thống": "SAR",
           "đồ hoạ": "GFX", "thị giác máy tính": "CVI", "học tăng cường": "RLN", "mô hình ngôn ngữ lớn": "LLM",
           "trí tuệ nhân tạo": "AIF", "điện toán đám mây": "CLC", "đám mây": "CLC", "hệ thống nhúng": "ESY", "nhúng": "ESY",
           "backend ngân hàng": "BNK", "ngân hàng": "BNK", "devops": "DVO", "mlops": "MLO", "blockchain": "BCH",
           "tương tác người": "HCI", "truy hồi thông tin": "IRS", "song song": "PAR", "tính toán song song": "PAR",
           "kiến trúc hướng sự kiện": "EVT", "ứng dụng web": "WEB", "web": "WEB", "hệ thống hướng dịch vụ": "CLD",
           "kỹ thuật lập trình": "SDP", "mẫu thiết kế": "SDP", "phần mềm đúng đắn": "SWF", "tình huống chuyên gia": "CAS",
           "đạo đức": "SEP", "ai agent": "AGT", "tác tử": "AGT",
           # tên gọi không chính thức đã gặp (SWF L03/L07/L12, 2026-11-09)
           "kiến trúc máy tính": "CSA", "cấu trúc dữ liệu": "CS112", "giải thuật": "CS112", "đại số tuyến tính": "CS115",
           "xác suất": "CS115", "thống kê": "CS115", "giải tích": "CS115", "lập trình": "JVA",
           "phân tích và thiết kế": "CS112", "phân tích & thiết kế": "CS112", "toán": "CS115",
           "tích hợp và triển khai liên tục": "DVO", "tích hợp, triển khai liên tục": "DVO", "triển khai liên tục": "DVO"}
# mọi vế của tên series ("MLOps: đưa mô hình học máy vào vận hành" → cả hai vế) cũng là tên tắt (CVI L10 từng lọt)
for _c, _n in NAMES.items():
    for _p in re.split(r"[:—–]", _n):
        _p = _p.strip().lower()
        if len(_p) >= 6:
            ALIASES.setdefault(_p, _c)
alias_rx = re.compile(r"(?i)\bkh(?:oá|óa)\s+(?:học\s+)?(?:về\s+)?(" + "|".join(sorted(map(re.escape, ALIASES), key=len, reverse=True))
                      + r")(?![a-zà-ỹđ])")
# "khoá trước" một mình thường là khoá loại trừ/khoá dòng ("lấy khoá trước", OSY L05/L06) → chỉ tính khi có "ở/từ/trong/của/như" đứng trước
gen_rx = re.compile(r"(?i)((?:ở|từ|trong|của|như) kh(?:oá|óa) trước(?! khi)|kh(?:oá|óa) nền|kh(?:oá|óa) học trước|kh(?:oá|óa) học khác|kh(?:oá|óa) tiên quyết|"
                    r"các kh(?:oá|óa) (?:trước|nền|khác|học))")
SKIP = {"source", "reason", "checks", "asr_reviewed", "sentence", "spec", "voice", "rate", "series",
        "requires", "requires_ext", "see_also", "assumes", "introduces", "focus", "id", "kind"}


def strings(node, path=()):
    if isinstance(node, dict):
        for k, v in node.items():
            if str(k) not in SKIP:
                yield from strings(v, path + (str(k),))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from strings(v, path + (str(i),))
    elif isinstance(node, str):
        yield path, node


def find(s, me):
    out = []
    for m in code_rx.finditer(s):
        c = m.group(1)
        if c == me:
            continue
        if m.start() > 0 and s[m.start() - 1] in "\"'":
            continue  # chuỗi trong mã nguồn, ví dụ case "APP", "WEB" (JVA L03)
        if c == "SEC" and (re.search(r"(lệnh|Lệnh|Uỷ ban|Ủy ban|của|theo|báo cáo)\s*$", s[max(0, m.start() - 12):m.start()])
                           or re.match(r"SEC\s+\d", s[m.start():m.start() + 8])):
            continue  # SEC = Uỷ ban Chứng khoán Mỹ (CAS)
        if c == "ACB" and not re.search(r"[Kk]h(?:oá|óa)\s*(?:học\s*)?$", s[max(0, m.start() - 12):m.start()]):
            continue
        out.append((m.start(), "mã " + c))
    for m in kh_rx.finditer(s):
        tail = m.group(1).strip().lower()
        for c, n in NAMES.items():
            if c != me and n and tail.startswith(n.lower()[:14]):
                out.append((m.start(), "tên " + c))
                break
    # (đã thử bắt mọi "khoá <Từ Viết Hoa>": quá nhiều dương tính giả — khoá Lạc quan, khoá Redis, khoá Tài khoản 1 → dùng ALIASES)
    # tên khoá viết thường hoặc gọi tắt ("khoá thuật toán", "khoá hệ điều hành") — CSA L07 từng lọt (2026-11-09)
    for m in alias_rx.finditer(s):
        c = ALIASES[m.group(1).lower()]
        if c == "JVA" and s[max(0, m.start() - 3):m.start()].lower() == "từ ":
            continue  # "từ khoá Java" = keyword (BNK L01); nhưng "Từ khoá Toán…" (LLM) vẫn bắt
        if c != me and not any(abs(p - m.start()) < 3 for p, _ in out):
            out.append((m.start(), "tên tắt " + c + " “" + m.group(1) + "”"))
    for m in gen_rx.finditer(s):
        out.append((m.start(), "cụm “" + m.group(1) + "”"))
    return out


hits = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(ROOT, "lessons", "*", "L*.yaml"))):
    y = yaml.safe_load(open(f, encoding="utf-8")) or {}
    me = str(y.get("course") or os.path.basename(os.path.dirname(f)).upper())
    rel = os.path.relpath(f, ROOT).replace("\\", "/")
    parts = {"title": y.get("title"), "objectives": y.get("objectives"), "scenes": y.get("scenes")}
    for path, s in strings(parts):
        for pos, kind in find(s, me):
            hits[me].append((rel, ".".join(path), kind, s[max(0, pos - 50):pos + 110].replace("\n", " ")))
for f in sorted(glob.glob(os.path.join(ROOT, "curriculum", "*.yaml"))):
    y = yaml.safe_load(open(f, encoding="utf-8")) or {}
    me = str(y.get("course") or "")
    if not me or not isinstance(y.get("lessons"), list):
        continue
    rel = os.path.relpath(f, ROOT).replace("\\", "/")
    for les in y["lessons"]:
        sub = {k: les.get(k) for k in ("title", "objectives", "example", "fix")}
        for path, s in strings(sub):
            for pos, kind in find(s, me):
                hits[me].append((rel, f"{les.get('id')}.{'.'.join(path)}", kind,
                                 s[max(0, pos - 50):pos + 110].replace("\n", " ")))

total = sum(len(v) for v in hits.values())
files = {h[0] for v in hits.values() for h in v}
for c in sorted(hits, key=lambda c: (-len(hits[c]), c)):
    if ONLY and c != ONLY:
        continue
    print(f"{c}: {len(hits[c])} lượt ở {len({h[0] for h in hits[c]})} tệp")
    if LIST:
        for h in hits[c]:
            print("   " + " | ".join(h))
print(f"check_xref: {total} lượt tham chiếu sang khoá khác ở {len(files)} tệp")
sys.exit(1 if total else 0)
