import sys
n = int(sys.stdin.read().split('=')[1])
s, ok = 0, True
for i in range(n):
    ok = ok and (s == i * (i - 1) // 2)
    s += i
i = n
ok = ok and (s == i * (i - 1) // 2)
print(f'invariant_holds_all={int(ok)}')
print(f'final_i={i}')
print(f'final_sum={s}')
