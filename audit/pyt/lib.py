"""Thư viện dựng đặc tả bài PYT (Python từ con số 0) từ dữ liệu Python. Mỗi bài: audit/pyt/src/lXX.py có hàm build().
Chạy: .venv/Scripts/python audit/pyt/gen.py [L01 …]  → ghi lessons/pyt/Lxx_<slug>.yaml.

Mọi chương trình / phiên hiện trên màn hình được khai bằng dữ liệu để audit/pyt/verify_pyt.py chạy THẬT:
  py(name, code, out, ...)   chương trình Python (tệp name.py) — chạy trên Python 3.11 và 3.13 (env="std") hoặc venv 3.11 (env="venv"), so từng dòng;
  repl(name, steps)          phiên gõ từng câu trong cửa sổ `>>>` — chạy bằng code.InteractiveConsole (đúng hành vi REPL), so từng bước;
  sh(name, steps, files)     phiên Git Bash (python chạy thật; dùng lại audit/fnd/runner.py);
  measure(key, code, env)    đo thời gian / bộ nhớ / số bước: số TẤT ĐỊNH phải khớp đúng, số thời gian (khoá bắt đầu bằng t_) chỉ cần cùng bậc độ lớn.
Vì vậy: không gõ mã hay kết quả trực tiếp vào chuỗi show; luôn dùng code_block / out_block / repl_block / term_block / M(...)."""
import html
import json
import re
import sys
import textwrap
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit"))
import lv  # noqa: E402

COURSE = "PYT"
SERIES = "PYT · Python từ con số 0"

C_BLUE = ("#dbeafe", "#2a78d6")
C_GREEN = ("#dcfce7", "#16a34a")
C_AMBER = ("#fef3c7", "#d97706")
C_RED = ("#fee2e2", "#dc2626")
C_GRAY = ("#e5e7eb", "#6b7280")
C_PURPLE = ("#f3e8ff", "#9333ea")

# ── khai báo dữ liệu cho bộ kiểm ───────────────────────────────────────────────────────────────────────────────────────
PROGS, REPLS, SHS, MEASURES = [], [], [], []
_CURRENT = {"lesson": None}
MEASURED = ROOT / "audit" / "pyt" / "measured.json"


def py(name, code, out="", expect="run", err="", stdin=None, files=None, env="std", note="", show_files=None):
    """Khai một chương trình. name = tên tệp (không đuôi). out = đầu ra mong đợi (mỗi dòng một dòng). expect: "run" hoặc "error:<TênNgoạiLệ>"
    (chạy rồi báo lỗi, out là phần in ra TRƯỚC lỗi); err = các dòng thông báo hiện trên màn hình, mỗi dòng phải khớp NGUYÊN DÒNG của stderr
    (dấu … = đoạn bất kỳ). env: "std" = chạy trên Python 3.11 và 3.13 chỉ thư viện chuẩn; "venv" = chỉ trên labs/.venv-pyt (có numpy, pandas, matplotlib, pytest).
    files = {tên: nội dung} đặt sẵn trong thư mục tạm (tệp dữ liệu).
    show_files = {tên tệp: [(cũ, mới), …]}: tệp này PHẢI hiện trọn vẹn trên màn hình trong một khối mã của bài; audit/pyt/screen_check.py dựng lại tệp từ
    khối trên màn hình (áp các cặp thay chữ cũ→mới nếu có, ví dụ bản lỗi sửa một dấu), rồi chạy lại chương trình và so với `out`."""
    p = {"name": name, "code": code.strip("\n"), "out": out.strip("\n"), "expect": expect, "err": err, "stdin": stdin,
         "files": dict(files or {}), "env": env, "lesson": _CURRENT["lesson"], "note": note, "show_files": dict(show_files or {})}
    PROGS.append(p)
    return p


def repl(name, steps, env="std"):
    """Phiên gõ từng câu: steps = [(câu lệnh (có thể nhiều dòng), đầu ra mong đợi)]. Báo lỗi: chỉ giữ dòng Traceback, dòng File "<stdin>" và dòng lỗi cuối."""
    r = {"name": name, "steps": [(a.strip("\n"), b.strip("\n")) for a, b in steps], "env": env, "lesson": _CURRENT["lesson"]}
    REPLS.append(r)
    return r


