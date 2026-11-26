import math, sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
mu, sig, pr, pf = kv['mu'], kv['sig'], kv['pr'], kv['pf']
kl = 0.5 * (sig ** 2 + mu ** 2 - 1.0 - math.log(sig ** 2))
d_star = pr / (pr + pf)
gan_val = math.log(d_star) + math.log(1.0 - d_star)
print(f"vae_kl={kl:.4f}")
print(f"gan_nash_d={d_star:.2f} val={gan_val:.4f}")
