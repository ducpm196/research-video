nA, mA, nB, mB = 80, 40.0, 20, 190.0
naive = (mA + mB) / 2.0
weighted = (nA * mA + nB * mB) / (nA + nB)
print(f"naive={naive:.2f} weighted={weighted:.2f}")
