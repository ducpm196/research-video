import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, "tools")
import lv  # noqa: E402

watch = {
    "ESY:L03", "ROB:L00", "ROB:L02", "GFX:L06", "GFX:L13",
    "BCH:L00", "BCH:L01", "BCH:L02", "BCH:L04", "BCH:L08", "BCH:L11",
}
err = warn = 0
for c in ("rbm", "esy", "rob", "gfx", "bch"):
    for p in sorted(Path("lessons", c).glob("L*.yaml")):
        sp = lv.load_spec(p)
        with redirect_stdout(io.StringIO()):
            r = lv.lint(sp, quiet=True)
        w = sum(len((s.get("say") or "").split()) for sc in sp["scenes"] for s in sc["steps"])
        err += len(r.errors)
        warn += len(r.warnings)
        k = f"{c.upper()}:{sp['id']}"
        if k in watch or r.errors or r.warnings:
            print(f"{k}: words={w} FAIL={len(r.errors)} WARN={len(r.warnings)}", r.errors[:2], r.warnings[:2])
print(f"TOTAL Stage 11 (75 lessons): FAIL={err}, WARN={warn}")
assert err == 0 and warn == 0
