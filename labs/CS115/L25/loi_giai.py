import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
w = [float(v) for v in kv['w'].split(',')]
x = [float(v) for v in kv['x'].split(',')]
b, y = float(kv['b']), float(kv['y'])
nw = math.hypot(*w); margin = 2.0 / nw
score = w[0] * x[0] + w[1] * x[1] + b
ypm = y * score; hinge = max(0.0, 1.0 - ypm)
print(f"norm_w={nw:.1f} margin={margin:.2f}")
print(f"y_pred_margin={ypm:.1f} hinge={hinge:.1f}")
