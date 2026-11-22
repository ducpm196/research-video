"""Khung dựng bài AF2 chuẩn hoá dùng chung cho các khoá mới (CPR, LNX, PRJ, MLP).

Mọi chương trình/lệnh hiện trên màn hình đều được biên dịch/chạy THẬT để lấy stdout thật;
mọi phòng lab đều được chấm thật qua labs/cham.sh; sổ screen_code/<KHOÁ>.yaml được sinh bằng
đúng hàm tách khối của audit/review/screen_code.py nên không bao giờ lệch sha."""
import html
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
import lv  # noqa: E402
import screen_code as sc_mod  # noqa: E402

C_BLUE = ("#dbeafe", "#2a78d6")
C_GREEN = ("#dcfce7", "#16a34a")
C_AMBER = ("#fef3c7", "#d97706")
C_RED = ("#fee2e2", "#dc2626")
C_GRAY = ("#e5e7eb", "#6b7280")

BASH_EXE = r"C:\Program Files\Git\bin\bash.exe"
if not pathlib.Path(BASH_EXE).exists():
    BASH_EXE = shutil.which("bash") or "bash"

GCC_EXE = shutil.which("gcc") or (
    r"C:\tools\w64devkit\bin\gcc.exe" if pathlib.Path(r"C:\tools\w64devkit\bin\gcc.exe").is_file() else "gcc"
)
VENV_PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
if not pathlib.Path(VENV_PY).is_file():
    VENV_PY = sys.executable


