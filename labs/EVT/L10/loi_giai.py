import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
print(f'seq_ms={kv["a"] + kv["b"] + kv["c"] + kv["d"]}')
print(f'critical_ms={kv["a"] + max(kv["b"], kv["c"]) + kv["d"]}')
