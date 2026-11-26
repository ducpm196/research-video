import sys
s = sys.stdin.read().strip() or "46|5,9,14,18,27|5,14,27"
ts, ss, cs = s.split("|")
T = int(ts)
S = [int(x) for x in ss.split(",")]
cert = [int(x) for x in cs.split(",")]
pool = list(S); in_S = True
for x in cert:
    if x in pool: pool.remove(x)
    else: in_S = False
tot = sum(cert)
print(f"cert_steps={len(cert)} verified={int(in_S and tot == T)} cert_sum={tot}")
