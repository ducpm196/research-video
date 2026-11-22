import math
xs = sorted([200, 204, 196, 202, 198, 206, 200, 900])
mean = sum(xs) / len(xs)
sd_pop = math.sqrt(sum((x - mean)**2 for x in xs) / len(xs))
med = (xs[3] + xs[4]) / 2.0
mad_list = sorted(abs(x - med) for x in xs)
norm_mad = 1.4826 * (mad_list[3] + mad_list[4]) / 2.0
print(f"z_classical={(900-mean)/sd_pop:.2f} z_robust={(900-med)/norm_mad:.1f}")
