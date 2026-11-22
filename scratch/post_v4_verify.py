"""Update EVT L04 screen_code SHAs, sync CLD figs/tpl, lint all 26 edited YAMLs, run sync_tpl/screen_code/verify_*/layout_scan cleanly."""
import hashlib
import subprocess
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv/Scripts/python.exe")
sys.path.insert(0, str(ROOT / "audit" / "review"))
import screen_code as sc_mod  # noqa: E402

# 1. Regenerate CLD figs (latency_curve updated to 980x380 matching L10_hang_doi.yaml)
subprocess.run([PY, "-B", "audit/cld/figs.py"], cwd=ROOT, check=True)

# 2. Update EVT L04 screen_code SHAs and expect_stdout=max_replay=499
evt_blocks = sc_mod.all_blocks("EVT")
ev_yaml_p = ROOT / "audit/review/screen_code/EVT.yaml"
ev_txt = ev_yaml_p.read_text("utf-8")
ev_data = yaml.safe_load(ev_txt)
for key in ("EVT L04 practice 1 0", "EVT L04 practice 4 0"):
    txt = evt_blocks[key]
    new_sha = hashlib.sha256(txt.encode("utf-8")).hexdigest()[:16]
    old_sha = ev_data["blocks"][key]["sha"]
    if old_sha != new_sha:
        print(f"EVT SHA {key}: {old_sha} -> {new_sha}", flush=True)
        ev_txt = ev_txt.replace(f"sha: {old_sha}", f"sha: {new_sha}", 1)
if "max_replay=500" in ev_txt:
    ev_txt = ev_txt.replace("max_replay=500", "max_replay=499", 1)
ev_yaml_p.write_text(ev_txt, encoding="utf-8")

# 3. Lint all 26 edited lessons
EDITED = [
    "lessons/llm/L08_tinh_chinh.yaml",
    "lessons/rln/L10_phan_thuong_tu_nguoi.yaml",
    "lessons/evt/L00_su_kien_va_lenh.yaml",
    "lessons/evt/L01_luoc_do_su_kien.yaml",
    "lessons/evt/L04_ghi_nguon_su_kien.yaml",
    "lessons/mlo/L03_kiem_thu_he_ml.yaml",
    "lessons/mlo/L11_luong_tu_hoa.yaml",
    "lessons/clc/L03_dinh_danh_quyen.yaml",
    "lessons/clc/L05_may_ao_chi_phi.yaml",
    "lessons/clc/L06_ham_theo_su_kien.yaml",
    "lessons/clc/L07_csdl_duoc_quan_ly.yaml",
    "lessons/clc/L08_chi_phi.yaml",
    "lessons/clc/L10_khoi_phuc_tham_hoa.yaml",
    "lessons/clc/L12_hanh_trinh_luu_tru_doi_tuong.yaml",
    "lessons/sar/L04_bo_nho_dem.yaml",
    "lessons/sar/L06_do_san_sang.yaml",
    "lessons/sar/L08_hang_doi_bat_dong_bo.yaml",
    "lessons/sar/L09_luy_dang.yaml",
    "lessons/sar/L10_nhat_quan_da_vung.yaml",
    "lessons/sar/L12_thiet_ke_tong_hop.yaml",
    "lessons/sar/L13_hanh_trinh_twitter.yaml",
    "lessons/den/L00_hang_va_cot.yaml",
    "lessons/den/L02_khuech_dai.yaml",
    "lessons/den/L04_khoa_phan_vung.yaml",
    "lessons/den/L13_lo_va_chat_luong.yaml",
    "lessons/cld/L00_nguyen_khoi_vi_dich_vu.yaml",
    "lessons/cld/L01_container.yaml",
    "lessons/cld/L06_xep_lich_pod.yaml",
    "lessons/cld/L08_cap_nhat_cuon_chieu.yaml",
    "lessons/cld/L09_can_bang_tai.yaml",
]
for rel in EDITED:
    print(">>> LINT", rel, flush=True)
    subprocess.run([PY, "-B", "tools/lv.py", "lint", rel], cwd=ROOT, check=True)

# 4. sync_tpl & screen_code check
for c in ("LLM", "RLN", "EVT", "MLO", "CLC", "SAR", "DEN", "CLD"):
    print(">>> SYNC_TPL + SCREEN_CODE", c, flush=True)
    subprocess.run([PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"], cwd=ROOT, check=True)
    subprocess.run([PY, "-B", "audit/review/screen_code.py", "check", "--course", c], cwd=ROOT, check=True)

# 5. verify_*.py
for vscript in (
    "audit/llm/verify_llm.py",
    "audit/rln/verify_rln.py",
    "audit/evt/verify_evt.py",
    "audit/mlo/verify_mlo.py",
    "audit/clc/verify_clc.py",
    "audit/sar/verify_sar.py",
    "audit/den/verify_den.py",
    "audit/cld/verify_cld.py",
):
    print(">>> VERIFY", vscript, flush=True)
    subprocess.run([PY, "-B", vscript], cwd=ROOT, check=True)

# 6. Check all 114 Stage 8 + 42 LLM/RLN/CVI have 0 non-code ' vs '
import re
for d in ("llm", "rln", "cvi", "dan", "dsc", "mlo", "evt", "den", "cld", "clc", "sar"):
    for f in sorted((ROOT / "lessons" / d).glob("L*.yaml")):
        txt = f.read_text("utf-8")
        assert " vs " not in txt, f"FOUND ' vs ' in {f}"
    for f in sorted((ROOT / "labs" / d).glob("*/de.md")):
        txt = f.read_text("utf-8")
        assert " vs " not in txt, f"FOUND ' vs ' in {f}"
print(">>> 0 ' vs ' across all 11 courses verified!", flush=True)

# 7. Sequential layout_scan on touched Stage 8 & 9 courses
for c in ("LLM", "RLN", "DSC", "MLO", "EVT", "CLC", "SAR", "DEN", "CLD"):
    print(">>> LAYOUT_SCAN", c, flush=True)
    subprocess.run([PY, "-B", "-u", "audit/layout_scan.py", c], cwd=ROOT, check=True)
    tsv = ROOT / f"audit/layout_{c}.tsv"
    assert not tsv.read_text("utf-8").strip(), f"Layout errors in {c}"

print("POST_V4_VERIFY 100% PASS!", flush=True)
