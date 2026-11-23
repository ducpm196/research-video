"""AF5 — số liệu theo chặng/lớp bài từ mech_scan.tsv + pack.stages (chỉ đọc)."""
import csv, pathlib, sys, collections
ROOT = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "audit/review/learn_start"))
sys.stdout.reconfigure(encoding="utf-8")
import pack
rows = {(r["course"], r["id"]): r for r in csv.DictReader(open(pathlib.Path(__file__).parent / "mech_scan.tsv", encoding="utf-8"), delimiter="\t")}
cur = pack.load_cur()
tot = collections.Counter()
print(f"{'chặng':<5}{'bài':>5}{'giờ':>7}{'prGEN':>7}{'đề lộ ĐA':>9}{'<9p':>5}{'>16p':>6}  khoá")
for sid, name, _lv, _intro, items in pack.stages(cur):
    n = gen = leak = sh = lg = 0; mins = 0.0; cs = []
    for c, l in items:
        r = rows[(c, l["id"])]
        n += 1; mins += float(r["dur_min"]); gen += r["pr_generic"] == "True"; leak += r["de_leaks_answers"] == "True"
        sh += float(r["dur_min"]) < 9; lg += float(r["dur_min"]) > 16
        if c not in cs: cs.append(c)
    print(f"{sid:<5}{n:>5}{mins/60:>7.1f}{gen:>7}{leak:>9}{sh:>5}{lg:>6}  {' '.join(cs)}")
    tot.update(n=n, gen=gen, leak=leak, sh=sh, lg=lg); tot["mins"] += mins
print("TỔNG", dict(tot))
HAND = {"FND", "JVA", "JV2", "PYT", "BNK", "BNX", "INT", "ACB", "DMS", "CS112"}
NEW = {"CPR", "LNX", "MLP", "PRJ"}
cls = collections.defaultdict(lambda: collections.Counter())
for (c, l), r in rows.items():
    k = "A_tay(ch.1-5)" if c in HAND or (c == "CS115" and r["pr_generic"] != "True") else "B_khoa_moi" if c in NEW else "C_nang_hang_loat"
    cls[k].update(n=1, gen=r["pr_generic"] == "True", leak=r["de_leaks_answers"] == "True", short=float(r["dur_min"]) < 9, long=float(r["dur_min"]) > 16)
    cls[k]["mins"] += float(r["dur_min"])
for k in sorted(cls): print(k, {a: (round(b / 60, 1) if a == "mins" else b) for a, b in cls[k].items()})