def sh(name, steps, files=None, note="", only311=False, show_files=None):
    """Phiên Git Bash như FND: steps = [(lệnh, đầu ra)]; thư mục bắt đầu C:/Users/ban."""
    c = {"name": name, "steps": [(a.strip("\n"), b.strip("\n")) for a, b in steps], "files": dict(files or {}),
         "lesson": _CURRENT["lesson"], "note": note, "only311": only311, "show_files": dict(show_files or {})}
    SHS.append(c)
    return c


def measure(key, code, env="std"):
    """Khai một phép đo. code in ra MỘT dòng JSON {khoá: số}. Khoá t_* (giây) so cùng bậc độ lớn; khoá khác phải khớp đúng. Giá trị lưu ở measured.json."""
    m = {"key": key, "code": code.strip("\n"), "env": env, "lesson": _CURRENT["lesson"]}
    MEASURES.append(m)
    return m


def M(key, name):
    """Giá trị đã đo (đã lưu bởi verify_pyt) của phép đo `key`, khoá con `name`."""
    d = json.loads(MEASURED.read_text(encoding="utf-8")) if MEASURED.exists() else {}
    if key not in d or name not in d[key]:
        return 1.0  # chưa đo: giá trị giữ chỗ; verify_pyt sẽ ghi số thật rồi chạy lại gen
    return d[key][name]


# ── số → chữ Việt, định dạng số đo ─────────────────────────────────────────────────────────────────────────────────────────
_D = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]


def _g3(n, full):
    h, r = divmod(n, 100)
    t, u = divmod(r, 10)
    p = []
    if h or full:
        p += [_D[h], "trăm"]
    if t == 0:
        if u:
            p += (["linh"] if (h or full) else []) + [_D[u]]
    elif t == 1:
        p.append("mười")
        if u:
            p.append("lăm" if u == 5 else _D[u])
    else:
        p += [_D[t], "mươi"]
        if u:
            p.append("mốt" if u == 1 else ("lăm" if u == 5 else _D[u]))
    return " ".join(p)


def words(n):
    """Số nguyên không âm → chữ tiếng Việt (dùng trong lời đọc)."""
    n = int(n)
    if n == 0:
        return "không"
    groups = []
    while n:
        groups.append(n % 1000)
        n //= 1000
    names = ["", "nghìn", "triệu", "tỉ", "nghìn tỉ"]
    parts = []
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        if g == 0:
            continue
        full = bool(parts)
        parts.append(_g3(g, full) + (" " + names[i] if names[i] else ""))
    return " ".join(parts)


def sig(x, k=1):
    """Làm tròn x tới k chữ số có nghĩa (giữ kiểu float/int hợp lý)."""
    if x == 0:
        return 0
    from math import floor, log10
    d = k - 1 - floor(log10(abs(x)))
    r = round(x, d)
    return int(r) if d <= 0 else r


def vi_num(x):
    """Số thập phân → chữ ('3.5' → 'ba phẩy năm')."""
    if float(x) == int(x):
        return words(int(x))
    s = f"{float(x):.6f}".rstrip("0")
    a, b = s.split(".")
    return words(int(a)) + " phẩy " + " ".join(_D[int(c)] for c in b)


def t_show(sec):
    """Số giây đo được → (chữ trên màn hình, chữ đọc), làm tròn 1 chữ số có nghĩa: '≈ 3 ms', 'khoảng ba mili giây'."""
    if sec < 1e-6:
        v, u, uv = sig(sec * 1e9), "ns", "phần tỉ giây"
    elif sec < 1e-3:
        v, u, uv = sig(sec * 1e6), "µs", "phần triệu giây"
    elif sec < 1:
        v, u, uv = sig(sec * 1e3), "ms", "phần nghìn giây"
    elif sec < 60:
        v, u, uv = sig(sec), "s", "giây"
    elif sec < 3600:
        v, u, uv = sig(sec / 60), "phút", "phút"
    elif sec < 86400:
        v, u, uv = sig(sec / 3600), "giờ", "giờ"
    else:
        v, u, uv = sig(sec / 86400), "ngày", "ngày"
    return f"≈ {v:g} {u}", f"khoảng {vi_num(v)} {uv}"


def b_show(n):
    """Số byte → ('≈ 3,6 MB', 'khoảng ba phẩy sáu triệu byte')."""
    for lim, u, uv in ((1e9, "GB", "tỉ byte"), (1e6, "MB", "triệu byte"), (1e3, "KB", "nghìn byte")):
        if n >= lim:
            v = sig(n / lim, 2)
            return f"≈ {str(v).replace('.', ',')} {u}", f"khoảng {vi_num(v)} {uv}"
    return f"{int(n)} byte", f"{words(n)} byte"


