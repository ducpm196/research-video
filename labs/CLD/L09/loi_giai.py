import random
def sim(p2c):
    r = random.Random(99); c = [0] * 50
    for _ in range(15_000):
        a = r.randrange(50)
        if p2c:
            b = r.randrange(50)
            if c[b] < c[a]: a = b
        c[a] += 1
    return max(c)
r1, r2 = sim(False), sim(True)
print(f'max_rand1={r1}')
print(f'max_p2c={r2}')
print(f'p2c_better={int(r2 < r1)}')
