import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
p1, p2 = kv['p1'], kv['p2']
p1 += 1; msg1 = p1
p2 = max(p2, msg1) + 1; recv2 = p2
p2 += 1; p1 = max(p1, p2) + 1
print(f'p2_recv={recv2}')
print(f'p2_next={p2}')
print(f'p1_recv_back={p1}')
