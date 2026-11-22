q = [98, 183, 37, 122, 14, 124, 65, 67]
fcfs = sum(abs(a - b) for a, b in zip([53] + q, q))
rem = q[:]; cur = 53; sstf = 0
while rem: nxt = min(rem, key=lambda x: abs(x - cur)); sstf += abs(nxt - cur); cur = nxt; rem.remove(nxt)
print(f'fcfs_tracks={fcfs}')
print(f'sstf_tracks={sstf}')
print(f'saved_pct={100 * (fcfs - sstf) / fcfs:.1f}%')
