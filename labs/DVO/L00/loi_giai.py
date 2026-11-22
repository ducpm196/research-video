import math
lo, hi = 0, 299
while lo < hi:
    m = (lo + hi) // 2
    if m >= 187: hi = m
    else: lo = m + 1
print(f'bisect_steps_3={math.ceil(math.log2(3))}')
print(f'bisect_steps_300={math.ceil(math.log2(300))}')
print(f'found_bad_commit={lo}')
