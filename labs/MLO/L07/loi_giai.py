old_p = [0.2, 0.8, 0.6, 0.3, 0.9]
new_p = [0.3, 0.7, 0.4, 0.3, 0.8]
disagree = sum(int((a >= 0.5) != (b >= 0.5)) for a, b in zip(old_p, new_p))
print(f"served=old disagree={disagree}/5")
