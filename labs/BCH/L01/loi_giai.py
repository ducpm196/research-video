import sys, hashlib
sys.stdin.reconfigure(encoding="utf-8")
s = sys.stdin.read().strip() or "2|khối 0;A->B 10;B->C 4;C->A 3|B->C 40"
idx_s, d_s, new_txt = s.split("|", 2)
idx = int(idx_s); data = d_s.split(";")
h = lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest()[:10]
chain = []; p = "0" * 10
for d in data: p = h(f"{p}|{d}"); chain.append(p)
tampered = list(chain); p = "0" * 10 if idx == 0 else chain[idx - 1]
for i in range(idx, len(data)):
    txt = new_txt if i == idx else data[i]
    p = h(f"{p}|{txt}"); tampered[i] = p
diff = sum(1 for a, b in zip(chain, tampered) if a != b)
print(f"orig_b2={chain[idx]} tampered_b2={tampered[idx]} broken_blocks={diff}")
