import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
cw, ss, st = kv['cwnd0'], kv['ssthresh'], kv['steps']
tr = [cw]
for _ in range(st):
    cw = cw * 2 if cw < ss else cw + 1
    tr.append(cw)
print('slowstart_trace=' + ','.join(map(str, tr[:-1])))
print(f'aimd_step1={tr[-1]}')
print(f'after_timeout_ssthresh={cw // 2} cwnd=1')
