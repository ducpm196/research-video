from collections import Counter
raw = Counter(['vip'] * 400)
salted = Counter(f'vip#{i % 5}' for i in range(400))
print(f'raw_hot_max={max(raw.values())}')
print(f'salted_max={max(salted.values())}')
