import sys
s = sys.stdin.read().strip() or "0.002 500000 0.05 2000 500"
pa, da, pb, db, fl = map(float, s.split())
exp_a = pa * da
exp_b = pb * db
p_fleet = 1.0 - (1.0 - pa) ** int(fl)
print(f"exp_A={exp_a:.0f} exp_B={exp_b:.0f} fleet_prob={p_fleet:.4f}")
