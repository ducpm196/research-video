rows = [[1, 0, 1], [0, 0, 1], [1, 1, 0]]
matches = 0
for mask in range(8):
    D = [(mask >> i) & 1 for i in range(3)]
    for idx, row in enumerate(rows):
        if D == row and D[idx] == (1 - row[idx]):
            matches += 1
print(f"table_size=3 candidates=8 possible_matches={matches}")
