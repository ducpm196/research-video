from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
ITEMS = [
    ("lessons/dan/L02_noi_nhan_dong.yaml", ["prereq", "sym"]),
    ("lessons/dan/L03_ham_cua_so.yaml", ["example", "check"]),
    ("lessons/dan/L12_hanh_trinh_thu_nghiem_ab.yaml", ["prereq", "sym"]),
    ("lessons/dan/L07_du_bao_co_so.yaml", ["example", "check"]),
    ("lessons/dan/L11_bang_dieu_khien.yaml", ["example", "check"]),
    ("lessons/dsc/L03_du_lieu_thieu.yaml", ["example", "check"]),
    ("lessons/dsc/L12_dien_giai_hoi_quy.yaml", ["example"]),
    ("lessons/mlo/L08_giam_sat_troi.yaml", ["example", "check"]),
    ("lessons/dsc/L08_thu_nghiem_ab.yaml", ["recap"]),
    ("lessons/dsc/L13_rieng_tu_dao_duc.yaml", ["check", "recap"]),
]
for rel, sids in ITEMS:
    d = yaml.safe_load((ROOT / rel).read_text("utf-8"))
    print(f"=== {rel} ===")
    for sid in sids:
        sc = next(s for s in d["scenes"] if s["id"] == sid)
        for i, st in enumerate(sc["steps"]):
            if sid != "example" or i >= len(sc["steps"]) - 2:
                print(f"  {sid}[{i}] focus={st.get('focus')} show_tail={st['show'][-150:]!r} say={st['say'][-180:]!r}")
