import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
p = kv['p_split']; a = kv['alpha']; v = int(kv['variants']); l = int(kv['looks'])
slow = 0.25 / (p * (1.0 - p)); fp1 = (1.0 - (1.0 - a) ** v) * 100; fp2 = (1.0 - (1.0 - a) ** (v * l)) * 100
print(f'split98_2_slow={slow:.2f}x fp4={fp1:.1f}% fp20={fp2:.1f}%')
