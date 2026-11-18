"""Kiểm "khối trên màn hình = mã chạy thật" cho khoá PYT (BRIEF_FIX_PYT, gốc chung 1).
Đọc đặc tả bài do build() trả về (không đọc YAML đã sinh, nên chạy được trước gen) và với MỖI khối mã hiện trong `show`:
  - khối phiên `>>>`: gõ lại nguyên văn từ trên xuống; các khối `>>>` của CÙNG MỘT CẢNH nối tiếp trong một cửa sổ (code.InteractiveConsole,
    3.11 và 3.13), mỗi cảnh một cửa sổ MỚI; từng câu phải ra đúng kết quả hiện ngay dưới nó (biến chưa gán, thiếu import,
    kết quả dán nhầm đều bị bắt);
  - khối mã chương trình (khớp một đoạn liên tiếp của một `py(...)`) có khối kết quả ngay sau trong cùng step: chạy ĐÚNG đoạn đó (cộng các đoạn
    trước của cùng chương trình đã hiện trong cùng cảnh: người học gõ từ trên xuống) rồi so từng dòng với khối kết quả;
  - khối mã chương trình đứng một mình: chỉ kiểm cú pháp (cùng các đoạn trước) trừ chương trình cố ý lỗi;
  - khối khớp mã của một `measure(...)`: bỏ qua (đã đo ở nơi khác, số hiện ra là số đo).
Không đụng khối lệnh vỏ (`$ …`) và khung chữ không phải mã (raw_block khác)."""
import ast
import html
import json
import os
import re
import subprocess
import tempfile
import textwrap
from pathlib import Path

BLOCK_RE = re.compile(r'<div class="code">((?:<div>.*?</div>)*)</div>', re.S)
LINE_RE = re.compile(r"<div>(.*?)</div>", re.S)

HARNESS = r'''
import code, contextlib, io, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
blocks = json.loads(sys.stdin.buffer.read().decode("utf-8"))
res = []
for stmts in blocks:  # mỗi phần tử = một cảnh
    con = code.InteractiveConsole()
    outs = []
    for text in stmts:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            more = False
            for line in text.split("\n"):
                more = con.push(line)
            if more:
                con.push("")
        out = buf.getvalue()
        if out.startswith("Traceback"):
            keep = []
            for l in out.rstrip("\n").split("\n"):
                if l.startswith("    "):
                    continue
                keep.append(re.sub(r'File "<console>"', 'File "<stdin>"', l))
            out = "\n".join(keep) + "\n"
        outs.append(out)
    res.append(outs)
sys.stdout.write(json.dumps(res))
'''


def _text(h):
    return html.unescape(re.sub(r"<[^>]+>", "", h)).replace("\xa0", " ").rstrip()


def blocks_of(show):
    return [[_text(l) for l in LINE_RE.findall(b)] for b in BLOCK_RE.findall(show)]


def _norm(lines):
    return "\n".join(l.rstrip() for l in lines).strip("\n")


def _window(lines, bl):
    """Vị trí (a, b) tính từ 1 của khối bl trong lines nếu bl là một đoạn liên tiếp (sau khi bỏ thụt lề chung), ngược lại None."""
    n = len(bl)
    for i in range(len(lines) - n + 1):
        win = textwrap.dedent("\n".join(lines[i:i + n])).split("\n")
        if [x.rstrip() for x in win] == bl:
            return i + 1, i + n
    return None


def _find(progs, bl):
    if not any(x.strip() for x in bl):
        return None
    for p in progs:
        w = _window(p["code"].split("\n"), bl)
        if w:
            return p, w
    return None


def _is_measured(measures, bl):
    return any(_window(m["code"].split("\n"), bl) for m in measures)


def _screen_ok(err_lines, stderr):
    lines = [l.strip() for l in stderr.replace("\r\n", "\n").split("\n")]
    pos = 0
    for want in [l.strip() for l in err_lines if l.strip()]:
        rx = re.compile("^" + ".*".join(re.escape(x) for x in want.split("…")) + "$")
        while pos < len(lines) and not rx.match(lines[pos]):
            pos += 1
        if pos == len(lines):
            return False
        pos += 1
    return True


def _run_prog(text, p, exe):
    with tempfile.TemporaryDirectory(prefix="pyts_") as d:
        for rel, content in p["files"].items():
            f = Path(d) / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(content.encode("utf-8"))
        (Path(d) / "s.py").write_bytes((text + "\n").encode("utf-8"))
        env = dict(os.environ)
        env.update({"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1", "PYTHONHASHSEED": "1", "PYTHONDONTWRITEBYTECODE": "1", "TZ": "UTC", "COLUMNS": "80"})
        r = subprocess.run([exe, "s.py"], cwd=d, env=env, capture_output=True, timeout=180, input=(p["stdin"] or "").encode("utf-8"))
        return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")


def _parse_repl(bl):
    stmts = []
    for l in bl:
        if l.startswith(">>> "):
            stmts.append([[l[4:]], []])
        elif (l.startswith("... ") or l == "...") and stmts and not stmts[-1][1]:
            stmts[-1][0].append(l[4:])
        elif stmts:
            stmts[-1][1].append(l)
    return stmts


