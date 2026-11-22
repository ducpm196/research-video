ppv = lambda b: (b * 0.90) / (b * 0.90 + (1.0 - b) * 0.15)
pa, pb = round(ppv(0.40), 3), round(ppv(0.15), 3)
print(f"ppv_A={pa:.3f} ppv_B={pb:.3f} mismatch={int(pa != pb)}")
