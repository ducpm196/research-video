from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import lv

TARGETS = [
    ("lessons/llm/L01_ngram_do_hon_loan.yaml", "check"),
    ("lessons/rln/L00_loi_nhuan_chiet_khau.yaml", "check"),
    ("lessons/rln/L11_khai_thac_phan_thuong.yaml", "check"),
    ("lessons/cvi/L00_anh_so.yaml", "formula"),
    ("lessons/cvi/L06_do_sau_hai_camera.yaml", "check"),
    ("lessons/aif/L13_tong_hop.yaml", "example"),
    ("lessons/llm/L05_chuyen_gia_thua.yaml", "sym"),
]
for rel, sid in TARGETS:
    p = ROOT / rel
    if not p.exists():
        p = sorted((ROOT / p.parent).glob(p.name[:4] + "*.yaml"))[0]
    d = yaml.safe_load(p.read_text("utf-8"))
    sc = next(s for s in d["scenes"] if s["id"] == sid)
    st = sc["steps"][-1]
    if sid == "sym":
        st = sc["steps"][0]
    print(f"=== {p.name} {sid} len_u={len(lv.html_units(st['show']))} n_s={len(lv.sentences(st['say']))} focus={st.get('focus')} ===")
    print("  show:", repr(st["show"][-160:]))
    print("  say:", repr(st["say"][-160:]))
