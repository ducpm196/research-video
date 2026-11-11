"""Cổng "mã trên màn hình": mọi khối mã người học THẤY phải được kiểm NGUYÊN VĂN.

Vì sao: `checks:` của bài gọi hàm trong tools/checklib.py, không chạy đoạn mã hiện trên màn hình, nên mã trên
màn hình có thể sai cú pháp hoặc thiếu hàm mà mọi cổng vẫn PASS (lỗi thật: SDP L02 thiếu `nap`, SDP L04/L05
`class X:   def …` trên một dòng — mẫu D/E 2026-11-10).

KHỐI MÃ = phần tử có class chứa từ "code" (`<div class="code">`, `<div class="box code">`, `<pre class="code">`)
hoặc `<pre>`; mỗi dòng là một `<div>` con (player.css: `.code > div { white-space: pre }`) hoặc dòng của <pre>.
Văn bản khối = bỏ thẻ, giải mã thực thể HTML, ghép dòng bằng "\\n", bỏ khoảng trắng cuối dòng.
NGOÀI PHẠM VI: mã nội dòng `<code>` trong câu, chữ trong <svg>.

SỔ: audit/review/screen_code/<KHOÁ>.yaml, `blocks: {"<KHOÁ> <Lxx> <scene_id> <step> <khối>": mục}`. Mỗi mục GHIM
`sha` = 16 hex đầu sha256 văn bản khối; đổi một ký tự trên màn hình → STALE → cổng FAIL tới khi kiểm lại.

Trường chung: kind (bắt buộc), lang, reason (bắt buộc với fragment/pseudo/output/other), note.
kind:
  run       chạy NGUYÊN VĂN. lang: python | sqlite | java | node | bash | go.
            prelude_keys: [khoá khối khác]  — nối văn bản (đã ghim) của khối đó lên trước (mã bài đã hiện ở khung khác)
            prelude: chuỗi  — chỉ dữ liệu/nhập thư viện mà bài NÓI ra nhưng không hiện thành mã; bắt buộc prelude_reason
            post: chuỗi     — khẳng định kết quả bài nói (assert …); claims: [trích nguyên chữ điều bài nói, …]
            expect_stdout / expect_rc / expect_stderr_contains / expect_compile_error (java) / java_class / java_wrap
            Bắt buộc có ít nhất một trong post / expect_stdout / expect_compile_error / expect_stderr_contains,
            HOẶC no_claim_reason (bài không nói kết quả nào của khối).
  syntax    chỉ kiểm cú pháp nguyên văn: python (compile), sqlite (EXPLAIN trên prelude), java (javac, java_wrap
            "{CODE}"), node (--check), bash (-n), go (gofmt -e, go_wrap), c (pycparser, c_wrap "{CODE}",
            c_typedefs). Dùng khi mã đúng nhưng cần môi trường ngoài, hoặc ngôn ngữ không chạy được trên máy (C).
  fragment  đoạn trích. Nếu `within: <khoá khối>` thì cổng kiểm các dòng (bỏ thụt lề chung) là một DÃY LIÊN TIẾP
            trong khối đó (khối đó phải PASS). Không có within → chỉ ghi reason (ví dụ "một dòng cấu hình").
  pseudo    mã giả tiếng Việt / ký hiệu toán. Nếu văn bản là Python hợp lệ có từ khoá lệnh → WARN (xét lại).
  output    khối là ĐẦU RA/nhật ký/thông báo lỗi. Nếu `of: <khoá khối run>` thì mỗi dòng khác rỗng (… = ký tự đại
            diện) phải là chuỗi con của một dòng đầu ra thật (stdout rồi stderr), đúng thứ tự.
  other     ngôn ngữ/định dạng không có trình kiểm (Dockerfile, cấu hình, giao thức…): bắt buộc `read_check` (đã đọc kiểm
            điều gì, theo nguồn nào); yaml/json được phân tích thật.
Trường thêm: claims [điều bài nói về kết quả khối — trích nguyên chữ]; unverified_claims [điều bài nói mà máy KHÔNG kiểm
được → cổng đếm và in ra với -v, là NOT_VERIFIED]; files {tên tệp: khoá khối/nguồn} (ghi văn bản đã ghim vào thư mục
chạy, ví dụ Chao.java cho lệnh `javac Chao.java`); hand: true (mục tay trong sổ sinh máy, gen-jva giữ lại).
NGUỒN: `sources: {tên: {lang, code, …như run}}` trong tệp sổ → khoá "src:<KHOÁ>:<tên>"; cổng chạy mọi nguồn. Nguồn dịch
một khối C sang Python để kiểm kết quả ghi `twin_of: <khoá khối C>` + reason (độ trung thực bản dịch = INFERRED).

Dùng:
  python -B audit/review/screen_code.py inventory [--course X]     # TSV mọi khối
  python -B audit/review/screen_code.py check [--course X] [-v]    # cổng; thoát 1 nếu FAIL/STALE/MISSING/ORPHAN
  python -B audit/review/screen_code.py stub --course X            # mục mẫu cho khối chưa vào sổ
  python -B audit/review/screen_code.py show "<khoá khối>"         # in văn bản khối (để đọc/so)
  python -B audit/review/screen_code.py gen-jva                    # sinh sổ JVA từ audit/jva lib.PROGRAMS
"""
import argparse, datetime, hashlib, json, os, pathlib, re, shutil, sqlite3, subprocess, sys, tempfile, textwrap
from html.parser import HTMLParser

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
REGDIR = pathlib.Path(os.environ["SC_REGDIR"]) if os.environ.get("SC_REGDIR") else ROOT / "audit" / "review" / "screen_code"   # SC_REGDIR: thử sổ nháp (audit/bnx/screen_try.py)
KINDS = {"run", "syntax", "fragment", "pseudo", "output", "other"}
NEED_REASON = {"fragment", "pseudo", "output", "other"}
RUN_LANGS = {"python", "sqlite", "java", "node", "bash", "go", "oracle", "mssql"}   # oracle/mssql: Docker, audit/bnx/dbrun.py (đợt LF1)
SYNTAX_LANGS = RUN_LANGS | {"c"}
CLAIM_KEYS = ("post", "expect_stdout", "expect_compile_error", "expect_stderr_contains", "expect_exception")
SYS_PY = shutil.which("python") or sys.executable   # python hệ thống có pycparser 3.00 (venv không có)


