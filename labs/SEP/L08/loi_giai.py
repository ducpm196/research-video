import sys
s = sys.stdin.read().strip() or "P1:2,2,1,-1;P2:1,1,2,0;P3:0,1,1,2"
plans = {}
for item in s.split(";"):
    k, vs = item.split(":")
    plans[k] = [int(x) for x in vs.split(",")]
safe = sorted(k for k, v in plans.items() if min(v) >= 0)
best = max(safe, key=lambda k: (sum(plans[k]), plans[k][-1]))
print(f"filtered={safe} fair_pick={best}")
