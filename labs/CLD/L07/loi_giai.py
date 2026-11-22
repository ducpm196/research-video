import math
def hpa(cur, cpu, tgt=60, tol=0.10):
    if abs(cpu / tgt - 1.0) <= tol: return cur
    return math.ceil(cur * cpu / tgt)
print(f'replicas_at_84={hpa(6, 84)}')
print(f'replicas_at_64={hpa(6, 64)}')
