left = [('M', 15), ('M', 25), ('M', 30)]
right = [('M', 'x'), ('M', 'y')]
joined = [(l, r) for kl, l in left for kr, r in right if kl == kr]
print(f"joined_rows={len(joined)} fake_sum={sum(x[0] for x in joined)}")
