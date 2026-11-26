import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
tx = kv['pkt_bits'] / kv['bw_bps']; rtt = kv['rtt_s']
sw = tx / (rtt + tx)
bdp_pkts = round((kv['bw_bps'] * rtt) / kv['pkt_bits'])
print(f'stop_wait_eff={sw:.5f}')
print(f'bdp_packets={bdp_pkts}')
print(f'w1000_eff={min(100.0, 100 * kv["win"] / bdp_pkts):.1f}%')