def _norm_out(s):
    s = re.sub(r"\bin \d+\.\d+s\b", "in 0.01s", s)
    return "\n".join(l.rstrip() for l in s.replace("\r\n", "\n").replace("\r", "\n").strip("\n").split("\n"))


def _cover(want, cands, repls):
    """Tệp `want` (chuỗi đã chuẩn hoá) hiện trên màn hình: hoặc MỘT khối giống hệt (sau khi áp các cặp thay chữ), hoặc nhiều khối LIÊN TIẾP
    nhau (tách step) mà ghép lại, chỉ cách nhau bằng dòng trống, ra đúng tệp. Trả về nội dung dựng lại hoặc None."""
    blocks = []
    for c in cands:
        t = c
        for a_, b_ in repls:
            t = t.replace(a_, b_)
        blocks.append(t)
    if want in blocks:
        return want
    wl = want.split("\n")
    for i in range(len(blocks)):
        bl = blocks[i].split("\n")
        if wl[:len(bl)] != bl:
            continue
        pos, j = len(bl), i + 1
        while pos < len(wl):
            while pos < len(wl) and not wl[pos].strip():
                pos += 1
            if pos >= len(wl):
                break
            if j >= len(blocks):
                break
            nb = blocks[j].split("\n")
            if wl[pos:pos + len(nb)] != nb:
                break
            pos += len(nb)
            j += 1
        if pos >= len(wl):
            return want
    return None


def check_show_files(lid, spec, progs, shs, py311, pyv):
    """Tệp khai `show_files` phải hiện TRỌN VẸN trên màn hình (một khối mã giống hệt, sau khi áp các cặp thay chữ cũ→mới nếu khai);
    với chương trình `py(...)`: dựng lại các tệp đó TỪ KHỐI TRÊN MÀN HÌNH, chạy lại chương trình và so từng dòng với đầu ra hiện trên màn hình."""
    out = []
    blocks = [bl for sc in spec["scenes"] for st in sc["steps"] for bl in blocks_of(st.get("show", ""))]
    cands = [_norm(textwrap.dedent("\n".join(bl)).split("\n")) for bl in blocks]
    for kind, item in [("py", p) for p in progs if p["lesson"] == lid] + [("sh", c) for c in shs if c["lesson"] == lid]:
        sf = item.get("show_files") or {}
        if not sf:
            continue
        rebuilt = {}
        for fname, repls in sf.items():
            want = _norm(item["files"][fname].split("\n"))
            hit = _cover(want, cands, repls or [])
            if hit is None:
                out.append((False, f"{lid} screen-files", f"tệp `{fname}` của `{item['name']}` không hiện trọn vẹn (đúng nguyên văn) trên màn hình của bài"))
                continue
            rebuilt[fname] = hit + "\n"
        if kind == "py" and len(rebuilt) == len(sf):
            exe = pyv if item["env"] == "venv" else py311
            with tempfile.TemporaryDirectory(prefix="pytf_") as d:
                for rel, content in {**item["files"], **rebuilt}.items():
                    f = Path(d) / rel
                    f.parent.mkdir(parents=True, exist_ok=True)
                    f.write_bytes(content.encode("utf-8"))
                (Path(d) / f"{item['name']}.py").write_bytes((item["code"] + "\n").encode("utf-8"))
                env = dict(os.environ)
                env.update({"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1", "PYTHONHASHSEED": "1", "PYTHONDONTWRITEBYTECODE": "1", "TZ": "UTC", "COLUMNS": "80"})
                r = subprocess.run([exe, f"{item['name']}.py"], cwd=d, env=env, capture_output=True, timeout=300)
            got = _norm_out(r.stdout.decode("utf-8", "replace"))
            if got != _norm_out(item["out"]):
                out.append((False, f"{lid} screen-files", f"`{item['name']}`: ghép các tệp từ khối trên màn hình rồi chạy ra kết quả khác với kết quả hiện: hiện {_norm_out(item['out'])[:120]!r}; chạy {got[:120]!r}"))
            else:
                out.append((True, f"{lid} screen-files", f"`{item['name']}`: tệp {sorted(rebuilt)} dựng lại từ màn hình, chạy thật ra đúng kết quả hiện"))
        elif kind == "sh" and len(rebuilt) == len(sf):
            out.append((True, f"{lid} screen-files", f"phiên `{item['name']}`: tệp {sorted(rebuilt)} hiện trọn vẹn, đúng nội dung phiên đã chạy"))
    return out


