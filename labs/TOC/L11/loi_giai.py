import sys
s = sys.stdin.read().strip() or "1,0,1;0,0,1;1,1,0"
rows = [[int(x) for x in r.split(",")] for r in s.split(";")]
k = len(rows); cands = 1 << k; matches = 0
for mask in range(cands):
    D = [(mask >> i) & 1 for i in range(k)]
    for idx, row in enumerate(rows):
        if D == row and D[idx] == (1 - row[idx]): matches += 1
print(f"table_size={k} candidates={cands} possible_matches={matches}")
