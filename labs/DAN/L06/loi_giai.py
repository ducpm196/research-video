y = [20 + 3*d + (35 if d % 7 in (5, 6) else 0) for d in range(14)]
ma7 = [sum(y[i-6:i+1]) / 7.0 for i in range(6, 14)]
diffs = [round(ma7[i+1] - ma7[i], 2) for i in range(len(ma7)-1)]
ok = int(all(x == 3.0 for x in diffs))
print(f"ma7_diffs={diffs[:3]} constant_slope={ok}")
