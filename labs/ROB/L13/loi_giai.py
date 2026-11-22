stop_d = lambda mph: (v := mph * 0.44704) * 0.2 + (v ** 2) / 8.0
miles_2004 = 0.05 * 142
miles_2005 = 132
ratio_dist = stop_d(30.0) / stop_d(20.0)
print(f"mi_2004={miles_2004:.1f} mi_2005={miles_2005} stop_ratio={ratio_dist:.2f}x")
