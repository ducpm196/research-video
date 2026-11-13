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
PHIÊN DÒNG LỆNH (FND, JV2): nguồn có `session: [{cmd, out}, …]` (+ `fs: {đường dẫn: nội dung}` tệp dựng sẵn, `profile: fnd|jv2`,
            `env`, `deps`) là MỘT phiên Git Bash chạy THẬT (fnd: audit/fnd/runner.py; jv2: thư mục tạm + jar audit/jv2/deps), mỗi
            bước so đầu ra (stdout+stderr gộp). Văn bản nguồn = phiên vẽ như màn hình (`$ lệnh`, `> ` dòng nối, rồi đầu ra), nên khối
            terminal là `fragment within` nguồn (dãy dòng liên tiếp); `cmds_only: true` = khối chỉ hiện dòng lệnh (ẩn đầu ra): các dòng
            phải là dãy liên tiếp của RIÊNG các dòng lệnh. `within: "src:<KHOÁ>:<tên>#<đường dẫn>"` = khối là nội dung (một đoạn) tệp
            dựng sẵn `fs` của phiên đó (tệp mà phiên đã chạy/đọc). Java `args`/`stdin`/`java_release` cho nguồn chạy chương trình.
NGUỒN: `sources: {tên: {lang, code, …như run}}` trong tệp sổ → khoá "src:<KHOÁ>:<tên>"; cổng chạy mọi nguồn. Nguồn dịch
một khối C sang Python để kiểm kết quả ghi `twin_of: <khoá khối C>` + reason (độ trung thực bản dịch = INFERRED).

