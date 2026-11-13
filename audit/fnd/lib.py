"""Thư viện dựng đặc tả bài FND (Nền thực hành: dòng lệnh, tệp, dữ liệu, HTTP, SQL, Git) từ dữ liệu Python. Mỗi bài: audit/fnd/src/lXX.py có hàm build().
Chạy: .venv/Scripts/python audit/fnd/gen.py [L01 …]  → ghi lessons/fnd/Lxx_<slug>.yaml (YAML do yaml.dump sinh).

Khác JVA: mọi đoạn dòng lệnh / tệp hiện trên màn hình được khai bằng cmd(...) — một PHIÊN Git Bash (nhiều bước, giữ thư mục hiện tại),
mỗi bước = (lệnh, đầu ra mong đợi). audit/fnd/verify_fnd.py chạy THẬT cả phiên trong một thư mục tạm sạch bằng Git Bash và so từng bước.
Vì vậy: không gõ lệnh hay kết quả trực tiếp vào chuỗi show; luôn dùng term_block(c, a, b) / file_block(c, tên tệp).
Phần không ổn định (đường dẫn tạm, ngày giờ, mã băm) không hiện: verify_fnd đổi thư mục tạm thành C:/Users/ban, đặt ngày Git cố định."""
import html
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import lv  # noqa: E402

COURSE = "FND"
SERIES = "FND · Nền thực hành: dòng lệnh, tệp, dữ liệu, HTTP, SQL, Git"

C_BLUE = ("#dbeafe", "#2a78d6")
C_GREEN = ("#dcfce7", "#16a34a")
C_AMBER = ("#fef3c7", "#d97706")
C_RED = ("#fee2e2", "#dc2626")
C_GRAY = ("#e5e7eb", "#6b7280")
C_PURPLE = ("#f3e8ff", "#9333ea")

# ── phiên dòng lệnh khai bằng dữ liệu, để bộ kiểm chạy thật ─────────────────────────────────────────────────────────────
CMDS = []  # mỗi phần tử: dict(name, steps[(lệnh, đầu ra)], files{đường dẫn: nội dung}, lesson, kind)
_CURRENT = {"lesson": None}


def cmd(name, steps, files=None, kind="bash", note=""):
    """Khai một phiên Git Bash. steps = [(lệnh, đầu ra mong đợi), …] — chạy lần lượt trong CÙNG một tiến trình bash (cd được giữ),
    thư mục bắt đầu là C:/Users/ban (đã đặt trước các tệp trong files = {đường dẫn tương đối: nội dung}). Đầu ra = stdout + stderr gộp;
    kiểm bỏ \\r và khoảng trắng cuối dòng. kind: "bash" (mặc định)."""
    c = {"name": name, "steps": [(a.strip("\n"), b.strip("\n")) for a, b in steps], "files": dict(files or {}), "lesson": _CURRENT["lesson"],
         "kind": kind, "note": note}
    CMDS.append(c)
    return c


def esc(s):
    """Thoát HTML và bọc dấu $ (MATH_RE của lint/KaTeX sẽ coi $…$ là công thức): `<span>&#36;</span>`, cách BNX đã dùng."""
    return html.escape(s, quote=False).replace("$", "<span>&#36;</span>")


def code(s):
    """<code>…</code> an toàn với $ (xem esc)."""
    return "<code>" + esc(s) + "</code>"


def _prompt_lines(text, out):
    lines = text.split("\n")
    res = []
    for i, l in enumerate(lines):
        pre = '<span class="cm"><span>&#36;</span> </span>' if i == 0 else '<span class="cm">&gt; </span>'
        res.append(f"<div>{pre}{esc(l)}</div>")
    if out:
        for o in out.split("\n"):
            res.append(f"<div>{esc(o) or ' '}</div>")
    return "".join(res)


def term_block(c, a=None, b=None, title=None, hide_out=False):
    """Khung cửa sổ lệnh: các bước c.steps[a:b] (chỉ số từ 0, b không gồm), mỗi bước hiện `$ lệnh` rồi đầu ra."""
    sel = c["steps"][a:b]
    t = f"<p><b>{title}</b></p>" if title else ""
    body = "".join(_prompt_lines(x, "" if hide_out else y) for x, y in sel)
    return t + '<div class="code">' + body + "</div>"


def file_block(c, path, title=None, lines=None):
    """Nội dung một tệp có trong c.files (được bộ kiểm ghi ra đĩa đúng nguyên văn)."""
    src = c["files"][path].rstrip("\n").split("\n")
    if lines:
        src = src[lines[0] - 1:lines[1]]
    t = f"<p><b>{title or 'Tệp ' + path}</b></p>"
    body = "".join(f"<div>{esc(l) or ' '}</div>" for l in src)
    return t + '<div class="code">' + body + "</div>"


