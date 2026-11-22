tbl = {(r, b): (2 * r + int(b)) % 5
       for r in range(5) for b in ('0', '1')}
complete = all((r, b) in tbl for r in range(5) for b in ('0', '1'))
def dfa_div5(bits):
    s = 0
    for ch in bits: s = tbl[(s, ch)]
    return s == 0
ok = all(dfa_div5(bin(n)[2:]) == (n % 5 == 0) for n in range(1, 2000))
print(f"states=5 complete={int(complete)}",
      f"s1010={int(dfa_div5('1010'))}",
      f"s1011={int(dfa_div5('1011'))} all_2000={int(ok)}")
