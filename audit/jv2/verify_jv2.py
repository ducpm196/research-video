"""Bộ kiểm độc lập khoá JV2: biên dịch (javac) và chạy (java) THẬT mọi chương trình khai bằng lib.prog(...), và chạy THẬT mọi dự án nhiều tệp
khai bằng lib.project(...) trong một phiên Git Bash ở thư mục tạm sạch, rồi so đầu ra với giá trị bài giảng ghi.
Chạy: .venv/Scripts/python audit/jv2/verify_jv2.py [L00 L01 …]   (cần javac/java trong PATH). Dự án dùng jar ngoài ({DEPS}) mà thiếu jar → NOT_VERIFIED.
Ghi chú: JDK 21 chuẩn (JV2_RELEASE=21 → javac --release 21)."""
import importlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "jv2"))
sys.path.insert(0, str(ROOT / "audit" / "jv2" / "src"))
sys.stdout.reconfigure(encoding="utf-8")
import lib  # noqa: E402

BASH = r"C:\Program Files\Git\bin\bash.exe"
if not Path(BASH).exists():
    BASH = shutil.which("bash") or "bash"
DEPS = ROOT / "audit" / "jv2" / "deps"
MARK = "\x01@@STEP "

want = [a.upper() for a in sys.argv[1:]] or sorted(p.stem.upper() for p in (ROOT / "audit/jv2/src").glob("l*.py"))
for lid in want:
    lib.begin(lid)
    importlib.import_module(lid.lower()).build()

ver = subprocess.run(["javac", "-version"], capture_output=True, text=True)
REL = os.environ.get("JV2_RELEASE", "21").strip()
JAVAC = ["javac", "-encoding", "UTF-8"] + (["--release", REL] if REL else [])
print("JDK:", (ver.stdout or ver.stderr).strip(), f"| --release {REL}" if REL else "")


def norm(s):
    return "\n".join(l.rstrip() for l in s.replace("\r\n", "\n").replace("\r", "\n").strip("\n").split("\n"))


def posix(p):
    p = str(p).replace("\\", "/")
    return "/" + p[0].lower() + p[2:] if len(p) > 1 and p[1] == ":" else p


def screen_lines_ok(err, out):
    lines = [l.strip() for l in out.replace("\r\n", "\n").split("\n")]
    pos = 0
    for w in [l.strip() for l in err.split("\n") if l.strip()]:
        rx = re.compile("^" + ".*".join(re.escape(x) for x in w.split("…")) + "$")
        while pos < len(lines) and not (rx.match(lines[pos]) or rx.match(re.sub(r"^\S+\.java:\d+:\s*", "", lines[pos]))):
            pos += 1
        if pos == len(lines):
            return False
        pos += 1
    return True


ok = fail = nv = 0
seen = set()
for p in lib.PROGRAMS:
    key = (p["lesson"], p["name"], p["code"], p.get("args", ""), p.get("stdin", ""), p["expect"])
    if key in seen:
        continue
    seen.add(key)
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / f'{p["name"]}.java'
        src.write_text(p["code"] + "\n", encoding="utf-8")
        c = subprocess.run(JAVAC + ["-d", d, str(src)], capture_output=True, text=True, encoding="utf-8", errors="replace")
        exp = p["expect"]
        if exp.startswith("compile_error:"):
            want_s = exp.split(":", 1)[1]
            err_lines = [l.strip() for l in p["err"].split("\n") if l.strip()]
            good = c.returncode != 0 and want_s in (c.stderr + c.stdout) and screen_lines_ok(p["err"], c.stderr + c.stdout)
            why = f"javac rc={c.returncode}; cần thấy “{want_s}”" + (f" + {len(err_lines)} dòng màn hình" if err_lines else "") + \
                ("" if good else f"; thấy: {(c.stderr or c.stdout)[:300]!r}")
        elif c.returncode != 0:
            good, why = False, f"không biên dịch được: {c.stderr[:300]!r}"
        else:
            cmdl = ["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", "-cp", d, p["name"]] + p.get("args", "").split()
            r = subprocess.run(cmdl, input=p.get("stdin", ""), capture_output=True, text=True, encoding="utf-8", errors="replace",
                               timeout=60, cwd=d)   # AF2: chạy trong thư mục tạm, chương trình ghi tệp không làm bẩn gốc kho
            got = norm(r.stdout)
            if exp.startswith("runtime_error:"):
                exc = exp.split(":", 1)[1]
                err_ok = screen_lines_ok(p["err"], r.stderr)
                good = r.returncode != 0 and exc in r.stderr and got == norm(p["out"]) and err_ok
                why = f"dòng lỗi màn hình {'khớp cả dòng' if err_ok else 'KHÔNG khớp cả dòng'} trong stderr; rc={r.returncode}; ngoại lệ {exc} " \
                      f"{'có' if exc in r.stderr else 'KHÔNG có'}; in ra {'khớp' if got == norm(p['out']) else 'LỆCH: ' + repr(got[:200])}"
            else:
                good = r.returncode == 0 and got == norm(p["out"])
                why = "khớp" if good else f"rc={r.returncode}; mong {norm(p['out'])[:300]!r}; thấy {got[:300]!r}; stderr {r.stderr[:200]!r}"
    ok += good
    fail += not good
    print(f"{'PASS' if good else 'FAIL'} {p['lesson']} {p['name']}: {why}")

