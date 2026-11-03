"""Liệt kê khung cần xem bằng mắt theo SKILL Bước 6: khung đầu, khung cuối mỗi phân cảnh có SVG/bảng/khối mã, khung cuối của
formula/example, một khung pitfall, khung cuối bài. Chạy: .venv/Scripts/python audit/cs112/frames_to_check.py L05 L06 …
Khoá khác CS112: ghi “DMS/L00” (thư mục lessons/<khoá viết thường>)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

for arg in sys.argv[1:]:
    course, _, lid = arg.rpartition("/")
    p = next((ROOT / "lessons" / (course or "CS112").lower()).glob(lid + "_*.yaml"))
    sp = lv.load_spec(p)
    i, picks = 0, {0}
    for sc in sp["scenes"]:
        start = i
        for st in sc["steps"]:
            n = len(lv.sentences(st["say"]))
            show = str(st.get("show", ""))
            if "<svg" in show or "<table" in show or 'class="code"' in show:
                picks.add(i + n - 1)
            i += n
        if sc["kind"] in ("formula", "example", "pitfall"):
            picks.add(i - 1)
    picks.add(i - 1)
    print(arg, sorted(picks))
