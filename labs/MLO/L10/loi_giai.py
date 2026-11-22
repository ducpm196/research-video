probs = [0.85, 0.70, 0.20, 0.40]
y = [1, 1, 0, 1]
brier = sum((p - t)**2 for p, t in zip(probs, y)) / len(y)
print(f"brier={brier:.4f}")
