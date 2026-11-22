import math
mu, sig = 1.0, 2.0
kl = 0.5 * (sig ** 2 + mu ** 2 - 1.0 - math.log(sig ** 2))
p_real, p_fake = 0.25, 0.25
d_star = p_real / (p_real + p_fake)
gan_val = math.log(d_star) + math.log(1.0 - d_star)
print(f"vae_kl={kl:.4f}")
print(f"gan_nash_d={d_star:.2f} val={gan_val:.4f}")
