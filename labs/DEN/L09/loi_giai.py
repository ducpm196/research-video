lag_s, in_r, proc_r = 120, 8000, 24000
replay = lag_s * in_r
catchup = replay / (proc_r - in_r)
print(f'replay_events={replay}')
print(f'catchup_s={catchup:.1f}')
