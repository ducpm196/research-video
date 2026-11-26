import sys
s = sys.stdin.read().strip() or "0.25 0.5|10,30,50,70|512"
uv_s, c_s, sz_s = s.split("|")
u, v = map(float, uv_s.split())
c00, c10, c01, c11 = map(float, c_s.split(","))
sz = int(sz_s)
top = (1 - u)*c00 + u*c10
bot = (1 - u)*c01 + u*c11
bilerp = (1 - v)*top + v*bot
levels = sz.bit_length()
ratios = sum(0.25 ** k for k in range(1, levels))
print(f"bilerp={bilerp:.1f} levels={levels} mip_extra_ratio={ratios:.3f}")
