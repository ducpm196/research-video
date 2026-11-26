import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
b = [int(x) for x in kv['bursts'].split(',')]
n = len(b); t = 0; fw = []
for x in b: fw.append(t); t += x
sw = [0] * n; t = 0
for i in sorted(range(n), key=lambda k: b[k]): sw[i] = t; t += b[i]
fa, sa = sum(fw) / n, sum(sw) / n
print('fcfs_waits=' + ','.join(map(str, fw)) + f' avg={fa:.2f}')
print('sjf_waits=' + ','.join(map(str, sw)) + f' avg={sa:.2f}')
print(f'wait_saved={fa - sa:.2f}')
