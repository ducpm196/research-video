import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
b, sl, bmp, n = kv['base'], kv['slope'], kv['bump'], kv['days']
y = [b + sl * d + (bmp if d % 7 in (5, 6) else 0) for d in range(n)]
ma7 = [sum(y[i - 6:i + 1]) / 7.0 for i in range(6, n)]
diffs = [round(ma7[i + 1] - ma7[i], 2) for i in range(len(ma7) - 1)]
ok = int(all(abs(x - float(sl)) < 1e-6 for x in diffs))
print(f'ma7_diffs={diffs[:3]} constant_slope={ok}')
