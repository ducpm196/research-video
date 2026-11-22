seen_n, seen_cnt = 120, 75
unseen_n, unseen_cnt = 150, 30
is_observational = 1
obs_diff = (seen_cnt / seen_n) - (unseen_cnt / unseen_n)
print(f"obs_diff={obs_diff:.2f} needs_randomization={int(is_observational == 1)}")
