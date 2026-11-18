"""Bộ kiểm độc lập khoá PYT: chạy THẬT mọi chương trình (py), phiên gõ từng câu (repl), phiên Git Bash (sh) và phép đo (measure) khai bằng
audit/pyt/lib.py trong audit/pyt/src/lXX.py, rồi so từng dòng với giá trị hiện trên màn hình.
  - py env="std": chạy trên Python 3.11 (python trong PATH) VÀ 3.13 (.venv), mỗi bản với PYTHONHASHSEED=1 và =2; bốn đầu ra phải GIỐNG HỆT và khớp bài;
  - py env="venv": chỉ trên labs/.venv-pyt (3.11 + numpy, pandas, matplotlib, pytest ghim ở labs/requirements-py.txt);
  - repl: code.InteractiveConsole (đúng hành vi cửa sổ `>>>`), cả hai bản Python;
  - sh: Git Bash thật (audit/fnd/runner.py), `python` lần lượt là 3.11 và 3.13;
  - measure: số tất định khớp đúng (m_ dung sai 10%), số thời gian t_* cùng bậc độ lớn (×/÷ 8, máy có thể đang tải) so với measured.json; khoá mới thì ghi.
Chạy: .venv/Scripts/python -B audit/pyt/verify_pyt.py [L00 L01 …]   (--remeasure để đo lại và ghi đè measured.json)"""
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "pyt"))
sys.path.insert(0, str(ROOT / "audit" / "pyt" / "src"))
sys.path.append(str(ROOT / "audit" / "fnd"))
sys.stdout.reconfigure(encoding="utf-8")
import lib  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
REMEASURE = "--remeasure" in sys.argv


def pyver(exe):
    try:
        r = subprocess.run([str(exe), "--version"], capture_output=True, text=True, timeout=30)
        return (r.stdout + r.stderr).strip()
    except Exception:
        return ""


def find_std311():
    for c in (shutil.which("python"), str(ROOT / "labs" / ".venv-pyt" / "Scripts" / "python.exe")):
        if c and pyver(c).startswith("Python 3.11"):
            return c
    return None


PY311 = find_std311()
PY313 = str(ROOT / ".venv" / "Scripts" / "python.exe")
PYV = str(ROOT / "labs" / ".venv-pyt" / "Scripts" / "python.exe")
INTERP = {"3.11": PY311, "3.13": PY313}
print("Python 3.11:", PY311, pyver(PY311) if PY311 else "KHÔNG CÓ", "| 3.13:", pyver(PY313), "| venv:", pyver(PYV))


def norm(s):
    s = re.sub(r"\bin \d+\.\d+s\b", "in 0.01s", s)  # tổng kết của pytest ("7 passed in 0.02s") luôn khác nhau giữa các lần chạy
    return "\n".join(l.rstrip() for l in s.replace("\r\n", "\n").replace("\r", "\n").strip("\n").split("\n"))


def env_for(seed):
    e = dict(os.environ)
    e.update({"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1", "MPLBACKEND": "Agg", "PYTHONHASHSEED": str(seed), "PYTHONDONTWRITEBYTECODE": "1",
              "TZ": "UTC", "COLUMNS": "80"})
    return e


def screen_lines_ok(err, text):
    lines = [l.strip() for l in text.replace("\r\n", "\n").split("\n")]
    pos = 0
    for want in [l.strip() for l in err.split("\n") if l.strip()]:
        rx = re.compile("^" + ".*".join(re.escape(x) for x in want.split("…")) + "$")
        while pos < len(lines) and not rx.match(lines[pos]):
            pos += 1
        if pos == len(lines):
            return False
        pos += 1
    return True


def run_prog(p, exe, seed):
    with tempfile.TemporaryDirectory(prefix="pyt_") as d:
        for rel, content in p["files"].items():
            f = Path(d) / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(content.encode("utf-8"))
        src = Path(d) / f'{p["name"]}.py'
        src.write_bytes((p["code"] + "\n").encode("utf-8"))
        r = subprocess.run([exe, src.name], cwd=d, env=env_for(seed), capture_output=True, timeout=180, input=(p["stdin"] or "").encode("utf-8"))
        return r.returncode, r.stdout.decode("utf-8", errors="replace"), r.stderr.decode("utf-8", errors="replace")


ok = fail = 0


def report(good, label, why):
    global ok, fail
    ok += good
    fail += not good
    print(f"{'PASS' if good else 'FAIL'} {label}: {why}")


