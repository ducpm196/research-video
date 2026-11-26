import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
bn = min(int(x) for x in kv['links'].split(','))
rtt = int(kv['rtt_ms'])
bdp_b = bn * 1_000_000 * rtt // 1000
print(f'bottleneck_mbps={bn}')
print(f'bdp_bits={bdp_b}')
print(f'bdp_bytes={bdp_b // 8}')
