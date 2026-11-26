import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
drop = int(kv['hi_bps']) // int(kv['lo_bps'])
bdp_mb = int(10_000_000_000 * kv['rtt_ms'] // 1000) // (8 * 1_000_000)
bloat = (kv['bloat_pkts'] * kv['mss_B'] * 8) / (kv['bloat_mbps'] * 1_000_000)
print(f'collapse_1986_drop={drop}x')
print(f'bdp_10g_100ms_MB={bdp_mb}')
print(f'bufferbloat_s={bloat:.1f} quic_iw_B={int(kv["iw_pkts"] * 1200)}')
