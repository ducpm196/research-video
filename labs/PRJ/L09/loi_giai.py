def dfa(s):
    st = 0
    for ch in s:
        if ch not in ('a', 'b'): return 0
        st = 1 if ch == 'a' else (2 if st == 1 else 0)
    return int(st == 2)
print(f'dfa_aaab={dfa("aaab")} dfa_aba={dfa("aba")}')
print(f'amdahl_8cores={1.0 / (0.10 + 0.90 / 8.0):.2f}')
print(f'amdahl_inf={1.0 / 0.10:.2f}')
