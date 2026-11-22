act, pred = [0, 15, 20, 9], [3, 14, 18, 12]
mae = sum(abs(a - p) for a, p in zip(act, pred)) / len(act)
has_zero = any(a == 0 for a in act)
print(f"mae={mae:.2f} mape_undefined={int(has_zero)}")