def run(specs, progs, measures, py311, py313, shs=None, pyv=None):
    """specs = {lid: spec}. Trả về [(đạt, nhãn, lý do)]."""
    results = []
    for lid, spec in specs.items():
        results += check_show_files(lid, spec, progs, shs or [], py311, pyv)
        lp = [p for p in progs if p["lesson"] == lid]
        lm = [m for m in measures if m["lesson"] == lid]
        repl_jobs = []   # mỗi cảnh một phiên: [(nhãn, câu, kết quả mong đợi)...]
        n_pair = n_lone = 0
        fails = []
        for sc in spec["scenes"]:
            shown = {}   # tên chương trình → [(a, b)] đã hiện trong cảnh này
            scene_repl = []
            for si, st in enumerate(sc["steps"]):
                where = f"{sc['id']}#{si}"
                bls = blocks_of(st.get("show", ""))
                i = 0
                while i < len(bls):
                    bl = bls[i]
                    i += 1
                    if not any(x.strip() for x in bl):
                        continue
                    if bl[0].startswith(">>> "):
                        stm = _parse_repl(bl)
                        scene_repl += [(where, "\n".join(s_[0]), "\n".join(s_[1])) for s_ in stm]
                        continue
                    if any(x.startswith("$ ") for x in bl):
                        continue
                    if _is_measured(lm, bl):
                        continue
                    f = _find(lp, bl)
                    if not f:
                        continue
                    p, (a, b) = f
                    prev = sorted(w for w in shown.get(p["name"] + "\0" + p["code"][:40], []) if w[1] < a)
                    plines = p["code"].split("\n")
                    text = "\n".join(["\n".join(textwrap.dedent("\n".join(plines[x - 1:y])).split("\n")) for x, y in prev]
                                     + [textwrap.dedent("\n".join(plines[a - 1:b]))])
                    shown.setdefault(p["name"] + "\0" + p["code"][:40], []).append((a, b))
                    nxt = bls[i] if i < len(bls) else None
                    paired = nxt is not None and not (nxt and (nxt[0].startswith(">>> ") or any(x.startswith("$ ") for x in nxt))) and _find(lp, nxt) is None
                    if paired:
                        i += 1
                    if not paired:
                        n_lone += 1
                        if p["expect"] == "run":
                            try:
                                ast.parse(text)
                            except SyntaxError as e:
                                fails.append(f"{where} `{p['name']}` dòng {a}-{b}: mã trên màn hình sai cú pháp: {e.msg} (dòng {e.lineno})")
                        continue
                    n_pair += 1
                    rc, so, se = _run_prog(text, p, py311)
                    want = [x.rstrip() for x in nxt]
                    got = [x.rstrip() for x in so.replace("\r\n", "\n").strip("\n").split("\n")] if so.strip() else []
                    err_expected = p["expect"] != "run"
                    if rc != 0 and not err_expected:
                        fails.append(f"{where} `{p['name']}` dòng {a}-{b}: gõ lại từ trên xuống thì lỗi: {se.strip().splitlines()[-1][:160] if se.strip() else rc}")
                        continue
                    if rc == 0 and err_expected and b == len(plines):
                        fails.append(f"{where} `{p['name']}`: chương trình lẽ ra báo lỗi nhưng chạy xong")
                        continue
                    if p["stdin"]:
                        continue
                    if want[:len(got)] != got:
                        fails.append(f"{where} `{p['name']}` dòng {a}-{b}: kết quả hiện {want[:6]} khác kết quả chạy thật {got[:6]}")
                    else:
                        rest = want[len(got):]
                        if rc == 0 and rest:
                            fails.append(f"{where} `{p['name']}` dòng {a}-{b}: màn hình hiện thêm dòng không do mã in: {rest[:4]}")
                        elif rc != 0 and rest and not _screen_ok(rest, se):
                            fails.append(f"{where} `{p['name']}` dòng {a}-{b}: dòng lỗi hiện {rest[:3]} không khớp stderr {se.strip().splitlines()[-1:]}")
            if scene_repl:
                repl_jobs.append(scene_repl)
        n_repl = 0
        if repl_jobs:
            for ver, exe in (("3.11", py311), ("3.13", py313)):
                q = subprocess.run([exe, "-X", "utf8", "-c", HARNESS], capture_output=True, timeout=300,
                                   input=json.dumps([[x[1] for x in j] for j in repl_jobs]).encode("utf-8"))
                if q.returncode != 0:
                    fails.append(f"{ver}: harness lỗi {q.stderr.decode('utf-8', 'replace')[-200:]!r}")
                    continue
                got = json.loads(q.stdout.decode("utf-8"))
                for job, outs in zip(repl_jobs, got):
                    for k, ((where, s_, w_), g_) in enumerate(zip(job, outs)):
                        if _norm(g_.split("\n")) != _norm(w_.split("\n")):
                            fails.append(f"{where} khối `>>>` {ver} câu {k} `{s_.splitlines()[0][:40]}`: hiện {_norm(w_.split(chr(10)))[:100]!r}, chạy thật {_norm(g_.split(chr(10)))[:100]!r}")
            n_repl = sum(len(j) for j in repl_jobs)
        if fails:
            for f_ in fails[:12]:
                results.append((False, f"{lid} screen", f_))
        else:
            results.append((True, f"{lid} screen", f"{n_repl} câu `>>>` gõ lại từ cửa sổ mới (mỗi cảnh một phiên) khớp (3.11, 3.13); {n_pair} cặp mã/kết quả chạy lại khớp; {n_lone} khối mã đứng riêng đúng cú pháp"))
    return results
