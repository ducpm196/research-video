def pda(s):
    st, ph1 = [], False
    for ch in s:
        if ch == '0' and not ph1: st.append('0')
        elif ch == '1' and st: ph1 = True; st.pop()
        else: return False
    return not st
spec = lambda s: s == '0' * (len(s) // 2) + '1' * (len(s) // 2)
strs = [format(m, f'0{L}b') if L else ''
        for L in range(11) for m in range(1 << L)]
ok = all(pda(s) == spec(s) for s in strs)
print(f"tested={len(strs)} all_match={int(ok)}",
      f"ex_00001111={int(pda('00001111'))} ex_01010101={int(pda('01010101'))}")
