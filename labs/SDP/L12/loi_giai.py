c1 = 0
def fn(n):
    global c1; c1 += 1
    return n if n < 2 else fn(n-1) + fn(n-2)
c2 = 0; memo = {}
def fm(n):
    global c2; c2 += 1
    if n in memo: return memo[n]
    memo[n] = n if n < 2 else fm(n-1) + fm(n-2); return memo[n]
res = fn(30); fm(30)
print(f'fib30={res}')
print(f'naive_calls={c1}')
print(f'memo_calls={c2}')