def raw_block(lines, title=None):
    """Khung chữ không chạy (ví dụ lỗi cú pháp cố ý, nội dung tệp cấu hình). KHÔNG dùng cho đầu ra của lệnh."""
    t = f"<p><b>{title}</b></p>" if title else ""
    body = "".join(f"<div>{esc(l) or ' '}</div>" for l in lines)
    return t + '<div class="code">' + body + "</div>"


# ── hình vẽ ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
def txt(x, y, s, size=24, anchor="middle", fill="#1f2937", bold=False):
    w = ' font-weight="bold"' if bold else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}"{w}>{s}</text>'


def pr_steps(*a, **k):
    """labkit.practice_steps + thay khung ở bước gợi ý (kết quả mong đợi dài làm tràn khung nếu không xoá)."""
    from labkit import practice_steps
    steps = practice_steps(*a, **k)
    for s_ in steps[2:]:
        s_["clear"] = True
    return steps


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
        out += txt((x1 + x2) // 2, (y1 + y2) // 2 - 10, label, size, "middle", color)
    return out


def svg(w, h, *parts):
    defs = ('<defs><marker id="ah" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" refX="10" refY="7" orient="auto">'
            '<path d="M0,0 L14,7 L0,14 z" fill="#475569"/></marker></defs>')
    return (f'<div><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="sans-serif">' + defs
            + "".join(parts) + "</svg></div>")


def tree_svg(nodes, w=1500, h=420, hi=None, size=26, dx=330, dy=62, x0=40, y0=30):
    """Cây thư mục: nodes = [(độ sâu, tên, loại)], loại 'd' thư mục / 'f' tệp; hi = chỉ số nút được tô (nơi đang đứng).
    Vẽ từ trên xuống, mỗi độ sâu thụt dx; đường nối từ cha tới con."""
    parts = []
    pos = []
    stack = {}
    for i, (dep, name, kind) in enumerate(nodes):
        x, y = x0 + dep * dx, y0 + i * dy
        pos.append((x, y))
        stack[dep] = i
        if dep > 0:
            p = stack[dep - 1]
            px, py = pos[p]
            parts.append(f'<path d="M{px + 18},{py + 22} L{px + 18},{y + 20} L{x - 8},{y + 20}" fill="none" stroke="#6b7280" stroke-width="3"/>')
    for i, (dep, name, kind) in enumerate(nodes):
        x, y = pos[i]
        col = C_AMBER if hi == i else (C_BLUE if kind == "d" else C_GRAY)
        label = ("▸ " if kind == "d" else "") + name
        width = max(130, int(len(label) * size * 0.62) + 28)
        parts.append(box(x, y, width, 44, label, col, size, bold=(hi == i)))
    return svg(w, h, *parts)


SAY_FORBIDDEN = re.compile(r"\b(ls|cd|pwd|mkdir|touch|echo|cat|cp|mv|rm|grep|head|tail|sort|uniq|wc|git|Git|curl|bash|Bash|sqlite|SQLite|"
                           r"select|SELECT|insert|INSERT|update|UPDATE|delete|DELETE|where|WHERE|from|FROM|commit|branch|add|log|diff|init|"
                           r"if|else|for|while|done|then|true|false|null|String|int|chmod|sed|awk|find|export|source|eval)\b")
# Từ ngoại chưa dò ASR không đọc trong lời: tả bằng tiếng Việt; tên gốc chỉ hiện trên màn hình. Danh sách này nới theo probes/f1.md (lexicon_vi.FND.yaml).

SAY_FIX = [("commit", "chốt")]
_ID_RE = re.compile(r"(?<![\w])id(?![\w])")


def fix_say(t):
    for a_, b_ in SAY_FIX:
        t = t.replace(a_, b_)
    return _ID_RE.sub("mã", t)


def st(show, say, focus=None, introduces=None, pause=None, clear=None, forward_ref=None, notation_note=None):
    d = {"show": show.strip("\n") + "\n" if "\n" in show else show}
    if ("<svg" in show or 'class="code"' in show) and clear is None:
        clear = True  # hình hay khối mã chiếm nhiều chỗ: thay khung trước
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


def sc(id, kind, title, steps, checks=None):
    if kind == "quiz":
        pi = next((i for i, s_ in enumerate(steps) if s_.get("pause")), None)
        if pi is not None:
            for i, s_ in enumerate(steps[pi + 1:], pi + 1):
                if i == pi + 1 or "<table" in s_["show"] or 'class="code"' in s_["show"]:
                    s_["clear"] = True
    for i, s_ in enumerate(steps):      # mỗi step sau thay khung (khung chỉ chứa một step): tránh tràn khi các step dồn lại
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
    """Gọi đầu build(): gắn các cmd(...) khai sau đó với bài này (bộ kiểm in theo bài)."""
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
    """Từ khoá tiếng Anh / tên lệnh chưa dò phát âm lọt vào lời đọc → danh sách (cảnh, step, từ)."""
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
