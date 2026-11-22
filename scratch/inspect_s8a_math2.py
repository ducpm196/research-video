import math
from pathlib import Path
ROOT = Path(r"D:\research-video")

def show_lines(path, a, b):
    print(f"=== {path} [{a}:{b}] ===")
    for i, ln in enumerate(path.read_text(encoding="utf-8").splitlines()[a-1:b], a):
        print(f"  {i}: {ln}")

def ab_n(p1, p2):
    pb = (p1 + p2) / 2.0
    za, zb = 1.959963984540054, 0.8416212335729143
    num = za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    return math.ceil((num / (p2 - p1)) ** 2)

show_lines(ROOT / "lessons/dan/L07_du_bao_co_so.yaml", 60, 82)
show_lines(ROOT / "lessons/dan/L07_du_bao_co_so.yaml", 258, 272)
show_lines(ROOT / "lessons/dsc/L08_thu_nghiem_ab.yaml", 280, 298)
show_lines(ROOT / "lessons/dsc/L15_hanh_trinh_netflix_prize.yaml", 328, 352)
show_lines(ROOT / "lessons/mlo/L07_phat_hanh_mo_hinh.yaml", 282, 298)
print("ab(0.10, 0.102) =", ab_n(0.10, 0.102))
print("ab(0.05, 0.06) =", ab_n(0.05, 0.06))
print("ab(0.10, 0.11) =", ab_n(0.10, 0.11))
