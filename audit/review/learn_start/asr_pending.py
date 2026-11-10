"""Liệt kê câu ASR gắn cờ CHƯA xem xét của các bài đã dựng lại trong đợt LS1 (đọc rebuild.done, rồi asr_report.md từng bài).
Dùng: .venv/Scripts/python -B audit/review/learn_start/asr_pending.py
Cột "đã xem xét" = "—" trong bảng đầu của asr_report.md là chưa xem xét (cùng quy ước audit/dms/asr_review_dms.py)."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.stdout.reconfigure(encoding="utf-8")
done = [l.split()[:2] for l in (ROOT / "audit/review/learn_start/rebuild.done").read_text(encoding="utf-8").splitlines() if l.strip()]
tot = 0
for c, i in done:
    md = ROOT / "out" / c / i / "asr_report.md"
    if not md.exists():
        print(f"{c} {i}: THIẾU asr_report.md"); tot += 1; continue
    t = md.read_text(encoding="utf-8")
    m = re.search(r"chưa xem xét: (\d+)", t)
    n = int(m.group(1)) if m else -1
    if n:
        tot += 1
        print(f"== {c} {i}: chưa xem xét {n}")
        body = t.split("## ")[0]
        for row in body.splitlines():
            if re.match(r"^\| \d+ \|", row) and row.rstrip().endswith("| — |"):
                cells = [x.strip() for x in row.strip("|").split("|")]
                print(f"   khung {cells[0]} ({cells[1]}): {cells[2][:150]}\n      nghe: {cells[3][:150]}\n      khác: {cells[4][:160]}")
print(f"# {len(done)} bài đã dựng; bài còn câu chưa xem xét: {tot}")