def _tool_env(extra=None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    for d in (str(ROOT / ".venv" / "Scripts"), r"C:\Program Files\Git\bin", r"C:\tools\w64devkit\bin"):
        if pathlib.Path(d).is_dir() and d not in env.get("PATH", ""):
            env["PATH"] = d + os.pathsep + env.get("PATH", "")
    for cand in sorted(pathlib.Path(r"C:\Program Files\NVIDIA Corporation").glob("Nsight*/host-windows-x64"), reverse=True):
        if (cand / "sqlite3.exe").is_file() and str(cand) not in env.get("PATH", ""):
            env["PATH"] = str(cand) + os.pathsep + env.get("PATH", "")
            break
    if extra:
        env.update(extra)
    return env


def esc(s):
    return html.escape(str(s), quote=False).replace("$", "<span>&#36;</span>")


def ic(s):
    return f"<code>{esc(s)}</code>"


def nowrap(s):
    return f"<span style='white-space:nowrap'>{s}</span>"


def code_block(text, title=None):
    lines = text.strip("\n").split("\n")
    hdr = f"<p><b>{title}</b></p>" if title else ""
    body = "".join(f"<div>{esc(l) or ' '}</div>" for l in lines)
    return f'{hdr}<div class="code">{body}</div>'


def out_block(text, title="Đầu ra chạy thật"):
    lines = text.strip("\n").split("\n")
    hdr = f"<p><b>{title}</b></p>" if title else ""
    body = "".join(f"<div>{esc(l) or ' '}</div>" for l in lines)
    return f'{hdr}<div class="code">{body}</div>'


def table(headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table class='t'><tr>{th}</tr>{trs}</table>"


def box(body, cls="key"):
    return f"<div class='box {cls}'>{body}</div>"


def svg_wrap(w, h, inner):
    return f'<div><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{inner}</svg></div>'


def svg_rect(x, y, w, h, title, sub="", color=C_BLUE):
    bg, st = color
    t1 = f'<text x="{x + w / 2}" y="{y + (h * 0.44 if sub else h * 0.56):.0f}" font-size="18" font-weight="700" text-anchor="middle" fill="#1e293b">{esc(title)}</text>'
    t2 = f'<text x="{x + w / 2}" y="{y + h * 0.74:.0f}" font-size="15" text-anchor="middle" fill="#475569">{esc(sub)}</text>' if sub else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{bg}" stroke="{st}" stroke-width="2"/>{t1}{t2}'


def svg_arrow(x1, y1, x2, y2, label=""):
    import math
    dx, dy = x2 - x1, y2 - y1
    dist = math.hypot(dx, dy) or 1.0
    ux, uy = dx / dist, dy / dist
    px, py = -uy, ux
    b1x, b1y = x2 - 8 * ux + 5 * px, y2 - 8 * uy + 5 * py
    b2x, b2y = x2 - 8 * ux - 5 * px, y2 - 8 * uy - 5 * py
    if abs(dx) >= abs(dy):
        lx, ly, anchor = (x1 + x2) / 2, min(y1, y2) - 8, "middle"
    else:
        lx, ly, anchor = (x1 + x2) / 2 + 10, (y1 + y2) / 2 + 5, "start"
    lbl = f'<text x="{lx:.0f}" y="{ly:.0f}" font-size="14" font-weight="600" text-anchor="{anchor}" fill="#1e293b">{esc(label)}</text>' if label else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#475569" stroke-width="2"/>'
        f'<polygon points="{x2},{y2} {b1x:.1f},{b1y:.1f} {b2x:.1f},{b2y:.1f}" fill="#475569"/>{lbl}'
    )


def st(show, say, focus=None, clear=None, pause=None, introduces=None, forward_ref=None, notation_note=None):
    d = {"show": show.strip("\n"), "say": " ".join(say.split())}
    if focus is not None:
        d["focus"] = focus
    if clear:
        d["clear"] = True
    if pause is not None:
        d["pause"] = pause
    if introduces:
        d["introduces"] = list(introduces)
    if forward_ref:
        d["forward_ref"] = True
    if notation_note:
        d["notation_note"] = True
    return d


def auto_focus(show_html, say_text):
    """Sinh `focus` khớp số câu lv.sentences(say_text) và số phần tử HTML thật."""
    sents = lv.sentences(say_text)
    n = len(sents)
    units = lv.html_units(show_html)
    if not units or n < 2:
        return None
    u0 = units[0]
    kids = u0.get("kids") or []
    if u0["tag"] == "table" and len(kids) >= 2:
        data_rows = [f"1.{i}" for i in range(2, len(kids) + 1)]
        if n == len(data_rows) + 1:
            return [0] + data_rows
        if n <= len(data_rows):
            return data_rows[:n]
        return [0] + [data_rows[min(i, len(data_rows) - 1)] for i in range(n - 1)]
    if len(units) >= 2:
        if n <= len(units):
            return [i + 1 for i in range(n)]
        return [min(i + 1, len(units)) for i in range(n)]
    if len(kids) >= 2:
        sub = [f"1.{i}" for i in range(1, len(kids) + 1)]
        if n <= len(sub):
            return sub[:n]
        return [0] + [sub[min(i, len(sub) - 1)] for i in range(n - 1)]
    return None


def st_auto(show, say, clear=None, pause=None, introduces=None, forward_ref=None, notation_note=None):
    return st(
        show,
        say,
        focus=auto_focus(show, say),
        clear=clear,
        pause=pause,
        introduces=introduces,
        forward_ref=forward_ref,
        notation_note=notation_note,
    )


def sc(sid, kind, title, steps, checks=None, lab=None):
    d = {"id": sid, "kind": kind, "title": title}
    if checks:
        d["checks"] = list(checks)
    if lab:
        d["lab"] = lab
    d["steps"] = steps
    return d


def build_spec(course, series, lid, title, source, objectives, scenes, covers, assumes=None):
    spec = {
        "id": lid,
        "course": course,
        "series": series,
        "title": title,
        "voice": "vi-VN-NamMinhNeural",
        "rate": "-5%",
        "depth": "full",
        "af2": True,
        "covers": [{"objective": o, "scene": s} for o, s in covers],
        "source": source,
        "assumes": list(assumes or []),
        "objectives": list(objectives),
        "asr_reviewed": [],
        "scenes": scenes,
    }
    return spec


def run_c(code, args="", stdin=None):
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
        dp = pathlib.Path(d)
        (dp / "prog.c").write_text(code.strip("\n") + "\n", encoding="utf-8", newline="\n")
        exe = str(dp / "prog.exe")
        env = _tool_env()
        c = subprocess.run([GCC_EXE, "-std=c11", "-Wall", "-Wextra", "-Werror", "prog.c", "-lm", "-o", exe],
                           cwd=d, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if c.returncode != 0:
            raise RuntimeError(f"gcc thất bại:\n{c.stderr}\n--- code ---\n{code}")
        r = subprocess.run([exe] + (args.split() if args else []), input=stdin, cwd=d, env=env,
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        if r.returncode != 0:
            raise RuntimeError(f"chạy C thất bại rc={r.returncode}:\n{r.stderr}")
        return r.stdout.replace("\r\n", "\n").strip("\n")


def run_bash(script, files=None, allow_nonzero=False):
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
        dp = pathlib.Path(d)
        for rel, content in (files or {}).items():
            p = dp / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content.strip("\n") + "\n", encoding="utf-8", newline="\n")
        (dp / "run.sh").write_text(script.strip("\n") + "\n", encoding="utf-8", newline="\n")
        r = subprocess.run([BASH_EXE, "run.sh"], cwd=d, env=_tool_env({"LC_ALL": "C.UTF-8"}),
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        if r.returncode != 0 and not allow_nonzero:
            raise RuntimeError(f"bash thất bại rc={r.returncode}:\n{r.stderr}\nstdout:\n{r.stdout}")
        return r.returncode, (r.stdout + r.stderr).replace("\r\n", "\n").strip("\n")


def run_py(code, files=None):
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
        dp = pathlib.Path(d)
        for rel, content in (files or {}).items():
            p = dp / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content.strip("\n") + "\n", encoding="utf-8", newline="\n")
        (dp / "prog.py").write_text(code.strip("\n") + "\n", encoding="utf-8", newline="\n")
        r = subprocess.run([VENV_PY, "-B", "-X", "utf8", "prog.py"], cwd=d, env=_tool_env(),
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        if r.returncode != 0:
            raise RuntimeError(f"python thất bại rc={r.returncode}:\n{r.stderr}")
        return r.stdout.replace("\r\n", "\n").strip("\n")


def write_and_grade_lab(course, lid, de_md, ext, sol_code):
    """Ghi labs/<KHOÁ>/<Lxx>/{de.md, loi_giai.<ext>, mong_doi.txt} từ đầu ra chạy thật và kiểm qua labs/cham.sh."""
    C = course.upper()
    ldir = ROOT / "labs" / C / lid
    ldir.mkdir(parents=True, exist_ok=True)
    sol_path = ldir / f"loi_giai.{ext}"
    sol_path.write_text(sol_code.strip("\n") + "\n", encoding="utf-8", newline="\n")
    (ldir / "de.md").write_text(de_md.strip("\n") + "\n", encoding="utf-8", newline="\n")
    if ext == "c":
        out = run_c(sol_code)
    elif ext == "py":
        out = run_py(sol_code)
    elif ext == "sh":
        _, out = run_bash(sol_code)
    else:
        raise ValueError(f"chưa hỗ trợ đuôi {ext}")
    (ldir / "mong_doi.txt").write_text(out + "\n", encoding="utf-8", newline="\n")
    env = _tool_env()
    chk = subprocess.run([BASH_EXE, str(ROOT / "labs" / "cham.sh"), C, lid, str(sol_path)],
                         cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if chk.returncode != 0 or chk.stdout.strip() != "ĐÚNG":
        raise RuntimeError(f"cham.sh {C} {lid} không ĐÚNG: rc={chk.returncode} out={chk.stdout!r} err={chk.stderr!r}")
    return out


def set_curriculum_spec(course, lid, spec_rel):
    p = ROOT / "curriculum" / f"{course.lower()}.yaml"
    txt = p.read_text(encoding="utf-8")
    # Chỉ thay đúng dòng spec_planned của bài lid
    cur = yaml.safe_load(txt)
    for it in cur.get("lessons") or []:
        if it.get("id") == lid:
            old_val = it.get("spec_planned") or it.get("spec")
            break
    else:
        raise KeyError(f"không thấy {lid} trong {p}")
    txt = txt.replace(f"spec_planned: {old_val}", f"spec: {spec_rel}", 1)
    p.write_text(txt, encoding="utf-8", newline="\n")


def check_say_limits(spec):
    total_words = 0
    for sc_obj in spec["scenes"]:
        for ki, step in enumerate(sc_obj["steps"]):
            say = step["say"]
            words = len(say.split())
            total_words += words
            for s in lv.sentences(say):
                sw = len(s.split())
                if sw > 38:
                    raise ValueError(f"{spec['id']} {sc_obj['id']}.{ki}: câu > 38 từ ({sw}): {s}")
                if len(s) > 170:
                    raise ValueError(f"{spec['id']} {sc_obj['id']}.{ki}: câu > 170 ký tự ({len(s)}): {s}")
    if not (900 <= total_words <= 2300):
        raise ValueError(f"{spec['id']}: tổng từ {total_words} ngoài [900, 2300]")
    return total_words


def write_lesson(spec, slug):
    c = spec["course"].lower()
    lid = spec["id"]
    check_say_limits(spec)
    out = ROOT / "lessons" / c / f"{lid}_{slug}.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        old = yaml.safe_load(out.read_text(encoding="utf-8")) or {}
        keep = {x["sentence"]: x for x in old.get("asr_reviewed") or []}
        caps = {s for sc_o in spec["scenes"] for st_o in sc_o["steps"] for s in lv.sentences(st_o["say"])}
        spec["asr_reviewed"] = [x for s, x in keep.items() if s in caps]
    out.write_text(yaml.dump(spec, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8", newline="\n")
    set_curriculum_spec(spec["course"], lid, f"lessons/{c}/{lid}_{slug}.yaml")
    res = lv.lint(lv.load_spec(out), quiet=True)
    if res.errors or res.warnings:
        raise RuntimeError(f"lint {out.name} lỗi:\nE={res.errors}\nW={res.warnings}")
    return out


def write_screen_ledger(course, meta_by_key, sources=None):
    """Sinh audit/review/screen_code/<KHOÁ>.yaml khớp từng sha với toàn bộ khối mã hiện có trong lessons/<khoá>/."""
    C = course.upper()
    actual = sc_mod.all_blocks(C)
    blocks = {}
    for k, text in actual.items():
        if k not in meta_by_key:
            raise KeyError(f"khối màn hình {k!r} chưa khai báo trong meta_by_key")
        ent = dict(meta_by_key[k])
        ent["sha"] = sc_mod.digest(text)
        blocks[k] = ent
    extra = sorted(set(meta_by_key) - set(actual))
    if extra:
        raise KeyError(f"meta_by_key dư khối không có trên màn hình: {extra[:5]}")
    doc = {"course": C, "blocks": blocks}
    if sources:
        doc["sources"] = sources
    out = ROOT / "audit" / "review" / "screen_code" / f"{C}.yaml"
    out.write_text(yaml.dump(doc, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8", newline="\n")
    return out
