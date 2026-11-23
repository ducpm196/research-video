"""AF5 — lint MỘT bài (dò bài làm phình RAM). Chỉ đọc. Chạy: python -B lint_one.py lessons/<khoá>/<bài>.yaml"""
import io, pathlib, sys, time
from contextlib import redirect_stdout
ROOT = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402
t = time.time()
with redirect_stdout(io.StringIO()):
    r = lv.lint(lv.load_spec(ROOT / sys.argv[1]), quiet=True)
print(f"LINT1 {sys.argv[1]}: {len(r.errors)} FAIL, {len(r.warnings)} WARN, {time.time()-t:.1f}s")
for x in r.errors + r.warnings: print("  ", x[:250])
