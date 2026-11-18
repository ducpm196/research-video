"""Thư viện dựng đặc tả bài BNK từ dữ liệu Python (tránh sửa YAML bằng tay). Mỗi bài: audit/bnk/src/lXX.py có hàm build().
Chạy: .venv/Scripts/python audit/bnk/gen.py [L01 …]  → ghi lessons/bnk/Lxx_<slug>.yaml (YAML do yaml.dump sinh, an toàn với \\ và $)."""
import html
import re
import sys
import textwrap
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import lv  # noqa: E402

SERIES = "BNK · Nền tảng Backend Ngân hàng cho người mất gốc"

# ── chương trình khai bằng dữ liệu (AF2): mã hiện trên màn hình CHẠY THẬT ─────────────────────────────────────────────────
# prog(...) khai một chương trình đầy đủ + đầu ra mong đợi; code_block(p)/out_block(p) dựng khối màn hình từ đúng mã đó.
# audit/bnk/screen_gen.py sinh sổ audit/review/screen_code/BNK.yaml từ PROGRAMS: mỗi chương trình là một NGUỒN chạy thật
# (screen_code.py check --course BNK), mỗi khối trên màn hình là đoạn (fragment) của nguồn hoặc đầu ra (output) của nguồn.
PROGRAMS = []
_CURRENT = {"lesson": None}


def begin(lesson_id):
    _CURRENT["lesson"] = lesson_id


def prog(name, code, out="", lang="java", extra=None):
    """name: tên lớp công khai (java) hoặc tên nguồn. lang: java | python | sqlite | bash | oracle | mssql.
    extra: trường thêm cho nguồn trong sổ (files, timeout, java_wrap, prelude…)."""
    p = {"name": name, "code": code.strip("\n"), "out": out.strip("\n"), "lang": lang, "extra": extra or {},
         "lesson": _CURRENT["lesson"]}
    PROGRAMS.append(p)
    return p


_KW = {
    "java": r"public|private|protected|class|static|void|int|long|double|boolean|char|byte|new|return|if|else|for|while|do|"
            r"switch|case|break|continue|try|catch|finally|throw|throws|final|this|null|true|false|var|record|interface|"
            r"implements|extends|import|synchronized|volatile",
    "python": r"def|class|return|if|elif|else|for|while|in|import|from|as|with|try|except|finally|raise|lambda|None|True|False|not|and|or|pass",
    "sqlite": r"SELECT|FROM|WHERE|CREATE|TABLE|INDEX|INSERT|INTO|VALUES|UPDATE|SET|DELETE|ORDER|BY|GROUP|PRIMARY|KEY|UNIQUE|ON|AND|OR|RECURSIVE|WITH|DEFAULT|UNION|ALL|HAVING|IGNORE|"
              r"NOT|NULL|EXPLAIN|QUERY|PLAN|INTEGER|TEXT|COUNT|SUM|DROP|BEGIN|COMMIT|ROLLBACK|LIMIT|AS|JOIN|DISTINCT",
    "bash": r"if|then|fi|do|done|for|while|echo|kill|sleep",
}
_KW["oracle"] = _KW["mssql"] = _KW["sqlite"]
_CMT = {"java": "//", "python": "#", "sqlite": "--", "oracle": "--", "mssql": "--", "bash": "#"}


def _hl(line, lang="java"):
    """Tô từ khoá; chú thích tô xám. Không tô trong chuỗi "…" hay '…'."""
    mark = _CMT.get(lang, "//")
    code, cm = line, ""
    m = re.search(re.escape(mark), line)
    if m and line[:m.start()].count('"') % 2 == 0 and line[:m.start()].count("'") % 2 == 0:
        code, cm = line[:m.start()], line[m.start():]
    flags = re.I if lang in ("sqlite", "oracle", "mssql") else 0
    rx = re.compile(r"\b(" + _KW.get(lang, _KW["java"]) + r")\b", flags)
    parts = re.split(r'("(?:[^"\\]|\\.)*"|\'[^\']*\')', code)
    for i in range(0, len(parts), 2):
        parts[i] = rx.sub(r'<span class="kw">\1</span>', html.escape(parts[i], quote=False))
    for i in range(1, len(parts), 2):
        parts[i] = html.escape(parts[i], quote=False)
    out = "".join(parts)
    if cm:
        out += f'<span class="cm">{html.escape(cm, quote=False)}</span>'
    return out


