"""Thư viện dựng đặc tả bài JVA (Lập trình Java từ con số 0) từ dữ liệu Python. Mỗi bài: audit/jva/src/lXX.py có hàm build().
Chạy: .venv/Scripts/python audit/jva/gen.py [L01 …]  → ghi lessons/jva/Lxx_<slug>.yaml (YAML do yaml.dump sinh).

Khác BNK: mọi chương trình Java hiện trên màn hình được khai bằng prog(...) — mã nguồn ĐẦY ĐỦ, kết quả in ra mong đợi.
audit/jva/verify_jva.py gom mọi prog đã khai, biên dịch bằng javac và chạy bằng java thật (JDK 22 trên máy), so từng dòng in ra.
Vì vậy: không gõ mã hay kết quả trực tiếp vào chuỗi show; luôn dùng code_block(p) và out_block(p)."""
import html
import textwrap
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import lv  # noqa: E402

COURSE = "JVA"
SERIES = "JVA · Lập trình Java từ con số 0"

C_BLUE = ("#dbeafe", "#2a78d6")
C_GREEN = ("#dcfce7", "#16a34a")
C_AMBER = ("#fef3c7", "#d97706")
C_RED = ("#fee2e2", "#dc2626")
C_GRAY = ("#e5e7eb", "#6b7280")
C_PURPLE = ("#f3e8ff", "#9333ea")

# ── chương trình Java khai bằng dữ liệu, để bộ kiểm chạy thật ─────────────────────────────────────────────────────────────
PROGRAMS = []  # mỗi phần tử: dict(name, code, out, expect, lesson)
_CURRENT = {"lesson": None}


def prog(name, code, out="", expect="run", note="", err=""):
    """Khai một chương trình. name = tên lớp công khai (tệp name.java). code = mã nguồn đầy đủ (thụt lề 4 dấu cách).
    out = các dòng in ra mong đợi (chuỗi, mỗi dòng một dòng). expect: "run" (chạy bình thường, so out);
    "compile_error:<chuỗi con>" (javac phải báo lỗi chứa chuỗi con); "runtime_error:<tên ngoại lệ>" (chạy rồi ném ngoại lệ đó;
    out là phần in ra TRƯỚC khi ném). err = dòng báo lỗi hiện trên màn hình; bộ kiểm đòi nó có NGUYÊN VĂN trong stderr."""
    p = {"name": name, "code": code.strip("\n"), "out": out.strip("\n"), "expect": expect, "note": note,
         "lesson": _CURRENT["lesson"], "err": err}
    PROGRAMS.append(p)
    return p


KW = ("public|private|protected|class|static|void|int|long|double|boolean|char|byte|short|float|new|return|if|else|for|while|do|"
      "switch|case|default|break|continue|try|catch|finally|throw|throws|final|this|null|true|false|var|record|enum|interface|"
      "implements|extends|import|package|instanceof|yield")
_KW_RE = re.compile(r"\b(" + KW + r")\b")


def _hl(line):
    """Tô từ khoá trong một dòng đã thoát HTML; chú thích // … tô xám. Không tô bên trong chuỗi "…"."""
    code, cm = line, ""
    m = re.search(r"//", line)
    if m and line[:m.start()].count('"') % 2 == 0:
        code, cm = line[:m.start()], line[m.start():]
    parts = re.split(r'("(?:[^"\\]|\\.)*")', code)
    for i in range(0, len(parts), 2):
        parts[i] = _KW_RE.sub(r'<span class="kw">\1</span>', html.escape(parts[i], quote=False))
    for i in range(1, len(parts), 2):
        parts[i] = html.escape(parts[i], quote=False)
    out = "".join(parts)
    if cm:
        out += f'<span class="cm">{html.escape(cm, quote=False)}</span>'
    return out


def code_lines(text):
    return "".join(f"<div>{_hl(l) if l.strip() else ' '}</div>" for l in text.split("\n"))


def code_block(p, lines=None, title=None):
    """Khối mã của chương trình p (cả tệp, hoặc chỉ các dòng lines=(đầu, cuối) tính từ 1, gồm cả hai đầu)."""
    src = p["code"].split("\n")
    if lines:
        src = textwrap.dedent("\n".join(src[lines[0] - 1:lines[1]])).split("\n")
    t = f'<p><b>{title}</b></p>' if title else ""
    return t + '<div class="code">' + code_lines("\n".join(src)) + "</div>"


def out_block(p, title="Kết quả chạy"):
    lines = p["out"].split("\n") if p["out"] else []
    body = "".join(f"<div>{html.escape(l, quote=False) or ' '}</div>" for l in lines)
    if p["expect"].startswith("runtime_error:"):
        e = p["err"] or ("Exception … " + p["expect"].split(":", 1)[1])
        body += f'<div><span class="cm">{html.escape(e, quote=False)}</span></div>'
    if p["expect"].startswith("compile_error:"):
        body = f'<div><span class="cm">error: {html.escape(p["expect"].split(":", 1)[1])}</span></div>'
    return f"<p><b>{title}</b></p>" + '<div class="code">' + body + "</div>"


# ── hình vẽ (giống BNK) ──────────────────────────────────────────────────────────────────────────────────────────────────
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
        out += txt((x1 + x2) // 2, (y1 + y2) // 2 - 10, label, size, "middle", color)
    return out


def svg(w, h, *parts):
    defs = ('<defs><marker id="ah" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" refX="10" refY="7" orient="auto">'
            '<path d="M0,0 L14,7 L0,14 z" fill="#475569"/></marker></defs>')
    return (f'<div><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="sans-serif">' + defs
            + "".join(parts) + "</svg></div>")


# Lời đọc: KHÔNG đọc từ khoá tiếng Anh của Java (if, for, while, class, static…) — tả bằng tiếng Việt, từ gốc chỉ hiện trên màn hình
# (luật kho: không bịa phiên âm chưa thử bằng ASR). SAY_FIX chặn các lỡ tay hay gặp.
SAY_FIX = [
    ("commit", "chốt"), ("rollback", "hoàn tác"),
    ("Đến lượt bạn. ", "Bây giờ tới phần bạn tự làm bài. "),
]
_ID_RE = re.compile(r"(?<![\w])id(?![\w])")
# từ khoá tiếng Anh cấm xuất hiện trong lời đọc (lint của kho không biết luật riêng này; gen.py kiểm trước khi ghi)
SAY_FORBIDDEN = re.compile(r"\b(if|else|for|while|switch|case|class|static|void|public|private|return|new|null|true|false|"
                           r"String|int|double|boolean|main|println|System|ArrayList|HashMap|try|catch|throw|Exception)\b")


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
    """Gọi đầu build(): gắn các prog(...) khai sau đó với bài này (bộ kiểm in theo bài)."""
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
    """Từ khoá tiếng Anh lọt vào lời đọc → danh sách (cảnh, step, từ)."""
    bad = []
    for sc_ in spec["scenes"]:
        for i, s_ in enumerate(sc_["steps"]):
            for m in SAY_FORBIDDEN.finditer(s_["say"]):
                bad.append((sc_["id"], i, m.group(0)))
    return bad


def lesson(id, slug, title, source, objectives, scenes, assumes=None, rate="-5%"):
    _auto_introduce(scenes)
    return slug, {
        "id": id, "course": COURSE, "series": SERIES, "title": title, "voice": "vi-VN-NamMinhNeural", "rate": rate,
        "depth": "full", "source": source, "assumes": assumes or [], "objectives": objectives, "asr_reviewed": [],
        "scenes": scenes,
    }


def dump(spec):
    return yaml.dump(spec, allow_unicode=True, sort_keys=False)
