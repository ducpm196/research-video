"""Chỉ ra các chuỗi khung LIỀN NHAU chỉ có chữ (không bảng, hình, chuỗi, công thức hiển thị, mã) — cảnh báo E39 “khung liền chỉ có chữ”.
Dùng cùng quy tắc của lv.lint_depth (kể cả hộp `box` được tính là trực quan với hồ sơ có visual: any).
Chạy: .venv/Scripts/python audit/review/text_runs.py lessons/<khoá>/<bài>.yaml [...]"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

for f in sys.argv[1:]:
    spec = lv.load_spec(f)
    dp = lv.profile_of(spec).get("depth") or {}
    vis = re.compile(lv.VISUAL_RE.pattern + (r"|class=[\"']box" if dp.get("visual") == "any" else ""))
    run, runs = [], []
    for si, sc, ki, st in lv.iter_steps(spec):
        show = str(st.get("show", "") or "")
        if not show.strip() or vis.search(show):
            if len(run) > lv.DEPTH_MAX_TEXT_RUN:
                runs.append(run)
            run = []
        else:
            run.append(f"{sc.get('id')}.{ki}")
    if len(run) > lv.DEPTH_MAX_TEXT_RUN:
        runs.append(run)
    print(Path(f).name, "→", runs or "không có chuỗi nào quá", lv.DEPTH_MAX_TEXT_RUN, "khung chữ")
