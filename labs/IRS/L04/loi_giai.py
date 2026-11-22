rrf = lambda r1, r2, k=60: 1.0 / (k + r1) + 1.0 / (k + r2)
sa, sb = rrf(1, 4), rrf(2, 2)
print(f"score_A={sa:.5f} score_B={sb:.5f} win={'B' if sb > sa else 'A'}")
