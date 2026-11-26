import sys
s = sys.stdin.read().strip() or "16|4,8;2,4"
ms_s, t_s = s.split("|")
H = int(ms_s)
tasks = [tuple(map(int, x.split(","))) for x in t_s.split(";") if x]
def sim(edf):
    rem, dl, misses = [0]*len(tasks), [0]*len(tasks), 0
    for t in range(H):
        for i, (c, p) in enumerate(tasks):
            if t % p == 0:
                if rem[i] > 0: misses += 1
                rem[i] = c; dl[i] = t + p
        ready = [i for i in range(len(tasks)) if rem[i] > 0]
        if ready:
            pick = min(ready, key=lambda i: dl[i]) if edf else ready[0]
            rem[pick] -= 1
    return misses + sum(1 for r in rem if r > 0)
u = sum(c / p for c, p in tasks)
print(f"U={u:.1f} fixed_misses={sim(False)} edf_misses={sim(True)}")
