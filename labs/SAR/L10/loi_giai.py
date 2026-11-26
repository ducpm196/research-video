import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
rtt = 2 * kv['one_way_ms']; loc = kv['local_ms']
print(f'sync_rtt_ms={rtt}\nlocal_async_ms={loc}\nlatency_ratio={rtt // loc}x')