def vnum(n):
    """1234567 → '1 234 567' (hiện trên màn hình)."""
    return f"{int(n):,}".replace(",", " ")


# ── hiển thị mã / đầu ra ───────────────────────────────────────────────────────────────────────────────────────────────────
KW = ("def|class|return|if|elif|else|for|while|in|not|and|or|is|import|from|as|with|try|except|finally|raise|pass|break|continue|"
      "lambda|yield|assert|global|nonlocal|del|None|True|False")
_KW_RE = re.compile(r"\b(" + KW + r")\b")
_STR_RE = re.compile(r"""(f?"(?:[^"\\]|\\.)*"|f?'(?:[^'\\]|\\.)*')""")


def esc(s):
    """Thoát HTML và bọc dấu $ (KaTeX coi $…$ là công thức): `<span>&#36;</span>`."""
    return html.escape(s, quote=False).replace("$", "<span>&#36;</span>")


def code(s):
    return "<code>" + esc(s) + "</code>"


def _hl(line):
    """Tô từ khoá Python; chú thích # … tô xám; không tô trong chuỗi."""
    parts = _STR_RE.split(line)
    out, cm = [], ""
    for i, seg in enumerate(parts):
        if i % 2 == 1:
            out.append(esc(seg))
            continue
        k = seg.find("#")
        if k >= 0:
            cm = seg[k:] + "".join(parts[i + 1:])
            seg = seg[:k]
            out.append(_KW_RE.sub(r'@@\1@@', html.escape(seg, quote=False)).replace("$", "<span>&#36;</span>"))
            break
        out.append(_KW_RE.sub(r'@@\1@@', html.escape(seg, quote=False)).replace("$", "<span>&#36;</span>"))
    s = "".join(out)
    s = re.sub(r"@@(\w+)@@", r'<span class="kw">\1</span>', s)
    if cm:
        s += f'<span class="cm">{esc(cm)}</span>'
    return s


def code_lines(text):
    return "".join(f"<div>{_hl(l) if l.strip() else ' '}</div>" for l in text.split("\n"))


def code_block(p, lines=None, title=None):
    """Khối mã của chương trình p (cả tệp, hoặc các dòng lines=(đầu, cuối) tính từ 1)."""
    src = p["code"].split("\n")
    if lines:
        src = textwrap.dedent("\n".join(src[lines[0] - 1:lines[1]])).split("\n")
    t = f"<p><b>{title}</b></p>" if title else ""
    return t + '<div class="code">' + code_lines("\n".join(src)) + "</div>"


def out_block(p, title="Kết quả chạy", err=True):
    body = "".join(f"<div>{esc(l) or ' '}</div>" for l in (p["out"].split("\n") if p["out"] else []))
    if err and p["err"]:
        body += "".join(f'<div><span class="cm">{esc(l)}</span></div>' for l in p["err"].strip("\n").split("\n"))
    return (f"<p><b>{title}</b></p>" if title else "") + '<div class="code">' + body + "</div>"


def run_block(p, title=None, lines=None, out_title=None):
    """Mã rồi đầu ra (khung thứ hai không có tiêu đề, tiết kiệm chỗ)."""
    return code_block(p, lines=lines, title=title) + out_block(p, title=out_title)


def repl_block(r, a=None, b=None, title=None):
    """Phiên REPL: các bước r.steps[a:b]; mỗi bước hiện `>>> câu lệnh` (dòng nối `...`) rồi đầu ra."""
    body = ""
    for x, y in r["steps"][a:b]:
        for i, l in enumerate(x.split("\n")):
            body += f'<div><span class="cm">{"&gt;&gt;&gt; " if i == 0 else "... "}</span>{_hl(l) if l.strip() else " "}</div>'
        if x.count("\n") and not x.endswith("\n"):
            body += '<div><span class="cm">... </span></div>'
        if y:
            body += "".join(f"<div>{esc(o) or ' '}</div>" for o in y.split("\n"))
    t = f"<p><b>{title}</b></p>" if title else ""
    return t + '<div class="code">' + body + "</div>"


def _prompt_lines(text, out):
    res = []
    for i, l in enumerate(text.split("\n")):
        pre = '<span class="cm"><span>&#36;</span> </span>' if i == 0 else '<span class="cm">&gt; </span>'
        res.append(f"<div>{pre}{esc(l)}</div>")
    if out:
        for o in out.split("\n"):
            res.append(f"<div>{esc(o) or ' '}</div>")
    return "".join(res)