_BR = "\x00BR\x00"


class _Blocks(HTMLParser):
    """Ba kiểu nội dung, theo đúng cách trình duyệt hiển thị (tools/templates/player.css):
    - `<div>` con trực tiếp của khối `.code`: `white-space: pre` → giữ nguyên dòng, khoảng trắng;
    - `<pre>`: giữ nguyên, tách dòng theo "\\n";
    - nội dung khác trong khối (ví dụ `<div class="box code"><code>…<br/>…</code>`): `white-space: normal` → gộp mọi
      chuỗi khoảng trắng thường thành một dấu cách, chỉ xuống dòng ở `<br>`, bỏ dấu cách hai đầu dòng (&nbsp; giữ lại).
      (Lỗi cũ: chữ ngoài <div> dòng bị nối nguyên, sinh dòng trắng giả — nhóm 3 SC1 báo 2026-11-10.)"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.depth, self.cur, self.line, self.pre, self.loose = [], 0, None, None, False, []

    def _flush_loose(self):
        if self.loose:
            for l in "".join(self.loose).split(_BR):
                l = l.strip(" ")
                if l:
                    self.cur.append(l)
            self.loose = []

    def _br(self):
        if self.line is not None:
            self.line.append("\n")
        else:
            self.loose.append(_BR)

    def handle_starttag(self, tag, attrs):
        cls = (dict(attrs).get("class") or "").split()
        if self.cur is None:
            if tag in ("div", "pre") and ("code" in cls or tag == "pre"):
                self.cur, self.depth, self.pre, self.loose = [], 1, (tag == "pre"), []
                self.line = [] if self.pre else None
            return
        if tag == "br":
            self._br()
            return
        self.depth += 1
        if not self.pre and tag == "div" and self.depth == 2:
            self._flush_loose()
            self.line = []

    def handle_startendtag(self, tag, attrs):
        if self.cur is None:
            return
        if tag == "br":
            self._br()

    def handle_endtag(self, tag):
        if self.cur is None or tag == "br":
            return
        if not self.pre and tag == "div" and self.depth == 2 and self.line is not None:
            self.cur.append("".join(self.line))
            self.line = None
        self.depth -= 1
        if self.depth == 0:
            if self.pre:
                self.cur.extend("".join(self.line).split("\n"))
            else:
                self._flush_loose()
            self.blocks.append(self.cur)
            self.cur, self.line = None, None

    def handle_data(self, data):
        if self.cur is None:
            return
        if self.line is not None:
            self.line.append(data)
        else:
            self.loose.append(re.sub(r"[ \t\r\n\f]+", " ", data))


def norm(lines):
    return "\n".join(l.replace(" ", " ").rstrip() for l in lines).strip("\n")


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def iter_lessons(course=None):
    for f in sorted((ROOT / "lessons").glob("*/L*.yaml")):
        c = f.parent.name.upper()
        if course and c != course.upper():
            continue
        yield c, f


def blocks_of(path):
    spec = yaml.safe_load(open(path, encoding="utf-8"))
    out = []
    for si, sc in enumerate(spec.get("scenes") or []):
        sid = sc.get("id") or f"s{si}"
        for ti, st in enumerate(sc.get("steps") or []):
            show = st.get("show") if isinstance(st, dict) else None
            if not isinstance(show, str):
                continue
            p = _Blocks()
            p.feed(show)
            p.close()
            for bi, b in enumerate(p.blocks):
                out.append((sid, ti, bi, norm(b)))
    return spec, out


def all_blocks(course=None):
    """{khoá: văn bản} theo thứ tự bài."""
    d = {}
    for c, f in iter_lessons(course):
        for sid, ti, bi, t in blocks_of(f)[1]:
            d[f"{c} {f.name[:3]} {sid} {ti} {bi}"] = t
    return d


def load_reg(course=None):
    """Mục khối + NGUỒN: `sources: {tên: {code, lang, …như run}}` của tệp <KHOÁ>.yaml thành khoá "src:<KHOÁ>:<tên>"
    (chương trình đầy đủ mà màn hình chỉ hiện từng đoạn; cổng chạy nó như một khối run)."""
    reg = {}
    for f in sorted(REGDIR.glob("*.yaml")):
        if course and f.stem.upper() != course.upper():
            continue
        d = yaml.safe_load(open(f, encoding="utf-8")) or {}
        items = list((d.get("blocks") or {}).items())
        items += [(f"src:{f.stem.upper()}:{n}", dict(v, _source=True)) for n, v in (d.get("sources") or {}).items()]
        for k, v in items:
            if k in reg:
                raise SystemExit(f"khoá trùng trong sổ: {k} ({f.name})")
            reg[k] = v
    return reg


# ───────────────────────── chạy ─────────────────────────
def _run(cmd, inp=None, cwd=None, timeout=60):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    r = subprocess.run(cmd, input=inp, cwd=cwd, capture_output=True, timeout=timeout, env=env,
                       text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout, r.stderr


def _py_exe():
    v = ROOT / ".venv" / "Scripts" / "python.exe"
    return str(v) if v.exists() else sys.executable


def _sql_split(s):
    out, buf = [], ""
    for line in s.split("\n"):
        buf += line + "\n"
        if sqlite3.complete_statement(buf):
            if buf.strip():
                out.append(buf.strip())
            buf = ""
    if buf.strip():
        out.append(buf.strip())
    return out


def _strip_c_comments(src):
    """Bỏ chú thích // và /* */ (thay bằng dấu cách, giữ số dòng), không đụng chuỗi "…" và ký tự '…'.
    pycparser cần mã đã qua bộ tiền xử lý, nên không nhận chú thích (nhóm 3 SC1 báo 2026-11-10)."""
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c in "\"'":
            j = i + 1
            while j < n and src[j] != c and src[j] != "\n":
                j += 2 if src[j] == "\\" else 1
            out.append(src[i:j + 1])
            i = j + 1
        elif src.startswith("//", i):
            j = src.find("\n", i)
            j = n if j < 0 else j
            out.append(" ")
            i = j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append(" " + "\n" * src.count("\n", i, j))
            i = j
        else:
            out.append(c)
            i += 1
    return "".join(out)


def _dedent_lines(t):
    return [l.rstrip() for l in textwrap.dedent(t).strip("\n").split("\n")]


_JAVAC_PREFIX = re.compile(r"^\S+\.java:\d+:\s*")


def _line_match(want, line):
    """Dòng màn hình khớp CẢ DÒNG đầu ra thật (bỏ khoảng trắng hai đầu). "…" trên màn hình = đoạn bị lược (khớp mọi
    chuỗi). Được bỏ tiền tố vị trí `Tệp.java:N:` mà javac in trước "error:". (Bản trước so chuỗi con: màn hình "5"
    khớp nhầm máy in "50000" — kiểm độc lập SC1 phần A phát hiện.)"""
    want, line = want.strip(), line.strip()
    rx = re.compile("^" + ".*".join(re.escape(p) for p in want.split("…")) + "$", re.S)
    return bool(rx.match(line) or rx.match(_JAVAC_PREFIX.sub("", line)))


class Gate:
    def __init__(self, blocks, reg):
        self.blocks, self.reg, self.cache = blocks, reg, {}

    def text(self, k):
        if k.startswith("src:"):
            e = self.reg.get(k)
            if e is None:
                raise KeyError(f"nguồn không có trong sổ: {k}")
            return str(e["code"]).strip("\n")
        if k not in self.blocks:
            raise KeyError(f"khối tham chiếu không tồn tại: {k}")
        e = self.reg.get(k)
        if e is None or e.get("sha") != digest(self.blocks[k]):
            raise KeyError(f"khối tham chiếu chưa vào sổ hoặc STALE: {k}")
        return self.blocks[k]

    def prelude(self, e):
        parts = [self.text(k) for k in e.get("prelude_keys") or []]
        if e.get("prelude"):
            if not (e.get("prelude_reason") or "").strip():
                raise ValueError("prelude thiếu prelude_reason")
            parts.append(e["prelude"])
        return "\n".join(parts)

    def check(self, k):
        if k in self.cache:
            return self.cache[k]
        self.cache[k] = (False, "vòng tham chiếu", "", "")
        try:
            r = self._check(k)
        except subprocess.TimeoutExpired:
            r = (False, "quá thời gian", "", "")
        except (KeyError, ValueError) as ex:
            r = (False, str(ex), "", "")
        self.cache[k] = r
        return r

    def _check(self, k):
        e = self.reg[k]
        text = self.text(k) if k.startswith("src:") else self.blocks[k]
        if e.get("_source"):
            e = dict(e, kind=e.get("kind", "run"))
        kind, lang = e.get("kind"), e.get("lang")
        if kind not in KINDS:
            return False, f"kind lạ {kind!r}", "", ""
        if kind in NEED_REASON and not (e.get("reason") or "").strip():
            return False, f"kind {kind} thiếu reason", "", ""
        if kind == "pseudo":
            try:
                compile(text, "<khối>", "exec")
                if re.search(r"^\s*(def|class|import|for|while|if|return|print)\b", text, re.M):
                    return True, "CẢNH BÁO: khai pseudo nhưng là Python hợp lệ — xét lại 'run'", "", ""
            except SyntaxError:
                pass
            return True, "pseudo", "", ""
        if kind == "fragment":
            w = e.get("within")
            if not w:
                return True, "fragment (không within)", "", ""
            ok, msg, _, _ = self.check(w)
            if not ok:
                return False, f"within {w} không PASS: {msg}", "", ""
            frag, host = _dedent_lines(text), [l.rstrip() for l in self.text(w).split("\n")]
            hd = None
            for i in range(len(host) - len(frag) + 1):
                if _dedent_lines("\n".join(host[i:i + len(frag)])) == frag:
                    hd = i
                    break
            if hd is None:
                return False, f"không phải dãy dòng liên tiếp của {w}", "", ""
            return True, f"dòng {hd + 1}–{hd + len(frag)} của {w}", "", ""
        if kind == "output":
            of = e.get("of")
            if not of:
                return True, "output (không of)", "", ""
            ok, msg, so, se = self.check(of)
            if not ok:
                return False, f"of {of} không PASS: {msg}", "", ""
            actual = [l.rstrip() for l in (so + "\n" + se).replace("\r\n", "\n").split("\n")]
            if e.get("field") is not None:
                # màn hình chỉ hiện MỘT cột của kết quả sqlite (cột ngăn bằng "|"), ví dụ cột chi tiết của
                # EXPLAIN QUERY PLAN như sqlite3 CLI in; vẫn so cả ô, đúng thứ tự
                fi = int(e["field"])
                actual = [l.split("|")[fi] if l else l for l in actual]
            pos = 0
            for want in [l.strip() for l in text.split("\n") if l.strip()]:
                while pos < len(actual) and not _line_match(want, actual[pos]):
                    pos += 1
                if pos == len(actual):
                    return False, f"dòng đầu ra {want[:80]!r} không có trong kết quả chạy thật của {of}", "", ""
                pos += 1
            return True, f"khớp đầu ra thật của {of}", "", ""
        if kind == "other":
            if not (e.get("read_check") or "").strip():
                return False, "other thiếu read_check (đã đọc kiểm điều gì, theo nguồn nào)", "", ""
            if lang == "yaml":
                try:
                    yaml.safe_load(text)
                except yaml.YAMLError as ex:
                    return False, f"yaml lỗi: {str(ex).splitlines()[0]}", "", ""
            if lang == "json":
                try:
                    json.loads(text)
                except ValueError as ex:
                    return False, f"json lỗi: {ex}", "", ""
            return True, f"other/{lang}", "", ""
        # run | syntax
        if kind == "run" and lang not in RUN_LANGS:
            return False, f"run không hỗ trợ lang {lang!r}", "", ""
        if kind == "syntax" and lang not in SYNTAX_LANGS:
            return False, f"syntax không hỗ trợ lang {lang!r}", "", ""
        if kind == "run" and not any(x in e for x in CLAIM_KEYS) and not (e.get("no_claim_reason") or "").strip():
            return False, "run thiếu khẳng định (post/expect_*) và không có no_claim_reason", "", ""
        pre, post = self.prelude(e), e.get("post") or ""
        src = "\n".join(x for x in (pre, text, post) if x)
        to = e.get("timeout", 60)
        with tempfile.TemporaryDirectory() as d:
            dp = pathlib.Path(d)
            # files: {tên tệp: khoá khối/nguồn} — ghi văn bản ĐÃ GHIM của khối/nguồn đó vào thư mục chạy (ví dụ lệnh
            # `javac Chao.java` cần tệp Chao.java đúng bằng mã đã hiện)
            for fname, ref in (e.get("files") or {}).items():
                if "/" in fname or "\\" in fname or fname.startswith("."):
                    raise ValueError(f"tên tệp không hợp lệ: {fname}")
                (dp / fname).write_text(self.text(ref) + "\n", encoding="utf-8", newline="\n")
            if lang == "python":
                try:
                    compile(text, "<khối>", "exec")
                except SyntaxError as ex:
                    return False, f"python cú pháp (nguyên văn): {ex.msg} dòng {ex.lineno}", "", ""
                if kind == "syntax":
                    return True, "python compile", "", ""
                (dp / "khoi.py").write_text(src + "\n", encoding="utf-8")
                # -I bỏ qua PYTHONIOENCODING → in tiếng Việt lỗi UnicodeEncodeError trên cp1252; -X utf8 sửa (nhóm 1 báo)
                return self._judge(*_run([_py_exe(), "-I", "-X", "utf8", "-B", "khoi.py"], cwd=d, timeout=to), e)
            if lang == "sqlite":
                con = sqlite3.connect(":memory:")
                try:
                    if pre:
                        con.executescript(pre)
                    if kind == "syntax":
                        for s in _sql_split(text):
                            con.execute("EXPLAIN " + s)
                        return True, "sqlite EXPLAIN", "", ""
                    rows = []
                    for s in _sql_split(text) + _sql_split(post):
                        cur = con.execute(s)
                        if cur.description:
                            rows += ["|".join("NULL" if v is None else str(v) for v in r) for r in cur.fetchall()]
                    con.commit()
                except sqlite3.Error as ex:
                    return self._judge(1, "", f"sqlite3.{type(ex).__name__}: {ex}", e)
                return self._judge(0, "\n".join(rows) + ("\n" if rows else ""), "", e)
            if lang == "java":
                cls = e.get("java_class") or "Main"
                jsrc = e["java_wrap"].replace("{CODE}", src) if e.get("java_wrap") else src
                (dp / f"{cls}.java").write_text(jsrc + "\n", encoding="utf-8")
                rc, so, se = _run(["javac", "-encoding", "UTF-8", "-d", d, f"{cls}.java"], cwd=d)
                if "expect_compile_error" in e:
                    w = e["expect_compile_error"]
                    good = rc != 0 and w in (so + se)
                    return (good, f"javac báo lỗi chứa {w!r}" if good else f"javac rc={rc}, không thấy {w!r}: {se[:160]!r}",
                            so, se)
                if rc:
                    return False, "javac: " + (se.strip().splitlines() or ["?"])[0][:200], so, se
                if kind == "syntax":
                    return True, "javac", "", ""
                rc, so, se = _run(["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", "-cp", d, cls],
                                  cwd=d, timeout=to)
                return self._judge(rc, so, se, e)
            if lang == "node":
                (dp / "khoi.js").write_text(src + "\n", encoding="utf-8")
                if kind == "syntax":
                    (dp / "nguyen.js").write_text(text + "\n", encoding="utf-8")
                    rc, so, se = _run(["node", "--check", "nguyen.js"], cwd=d)
                    return (rc == 0), ("node --check" if rc == 0 else se.strip()[:200]), "", ""
                return self._judge(*_run(["node", "khoi.js"], cwd=d, timeout=to), e)
            if lang == "bash":
                (dp / "khoi.sh").write_text(src + "\n", encoding="utf-8", newline="\n")
                if kind == "syntax":
                    rc, so, se = _run([shutil.which("bash"), "-n", "khoi.sh"], cwd=d)
                    return (rc == 0), ("bash -n" if rc == 0 else se.strip()[:200]), "", ""
                return self._judge(*_run([shutil.which("bash"), "khoi.sh"], cwd=d, timeout=to), e)
            if lang in ("oracle", "mssql"):
                # Chạy NGUYÊN VĂN trên Oracle AI Database 26ai Free / SQL Server 2022 trong Docker (audit/bnx/dbrun.py).
                # Không có container → FAIL "NOT_VERIFIED" (không bao giờ PASS lặng lẽ).
                sys.path.insert(0, str(ROOT / "audit" / "bnx"))
                import dbrun
                try:
                    ok_o, ok_m = dbrun.ready()
                except Exception as ex:
                    return False, f"NOT_VERIFIED: không gọi được Docker ({type(ex).__name__})", "", ""
                if not (ok_o if lang == "oracle" else ok_m):
                    return False, f"NOT_VERIFIED: container {lang} chưa chạy (docker start bnx-ora bnx-mss)", "", ""
                if kind == "syntax":
                    return False, f"{lang}: chỉ hỗ trợ kind run", "", ""
                out = dbrun.ora(src) if lang == "oracle" else dbrun.mss(src, db=e.get("db"))
                err = "\n".join(ln for ln in out.splitlines() if re.match(r"\s*(ORA-|PLS-|SP2-|Msg \d+)", ln))
                if err and not e.get("expect_stderr_contains") and not e.get("allow_errors"):
                    return False, f"{lang} báo lỗi: {err.splitlines()[0][:200]}", out, err
                return self._judge(0, out, err, e)
            if lang == "go":
                gsrc = e["go_wrap"].replace("{CODE}", src) if e.get("go_wrap") else src
                (dp / "main.go").write_text(gsrc + "\n", encoding="utf-8")
                if kind == "syntax":
                    rc, so, se = _run(["gofmt", "-e", "main.go"], cwd=d)
                    return (rc == 0), ("gofmt -e" if rc == 0 else se.strip()[:200]), "", ""
                return self._judge(*_run(["go", "run", "main.go"], cwd=d, timeout=to), e)
            if lang == "c":
                csrc = e["c_wrap"].replace("{CODE}", text) if e.get("c_wrap") else text
                csrc = (e.get("c_typedefs") or "") + "\n" + _strip_c_comments(csrc)
                (dp / "khoi.c").write_text(csrc + "\n", encoding="utf-8")
                prog = ("import sys\nfrom pycparser import c_parser\n"
                        "c_parser.CParser().parse(open(sys.argv[1], encoding='utf-8').read(), filename='khoi.c')\n")
                (dp / "p.py").write_text(prog, encoding="utf-8")
                # KHÔNG dùng -I: pycparser nằm ở user site-packages của python hệ thống, -I tắt user site (lỗi thật,
                # bắt được bằng ca dương của negative_controls 2026-11-10). Thư mục chạy chỉ có p.py và khoi.c.
                rc, so, se = _run([SYS_PY, "-B", "p.py", "khoi.c"], cwd=d)
                if rc and "No module named" in se:
                    return False, "NOT_VERIFIED: thiếu pycparser", "", ""
                return (rc == 0), ("pycparser C99" if rc == 0 else se.strip().splitlines()[-1][:200]), "", ""
        return False, f"không có trình kiểm cho {kind}/{lang}", "", ""

    @staticmethod
    def _judge(rc, so, se, e):
        so, se = so.replace("\r\n", "\n"), se.replace("\r\n", "\n")
        if "expect_exception" in e:
            good = rc != 0 and e["expect_exception"] in se
            if not good:
                return False, f"cần ngoại lệ {e['expect_exception']!r}, rc={rc}: {se.strip()[-200:]!r}", so, se
        else:
            want_rc = e.get("expect_rc", 0)
            if rc != want_rc:
                return False, f"mã thoát {rc} (cần {want_rc}): {(se or so).strip()[-240:]}", so, se
        if "expect_stdout" in e:
            want = "\n".join(l.rstrip() for l in str(e["expect_stdout"]).split("\n")).strip("\n")
            got = "\n".join(l.rstrip() for l in so.split("\n")).strip("\n")
            if got != want:
                return False, f"stdout lệch: được {got[:200]!r} — cần {want[:200]!r}", so, se
        if "expect_stderr_contains" in e:
            want = str(e["expect_stderr_contains"])
            if "…" in want or "\n" in want.strip("\n"):
                # dòng thông báo trên màn hình (có thể lược bằng "…", nhiều dòng): mỗi dòng khớp CẢ MỘT dòng stderr, đúng thứ tự
                lines, pos = se.split("\n"), 0
                for wl in [x for x in want.split("\n") if x.strip()]:
                    while pos < len(lines) and not _line_match(wl, lines[pos]):
                        pos += 1
                    if pos == len(lines):
                        return False, f"stderr không có dòng khớp {wl.strip()[:120]!r}: {se.strip()[-200:]!r}", so, se
                    pos += 1
            elif want not in se:
                return False, f"stderr thiếu {want!r}: {se.strip()[-200:]!r}", so, se
        return True, f"chạy rc={rc}" + (" stdout khớp" if "expect_stdout" in e else "") + \
            (" post qua" if e.get("post") else ""), so, se


# ───────────────────────── lệnh ─────────────────────────
def cmd_inventory(a):
    print("khoá\tbài\tcảnh\tstep\tkhối\tsố_dòng\tsha16\tdòng_đầu")
    bl = all_blocks(a.course)
    for k, t in bl.items():
        c, lid, sid, ti, bi = k.split(" ")
        first = t.splitlines()[0] if t else ""
        print(f"{c}\t{lid}\t{sid}\t{ti}\t{bi}\t{len(t.splitlines())}\t{digest(t)}\t{first[:80]}")
    print(f"# {len(bl)} khối", file=sys.stderr)


def cmd_show(a):
    bl = all_blocks(a.key.split()[0])
    t = bl.get(a.key)
    if t is None:
        print("không có khối", a.key)
        return 1
    print(f"# sha {digest(t)}\n{t}")


def cmd_stub(a):
    reg = load_reg()
    for k, t in all_blocks(a.course).items():
        if k in reg:
            continue
        first = t.splitlines()[0][:90] if t else ""
        print(f"  {json.dumps(k, ensure_ascii=False)}:\n    sha: {digest(t)}\n    kind: TODO\n    # {first}")


def cmd_check(a):
    blocks, reg = all_blocks(a.course), load_reg(a.course)
    g = Gate(all_blocks() if a.course else blocks, load_reg() if a.course else reg)
    res = dict(PASS=0, FAIL=0, STALE=0, MISSING=0)
    warn, lines, kinds = 0, [], {}
    for k, t in blocks.items():
        e = reg.get(k)
        if e is None:
            res["MISSING"] += 1
            lines.append(f"MISSING {k} sha={digest(t)} | {(t.splitlines() or [''])[0][:80]}")
            continue
        if e.get("sha") != digest(t):
            res["STALE"] += 1
            lines.append(f"STALE   {k} sổ={e.get('sha')} thật={digest(t)}")
            continue
        ok, msg, _, _ = g.check(k)
        kk = f"{e.get('kind')}/{e.get('lang') or '-'}"
        kinds[kk] = kinds.get(kk, 0) + 1
        if ok:
            res["PASS"] += 1
            if msg.startswith("CẢNH BÁO"):
                warn += 1
                lines.append(f"WARN    {k} {msg}")
            elif a.verbose:
                lines.append(f"PASS    {k} [{kk}] {msg}")
        else:
            res["FAIL"] += 1
            lines.append(f"FAIL    {k} [{kk}] {msg}")
    for k in [k for k in reg if k.startswith("src:")]:
        ok, msg, _, _ = g.check(k)
        tw = reg[k].get("twin_of")
        if tw is not None:   # bản dịch đối chiếu phải trỏ tới một khối có thật, đã vào sổ (nhóm 4 SC1 đề xuất)
            tws = tw if isinstance(tw, list) else [tw]
            bad_tw = [t for t in tws if t not in g.blocks or t not in g.reg]
            if bad_tw:
                ok, msg = False, f"twin_of trỏ tới khối không có/không vào sổ: {bad_tw}"
            elif not (reg[k].get("reason") or "").strip():
                ok, msg = False, "nguồn twin_of thiếu reason"
        res["PASS" if ok else "FAIL"] += 1
        if not ok or a.verbose:
            lines.append(f"{'PASS' if ok else 'FAIL'}    {k} [nguồn/{reg[k].get('lang')}] {msg}")
    orphan = [k for k in reg if k not in blocks and not k.startswith("src:")]
    lines += [f"ORPHAN  {k} (mục sổ không còn khối)" for k in orphan]
    print("\n".join(lines))
    print("loại:", ", ".join(f"{k} {v}" for k, v in sorted(kinds.items(), key=lambda x: -x[1])))
    # điều bài nói mà máy KHÔNG kiểm được (NOT_VERIFIED) — liệt kê để không ai hiểu nhầm là đã kiểm
    unv = [(k, c) for k, e in reg.items() if k in blocks or k.startswith("src:") for c in (e.get("unverified_claims") or [])]
    print(f"unverified_claims (NOT_VERIFIED bằng máy): {len(unv)}")
    if a.verbose:
        for k, c in unv:
            print(f"  NOT_VERIFIED {k}: {c}")
    print(f"screen_code: {len(blocks)} khối — PASS {res['PASS']} · FAIL {res['FAIL']} · STALE {res['STALE']} · "
          f"MISSING {res['MISSING']} · ORPHAN {len(orphan)} · WARN {warn}")
    print("checked_at=" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    return 1 if (res["FAIL"] or res["STALE"] or res["MISSING"] or orphan) else 0


def cmd_gen_jva(a):
    """Sổ JVA từ lib.PROGRAMS (audit/jva/src): mỗi chương trình → một NGUỒN run/java (so đầu ra, lỗi biên dịch, ngoại lệ
    như verify_jva); khối mã trên màn hình → fragment `within` nguồn có chứa nó (dãy dòng liên tiếp, bỏ thụt lề chung);
    khối kết quả → output `of` nguồn. Khối không khớp gì → in "CHƯA KHỚP", không ghi (thêm tay với `hand: true`)."""
    sys.path[:0] = [str(ROOT / "audit" / "jva"), str(ROOT / "audit" / "jva" / "src")]
    import importlib
    import lib  # noqa
    for p in sorted((ROOT / "audit/jva/src").glob("l*.py")):
        lib.begin(p.stem.upper())
        importlib.import_module(p.stem).build()
    sources, by_lesson, seen = {}, {}, {}
    for pr in lib.PROGRAMS:
        key = (pr["lesson"], pr["code"], pr["expect"], pr["out"], pr["err"])
        if key in seen:
            continue
        n = f"{pr['lesson']}_{pr['name']}"
        i = 2
        while n in sources:
            n, i = f"{pr['lesson']}_{pr['name']}_{i}", i + 1
        seen[key] = n
        e = {"lang": "java", "java_class": pr["name"]}
        ex = pr["expect"]
        if ex.startswith("compile_error:"):
            e["expect_compile_error"] = ex.split(":", 1)[1]
        elif ex.startswith("runtime_error:"):
            e["expect_exception"] = ex.split(":", 1)[1]
            e["expect_stdout"] = pr["out"]
            if pr["err"]:
                e["expect_stderr_contains"] = pr["err"]
        else:
            e["expect_stdout"] = pr["out"]
        e["code"] = pr["code"]
        sources[n] = e
        by_lesson.setdefault(pr["lesson"], []).append((n, pr))
    blocks = all_blocks("JVA")
    reg, unmatched = {}, []
    for k, t in blocks.items():
        lid, frag, hit = k.split()[1], _dedent_lines(t), None
        tl = [l.rstrip() for l in t.split("\n")]
        for n, pr in by_lesson.get(lid, []):
            hl = pr["code"].split("\n")
            if any(_dedent_lines("\n".join(hl[i:i + len(frag)])) == frag for i in range(len(hl) - len(frag) + 1)):
                hit = {"sha": digest(t), "kind": "fragment", "within": f"src:JVA:{n}",
                       "reason": f"dãy dòng của chương trình {pr['name']} (nguồn chạy thật)"}
                break
        if hit is None:
            # ưu tiên chương trình có đoạn mã hiện ở CÙNG bước (khối kết quả đứng ngay sau đoạn mã của nó)
            same = {v["within"] for kk, v in reg.items() if kk.rsplit(" ", 1)[0] == k.rsplit(" ", 1)[0]
                    and v.get("kind") == "fragment"}
            cands = sorted(by_lesson.get(lid, []), key=lambda x: f"src:JVA:{x[0]}" not in same)
            for n, pr in cands:
                outs = [l.rstrip() for l in pr["out"].split("\n")] if pr["out"] else []
                ex = pr["expect"]
                extra = tl[len(outs):]
                # dòng thêm sau phần in ra: dòng báo lỗi biên dịch, hoặc ngoại lệ + dấu vết ngăn xếp; cổng `output`
                # đối chiếu TỪNG dòng với đầu ra thật (stdout rồi stderr), nên ở đây chỉ cần nhận dạng loại khối
                ok_extra = (not extra and not ex.startswith(("compile_error:", "runtime_error:"))) or bool(extra) and (
                    (ex.startswith("compile_error:") and extra[0].startswith("error:")
                     and any(ex.split(":", 1)[1] in x for x in extra)) or
                    (ex.startswith("runtime_error:") and ex.split(":", 1)[1] in extra[0]))
                if outs == tl[:len(outs)] and ok_extra and (outs or extra):
                    hit = {"sha": digest(t), "kind": "output", "of": f"src:JVA:{n}",
                           "reason": f"khối kết quả của chương trình {pr['name']}"}
                    break
        if hit:
            reg[k] = hit
        else:
            unmatched.append(k)
    REGDIR.mkdir(parents=True, exist_ok=True)
    out = REGDIR / "JVA.yaml"
    if out.exists():
        d = yaml.safe_load(open(out, encoding="utf-8")) or {}
        for k, v in (d.get("blocks") or {}).items():
            if v.get("hand") and k in unmatched:
                reg[k] = v
                unmatched.remove(k)
    hdr = ("# Sổ mã trên màn hình khoá JVA — SINH bằng `screen_code.py gen-jva` từ audit/jva/src (lib.PROGRAMS).\n"
           "# Mục `hand: true` (khối không khớp chương trình nào) được giữ qua các lần sinh lại.\n")
    out.write_text(hdr + yaml.safe_dump({"blocks": reg, "sources": sources}, allow_unicode=True, sort_keys=False,
                                        width=200), encoding="utf-8", newline="\n")
    print(f"gen-jva: {len(blocks)} khối, ghi {len(reg)}, nguồn {len(sources)}, chưa khớp {len(unmatched)}")
    for k in unmatched:
        print("  CHƯA KHỚP", k, "|", (blocks[k].splitlines() or [""])[0][:90])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["inventory", "check", "stub", "show", "gen-jva"])
    ap.add_argument("key", nargs="?")
    ap.add_argument("--course")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    f = {"inventory": cmd_inventory, "check": cmd_check, "stub": cmd_stub, "show": cmd_show,
         "gen-jva": cmd_gen_jva}[a.cmd]
    return f(a) or 0


if __name__ == "__main__":
    sys.exit(main())
