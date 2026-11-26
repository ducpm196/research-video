"""Kiểm độc lập mọi khẳng định của PRJ: chạy thật mã mẫu trên màn hình, lab (kèm ca_an/) và đối chiếu checklib."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.path.insert(0, str(ROOT / "audit" / "prj"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402
import af2_kit as ak  # noqa: E402
import data  # noqa: E402
import screen_code as sc_mod  # noqa: E402

R = []
UPGRADED = {"L00", "L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09", "L10"}
BASH = r"C:\Program Files\Git\bin\bash.exe"
if not Path(BASH).exists():
    BASH = "bash"


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


def verify_yaml_code_pairs(lid: str, path: Path):
    _, blocks = sc_mod.blocks_of(path)
    pairs = []
    cur = []
    for sid, ti, bi, txt in blocks:
        if sid not in ("example", "check"):
            continue
        if txt.startswith("valid=") or txt.startswith("match=") or txt.startswith("same=") or txt.startswith("n=100000") or txt.startswith("res=") or txt.startswith("self=") or txt.startswith("matched=") or txt.startswith("merge_classify="):
            code = "\n".join(cur)
            out = ak.run_py(code)
            rec(lid, out == txt.strip("\n"), f"{sid} step {ti}: chạy thật Python khớp đầu ra")
            cur = []
            pairs.append((code, out))
        else:
            cur.append(txt)
    assert pairs, f"{lid}: không tìm thấy cặp mã-đầu ra nào"


for lid, fn in (
    ("L00", "L00_du_an_chang_1_cli_giao_dich.yaml"),
    ("L01", "L01_du_an_chang_2_but_toan_kep.yaml"),
    ("L02", "L02_du_an_chang_3_cong_tich_hop.yaml"),
    ("L03", "L03_du_an_chang_4_doi_soat_phong_van.yaml"),
):
    verify_yaml_code_pairs(lid, ROOT / "lessons" / "prj" / fn)

for cfg in data.lessons():
    lid = cfg["id"]
    if lid in UPGRADED:
        continue
    for pid, pinfo in cfg["progs"].items():
        out = ak.run_py(pinfo["code"], files=pinfo.get("files"))
        rec(lid, out == pinfo["expect"].strip("\n"), f"prog {pid}: chạy thật Python khớp đầu ra")

for cfg in data.lessons():
    lid = cfg["id"]
    if lid in UPGRADED:
        p = subprocess.run([BASH, str(ROOT / "labs" / "cham.sh"), "PRJ", lid], capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
        rec(lid, p.returncode == 0, f"lab {lid}: cham.sh (du_lieu.txt + ca_an/)")
    else:
        sol = (ROOT / "labs" / "PRJ" / lid / "loi_giai.py").read_text(encoding="utf-8")
        exp = (ROOT / "labs" / "PRJ" / lid / "mong_doi.txt").read_text(encoding="utf-8").strip("\n")
        rec(lid, ak.run_py(sol) == exp, f"lab {lid}: chạy thật Python khớp mong_doi.txt")

rec("PRJ:ALG00", alg.prj_csv_totals([("IN", 1000), ("OUT", 300), ("IN", 500), ("OUT", 200)]) == (2, 2, 1000), "CSV net=1000")
rec("PRJ:ALG01", alg.prj_double_entry_sum([("A", "B", 300), ("B", "C", 150), ("B", "FEE", 5)]) == 0, "bút toán kép Σ=0")
rec("PRJ:ALG02", alg.prj_idem_dedup([("k1", 400), ("k2", 500), ("k1", 400), ("k3", 300), ("k2", 500)]) == (3, 1200), "khử trùng 3 giao dịch")
rec("PRJ:ALG03", alg.prj_reconcile_3way(["t1", "t2", "t3", "t4"], ["t1", "t2", "t3", "t5"], ["t1", "t2", "t3", "t4"]) == (3, 2), "đối soát 3 bên (3, 2)")
rec("PRJ:ALG04", alg.prj_dijkstra_cost([("A", "D", 15), ("A", "B", 2), ("B", "C", 3), ("C", "D", 4)], "A", "D") == 9, "Dijkstra A->D = 9")

for lid in ("L05", "L06", "L07", "L08", "L09", "L10"):
    sol = (ROOT / "labs" / "PRJ" / lid / "loi_giai.py").read_text(encoding="utf-8")
    if lid == "L07":
        rec(lid, "state" in sol and "fails" in sol and "'cb_after_3fails=OPEN'" not in sol, "L07 CB dùng biến trạng thái thật (không hardcode)")
    if lid == "L09":
        ns = {}
        exec(sol, ns)
        rec(lid, ns["dfa"]("") == 0 and ns["dfa"]("ab") == 1 and ns["dfa"]("aba") == 0 and ns["dfa"]("axb") == 0, "L09 dfa() nhận đúng chuỗi {a,b}*ab")

bad = [c for c, ok in R if not ok]
print(f"\nverify_prj: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
