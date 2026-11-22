import math
w = (6.0, 8.0)
b = -1.0
nw = math.hypot(*w)
margin = 2.0 / nw
score = w[0] * 1 + w[1] * 1 + b
hinge = max(0.0, 1.0 - (-1.0) * score)
print(f"norm_w={nw:.1f} margin={margin:.2f}")
print(f"y_pred_margin={-score:.1f} hinge={hinge:.1f}")
