import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
sa, sb = float(kv['sa']), float(kv['sb']); rs = [float(x) for x in kv['rels'].split(',')]
l_ok = math.log1p(math.exp(-(sa - sb))); l_sw = math.log1p(math.exp(-(sb - sa)))
d12 = (rs[0] - rs[1]) * (1.0 / math.log2(2) - 1.0 / math.log2(3))
d34 = (rs[2] - rs[3]) * (1.0 / math.log2(4) - 1.0 / math.log2(5))
print(f'loss_ok={l_ok:.3f} loss_swap={l_sw:.3f}\ndcg_drop_12={d12:.3f} dcg_drop_34={d34:.3f}')
