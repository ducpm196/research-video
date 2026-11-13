"""G-ORDER (plan AF2): lời hẹn "Bài sau (bài N)" phải trỏ tới bài đứng SAU bài hiện tại trong dãy học thật của HOC_TAP (audit/review/learn_start/pack.py),
và nếu có bài đứng ngay sau trong cùng khoá thì N phải là chính bài đó (người học xem ngay bài kế tiếp).
Lỗi thật đã biết: CLC L11 hẹn L12 trong khi dãy học đặt L12 trước.
Dùng: .venv/Scripts/python -B audit/review/check_next_refs.py   — in từng vi phạm và một dòng tổng; mã thoát 1 nếu có."""
import re
import sys
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review" / "learn_start"))
import pack  # noqa: E402

cur = pack.load_cur()
seq = [(C, l["id"]) for _, _, _, _, items in pack.stages(cur) for C, l in items]
pos = {f"{C}:{i}": n for n, (C, i) in enumerate(seq)}
nxt_same = {}
for n, (C, i) in enumerate(seq):
    for C2, i2 in seq[n + 1:]:
        if C2 == C:
            nxt_same[f"{C}:{i}"] = i2
            break
REF = re.compile(r"[Bb]ài sau \(bài (\d+)\)")
bad = tot = 0
for C, c in cur.items():
    for l in c["lessons"]:
        spec = l.get("spec")
        if not spec or not (ROOT / spec).exists():
            continue
        text = (ROOT / spec).read_text(encoding="utf-8")
        for m in REF.finditer(text):
            tot += 1
            ref = f"{C}:L{int(m.group(1)):02d}"
            me = f"{C}:{l['id']}"
            if ref not in pos:
                print(f"FAIL {me}: hẹn bài {m.group(1)} không có trong khoá")
                bad += 1
            elif pos[ref] <= pos[me]:
                print(f"FAIL {me}: hẹn {ref} nhưng dãy học đặt {ref} TRƯỚC bài này")
                bad += 1
            elif nxt_same.get(me) and nxt_same[me] != f"L{int(m.group(1)):02d}":
                print(f"FAIL {me}: hẹn {ref} nhưng bài kế tiếp trong khoá theo dãy học là {nxt_same[me]}")
                bad += 1
print(f"check_next_refs: {tot} lời hẹn, {bad} lệch dãy học")
sys.exit(1 if bad else 0)
