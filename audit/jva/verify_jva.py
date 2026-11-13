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
# JVA_RELEASE=21 → javac --release 21: kiểm ngôn ngữ + API chuẩn đúng Java 21 (người học được dặn cài JDK 21+).
# Máy chạy vẫn là JDK đang cài; tham số này không thay cho việc chạy trên JVM 21 thật.
import os  # noqa: E402
REL = os.environ.get("JVA_RELEASE", "").strip()
JAVAC = ["javac", "-encoding", "UTF-8"] + (["--release", REL] if REL else [])
print("JDK:", (ver.stdout or ver.stderr).strip(), f"| --release {REL}" if REL else "")


def norm(s):
    return "\n".join(l.rstrip() for l in s.replace("\r\n", "\n").strip("\n").split("\n"))


def screen_lines_ok(err, out):
    """Mỗi dòng thông báo hiện trên màn hình (p["err"]) phải khớp CẢ MỘT dòng đầu ra thật, đúng thứ tự; "…" = đoạn bị lược;
    được bỏ tiền tố `Tệp.java:N:` của javac. (Trước 2026-11-10 so chuỗi con, nên dòng bị cắt cụt không có "…" vẫn qua —
    JVA L08; cùng luật với audit/review/screen_code.py `_line_match`.)"""
    import re
    lines = [l.strip() for l in out.replace("\r\n", "\n").split("\n")]
    pos = 0
    for want in [l.strip() for l in err.split("\n") if l.strip()]:
        rx = re.compile("^" + ".*".join(re.escape(x) for x in want.split("…")) + "$")
        while pos < len(lines) and not (rx.match(lines[pos]) or rx.match(re.sub(r"^\S+\.java:\d+:\s*", "", lines[pos]))):
            pos += 1
        if pos == len(lines):
            return False
        pos += 1
    return True


ok = fail = 0
seen = set()
for p in lib.PROGRAMS + lib.PROGRAMS_IO:
    key = (p["lesson"], p["name"], p["code"])
    if key in seen:
        continue
    seen.add(key)
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / f'{p["name"]}.java'
        src.write_text(p["code"] + "\n", encoding="utf-8")
        # chạy trong thư mục tạm với tên tệp tương đối: javac in `Thieu.java:3: error: …` đúng như người học thấy trong Git Bash
        c = subprocess.run(JAVAC + ["-d", d, src.name], capture_output=True, text=True, cwd=d,
                           encoding="utf-8", errors="replace")
        exp = p["expect"]
        if exp.startswith("compile_error:"):
            want_s = exp.split(":", 1)[1]
            # p["err"] (nếu có) = các dòng thông báo hiện trên màn hình; mỗi dòng phải có NGUYÊN VĂN trong đầu ra javac
            err_lines = [l.strip() for l in p["err"].split("\n") if l.strip()]
            good = c.returncode != 0 and want_s in (c.stderr + c.stdout) and screen_lines_ok(p["err"], c.stderr + c.stdout)
            why = f"javac rc={c.returncode}; cần thấy “{want_s}”" + (f" + {len(err_lines)} dòng màn hình" if err_lines else "") + \
                ("" if good else f"; thấy: {(c.stderr or c.stdout)[:300]!r}")
        elif c.returncode != 0:
            good, why = False, f"không biên dịch được: {c.stderr[:300]!r}"
        else:
            r = subprocess.run(["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8", "-cp", d, p["name"]],
                               capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
                               input=p.get("stdin"), cwd=d)   # cwd=d: tệp chương trình tạo ra nằm trong thư mục tạm
            got = norm(r.stdout)
            if exp.startswith("runtime_error:"):
                exc = exp.split(":", 1)[1]
                err_ok = screen_lines_ok(p["err"], r.stderr)
                good = r.returncode != 0 and exc in r.stderr and got == norm(p["out"]) and err_ok
                why = f"dòng lỗi màn hình {'khớp cả dòng' if err_ok else 'KHÔNG khớp cả dòng'} trong stderr; rc={r.returncode}; ngoại lệ {exc} {'có' if exc in r.stderr else 'KHÔNG có'} trong stderr; in ra {'khớp' if got == norm(p['out']) else 'LỆCH: ' + repr(got[:200])}"
            else:
                good = r.returncode == 0 and got == norm(p["out"])
                why = "khớp" if good else f"rc={r.returncode}; mong {norm(p['out'])[:200]!r}; thấy {got[:200]!r}; stderr {r.stderr[:200]!r}"
    ok += good
    fail += not good
    print(f"{'PASS' if good else 'FAIL'} {p['lesson']} {p['name']}: {why}")
print(f"verify_jva: {ok}/{ok + fail} PASS")
print("checked_at=" + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
sys.exit(1 if fail else 0)
