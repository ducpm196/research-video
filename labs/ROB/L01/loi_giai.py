vl, vr, L = 0.6, 1.0, 0.8
v = (vr + vl) / 2.0
w = (vr - vl) / L
R = v / w
print(f"v={v:.1f}m/s omega={w:.1f}rad/s R={R:.2f}m")
