valid = []
for m in range(1 << 10):
    s = ''.join('(' if (m >> i) & 1 else ')' for i in range(10))
    bal, ok = 0, True
    for ch in s:
        bal += 1 if ch == '(' else -1
        if bal < 0:
            ok = False; break
    if ok and bal == 0:
        valid.append(s)
print(f"catalan_5={len(valid)}")
