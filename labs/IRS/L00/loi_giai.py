hits = lambda ranks, k: sum(1 for r in ranks if r <= k)
ranks_a, ranks_b, total = [2, 4, 7], [3, 5, 8], 6
p5 = hits(ranks_a, 5) / 5
r5, r10 = hits(ranks_a, 5) / total, hits(ranks_a, 10) / total
p3_b = hits(ranks_b, 3) / 3
first_pos = [2, 4, None]
mrr = sum(0.0 if p is None else 1.0 / p
          for p in first_pos) / len(first_pos)
print(f"A_P5={p5:.1f} R5={r5:.1f} R10={r10:.1f} B_P3={p3_b:.1f}")
print(f"MRR_3={mrr:.4f}")
