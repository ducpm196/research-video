import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
a, b = kv['a'], kv['b']
steps, dec = 0, True
while b > 0:
    nxt = a % b
    dec = dec and (0 <= nxt < b)
    a, b = b, nxt
    steps += 1
print(f'gcd={a}')
print(f'steps={steps}')
print(f'strictly_decreasing={int(dec)}')
