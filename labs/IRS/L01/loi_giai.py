import math, sys
rels = [int(x) for x in sys.stdin.read().strip().split('=', 1)[1].split(',')]
dcg = lambda rs: sum(r / math.log2(i + 2) for i, r in enumerate(rs))
d, idcg = dcg(rels), dcg(sorted(rels, reverse=True))
print(f'DCG={d:.5f} IDCG={idcg:.5f} nDCG={d/idcg:.5f}')
