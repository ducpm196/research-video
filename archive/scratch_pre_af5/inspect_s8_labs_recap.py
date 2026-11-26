from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

# Print relevant labs/*/de.md & loi_giai.py
for rel in [
    "labs/mlo/L01/de.md", "labs/mlo/L06/de.md", "labs/mlo/L09/de.md", "labs/mlo/L10/de.md", "labs/mlo/L14/de.md",
    "labs/evt/L00/de.md", "labs/evt/L05/de.md", "labs/evt/L09/de.md",
    "labs/dsc/L01/de.md", "labs/dsc/L15/de.md",
    "labs/dsc/L00/loi_giai.py", "labs/dsc/L00/de.md",
]:
    p = ROOT / rel
    print(f"=== {rel} ===")
    print(p.read_text("utf-8").strip())

# Check DEN recap#1 & hook#0
p_den = sorted((ROOT / "lessons/den").glob("L*.yaml"))
for p in p_den[:2]:
    d = yaml.safe_load(p.read_text("utf-8"))
    print(f"\n=== DEN {d['id']} hook#0 & recap#1 ===")
    print("hook#0 show:", repr(d["scenes"][0]["steps"][0]["show"][-120:]))
    rec = [s for s in d["scenes"] if s["id"] == "recap"][0]
    print("recap#1 show:", repr(rec["steps"][1]["show"]))
    print("recap#1 focus:", rec["steps"][1].get("focus"))
    print("recap#1 say:", repr(rec["steps"][1]["say"]))

# Check recap#1 of CLC L12, CLD L15, EVT L11, DSC L08, DSC L10
for rel in [
    "lessons/clc/L12_hanh_trinh_luu_tru_doi_tuong.yaml",
    "lessons/cld/L15_hanh_trinh_borg_kubernetes.yaml",
    "lessons/evt/L11_hanh_trinh_nhat_ky_su_kien.yaml",
    "lessons/dsc/L08_thu_nghiem_ab.yaml",
    "lessons/dsc/L10_ro_ri_du_lieu.yaml",
]:
    d = yaml.safe_load((ROOT / rel).read_text("utf-8"))
    rec = [s for s in d["scenes"] if s["id"] == "recap"][0]
    print(f"\n=== {rel} recap#1 ===")
    print("show:", repr(rec["steps"][1]["show"]))
    print("focus:", rec["steps"][1].get("focus"))
    print("say:", repr(rec["steps"][1]["say"]))