def code_block(p, lines=None, title=None):
    """Khối mã của chương trình p (cả tệp, hoặc các dòng lines=(đầu, cuối) tính từ 1, gồm cả hai đầu). Khung ≤ 12 dòng."""
    src = p["code"].split("\n")
    if lines:
        src = textwrap.dedent("\n".join(src[lines[0] - 1:lines[1]])).split("\n")
    assert len(src) <= 14, f"khối mã {p['name']} dài {len(src)} dòng (> 14)"
    t = f"<p><b>{title}</b></p>" if title else ""
    return t + '<div class="code">' + "".join(f"<div>{_hl(l, p['lang']) if l.strip() else ' '}</div>" for l in src) + "</div>"


def out_block(p, title="Kết quả chạy thật"):
    body = "".join(f"<div>{html.escape(l, quote=False) or ' '}</div>" for l in (p["out"].split("\n") if p["out"] else []))
    return f"<p><b>{title}</b></p>" + '<div class="code">' + body + "</div>"

C_BLUE = ("#dbeafe", "#2a78d6")
C_GREEN = ("#dcfce7", "#16a34a")
C_AMBER = ("#fef3c7", "#d97706")
C_RED = ("#fee2e2", "#dc2626")
C_GRAY = ("#e5e7eb", "#6b7280")
C_PURPLE = ("#f3e8ff", "#9333ea")


