tx = 8000 / 1e9; rtt = 0.030
sw = tx / (rtt + tx)
bdp_pkts = round((1e9 * rtt) / 8000)
print(f'stop_wait_eff={sw:.5f}')
print(f'bdp_packets={bdp_pkts}')
print(f'w1000_eff={100 * 1000 / bdp_pkts:.1f}%')
