models = [
    (a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)
    if ((not a or b) and (b or c) and (not c))
]
entails_b = all(b == 1 for _, b, _ in models)
print(f"kb_models={len(models)} entails_B={int(entails_b)}")
