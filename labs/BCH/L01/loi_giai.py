import hashlib
h = lambda s: hashlib.sha256(s.encode()).hexdigest()[:10]
data = ["khối 0", "A->B 10", "B->C 4", "C->A 3"]
chain = []; p = "0" * 10
for d in data: p = h(f"{p}|{d}"); chain.append(p)
tampered = list(chain); p = chain[1]
for i in (2, 3):
    txt = "B->C 40" if i == 2 else data[i]
    p = h(f"{p}|{txt}"); tampered[i] = p
diff = sum(1 for a, b in zip(chain, tampered) if a != b)
print(f"orig_b2={chain[2]} tampered_b2={tampered[2]} broken_blocks={diff}")
