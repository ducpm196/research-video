import sys
s = sys.stdin.read().strip() or "10"
n = int(s); cnt = 0
for m in range(1 << n):
    bal, ok = 0, True
    for i in range(n):
        bal += 1 if (m >> i) & 1 else -1
        if bal < 0: ok = False; break
    if ok and bal == 0: cnt += 1
print(f"catalan_5={cnt}")
