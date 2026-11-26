import sys
s = sys.stdin.read().strip() or "90 10 25"
cg, cn, sn = map(int, s.split())
tr = [{"has_grass": True}] * cg + [{"has_grass": False}] * cn
snow = [{"has_grass": False}] * sn
acc = lambda ds: sum(1 for x in ds if x["has_grass"]) / len(ds) * 100.0
print(f"spur_train={acc(tr):.0f}% counterexample_snow={acc(snow):.0f}%")
