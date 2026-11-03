"""Chèn `focus:` vào bài CS115 theo audit/cs115/focus_plan/Lxx.yaml ({"cảnh.step": [mục mỗi câu]}): dòng focus đặt
ngay trước dòng `say:` của step (step thứ k trong bài = dòng `say:` thứ k), rồi đọc lại bài và so focus từng step.
Không ghi đè focus đã có. Chạy: focus_apply.py L01 [L02 …]"""
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

COURSE = __import__("os").environ.get("LV_COURSE", "cs115")  # khoá: LV_COURSE=cs112

for lid in sys.argv[1:]:
    p = next((ROOT / "lessons" / COURSE).glob(lid + "_*.yaml"))
    plan = yaml.safe_load((ROOT / "audit" / COURSE / "focus_plan" / f"{lid}.yaml").read_text(encoding="utf-8")) or {}
    sp = lv.load_spec(p)
    keys = [f"{sc['id']}.{ki}" for sc in sp["scenes"] for ki, _ in enumerate(sc["steps"])]
    steps = {f"{sc['id']}.{ki}": st for sc in sp["scenes"] for ki, st in enumerate(sc["steps"])}
    bad = [k for k in plan if k not in steps]
    assert not bad, f"{lid}: step không có trong bài {bad}"
    for k, v in plan.items():
        assert steps[k].get("focus") is None, f"{lid} {k}: đã có focus {steps[k]['focus']}"
        n = len(lv.sentences(steps[k]["say"]))
        assert len(v) == n, f"{lid} {k}: plan {len(v)} mục, bài {n} câu"
    lines = p.read_text(encoding="utf-8").split("\n")
    says = [i for i, ln in enumerate(lines) if ln.startswith("        say:")]
    assert len(says) == len(keys), f"{lid}: {len(says)} dòng say, {len(keys)} step"
    for idx in sorted((keys.index(k) for k in plan), reverse=True):
        lines.insert(says[idx], "        focus: " + json.dumps(plan[keys[idx]], ensure_ascii=False).replace(",", ", ").replace(",  ", ", "))
    p.write_text("\n".join(lines), encoding="utf-8")
    sp2 = lv.load_spec(p)
    got = {f"{sc['id']}.{ki}": st.get("focus") for sc in sp2["scenes"] for ki, st in enumerate(sc["steps"])}
    for k in keys:
        want = plan.get(k, steps[k].get("focus"))
        assert got[k] == want, f"{lid} {k}: đọc lại {got[k]} ≠ {want}"
    print(f"{lid}: chèn {len(plan)} focus, đọc lại khớp")
