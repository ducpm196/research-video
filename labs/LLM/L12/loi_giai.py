import math
cos = lambda u, v: (
    sum(a * b for a, b in zip(u, v)) / (math.hypot(*u) * math.hypot(*v))
)
q, relevant = [2, 1, 0], 'docA'
docs = {'docA': [3, 2, 1], 'docB': [0, 1, 4]}
best = max(docs, key=lambda k: cos(q, docs[k]))
r1 = float(best == relevant)
print(f"top1={best} cos={cos(q, docs[best]):.3f} recall_at_1={r1:.1f}")
