from pathlib import Path
import re, yaml

print("=== 1. Stage 10 lint summary ===")
import sys, io
from contextlib import redirect_stdout
sys.path.insert(0, "tools")
import lv
for c in ("toc", "plc", "par", "hci", "sep", "cas"):
    e = w = 0
    bad = []
    for p in sorted(Path("lessons", c).glob("L*.yaml")):
        sp = lv.load_spec(p)
        with redirect_stdout(io.StringIO()):
            r = lv.lint(sp, quiet=True)
        e += len(r.errors); w += len(r.warnings)
        if r.errors or r.warnings:
            bad.append((p.name, r.errors[:2], r.warnings[:2]))
    print(f"  {c.upper()}: FAIL={e}, WARN={w}", bad[:2])

print("\n=== 2. TOC P9 body ('Hai mức quy mô' or 'quy mô') check ===")
for p in sorted(Path("lessons/toc").glob("L*.yaml")):
    doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    body = " ".join((st.get("show") or "") for sc in doc["scenes"] if sc.get("kind") != "recap" for st in sc["steps"])
    has_q = "quy mô" in body.lower()
    print(f"  TOC {p.stem[:3]}: body_has_quymo={has_q}")

print("\n=== 3. HCI L08 SVG + L01 Phai-Duoi + recap terms ===")
p_hci8 = next(Path("lessons/hci").glob("L08_*.yaml"))
for i, ln in enumerate(p_hci8.read_text(encoding="utf-8").splitlines(), 1):
    if "<svg" in ln or "#0" in ln or "#2" in ln or "#1" in ln or "stroke=" in ln:
        if "svg" in ln or "intuition" in ln:
            print(f"  HCI L08:{i}: {ln.strip()[:220]}")
p_hci1 = next(Path("lessons/hci").glob("L01_*.yaml"))
for i, ln in enumerate(p_hci1.read_text(encoding="utf-8").splitlines(), 1):
    if "Phải" in ln:
        print(f"  HCI L01:{i}: {ln.strip()[:160]}")

print("\n=== 4. CAS L00/L05/L07 recap/check ===")
p_cas0 = next(Path("lessons/cas").glob("L00_*.yaml"))
for i, ln in enumerate(p_cas0.read_text(encoding="utf-8").splitlines(), 1):
    if "quay lui" in ln.lower():
        print(f"  CAS L00:{i}: {ln.strip()[:120]}")
p_cas7 = next(Path("lessons/cas").glob("L07_*.yaml"))
for i, ln in enumerate(p_cas7.read_text(encoding="utf-8").splitlines(), 1):
    if ".*.*" in ln or "Bài sau" in ln:
        print(f"  CAS L07:{i}: {ln.strip()[:160]}")

print("\n=== 5. Tight S10 lessons recap/say targets ===")
tight_list = [
    ("toc", ["L00", "L01", "L02", "L06", "L07", "L08", "L09", "L11"]),
    ("plc", ["L00", "L03", "L04", "L06", "L07", "L09", "L10", "L11", "L12"]),
    ("par", ["L12"]),
    ("hci", ["L11", "L12"]),
]
for c, lids in tight_list:
    for lid in lids:
        p = next(Path("lessons", c).glob(f"{lid}_*.yaml"))
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
        recap0 = next(sc["steps"][0] for sc in doc["scenes"] if sc["id"] == "recap")
        w = sum(len((s.get("say") or "").split()) for sc in doc["scenes"] for s in sc["steps"])
        print(f"  {c.upper()} {lid} ({w}w): recap0.focus={recap0.get('focus')} show_p={recap0['show'].count('<p')}")
