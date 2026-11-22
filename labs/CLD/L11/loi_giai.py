p_slow, k = 0.015, 80
all_fast = (1.0 - p_slow) ** k
print(f'all_fast_pct={all_fast * 100:.1f}%')
print(f'slow_req_pct={(1.0 - all_fast) * 100:.1f}%')
