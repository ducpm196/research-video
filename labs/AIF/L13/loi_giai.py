import math, sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
lf = kv['d_full'] * math.log10(kv['b']); d3 = kv['b'] ** kv['d_cut']; red = lf - kv['d_cut'] * math.log10(kv['b'])
print(f'log10_tree={lf:.1f} depth3_nodes={d3} log10_reduction={red:.1f}')
