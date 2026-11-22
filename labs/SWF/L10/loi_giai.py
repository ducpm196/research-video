import math
d = [12.0 + (i % 5 - 2) * 0.5 for i in range(30)]; n = len(d)
m = sum(d) / n; sd = math.sqrt(sum((x - m)**2 for x in d) / (n - 1)); se = sd / math.sqrt(n); hw = 2.045 * se
print(f'n={n} mean={m:.2f}')
print(f'sd={sd:.3f} se={se:.3f}')
print(f'ci95={m-hw:.2f},{m+hw:.2f}')
