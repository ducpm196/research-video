acc_old = 0.80 * 0.92 + 0.20 * 0.60
acc_dep = 0.40 * 0.92 + 0.60 * 0.60
print(f"test_overall={acc_old * 100:.1f}% deploy_real={acc_dep * 100:.1f}%")
