"""Sinh lại hình của NET rồi điền mọi tệp mẫu thành bài trong lessons/net/ (fill_tpl.py). Sửa mẫu hoặc hình thì chạy lại.
Chạy: .venv/Scripts/python audit/net/fill_all.py"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable
F = "audit/net/fig/"
JOBS = {
    "L01_cac_loai_tre": {"DELAY_SHORT": "delay_short.svg", "DELAY_REAL": "delay_real.svg"},
    "L03_phat_hien_loi": {"CRC_MAIN": "crc_main.html", "CRC_QUIZ": "crc_quiz.html"},
    "L07_trang_thai_lien_ket": {"RT_MAP": "rt_map.svg", "RT_TREE": "rt_tree.svg", "RT_QUIZ": "rt_quiz.svg"},
    "L08_vecto_khoang_cach": {"DV_LINE": "dv_line.svg", "DV_CUT": "dv_cut.svg"},
    "L09_tcp_udp_bat_tay": {"HANDSHAKE": "handshake.svg"},
    "L10_dung_cho_cua_so": {"STOPWAIT": "stopwait.svg"},
    "L11_tac_nghen_tcp": {"CWND_SS": "cwnd_ss.svg", "CWND_LOSS": "cwnd_loss.svg"},
    "L12_dns_http": {"DNS": "dns.svg"},
}
for gen in ("seq_svg.py", "cwnd_svg.py", "graph_figs.py", "crc_html.py"):
    subprocess.run([PY, f"audit/net/{gen}"], cwd=ROOT, check=True)
for stem, figs in JOBS.items():
    args = [f"{k}={F}{v}" for k, v in figs.items()]
    subprocess.run([PY, "audit/cs112/fill_tpl.py", f"audit/net/src/{stem}.tpl.yaml", f"lessons/net/{stem}.yaml", *args], cwd=ROOT, check=True)
