import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
done, dlq, pt = 0, [], 0
for msg in range(1, kv['total'] + 1):
    ok = False
    for _ in range(kv['retries']):
        if msg == kv['poison']: pt += 1
        else: ok = True; break
    if ok: done += 1
    else: dlq.append(msg)
print(f'processed={done}\ndlq={dlq}\npoison_attempts={pt}')
