clicks = [2, 2, 2, 2, 2]
for _ in range(8):
    top2 = sorted(range(5), key=lambda i: (-clicks[i], i))[:2]
    for i in top2: clicks[i] += 3
share = sum(sorted(clicks, reverse=True)[:2]) / sum(clicks) * 100
print(f"clicks={clicks} top2_share={share:.1f}%")
