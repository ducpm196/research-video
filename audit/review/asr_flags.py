"""Liệt kê câu ASR gắn cờ CHƯA xem xét của một khoá, đọc từ out/<KHOÁ>/Lxx/asr_report.md (bảng chính, cột “đã xem xét” = —).
Mỗi dòng: bài, khung, độ khớp, câu, bản chép, khác biệt — đủ để viết lý do HAND (audit/dms/asr_review_dms.py) hoặc
quyết định viết lại câu (câu ≤ 7 từ có độ khớp < 0,7 → viết dài ra rồi dựng lại; xem references/new-domain.md §6).
Báo cáo phải được sinh lại (`lv.py asr`) sau khi thêm asr_reviewed, nếu không câu đã xem xét vẫn hiện “—”.
Chạy: .venv/Scripts/python audit/review/asr_flags.py <KHOÁ> [Lxx ...]"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from vi_text import normalize  # noqa: E402  số → chữ trước khi so độ dài (ASR viết “15,71” cho “15 phẩy 71”)
sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")
C, only = sys.argv[1].upper(), set(sys.argv[2:])
n = 0
for d in sorted((ROOT / "out" / C).glob("L*")):
    f = d / "asr_report.md"
    if not f.exists() or (only and d.name not in only):
        continue
    for line in f.read_text(encoding="utf-8").split("## Tham khảo")[0].splitlines():
        p = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(p) == 8 and p[0].isdigit() and p[7] in ("—", ""):
            n += 1
            short = " ⚠ NGẮN" if len(p[2].split()) <= 7 and float(p[1]) < 0.7 else ""
            # bản chép ngắn hẳn câu → nghi ÂM THANH CỤT (lỗi thật AIF L08, CSA L11, DBS L15): không viết lý do, chạy tts_speed_scan
            if len(normalize(p[3]).split()) < 0.7 * len(normalize(p[2]).split()):
                short += " ⚠ THIẾU (nghi âm thanh cụt)"
            print(f"{d.name}\t{p[0]}\t{p[1]}{short}\t{p[2]}\t=> {p[3]}\t[{p[4]}]")
print(f"{C}: {n} câu chưa xem xét", file=sys.stderr)
