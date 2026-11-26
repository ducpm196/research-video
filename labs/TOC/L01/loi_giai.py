import sys
s = sys.stdin.read().strip() or "5|1010 1011 1999"
ms, ws = s.split("|")
mod = int(ms); w1, w2, lims = ws.split(); lim = int(lims)
tbl = {(r, b): (2 * r + int(b)) % mod for r in range(mod) for b in ("0", "1")}
complete = all((r, b) in tbl for r in range(mod) for b in ("0", "1"))
def dfa_div(bits):
    st = 0
    for ch in bits: st = tbl[(st, ch)]
    return st == 0
ok = all(dfa_div(bin(n)[2:]) == (n % mod == 0) for n in range(1, lim + 1))
print(f"states={mod} complete={int(complete)} s1010={int(dfa_div(w1))} s1011={int(dfa_div(w2))} all_2000={int(ok)}")