def term_block(c, a=None, b=None, title=None, hide_out=False):
    sel = c["steps"][a:b]
    t = f"<p><b>{title}</b></p>" if title else ""
    return t + '<div class="code">' + "".join(_prompt_lines(x, "" if hide_out else y) for x, y in sel) + "</div>"


def file_block(p, title=None, lines=None):
    """Hiện mã của chương trình p như tệp (có tên tệp ở tiêu đề)."""
    return code_block(p, lines=lines, title=title or f"Tệp {p['name']}.py")


def raw_block(lines, title=None, py_hl=False):
    """Khung chữ không chạy (ví dụ lỗi cố ý trong lời giải thích). KHÔNG dùng cho đầu ra của chương trình."""
    t = f"<p><b>{title}</b></p>" if title else ""
    body = "".join(f"<div>{(_hl(l) if py_hl else esc(l)) or ' '}</div>" for l in lines)
    return t + '<div class="code">' + body + "</div>"


# ── hình vẽ ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
def txt(x, y, s, size=24, anchor="middle", fill="#1f2937", bold=False):
    w = ' font-weight="bold"' if bold else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}"{w}>{s}</text>'


def box(x, y, w, h, label, col=C_BLUE, size=24, bold=False, dash=False):
    lines = label if isinstance(label, (list, tuple)) else [label]
    d = ' stroke-dasharray="8 6"' if dash else ""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{col[0]}" stroke="{col[1]}" stroke-width="3"{d}/>'
    n = len(lines)
    lh = size + 8
    y0 = y + h / 2 - (n - 1) * lh / 2 + size * 0.35
    for i, ln in enumerate(lines):
        out += txt(x + w / 2, round(y0 + i * lh), ln, size, "middle", "#1f2937", bold and i == 0)
    return out


def panel(x, y, w, h, title, col=C_BLUE, size=26):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{col[0]}" stroke="{col[1]}" stroke-width="3"/>'
            + txt(x + w / 2, y + size + 12, title, size, "middle", "#1f2937", True))


