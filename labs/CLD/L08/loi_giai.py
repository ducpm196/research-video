import math
n, unavail_p, surge_p = 12, 0.25, 0.25
min_r = n - math.floor(n * unavail_p)
max_t = n + math.ceil(n * surge_p)
print(f'min_ready={min_r}')
print(f'max_total={max_t}')
