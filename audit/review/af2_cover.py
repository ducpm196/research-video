"""G-COVER (AF3, 2026-11-13): độ phủ chuẩn AF2 theo chặng học. Đếm bài `af2: true`, bài có cảnh `practice` và thư mục lab chạy được.
Dùng: python audit/review/af2_cover.py [--require S01 S02 …]  → in bảng; mã thoát 1 nếu chặng bắt buộc chưa phủ 100%.
Chặng lấy từ STAGES của audit/review/learn_start/pack.py (khoá của mỗi chặng = phần trước dấu “:” của mục tiêu)."""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review" / "learn_start"))
sys.stdout.reconfigure(encoding="utf-8")
import pack  # noqa: E402


def lessons_of(course):
    cur = yaml.safe_load((ROOT / "curriculum" / f"{course.lower()}.yaml").read_text(encoding="utf-8"))
    return [l for l in cur.get("lessons") or [] if l.get("spec")]


def main():
    req = []
    if "--require" in sys.argv:
        req = sys.argv[sys.argv.index("--require") + 1:]
    bad = 0
    cur = pack.load_cur()
    print(f"{'chặng':<6}{'khoá':<26}{'bài':>5}{'af2':>5}{'practice':>9}{'lab':>5}   phủ")
    for sid, name, _lv, _intro, items in pack.stages(cur):
        courses = []
        tot = af2 = pr = lab = 0
        for c, l in items:
            if c not in courses:
                courses.append(c)
            if not l.get("spec"):
                continue
            tot += 1
            t = (ROOT / l["spec"]).read_text(encoding="utf-8")
            af2 += bool(re.search(r"^af2:\s*true", t, re.M))
            has_pr = bool(re.search(r"kind:\s*practice", t))
            pr += has_pr
            m = re.search(r"lab:\s*(labs/\S+)", t)
            lab += bool(m and (ROOT / m.group(1).strip("'\"")).is_dir())
        pct = 100.0 * min(af2, pr, lab) / tot if tot else 0
        flag = ""
        if sid in req and min(af2, pr, lab) < tot:
            flag = "  ← FAIL (bắt buộc 100%)"
            bad += 1
        print(f"{sid:<6}{'+'.join(courses)[:25]:<26}{tot:>5}{af2:>5}{pr:>9}{lab:>5}   {pct:5.1f}%{flag}")
    print(f"af2_cover: {bad} chặng bắt buộc chưa phủ")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
