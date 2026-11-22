def conf(b):
    return sum(
        b[i] == b[j] or abs(b[i] - b[j]) == j - i
        for i in range(4) for j in range(i + 1, 4)
    )
cur = [2, 2, 1, 3]; c0 = conf(cur)
while True:
    best_b, best_c = cur, conf(cur)
    for col in range(4):
        for row in range(4):
            cand = list(cur); cand[col] = row
            if conf(cand) < best_c: best_b, best_c = cand, conf(cand)
    if best_c == conf(cur): break
    cur = best_b
print(f"init_conflicts={c0} final_conflicts={conf(cur)} final_board={cur}")
