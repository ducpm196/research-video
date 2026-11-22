from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

for rel in [
    "lessons/dsc/L00_quy_trinh.yaml",
    "lessons/dsc/L03_du_lieu_thieu.yaml",
    "lessons/dsc/L13_rieng_tu_dao_duc.yaml",
    "lessons/clc/L00_dam_may_la_gi.yaml",
    "lessons/clc/L02_mang_ao.yaml",
    "lessons/dan/L02_noi_nhan_dong.yaml",
    "lessons/dan/L03_ham_cua_so.yaml",
    "lessons/den/L10_hop_thu_di.yaml",
    "lessons/den/L12_kho_du_lieu.yaml",
    "lessons/sar/L05_phan_manh.yaml",
    "lessons/sar/L09_luy_dang.yaml",
    "lessons/sar/L11_kien_truc_an_toan.yaml",
]:
    d = yaml.safe_load((ROOT / rel).read_text("utf-8"))
    print(f"=== {rel} ===")
    for s in d["scenes"]:
        if s["id"] == "practice":
            for i, st in enumerate(s["steps"]):
                if "viết trong mã" in str(st.get("show", "")) or "Lời giải" in str(st.get("show", "")):
                    print(f"  practice[{i}]: {st['show'][:260]}")
        if rel.endswith(("L03_du_lieu_thieu.yaml", "L13_rieng_tu_dao_duc.yaml")) and s["id"] in ("check", "recap"):
            for i, st in enumerate(s["steps"]):
                print(f"  {s['id']}[{i}] focus={st.get('focus')} show={st['show']!r} say={st['say']!r}")
        if rel.endswith("L00_dam_may_la_gi.yaml") and s["id"] == "recap":
            print(f"  recap[1]: {s['steps'][1]['show']!r}")

print("\n=== DEN hook#0 focus check ===")
for p in sorted((ROOT / "lessons/den").glob("L*.yaml")):
    d = yaml.safe_load(p.read_text("utf-8"))
    st0 = d["scenes"][0]["steps"][0]
    rec1 = [s for s in d["scenes"] if s["id"] == "recap"][0]["steps"][1]
    print(p.name, "hook#0 focus=", st0.get("focus"), "| recap#1 focus=", rec1.get("focus"))
