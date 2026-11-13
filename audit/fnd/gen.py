"""Sinh lessons/fnd/*.yaml từ audit/fnd/src/lXX.py. Dùng: .venv/Scripts/python audit/fnd/gen.py [L01 L02 …] (không đối số = tất cả).
Từ chối ghi bài có từ khoá tiếng Anh của Java trong lời đọc (lib.SAY_FORBIDDEN)."""
import importlib
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "fnd"))
sys.path.insert(0, str(ROOT / "audit" / "fnd" / "src"))
sys.stdout.reconfigure(encoding="utf-8")
import lib  # noqa: E402

want = [a.upper() for a in sys.argv[1:]] or sorted(p.stem.upper() for p in (ROOT / "audit/fnd/src").glob("l*.py"))
bad_total = 0
for lid in want:
    f = ROOT / "audit" / "fnd" / "src" / f"{lid.lower()}.py"
    if not f.exists():
        print("chưa có", f.name)
        continue
    lib.begin(lid)
    m = importlib.import_module(lid.lower())
    slug, spec = m.build()
    bad = lib.say_violations(spec)
    if bad:
        bad_total += len(bad)
        print(f"{lid}: TỪ CHỐI — từ khoá tiếng Anh trong lời đọc: {bad[:8]}")
        continue
    out = ROOT / "lessons" / "fnd" / f"{lid}_{slug}.yaml"
    if out.exists():  # giữ asr_reviewed đã có khi câu còn nguyên
        old = yaml.safe_load(out.read_text(encoding="utf-8"))
        keep = {x["sentence"]: x for x in old.get("asr_reviewed") or []}
        caps = {s for sc in spec["scenes"] for stp in sc["steps"] for s in re.split(r"(?<=[.!?])\s+", stp["say"])}
        spec["asr_reviewed"] = [x for s, x in keep.items() if s in caps]
    out.write_text(lib.dump(spec), encoding="utf-8", newline="\n")
    print("ghi", out.relative_to(ROOT))
sys.exit(1 if bad_total else 0)
