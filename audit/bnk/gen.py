"""Sinh lessons/bnk/*.yaml từ audit/bnk/src/lXX.py. Dùng: .venv/Scripts/python audit/bnk/gen.py [L01 L02 …] (không đối số = tất cả)."""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "bnk"))
sys.path.insert(0, str(ROOT / "audit" / "bnk" / "src"))
sys.stdout.reconfigure(encoding="utf-8")
import lib  # noqa: E402

want = [a.upper() for a in sys.argv[1:]] or [f"L{i:02d}" for i in range(0, 15)]
for lid in want:
    f = ROOT / "audit" / "bnk" / "src" / f"{lid.lower()}.py"
    if not f.exists():
        print("chưa có", f.name)
        continue
    m = importlib.import_module(lid.lower())
    slug, spec = m.build()
    out = ROOT / "lessons" / "bnk" / f"{lid}_{slug}.yaml"
    # giữ asr_reviewed đã có (xem xét ASR ghi thẳng vào YAML) khi sinh lại
    if out.exists():
        import yaml
        old = yaml.safe_load(out.read_text(encoding="utf-8"))
        keep = {x["sentence"]: x for x in old.get("asr_reviewed") or []}
        caps = {s for sc in spec["scenes"] for stp in sc["steps"] for s in
                __import__("re").split(r"(?<=[.!?])\s+", stp["say"])}
        spec["asr_reviewed"] = [x for s, x in keep.items() if s in caps]
    out.write_text(lib.dump(spec), encoding="utf-8", newline="\n")
    print("ghi", out.relative_to(ROOT))
