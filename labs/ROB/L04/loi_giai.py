import sys
s = sys.stdin.read().strip() or "8 0.85 0.15|2,5"
hdr, ds = s.split("|")
ns, phs, pws = hdr.split()
N, ph, pw = int(ns), float(phs), float(pws)
doors = {int(x) for x in ds.split(",") if x}
bel = [(1.0 / N) * (ph if i in doors else pw) for i in range(N)]
tot = sum(bel)
bel = [b / tot for b in bel]
print(f"p_door2={bel[2]:.3f} p_wall0={bel[0]:.3f} sum={sum(bel):.1f}")
