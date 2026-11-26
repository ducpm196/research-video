import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
def safe_hb(claimed, actual): return 0 <= claimed <= actual
ok = safe_hb(kv['claimed'], kv['actual'])
leaked = max(0, kv['claimed'] - kv['actual'])
print(f'max_u16_bytes={2 ** kv["bits"]}')
print(f'leaked_bytes={leaked}')
print(f'safe_check_rejected={int(not ok)}')
