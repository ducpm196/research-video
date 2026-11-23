"""AF5 — lint mọi bài của MỘT khoá trong một tiến trình riêng (tránh phình RAM như audit_all.py). Chỉ đọc.
Chạy: .venv/Scripts/python -B audit/review/audit_final/logs/af5/lint_course.py <khoá>   → in dòng lỗi + dòng tổng."""
import io, pathlib, sys
from contextlib import redirect_stdout
ROOT = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402
c = sys.argv[1].lower()
n = fe = fw = 0
for f in sorted((ROOT / "lessons" / c).glob("L*_*.yaml")):
    with redirect_stdout(io.StringIO()):
        r = lv.lint(lv.load_spec(f), quiet=True)
    n += 1; fe += len(r.errors); fw += len(r.warnings)
    for x in r.errors + r.warnings:
        print(f"{c.upper()} {f.name[:3]} {x}"[:300])
print(f"LINT {c.upper()}: {n} bài, {fe} FAIL, {fw} WARN")
