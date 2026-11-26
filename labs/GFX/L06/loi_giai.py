import sys
s = sys.stdin.read().strip() or "0.0,0.6,0.8|0.0,0.8,0.6|0.95 64 128"
ns, ls, ss = s.split("|")
n = tuple(map(float, ns.split(",")))
l = tuple(map(float, ls.split(",")))
bs, s1, s2 = ss.split()
base, p1, p2 = float(bs), int(s1), int(s2)
ndotl = max(0.0, sum(a*b for a, b in zip(n, l)))
print(f"diffuse={ndotl:.2f} spec_s64={base**p1:.4f} spec_s128={base**p2:.4f}")
