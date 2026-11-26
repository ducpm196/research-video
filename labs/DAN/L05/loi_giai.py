import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
s = [int(x) for x in kv['steps'].split(',')]; n2 = float(kv['new_s2'])
rates = [round(s[i + 1] / s[i] * 100, 1) for i in range(len(s) - 1)]; ov = s[-1] / s[0] * 100
proj = (rates[0] / 100) * n2 * (rates[2] / 100) * 100
print(f'step_pct={rates} overall={ov:.1f}% overall_step2_38={proj:.1f}%')
