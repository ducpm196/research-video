"""Đối chứng âm cho `checks` của bài CS112: với mỗi check, đổi số nguyên/thập phân đứng ngay sau dấu `==` CUỐI CÙNG
(cộng thêm 1) rồi chạy lại — kết quả phải KHÔNG còn là True. Check nào vẫn True sau khi đổi số là check không kiểm gì
(production.md: lỗi thật L10 “so hai hằng số chép tay”). Check không có `==` số ở cuối được liệt kê là “không đổi được”
để người soạn tự xem (đa số là check bất đẳng thức/all(...) — đã có đối chứng riêng trong bài).
Chạy: .venv/Scripts/python audit/cs112/mutate_checks.py lessons/cs112/L00_*.yaml ..."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

NUM_AFTER_EQ = re.compile(r"==\s*(-?\d+(?:\.\d+)?)(?![\d.])(?!.*==)")
bad = 0
for path in sys.argv[1:]:
    spec = lv.load_spec(path)
    ns = lv._check_namespace()
    n_mut = n_skip = 0
    for sc in spec["scenes"]:
        for ci, expr in enumerate(sc.get("checks") or []):
            m = NUM_AFTER_EQ.search(expr)
            if not m:
                n_skip += 1
                continue
            v = m.group(1)
            nv = str(float(v) + 1) if "." in v else str(int(v) + 1)
            mutated = expr[:m.start(1)] + nv + expr[m.end(1):]
            try:
                res = eval(mutated, dict(ns))
            except Exception:
                res = "lỗi"
            n_mut += 1
            if str(res) == "True":
                bad += 1
                print(f"[FAIL] {Path(path).name} {sc['id']}#{ci}: vẫn True sau khi đổi {v} → {nv}: {expr[:90]}")
    print(f"{Path(path).name}: {n_mut} check bị đổi số đều ra khác True; {n_skip} check không có số sau == cuối (xem tay)")
print(f"mutate: {bad} FAIL")
sys.exit(1 if bad else 0)
