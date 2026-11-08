"""Bộ kiểm độc lập khoá JVA: biên dịch (javac) và chạy (java) THẬT mọi chương trình khai bằng lib.prog(...) trong audit/jva/src/lXX.py,
so kết quả in ra với giá trị bài giảng ghi. Đây là cách kiểm khác hẳn `checks` (Python): chạy chính mã Java người học sẽ gõ.
Chạy: .venv/Scripts/python audit/jva/verify_jva.py [L00 L01 …]   (cần javac/java trong PATH; ghi phiên bản JDK vào kết quả)"""
import importlib
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "jva"))
sys.path.insert(0, str(ROOT / "audit" / "jva" / "src"))
sys.stdout.reconfigure(encoding="utf-8")
import lib  # noqa: E402

want = [a.upper() for a in sys.argv[1:]] or sorted(p.stem.upper() for p in (ROOT / "audit/jva/src").glob("l*.py"))
for lid in want:
    lib.begin(lid)
    importlib.import_module(lid.lower()).build()

ver = subprocess.run(["javac", "-version"], capture_output=True, text=True)
print("JDK:", (ver.stdout or ver.stderr).strip())


def norm(s):
    return "\n".join(l.rstrip() for l in s.replace("\r\n", "\n").strip("\n").split("\n"))


ok = fail = 0
seen = set()
for p in lib.PROGRAMS:
    key = (p["lesson"], p["name"], p["code"])
    if key in seen:
        continue
    seen.add(key)
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / f'{p["name"]}.java'
        src.write_text(p["code"] + "\n", encoding="utf-8")
        c = subprocess.run(["javac", "-encoding", "UTF-8", "-d", d, str(src)], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        exp = p["expect"]
        if exp.startswith("compile_error:"):
            want_s = exp.split(":", 1)[1]
            good = c.returncode != 0 and want_s in (c.stderr + c.stdout)
            why = f"javac rc={c.returncode}; cần thấy “{want_s}”" + ("" if good else f"; thấy: {(c.stderr or c.stdout)[:200]!r}")
        elif c.returncode != 0:
            good, why = False, f"không biên dịch được: {c.stderr[:300]!r}"
        else:
            r = subprocess.run(["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", "-cp", d, p["name"]],
                               capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
            got = norm(r.stdout)
            if exp.startswith("runtime_error:"):
                exc = exp.split(":", 1)[1]
                good = r.returncode != 0 and exc in r.stderr and got == norm(p["out"]) and (p["err"] in r.stderr)
                why = f"dòng lỗi màn hình {'có' if p['err'] in r.stderr else 'KHÔNG có'} trong stderr; rc={r.returncode}; ngoại lệ {exc} {'có' if exc in r.stderr else 'KHÔNG có'} trong stderr; in ra {'khớp' if got == norm(p['out']) else 'LỆCH: ' + repr(got[:200])}"
            else:
                good = r.returncode == 0 and got == norm(p["out"])
                why = "khớp" if good else f"rc={r.returncode}; mong {norm(p['out'])[:200]!r}; thấy {got[:200]!r}; stderr {r.stderr[:200]!r}"
    ok += good
    fail += not good
    print(f"{'PASS' if good else 'FAIL'} {p['lesson']} {p['name']}: {why}")
print(f"verify_jva: {ok}/{ok + fail} PASS")
print("checked_at=" + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
sys.exit(1 if fail else 0)
