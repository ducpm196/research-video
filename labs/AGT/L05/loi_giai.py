tp, fp = 0.55 * 0.85, 0.45 * 0.15
post = tp / (tp + fp) * 100
print(f"accepted_true_pct={post:.1f}%")
