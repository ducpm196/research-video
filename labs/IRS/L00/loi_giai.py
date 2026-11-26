import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
tot = int(kv['total']); ra = [int(x) for x in kv['ra'].split(',')]; rb = [int(x) for x in kv['rb'].split(',')]
fps = [int(x) for x in kv['first'].split(',')]
hits = lambda rs, k: sum(1 for r in rs if r <= k)
p5, r5, r10 = hits(ra, 5) / 5, hits(ra, 5) / tot, hits(ra, 10) / tot
p3b = hits(rb, 3) / 3; mrr = sum(0.0 if p <= 0 else 1.0 / p for p in fps) / len(fps)
print(f'A_P5={p5:.1f} R5={r5:.1f} R10={r10:.1f} B_P3={p3b:.1f}\nMRR_3={mrr:.4f}')