Dùng:
  python -B audit/review/screen_code.py inventory [--course X]     # TSV mọi khối
  python -B audit/review/screen_code.py check [--course X] [-v]    # cổng; thoát 1 nếu FAIL/STALE/MISSING/ORPHAN
  python -B audit/review/screen_code.py stub --course X            # mục mẫu cho khối chưa vào sổ
  python -B audit/review/screen_code.py show "<khoá khối>"         # in văn bản khối (để đọc/so)
  python -B audit/review/screen_code.py gen-jva                    # sinh sổ JVA từ audit/jva lib.PROGRAMS
  python -B audit/review/screen_code.py gen-fnd | gen-jv2          # sinh sổ FND (lib.CMDS) / JV2 (lib.PROGRAMS + lib.PROJECTS)
  python -B audit/review/screen_code.py gen-prog --course JVA|FND|JV2   # như trên, chọn khoá bằng --course
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
def _run(cmd, inp=None, cwd=None, timeout=60, path_prepend=None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    if path_prepend:
        env["PATH"] = str(path_prepend) + os.pathsep + env.get("PATH", "")
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


def render_session(session, outputs=True):
    """Phiên [{cmd, out}] vẽ như khung cửa sổ lệnh trên màn hình (audit/fnd/lib.term_block, audit/jv2/lib.term_block):
    dòng đầu của lệnh `$ …`, dòng nối `> …`, rồi các dòng đầu ra (dòng trống = ""). outputs=False: chỉ dòng lệnh."""
    lines = []
    for s in session:
        for i, l in enumerate(str(s["cmd"]).split("\n")):
            lines.append(("$ " if i == 0 else "> ") + l)
        if outputs and str(s.get("out") or ""):
            lines += str(s["out"]).split("\n")
    return "\n".join(l.rstrip() for l in lines)


def _norm_out(s):
    return "\n".join(l.rstrip() for l in s.replace("\r\n", "\n").replace("\r", "\n").strip("\n").split("\n"))


_FND_RUNNER = []


def _fnd_runner():
    """audit/fnd/runner.py nạp theo đường dẫn (tên module riêng, tránh đụng `runner` khác)."""
    if not _FND_RUNNER:
        import importlib.util
        spec = importlib.util.spec_from_file_location("fnd_runner_for_screen_code", ROOT / "audit" / "fnd" / "runner.py")
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _FND_RUNNER.append(m)
    return _FND_RUNNER[0]


def _posix(p):
    p = str(p).replace("\\", "/")
    return "/" + p[0].lower() + p[2:] if len(p) > 1 and p[1] == ":" else p


def _session_outputs(e):
    """Chạy THẬT một phiên dòng lệnh; trả (danh sách đầu ra từng bước hoặc None, lỗi). profile fnd = audit/fnd/runner.run_session
    (thư mục tạm = C:/Users/ban, Git cấu hình riêng); profile jv2 = thư mục tạm sạch + jar audit/jv2/deps vào lib/ (như verify_jv2)."""
    steps, fs = e["session"], {k: str(v) for k, v in (e.get("fs") or {}).items()}
    prof = e.get("profile") or "fnd"
    if prof == "fnd":
        got, err, R = _fnd_runner().run_session(fs, [s["cmd"] for s in steps])
        shutil.rmtree(R, ignore_errors=True)
        if got is None:
            return None, err
        return [got.get(i, "<<không có đầu ra>>") for i in range(len(steps))], ""
    if prof != "jv2":
        return None, f"profile lạ {prof!r}"
    deps = ROOT / "audit" / "jv2" / "deps"
    uses = e.get("deps") or any("{DEPS}" in s["cmd"] for s in steps)
    if uses and not any(deps.glob("*.jar")):
        return None, "NOT_VERIFIED: thiếu jar trong audit/jv2/deps"
    R = pathlib.Path(os.path.realpath(tempfile.mkdtemp(prefix="sc_jv2_")))
    try:
        W = R / "w"
        W.mkdir()
        for rel, content in fs.items():
            f = W / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(content.encode("utf-8"))
        if uses:
            (W / "lib").mkdir(exist_ok=True)
            for j in deps.glob("*.jar"):
                shutil.copy(j, W / "lib" / j.name)
        body = ["__rc=0"]
        for i, s in enumerate(steps):
            body.append(f"__rc=$?; printf '\\001@@STEP {i}\\n'; (exit $__rc)")
            body.append(s["cmd"].replace("{DEPS}", _posix(deps)))
        (R / "run.sh").write_text("\n".join(body) + "\n", encoding="utf-8", newline="\n")
        (R / "wrap.sh").write_text(f'exec 2>&1\ncd "{_posix(W)}"\nsource "{_posix(R / "run.sh")}"\n', encoding="utf-8", newline="\n")
        env = dict(os.environ, LC_ALL="C.UTF-8", MSYS_NO_PATHCONV="1")
        env.update({str(k): str(v) for k, v in (e.get("env") or {}).items()})
        bash = r"C:\Program Files\Git\bin\bash.exe"
        if not pathlib.Path(bash).exists():
            bash = shutil.which("bash") or "bash"
        try:
            r = subprocess.run([bash, str(R / "wrap.sh")], cwd=str(W), env=env, capture_output=True, timeout=300,
                               stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return None, "quá thời gian (300 s)"
        raw = r.stdout.decode("utf-8", errors="replace").replace(chr(92), "/")   # javac Windows in gạch ngược; màn hình hiện gạch xuôi
        raw = raw.replace("Picked up JAVA_TOOL_OPTIONS: -Dstdout.encoding=UTF-8 -Dstderr.encoding=UTF-8\n", "")
        got = {}
        for seg in raw.split("\x01@@STEP ")[1:]:
            n, _, rest = seg.partition("\n")
            got[int(n)] = rest
        return [got.get(i, "<<không có đầu ra>>") for i in range(len(steps))], ""
    finally:
        shutil.rmtree(R, ignore_errors=True)


class Gate:
    def __init__(self, blocks, reg):
        self.blocks, self.reg, self.cache = blocks, reg, {}

    def text(self, k):
        if k.startswith("src:"):
            base, _, fpath = k.partition("#")
            e = self.reg.get(base)
            if e is None:
                raise KeyError(f"nguồn không có trong sổ: {base}")
            if fpath:   # tệp dựng sẵn của phiên: `src:<KHOÁ>:<tên>#<đường dẫn>`
                fs = e.get("fs") or {}
                if fpath not in fs:
                    raise KeyError(f"tệp {fpath!r} không có trong fs của {base}")
                return str(fs[fpath]).strip("\n")
            if e.get("session") is not None:
                return render_session(e["session"])
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
        if k.startswith("src:") and "#" in k:   # tệp dựng sẵn của một phiên: PASS khi phiên PASS và tệp có thật
            base = k.partition("#")[0]
            ok, msg, so, se = self.check(base)
            try:
                self.text(k)
            except KeyError as ex:
                ok, msg = False, str(ex)
            self.cache[k] = (ok, msg, so, se)
            return self.cache[k]
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
            if e.get("cmds_only"):   # khối chỉ hiện dòng lệnh của phiên (đầu ra bị ẩn): so với RIÊNG các dòng lệnh
                hs = (self.reg.get(w.partition("#")[0]) or {}).get("session")
                if hs is None or "#" in w:
                    return False, f"cmds_only cần `within` là nguồn có session: {w}", "", ""
                host = render_session(hs, outputs=False).split("\n")
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
        if e.get("session") is not None:
            # PHIÊN DÒNG LỆNH: chạy thật từng bước, đầu ra mỗi bước phải khớp `out` (đã là khẳng định của bài)
            if kind != "run" or lang != "bash":
                return False, "session chỉ dùng với kind run, lang bash", "", ""
            # retries: CHỈ cho phiên có bước không tất định (đã nêu trong unverified_claims của nguồn): thử lại tới `retries` lần,
            # PASS khi một lần chạy khớp trọn; vẫn lệch cả `retries` lần → FAIL (mặc định 1 lần, không thử lại)
            tries = max(1, int(e.get("retries") or 1))
            for att in range(1, tries + 1):
                outs, err = _session_outputs(e)
                if outs is None:
                    return False, err, "", ""
                bad = [f"bước {i} `{s['cmd'].splitlines()[0][:50]}`: màn hình {_norm_out(str(s.get('out') or ''))[:160]!r}; "
                       f"máy chạy {_norm_out(o)[:160]!r}"
                       for i, (s, o) in enumerate(zip(e["session"], outs)) if _norm_out(o) != _norm_out(str(s.get("out") or ""))]
                if not bad:
                    break
            if bad:
                return False, (f"[{tries} lần thử] " if tries > 1 else "") + " | ".join(bad[:2]), "\n".join(outs), ""
            return True, f"phiên {len(outs)} bước khớp" + (f" (lần thử {att}/{tries})" if tries > 1 else ""), "\n".join(outs), ""
        if kind == "run" and not any(x in e for x in CLAIM_KEYS) and not (e.get("no_claim_reason") or "").strip():
            return False, "run thiếu khẳng định (post/expect_*) và không có no_claim_reason", "", ""
        pre, post = self.prelude(e), e.get("post") or ""
        src = "\n".join(x for x in (pre, text, post) if x)
        to = e.get("timeout", 60)
        # ignore_cleanup_errors: lời giải lab FND L07 chạy máy chủ nền rồi `kill`; trên Windows tiến trình python con còn giữ thư mục
        # thêm một lúc → xoá thư mục tạm lỗi PermissionError (không phải lỗi của khối)
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
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
                rel = ["--release", str(e["java_release"])] if e.get("java_release") else []
                rc, so, se = _run(["javac", "-encoding", "UTF-8"] + rel + ["-d", d, f"{cls}.java"], cwd=d)
                if "expect_compile_error" in e:
                    w = e["expect_compile_error"]
                    good = rc != 0 and w in (so + se)
                    return (good, f"javac báo lỗi chứa {w!r}" if good else f"javac rc={rc}, không thấy {w!r}: {se[:160]!r}",
                            so, se)
                if rc:
                    return False, "javac: " + (se.strip().splitlines() or ["?"])[0][:200], so, se
                if kind == "syntax":
                    return True, "javac", "", ""
                rc, so, se = _run(["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", "-cp", d, cls]
                                  + str(e.get("args") or "").split(), inp=e.get("stdin") or None, cwd=d, timeout=to)
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
                # shim_sqlite3: máy chưa cài sqlite3 CLI thì đặt lớp giả lập audit/fnd/shim lên PATH (như phiên FND)
                shim = ROOT / "audit" / "fnd" / "shim" if e.get("shim_sqlite3") and not shutil.which("sqlite3") else None
                return self._judge(*_run([shutil.which("bash"), "khoi.sh"], cwd=d, timeout=to, path_prepend=shim), e)
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


def _load_course_lib(course):
    """Nạp lib + src/lXX.py của audit/<khoá> (build() khai chương trình/phiên vào lib.PROGRAMS/CMDS/PROJECTS)."""
    d = ROOT / "audit" / course.lower()
    sys.path[:0] = [str(d), str(d / "src")]
    import importlib
    import lib  # noqa
    for p in sorted((d / "src").glob("l*.py")):
        lib.begin(p.stem.upper())
        importlib.import_module(p.stem).build()
    return lib


def _java_sources(progs, course, release=None, unv=None):
    """lib.PROGRAMS → ({tên: nguồn run/java}, {bài: [(tên, prog)]}). Nguồn so đầu ra, lỗi biên dịch, ngoại lệ như verify_*;
    `args`/`stdin` (nếu prog có) và `java_release` đi theo nguồn."""
    sources, by_lesson, seen = {}, {}, {}
    for pr in progs:
        key = (pr["lesson"], pr["code"], pr["expect"], pr["out"], pr["err"], pr.get("args") or "", pr.get("stdin") or "")
        if key in seen:
            continue
        n = f"{pr['lesson']}_{pr['name']}"
        i = 2
        while n in sources:
            n, i = f"{pr['lesson']}_{pr['name']}_{i}", i + 1
        seen[key] = n
        e = {"lang": "java", "java_class": pr["name"]}
        if release:
            e["java_release"] = release
        if pr.get("args"):
            e["args"] = pr["args"]
        if pr.get("stdin"):
            e["stdin"] = pr["stdin"]
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
        if unv and unv(course, pr):
            e["unverified_claims"] = unv(course, pr)
        sources[n] = e
        by_lesson.setdefault(pr["lesson"], []).append((n, pr))
    return sources, by_lesson


def _java_fragment(course, k, t, by_lesson):
    """Khối là dãy dòng liên tiếp của một chương trình Java → mục fragment, không thì None."""
    lid, frag = k.split()[1], _dedent_lines(t)
    for n, pr in by_lesson.get(lid, []):
        hl = pr["code"].split("\n")
        if any(_dedent_lines("\n".join(hl[i:i + len(frag)])) == frag for i in range(len(hl) - len(frag) + 1)):
            return {"sha": digest(t), "kind": "fragment", "within": f"src:{course}:{n}",
                    "reason": f"dãy dòng của chương trình {pr['name']} (nguồn chạy thật)"}
    return None


def _java_output(course, k, t, by_lesson, reg):
    """Khối là kết quả (in ra, lỗi biên dịch, ngoại lệ) của một chương trình Java → mục output `of`, không thì None."""
    lid = k.split()[1]
    tl = [l.rstrip() for l in t.split("\n")]
    # ưu tiên chương trình có đoạn mã hiện ở CÙNG bước (khối kết quả đứng ngay sau đoạn mã của nó)
    same = {v["within"] for kk, v in reg.items() if kk.rsplit(" ", 1)[0] == k.rsplit(" ", 1)[0]
            and v.get("kind") == "fragment"}
    cands = sorted(by_lesson.get(lid, []), key=lambda x: f"src:{course}:{x[0]}" not in same)
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
            return {"sha": digest(t), "kind": "output", "of": f"src:{course}:{n}",
                    "reason": f"khối kết quả của chương trình {pr['name']}"}
    return None


def _java_output_loose(course, k, t, by_lesson, reg):
    """Màn hình chỉ hiện MỘT PHẦN đầu ra (vài dòng, hoặc dòng đầu của dấu vết ngăn xếp có `…`): mỗi dòng khác rỗng phải khớp CẢ
    DÒNG của stdout rồi stderr của chương trình, đúng thứ tự (như cổng output). Chỉ dùng cho khoá mới (JVA không bật)."""
    lid = k.split()[1]
    want = [l.strip() for l in t.split("\n") if l.strip()]
    same = {v["within"] for kk, v in reg.items() if kk.rsplit(" ", 1)[0] == k.rsplit(" ", 1)[0] and v.get("kind") == "fragment"}
    cands = sorted(by_lesson.get(lid, []), key=lambda x: f"src:{course}:{x[0]}" not in same)
    for n, pr in cands:
        actual = [l.rstrip() for l in (pr["out"] + "\n" + pr["err"]).split("\n")]
        if pr["expect"].startswith("compile_error:") and not pr["err"]:
            continue
        pos = 0
        for w in want:
            while pos < len(actual) and not _line_match(w, actual[pos]):
                pos += 1
            if pos == len(actual):
                break
            pos += 1
        else:
            if want:
                return {"sha": digest(t), "kind": "output", "of": f"src:{course}:{n}",
                        "reason": f"một phần đầu ra của chương trình {pr['name']} (các dòng khớp cả dòng, đúng thứ tự)"}
    return None


_SQLITE_CMD = re.compile(r"(?m)(^|[|;&(]\s*)sqlite3\b")   # lệnh sqlite3 (đầu dòng / sau | ; & ( ), không phải `import sqlite3`


def _lab_sources(course):
    """labs/<KHOÁ>/Lxx/{loi_giai.*, mong_doi.txt} → nguồn LAB_Lxx chạy lời giải THẬT (như labs/cham.sh) và đòi đúng mong_doi.txt.
    Khối `practice` hiện kết quả mong đợi / đoạn đề của lab là fragment/output của nguồn này."""
    out, by_lesson = {}, {}
    for d in sorted((ROOT / "labs" / course).glob("L*")):
        sol = next(iter(sorted(d.glob("loi_giai.*"))), None)
        exp = d / "mong_doi.txt"
        if sol is None or not exp.exists():
            continue
        code = sol.read_text(encoding="utf-8").strip("\n")
        e = {"lang": {".sh": "bash", ".java": "java", ".py": "python", ".sql": "sqlite"}.get(sol.suffix)}
        if e["lang"] is None:
            continue
        if e["lang"] == "java":
            m = re.search(r"public\s+(?:final\s+)?class\s+(\w+)", code)
            e["java_class"] = m.group(1) if m else "Main"
            if course == "JV2":
                e["java_release"] = 21
        e["expect_stdout"] = exp.read_text(encoding="utf-8").strip("\n")
        if e["lang"] == "bash" and _SQLITE_CMD.search(code):
            e["shim_sqlite3"] = True
        if _SQLITE_CMD.search(code) and not shutil.which("sqlite3"):
            e["unverified_claims"] = ["lời giải chạy sqlite3 bằng lớp giả lập audit/fnd/shim (máy chưa cài sqlite3 CLI thật): "
                                      "định dạng đầu ra của CLI thật chưa được máy đối chiếu"]
        if e["lang"] == "sqlite":
            e["unverified_claims"] = ["lời giải SQL chạy bằng thư viện sqlite3 của python (cột ngăn bằng `|`), không bằng sqlite3 CLI thật: "
                                      "định dạng đầu ra của CLI thật chưa được máy đối chiếu"]
        e["code"] = code
        out[f"LAB_{d.name}"] = e
        by_lesson[d.name] = (f"LAB_{d.name}", e)
    return out, by_lesson


def _lab_hit(course, k, t, labs):
    """Khối của bài `lid`: đoạn liên tiếp của lời giải lab (đề) hoặc kết quả mong đợi của lab → mục sổ, không thì None."""
    lab = labs.get(k.split()[1])
    if lab is None:
        return None
    n, e = lab
    frag = _dedent_lines(t)
    if _windows(e["code"].split("\n"), frag) is not None:
        return {"sha": digest(t), "kind": "fragment", "within": f"src:{course}:{n}",
                "reason": f"dãy dòng của lời giải lab {n} (nguồn chạy thật qua cách chấm của labs/cham.sh)"}
    want = [l.strip() for l in t.split("\n") if l.strip()]
    actual = [l.rstrip() for l in e["expect_stdout"].split("\n")]
    pos = 0
    for w in want:
        while pos < len(actual) and not _line_match(w, actual[pos]):
            pos += 1
        if pos == len(actual):
            return None
        pos += 1
    return {"sha": digest(t), "kind": "output", "of": f"src:{course}:{n}",
            "reason": f"kết quả mong đợi của lab {n}: đầu ra THẬT của lời giải (chạy như labs/cham.sh)"}


def _write_ledger(course, cmdname, hdr, reg, sources, unmatched, blocks, pretty):
    """Ghi REGDIR/<KHOÁ>.yaml; mục `hand: true` của sổ cũ ứng với khối chưa khớp được giữ lại (và bỏ khỏi `unmatched`)."""
    REGDIR.mkdir(parents=True, exist_ok=True)
    out = REGDIR / f"{course}.yaml"
    if out.exists():
        d = yaml.safe_load(open(out, encoding="utf-8")) or {}
        for k, v in (d.get("blocks") or {}).items():
            if v.get("hand") and k in unmatched:
                if pretty and v.get("sha") != digest(blocks[k]):
                    continue   # khối đã đổi chữ: mục tay hết hiệu lực, in CHƯA KHỚP để làm lại (JVA: giữ y như cũ)
                reg[k] = v
                unmatched.remove(k)
    if pretty:
        body = yaml.dump({"blocks": reg, "sources": sources}, Dumper=_PrettyDumper, allow_unicode=True, sort_keys=False,
                         width=200)
    else:
        body = yaml.safe_dump({"blocks": reg, "sources": sources}, allow_unicode=True, sort_keys=False, width=200)
    out.write_text(hdr + body, encoding="utf-8", newline="\n")
    print(f"{cmdname}: {len(blocks)} khối, ghi {len(reg)}, nguồn {len(sources)}, chưa khớp {len(unmatched)}")
    for k in unmatched:
        print("  CHƯA KHỚP", k, "|", (blocks[k].splitlines() or [""])[0][:90])


class _PrettyDumper(yaml.SafeDumper):
    """Chuỗi nhiều dòng ghi dạng khối `|` (đọc được, diff được); chỉ dùng cho FND/JV2 (JVA giữ safe_dump để sổ cũ không đổi)."""


def _pretty_str(dumper, s):
    return dumper.represent_scalar("tag:yaml.org,2002:str", s, style="|" if "\n" in s else None)


_PrettyDumper.add_representer(str, _pretty_str)


def cmd_gen_jva(a):
    """Sổ JVA từ lib.PROGRAMS (audit/jva/src): mỗi chương trình → một NGUỒN run/java (so đầu ra, lỗi biên dịch, ngoại lệ
    như verify_jva); khối mã trên màn hình → fragment `within` nguồn có chứa nó (dãy dòng liên tiếp, bỏ thụt lề chung);
    khối kết quả → output `of` nguồn. Khối không khớp gì → in "CHƯA KHỚP", không ghi (thêm tay với `hand: true`)."""
    lib = _load_course_lib("JVA")
    sources, by_lesson = _java_sources(lib.PROGRAMS, "JVA")
    blocks = all_blocks("JVA")
    reg, unmatched = {}, []
    for k, t in blocks.items():
        hit = _java_fragment("JVA", k, t, by_lesson) or _java_output("JVA", k, t, by_lesson, reg)
        if hit:
            reg[k] = hit
        else:
            unmatched.append(k)
    hdr = ("# Sổ mã trên màn hình khoá JVA — SINH bằng `screen_code.py gen-jva` từ audit/jva/src (lib.PROGRAMS).\n"
           "# Mục `hand: true` (khối không khớp chương trình nào) được giữ qua các lần sinh lại.\n")
    _write_ledger("JVA", "gen-jva", hdr, reg, sources, unmatched, blocks, pretty=False)


# ───────────── FND / JV2: phiên dòng lệnh chạy thật (lib.CMDS, lib.PROJECTS) ─────────────
def _session_sources(items, course, profile):
    """lib.CMDS (FND) / lib.PROJECTS (JV2) → ({tên: nguồn session}, {bài: [(tên, nguồn)]}); trùng (bài, tên, bước, tệp) gộp một."""
    sources, by_lesson, seen = {}, {}, set()
    for c in items:
        key = (c["lesson"], c["name"], tuple(c["steps"]), tuple(sorted(c["files"].items())))
        if key in seen:
            continue
        seen.add(key)
        n = f"{c['lesson']}_{c['name']}"
        i = 2
        while n in sources:
            n, i = f"{c['lesson']}_{c['name']}_{i}", i + 1
        e = {"lang": "bash", "profile": profile}
        if profile == "jv2":
            if c.get("env"):
                e["env"] = dict(c["env"])
            if c.get("deps") or any("{DEPS}" in a for a, _ in c["steps"]):
                e["deps"] = True
        if c["files"]:
            e["fs"] = dict(c["files"])
        e["session"] = [{"cmd": a, "out": b} for a, b in c["steps"]]
        unv = _unverified(course, c, e)
        if any("AppSong" in a and "head -1" in a for a, _ in c["steps"]):
            # JV2 L09: bước chạy AppSong với -Xmx64m: nhiều luồng ForkJoin cùng ném OutOfMemoryError nên các dòng stderr xen kẽ;
            # `head -1` đôi khi cắt đúng dòng bị xen (máy chạy ra "" thay vì OutOfMemoryError). Đo 2026-11-13: khoảng 1 trong 6 lần.
            e["retries"] = 4
            unv.append("bước `java -Xmx64m … AppSong … | head -1 | grep -o OutOfMemoryError` KHÔNG TẤT ĐỊNH: stderr của nhiều luồng xen kẽ, "
                       "có lần dòng đầu không chứa OutOfMemoryError (grep in rỗng); cổng cho thử lại tới 4 lần (retries) — màn hình chỉ đúng "
                       "phần lớn lần chạy. Đề xuất sửa bài: dùng `grep -m1 -o OutOfMemoryError` hoặc `grep -c`")
        if unv:
            e["unverified_claims"] = unv
        sources[n] = e
        by_lesson.setdefault(c["lesson"], []).append((n, e))
    return sources, by_lesson


def _windows(host, frag):
    """Chỉ số đầu của dãy dòng liên tiếp trong host bằng frag (bỏ thụt lề chung, như cổng), không có → None."""
    for i in range(len(host) - len(frag) + 1):
        if _dedent_lines("\n".join(host[i:i + len(frag)])) == frag:
            return i
    return None


def _session_hit(course, k, t, by_lesson):
    """Khối terminal / tệp / kết quả của một phiên → mục sổ, không khớp → None.
    1) dãy dòng liên tiếp của phiên vẽ đủ ($ lệnh + đầu ra); 2) dãy dòng liên tiếp của RIÊNG các dòng lệnh (đầu ra bị ẩn);
    3) đoạn một tệp dựng sẵn (fs)."""
    lid, frag = k.split()[1], _dedent_lines(t)
    cand = by_lesson.get(lid, [])
    for n, e in cand:
        if _windows(render_session(e["session"]).split("\n"), frag) is not None:
            return {"sha": digest(t), "kind": "fragment", "within": f"src:{course}:{n}",
                    "reason": f"dãy dòng của phiên dòng lệnh {n} (chạy thật từng bước, đầu ra so nguyên văn)"}
    for n, e in cand:
        if _windows(render_session(e["session"], outputs=False).split("\n"), frag) is not None:
            return {"sha": digest(t), "kind": "fragment", "within": f"src:{course}:{n}", "cmds_only": True,
                    "reason": f"các dòng lệnh của phiên {n} (đầu ra không hiện trên màn hình ở khối này)"}
    for n, e in cand:
        for path, content in (e.get("fs") or {}).items():
            hl = [l.rstrip() for l in str(content).strip("\n").split("\n")]
            if _windows(hl, frag) is not None:
                return {"sha": digest(t), "kind": "fragment", "within": f"src:{course}:{n}#{path}",
                        "reason": f"nội dung tệp {path} dựng sẵn cho phiên {n} (phiên chạy thật trên đúng tệp này)"}
    return None


def _session_output_hit(course, k, t, by_lesson):
    """Các dòng của khối là một DÃY CON có thứ tự của đầu ra các bước một phiên (khối kết quả mong đợi, không hiện lệnh)."""
    want = [l.strip() for l in t.split("\n") if l.strip()]
    for n, e in by_lesson.get(k.split()[1], []):
        actual = [l.rstrip() for s in e["session"] for l in str(s.get("out") or "").split("\n")]
        pos = 0
        for w in want:
            while pos < len(actual) and not _line_match(w, actual[pos]):
                pos += 1
            if pos == len(actual):
                break
            pos += 1
        else:
            return {"sha": digest(t), "kind": "output", "of": f"src:{course}:{n}",
                    "reason": f"đầu ra thật của phiên {n} (các dòng liên tiếp có thứ tự)"}
    return None


# điều bài nói mà máy KHÔNG kiểm được → unverified_claims của nguồn (sinh theo luật, ổn định giữa các lần gen)
def _unverified(course, c, e):
    cmds = "\n".join(a for a, _ in c["steps"])
    u = []
    if course == "FND":
        if _SQLITE_CMD.search(cmds) and not shutil.which("sqlite3"):
            u.append("đầu ra của lệnh sqlite3 được kiểm bằng lớp giả lập audit/fnd/shim (python sqlite3), vì máy kiểm chưa cài sqlite3 "
                     "CLI thật: định dạng bảng/tiêu đề/ký tự ngăn của CLI thật chưa được máy đối chiếu")
        if any(not re.search(r"[|>`]|\$\(", a) and re.search(r"(^|[;&] *)ls\b", a) for a, _ in c["steps"]):
            u.append("bố cục cột của `ls` là giả lập cửa sổ lệnh rộng 80 cột (alias -F -C -w 80 của runner), không phải cửa sổ thật")
        if re.search(r"\bcurl\b", cmds):
            u.append("phiên chạy máy chủ thử python trên cổng cục bộ 18765; hành vi trên mạng thật (độ trễ, DNS) không kiểm được")
        if "--max-time" in cmds:
            u.append("bài nói cờ thời gian chờ làm ta bỏ cuộc sau một giây: máy kiểm mã thoát 28 và dòng in ra, không đo thời gian chờ thật")
        if "grep -n ERROR big.log" in cmds:
            u.append("bài nói hai nhật ký (1201 và 120001 dòng) cùng nhanh dù lớn gấp một trăm lần: máy kiểm dòng tìm ra, không đo thời gian")
        if "big.db" in cmds:
            u.append("bài nói chênh lệch thời gian truy vấn tăng nhanh theo kích thước bảng và chỉ mục làm ghi chậm hơn: máy kiểm số dòng và "
                     "kết quả truy vấn, không đo thời gian")
    return u


def _unverified_prog(course, pr):
    """Điều bài nói về một chương trình Java mà đầu ra in ra không chứng minh được."""
    if course == "JV2" and pr["name"] == "ThoiGian":
        return ["bài nói đo thật khớp lý thuyết (2000 ms và 200 ms): máy chỉ kiểm cờ boolean `do gan dung` (sai số cho phép, phụ thuộc "
                "máy), không kiểm số mili giây đo được"]
    return []


def cmd_gen_prog(a):
    """Sổ FND / JV2 (hoặc JVA) theo mẫu gen-jva.
    FND: mỗi lib.cmd(...) → một NGUỒN `session` (Git Bash chạy thật, so từng bước); khối terminal → fragment `within` phiên
    (dãy dòng liên tiếp của phiên vẽ như màn hình; `cmds_only` khi đầu ra bị ẩn); khối nội dung tệp → fragment `within`
    `src:…#<tệp>`; khối kết quả mong đợi → output `of` phiên.
    JV2: lib.prog(...) như JVA (nguồn java + `args`/`stdin`, javac --release 21 như verify_jv2) và lib.project(...) như FND
    (profile jv2: javac/java/jar/junit chạy thật trong phiên Git Bash, jar ngoài ở audit/jv2/deps).
    Khối không khớp gì → in "CHƯA KHỚP" (thêm tay `hand: true`, giữ qua các lần sinh)."""
    course = (a.course or {"gen-fnd": "FND", "gen-jv2": "JV2"}.get(a.cmd) or "").upper()
    if course == "JVA":
        return cmd_gen_jva(a)
    if course not in ("FND", "JV2"):
        raise SystemExit("gen-prog cần --course JVA|FND|JV2")
    lib = _load_course_lib(course)
    labs_src, labs = _lab_sources(course)
    sources, java_by, sess_by = {}, {}, {}
    if course == "JV2":
        sources, java_by = _java_sources(lib.PROGRAMS, course, release=21, unv=_unverified_prog)
        ss, sess_by = _session_sources(lib.PROJECTS, course, "jv2")
    else:
        ss, sess_by = _session_sources(lib.CMDS, course, "fnd")
    for n in ss:
        if n in sources:
            raise SystemExit(f"tên nguồn trùng giữa chương trình và phiên: {n}")
    sources.update(ss)
    sources.update(labs_src)
    blocks = all_blocks(course)
    reg, unmatched = {}, []
    for k, t in blocks.items():
        lab_first = k.split()[2] == "practice"   # cảnh Tự làm: khối là đề/kết quả của lab (số liệu khác ví dụ của bài)
        hit = ((_lab_hit(course, k, t, labs) if lab_first else None) or _java_fragment(course, k, t, java_by)
               or _session_hit(course, k, t, sess_by) or _java_output(course, k, t, java_by, reg)
               or _session_output_hit(course, k, t, sess_by) or _java_output_loose(course, k, t, java_by, reg)
               or _lab_hit(course, k, t, labs))
        if hit:
            reg[k] = hit
        else:
            unmatched.append(k)
    cn = {"FND": "audit/fnd/src (lib.CMDS)", "JV2": "audit/jv2/src (lib.PROGRAMS + lib.PROJECTS)"}[course]
    hdr = (f"# Sổ mã trên màn hình khoá {course} — SINH bằng `screen_code.py gen-{course.lower()}` từ {cn}.\n"
           "# Mục `hand: true` (khối không khớp nguồn nào, đã đọc kiểm tay) được giữ qua các lần sinh lại.\n")
    _write_ledger(course, f"gen-{course.lower()}", hdr, reg, sources, unmatched, blocks, pretty=True)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["inventory", "check", "stub", "show", "gen-jva", "gen-prog", "gen-fnd", "gen-jv2"])
    ap.add_argument("key", nargs="?")
    ap.add_argument("--course")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    f = {"inventory": cmd_inventory, "check": cmd_check, "stub": cmd_stub, "show": cmd_show,
         "gen-jva": cmd_gen_jva, "gen-prog": cmd_gen_prog, "gen-fnd": cmd_gen_prog, "gen-jv2": cmd_gen_prog}[a.cmd]
    return f(a) or 0


if __name__ == "__main__":
    sys.exit(main())
