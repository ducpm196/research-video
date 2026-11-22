import yaml
targets = [
    ("lessons/aif/L14_hanh_trinh_may_choi_co.yaml", "stage5"),
    ("lessons/llm/L01_ngram_do_hon_loan.yaml", "check"),
    ("lessons/llm/L07_sinh_van_ban.yaml", "example"),
    ("lessons/llm/L14_hanh_trinh_mo_rong.yaml", "stage5"),
    ("lessons/rln/L00_loi_nhuan_chiet_khau.yaml", "check"),
    ("lessons/rln/L03_ke_cuop_nhieu_tay.yaml", "example"),
    ("lessons/rln/L03_ke_cuop_nhieu_tay.yaml", "check"),
    ("lessons/rln/L04_monte_carlo_td.yaml", "check"),
    ("lessons/rln/L11_khai_thac_phan_thuong.yaml", "check"),
    ("lessons/rln/L13_hanh_trinh_atari.yaml", "stage5"),
    ("lessons/cvi/L00_anh_so.yaml", "formula"),
    ("lessons/cvi/L00_anh_so.yaml", "example"),
    ("lessons/cvi/L03_hieu_chuan_camera.yaml", "formula"),
    ("lessons/cvi/L05_ransac.yaml", "check"),
    ("lessons/cvi/L06_do_sau_hai_camera.yaml", "check"),
    ("lessons/cvi/L10_dich_chuyen_mien.yaml", "check"),
]
for path, sid in targets:
    d = yaml.safe_load(open(path, encoding="utf-8"))
    sc = next(s for s in d["scenes"] if s["id"] == sid)
    last = sc["steps"][-1]
    print(f"=== {path} [{sid}] focus={last.get('focus')} ===")
    print("SHOW:", str(last.get("show", "")).strip())
    print("SAY:", str(last.get("say", "")).strip())
