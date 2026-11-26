import sys
s = sys.stdin.read().strip() or "32|10,12,10"
ws, bs = s.split("|")
warp = int(ws); branches = [int(x) for x in bs.split(",")]
eff = sum(branches) / (len(branches) * warp) * 100.0
print(f"warp_eff_diverged={eff:.0f}%")
