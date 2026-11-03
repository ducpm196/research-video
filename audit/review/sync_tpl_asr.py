"""Chép khối `asr_reviewed` từ tệp mẫu audit/<khoá>/src/<id>_*.tpl.yaml sang bài sinh ra lessons/<khoá>/<id>_*.yaml mà KHÔNG sinh lại hình
(fill_all có thể đổi byte của SVG và làm video thành cũ). Kiểm spec_digest trước và sau phải giống nhau (asr_reviewed không vào digest).
Chạy: .venv/Scripts/python audit/review/sync_tpl_asr.py DBS L08 L12 …"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

course, ids = sys.argv[1].upper(), sys.argv[2:]
pat = re.compile(r"\nasr_reviewed:(?: \[\])?\n((?:  - .*\n)*)")
for lid in ids:
    tpl = next((ROOT / "audit" / course.lower() / "src").glob(f"{lid}_*.tpl.yaml"), None)
    if tpl is None:  # bài không sinh từ mẫu: asr_review_dms đã ghi thẳng vào bài
        continue
    les = next((ROOT / "lessons" / course.lower()).glob(f"{lid}_*.yaml"))
    block = pat.search(tpl.read_text(encoding="utf-8")).group(1)
    text = les.read_text(encoding="utf-8")
    d0 = lv.spec_digest(lv.load_spec(les))
    m = pat.search(text)
    new = text[:m.start()] + "\nasr_reviewed:" + ("\n" + block if block else " []\n") + text[m.end():]
    les.write_text(new, encoding="utf-8")
    d1 = lv.spec_digest(lv.load_spec(les))
    if d0 != d1:
        les.write_text(text, encoding="utf-8")
        print(lid, "KHÔNG GHI: digest đổi — hoàn tác")
    else:
        print(lid, "đã chép", block.count("\n  - ") + (1 if block.startswith("  - ") else 0), "mục, digest giữ nguyên")
