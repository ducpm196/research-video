n = 20_000
loc_ms = n * 15e-6
rpc_ms = n * 1.5
print(f'local_ms={loc_ms:.3f}')
print(f'rpc_ms={rpc_ms:.1f}')
print(f'slowdown={round(rpc_ms / loc_ms)}x')
