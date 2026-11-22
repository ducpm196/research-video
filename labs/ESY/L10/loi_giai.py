def sim(edf):
    rem, dl, misses = [0, 0], [0, 0], 0
    for t in range(16):
        for i, (c, p) in enumerate(((4, 8), (2, 4))):
            if t % p == 0:
                if rem[i] > 0: misses += 1
                rem[i] = c; dl[i] = t + p
        ready = [i for i in (0, 1) if rem[i] > 0]
        if ready:
            pick = min(ready, key=lambda i: dl[i]) if edf else ready[0]
            rem[pick] -= 1
    return misses + sum(1 for r in rem if r > 0)
u = 4/8 + 2/4
print(f"U={u:.1f} fixed_misses={sim(False)} edf_misses={sim(True)}")
