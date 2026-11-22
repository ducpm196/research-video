hist_days, speed = 20.0, 4.0
naive = hist_days / speed
real = hist_days / (speed - 1.0)
print(f'naive_days={naive:.1f}')
print(f'real_catchup_days={real:.1f}')
