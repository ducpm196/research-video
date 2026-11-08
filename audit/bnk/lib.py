"""Thư viện dựng đặc tả bài BNK từ dữ liệu Python (tránh sửa YAML bằng tay). Mỗi bài: audit/bnk/src/lXX.py có hàm build().
Chạy: .venv/Scripts/python audit/bnk/gen.py [L01 …]  → ghi lessons/bnk/Lxx_<slug>.yaml (YAML do yaml.dump sinh, an toàn với \\ và $)."""
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import lv  # noqa: E402

SERIES = "BNK · Nền tảng Backend Ngân hàng cho người mất gốc"

C_BLUE = ("#dbeafe", "#2a78d6")
C_GREEN = ("#dcfce7", "#16a34a")
C_AMBER = ("#fef3c7", "#d97706")
C_RED = ("#fee2e2", "#dc2626")
C_GRAY = ("#e5e7eb", "#6b7280")
C_PURPLE = ("#f3e8ff", "#9333ea")


def txt(x, y, s, size=24, anchor="middle", fill="#1f2937", bold=False):
    w = ' font-weight="bold"' if bold else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}"{w}>{s}</text>'


def box(x, y, w, h, label, col=C_BLUE, size=24, bold=False, dash=False):
    """Hình chữ nhật có chữ ở giữa; label là chuỗi hoặc danh sách dòng."""
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
    """Khung chứa có tiêu đề ở sát mép trên (các hộp con vẽ bên trong, không đè tiêu đề)."""
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


# Từ ngoại chưa có cách đọc đã dò: lời đọc dùng tên tiếng Việt, tên gốc vẫn hiện trên màn hình (luật “không bịa phiên âm chưa thử bằng ASR”).
SAY_FIX = [
    ("gọi thẳng bằng this", "gọi thẳng chính nó"), ("bằng từ khoá this", "bằng cách gọi thẳng chính nó"), ("bằng this", "bằng cách gọi thẳng chính nó"),
    ("Controller", "bộ điều khiển"),
    ("Lệnh explain cho xem kế hoạch, tức là máy sẽ tìm dòng bằng cách nào. Chữ scan nghĩa là quét toàn bảng. Còn search using index là tìm qua chỉ mục.",
     "Lệnh xem kế hoạch cho biết máy sẽ tìm dòng bằng cách nào. Quét toàn bảng là đọc từng dòng. Còn tìm qua chỉ mục là đi theo cây tới thẳng dòng cần."),
    ("từ khoá where", "mệnh đề điều kiện"), ("ta dùng sqlite", "ta dùng một cơ sở dữ liệu nhỏ"),
    ("Byte đầu", "Khúc đầu"), ("Byte thứ hai", "Khúc thứ hai"), ("Byte hai", "Khúc hai"), ("Byte tiếp theo", "Khúc tiếp theo"), ("hex", "thập lục phân"),
    # câu quá ngắn bị TTS/ASR làm méo (⚠ NGẮN): ghép thêm ý, giữ nguyên nghĩa
    ("Ôn ba điều.", "Trước hết ta ôn lại ba điều sẽ dùng."), ("Ôn năm mảnh ghép.", "Trước hết ta ôn lại năm mảnh ghép sẽ dùng."),
    ("Đến lượt bạn. ", "Bây giờ tới phần bạn tự làm bài. "), ("Bộ đệm có thể cũ.", "Bộ đệm có thể chứa dữ liệu đã cũ."),
    ("Dịch vụ hỏi Redis trước.", "Trước tiên, dịch vụ sẽ hỏi Redis trước."), ("Kết quả khớp từng trường.", "Kết quả đọc lại khớp từng trường một."),
    ("Bảng này giải thích chênh lệch.", "Bảng này giải thích từng nguồn chênh lệch giữa hai tổng."), ("A một khớp.", "Mã a một khớp ở cả hai sổ."),
    ("Giao dịch cân đối.", "Vậy giao dịch này cân đối."), ("Bảng này tổng hợp.", "Bảng này tổng hợp lại ba trường hợp."),
    ("Vậy cần bốn tầng.", "Vậy cây này cần bốn tầng."),
    # từ ngoại dò ASR không đạt 7/8 (audit/bnk/probes/b1.md): lời đọc dùng tiếng Việt, tên gốc chỉ hiện trên màn hình
    ("Temenos T24", "T24"),
    ("commit", "chốt"), ("rollback", "hoàn tác"), ("Topic", "Chủ đề"), ("topic", "chủ đề"),
    ("Luhn là phép kiểm số cuối của số thẻ, bắt lỗi gõ nhầm.", "Còn phép kiểm số kiểm cuối của số thẻ bắt lỗi gõ nhầm."), ("phép kiểm Luhn", "phép kiểm số kiểm cuối"),
]
_ID_RE = re.compile(r"(?<![\w])id(?![\w])")


def fix_say(t):
    for a_, b_ in SAY_FIX:
        t = t.replace(a_, b_)
    return _ID_RE.sub("mã", t)


def st(show, say, focus=None, introduces=None, pause=None, clear=None, forward_ref=None, notation_note=None):
    d = {"show": show.strip("\n") + "\n" if "\n" in show else show}
    if "<svg" in show and clear is None:
        clear = True  # mỗi hình SVG chiếm cả bảng, thay hình trước
    if focus is None and show.strip():
        # focus tự động: câu j nói về phần ⌊j·u/n⌋+1 của khối (u phần, n câu) — khớp luật E31/E32 của lint
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
    if kind == "quiz":  # đáp án thay đề; mỗi bảng đáp án thay bảng trước (tránh tràn khung)
        pi = next((i for i, s_ in enumerate(steps) if s_.get("pause")), None)
        if pi is not None:
            for i, s_ in enumerate(steps[pi + 1:], pi + 1):
                if i == pi + 1 or "<table" in s_["show"]:
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


def _auto_introduce(scenes):
    """Ký hiệu trong sổ chung phải được khai `introduces` ở step đầu tiên dùng nó (luật “ký hiệu trước khi dùng”) — tự gắn nếu bài chưa khai."""
    for sym, tex in (("cdot", r"\cdot"), ("implies", r"\Rightarrow")):
        if any(sym in (s_.get("introduces") or []) for sc_ in scenes for s_ in sc_["steps"]):
            continue
        done = False
        for sc_ in scenes:
            for s_ in sc_["steps"]:
                if tex in s_["show"] and not done:
                    s_["introduces"] = list(s_.get("introduces") or []) + [sym]
                    done = True


def lesson(id, slug, title, source, objectives, scenes, assumes=None, rate="-5%"):
    _auto_introduce(scenes)
    return slug, {
        "id": id, "course": "BNK", "series": SERIES, "title": title, "voice": "vi-VN-NamMinhNeural", "rate": rate,
        "depth": "full", "source": source, "assumes": assumes or [], "objectives": objectives, "asr_reviewed": [],
        "scenes": scenes,
    }


def dump(spec):
    return yaml.dump(spec, allow_unicode=True, sort_keys=False)
