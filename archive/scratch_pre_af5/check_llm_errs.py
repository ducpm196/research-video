import io, sys
from contextlib import redirect_stdout
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv
sys.stdout.reconfigure(encoding="utf-8")

# First fix L12 yaml colon issue
l12 = ROOT / "lessons" / "llm" / "L12_sinh_co_truy_xuat.yaml"
t12 = l12.read_text(encoding="utf-8")
t12 = t12.replace("cả hai khâu hoạt động nhịp nhàng: khâu truy xuất", "cả hai khâu hoạt động nhịp nhàng, tức là khâu truy xuất")
l12.write_text(t12, encoding="utf-8", newline="\n")

for i in range(15):
    p = sorted((ROOT / "lessons" / "llm").glob(f"L{i:02d}_*.yaml"))[0]
    sp = lv.load_spec(p)
    with redirect_stdout(io.StringIO()):
        res = lv.lint(sp, quiet=True)
    if res.errors or res.warnings:
        print(f"=== L{i:02d} ===")
        for e in res.errors: print("  E:", e)
        for w in res.warnings: print("  W:", w)
