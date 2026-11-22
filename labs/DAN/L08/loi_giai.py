rev = [800, 300, 150, 90, 80, 70, 50, 30, 20, 10]
mean_v = sum(rev) / len(rev)
med_v = (rev[4] + rev[5]) / 2.0
top20_share = sum(rev[:2]) / sum(rev) * 100
print(f"mean={mean_v:.1f} median={med_v:.1f} top20={top20_share:.1f}%")