SPECS = {}
for lid in (a.upper() for a in args) if args else sorted(p.stem.upper() for p in (ROOT / "audit/pyt/src").glob("l*.py")):
    lib.begin(lid)
    SPECS[lid] = importlib.import_module(lid.lower()).build()[1]

seen = set()
# ── py ──
for p in lib.PROGS:
    key = (p["lesson"], p["name"], p["code"], p["out"])
    if key in seen:
        continue
    seen.add(key)
    runs = [("3.11", PYV if p["env"] == "venv" else PY311, 1)]
    if p["env"] == "std":
        runs += [("3.11", PY311, 2), ("3.13", PY313, 1), ("3.13", PY313, 2)]
    outs, why, good = [], [], True
    for ver, exe, seed in runs:
        if not exe:
            good = False
            why.append("thiếu Python " + ver)
            continue
        rc, so, se = run_prog(p, exe, seed)
        outs.append(norm(so))
        tag = f"{ver}/s{seed}"
        if p["expect"] == "run":
            if rc != 0:
                good = False
                why.append(f"{tag}: rc={rc} stderr={se[-300:]!r}")
        else:
            exc = p["expect"].split(":", 1)[1]
            lastl = [l for l in se.strip().split("\n") if l.strip()][-1:] or [""]
            if rc == 0 or not lastl[0].startswith(exc):
                good = False
                why.append(f"{tag}: cần lỗi {exc}; rc={rc} cuối stderr={lastl[0][:120]!r}")
            elif p["err"] and not screen_lines_ok(p["err"], se):
                good = False
                why.append(f"{tag}: dòng lỗi trên màn hình không khớp stderr: {se[-400:]!r}")
        if outs[-1] != norm(p["out"]):
            good = False
            why.append(f"{tag}: đầu ra LỆCH mong {norm(p['out'])[:200]!r} thấy {outs[-1][:200]!r}")
    if len(set(outs)) > 1:
        good = False
        why.append("đầu ra khác nhau giữa các lần chạy")
    report(good, f"{p['lesson']} py {p['name']}", f"{len(runs)} lần chạy khớp" if good else " | ".join(why[:3]))

# ── repl ──
HARNESS = '''
import code, contextlib, io, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
steps = json.loads(sys.stdin.buffer.read().decode("utf-8"))
con = code.InteractiveConsole()
res = []
for text in steps:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        more = False
        for line in text.split("\\n"):
            more = con.push(line)
        if more:
            con.push("")
    out = buf.getvalue()
    if out.startswith("Traceback"):
        keep = []
        for l in out.rstrip("\\n").split("\\n"):
            if l.startswith("    "):
                continue
            keep.append(re.sub(r'File "<console>"', 'File "<stdin>"', l))
        out = "\\n".join(keep) + "\\n"
    res.append(out)
sys.stdout.write(json.dumps(res))
'''
for r in lib.REPLS:
    key = (r["lesson"], r["name"], tuple(r["steps"]))
    if key in seen:
        continue
    seen.add(key)
    good, why = True, []
    runs = [("3.11", PYV if r["env"] == "venv" else PY311)] + ([("3.13", PY313)] if r["env"] == "std" else [])
    for ver, exe in runs:
        with tempfile.TemporaryDirectory(prefix="pyt_") as d:
            Path(d, "h.py").write_text(HARNESS, encoding="utf-8")
            q = subprocess.run([exe, "-X", "utf8", "h.py"], cwd=d, env=env_for(1), capture_output=True, timeout=180,
                               input=json.dumps([a for a, _ in r["steps"]]).encode("utf-8"))
            if q.returncode != 0:
                good = False
                why.append(f"{ver}: {q.stderr.decode('utf-8', 'replace')[-300:]!r}")
                continue
            got = json.loads(q.stdout.decode("utf-8"))
            for i, (a, w) in enumerate(r["steps"]):
                if norm(got[i]) != norm(w):
                    good = False
                    why.append(f"{ver} bước {i} `{a.splitlines()[0][:40]}`: mong {norm(w)[:160]!r}; thấy {norm(got[i])[:160]!r}")
    report(good, f"{r['lesson']} repl {r['name']}", f"{len(r['steps'])} bước khớp trên {len(runs)} bản Python" if good else " | ".join(why[:3]))

