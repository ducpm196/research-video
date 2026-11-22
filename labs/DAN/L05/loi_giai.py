s = [8000, 3600, 1080, 270]
rates = [round(s[i+1]/s[i]*100, 1) for i in range(3)]
overall = s[-1] / s[0] * 100
proj = (rates[0] / 100) * 0.38 * (rates[2] / 100) * 100
print(f"step_pct={rates} overall={overall:.1f}% overall_step2_38={proj:.1f}%")
