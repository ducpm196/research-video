import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(c - m, 3), round(c + m, 3)
k1, n1 = (int(x) for x in kv['a'].split(',')); k2, n2 = (int(x) for x in kv['b'].split(','))
print('A_3_3=', wilson(k1, n1), 'B_120_800=', wilson(k2, n2))
