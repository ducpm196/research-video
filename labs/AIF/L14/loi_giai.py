theo = 480 * 2_500_000
eff = 126_000_000 / theo * 100.0
sim_s = 1600 / 0.4
draws = 1000 - 155 - 6
print(f"deepblue_eff={eff:.1f}% sim_rate={sim_s:.0f}/s az_draws={draws}")