for p in lib.PROJECTS:
    key = (p["lesson"], p["name"], tuple(p["steps"]), tuple(sorted(p["files"].items())))
    if key in seen:
        continue
    seen.add(key)
    uses_deps = p.get("deps") or any("{DEPS}" in a for a, _ in p["steps"])
    if uses_deps and not any(DEPS.glob("*.jar")):
        nv += 1
        print(f"NOT_VERIFIED {p['lesson']} {p['name']}: thiếu jar trong audit/jv2/deps")
        continue
    R = Path(os.path.realpath(tempfile.mkdtemp(prefix="jv2_")))
    W = R / "w"
    W.mkdir()
    for rel, content in p["files"].items():
        f = W / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(content.encode("utf-8"))
    if uses_deps:  # jar ngoài được chép vào W/lib: lệnh trong bài viết đường dẫn lib/…
        (W / "lib").mkdir()
        for j in DEPS.glob("*.jar"):
            shutil.copy(j, W / "lib" / j.name)
    body = ["__rc=0"]
    for i, (a, _) in enumerate(p["steps"]):
        body.append(f"__rc=$?; printf '\\001@@STEP {i}\\n'; (exit $__rc)")
        body.append(a.replace("{DEPS}", posix(DEPS)))
    (R / "run.sh").write_text("\n".join(body) + "\n", encoding="utf-8", newline="\n")
    (R / "wrap.sh").write_text(f'exec 2>&1\ncd "{posix(W)}"\nsource "{posix(R / "run.sh")}"\n', encoding="utf-8", newline="\n")
    env = dict(os.environ)
    env.update({"LC_ALL": "C.UTF-8", "MSYS_NO_PATHCONV": "1"})
    env.update(p["env"])
    try:
        r = subprocess.run([BASH, str(R / "wrap.sh")], cwd=str(W), env=env, capture_output=True, timeout=300, stdin=subprocess.DEVNULL)
        raw = r.stdout.decode("utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        raw = ""
    raw = raw.replace(chr(92), "/")  # javac trên Windows in đường dẫn bằng gạch ngược; màn hình hiện gạch xuôi
    raw = raw.replace("Picked up JAVA_TOOL_OPTIONS: -Dstdout.encoding=UTF-8 -Dstderr.encoding=UTF-8\n", "")
    got = {}
    for seg in raw.split(MARK)[1:]:
        n, _, rest = seg.partition("\n")
        got[int(n)] = rest
    msgs = []
    for i, (a, want_out) in enumerate(p["steps"]):
        have = norm(got.get(i, "<<không có đầu ra>>"))
        if have != norm(want_out):
            msgs.append(f"bước {i} `{a.splitlines()[0][:60]}`: mong {norm(want_out)[:300]!r}; thấy {have[:300]!r}")
    good = not msgs
    ok += good
    fail += not good
    print(f"{'PASS' if good else 'FAIL'} {p['lesson']} {p['name']}: " + (f"{len(p['steps'])} bước khớp" if good else " | ".join(msgs)))
    shutil.rmtree(R, ignore_errors=True)
print(f"verify_jv2: {ok}/{ok + fail + nv} PASS" + (f", {nv} NOT_VERIFIED" if nv else ""))
print("checked_at=" + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
sys.exit(1 if fail else 0)
