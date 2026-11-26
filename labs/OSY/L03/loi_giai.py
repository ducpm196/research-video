import sys
from collections import deque
kv = dict(t.split('=') for t in sys.stdin.read().split())
b = [int(x) for x in kv['bursts'].split(',')]; q_sz = int(kv['q'])
n = len(b); rem = b[:]; fin = [0]*n; resp = [-1]*n; t = 0; q = deque(range(n))
while q:
    i = q.popleft()
    if resp[i] < 0: resp[i] = t
    d = min(q_sz, rem[i]); t += d; rem[i] -= d
    if rem[i] > 0: q.append(i)
    else: fin[i] = t
w = [fin[i] - b[i] for i in range(n)]
print('rr_waits=' + ','.join(map(str, w)))
print(f'rr_avg_wait={sum(w)/n:.2f}')
print('response_p1_p2_p3=' + ','.join(map(str, resp)))
