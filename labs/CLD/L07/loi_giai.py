import math, sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
def hpa(cur, cpu, tgt, tol):
    return int(cur) if abs(cpu / tgt - 1.0) <= tol else math.ceil(cur * cpu / tgt)
print(f'replicas_at_84={hpa(kv["cur"], kv["cpu1"], kv["tgt"], kv["tol"])}')
print(f'replicas_at_64={hpa(kv["cur"], kv["cpu2"], kv["tgt"], kv["tol"])}')
