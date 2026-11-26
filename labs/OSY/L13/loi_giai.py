import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
head = int(kv['head']); q = [int(x) for x in kv['queue'].split(',')]
fcfs = sum(abs(a - b) for a, b in zip([head] + q, q))
rem = q[:]; cur = head; sstf = 0
while rem:
    nxt = min(rem, key=lambda x: abs(x - cur))
    sstf += abs(nxt - cur); cur = nxt; rem.remove(nxt)
print(f'fcfs_tracks={fcfs}')
print(f'sstf_tracks={sstf}')
print(f'saved_pct={100 * (fcfs - sstf) / fcfs:.1f}%')