# ── sh (Git Bash) ──
if lib.SHS:
    from runner import run_session  # noqa: E402
    old_path = os.environ["PATH"]
    for c in lib.SHS:
        key = (c["lesson"], c["name"], tuple(c["steps"]), tuple(sorted(c["files"].items())))
        if key in seen:
            continue
        seen.add(key)
        good, why = True, []
        for ver, exe in (("3.11", PY311), ("3.13", PY313)):
            if c.get("only311") and ver != "3.11":
                continue
            os.environ["PATH"] = str(Path(exe).parent) + os.pathsep + old_path
            got, err, R = run_session(c["files"], [a for a, _ in c["steps"]])
            if got is None:
                good = False
                why.append(err)
            else:
                for i, (a, w) in enumerate(c["steps"]):
                    have = norm(got.get(i, "<<không có đầu ra>>"))
                    if have != norm(w):
                        good = False
                        why.append(f"{ver} bước {i} `{a.splitlines()[0][:40]}`: mong {norm(w)[:160]!r}; thấy {have[:160]!r}")
            shutil.rmtree(R, ignore_errors=True)
        os.environ["PATH"] = old_path
        report(good, f"{c['lesson']} sh {c['name']}", f"{len(c['steps'])} bước khớp trên " + ("3.11" if c.get("only311") else "3.11 và 3.13") if good else " | ".join(why[:3]))

# ── measure ──
stored = json.loads(lib.MEASURED.read_text(encoding="utf-8")) if lib.MEASURED.exists() else {}
changed = False
touched = set()
for m in lib.MEASURES:
    exe = PYV if m["env"] == "venv" else PY311
    best = None
    for _ in range(3 if (m["key"] not in stored or REMEASURE) else 1):
        with tempfile.TemporaryDirectory(prefix="pyt_") as d:
            Path(d, "m.py").write_bytes((m["code"] + "\n").encode("utf-8"))
            q = subprocess.run([exe, "m.py"], cwd=d, env=env_for(1), capture_output=True, timeout=600)
        if q.returncode != 0:
            best = ("ERR", q.stderr.decode("utf-8", "replace")[-300:])
            break
        got = json.loads(q.stdout.decode("utf-8").strip().split("\n")[-1])
        if best is None:
            best = got
        else:
            for k, v in got.items():
                if k.startswith("t_"):
                    best[k] = min(best[k], v)
    if isinstance(best, tuple):
        report(False, f"{m['lesson']} measure {m['key']}", f"chạy lỗi: {best[1]!r}")
        continue
    st_ = stored.get(m["key"])
    if st_ is None or REMEASURE:
        stored[m["key"]] = best
        changed = True
        touched.add(m["key"])
        report(True, f"{m['lesson']} measure {m['key']}", "ĐO MỚI " + json.dumps(best))
        continue
    why = []
    for k, v in best.items():
        s = st_.get(k)
        if s is None:
            st_[k] = v
            changed = True
            touched.add(m["key"])
        elif k.startswith("t_"):
            if not (s / 8 <= v <= s * 8):
                why.append(f"{k}: lưu {s:.3g} s, đo lại {v:.3g} s (lệch quá ×8)")
        elif k.startswith("m_"):
            if abs(v - s) > 0.1 * abs(s):
                why.append(f"{k}: lưu {s}, đo lại {v}")
        elif v != s:
            why.append(f"{k}: lưu {s}, đo lại {v}")
    report(not why, f"{m['lesson']} measure {m['key']}", "khớp số đã lưu " + json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in best.items()})
           if not why else " | ".join(why))
if changed:  # đọc lại tệp ngay trước khi ghi để hai lần chạy song song không đè số đo của nhau
    cur = json.loads(lib.MEASURED.read_text(encoding="utf-8")) if lib.MEASURED.exists() else {}
    for k_ in touched:
        cur[k_] = stored[k_]
    lib.MEASURED.write_text(json.dumps(cur, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8", newline="\n")

# ── screen: khối mã trên màn hình gõ lại được và ra đúng kết quả hiện kèm (audit/pyt/screen_check.py) ──
import screen_check  # noqa: E402
for good_, label_, why_ in screen_check.run(SPECS, lib.PROGS, lib.MEASURES, PY311, PY313, lib.SHS, PYV):
    report(good_, label_, why_)

print(f"verify_pyt: {ok}/{ok + fail} PASS")
print("checked_at=" + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
sys.exit(1 if fail else 0)
