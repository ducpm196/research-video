xs = sorted([2.0, 4.0, 6.0, 8.0, 9.0, 10.0, 12.0, 80.0])
n = len(xs)
mean_x = sum(xs) / n
med_x = (xs[n // 2 - 1] + xs[n // 2]) / 2.0
lo, hi = xs[:n // 2], xs[n // 2:]
q1 = (lo[len(lo) // 2 - 1] + lo[len(lo) // 2]) / 2.0
q3 = (hi[len(hi) // 2 - 1] + hi[len(hi) // 2]) / 2.0
fence = q3 + 1.5 * (q3 - q1)
print(f"mean={mean_x:.1f} median={med_x:.1f} fence={fence:.1f} outlier={int(max(xs) > fence)}")
