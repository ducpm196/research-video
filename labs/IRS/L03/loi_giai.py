import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
N, c, pr = kv['N'], kv['clusters'], kv['probe']; ivf = c + pr * (N // c)
print(f'ivf_ops={ivf} speedup={N / ivf:.1f}x')
