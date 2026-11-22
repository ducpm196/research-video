schlick = lambda cos_t, F0=0.04: F0 + (1.0 - F0) * ((1.0 - cos_t) ** 5)
print(f"F0={schlick(1.0):.3f} F60={schlick(0.5):.3f} F84={schlick(0.1):.3f}")
