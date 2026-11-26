import sys
s = sys.stdin.read().strip() or "10|00001111|01010101"
ls, w1, w2 = s.split("|"); max_l = int(ls)
def pda(w):
    st, ph1 = [], False
    for ch in w:
        if ch == "0" and not ph1: st.append("0")
        elif ch == "1" and st: ph1 = True; st.pop()
        else: return False
    return not st
spec = lambda w: w == "0" * (len(w) // 2) + "1" * (len(w) // 2)
strs = [format(m, f"0{L}b") if L else "" for L in range(max_l + 1) for m in range(1 << L)]
ok = all(pda(w) == spec(w) for w in strs)
print(f"tested={len(strs)} all_match={int(ok)} ex_00001111={int(pda(w1))} ex_01010101={int(pda(w2))}")
