from collections import Counter
vocab = {
    's t a r </w>': 7, 's t a r t </w>': 4,
    'c a r </w>': 3, 'f a r </w>': 2,
}
for step in (1, 2):
    pairs = Counter()
    for w, f in vocab.items():
        syms = w.split()
        for a, b in zip(syms, syms[1:]):
            pairs[(a, b)] += f
    best = max(pairs, key=pairs.__getitem__)
    print(f"merge{step}={best[0]}+{best[1]} freq={pairs[best]}")
    pair_s, merged_s = f"{best[0]} {best[1]}", "".join(best)
    vocab = {w.replace(pair_s, merged_s): f for w, f in vocab.items()}
