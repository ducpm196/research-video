import random
rng = random.Random(7)
n_m, n_s = 150, 80
best_val = max(sum(rng.random() < 0.5 for _ in range(n_s)) / n_s
               for _ in range(n_m))
print(f"true_skill=0.50 best_lucky_val={best_val:.2f}")
