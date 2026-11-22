import random
ids = list(range(12))
s7a = random.Random(7).sample(ids, 5)
s7b = random.Random(7).sample(ids, 5)
s9 = random.Random(9).sample(ids, 5)
print(f"same_seed={int(s7a==s7b)} diff_seed={int(s7a!=s9)} s7={s7a}")