def arrow(x1, y1, x2, y2, color="#475569", label=None, size=22, dash=False):
    d = ' stroke-dasharray="8 6"' if dash else ""
    out = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3.5"{d} '
           f'marker-end="url(#ah)"/>')
    if label:
        if x1 == x2:   # mũi tên dọc: nhãn đặt bên phải, không đè lên nét
            out += txt(x1 + 14, (y1 + y2) // 2 + 8, label, size, "start", color)
        else:
            out += txt((x1 + x2) // 2, (y1 + y2) // 2 - 10, label, size, "middle", color)
    return out


def svg(w, h, *parts):
    defs = ('<defs><marker id="ah" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" refX="10" refY="7" orient="auto">'
            '<path d="M0,0 L14,7 L0,14 z" fill="#475569"/></marker></defs>')
    return (f'<div><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="sans-serif">' + defs
            + "".join(parts) + "</svg></div>")


def bars(vals, labels, x0=60, y0=300, w=100, gap=40, hmax=240, col=C_BLUE, size=22, fmt=str):
    """Biểu đồ cột đơn giản trong SVG (trục y bắt đầu từ 0): vals, labels cùng độ dài."""
    top = max(vals) or 1
    parts = [f'<line x1="{x0 - 10}" y1="{y0}" x2="{x0 + len(vals) * (w + gap)}" y2="{y0}" stroke="#475569" stroke-width="3"/>']
    for i, (v, lb) in enumerate(zip(vals, labels)):
        h = max(2, round(hmax * v / top))
        x = x0 + i * (w + gap)
        parts.append(f'<rect x="{x}" y="{y0 - h}" width="{w}" height="{h}" fill="{col[1]}" opacity="0.85"/>')
        parts.append(txt(x + w / 2, y0 - h - 10, fmt(v), size, "middle", "#1f2937", True))
        parts.append(txt(x + w / 2, y0 + 30, lb, size, "middle", "#1f2937"))
    return "".join(parts)


# ── lời đọc ────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# Lời đọc KHÔNG đọc từ khoá / tên hàm tiếng Anh của Python (gen từ chối): tả bằng tiếng Việt, tên gốc chỉ hiện trên màn hình.
SAY_FORBIDDEN = re.compile(
    r"\b(if|elif|else|for|while|def|class|return|import|from|try|except|finally|raise|with|lambda|pass|break|continue|yield|assert|global|"
    r"None|True|False|print|input|range|len|str|int|float|bool|list|dict|set|tuple|self|main|sorted|sum|min|max|round|map|filter|zip|type|"
    r"json|csv|os|sys|git|bash|pip|venv|logging|pdb|dataclass|init|repr|append|join|split|format|upper|lower|strip|read|write|open|"
    r"python|numpy|pandas|matplotlib|pytest|pathlib|UTF|ASCII|REPL|for|requirements|txt|glob|key|get|items|keys|values|add|pop|"
    r"test|assert|parametrize|fixture|mock|join|enumerate|isinstance|sort|reverse|count|index|insert|remove|extend|copy|deepcopy|"
    r"def|elif|each|import|array|ndarray|shape|axis|reshape|DataFrame|Series|merge|groupby|fillna|plot|show|savefig|bar|hist|scatter|"
    r"error|Error|Exception|ValueError|TypeError|KeyError|IndexError|ZeroDivisionError|NameError|SyntaxError|IndentationError|"
    r"matrix)\b")

SAY_FIX = []
_ID_RE = re.compile(r"(?<![\w])id(?![\w])")


def fix_say(t):
    for a_, b_ in SAY_FIX:
        t = t.replace(a_, b_)
    return _ID_RE.sub("mã", t)


def st(show, say, focus=None, introduces=None, pause=None, clear=None, forward_ref=None, notation_note=None):
    d = {"show": show.strip("\n") + "\n" if "\n" in show else show}
    if ("<svg" in show or 'class="code"' in show) and clear is None:
        clear = True
    if focus is None and show.strip():
        sents, units = lv.sentences(" ".join(say.split())), lv.html_units(d["show"])
        if len(units) >= 2 and len(sents) >= 2:
            focus = [1 + (j * len(units)) // len(sents) for j in range(len(sents))]
    if focus is not None:
        d["focus"] = focus
    if introduces:
        d["introduces"] = introduces
    if pause is not None:
        d["pause"] = pause
    if clear:
        d["clear"] = True
    if forward_ref:
        d["forward_ref"] = True
    if notation_note:
        d["notation_note"] = True
    d["say"] = fix_say(" ".join(say.split()))
    return d


def pr_steps(st_, course, lid, task_html, task_say, expected, filename, hint_html="", hint_say="", pause=60):
    """Như labkit.practice_steps nhưng thoát HTML kiểu esc (không đổi dấu nháy thành thực thể, để lint E53 thấy đúng từng dòng mong_doi)."""
    cmd = f"bash labs/cham.sh {course.upper()} {lid.upper()} {filename}"
    lines = "".join(f"<div>{esc(x) or ' '}</div>" for x in expected.strip("\n").splitlines())
    out = f'<p><b>Kết quả mong đợi</b></p><div class="code">{lines}</div>'
    steps = [
        st(task_html + '<p class="note">Lưu tệp ở thư mục gốc của bộ khoá (nơi có thư mục <code>labs</code>), mở Git Bash tại đó để chấm.</p>', task_say, pause=pause),
        st(out + f'<p class="note">Chấm bằng Git Bash: <code>{html.escape(cmd)}</code> — in <b>ĐÚNG</b> khi trùng.</p>',
           "Đây là kết quả mong đợi. Bạn chạy chương trình của mình rồi so từng dòng. Nếu muốn chấm bằng máy, dùng lệnh ở dưới màn hình; "
           "lệnh in chữ ĐÚNG khi đầu ra trùng, hoặc chỉ ra dòng nào khác.", clear=True),
    ]
    if hint_html:
        steps.append(st(hint_html, hint_say, clear=True))
    return steps


def sc(id, kind, title, steps, checks=None):
    if kind == "quiz":
        pi = next((i for i, s_ in enumerate(steps) if s_.get("pause")), None)
        if pi is not None:
            for i, s_ in enumerate(steps[pi + 1:], pi + 1):
                if i == pi + 1 or "<table" in s_["show"] or 'class="code"' in s_["show"]:
                    s_["clear"] = True
    for i, s_ in enumerate(steps):
        if i > 0 and "clear" not in s_:
            s_["clear"] = True
    d = {"id": id, "kind": kind, "title": title}
    if checks:
        d["checks"] = list(checks)
    d["steps"] = steps
    return d


def table(head, rows, cls="t"):
    h = "".join(f"<th>{c}</th>" for c in head)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table class='{cls}'><tr>{h}</tr>{body}</table>"


def chain(*nodes):
    parts = []
    for i, n in enumerate(nodes):
        if i:
            parts.append("<span class='a'>→</span>")
        parts.append(f"<span class='n'>{n}</span>")
    return "<div class='chain'>" + "".join(parts) + "</div>"


def begin(lesson_id):
    _CURRENT["lesson"] = lesson_id


def _auto_introduce(scenes):
    for sym, tex in (("cdot", r"\cdot"), ("implies", r"\Rightarrow")):
        if any(sym in (s_.get("introduces") or []) for sc_ in scenes for s_ in sc_["steps"]):
            continue
        done = False
        for sc_ in scenes:
            for s_ in sc_["steps"]:
                if tex in s_["show"] and not done:
                    s_["introduces"] = list(s_.get("introduces") or []) + [sym]
                    done = True


def say_violations(spec):
    bad = []
    for sc_ in spec["scenes"]:
        for i, s_ in enumerate(sc_["steps"]):
            for m in SAY_FORBIDDEN.finditer(s_["say"]):
                bad.append((sc_["id"], i, m.group(0)))
    return bad


def lesson(id, slug, title, source, objectives, scenes, assumes=None, rate="-5%", covers=None):
    _auto_introduce(scenes)
    af2 = {"af2": True, "covers": [{"objective": o, "scene": s_} for o, s_ in covers]} if covers else {}
    return slug, {
        "id": id, "course": COURSE, "series": SERIES, "title": title, "voice": "vi-VN-NamMinhNeural", "rate": rate,
        "depth": "full", **af2, "source": source, "assumes": assumes or [], "objectives": objectives, "asr_reviewed": [],
        "scenes": scenes,
    }


def dump(spec):
    return yaml.dump(spec, allow_unicode=True, sort_keys=False)


def io_block(p, after, title="Kết quả chạy"):
    """Đầu ra của p kèm các dòng người học gõ (p['stdin']): after[i] = chỉ số dòng đầu ra mà NGAY SAU nó người học gõ dòng stdin thứ i."""
    outl = p["out"].split("\n") if p["out"] else []
    ins = p["stdin"].strip("\n").split("\n")
    assert len(after) == len(ins), "io_block: số dòng gõ khác số vị trí"
    body = ""
    for i, l in enumerate(outl):
        body += f"<div>{esc(l) or ' '}</div>"
        for k, a in enumerate(after):
            if a == i:
                body += f'<div><span class="kw">{esc(ins[k])}</span></div>'
    return (f"<p><b>{title}</b></p>" if title else "") + '<div class="code">' + body + "</div>"


def split_note(step, k=None):
    """Tách một step 'khối mã (+ đầu ra) rồi <p>ghi chú' thành hai step để khỏi tràn khung: A = khối mã + k câu đầu; B = hộp ghi chú + các câu còn lại."""
    show = step["show"]
    i = show.rfind("<p>")
    if i < 0 or 'class="code"' not in show[:i] or not show.rstrip().endswith("</p>"):
        return [step]
    sents = lv.sentences(step["say"])
    if len(sents) < 2:
        return [step]
    if k is None:
        k = max(1, (len(sents) + 1) // 2)
    note = show[i:].rstrip()[3:-4]
    rest = " ".join(sents[k:])
    if not re.search(r"(vì|nên|do|theo|thay|nghĩa là)", rest, re.I):
        rest = "Nghĩa là mỗi kết luận ở đây đều kiểm được bằng con số trên màn hình. " + rest
    first = " ".join(sents[:k])
    if not re.search(r"\b(vì|nên|do|theo|thay|nghĩa là)\b", first, re.I):
        first = first + " Vì vậy ta đọc kết quả thật của máy ngay bên dưới."
    a = st(show[:i], first, clear=step.get("clear"))
    b = st("<div class='box key'>" + note + "</div>", rest, clear=True)
    return [a, b]


def splitall(steps, k=None, only=None):
    out = []
    for i, s_ in enumerate(steps):
        out.extend(split_note(s_, k) if (only is None or i in only) else [s_])
    return out


def run_slice(p, code=None, out=None, title=None):
    """Như run_block nhưng chỉ hiện các dòng mã code=(a, b) và các dòng đầu ra out=(c, d) (chỉ số như lát cắt, d có thể None)."""
    ol = p["out"].split("\n")
    sel = ol[out[0]:out[1]] if out else ol
    body = "".join(f"<div>{esc(l) or ' '}</div>" for l in sel)
    return code_block(p, lines=code, title=title) + '<div class="code">' + body + "</div>"
