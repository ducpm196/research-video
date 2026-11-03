"""Sinh lại hình (figs.py) rồi điền mọi tệp mẫu của RBM thành bài trong lessons/rbm/ (fill_tpl.py, mỗi {{TÊN}} = một hình một dòng).
Chạy: .venv/Scripts/python audit/rbm/fill_all.py — sửa mẫu hoặc hình thì chạy lại, không sửa tay tệp bài sinh ra."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable
F = "audit/rbm/fig/"
JOBS = {
    "L00_phep_quay_2d": {"ROT90": "rot90", "ROT30": "rot30"},
    "L01_quay_3d_euler": {"ORDER3D": "order3d"},
    "L03_toa_do_thuan_nhat": {"ORDER": "order"},
    "L04_dong_hoc_thuan": {"FK": "fk"},
    "L05_dong_hoc_nguoc": {"IK": "ik", "REACH": "reach"},
    "L06_jacobian_ky_di": {"SING": "sing"},
    "L07_ode_euler": {"EULER": "euler"},
    "L09_he_tuyen_tinh_on_dinh": {"RESP": "resp"},
    "L10_dieu_khien_pid": {"PID": "pid"},
    "L11_roi_rac_on_dinh_so": {"STEPS": "steps"},
    "L12_kalman_1d": {"FUSE": "fuse"},
    "L13_kalman_nhieu_chieu": {"ELLIPSE": "ellipse"},
    "L14_lay_mau_chong_pho": {"ALIAS": "alias", "DFT": "dft"},
    "L15_a_sao": {"GRID0": "grid0", "GRID": "grid"},
    "L16_hieu_chuan_cam_bien": {"FIT": "fit"},
}
subprocess.run([PY, "audit/rbm/figs.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
for stem, figs in JOBS.items():
    args = [f"{k}={F}{v}.svg" for k, v in figs.items()]
    subprocess.run([PY, "audit/cs112/fill_tpl.py", f"audit/rbm/src/{stem}.tpl.yaml", f"lessons/rbm/{stem}.yaml", *args], cwd=ROOT, check=True)
