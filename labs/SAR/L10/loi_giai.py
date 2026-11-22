rtt, loc = 2 * 36, 3
print(f'sync_rtt_ms={rtt}')
print(f'local_async_ms={loc}')
print(f'latency_ratio={rtt // loc}x')
