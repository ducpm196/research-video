import math
dcg = lambda rels: sum(r / math.log2(i + 2) for i, r in enumerate(rels))
rels = [2, 3, 1, 2]
d = dcg(rels)
idcg = dcg(sorted(rels, reverse=True))
print(f"DCG={d:.5f} IDCG={idcg:.5f} nDCG={d/idcg:.5f}")
