"""Chạy lại ASR cho mọi bài đã dựng (có <id>.mp4) mà thiếu asr_report.md — ví dụ khi bước asr của hàng đợi dựng hỏng vì thiếu bộ nhớ.
Chỉ đọc lại âm thanh đã có (lv.py asr), không dựng lại video. Chạy tuần tự, mỗi bài một tiến trình.
Chạy: .venv/Scripts/python audit/review/asr_catchup.py [KHOÁ …]  (bỏ trống = mọi khoá)"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")
want = {c.upper() for c in sys.argv[1:]}
todo = []
for cdir in sorted((ROOT / "out").iterdir()):
    if not cdir.is_dir() or cdir.name.startswith("_") or (want and cdir.name not in want):
        continue
    for ldir in sorted(cdir.iterdir()):
        if (ldir / f"{ldir.name}.mp4").exists() and not (ldir / "asr_report.md").exists():
            spec = next((ROOT / "lessons" / cdir.name.lower()).glob(f"{ldir.name}_*.yaml"), None)
            if spec:
                todo.append((cdir.name, ldir.name, spec))
print(f"thiếu asr_report: {len(todo)} bài", [f"{c} {l}" for c, l, _ in todo])
for c, l, spec in todo:
    r = subprocess.run([sys.executable, "tools/lv.py", "asr", str(spec.relative_to(ROOT))], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    tail = (r.stdout.strip().splitlines() or [""])[-1]
    print(c, l, "→", "OK" if (ROOT / "out" / c / l / "asr_report.md").exists() else "VẪN THIẾU", "|", tail[:160])
