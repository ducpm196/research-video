import sys
cur = [int(x) for x in sys.stdin.read().strip().split('=')[1].split(',')]
def conf(b): return sum(b[i] == b[j] or abs(b[i] - b[j]) == j - i for i in range(4) for j in range(i + 1, 4))
c0 = conf(cur)
while True:
    bb, bc = cur, conf(cur)
    for col in range(4):
        for row in range(4):
            cand = list(cur); cand[col] = row
            if conf(cand) < bc: bb, bc = cand, conf(cand)
    if bc == conf(cur): break
    cur = bb
print(f'init_conflicts={c0} final_conflicts={conf(cur)} final_board={cur}')
