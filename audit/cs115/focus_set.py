"""Thay `focus` của một step đã có: focus_set.py L02 singular.1 '["1.3", "1.3", 2, 2]' — tìm dòng `focus:` trong step
(từ dòng `say:` của step lùi lên tới đầu step), thay, đọc lại bài và so."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

COURSE = __import__("os").environ.get("LV_COURSE", "cs115")  # khoá: LV_COURSE=cs112

lid, key, val = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
p = next((ROOT / "lessons" / COURSE).glob(lid + "_*.yaml"))
sp = lv.load_spec(p)
keys = [f"{sc['id']}.{ki}" for sc in sp["scenes"] for ki, _ in enumerate(sc["steps"])]
st = {f"{sc['id']}.{ki}": s for sc in sp["scenes"] for ki, s in enumerate(sc["steps"])}[key]
assert len(val) == len(lv.sentences(st["say"])), "số mục ≠ số câu"
lines = p.read_text(encoding="utf-8").split("\n")
says = [i for i, ln in enumerate(lines) if ln.startswith("        say:")]
i = says[keys.index(key)]
while not lines[i].startswith("        focus:"):
    i -= 1
    assert not lines[i].startswith("      - "), "step không có focus"
old = lines[i]
lines[i] = "        focus: " + json.dumps(val, ensure_ascii=False)
p.write_text("\n".join(lines), encoding="utf-8")
got = {f"{sc['id']}.{ki}": s.get("focus") for sc in lv.load_spec(p)["scenes"] for ki, s in enumerate(sc["steps"])}
assert got[key] == val, got[key]
print(f"{lid} {key}: {old.strip()} → focus: {val}")
