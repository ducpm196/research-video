import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
print(f'wait_no_inherit={kv["low_ms"] + kv["med_ms"]}ms wait_with_inherit={kv["low_ms"]}ms')
