import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
tok, tot, acc = kv['cap'], kv['total'], 0
for s in range(kv['secs']):
    if s > 0: tok = min(kv['cap'], tok + kv['rate'])
    take = min(tok, tot - acc, kv['burst'] if s > 0 else tok)
    acc += take; tok -= take
rej = tot - acc
print(f'accepted={acc}\nrejected={rej}\naccept_pct={100 * acc / tot:.2f}%')
