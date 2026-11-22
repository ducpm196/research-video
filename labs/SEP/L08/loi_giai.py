plans = {'P1': [2, 2, 1, -1], 'P2': [1, 1, 2, 0], 'P3': [0, 1, 1, 2]}
safe = sorted(k for k, v in plans.items() if min(v) >= 0)
best = max(safe, key=lambda k: (sum(plans[k]), plans[k][-1]))
print(f"filtered={safe} fair_pick={best}")
