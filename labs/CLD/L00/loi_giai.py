import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
n = kv['calls']; lms = n * kv['loc_ns'] * 1e-6; rms = n * kv['rpc_ms']
print(f'local_ms={lms:.3f}\nrpc_ms={rms:.1f}\nslowdown={round(rms / lms)}x')
