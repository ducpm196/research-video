cap, per = 1000, 300
d4 = 4 * per; d3 = 3 * per
print(f'demand_4procs={d4} thrashing={int(d4 > cap)}')
print(f'demand_after_suspend={d3} thrashing={int(d3 > cap)}')
print(f'free_frames_after={cap - d3}')
