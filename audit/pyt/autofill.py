"""Điền sẵn đầu ra mong đợi: trong audit/pyt/src/lXX.py khai py(name, code, "@AUTO", ...) hoặc repl bước (lệnh, "@AUTO");
chạy: .venv/Scripts/python -B audit/pyt/autofill.py L10  → chạy THẬT (venv 3.11 hoặc 3.11 thường), thay từng "@AUTO" theo thứ tự xuất hiện bằng đầu ra thật.
Chỉ để đỡ chép tay: verify_pyt vẫn chạy lại độc lập trên 3.11 + 3.13 và so từng dòng, nên đầu ra điền sai chỗ sẽ bị bắt."""
import importlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "pyt"))
sys.path.insert(0, str(ROOT / "audit" / "pyt" / "src"))
sys.stdout.reconfigure(encoding="utf-8")
import lib  # noqa: E402

lid = sys.argv[1].upper()
src_path = ROOT / "audit" / "pyt" / "src" / f"{lid.lower()}.py"
lib.begin(lid)
mod = importlib.import_module(lid.lower())
pass  # chương trình khai ở cấp mô-đun; build() không cần
PYV = str(ROOT / "labs" / ".venv-pyt" / "Scripts" / "python.exe")
ENV = {"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1", "MPLBACKEND": "Agg", "PYTHONHASHSEED": "1", "TZ": "UTC"}
import os  # noqa: E402

env = dict(os.environ)
env.update(ENV)
text = src_path.read_text(encoding="utf-8")
HARNESS = (ROOT / "audit" / "pyt" / "verify_pyt.py").read_text(encoding="utf-8")
HARNESS = HARNESS[HARNESS.index("HARNESS = '''") + len("HARNESS = '''"):]
HARNESS = HARNESS[:HARNESS.index("'''")].replace("\\\\n", "\\n")
n_fill = 0
# chương trình
for p in lib.PROGS:
    if p["lesson"] != lid or p["out"] != "@AUTO":
        continue
    with tempfile.TemporaryDirectory(prefix="pyt_") as d:
        for rel, content in p["files"].items():
            f = Path(d) / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(content.encode("utf-8"))
        Path(d, p["name"] + ".py").write_bytes((p["code"] + "\n").encode("utf-8"))
        r = subprocess.run([PYV, p["name"] + ".py"], cwd=d, env=env, capture_output=True, input=(p["stdin"] or "").encode("utf-8"), timeout=300)
    out = r.stdout.decode("utf-8", "replace").replace("\r\n", "\n").strip("\n")
    out = "\n".join(l.rstrip() for l in out.split("\n"))
    if r.returncode != 0 and p["expect"] == "run":
        print("CẢNH BÁO:", p["name"], "rc", r.returncode, r.stderr.decode("utf-8", "replace")[-300:])
    i = text.index('"@AUTO"')
    text = text[:i] + repr(out) + text[i + len('"@AUTO"'):]
    n_fill += 1
    print("điền", p["name"], "→", out[:70].replace("\n", " ⏎ "))
src_path.write_text(text, encoding="utf-8", newline="\n")
print("đã điền", n_fill, "chương trình. (Bước repl dùng '@AUTO' thì điền tay hoặc chạy verify để xem đầu ra thật.)")
