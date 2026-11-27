"""So bộ đọc YAML thuần của lv.py với CSafeLoader trên MỌI tệp YAML của kho + ca biên. Dùng từ gốc kho:
.venv/Scripts/python -B audit/perf/fast_pipeline_20261126/yaml_eq.py"""

import sys, time, datetime, math
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode=True
import ctypes
def _idle():  # ưu tiên thấp nhất của Windows (tiến trình con thừa hưởng) để không giành CPU với hàng dựng đang chạy
    k = ctypes.windll.kernel32; k.GetCurrentProcess.restype = ctypes.c_void_p
    k.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]; k.SetPriorityClass(k.GetCurrentProcess(), 0x40)
_idle()
from pathlib import Path as _P; sys.path.insert(0, str(_P(__file__).resolve().parents[3] / "tools"))
import yaml, lv_fast, lv
from pathlib import Path
R = Path(__file__).resolve().parents[3]
pure = lv._StrictLoader; C = lv_fast._CStrictLoader
def canon(o):
    if isinstance(o, dict): return ("dict", tuple((canon(k), canon(v)) for k, v in o.items()))   # giữ cả THỨ TỰ khoá
    if isinstance(o, (list, tuple)): return (type(o).__name__, tuple(canon(x) for x in o))
    if isinstance(o, set): return ("set", tuple(sorted(map(repr, o))))
    if isinstance(o, float) and math.isnan(o): return ("nan",)
    return (type(o).__name__, o)
def load(text, L):
    try: return ("ok", canon(yaml.load(text, Loader=L)))
    except Exception as e: return ("err", type(e).__name__)
skip = {".venv", ".venv-tts", "node_modules", "deps", ".git", "__pycache__", "out"}
files = [p for ext in ("*.yaml", "*.yml") for p in R.rglob(ext) if not (set(p.relative_to(R).parts) & skip)]
t0 = time.time(); same = diff = both_err = 0; bad = []; tp = tc = 0.0
for p in files:
    txt = p.read_text(encoding="utf-8-sig") if False else open(p, encoding="utf-8").read()
    a = time.perf_counter(); x = load(txt, pure); b = time.perf_counter(); y = load(txt, C); c = time.perf_counter()
    tp += b - a; tc += c - b
    if x == y: same += 1; both_err += x[0] == "err"
    else: diff += 1; bad.append((str(p.relative_to(R)), x[0], x[1] if x[0]=="err" else "", y[0], y[1] if y[0]=="err" else ""))
print(f"files {len(files)} | giống {same} (trong đó cả hai cùng lỗi {both_err}) | khác {diff} | pure {tp:.1f}s, C {tc:.1f}s")
for r in bad[:30]: print("  KHÁC", r)
# phủ theo thư mục
from collections import Counter
print(Counter(p.relative_to(R).parts[0] for p in files))
# ca biên: phải giống nhau
cases = {
 "dup_key": "a: 1\nb: 2\na: 3\n",
 "dup_key_nested": "x:\n  - {k: 1, k: 2}\n",
 "bool_like": "a: on\nb: off\nc: yes\nd: no\ne: Null\nf: ~\ng: 'on'\n",
 "numbers": "a: 012\nb: 0x1F\nc: 1_000\nd: 1e3\ne: 1.0e+3\nf: .5\ng: -.inf\nh: 12:30\n",
 "dates": "a: 2026-11-26\nb: 2026-11-26 14:00:00\n",
 "block": "a: |\n  dòng 1\n\n  dòng 2\nb: >-\n  gấp\n  dòng\n",
 "unicode": "k: 'Đường — “trích” … 𝔸'\n",
 "anchors_merge": "base: &b {x: 1, y: 2}\nc:\n  <<: *b\n  y: 3\n",
 "tab_indent": "a:\n\tb: 1\n",
 "tab_after_colon": "a:\tb\n",
 "bad": "a: [1, 2\n",
 "latex": "s: '$\\\\frac{1}{2}$'\nt: \"a\\\\n\"\n",
}
for n, s in cases.items():
    x = load(s, pure); y = load(s, C)
    print(f"ca {n:16s} {'GIỐNG' if x==y else 'KHÁC'}: pure={x[0]} {x[1] if x[0]=='err' else ''} | C={y[0]} {y[1] if y[0]=='err' else ''}")
# đường load_yaml thật của lv_fast: lỗi khoá trùng phải nổi lên với đúng thông điệp lv
import tempfile, os
d = tempfile.mkdtemp(); f = os.path.join(d, "dup.yaml"); open(f, "w", encoding="utf-8").write("a: 1\na: 2\n")
for name, fn in (("lv gốc", lv_fast._orig_load_yaml), ("lv_fast", lv.load_yaml)):
    try: fn(f); print(name, "KHÔNG báo lỗi khoá trùng")
    except Exception as e: print(name, "→", type(e).__name__, str(e).splitlines()[0])
print("tổng s", round(time.time()-t0))
