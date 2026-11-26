import sys
sys.setrecursionlimit(10000)
n = int(sys.stdin.read().split('=')[1])
c1 = 0
def fn(k):
    global c1; c1 += 1
    return k if k < 2 else fn(k - 1) + fn(k - 2)
c2 = 0; memo = {}
def fm(k):
    global c2; c2 += 1
    if k in memo: return memo[k]
    memo[k] = k if k < 2 else fm(k - 1) + fm(k - 2)
    return memo[k]
res = fn(n); fm(n)
print(f'fib30={res}')
print(f'naive_calls={c1}')
print(f'memo_calls={c2}')