def txt(x, y, s, size=24, anchor="middle", fill="#1f2937", bold=False, halo=False):
    """halo=True: viền trắng quanh chữ (paint-order) để nét/mũi tên chạy ngang không cắt chữ."""
    w = ' font-weight="bold"' if bold else ""
    h = ' stroke="#ffffff" stroke-width="8" stroke-linejoin="round" paint-order="stroke"' if halo else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}"{w}{h}>{s}</text>'


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
    if label:  # nhãn nằm trên nét, có viền trắng để nét không cắt chữ
        out += txt((x1 + x2) // 2, (y1 + y2) // 2 - 12, label, size, "middle", color, halo=True)
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
    ("Ôn ba điều.", "Trước hết, ta cần hiểu ba điều sẽ dùng trong bài."), ("Ôn năm mảnh ghép.", "Trước hết, ta nhắc lại từ đầu năm mảnh ghép sẽ dùng."),
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
            if _CURRENT["lesson"] in ("L12", "L13"):  # R7: khung nhấn không bọc tiêu đề "Kết quả chạy thật" mà bọc khối kết quả ngay sau nó
                def _is_title(u):
                    return u["tag"] == "p" and len(u["kids"]) == 1 and u["kids"][0]["tag"] == "b"
                focus = [f + 1 if f < len(units) and _is_title(units[f - 1]) and units[f]["tag"] == "div" else f for f in focus]
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
    def _c(c):  # ô tải "×10 000": không ngắt dòng giữa các nhóm số
        return f'<span style="white-space:nowrap">{c}</span>' if isinstance(c, str) and c.startswith("×") and "<" not in c else c
    body = "".join("<tr>" + "".join(f"<td>{_c(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table class='{cls}'><tr>{h}</tr>{body}</table>"


# ── bảng "cách đọc cú pháp Java" dùng chung (R4: bài tự đứng được, nhắc lại một dòng ở mỗi bài dùng lại) ─────────────────────
# Một khuôn duy nhất: cột "viết trong mã | đọc là | ví dụ". jstep([(khoá, ví_dụ_html, ví_dụ_lời_đọc), …]) dựng một step.
JHEAD = ["viết trong mã", "đọc là", "ví dụ"]
JROW = {
    "sig": ("<code>public static kiểu tên(kiểu a, kiểu b)</code>",
            "khai một hàm: <b>kiểu trả về</b> (<code>void</code> là không trả gì), <b>tên</b>, rồi <b>tham số</b> trong ngoặc tròn, mỗi tham số là kiểu rồi tên; <code>static</code>: thuộc cả lớp; <code>public</code>: nơi khác gọi được",
            "Khai một hàm gồm kiểu giá trị trả về, rỗng nghĩa là không trả gì, rồi tên hàm, rồi các tham số trong ngoặc tròn, mỗi tham số là kiểu rồi tên. "
            "Chữ tĩnh nghĩa là hàm thuộc cả lớp, chữ công khai nghĩa là nơi khác gọi được."),
    "final": ("<code>static final Kiểu TÊN = …;</code>",
              "biến dùng chung cho cả lớp; <code>final</code>: gán giá trị một lần rồi không đổi nữa",
              "Chữ cuối cùng nghĩa là gán giá trị một lần rồi không đổi nữa, còn chữ tĩnh nghĩa là biến dùng chung cho cả lớp."),
    "default": ("<code>tên KIỂU DEFAULT giá_trị</code>",
                "cột có giá trị mặc định: dòng mới thêm mà không ghi cột này thì tự mang giá trị đó",
                "Chữ mặc định sau kiểu cột nghĩa là dòng mới thêm mà không ghi cột này thì tự mang giá trị đó."),
    "count": ("<code>SELECT COUNT(*) FROM bảng;</code>",
              "đếm số dòng của bảng",
              "Lệnh chọn đếm cho biết số dòng hiện có của một bảng."),
    "call": ("<code>hàm(a, b)</code>, <code>s.length()</code>",
             "gọi một hàm: các giá trị trong ngoặc tròn là đối số; <code>s.length()</code> cho số ký tự của chuỗi s",
             "Gọi một hàm thì các giá trị trong ngoặc tròn là đối số, và chấm độ dài kèm ngoặc tròn cho số ký tự của chuỗi."),
    "strmul": ("<code>\"x\" * n</code>",
               "nhân chuỗi: lặp chuỗi n lần, nối liền nhau",
               "Nhân một chuỗi với một số nghĩa là lặp chuỗi đó chừng ấy lần, nối liền nhau."),
    "encode": ("<code>chuỗi.encode()</code>",
               "đổi chuỗi chữ thành dãy byte, vì hàm mã xác thực chỉ nhận byte",
               "Lệnh mã hoá chuỗi đổi chữ thành dãy byte, vì hàm mã xác thực chỉ nhận byte."),
    "sorted": ("<code>sorted(từ_điển)</code>",
               "danh sách các khoá của từ điển, xếp từ nhỏ đến lớn",
               "Hàm sắp xếp trả về các khoá của từ điển, xếp từ nhỏ đến lớn."),
    "runtime": ("<code>Runtime rt = Runtime.getRuntime();</code>", "<code>Runtime</code>: đối tượng đại diện chương trình đang chạy; <code>totalMemory() − freeMemory()</code> = bộ nhớ đang dùng",
                "Đối tượng Runtime đại diện chương trình đang chạy, và tổng bộ nhớ đã xin trừ phần còn trống là bộ nhớ đang dùng."),
    "try": ("<code>try { … } catch (Lỗi e) { }</code>", "thử chạy khối; nếu bị ngắt giữa chừng thì vào <code>catch</code>; để trống vì ta không cần xử lý",
            "Khối thử chạy phần việc, nếu bị ngắt giữa chừng thì nhảy vào khối bắt, ở đây để trống vì ta không cần xử lý."),
    "pk": ("<code>CREATE TABLE t (khoa TEXT PRIMARY KEY, …)</code>", "khai bảng; cột <code>PRIMARY KEY</code> không cho hai dòng trùng giá trị",
           "Lệnh tạo bảng khai các cột, và cột khoá chính không cho hai dòng trùng giá trị."),
    "ignore": ("<code>INSERT OR IGNORE INTO t VALUES (…)</code>", "thêm dòng; nếu trùng khoá thì bỏ qua, không báo lỗi",
               "Lệnh thêm dòng bỏ qua nếu trùng khoá, không báo lỗi."),
    "selwhere": ("<code>SELECT cột FROM t WHERE khoa = 'abc'</code>", "lấy cột của những dòng có khoá bằng <code>'abc'</code>",
                 "Lệnh chọn lấy cột của những dòng có khoá bằng giá trị đã cho."),
    "txn": ("<code>BEGIN; … COMMIT;</code>", "mở giao dịch; chốt lưu mọi thay đổi bên trong cùng lúc",
            "Lệnh bắt đầu mở giao dịch, lệnh chốt lưu mọi thay đổi bên trong cùng lúc."),
    "rollback": ("<code>ROLLBACK;</code>", "huỷ mọi thay đổi của giao dịch đang mở", "Lệnh huỷ bỏ mọi thay đổi của giao dịch đang mở."),
    "update": ("<code>UPDATE t SET c = c - 500000 WHERE tk = 'A'</code>", "sửa cột c của những dòng thoả điều kiện: trừ 500 000 ở số dư của A",
               "Lệnh cập nhật sửa một cột của những dòng thoả điều kiện, ở đây trừ năm trăm nghìn ở số dư của A."),
    "insertcols": ("<code>INSERT INTO outbox (su_kien) VALUES (…)</code>", "thêm dòng chỉ ghi cột <code>su_kien</code>; cột còn lại lấy giá trị mặc định",
                   "Lệnh thêm dòng này chỉ ghi cột sự kiện, cột còn lại lấy giá trị mặc định."),
    "diamond": ("<code>new ArrayList&lt;&gt;()</code>", "<code>&lt;&gt;</code> để trống: Java tự điền kiểu theo vế trái",
                "Cặp ngoặc nhọn để trống nghĩa là Java tự điền kiểu theo vế trái."),
    "inc1": ("<code>x++</code>", "tăng x thêm 1", "Hai dấu cộng sau tên biến tăng biến thêm một."),
    "dec": ("<code>j--</code>, <code>j &gt;= 0</code>", "<code>j--</code>: giảm j đi 1; <code>&gt;=</code>: lớn hơn hoặc bằng",
            "Hai dấu trừ giảm biến đi một, và dấu lớn hơn hoặc bằng so sánh hai giá trị."),
    "concat": ("<code>\"chữ\" + giá_trị</code>", "dấu <code>+</code> giữa chữ và một giá trị nối chúng thành một chuỗi",
               "Dấu cộng giữa chữ và một giá trị nối chúng thành một chuỗi."),
    "cmp": ("<code>&lt;=</code>, <code>&gt;=</code>, <code>==</code>, <code>!=</code>", "nhỏ hơn hoặc bằng; lớn hơn hoặc bằng; bằng nhau; khác nhau",
            "Các dấu so sánh gồm nhỏ hơn hoặc bằng, lớn hơn hoặc bằng, bằng nhau, và khác nhau."),
    "modulo": ("<code>a / b</code>, <code>a % b</code>", "với số nguyên: <code>/</code> chia lấy phần nguyên; <code>%</code> lấy phần dư",
               "Với số nguyên, dấu chia lấy phần nguyên, còn dấu phần trăm lấy phần dư."),
    "inssel": ("<code>INSERT INTO t SELECT …</code>", "chèn mọi dòng mà truy vấn trả về; <code>-tien</code> đổi dấu số tiền",
               "Lệnh chèn kèm truy vấn thêm mọi dòng mà truy vấn trả về, ở đây đổi dấu số tiền."),
    "map": ("<code>cho.put(k, v)</code>, <code>cho.get(k)</code>, <code>a.equals(b)</code>", "<code>put</code> cất giá trị v dưới khoá k; <code>get</code> lấy giá trị theo khoá; <code>equals</code> so nội dung hai chuỗi",
            "Lệnh cất đặt giá trị dưới một khoá, lệnh lấy trả giá trị theo khoá, và lệnh so bằng so nội dung hai chuỗi."),
    "arrinit": ("<code>String[] ve = { \"…\", \"…\" };</code>", "khai mảng chuỗi và điền sẵn các phần tử trong cặp ngoặc nhọn",
                "Cặp ngoặc nhọn sau dấu bằng điền sẵn các phần tử của mảng."),
    "pyidx": ("<code>d[k]</code>", "lấy giá trị của khoá k trong từ điển d; <code>truong[2]</code> là giá trị của khoá 2",
              "Ngoặc vuông kèm khoá lấy giá trị của khoá đó trong từ điển."),
    "pycmt": ("<code># chú thích</code>", "chú thích Python: máy bỏ qua phần sau dấu thăng", "Dấu thăng mở đầu một chú thích Python, máy bỏ qua."),
    "pyassign": ("<code>a, b = x, y</code>", "gán hai biến một lúc: a nhận x, b nhận y", "Gán song song đặt hai biến cùng lúc: biến đầu nhận giá trị đầu, biến sau nhận giá trị sau."),
    "pygen": ("<code>\"\".join(… for x, y in zip(a, b))</code>", "với mỗi cặp x, y ghép từ hai dãy, tính một mảnh chữ; <code>join</code> nối mọi mảnh lại",
              "Biểu thức sinh tính một mảnh chữ cho mỗi cặp ghép từ hai dãy, rồi lệnh nối ghép mọi mảnh thành một chuỗi."),
    "pybytes": ("<code>b\"k\"</code>", "chữ <code>b</code> trước dấu nháy: chuỗi byte, không phải chuỗi chữ", "Chữ b trước dấu nháy báo đây là chuỗi byte, không phải chuỗi chữ."),
    "nano": ("<code>System.nanoTime()</code>, <code>/ 1_000_000</code>", "<code>nanoTime</code>: đồng hồ chính xác tính bằng nano giây; chia 1 triệu ra mili giây",
             "Đồng hồ nano giây rất chính xác, và chia cho một triệu thì ra mili giây."),
    "thread": ("<code>t.start(); t.join();</code>", "<code>start</code>: cho luồng t chạy; <code>join</code>: chờ luồng t chạy xong",
               "Lệnh bắt đầu cho luồng chạy, còn lệnh chờ xong chờ luồng đó chạy xong."),
    "sb": ("<code>sb.append(x)</code>", "<code>StringBuilder</code>: hộp chữ nối được; <code>append</code> thêm x vào cuối",
           "Hộp chữ nối được dựng dòng in dần, và lệnh thêm đưa mảnh mới vào cuối."),
    "base": ("<code>System.out.println(x)</code>, <code>return</code>, <code>//</code>, <code>import</code>, <code>\"a\" + x</code>", "in x ra màn hình; trả giá trị về; chú thích; nhập lớp có sẵn; nối chữ",
             "In giá trị ra màn hình, trả về đưa giá trị cho nơi gọi, hai gạch chéo mở chú thích, dòng nhập lấy lớp có sẵn, và dấu cộng nối chữ."),
    "pyeq": ("<code>==</code>, <code>#</code>", "<code>==</code>: so hai giá trị có bằng nhau không; <code>#</code>: chú thích, máy bỏ qua",
             "Hai dấu bằng so hai giá trị có bằng nhau không, và dấu thăng mở một chú thích."),
    "pyeq1": ("<code>==</code>", "so hai giá trị có bằng nhau không", "Hai dấu bằng so hai giá trị có bằng nhau không."),
    "throws": ("<code>… throws Lỗi {</code>",
               "lời báo: hàm này có thể ném lỗi loại đó; hàm không tự xử lý mà chuyển lỗi lên cho nơi gọi xử lý",
               "Lời báo ném lỗi nghĩa là hàm có thể ném lỗi loại đó, và không tự xử lý mà chuyển lỗi lên cho nơi gọi xử lý."),
    "main": ("<code>public static void main(String[] args)</code>",
             "hàm chính: chương trình bắt đầu chạy từ đây; <code>args</code> là mảng chuỗi gõ thêm sau lệnh chạy, bài này không dùng",
             "Hàm chính là nơi chương trình bắt đầu chạy, và tham số mảng chuỗi chứa các chữ gõ thêm sau lệnh chạy, bài này không dùng."),
    "cmt": ("<code>// chú thích</code>", "chú thích: máy bỏ qua, chỉ để người đọc hiểu mã",
            "Hai gạch chéo mở đầu một chú thích, máy bỏ qua, chỉ để người đọc hiểu mã."),
    "incr": ("<code>x++</code>, <code>x += 5</code>", "<code>x++</code>: tăng x thêm 1; <code>x += 5</code>: tăng x thêm 5",
             "Hai dấu cộng tăng biến thêm một, còn cộng bằng tăng biến thêm đúng số đứng sau."),
    "for": ("<code>for (int i = 0; i &lt; n; i++) { … }</code>", "vòng lặp: i bắt đầu từ 0, còn i &lt; n thì làm khối, mỗi vòng tăng i thêm 1",
            "Vòng lặp có ba phần trong ngoặc: điểm bắt đầu, điều kiện để chạy tiếp, và bước tăng sau mỗi vòng."),
    "if": ("<code>if (điều_kiện) { … } else { … }</code>", "nếu điều kiện đúng thì làm khối đầu, không thì làm khối sau <code>else</code>",
           "Nếu điều kiện đúng thì làm khối thứ nhất, nếu không thì làm khối còn lại."),
    "ret": ("<code>return giá_trị;</code>", "trả giá trị về cho nơi gọi hàm, và hàm kết thúc",
            "Lệnh trả về đưa một giá trị cho nơi gọi hàm và kết thúc hàm."),
    "arr": ("<code>int[] dem = new int[5];</code>", "khai mảng <code>dem</code> gồm 5 số nguyên, ban đầu đều 0; ô đầu là <code>dem[0]</code>",
            "Khai một mảng năm số nguyên, ban đầu đều bằng không, và chỉ số bắt đầu từ không."),
    "null": ("<code>null</code>, <code>&lt;&gt;</code>", "<code>null</code>: không trỏ tới đối tượng nào; <code>&lt;&gt;</code> để trống: Java tự điền kiểu",
             "Rỗng nghĩa là biến không trỏ tới đối tượng nào, còn cặp ngoặc nhọn để trống nghĩa là Java tự suy ra kiểu."),
    "write": ("<code>….write(s.getBytes())</code>", "lấy luồng ghi phản hồi của yêu cầu, rồi ghi các byte của chuỗi <code>s</code> vào đó",
              "Dòng này lấy luồng ghi phản hồi của yêu cầu rồi ghi các byte của chuỗi vào đó."),
    "sqltype": ("<code>TEXT</code>, <code>INTEGER</code>", "kiểu cột: <code>TEXT</code> chứa chữ, <code>INTEGER</code> chứa số nguyên",
                "Kiểu cột chữ chứa chuỗi chữ, kiểu cột số nguyên chứa số nguyên."),
    "values": ("<code>VALUES (…), (…)</code>", "mỗi cặp ngoặc là một dòng mới; nhiều cặp thì một lệnh thêm nhiều dòng",
               "Mỗi cặp ngoặc sau từ khoá giá trị là một dòng mới, nhiều cặp thì một lệnh thêm nhiều dòng."),
    "sqlcmt": ("<code>-- chú thích</code>", "chú thích SQL: máy bỏ qua phần sau hai gạch ngang",
               "Hai gạch ngang mở đầu một chú thích trong SQL, máy bỏ qua."),
    "recursive": ("<code>WITH RECURSIVE n(i) AS (…)</code>", "lặp tự tham chiếu: <code>AS (…)</code> đặt cho bảng tạm tên <code>n</code>; bắt đầu từ 1, <code>UNION ALL</code> nối thêm <code>i + 1</code> mỗi vòng cho tới 5000",
                  "Truy vấn lặp tự tham chiếu dựng bảng tạm, bắt đầu từ một. Chữ nối tất cả thêm số kế tiếp mỗi vòng cho tới năm nghìn, và chữ là đặt tên cho bảng tạm."),
    "cast": ("<code>(Kiểu) giá_trị</code>",
             "ép kiểu: bảo máy coi giá trị đứng sau là kiểu ghi trong ngoặc tròn",
             "Ép kiểu là bảo máy coi giá trị đứng sau thuộc kiểu ghi trong ngoặc tròn đứng trước nó."),
    "idx": ("<code>a[i]</code>, <code>a.length</code>",
            "<code>a[i]</code>: ô thứ i của mảng a, ô đầu là <code>a[0]</code>; <code>a.length</code>: số ô của mảng, không có ngoặc tròn",
            "Chỉ số trong ngoặc vuông chọn một ô của mảng, ô đầu có chỉ số không, và chấm độ dài cho biết số ô của mảng."),
    "inc": ("<code>p++</code>",
            "đưa ra giá trị hiện tại của p rồi mới tăng p thêm 1",
            "Hai dấu cộng sau tên biến nghĩa là đưa ra giá trị hiện tại rồi mới tăng biến thêm một."),
}


def jstep(items, intro="", clear=True):
    """items: [(khoá trong JROW, ví dụ HTML, ví dụ lời đọc)]. Trả về một step: bảng 'viết trong mã → đọc là → ví dụ'."""
    def _vd(t):  # dấu ";" của mã không được dính ":" / ";" của lời giải
        return t.replace("</code>: ", "</code> — ").replace("</code>; ", "</code> | ")
    rows = [[JROW[k][0], JROW[k][1], _vd(vd)] for k, vd, _ in items]
    say = (intro + " " if intro else "") + " ".join(f"{JROW[k][2]} Ví dụ, {vs}" if vs else JROW[k][2] for k, _, vs in items)
    return st(table(JHEAD, rows), say, clear=clear)


def jsteps(items, intro="", max_rows=3, max_chars=520):
    """Như jstep nhưng tự tách thành nhiều step (mỗi bảng ≤ max_rows hàng và ≤ max_chars ký tự chữ) để không TRÀN khung."""
    def _len(it):
        k, vd, _ = it
        return len(re.sub(r"<[^>]+>", "", JROW[k][0] + JROW[k][1] + vd))
    chunks, cur, n = [], [], 0
    for it in items:
        if cur and (len(cur) >= max_rows or n + _len(it) > max_chars):
            chunks.append(cur)
            cur, n = [], 0
        cur.append(it)
        n += _len(it)
    if cur:
        chunks.append(cur)
    return [jstep(c, intro if i == 0 else "") for i, c in enumerate(chunks)]


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


def add_steps(scenes, scene_id, steps, at=None):
    """Chèn thêm step vào cảnh có sẵn (cuối cảnh, hoặc vị trí at)."""
    for s_ in scenes:
        if s_["id"] == scene_id:
            if at is None:
                s_["steps"].extend(steps)
            else:
                s_["steps"][at:at] = steps
            return
    raise KeyError(scene_id)


def lesson(id, slug, title, source, objectives, scenes, assumes=None, rate="-5%", covers=None, intro=None):
    """intro: {(id_cảnh, chỉ_số_step): [id_thuật_ngữ]} — gắn `introduces` (E52) vào step giảng thuật ngữ (id trong tools/registry/symbols.BNK.yaml)."""
    _auto_introduce(scenes)
    for (sid, si), ids in (intro or {}).items():
        sc_ = next(s_ for s_ in scenes if s_["id"] == sid)
        st_ = sc_["steps"][si]
        st_["introduces"] = list(st_.get("introduces") or []) + list(ids)
    for sc_ in scenes:  # bước ngay sau bảng cách đọc (jstep) phải xoá bảng, nếu không nội dung dồn lên bảng và TRÀN khung
        for a_, b_ in zip(sc_["steps"], sc_["steps"][1:]):
            if a_["show"].startswith("<table class='t'><tr><th>" + JHEAD[0]):
                b_["clear"] = True
    for sc_ in scenes:  # cảnh Tự làm: gợi ý thay kết quả mong đợi (cả hai chung một bảng thì tràn khung)
        if sc_.get("kind") == "practice" and len(sc_["steps"]) >= 3:
            sc_["steps"][-1]["clear"] = True
    af2 = {"af2": True, "covers": [{"objective": o, "scene": s_} for o, s_ in covers]} if covers else {}
    return slug, {
        "id": id, "course": "BNK", "series": SERIES, "title": title, "voice": "vi-VN-NamMinhNeural", "rate": rate,
        "depth": "full", **af2, "source": source, "assumes": assumes or [], "objectives": objectives, "asr_reviewed": [],
        "scenes": scenes,
    }


def dump(spec):
    return yaml.dump(spec, allow_unicode=True, sort_keys=False)
