import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
hdr = kv['tcp'] + kv['ip'] + kv['eth']; frame = kv['payload'] + hdr
print(f'headers_B={hdr}')
print(f'frame_B={frame}')
print(f'efficiency_pct={100 * kv["payload"] / frame:.1f}%')
