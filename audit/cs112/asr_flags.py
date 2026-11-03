"""Gom mọi câu ASR gắn cờ CHƯA xem xét của các bài CS112 (đọc out/CS112/<id>/asr_report.md, bảng đầu tiên).
Chạy: .venv/Scripts/python audit/cs112/asr_flags.py [L01 L02 …]  → in: bài | khung | độ khớp | câu | nghe được | từ rủi ro."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")
COURSE = __import__("os").environ.get("LV_OUT", "CS112")
ids = sys.argv[1:] or sorted(p.name for p in (ROOT / "out" / COURSE).glob("L??"))
for lid in ids:
    rep = ROOT / "out" / COURSE / lid / "asr_report.md"
    if not rep.exists():
        print(f"{lid}: CHƯA có asr_report"); continue
    rows = []
    for line in rep.read_text(encoding="utf-8").split("## Tham khảo")[0].splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 8 and c[0].isdigit() and c[7] == "—":
            rows.append(c)
    for c in rows:
        print(f"{lid}\t{c[0]}\t{c[1]}\t{c[2]}\t=> {c[3]}\t[{c[5]}]")
