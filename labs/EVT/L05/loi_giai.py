w, p, t = 600, 450, 600
backlog = (w - p) * t
lag_s = backlog / w
drain_2 = backlog / (2 * p - w)
print(f'backlog={backlog}')
print(f'data_lag_s={lag_s:.1f}')
print(f'drain_with_2_s={drain_2:.1f}')
